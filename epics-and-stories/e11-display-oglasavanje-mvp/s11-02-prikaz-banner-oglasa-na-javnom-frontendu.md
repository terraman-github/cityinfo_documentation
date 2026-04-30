---
id: S11-02
confluence_page_id: "252739585"
title: "S11-02 — Prikaz banner oglasa na javnom frontendu"
parent_epic: E11
linear_id: "CIT2-67"
phase: MVP
journey_milestones: [J-08]
type: fullstack
---

**Naslov:** Prikaz banner oglasa na javnom frontendu

**Excerpt:** Javni frontend prikazuje banner oglase na predefinisanim pozicijama (header, sidebar, in-feed, mobile). Sistem dohvata aktivne oglase za traženu zonu, prikazuje ih po prioritetu sa round-robin rotacijom, a klik vodi na destination URL oglašivača.

**Phase:** MVP

**Journey milestones:** J-08

**User story:**

*Kao posjetilac platforme,*  
*želim vidjeti relevantne banner oglase na stranici,*  
*kako bih mogao otkriti lokalne ponude i usluge.*

**Kontekst:** Oglasi se prikazuju na predefinisanim pozicijama (zonama) na javnom frontendu. Za svaku zonu, sistem dohvata aktivne oglase čiji datumski okvir uključuje danas, sortira ih po prioritetu (sortOrder), i prikazuje onaj sa najvećim prioritetom. Ako ima više oglasa za istu zonu, rotira ih pri svakom učitavanju (round-robin). Prazna zona se ne prikazuje. Detalji o logici prikaza → **Ch.06, sekcija 6.3**.4.

**Acceptance criteria:**

- [ ] Za svaku zonu na stranici, sistem dohvata aktivne oglase iz API-ja
- [ ] Oglas se prikazuje kao klikabilna slika (banner) sa linkom na targetUrl
- [ ] Ako za zonu nema aktivnog oglasa, zona se ne prikazuje (nema placeholder-a)
- [ ] Klik na oglas otvara targetUrl u novom tabu
- [ ] Prikazuje se oglas sa najmanjim sortOrder-om (najveći prioritet); pri svakom učitavanju rotira se među oglasima iste zone
- [ ] Samo oglasi sa isActive=true i čiji datumski okvir uključuje danas (ili nemaju definisan okvir) se prikazuju
- [ ] Responsive prikaz: zone se prilagođavaju dimenzijama uređaja (desktop vs mobile)
- [ ] Zone su pozicionirane na stranicama prema konfiguraciji: Z-001 header, Z-002 sidebar, Z-003 između listinga, Z-004 mobile

**Backend Scope:**

- `GET /api/ads/zone/{zoneId}` — javni endpoint, vraća oglas za prikaz (adId, bannerUrl, targetUrl, zoneId); filtrira po isActive=true, datumskom okviru, i sortOrder
- Logika: dohvati aktivne oglase za zonu, sortiraj po sortOrder, primijeni round-robin rotaciju
- Side effects: inkrementira impressions za prikazani oglas (vidi [S11-03](s11-03-praenje-impressions-i-clicks.md))

**Frontend Scope:**

- UI: komponenta za prikaz banner-a u svakoj zoni — slika sa linkom, prilagođena dimenzijama zone (728×90 header, 300×250 sidebar, 600×100 in-feed, 320×50 mobile)
- Klijentska validacija: nema — backend odlučuje koji oglas prikazati
- UX: banner se učitava lazy (ne blokira renderovanje stranice), klik otvara novi tab, prazna zona ne zauzima prostor

**Tehničke napomene:**

- Round-robin rotacija u MVP-u može biti jednostavna: backend vraća sljedeći oglas po redu iz liste aktivnih za tu zonu
- Impression se broji pri svakom dohvatu oglasa za zonu — logika u [S11-03](s11-03-praenje-impressions-i-clicks.md)
- Zone se ne prikazuju ako API vrati prazan rezultat

**Testovi (MVP):**

- [ ] Zona sa jednim aktivnim oglasom → oglas se prikazuje
- [ ] Zona sa više aktivnih oglasa → oglasi se rotiraju pri učitavanjima
- [ ] Zona bez aktivnog oglasa → ništa se ne prikazuje, nema praznog prostora
- [ ] Oglas sa isteklim endDate → ne prikazuje se
- [ ] Oglas sa isActive=false → ne prikazuje se
- [ ] Klik na oglas → otvara targetUrl u novom tabu

**Wireframe referenca:** —

**Implementacijske napomene:** Lazy loading banner slika poboljšava performanse stranice, posebno na mobilnim uređajima. Za round-robin, najjednostavniji pristup je offset po sesiji ili po učitavanju — ne zahtijeva persistent state na klijentu.