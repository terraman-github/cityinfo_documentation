---
id: S08-03
parent_epic: E08
linear_id: "CIT2-53"
phase: MVP
journey_milestones: [J-03, J-07]
type: fullstack
---

# S08-03 — Odgovor vlasnika listinga na poruku moderatora

**Naslov:** Odgovor vlasnika listinga na poruku moderatora

**Excerpt:** Vlasnik listinga odgovara na poruku moderatora kroz isti thread. Ovo je druga strana komunikacijskog toka — korisnik vidi primljene poruke u svom profilu i može odgovoriti sa tekstom. Thread prelazi u `waiting_moderator` kada vlasnik odgovori.

**Phase:** MVP

**Journey milestones:** **J-03**, **J-07**

**User story:**  
Kao vlasnik listinga,  
želim odgovoriti na poruku moderatora kroz message thread,  
kako bih mogao dostaviti tražene informacije ili pojašnjenja bez korištenja eksternih kanala.

**Kontekst:** Vlasnik listinga prima obavijest (notifikacija — obrađena u [E12](../e12-notifikacije.md)) da je moderator poslao poruku. Korisnik pristupa thread-u kroz svoj profil ili kroz listing detail stranicu. Thread je u statusu `waiting_owner` ili `waiting_moderator` — u oba slučaja vlasnik može slati poruku. Kada je thread u `idle` statusu, vlasnik ne može slati poruke — samo moderator može pokrenuti komunikaciju. Detalji o kontroli pristupa → **Ch.07, sekcija 7.1**.4.

**Acceptance criteria:**

- [ ] Vlasnik listinga može poslati tekstualnu poruku u thread kada je status `waiting_owner` ili `waiting_moderator`
- [ ] Vlasnik ne može poslati poruku kada je thread u statusu `idle` — API vraća odgovarajuću grešku
- [ ] Slanje poruke iz `waiting_owner` statusa mijenja thread status u `waiting_moderator`
- [ ] Slanje poruke iz `waiting_moderator` statusa ne mijenja status (vlasnik dopunjuje prethodni odgovor)
- [ ] Poruka se kreira sa `senderRole: owner` i ispravnim `senderId`
- [ ] `messageCount`, `lastMessageAt` i `lastMessageBy` se ažuriraju
- [ ] Poruka ne može biti prazna
- [ ] Samo vlasnik listinga može slati poruke kao `owner` — drugi korisnici ne mogu pristupiti thread-u

**Backend Scope:**

- `POST /threads/{threadId}/messages` — isti endpoint kao za moderatora, ali sa `senderRole: owner`
- Validacija: korisnik je vlasnik listinga, thread nije u `idle` statusu, `messageText` neprazan
- Side effects: ažurira thread status, `messageCount`, `lastMessageAt`, `lastMessageBy`

**Frontend Scope:**

- UI: Lista primljenih poruka sa mogućnošću odgovora — textarea i dugme "Odgovori" unutar thread prikaza
- UI: Thread je dostupan kroz profil korisnika (sekcija "Poruke" ili "Komunikacija") i kroz listing detail stranicu
- Klijentska validacija: `messageText` neprazan, dugme "Odgovori" je onemogućeno kad je thread `idle`
- UX: nakon uspješnog slanja poruka se pojavljuje u thread-u; pri grešci inline poruka

**Tehničke napomene:**

- Endpoint za slanje poruka je isti za moderatora i vlasnika — razlika je u autorizaciji i `senderRole` koji se određuje na osnovu korisnikovog identiteta
- Vlasnik vidi samo poruke iz svog thread-a — nema pristup tuđim thread-ovima

**Testovi (MVP):**

- [ ] Vlasnik šalje poruku u `waiting_owner` thread — status prelazi u `waiting_moderator`
- [ ] Vlasnik šalje dodatnu poruku u `waiting_moderator` thread — status ostaje isti
- [ ] Vlasnik pokušava slati poruku u `idle` thread — API vraća grešku
- [ ] Korisnik koji nije vlasnik listinga pokušava slati poruku — API vraća grešku
- [ ] Poruka se ispravno prikazuje u thread-u sa oznakom `owner`

**Wireframe referenca:** —

**Implementacijske napomene:** User UI za poruke može biti jednostavna lista poruka sa textarea na dnu — ne treba komplikovan chat interfejs. Kronološki redoslijed (starije gore, novije dole) je najprirodniji za ovaj tip komunikacije.