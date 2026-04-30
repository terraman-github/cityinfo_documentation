---
id: S03a-01
parent_epic: E03a
linear_id: "CIT2-18"
phase: MVP
journey_milestones: [J-02]
type: backend-only
---
<!-- confluence-page-id: 251330561 -->
<!-- confluence-space-key: GI -->


# S03a-01 — Category entiteti i relaciona tabela

**Naslov:** Category entiteti i relaciona tabela

**Excerpt:** Kreiranje EventCategory i PlaceCategory tabela sa svim atributima, plus relaciona tabela za vezu listing-kategorija. Ovo je data model na kojem stoji sva organizacija sadržaja.

**Phase:** MVP

**Journey milestones:** J-02

**User story:**

*Kao developer,*  
*želim imati Category entitete i relacionu tabelu za listing-kategorija vezu,*  
*kako bih mogao povezati listinge sa kategorijama pri kreiranju sadržaja.*

**Kontekst:** Migracije za skeleton tabele su kreirane u [S14-04](../e14-infrastruktura-i18n-i-pozadinski-procesi/s14-04-inicijalna-db-schema-i-migracije.md), ali bez svih atributa. Ova storija dodaje kompletne atribute na Category entitete prema **Ch.04, sekcija 4.4**, i kreira relacionu tabelu `ListingCategories` (odvojeno za Event i Place) sa `isPrimary` flagom.

**Acceptance criteria:**

- [ ] EventCategory tabela postoji sa svim atributima iz **Ch.04, sekcija 4.4** (categoryId, slug, name, nameAlt, sectorSlug, sectorName, sectorNameAlt, description, icon, color, defaultImageUrl, sortOrder, isActive)
- [ ] PlaceCategory tabela postoji sa identičnom strukturom
- [ ] EventListingCategories relaciona tabela postoji (listingId, categoryId, isPrimary)
- [ ] PlaceListingCategories relaciona tabela postoji sa identičnom strukturom
- [ ] Slug je jedinstven unutar tabele i immutable
- [ ] `isPrimary` flag osigurava da svaki listing ima tačno jednu primarnu kategoriju (constraint)

**Testovi (MVP):**

- [ ] Migracija se uspješno pokreće na postojećoj bazi
- [ ] Pokušaj kreiranja dvije kategorije sa istim slug-om unutar iste tabele pada (unique constraint)
- [ ] Listing može imati jednu primarnu i više sekundarnih kategorija

**Wireframe referenca:** —