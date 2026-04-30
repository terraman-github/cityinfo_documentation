---
id: S05-02
confluence_page_id: "252149761"
parent_epic: E05
linear_id: "CIT2-35"
phase: MVP
journey_milestones: [J-04, J-05]
type: fullstack
---

**Naslov:** Detaljna stranica listinga

**Excerpt:** Kad korisnik klikne na karticu, otvara se puna stranica sa galerijom slika, kompletnim opisom, mapom, kontakt informacijama, i CTA elementima. Za evente se prikazuju datum/vrijeme i child eventi (ako je parent), za mjesta adresa i povezani eventi. Stranica je prilagođena za oba jezika tenanta.

**Phase:** MVP

**Journey milestones:** J-04, **J-05**

**User story:**  
Kao posjetilac,

želim vidjeti sve detalje listinga na jednoj stranici,

kako bih mogao donijeti odluku da li ću posjetiti to mjesto ili prisustvovati tom događaju.

**Kontekst:** Korisnik je kliknuo na karticu iz liste rezultata, naslovne, ili related contenta. Detaljna stranica prikazuje sve dostupne informacije o listingu. Razlikuje se za Event i Place — Event ima datum/vrijeme i hijerarhiju child evenata, Place ima adresu i povezane evente vlasnika. Elementi stranice definirani u **Ch.02, sekcija 2.3**.

**Acceptance criteria:**

- [ ] Stranica prikazuje galeriju slika (swipeable carousel na mobilnom, grid/carousel na desktopu)
- [ ] Puni opis listinga sa HTML formatiranjem
- [ ] Svi tekstualni sadržaji se prikazuju na jeziku koji je korisnik odabrao (name/nameAlt, description/descriptionAlt, excerpt/excerptAlt), sa fallback-om na primarni
- [ ] Primarna kategorija sa bojom i nazivom sektora
- [ ] Tagovi (ako postoje)
- [ ] Verifikacioni badge "✓ Potvrđen vlasnik" (ako je verificiran)
- [ ] Vanjski link (`listingUrl`) — otvara se u novom tabu
- [ ] Broj lajkova (`totalAppreciations`)
- [ ] CTA elementi: lajkaj, spremi u favorite, podijeli (pokriveno detaljnije u [S05-03](s05-03-lajkovi-za-registrovane-korisnike-i-visitore.md)/04/05)
- [ ] **Za Event:** startDateTime i endDateTime u lokalizovanom formatu; ako je parent event (`hasChildren = true`), prikazuje listu child evenata
- [ ] **Za Event:** lokacija — ako je povezan sa Place-om, prikazuje ime mjesta kao link; ako je ručna adresa, prikazuje adresu sa mapom
- [ ] **Za Place:** adresa sa interaktivnom Google mapom i navigacijskim linkom ("Navigiraj")
- [ ] **Za Place:** lista nadolazećih evenata vlasnika na tom mjestu (ako ih ima)
- [ ] Stranica ima ispravne Open Graph meta tagove za preview pri dijeljenju (naslov, slika, opis)
- [ ] Ako listing više nije dostupan (`isPublic = false`), prikazuje se poruka "Ovaj sadržaj više nije dostupan"

**Backend Scope:**

- `GET /events/{id}` — vraća kompletne podatke eventa uključujući child evente (ako je parent)
- `GET /places/{id}` — vraća kompletne podatke mjesta
- `GET /places/{id}/events` — vraća nadolazeće evente na tom mjestu
- Response uključuje sve atribute potrebne za prikaz + user-specific podatke (da li je korisnik lajkao, da li je u favoritima)

**Frontend Scope:**

- UI: Galerija slika (carousel/lightbox)
- UI: Sekcija sa opisom, kategorijom, tagovima, verifikacijom
- UI: Google Maps embed za lokaciju
- UI: CTA bar (lajk, favorit, share, navigiraj)
- UI: Child eventi sekcija za parent evente
- UI: Nadolazeći eventi sekcija za Place
- UX: Smooth scroll između sekcija
- UX: Responsive — na mobilnom elementi su vertikalno poredani, na desktopu sidebar sa mapom/CTA

**Tehničke napomene:**

- Open Graph meta tagovi se renderaju server-side (SSR/SSG) jer social media crawleri ne izvršavaju JavaScript.
- Google Maps embed se lazy-loada — ne blokira učitavanje stranice.
- Child eventi se prikazuju kao mini-kartice sa datumom i nazivom.

**Testovi (MVP):**

- [ ] Event detaljna stranica prikazuje datum, lokaciju, i opis
- [ ] Parent event prikazuje listu child evenata
- [ ] Place detaljna stranica prikazuje adresu sa mapom i nadolazeće evente
- [ ] Prebacivanje jezika — svi tekstovi se mijenjaju na sekundarni jezik (gdje postoji prevod)
- [ ] Dijeljenje linka na social media prikazuje ispravan preview (naslov + slika)
- [ ] Listing koji nije javan prikazuje poruku "Ovaj sadržaj više nije dostupan"

**Wireframe referenca:** —

**Implementacijske napomene:** Za galeriju slika razmotriti lightweight biblioteku (npr. Swiper ili Splide) koja podržava touch swipe i lazy loading. Lightbox za full-screen pregled slika.