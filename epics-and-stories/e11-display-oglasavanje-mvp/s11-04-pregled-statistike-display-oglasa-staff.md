---
id: S11-04
parent_epic: E11
linear_id: "CIT2-69"
phase: MVP
journey_milestones: [J-08]
type: fullstack
---

# S11-04 — Pregled statistike display oglasa (Staff)

**Naslov:** Pregled statistike display oglasa (Staff)

**Excerpt:** Staff može pregledati detaljnu statistiku za svaki display oglas — impressions, clicks, CTR (click-through rate) i aktivni period. Ovo je osnova za izvještavanje prema oglašivačima i evaluaciju performansi oglasnih pozicija.

**Phase:** MVP

**Journey milestones:** **J-08**

**User story:**  
Kao Staff korisnik,  
želim pregledati statistiku prikaza i klikova za svaki display oglas,  
kako bih mogao informisati oglašivače o performansama i donositi odluke o optimizaciji.

**Kontekst:** Staff pristupa statistici kroz admin panel, bilo iz liste oglasa (osnovni pregled) ili kroz detaljnu statistiku pojedinog oglasa. U MVP-u, statistika je ograničena na ukupne brojke — bez breakdown-a po danu ili po zoni (to dolazi s Naprednim Display Ads u Fazi 2). CTR se kalkuliše na klijentu ili serveru kao clicks/impressions × 100. Detalji o DisplayAd entitetu → **Ch.06, sekcija 6.3**.2.

**Acceptance criteria:**

- [ ] Staff može vidjeti statistiku za pojedinačni oglas: impressions, clicks, CTR (procenat)
- [ ] Statistika prikazuje i period aktivnosti oglasa (startDate — endDate ili "aktivan od" ako nema endDate)
- [ ] CTR se kalkuliše kao (clicks / impressions) × 100, zaokružen na 2 decimale
- [ ] Ako oglas nema impressions (novi oglas), CTR prikazuje "—" umjesto 0% ili dijeljenja nulom
- [ ] Statistika je dostupna iz liste oglasa (kolone impressions/clicks) i iz detaljnog pregleda pojedinog oglasa

**Backend Scope:**

- `GET /api/admin/display-ads/{id}/stats` — vraća {impressions, clicks, ctr, startDate, endDate, isActive, daysActive}
- Kalkulacija: ctr = impressions > 0 ? (clicks / impressions) \* 100 : null; daysActive = razlika između startDate (ili createdAt) i danas (ili endDate ako je istekao)
- Side effects: nema — read-only endpoint

**Frontend Scope:**

- UI: statistički prikaz na detail stranici oglasa — impressions, clicks, CTR sa vizuelnim indikatorom, period aktivnosti
- Klijentska validacija: nema
- UX: CTR prikazan kao procenat sa 2 decimale; "—" za oglase bez impressions-a; pregledan i čist layout bez grafova (grafovi dolaze u Fazi 2)

**Tehničke napomene:**

- U MVP-u nema vremenskih serija (impressions po danu) — samo ukupni brojevi
- Napredna analitika (breakdown po danu, po zoni, po uređaju) planirana za Napredni Display Ads u Fazi 2

**Testovi (MVP):**

- [ ] Oglas sa 1000 impressions i 50 clicks → CTR = 5.00%
- [ ] Novi oglas bez impressions → CTR prikazuje "—"
- [ ] Statistika prikazuje tačan period aktivnosti

**Wireframe referenca:** —

**Implementacijske napomene:** CTR kalkulacija može živjeti na backendu (endpoint vraća gotov CTR) ili na frontendu (klijent dijeli clicks/impressions) — za MVP je svejedno, ali backend pristup je čistiji jer centralizira logiku.