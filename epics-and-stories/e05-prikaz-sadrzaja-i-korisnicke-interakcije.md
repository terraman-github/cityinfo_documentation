---
id: E05
confluence_page_id: "252084225"
title: "E05 — Prikaz sadržaja i korisničke interakcije"
linear_id: ""
phase: MVP
journey_milestones: [J-04, J-05]
personas: [Milica, Thomas, Ana]
story_count: 6
---

**Naslov:** Prikaz sadržaja i korisničke interakcije

**Excerpt:** Korisnik je pronašao listing — sada ga treba vidjeti u punom sjaju i moći interagovati sa njim. Ovaj epic pokriva card komponentu za liste, detaljnu stranicu sa galerijom i mapom, te tri forme interakcije: lajkovi (uključujući visitor lajkove), favoriti, i dijeljenje. Na dnu detail stranice, related content pomaže korisniku da otkrije još relevantnog sadržaja.

**Scope — šta ulazi:**

- Card komponenta za prikaz listinga u listama/gridovima (slika, naziv, excerpt, kategorija, tagovi, datum, udaljenost, badge-ovi)
- Vizuelno razlikovanje promocija na karticama (Standard, Premium, Premium+Homepage)
- Detaljna stranica listinga sa galerijom, mapom, punim opisom, kontakt informacijama
- Prikaz child evenata na parent event stranici
- Prikaz povezanih evenata na Place stranici
- Lajkovi (Appreciation) za registrovane korisnike — lajk/unlike, historija lajkova
- Visitor lajkovi — samo brojač, zaštita od zloupotrebe
- Favoriti (Saved listings) za registrovane korisnike — dodaj/ukloni, lista favorita u profilu
- Dijeljenje (Share) — native share API + copy-to-clipboard fallback, Open Graph meta tagovi
- Related content na dnu detail stranice

**Scope — šta NE ulazi:**

- Pretraga i filtriranje — pokriveno u [E04](e04-otkrivanje-i-pretraga-sadrzaja.md)
- Kreiranje i editovanje listinga — pokriveno u [E02](e02-listing-crud-i-lifecycle.md)
- Moderacijski pregled — pokriveno u [E07](e07-moderacijski-workflow-i-ai-screening.md)
- Promocije i wallet — pokriveno u [E09](e09-kreditni-sistem-i-wallet.md)/[E10](e10-promocije-listinga.md)
- Notifikacije — pokriveno u [E12](e12-notifikacije.md)
- Mapni prikaz svih listinga (map view) — Backlog

**Persone:** Milica (mlada profesionalka — lajkuje i sprema u favorite), Thomas (turist — dijeli listing prijateljima, koristi sekundarni jezik), Ana (vlasnica biznisa — provjerava kako joj listing izgleda)

**Journey milestones:** J-04, **J-05**

**Phase:** MVP

**Dokumentacijska referenca:** Ch.02, sekcije 2.3, 2.6 (listing prikaz, visitors); **Ch.04, sekcija 4.9** (korisničke interakcije)

**Tehničke napomene:**

- Zavisnost od [E02](e02-listing-crud-i-lifecycle.md) (listinzi moraju postojati), [E03a](e03a-kategorizacija-sadrzaja-entiteti-i-seed-data.md) (kategorije za prikaz na karticama), [E04](e04-otkrivanje-i-pretraga-sadrzaja.md) (naslovna i pretraga gdje se kartice prikazuju).
- Visitor lajkovi koriste jednosmjerni hash kombinacije identifikacionih signala + listingId za zaštitu od duplikata — ne čuvati sirove podatke (**Ch.04**, 4.9).
- Related content algoritam ne mora biti savršen pri lansiranju — bitno je da prikazuje nešto smisleno (**Ch.02**, 2.3).
- Open Graph meta tagovi su potrebni za kvalitetan preview pri dijeljenju na socijalnim mrežama.
- Favoriti su privatni — samo korisnik vidi svoju listu.

**Success metrika:** Korisnik može pregledati detalje listinga, lajkovati ga, spremiti u favorite i podijeliti link prijatelju — sve u manje od 3 klika od liste rezultata.

* * *

<a id="storije-u-ovom-epicu"></a>

## Storije u ovom epicu

| ID  | Naslov | Phase | Sprint |
| --- | --- | --- | --- |
| [S05-01](e05-prikaz-sadrzaja-i-korisnicke-interakcije/s05-01-card-komponenta-za-prikaz-listinga-u-listama.md) | Card komponenta za prikaz listinga u listama | MVP | 5–6 |
| [S05-02](e05-prikaz-sadrzaja-i-korisnicke-interakcije/s05-02-detaljna-stranica-listinga.md) | Detaljna stranica listinga | MVP | 5–6 |
| [S05-03](e05-prikaz-sadrzaja-i-korisnicke-interakcije/s05-03-lajkovi-za-registrovane-korisnike-i-visitore.md) | Lajkovi za registrovane korisnike i visitore | MVP | 5–6 |
| [S05-04](e05-prikaz-sadrzaja-i-korisnicke-interakcije/s05-04-favoriti-saved-listings.md) | Favoriti (Saved listings) | MVP | 5–6 |
| [S05-05](e05-prikaz-sadrzaja-i-korisnicke-interakcije/s05-05-dijeljenje-listinga.md) | Dijeljenje listinga | MVP | 5–6 |
| [S05-06](e05-prikaz-sadrzaja-i-korisnicke-interakcije/s05-06-related-content-na-detail-stranici.md) | Related content na detail stranici | MVP | 5–6 |