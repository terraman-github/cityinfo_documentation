---
id: S09-01
parent_epic: E09
linear_id: ""
phase: MVP
journey_milestones: [J-09]
type: fullstack
---

# S09-01 — Kreiranje wallet-a pri registraciji korisnika

**Naslov:** Kreiranje wallet-a pri registraciji korisnika

**Excerpt:** Svaki korisnik automatski dobija wallet pri registraciji sa početnim stanjem 0 kredita. Wallet je preduvjet za sve monetizacijske funkcionalnosti — bez njega korisnik ne može kupovati kredite niti aktivirati promocije.

**Phase:** MVP

**Journey milestones:** **J-09**

**User story:**  
Kao sistem,  
želim automatski kreirati wallet za svakog novog korisnika pri registraciji,  
kako bi korisnik imao spreman račun za kupovinu kredita čim mu zatreba.

**Kontekst:** Wallet se kreira kao dio registracijskog procesa ([E01](../e01-korisnicka-registracija-i-profil.md)). Početno stanje je 0 kredita, minimalni balans je 0 (ne može biti negativan). Wallet stanje treba biti vidljivo korisniku u header-u aplikacije od prvog logina. Detalji o wallet konceptu → **Ch.06, sekcija 6.1**.2.

**Acceptance criteria:**

- [ ] Pri uspješnoj registraciji korisnika, automatski se kreira wallet sa `balance: 0`
- [ ] Kreiranje wallet-a je dio iste transakcije kao registracija — ako jedno padne, pada i drugo
- [ ] Wallet se ne kreira duplikat ako korisnik već ima wallet (idempotentnost)
- [ ] `GET /wallet` vraća wallet stanje za ulogovanog korisnika
- [ ] Wallet balance ne može biti negativan — ovo je enforceano na nivou sistema

**Backend Scope:**

- Wallet se kreira kao dio registracijskog flow-a — nije zaseban endpoint za kreiranje
- `GET /wallet` — vraća `{ balance, currency }` za ulogovanog korisnika
- Validacija: korisnik mora biti autentificiran

**Frontend Scope:**

- UI: Wallet stanje prikazano u header-u aplikacije (npr. "💰 0 kredita") — uvijek vidljivo kad je korisnik ulogovan
- UX: Klik na wallet stanje vodi na wallet stranicu ([S09-03](s09-03-prikaz-wallet-stanja-i-historije-transakcija.md))

**Tehničke napomene:**

- Wallet je per-user entitet — jedan korisnik, jedan wallet
- Za MVP, nema koncepta "isteka" kredita (validityDays na paketu može biti NULL)

**Testovi (MVP):**

- [ ] Registracija korisnika rezultira kreiranjem wallet-a sa `balance: 0`
- [ ] `GET /wallet` za novog korisnika vraća `balance: 0`
- [ ] Header prikazuje wallet stanje nakon logina
- [ ] Neuspjela registracija ne ostavlja orphan wallet

**Wireframe referenca:** —