# E05 — Prikaz sadržaja i korisničke interakcije

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

- Pretraga i filtriranje — pokriveno u E04
- Kreiranje i editovanje listinga — pokriveno u E02
- Moderacijski pregled — pokriveno u E07
- Promocije i wallet — pokriveno u E09/E10
- Notifikacije — pokriveno u E12
- Mapni prikaz svih listinga (map view) — Backlog

**Persone:** Milica (mlada profesionalka — lajkuje i sprema u favorite), Thomas (turist — dijeli listing prijateljima, koristi sekundarni jezik), Ana (vlasnica biznisa — provjerava kako joj listing izgleda)

**Journey milestones:** J-04, J-05

**Phase:** MVP

**Dokumentacijska referenca:** Ch.02, sekcije 2.3, 2.6 (listing prikaz, visitors); Ch.04, sekcija 4.9 (korisničke interakcije)

**Tehničke napomene:**

- Zavisnost od E02 (listinzi moraju postojati), E03a (kategorije za prikaz na karticama), E04 (naslovna i pretraga gdje se kartice prikazuju).
- Visitor lajkovi koriste jednosmjerni hash kombinacije identifikacionih signala + listingId za zaštitu od duplikata — ne čuvati sirove podatke (Ch.04, 4.9).
- Related content algoritam ne mora biti savršen pri lansiranju — bitno je da prikazuje nešto smisleno (Ch.02, 2.3).
- Open Graph meta tagovi su potrebni za kvalitetan preview pri dijeljenju na socijalnim mrežama.
- Favoriti su privatni — samo korisnik vidi svoju listu.

**Success metrika:** Korisnik može pregledati detalje listinga, lajkovati ga, spremiti u favorite i podijeliti link prijatelju — sve u manje od 3 klika od liste rezultata.

* * *

<a id="storije-u-ovom-epicu"></a>

## Storije u ovom epicu

| ID  | Naslov | Phase | Sprint |
| --- | --- | --- | --- |
| S05-01 | Card komponenta za prikaz listinga u listama | MVP | 5–6 |
| S05-02 | Detaljna stranica listinga | MVP | 5–6 |
| S05-03 | Lajkovi za registrovane korisnike i visitore | MVP | 5–6 |
| S05-04 | Favoriti (Saved listings) | MVP | 5–6 |
| S05-05 | Dijeljenje listinga | MVP | 5–6 |
| S05-06 | Related content na detail stranici | MVP | 5–6 |