---
id: S10-05
confluence_page_id: "252641281"
title: "S10-05 — Ručno osvježavanje pozicije listinga"
parent_epic: E10
linear_id: "CIT2-64"
phase: MVP
journey_milestones: [J-06]
type: fullstack
---

**Naslov:** Ručno osvježavanje pozicije listinga

**Excerpt:** Svaki korisnik može besplatno osvježiti poziciju svog javno vidljivog listinga jednom u 24 sata. Ovo je bazična funkcionalnost dostupna svima — ne zahtijeva promociju niti kredite. Listing dobija novi `sortDate` i efektivno "raste" na vrh liste.

**Phase:** MVP

**Journey milestones:** J-06

**User story:**

*Kao vlasnik listinga,*  
*želim besplatno osvježiti poziciju svog listinga jednom dnevno,*  
*kako bi moj listing bio vidljiviji bez troškova.*

**Kontekst:** Korisnik pristupa opciji refresh-a kroz "Moji listinzi" pregled ili listing detail stranicu. Klikom na "Osvježi poziciju", `sortDate` se ažurira na NOW() i listing se pojavljuje više u rezultatima. Cooldown je 24 sata — korisnik ne može osvježiti ponovo dok ne prođe 24h od zadnjeg ručnog refresh-a. Listing ima polje `lastManualRefreshAt` koje prati kad je korisnik zadnji put ručno osvježio. Detalji → **Ch.06, sekcija 6.2**.4.

**Acceptance criteria:**

- [ ] Korisnik može kliknuti "Osvježi poziciju" na svom javno vidljivom listingu
- [ ] Po kliku: `sortDate = NOW()`, `lastManualRefreshAt = NOW()`
- [ ] Ako je prošlo manje od 24h od zadnjeg ručnog refresh-a, dugme je onemogućeno sa prikazom preostalog vremena
- [ ] Samo javno vidljivi listinzi (`isPublic = true`) mogu biti osvježeni
- [ ] Ručni refresh je nezavisan od AutoRenew — oba mehanizma rade odvojeno
- [ ] Samo vlasnik listinga može osvježiti poziciju
- [ ] Refresh ne košta kredite — potpuno besplatan

**Backend Scope:**

- `POST /listings/{id}/refresh` — ažurira `sortDate` i `lastManualRefreshAt` na NOW(); vraća `{ listingId, newSortDate, nextRefreshAvailableAt }`
- Validacija: listing javno vidljiv (`isPublic = true`), korisnik je vlasnik, `lastManualRefreshAt` + 24h <= NOW()
- Ako je cooldown aktivan, vraća grešku sa `nextRefreshAvailableAt`

**Frontend Scope:**

- UI: Dugme "Osvježi poziciju" na listing kartici u "Moji listinzi" i na listing detail stranici
- UI: Ako je cooldown aktivan, dugme je disabled sa countdown-om ili tekstom "Dostupno za X sati"
- Klijentska validacija: nema — server kontroliše cooldown
- UX: Po uspjehu toast "Pozicija osvježena!"; po grešci (cooldown) inline poruka sa preostalim vremenom

**Tehničke napomene:**

- `lastManualRefreshAt` je per-listing polje, ne per-user — svaki listing ima svoj cooldown
- AutoRenew iz promocije i ručni refresh su potpuno nezavisni — korisnik sa AutoRenew-om može i dalje ručno refreshati (mada rijetko ima smisla)

**Testovi (MVP):**

- [ ] Ručni refresh ažurira `sortDate` i `lastManualRefreshAt`
- [ ] Pokušaj refresh-a unutar 24h vraća grešku sa `nextRefreshAvailableAt`
- [ ] Refresh nakon 24h prolazi uspješno
- [ ] Pokušaj refresh-a za listing koji nije javno vidljiv (`isPublic = false`) vraća grešku
- [ ] Korisnik koji nije vlasnik ne može osvježiti tuđi listing

**Wireframe referenca:** —