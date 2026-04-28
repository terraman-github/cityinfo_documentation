---
id: S01-02
parent_epic: E01
linear_id: ""
phase: MVP
journey_milestones: [J-01]
type: fullstack
---

# S01-02 — Email verifikacija

**Naslov:** Email verifikacija

**Excerpt:** Nakon registracije, korisnik mora potvrditi email adresu klikom na link koji dobije u inbox. Bez verificiranog emaila, korisnik ima ograničen pristup platformi — ne može kreirati sadržaj.

**Phase:** MVP

**Journey milestones:** **J-01**

**User story:**  
Kao novoregistrovani korisnik,  
želim potvrditi svoju email adresu klikom na verifikacioni link,  
kako bih dokazao da imam pristup tom emailu i otključao punu funkcionalnost platforme.

**Kontekst:** Odmah nakon registracije ([S01-01](s01-01-registracija-novog-korisnika.md)), korisnik prima email sa verifikacionim linkom. Korisnik se može prijaviti i prije verifikacije emaila, ali ne može kreirati listinge dok email nije potvrđen (uz dodatni preduslov verifikacije telefona — [S01-03](s01-03-verifikacija-telefona-sms.md)). Ovo je standardni tok iz **Ch.02, sekcija 2.7** — korak "Email verifikacija".

**Acceptance criteria:**

- [ ] Verifikacioni email se šalje automatski nakon uspješne registracije
- [ ] Email sadrži jedinstven, vremenski ograničen link za potvrdu
- [ ] Klik na validan link postavlja `emailVerified = true`
- [ ] Klik na istekli link prikazuje poruku sa opcijom za slanje novog linka
- [ ] Korisnik može zatražiti ponovni slanje verifikacionog emaila (resend)
- [ ] Resend ima rate limiting — ne može se zatražiti neograničen broj puta
- [ ] Korisnik koji nije verificirao email vidi jasnu poruku/banner sa pozivom na verifikaciju

**Backend Scope:**

- `POST /auth/verify-email` — prima {token}, vraća {success}. Postavlja `emailVerified = true`.
- `POST /auth/resend-verification` — prima {email}, triggeruje novi verifikacioni email. Rate limited.
- Validacija: token validnost (istekao?), token jedinstvenost (već iskorišten?)
- Side effects: slanje emaila sa verifikacionim linkom (automatski pri registraciji i pri resend-u)

**Frontend Scope:**

- UI: landing stranica za verifikacioni link (success/error prikaz); banner na dashboard-u za neveificirani email sa "Pošalji ponovo" dugmetom
- UX: klik na validan link → success poruka + redirect na login/dashboard; istekli link → error poruka + "Pošalji novi link" dugme; resend → potvrda "Email poslat" ili rate limit poruka

**Tehničke napomene:**

- Verifikacioni token treba imati razumno vrijeme isteka (npr. 24–48h) — konfigurisano, ne hardkodirano.
- Rate limiting za resend spriječava spam — detalji su implementacijski.

**Testovi (MVP):**

- [ ] Klik na validan verifikacioni link uspješno verificira email
- [ ] Klik na istekli link prikazuje odgovarajuću poruku i nudi resend
- [ ] Resend funkcioniše i šalje novi email
- [ ] Višestruki brzi resend zahtjevi su ograničeni (rate limited)

**Wireframe referenca:** —