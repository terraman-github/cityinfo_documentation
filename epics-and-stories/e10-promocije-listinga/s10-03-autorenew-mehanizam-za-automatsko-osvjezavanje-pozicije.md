---
id: S10-03
parent_epic: E10
linear_id: "CIT2-62"
phase: MVP
journey_milestones: [J-06]
type: backend-only
---

# S10-03 — AutoRenew mehanizam za automatsko osvježavanje pozicije

**Naslov:** AutoRenew mehanizam za automatsko osvježavanje pozicije

**Excerpt:** AutoRenew automatski osvježava `sortDate` listinga na odabranom intervalu (3h/8h/24h), čime listing periodično "raste" na vrh liste. Ovo je plaćena automatizacija besplatnog ručnog refresh-a — bez 24h ograničenja, sa do 8 osvježavanja dnevno. Zahtijeva background job koji periodično pronalazi i ažurira eligible promocije.

**Phase:** MVP

**Journey milestones:** **J-06**

**User story:**  
Kao vlasnik listinga sa aktivnom promocijom,  
želim da se moj listing automatski osvježava na odabranom intervalu,  
kako bih zadržao visoku vidljivost bez da se ručno vraćam na platformu.

**Kontekst:** Korisnik je kreirao promociju ([S10-01](s10-01-kreiranje-i-aktivacija-promocije-listinga.md)) sa uključenim AutoRenew-om i odabranim intervalom. Background job periodično provjerava sve aktivne promocije sa `autoRenewEnabled: true` i ažurira `sortDate` za one čiji je `nextAutoRenewAt` prošao. Nakon svakog osvježavanja, `nextAutoRenewAt` se pomjera za interval unaprijed, a `autoRenewsCompleted` se inkrementira. Detalji o AutoRenew mehanizmu → **Ch.06, sekcija 6.2**.4.

**Acceptance criteria:**

- [ ] Background job periodično (npr. svakih 5 minuta) pronalazi promocije sa `autoRenewEnabled: true` i `nextAutoRenewAt <= NOW()` i `status: active`
- [ ] Za svaku eligible promociju: `sortDate` listinga se ažurira na NOW(), `nextAutoRenewAt` se postavlja na `NOW() + autoRenewInterval`, `autoRenewsCompleted` se inkrementira
- [ ] AutoRenew ne radi za pauzirane promocije (`status: paused`) — background job ih preskače
- [ ] AutoRenew ne radi za istekle promocije (`endDate < NOW()`) — background job ih označava kao `expired`
- [ ] Kreira se CreditTransaction sa `type: promo_autorenew` za svako osvježavanje (ako je AutoRenew pricing definisan; inače samo sortDate update bez naplate)
- [ ] Ako korisnik nema dovoljno kredita za AutoRenew naknadu, AutoRenew se deaktivira (`autoRenewEnabled: false`) i korisnik se obavještava
- [ ] Intervali su: 3h (8×/dan), 8h (3×/dan), 24h (1×/dan)

**Backend Scope:**

- Background job/scheduled task koji se pokreće periodično (preporučeno: svakih 5 minuta)
- Query: `SELECT * FROM Promos WHERE autoRenewEnabled = true AND nextAutoRenewAt <= NOW() AND status = 'active'`
- Za svaku: ažuriraj listing `sortDate`, Promo `nextAutoRenewAt` i `autoRenewsCompleted`
- Opciono: kreiraj CreditTransaction ako je pricing definisan
- Expiry check: ako je `endDate < NOW()`, postavi `status: expired`

**Tehničke napomene:**

- AutoRenew pricing model još nije finaliziran (vidi draft napomenu **Ch.06, sekcija 6.2**.4) — za MVP, implementirati mehanizam osvježavanja bez naplate po renewal-u; naplata se može dodati kad se pricing finalizira
- Background job treba biti idempotent — ako se pokrene dvaput, ne smije duplo osvježiti isti listing
- AutoRenew zaobilazi 24h cooldown za besplatni ručni refresh — to su dva odvojena mehanizma

**Testovi (MVP):**

- [ ] Promocija sa 3h intervalom: sortDate se ažurira 8× dnevno u pravilnim intervalima
- [ ] Pauzirana promocija se ne osvježava
- [ ] Istekla promocija se automatski označava kao `expired`
- [ ] `autoRenewsCompleted` se ispravno inkrementira
- [ ] Background job je idempotent — duplo pokretanje ne uzrokuje duplo osvježavanje

**Wireframe referenca:** —

**Implementacijske napomene:** Background job može biti jednostavan scheduled task (npr. IHostedService sa Timer-om) koji radi batch processing. Za MVP ne treba distribuirani lock — jedna instanca aplikacije je dovoljna.