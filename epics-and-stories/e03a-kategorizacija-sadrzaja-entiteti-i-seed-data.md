---
id: E03a
linear_id: ""
phase: MVP
journey_milestones: [J-02, J-04]
personas: [Marko, Ana, Thomas]
story_count: 5
---

# E03a — Kategorizacija sadržaja — entiteti i seed data

**Naslov:** Kategorizacija sadržaja — entiteti i seed data

**Excerpt:** Listinzi ne postoje u vakuumu — svaki event je koncert ili radionica, svako mjesto je restoran ili muzej. Ovaj epic uspostavlja trostruku organizaciju sadržaja (Sektor → Kategorija → Tagovi) i popunjava bazu inicijalnim setom kategorija i tagova za Sarajevo. Bez ovoga, Listing CRUD forma nema šta ponuditi korisniku za odabir.

**Scope — šta ulazi:**

- Category entitet (EventCategory + PlaceCategory) sa svim atributima iz Ch.04, sekcija 4.4
- Tag entiteti (EventTags + PlaceTags) sa atributima iz Ch.04, sekcija 4.5
- Relaciona tabela za listing-kategorija vezu (ListingCategories sa `isPrimary` flagom)
- Seed data: svih 16 sektora za mjesta i 11 sektora za događaje sa kompletnim listama kategorija
- Seed data: inicijalni set tagova za evente i mjesta
- Alias tabela za pretragu (alias → categoryId mapiranje)
- Seed data: inicijalni aliasi za Sarajevo (gym → Teretane i fitness, picerija → Restorani, itd.)
- API endpoint-i za čitanje kategorija i tagova (GET — javni, bez autentifikacije)

**Scope — šta NE ulazi:**

- Admin UI za upravljanje kategorijama i tagovima — dolazi u E03b (Sprint 5–6)
- Admin CRUD API za kategorije (POST/PUT/DELETE) — dolazi u E03b
- Spajanje tagova (merge) — dolazi u E03b
- Fulltext pretraga po aliasima — dolazi u E04 (Pretraga)

**Persone:** Marko (organizator), Ana (vlasnica biznisa), Thomas (turist) — indirektno, jer ovdje se postavljaju kategorije koje će oni koristiti

**Journey milestones:** J-02, J-04

**Phase:** MVP

**Dokumentacijska referenca:** Ch.04, sekcije 4.4–4.5 (kategorije i tagovi)

**Tehničke napomene:**

- Ovo je preduslov za E02 (Listing CRUD) — listing forma ne može funkcionisati bez kategorija u bazi.
- Sektor nije zaseban entitet — `sectorSlug` i `sectorName` su denormalizovani atributi na kategoriji (Ch.04, 4.4).
- EventCategory i PlaceCategory su odvojene tabele. EventTags i PlaceTags su odvojene tabele. Ne miješati.
- Slug kategorije je immutable — jednom kreiran, ne može se mijenjati.
- Seed data se piše kao zaseban korak (ne dio migracije) da bi se mogao ponovno pokrenuti ili ažurirati bez rollback-a schema-e.

**Success metrika:** API vraća kompletnu listu kategorija i tagova za evente i mjesta; developer može koristiti te podatke u Listing CRUD formi.

* * *

<a id="storije-u-ovom-epicu"></a>

## Storije u ovom epicu

| ID  | Naslov | Phase | Sprint |
| --- | --- | --- | --- |
| S03a-01 | Category entiteti i relaciona tabela | MVP | 0   |
| S03a-02 | Tag entiteti | MVP | 0   |
| S03a-03 | Seed data — kategorije za Sarajevo | MVP | 0   |
| S03a-04 | Seed data — tagovi i aliasi | MVP | 0   |
| S03a-05 | API endpoint-i za čitanje kategorija i tagova | MVP | 0   |