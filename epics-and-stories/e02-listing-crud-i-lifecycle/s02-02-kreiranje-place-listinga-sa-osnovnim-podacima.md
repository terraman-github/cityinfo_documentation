---
id: S02-02
parent_epic: E02
linear_id: ""
phase: MVP
journey_milestones: [J-02]
type: fullstack
---

# S02-02 — Kreiranje Place listinga sa osnovnim podacima

<a id="s02-02-kreiranje-place-listinga-sa-osnovnim-podacima"></a>

# S02-02 — Kreiranje Place listinga sa osnovnim podacima

**Naslov:** Kreiranje Place listinga sa osnovnim podacima

**Excerpt:** Omogućava korisniku da kreira novi Place listing — restoran, prodavnicu, muzej ili bilo koji drugi tip mjesta — popunjavanjem obaveznih polja uključujući adresu i geolokaciju. Place je stalna lokacija bez vremenskog ograničenja.

**Phase:** MVP

**Journey milestones:** **J-02**

**User story:**  
Kao vlasnica biznisa,  
želim kreirati Place listing sa informacijama o mom poslovnom objektu,  
kako bih ga učinila vidljivim na platformi i privukla korisnike.

**Kontekst:** Korisnik je ulogovan, ima verificiran telefon. Pristupa formi za kreiranje Place-a kroz navigaciju. Place listing zahtijeva fizičku adresu i koordinate — za razliku od Event-a koji ima fleksibilniju lokaciju. Listing se kreira u `listingStatus = draft`. Detalji o Place atributima → **Ch.04, sekcija 4.3**. Zajednički atributi → **Ch.04, sekcija 4.1**.

**Acceptance criteria:**

- [ ] Korisnik može otvoriti formu za kreiranje novog Place-a
- [ ] Forma sadrži sva obavezna polja: `name`, `description`, `addressLine`, `city`, `latitude`, `longitude`, primarna kategorija
- [ ] Forma sadrži opciona polja: `nameAlt`, `descriptionAlt`, `excerpt`, `excerptAlt`, `listingUrl`, sekundarne kategorije, tagovi (do `MAX_TAGS_PER_LISTING`)
- [ ] Korisnik bira primarnu kategoriju kroz sektor → kategorija flow (samo PlaceCategory)
- [ ] Sekundarne kategorije se biraju iz istog tipa (PlaceCategory), do `MAX_SECONDARY_CATEGORIES`
- [ ] Adresa se unosi ručno ili putem Google Places autocomplete koji popunjava polja i koordinate
- [ ] `googlePlusCode` se automatski generiše iz koordinata
- [ ] `excerpt` se auto-generiše iz `description` ako ga korisnik ne popuni
- [ ] Listing se kreira u statusu `listingStatus = draft`
- [ ] `sortDate` se postavlja na trenutno vrijeme pri kreiranju
- [ ] Validacijske greške se prikazuju inline
- [ ] Nakon uspješnog kreiranja, korisnik se preusmjerava na stranicu drafta

**Backend Scope:**

- `POST /places` — prima listing podatke (name, description, addressLine, city, latitude, longitude, primaryCategoryId, sekundarneKategorije, tagovi, dvojezična polja, listingUrl), vraća kreirani Place sa ID-em
- Validacija: `name` obavezan, `description` obavezan (min 50 karaktera), `addressLine` obavezan, `city` obavezan, `latitude`/`longitude` obavezni i unutar validnog opsega, `primaryCategoryId` mora postojati u PlaceCategory
- Side effects: generisanje `googlePlusCode` iz koordinata (Google Maps API), kreira zapis u ListingCategories, denormalizuje `primaryCategoryData`

**Frontend Scope:**

- UI: forma sa sekcijama — osnovni podaci, lokacija (mapa + adresna polja), kategorija/tagovi, dvojezični sadržaj
- Klijentska validacija: obavezna polja, `description` min 50 karaktera, koordinate u validnom opsegu
- UX: Google Places autocomplete za adresu sa automatskim popunjavanjem koordinata; interaktivna mapa za vizuelnu potvrdu lokacije (pin); toast i redirect nakon uspjeha

**Tehničke napomene:**

- Google Maps API integracija je potrebna za autocomplete i Plus Code generisanje — ovo je zavisnost na [E14](../e14-infrastruktura-i18n-i-pozadinski-procesi.md) (infrastruktura)
- Slike i dokumenti su zasebne storije ([S02-05](s02-05-upload-i-upravljanje-slikama-listinga.md), [S02-06](s02-06-upload-i-upravljanje-dokumentima-listinga.md))

**Testovi (MVP):**

- [ ] Happy path: kreiranje Place-a sa svim obaveznim poljima → draft kreiran
- [ ] Google Places autocomplete popunjava adresu i koordinate → sva polja ispravna
- [ ] Kreiranje bez adrese → validacijska greška
- [ ] Kreiranje sa PlaceCategory kategorijama → uspješno; pokušaj sa EventCategory → greška
- [ ] `googlePlusCode` se automatski generiše iz koordinata
- [ ] Kreiranje sa dvojezičnim poljima → sva polja sačuvana

**Wireframe referenca:** —

**Implementacijske napomene:**

- Mapa može koristiti Google Maps JS API sa draggable markerom za fino podešavanje pozicije
- Autocomplete treba biti ograničen na državu tenanta za bolje rezultate