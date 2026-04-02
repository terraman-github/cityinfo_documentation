# CityInfo — CLAUDE.md

> Kontekst za Claude Code agenta. Čitaj ovaj fajl na početku svake sesije.

---

## Projekat

**CityInfo** (cityinfo.ba) — multi-tenant, dvojezična city guide platforma za
otkrivanje i promociju lokalnih događaja i mjesta.

- **Backend:** .NET 10 (LTS), C#, ASP.NET Core, MS SQL Server
- **Frontend:** Svelte 5 + SvelteKit + TailwindCSS + Flowbite
- **Tri frontend sistema:** User (cityinfo.ba), Staff (admin.cityinfo.ba), GlobalAdmin (master.cityinfo.ba — Phase 2)

---

## Dokumentacija — fajlovi

Projektna dokumentacija je izvučena iz Confluencea (`terraprojects.atlassian.net`,
space `98463`) u zasebne markdown fajlove.

### Poglavlja

| Fajl | Page ID | Opis |
|------|---------|------|
| `01-uvod-i-koncepti.md` | `240156678` | Vizija, arhitektura, ključni koncepti, persone |
| `02-korisnicko-iskustvo.md` | `240254995` | Naslovna, pretraga, prikaz, sortDate, onboarding |
| `03-korisnici-i-pristup.md` | `240156686` | User/Staff/GlobalAdmin entiteti, Trust Tier, sigurnost |
| `04-sadrzaj.md` | `240189477` | Listing, Event, Place, kategorije, tagovi, lifecycle, interakcije |
| `05-moderacija.md` | `240189485` | Workflow, AI screening, moderatorske akcije, verifikacija |
| `06-monetizacija.md` | `240222244` | Krediti, promocije, display oglasi, franšiza |
| `07-komunikacija.md` | `240320540` | Message sistem, notifikacije, support |
| `08-infrastruktura.md` | `240189509` | Multi-tenant, audit, background procesi, tech stack |

### Ostali fajlovi

| Fajl | Page ID | Opis |
|------|---------|------|
| `novi-listing-statusni-model-specifikacija.md` | `253526019` | 13 statusa, tabela tranzicija, scenariji |
| `mvp-scope-opseg-prve-verzije.md` | `242188289` | Šta ulazi u MVP, šta u Phase 2/3 |
| `cityinfo-epics-stories-instructions.md` | — | Format za pisanje epica i storija |

---

## Ključni koncepti (sažetak)

### Listing
Zajednički entitet za **Event** (vremenski ograničen) i **Place** (stalan).

### Listing statusni model (jednostatus, od 1.4.2026)
- **`listingStatus`** — 13 vrijednosti: `draft`, `in_review`, `changes_requested`,
  `published`, `published_under_review`, `published_needs_changes`, `hidden_by_owner`,
  `hidden_by_moderator`, `hidden_by_system`, `rejected`, `expired`, `canceled`, `removed`
- **`removedReason`** — samo kad je status `removed`
- **`isPublic`** — kalkulisano polje (nikad se ne upisuje direktno)
- **`wasEverActive`** — jednom true, uvijek true

> ⚠️ Stari termini `lifecycleStatus`, `moderationStatus`, `closedReason` su
> zamijenjeni. Ako ih nađeš u dokumentaciji — to je greška koju treba prijaviti.

### Trust Tier (0–4)
Restricted → Standard → Trusted → Established → Verified Partner.
Određuje pre/post-moderation routing i sampling procenat.

### Tri korisnička sistema
User, Staff, GlobalAdmin — odvojene baze, odvojeni API-ji, odvojeni login sistemi.

### sortDate
Centralni mehanizam sortiranja. Ručni refresh 1x/24h besplatno. AutoRenew na
konfigurisanom intervalu (plaćena funkcija).

### Kategorizacija
Sektor → Kategorija → Tagovi. Eventi i Places imaju potpuno odvojene sisteme
kategorija i tagova.

---

## Confluence page ID-evi (referenca)

### Dodatne stranice (nisu eksportovane u fajlove)

| Stranica | Page ID |
|----------|---------|
| Plan epica/storija | `250970134` |
| EPICS AND STORIES folder | `250249231` |
| Projektni indeks | `240812033` |
| Persone i putovanja | `243040257` |
| Migracija statusnog modela | `253853698` |

### Kreirani epici

| Epic | Page ID | Broj storija |
|------|---------|--------------|
| E14 — Infrastruktura | `251199489` | 7 |
| E03a — Kategorije seed | `251297793` | 5 |
| E01 — Registracija i profil | `251232295` | 8 |
| E02 — Listing CRUD | `251330580` | 9 |
| E06 — Trust Tier | `250478652` | 5 |
| E07 — Moderacija | `251265065` | 6 |
| E13 — Staff panel | `250970205` | 7 |
| E03b — Kategorije admin | `251691009` | 4 |
| E04 — Pretraga | `251854849` | 7 |
| E05 — Prikaz i interakcije | `252084225` | 6 |
| E08 — Komunikacija | `252018708` | 5 |
| E09 — Wallet | `252411905` | 4 |
| E10 — Promocije | `252280852` | 6 |
| E11 — Display Ads | `252706817` | 5 |
| E12 — Notifikacije | `252575764` | 5 |

**Ukupno: 15 epica, 92 storije.**

---

## Tipični zadaci

### 1. Analiza konzistentnosti dokumentacije
Pročitaj sva poglavlja (`01-uvod-i-koncepti.md` do `08-infrastruktura.md`) i provjeri:
- Da li se termini koriste konzistentno (posebno: stari vs novi statusni model)
- Da li cross-reference-i (npr. "Ch.04, sekcija 4.8") pokazuju na prave sekcije
- Da li su Trust Tier pragovi i parametri isti u `03-korisnici-i-pristup.md` i `05-moderacija.md`
- Da li su API endpointi konzistentni između poglavlja
- Da li postoje kontradikcije između poglavlja

### 2. Pronalaženje grešaka
Traži:
- Stare termine (`lifecycleStatus`, `moderationStatus`, `closedReason`) — to su greške
- Nepostojeće sekcije u cross-referencama
- Nedefinisane parametre koji se spominju
- Nedosljedne nazive entiteta ili atributa
- Tech stack greške (.NET 8 umjesto .NET 10)
- Broken linkove na Confluence stranice

### 3. Validacija epica i storija
Ako dobiješ pristup epic/story fajlovima, provjeri prema `cityinfo-epics-stories-instructions.md`:
- Prate li format (excerpt, user story, AC, scope sekcije)
- Jesu li AC-ovi provjerljivi (DA/NE)
- Referenciraju li dokumentaciju umjesto da je dupliciraju
- Imaju li Backend/Frontend Scope gdje treba

### 4. Generisanje izvještaja
Kreiraj strukturirane izvještaje sa:
- Konkretnim nalazom (šta je problem)
- Lokacijom (poglavlje, sekcija, paragraf)
- Severity: **critical** (greška u logici/modelu), **minor** (nekonzistentnost/terminologija), **info** (prijedlog poboljšanja)
- Preporukom za ispravku (konkretan tekst ili smjernica)

---

## Ton i stil

- **Jezik:** Bosanski (ijekavica). Tehnički termini na engleskom kad je prirodnije.
- **Ton:** Opušteno-profesionalno, kao da objašnjavaš kolegi.
- **Ne dupliciraj dokumentaciju** — referenciraj (npr. "Ch.04, sekcija 4.8").

---

## Šta NE raditi

- **Ne pretpostavljaj sadržaj dokumentacije** — pročitaj iz fajlova.
- **Ne koristi stare termine** (`lifecycleStatus`, `moderationStatus`, `closedReason`).
- **Ne mijenjaj Phase oznake** bez eksplicitne potvrde vlasnika.
- **Tech stack je .NET 10 (LTS)** — ne .NET 8.
