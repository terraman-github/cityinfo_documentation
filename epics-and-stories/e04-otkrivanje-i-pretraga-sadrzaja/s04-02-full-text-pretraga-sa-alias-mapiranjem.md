---
id: S04-02
parent_epic: E04
linear_id: ""
phase: MVP
journey_milestones: [J-04]
type: fullstack
---

# S04-02 — Full-text pretraga sa alias mapiranjem

**Naslov:** Full-text pretraga sa alias mapiranjem

**Excerpt:** Korisnik kuca u search bar i dobija rezultate po nazivu, opisu i aliasima kategorija. Pretraga "gym" pronalazi kategoriju "Teretane i fitness" zahvaljujući alias tabeli. Pretraga radi isključivo unutar aktivnog režima (Events ili Places).

**Phase:** MVP

**Journey milestones:** J-04

**User story:**  
Kao posjetilac,  
želim pretražiti sadržaj unosom teksta u search bar,  
kako bih brzo pronašao konkretne listinge, kategorije ili tagove bez ručnog prolaženja kroz liste.

**Kontekst:** Korisnik je na naslovnoj ili stranici sa rezultatima i koristi search bar. Pretraga pretražuje samo sadržaj aktivnog režima (Events ili Places). Full-text pretraga pokriva polja: name, nameAlt, description, descriptionAlt. Alias tabela (iz E03a) proširuje pretraživo polje — termin "picerija" pronalazi kategoriju "Restorani". Detalji o pretrazi u Ch.02, sekcija 2.2.

**Acceptance criteria:**

- [ ] Korisnik može unijeti tekst u search bar i pokrenuti pretragu (Enter ili klik na ikonu)
- [ ] Pretraga pretražuje po: name, nameAlt, description, descriptionAlt listinga
- [ ] Rezultati uključuju samo javno vidljive listinge iz aktivnog režima
- [ ] Pretraga je case-insensitive i tolerantna na dijakritike (npr. "cevabdzinice" pronalazi "Ćevabdžinice")
- [ ] Alias mapiranje: pretraga "gym" pronalazi kategoriju "Teretane i fitness" i prikazuje njene listinge
- [ ] Alias mapiranje: pretraga "picerija" pronalazi kategoriju "Restorani" i prikazuje njene listinge
- [ ] Pretraga na sekundarnom jeziku funkcioniše — turist koji traži "restaurant" pronalazi listinge sa nameAlt ili descriptionAlt koji sadrži taj termin
- [ ] Rezultati se prikazuju u istom card formatu kao na naslovnoj
- [ ] Ako nema rezultata, prikazuje se poruka sa prijedlogom (npr. "Pokušajte sa širim terminom")
- [ ] Pretraga se može kombinovati sa aktivnim filterima (AND logika)

**Backend Scope:**

- `GET /events?q={searchTerm}` — full-text pretraga evenata
- `GET /places?q={searchTerm}` — full-text pretraga mjesta
- Backend provjerava alias tabelu: ako searchTerm odgovara aliasu, proširuje rezultate listinzima iz ciljne kategorije
- Pretraga treba biti efikasna — koristiti indekse za full-text search

**Frontend Scope:**

- UI: Search bar u headeru, uvijek vidljiv
- UI: Rezultati pretrage u istom grid/lista formatu kao naslovna
- Klijentska validacija: minimum 2 karaktera za pokretanje pretrage
- UX: Pretraga se pokreće pritiskom Enter ili klikom na search ikonu (ne automatski dok se kuca — to je autosuggest u S04-03)
- UX: Loading indikator dok se rezultati učitavaju
- UX: Aktivni search termin se prikazuje kao chip koji se može ukloniti

**Tehničke napomene:**

- Dijakritička tolerancija se može postići normalizacijom na backend-u (npr. Unicode normalization ili custom collation).
- Alias lookup se radi na backend-u — frontend samo šalje originalni termin.

**Testovi (MVP):**

- [ ] Pretraga "koncert" vraća evente koji sadrže "koncert" u nazivu ili opisu
- [ ] Pretraga "gym" vraća listinge iz kategorije "Teretane i fitness" (alias mapiranje)
- [ ] Pretraga "restaurant" vraća listinge sa engleskim nameAlt ili descriptionAlt
- [ ] Pretraga u Events režimu ne vraća Places i obrnuto
- [ ] Pretraga sa aktivnim filterom kategorije — rezultati su presjek oba kriterija
- [ ] Prazan rezultat — prikazuje se smislena poruka

**Wireframe referenca:** —