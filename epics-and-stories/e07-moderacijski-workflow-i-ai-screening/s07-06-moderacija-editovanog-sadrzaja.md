# S07-06 — Moderacija editovanog sadržaja

**Naslov:** Moderacija editovanog sadržaja

**Excerpt:** Kada korisnik edituje aktivan listing, ponašanje u moderacijskom queue-u zavisi od Trust Tier-a. Za Tier 0/1, editovani listing se skriva i ponovo čeka odobrenje. Za Tier 2+, listing ostaje vidljiv ali ulazi u queue za naknadni pregled. Ovo sprečava zaobilaženje kontrole kvaliteta kroz editovanje.

**Phase:** MVP

**Journey milestones:** J-03

**User story:**  
Kao sistem,  
želim primijeniti odgovarajuću moderaciju kada korisnik edituje aktivan listing,  
kako bi se spriječilo zaobilaženje kontrole kvaliteta kroz izmjenu sadržaja nakon inicijalnog odobrenja.

**Kontekst:** Korisnik može editovati aktivan listing u bilo kojem trenutku. Bez ovog mehanizma, korisnik na Tier 1 bi mogao dobiti odobrenje za kvalitetan listing, pa ga zatim izmijeniti u potpuno neprikladan sadržaj koji bi bio vidljiv bez ponovnog pregleda. Ponašanje se razlikuje po tier-u da bi se balansirala sigurnost i korisničko iskustvo — Verified Partner ne bi trebao čekati odobrenje za ispravku radnog vremena. Detalji → Ch.05, sekcija 5.2.5.

**Acceptance criteria:**

- [ ] Tier 0/1 — editovani listing prelazi u `listingStatus = in_review` i skriva se iz javnog prikaza
- [ ] Tier 0/1 — korisnik dobija poruku da će listing ponovo postati vidljiv nakon odobrenja
- [ ] Tier 2+ — editovani listing ostaje vidljiv javno i prelazi u `listingStatus = published_under_review`
- [ ] Tier 2+ — sistem kreira novu stavku u post-moderacijskom queue-u za naknadni pregled
- [ ] Tier 2+ — sampling logika se primjenjuje kao za novo submitovani sadržaj (→ S07-05)
- [ ] AI screening se pokreće ponovo na editovanom sadržaju (novi scan)
- [ ] AI blocking važi i za editovani sadržaj — ako AI detektuje ekstreman rizik, listing prelazi u `hidden_by_system` bez obzira na tier
- [ ] Edit se bilježi u audit log sa informacijom šta je promijenjeno

**Backend Scope:**

- Logika u listing edit endpoint-u: provjera Trust Tier vlasnika, primjena odgovarajućeg moderacijskog flow-a
- Za Tier 0/1: `listingStatus` prelazi u `in_review`, listing skriven iz javnog prikaza, kreiranje queue stavke
- Za Tier 2+: `listingStatus` prelazi u `published_under_review`, kreiranje post-mod queue stavke (sa sampling logikom), listing ostaje vidljiv
- Pokretanje AI re-screening-a na editovanom sadržaju
- Audit log: bilježenje edita sa before/after za promijenjene atribute

**Frontend Scope:**

- Korisnik Tier 0/1: upozorenje prije edita ("Izmjena će poslati listing na ponovni pregled i privremeno ga sakriti")
- Korisnik Tier 2+: informacija da će edit biti naknadno pregledan (ali listing ostaje vidljiv)
- Moderator: u queue-u se jasno vidi da je stavka "edit aktivnog listinga" (ne novo submitovanje), sa diff prikazom promjena

**Tehničke napomene:**

- Diff prikaz promjena u moderatorskom queue-u je jako koristan ali nije kritičan za MVP — moderator može pregledati cijeli sadržaj. Ali ako je izvedivo, značajno ubrzava pregled.
- AI re-screening treba analizirati cijeli sadržaj, ne samo izmijenjene dijelove — jer kontekst može promijeniti značenje.
- Ova storija se nadovezuje na listing edit iz E02 — E02 definira mehaniku edita, E07 dodaje moderacijski sloj.

**Testovi (MVP):**

- [ ] Tier 1 korisnik edituje aktivan listing → `listingStatus = in_review`, listing skriven
- [ ] Tier 1 korisnik — poruka da listing čeka ponovni pregled
- [ ] Tier 2 korisnik edituje aktivan listing → `listingStatus = published_under_review`, listing ostaje vidljiv
- [ ] Tier 3 korisnik edituje listing → sampling logika se primjenjuje (možda ne uđe u queue)
- [ ] AI screening se pokreće ponovo na editovanom sadržaju
- [ ] AI blocking na editovanom sadržaju → `listingStatus = hidden_by_system` bez obzira na tier

**Wireframe referenca:** —

**Implementacijske napomene:**

- "Minor edit" koncept (npr. ispravka tipfeler-a) može biti razmatran u budućnosti da se izbjegne nepotrebna re-moderacija — ali za MVP, svaki edit ide kroz isti flow.