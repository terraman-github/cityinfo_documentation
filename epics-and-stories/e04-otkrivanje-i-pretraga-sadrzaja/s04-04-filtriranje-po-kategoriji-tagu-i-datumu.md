---
id: S04-04
parent_epic: E04
linear_id: "CIT2-30"
phase: MVP
journey_milestones: [J-04]
type: fullstack
---

# S04-04 — Filtriranje po kategoriji, tagu i datumu

**Naslov:** Filtriranje po kategoriji, tagu i datumu

**Excerpt:** Korisnik sužava rezultate kombinacijom filtera — kategorija, tag, i datum (samo za Events). Filteri koriste AND logiku, prikazuju se kao chipovi, i ostaju aktivni dok ih korisnik eksplicitno ne ukloni. Kad kombinacija ne daje rezultate, sistem nudi prijedloge za relaksaciju.

**Phase:** MVP

**Journey milestones:** **J-04**

**User story:**  
Kao posjetilac,  
želim filtrirati sadržaj po kategoriji, tagu i datumu,  
kako bih suzio rezultate na ono što me zaista zanima bez ručnog prolaženja kroz sve listinge.

**Kontekst:** Korisnik je na stranici sa rezultatima (naslovna ili pretraga) i želi suziti prikaz. Filteri se koriste unutar aktivnog režima. Kategorije dolaze iz odgovarajućeg sistema (EventCategory ili PlaceCategory), tagovi iz EventTags ili PlaceTags. Datum filter postoji samo u Events režimu — filtrira po jednom datumu, ne po intervalu. Pravila za filtere u **Ch.02, sekcija 2.2**.

**Acceptance criteria:**

- [ ] Korisnik može filtrirati po kategoriji — klik na kategoriju prikazuje listinge koji imaju tu kategoriju kao primarnu ili bilo koju sekundarnu
- [ ] Kategorije su grupisane po sektorima za lakše snalaženje
- [ ] Korisnik može filtrirati po tagu — prikazuje listinge koji imaju odabrani tag (primaryTagSlug ili secondaryTagSlug)
- [ ] Korisnik može filtrirati po datumu (samo Events režim) — prikazuje evente koji se dešavaju tog datuma (startDateTime <= datum <= endDateTime)
- [ ] Filteri koriste AND logiku — rezultati su presjek svih aktivnih filtera
- [ ] Aktivni filteri se prikazuju kao chipovi sa opcijom uklanjanja (✕)
- [ ] Filteri su sticky — ostaju aktivni dok ih korisnik eksplicitno ne ukloni
- [ ] "Očisti sve" dugme resetuje sve filtere (ali ne lokaciju)
- [ ] Promjena režima (Events ↔ Places) resetuje sve filtere
- [ ] Kad kombinacija filtera ne daje rezultate, prikazuje se poruka sa prijedlogom za relaksaciju (npr. "Ukloni filter 'Koncerti' za Y rezultata")
- [ ] Datum filter koristi date picker sa kalendarom

**Backend Scope:**

- `GET /events?category={slug}&tag={slug}&date={YYYY-MM-DD}` — filtriranje evenata
- `GET /places?category={slug}&tag={slug}` — filtriranje mjesta (bez datuma)
- Datum filter: event se prikazuje ako `startDateTime <= date <= endDateTime`
- Kategorija filter: listing se prikazuje ako ima tu kategoriju kao primarnu ILI sekundarnu
- Backend treba podržati vraćanje ukupnog broja rezultata za prazne rezultate suggestije

**Frontend Scope:**

- UI: Filter panel (sidebar na desktopu, drawer/modal na mobilnom)
- UI: Kategorije grupisane po sektorima sa brojem listinga
- UI: Tagovi kao chipovi za odabir
- UI: Date picker za datum filter (samo Events režim)
- UI: Chip bar za aktivne filtere sa ✕ za uklanjanje i "Očisti sve"
- Klijentska validacija: datum ne može biti u prošlosti (za Events)
- UX: Filter promjena odmah osvježava rezultate bez potrebe za "Primijeni" dugmetom
- UX: Na mobilnom, filteri se otvaraju u drawer-u/modalu sa "Primijeni" dugmetom

**Testovi (MVP):**

- [ ] Filter po kategoriji "Restorani" — prikazuju se samo mjesta sa tom kategorijom (primarnom ili sekundarnom)
- [ ] Filter po tagu "parking" — prikazuju se samo mjesta sa tim tagom
- [ ] Filter po datumu "15.06." — prikazuju se samo eventi koji se dešavaju tog datuma
- [ ] Kombinacija kategorija + tag — rezultati su presjek
- [ ] Uklanjanje jednog filtera — ostali ostaju aktivni
- [ ] "Očisti sve" — svi filteri su uklonjeni, prikazuju se svi rezultati
- [ ] Prazni rezultati — prikazuje se poruka sa prijedlogom

**Wireframe referenca:** —