# md2conf migracija — handoff za sljedeću sesiju

> **Kreirano:** 30.4.2026.
> **Svrha:** Nastavak rada na md2conf integraciji u CityInfo dokumentaciji.
> Ovaj fajl pokupiti na početku sljedeće sesije i pokazati AI-u.

---

## TL;DR — gdje smo stali

**Faza 0, 1, 2 i 3 su gotove.** Markdown SSoT u GitHub-u → Confluence sync radi
preko `md2conf` alata. 115 fajlova sinhronizirano. Template instrukcije za
pisanje epica/storija ažuriran na **v1.2** (md2conf-compatible).

**Trenutno stanje:** gotovo sve commit-irano, instrukcija template ažuriran na
sva tri mjesta (markdown SSoT + epics-and-stories interna kopija + Confluence
page 251068418). **Korak 7 (Claude.ai project knowledge update) ostaje
manualno preko UI-a — to AI ne može uraditi.**

**Što slijedi (ako se nastavi):**
- Faza 4: GitHub Actions automatizacija (push u main → md2conf)
- Faza 5: Operating manual u repou
- Bot user za md2conf (umjesto Zoranovog naloga)

---

## Stanje projekta

### Šta je urađeno

| Faza | Šta | Status |
|------|-----|--------|
| 0 | Page ID inventory (`build_page_id_map.py`) | ✅ |
| 1 | `confluence_page_id` injection u sve epic/story fajlove | ✅ |
| 1 | `title` injection u sve fajlove | ✅ |
| 1 | Frontmatter za chapter fajlove | ✅ |
| 2 | Cleanup epica/storija (H1, bold-bold, user story format) | ✅ |
| 2 | User story italic + soft breaks | ✅ |
| 2 | `--no-generated-by` flag — banner uklonjen | ✅ |
| 2 | Cross-folder linkovi rezolvirani | ✅ |
| 2 | Stale `../project-specs/` linkovi popravljeni | ✅ |
| 2 | Persone link → direktan Confluence URL | ✅ |
| 2 | Root `.mdignore` (tooling foldere isključuje) | ✅ |
| 2 | 89 storija + 15 epica + 10 chapter fajlova pushano | ✅ |
| 3 | Template instrukcije v1.2 napravljen | ✅ |
| 3 | v1.2 pushan na sva tri mjesta (root, epics-and-stories, Confluence) | ✅ |
| 3 | Claude.ai project knowledge update | ⏳ MANUALNO |

### Šta NIJE urađeno (sljedeće sesije)

- [ ] **Manualno:** Update `cityinfo-epics-stories-instructions.md` u Claude.ai
  project knowledge (preko UI-a — vidi "Manualni koraci za Zorana" niže)
- [ ] GitHub Actions automatizacija (push u main → md2conf)
- [ ] Operating manual u repou (`md2conf-tooling/README.md` ažurirati ili
  novi `OPERATING.md`)
- [ ] Bot user za Confluence (umjesto Zoranovog ATLASSIAN_API_TOKEN)
- [ ] Sitne kozmetičke popravke u chapter fajlovima (header u tabeli,
  razmak iza bold close)

---

## Konfiguracija

### Atlassian

```
Cloud ID:        45983047-331b-459e-b1a5-052825171c8c
Domain:          terraprojects.atlassian.net
Space ID:        98463 (GI space)
Confluence API:  https://api.atlassian.com/ex/confluence/{cloudId}/
Auth:            Basic Auth sa ATLASSIAN_EMAIL + ATLASSIAN_API_TOKEN
```

### Repo

```
Putanja:         C:\Users\zoran\source\repos\cityinfo_documentation
Branch:          main
Venv:            .venv (PowerShell aktivacija: .\.venv\Scripts\Activate.ps1)
md2conf path:    md2conf-tooling/
md2conf alat:    pip package "markdown-to-confluence" (hunyadi/md2conf)
```

### Ključne Confluence stranice

| Naslov | Page ID |
|--------|---------|
| EPICS AND STORIES (parent folder) | 250249231 |
| Pisanje Epica i User Storija — Instrukcija | 251068418 |
| Plan pisanja epica i storija | 250970134 |
| Migracija statusnog modela (tracking) | 253853698 |
| Novi listing statusni model — specifikacija | 253526019 |
| Persone i korisnička putovanja | 243040257 |
| Project Index | 240812033 |
| Ch.01 (Uvod i koncepti) | 240156678 |
| Ch.02 (Korisničko iskustvo) | 240254995 |
| Ch.03 (Korisnici i pristup) | 240156686 |
| Ch.04 (Sadržaj) | 240189477 |
| Ch.05 (Moderacija) | 240189485 |
| Ch.06 (Monetizacija) | 240222244 |
| Ch.07 (Komunikacija) | 240320540 |
| Ch.08 (Infrastruktura) | 240189509 |
| MVP SCOPE | 242188289 |

---

## md2conf workflow (kako to radi sad)

### Komanda za push

```powershell
cd C:\Users\zoran\source\repos\cityinfo_documentation
.\.venv\Scripts\Activate.ps1
md2conf "." --no-generated-by -l info 2>&1 | Tee-Object -FilePath md2conf-push.log
```

### Šta md2conf radi

1. Skenira sve `*.md` fajlove iz repo root-a (rekurzivno)
2. Preskače sve u `.mdignore` listama (root + epics-and-stories)
3. Preskače sve hidden direktorije (`.git`, `.venv`, `.claude`, `.vscode`)
4. Za svaki fajl sa `confluence_page_id` u frontmatter-u:
   - Detektuje promjene preko checksum-a
   - Update-uje postojeću Confluence stranicu ako ima izmjena
   - Ostavlja netaknut ako nije mijenjan (idempotentno)
5. Za fajl bez `confluence_page_id`:
   - Kreira novu Confluence stranicu pod root parent-om
   - Upisuje page ID nazad u markdown frontmatter

Trajanje: ~3-5 minuta za 115 fajlova.

### Idempotentnost

Drugi run na istim fajlovima → sve `Up-to-date page (matching checksum)`,
**0 update-a**. Sigurno je pokretati md2conf po potrebi.

---

## Tooling u `md2conf-tooling/`

Sve skripte u `C:\Users\zoran\source\repos\cityinfo_documentation\md2conf-tooling\`.

| Skripta | Svrha | Kada se koristi |
|---------|-------|-----------------|
| `build_page_id_map.py` | Skenira Confluence i mapira logičke ID → page ID | Kad se kreiraju nove stranice |
| `inject_page_ids.py` | Upisuje `confluence_page_id` u frontmatter | Legacy, jednokratno (gotovo) |
| `inject_titles.py` | Upisuje `title` u frontmatter (preko Confluence API-ja) | Legacy, jednokratno (gotovo) |
| `add_chapter_frontmatter.py` | Dodaje frontmatter na chapter fajlove | Legacy, jednokratno (gotovo) |
| `markdown_cleanup.py` | Cleanup: H1 duplikat, bold-bold, user story breaks | Po potrebi (npr. kad se uvozi novi fajl) |
| `markdown_userstory_format.py` | User story u italic + soft line breaks | Po potrebi |
| `fix_project_specs_links.py` | Stale `../project-specs/` linkove popravlja | Legacy, jednokratno (gotovo) |
| `page-id-map.json` | Output `build_page_id_map.py` (committed) | Reference za skripte |
| `requirements.txt` | Python deps (`requests>=2.28.0`) | — |
| `README.md` | Dokumentacija (treba ažuriranje za novu sesiju) | — |

**Skripte koje su važne za novi epic/story workflow:**
- `markdown_cleanup.py` — popravlja sitnice u markdownu
- `markdown_userstory_format.py` — User story format

**Ostale skripte su legacy** (jednokratno korištene za migraciju).

---

## Repo struktura

```
cityinfo_documentation/
├── .gitignore                              ← ignoruje *.log, *.csf, .venv
├── .mdignore                               ← root mdignore (10 linija)
├── .venv/                                  ← Python venv (hidden, auto-skip)
├── .git/                                   ← Git (hidden, auto-skip)
├── 01-uvod-i-koncepti.md                   ← chapter, frontmatter, page_id 240156678
├── 02-korisnicko-iskustvo.md               ← chapter
├── 03-korisnici-i-pristup.md               ← chapter
├── 04-sadrzaj.md                           ← chapter
├── 05-moderacija.md                        ← chapter
├── 06-monetizacija.md                      ← chapter
├── 07-komunikacija.md                      ← chapter
├── 08-infrastruktura.md                    ← chapter
├── mvp-scope-opseg-prve-verzije.md         ← MVP scope
├── novi-listing-statusni-model-specifikacija.md  ← Status spec
├── audit-report.md                         ← internal (excluded)
├── CLAUDE.md                               ← internal (excluded)
├── CLAUDE-13-to-12.md                      ← internal (excluded)
├── README.md                               ← internal (excluded)
├── cityinfo-epics-stories-instructions.md  ← AI prompt instrukcija (excluded)
├── jira-sync/                              ← excluded folder
├── md2conf-tooling/                        ← excluded folder
└── epics-and-stories/
    ├── .mdignore                           ← interna ignoruje plan + instrukciju
    ├── plan-pisanja-epica-i-storija.md     ← internal (excluded)
    ├── pisanje-epica-i-user-storija-instrukcija.md  ← v1.2, sync na page 251068418
    ├── e01-...md                           ← epic
    ├── e01-.../                            ← story folder
    │   ├── s01-01-...md
    │   └── ...
    └── ...
```

### Sadržaj `.mdignore` fajlova

**Root `.mdignore`** (`C:\...\cityinfo_documentation\.mdignore`):
```
# Internal documentation that doesn't sync to Confluence
audit-report.md
CLAUDE.md
CLAUDE-13-to-12.md
cityinfo-epics-stories-instructions.md
README.md

# Tooling folders (bare names, no trailing slash!)
jira-sync
md2conf-tooling

# Generated artifacts
*.csf
```

**`epics-and-stories/.mdignore`**:
```
# Internal planning and instruction docs - NOT synced to Confluence
plan-pisanja-epica-i-storija.md
pisanje-epica-i-user-storija-instrukcija.md
```

**Napomena:** md2conf `.mdignore` koristi **fnmatch glob patterne**. Pravila ne
smiju sadržavati `/`. Hidden direktorije (`.git`, `.venv`) automatski preskaču.

---

## Pravila pisanja novih epica/storija (v1.2)

### Frontmatter format (OBAVEZNO)

**Epic:**
```yaml
---
id: E01
phase: MVP
journey_milestones: [J-01]
personas: [Marko, Ana, Thomas, Lejla]
story_count: 8
title: "E01 — Korisnička registracija i profil"
confluence_page_id: ""
---
```

**Story:**
```yaml
---
id: S01-01
parent_epic: E01
phase: MVP
journey_milestones: [J-01]
type: fullstack
title: "S01-01 — Registracija novog korisnika"
confluence_page_id: ""
---
```

### Pravila

1. `title` mora biti identičan Confluence page title-u
2. `confluence_page_id` ostaje `""` pri kreiranju (md2conf ga popunjava)
3. **NE pisati H1 heading u tijelu** (duplikat title-a)
4. Body počinje **direktno sa `**Naslov:**` linijom**
5. User story u **italic + soft break** formatu:
   ```markdown
   **User story:**

   *Kao [tip korisnika],*  ← 2 razmaka na kraju
   *želim [cilj],*  ← 2 razmaka na kraju
   *kako bih [benefit].*  ← bez razmaka
   ```
6. **Bold label sa vrijednošću u istoj liniji** — bez drugog bold-a
   (`**Phase:** MVP`, NE `**Phase:** **MVP**`)

Detaljna pravila u `cityinfo-epics-stories-instructions.md` (root) i
`epics-and-stories/pisanje-epica-i-user-storija-instrukcija.md`.

---

## Manualni koraci za Zorana (poslije zadnje sesije, prije nove)

### KRITIČNO: Update Claude.ai project knowledge

**Bez ovog koraka, AI će u sljedećoj sesiji koristiti staru v1.1 instrukciju!**

1. Otvori claude.ai u browseru
2. Idi u CityInfo projekat
3. **Project knowledge** sekcija (sa strane)
4. Pronađi `cityinfo-epics-stories-instructions.md` u listi
5. **Obriši** stari fajl
6. **Upload** novi `cityinfo-epics-stories-instructions.md` iz repoa
   (`C:\Users\zoran\source\repos\cityinfo_documentation\cityinfo-epics-stories-instructions.md`)

Trajanje: 1 minuta.

### Provjera (poslije Claude.ai update-a)

Otvori novu sesiju u Claude.ai i provjeri da li v1.2 sadržaj postoji u
project knowledge:
```
Pretraga unutar fajla: "1.2"
```
Trebao bi pronaći verziju u changelog-u.

---

## Git status zadnji poznat

```
On branch main
Your branch is up to date with 'origin/main'.
```

Zadnji commit (8cd233a):
```
8cd233a chore: ignore md2conf log files
```

**Šta još treba commit-irati nakon zadnjeg push-a:**

Ako je Korak 4 (vrati `pisanje-...md` u `.mdignore`) i Korak 5 (zamjena root fajla)
i Korak 6 (commit) urađeni — nema neispitanog rada.

Ako nisu — trebaju biti ovi koraci:

```powershell
# Korak 4: vrati u .mdignore
Add-Content "epics-and-stories\.mdignore" "pisanje-epica-i-user-storija-instrukcija.md"

# Korak 5: kopiraj sadržaj v1.2 u root cityinfo-epics-stories-instructions.md
# (preskoči prvih 4 linije frontmatter-a)
Get-Content "epics-and-stories\pisanje-epica-i-user-storija-instrukcija.md" | Select-Object -Skip 4 | Set-Content "cityinfo-epics-stories-instructions.md" -Encoding utf8

# Korak 6: commit
git add .
git commit -m "docs: update epics-and-stories instructions to v1.2 (md2conf integration)"
git push
```

---

## Sljedeće faze (kandidati za rad u novoj sesiji)

### Faza 4: GitHub Actions automatizacija

**Cilj:** Push u main automatski pokreće md2conf, Confluence sync se dešava
bez ručne intervencije.

**Šta treba:**
1. GitHub Actions workflow fajl (`.github/workflows/md2conf-sync.yml`)
2. GitHub Secrets za:
   - `ATLASSIAN_EMAIL`
   - `ATLASSIAN_API_TOKEN`
   - `CONFLUENCE_DOMAIN` (ili hardcoded)
   - `CONFLUENCE_SPACE_KEY` (ili hardcoded)
3. Workflow koraci:
   - Checkout repo
   - Setup Python
   - `pip install markdown-to-confluence`
   - Run md2conf sa env vars
4. Bot user za Confluence (sigurnije od ličnog tokena)

**Trajanje:** 30 min za workflow + 15 min za testiranje.

### Faza 5: Operating manual

**Cilj:** Dokumentovati ceo md2conf workflow u repou da svaki novi član tima
brzo razumije.

**Šta treba:**
- `OPERATING.md` u root-u repoa, ili
- Update `md2conf-tooling/README.md` sa kompletnim vodičem

**Sadržaj:**
- Setup (venv, env vars)
- Kako kreirati novi epic/story
- Kako pokrenuti md2conf
- Kako rješavati česte greške
- Lista skripti i kad ih koristiti
- Šta NE treba raditi (npr. uređivati Confluence direktno)

**Trajanje:** 30-45 min.

### Sitne kozmetičke popravke

U chapter stranicama (vidljivo na Confluence-u):

1. **Header u tabeli:**
   ```
   | Korisnici ne znaju... | Personalizovane preporuke... |
   | ### Vrijednosna propozicija |  |
   ```
   Treba: dodati blank line između tabele i `### Vrijednosna propozicija`.
   Lokacije: `01-uvod-i-koncepti.md` (~3 mjesta).

2. **Razmak fali iza bold close:**
   ```
   **Obavezno:**[05 - Moderacija](...)   ← fali razmak
   **Detaljne persone i putovanja:**[Persone...](...)
   ```
   Treba: `**Obavezno:** [05 - Moderacija](...)`.
   Lokacije: `01-uvod-i-koncepti.md` (~5 mjesta).

**Trajanje:** 10 min ručno.

---

## Ključna naučenja iz ove sesije

### md2conf

- **`.mdignore` sintaksa:** glob patterni bez `/`. Bare imena foldera rade.
- **Hidden dirs auto-skip:** `.git`, `.venv` itd. ne treba u `.mdignore`.
- **`title` u frontmatter** je obavezan za chapter/instrukcijske fajlove jer
  nemaju H1 koji bi md2conf koristio.
- **`--no-generated-by`** flag uklanja "This page has been generated with a tool" banner.
- **`--skip-title-heading`** ne radi ako `title` dolazi iz frontmatter-a
  (kao u našem slučaju). Pa moramo H1 ručno ukloniti iz body-ja.
- **Cross-folder linkovi rade** kad se md2conf pokreće iz root-a (`md2conf "."`).
  Ako se pokreće na pojedinačnom fajlu, padne na "outside root path".
- **Idempotentnost:** drugi run = 0 update-a (checksum match).

### User story format na Confluenceu

Razlika između paragraph break (`\n\n`) i soft break (`  \n`):
- Paragraph break = tri zasebna paragrafa
- Soft break (trailing 2 razmaka + newline) = jedan paragraf sa `<br/>`

Mi koristimo **soft break** za User story.

### Workflow

- Markdown SSoT u Git, Confluence je view layer
- Push u Git → pokreni md2conf → Confluence se ažurira
- **Niko ne uređuje Confluence direktno** (ako se uredi, sljedeći md2conf push
  će prepisati izmjene)

---

## Kako koristiti ovaj fajl u sljedećoj sesiji

1. **Upload ovaj fajl** kao prvi attachment u novoj Claude sesiji
2. **Reci AI-u:** "Nastavljamo md2conf migraciju iz prethodne sesije.
   Ovaj handoff fajl ima sve potrebno. Pročitaj ga, pa nastavljamo
   sa [Faza 4 / Faza 5 / nešto drugo]."
3. AI će imati kompletan kontekst i može direktno krenuti.

---

## Check pri početku nove sesije

Provjeri da je Korak 7 urađen (Claude.ai project knowledge update):

```
[u novoj sesiji, prije nego što kreneš]
"Pretraži cityinfo-epics-stories-instructions.md u project knowledge.
Da li sadrži 'Verzija: 1.2' u changelog-u?"
```

Ako da → krećemo dalje.
Ako ne → uradi Korak 7 prije rada.
