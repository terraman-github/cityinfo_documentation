#!/usr/bin/env python3
"""
markdown_cleanup.py
===================

Popravlja tri konkretna problema u markdown fajlovima koji uzrokuju loše
renderovanje na Confluenceu nakon md2conf push-a:

1. **Duplikat H1 heading-a** — ukloni `# X` na vrhu fajla ako se podudara sa
   imenom (npr. fajl S01-01-... ima `# S01-01 — Registracija novog korisnika`,
   što duplira Confluence page title).

2. **Zalijepljen bold pattern** — `**Label:** **Value**` na početku linije
   se popravlja u `**Label:** Value`. Confluence renderuje dvostruki bold bez
   razmaka. Akcija samo na "label + value" patternu.

3. **User story trailing-spaces** — pretvori
       Kao posjetilac,  <2 spaces>
       želim X,         <2 spaces>
       kako bih Y.
   u tri zasebna paragrafa razdvojena praznim linijama. Ovo se primjenjuje
   samo unutar **User story:** sekcije.

Strategija:
- Line-by-line obrada uvijek (ne YAML/markdown parser).
- Default je dry-run sa --apply za primjenu.
- Verbose pokazuje šta je popravljeno u svakom fajlu.
- Idempotentno: drugi run ne mijenja ništa.

Pokretanje:
    python markdown_cleanup.py                    # dry-run
    python markdown_cleanup.py --apply            # primjeni izmjene
    python markdown_cleanup.py --apply -v         # primjeni + detalji
    python markdown_cleanup.py --only-h1          # samo popravka 1
    python markdown_cleanup.py --only-bold        # samo popravka 2
    python markdown_cleanup.py --only-userstory   # samo popravka 3
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = SCRIPT_DIR.parent

# Foldere/fajlove koje preskačemo (isti kao u inject_page_ids.py)
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


# --------------------------------------------------------------------------
# Frontmatter helperi
# --------------------------------------------------------------------------

FRONTMATTER_DELIM = "---"


def split_frontmatter(content: str) -> tuple[list[str] | None, list[str], str]:
    """
    Vrati (frontmatter_lines, body_lines, line_ending).
    Ako frontmatter ne postoji, frontmatter_lines = None.
    """
    line_ending = "\r\n" if "\r\n" in content[:4096] else "\n"
    lines = content.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != FRONTMATTER_DELIM:
        return None, lines, line_ending

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r\n") == FRONTMATTER_DELIM:
            end_idx = i
            break
    if end_idx is None:
        return None, lines, line_ending

    # Frontmatter (sa --- markerima), pa body
    frontmatter = lines[: end_idx + 1]
    body = lines[end_idx + 1:]
    return frontmatter, body, line_ending


def extract_frontmatter_title(frontmatter_lines: list[str]) -> str | None:
    """Izvuci `title:` field iz frontmatter-a."""
    title_re = re.compile(r'^title\s*:\s*"?(?P<value>.+?)"?\s*$')
    for line in frontmatter_lines:
        m = title_re.match(line.strip())
        if m:
            return m.group("value").strip().strip('"').strip("'")
    return None


def extract_frontmatter_id(frontmatter_lines: list[str]) -> str | None:
    """Izvuci `id:` field iz frontmatter-a."""
    id_re = re.compile(r'^id\s*:\s*"?(?P<value>.+?)"?\s*$')
    for line in frontmatter_lines:
        m = id_re.match(line.strip())
        if m:
            return m.group("value").strip().strip('"').strip("'")
    return None


# --------------------------------------------------------------------------
# Popravka 1: Ukloni redundantni H1
# --------------------------------------------------------------------------

H1_RE = re.compile(r"^#\s+(?P<heading>.+?)\s*$")


def fix_redundant_h1(
    body_lines: list[str],
    frontmatter_id: str | None,
    frontmatter_title: str | None,
) -> tuple[list[str], bool]:
    """
    Pronađi prvi H1 u body-ju. Ukloni ga ako:
    1. Počinje sa logičkim ID-em iz frontmatter-a (npr. "# E01 — ..."), ILI
    2. Tekst H1-a je identičan title-u iz frontmatter-a (case-insensitive,
       tolerantan na - vs —).

    Vrati (nove_linije, is_modified).
    """
    if not frontmatter_id and not frontmatter_title:
        return body_lines, False

    # Pronađi prvu nepraznu liniju
    first_nonempty_idx = None
    for i, line in enumerate(body_lines):
        if line.strip():
            first_nonempty_idx = i
            break

    if first_nonempty_idx is None:
        return body_lines, False

    first_line = body_lines[first_nonempty_idx]
    m = H1_RE.match(first_line.strip())
    if not m:
        return body_lines, False

    heading = m.group("heading").strip()

    # Pokušaj 1: H1 počinje sa frontmatter ID-em (E01, S01-01, ...)
    matches_id = (
        frontmatter_id
        and heading.upper().startswith(frontmatter_id.upper())
    )

    # Pokušaj 2: H1 je u suštini isti kao title (case-insensitive,
    # tolerantan na različite tipove dash-eva)
    matches_title = False
    if frontmatter_title:
        norm_heading = _normalize_for_match(heading)
        norm_title = _normalize_for_match(frontmatter_title)
        matches_title = norm_heading == norm_title

    if not (matches_id or matches_title):
        return body_lines, False

    # Ukloni H1 liniju + prazne linije ispred (ako ih ima)
    new_lines = list(body_lines)
    del new_lines[first_nonempty_idx]
    while first_nonempty_idx > 0 and not new_lines[first_nonempty_idx - 1].strip():
        del new_lines[first_nonempty_idx - 1]
        first_nonempty_idx -= 1

    return new_lines, True


def _normalize_for_match(text: str) -> str:
    """
    Normalizuj string za match: lowercase, sve dash-eve pretvori u jedan tip,
    skupi razmake.
    """
    # Sve vrste dash-eva u običan -
    for dash in ["—", "–", "‒", "−"]:
        text = text.replace(dash, "-")
    # Skupi višestruke razmake u jedan
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


# --------------------------------------------------------------------------
# Popravka 2: Razdvoji **Label:** **Value** pattern
# --------------------------------------------------------------------------

# Pattern: linija počinje sa "**Label:**", zatim razmak, pa "**Value**", pa
# opciono dodatni tekst do kraja linije. Akcija je samo da se drugi par
# zvjezdica ukloni; dodatni tekst (npr. ", sekcije 3.2–3.3") ostaje.
#
# Primjeri koji se popravljaju:
#   **Phase:** **MVP**                                 → **Phase:** MVP
#   **Journey milestones:** **J-01**                   → **Journey milestones:** J-01
#   **Dokumentacijska referenca:** **Ch.03**, sekcije  → **Dokumentacijska referenca:** Ch.03, sekcije
#
# Primjeri koji se NE diraju:
#   **Label:** vrijednost bez bold-a                   → match ne uspijeva (nema drugi **)
#   **Mješano:** vrijednost sa **bold** dijelom        → match ne uspijeva (** nije odmah nakon labela)
#
# Ključno: zahtijevamo da drugi ** počinje odmah nakon razmaka (\s+), tako da
# slučajevi gdje je bold blok u sredini paragrafa ne match-iraju.
BOLD_LABEL_VALUE_RE = re.compile(
    r"^(?P<indent>\s*)"
    r"(?P<label>\*\*[^*]+:\*\*)"     # **Label:**
    r"\s+"
    r"\*\*(?P<value>[^*\n]+?)\*\*"   # **Value**  (ne sadrži ** ili newline)
    r"(?P<rest>[^\n]*)"              # opciono: dodatni tekst do kraja linije
    r"\s*$"
)


def fix_bold_label_value(body_lines: list[str]) -> tuple[list[str], int]:
    """
    Pronađi linije sa patternom "**Label:** **Value**" i pretvori u "**Label:** Value".
    Vrati (nove_linije, broj_promjena).
    """
    new_lines = []
    changes = 0
    for line in body_lines:
        # Sačuvaj line ending za output
        line_no_ending = line
        ending = ""
        if line.endswith("\r\n"):
            ending = "\r\n"
            line_no_ending = line[:-2]
        elif line.endswith("\n"):
            ending = "\n"
            line_no_ending = line[:-1]

        m = BOLD_LABEL_VALUE_RE.match(line_no_ending)
        if m:
            rest = m.group("rest") or ""
            new_line = f"{m.group('indent')}{m.group('label')} {m.group('value')}{rest}{ending}"
            new_lines.append(new_line)
            changes += 1
        else:
            new_lines.append(line)

    return new_lines, changes


# --------------------------------------------------------------------------
# Popravka 3: User story trailing-spaces -> prazne linije
# --------------------------------------------------------------------------

# Detektuj početak User story sekcije
USER_STORY_HEADER_RE = re.compile(r"^\*\*User story:\*\*\s*$")


def fix_user_story_line_breaks(body_lines: list[str]) -> tuple[list[str], int]:
    """
    Pronađi blok između "**User story:**" i sljedeće prazne linije ili sljedećeg
    `**Header:**` block-a. Ako linije unutar bloka završavaju trailing spaces
    (markdown soft break), zamijeni "trailing spaces + newline" sa "newline +
    prazna linija + newline".

    Vrati (nove_linije, broj_promjena).
    """
    new_lines = []
    changes = 0
    i = 0
    n = len(body_lines)

    while i < n:
        line = body_lines[i]

        # Detektuj početak User story sekcije
        line_stripped = line.rstrip("\r\n")
        if not USER_STORY_HEADER_RE.match(line_stripped):
            new_lines.append(line)
            i += 1
            continue

        # Smo na User story header liniji. Dodaj je.
        new_lines.append(line)
        i += 1

        # Pronađi sve linije do kraja sekcije (do prazne linije ili sljedećeg headera)
        block_lines: list[str] = []
        while i < n:
            next_line = body_lines[i]
            next_stripped = next_line.rstrip("\r\n")
            # Sekcija završava na praznoj liniji ili sljedećem **Header:**
            if not next_stripped.strip():
                break
            # Sljedeći **X:** header (kao **Kontekst:**) označava kraj
            if re.match(r"^\*\*[^*]+:\*\*", next_stripped.lstrip()):
                # Ali ne ako je trenutna linija dio user story-a (rijetko)
                # Sigurnije: prekini ovdje
                break
            block_lines.append(next_line)
            i += 1

        # Procijeni da li blok ima trailing spaces (markdown soft break)
        has_trailing_spaces = any(
            l.rstrip("\r\n").endswith("  ") for l in block_lines
        )

        if has_trailing_spaces and len(block_lines) > 1:
            # Otkrij line ending iz prve linije bloka
            ending = "\n"
            for l in block_lines:
                if l.endswith("\r\n"):
                    ending = "\r\n"
                    break
                if l.endswith("\n"):
                    ending = "\n"
                    break

            # Pretvori svaku liniju: ukloni trailing spaces, dodaj praznu liniju nakon
            # (osim nakon zadnje)
            for j, bl in enumerate(block_lines):
                # Ukloni trailing whitespace prije line ending-a
                stripped = bl.rstrip()  # ovo skida i \r\n i trailing spaces
                new_lines.append(stripped + ending)
                # Dodaj praznu liniju ako nije zadnja
                if j < len(block_lines) - 1:
                    new_lines.append(ending)
            changes += 1
        else:
            new_lines.extend(block_lines)

    return new_lines, changes


# --------------------------------------------------------------------------
# Glavna obrada fajla
# --------------------------------------------------------------------------

@dataclass
class FileResult:
    path: Path
    h1_removed: bool = False
    bold_fixes: int = 0
    user_story_fixes: int = 0
    error: str | None = None

    @property
    def total_changes(self) -> int:
        return int(self.h1_removed) + self.bold_fixes + self.user_story_fixes

    @property
    def is_changed(self) -> bool:
        return self.total_changes > 0 or self.error is not None


def process_file(
    path: Path,
    apply_changes: bool,
    do_h1: bool,
    do_bold: bool,
    do_userstory: bool,
) -> FileResult:
    result = FileResult(path=path)

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        result.error = f"read error: {e}"
        return result

    frontmatter, body, line_ending = split_frontmatter(content)
    frontmatter_id = extract_frontmatter_id(frontmatter or [])
    frontmatter_title = extract_frontmatter_title(frontmatter or [])

    new_body = body

    if do_h1 and (frontmatter_id or frontmatter_title):
        new_body, h1_removed = fix_redundant_h1(
            new_body, frontmatter_id, frontmatter_title
        )
        result.h1_removed = h1_removed

    if do_bold:
        new_body, bold_changes = fix_bold_label_value(new_body)
        result.bold_fixes = bold_changes

    if do_userstory:
        new_body, us_changes = fix_user_story_line_breaks(new_body)
        result.user_story_fixes = us_changes

    if not result.is_changed:
        return result

    if apply_changes:
        # Sastavi novi sadržaj
        if frontmatter:
            new_content = "".join(frontmatter) + "".join(new_body)
        else:
            new_content = "".join(new_body)
        try:
            path.write_text(new_content, encoding="utf-8", newline="")
        except Exception as e:
            result.error = f"write error: {e}"

    return result


# --------------------------------------------------------------------------
# File discovery
# --------------------------------------------------------------------------

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


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_REPO_ROOT,
        help=f"Repo root (default: {DEFAULT_REPO_ROOT})",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Pravi stvarne izmjene (bez ovog flag-a, dry-run).",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Pokaži šta je popravljeno u svakom fajlu.",
    )
    parser.add_argument(
        "--only-h1",
        action="store_true",
        help="Primjeni samo Popravku 1 (ukloni redundantni H1).",
    )
    parser.add_argument(
        "--only-bold",
        action="store_true",
        help="Primjeni samo Popravku 2 (razdvoji **Label:** **Value**).",
    )
    parser.add_argument(
        "--only-userstory",
        action="store_true",
        help="Primjeni samo Popravku 3 (User story line breaks).",
    )
    args = parser.parse_args()

    # Određivanje koje popravke pokrenuti
    only_flags = [args.only_h1, args.only_bold, args.only_userstory]
    if any(only_flags):
        do_h1 = args.only_h1
        do_bold = args.only_bold
        do_userstory = args.only_userstory
    else:
        do_h1 = do_bold = do_userstory = True

    repo_root = args.root.resolve()
    mode = "APPLY" if args.apply else "DRY-RUN"

    print(f"=== markdown_cleanup.py — {mode} ===")
    print(f"Repo root: {repo_root}")
    enabled = []
    if do_h1: enabled.append("H1-removal")
    if do_bold: enabled.append("bold-fix")
    if do_userstory: enabled.append("user-story-fix")
    print(f"Aktivne popravke: {', '.join(enabled)}")
    print()

    files = iter_target_files(repo_root)
    print(f"Pronađeno {len(files)} markdown fajlova za pregled.\n")

    total_h1 = 0
    total_bold = 0
    total_userstory = 0
    errors: list[FileResult] = []
    changed_files = 0

    for f in files:
        r = process_file(
            f,
            apply_changes=args.apply,
            do_h1=do_h1,
            do_bold=do_bold,
            do_userstory=do_userstory,
        )
        if r.error:
            errors.append(r)
            continue
        if not r.is_changed:
            continue
        changed_files += 1
        total_h1 += int(r.h1_removed)
        total_bold += r.bold_fixes
        total_userstory += r.user_story_fixes

        if args.verbose:
            rel = r.path.relative_to(repo_root)
            parts = []
            if r.h1_removed: parts.append("H1")
            if r.bold_fixes: parts.append(f"bold×{r.bold_fixes}")
            if r.user_story_fixes: parts.append("user-story")
            print(f"  ~ {rel}  [{', '.join(parts)}]")

    print()
    print("=== REZULTAT ===")
    print(f"  Fajlova promijenjeno:           {changed_files}")
    print(f"  H1 heading-a uklonjeno:         {total_h1}")
    print(f"  Bold label-value popravki:      {total_bold}")
    print(f"  User story popravki:            {total_userstory}")
    print(f"  Greške:                         {len(errors)}")

    if errors:
        print("\n--- GREŠKE ---")
        for e in errors:
            print(f"  {e.path.relative_to(repo_root)}: {e.error}")

    if not args.apply and changed_files > 0:
        print()
        print("*** DRY-RUN. Ništa nije zapisano. Pokreni sa --apply za primjenu. ***")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
