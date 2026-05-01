# Handoff — md2conf migracija (Faza 4 zatvorena)

> **Datum:** 1. maj 2026.
> **Status:** Faze 0–4 gotove. md2conf radi end-to-end + GitHub Actions auto-sync na svaki push u `main`.
> **Sljedeća sesija:** Faza 5 — operating manual u repou.

---

## TL;DR za naredne sesije

1. **Workflow je live i radi.** GitHub Actions sinhronizuje Confluence na svaki push u `main` (auto) ili kroz "Run workflow" dugme (ručno). Trajanje: ~3 minute. Idempotentno.
2. **Coristi se Zoranov lični Atlassian token.** Bot user setup (`admin@terrafirma.ba`) je probali, nije radilo, ostavili smo za kasnije. Detalji u sekciji "Bot user — backlog stavka" niže. **Ne pokušavati ponovo bez konkretnog plana**.
3. **Faza 5 (operating manual) je sljedeći logičan korak** — kratak `OPERATING.md` u root-u repoa za buduće reference (tebe za 3 mjeseca, novog Svelte dev-a kad uđe).
4. **Handoff fajl je u `.mdignore`** — ne ide na Confluence, živi samo u repou.

---

## Trenutno stanje (1. maj 2026, kraj sesije)

### Repo

- **Lokalna putanja:** `C:\Code\cityinfo_documentation` (nova radna stanica — stara `C:\Users\zoran\source\repos\` se **ne koristi više**)
- **Branch:** `main`
- **Stanje:** clean, push-ovano

### GitHub Actions

- **Workflow:** `.github/workflows/md2conf-sync.yml`
- **Triggers:** `push: branches: [main]`, `workflow_dispatch`
- **Concurrency control:** `cancel-in-progress: true` (novi push otkazuje stari run)
- **Timeout:** 15 min
- **Artifact:** `md2conf-push-log` (raw md2conf log, 14 dana retention)
- **Summary:** custom markdown summary u Actions UI-u sa brojačima

### Secrets (GitHub → Settings → Secrets and variables → Actions)

| Secret | Trenutna vrijednost |
|--------|---------------------|
| `ATLASSIAN_EMAIL` | `zoran.husanovic@terrafirma.ba` (Zoranov lični email) |
| `ATLASSIAN_API_TOKEN` | Zoranov lični classic API token |

`CONFLUENCE_DOMAIN`, `CONFLUENCE_PATH`, `CONFLUENCE_SPACE_KEY` nisu secrets — hardcoded u workflow env varijablama.

### md2conf konfiguracija u workflow-u

```yaml
CONFLUENCE_DOMAIN: terraprojects.atlassian.net
CONFLUENCE_PATH: /wiki/
CONFLUENCE_SPACE_KEY: GI
CONFLUENCE_USER_NAME: ${{ secrets.ATLASSIAN_EMAIL }}
CONFLUENCE_API_KEY: ${{ secrets.ATLASSIAN_API_TOKEN }}
```

### `.mdignore` fajlovi (KRITIČNO za stabilnost)

**`C:\Code\cityinfo_documentation\.mdignore`** (root, 10 linija):

```
README.md
audit-report.md
cityinfo-epics-stories-instructions.md
CLAUDE-13-to-12.md
CLAUDE.md
HANDOFF-md2conf-migration.md
jira-sync
md2conf-tooling
*.csf
*.log
```

**`epics-and-stories/.mdignore`** (2 linije):

```
plan-pisanja-epica-i-storija.md
pisanje-epica-i-user-storija-instrukcija.md
```

**Ostali .mdignore u repou (postojeći, ne diraj):**
- `jira-sync/.mdignore`
- `md2conf-tooling/.mdignore`

### Stanje sinkronizacije

- **Confluence stranice u GI space-u:** 114 (chapter-i, MVP SCOPE, status spec, persone, journeys, instrukcije, 15 epica + 89 storija)
- **Zadnji workflow run:** ✅ Uspješno, 24 ažurirano, 90 bez promjene, 0 grešaka, 0 kreiranih
- **Idempotentnost:** sljedeći run će biti 0 izmjena (Actions/local checksum će se izjednačiti)

---

## Šta je urađeno u ovoj sesiji

### Faza 4 — GitHub Actions automatizacija

**Cilj:** push u `main` → Confluence se ažurira automatski.

**Šta je urađeno:**

1. ✅ Kreiran workflow fajl `.github/workflows/md2conf-sync.yml` sa push + workflow_dispatch trigger-ima, concurrency control, custom summary u Actions UI-u, log artifact.
2. ✅ Postavljeni GitHub Secrets (`ATLASSIAN_EMAIL`, `ATLASSIAN_API_TOKEN`).
3. ❌ **Pokušaj sa bot user-om** (`admin@terrafirma.ba`) nije uspio — vidi sekciju "Bot user — backlog stavka" niže. Vraćeno na Zoranov lični token kao privremeno rješenje.
4. ✅ Workflow proradio sa Zoranovim tokenom — manualni run i real push test prošli su zeleno.

**Faza 4 zatvorena — workflow je live.**

### Cleanup mizerija (kasnije u sesiji)

Kad smo dodali HANDOFF fajl u repo i pokrenuli novi push, **workflow je pao i kreirao 10 orphan stranica na Confluenceu** (HANDOFF, CLAUDE, audit-report, CLAUDE-13-to-12, plus duplikate iz tooling foldera). Razlog: tokom dodavanja `.mdignore` fajlova, **PowerShell here-string je auto-konvertovao plain filename-ove u markdown linkove**, što je `.mdignore` učinilo nefunkcionalnim.

**Cleanup koraci (urađeni):**

1. ✅ Disable-ovan workflow privremeno
2. ✅ Manualno obrisano 10 orphan stranica na Confluenceu (Zoran, kroz Confluence UI)
3. ✅ Rebuild oba `.mdignore` fajla preko **Notepad-a** (PowerShell here-string je probematic)
4. ✅ Dodati tooling foldere (`jira-sync`, `md2conf-tooling`) u root `.mdignore`
5. ✅ Lokalni dry-run sa md2conf-om kao verifikacija prije push-a (114 docs, 0 errors, 0 creates)
6. ✅ Push fix-a, re-enable workflow, manualni run = ✅

**Zaključak: kombinacija (a) PowerShell auto-konverzije i (b) zaboravljanja tooling foldera u `.mdignore` napravila je probleme. Lessons learned u sekciji niže.**

---

## Lessons Learned (KRITIČNO za buduće sesije)

### 1. PowerShell here-string konvertuje `.md` filename u markdown link

**Symptom:** Kreiraš `.mdignore` sa:
```powershell
$content = @"
HANDOFF-md2conf-migration.md
"@
$content | Set-Content -Path .mdignore
```

Rezultat u fajlu:
```
[HANDOFF-md2conf-migration.md](http://HANDOFF-md2conf-migration.md)
```

**Razlog:** Neki PowerShell terminal renderer (vjerovatno VS Code integration ili Windows clipboard) tretira `.md` ekstenziju kao "ovo izgleda kao markdown link" i auto-konvertuje. Bug se manifestuje i pri direct paste-u u terminal.

**Workaround: Notepad.** Notepad ne radi nikakvu auto-konverziju. Za kreiranje ili editovanje `.mdignore` fajlova:

```powershell
notepad .mdignore
```

**Kucati ručno** (ne paste, jer i clipboard može biti zaražen). Ctrl+S, zatvori.

**Provjera:** poslije bilo koje edit operacije, uvijek:
```powershell
Get-Content .mdignore
```

Treba da vidiš plain filename-ove. Ako vidiš `[X](http://X)` — bug se pojavio, treba ponovo Notepad.

### 2. md2conf `.mdignore` sintaksa

- **Lokacija:** `.mdignore` mora biti u **istom direktoriju** kao fajl koji ignoriše. `.mdignore` u rootu pokriva samo root, ne podfoldere.
- **Pattern:** koristi fnmatch glob (npr. `*.md`, `up-*.md`).
- **Folderi:** **bare ime, BEZ trailing slash-a** (`md2conf-tooling`, ne `md2conf-tooling/`).
- **Hidden direktoriji:** `.git`, `.venv`, `.claude`, `.github`, `.vscode` — md2conf ih automatski preskače.
- **Komentari:** linije koje počinju sa `#` su komentari.

### 3. Markdown fajlovi bez frontmatter-a uvijek kreiraju nove stranice

Ako fajl nema YAML frontmatter sa `confluence_page_id`, md2conf:
1. Ne može ga vezati za postojeću Confluence stranicu
2. Kreira **novu** stranicu pri svakom run-u
3. Upisuje page ID nazad u frontmatter — **ali samo ako frontmatter postoji**

Tooling fajlovi (README u `md2conf-tooling/`, `jira-sync/`, ATLASSIAN-SCRIPTING-NOTES, itd.) **nemaju frontmatter**, pa svaki run kreira nove orphan stranice. **Zato moraju biti u `.mdignore`**.

### 4. Lokalni dry-run je obavezan korak prije push-a

Kad mijenjaš:
- `.mdignore` fajlove
- Dodaješ nove markdown fajlove
- Mijenjaš strukturu repoa

**Uvijek prvo pokreni lokalni dry-run** prije push-a:

```powershell
cd C:\Code\cityinfo_documentation
.\.venv\Scripts\Activate.ps1

# Postavi env varijable u sesiji
$env:CONFLUENCE_DOMAIN = "terraprojects.atlassian.net"
$env:CONFLUENCE_PATH = "/wiki/"
$env:CONFLUENCE_SPACE_KEY = "GI"
$env:CONFLUENCE_USER_NAME = "zoran.husanovic@terrafirma.ba"
$env:CONFLUENCE_API_KEY = "<token>"

md2conf "." --no-generated-by -l info > md2conf-local.log 2>&1
```

(Koristi `> file 2>&1` umjesto `Tee-Object` — manje encoding problema.)

**Šta tražiti u logu:**

```powershell
findstr /C:"Indexed" md2conf-local.log
findstr /C:"Creating page" md2conf-local.log
findstr /C:"ERROR" md2conf-local.log
```

Ako:
- `Indexed N documents` gdje je N očekivani broj (114 trenutno)
- 0 `Creating page` linija
- 0 `ERROR` linija

→ sigurno za push.

Ako iz dry-run-a izađu nove `Creating page` linije za fajlove koji **ne treba** da budu na Confluenceu, dodati ih u `.mdignore` PRIJE push-a.

### 5. Lokalni run i Actions run mogu imati različite checksum-e

Pri prvom push-u poslije lokalnog rada, **Actions može pokazati N "ažurirano"** stranica iako je lokalno sve "up-to-date". Razlog: razlike u CRLF (Windows) vs LF (Linux) line endings, trailing whitespace, encoding nijanse.

**Ovo je očekivano i normalno** — **drugi push** će biti idempotentan (0 izmjena).

### 6. PowerShell terminal skraćuje stdout na 80 znakova

`Tee-Object` i ponekad `Out-File` propuštaju output kroz konzolu i skraćuju na terminal width. Za log fajlove sa dugim putanjama:
- Koristi `> file.log 2>&1` umjesto `| Tee-Object`
- Ili `Out-File -Width 500 -FilePath file.log`
- Za parsing log fajla u UTF-16 encodingu, najbrže ga je poslati Claude-u koji može iconv UTF-16 → UTF-8 i grep normalno

---

## Bot user — backlog stavka

> **Status:** Probano, ne radi. Privremeno odgođeno. Prioritet: nizak.

### Cilj (zašto se vrijedi vratiti na ovo)

Razdvojiti "ljudske" od "automatskih" izmjena u Confluence audit log-u. Posebno bitno kad uđe novi developer u repo — njegov push ne treba da propagira pod Zoranovim imenom u Confluenceu.

### Šta je probano u ovoj sesiji

#### Pokušaj 1: Classic API token (bez scope-ova)

- **Setup:** bot user kreiran, dodan u CityInfo (GI) space sa svim permissions
- **Token:** `Create API token` (klasični, samo label, bez scope-ova)
- **Rezultat:** ❌ **404 Not Found** na `api.atlassian.com/ex/confluence/{cloudId}/api/v2/pages/240156678`
- **md2conf log:**
  ```
  Configured scoped Confluence REST API URL: https://api.atlassian.com/ex/confluence/{cloudId}/
  ```

#### Pokušaj 2: Scoped token sa klasičnim scope-ovima

- **Setup:** isti bot user, isti space permissions
- **Token:** `Create API token with scopes` (kategorija: Classic), odabrani scope-ovi:
  - Read: `read:confluence-content.all`, `.permission`, `.summary`, `read:confluence-groups`, `read:confluence-props`, `read:confluence-space.summary`, `read:confluence-user`, `read:me`, `readonly:content.attachment:confluence`, `read:account`
  - Write: `write:confluence-content`, `write:confluence-file`, `write:confluence-groups`, `write:confluence-props`, `write:confluence-space`
  - Search: `search:confluence`
  - Manage: `manage:confluence-configuration`
- **Rezultat:** ❌ **401 Unauthorized** na `terraprojects.atlassian.net/wiki/api/v2/pages/240156678`
- **md2conf log:**
  ```
  Probing scoped Confluence REST API URL
  Configured classic Confluence REST API URL: https://terraprojects.atlassian.net/wiki/
  ```
  md2conf je sada uspio detektovati i konfigurisati direktni site URL, ali server je svejedno odbio auth.

#### Hipoteza koja nije testirana

Atlassian je u tranziciji oko token vrsta. Postoje **granularni** scope-ovi (`read:page:confluence`, `write:page:confluence`, `read:space:confluence` itd.) koji su novija generacija — možda baš oni rade sa API v2 endpoint-ima koje md2conf koristi. Naš token je imao **klasične** scope-ove (`read:confluence-content.all`, `write:confluence-content` itd.) koje su starije.

### Sljedeći korak za debug (kad bude vremena)

1. Generisati novi scoped token za bot user-a, ali ovaj put odabrati **granularne** scope-ove:
   - `read:page:confluence`
   - `write:page:confluence`
   - `delete:page:confluence`
   - `read:space:confluence`
   - `read:hierarchical-content:confluence`
   - `read:attachment:confluence`
   - `write:attachment:confluence`
2. Ili alternativno — testirati direktno cURL-om sa bot tokenom da se vidi šta tačno API vraća izvan md2conf-a:
   ```bash
   curl -u "admin@terrafirma.ba:TOKEN" \
     "https://terraprojects.atlassian.net/wiki/api/v2/pages/240156678"
   ```

### Šta je probano i radilo (za referencu)

- **Zoranov nalog sa classic tokenom (bez scope-ova):** ✅ radi, sve API v1 i v2 endpoint-i prolaze
- Trenutno workflow koristi ovo

### Zaključak

Atlassian token sistem je u tranziciji i dokumentacija je nedosljedna — minimum 60 minuta debug-a sa eksperimentisanjem da se nađe pravi setup. **Ne pokušavati ponovo dok ne bude konkretne potrebe** (npr. novi dev počinje da commit-uje, audit log postaje zaista bitan).

---

## Faza 5 — sljedeći korak

### Cilj

Kratak `OPERATING.md` u root-u repoa koji odgovara na 3 pitanja:

1. **Kako se mijenja dokumentacija?** (workflow: edit md → commit → push → Actions sinhronizuje)
2. **Šta da radim ako sync padne?** (provjera GitHub Actions log-a, common failure modes, lessons learned iz ove sesije)
3. **Kako lokalno testirati md2conf prije push-a?** (povratak na manuelni `md2conf "."` kao backup)

### Predlog strukture (~150-250 linija)

- **Pregled** — šta je SSoT, šta je view layer, kako su povezani
- **Workflow za izmjene**
  - Mali fix (1-2 fajla) — direktno commit + push, Actions sinhronizuje
  - Veća izmjena (`.mdignore` modifikacije, novi tooling fajlovi, struktura repoa) — **lokalni dry-run prvo**
- **Lokalni setup**
  - venv, pip install, env varijable, lokalni dry-run komanda
  - Korisno za debug i za fallback ako Actions ne radi
- **Šta se dešava na push** — high-level dijagram (markdown → Actions → Confluence)
- **Troubleshooting**
  - Workflow failed sa 401 → token expired ili invalid
  - Workflow failed sa 404 → page_id u frontmatter-u koji više ne postoji na Confluenceu
  - Workflow failed pri pip install → vjerovatno PyPI outage, retry
  - **Workflow kreirao orphan stranice** → fajl bez frontmatter-a koji nije u `.mdignore`
  - **`.mdignore` izgleda pokvareno** (sa `[X](http://X)`) → PowerShell auto-konverzija, koristi Notepad
- **`.mdignore` cheat sheet** — sintaksa, primjeri, šta NE raditi
- **Manualni override** — kako lokalno pokrenuti md2conf ako Actions je out
- **Sigurnosne napomene** — token expiration, secret rotation
- **Kontakt / odgovornost** — ko upravlja secret-ovima, ko je vlasnik repoa

### Šta NE ide u OPERATING.md

- Sve što je već u `cityinfo-epics-stories-instructions.md` (format epica i storija) — taj fajl je za pisanje sadržaja, OPERATING.md je za infrastrukturu
- Detalji md2conf-a kao alata — link na hunyadi/markdown-to-confluence repo
- Bot user backlog (to ostaje u handoff-u, ne u OPERATING-u)

### Sljedeća sesija — preporučen prompt

> "Krećemo Fazu 5 md2conf migracije. Pročitaj `HANDOFF-md2conf-migration.md` u root-u repoa za kontekst. Cilj: napiši `OPERATING.md` po predloženoj strukturi iz handoff-a. Posebno uključi lessons learned iz Faza 4 cleanup mizerije (PowerShell `.mdignore` bug, tooling foldere, lokalni dry-run obavezan)."

---

## Tehnička referenca

### Workflow fajl (snapshot)

Lokacija: `.github/workflows/md2conf-sync.yml`. Ne mijenjati bez razumijevanja:

- **Concurrency group `md2conf-sync`** — globalan, otkazuje stari run kad stigne novi push
- **`set -o pipefail`** — md2conf failure ne smije biti maskiran tee-om
- **`hashFiles('md2conf-push.log') != ''`** — summary i artifact step rade samo ako log fajl postoji (sigurnost ako md2conf padne prije nego što išta logira)

### Token expiration

Zoranov token nema expiration ili je default 1 godina. **Backlog stavka:** kreirati expiration sa kalendar reminder-om za rotaciju, ili još bolje — riješiti bot user pa migriraju na expiring token.

### Lokalni md2conf workflow (backup)

Ako GitHub Actions je iz nekog razloga out, manuelni run sa Zoranovog laptopa:

```powershell
cd C:\Code\cityinfo_documentation
.\.venv\Scripts\Activate.ps1

$env:CONFLUENCE_DOMAIN = "terraprojects.atlassian.net"
$env:CONFLUENCE_PATH = "/wiki/"
$env:CONFLUENCE_SPACE_KEY = "GI"
$env:CONFLUENCE_USER_NAME = "zoran.husanovic@terrafirma.ba"
$env:CONFLUENCE_API_KEY = "<token>"

md2conf "." --no-generated-by -l info > md2conf-local.log 2>&1
```

---

## Diagnostički put — full timeline

### Bot user pokušaji

| Korak | Token tip | URL koji md2conf koristi | Rezultat |
|-------|-----------|--------------------------|----------|
| 1 | Bot user, classic (bez scope-ova) | `api.atlassian.com/ex/confluence/{cloudId}/api/v2/pages/...` | ❌ 404 Not Found |
| 2 | Bot user, scoped sa klasičnim scope-ovima | `terraprojects.atlassian.net/wiki/api/v2/pages/...` | ❌ 401 Unauthorized |
| 3 | Zoranov classic (bez scope-ova) | `api.atlassian.com/ex/confluence/{cloudId}/api/v2/pages/...` | ✅ Radi |

### Cleanup mizerija

| Problem | Uzrok | Fix |
|---------|-------|-----|
| `.mdignore` ne radi | PowerShell here-string je konvertovao `.md` filename u markdown link | Rebuild kroz Notepad |
| Workflow kreirao 10 orphan stranica | (a) `.mdignore` ne radi (b) tooling foldere nisu bili u `.mdignore` | Manualno obrisati 10 stranica + dodati `jira-sync` i `md2conf-tooling` u `.mdignore` |
| ConversionError u plan-pisanja-epica | Broken link `/wiki/pages/createpage.action` | Fajl uključen u `.mdignore` (interni plan, ne za sync) |
| Lokalni log ima skraćene putanje | UTF-16 encoding + 80-char terminal width | `> file.log 2>&1` umjesto `Tee-Object`, ili pošalji fajl Claude-u za UTF-8 konverziju |

---

## Korisni linkovi

- **Repo:** https://github.com/terraman-github/cityinfo_documentation
- **Confluence GI space:** https://terraprojects.atlassian.net/wiki/spaces/ci/
- **md2conf alat:** https://github.com/hunyadi/md2conf
- **Atlassian API tokens:** https://id.atlassian.com/manage-profile/security/api-tokens
- **Project Index na Confluenceu:** page ID `240812033`

---

## Promjena u radnom okruženju (bitno za buduće sesije)

- **Stara putanja:** `C:\Users\zoran\source\repos\cityinfo_documentation` ❌ (nije više aktualno)
- **Nova putanja:** `C:\Code\cityinfo_documentation` ✅
- **Razlog:** Zoran je promijenio radnu stanicu

Sve PowerShell komande u workflow-u, dokumentaciji, i instrukcijama treba referencirati **novu putanju**.

---

## Status checklist na kraju sesije

- ✅ GitHub Actions workflow live i radi
- ✅ Push u `main` automatski sinhronizuje Confluence
- ✅ `.mdignore` fajlovi ispravno konfigurisani (root + epics-and-stories)
- ✅ Tooling foldere (`jira-sync`, `md2conf-tooling`) isključeni iz sync-a
- ✅ Confluence GI space čist od orphan stranica
- ✅ Lokalni dry-run validan kao verifikacijski korak
- ⏳ Bot user — backlog (probano, nije radilo)
- ⏳ Faza 5 (operating manual) — sljedeća sesija
