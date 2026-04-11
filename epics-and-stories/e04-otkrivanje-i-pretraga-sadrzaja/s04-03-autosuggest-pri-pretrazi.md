# S04-03 — Autosuggest pri pretrazi

**Naslov:** Autosuggest pri pretrazi

**Excerpt:** Dok korisnik kuca u search bar, sistem nudi prijedloge u hijerarhijskom redoslijedu: kategorije, zatim tagovi, pa listinzi. Klik na kategoriju aktivira filter, klik na listing otvara detail stranicu. Autosuggest radi samo unutar aktivnog režima.

**Phase:** MVP

**Journey milestones:** J-04

**User story:**  
Kao posjetilac,  
želim vidjeti prijedloge dok kucam u search bar,  
kako bih brže došao do željenog rezultata bez kompletnog unosa i čekanja na pretragu.

**Kontekst:** Korisnik počinje kucati u search bar. Nakon minimalno 2 karaktera, dropdown se pojavljuje sa hijerarhijskim prijedlozima. Redoslijed prikazivanja: kategorije → tagovi → listinzi (Ch.02, sekcija 2.2). Autosuggest prikazuje samo sadržaj relevantan za aktivni režim.

**Acceptance criteria:**

- [ ] Autosuggest dropdown se pojavljuje nakon unosa minimalno 2 karaktera
- [ ] Rezultati su grupisani hijerarhijski: KATEGORIJE, TAGOVI, LISTINZI — sa jasnim vizuelnim razdvajanjem
- [ ] Svaka grupa prikazuje do 3 rezultata (ukupno max 9 prijedloga)
- [ ] Klik na kategoriju aktivira filter te kategorije i prikazuje listu listinga
- [ ] Klik na tag aktivira filter tog taga i prikazuje listu listinga
- [ ] Klik na listing otvara detaljnu stranicu tog listinga
- [ ] Autosuggest pretražuje samo sadržaj aktivnog režima (Events ili Places)
- [ ] Alias mapiranje funkcioniše i u autosuggest-u — "gym" prikazuje kategoriju "Teretane i fitness"
- [ ] Dropdown se zatvara kad korisnik klikne izvan njega ili pritisne Escape
- [ ] Korisnik može koristiti tastaturne strelice za navigaciju kroz prijedloge

**Backend Scope:**

- `GET /search/suggest?q={term}&type={events|places}` — vraća {categories: \[...\], tags: \[...\], listings: \[...\]} sa limitiranim brojem rezultata po grupi
- Uključuje alias provjeru za termin
- Response mora biti brz (cilj: < 200ms)

**Frontend Scope:**

- UI: Dropdown ispod search bara sa tri sekcije i ikonama za tip (kategorija/tag/listing)
- Klijentska validacija: minimum 2 karaktera, debounce na input
- UX: Debounce od 300ms na input da se izbjegnu prekomjerni API pozivi
- UX: Loading indikator u dropdown-u dok se rezultati učitavaju
- UX: Keyboard navigacija (strelice gore/dolje, Enter za odabir)

**Tehničke napomene:**

- Debounce je ključan za performanse — ne slati API poziv na svako pritiskanje tipke.
- Rezultati se mogu keširati na frontendu za isti termin tokom iste sesije.

**Testovi (MVP):**

- [ ] Unos "teh" prikazuje kategorije koje počinju sa "teh", tagove i listinge
- [ ] Klik na kategoriju "Tehnika i elektronika" — aktivira filter i prikazuje listinge
- [ ] Klik na listing — otvara se detail stranica
- [ ] Prebacivanje iz Events u Places režim — autosuggest rezultati se mijenjaju
- [ ] Unos jednog karaktera — dropdown se ne pojavljuje

**Wireframe referenca:** —

**Implementacijske napomene:** Debounce vrijednost od 300ms je dobar početak — može se prilagoditi na osnovu korisničkog feedbacka. Za keyboard navigaciju razmotriti WAI-ARIA combobox pattern za pristupačnost.