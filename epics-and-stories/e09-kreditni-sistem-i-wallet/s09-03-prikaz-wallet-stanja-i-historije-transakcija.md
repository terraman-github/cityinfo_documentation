---
id: S09-03
parent_epic: E09
linear_id: ""
phase: MVP
journey_milestones: [J-09]
type: fullstack
---

# S09-03 — Prikaz wallet stanja i historije transakcija

**Naslov:** Prikaz wallet stanja i historije transakcija

**Excerpt:** Korisnik pristupa wallet stranici gdje vidi trenutno stanje kredita i kompletnu historiju transakcija — kupovine, trošenja na promocije, admin korekcije. Transparentnost troškova i zarada je ključna za povjerenje korisnika u monetizacijski sistem.

**Phase:** MVP

**Journey milestones:** **J-09**

**User story:**  
Kao korisnik platforme,  
želim pregledati stanje wallet-a i historiju svih transakcija,  
kako bih imao potpunu kontrolu i pregled nad svojim troškovima i dopunama.

**Kontekst:** Korisnik pristupa wallet stranici kroz header (klik na wallet stanje) ili kroz navigaciju u profilu. Stranica prikazuje trenutno stanje i listu transakcija sa filtrima. Svaka transakcija ima tip, iznos (+/-), opis i datum. Detalji o CreditTransaction entitetu → **Ch.06, sekcija 6.1**.4; tipovi transakcija → **Ch.06, sekcija 6.1**.4.

**Acceptance criteria:**

- [ ] Wallet stranica prikazuje trenutno stanje kredita na vrhu
- [ ] Lista transakcija prikazuje: tip, iznos (sa predznakom + ili -), opis, datum, i `balanceAfter`
- [ ] Transakcije su sortirane od najnovije prema najstarijoj (default)
- [ ] Lista je paginirana
- [ ] Filter po tipu transakcije (purchase, promo\_purchase, refund, admin\_credit, admin\_debit, itd.)
- [ ] Filter po datumskom rasponu (od — do)
- [ ] Pozitivne transakcije (dopune) su vizualno označene zelenom, negativne (trošenja) crvenom
- [ ] Prazna lista prikazuje poruku "Nemate transakcija" sa CTA za kupovinu kredita
- [ ] Klik na transakciju sa `referenceType` / `referenceId` vodi na povezani entitet (npr. promocija, paket)

**Backend Scope:**

- `GET /wallet` — vraća `{ balance, currency }`
- `GET /wallet/transactions` — paginirano, sa filterima: `type`, `dateFrom`, `dateTo`, `sortBy`, `sortOrder`
- `GET /wallet/transactions/{id}` — detalji pojedinačne transakcije
- Response za listu: `{ items: [...], totalCount, page, pageSize }`

**Frontend Scope:**

- UI: Wallet stranica sa balance prikazom na vrhu, CTA "Kupi kredite" dugme, i lista transakcija ispod
- UI: Filter bar sa dropdown za tip i date picker za raspon
- UI: Transakcija redak: ikona tipa, opis, iznos (obojen), datum, stanje nakon
- Klijentska validacija: nema — čisto prikaz
- UX: Klik na wallet stanje u headeru vodi ovdje; prazno stanje pokazuje helpful poruku

**Tehničke napomene:**

- `balanceBefore` i `balanceAfter` omogućavaju korisniku da rekonstruiše tok promjena bez sumnje
- Transakcijski log je append-only — jednom kreiran zapis se ne mijenja

**Testovi (MVP):**

- [ ] Wallet stranica prikazuje ispravno stanje
- [ ] Lista transakcija prikazuje sve transakcije korisnika paginirano
- [ ] Filter po tipu vraća samo transakcije tog tipa
- [ ] Filter po datumu vraća transakcije unutar raspona
- [ ] Prazan wallet prikazuje poruku sa CTA za kupovinu

**Wireframe referenca:** —