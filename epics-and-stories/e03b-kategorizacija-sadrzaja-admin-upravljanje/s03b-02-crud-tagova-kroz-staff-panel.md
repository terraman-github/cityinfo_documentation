---
id: S03b-02
parent_epic: E03b
linear_id: ""
phase: MVP
journey_milestones: [J-08]
type: fullstack
---

# S03b-02 — CRUD tagova kroz Staff panel

**Naslov:** CRUD tagova kroz Staff panel

**Excerpt:** Moderatori sa `can_manage_tags` permisijom (ili local\_admin) mogu kreirati nove tagove, uređivati postojeće, deaktivirati ih, i brisati — odvojeno za EventTags i PlaceTags. Tagovi su bliži svakodnevnom radu sa sadržajem od kategorija, pa je upravljanje njima namjerno delegirano na moderatorski nivo.

**Phase:** MVP

**Journey milestones:** J-08

**User story:**  
Kao moderator sa `can_manage_tags` permisijom,  
želim upravljati tagovima kroz Staff panel,  
kako bih mogao dodati nove tagove kad korisnici izraze potrebu ili ukloniti zastarjele bez developer pomoći.

**Kontekst:** Moderator pristupa Staff panelu ([admin.cityinfo.ba](http://admin.cityinfo.ba)) i otvara sekciju za upravljanje tagovima. EventTags i PlaceTags su odvojeni sistemi — moderator radi sa jednim tipom u datom trenutku. Inicijalni tagovi su postavljeni u E03a. Pravila za tagove definisana u Ch.04, sekcija 4.5 — slug je PK, brisanje uklanja tag sa listinga (NULL), deaktivacija skriva tag iz odabira ali zadržava vezu.

**Acceptance criteria:**

- [ ] Moderator može kreirati novi tag sa atributima: tagSlug, tagName, tagNameAlt, tagIcon, orderIndex
- [ ] tagSlug se auto-generiše iz tagName, ali je prilagodljiv prije prvog snimanja
- [ ] Moderator može editovati sve atribute taga (uključujući slug — za razliku od kategorija, tag slug se može mijenjati jer se čuva denormalizovano u listingu)
- [ ] Moderator može deaktivirati tag (`isActive = false`) — tag se ne prikazuje pri kreiranju/editovanju listinga, ali postojeći listinzi zadržavaju tag
- [ ] Moderator može reaktivirati tag (`isActive = true`)
- [ ] Moderator može obrisati tag — listinzi koji su koristili obrisani tag ostaju bez tog taga (slug postaje NULL na listingu)
- [ ] Brisanje taga prikazuje confirmation dialog sa brojem pogođenih listinga
- [ ] Lista tagova prikazuje: slug, naziv, ikonu, status (active/inactive), broj listinga koji koriste tag, i redoslijed (orderIndex)
- [ ] Validacija: tagSlug mora biti jedinstven unutar tabele (EventTags ili PlaceTags)
- [ ] Promjene su odvojene za EventTags i PlaceTags — moderator jasno vidi sa kojim tipom radi

**Backend Scope:**

- `POST /event-tags` — prima {tagSlug, tagName, tagNameAlt, tagIcon, orderIndex}, vraća kreiran tag
- `PUT /event-tags/{slug}` — prima izmjene, vraća ažuriran tag
- `DELETE /event-tags/{slug}` — briše tag, ažurira pogođene listinge (NULL-uje slug reference)
- Isti endpoint-i za `/place-tags`
- Validacija: slug unikatnost, obavezna polja
- Side effects: brisanje taga → ažuriranje `primaryTagSlug` i `secondaryTagSlug` na pogođenim listinzima

**Frontend Scope:**

- UI: Lista tagova sa kolonama: slug, naziv, ikona, status, broj listinga, orderIndex, akcije
- UI: Forma za kreiranje/editovanje sa svim atributima, emoji picker za ikonu
- Klijentska validacija: obavezna polja (tagSlug, tagName), slug format
- UX: Drag-and-drop ili input za promjenu orderIndex-a
- UX: Delete prikazuje confirmation sa porukom "X listinga će izgubiti ovaj tag"
- UX: Tab ili toggle za prebacivanje između EventTags i PlaceTags

**Tehničke napomene:**

- Za razliku od kategorija, tag slug se **može mijenjati** jer se čuva denormalizovano u listingu — pri promjeni slug-a treba ažurirati sve pogođene listinge.
- Brisanje taga je sigurna operacija — ne utiče na vidljivost listinga, samo uklanja tag oznaku.

**Testovi (MVP):**

- [ ] Kreiranje taga — pojavljuje se u listi i dostupan je za odabir na listingu
- [ ] Pokušaj kreiranja taga sa duplikatnim slug-om — prikazuje grešku
- [ ] Editovanje naziva i ikone taga — promjene vidljive odmah
- [ ] Deaktivacija taga — ne pojavljuje se pri kreiranju listinga, ali postojeći listinzi prikazuju tag
- [ ] Brisanje taga koji koriste 3 listinga — slug postaje NULL na sva tri listinga
- [ ] Confirmation dialog pri brisanju prikazuje tačan broj pogođenih listinga

**Wireframe referenca:** —

**Implementacijske napomene:** Promjena slug-a na postojećem tagu je batch operacija na listinzima — razmotriti da li se radi sinhrono (mali broj pogođenih) ili asinhrono (velik broj). Za MVP, sinhrono je dovoljno jer se ne očekuje veliki obim.