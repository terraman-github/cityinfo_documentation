---
id: S02-03
confluence_page_id: "251330600"
title: "S02-03 — Lokacija Event-a — povezivanje sa Place-om ili ručna adresa"
parent_epic: E02
linear_id: "CIT2-11"
phase: MVP
journey_milestones: [J-02]
type: fullstack
---

<a id="s02-03-lokacija-event-a-povezivanje-sa-place-om-ili-ručna-adresa"></a>

# S02-03 — Lokacija Event-a — povezivanje sa Place-om ili ručna adresa

**Naslov:** Lokacija Event-a — povezivanje sa Place-om ili ručna adresa

**Excerpt:** Event mora imati definisanu lokaciju. Korisnik može povezati event sa vlastitim Place-om (cross-promotion) ili unijeti ručnu adresu sa koordinatama za lokacije koje ne posjeduje u sistemu.

**Phase:** MVP

**Journey milestones:** J-02

**User story:**

*Kao organizator događaja,*  
*želim definisati gdje se moj event održava — bilo povezivanjem sa mojim mjestom ili unosom adrese,*  
*kako bi posjetioci znali gdje doći.*

**Kontekst:** Korisnik je kreirao Event draft ([S02-01](s02-01-kreiranje-event-listinga-sa-osnovnim-podacima.md)) i sada dodaje lokaciju. Postoje dvije opcije: povezivanje sa vlastitim Place-om (samo ako je isti korisnik vlasnik oba listinga) ili ručna adresa sa koordinatama. Jedna od opcija je obavezna za objavu, ali ne za draft. Detalji → **Ch.04, sekcija 4.2** (Lokacija listinga događaja).

**Acceptance criteria:**

- [ ] Na Event formi/stranici postoji sekcija za definisanje lokacije sa dvije opcije
- [ ] **Opcija 1 — Moj Place:** korisnik vidi listu vlastitih objavljenih Place-ova i može odabrati jedan
- [ ] Lista Places-ova prikazuje samo Place-ove čiji je `ownerId` isti kao korisnikov ID i čiji je `listingStatus` u nekom od javno vidljivih statusa (`published`, `published_under_review`, `published_needs_changes`)
- [ ] Pri odabiru Place-a, `placeId` se sprema na Event
- [ ] **Opcija 2 — Ručna adresa:** korisnik unosi adresu, sa koordinatama putem mape ili autocomplete-a
- [ ] Pri ručnom unosu, spremaju se `manualAddress`, `latitude`, `longitude`
- [ ] `placeId` i ručna adresa su međusobno isključivi — odabir jednog briše drugo
- [ ] Lokacija nije obavezna za `draft` status, ali jeste za submit/objavu
- [ ] Ako se povezani Place ukloni nakon kreiranja eventa, sistem automatski kreira `placeSnapshot` sa svim potrebnim podacima za prikaz

**Backend Scope:**

- `PUT /events/{id}` — prima lokacijske podatke (placeId ILI manualAddress + latitude + longitude)
- Validacija: `placeId` mora postojati, biti u javno vidljivom statusu, i pripadati istom korisniku; ako je ručna adresa — `latitude`/`longitude` obavezni
- Side effects: pri uklanjanju povezanog Place-a, automatski se popunjava `placeSnapshot` na Event-u (ovo može biti background job ili trigger)

**Frontend Scope:**

- UI: toggle/tab za odabir opcije (Moj Place / Ručna adresa); dropdown ili lista sa vlastitim Place-ovima; mapa + adresna polja za ručni unos
- Klijentska validacija: jedno od dvoje mora biti popunjeno za submit
- UX: pri odabiru Place-a prikazati preview (naziv, adresa) na mapi; pri ručnom unosu Google Places autocomplete + draggable pin

**Tehničke napomene:**

- Snapshot mehanizam za Place je bitan za integritet historijskih podataka — osigurava da prošli eventi i dalje prikazuju lokaciju čak i kad Place više ne postoji
- Snapshot treba sadržavati: naziv, adresu, koordinate — sve što je potrebno za prikaz

**Testovi (MVP):**

- [ ] Happy path: povezivanje Event-a sa vlastitim Place-om → `placeId` sačuvan
- [ ] Happy path: unos ručne adrese sa koordinatama → `manualAddress`, `latitude`, `longitude` sačuvani
- [ ] Pokušaj povezivanja sa tuđim Place-om → greška
- [ ] Promjena sa Place-a na ručnu adresu → `placeId` se briše, ručni podaci se spremaju
- [ ] Event bez lokacije — može se sačuvati kao draft, ali ne može se submitovati
- [ ] Uklanjanje povezanog Place-a → `placeSnapshot` se automatski kreira na Event-u

**Wireframe referenca:** —

**Implementacijske napomene:**

- Lista vlastitih Place-ova može se dohvatiti putem `GET /places?ownerId=me&isPublic=true`
- Snapshot se može kreirati sinhrono pri uklanjanju Place-a ili asinhrono kroz event-driven mehanizam