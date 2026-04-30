#!/usr/bin/env python3
"""
markdown_userstory_format.py
============================

Reformatira **User story:** sekcije u markdown fajlovima:

PRIJE (nakon prethodnog cleanup-a):
    **User story:**
    Kao posjetilac CityInfo platforme,

    želim kreirati korisnički račun unosom osnovnih podataka,

    kako bih mogao pristupiti funkcionalnostima koje zahtijevaju registraciju.

    **Kontekst:** ...

POSLIJE:
    **User story:**

    *Kao posjetilac CityInfo platforme,*  
    *želim kreirati korisnički račun unosom osnovnih podataka,*  
    *kako bih mogao pristupiti funkcionalnostima koje zahtijevaju registraciju.*

    **Kontekst:** ...

Šta tačno radi:
1. Detektuje **User story:** sekciju
2. Pronalazi sve linije sadržaja (do sljedećeg **Header:** ili kraja fajla)
3. Uklanja prazne linije ИЗМЕЂУ rečenica (paragraph breaks)
4. Wrap-uje svaku liniju u italic markere `*...*`
5. Dodaje 2 razmaka na kraj svake linije osim zadnje (soft line break)
6. Header dobija praznu liniju ispod sebe
7. Razmak na početku prve linije se uklanja

Sigurnost:
- Akcija se primjenjuje samo na User story sekciju
- Ako je sadržaj već italic ili izgleda već formatiran (npr. počinje sa `*`),
  preskačemo da ne bi pokvarili
- Idempotentno

Pokretanje:
    python markdown_userstory_format.py            # dry-run
    python markdown_userstory_format.py --apply    # primijeni izmjene
    python markdown_userstory_format.py --apply -v # detalji
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


# Detektuj **User story:** header (može imati trailing whitespace ili spaces).
USER_STORY_HEADER_RE = re.compile(r"^\s*\*\*User story:\*\*\s*$")
# Detektuj bilo koji **Header:** koji označava kraj User story sekcije.
ANY_HEADER_RE = re.compile(r"^\s*\*\*[^*\n]+:\*\*")


def split_frontmatter(content: str) -> tuple[list[str], list[str], str]:
    """Vrati (frontmatter, body, line_ending)."""
    line_ending = "\r\n" if "\r\n" in content[:4096] else "\n"
    lines = content.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        return [], lines, line_ending

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r\n") == "---":
            end_idx = i
            break
    if end_idx is None:
        return [], lines, line_ending

    frontmatter = lines[: end_idx + 1]
    body = lines[end_idx + 1:]
    return frontmatter, body, line_ending


def is_already_formatted(content_lines: list[str]) -> bool:
    """
    Provjeri da li je User story već u traženom formatu.
    Heuristika: ako je prva neprazna linija sadržaja u italicu (počinje sa `*`
    i ne sa `**`), pretpostavljamo da je već formatirano.
    """
    for line in content_lines:
        stripped = line.strip()
        if not stripped:
            continue
        # Prva neprazna linija — provjeri da li je italic (*tekst*) a ne bold (**tekst**)
        if stripped.startswith("*") and not stripped.startswith("**"):
            return True
        return False
    return False


def reformat_user_story_block(
    content_lines: list[str], line_ending: str
) -> list[str]:
    """
    Uzmi linije sadržaja User story sekcije i vrati nove linije u traženom formatu.
    Input: linije između **User story:** header-a i sljedećeg **Header:** ili EOF.
    Output: header zamijenjen sa praznom linijom, sadržaj italic, soft line breaks.

    Linije ulaza mogu sadržavati prazne linije (paragraph breaks) — one se
    izbacuju jer želimo da sve rečenice budu u jednom paragrafu.
    """
    # Filtriraj prazne linije i normalizuj sadržaj
    sentences = []
    for line in content_lines:
        stripped = line.strip()
        if not stripped:
            continue
        # Ukloni postojeće italic markere ako ih ima (idempotentnost guard)
        # Pažljivo: samo ako linija počinje i završava sa jednim *
        if (stripped.startswith("*") and stripped.endswith("*")
                and not stripped.startswith("**") and not stripped.endswith("**")):
            stripped = stripped[1:-1].strip()
        sentences.append(stripped)

    if not sentences:
        return []

    # Konstruiši output: prazna linija + italic linije sa soft breaks
    output = [line_ending]  # prazna linija ispod **User story:**
    for i, sentence in enumerate(sentences):
        if i < len(sentences) - 1:
            # Sve osim zadnje — sa trailing 2 razmaka (soft break)
            output.append(f"*{sentence}*  {line_ending}")
        else:
            # Zadnja — bez trailing razmaka
            output.append(f"*{sentence}*{line_ending}")

    return output


def fix_user_story_in_body(
    body_lines: list[str], line_ending: str
) -> tuple[list[str], int]:
    """
    Pronađi sve User story sekcije i reformat-iraj ih.
    Vrati (nove_linije, broj_promjena).
    """
    new_lines = []
    changes = 0
    i = 0
    n = len(body_lines)

    while i < n:
        line = body_lines[i]
        # Detektuj User story header
        if not USER_STORY_HEADER_RE.match(line.rstrip("\r\n")):
            new_lines.append(line)
            i += 1
            continue

        # Found **User story:** header
        # Normalizuj: header bez trailing whitespace
        new_lines.append(f"**User story:**{line_ending}")
        i += 1

        # Skupi sve linije do sljedećeg **Header:** ili EOF
        block_start = i
        while i < n:
            next_line = body_lines[i]
            next_stripped = next_line.lstrip().rstrip("\r\n")
            # Sljedeći **Xxx:** header označava kraj User story sekcije
            if ANY_HEADER_RE.match(next_stripped):
                break
            i += 1

        block_lines = body_lines[block_start:i]

        # Provjeri idempotentnost
        if is_already_formatted(block_lines):
            # Već formatirano — vrati originalne linije bez promjene
            new_lines.extend(block_lines)
            continue

        # Reformat-iraj
        new_block = reformat_user_story_block(block_lines, line_ending)
        new_lines.extend(new_block)

        # Ako blok završava bez prazne linije, dodaj jednu prije sljedećeg headera
        # (samo ako sljedeći red postoji i nije već prazan)
        if (i < n and new_block and
                not new_block[-1].rstrip("\r\n") == "" and
                body_lines[i].strip()):
            new_lines.append(line_ending)

        changes += 1

    return new_lines, changes


# --------------------------------------------------------------------------
# Glavna logika
# --------------------------------------------------------------------------

@dataclass
class FileResult:
    path: Path
    changed: bool = False
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


def process_file(path: Path, apply_changes: bool) -> FileResult:
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return FileResult(path, error=f"read error: {e}")

    frontmatter, body, line_ending = split_frontmatter(content)
    new_body, changes = fix_user_story_in_body(body, line_ending)

    if changes == 0:
        return FileResult(path, changed=False)

    if apply_changes:
        new_content = "".join(frontmatter) + "".join(new_body)
        try:
            path.write_text(new_content, encoding="utf-8", newline="")
        except Exception as e:
            return FileResult(path, error=f"write error: {e}")

    return FileResult(path, changed=True)


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
    print(f"=== markdown_userstory_format.py — {mode} ===")
    print(f"Repo root: {repo_root}\n")

    files = iter_target_files(repo_root)
    print(f"Pronađeno {len(files)} markdown fajlova.\n")

    changed = 0
    errors = []
    for f in files:
        r = process_file(f, args.apply)
        if r.error:
            errors.append(r)
            continue
        if r.changed:
            changed += 1
            if args.verbose:
                print(f"  ~ {r.path.relative_to(repo_root)}")

    print(f"\n=== REZULTAT ===")
    print(f"  Fajlova promijenjeno:  {changed}")
    print(f"  Greške:                {len(errors)}")

    if errors:
        print("\n--- GREŠKE ---")
        for e in errors:
            print(f"  {e.path.relative_to(repo_root)}: {e.error}")

    if not args.apply and changed > 0:
        print("\n*** DRY-RUN. Pokreni sa --apply. ***")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
