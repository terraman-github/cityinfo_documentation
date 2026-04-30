#!/usr/bin/env python3
"""
add_chapter_frontmatter.py
==========================

Dodaje minimalan YAML frontmatter (samo `title` i `confluence_page_id`) na
chapter fajlove koji ga nemaju (01-uvod-i-koncepti.md, MVP scope, status spec).

Naslovi su uzeti direktno sa Confluence-a (page ID 15695888 sub-tree) tako da
se savršeno poklope sa onim što je već publikovano.

Strategija upisivanja:
- Pretpostavlja da fajl POČINJE sa H1 heading-om (npr. "# 01 — Uvod i koncepti")
  ili nečim drugim.
- Frontmatter blok se ubacuje kao prvi ured u fajlu (prije svega ostalog).
- Ako fajl već ima frontmatter, skripta ga PRESKAČE (ne dira).
- Default je dry-run.

Pokretanje:
    python add_chapter_frontmatter.py            # dry-run
    python add_chapter_frontmatter.py --apply    # pravi izmjene
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = SCRIPT_DIR.parent

# Mapping fajla -> (Confluence title, Confluence page ID)
# Naslovi su uzeti tačno sa Confluence-a da se poklope sa publikovanim stranicama.
CHAPTER_FRONTMATTER = {
    "01-uvod-i-koncepti.md": ("01 - UVOD I KONCEPTI", "240156678"),
    "02-korisnicko-iskustvo.md": ("02 - KORISNIČKO ISKUSTVO", "240254995"),
    "03-korisnici-i-pristup.md": ("03 - KORISNICI I PRISTUP", "240156686"),
    "04-sadrzaj.md": ("04 - SADRŽAJ", "240189477"),
    "05-moderacija.md": ("05 - MODERACIJA", "240189485"),
    "06-monetizacija.md": ("06 - MONETIZACIJA", "240222244"),
    "07-komunikacija.md": ("07 - KOMUNIKACIJA", "240320540"),
    "08-infrastruktura.md": ("08 - INFRASTRUKTURA", "240189509"),
    "mvp-scope-opseg-prve-verzije.md": ("MVP SCOPE — Opseg prve verzije", "242188289"),
    "novi-listing-statusni-model-specifikacija.md": (
        "Novi listing statusni model — specifikacija",
        "253526019",
    ),
}


def detect_line_ending(content: str) -> str:
    """Vrati \\r\\n ili \\n na osnovu prvog reda fajla."""
    if "\r\n" in content[:4096]:
        return "\r\n"
    return "\n"


def has_frontmatter(content: str) -> bool:
    """Vrati True ako fajl počinje sa --- frontmatter blokom."""
    lines = content.splitlines()
    return bool(lines) and lines[0].strip() == "---"


def build_frontmatter(title: str, page_id: str, line_ending: str) -> str:
    """Sastavi YAML frontmatter blok kao string sa završnim line ending-om."""
    return (
        f"---{line_ending}"
        f'title: "{title}"{line_ending}'
        f'confluence_page_id: "{page_id}"{line_ending}'
        f"---{line_ending}"
        f"{line_ending}"
    )


def process_file(
    path: Path, title: str, page_id: str, apply_changes: bool
) -> tuple[str, str]:
    """
    Vrati (status, detail) gdje je status:
        "added"   — frontmatter dodan
        "skipped_existing" — već ima frontmatter
        "missing" — fajl ne postoji
        "error"   — read/write greška
    """
    if not path.exists():
        return ("missing", f"fajl ne postoji: {path}")

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return ("error", f"read error: {e}")

    if has_frontmatter(content):
        return ("skipped_existing", "već ima frontmatter")

    line_ending = detect_line_ending(content)
    frontmatter = build_frontmatter(title, page_id, line_ending)
    new_content = frontmatter + content

    if apply_changes:
        try:
            # newline="" da Python ne radi automatsku konverziju line endings
            path.write_text(new_content, encoding="utf-8", newline="")
        except Exception as e:
            return ("error", f"write error: {e}")

    return ("added", f"title={title!r}, page_id={page_id}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Pravi stvarne izmjene. Bez ovog flag-a, dry-run.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_REPO_ROOT,
        help=f"Repo root (default: {DEFAULT_REPO_ROOT})",
    )
    args = parser.parse_args()

    repo_root = args.root.resolve()
    mode = "APPLY" if args.apply else "DRY-RUN"

    print(f"=== add_chapter_frontmatter.py — {mode} ===")
    print(f"Repo root: {repo_root}")
    print()

    counts = {"added": 0, "skipped_existing": 0, "missing": 0, "error": 0}

    for filename, (title, page_id) in CHAPTER_FRONTMATTER.items():
        path = repo_root / filename
        status, detail = process_file(path, title, page_id, args.apply)
        counts[status] += 1
        marker = {
            "added": "✓",
            "skipped_existing": "·",
            "missing": "?",
            "error": "✗",
        }[status]
        print(f"  {marker} [{status:18s}] {filename}")
        if status in ("error", "missing"):
            print(f"      → {detail}")

    print()
    print("=== REZULTAT ===")
    print(f"  Dodano:                   {counts['added']}")
    print(f"  Preskočeno (već postoji): {counts['skipped_existing']}")
    print(f"  Fajl ne postoji:          {counts['missing']}")
    print(f"  Greške:                   {counts['error']}")

    if not args.apply and counts["added"] > 0:
        print()
        print("*** DRY-RUN. Ništa nije zapisano. Pokreni sa --apply za primjenu. ***")

    return 1 if counts["error"] else 0


if __name__ == "__main__":
    sys.exit(main())
