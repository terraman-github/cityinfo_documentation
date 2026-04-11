# S13-07 — Staff panel shell i navigacija

**Naslov:** Staff panel shell i navigacija

**Excerpt:** Admin panel treba imati funkcionalan shell — layout, sidebar navigaciju, tenant switcher i prikaz ulogovanog korisnika — prije nego što se počnu implementirati konkretne funkcionalnosti poput moderacije ili upravljanja korisnicima. Ova storija postavlja "kostur" admin panela.

**Phase:** MVP

**Journey milestones:** J-08

**User story:**  
Kao moderator,  
želim imati pregledan admin panel sa jasnom navigacijom,  
kako bih mogao brzo pristupiti moderacijskom queue-u, korisnicima i drugim alatima bez lutanja.

**Kontekst:** Staff panel živi na [admin.cityinfo.ba](http://admin.cityinfo.ba) kao odvojen SvelteKit projekat. Navigacija se razlikuje po ulogama — moderator vidi moderacijske alate, operator vidi finansijske izvještaje, local\_admin vidi sve + sistemske postavke. Detalji o matrici ovlasti → Ch.03, sekcija 3.5. Staff panel je tehnički postavljen u E14 (S14-03), ova storija gradi na tom temelju.

**Acceptance criteria:**

- [ ] Admin panel ima persistent sidebar navigaciju sa sekcijama prema ulozi ulogovanog Staff-a
- [ ] Moderator vidi: Dashboard, Moderation Queue, Korisnici, Komunikacija
- [ ] Operator vidi: Dashboard, Finansije, Promocije, Komunikacija
- [ ] Local\_admin vidi sve sekcije + Postavke, Staff upravljanje
- [ ] Navigacija se dinamički prilagođava ulozi — nema prikaza stavki kojima Staff nema pristup
- [ ] Header prikazuje ime ulogovanog Staff-a, ulogu i aktivni tenant
- [ ] Tenant switcher omogućava prebacivanje između tenanta iz `tenantAccess` liste (prikazuje se samo ako Staff ima pristup više tenanta)
- [ ] Prebacivanje tenanta osvježava podatke u svim prikazima
- [ ] Dashboard stranica prikazuje placeholder sadržaj (konkretne widgete implementiraju drugi epici)
- [ ] Shell je responzivan — sidebar se collapse-uje na manjim ekranima
- [ ] Logout dugme je uvijek dostupno u headeru

**Frontend Scope:**

- UI: sidebar layout sa ikonama i labelama; header sa Staff info + tenant switcher + logout; placeholder dashboard
- Klijentska validacija: N/A (čist UI)
- UX: active state na trenutnoj navigaciji; smooth transition pri prebacivanju tenanta; collapsible sidebar

**Tehničke napomene:**

- Navigacijske stavke se generišu na osnovu `role` ulogovanog Staff-a — nije hardcode po stranicama
- Tenant switcher koristi `tenantAccess` listu iz profila Staff-a
- Placeholder stranice za sekcije koje još nemaju implementaciju (Moderation Queue, Korisnici, itd.) — prikazuju "Coming soon" ili prazan state
- Ova storija ne uključuje backend — koristi podatke iz Staff profila koji je već dostupan nakon logina (S13-01)

**Testovi (MVP):**

- [ ] Moderator vidi samo moderatorske navigacijske stavke
- [ ] Local\_admin vidi sve navigacijske stavke
- [ ] Tenant switcher se prikazuje samo za Staff sa pristupom više tenanta
- [ ] Prebacivanje tenanta mijenja kontekst podataka
- [ ] Sidebar se collapse-uje na mobilnom/tablet prikazu

**Wireframe referenca:** —

**Implementacijske napomene:**

- Flowbite (Tailwind) ima gotove sidebar/layout komponente — razmotriti kao polaznu tačku
- Navigacijski config kao JSON objekat mapiran na role — olakšava dodavanje novih stavki kasnije