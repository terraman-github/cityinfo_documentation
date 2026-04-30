---
id: S04-06
confluence_page_id: "252051457"
title: "S04-06 — Sortiranje po sortDate sa promocijskim prioritetima i paginacija"
parent_epic: E04
linear_id: "CIT2-32"
phase: MVP
journey_milestones: [J-04]
type: fullstack
---

**Naslov:** Sortiranje po sortDate sa promocijskim prioritetima i paginacija

**Excerpt:** Redoslijed listinga nije slučajan — kontroliše ga sortDate u kombinaciji sa promocijskim statusom. Premium listinzi imaju prioritet unutar kategorije, Premium+Homepage na naslovnoj. Dugi rezultati koriste lazy loading pristup sa cursor-based paginacijom.

**Phase:** MVP

**Journey milestones:** J-04

**User story:**

*Kao posjetilac,*  
*želim da mi se listinzi prikazuju u smislenom redoslijedu i da mogu pregledati sve rezultate,*  
*kako bih vidio najrelevantnije sadržaje prvi, a zatim nastaviti listanje bez čekanja.*

**Kontekst:** Sortiranje je definirano u **Ch.02, sekcija 2.4**. `sortDate` je centralni mehanizam — svaki listing ima ovo polje koje se osvježava pri kreiranju, odobrenju, ručnom refresh-u (jednom u 24h), i AutoRenew promocijama. Promocijski status dodaje drugi sloj: Premium listinzi idu na vrh unutar kategorije, Premium+Homepage na vrh naslovne. Paginacija koristi lazy loading — inicijalni set rezultata se učitava, a dodatni po potrebi.

**Acceptance criteria:**

- [ ] Listinzi su sortirani po `sortDate` descending (najnoviji prvi) kao default sortiranje
- [ ] Na naslovnoj: Grupa 1 (Premium+Homepage) uvijek iznad Grupe 2 (svi ostali)
- [ ] U kategoriji: Premium listinzi uvijek na vrhu, sortirani po sortDate međusobno, pa svi ostali
- [ ] Standard promocije nemaju prioritet u sortiranju — vizualno su istaknute ali redoslijed je po sortDate
- [ ] Inicijalni set rezultata se učitava odmah (konfigurabilan broj, preporučeno 20)
- [ ] Dodatni rezultati se dohvataju automatski kad korisnik skrola blizu kraja (infinite scroll) ili klikom na "Prikaži više"
- [ ] Paginacija koristi cursor-based pristup (ne offset) za konzistentnost kad se dodaju novi listinzi
- [ ] Korisnik vidi indikator da se učitavaju dodatni rezultati (spinner na dnu)
- [ ] Kad nema više rezultata, korisnik vidi poruku "Prikazani su svi rezultati"
- [ ] Ručni refresh sortDate-a je pokrit u [E02](../e02-listing-crud-i-lifecycle.md) — ovdje samo sortiranje po tom polju

**Backend Scope:**

- `GET /events?cursor={cursor}&limit={limit}&sort=sortDate` — cursor-based paginacija
- `GET /places?cursor={cursor}&limit={limit}&sort=sortDate` — isto za mjesta
- Backend vraća: {items: \[...\], nextCursor: string | null, totalCount: number}
- Sortiranje uzima u obzir promocijski status: promotionGroup (1 = Premium+Homepage, 2 = Premium, 3 = ostali) + sortDate desc

**Frontend Scope:**

- UI: Lista/grid kartica sa automatskim dohvatom sljedećeg seta pri scrollu
- UI: Spinner na dnu dok se učitavaju dodatni rezultati
- UI: "Prikazani su svi rezultati" kad nema više
- UX: Infinite scroll sa fallback "Prikaži više" dugmetom
- UX: Scroll pozicija se čuva pri navigaciji nazad sa detail stranice

**Tehničke napomene:**

- Cursor-based paginacija je preferirana jer offset-based ima problem sa konzistentnošću kad se dodaju novi listinzi tokom browsanja.
- Promocijski prioriteti se potpuno aktiviraju kad [E10](../e10-promocije-listinga.md) (Promocije) bude implementiran — do tada, svi listinzi su u istoj grupi.

**Testovi (MVP):**

- [ ] Listinzi su sortirani po sortDate descending — listing sa novijim sortDate je iznad
- [ ] Scroll do kraja — automatski se učitava sljedeći set rezultata
- [ ] Kad nema više — prikazuje se "Prikazani su svi rezultati"
- [ ] Premium+Homepage listing je iznad non-premium na naslovnoj (kad [E10](../e10-promocije-listinga.md) bude aktivan)
- [ ] Premium listing je iznad non-premium unutar kategorije (kad [E10](../e10-promocije-listinga.md) bude aktivan)

**Wireframe referenca:** —