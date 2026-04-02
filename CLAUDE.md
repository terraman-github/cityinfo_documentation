# CityInfo — CLAUDE.md

> Kontekst fajl za Claude Code agenta. Sadrži sve što agent treba znati
> da radi sa CityInfo projektnom dokumentacijom.

---

## O projektu

**CityInfo** (cityinfo.ba) je multi-tenant, dvojezična city guide platforma
za otkrivanje i promociju lokalnih događaja i mjesta. Ciljne grupe: građani,
turisti, organizatori događaja, vlasnici biznisa.

**Tech stack:**
- Backend: .NET 10 (LTS), C#, ASP.NET Core + MS SQL Server
- Frontend: Svelte 5 + SvelteKit + TailwindCSS + Flowbite
- Tri odvojena frontend sistema: User (cityinfo.ba), Staff (admin.cityinfo.ba), GlobalAdmin (master.cityinfo.ba — Faza 2)

---

## Confluence kao SSoT

Sva projektna dokumentacija živi na Confluenceu. **Confluence je jedini izvor
istine** — lokalni fajlovi su kopije ili instrukcije, ne primarna dokumentacija.

### Pristup Confluenceu

- **Cloud ID:** `terraprojects.atlassian.net`
- **Space ID:** `98463`
- **Content format:** uvijek `markdown` za čitanje i pisanje
- **MCP endpoint:** `https://mcp.atlassian.com/v1/mcp` (nakon 30.6.2026. SSE endpoint neće raditi)

### Ključne Confluence stranice

| Stranica | Page ID | Opis |
|----------|---------|------|
| Projektni indeks | `240812033` | Navigacija — linkovi i opisi svih stranica |
| MVP SCOPE | `242188289` | Šta ulazi u MVP, šta u Phase 2/3 |
| Ch.01 — Uvod i koncepti | `240156678` | Osnove platforme, pojmovi |
| Ch.02 — Korisnički doživljaj | `240254995` | UX, pretraga, prikaz, sortDate |
| Ch.03 — Korisnici i pristup | `240156686` | Registracija, profil, Trust Tier, Staff |
| Ch.04 — Sadržaj | `240189477` | Listing model, kategorije, dokumenti, lifecycle |
| Ch.05 — Moderacija | `240189485` | Moderation workflow, AI screening, queue |
| Ch.06 — Monetizacija | `240222244` | Krediti, promocije, display oglasi |
| Ch.07 — Komunikacija | `240320540` | Poruke uz listing, notifikacije |
| Ch.08 — Infrastruktura | `240189509` | Multi-tenancy, i18n, background jobs |
| Persone i putovanja | `243040257` | Persone (Milica, Marko, Ana, Thomas, Lejla, Damir) |
| EPICS AND STORIES folder | `250249231` | Root za sve epice i storije |
| Plan pisanja epica i storija | `250970134` | SSoT za status epica/storija |
| Listing statusni model — spec | `253526019` | Jednostatus model (13 vrijednosti) |
| Migracija statusnog modela | `253853698` | Plan i izvršenje migracije |

### Journey stranice

| Journey | Page ID |
|---------|---------|
| J-01 | `243499009` |
| J-02 | `242974724` |
| J-03 | `243007490` |
| J-04 | `243531777` |
| J-05 | `243367956` |
| J-06 | `243564545` |

### Kreirani epici (sa page ID-evima)

| Epic | Page ID | Storija |
|------|---------|---------|
| E14 — Infrastruktura, i18n i pozadinski procesi | `251199489` | 7 |
| E03a — Kategorizacija sadržaja — entiteti i seed data | `251297793` | 5 |
| E01 — Korisnička registracija i profil | `251232295` | 8 |
| E02 — Listing CRUD i lifecycle | `251330580` | 9 |
| E06 — Trust Tier sistem | `250478652` | 5 |
| E07 — Moderacijski workflow i AI screening | `251265065` | 6 |
| E13 — Staff panel, autentifikacija i upravljanje | `250970205` | 7 |
| E03b — Kategorizacija sadržaja — admin upravljanje | `251691009` | 4 |
| E04 — Otkrivanje i pretraga sadržaja | `251854849` | 7 |
| E05 — Prikaz sadržaja i korisničke interakcije | `252084225` | 6 |
| E08 — Komunikacija uz listing i dokumenti | `252018708` | 5 |
| E09 — Kreditni sistem i wallet | `252411905` | 4 |
| E10 — Promocije listinga | `252280852` | 6 |
| E11 — Display oglašavanje (MVP) | `252706817` | 5 |
| E12 — Notifikacije | `252575764` | 5 |

**Ukupno: 15 epica, 92 storije.**

---

## Ključni domenski koncepti

Ovi koncepti se koriste kroz cijelu dokumentaciju — razumijevanje je obavezno
za bilo kakvu analizu ili izmjenu.

### Listing
Zajednički apstraktni entitet za **Event** i **Place**. Svaki listing ima
`listingStatus`, pripada kategorijama, i prolazi kroz moderaciju.

### Listing statusni model (jednostatus)
Od 1.4.2026. koristi se **jednostatus model**:
- **`listingStatus`** — 13 eksplicitnih vrijednosti: `draft`, `pending_review`,
  `in_review`, `changes_requested`, `rejected`, `scheduled`, `active`,
  `expired`, `closed_by_owner`, `suspended`, `removed_by_admin`,
  `removed_by_system`, `removed_by_owner`
- **`removedReason`** — razlog uklanjanja (popunjen samo za removed statuse)
- **`isPublic`** — boolean, da li je listing vidljiv javnosti
- **`wasEverActive`** — boolean, da li je listing ikad bio aktivan

> ⚠️ **Stari termini `lifecycleStatus`, `moderationStatus`, `closedReason`
> su zamijenjeni.** Ako ih nađeš u dokumentaciji — to je greška koja treba
> biti ispravljena.

### Trust Tier (0–4)
Sistem povjerenja za korisnike: Restricted → Standard → Trusted → Established → Verified Partner.
Određuje pre/post-moderation routing, ponašanje pri editovanju, sampling rate.
- Tier 1→2 napredovanje: min 5 odobrenih listinga, 80% success rate, 7 dana starost naloga
- `changes_requested` je neutralan — samo finalna odluka se računa

### Tri korisnička sistema
- **User** (cityinfo.ba) — registrovani korisnici
- **Staff** (admin.cityinfo.ba) — moderatori, local admini
- **GlobalAdmin** (master.cityinfo.ba) — super admini (Faza 2)
- Svaki ima izolovanu bazu

### sortDate
Centralni mehanizam sortiranja. Manuelni refresh jednom u 24h besplatno.
AutoRenew na konfigurisanom intervalu (plaćena funkcija).

### Kategorizacija (tri nivoa)
Sektor → Kategorija → Tagovi, sa alias/synonym mehanizmom za tenant-konfigurisani
mapping pretraga.

### ListingDocument
SSoT za vlasničku/verifikacijsku dokumentaciju. Max 3 dokumenta, PDF/JPG/PNG.
Status: `accepted`/`rejected` (ne `verified` — da se izbjegne zabuna sa listing `verificationStatus`).

### Monetizacija
Kreditni sistem sa promotion tierovima (Standard / Premium / Premium+Homepage)
i Display Advertising.

### Persone
- **Milica** — mlada profesionalka (korisnik)
- **Marko** — organizator događaja
- **Ana** — vlasnica biznisa
- **Thomas** — turista
- **Lejla** — moderator
- **Damir** — ops menadžer

---

## Pravila za rad sa Confluenceom

### Čitanje
```
getConfluencePage(cloudId="terraprojects.atlassian.net", pageId="...", contentFormat="markdown")
```

### Pisanje (KRITIČNO)
- **`updateConfluencePage` zamjenjuje CIJELO tijelo stranice.** Nikad ne šalji
  parcijalni sadržaj — prvo dohvati stranicu, izmijeni kompletni body, pa šalji.
- **Uvijek dohvati trenutnu verziju prije ažuriranja** da izbjegneš prepisivanje
  novijeg sadržaja. Provjeri `version.number`.
- **Za stranice ~50KB+:** pripremi kompletni body u lokalnom fajlu prije slanja.
- **Mermaid dijagrami:** embedduj direktno kao fenced code blocks sa `mermaid`
  labelom — Confluence ih renderira nativno.
- **Uvijek koristi `versionMessage`** za audit trail.

### Navigacija
Kad ti treba kontekst o bilo kojem dijelu projekta, počni od **Projektnog
indeksa** (page ID `240812033`) — on sadrži linkove i opise svih stranica.

---

## Ton i stil pisanja

- **Jezik:** Bosanski (ijekavica). Tehnički termini na engleskom kad je
  prirodnije (`listingStatus`, `sortDate`, `Trust Tier`, `endpoint`).
- **Ton:** Opušteno-profesionalno. Piši kao da objašnjavaš kolegi, ne ISO standard.
- **Izbjegavaj:** Pasiv, korporativne fraze, dupliciranje dokumentacije.
- **Referenciraj:** `Ch.04, sekcija 4.8` umjesto kopiranja sadržaja.

---

## Tipični zadaci za Claude Code

### 1. Analiza konzistentnosti dokumentacije
Prolazak kroz svih 8 poglavlja + epice/storije i provjera:
- Da li se termini koriste konzistentno (npr. stari vs novi statusni model)
- Da li cross-reference-i pokazuju na prave sekcije
- Da li su Trust Tier pragovi isti u Ch.03 i epicima
- Da li neka storija referira sekciju koja ne postoji

**Pristup:**
1. Dohvati sve poglavlja (Ch.01–Ch.08)
2. Dohvati sve epice i njihove storije (page ID-evi gore)
3. Analiziraj, generiši izvještaj sa konkretnim nalazima

### 2. Bulk ažuriranje nakon promjene modela
Kad se promijeni ključni koncept (npr. statusni model), treba ažurirati
sve pogođene stranice.

**Pristup:**
1. Identifikuj sve stranice koje koriste stari termin
2. Za svaku: dohvati → izmijeni → pošalji sa `versionMessage`
3. Vodi evidenciju šta je ažurirano

### 3. Validacija epica i storija
Provjera da li svaki epic i svaka storija prate format iz
`cityinfo-epics-stories-instructions.md`:
- Ima li excerpt?
- Jesu li AC-ovi provjerljivi?
- Ima li Backend/Frontend Scope gdje treba?
- Referencira li dokumentaciju umjesto da je duplicira?

### 4. Generisanje izvještaja
Cross-cutting analize poput:
- "Koje storije pokriva Journey J-02?"
- "Koje storije nemaju wireframe referencu?"
- "Lista svih API endpointa iz Backend Scope sekcija"

---

## Čuvanje rezultata

- Izvještaje i analize sačuvaj u `/home/user/cityinfo-reports/` (ili sl.)
- Za izmjene na Confluenceu: uvijek prvo prikaži šta će se promijeniti,
  pa tek onda primijeni (osim ako je eksplicitno rečeno da primijeni direktno)
- Generiši markdown izvještaje koji se mogu pregledati ili uploadovati

---

## MCP konfiguracija za Claude Code

Za pristup Confluenceu iz Claude Code-a, dodaj u `.mcp.json`:

```json
{
  "mcpServers": {
    "atlassian": {
      "type": "url",
      "url": "https://mcp.atlassian.com/v1/mcp"
    }
  }
}
```

> Napomena: Autentifikacija se rješava kroz OAuth flow koji MCP server
> pokrene pri prvom pozivu. Trebat će odobriti pristup za Atlassian nalog.

---

## Šta NE raditi

- **Ne pretpostavljaj sadržaj dokumentacije** — uvijek dohvati i pročitaj.
- **Ne koristi stare termine** (`lifecycleStatus`, `moderationStatus`,
  `closedReason`) — zamijenjeni su jednostatus modelom.
- **Ne šalji parcijalni body** na `updateConfluencePage` — zamijeniće cijelu stranicu.
- **Ne mijenjaj Phase oznake** bez eksplicitne potvrde — dolaze iz MVP SCOPE.
- **Ne dupliciraj dokumentaciju** u epicima/storijama — referenciraj.
- **Ne koristi .NET 8** — tech stack je **.NET 10 (LTS)**.
