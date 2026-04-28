---
id: S01-05
parent_epic: E01
linear_id: ""
phase: MVP
journey_milestones: [J-01]
type: fullstack
---

# S01-05 — Zaboravljena lozinka i reset

**Naslov:** Zaboravljena lozinka i reset

**Excerpt:** Korisnik koji je zaboravio lozinku može zatražiti reset putem emaila. Standardan flow — unese email, primi link, postavi novu lozinku. Jednostavno ali kritično jer bez ovoga korisnici gube pristup računu.

**Phase:** MVP

**Journey milestones:** **J-01**

**User story:**  
Kao korisnik koji je zaboravio lozinku,  
želim zatražiti reset putem emaila i postaviti novu lozinku,  
kako bih ponovo mogao pristupiti svom računu.

**Kontekst:** Korisnik je na login stranici i ne može se sjetiti lozinke. Klikne "Zaboravljena lozinka", unese email, i prima link za reset. Ovo je standardan sigurnosni flow — API endpointi su definirani u **Ch.03, sekcija 3.8** (`/auth/forgot-password`, `/auth/reset-password`).

**Acceptance criteria:**

- [ ] Korisnik može zatražiti reset lozinke unosom email adrese
- [ ] Sistem šalje email sa reset linkom — bez obzira da li email postoji u sistemu (ne otkriva registraciju)
- [ ] Reset link je jedinstven i vremenski ograničen (konfigurisano, npr. 1h)
- [ ] Klik na validan link vodi na formu za postavljanje nove lozinke
- [ ] Nova lozinka prolazi istu validaciju kao pri registraciji
- [ ] Uspješan reset invalidira reset link (ne može se koristiti ponovo)
- [ ] Uspješan reset invalidira sve postojeće sesije korisnika (sigurnosna mjera)
- [ ] Klik na istekli link prikazuje poruku sa opcijom za novi zahtjev

**Backend Scope:**

- `POST /auth/forgot-password` — prima {email}, šalje reset email. Uvijek vraća success (ne otkriva da li email postoji).
- `POST /auth/reset-password` — prima {token, newPassword}, vraća {success}. Postavlja novu lozinku.
- Validacija: token validnost (istekao? već iskorišten?), password policy za novu lozinku
- Side effects: slanje reset emaila, invalidacija reset tokena nakon uspješnog reseta, invalidacija svih aktivnih sesija korisnika

**Frontend Scope:**

- UI: (1) "Zaboravljena lozinka" forma sa email poljem; (2) "Postavi novu lozinku" forma sa password + confirm password
- Klijentska validacija: format emaila na prvoj formi; password match i minimalna dužina na drugoj
- UX: nakon zahtjeva → poruka "Ako email postoji, poslali smo link" (bez otkrivanja); nakon uspješnog reseta → poruka + redirect na login; istekli link → error sa "Zatraži novi link" dugmetom

**Testovi (MVP):**

- [ ] Zahtjev za reset sa validnim emailom šalje email
- [ ] Zahtjev za reset sa nepostojećim emailom ne otkriva da email ne postoji
- [ ] Reset sa validnim linkom i novom lozinkom uspješno mijenja lozinku
- [ ] Stari login kredencijali više ne rade nakon reseta
- [ ] Istekli reset link prikazuje odgovarajuću poruku

**Wireframe referenca:** —