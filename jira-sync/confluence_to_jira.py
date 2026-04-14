#!/usr/bin/env python3
"""
CityInfo — Confluence → Jira sync
===================================
Čita epike i storije iz Confluence EPICS AND STORIES foldera,
te kreira odgovarajuće Epike i Story issue-e u Jiri.

Mod: DRY-RUN (--dry-run) — samo prikazuje šta bi se kreiralo, bez pisanja u Jiru.

Autor: CityInfo tim
Verzija: 1.0
"""

import os
import re
import json
import argparse
import requests
from typing import Optional

# ─────────────────────────────────────────────
# KONFIGURACIJA — postavi kao env varijable
# ─────────────────────────────────────────────
ATLASSIAN_EMAIL     = os.environ.get("ATLASSIAN_EMAIL", "")
ATLASSIAN_API_TOKEN = os.environ.get("ATLASSIAN_API_TOKEN", "")
CONFLUENCE_BASE_URL = "https://terraprojects.atlassian.net/wiki"
JIRA_BASE_URL       = "https://terraprojects.atlassian.net"
JIRA_PROJECT_KEY    = "CIT"

# Page ID glavnog EPICS AND STORIES foldera
EPICS_FOLDER_PAGE_ID = "250249231"

# Prefiksi koji označavaju epike i storije u naslovima
EPIC_PREFIX_RE  = re.compile(r"^E\d+[a-zA-Z]?[\s—–-]")
STORY_PREFIX_RE = re.compile(r"^S\d+-\d+[\s—–-]")


# ─────────────────────────────────────────────
# HTTP helperi
# ─────────────────────────────────────────────
def confluence_auth() -> tuple:
    return (ATLASSIAN_EMAIL, ATLASSIAN_API_TOKEN)


def jira_auth() -> tuple:
    return (ATLASSIAN_EMAIL, ATLASSIAN_API_TOKEN)


def confluence_get(path: str, params: dict = None) -> dict:
    """GET poziv prema Confluence REST API v2."""
    url = f"{CONFLUENCE_BASE_URL}/api/v2{path}"
    response = requests.get(url, auth=confluence_auth(), params=params or {})
    response.raise_for_status()
    return response.json()


def jira_post(path: str, body: dict) -> dict:
    """POST poziv prema Jira REST API v3."""
    url = f"{JIRA_BASE_URL}/rest/api/3{path}"
    response = requests.post(
        url,
        auth=jira_auth(),
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        json=body,
    )
    response.raise_for_status()
    return response.json()


# ─────────────────────────────────────────────
# Confluence helperi
# ─────────────────────────────────────────────
def get_child_pages(page_id: str) -> list[dict]:
    """Vraća direktnu djecu date stranice (depth=1)."""
    results = []
    cursor = None
    while True:
        params = {"limit": 50}
        if cursor:
            params["cursor"] = cursor
        data = confluence_get(f"/pages/{page_id}/children", params)
        results.extend(data.get("results", []))
        next_link = data.get("_links", {}).get("next")
        if not next_link:
            break
        # Izvuci cursor iz next linka
        m = re.search(r"cursor=([^&]+)", next_link)
        if not m:
            break
        cursor = m.group(1)
    return results


def get_page_content(page_id: str) -> dict:
    """Dohvata stranicu sa body sadržajem u markdown formatu."""
    data = confluence_get(f"/pages/{page_id}", params={"body-format": "storage"})
    # Dohvati markdown verziju odvojenim pozivom
    md_data = confluence_get(f"/pages/{page_id}", params={"body-format": "atlas_doc_format"})
    # Koristimo direktni API s representation=export_view za čisti tekst
    # Jednostavnije: koristimo pages API s body-format=markdown (Confluence API v2 podržava)
    return data


def get_page_markdown(page_id: str) -> tuple[str, str]:
    """
    Vraća (title, markdown_body) za datu stranicu.
    Koristi Confluence v1 API sa view reprezentacijom i pretvara HTML u
    tekst sa **bold** markerima potrebnim za parsing Excerpta i User Storija.
    """
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{page_id}"
    params = {"expand": "body.view"}
    response = requests.get(url, auth=confluence_auth(), params=params)
    response.raise_for_status()
    data = response.json()

    title = data.get("title", "")
    html_body = data.get("body", {}).get("view", {}).get("value", "")

    # Zamijeni block elemente sa newline-om
    text = re.sub(r"<br[^>]*>", "\n", html_body)
    text = re.sub(r"</p>", "\n", text)
    text = re.sub(r"</li>", "\n", text)
    text = re.sub(r"<li[^>]*>", "- ", text)
    # Pretvori <strong> tagove u ** marker (potreban za parse_section)
    text = re.sub(r"<strong>", "**", text)
    text = re.sub(r"</strong>", "**", text)
    # Ukloni sve ostale HTML tagove
    text = re.sub(r"<[^>]+>", "", text)
    # Dekodiraj HTML entitete
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&nbsp;", " ").replace("&#8212;", "\u2014").replace("&#x2019;", "'")
    # Normalizuj praznine
    text = re.sub(r"[ \t]+", " ", text)
    # Normalizuj višestruke prazne redove
    result = []
    prev_blank = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "":
            if not prev_blank:
                result.append("")
            prev_blank = True
        else:
            result.append(stripped)
            prev_blank = False

    return title, "\n".join(result).strip()


def get_page_url(page_id: str) -> str:
    """Vraća URL stranice na Confluenceu."""
    return f"{CONFLUENCE_BASE_URL}/pages/{page_id}"


# ─────────────────────────────────────────────
# Parseri za Excerpt i User Story
# ─────────────────────────────────────────────
def parse_section(text: str, marker: str) -> Optional[str]:
    """
    Izvlači sadržaj sekcije koja počinje sa `marker` (npr. '**Excerpt:**').
    Uzima tekst od markera do sljedeće bold sekcije ili kraja.
    """
    # Normalizuj razmake
    lines = text.splitlines()
    collecting = False
    section_lines = []

    for line in lines:
        # Provjeri da li linija sadrži marker (može biti u HTML ili plain textu)
        clean_line = re.sub(r"<[^>]+>", "", line).strip()

        if not collecting:
            # Tražimo početak sekcije
            if marker.lower().replace("**", "") in clean_line.lower():
                # Uzmi tekst iza markera na istoj liniji
                rest = re.sub(
                    re.escape(marker.replace("**", "")), "", clean_line,
                    count=1, flags=re.IGNORECASE
                ).strip(": ").strip()
                if rest:
                    section_lines.append(rest)
                collecting = True
        else:
            # Provjeri da li smo stigli do sljedeće bold sekcije
            # (linija koja počinje sa ** ili je heading)
            if re.match(r"^\*\*[A-ZŠĐČĆŽ]", clean_line) or re.match(r"^#{1,4}\s", clean_line):
                break
            if clean_line:
                section_lines.append(clean_line)

    result = " ".join(section_lines).strip()
    # Ukloni eventualni **** artefakt koji ostaje od praznog </strong><strong> para
    result = re.sub(r"^\*{2,4}\s*", "", result).strip()
    return result if result else None


def extract_excerpt(body: str) -> Optional[str]:
    """Izvlači Excerpt iz body teksta epica."""
    # Pokušaj različite varijante markera
    for marker in ["Excerpt:", "**Excerpt:**", "EXCERPT:"]:
        result = parse_section(body, marker)
        if result:
            return result
    return None


def extract_user_story(body: str) -> Optional[str]:
    """Izvlači User Story iz body teksta storije (format: Kao .../želim .../kako bih ...)."""
    for marker in ["User story:", "**User story:**", "UserStory:", "**UserStory:**"]:
        result = parse_section(body, marker)
        if result:
            return result

    # Fallback: traži "Kao " pattern direktno
    m = re.search(r"(Kao\s+.+?kako\s+bih\s+.+?)(?=\n\n|\Z)", body, re.DOTALL | re.IGNORECASE)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()

    return None


# ─────────────────────────────────────────────
# Jira kreator
# ─────────────────────────────────────────────
def build_epic_description(excerpt: str, confluence_url: str) -> dict:
    """
    Kreira Jira ADF (Atlassian Document Format) opis za Epic.
    Sadrži Excerpt i link na Confluence stranicu.
    """
    return {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": excerpt or "(Excerpt nije pronađen)"}]
            },
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "📄 Confluence: "},
                    {
                        "type": "text",
                        "text": confluence_url,
                        "marks": [{"type": "link", "attrs": {"href": confluence_url}}]
                    }
                ]
            }
        ]
    }


def build_story_description(user_story: str, confluence_url: str) -> dict:
    """
    Kreira Jira ADF opis za Story.
    Sadrži User Story citat i link na Confluence stranicu.
    """
    return {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "blockquote",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": user_story or "(User Story nije pronađen)"}]
                    }
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "📄 Confluence: "},
                    {
                        "type": "text",
                        "text": confluence_url,
                        "marks": [{"type": "link", "attrs": {"href": confluence_url}}]
                    }
                ]
            }
        ]
    }


def create_jira_epic(title: str, description: dict, dry_run: bool) -> Optional[str]:
    """Kreira Jira Epic i vraća issue key (npr. CIT-1)."""
    payload = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": title,
            "description": description,
            "issuetype": {"name": "Epic"},
        }
    }
    if dry_run:
        return None

    result = jira_post("/issue", payload)
    return result.get("key")


def create_jira_story(title: str, description: dict, epic_key: str, dry_run: bool) -> Optional[str]:
    """Kreira Jira Story unutar epica i vraća issue key."""
    payload = {
        "fields": {
            "project": {"key": JIRA_PROJECT_KEY},
            "summary": title,
            "description": description,
            "issuetype": {"name": "Story"},
        }
    }
    # Poveži sa epicom putem parent polja (Jira classic stil, hijerarhija Epic → Story)
    if epic_key:
        payload["fields"]["parent"] = {"key": epic_key}

    if dry_run:
        return None

    result = jira_post("/issue", payload)
    return result.get("key")


# ─────────────────────────────────────────────
# Čišćenje naslova
# ─────────────────────────────────────────────
def clean_title(raw_title: str) -> str:
    """
    Uklanja prefiks i separator iz naslova.
    'E01 — Korisnička registracija' → 'Korisnička registracija'
    'S01-01 — Registracija novog korisnika' → 'Registracija novog korisnika'
    """
    # Ukloni prefiks tipa "E01 — ", "E03a — ", "S01-01 — " itd.
    cleaned = re.sub(r"^[ES]\d+[a-zA-Z]?(-\d+)?\s*[—–\-]+\s*", "", raw_title).strip()
    return cleaned if cleaned else raw_title


# ─────────────────────────────────────────────
# GLAVNI TOK
# ─────────────────────────────────────────────
def run(dry_run: bool = True, epic_filter: str = None):
    print(f"\n{'='*60}")
    print(f"  CityInfo — Confluence → Jira sync")
    print(f"  Mod: {'DRY-RUN (nema pisanja u Jiru)' if dry_run else '🚀 LIVE — kreira issue-e u Jiri'}")
    if epic_filter:
        print(f"  Filter: samo epic '{epic_filter}'")
    print(f"{'='*60}\n")

    # Dohvati sve child stranice EPICS foldera
    print("📥 Dohvatam epike iz Confluencea...")
    all_children = get_child_pages(EPICS_FOLDER_PAGE_ID)

    # Filtriraj samo epike (naslovi koji počinju sa E## pattern)
    epic_pages = [p for p in all_children if EPIC_PREFIX_RE.match(p["title"])]
    print(f"   Pronađeno epika: {len(epic_pages)}\n")

    summary = []  # Za finalni ispis

    for epic_page in epic_pages:
        epic_page_id = epic_page["id"]
        epic_raw_title = epic_page["title"]

        # Opcionalni filter
        if epic_filter and epic_filter.lower() not in epic_raw_title.lower():
            continue

        epic_title = clean_title(epic_raw_title)
        epic_url = get_page_url(epic_page_id)

        print(f"📌 EPIC: {epic_raw_title}")

        # Dohvati sadržaj epica
        _, epic_body = get_page_markdown(epic_page_id)
        excerpt = extract_excerpt(epic_body)

        if not excerpt:
            print(f"   ⚠️  Excerpt nije pronađen u sadržaju epica!")
        else:
            print(f"   Excerpt: {excerpt[:80]}{'...' if len(excerpt) > 80 else ''}")

        # Kreiraj ili simuliraj kreiranje Jira Epica
        epic_description = build_epic_description(excerpt or "", epic_url)
        epic_key = create_jira_epic(epic_title, epic_description, dry_run)

        if dry_run:
            epic_key = f"{JIRA_PROJECT_KEY}-EPIC-{epic_raw_title[:10].replace(' ', '')}"
            print(f"   [DRY-RUN] Epic bi se kreirao: '{epic_title}'")
        else:
            print(f"   ✅ Epic kreiran: {epic_key}")

        epic_summary = {
            "epic_title": epic_title,
            "confluence_page_id": epic_page_id,
            "jira_key": epic_key if not dry_run else "(dry-run)",
            "excerpt_found": excerpt is not None,
            "stories": []
        }

        # Dohvati storije (child stranice epica)
        story_pages = get_child_pages(epic_page_id)
        story_pages = [p for p in story_pages if STORY_PREFIX_RE.match(p["title"])]
        print(f"   Pronađeno storija: {len(story_pages)}")

        for story_page in story_pages:
            story_page_id = story_page["id"]
            story_raw_title = story_page["title"]
            story_title = clean_title(story_raw_title)
            story_url = get_page_url(story_page_id)

            _, story_body = get_page_markdown(story_page_id)
            user_story = extract_user_story(story_body)

            if not user_story:
                print(f"   ⚠️  [{story_raw_title}] User Story nije pronađen!")
            
            story_description = build_story_description(user_story or "", story_url)
            story_key = create_jira_story(
                story_title,
                story_description,
                epic_key if not dry_run else None,
                dry_run
            )

            if dry_run:
                print(f"      [DRY-RUN] Story bi se kreirao: '{story_title}'")
            else:
                print(f"      ✅ Story kreiran: {story_key}")

            epic_summary["stories"].append({
                "story_title": story_title,
                "confluence_page_id": story_page_id,
                "jira_key": story_key if not dry_run else "(dry-run)",
                "user_story_found": user_story is not None,
            })

        summary.append(epic_summary)
        print()

    # Finalni JSON izvještaj
    print(f"\n{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}")
    total_epics  = len(summary)
    total_stories = sum(len(e["stories"]) for e in summary)
    missing_excerpts = sum(1 for e in summary if not e["excerpt_found"])
    missing_stories  = sum(
        1 for e in summary for s in e["stories"] if not s["user_story_found"]
    )
    print(f"  Epika:   {total_epics}")
    print(f"  Storija: {total_stories}")
    if missing_excerpts:
        print(f"  ⚠️  Epika bez Excerpta:     {missing_excerpts}")
    if missing_stories:
        print(f"  ⚠️  Storija bez User Story: {missing_stories}")

    # Spremi JSON dump
    output_path = "confluence_to_jira_dryrun.json" if dry_run else "confluence_to_jira_result.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"\n  📄 Detaljan izvještaj: {output_path}")
    print(f"{'='*60}\n")


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CityInfo: Confluence → Jira sync skript"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Prikaži šta bi se kreiralo, bez pisanja u Jiru (default: uključeno)"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Stvarno kreiraj issue-e u Jiri (overriduje --dry-run)"
    )
    parser.add_argument(
        "--epic",
        type=str,
        default=None,
        help="Filtriraj samo jedan epic po dijelu naslova, npr. --epic E01"
    )
    args = parser.parse_args()

    dry_run_mode = not args.live  # --live isključuje dry-run

    # Provjera kredencijala
    if not ATLASSIAN_EMAIL or not ATLASSIAN_API_TOKEN:
        print("❌ Greška: ATLASSIAN_EMAIL i ATLASSIAN_API_TOKEN moraju biti postavljeni kao env varijable.")
        print("   export ATLASSIAN_EMAIL='tvoj@email.com'")
        print("   export ATLASSIAN_API_TOKEN='tvoj-api-token'")
        exit(1)

    run(dry_run=dry_run_mode, epic_filter=args.epic)
