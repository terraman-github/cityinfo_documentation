---
id: S03a-03
parent_epic: E03a
linear_id: ""
phase: MVP
journey_milestones: [J-02, J-04]
type: infra
---

# S03a-03 — Seed data — kategorije za Sarajevo

**Naslov:** Seed data — kategorije za Sarajevo

**Excerpt:** Popunjavanje baze kompletnim listama kategorija za mjesta (16 sektora) i događaje (11 sektora). Ovo je sadržaj koji korisnik vidi u dropdown-u pri kreiranju listinga.

**Phase:** MVP

**Journey milestones:** J-02, J-04

**User story:**  
Kao developer,  
želim imati bazu popunjenu inicijalnim kategorijama za Sarajevo,  
kako bi listing forma imala šta ponuditi korisniku pri odabiru kategorije.

**Kontekst:** Kompletne liste kategorija su definirane u Ch.04, sekcija 4.4 — 16 sektora za mjesta i 11 za događaje. Seed skripta treba biti idempotentna (može se pokrenuti više puta bez duplikata) i odvojena od schema migracija.

**Acceptance criteria:**

- [ ] Seed skripta popunjava sve PlaceCategory zapise — 16 sektora sa svim kategorijama iz Ch.04, sekcija 4.4
- [ ] Seed skripta popunjava sve EventCategory zapise — 11 sektora sa svim kategorijama iz Ch.04, sekcija 4.4
- [ ] Svaka kategorija ima: slug (auto-generisan iz naziva), name (bosanski), sectorSlug, sectorName, sortOrder, isActive=true
- [ ] `nameAlt`, `sectorNameAlt` su popunjeni engleskim prevodima gdje je očigledno (npr. "Restaurants" za "Restorani")
- [ ] Ikona (emoji) je dodijeljena svakom sektoru
- [ ] Seed skripta je idempotentna — pokretanje na već popunjenoj bazi ne kreira duplikate
- [ ] Seed skripta je odvojena od migracija (zasebna komanda/skript)

**Testovi (MVP):**

- [ ] Nakon pokretanja seed-a, API vraća sve PlaceCategory zapise grupirane po sektoru
- [ ] Nakon pokretanja seed-a, API vraća sve EventCategory zapise grupirane po sektoru
- [ ] Ponavljano pokretanje seed skripte ne kreira duplikate
- [ ] Kategorija "Festivali" postoji i pod Muzika i pod Kultura i umjetnost (ispravan duplikat po dokumentaciji)

**Wireframe referenca:** —