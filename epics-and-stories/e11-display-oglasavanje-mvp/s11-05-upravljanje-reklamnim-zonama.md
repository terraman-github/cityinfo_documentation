---
id: S11-05
confluence_page_id: "251789341"
parent_epic: E11
linear_id: "CIT2-70"
phase: MVP
journey_milestones: [J-08]
type: fullstack
---

**Naslov:** Upravljanje reklamnim zonama

**Excerpt:** Reklamne zone definišu pozicije na stranici gdje se prikazuju banner oglasi. Zone su predefinisane i konfigurisane po tenantu — Staff ih može pregledati i vidjeti koje su dostupne, a sistem ih koristi za mapiranje oglasa na konkretne pozicije.

**Phase:** MVP

**Journey milestones:** J-08

**User story:**  
Kao Staff korisnik,

želim vidjeti listu dostupnih reklamnih zona sa njihovim karakteristikama,

kako bih znao na koje pozicije mogu dodijeliti oglase.

**Kontekst:** Reklamne zone su predefinisane u sistemu i konfigurisane po tenantu. MVP koristi 4 zone: Z-001 (Header Banner, 728×90), Z-002 (Sidebar, 300×250), Z-003 (In-Feed, 600×100), Z-004 (Mobile Banner, 320×50). Zone se mogu dodavati ili mijenjati bez promjene koda — konfigurisane su na nivou tenanta. Detalji o zonama → **Ch.06, sekcija 6.3**.3.

**Acceptance criteria:**

- [ ] Sistem ima predefinisane zone za MVP: Z-001 (Header), Z-002 (Sidebar), Z-003 (In-Feed), Z-004 (Mobile)
- [ ] Staff može vidjeti listu zona sa: ID, naziv, lokacija na stranici, dimenzije, tip
- [ ] Pri kreiranju oglasa ([S11-01](s11-01-kreiranje-i-upravljanje-display-oglasima-staff.md)), Staff bira zonu iz dropdown-a sa dostupnim zonama
- [ ] API vraća listu zona za trenutni tenant
- [ ] Seed data uključuje inicijalne zone za MVP tenant

**Backend Scope:**

- `GET /api/ad-zones` — javni endpoint, vraća listu zona za trenutni tenant {zoneId, name, location, dimensions, type}
- Seed data: 4 predefinisane zone za MVP tenant (Z-001 do Z-004 prema **Ch.06, sekcija 6.3**.3)
- Side effects: nema — read-only

**Frontend Scope:**

- UI: dropdown za izbor zone u formi za kreiranje/uređivanje oglasa ([S11-01](s11-01-kreiranje-i-upravljanje-display-oglasima-staff.md)); opciono — lista zona u admin panelu za pregled
- Klijentska validacija: zona mora biti odabrana pri kreiranju oglasa
- UX: dropdown prikazuje naziv i dimenzije zone za lakši odabir

**Tehničke napomene:**

- Zone su konfigurisane na nivou tenanta — u MVP-u sa jednim tenantom, to je praktično globalna konfiguracija
- Dodavanje novih zona ne zahtijeva promjenu koda — samo novi zapis u konfiguraciji
- U MVP-u Staff ne može kreirati/brisati zone — samo ih pregledati; upravljanje zonama može doći u budućoj fazi ako bude potrebe

**Testovi (MVP):**

- [ ] API vraća 4 predefinisane zone za MVP tenant
- [ ] Dropdown u formi za oglas prikazuje sve dostupne zone
- [ ] Kreiranje oglasa sa odabranom zonom → oglas je vezan za tu zonu

**Wireframe referenca:** —

**Implementacijske napomene:** Zone se mogu čuvati u bazi ili u konfiguracijskom fajlu — za MVP je svejedno jer ih ima malo i rijetko se mijenjaju. Baza je fleksibilnija za buduće proširenje.