---
id: E03b
linear_id: ""
phase: MVP
journey_milestones: [J-08]
personas: [Lejla, Damir]
story_count: 4
---

# E03b — Kategorizacija sadržaja — admin upravljanje

**Naslov:** Kategorizacija sadržaja — admin upravljanje

**Excerpt:** Kategorije i tagovi su postavljeni u [E03a](e03a-kategorizacija-sadrzaja-entiteti-i-seed-data.md), ali neko ih mora moći mijenjati bez direktnog pristupa bazi. Ovaj epic daje Staff korisnicima (local\_admin i moderatorima sa `can_manage_tags`) alate za kreiranje, uređivanje, deaktivaciju i brisanje kategorija, tagova i aliasa — uključujući spajanje tagova kad se pojave duplikati. Bez ovoga, svaka promjena u kategorizaciji zahtijeva developer intervenciju.

**Scope — šta ulazi:**

- Admin CRUD za kategorije (EventCategory + PlaceCategory) — kreiranje, uređivanje, deaktivacija, brisanje
- Admin CRUD za tagove (EventTags + PlaceTags) — kreiranje, uređivanje, deaktivacija, brisanje
- Spajanje tagova (merge) — source tag se zamjenjuje target tagom na svim pogođenim listinzima
- Admin CRUD za aliase kategorija — kreiranje i brisanje mapiranja (alias → kategorija)
- Staff UI za upravljanje svim gore navedenim ([admin.cityinfo.ba](http://admin.cityinfo.ba))

**Scope — šta NE ulazi:**

- Kreiranje novih sektora — sektori su fiksni, dodaju se kroz seed data ([E03a](e03a-kategorizacija-sadrzaja-entiteti-i-seed-data.md))
- Bulk import/export kategorija — eventualno Backlog
- Fulltext pretraga po aliasima — pokriveno u [E04](e04-otkrivanje-i-pretraga-sadrzaja.md) (Pretraga)
- Public-facing API za čitanje kategorija/tagova — već isporučeno u [E03a](e03a-kategorizacija-sadrzaja-entiteti-i-seed-data.md)

**Persone:** Lejla (moderator — upravljanje tagovima), Damir (ops manager — upravljanje kategorijama i aliasima)

**Journey milestones:** **J-08**

**Phase:** MVP

**Dokumentacijska referenca:** **Ch.04**, sekcije 4.4–4.5 (pravila za kategorije, tagove, aliase, spajanje tagova)

**Tehničke napomene:**

- Zavisnost od [E03a](e03a-kategorizacija-sadrzaja-entiteti-i-seed-data.md) (entiteti moraju postojati) i [E13](e13-staff-panel-autentifikacija-i-upravljanje-osobljem.md) (Staff panel mora biti funkcionalan za pristup admin UI-ju).
- Kategorijama upravlja isključivo `local_admin`. Tagovima upravlja `can_manage_tags` permisija ili `local_admin`.
- Slug kategorije je immutable — ne može se mijenjati nakon kreiranja. Ako admin želi promijeniti slug, treba kreirati novu kategoriju i migrirati sadržaj — to je van MVP scope-a.
- Brisanje kategorije je moguće samo ako nijedan listing ne koristi tu kategoriju. U praksi se koristi deaktivacija.
- Spajanje tagova je atomična operacija — svi pogođeni listinzi se ažuriraju u jednoj transakciji, source tag se trajno briše, operacija se loguje za audit.

**Success metrika:** local\_admin može kreirati novu kategoriju, deaktivirati postojeću, i upravljati tagovima i aliasima — sve kroz Staff UI bez developer intervencije.

* * *

<a id="storije-u-ovom-epicu"></a>

## Storije u ovom epicu

| ID  | Naslov | Phase | Sprint |
| --- | --- | --- | --- |
| [S03b-01](e03b-kategorizacija-sadrzaja-admin-upravljanje/s03b-01-crud-kategorija-kroz-staff-panel.md) | CRUD kategorija kroz Staff panel | MVP | 5–6 |
| [S03b-02](e03b-kategorizacija-sadrzaja-admin-upravljanje/s03b-02-crud-tagova-kroz-staff-panel.md) | CRUD tagova kroz Staff panel | MVP | 5–6 |
| [S03b-03](e03b-kategorizacija-sadrzaja-admin-upravljanje/s03b-03-spajanje-tagova.md) | Spajanje tagova | MVP | 5–6 |
| [S03b-04](e03b-kategorizacija-sadrzaja-admin-upravljanje/s03b-04-crud-aliasa-kategorija-kroz-staff-panel.md) | CRUD aliasa kategorija kroz Staff panel | MVP | 5–6 |