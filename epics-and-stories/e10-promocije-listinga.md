# E10 — Promocije listinga

**Naslov:** Promocije listinga

**Excerpt:** Promocije omogućavaju listing-ima bolju vidljivost kroz plaćeno isticanje. Tri tipa promocija (Standard, Premium, Premium+Homepage) sa različitim nivoima vidljivosti i cijenom, plus AutoRenew mehanizam za automatsko osvježavanje pozicije i mogućnost pauziranja/nastavka. Ovo je primarni mehanizam monetizacije koji direktno povezuje kreditni sistem sa vidljivošću sadržaja.

**Scope — šta ulazi:**

- Kreiranje promocije (Standard, Premium, Premium+Homepage) sa instant aktivacijom iz wallet-a
- Vizualno isticanje promotivnih listinga u listama i na naslovnoj
- Sortiranje: Premium sekcija na vrhu, Standard izmiješan sa običnim
- AutoRenew mehanizam (3h/8h/24h interval) sa background job-om
- Pauziranje i nastavak (Pause/Resume) promocije sa zamrzavanjem dana
- Besplatni ručni refresh pozicije (jednom u 24h)
- Pregled promocija za korisnika (moje promocije) i admin (sve promocije)
- Automatski expiry promocija (endDate prošao)
- Otkazivanje promocije pri brisanju listinga ili blokiranju korisnika

**Scope — šta NE ulazi:**

- Kreditni sistem i wallet (E09 — preduvjet)
- Scheduled promotions / zakazivanje unaprijed (Backlog)
- Pricing prilagođavanje po tenantu (Backlog)
- Napredna statistika promocija sa demographics (post-MVP)

**Persone:** Marko (organizator događaja), Ana (vlasnica biznisa)

**Journey milestones:** J-06 (Promocija sadržaja)

**Phase:** MVP

**Dokumentacijska referenca:** Ch.06, sekcije 6.2.1–6.2.7; Ch.02, sekcija 2.1 (naslovna stranica sortiranje)

**Tehničke napomene:**

- Promocije se aktiviraju instant pri kreiranju (prepaid model) — nema pending stanja
- Samo javno vidljivi listinzi (`isPublic = true`) mogu imati promociju
- Jedna aktivna promocija po listingu
- AutoRenew zahtijeva background job koji periodično ažurira `sortDate`
- Pauza zamrzava preostale dane i suspenduje AutoRenew
- Resume osvježava `sortDate` na NOW() i preračunava `endDate`
- `PROMO_MAX_PAUSE_DAYS` parametar kontroliše maksimalno trajanje pauze (default: 30 dana)
- Pricing za AutoRenew još nije finaliziran — vidi draft napomenu u Ch.06, sekcija 6.2.4

**Success metrika:** Korisnik može kreirati promociju, vidjeti listing istaknut u rezultatima, pauzirati i nastaviti promociju, i koristiti AutoRenew — sve bez potrebe za podrškom ili manualnom intervencijom.

* * *

<a id="storije-u-ovom-epicu"></a>

## Storije u ovom epicu

| #   | Naslov | Phase | Journey |
| --- | --- | --- | --- |
| S10-01 | Kreiranje i aktivacija promocije listinga | MVP | J-06 |
| S10-02 | Prikaz promotivnih listinga (sortiranje i vizualno isticanje) | MVP | J-06 |
| S10-03 | AutoRenew mehanizam za automatsko osvježavanje pozicije | MVP | J-06 |
| S10-04 | Pauziranje i nastavak promocije | MVP | J-06 |
| S10-05 | Ručno osvježavanje pozicije listinga | MVP | J-06 |
| S10-06 | Pregled i upravljanje promocijama | MVP | J-06 |