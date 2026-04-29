#!/usr/bin/env python3
"""
build_page_id_map.py
====================

Prolazi kroz Confluence sub-tree pod EPICS AND STORIES folderom (page ID 250249231)
i gradi mapping {epic_or_story_id: confluence_page_id}.

Naslov stranice ima format:
    E01 — Korisnička registracija i profil          -> id = "E01"
    E03a — Kategorizacija sadržaja — entiteti...    -> id = "E03a"
    S01-01 — Registracija novog korisnika           -> id = "S01-01"
    S03a-01 — Category entiteti i relaciona tabela  -> id = "S03a-01"

Dodatno se ručno mapiraju i chapter/MVP stranice na root nivou
(jer one nisu pod EPICS AND STORIES folderom).

Output: page-id-map.json u istom direktorijumu (ili na putanju iz --output flag-a).

Konfiguracija preko ENV varijabli:
    ATLASSIAN_EMAIL       — Confluence user email
    ATLASSIAN_API_TOKEN   — API token sa id.atlassian.com/manage/api-tokens

Pokretanje:
    python build_page_id_map.py
    python build_page_id_map.py --output ../md2conf-config/page-id-map.json
    python build_page_id_map.py --include-stale          # uključi i obrisane page-ove
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Iterator

import requests
from requests.auth import HTTPBasicAuth


# --------------------------------------------------------------------------
# Konfiguracija — promijeni ako budeš koristio drugi Cloud ID
# --------------------------------------------------------------------------

CLOUD_ID = "45983047-331b-459e-b1a5-052825171c8c"
CONFLUENCE_API_BASE = f"https://api.atlassian.com/ex/confluence/{CLOUD_ID}/wiki/api/v2"

EPICS_AND_STORIES_ROOT = "250249231"

# Ručno mapirane stranice koje nisu pod EPICS AND STORIES folderom
# Ključevi su "logički ID-evi" koje ćemo koristiti u markdown frontmatter-u.
# Ako neki od ovih treba ipak ostati ručno uređivan na Confluenceu (a ne sync-ovan),
# samo ga ne ubacuj u page-id-map.json odnosno ne dodaj page_id u markdown frontmatter.
ROOT_PAGES = {
    "Ch.01": "240156678",   # 01-uvod-i-koncepti.md
    "Ch.02": "240254995",   # 02-korisnicko-iskustvo.md
    "Ch.03": "240156686",   # 03-korisnici-i-pristup.md
    "Ch.04": "240189477",   # 04-sadrzaj.md
    "Ch.05": "240189485",   # 05-moderacija.md
    "Ch.06": "240222244",   # 06-monetizacija.md
    "Ch.07": "240320540",   # 07-komunikacija.md
    "Ch.08": "240189509",   # 08-infrastruktura.md
    "MVP-SCOPE": "242188289",         # mvp-scope-opseg-prve-verzije.md
    "STATUS-MODEL-SPEC": "253526019", # novi-listing-statusni-model-specifikacija.md
}

# Regex za izvlačenje logičkog ID-a iz naslova Confluence stranice.
# Pattern matchuje:
#   E01 — ...        -> "E01"
#   E03a — ...       -> "E03a"
#   S01-01 — ...     -> "S01-01"
#   S03a-01 — ...    -> "S03a-01"
# Razdvajač između ID-a i ostatka može biti em-dash (—), en-dash (–) ili minus (-).
TITLE_ID_RE = re.compile(r"^(?P<id>[ESes]\d+[a-z]?(?:-\d+)?)\s*[—–-]")


# --------------------------------------------------------------------------
# HTTP helperi
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


def fetch_descendants(
    page_id: str, auth: HTTPBasicAuth, depth: int = 5
) -> Iterator[dict]:
    """
    Vrati sve descendants pod datim page_id, koristeći cursor paginaciju.
    `depth` kontroliše dubinu. Za 2-nivo (epic -> story) dovoljno je 2,
    ali stavljamo 5 da bismo bili sigurni za bilo koje nested stranice.
    """
    url = f"{CONFLUENCE_API_BASE}/pages/{page_id}/descendants"
    params = {"depth": depth, "limit": 250}
    while True:
        resp = requests.get(url, auth=auth, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        for page in data.get("results", []):
            yield page
        next_link = data.get("_links", {}).get("next")
        if not next_link:
            break
        # next_link je relativan na /wiki/, npr.
        # "/wiki/api/v2/pages/.../descendants?depth=1&cursor=..."
        # Skripta API base već uključuje /wiki/api/v2, pa moramo izgraditi pun URL.
        if next_link.startswith("/wiki/"):
            url = f"https://api.atlassian.com/ex/confluence/{CLOUD_ID}{next_link}"
        else:
            url = next_link
        params = None  # cursor je već u URL-u
        time.sleep(0.2)  # blagi rate limit hedging


# --------------------------------------------------------------------------
# Glavna logika
# --------------------------------------------------------------------------

def extract_id_from_title(title: str) -> str | None:
    m = TITLE_ID_RE.match(title.strip())
    if not m:
        return None
    return m.group("id")


def build_map(auth: HTTPBasicAuth, include_stale: bool = False) -> dict:
    """
    Vrati strukturu:
        {
            "generated_at": "...",
            "root_pages": { "Ch.01": "240156678", ... },
            "epics_and_stories": { "E01": "251232295", "S01-01": "251396116", ... },
            "unmapped": [ {"id": "...", "title": "...", "reason": "..."} ]
        }
    """
    epics_and_stories: dict[str, str] = {}
    unmapped: list[dict] = []
    duplicates: dict[str, list[dict]] = {}

    print(
        f"Skeniram descendants pod page ID {EPICS_AND_STORIES_ROOT} "
        f"(EPICS AND STORIES)...",
        file=sys.stderr,
    )

    count = 0
    for page in fetch_descendants(EPICS_AND_STORIES_ROOT, auth):
        count += 1
        status = page.get("status", "current")
        if status != "current" and not include_stale:
            continue

        title = page.get("title", "")
        page_id = page.get("id")
        logical_id = extract_id_from_title(title)

        if not logical_id:
            # Ovo su meta stranice tipa "Plan pisanja epica i storija",
            # "Pisanje Epica i User Storija — Instrukcija", itd.
            unmapped.append(
                {
                    "id": page_id,
                    "title": title,
                    "reason": "naslov ne počinje sa E##/S##-## patternom",
                }
            )
            continue

        if logical_id in epics_and_stories:
            duplicates.setdefault(logical_id, []).append(
                {"id": page_id, "title": title}
            )
            continue

        epics_and_stories[logical_id] = page_id

    print(f"Obrađeno {count} stranica.", file=sys.stderr)
    print(f"Mapirano: {len(epics_and_stories)} epica/storija.", file=sys.stderr)
    print(f"Nemapirano: {len(unmapped)} stranica.", file=sys.stderr)
    if duplicates:
        print(
            f"PAŽNJA: nađeno {len(duplicates)} duplikata "
            "(isti logički ID na više stranica). Vidi 'duplicates' u output-u.",
            file=sys.stderr,
        )

    return {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z") or time.strftime("%Y-%m-%dT%H:%M:%S"),
        "cloud_id": CLOUD_ID,
        "epics_and_stories_root": EPICS_AND_STORIES_ROOT,
        "root_pages": ROOT_PAGES,
        "epics_and_stories": dict(sorted(epics_and_stories.items())),
        "unmapped": unmapped,
        "duplicates": duplicates,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("page-id-map.json"),
        help="Output JSON fajl (default: page-id-map.json u trenutnom dir-u)",
    )
    parser.add_argument(
        "--include-stale",
        action="store_true",
        help="Uključi i arhivirane/obrisane stranice (default: samo current).",
    )
    args = parser.parse_args()

    auth = get_auth()
    result = build_map(auth, include_stale=args.include_stale)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Mapping zapisan u: {args.output.resolve()}", file=sys.stderr)

    # Brz sažetak na stdout-u za quick scan
    print()
    print("=== SAŽETAK ===")
    print(f"Root pages (ručno):      {len(result['root_pages'])}")
    print(f"Epics & stories (auto):  {len(result['epics_and_stories'])}")
    print(f"Unmapped (meta/ostalo):  {len(result['unmapped'])}")
    print(f"Duplicates:              {len(result['duplicates'])}")

    if result["unmapped"]:
        print("\nNemapirano (provjeri):")
        for u in result["unmapped"]:
            print(f"  - [{u['id']}] {u['title']}")

    if result["duplicates"]:
        print("\nDuplikati (mora se ručno riješiti):")
        for logical_id, pages in result["duplicates"].items():
            print(f"  - {logical_id}:")
            for p in pages:
                print(f"      - [{p['id']}] {p['title']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
