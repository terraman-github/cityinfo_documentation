---
id: S12-02
parent_epic: E12
linear_id: "CIT2-72"
phase: MVP
journey_milestones: [J-02, J-03, J-05, J-06]
type: fullstack
---

# S12-02 — Prikaz notifikacija i badge nepročitanih

**Naslov:** Prikaz notifikacija i badge nepročitanih

**Excerpt:** Korisnik vidi badge sa brojem nepročitanih notifikacija u headeru aplikacije, može otvoriti listu svih notifikacija, označiti ih kao pročitane, i klikom na notifikaciju navigirati do relevantnog sadržaja (listing, thread, promocija).

**Phase:** MVP

**Journey milestones:** Cross-cutting

**User story:**  
Kao registrovani korisnik,  
želim vidjeti svoje notifikacije i broj nepročitanih u headeru,  
kako bih bio u toku sa dešavanjima na mojim listinzima i promocijama.

**Kontekst:** Badge sa brojem nepročitanih notifikacija se uvijek prikazuje u headeru aplikacije za ulogovane korisnike. Klik na badge otvara listu notifikacija (paginirano, sortirano od najnovije). Svaka notifikacija ima naslov, kratki tekst, vrijeme i indikator da li je pročitana. Klik na notifikaciju je označava kao pročitanu i navigira korisnika na relevantni entitet. Detalji o Notification entitetu → **Ch.07, sekcija 7.2**.3.

**Acceptance criteria:**

- [ ] Header prikazuje badge sa brojem nepročitanih in-app notifikacija
- [ ] Badge prikazuje broj (npr. "3") ili indikator (dot) ako ima nepročitanih; ne prikazuje se ako je 0
- [ ] Klik na badge otvara listu notifikacija (dropdown ili zasebna stranica)
- [ ] Lista notifikacija prikazuje: naslov, kratki tekst, vrijeme (relativno — "prije 2 sata"), status čitanja (pročitana/nepročitana)
- [ ] Nepročitane notifikacije su vizuelno istaknute (npr. bold, pozadina)
- [ ] Klik na notifikaciju je označava kao pročitanu i navigira na referencirani entitet (listing, thread, promocija)
- [ ] Korisnik može označiti sve notifikacije kao pročitane ("Označi sve kao pročitano")
- [ ] Lista je paginirana (scroll ili "Učitaj više")
- [ ] Email notifikacije (channel='email') se ne prikazuju u in-app listi

**Backend Scope:**

- `GET /api/notifications` — lista in-app notifikacija korisnika (paginirano, sortirano po sentAt desc), filtrirano na channel='in\_app'
- `GET /api/notifications/unread-count` — vraća {count} nepročitanih in-app notifikacija
- `PATCH /api/notifications/{notificationId}` — označava notifikaciju kao pročitanu {isRead: true, readAt: NOW()}
- `POST /api/notifications/mark-all-read` — označava sve nepročitane kao pročitane
- Side effects: ažurira isRead i readAt polja

**Frontend Scope:**

- UI: badge u headeru (broj ili dot), dropdown/lista sa notifikacijama, "Označi sve kao pročitano" akcija
- Klijentska validacija: nema
- UX: badge se osvježava periodično (polling) ili pri navigaciji; relativno vrijeme ("prije 5 min", "jučer"); smooth tranzicija kad se notifikacija označi kao pročitana; klik navigira na relevantni entitet na osnovu referenceType/referenceId

**Tehničke napomene:**

- Badge count se može dohvatiti zasebnim lightweight endpointom (unread-count) da ne opterećuje glavni notifikacijski endpoint
- Polling interval za badge: svakih 30-60 sekundi je dovoljno za MVP; WebSocket pristup može doći kasnije
- Navigacija na osnovu referenceType: 'listing' → /listings/{id}, 'thread' → /listings/{listingId}/messages, 'promotion' → /promotions/{id}

**Testovi (MVP):**

- [ ] Korisnik sa 3 nepročitane notifikacije → badge prikazuje "3"
- [ ] Korisnik bez nepročitanih → badge se ne prikazuje
- [ ] Klik na nepročitanu notifikaciju → označena kao pročitana, badge se ažurira, navigacija na entitet
- [ ] "Označi sve kao pročitano" → sve nepročitane postaju pročitane, badge nestaje
- [ ] Lista prikazuje samo in-app notifikacije (ne email)
- [ ] Paginacija: scroll učitava starije notifikacije

**Wireframe referenca:** —

**Implementacijske napomene:** Za polling badge count-a, lightweight endpoint koji vraća samo broj je efikasniji od dohvatanja cijele liste. Ako se u budućnosti pojavi potreba za real-time notifikacijama, WebSocket ili Server-Sent Events su prirodna nadogradnja.