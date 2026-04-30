---
id: S02-01
confluence_page_id: "251527176"
title: "S02-01 — Kreiranje Event listinga sa osnovnim podacima"
parent_epic: E02
linear_id: "CIT2-9"
phase: MVP
journey_milestones: [J-02]
type: fullstack
---

<a id="s02-01-kreiranje-event-listinga-sa-osnovnim-podacima"></a>

# S02-01 — Kreiranje Event listinga sa osnovnim podacima

**Naslov:** Kreiranje Event listinga sa osnovnim podacima

**Excerpt:** Omogućava korisniku da kreira novi Event listing popunjavanjem obaveznih i opcionih polja — naziv, opis, datum, kategoriju, tagove i kontakt informacije. Ovo je prvi korak u objavljivanju događaja na platformi.

**Phase:** MVP

**Journey milestones:** J-02

**User story:**

*Kao organizator događaja,*  
*želim kreirati novi Event listing sa svim relevantnim informacijama,*  
*kako bih mogao pripremiti sadržaj za objavu i privući posjetioce.*

**Kontekst:** Korisnik je ulogovan, ima verificiran telefon (preduslov iz [E01](../e01-korisnicka-registracija-i-profil.md)), i pristupa formi za kreiranje Event-a kroz navigaciju ili floating action button. Listing se kreira u `listingStatus = draft` — objava je zasebna akcija ([S02-07](s02-07-objava-listinga-i-statusne-tranzicije.md)). Kategorije i tagovi moraju biti seedani ([E03a](../e03a-kategorizacija-sadrzaja-entiteti-i-seed-data.md)). Detalji o zajedničkim Listing atributima → **Ch.04, sekcija 4.1**. Specifični Event atributi → **Ch.04, sekcija 4.2**. Dvojezična polja → **Ch.04**, napomena o dvojezičnosti u 4.1.

**Acceptance criteria:**

- [ ] Korisnik može otvoriti formu za kreiranje novog Event-a
- [ ] Forma sadrži sva obavezna polja: `name`, `description`, `startDateTime`, `endDateTime`, primarna kategorija
- [ ] Forma sadrži opciona polja: `nameAlt`, `descriptionAlt`, `excerpt`, `excerptAlt`, `listingUrl`, sekundarne kategorije, tagovi (do `MAX_TAGS_PER_LISTING`)
- [ ] `endDateTime` se automatski postavlja na isti dan kao `startDateTime` ako korisnik ne unese vrijednost
- [ ] `startDateTime` ne može biti u prošlosti
- [ ] Korisnik bira primarnu kategoriju kroz sektor → kategorija flow (samo EventCategory)
- [ ] Sekundarne kategorije se biraju iz istog tipa (EventCategory), do `MAX_SECONDARY_CATEGORIES`
- [ ] `excerpt` se auto-generiše iz `description` ako ga korisnik ne popuni
- [ ] Listing se kreira u statusu `listingStatus = draft`
- [ ] `sortDate` se postavlja na trenutno vrijeme pri kreiranju
- [ ] `ownerId` se automatski postavlja na ID ulogovanog korisnika
- [ ] Validacijske greške se prikazuju inline uz odgovarajuće polje
- [ ] Nakon uspješnog kreiranja, korisnik se preusmjerava na stranicu drafta sa opcijom za dalji edit ili objavu

**Backend Scope:**

- `POST /events` — prima listing podatke (name, description, startDateTime, endDateTime, primaryCategoryId, sekundarneKategorije, tagovi, dvojezična polja, listingUrl), vraća kreirani Event sa ID-em i statusom
- Validacija: `name` obavezan, `description` obavezan (min 50 karaktera), `startDateTime` obavezan i ne smije biti u prošlosti, `endDateTime` ≥ `startDateTime`, `primaryCategoryId` mora postojati u EventCategory i biti aktivan, sekundarne kategorije moraju biti iz EventCategory
- Side effects: kreira zapis u ListingCategories relacionoj tabeli, denormalizuje `primaryCategoryData` u Listing entitet, postavlja `sortDate`, `createdAt`, `updatedAt`

**Frontend Scope:**

- UI: Višekoračna forma ili single-page forma sa sekcijama — osnovni podaci, datum/vrijeme, kategorija/tagovi, dvojezični sadržaj, kontakt
- Klijentska validacija: obavezna polja, `description` min 50 karaktera, `startDateTime` ne u prošlosti, `endDateTime` ≥ `startDateTime`
- UX: nakon uspješnog kreiranja redirect na draft pregled sa toast "Event kreiran"; pri greški inline poruke uz polja; sektor → kategorija picker sa filtriranim listama

**Tehničke napomene:**

- Lokacija Event-a je zasebna storija ([S02-03](s02-03-lokacija-event-a-povezivanje-sa-place-om-ili-rucna-adresa.md)) — ova forma ne uključuje lokacijske podatke
- Slike i dokumenti su zasebne storije ([S02-05](s02-05-upload-i-upravljanje-slikama-listinga.md), [S02-06](s02-06-upload-i-upravljanje-dokumentima-listinga.md)) — upload nije dio ove forme
- Lista kategorija i tagova dolazi iz seed data ([E03a](../e03a-kategorizacija-sadrzaja-entiteti-i-seed-data.md))

**Testovi (MVP):**

- [ ] Happy path: kreiranje Event-a sa svim obaveznim poljima → draft kreiran
- [ ] Kreiranje Event-a sa opcionalnim dvojezičnim poljima → sva polja sačuvana
- [ ] `startDateTime` u prošlosti → validacijska greška
- [ ] `endDateTime` prije `startDateTime` → validacijska greška
- [ ] Bez primarne kategorije → validacijska greška
- [ ] `description` kraći od 50 karaktera → validacijska greška
- [ ] Kreiranje sa sekundarnim kategorijama iz pogrešnog tipa (PlaceCategory) → greška

**Wireframe referenca:** —

**Implementacijske napomene:**

- Razmotriti rich text editor za `description` polje (Markdown ili WYSIWYG)
- Sektor → kategorija picker može koristiti grouped dropdown ili dvostepeni selektor
- Auto-generisanje excerpta: prvih ~150 karaktera iz description, bez HTML tagova