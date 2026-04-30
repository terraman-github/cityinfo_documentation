---
id: E02
confluence_page_id: "251330580"
linear_id: ""
phase: MVP
journey_milestones: [J-02]
personas: [Marko, Ana, Kemal]
story_count: 9
---

# E02 — Listing CRUD i lifecycle

<a id="e02-listing-crud-i-lifecycle"></a>

# E02 — Listing CRUD i lifecycle

**Naslov:** Listing CRUD i lifecycle

**Excerpt:** Bez listinga nema platforme — ovo je centralna funkcionalnost koja omogućava korisnicima da kreiraju, uređuju, objavljuju i upravljaju događajima (Events) i mjestima (Places). Epic pokriva kompletan CRUD za oba tipa sadržaja, statusne tranzicije (draft → in\_review/published\_under\_review → published → removed/expired), upload multimedijalnog sadržaja i dokumenata, te mehanizme brisanja i sakrivanja. Ovo je srce CityInfo-a i preduslov za gotovo sve što dolazi poslije.

**Scope — šta ulazi:**

- Kreiranje Event listinga sa svim zajedničkim (Listing) i specifičnim (Event) atributima
- Kreiranje Place listinga sa svim zajedničkim i specifičnim atributima
- Editovanje objavljenog listinga (ponašanje ovisno o Trust Tier-u — **Ch.04**, 4.8)
- Submit na moderaciju (pre-mod za Tier 0–1, post-mod za Tier 2+)
- Statusne tranzicije: draft → in\_review → published (pre-mod); draft → published\_under\_review → published (post-mod). Dijagram u **Ch.04**, 4.8.
- Sakrivanje od strane vlasnika (`hidden_by_owner`), moderatora (`hidden_by_moderator`) i sistema (`hidden_by_system`)
- Otkazivanje Event-a (`canceled`) i reaktivacija
- Automatski istek Event-a (`expired`) i Place snapshot mehanizam
- Brisanje listinga — `removed` sa `removedReason` (`user_delete` za korisničko brisanje; ostali razlozi iz moderacije)
- `wasEverActive` flag koji kontrolira mogućnost brisanja
- Event hijerarhija (parent/child — festivali, konferencije)
- Lokacija Event-a (povezivanje sa Place-om istog vlasnika ili ručna adresa)
- Ručno osvježavanje sortDate (jednom u 24h, besplatno)
- Upload i upravljanje slikama (featured image + galerija do 5 slika, AI screening)
- Upload i upravljanje dokumentima listinga (ListingDocument, virus scanning)
- changes\_requested timeout mehanizam (parametrizirano)
- Dvojezična polja (nameAlt, descriptionAlt, excerptAlt) na listing formi
- Praćenje statusa objave iz korisničke perspektive (**Ch.02**, 2.8)

**Scope — šta NE ulazi:**

- Moderacijski workflow i moderatorski UI ([E07](e07-moderacijski-workflow-i-ai-screening.md))
- Trust Tier logika i automatsko napredovanje/degradacija ([E06](e06-trust-tier-sistem.md))
- Korisničke interakcije — lajkovi, favoriti, dijeljenje ([E05](e05-prikaz-sadrzaja-i-korisnicke-interakcije.md))
- Promocije i AutoRenew ([E10](e10-promocije-listinga.md))
- Pretraga i filtriranje listinga ([E04](e04-otkrivanje-i-pretraga-sadrzaja.md))
- Prikaz listing kartice i detaljne stranice za posjetioce ([E05](e05-prikaz-sadrzaja-i-korisnicke-interakcije.md))
- Komunikacija uz listing — Message sistem ([E08](e08-komunikacija-uz-listing-i-dokumenti.md))
- Verifikacija vlasništva workflow iz moderatorske perspektive ([E07](e07-moderacijski-workflow-i-ai-screening.md)/[E08](e08-komunikacija-uz-listing-i-dokumenti.md))
- Upravljanje kategorijama i tagovima od strane Staff-a ([E03b](e03b-kategorizacija-sadrzaja-admin-upravljanje.md))
- Notifikacije ([E12](e12-notifikacije.md))

**Persone:** Marko (organizator događaja), Ana (vlasnica biznisa), Kemal (lokalni entuzijast)

**Journey milestones:** **J-02**

**Phase:** MVP

**Dokumentacijska referenca:** **Ch.04** (sekcije 4.1–4.3, 4.6–4.8), **Ch.02** (sekcija 2.8)

**Tehničke napomene:**

- Zavisi od [E14](e14-infrastruktura-i18n-i-pozadinski-procesi.md) (infrastruktura) i [E03a](e03a-kategorizacija-sadrzaja-entiteti-i-seed-data.md) (kategorije seed data — forma za kreiranje listinga treba kategorije)
- Zavisi od [E01](e01-korisnicka-registracija-i-profil.md) (registracija) — korisnik mora biti registrovan i verificiran
- Listing entitet je apstraktan — Event i Place nasljeđuju zajedničku osnovu
- Image upload i AI screening su asinhroni — ne blokiraju kreiranje listinga
- Trust Tier logika za pre/post moderaciju implementira se u [E06](e06-trust-tier-sistem.md), ali E02 mora poštovati interface (statusne tranzicije moraju podržavati oba toka)
- sortDate se inicijalno postavlja pri kreiranju; osvježavanje kroz promocije pripada [E10](e10-promocije-listinga.md)
- `listingStatus` je jedini status field — nema odvojenog `lifecycleStatus`/`moderationStatus`. `isPublic` se derivira iz statusa, `removedReason` opisuje razlog trajnog uklanjanja.

**Success metrika:** Korisnik može kreirati Event ili Place listing, popuniti sve podatke uključujući slike i dokumente, objaviti ga, i pratiti status objave — sve u manje od 5 minuta.

* * *

<a id="storije-u-ovom-epicu"></a>

## Storije u ovom epicu

| #   | Naslov | Phase |
| --- | --- | --- |
| [S02-01](e02-listing-crud-i-lifecycle/s02-01-kreiranje-event-listinga-sa-osnovnim-podacima.md) | Kreiranje Event listinga sa osnovnim podacima | MVP |
| [S02-02](e02-listing-crud-i-lifecycle/s02-02-kreiranje-place-listinga-sa-osnovnim-podacima.md) | Kreiranje Place listinga sa osnovnim podacima | MVP |
| [S02-03](e02-listing-crud-i-lifecycle/s02-03-lokacija-event-a-povezivanje-sa-place-om-ili-rucna-adresa.md) | Lokacija Event-a — povezivanje sa Place-om ili ručna adresa | MVP |
| [S02-04](e02-listing-crud-i-lifecycle/s02-04-event-hijerarhija-kreiranje-i-upravljanje-child-eventima.md) | Event hijerarhija — kreiranje i upravljanje child eventima | MVP |
| [S02-05](e02-listing-crud-i-lifecycle/s02-05-upload-i-upravljanje-slikama-listinga.md) | Upload i upravljanje slikama listinga | MVP |
| [S02-06](e02-listing-crud-i-lifecycle/s02-06-upload-i-upravljanje-dokumentima-listinga.md) | Upload i upravljanje dokumentima listinga | MVP |
| [S02-07](e02-listing-crud-i-lifecycle/s02-07-objava-listinga-i-statusne-tranzicije.md) | Objava listinga i statusne tranzicije | MVP |
| [S02-08](e02-listing-crud-i-lifecycle/s02-08-editovanje-brisanje-i-sakrivanje-listinga.md) | Editovanje, brisanje i sakrivanje listinga | MVP |
| [S02-09](e02-listing-crud-i-lifecycle/s02-09-rucno-osvjezavanje-sortdate-i-praenje-statusa-objave.md) | Ručno osvježavanje sortDate i praćenje statusa objave | MVP |