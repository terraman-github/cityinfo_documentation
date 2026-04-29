---
id: S10-06
parent_epic: E10
linear_id: "CIT2-65"
phase: MVP
journey_milestones: [J-06]
type: fullstack
---

# S10-06 — Pregled i upravljanje promocijama

**Naslov:** Pregled i upravljanje promocijama

**Excerpt:** Korisnik vidi svoje promocije (aktivne, pauzirane, istekle) sa ključnim informacijama i akcijama. Admin/Staff vidi sve promocije na platformi sa mogućnošću otkazivanja. Ova storija pokriva pregled promocija iz obje perspektive — korisničke i admin.

**Phase:** MVP

**Journey milestones:** **J-06**

**User story:**  
Kao vlasnik listinga,  
želim pregledati sve svoje promocije sa statusima i preostalim trajanjem,  
kako bih mogao pratiti ulaganja i donositi odluke o nastavku ili pauziranju.

**Kontekst:** Korisnik pristupa sekciji "Moje promocije" u profilu ili kroz navigaciju. Vidi listu svih svojih promocija — aktivnih, pauziranih i istorijskih (istekle, otkazane). Za svaku promociju vidi tip, listing, trajanje, preostalo dana, AutoRenew status, i dostupne akcije. Staff pristupa admin pregledu sa svim promocijama na platformi. Detalji o Promo entitetu i statusima → **Ch.06**, sekcije 6.2.2–6.2.3; API endpointi → **Ch.06, sekcija 6.6**.3.

**Acceptance criteria:**

- [ ] Korisnik vidi listu svojih promocija sa: listing naziv, promoType, status (badge), startDate, endDate/remainingDays, AutoRenew status
- [ ] Lista je filtrabilna po statusu: active, paused, expired, cancelled, ili svi
- [ ] Za aktivnu promociju: dostupne akcije su "Pauziraj" i "Otkaži"
- [ ] Za pauziranu: dostupne akcije su "Nastavi" i "Otkaži"
- [ ] Za isteklu/otkazanu: nema akcija, samo pregled
- [ ] Korisnik može otkazati promociju (`DELETE /promotions/{id}`) — status prelazi u `cancelled`, bez refunda
- [ ] Otkazivanje zahtijeva potvrdu ("Da li ste sigurni? Krediti se ne vraćaju.")
- [ ] Staff/admin vidi sve promocije na platformi sa filterima po statusu, tipu, i korisniku
- [ ] Staff može otkazati bilo koju promociju (npr. listing obrisan, korisnik blokiran)
- [ ] Osnovna statistika po promociji: views i clicks (ako su dostupni iz listing analytics)

**Backend Scope:**

- `GET /promotions` — lista korisnikovih promocija sa filterima (`status`, paginacija)
- `GET /promotions/{id}` — detalji promocije
- `DELETE /promotions/{id}` — otkazivanje promocije (validacija: korisnik je vlasnik ili Staff)
- `GET /admin/promotions` — sve promocije sa proširenim filterima (`status`, `promoType`, `userId`, paginacija)
- Side effects otkazivanja: Promo `status: cancelled`, listing gubi promotivno isticanje, AutoRenew se deaktivira

**Frontend Scope:**

- UI (User): Stranica "Moje promocije" sa karticama/tabelom — listing, tip, status badge, datumi, akcije
- UI (User): Filter po statusu, sortiranje po datumu
- UI (Staff): Admin pregled promocija sa proširenim filterima i akcijama
- UX: Confirmation dialog za otkazivanje sa upozorenjem o no-refund politici
- UX: Prazna lista prikazuje CTA za kreiranje prve promocije

**Tehničke napomene:**

- Otkazivanje pri brisanju listinga ili blokiranju korisnika može biti automatsko (side effect iz [E02](../e02-listing-crud-i-lifecycle.md)/[E06](../e06-trust-tier-sistem.md)) — ova storija pokriva ručno otkazivanje
- Statistika (views, clicks) za MVP može biti bazična — detaljne demographics su post-MVP

**Testovi (MVP):**

- [ ] Korisnik vidi svoje promocije sa ispravnim statusima i podacima
- [ ] Filter po statusu vraća ispravne rezultate
- [ ] Otkazivanje aktivne promocije: status = `cancelled`, listing gubi isticanje
- [ ] Otkazivanje pauzirane promocije: status = `cancelled`
- [ ] Staff vidi sve promocije i može otkazati bilo koju
- [ ] Pokušaj otkazivanja tuđe promocije (non-Staff korisnik) vraća grešku

**Wireframe referenca:** —