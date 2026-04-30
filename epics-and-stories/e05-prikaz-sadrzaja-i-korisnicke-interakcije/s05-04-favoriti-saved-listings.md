---
id: S05-04
confluence_page_id: "252215297"
title: "S05-04 — Favoriti (Saved listings)"
parent_epic: E05
linear_id: "CIT2-37"
phase: MVP
journey_milestones: [J-05]
type: fullstack
---

**Naslov:** Favoriti (Saved listings)

**Excerpt:** Registrovani korisnici mogu spremiti listinge u listu favorita za kasniji pristup — korisno za planiranje vikenda ili praćenje omiljenih mjesta. Lista favorita je privatna, dostupna u profilu, i graceful degradira kad se listing zatvori.

**Phase:** MVP

**Journey milestones:** J-05

**User story:**  
Kao registrovan korisnik,

želim spremiti zanimljive listinge u favorite,

kako bih im se mogao brzo vratiti kad budem spreman za posjetu.

**Kontekst:** Favoriti su dostupni samo registrovanim korisnicima — visitors ne mogu koristiti ovu funkcionalnost. Favorite entitet je definisan u **Ch.04, sekcija 4.9**. Lista favorita je privatna — samo korisnik vidi svoju listu. Ako se listing zatvori ili obriše, zapis ostaje u favoritima ali se prikazuje kao "Više nije dostupan".

**Acceptance criteria:**

- [ ] Registrovan korisnik može dodati listing u favorite klikom na bookmark ikonu
- [ ] Registrovan korisnik može ukloniti listing iz favorita klikom na istu ikonu
- [ ] Bookmark ikona vizuelno pokazuje stanje (u favoritima / nije u favoritima)
- [ ] Kombinacija userId + listingId je jedinstvena — duplikat se ne kreira
- [ ] Lista favorita je dostupna na `/users/me/favorites` u korisničkom profilu
- [ ] Lista favorita prikazuje listinge kao kartice (reuse `<ListingCard>` komponente)
- [ ] Ako je listing zatvoren ili obrisan (`isPublic = false`), kartica u favoritima prikazuje "Više nije dostupan" sa smanjenom opasnošću (grayed out)
- [ ] Korisnik može ukloniti nedostupan listing iz favorita
- [ ] Favoriti su privatni — ne postoji javni prikaz nečijih favorita
- [ ] Visitor koji klikne bookmark ikonu dobija prompt za registraciju/login

**Backend Scope:**

- `POST /listings/{id}/favorite` — kreira Favorite zapis
- `DELETE /listings/{id}/favorite` — briše Favorite zapis
- `GET /users/me/favorites` — lista favorita sa listing podacima (uključujući zatvorene/obrisane)

**Frontend Scope:**

- UI: Bookmark ikona na kartici i detail stranici
- UI: "Moji favoriti" stranica u korisničkom profilu sa karticama
- UI: Grayed out kartica za nedostupne listinge sa porukom
- UX: Optimistic UI — ikona se odmah mijenja
- UX: Prompt za registraciju kad visitor pokuša dodati u favorite

**Testovi (MVP):**

- [ ] Dodavanje u favorite — listing se pojavljuje u listi favorita
- [ ] Uklanjanje iz favorita — listing nestaje iz liste
- [ ] Listing koji je zatvoren — prikazuje se kao "Više nije dostupan" u favoritima
- [ ] Visitor klikne bookmark — prikazuje se prompt za login/registraciju
- [ ] Duplikat dodavanja — ne kreira novi zapis

**Wireframe referenca:** —