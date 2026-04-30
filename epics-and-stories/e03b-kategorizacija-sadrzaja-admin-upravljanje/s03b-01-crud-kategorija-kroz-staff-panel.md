---
id: S03b-01
parent_epic: E03b
linear_id: "CIT2-23"
phase: MVP
journey_milestones: [J-08]
type: fullstack
---
<!-- confluence-page-id: 251723777 -->
<!-- confluence-space-key: GI -->


# S03b-01 — CRUD kategorija kroz Staff panel

**Naslov:** CRUD kategorija kroz Staff panel

**Excerpt:** Omogućava local\_admin-u da kreira nove kategorije, uređuje postojeće (naziv, ikona, boja, sortOrder), deaktivira kategorije koje više nisu relevantne, i briše one koje nijedan listing ne koristi — sve kroz Staff UI bez pristupa bazi.

**Phase:** MVP

**Journey milestones:** J-08

**User story:**  
Kao local\_admin,

želim upravljati kategorijama (EventCategory i PlaceCategory) kroz Staff panel,

kako bih mogao prilagoditi ponudu kategorija potrebama grada bez developer intervencije.

**Kontekst:** Admin pristupa Staff panelu ([admin.cityinfo.ba](http://admin.cityinfo.ba)) gdje postoji sekcija za upravljanje kategorizacijom. Kategorije su grupisane po sektorima. Entiteti i seed data su već postavljeni kroz [E03a](../e03a-kategorizacija-sadrzaja-entiteti-i-seed-data.md). Pravila za kategorije definisana u **Ch.04, sekcija 4.4** — slug je immutable, brisanje moguće samo ako nema povezanih listinga, deaktivacija je preferirana opcija.

**Acceptance criteria:**

- [ ] Admin može kreirati novu kategoriju sa svim atributima: naziv, nameAlt, slug (auto-generisan, ali prilagodljiv prije snimanja), sectorSlug (odabir iz postojećih sektora), ikona, boja, defaultImageUrl, sortOrder
- [ ] Slug se automatski generiše iz naziva, ali admin ga može prilagoditi prije prvog snimanja
- [ ] Jednom snimljen slug se ne može mijenjati — polje je disabled pri editovanju
- [ ] Admin može editovati sve atribute osim slug-a na postojećoj kategoriji
- [ ] Admin može deaktivirati kategoriju (`isActive = false`) — kategorija ostaje u sistemu, ali se ne prikazuje pri kreiranju novih listinga
- [ ] Admin može reaktivirati deaktiviranu kategoriju (`isActive = true`)
- [ ] Admin može obrisati kategoriju samo ako nijedan listing ne koristi tu kategoriju — u suprotnom, prikazuje se poruka sa brojem povezanih listinga
- [ ] Lista kategorija prikazuje ukupan broj listinga po kategoriji za brzu referensu
- [ ] Validacija: naziv i slug su obavezni, slug mora biti jedinstven unutar tabele (EventCategory ili PlaceCategory)
- [ ] Promjene su odvojene za EventCategory i PlaceCategory — admin jasno vidi sa kojim tipom radi

**Backend Scope:**

- `POST /event-categories` — prima {name, nameAlt, slug, sectorSlug, sectorName, sectorNameAlt, icon, color, defaultImageUrl, sortOrder}, vraća kreiranu kategoriju
- `PUT /event-categories/{id}` — prima izmjene (bez slug-a), vraća ažuriranu kategoriju
- `DELETE /event-categories/{id}` — briše ako nema povezanih listinga, vraća 409 Conflict sa brojem listinga ako ih ima
- Isti endpoint-i za `/place-categories`
- Validacija: slug unikatnost, obavezna polja, slug immutability pri update-u
- Side effects: deaktivacija ne utiče na postojeće listinge (zadržavaju vezu)

**Frontend Scope:**

- UI: Lista kategorija grupisana po sektorima, sa brojem listinga, statusom (active/inactive), i akcijama (Edit, Deactivate/Activate, Delete)
- UI: Forma za kreiranje/editovanje sa svim atributima, color picker za boju, emoji picker za ikonu
- Klijentska validacija: obavezna polja (naziv, slug, sectorSlug), slug format (URL-friendly karakteri)
- UX: Slug polje je editable samo pri kreiranju, disabled pri editovanju sa tooltipom koji objašnjava zašto
- UX: Delete dugme prikazuje confirmation dialog sa upozorenjem; ako ima povezanih listinga, prikazuje broj i blokira brisanje
- UX: Tab ili toggle za prebacivanje između EventCategory i PlaceCategory

**Tehničke napomene:**

- Slug auto-generisanje iz naziva treba ukloniti dijakritike i specijalne karaktere (npr. "Hrana i piće" → "hrana-i-pice").
- Lista kategorija sa brojem listinga treba koristiti denormalizovani count ili efikasan upit — ne dohvatati sve listinge da bi se prebrojale kategorije.

**Testovi (MVP):**

- [ ] Kreiranje kategorije sa svim obaveznim poljima — kategorija se pojavljuje u listi i dostupna je u API-ju
- [ ] Pokušaj kreiranja kategorije sa duplikatnim slug-om — prikazuje grešku
- [ ] Editovanje naziva i boje kategorije — promjene vidljive odmah
- [ ] Pokušaj editovanja slug-a na postojećoj kategoriji — polje je disabled
- [ ] Deaktivacija kategorije — kategorija se ne pojavljuje pri kreiranju novih listinga, ali postojeći listinzi zadržavaju vezu
- [ ] Brisanje kategorije bez listinga — uspješno
- [ ] Pokušaj brisanja kategorije sa listinzima — prikazuje poruku sa brojem i blokira

**Wireframe referenca:** —

**Implementacijske napomene:** Za color picker i emoji picker mogu se koristiti postojeće Flowbite/Tailwind komponente ili lightweight biblioteke. Sortiranje po `sortOrder` unutar sektora određuje redoslijed prikaza u formi za kreiranje listinga.