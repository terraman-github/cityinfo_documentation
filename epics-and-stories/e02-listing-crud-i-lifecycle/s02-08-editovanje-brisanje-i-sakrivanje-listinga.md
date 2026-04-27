---
id: S02-08
parent_epic: E02
linear_id: ""
phase: MVP
journey_milestones: [J-02]
type: fullstack
---

# S02-08 — Editovanje, brisanje i sakrivanje listinga

<a id="s02-08-editovanje-brisanje-i-sakrivanje-listinga"></a>

# S02-08 — Editovanje, brisanje i sakrivanje listinga

**Naslov:** Editovanje, brisanje i sakrivanje listinga

**Excerpt:** Pokriva tri ključne operacije nad postojećim listingom: editovanje (sa različitim ponašanjem za pre/post-mod korisnike), brisanje (`removed` sa `removedReason`), i privremeno sakrivanje/prikazivanje od strane vlasnika (`hidden_by_owner`). Uključuje i otkazivanje Event-a (`canceled`) sa mogućnošću reaktivacije.

**Phase:** MVP

**Journey milestones:** J-02

**User story:**  
Kao vlasnik listinga,  
želim moći izmijeniti podatke, privremeno sakriti, otkazati event ili trajno obrisati svoj listing,  
kako bih imao punu kontrolu nad sadržajem koji sam objavio.

**Kontekst:** Korisnik ima listing u nekom od aktivnih statusa (`draft`, `in_review`, `changes_requested`, `published`, `published_under_review`, `published_needs_changes`). Ponašanje pri editu objavljenog listinga zavisi od Trust Tier-a korisnika (Ch.04, 4.8 — Ažuriranje objavljenog listinga). Brisanje ima različitu logiku zavisno o `wasEverActive` flagu i tipu listinga (Ch.04, 4.2 za Event, 4.3 za Place). Sakrivanje (`hidden_by_owner`) je reverzibilno, za razliku od brisanja (`removed`).

**Acceptance criteria:**

**Editovanje:**

- [ ] Korisnik može editovati listing u statusu `draft`, `in_review`, `changes_requested`, `published`, `published_under_review`, ili `published_needs_changes`
- [ ] **Tier 0–1 (pre-mod):** edit objavljenog listinga ga skriva i šalje nazad na moderaciju — `listingStatus` prelazi u `in_review`
- [ ] Korisnik Tier 0–1 dobija poruku: "Listing će ponovo postati vidljiv nakon odobrenja izmjena."
- [ ] **Tier 2+ (post-mod):** edit objavljenog listinga — listing ostaje vidljiv, prelazi u `published_under_review`, izmjene odmah primijenjene, kreira se stavka za naknadni pregled
- [ ] Sva polja koja se mogu postaviti pri kreiranju mogu se i editovati (osim `ownerId`)
- [ ] `updatedAt` se ažurira pri svakom editu

**Brisanje (korisničko):**

- [ ] `wasEverActive = false` (listing nikad nije bio javno vidljiv) → korisnik može trajno obrisati listing: `listingStatus = removed`, `removedReason = user_delete`
- [ ] `wasEverActive = true` → opcija brisanja nije dostupna; korisnik može samo sakriti listing (`hidden_by_owner`) ili otkazati event (`canceled`)
- [ ] Brisanje je instant — ne zahtijeva moderatorsko odobrenje

**Brisanje Place-a (dodatna pravila):**

- [ ] Ako Place ima evente u javno vidljivom statusu (`isPublic = true`) → brisanje blokirano sa porukom "Prvo otkažite ili sakrijte aktivne događaje"
- [ ] Ako nema javno vidljivih evenata i `wasEverActive = false` → `removed` sa `user_delete`
- [ ] Ako nema javno vidljivih evenata ali `wasEverActive = true` → brisanje nije dostupno (sakrivanje ili moderatorska akcija)
- [ ] Prošli eventi povezani sa obrisanim Place-om dobijaju `placeSnapshot`

**Sakrivanje (hide/unhide):**

- [ ] Korisnik može sakriti objavljeni listing → `listingStatus = hidden_by_owner`
- [ ] Korisnik može ponovo prikazati sakriveni listing → `listingStatus = published`
- [ ] Sakriveni listing nije vidljiv javnosti ali ostaje vidljiv vlasniku na profilu

**Otkazivanje Event-a:**

- [ ] Korisnik može otkazati objavljeni Event → `listingStatus = canceled`
- [ ] Otkazani event ostaje vidljiv sa badge-om "Otkazano" ali je isključen iz naslovne, feed-ova i promoted listi
- [ ] Ako `endDateTime > NOW()` → korisnik može reaktivirati event → `listingStatus = published`
- [ ] Ako `endDateTime` prođe dok je event u `canceled` → automatski prelazi u `expired`
- [ ] Aktivne promocije se pauziraju pri prelasku u `canceled`; nastavljaju se pri reaktivaciji ako period nije istekao
- [ ] `canceled` važi samo za Event — Place ne može biti otkazan

**Backend Scope:**

- `PUT /events/{id}` — ažurira Event, ponašanje ovisno o Trust Tier-u (Tier 0–1: `published` → `in_review`; Tier 2+: `published` → `published_under_review`)
- `PUT /places/{id}` — ažurira Place, ista Tier logika
- `DELETE /events/{id}` — brisanje prema `wasEverActive` logici
- `DELETE /places/{id}` — brisanje sa provjerom javno vidljivih evenata i `wasEverActive`
- `POST /events/{id}/hide` — `published` → `hidden_by_owner`
- `POST /events/{id}/unhide` — `hidden_by_owner` → `published`
- `POST /places/{id}/hide` / `POST /places/{id}/unhide` — isto za Place
- `POST /events/{id}/cancel` — `published` → `canceled`
- `POST /events/{id}/reactivate` — `canceled` → `published` (samo ako `endDateTime > NOW()`)
- Validacija: vlasništvo, dozvoljenost operacije po statusu, za Place brisanje — provjera `isPublic` evenata i `wasEverActive`
- Side effects: pri editu Tier 0–1 → kreira stavku u mod redu; pri brisanju Place-a → snapshot za prošle evente; pri brisanju parent Event-a → kaskadno procesiranje child-ova; pri cancel-u → pauziranje promocija

**Frontend Scope:**

- UI: "Uredi", "Obriši" (samo ako `wasEverActive = false`), "Sakrij/Prikaži", "Otkaži event" dugmad na listing stranici (vidljiva samo vlasniku); potvrda za brisanje i otkazivanje (modal); lista listinga na profilu sa statusima
- Klijentska validacija: nema dodatne — odluke su server-side
- UX: potvrda pred brisanje ("Jeste li sigurni?"); za Place sa javnim eventima — poruka o blokiranom brisanju; za Tier 0–1 edit — upozorenje da će listing biti sakriven do odobrenja; hide/unhide toggle; za cancel — potvrda sa objašnjenjem posljedica; za reaktivaciju — dostupna samo ako event još nije prošao

**Tehničke napomene:**

- Brisanje je uvijek soft delete za listinge koji su ikad bili javno vidljivi — `wasEverActive` flag kontroliše ovo
- `hidden_by_moderator` akcija dolazi iz moderatorskog panela (E07/E13) — ova storija pokriva samo `hidden_by_owner`
- `hidden_by_system` je automatska akcija pri blokiranju korisnika ili AI detekciji (E06/E07)
- `removed` je terminalni status — nema reaktivacije

**Testovi (MVP):**

- [ ] Edit draft-a → podaci ažurirani, status nepromijenjen
- [ ] Edit objavljenog listinga (Tier 1) → `listingStatus = in_review`, listing skriven
- [ ] Edit objavljenog listinga (Tier 2+) → `listingStatus = published_under_review`, listing ostaje vidljiv
- [ ] Brisanje listinga sa `wasEverActive = false` → `removed` + `user_delete`
- [ ] Pokušaj brisanja listinga sa `wasEverActive = true` → akcija nedostupna
- [ ] Brisanje Place-a sa javno vidljivim eventima → greška
- [ ] Brisanje Place-a bez javnih evenata (`wasEverActive = false`) → `removed` + `user_delete`, prošli eventi dobijaju snapshot
- [ ] Sakrivanje objavljenog listinga → `hidden_by_owner`
- [ ] Unhide sakrivenog listinga → `published`
- [ ] Otkazivanje Event-a → `canceled`, badge "Otkazano" vidljiv
- [ ] Reaktivacija `canceled` eventa (koji još nije prošao) → `published`
- [ ] Reaktivacija `canceled` eventa koji je prošao → greška
- [ ] Pokušaj otkazivanja Place-a → akcija nedostupna

**Wireframe referenca:** —

**Implementacijske napomene:**

- Razmotriti optimistic UI za hide/unhide (instant vizualni feedback, server poziv u pozadini)
- Brisanje Place-a je najkompleksnija operacija — snapshot kreiranje za svaki prošli event treba biti transakciono