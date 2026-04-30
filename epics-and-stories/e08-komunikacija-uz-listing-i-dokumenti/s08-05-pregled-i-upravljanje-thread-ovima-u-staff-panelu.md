---
id: S08-05
confluence_page_id: "252313630"
parent_epic: E08
linear_id: "CIT2-55"
phase: MVP
journey_milestones: [J-03]
type: fullstack
---

**Naslov:** Pregled i upravljanje thread-ovima u Staff panelu

**Excerpt:** Moderatori trebaju pregled svih aktivnih thread-ova, mogućnost filtriranja po statusu, i brz pristup thread-u iz moderacijskog queue-a. Ova storija pokriva Staff UI za message sistem — listu thread-ova, prikaz poruka, i ažuriranje thread statusa.

**Phase:** MVP

**Journey milestones:** J-03

**User story:**  
Kao moderator,

želim imati pregled svih message thread-ova sa filterima po statusu i dodijeljenom moderatoru,

kako bih mogao efikasno pratiti komunikaciju sa vlasnicima listinga i ne propustiti čekajuće odgovore.

**Kontekst:** Moderator koristi Staff panel za upravljanje komunikacijom. Pored pristupa thread-u direktno iz listing pregleda (kao dio moderacijskog workflow-a), moderator treba i centraliziran pregled svih thread-ova — posebno onih u statusu `waiting_moderator` koji čekaju njegov odgovor. Ova storija pokriva Staff-specifičan UI i endpoint za upravljanje thread-ovima. Detalji o thread modelu → **Ch.07**, sekcije 7.1.3–7.1.5; PATCH endpoint za thread → **Ch.07, sekcija 7.4**.1.

**Acceptance criteria:**

- [ ] Staff panel ima sekciju "Poruke" sa listom thread-ova (paginirana)
- [ ] Lista thread-ova prikazuje: listing naziv, thread status, assignedTo moderator, `lastMessageAt`, `messageCount`
- [ ] Filtriranje po statusu: `idle`, `waiting_owner`, `waiting_moderator`, ili svi
- [ ] Filtriranje po dodijeljenom moderatoru: "moji thread-ovi" vs "svi"
- [ ] Sortiranje po `lastMessageAt` (default: najnoviji prvo)
- [ ] Klik na thread otvara prikaz poruka sa mogućnošću slanja odgovora
- [ ] Moderator može ručno postaviti thread status u `idle` (tema riješena) kroz PATCH endpoint
- [ ] Moderator može preuzeti (assign) thread na sebe ili ga dodijeliti drugom moderatoru
- [ ] Thread-ovi za obrisane listinge su vizualno označeni i ne dozvoljavaju slanje novih poruka

**Backend Scope:**

- `GET /threads` — lista thread-ova sa filterima (`status`, `assignedTo`, paginacija, sortiranje)
- `GET /threads/{threadId}` — detalji thread-a
- `GET /threads/{threadId}/messages` — poruke u thread-u (paginirano, kronološki)
- `PATCH /threads/{threadId}` — ažuriranje thread-a: promjena `status` (npr. u `idle`), promjena `assignedTo`
- Validacija za PATCH: validni statusi, moderator postoji

**Frontend Scope:**

- UI: Tabela/lista thread-ova sa kolonama: listing, status (badge), assigned moderator, zadnja poruka, broj poruka
- UI: Filter bar sa dropdown za status i toggle "Moji / Svi"
- UI: Thread detail view — lista poruka kronološki + textarea za odgovor (reuse iz [S08-02](s08-02-slanje-poruke-moderatora-vlasniku-listinga.md))
- UI: Akcije na thread-u: "Označi kao riješeno" (→ idle), "Preuzmi" (→ assign to me), "Dodijeli" (→ assign to other)
- UX: Badge/indikator na "Poruke" navigaciji koji pokazuje broj thread-ova u `waiting_moderator` statusu

**Tehničke napomene:**

- Lista thread-ova je Staff-only endpoint — korisnici ne vide tuđe thread-ove
- `waiting_moderator` count za badge se može dohvatiti kao agregatni upit ili kao dio thread liste

**Testovi (MVP):**

- [ ] Lista thread-ova prikazuje ispravne podatke sa paginacijom
- [ ] Filter po statusu `waiting_moderator` vraća samo thread-ove koji čekaju moderatora
- [ ] Filter "moji thread-ovi" vraća samo thread-ove assignovane ulogovanom moderatoru
- [ ] PATCH thread-a u `idle` status uspješno mijenja status
- [ ] PATCH thread-a sa novim `assignedTo` uspješno mijenja dodijeljenog moderatora
- [ ] Thread za obrisani listing ne dozvoljava slanje poruka

**Wireframe referenca:** —

**Implementacijske napomene:** Thread lista se dobro uklapa kao tab unutar postojeće Staff navigacije, uz moderacijski queue. Badge sa brojem `waiting_moderator` thread-ova daje moderatoru brz pregled koliko komunikacija čeka odgovor.