#!/usr/bin/env python3
"""
fix_project_specs_links.py
==========================

Popravlja stale linkove `[text](../project-specs/<path>/<filename>.md)` koji
su zaostali iz prethodne strukture repoa, kada su chapter fajlovi živjeli
u poddirektorijumu `project-specs/`.

Sada su fajlovi u root-u repoa, pa su ti linkovi nevažeći — md2conf padne
sa "DocumentError: relative URL ... points to outside root path".

Strategija:
- Pronađe sve linkove pattern `(../project-specs/<anything>/<filename>.md)`
- Izvuče samo `<filename>.md` (zadnji segment putanje)
- Ako taj fajl postoji u root-u repoa → zamijeni link sa samo `<filename>.md`
- Ako ne postoji → loguje upozorenje i NE dira link

Default je dry-run.

Pokretanje:
    python fix_project_specs_links.py            # dry-run
    python fix_project_specs_links.py --apply    # primijeni izmjene
    python fix_project_specs_links.py --apply -v # detalji
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = SCRIPT_DIR.parent

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

# Pattern: [text](../project-specs/<anything>/<filename>.md[#anchor])
# Hvata:
#   - ../project-specs/02-korisnicko-iskustvo.md
#   - ../project-specs/migracija-.../novi-listing-statusni-model-specifikacija.md
#   - sa opcionim #anchor na kraju
LINK_RE = re.compile(
    r"\]\("                              # ](
    r"\.\.\/project-specs\/"             # ../project-specs/
    r"(?P<path>[^)\s]*?"                 # bilo šta osim ) i razmak (lazy)
    r"(?P<filename>[^/)\s]+\.md))"       # .../filename.md (zadnji segment)
    r"(?P<anchor>#[^)]*)?"               # opciono: #anchor
    r"\)"                                # )
)


@dataclass
class FileResult:
    path: Path
    fixes_applied: int = 0
    fixes_unresolved: list[str] = field(default_factory=list)
    error: str | None = None


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
    path: Path, repo_root: Path, apply_changes: bool
) -> FileResult:
    result = FileResult(path=path)

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        result.error = f"read error: {e}"
        return result

    new_content_parts = []
    last_end = 0

    for m in LINK_RE.finditer(content):
        filename = m.group("filename")
        anchor = m.group("anchor") or ""

        # Provjeri da li ciljni fajl postoji u root-u repoa
        target = repo_root / filename
        if not target.exists():
            result.fixes_unresolved.append(
                f"{m.group(0)} → fajl '{filename}' ne postoji u root-u"
            )
            # Ne diraj — ostavi original
            new_content_parts.append(content[last_end : m.end()])
            last_end = m.end()
            continue

        # Zamijeni link
        new_content_parts.append(content[last_end : m.start()])
        new_content_parts.append(f"]({filename}{anchor})")
        last_end = m.end()
        result.fixes_applied += 1

    new_content_parts.append(content[last_end:])
    new_content = "".join(new_content_parts)

    if apply_changes and result.fixes_applied > 0:
        try:
            path.write_text(new_content, encoding="utf-8", newline="")
        except Exception as e:
            result.error = f"write error: {e}"

    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--root", type=Path, default=DEFAULT_REPO_ROOT)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    repo_root = args.root.resolve()
    mode = "APPLY" if args.apply else "DRY-RUN"

    print(f"=== fix_project_specs_links.py — {mode} ===")
    print(f"Repo root: {repo_root}\n")

    files = iter_target_files(repo_root)
    print(f"Pronađeno {len(files)} markdown fajlova.\n")

    total_fixed = 0
    total_unresolved = 0
    files_with_changes = 0
    errors = []

    for f in files:
        r = process_file(f, repo_root, args.apply)
        if r.error:
            errors.append(r)
            continue
        if r.fixes_applied == 0 and not r.fixes_unresolved:
            continue
        files_with_changes += 1
        total_fixed += r.fixes_applied
        total_unresolved += len(r.fixes_unresolved)

        if args.verbose or r.fixes_unresolved:
            rel = r.path.relative_to(repo_root)
            print(f"  ~ {rel}: {r.fixes_applied} popravljeno"
                  + (f", {len(r.fixes_unresolved)} neriješeno" if r.fixes_unresolved else ""))
            for u in r.fixes_unresolved:
                print(f"      ⚠ {u}")

    print(f"\n=== REZULTAT ===")
    print(f"  Fajlova sa izmjenama:  {files_with_changes}")
    print(f"  Linkova popravljeno:   {total_fixed}")
    print(f"  Linkova neriješeno:    {total_unresolved}")
    print(f"  Greške:                {len(errors)}")

    if errors:
        print("\n--- GREŠKE ---")
        for e in errors:
            print(f"  {e.path.relative_to(repo_root)}: {e.error}")

    if not args.apply and total_fixed > 0:
        print("\n*** DRY-RUN. Pokreni sa --apply. ***")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
