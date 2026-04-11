# S02-04 — Event hijerarhija — kreiranje i upravljanje child eventima

<a id="s02-04-event-hijerarhija-kreiranje-i-upravljanje-child-eventima"></a>

# S02-04 — Event hijerarhija — kreiranje i upravljanje child eventima

**Naslov:** Event hijerarhija — kreiranje i upravljanje child eventima

**Excerpt:** Festivali, konferencije i višednevni događaji mogu imati pod-događaje (child events). Ova storija pokriva kreiranje child event-a unutar parent-a, pravila hijerarhije (max 2 nivoa), i kaskadno brisanje.

**Phase:** MVP

**Journey milestones:** J-02

**User story:**  
Kao organizator festivala,  
želim kreirati pod-događaje (koncerte, radionice) unutar svog festivala,  
kako bi svaki program imao vlastiti listing sa detaljima i opcijom za zasebnu promociju.

**Kontekst:** Korisnik ima kreiran parent Event (S02-01). Parent/child hijerarhija je ograničena na dva nivoa — child ne može imati vlastite child-ove. Samo vlasnik parent-a može kreirati child evente. Detalji o hijerarhiji → Ch.04, sekcija 4.2 (Hijerarhija događaja).

**Acceptance criteria:**

- [ ] Na stranici parent Event-a postoji opcija "Dodaj pod-događaj"
- [ ] Child event se kreira kroz istu formu kao obični event, sa dodatnim ograničenjima
- [ ] `parentEventId` se automatski postavlja na ID parent Event-a
- [ ] `hasChildren` flag na parent-u se automatski postavlja na `true` kada dobije prvi child
- [ ] Child event ne može imati `startDateTime` izvan vremenskog okvira parent-a
- [ ] Child event ne može sam biti parent (`hasChildren` i `parentEventId` su međusobno isključivi)
- [ ] Samo vlasnik parent Event-a može kreirati child evente
- [ ] Parent Event prikazuje listu svojih child evenata
- [ ] Brisanje parent-a: child-ovi sa `wasEverActive = false` prelaze u `removed` (`user_delete`); child-ovi sa `wasEverActive = true` prelaze u `hidden_by_owner`
- [ ] Brisanje zadnjeg child-a automatski postavlja `hasChildren = false` na parent-u

**Backend Scope:**

- `POST /events/{id}/children` — prima iste podatke kao kreiranje eventa, dodatno validira hijerarhiju
- `GET /events/{id}/children` — vraća listu child evenata
- Validacija: parent mora postojati, korisnik mora biti vlasnik parent-a, `startDateTime`/`endDateTime` child-a unutar parent-ovog okvira, parent ne smije sam biti child
- Side effects: postavlja `hasChildren = true` na parent-u; pri brisanju parent-a kaskadno procesira child evente prema `wasEverActive` logici; pri brisanju zadnjeg child-a resetuje `hasChildren`

**Frontend Scope:**

- UI: dugme "Dodaj pod-događaj" na parent Event stranici; lista child evenata na parent detaljima; forma za kreiranje child-a (ista kao Event forma, sa ograničenim date pickerom)
- Klijentska validacija: datumi unutar parent-ovog okvira
- UX: date picker ograničen na raspon parent-a; oznaka na karticama parent-a "Festival — više događaja"

**Tehničke napomene:**

- Kaskadno brisanje child evenata treba obraditi u jednoj transakciji
- Child event nasljeđuje lokaciju parent-a kao default, ali može imati vlastitu

**Testovi (MVP):**

- [ ] Happy path: kreiranje child Event-a unutar parent-a → child kreiran, `hasChildren = true`
- [ ] Child sa datumima van okvira parent-a → validacijska greška
- [ ] Pokušaj kreiranja child-a unutar child-a (treći nivo) → greška
- [ ] Pokušaj kreiranja child-a na tuđem parent Event-u → greška
- [ ] Brisanje parent-a sa child-ovima (`wasEverActive = true`) → child-ovi prelaze u `hidden_by_owner`
- [ ] Brisanje parent-a sa child-ovima (`wasEverActive = false`) → child-ovi prelaze u `removed` (`user_delete`)
- [ ] Brisanje zadnjeg child-a → `hasChildren` na parent-u postaje `false`
- [ ] Lista child evenata na parent stranici prikazuje ispravne podatke

**Wireframe referenca:** —

**Implementacijske napomene:**

- Razmotriti da child event automatski naslijedi kategoriju parent-a kao default (ali da korisnik može promijeniti)
- UI za listu child-ova može koristiti isti card format kao i glavni listing grid