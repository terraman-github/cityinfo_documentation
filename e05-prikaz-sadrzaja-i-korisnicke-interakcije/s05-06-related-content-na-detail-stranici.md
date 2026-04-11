# S05-06 — Related content na detail stranici

**Naslov:** Related content na detail stranici

**Excerpt:** Na dnu svake detail stranice prikazuju se povezani sadržaji — do 6 stavki koje pomažu korisniku da otkrije još relevantnog sadržaja bez povratka na pretragu. Logika odabira se razlikuje za Event i Place i prioritizira relevantnost nad monetizacijom.

**Phase:** MVP

**Journey milestones:** J-04, J-05

**User story:**  
Kao posjetilac,  
želim vidjeti povezane sadržaje na dnu detail stranice,  
kako bih otkrio još zanimljivih mjesta ili događaja bez vraćanja na pretragu.

**Kontekst:** Related content se prikazuje na dnu svake detail stranice. Logika odabira je definisana u Ch.02, sekcija 2.3. Za Event: prioritet imaju drugi eventi na istom Place-u, zatim eventi iste kategorije u narednih 14 dana, pa eventi sa istim tagovima. Za Place: nadolazeći eventi na tom mjestu, zatim mjesta iste kategorije u blizini. Promovirani listinzi nemaju prioritet u related contentu.

**Acceptance criteria:**

- [ ] Na dnu Event detail stranice prikazuje se sekcija "Povezano" sa do 6 stavki
- [ ] Za Event, stavke se biraju ovim redoslijedom dok se ne popuni lista: (1) drugi eventi na istom Place-u, (2) eventi iste primarne kategorije u narednih 14 dana, (3) eventi sa istim tagovima
- [ ] Child eventi parent-a se ne prikazuju u related contentu (imaju zasebnu sekciju)
- [ ] Na dnu Place detail stranice prikazuje se sekcija "Povezano" sa do 6 stavki
- [ ] Za Place, stavke se biraju ovim redoslijedom: (1) nadolazeći eventi na tom mjestu, (2) mjesta iste primarne kategorije u blizini (po udaljenosti ako je lokacija poznata, inače po sortDate)
- [ ] Promovirani listinzi nemaju prioritet u related content sekciji
- [ ] Stavke se prikazuju kao mini-kartice (reuse `<ListingCard>` komponente, kompaktna varijanta)
- [ ] Ako nema dovoljno stavki za related content — sekcija prikazuje koliko ima (može i manje od 6)
- [ ] Ako nema nijedne stavke — sekcija se ne prikazuje

**Backend Scope:**

- `GET /events/{id}/related?limit=6` — vraća listu related listinga prema definisanoj logici
- `GET /places/{id}/related?limit=6` — isto za mjesta
- Backend implementira logiku prioritizacije izvora (isti Place → ista kategorija → isti tagovi)

**Frontend Scope:**

- UI: Sekcija "Povezano" na dnu detail stranice
- UI: Horizontalni scroll ili grid sa mini-karticama
- UX: Sekcija se ne prikazuje ako nema related sadržaja
- UX: "Vidi sve" link ako ima više od 6 stavki iste kategorije (opciono za MVP)

**Tehničke napomene:**

- Related content algoritam ne mora biti savršen pri lansiranju — bitno je da prikazuje nešto smisleno (Ch.02, 2.3).
- Za "u blizini" logiku kod Place-ova, koristiti istu Haversine kalkulaciju kao za filter po udaljenosti.
- Related content se može keširati kratkoročno jer se ne mijenja često.

**Testovi (MVP):**

- [ ] Event na Place-u koji ima druge evente — prikazuje te evente prvi
- [ ] Event bez Place-a — prikazuje evente iste kategorije u narednih 14 dana
- [ ] Place sa nadolazećim eventima vlasnika — prikazuje te evente
- [ ] Place bez evenata — prikazuje mjesta iste kategorije
- [ ] Nema related sadržaja — sekcija se ne prikazuje
- [ ] Parent event — child eventi nisu u related sekciji (imaju svoju sekciju gore)

**Wireframe referenca:** —

**Implementacijske napomene:** Za MVP, related content može koristiti jednostavne SQL upite sa UNION i LIMIT. Nije potreban ML ili collaborative filtering — to je potencijalna optimizacija za kasnije.