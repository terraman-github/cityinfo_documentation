---
id: S01-07
confluence_page_id: "250839063"
parent_epic: E01
linear_id: "CIT2-7"
phase: MVP
journey_milestones: [J-01]
type: fullstack
---

**Naslov:** Brisanje korisničkog računa (GDPR)

**Excerpt:** Korisnik ima pravo obrisati svoj račun — GDPR to zahtijeva. Brisanje je soft delete sa 30-dnevnim grace periodom tokom kojeg se račun može reaktivirati. Nakon 30 dana, podaci se trajno brišu. Aktivni listinzi i promocije se moraju obraditi pri brisanju.

**Phase:** MVP

**Journey milestones:** J-01

**User story:**  
Kao korisnik koji želi napustiti platformu,

želim obrisati svoj račun i sve vezane podatke,

kako bih ostvario svoje pravo na brisanje podataka prema GDPR-u.

**Kontekst:** Korisnik pristupa opciji brisanja kroz profil. Brisanje postavlja `accountStatus = deleted` i pokreće 30-dnevni countdown. Tokom tog perioda, korisnik se ne može prijaviti, ali podaci postoje u bazi. Nakon 30 dana, background job trajno briše podatke. Detalji o accountStatus → **Ch.03, sekcija 3.3**. Endpoint: `DELETE /users/me` (**Ch.03, sekcija 3.8**).

**Acceptance criteria:**

- [ ] Korisnik može zatražiti brisanje računa kroz profil
- [ ] Brisanje zahtijeva potvrdu (npr. unos lozinke ili dvostruki klik/modal)
- [ ] `accountStatus` se postavlja na `deleted`, `deletedAt` se bilježi
- [ ] Korisnik se odmah odjavljuje sa svih uređaja
- [ ] Korisnik se ne može prijaviti dok je `accountStatus = deleted`
- [ ] Aktivni listinzi korisnika prelaze u `closed` sa odgovarajućim razlogom
- [ ] Aktivne promocije se otkazuju (povrat kredita — politika se definira u [E10](../e10-promocije-listinga.md))
- [ ] Korisnik može reaktivirati račun unutar 30 dana (npr. putem support kontakta ili posebnog linka)
- [ ] Nakon 30 dana, background job trajno briše korisničke podatke iz baze
- [ ] Trajno brisanje uključuje lične podatke — anonimizacija umjesto kompletnog brisanja gdje je potrebno za integritet podataka (npr. transakcije)

**Backend Scope:**

- `DELETE /users/me` — prima {password} za potvrdu, postavlja `accountStatus = deleted` i `deletedAt = now()`
- Validacija: provjera lozinke za potvrdu identiteta
- Side effects: invalidacija svih sesija korisnika; zatvaranje aktivnih listinga (`closed` sa odgovarajućim razlogom); otkazivanje aktivnih promocija; background job za trajno brisanje nakon 30 dana (dio [E14](../e14-infrastruktura-i18n-i-pozadinski-procesi.md) infrastrukture)

**Frontend Scope:**

- UI: "Obriši račun" opcija na profil stranici; konfirmacioni modal sa upozorenjem o posledicama i poljem za unos lozinke
- UX: klik na "Obriši" → modal sa jasnim upozorenjem ("Vaš račun će biti trajno obrisan nakon 30 dana. Aktivni listinzi će biti zatvoreni.") + unos lozinke za potvrdu; nakon potvrde → odjava i redirect na landing stranicu sa porukom "Račun je označen za brisanje"

**Tehničke napomene:**

- Background job za cleanup je dio [E14](../e14-infrastruktura-i18n-i-pozadinski-procesi.md) infrastrukture (soft delete cleanup).
- Razlika između `inactive` (korisnik pauzira) i `deleted` (korisnik briše) — **Ch.03, sekcija 3.3**.

**Testovi (MVP):**

- [ ] Brisanje računa uspješno postavlja accountStatus na deleted
- [ ] Korisnik se ne može prijaviti nakon brisanja
- [ ] Aktivni listinzi su zatvoreni
- [ ] Reaktivacija unutar 30 dana vraća račun u active stanje
- [ ] (Background job test) — nakon 30 dana podaci su trajno obrisani/anonimizirani

**Wireframe referenca:** —