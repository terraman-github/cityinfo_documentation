#!/usr/bin/env python3
"""
inject_page_ids.py
==================

Dodaje `confluence_page_id` field u YAML frontmatter svakog markdown fajla
u repou na osnovu page-id-map.json fajla generisanog od strane build_page_id_map.py.

Strategija:
- Frontmatter se obrađuje kao TEKST (line-by-line), ne preko YAML parsera.
  Ovo čuva originalno formatiranje (flow vs block style liste, redoslijed
  polja, navodnike ili odsustvo navodnika, itd.). Cilj je clean diff.
- `confluence_page_id` se ubacuje odmah ispod `id:` linije.
- Ako fajl već ima `confluence_page_id`, default je SKIP (ne pregaziti).
  Sa --update flag-om, vrijednost se ažurira ako se razlikuje.
- Default je dry-run (samo pokaže šta bi uradilo). Sa --apply, pravi izmjene.

Mapping fajlova na page ID-eve:
1. Story fajlovi (s##-## ili s##a-## u imenu) -> mapping iz `epics_and_stories`
2. Epic fajlovi (e## ili e##a/b u imenu) -> mapping iz `epics_and_stories`
3. Root chapters (01-..., 02-..., itd.) -> mapping iz `root_pages`
4. Specijalni root fajlovi (mvp-scope-..., novi-listing-statusni-...)
   -> mapping iz `root_pages`

Pokretanje:
    python inject_page_ids.py                          # dry-run, pokaze sta bi se promijenilo
    python inject_page_ids.py --apply                  # pravi izmjene
    python inject_page_ids.py --apply --update         # i ažurira postojeće page_id ako se razlikuje
    python inject_page_ids.py --map ../path/to/map.json --root ../  # nestandardne putanje
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


# --------------------------------------------------------------------------
# Default putanje (relativne na lokaciju skripte: md2conf-tooling/)
# --------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_MAP = SCRIPT_DIR / "page-id-map.json"
DEFAULT_REPO_ROOT = SCRIPT_DIR.parent  # cityinfo_documentation/

# Mapiranje imena root fajlova na ključeve u root_pages.
# Ovo je jedina ručna stvar koja se mora održavati ako se promijene imena
# fajlova ili dodaju novi root dokumenti.
ROOT_FILE_TO_KEY = {
    "01-uvod-i-koncepti.md": "Ch.01",
    "02-korisnicko-iskustvo.md": "Ch.02",
    "03-korisnici-i-pristup.md": "Ch.03",
    "04-sadrzaj.md": "Ch.04",
    "05-moderacija.md": "Ch.05",
    "06-monetizacija.md": "Ch.06",
    "07-komunikacija.md": "Ch.07",
    "08-infrastruktura.md": "Ch.08",
    "mvp-scope-opseg-prve-verzije.md": "MVP-SCOPE",
    "novi-listing-statusni-model-specifikacija.md": "STATUS-MODEL-SPEC",
}

# Prepoznavanje epic/story fajlova po imenu — tolerantan regex.
# Matcuje: e01-..., e03a-..., s01-01-..., s03a-01-...
EPIC_FILENAME_RE = re.compile(r"^e(\d+[a-z]?)-", re.IGNORECASE)
STORY_FILENAME_RE = re.compile(r"^s(\d+[a-z]?-\d+)-", re.IGNORECASE)

# Prepoznavanje frontmatter granica i polja.
FRONTMATTER_DELIM = "---"
ID_LINE_RE = re.compile(r"^(?P<indent>\s*)id\s*:\s*(?P<value>.+?)\s*$")
PAGE_ID_LINE_RE = re.compile(
    r"^(?P<indent>\s*)confluence_page_id\s*:\s*(?P<value>.+?)\s*$"
)


# --------------------------------------------------------------------------
# Data klase za rezultat
# --------------------------------------------------------------------------

@dataclass
class FileResult:
    path: Path
    status: str  # "added", "skipped_existing", "skipped_no_match", "skipped_no_frontmatter", "error", "updated"
    detail: str = ""
    expected_page_id: str | None = None
    existing_page_id: str | None = None


@dataclass
class Summary:
    added: list[FileResult] = field(default_factory=list)
    updated: list[FileResult] = field(default_factory=list)
    skipped_existing: list[FileResult] = field(default_factory=list)
    skipped_no_match: list[FileResult] = field(default_factory=list)
    skipped_no_frontmatter: list[FileResult] = field(default_factory=list)
    errors: list[FileResult] = field(default_factory=list)

    def add(self, r: FileResult) -> None:
        getattr(self, r.status).append(r)


# --------------------------------------------------------------------------
# Ključna logika — derivacija page ID-a iz fajla
# --------------------------------------------------------------------------

def _normalize_epic_id(raw: str) -> str:
    """E.g. '01' -> 'E01', '03a' -> 'E03a'."""
    return f"E{raw.upper() if raw[-1:].isalpha() else raw}"


def _normalize_story_id(raw: str) -> str:
    """E.g. '01-01' -> 'S01-01', '03a-01' -> 'S03a-01'."""
    # raw je npr. "01-01" ili "03a-01"
    # Velika slova zadržavamo samo ako su slova prisutna.
    head, _, tail = raw.partition("-")
    head_norm = head.upper() if head and head[-1:].isalpha() else head
    return f"S{head_norm}-{tail}"


def derive_logical_id(file_path: Path, repo_root: Path) -> str | None:
    """
    Vrati logički ID koji se koristi kao ključ u page-id-map.json.

    Za root fajlove ključ je iz ROOT_FILE_TO_KEY (npr. "Ch.01", "MVP-SCOPE").
    Za epic fajlove ključ je oblika "E01", "E03a".
    Za story fajlove ključ je oblika "S01-01", "S03a-01".
    Vrati None ako je fajl izvan očekivanih lokacija.
    """
    rel = file_path.relative_to(repo_root)
    parts = rel.parts
    name = file_path.name

    if len(parts) == 1 and name in ROOT_FILE_TO_KEY:
        return ROOT_FILE_TO_KEY[name]

    if len(parts) >= 2 and parts[0] == "epics-and-stories":
        if len(parts) == 2:
            m = EPIC_FILENAME_RE.match(name)
            if m:
                return _normalize_epic_id(m.group(1))
        if len(parts) == 3:
            m = STORY_FILENAME_RE.match(name)
            if m:
                return _normalize_story_id(m.group(1))

    return None


# --------------------------------------------------------------------------
# Frontmatter manipulacija (line-by-line, čuva formatiranje)
# --------------------------------------------------------------------------

def split_frontmatter(content: str) -> tuple[list[str] | None, str]:
    """
    Vrati (frontmatter_lines, ostatak) ili (None, content) ako frontmatter ne postoji.
    frontmatter_lines NE uključuje --- markere.
    ostatak uključuje sve od --- na kraju frontmattera nadalje.
    """
    lines = content.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != FRONTMATTER_DELIM:
        return None, content

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r\n") == FRONTMATTER_DELIM:
            end_idx = i
            break

    if end_idx is None:
        # Otvoreni frontmatter bez zatvaranja — ne dirati.
        return None, content

    frontmatter_lines = lines[1:end_idx]
    rest = "".join(lines[end_idx:])  # uključi zatvarajući ---
    return frontmatter_lines, rest


def find_existing_page_id(frontmatter_lines: list[str]) -> tuple[int, str] | None:
    """Vrati (line_index, value) ako postoji confluence_page_id, inače None."""
    for i, line in enumerate(frontmatter_lines):
        m = PAGE_ID_LINE_RE.match(line)
        if m:
            return (i, m.group("value").strip().strip('"').strip("'"))
    return None


def find_id_line_index(frontmatter_lines: list[str]) -> int | None:
    """Vrati index linije sa `id:` field-om, ili None ako ne postoji."""
    for i, line in enumerate(frontmatter_lines):
        if ID_LINE_RE.match(line):
            return i
    return None


def inject_page_id(
    frontmatter_lines: list[str],
    page_id: str,
    update_existing: bool = False,
) -> tuple[list[str], str]:
    """
    Vrati (nove_linije, status) gdje je status:
        "added"            — uspješno dodano (ispod id: ako postoji, inače na kraj frontmattera)
        "skipped_existing" — već postoji, nije ažurirano
        "updated"          — postojalo je ali sa drugom vrijednošću, ažurirano
    """
    existing = find_existing_page_id(frontmatter_lines)
    if existing is not None:
        idx, current_value = existing
        if current_value == page_id:
            return frontmatter_lines, "skipped_existing"
        if not update_existing:
            return frontmatter_lines, "skipped_existing"
        # Ažuriraj
        old_line = frontmatter_lines[idx]
        m = PAGE_ID_LINE_RE.match(old_line)
        indent = m.group("indent") if m else ""
        # Sačuvaj line ending iz originala
        line_ending = ""
        if old_line.endswith("\r\n"):
            line_ending = "\r\n"
        elif old_line.endswith("\n"):
            line_ending = "\n"
        new_line = f'{indent}confluence_page_id: "{page_id}"{line_ending}'
        new_lines = list(frontmatter_lines)
        new_lines[idx] = new_line
        return new_lines, "updated"

    id_idx = find_id_line_index(frontmatter_lines)
    if id_idx is not None:
        # Standardni put: ubaci confluence_page_id odmah ispod id linije, sa istim indent-om
        id_line = frontmatter_lines[id_idx]
        m = ID_LINE_RE.match(id_line)
        indent = m.group("indent") if m else ""
        line_ending = ""
        if id_line.endswith("\r\n"):
            line_ending = "\r\n"
        elif id_line.endswith("\n"):
            line_ending = "\n"
        else:
            line_ending = "\n"

        new_line = f'{indent}confluence_page_id: "{page_id}"{line_ending}'
        new_lines = list(frontmatter_lines)
        new_lines.insert(id_idx + 1, new_line)
        return new_lines, "added"

    # Fallback: nema `id:` linije (npr. chapter fajlovi sa samo `title`).
    # Ubaci confluence_page_id na kraj frontmattera, bez indent-a.
    # Sačuvaj line ending stila iz nekog postojećeg reda.
    line_ending = "\n"
    for line in frontmatter_lines:
        if line.endswith("\r\n"):
            line_ending = "\r\n"
            break
        if line.endswith("\n"):
            line_ending = "\n"
            break

    new_line = f'confluence_page_id: "{page_id}"{line_ending}'
    new_lines = list(frontmatter_lines)
    # Ako zadnji red ne završava sa newline-om, dodaj ga prvo da naš novi red bude na svojoj liniji
    if new_lines and not (new_lines[-1].endswith("\n") or new_lines[-1].endswith("\r\n")):
        new_lines[-1] = new_lines[-1] + line_ending
    new_lines.append(new_line)
    return new_lines, "added"


def reassemble(frontmatter_lines: list[str], rest: str, original_content: str) -> str:
    """
    Sastavi nazad cijeli sadržaj fajla. Sačuvaj line ending stila prvog --- markera.
    """
    # Detektuj line ending iz original prvog reda
    if original_content.startswith("---\r\n"):
        delim_line = "---\r\n"
    else:
        delim_line = "---\n"
    return delim_line + "".join(frontmatter_lines) + rest


# --------------------------------------------------------------------------
# Glavna iteracija
# --------------------------------------------------------------------------

def iter_target_files(repo_root: Path) -> list[Path]:
    """
    Vrati listu kandidata. Ne ulazi u .venv, .git, jira-sync, md2conf-tooling, itd.
    """
    excluded_top_dirs = {
        ".venv", ".git", "jira-sync", "md2conf-tooling", "node_modules",
        ".claude", ".vscode",
    }
    # Internal-only fajlovi koje preskačemo iako su .md
    excluded_filenames = {
        "audit-report.md",
        "CLAUDE.md",
        "CLAUDE-13-to-12.md",
        "cityinfo-epics-stories-instructions.md",
        "README.md",
        "pisanje-epica-i-user-storija-instrukcija.md",
        "plan-pisanja-epica-i-storija.md",
    }

    results = []
    for p in repo_root.rglob("*.md"):
        # Provjeri da li je u isključenom top-level direktorijumu
        rel = p.relative_to(repo_root)
        if rel.parts and rel.parts[0] in excluded_top_dirs:
            continue
        if p.name in excluded_filenames:
            continue
        results.append(p)
    return sorted(results)


def process_file(
    path: Path,
    repo_root: Path,
    page_id_map: dict,
    update_existing: bool,
    apply_changes: bool,
) -> FileResult:
    logical_id = derive_logical_id(path, repo_root)
    if logical_id is None:
        return FileResult(
            path=path,
            status="skipped_no_match",
            detail="ne mapira se na poznati ID (interni dokument?)",
        )

    # Pronađi page ID u mapi
    page_id = (
        page_id_map.get("epics_and_stories", {}).get(logical_id)
        or page_id_map.get("root_pages", {}).get(logical_id)
    )
    if page_id is None:
        return FileResult(
            path=path,
            status="skipped_no_match",
            detail=f"logički ID '{logical_id}' nije u page-id-map.json",
        )

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return FileResult(path=path, status="errors", detail=f"read error: {e}")

    fm_lines, rest = split_frontmatter(content)
    if fm_lines is None:
        return FileResult(
            path=path,
            status="skipped_no_frontmatter",
            detail="nema YAML frontmatter-a (--- ... ---)",
            expected_page_id=page_id,
        )

    new_fm_lines, op_status = inject_page_id(fm_lines, page_id, update_existing)

    if op_status == "skipped_existing":
        existing = find_existing_page_id(fm_lines)
        existing_value = existing[1] if existing else None
        return FileResult(
            path=path,
            status="skipped_existing",
            detail=f"već ima confluence_page_id={existing_value!r}",
            expected_page_id=page_id,
            existing_page_id=existing_value,
        )

    # op_status je "added" ili "updated" — treba upisati ako apply_changes
    if apply_changes:
        new_content = reassemble(new_fm_lines, rest, content)
        try:
            path.write_text(new_content, encoding="utf-8", newline="")
        except Exception as e:
            return FileResult(path=path, status="errors", detail=f"write error: {e}")

    status_key = "added" if op_status == "added" else "updated"
    return FileResult(
        path=path,
        status=status_key,
        detail=f"page_id={page_id}",
        expected_page_id=page_id,
    )


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--map",
        type=Path,
        default=DEFAULT_MAP,
        help=f"Path do page-id-map.json (default: {DEFAULT_MAP})",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_REPO_ROOT,
        help=f"Root direktorij repoa (default: {DEFAULT_REPO_ROOT})",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Pravi stvarne izmjene. Bez ovog flag-a, samo dry-run pregled.",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Ažuriraj postojeći confluence_page_id ako se razlikuje. "
             "Default: preskoči fajl ako već ima confluence_page_id.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Detaljniji ispis (svaki fajl posebno).",
    )
    args = parser.parse_args()

    if not args.map.exists():
        sys.exit(f"GREŠKA: ne mogu naći page-id-map.json na {args.map}")
    if not args.root.exists():
        sys.exit(f"GREŠKA: repo root ne postoji: {args.root}")

    page_id_map = json.loads(args.map.read_text(encoding="utf-8"))
    repo_root = args.root.resolve()

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"=== inject_page_ids.py — {mode} ===")
    print(f"Repo root: {repo_root}")
    print(f"Map file:  {args.map}")
    if args.update:
        print("Update mode: postojeći confluence_page_id će biti ažuriran ako se razlikuje")
    print()

    files = iter_target_files(repo_root)
    print(f"Pronađeno {len(files)} markdown fajlova za obradu.\n")

    summary = Summary()
    for f in files:
        r = process_file(
            f,
            repo_root=repo_root,
            page_id_map=page_id_map,
            update_existing=args.update,
            apply_changes=args.apply,
        )
        summary.add(r)
        if args.verbose:
            rel = r.path.relative_to(repo_root)
            print(f"  [{r.status:25s}] {rel}  — {r.detail}")

    # === SAŽETAK ===
    print("\n=== REZULTAT ===")
    print(f"  Dodano novih confluence_page_id:    {len(summary.added)}")
    print(f"  Ažurirano postojećih:               {len(summary.updated)}")
    print(f"  Preskočeno (već postoji):           {len(summary.skipped_existing)}")
    print(f"  Preskočeno (nije u mapi):           {len(summary.skipped_no_match)}")
    print(f"  Preskočeno (bez frontmatter-a):     {len(summary.skipped_no_frontmatter)}")
    print(f"  Greške:                             {len(summary.errors)}")

    if summary.errors:
        print("\n--- GREŠKE ---")
        for r in summary.errors:
            print(f"  {r.path.relative_to(repo_root)}: {r.detail}")

    if summary.skipped_no_match and not args.verbose:
        print(f"\nNapomena: {len(summary.skipped_no_match)} fajlova nije moglo biti "
              f"mapirano (interni dokumenti i sl.). Pokreni sa -v za detalje.")

    if summary.skipped_no_frontmatter:
        print("\n--- BEZ FRONTMATTER-A (ne dirano) ---")
        for r in summary.skipped_no_frontmatter:
            rel = r.path.relative_to(repo_root)
            print(f"  {rel}  (očekivao bi page_id={r.expected_page_id})")
        print("\n  Ovi fajlovi se mogu ručno popraviti — dodaj YAML frontmatter na vrh sa `id: <ID>`")
        print("  pa ponovo pokreni skriptu.")

    if not args.apply:
        if summary.added or summary.updated:
            print("\n*** DRY-RUN. Ništa nije zapisano na disk. ***")
            print("    Pokreni ponovo sa --apply za primjenu izmjena.")
        else:
            print("\nNema izmjena za primijeniti.")

    return 0 if not summary.errors else 1


if __name__ == "__main__":
    sys.exit(main())
