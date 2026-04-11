# S10-04 — Pauziranje i nastavak promocije

**Naslov:** Pauziranje i nastavak promocije

**Excerpt:** Korisnik može privremeno pauzirati aktivnu promociju da "sačuva" preostale dane — npr. restoran zatvoren za renovaciju ili organizator čeka bolji termin. Pri pauzi se zamrzavaju preostali dani i suspenduje AutoRenew; pri nastavku se preračunava endDate, osvježava sortDate, i reaktivira AutoRenew.

**Phase:** MVP

**Journey milestones:** J-06

**User story:**  
Kao vlasnik listinga sa aktivnom promocijom,  
želim pauzirati promociju kad mi ne treba i nastaviti je kad sam spreman,  
kako ne bih gubio plaćene dane promocije u periodima kad listing nije relevantan.

**Kontekst:** Korisnik pristupa opciji pauze kroz pregled svojih promocija ili kroz listing detail stranicu. Pauza zamrzava preostale dane i suspenduje sve efekte promocije — listing gubi promotivno isticanje i AutoRenew se zaustavlja. Korisnik može nastaviti promociju kad god želi; pri nastavku, endDate se preračunava na osnovu preostalih dana, sortDate se osvježava na NOW(), i AutoRenew se reaktivira. Maksimalno trajanje pauze je kontrolisano parametrom `PROMO_MAX_PAUSE_DAYS`. Detalji → Ch.06, sekcija 6.2.5.

**Acceptance criteria:**

- [ ] Korisnik može pauzirati aktivnu promociju — status prelazi u `paused`, `pausedAt = NOW()`
- [ ] Pri pauziranju: `remainingDays` se kalkuliše kao razlika između `endDate` i `NOW()`, `endDate` se zamrzava
- [ ] Pri pauziranju: AutoRenew se suspenduje (`nextAutoRenewAt` se briše), listing gubi promotivno isticanje
- [ ] Listing sa pauziranom promocijom se tretira kao obični u sortiranju (nema premium sekcije, nema vizualnog highlight-a)
- [ ] `sortDate` se NE mijenja pri pauziranju — listing zadržava trenutnu poziciju ali bez promotivnog statusa
- [ ] Korisnik može nastaviti (resume) pauziranu promociju — status se vraća na `active`
- [ ] Pri nastavku: `endDate = NOW() + remainingDays`, `sortDate = NOW()`, `pausedAt` i `remainingDays` se čiste
- [ ] Pri nastavku: AutoRenew se reaktivira (ako je bio enabled) — `nextAutoRenewAt = NOW() + autoRenewInterval`
- [ ] Nema ograničenja broja pauza — korisnik može pauzirati i nastaviti proizvoljan broj puta
- [ ] Pauzirana promocija automatski prelazi u `expired` nakon `PROMO_MAX_PAUSE_DAYS` dana (parametar, default: 30)
- [ ] Krediti se ne vraćaju pri pauziranju (prepaid model)

**Backend Scope:**

- `POST /promotions/{id}/pause` — postavlja `status: paused`, kalkuliše `remainingDays`, briše `nextAutoRenewAt`; vraća `{ promoId, status, remainingDays, pausedAt }`
- `POST /promotions/{id}/resume` — postavlja `status: active`, preračunava `endDate`, osvježava `sortDate`, reaktivira AutoRenew; vraća `{ promoId, status, newEndDate, sortDate }`
- Validacija za pause: promocija mora biti `active`
- Validacija za resume: promocija mora biti `paused`
- Background job check: pauzirane promocije čiji je `pausedAt + PROMO_MAX_PAUSE_DAYS < NOW()` prelaze u `expired`

**Frontend Scope:**

- UI: Dugme "Pauziraj" na aktivnoj promociji (u pregledu promocija i na listing detail-u)
- UI: Dugme "Nastavi" na pauziranoj promociji sa prikazom preostalih dana
- UI: Indikator da je promocija pauzirana — vizualno različit od aktivne i istekle
- UX: Potvrda prije pauziranja ("Promocija će biti pauzirana. Preostalo dana: X. Nastavite?")
- UX: Toast nakon uspješne pauze/nastavka

**Tehničke napomene:**

- `remainingDays` se kalkuliše pri pauziranju, ne čuva se unaprijed — ovo je jedini trenutak kad je ova vrijednost relevantna
- Resume osvježava `sortDate` na NOW() — listing efektivno "skače" na vrh kao da je tek promoviran
- Background job za max pause check može biti dio istog job-a koji radi AutoRenew i expiry provjere

**Testovi (MVP):**

- [ ] Pauziranje aktivne promocije: status = `paused`, `remainingDays` ispravno kalkulisan
- [ ] Nastavak pauzirane promocije: status = `active`, `endDate` preračunat, `sortDate` osvježen
- [ ] Listing sa pauziranom promocijom nema promotivno isticanje u listi
- [ ] AutoRenew se suspenduje pri pauzi i reaktivira pri nastavku
- [ ] Promocija pauzirana duže od `PROMO_MAX_PAUSE_DAYS` automatski prelazi u `expired`
- [ ] Pokušaj pauziranja već pauzirane promocije vraća grešku
- [ ] Pokušaj nastavka aktivne promocije vraća grešku

**Wireframe referenca:** —