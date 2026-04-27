---
id: S03b-04
parent_epic: E03b
linear_id: ""
phase: MVP
journey_milestones: [J-08]
type: fullstack
---

# S03b-04 — CRUD aliasa kategorija kroz Staff panel

**Naslov:** CRUD aliasa kategorija kroz Staff panel

**Excerpt:** Korisnici pretražuju koristeći različite termine za isti koncept — "gym" umjesto "teretana", "picerija" umjesto "restorani". Ovaj story omogućava local\_admin-u da kreira i briše alias mapiranja koja nevidljivo preusmjeravaju pretrage na odgovarajuću kategoriju.

**Phase:** MVP

**Journey milestones:** J-08

**User story:**  
Kao local\_admin,  
želim upravljati aliasima kategorija kroz Staff panel,  
kako bih mogao dodati lokalne sinonime i poboljšati uspješnost pretrage bez promjene strukture kategorija.

**Kontekst:** Admin pristupa sekciji za upravljanje aliasima u Staff panelu. Inicijalni aliasi za Sarajevo su postavljeni u E03a. Aliasi su nevidljivi korisnicima — koriste se interno za mapiranje pretrage. Tabela aliasa je konfigurabilan parametar po tenantu — svaki grad može imati lokalne sinonime. Više o aliasima u Ch.04, sekcija 4.4.

**Acceptance criteria:**

- [ ] Admin može kreirati novi alias sa: aliasni termin (tekst), ciljna kategorija (odabir iz liste aktivnih kategorija)
- [ ] Alias termin mora biti jedinstven — ne može postojati dva aliasa sa istim terminom
- [ ] Admin može obrisati postojeći alias
- [ ] Lista aliasa prikazuje: termin, ciljnu kategoriju (naziv + sektor), i akciju za brisanje
- [ ] Aliasi nisu vezani za tip (Event/Place) — jedan alias može mapirati na EventCategory ili PlaceCategory, ali ne na oboje istovremeno
- [ ] Admin može filtrirati listu aliasa po kategoriji ili pretragom po terminu
- [ ] Nema editovanja aliasa — ako treba promijeniti mapiranje, admin briše stari i kreira novi

**Backend Scope:**

- `GET /category-aliases` — vraća listu svih aliasa sa informacijom o ciljnoj kategoriji
- `POST /category-aliases` — prima {alias, categoryId}, vraća kreiran alias
- `DELETE /category-aliases/{id}` — briše alias
- Validacija: alias termin unikatnost, categoryId mora postojati

**Frontend Scope:**

- UI: Lista aliasa sa kolonama: termin, ciljna kategorija (naziv + sektor), akcija (Delete)
- UI: Forma za kreiranje: text input za termin, dropdown za odabir kategorije (grupisane po sektoru i tipu Event/Place)
- Klijentska validacija: termin obavezan, kategorija obavezna
- UX: Confirmation dialog pri brisanju
- UX: Search/filter za brzo pronalaženje aliasa u listi

**Tehničke napomene:**

- Aliasi se koriste pri pretrazi (E04) — ovdje se samo upravlja tabelom mapiranja.
- Termin treba biti case-insensitive pri provjeri unikatnosti i pri pretrazi.

**Testovi (MVP):**

- [ ] Kreiranje aliasa "gym" → "Teretane i fitness" — alias se pojavljuje u listi
- [ ] Pokušaj kreiranja aliasa sa terminom koji već postoji — prikazuje grešku
- [ ] Brisanje aliasa — nestaje iz liste
- [ ] Lista prikazuje čitljiv prikaz ciljne kategorije (ne samo ID)

**Wireframe referenca:** —