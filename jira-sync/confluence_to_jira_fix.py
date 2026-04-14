#!/usr/bin/env python3
"""
CityInfo — Jira description fix
=================================
Azurira opise postojecih Jira issue-a (Epika i Storija) sa ispravnim
sadrzajem iz Confluencea:
  - Epic opis: samo Excerpt + Confluence link
  - Story opis: samo User story citat (blockquote) + Confluence link

Koristi ugradjenu staticku mapu Jira key -> Confluence page ID.
NE koristi Jira search API (ne radi sa Basic Auth na ovom planu).

Pokretanje:
  py confluence_to_jira_fix.py              # dry-run sve
  py confluence_to_jira_fix.py --epic CIT-1 # dry-run jedan epic
  py confluence_to_jira_fix.py --live       # azuriraj sve
"""

import os
import re
import time
import argparse
import requests
from typing import Optional

ATLASSIAN_EMAIL     = os.environ.get("ATLASSIAN_EMAIL", "")
ATLASSIAN_API_TOKEN = os.environ.get("ATLASSIAN_API_TOKEN", "")
CONFLUENCE_BASE_URL = "https://terraprojects.atlassian.net/wiki"
JIRA_CLOUD_ID       = "45983047-331b-459e-b1a5-052825171c8c"
JIRA_BASE_URL       = f"https://api.atlassian.com/ex/jira/{JIRA_CLOUD_ID}"
API_DELAY           = 0.4

EPIC_CONFLUENCE_MAP = {
    "CIT-1":  "251232295",
    "CIT-10": "251330580",
    "CIT-20": "251297793",
    "CIT-21": "251691009",
    "CIT-22": "251854849",
    "CIT-30": "252084225",
    "CIT-37": "250478652",
    "CIT-43": "251265065",
    "CIT-50": "252018708",
    "CIT-56": "252411905",
    "CIT-61": "252280852",
    "CIT-68": "252706817",
    "CIT-74": "252575764",
    "CIT-80": "250970205",
    "CIT-88": "251199489",
}

STORY_MAP = {
    "CIT-1":  [("CIT-2","Registracija novog korisnika"),("CIT-3","Email verifikacija"),("CIT-4","Verifikacija telefona (SMS)"),("CIT-5","Login, logout i session management"),("CIT-6","Zaboravljena lozinka i reset"),("CIT-7","Korisni\u010dki profil \u2014 pregled i ure\u0111ivanje"),("CIT-8","Brisanje korisni\u010dkog ra\u010duna (GDPR)"),("CIT-9","Dvofaktorska autentifikacija (2FA) za korisnike")],
    "CIT-10": [("CIT-11","Kreiranje Event listinga sa osnovnim podacima"),("CIT-12","Kreiranje Place listinga sa osnovnim podacima"),("CIT-13","Lokacija Event-a \u2014 povezivanje sa Place-om ili ru\u010dna adresa"),("CIT-14","Event hijerarhija \u2014 kreiranje i upravljanje child eventima"),("CIT-15","Upload i upravljanje slikama listinga"),("CIT-16","Upload i upravljanje dokumentima listinga"),("CIT-17","Objava listinga i statusne tranzicije"),("CIT-18","Editovanje, brisanje i sakrivanje listinga"),("CIT-19","Ru\u010dno osvje\u017eavanje sortDate i pra\u0107enje statusa objave")],
    "CIT-20": [],
    "CIT-21": [],
    "CIT-22": [("CIT-23","Naslovna stranica sa dva re\u017eima i promocijskim prioritetima"),("CIT-24","Full-text pretraga sa alias mapiranjem"),("CIT-25","Autosuggest pri pretrazi"),("CIT-26","Filtriranje po kategoriji, tagu i datumu"),("CIT-27","Lokacijski dijalog i filter po udaljenosti"),("CIT-28","Sortiranje po sortDate sa promocijskim prioritetima i paginacija"),("CIT-29","Responsive dizajn i mobile-first layout")],
    "CIT-30": [("CIT-31","Card komponenta za prikaz listinga u listama"),("CIT-32","Detaljna stranica listinga"),("CIT-33","Lajkovi za registrovane korisnike i visitore"),("CIT-34","Favoriti (Saved listings)"),("CIT-35","Dijeljenje listinga"),("CIT-36","Related content na detail stranici")],
    "CIT-37": [("CIT-38","Automatska evaluacija Trust Tier napredovanja"),("CIT-39","Automatska degradacija na Restricted (Tier 0)"),("CIT-40","Ru\u010dna promjena Trust Tier-a"),("CIT-41","isVerifiedPublisher flag \u2014 postavljanje i efekti"),("CIT-42","Pre-moderacija limit za Tier 0 i 1")],
    "CIT-43": [("CIT-44","Moderacijski queue \u2014 struktura, prioritizacija i claim/release"),("CIT-45","Moderatorske odluke (approve, reject, changes_requested)"),("CIT-46","AI content screening i scoring"),("CIT-47","AI blocking logic i override"),("CIT-48","Sampling logika za post-moderaciju"),("CIT-49","Moderacija editovanog sadr\u017eaja")],
    "CIT-50": [("CIT-51","Automatsko kreiranje message thread-a uz listing"),("CIT-52","Slanje poruke moderatora vlasniku listinga"),("CIT-53","Odgovor vlasnika listinga na poruku moderatora"),("CIT-54","Referenciranje dokumenata u porukama"),("CIT-55","Pregled i upravljanje thread-ovima u Staff panelu")],
    "CIT-56": [("CIT-57","Kreiranje wallet-a pri registraciji korisnika"),("CIT-58","Prikaz kredit paketa i kupovina kredita"),("CIT-59","Prikaz wallet stanja i historije transakcija"),("CIT-60","Admin upravljanje kreditima")],
    "CIT-61": [("CIT-62","Kreiranje i aktivacija promocije listinga"),("CIT-63","Prikaz promotivnih listinga (sortiranje i vizualno isticanje)"),("CIT-64","AutoRenew mehanizam za automatsko osvje\u017eavanje pozicije"),("CIT-65","Pauziranje i nastavak promocije"),("CIT-66","Ru\u010dno osvje\u017eavanje pozicije listinga"),("CIT-67","Pregled i upravljanje promocijama")],
    "CIT-68": [("CIT-69","Kreiranje i upravljanje display oglasima (Staff)"),("CIT-70","Prikaz banner oglasa na javnom frontendu"),("CIT-71","Pra\u0107enje impressions i clicks"),("CIT-72","Pregled statistike display oglasa (Staff)"),("CIT-73","Upravljanje reklamnim zonama")],
    "CIT-74": [("CIT-75","Kreiranje i slanje in-app notifikacija"),("CIT-76","Prikaz notifikacija i badge nepro\u010ditanih"),("CIT-77","Slanje email notifikacija"),("CIT-78","Notifikacije za listing lifecycle doga\u0111aje"),("CIT-79","Notifikacije za promocije i Trust Tier")],
    "CIT-80": [("CIT-81","Staff login i session management"),("CIT-82","Promjena lozinke i politika rotacije"),("CIT-83","Kreiranje Staff naloga"),("CIT-84","Pregled i upravljanje Staff nalozima"),("CIT-85","Dodjela i oduzimanje moderatorskih permisija"),("CIT-86","Upravljanje tenant pristupom za Staff"),("CIT-87","Staff panel shell i navigacija")],
    "CIT-88": [("CIT-89","Postavljanje repozitorija i razvojnog okru\u017eenja"),("CIT-90","Inicijalni .NET 10 API projekat sa middleware-om"),("CIT-91","Inicijalni SvelteKit frontend projekat"),("CIT-92","Inicijalna DB schema i migracije"),("CIT-93","Single-tenant konfiguracija za Sarajevo"),("CIT-94","i18n framework i lokalizacija"),("CIT-95","CI/CD pipeline")],
}


def auth():
    return (ATLASSIAN_EMAIL, ATLASSIAN_API_TOKEN)


def jira_put(issue_key, body):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"
    r = requests.put(url, auth=auth(),
                     headers={"Accept": "application/json", "Content-Type": "application/json"},
                     json=body)
    if r.status_code not in (200, 204):
        raise Exception(f"PUT {issue_key} failed {r.status_code}: {r.text[:300]}")


def confluence_get_page(page_id):
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{page_id}"
    r = requests.get(url, auth=auth(), params={"expand": "body.view"})
    r.raise_for_status()
    d = r.json()
    title = d.get("title", "")
    html = d.get("body", {}).get("view", {}).get("value", "")
    return title, html_to_text(html)


def confluence_get_children(page_id):
    results = []
    cursor = None
    while True:
        url = f"{CONFLUENCE_BASE_URL}/api/v2/pages/{page_id}/children"
        params = {"limit": 50}
        if cursor:
            params["cursor"] = cursor
        r = requests.get(url, auth=auth(), params=params)
        r.raise_for_status()
        d = r.json()
        results.extend(d.get("results", []))
        nl = d.get("_links", {}).get("next")
        if not nl:
            break
        m = re.search(r"cursor=([^&]+)", nl)
        if not m:
            break
        cursor = m.group(1)
    return results


def html_to_text(html):
    t = re.sub(r"<br[^>]*>", "\n", html)
    t = re.sub(r"</p>", "\n", t)
    t = re.sub(r"</li>", "\n", t)
    t = re.sub(r"<li[^>]*>", "- ", t)
    t = re.sub(r"<strong>", "**", t)
    t = re.sub(r"</strong>", "**", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    t = t.replace("&nbsp;", " ").replace("&#8212;", "\u2014").replace("&#x2019;", "'")
    t = re.sub(r"[ \t]+", " ", t)
    result, prev_blank = [], False
    for line in t.splitlines():
        s = line.strip()
        if s == "":
            if not prev_blank:
                result.append("")
            prev_blank = True
        else:
            result.append(s)
            prev_blank = False
    return "\n".join(result).strip()


def parse_section(text, marker):
    lines = text.splitlines()
    collecting = False
    buf = []
    for line in lines:
        c = line.strip()
        if not collecting:
            if marker.lower().replace("**", "") in c.lower():
                rest = re.sub(re.escape(marker.replace("**", "")), "", c, count=1, flags=re.IGNORECASE).strip(": ").strip()
                if rest:
                    buf.append(rest)
                collecting = True
        else:
            if re.match(r"^\*\*[A-Z\u0160\u0110\u010c\u0106\u017d]", c) or re.match(r"^#{1,4}\s", c):
                break
            if c:
                buf.append(c)
    result = " ".join(buf).strip()
    result = re.sub(r"^\*{2,4}\s*", "", result).strip()
    return result if result else None


def extract_excerpt(text):
    for m in ["**Excerpt:**", "Excerpt:"]:
        r = parse_section(text, m)
        if r:
            return r
    return None


def extract_user_story(text):
    for m in ["**User story:**", "**UserStory:**", "User story:", "UserStory:"]:
        r = parse_section(text, m)
        if r:
            return r
    match = re.search(r"(Kao\s+.+?kako\s+bih\s+[^\n]+)", text, re.DOTALL | re.IGNORECASE)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    return None


def conf_url(page_id):
    return f"{CONFLUENCE_BASE_URL}/pages/viewpage.action?pageId={page_id}"


def build_epic_desc(excerpt, page_id, title=""):
    u = conf_url(page_id)
    return {"version": 1, "type": "doc", "content": [
        {"type": "paragraph", "content": [{"type": "text", "text": excerpt}]},
        {"type": "paragraph", "content": [
            {"type": "inlineCard", "attrs": {"url": u}}
        ]}
    ]}


def build_story_desc(user_story, page_id, title=""):
    u = conf_url(page_id)
    return {"version": 1, "type": "doc", "content": [
        {"type": "blockquote", "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": user_story}]}
        ]},
        {"type": "paragraph", "content": [
            {"type": "inlineCard", "attrs": {"url": u}}
        ]}
    ]}


STORY_PREFIX_RE = re.compile(r"^S\d+-\d+[\s\u2014\u2013\-]")


def build_story_conf_map(epic_conf_id):
    children = confluence_get_children(epic_conf_id)
    result = {}
    for child in children:
        raw = child["title"]
        if STORY_PREFIX_RE.match(raw):
            clean = re.sub(r"^S\d+-\d+\s*[\u2014\u2013\-]+\s*", "", raw).strip()
            result[clean] = child["id"]
    return result


def run(dry_run=True, epic_filter=None, story_filter=None):
    print(f"\n{'='*60}")
    print(f"  CityInfo \u2014 Jira description fix")
    print(f"  Mod: {'DRY-RUN' if dry_run else 'LIVE \u2014 azurira Jiru'}")
    if epic_filter:
        print(f"  Filter: {epic_filter.upper()}")
    print(f"{'='*60}\n")

    stats = {"epics_ok": 0, "epics_warn": 0, "stories_ok": 0, "stories_warn": 0}

    for epic_key, conf_page_id in EPIC_CONFLUENCE_MAP.items():
        if epic_filter and epic_filter.upper() != epic_key:
            continue

        print(f"\U0001f4cc {epic_key}")

        try:
            _, epic_text = confluence_get_page(conf_page_id)
            excerpt = extract_excerpt(epic_text)
            if not excerpt:
                print(f"   \u26a0\ufe0f  Excerpt nije pronadjen \u2014 preskacemo")
                stats["epics_warn"] += 1
            else:
                short = excerpt[:90] + ("..." if len(excerpt) > 90 else "")
                print(f"   Excerpt: {short}")
                if not dry_run:
                    jira_put(epic_key, {"fields": {"description": build_epic_desc(excerpt, conf_page_id, title=epic_text.splitlines()[0].replace("**Naslov:**", "").strip() if epic_text else "")}})
                    time.sleep(API_DELAY)
                    print(f"   \u2705 Epic {epic_key} azuriran")
                else:
                    print(f"   [DRY-RUN] Epic {epic_key} bi se azurirao")
                stats["epics_ok"] += 1
        except Exception as e:
            print(f"   \u274c Greska za epic: {e}")
            stats["epics_warn"] += 1
            continue

        stories = STORY_MAP.get(epic_key, [])
        if not stories:
            print(f"   (nema storija)\n")
            continue

        try:
            story_conf_map = build_story_conf_map(conf_page_id)
        except Exception as e:
            print(f"   \u274c Greska pri dohvatanju Confluence child stranica: {e}")
            continue

        print(f"   Storija: {len(stories)}")

        for story_key, story_title in stories:
            if story_filter and story_filter.upper() != story_key:
                continue
            story_conf_id = story_conf_map.get(story_title)
            if not story_conf_id:
                for ct, cid in story_conf_map.items():
                    if ct.lower().strip() == story_title.lower().strip():
                        story_conf_id = cid
                        break
            if not story_conf_id:
                print(f"      \u26a0\ufe0f  {story_key} '{story_title}' \u2014 Confluence stranica nije pronadjena")
                stats["stories_warn"] += 1
                continue
            try:
                _, story_text = confluence_get_page(story_conf_id)
                user_story = extract_user_story(story_text)
                if not user_story:
                    print(f"      \u26a0\ufe0f  {story_key} \u2014 User story nije pronadjen")
                    stats["stories_warn"] += 1
                    continue
                short_us = user_story[:90] + ("..." if len(user_story) > 90 else "")
                if not dry_run:
                    jira_put(story_key, {"fields": {"description": build_story_desc(user_story, story_conf_id, title=story_title)}})
                    time.sleep(API_DELAY)
                    print(f"      \u2705 {story_key}: {short_us}")
                else:
                    print(f"      [DRY-RUN] {story_key}: {short_us}")
                stats["stories_ok"] += 1
            except Exception as e:
                print(f"      \u274c {story_key} greska: {e}")
                stats["stories_warn"] += 1

        print()

    print(f"{'='*60}")
    print(f"  SUMMARY {'(DRY-RUN)' if dry_run else '(LIVE)'}")
    print(f"{'='*60}")
    print(f"  Epika azurirano:        {stats['epics_ok']}")
    print(f"  Storija azurirano:      {stats['stories_ok']}")
    if stats["epics_warn"]:
        print(f"  \u26a0\ufe0f  Epika s problemom:   {stats['epics_warn']}")
    if stats["stories_warn"]:
        print(f"  \u26a0\ufe0f  Storija s problemom: {stats['stories_warn']}")
    print(f"  Ukupno:                 {stats['epics_ok'] + stats['stories_ok']}")
    print(f"{'='*60}\n")
    if dry_run:
        print("  Pokreni sa --live da stvarno azuriras issue-e.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--epic", type=str, default=None,
        help="Filtriraj po epicu, npr. --epic CIT-1")
    parser.add_argument("--story", type=str, default=None,
        help="Ažuriraj samo jednu storiju, npr. --story CIT-42")
    args = parser.parse_args()

    if not ATLASSIAN_EMAIL or not ATLASSIAN_API_TOKEN:
        print("Greska: postavi ATLASSIAN_EMAIL i ATLASSIAN_API_TOKEN env varijable.")
        exit(1)

    run(dry_run=not args.live, epic_filter=args.epic, story_filter=args.story)
