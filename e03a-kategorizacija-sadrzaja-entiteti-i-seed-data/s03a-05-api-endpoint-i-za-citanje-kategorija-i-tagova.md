# S03a-05 — API endpoint-i za čitanje kategorija i tagova

**Naslov:** API endpoint-i za čitanje kategorija i tagova

**Excerpt:** Javni GET endpoint-i koji vraćaju liste kategorija i tagova. Ove podatke koristi frontend za prikaz u formama i filterima.

**Phase:** MVP

**Journey milestones:** J-02, J-04

**User story:**  
Kao frontend developer,  
želim imati API endpoint-e za dohvat kategorija i tagova,  
kako bih mogao prikazati odabir kategorije i tagova u listing formi i filterima.

**Kontekst:** Ovo su javni endpoint-i (ne zahtijevaju autentifikaciju) jer ih koriste i visitors za pretragu. Endpoint-i su definirani u Ch.04, sekcija 4.10. Kategorije se vraćaju grupirane po sektoru. Tagovi se vraćaju sortirani po orderIndex.

**Acceptance criteria:**

- [ ] `GET /event-categories` vraća listu EventCategory zapisa, grupisanih po sektoru
- [ ] `GET /place-categories` vraća listu PlaceCategory zapisa, grupisanih po sektoru
- [ ] Odgovor uključuje sve atribute: slug, name, nameAlt, sectorSlug, sectorName, sectorNameAlt, icon, color, sortOrder
- [ ] Samo aktivne kategorije se vraćaju (`isActive = true`)
- [ ] `GET /event-tags` vraća listu EventTags zapisa (samo aktivni)
- [ ] `GET /event-tags/active` vraća isto kao `/event-tags` (eksplicitni filter)
- [ ] `GET /place-tags` i `GET /place-tags/active` vraćaju PlaceTags (samo aktivni)
- [ ] Tagovi su sortirani po `orderIndex`
- [ ] Endpoint-i ne zahtijevaju autentifikaciju (javni)
- [ ] Odgovor uključuje `nameAlt` i `tagNameAlt` polja za dvojezični prikaz

**Backend Scope:**

- `GET /event-categories` — vraća listu EventCategory grupisanih po sektoru, filtriranih na `isActive = true`
- `GET /place-categories` — vraća listu PlaceCategory grupisanih po sektoru, filtriranih na `isActive = true`
- `GET /event-tags` — vraća listu aktivnih EventTags, sortiranih po `orderIndex`
- `GET /place-tags` — vraća listu aktivnih PlaceTags, sortiranih po `orderIndex`
- Odgovor uključuje sva polja uključujući `nameAlt` / `tagNameAlt` za dvojezičnost
- Razmotriti response caching — kategorije se mijenjaju rijetko, a pozivaju često

**Tehničke napomene:**

- Admin CRUD endpoint-i (POST/PUT/DELETE za kategorije i tagove) dolaze u E03b — ova storija pokriva samo čitanje.

**Testovi (MVP):**

- [ ] `GET /event-categories` vraća neprazan odgovor sa ispravnom strukturom
- [ ] `GET /place-categories` vraća sve 16 sektora sa svim kategorijama
- [ ] Deaktivirana kategorija (ako se ručno deaktivira u bazi) ne pojavljuje se u odgovoru
- [ ] `GET /place-tags` vraća tagove sortirane po orderIndex
- [ ] Endpoint-i rade bez auth tokena

**Wireframe referenca:** —