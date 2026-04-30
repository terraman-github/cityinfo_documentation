---
id: E11
confluence_page_id: "252706817"
linear_id: ""
phase: MVP
journey_milestones: [J-08]
personas: [Lejla, Damir]
story_count: 5
---

# E11 — Display oglašavanje (MVP)

**Naslov:** Display oglašavanje (MVP)

**Excerpt:** Display oglašavanje je u MVP-u dizajnirano kao maksimalno jednostavan model: Staff ručno postavlja banner oglase kroz admin panel, a sistem ih prikazuje na predefinisanim pozicijama. Nema self-service portala za oglašivače, nema kampanja ni biddinga — samo slika, link, zona i vremenski okvir. Ovaj pristup daje potpunu kontrolu timu i dovoljan je za prvih 5–10 oglašivača u ranoj fazi, dok display ads vjerovatno predstavlja primarni izvor prihoda dok korisnici još ne vide dovoljno traffica da investiraju u promocije listinga.

**Scope — šta ulazi:**

- DisplayAd CRUD za Staff (kreiranje, uređivanje, brisanje banner oglasa)
- Predefinisane reklamne zone (header, sidebar, in-feed, mobile)
- Logika prikaza oglasa na javnom frontendu (round-robin po prioritetu)
- Praćenje impressions i clicks za izvještavanje prema oglašivačima
- Aktivacija/deaktivacija oglasa i datumski okvir (startDate/endDate)
- Staff pregled statistike po oglasu

**Scope — šta NE ulazi:**

- Self-service portal za oglašivače (Faza 2 — Napredni Display Ads)
- AdCampaign entitet i CPC bidding (Faza 2)
- Targeting po kategorijama (Faza 2)
- Fraud detection (Faza 2)
- Advertiser entitet i advertiser balans (Faza 2)
- Weighted random selection (Faza 2)

**Persone:** Lejla (moderator/staff), Damir (ops manager)

**Journey milestones:** **J-08**

**Phase:** MVP

**Dokumentacijska referenca:** **Ch.06, sekcija 6.3**

**Tehničke napomene:**

- DisplayAd entitet i reklamne zone su tenant-specifični
- Impressions/clicks se broje automatski — impressions pri renderovanju zone, clicks pri redirectu na targetUrl
- Prazna zona (bez aktivnog oglasa) se ne prikazuje — nema placeholder sadržaja
- Napredni Display Ads sistem je planiran za Fazu 2 kad broj oglašivača preraste kapacitet ručnog upravljanja — detalji u **Ch.06, sekcija 6.3**.6

**Success metrika:** Staff može kreirati banner oglas, dodijeliti ga zoni, i vidjeti impressions/clicks statistiku — a korisnik vidi oglas na odgovarajućoj poziciji na stranici.

* * *

<a id="storije-u-ovom-epicu"></a>

## Storije u ovom epicu

| #   | Storija | Phase | Journey |
| --- | --- | --- | --- |
| [S11-01](e11-display-oglasavanje-mvp/s11-01-kreiranje-i-upravljanje-display-oglasima-staff.md) | Kreiranje i upravljanje display oglasima (Staff) | MVP | **J-08** |
| [S11-02](e11-display-oglasavanje-mvp/s11-02-prikaz-banner-oglasa-na-javnom-frontendu.md) | Prikaz banner oglasa na javnom frontendu | MVP | **J-08** |
| [S11-03](e11-display-oglasavanje-mvp/s11-03-praenje-impressions-i-clicks.md) | Praćenje impressions i clicks | MVP | **J-08** |
| [S11-04](e11-display-oglasavanje-mvp/s11-04-pregled-statistike-display-oglasa-staff.md) | Pregled statistike display oglasa (Staff) | MVP | **J-08** |
| [S11-05](e11-display-oglasavanje-mvp/s11-05-upravljanje-reklamnim-zonama.md) | Upravljanje reklamnim zonama | MVP | **J-08** |