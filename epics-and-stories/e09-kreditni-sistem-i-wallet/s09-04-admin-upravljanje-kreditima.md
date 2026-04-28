---
id: S09-04
parent_epic: E09
linear_id: ""
phase: MVP
journey_milestones: [J-09]
type: fullstack
---

# S09-04 — Admin upravljanje kreditima

**Naslov:** Admin upravljanje kreditima

**Excerpt:** Staff/admin može ručno dodati ili oduzeti kredite korisniku — za korekcije, kompenzacije, ili penalizacije. Svaka admin operacija kreira CreditTransaction sa odgovarajućim tipom i opisom za potpunu revizijsku traživost.

**Phase:** MVP

**Journey milestones:** **J-09**

**User story:**  
Kao admin/staff,  
želim ručno dodati ili oduzeti kredite korisniku,  
kako bih mogao rješavati izuzetne situacije (kompenzacije, korekcije grešaka, penalizacije) bez direktnog pristupa bazi.

**Kontekst:** U operativnom radu će se pojaviti situacije koje zahtijevaju ručnu korekciju wallet stanja — npr. korisnik je imao tehnički problem pri kupovini pa mu se odobrava kompenzacija, ili je zloupotrijebio sistem pa se oduzimaju krediti. Admin pristupa korisničkom profilu u Staff panelu i koristi formu za dodavanje/oduzimanje kredita. Svaka operacija zahtijeva opis razloga. Detalji o admin operacijama → **Ch.06, sekcija 6.1**.4 (tipovi `admin_credit` i `admin_debit`).

**Acceptance criteria:**

- [ ] Staff može dodati kredite korisniku kroz admin formu — kreira CreditTransaction sa `type: admin_credit`
- [ ] Staff može oduzeti kredite korisniku — kreira CreditTransaction sa `type: admin_debit`
- [ ] Oduzimanje ne može rezultirati negativnim wallet balansom — API vraća grešku ako pokušaj oduzimanja premašuje stanje
- [ ] Svaka admin operacija zahtijeva `description` (razlog) — polje je obavezno
- [ ] CreditTransaction sadrži `balanceBefore` i `balanceAfter` za audit
- [ ] Korisnik vidi admin operacije u svojoj historiji transakcija ([S09-03](s09-03-prikaz-wallet-stanja-i-historije-transakcija.md)) sa oznakom tipa
- [ ] Operacija je vidljiva u admin pregledu korisnikovog wallet-a

**Backend Scope:**

- `POST /admin/credits/add` — prima `{ userId, amount, description }`, vraća `{ transactionId, newBalance }`
- `POST /admin/credits/deduct` — prima `{ userId, amount, description }`, vraća `{ transactionId, newBalance }`
- Validacija: `amount` > 0, `description` neprazan, korisnik postoji, za deduct: wallet balance >= amount
- Side effects: CreditTransaction zapis, wallet balance update (atomska operacija)

**Frontend Scope:**

- UI: Forma u Staff panelu na korisničkom profilu — polja: iznos (Number), razlog (Text), akcija (Dodaj / Oduzmi)
- UI: Prikaz trenutnog wallet stanja korisnika prije operacije
- Klijentska validacija: iznos > 0, razlog neprazan
- UX: Potvrda prije izvršenja ("Da li ste sigurni da želite dodati/oduzeti X kredita korisniku Y?"); po uspjehu toast sa novim stanjem

**Tehničke napomene:**

- Admin operacije su Staff-only — korisnici ne mogu ručno dodavati kredite sebi
- Opis razloga je bitan za audit — bez njega operacija nema smisla pri kasnijoj reviziji

**Testovi (MVP):**

- [ ] Admin dodaje kredite — wallet balance se povećava, CreditTransaction kreiran sa `admin_credit`
- [ ] Admin oduzima kredite — wallet balance se smanjuje, CreditTransaction kreiran sa `admin_debit`
- [ ] Pokušaj oduzimanja više kredita nego što korisnik ima vraća grešku
- [ ] Operacija bez opisa vraća validacijsku grešku
- [ ] Korisnik vidi admin korekcije u svojoj historiji transakcija

**Wireframe referenca:** —