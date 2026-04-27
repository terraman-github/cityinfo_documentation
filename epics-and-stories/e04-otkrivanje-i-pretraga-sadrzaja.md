---
id: E04
linear_id: ""
phase: MVP
journey_milestones: [J-04]
personas: [Milica, Thomas, Ana]
story_count: 7
---

# E04 — Otkrivanje i pretraga sadržaja

**Naslov:** Otkrivanje i pretraga sadržaja

**Excerpt:** Platforma bez pretrage je katalog koji niko ne čita. Ovaj epic pokriva sve načine na koje korisnik pronalazi sadržaj — od naslovne stranice sa promocijskim prioritetima, preko full-text pretrage sa autosuggest-om i alias mapiranjem, do filtriranja po kategoriji, tagu, datumu i lokaciji. Uključuje i lokacijski dijalog, paginaciju, te responsive prilagodbu svih prikaza.

**Scope — šta ulazi:**

- Naslovna stranica sa dva režima (Događaji / Mjesta) i dvije grupe sadržaja (Premium+Homepage, ostali)
- Prebacivanje režima (Events ↔ Places) kroz navigaciju
- Quick search sa full-text pretragom (po name, nameAlt, description, descriptionAlt)
- Autosuggest pri pretrazi (hijerarhijski: kategorije → tagovi → listinzi)
- Alias mapiranje u pretrazi — pretraga "gym" pronalazi kategoriju "Teretane i fitness"
- Filter po kategoriji (primarna ili bilo koja sekundarna)
- Filter po tagu
- Filter po datumu (samo Events režim) — jednodnevni filter, ne interval
- Filter po udaljenosti (od korisnikove lokacije, samo unutar zone tenanta)
- Kombinovanje filtera (AND logika), sticky filteri, chipovi za aktivne filtere
- Prazni rezultati — prijedlozi za relaksaciju filtera
- Lokacijski indikator u headeru i lokacijski dijalog (GPS, ručni unos, zona pokrivenosti)
- Sortiranje po `sortDate` sa promocijskim prioritetima u kategorijama (Premium na vrhu)
- Paginacija (lazy loading / infinite scroll)
- Responsive dizajn: mobile-first, breakpoints za telefon/tablet/desktop
- Featured sekcije na naslovnoj (konfigurisane od admina)
- Jezik sučelja — prikaz na odabranom jeziku, fallback na primarni

**Scope — šta NE ulazi:**

- Listing detail stranica — pokriveno u E05
- Korisničke interakcije (lajk, favorit, share) — pokriveno u E05
- Related content na detail stranici — pokriveno u E05
- Admin konfiguracija featured sekcija — Backlog (za MVP: hardkodirane sekcije)
- Geofencing notifikacije — Phase 2
- Napredni search (faceted, weighted scoring, ML ranking) — Phase 2+

**Persone:** Milica (mlada profesionalka — brza pretraga), Thomas (turist — browse po kategorijama, sekundarni jezik), Ana (vlasnica biznisa — provjerava poziciju svog listinga)

**Journey milestones:** J-04

**Phase:** MVP

**Dokumentacijska referenca:** Ch.02, sekcije 2.1–2.2, 2.4–2.5 (naslovna, pretraga, sortiranje, responsive)

**Tehničke napomene:**

- Zavisnost od E02 (listinzi moraju postojati), E03a (kategorije i tagovi), i E10 (promocije — za ispravno sortiranje promoviranih listinga). Bez E10 se koristi samo sortDate sortiranje.
- Dva režima (Events / Places) koriste odvojene API pozive i odvojene sisteme kategorija/tagova — nema miješanja.
- Lokacijski dijalog koristi Google Maps API za autocomplete (ručni unos) i Google Maps za prikaz mape sa zonom pokrivenosti.
- Featured sekcije za MVP mogu biti hardkodirane (npr. "Ovaj vikend", "Novo otvoreno") — admin konfiguracija je Backlog.
- Alias mapiranje se dešava na backend-u — frontend šalje originalni tekst pretrage, backend provjerava alias tabelu i proširuje rezultate.

**Success metrika:** Korisnik može pronaći relevantan listing u manje od 3 interakcije (search, filter, ili browse); autosuggest prikazuje rezultate dok korisnik kuca; promjena lokacije odmah utiče na prikaz udaljenosti.

* * *

<a id="storije-u-ovom-epicu"></a>

## Storije u ovom epicu

| ID  | Naslov | Phase | Sprint |
| --- | --- | --- | --- |
| S04-01 | Naslovna stranica sa dva režima i promocijskim prioritetima | MVP | 5–6 |
| S04-02 | Full-text pretraga sa alias mapiranjem | MVP | 5–6 |
| S04-03 | Autosuggest pri pretrazi | MVP | 5–6 |
| S04-04 | Filtriranje po kategoriji, tagu i datumu | MVP | 5–6 |
| S04-05 | Lokacijski dijalog i filter po udaljenosti | MVP | 5–6 |
| S04-06 | Sortiranje po sortDate sa promocijskim prioritetima i paginacija | MVP | 5–6 |
| S04-07 | Responsive dizajn i mobile-first layout | MVP | 5–6 |