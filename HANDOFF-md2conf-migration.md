# Handoff — md2conf migracija (Faza 4 zatvorena)

> **Datum:** 1. maj 2026.
> **Status:** Faze 0–4 gotove. md2conf radi end-to-end + GitHub Actions auto-sync na svaki push u `main`.
> **Sljedeća sesija:** Faza 5 — operating manual u repou.

---

## TL;DR za naredne sesije

1. **Workflow je live.** GitHub Actions sinhronizuje Confluence na svaki push u `main` (auto) ili kroz "Run workflow" dugme (ručno). Trajanje: ~3 minute. Idempotentno.
2. **Coristi se Zoranov lični Atlassian token.** Bot user setup (`admin@terrafirma.ba`) je probali ali nije radilo. Detalji u sekciji "Bot user — backlog stavka" niže. **Ne pokušavati ponovo bez konkretnog pristupa**.
3. **Faza 5 (operating manual) je sljedeći logičan korak** — kratak `OPERATING.md` u root-u repoa za buduće reference (sebe za 3 mjeseca, novog Svelte dev-a kad uđe).
4. **Handoff fajl je u `.mdignore`** — ne ide na Confluence, živi samo u repou.

---

## Trenutno stanje (1. maj 2026)

### Repo

- **Lokalna putanja:** `C:\Code\cityinfo_documentation` (nova radna stanica — stara `C:\Users\zoran\source\repos\` se **ne koristi više**)
- **Branch:** `main`
- **Zadnji commit:** `7754150` — `test: trigger md2conf workflow on real push`
- **Stanje:** clean, push-ovano

### GitHub Actions

- **Workflow:** `.github/workflows/md2conf-sync.yml`
- **Triggers:** `push: branches: [main]`, `workflow_dispatch`
- **Concurrency control:** `cancel-in-progress: true` (novi push otkazuje stari run)
- **Timeout:** 15 min
- **Artifact:** `md2conf-push-log` (raw md2conf log, 14 dana retention)
- **Summary:** custom markdown summary u Actions UI-u sa brojačima (Ažurirano / Kreirano / Bez promjene / Greške)

### Secrets (GitHub → Settings → Secrets and variables → Actions)

| Secret | Trenutna vrijednost |
|--------|---------------------|
| `ATLASSIAN_EMAIL` | `zoran.husanovic@terrafirma.ba` (Zoranov lični email) |
| `ATLASSIAN_API_TOKEN` | Zoranov lični classic API token |
| ~~`CONFLUENCE_DOMAIN`~~ | nije korišten kao secret — hardcoded u workflow-u |

### md2conf konfiguracija

Hardcoded u workflow env varijablama:
```yaml
CONFLUENCE_DOMAIN: terraprojects.atlassian.net
CONFLUENCE_PATH: /wiki/
CONFLUENCE_SPACE_KEY: GI
CONFLUENCE_USER_NAME: ${{ secrets.ATLASSIAN_EMAIL }}
CONFLUENCE_API_KEY: ${{ secrets.ATLASSIAN_API_TOKEN }}
```

### Stanje sinkronizacije

- **Confluence stranice u GI space-u:** 114 (svi indeksirani fajlovi iz `epics-and-stories/` + chapter-i + ostale dokumentacijske stranice)
- **Provjera radnog stanja:** zadnji push (`7754150`) — Status ✅ Uspješno, 0 izmjena (idempotentno)

---

## Šta je urađeno u ovoj sesiji (Faza 4)

### Korak 1: Bot user setup (probali, ne radi za sad)

Kreiran je novi Atlassian korisnik `admin@terrafirma.ba` (display name: "CityInfo Docs Bot") sa idejom da automatski sync ne dolazi pod Zoranovim ličnim nalogom. **Permissions su postavljene maksimalno na CityInfo (GI) space** — bot ima sve što i Zoran. **Token je generisan kao scoped token** sa svim Confluence scope-ovima (vidi screenshot iz sesije). Workflow je probao auth — nije uspio, ostaje **401 Unauthorized** na API v2 endpoint-e.

Detalji + dijagnostika u sekciji "Bot user — backlog stavka" niže.

**Odluka:** prebacujemo na Zoranov lični token kao **privremeno rješenje** dok ne bude vremena za pravi diagnostički pristup. Trošak: Confluence audit log ne razlikuje "ručna izmjena" od "auto sync" jer obje izgledaju kao Zoranove.

### Korak 2: Workflow fajl

`.github/workflows/md2conf-sync.yml` kreiran sa sljedećim karakteristikama:

- **Triggers:** push u main + workflow_dispatch (ručni)
- **Concurrency control:** stari run-ovi se otkazuju kad stigne novi push (sprječava race conditions)
- **Steps:** checkout → Python setup → pip install md2conf → md2conf --version → md2conf sync → generiši summary → upload log artifact
- **Fail strategija:** `set -o pipefail` osigurava da md2conf greška obara cijeli workflow (ne tiho)
- **Summary:** custom GitHub Actions summary sa tabelom brojača i listom promijenjenih stranica

### Korak 3: GitHub Secrets

Kreirana 2 secret-a (`ATLASSIAN_EMAIL`, `ATLASSIAN_API_TOKEN`). Token vrsta i email su mijenjani tokom debugging-a (vidi diagnostic put u sekciji bot user-a niže).

### Korak 4: Test

- **Manual run** sa Zoranovim tokenom: ✅ Uspješno (114 bez promjene, 0 grešaka)
- **Real push test** (`.mdignore` modifikacija): ✅ Uspješno (push trigger radi, workflow se auto-pokreće)

---

## Bot user — backlog stavka

> **Status:** Probano, ne radi. Privremeno odgođeno. Prioritet: nizak.

### Cilj (zašto se vrijedi vratiti na ovo)

Razdvojiti "ljudske" od "automatskih" izmjena u Confluence audit log-u. Posebno bitno kad uđe novi developer u repo — njegov push ne treba da propagira pod Zoranovim imenom u Confluenceu.

### Šta je probano u ovoj sesiji

#### Pokušaj 1: Classic API token (bez scope-ova)

- **Setup:** bot user kreiran, dodan u CityInfo (GI) space sa svim permissions
- **Token:** `Create API token` (klasični, samo label)
- **Rezultat:** ❌ **404 Not Found** na `api.atlassian.com/ex/confluence/{cloudId}/api/v2/pages/240156678`
- **Dijagnoza u trenutku:** mislili smo da je permissions problem, dodali pune permissions na space — nije pomoglo. md2conf je u logu izvjestio:
  ```
  Configured scoped Confluence REST API URL: https://api.atlassian.com/ex/confluence/{cloudId}/
  ```

#### Pokušaj 2: Scoped token sa klasičnim scope-ovima

- **Setup:** isti bot user, isti space permissions
- **Token:** `Create API token with scopes` (kategorija: Classic), odabrani scope-ovi:
  - Read: `read:confluence-content.all`, `read:confluence-content.permission`, `read:confluence-content.summary`, `read:confluence-groups`, `read:confluence-props`, `read:confluence-space.summary`, `read:confluence-user`, `read:me`, `readonly:content.attachment:confluence`, `read:account`
  - Write: `write:confluence-content`, `write:confluence-file`, `write:confluence-groups`, `write:confluence-props`, `write:confluence-space`
  - Search: `search:confluence`
  - Manage: `manage:confluence-configuration`
- **Rezultat:** ❌ **401 Unauthorized** na `terraprojects.atlassian.net/wiki/api/v2/pages/240156678`
- **md2conf log:**
  ```
  Probing scoped Confluence REST API URL
  Configured classic Confluence REST API URL: https://terraprojects.atlassian.net/wiki/
  ```
  Tj. md2conf je sada uspio detektovati i konfigurisati direktni site URL (nije više `api.atlassian.com/ex/...`), ali server je svejedno odbio auth.

#### Hipoteza koja nije testirana

Atlassian je u tranziciji oko token vrsta. Postoje **granularni** scope-ovi (`read:page:confluence`, `write:page:confluence`, `read:space:confluence` itd.) koji su novija generacija — možda baš oni rade sa API v2 endpoint-ima koje md2conf koristi. Naš token je imao **klasične** scope-ove (`read:confluence-content.all`, `write:confluence-content` itd.) koje su starije.

**Sljedeći korak za debug** kad bude vremena:

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

- **Tvoj nalog (Zoran) sa classic tokenom (bez scope-ova):** ✅ radi, scoped URL detection radi, sve API v1 i v2 endpoint-i prolaze
- **Tvoj nalog sa scoped granularnim tokenom:** nije probano u ovoj sesiji (radio si sa classic-om, koji već radi)

### Zaključak

Atlassian token sistem je u tranziciji i dokumentacija je nedosljedna — minimum 60 minuta debug-a sa eksperimentisanjem da se nađe pravi setup. **Ne pokušavati ponovo dok ne bude konkretne potrebe** (npr. novi dev počinje da commit-uje, audit log postaje zaista bitan).

---

## Faza 5 — sljedeći korak

### Cilj

Kratak `OPERATING.md` u root-u repoa koji odgovara na 3 pitanja:

1. **Kako se mijenja dokumentacija?** (workflow: edit md → commit → push → Actions sinhronizuje)
2. **Šta da radim ako sync padne?** (provjera GitHub Actions log-a, common failure modes)
3. **Kako lokalno testirati md2conf prije push-a?** (povratak na manuelni `md2conf "."` kao backup)

### Predlog strukture (~150-200 linija)

- **Pregled** — šta je SSoT, šta je view layer, kako su povezani
- **Workflow** — typical edit cycle (par komandi)
- **Što se dešava na push** — high-level dijagram (markdown → Actions → Confluence)
- **Troubleshooting**
  - Workflow run failed sa 401 → token expired ili invalid
  - Workflow run failed sa 404 → vjerovatno page page_id u frontmatter-u koji više ne postoji na Confluenceu
  - Workflow run failed pri pip install → vjerovatno PyPI outage, retry
  - Lokalni `md2conf` failure modes (separate sekcija)
- **Manualni override** — kako lokalno pokrenuti md2conf ako Actions je out
- **Sigurnosne napomene** — token expiration, secret rotation
- **Kontakt / odgovornost** — ko upravlja secret-ovima, ko je vlasnik repoa

### Šta NE ide u OPERATING.md

- Sve što je već u `cityinfo-epics-stories-instructions.md` (format epica i storija) — taj fajl je za pisanje sadržaja, OPERATING.md je za infrastrukturu
- Detalji md2conf-a kao alata — ide kroz link na hunyadi/markdown-to-confluence repo
- Bot user backlog (to ostaje u handoff-u, ne u OPERATING-u)

### Sljedeća sesija — preporučen prompt

> "Krećemo Fazu 5 md2conf migracije. Pročitaj `HANDOFF-md2conf-migration.md` u root-u repoa za kontekst. Cilj: napiši `OPERATING.md` po predloženoj strukturi iz handoff-a."

---

## Tehnička referenca

### Workflow fajl (snapshot)

Lokacija: `.github/workflows/md2conf-sync.yml`. Ako trebaš ga regenerisati, kopija je commit-ovana u `7754150`. Ne mijenjati bez razumijevanja:

- **Concurrency group `md2conf-sync`** — globalan, otkazuje stari run kad stigne novi push
- **`set -o pipefail`** — md2conf failure ne smije biti maskiran tee-om
- **`hashFiles('md2conf-push.log') != ''`** — summary i artifact step rade samo ako log fajl postoji (sigurnost ako md2conf padne prije nego što išta logira)

### md2conf scope-ovi koji su radili sa Zoranovim Classic tokenom

Zoranov token je **stari classic** (`Create API token`, ne `Create API token with scopes`). Nema scope-ove uopšte. Atlassian ga tretira kao "token sa svim legacy permissions". Radi za sve što md2conf zove — i scoped (`api.atlassian.com/ex/confluence/...`) i direct (`terraprojects.atlassian.net/wiki/...`) endpoint-e.

### Token expiration

Zoranov token nema expiration (ili je default 1 godina, treba provjeriti). Za production bi trebao biti scoped sa eksplicitnim expiration-om i kalendar reminder-om za rotaciju. **Backlog stavka** za later.

### `.mdignore`

Ovaj handoff fajl mora biti dodat u `.mdignore` da md2conf ne pokušava da ga sinhronizuje na Confluence. Provjeri da li je dodan prije commit-a.

```
# .mdignore
HANDOFF-md2conf-migration.md
```

### Lokalni md2conf workflow (backup)

Ako GitHub Actions je iz nekog razloga out, manuelni run sa Zoranovog laptopa i dalje radi:

```powershell
cd C:\Code\cityinfo_documentation
.\.venv\Scripts\Activate.ps1
md2conf "." --no-generated-by -l info
```

Koristi iste credentials kao Actions (Zoranov email + token preko local env varijabli).

---

## Diagnostički put — full timeline (za buduće reference)

| Korak | Token tip | URL koji md2conf koristi | Rezultat |
|-------|-----------|--------------------------|----------|
| 1 | Bot user, classic (bez scope-ova) | `api.atlassian.com/ex/confluence/{cloudId}/api/v2/pages/...` | ❌ 404 Not Found |
| 2 | Bot user, scoped sa klasičnim scope-ovima | `terraprojects.atlassian.net/wiki/api/v2/pages/...` | ❌ 401 Unauthorized |
| 3 | Zoranov classic (bez scope-ova) | `api.atlassian.com/ex/confluence/{cloudId}/api/v2/pages/...` | ✅ Radi |

**Konkretne URL razlike:**

- md2conf prvo proba `api.atlassian.com/ex/confluence/{cloudId}/...` (scoped path)
- Ako server odbije auth na tom putu, prebacuje se na `terraprojects.atlassian.net/wiki/...` (direct site path)
- Tvoj Zoranov classic token radi na **prvom** putu (scoped)
- Bot scoped tokens su radili na **drugom** putu (direct), ali server je svejedno odbijao auth

To sugeriše da je problem **specifičan za bot user**, ne za vrstu tokena. Možda u tome kako je dodan u organizaciju, ili neka stvar oko "managed account" statusa, ili nešto drugo.

---

## Korisni linkovi

- **Repo:** https://github.com/terraman-github/cityinfo_documentation
- **Confluence GI space:** https://terraprojects.atlassian.net/wiki/spaces/ci/
- **md2conf alat:** https://github.com/hunyadi/md2conf
- **Atlassian API tokens:** https://id.atlassian.com/manage-profile/security/api-tokens
- **Project Index na Confluenceu:** page ID `240812033`

---

## Promjena u radnom okruženju

**Bitno za sve buduće sesije:**

- **Stara putanja:** `C:\Users\zoran\source\repos\cityinfo_documentation` ❌ (nije više aktualno)
- **Nova putanja:** `C:\Code\cityinfo_documentation` ✅
- **Razlog:** Zoran je promijenio radnu stanicu

Sve PowerShell komande u workflow-u, dokumentaciji, i instrukcijama treba referencirati **novu putanju**.
