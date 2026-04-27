---
id: S11-03
parent_epic: E11
linear_id: ""
phase: MVP
journey_milestones: [J-08]
type: fullstack
---

# S11-03 — Praćenje impressions i clicks

**Naslov:** Praćenje impressions i clicks

**Excerpt:** Sistem automatski broji impressions (prikazi) i clicks (klikove) za svaki display oglas. Ove metrike su osnova za izvještavanje prema oglašivačima i jedini mjerljivi indikator vrijednosti display oglašavanja u MVP-u.

**Phase:** MVP

**Journey milestones:** **J-08**

**User story:**  
Kao Staff korisnik,  
želim da sistem automatski prati koliko puta je oglas prikazan i koliko puta je kliknut,  
kako bih mogao izvijestiti oglašivače o performansama njihovih oglasa.

**Kontekst:** Impressions se inkrementiraju svaki put kad se oglas prikaže korisniku (pri dohvatu iz API-ja za prikaz u zoni). Clicks se inkrementiraju pri kliku na oglas — frontend šalje zahtjev za registraciju klika prije redirecta na targetUrl. Ovo su osnovne metrike bez napredne analitike — dovoljan nivo za MVP izvještavanje. Detalji → **Ch.06, sekcija 6.3**.5.

**Acceptance criteria:**

- [ ] Svaki put kad se oglas prikaže korisniku, impressions counter se inkrementira
- [ ] Svaki put kad korisnik klikne na oglas, clicks counter se inkrementira
- [ ] Klik registracija ne blokira redirect na targetUrl — korisnik ne osjeća kašnjenje
- [ ] Impressions i clicks su vidljivi u Staff admin panelu (prikaz u [S11-01](s11-01-kreiranje-i-upravljanje-display-oglasima-staff.md), statistika u [S11-04](s11-04-pregled-statistike-display-oglasa-staff.md))
- [ ] Counteri su konzistentni — ne gube se brojevi pri concurrent requestima

**Backend Scope:**

- Impression tracking: integrisano u `GET /api/ads/zone/{zoneId}` — pri svakom dohvatu oglasa, inkrementira se impressions za prikazani oglas
- `POST /api/ads/{adId}/click` — javni endpoint, registruje klik i vraća targetUrl za redirect; inkrementira clicks counter
- Validacija: adId mora postojati
- Side effects: ažurira impressions/clicks polja na DisplayAd entitetu

**Frontend Scope:**

- UI: nema posebnog UI-ja — ovo je pozadinska logika
- Klijentska validacija: nema
- UX: pri kliku na banner, frontend šalje async zahtjev na click endpoint i odmah radi redirect na targetUrl (fire-and-forget)

**Tehničke napomene:**

- Impression se broji pri dohvatu, ne pri renderovanju na klijentu — ovo je jednostavniji pristup za MVP
- Click tracking koristi fire-and-forget pattern — ne čekaj odgovor prije redirecta
- U MVP-u nema fraud detectiona — broje se svi impressions i clicks bez filtriranja

**Testovi (MVP):**

- [ ] Dohvat oglasa za zonu → impressions se inkrementira za 1
- [ ] Klik na oglas → clicks se inkrementira za 1 i korisnik je redirectan na targetUrl
- [ ] Više uzastopnih dohvata → impressions raste konzistentno
- [ ] Klik na nepostojeći oglas → 404

**Wireframe referenca:** —

**Implementacijske napomene:** Za MVP, direktno inkrementiranje countera na entitetu je dovoljno. Ako se pojavi potreba za detaljnijom analitikom (impressions po danu, unique clicks), može se dodati zasebna tabela sa događajima u budućoj fazi.