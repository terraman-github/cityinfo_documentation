---
id: S11-01
confluence_page_id: "251920405"
title: "S11-01 — Kreiranje i upravljanje display oglasima (Staff)"
parent_epic: E11
linear_id: "CIT2-66"
phase: MVP
journey_milestones: [J-08]
type: fullstack
---

**Naslov:** Kreiranje i upravljanje display oglasima (Staff)

**Excerpt:** Staff kreira, uređuje i briše banner oglase kroz admin panel. Svaki oglas ima sliku, destination link, dodijeljenu zonu i opcioni vremenski okvir — to je sve što treba za MVP model ručnog upravljanja display oglašavanjem.

**Phase:** MVP

**Journey milestones:** J-08

**User story:**

*Kao Staff korisnik,*  
*želim kreirati i upravljati banner oglasima kroz admin panel,*  
*kako bih mogao brzo postaviti oglase za lokalne oglašivače bez potrebe za složenim kampanjama.*

**Kontekst:** Display oglašavanje u MVP-u koristi maksimalno jednostavan model — Staff ručno postavlja oglase, nema self-service portala za oglašivače. Staff pristupa admin panelu ([admin.cityinfo.ba](http://admin.cityinfo.ba)), odabire sekciju za display oglase i kreira nove ili uređuje postojeće. Svaki oglas je vezan za konkretnu zonu (header, sidebar, in-feed, mobile). Detalji o DisplayAd entitetu → **Ch.06, sekcija 6.3**.2.

**Acceptance criteria:**

- [ ] Staff može kreirati novi display oglas popunjavanjem: naziv (interni), banner slika (URL), destination URL, zona, sortOrder (prioritet)
- [ ] Opciona polja: startDate, endDate (ako nisu popunjena — oglas je aktivan odmah i dok se ručno ne isključi)
- [ ] Staff može uređivati sve atribute postojećeg oglasa
- [ ] Staff može obrisati oglas — brisanje je trajno
- [ ] Staff može uključiti/isključiti oglas toggle-om (isActive)
- [ ] Lista oglasa prikazuje: naziv, zona, status (aktivan/neaktivan), impressions, clicks, datumski okvir
- [ ] Lista podržava filtriranje po zoni i statusu (aktivan/neaktivan)
- [ ] Validacija: bannerUrl i targetUrl moraju biti validni URL-ovi, sortOrder mora biti pozitivan broj, naziv obavezan

**Backend Scope:**

- `POST /api/admin/display-ads` — prima {name, bannerUrl, targetUrl, zoneId, sortOrder, isActive, startDate?, endDate?}, vraća kreirani DisplayAd
- `PUT /api/admin/display-ads/{id}` — prima iste atribute, vraća ažurirani DisplayAd
- `DELETE /api/admin/display-ads/{id}` — briše oglas, vraća 204
- `GET /api/admin/display-ads` — lista svih oglasa sa filtrima (zoneId?, isActive?), paginirana
- `GET /api/admin/display-ads/{id}` — detalji pojedinačnog oglasa
- Validacija: URL format za bannerUrl i targetUrl, sortOrder > 0, name obavezan, zoneId mora postojati u konfiguraciji
- Side effects: nema — oglas se samo kreira/ažurira/briše u bazi

**Frontend Scope:**

- UI: lista oglasa sa tabelarnim prikazom (naziv, zona, aktivan/neaktivan toggle, impressions, clicks, datumski okvir), forma za kreiranje/uređivanje (sva polja iz AC-a), confirm dialog za brisanje
- Klijentska validacija: URL format za bannerUrl i targetUrl, obavezna polja (naziv, bannerUrl, targetUrl, zona, sortOrder)
- UX: toast nakon uspješnog kreiranja/uređivanja/brisanja, inline greške za validaciju, toggle za isActive bez reloada stranice

**Tehničke napomene:**

- DisplayAd entitet je tenant-specifičan — **Ch.06, sekcija 6.3**.2
- Zone su predefinisane i konfigurisane po tenantu — lista zona se dohvata sa servera ([S11-05](s11-05-upravljanje-reklamnim-zonama.md))
- Impressions i clicks se samo prikazuju u listi — logika brojanja je u zasebnoj storiji ([S11-03](s11-03-praenje-impressions-i-clicks.md))

**Testovi (MVP):**

- [ ] Kreiranje oglasa sa svim obaveznim poljima → oglas vidljiv u listi
- [ ] Uređivanje postojećeg oglasa → promjene sačuvane
- [ ] Brisanje oglasa → uklonjen iz liste
- [ ] Toggle isActive → oglas se uključuje/isključuje bez reloada
- [ ] Kreiranje sa nevalidnim URL-om → validacijska greška
- [ ] Filtriranje po zoni → prikazuju se samo oglasi za tu zonu

**Wireframe referenca:** —

**Implementacijske napomene:** Interni naziv oglasa (name) služi isključivo za Staff pregled — korisnici ga ne vide. Banner slika se referencira URL-om, ne uploaduje kroz platformu (Staff koristi externe hosting servise za slike).