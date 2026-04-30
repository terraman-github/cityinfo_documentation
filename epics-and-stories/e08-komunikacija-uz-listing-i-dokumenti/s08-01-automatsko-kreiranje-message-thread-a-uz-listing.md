---
id: S08-01
confluence_page_id: "252313611"
title: "S08-01 — Automatsko kreiranje message thread-a uz listing"
parent_epic: E08
linear_id: "CIT2-51"
phase: MVP
journey_milestones: [J-03]
type: backend-only
---

**Naslov:** Automatsko kreiranje message thread-a uz listing

**Excerpt:** Svaki listing (Event ili Place) automatski dobija message thread pri kreiranju. Thread je trajni komunikacijski kanal između moderatora i vlasnika — ne otvara se i ne zatvara, samo mijenja status ovisno o aktivnosti.

**Phase:** MVP

**Journey milestones:** J-03

**User story:**

*Kao sistem,*  
*želim automatski kreirati ListingMessageThread pri kreiranju svakog listinga,*  
*kako bi moderator imao spreman komunikacijski kanal kad god treba kontaktirati vlasnika.*

**Kontekst:** Kada korisnik kreira novi listing (Event ili Place), sistem pored samog listinga kreira i prazan message thread sa statusom `idle`. Thread živi koliko i listing — nema potrebe za ručnim otvaranjem ili zatvaranjem. Ovaj pristup osigurava da je komunikacijski kanal uvijek dostupan bez dodatne akcije. Detalji o thread modelu → **Ch.07, sekcija 7.1**.3.

**Acceptance criteria:**

- [ ] Pri kreiranju novog listinga (Event ili Place), automatski se kreira `ListingMessageThread` sa statusom `idle`
- [ ] Thread sadrži referencu na listing (`listingId`) i inicijalne vrijednosti (`messageCount: 0`, `assignedTo: null`, `lastMessageAt: null`)
- [ ] Kreiranje thread-a je dio iste transakcije kao kreiranje listinga — ako jedno padne, pada i drugo
- [ ] Thread se ne kreira duplikat ako listing već ima thread (idempotentnost)
- [ ] Pri brisanju listinga (soft delete), thread ostaje ali postaje nedostupan za nove poruke

**Backend Scope:**

- Thread se kreira kao dio `POST /listings` flow-a — nije zaseban endpoint
- Kreiranje je transakcijsko sa listingom (atomska operacija)
- `GET /listings/{listingId}/thread` — dohvat thread-a za listing (vraća thread sa osnovnim podacima)
- Validacija: listing mora postojati, thread ne smije već postojati za taj listing

**Tehničke napomene:**

- Thread kreiranje je interni side effect listing kreiranja, ne eksplicitna korisnička akcija
- Statusni model thread-a definisan u **Ch.07, sekcija 7.1**.3 — za ovu storiju relevantan je samo inicijalni status `idle`

**Testovi (MVP):**

- [ ] Kreiranje listinga rezultira kreiranjem thread-a sa statusom `idle` i `messageCount: 0`
- [ ] Dohvat thread-a po `listingId` vraća ispravan thread
- [ ] Pokušaj kreiranja drugog thread-a za isti listing ne kreira duplikat
- [ ] Neuspjelo kreiranje listinga ne ostavlja orphan thread u bazi

**Wireframe referenca:** —

**Implementacijske napomene:** Thread kreiranje se može riješiti kao dio istog servisnog metoda koji kreira listing — nema potrebe za event-driven pristupom u ovoj fazi.