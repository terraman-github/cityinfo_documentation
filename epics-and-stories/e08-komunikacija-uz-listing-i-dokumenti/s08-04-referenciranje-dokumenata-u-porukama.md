---
id: S08-04
confluence_page_id: "251822101"
title: "S08-04 — Referenciranje dokumenata u porukama"
parent_epic: E08
linear_id: "CIT2-54"
phase: MVP
journey_milestones: [J-07]
type: fullstack
---

**Naslov:** Referenciranje dokumenata u porukama

**Excerpt:** Poruke u thread-u mogu referencirati dokumente vezane za listing (ListingDocument). Moderator može zatražiti dokument, a vlasnik ga uploadati i priložiti uz odgovor. Dokumenti se ne čuvaju u poruci — poruka samo sadrži reference na postojeće dokumente.

**Phase:** MVP

**Journey milestones:** J-07

**User story:**

*Kao vlasnik listinga,*  
*želim priložiti dokument (dokaz vlasništva, dozvolu, certifikat) uz poruku moderatoru,*  
*kako bih mogao dostaviti traženu dokumentaciju bez eksternih kanala.*

**Kontekst:** Moderator je kroz poruku zatražio od vlasnika da dostavi dokument — npr. dokaz vlasništva nad mjestom, dozvolu za organizaciju događaja, ili certifikat. Vlasnik uploaduje dokument kroz listing (ListingDocument entitet — SSoT u **Ch.04, sekcija 4.7**), a zatim ga referencira u poruci koristeći `documentIds` polje. Poruka ne sadrži sam dokument, samo ID reference. Upload i virus scanning dokumenata su pokriveni u [E02](../e02-listing-crud-i-lifecycle.md) (Listing CRUD). Ova storija pokriva samo referenciranje postojećih dokumenata u porukama.

**Acceptance criteria:**

- [ ] Pri slanju poruke, korisnik može priložiti jedan ili više `documentIds` koji referenciraju postojeće ListingDocument zapise
- [ ] Referencirani dokumenti moraju pripadati istom listingu kao i thread
- [ ] Referencirani dokumenti moraju imati `scanStatus: clean` — dokumenti koji čekaju ili nisu prošli virus scan ne mogu se referencirati
- [ ] Poruka sa `documentIds` se ispravno prikazuje u thread-u sa linkovima na priložene dokumente
- [ ] Moderator može pregledati priložene dokumente direktno iz thread prikaza
- [ ] Poruka može sadržavati samo tekst (bez dokumenata), samo dokumente (bez teksta), ili oboje
- [ ] Nepostojeći `documentId` ili document koji ne pripada tom listingu vraća validacijsku grešku

**Backend Scope:**

- `POST /threads/{threadId}/messages` — proširenje postojećeg endpointa: `{ messageText?, documentIds? }` (barem jedno od dva mora biti prisutno)
- Validacija: svi `documentIds` postoje, pripadaju istom listingu, imaju `scanStatus: clean`
- Response uključuje resolved document metadata (ime fajla, tip, status) za priložene dokumente

**Frontend Scope:**

- UI: Dugme "Priloži dokument" pored textarea u thread prikazu — otvara picker sa listom dostupnih dokumenata za taj listing
- UI: Priloženi dokumenti se prikazuju kao klikabilni linkovi/kartice ispod teksta poruke
- Klijentska validacija: barem `messageText` ili `documentIds` mora biti prisutno
- UX: Ako listing nema uploadovanih dokumenata, picker je prazan sa porukom "Nema dostupnih dokumenata — uploadajte dokument na listing stranicu"

**Tehničke napomene:**

- Dokumenti žive u ListingDocument entitetu (**Ch.04, sekcija 4.7**) — poruke ih samo referenciraju, ne dupliciraju
- API endpointi za upload i upravljanje dokumentima su definirani u **Ch.04, sekcija 4.10**
- Virus scan status (`scanStatus`) je kritičan — nikad ne prikazuj dokument koji nije prošao scan

**Testovi (MVP):**

- [ ] Poruka sa validnim `documentIds` se uspješno kreira i prikazuje linkove na dokumente
- [ ] Pokušaj referenciranja dokumenta koji ne pripada tom listingu vraća grešku
- [ ] Pokušaj referenciranja dokumenta sa `scanStatus` koji nije `clean` vraća grešku
- [ ] Poruka bez teksta ali sa `documentIds` se uspješno kreira
- [ ] Poruka bez teksta i bez `documentIds` vraća validacijsku grešku

**Wireframe referenca:** —

**Implementacijske napomene:** Document picker može biti jednostavan dropdown/lista sa imenom fajla i statusom — ne treba preview dokumenata u pickeru. Preview je dostupan tek kad se klikne na link u poruci.