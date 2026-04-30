#!/usr/bin/env python3
"""
inject_titles.py
================

Dodaje `title:` field u YAML frontmatter svakog markdown fajla, na osnovu
naslova Confluence stranice koja je referencirana preko `confluence_page_id`.

Razlog: nakon što markdown_cleanup.py ukloni redundantni H1 heading, md2conf
više ne može izvući title iz sadržaja — pa pada nazad na default koji
duplicira između fajlova. Eksplicitni `title:` u frontmatter-u rješava to
trajno.

Strategija:
- Za svaki markdown fajl koji ima `confluence_page_id` u frontmatter-u:
  - Dohvati title sa Confluence-a (jedan API poziv po fajlu)
  - Upiši ga u frontmatter kao `title: "..."` odmah ispod confluence_page_id
  - Ako title već postoji, preskoči (osim sa --update)
- Idempotentno: drugi run preskače sve fajlove koji već imaju title
- Default je dry-run

Pokretanje:
    python inject_titles.py            # dry-run
    python inject_titles.py --apply    # pravi izmjene
    python inject_titles.py --apply -v # detalji
    python inject_titles.py --apply --update  # azuriraj postojeci title

Preduslov:
    pip install requests
    ATLASSIAN_EMAIL i ATLASSIAN_API_TOKEN environment varijable
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

import requests
from requests.auth import HTTPBasicAuth


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = SCRIPT_DIR.parent

CLOUD_ID = "45983047-331b-459e-b1a5-052825171c8c"
CONFLUENCE_API_BASE = (
    f"https://api.atlassian.com/ex/confluence/{CLOUD_ID}/wiki/api/v2"
)

EXCLUDED_TOP_DIRS = {
    ".venv", ".git", "jira-sync", "md2conf-tooling", "node_modules",
    ".claude", ".vscode",
}
EXCLUDED_FILENAMES = {
    "audit-report.md",
    "CLAUDE.md",
    "CLAUDE-13-to-12.md",
    "cityinfo-epics-stories-instructions.md",
    "README.md",
    "pisanje-epica-i-user-storija-instrukcija.md",
    "plan-pisanja-epica-i-storija.md",
}

FRONTMATTER_DELIM = "---"
PAGE_ID_LINE_RE = re.compile(
    r'^(?P<indent>\s*)confluence_page_id\s*:\s*"?(?P<value>[^"\s]+?)"?\s*$'
)
TITLE_LINE_RE = re.compile(
    r'^(?P<indent>\s*)title\s*:\s*"?(?P<value>.+?)"?\s*$'
)


# --------------------------------------------------------------------------
# Auth
# --------------------------------------------------------------------------

def get_auth() -> HTTPBasicAuth:
    email = os.environ.get("ATLASSIAN_EMAIL")
    token = os.environ.get("ATLASSIAN_API_TOKEN")
    if not email or not token:
        sys.exit(
            "GREŠKA: postavi ATLASSIAN_EMAIL i ATLASSIAN_API_TOKEN environment "
            "varijable prije pokretanja skripte."
        )
    return HTTPBasicAuth(email, token)


# Cache za page title-ove (da ne dohvaćamo isti page više puta)
_title_cache: dict[str, str] = {}


def fetch_page_title(page_id: str, auth: HTTPBasicAuth) -> str | None:
    """Vrati title Confluence stranice sa datim ID-om, ili None ako greška."""
    if page_id in _title_cache:
        return _title_cache[page_id]

    url = f"{CONFLUENCE_API_BASE}/pages/{page_id}"
    try:
        resp = requests.get(url, auth=auth, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        title = data.get("title")
        if title:
            _title_cache[page_id] = title
        return title
    except Exception as e:
        print(f"  WARN: ne mogu dohvatiti title za page {page_id}: {e}", file=sys.stderr)
        return None


# --------------------------------------------------------------------------
# Frontmatter manipulation
# --------------------------------------------------------------------------

def split_frontmatter(content: str) -> tuple[list[str] | None, str]:
    lines = content.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != FRONTMATTER_DELIM:
        return None, content
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r\n") == FRONTMATTER_DELIM:
            end_idx = i
            break
    if end_idx is None:
        return None, content
    return lines[1:end_idx], "".join(lines[end_idx:])


def find_page_id_line(frontmatter_lines: list[str]) -> tuple[int, str] | None:
    for i, line in enumerate(frontmatter_lines):
        m = PAGE_ID_LINE_RE.match(line)
        if m:
            return (i, m.group("value").strip())
    return None


def find_title_line(frontmatter_lines: list[str]) -> tuple[int, str] | None:
    for i, line in enumerate(frontmatter_lines):
        m = TITLE_LINE_RE.match(line)
        if m:
            return (i, m.group("value").strip().strip('"').strip("'"))
    return None


def inject_title(
    frontmatter_lines: list[str],
    title: str,
    update_existing: bool = False,
) -> tuple[list[str], str]:
    """
    Vrati (nove_linije, status):
        "added"            — novi title dodan
        "skipped_existing" — title već postoji, nije ažuriran
        "updated"          — title ažuriran (sa --update)
        "no_page_id"       — nema confluence_page_id, ne znamo gdje da ubacimo
    """
    existing_title = find_title_line(frontmatter_lines)
    if existing_title is not None:
        idx, current = existing_title
        if current == title:
            return frontmatter_lines, "skipped_existing"
        if not update_existing:
            return frontmatter_lines, "skipped_existing"
        # Ažuriraj
        old_line = frontmatter_lines[idx]
        m = TITLE_LINE_RE.match(old_line)
        indent = m.group("indent") if m else ""
        ending = "\r\n" if old_line.endswith("\r\n") else ("\n" if old_line.endswith("\n") else "\n")
        new_line = f'{indent}title: "{title}"{ending}'
        new_lines = list(frontmatter_lines)
        new_lines[idx] = new_line
        return new_lines, "updated"

    # Nema title — ubaci ga odmah ispod confluence_page_id linije
    pid = find_page_id_line(frontmatter_lines)
    if pid is None:
        return frontmatter_lines, "no_page_id"

    pid_idx, _ = pid
    pid_line = frontmatter_lines[pid_idx]
    m = PAGE_ID_LINE_RE.match(pid_line)
    indent = m.group("indent") if m else ""
    ending = "\r\n" if pid_line.endswith("\r\n") else ("\n" if pid_line.endswith("\n") else "\n")

    # Escape any " in title
    safe_title = title.replace('"', '\\"')
    new_line = f'{indent}title: "{safe_title}"{ending}'
    new_lines = list(frontmatter_lines)
    new_lines.insert(pid_idx + 1, new_line)
    return new_lines, "added"


def reassemble(frontmatter_lines: list[str], rest: str, original: str) -> str:
    delim_line = "---\r\n" if original.startswith("---\r\n") else "---\n"
    return delim_line + "".join(frontmatter_lines) + rest


# --------------------------------------------------------------------------
# Glavna logika
# --------------------------------------------------------------------------

@dataclass
class FileResult:
    path: Path
    status: str
    detail: str = ""


@dataclass
class Summary:
    added: list[FileResult] = field(default_factory=list)
    updated: list[FileResult] = field(default_factory=list)
    skipped_existing: list[FileResult] = field(default_factory=list)
    no_page_id: list[FileResult] = field(default_factory=list)
    no_frontmatter: list[FileResult] = field(default_factory=list)
    api_error: list[FileResult] = field(default_factory=list)
    error: list[FileResult] = field(default_factory=list)


def iter_target_files(repo_root: Path) -> list[Path]:
    results = []
    for p in repo_root.rglob("*.md"):
        rel = p.relative_to(repo_root)
        if rel.parts and rel.parts[0] in EXCLUDED_TOP_DIRS:
            continue
        if p.name in EXCLUDED_FILENAMES:
            continue
        results.append(p)
    return sorted(results)


def process_file(
    path: Path,
    repo_root: Path,
    auth: HTTPBasicAuth,
    apply_changes: bool,
    update_existing: bool,
) -> FileResult:
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return FileResult(path, "error", f"read error: {e}")

    fm_lines, rest = split_frontmatter(content)
    if fm_lines is None:
        return FileResult(path, "no_frontmatter", "")

    pid = find_page_id_line(fm_lines)
    if pid is None:
        return FileResult(path, "no_page_id", "")

    _, page_id = pid

    # Provjeri da li već ima title — ako da i nije --update, nemoj ni zvati API
    existing = find_title_line(fm_lines)
    if existing and not update_existing:
        return FileResult(path, "skipped_existing", f"title='{existing[1]}'")

    # Dohvati title sa Confluence-a
    title = fetch_page_title(page_id, auth)
    if not title:
        return FileResult(path, "api_error", f"failed to fetch title for page {page_id}")

    new_fm_lines, op_status = inject_title(fm_lines, title, update_existing)

    if op_status == "skipped_existing":
        return FileResult(path, "skipped_existing", f"title='{title}'")
    if op_status == "no_page_id":
        return FileResult(path, "no_page_id", "")

    # added or updated
    if apply_changes:
        new_content = reassemble(new_fm_lines, rest, content)
        try:
            path.write_text(new_content, encoding="utf-8", newline="")
        except Exception as e:
            return FileResult(path, "error", f"write error: {e}")

    return FileResult(path, op_status, f"title='{title}'")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--root", type=Path, default=DEFAULT_REPO_ROOT)
    parser.add_argument("--apply", action="store_true", help="Pravi stvarne izmjene.")
    parser.add_argument("--update", action="store_true", help="Ažuriraj postojeći title.")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    repo_root = args.root.resolve()
    auth = get_auth()
    mode = "APPLY" if args.apply else "DRY-RUN"

    print(f"=== inject_titles.py — {mode} ===")
    print(f"Repo root: {repo_root}")
    if args.update:
        print("Update mode: postojeći title će biti ažuriran")
    print()

    files = iter_target_files(repo_root)
    print(f"Pronađeno {len(files)} markdown fajlova.\n")

    summary = Summary()
    for i, f in enumerate(files):
        r = process_file(f, repo_root, auth, args.apply, args.update)
        getattr(summary, r.status).append(r)
        if args.verbose:
            rel = r.path.relative_to(repo_root)
            print(f"  [{r.status:18s}] {rel}  {r.detail}")
        # Mali rate limit hedging — Confluence API može throttle pri burst-u
        if r.status in ("added", "updated"):
            time.sleep(0.15)

    print("\n=== REZULTAT ===")
    print(f"  Title dodano:                {len(summary.added)}")
    print(f"  Title ažurirano:             {len(summary.updated)}")
    print(f"  Preskočeno (već postoji):    {len(summary.skipped_existing)}")
    print(f"  Bez confluence_page_id:      {len(summary.no_page_id)}")
    print(f"  Bez frontmatter-a:           {len(summary.no_frontmatter)}")
    print(f"  API greške:                  {len(summary.api_error)}")
    print(f"  Greške:                      {len(summary.error)}")

    if summary.api_error:
        print("\n--- API GREŠKE ---")
        for r in summary.api_error:
            print(f"  {r.path.relative_to(repo_root)}: {r.detail}")
    if summary.error:
        print("\n--- GREŠKE ---")
        for r in summary.error:
            print(f"  {r.path.relative_to(repo_root)}: {r.detail}")

    if not args.apply and (summary.added or summary.updated):
        print("\n*** DRY-RUN. Pokreni sa --apply. ***")

    return 1 if (summary.error or summary.api_error) else 0


if __name__ == "__main__":
    sys.exit(main())
