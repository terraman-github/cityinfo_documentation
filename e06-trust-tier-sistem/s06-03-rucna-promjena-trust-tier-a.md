# S06-03 — Ručna promjena Trust Tier-a

**Naslov:** Ručna promjena Trust Tier-a

**Excerpt:** Moderatori mogu ručno promijeniti Trust Tier korisnika — bilo da se radi o degradaciji problemtičnog korisnika na Restricted, postavljanju poslovnog partnera na Verified Partner (Tier 4), ili vraćanju korisnika iz Restricted-a nakon pregleda. Osjetljive akcije (Tier 0 i Tier 4) zahtijevaju `can_manage_trust_tier` permisiju.

**Phase:** MVP

**Journey milestones:** J-03, J-08

**User story:**  
Kao moderator,  
želim ručno promijeniti Trust Tier korisnika,  
kako bih mogao reagovati na situacije koje automatski sistem ne pokriva — od ozbiljnih kršenja do uspostavljanja poslovnih partnerstava.

**Kontekst:** Ručna promjena tier-a pokriva scenarije koji zahtijevaju ljudsku procjenu: degradacija zbog ozbiljnog kršenja (hate speech, spam, ilegalni sadržaj) direktno na Tier 0, promjena sa Tier 3 na Tier 2 zbog problema u samplingu, ili postavljanje Tier 4 za ugovorne partnere. Akcije prema Tier 0 i Tier 4 zahtijevaju `can_manage_trust_tier` permisiju — ostale promjene (npr. Tier 3 → Tier 2) mogu izvršiti svi moderatori. Staff sa ulogom `local_admin` ima inherentnu ovlast za sve akcije. Detalji → Ch.03, sekcija 3.4 (Degradacija); Ch.05, sekcija 5.4.

**Acceptance criteria:**

- [ ] Moderator može promijeniti Trust Tier korisnika kroz Staff panel
- [ ] Promjena na Tier 0 (Restricted) zahtijeva `can_manage_trust_tier` permisiju
- [ ] Postavljanje na Tier 4 (Verified Partner) zahtijeva `can_manage_trust_tier` permisiju
- [ ] Ostale promjene (npr. Tier 3 → Tier 2) mogu izvršiti svi moderatori
- [ ] Staff sa ulogom `local_admin` može izvršiti sve promjene bez eksplicitnih permisija
- [ ] Svaka ručna promjena zahtijeva unos razloga (obavezno tekstualno polje)
- [ ] Promjena se odmah reflektuje na korisnika — sljedeća objava koristi novi tier
- [ ] Audit log bilježi: ko je promijenio, prethodni tier, novi tier, razlog, timestamp
- [ ] Korisnik na Tier 0 može biti vraćen na Tier 1 (ili viši) samo ručnom intervencijom moderatora sa `can_manage_trust_tier`

**Backend Scope:**

- `PATCH /staff/users/{userId}/trust-tier` — prima: `newTier` (Number 0–4), `reason` (String, obavezno)
- Validacija permisija: za Tier 0 i Tier 4 provjeriti `can_manage_trust_tier` ili `local_admin` ulogu
- Update `trustTier` na User entitetu
- Audit log entry sa before/after vrijednostima
- Side effect: ako se korisnik degradira ispod Tier 3, automatski ukloniti `isVerifiedPublisher` flag (→ S06-04)

**Frontend Scope:**

- UI: dropdown ili input za odabir novog tier-a na korisničkom profilu u Staff panelu
- Polje za razlog (obavezno)
- Vizualni indikator trenutnog tier-a
- Prikaz permisijskih ograničenja: Tier 0 i Tier 4 opcije vidljive samo moderatorima sa odgovarajućom permisijom (ili local\_admin-u)
- UX: potvrda prije izvršenja ("Da li ste sigurni?"), toast notifikacija nakon uspjeha

**Tehničke napomene:**

- Ova storija pokriva i "izlaz iz Tier 0" — jedini način je ručna promjena moderatora sa `can_manage_trust_tier`.
- Degradacija ispod Tier 3 mora triggerovati automatsko uklanjanje `isVerifiedPublisher` flaga. To je cross-cutting logika koja se referencira iz S06-04.

**Testovi (MVP):**

- [ ] Moderator sa `can_manage_trust_tier` degradira korisnika na Tier 0 → uspješno, audit log kreiran
- [ ] Moderator bez `can_manage_trust_tier` pokušava degradirati na Tier 0 → odbijeno (403)
- [ ] Moderator sa `can_manage_trust_tier` postavlja korisnika na Tier 4 → uspješno
- [ ] Moderator mijenja Tier 3 → Tier 2 bez posebne permisije → uspješno
- [ ] local\_admin postavlja Tier 4 → uspješno (inherentna ovlast)
- [ ] Promjena bez unesenog razloga → validacijska greška
- [ ] Degradacija sa Tier 3 na Tier 1 → `isVerifiedPublisher` se automatski uklanja

**Wireframe referenca:** —