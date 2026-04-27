---
id: S04-07
parent_epic: E04
linear_id: ""
phase: MVP
journey_milestones: [J-04]
type: frontend-only
---

# S04-07 — Responsive dizajn i mobile-first layout

**Naslov:** Responsive dizajn i mobile-first layout

**Excerpt:** CityInfo je mobile-first platforma — većina korisnika dolazi sa mobilnih uređaja. Ova storija pokriva responsive layout sa tri breakpointa, mobile-specifične elemente (sticky header, bottom nav, FAB), i prilagodbu svih komponenti za touch interakciju.

**Phase:** MVP

**Journey milestones:** **J-04**

**User story:**  
Kao korisnik na mobilnom uređaju,  
želim da platforma bude prilagođena mom ekranu i touch interakciji,  
kako bih mogao udobno koristiti sve funkcionalnosti bez zumiranja ili horizontalnog scrolla.

**Kontekst:** Mobile-first pristup je definisan u **Ch.02, sekcija 2.5**. Tri breakpointa: telefon (< 640px), tablet (640–1024px), desktop (> 1024px). Mobile-specifični elementi uključuju sticky header, bottom navigation bar, floating action button za kreiranje sadržaja, i filtere u drawer/modal formatu. Ova storija je horizontalna — utiče na sve ostale storije iz E04 i [E05](../e05-prikaz-sadrzaja-i-korisnicke-interakcije.md).

**Acceptance criteria:**

- [ ] Layout se prilagođava na tri breakpointa: telefon (jedna kolona), tablet (dvije kolone), desktop (višekolonski grid sa sidebar navigacijom)
- [ ] Na mobilnom: sticky header sa search barom koji ostaje vidljiv pri scrollu
- [ ] Na mobilnom: bottom navigation bar za brzi pristup ključnim sekcijama (Početna, Pretraga, Kreiraj, Favoriti, Profil)
- [ ] Na mobilnom: floating action button (FAB) za kreiranje novog sadržaja (samo za registrovane korisnike)
- [ ] Na mobilnom: filteri se otvaraju u drawer/modal formatu, ne u sidebar-u
- [ ] Kartice listinga se prilagođavaju širini ekrana — full-width na telefonu, u gridu na tabletu/desktopu
- [ ] Touch-friendly elementi — dovoljno veliki touch target-i (min 44x44px), bez hover-only interakcija
- [ ] Slike su responsive — učitavaju se odgovarajuće verzije (thumbnail za liste, medium za detail)
- [ ] Nema horizontalnog scrolla na bilo kojem breakpointu
- [ ] Font veličine i spacing su prilagođeni za čitljivost na malim ekranima

**Frontend Scope:**

- UI: Responsive grid system (Tailwind breakpoints: sm, md, lg)
- UI: Sticky header komponenta
- UI: Bottom navigation bar komponenta (mobile only)
- UI: FAB komponenta (mobile only, registrovani korisnici)
- UI: Filter drawer/modal za mobilni
- UX: Smooth tranzicije između breakpointa
- UX: Lazy loading slika sa placeholder-om
- UX: Pull-to-refresh na mobilnom (opciono za MVP)

**Tehničke napomene:**

- Ovo je frontend-only storija — nema Backend Scope.
- Tailwind CSS + Flowbite već podržavaju responsive dizajn — koristiti postojeće breakpointe.
- Bottom navigation i FAB su isključivo mobile elementi — ne prikazuju se na desktopu.

**Testovi (MVP):**

- [ ] Na telefonu (< 640px): jedna kolona kartica, sticky header, bottom nav, FAB vidljiv za registrovane korisnike
- [ ] Na tabletu (640–1024px): dvije kolone, kompaktnija navigacija
- [ ] Na desktopu (> 1024px): višekolonski grid, sidebar navigacija, nema bottom nav-a ni FAB-a
- [ ] Nema horizontalnog scrolla na iPhone SE (320px širina)
- [ ] Touch target-i su dovoljno veliki — nema slučajnih klikova na bliske elemente

**Wireframe referenca:** —

**Implementacijske napomene:** Testiranje na stvarnim uređajima (ili emulatorima) je kritično — samo browser resize nije dovoljan jer touch interakcija i viewport ponašanje se razlikuju. Chrome DevTools device emulator je dobar početak.