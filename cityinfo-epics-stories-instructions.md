# CityInfo — Pisanje Epica i User Storija

> **Verzija:** 1.1  
> **Namjena:** Instrukcija za pisanje Jira epica i user storija — služi i kao
> referenca za tim (Confluence) i kao prompt instrukcija za AI-asistiranu izradu.  
> **Ažurirano:** 30.3.2026.

---

## Zašto ovaj dokument?

CityInfo dokumentacija (poglavlja 01–08) opisuje **šta** sistem radi i **zašto**.
Epici i storije prevode to u **šta trebamo izgraditi** — komade posla koje tim
može preuzeti, procijeniti i isporučiti u sprintovima.

Ovaj dokument definiše format, ton i pravila za pisanje epica i storija tako
da budu konzistentni bez obzira ko ih piše — čovjek ili AI asistent. Nije
birokratski šablon, nego praktičan vodič koji osigurava da svaki epic i svaka
storija daju dovoljno konteksta da developer može krenuti, a product owner
može validirati rezultat.

---

## Opšta pravila (važe za epice i storije)

### Izvor istine i SSoT princip

Sav sadržaj epica i storija mora biti utemeljen na Confluence dokumentaciji
(poglavlja 01–08) i MVP SCOPE dokumentu. Ako nešto nije pokriveno u
dokumentaciji — to je signal da prvo treba dopuniti specifikaciju, ne
izmišljati u storiji.

**Confluence je SSoT (Single Source of Truth) za epice i storije.** Jira
služi za praćenje rada (sprint planning, assignees, statusi), ali definicija
— scope, acceptance criteria, kontekst — živi na Confluenceu. Jira epic/story
sadrži link na odgovarajuću Confluence stranicu, ne kopiju sadržaja. Time se
izbjegava dupliciranje i nekonzistentnost.

### Confluence struktura

Epici i storije žive u Confluence folderu **EPICS AND STORIES**. Struktura
prati princip: **jedan epic = jedna Confluence stranica**, a storije su
**podstranice svog epica**.

```
📁 EPICS AND STORIES/
├── 📄 [Epic naslov]              ← epic stranica
│   ├── 📄 [Story naslov 1]      ← story podstranica
│   ├── 📄 [Story naslov 2]
│   └── 📄 [Story naslov 3]
├── 📄 [Drugi epic naslov]
│   ├── 📄 [Story naslov 4]
│   └── 📄 [Story naslov 5]
└── ...
```

**Tok rada:**

1. Prvo se kreira epic stranica na Confluenceu sa kompletnom definicijom.
2. Zatim se kreiraju story podstranice unutar epica.
3. U Jiri se kreira epic/story sa linkom na odgovarajuću Confluence stranicu.
4. Sve izmjene scope-a, AC-a ili konteksta rade se **na Confluenceu** —
   Jira samo prati execution status.

Ovaj pristup osigurava da developer uvijek čita aktuelnu verziju definicije,
a product owner može ažurirati specifikaciju bez brige o sinhronizaciji
između dva sistema.

### Ton i stil

- Opušteno-profesionalno: piši kao da objašnjavaš kolegi, ne kao da pišeš
  ISO standard.
- Svaka storija treba imati dovoljno konteksta da je developer može razumjeti
  **bez** čitanja čitavog poglavlja — ali ne treba duplicirati dokumentaciju.
  Dovoljno je referencirati: *"Detalji o Trust Tier logici → Ch.03, sekcija 3.4"*.
- Izbjegavaj pasiv i korporativne fraze ("potrebno je obezbijediti da se..."
  → "sistem treba...").

### Jezik

- Bosanski (ijekavica) za naslove, opise, kontekst i acceptance criteria.
- Tehnički termini ostaju na engleskom kad je to prirodnije:
  `listingStatus`, `sortDate`, `Trust Tier`, `endpoint` — ne prevodi ih
  na silu.
- Jira labele i identifikatori (epic key, story key) su na engleskom.

### Veza sa Journey milestone strukturom

CityInfo koristi hibridnu strukturu: **funkcionalni epici** (grupisani po
domeni) + **journey milestones** (J-01 do J-09) koji prate korisnička
putovanja. Svaka storija pripada jednom funkcionalnom epicu, ali može biti
označena sa jednim ili više journey milestone-ova.

Journey milestones služe za **cross-cutting praćenje** — npr. "da li su sve
storije potrebne za Markovo putovanje (J-02) isporučene?" — bez da
narušavaju funkcionalnu grupaciju epica.

| Milestone | Fokus |
|-----------|-------|
| J-01 | Registracija i onboarding |
| J-02 | Kreiranje i objava sadržaja |
| J-03 | Moderacija sadržaja |
| J-04 | Otkrivanje i pretraga |
| J-05 | Interakcija sa sadržajem |
| J-06 | Promocija sadržaja |
| J-07 | Verifikacija vlasništva |
| J-08 | Operativno upravljanje |
| J-09 | Wallet i plaćanje |

### MVP / Phase oznake

Svaki epic i svaka storija nosi oznaku faze:

- **MVP** — ulazi u prvu verziju
- **Phase 2** — planirano za drugu iteraciju
- **Phase 3** — dugoročno, skaliranje
- **Backlog** — ideja, nije raspoređena

Ove oznake dolaze iz MVP SCOPE dokumenta i ne smiju se proizvoljno
mijenjati bez usaglašavanja sa product ownerom.

---

## Format epica

### Šablon

```
**Naslov:** [Kratak, jasan naziv — imenica ili imenička sintagma]

**Excerpt:** [2–3 rečenice — šta epic pokriva, zašto postoji, i koji je
poslovni cilj. Ovo je "elevator pitch" za epic.]

**Scope — šta ulazi:**
- Stavka 1
- Stavka 2
- ...

**Scope — šta NE ulazi:**
- Stavka koja bi se mogla pretpostaviti ali je izvan scope-a
- ...

**Persone:** [Koje persone su primarno pogođene]

**Journey milestones:** [J-## oznake koje epic pokriva]

**Phase:** [MVP | Phase 2 | Phase 3]

**Dokumentacijska referenca:** [Poglavlje/sekcija u Confluenceu]

**Tehničke napomene:** [Opciono — bitne arhitekturalne smjernice,
zavisnosti od drugih epica, ili poznata ograničenja koja utiču na scope]

**Success metrika:** [Opciono — kako znamo da je epic uspješno isporučen,
izvan pukog "sve storije su done". Npr. "korisnik može kreirati i objaviti
listing u manje od 3 minuta"]
```

### Pravila za pisanje epica

1. **Naslov je imenica, ne glagol.** "Listing CRUD i lifecycle" — ne
   "Implementirati listing CRUD".

2. **Excerpt objašnjava "zašto".** Ne samo šta epic pokriva, nego zašto to
   postoji kao cjelina. Čitaoc treba iz excerpta razumjeti poslovnu vrijednost.

3. **Scope granice su eksplicitne.** Sekcija "šta NE ulazi" je jednako važna
   kao "šta ulazi" — sprečava scope creep i nejasnoće. Ako postoji nešto
   što bi se logično moglo pretpostaviti ali je namjerno izostavljeno
   (npr. "push notifikacije" u MVP komunikacijskom epicu), to eksplicitno
   navedi ovdje.

4. **Ne dupliciraj dokumentaciju.** Epic daje pregled i kontekst — za detalje
   referencira poglavlje. Npr. "Trust Tier logika sa 5 nivoa, parametrizovanim
   pragovima i auto-napredovanjem — detalji u Ch.03, sekcija 3.4."

5. **Jedna domena, jedan epic.** Epic ne smije pokrivati više nepovezanih
   domena. Ako se nađeš u situaciji da epic ima storije iz dva različita
   poglavlja dokumentacije koje nemaju jaku vezu — razdvoji ga.

6. **Tehničke napomene samo kad su kritične.** Ovo nije mjesto za
   implementacijske detalje — samo za stvari koje fundamentalno utiču na
   scope ili pristup (npr. "zahtijeva integraciju sa payment providerom"
   ili "ovisi o AUTH epicu — ne može se raditi paralelno").

### Primjer epica

> ⚠️ Ovo je ilustrativni primjer formata — ne predstavlja stvarni epic
> iz projekta. Konkretni epici se definišu zasebno na Confluenceu.

```
**Naslov:** [Imenica — npr. "Korisnička registracija i onboarding"]

**Excerpt:** [Zašto ovaj epic postoji i koja je poslovna vrijednost.
Npr. "Bez registracije nema korisnika, bez korisnika nema sadržaja.
Ovaj epic pokriva kompletni tok od anonimnog posjetitelja do
registrovanog korisnika sa aktivnim nalogom."]

**Scope — šta ulazi:**
- Funkcionalna cjelina 1
- Funkcionalna cjelina 2
- ...

**Scope — šta NE ulazi:**
- Nešto što bi se moglo pretpostaviti ali je izvan scope-a
- Nešto što pripada drugom epicu (navesti kojem)

**Persone:** [Relevantne persone iz dokumentacije]

**Journey milestones:** [J-## oznake]

**Phase:** MVP

**Dokumentacijska referenca:** Ch.XX, sekcije X.X–X.X

**Tehničke napomene:**
- Zavisnost ili ograničenje koje utiče na scope
- Arhitekturalna smjernica bitna za razumijevanje

**Success metrika:** [Kako znamo da je epic uspješno isporučen —
korisnik može uraditi X u Y koraka.]
```

---

## Format user storije

### Šablon

```
**Naslov:** [Kratki opisni naslov — glagolska radnja iz perspektive korisnika]

**Excerpt:** [1–2 rečenice — šta storija pokriva i zašto postoji. Ovo je
najbrži način da neko shvati o čemu se radi bez čitanja ostatka.]

**Phase:** [MVP | Phase 2 | Phase 3]

**Journey milestones:** [J-## oznake]

**User story:**
Kao [tip korisnika],
želim [cilj — šta korisnik želi postići],
kako bih [benefit — zašto mu je to bitno].

**Kontekst:** [Gdje i kada se ova storija dešava u sistemu. Koji koraci
prethode, šta korisnik očekuje, koje pretpostavke postoje. Referencira
dokumentaciju gdje je relevantno. 2–5 rečenica.]

**Acceptance criteria:**
- [ ] Kriterij 1
- [ ] Kriterij 2
- [ ] ...

**Backend Scope:** [Šta backend treba isporučiti za ovu storiju.
Uključuje: API endpoint(e) sa HTTP metodom, putanjom, kratkim opisom
šta prima i šta vraća; server-side validaciju; side effects (npr.
šalje email, kreira entitet, triggeruje job). Opciono — izostaviti
za storije koje su čisto frontend ili čisto infrastrukturne.]
- `POST /auth/register` — prima {polja}, vraća {rezultat}
- Validacija: šta se provjerava na serveru
- Side effects: šta se dešava kao posljedica

**Frontend Scope:** [Šta frontend treba isporučiti. Uključuje: koje
UI elemente korisnik vidi (forma, lista, modal), klijentsku validaciju,
error handling i UX ponašanje (redirect, toast, inline greške).
Opciono — izostaviti za storije koje su čisto backend ili infrastrukturne.]
- UI elementi: forma/lista/modal sa poljima X, Y, Z
- Klijentska validacija: šta se provjerava prije slanja
- UX ponašanje: šta se dešava nakon uspjeha/greške

**Tehničke napomene:** [Bitne smjernice za implementaciju — bez
konkretnih tehnologija, algoritama ili DB detalja. Samo ono što
developer treba znati unaprijed da ne ode u pogrešnom smjeru.
Opciono — izostaviti ako nema šta reći.]

**Testovi (MVP):** [Optimizirani testovi — samo bitni scenariji,
ne exhaustive test plan. Fokus na happy path + ključne edge case-ove.]
- [ ] Test 1
- [ ] Test 2
- [ ] ...

**Wireframe referenca:** [Opciono — link na Balsamiq wireframe ili
screenshot ako postoji. Ako je wireframe dostavljen, acceptance criteria
treba reflektovati vidljive UI elemente.]

**Implementacijske napomene:** [Opciono — kratke napomene koje pomažu
pri izvedbi ali nisu dio AC-a. Npr. "razmotriti debounce na autosuggest
— 300ms je dobar početak" ili "sortDate logika je opisana u Ch.02, 2.4".]
```

### Pravila za pisanje user storija

1. **Naslov je radnja, ne entitet.** "Kreiranje Event listinga sa osnovnim
   podacima" — ne "Event listing" ili "Event CRUD".

2. **Excerpt je "too long, didn't read".** Ako neko čita samo excerpt, treba
   znati o čemu je storija i zašto postoji.

3. **User story format (kao/želim/kako bih) je obavezan.** Čak i za
   tehničke storije — prilagodi perspektivu. Ako je storija isključivo
   infrastrukturna, korisnik može biti "developer" ili "sistem".

4. **Kontekst objašnjava "odakle dolazim".** Ne pretpostavljaj da čitaoc
   poznaje cijeli flow. Navedi koji koraci prethode (npr. "korisnik je
   već ulogovan i ima Trust Tier 1+") i referencira dokumentaciju.

5. **Acceptance criteria su provjerljivi.** Svaki kriterij mora biti nešto
   što se može testirati sa DA/NE odgovorom. Izbjegavaj subjektivno
   ("stranica treba biti brza") — preferiraj mjerljivo ili konkretno
   ("listing se pojavljuje u rezultatima pretrage unutar 5 sekundi od
   odobravanja").

6. **AC ne duplicira dokumentaciju.** Umjesto "lifecycle statusi su:
   draft, pending, active, expired, closed, cancelled" (što je copy/paste
   iz Ch.04), napiši: "lifecycle tranzicije prate dijagram iz Ch.04,
   sekcija 4.8". Duplicirani sadržaj brzo postane nekonzistentan.

7. **Tehničke napomene su smjernice, ne specifikacije.** "AI screening
   je async i ne blokira kreiranje listinga" — da. "Koristiti
   BackgroundService sa SemaphoreSlim throttling-om i retry policy
   od 3 pokušaja" — ne.

8. **Testovi su optimizirani, ne exhaustive.** Piši testove za MVP
   validaciju: happy path + ključni edge case-ovi + failure scenariji
   koji bi bili dealbreaker. Ovo nije QA test plan.

9. **Jedna storija = jedan koherentan komad posla.** Storija treba biti
   dovoljno mala da se može završiti u jednom sprintu, ali dovoljno
   velika da isporučuje vrijednost. Ako storija ima 15+ acceptance
   criteria — vjerovatno je prevelika i treba je razbiti.

10. **Wireframe informira, ne diktira.** Ako je dostavljen wireframe,
    koristi ga da razumiješ namjeru — ali ne prepisuj pixel-perfect
    layout u AC. Wireframe pokazuje *šta* korisnik treba vidjeti i
    *kako* interaguje, ne finalni dizajn.

11. **Backend Scope i Frontend Scope razdvajaju odgovornosti.** Backend
    dev treba znati koji endpoint gradi, šta prima, šta vraća i koje
    side effecte ima. Frontend dev treba znati koju UI komponentu
    pravi, kakvu klijentsku validaciju radi i koji endpoint poziva.
    Ove sekcije su opcione — izostaviti za čisto infrastrukturne
    storije (npr. repo setup, CI/CD) ili storije koje nemaju frontend
    komponentu (npr. seed data, background job) ili backend komponentu
    (npr. čisto UI/layout storije). Za fullstack storije, obje sekcije
    su obavezne.

### Primjer user storije

> ⚠️ Ovo je ilustrativni primjer formata — ne predstavlja stvarnu storiju
> iz projekta. Konkretne storije se definišu na Confluenceu kao podstranice
> svog epica.

```
**Naslov:** [Glagolska radnja — npr. "Kreiranje novog listinga sa
osnovnim podacima"]

**Excerpt:** [1–2 rečenice — šta i zašto. Npr. "Omogućava korisniku
da kreira novi listing popunjavanjem obaveznih polja. Ovo je prvi
korak u objavljivanju sadržaja na platformi."]

**Phase:** MVP

**Journey milestones:** [J-## oznake]

**User story:**
Kao [tip korisnika — npr. organizator događaja],
želim [cilj — npr. kreirati novi listing sa osnovnim informacijama],
kako bih [benefit — npr. mogao objaviti sadržaj i privući posjetioce].

**Kontekst:** [Pretpostavke, prethodni koraci, i referenca na
dokumentaciju. Npr. "Korisnik je ulogovan, pristupa formi kroz
navigaciju. Detalji o atributima → Ch.XX, sekcija X.X."]

**Acceptance criteria:**
- [ ] Konkretan, provjerljiv kriterij 1
- [ ] Konkretan, provjerljiv kriterij 2
- [ ] Validacija / error handling kriterij
- [ ] ...

**Backend Scope:**
- `POST /example/endpoint` — prima {relevantna polja}, vraća {rezultat}
- Validacija: server-side provjere (unikatnost, format, itd.)
- Side effects: šta se dešava kao posljedica (email, kreiranje entiteta...)

**Frontend Scope:**
- UI: forma/modal/lista sa relevantnim poljima i elementima
- Klijentska validacija: format, obavezna polja, match provjere
- UX: ponašanje nakon uspjeha (redirect, toast) i greške (inline poruke)

**Tehničke napomene:** [Opciono]
- Smjernica koja utiče na pristup implementaciji
- Referenca na specifičnu logiku u dokumentaciji

**Testovi (MVP):**
- [ ] Happy path test
- [ ] Ključni edge case
- [ ] Failure / validacijski scenarij

**Wireframe referenca:** [Link ili "—" ako ne postoji]

**Implementacijske napomene:** [Opciono — prijedlozi za "kako",
koji developer može ignorisati ako nađe bolji pristup.]
```

---

## Česta pitanja i smjernice

### Koliko storija po epicu?

Nema čvrstog pravila, ali kao orijentir: 3–10 storija po epicu je zdravo.
Manje od 3 — razmisli da li je epic opravdan ili ga treba spojiti sa
drugim. Više od 10 — razmisli da li epic pokriva previše i treba ga
razbiti.

### Kada koristiti "Tehničke napomene" vs "Implementacijske napomene"?

- **Tehničke napomene** su stvari koje utiču na *šta* se gradi — ograničenja,
  zavisnosti, arhitekturalne odluke koje developer mora znati unaprijed.
- **Implementacijske napomene** su prijedlozi za *kako* — korisni savjeti
  koji nisu obavezujući. Developer ih može ignorisati ako nađe bolji pristup.

### Kako referencirati dokumentaciju?

Kratko i precizno: `Ch.04, sekcija 4.8` ili `MVP SCOPE, sekcija "Phase 2"`.
Ne kopirati sadržaj iz dokumentacije u storiju — ako se dokumentacija
promijeni, storija postaje nekonzistentna.

### Šta sa storijama koje pokrivaju više journey milestones?

Normalna situacija. Storija pripada jednom epicu ali može biti označena
sa više J-## milestones. Npr. "Kreiranje listinga" pripada epicu
"Listing CRUD" (E01), ali pokriva J-02 (kreiranje) i indirektno J-03
(moderacija, jer listing ide na review).

### Šta ako wireframe ne postoji?

Normalno za backend storije i infrastrukturne zadatke. Za frontend
storije bez wireframea: napiši AC na osnovu dokumentacije i naznači
da wireframe treba biti dostavljen prije implementacije, ili da
dizajner treba biti uključen u refinement.

### Kako pisati tehničke/infrastrukturne storije?

Koristi isti format, ali prilagodi perspektivu:

```
Kao developer,
želim imati konfigurisan CI/CD pipeline,
kako bih mogao pouzdano deployati promjene bez manualnih koraka.
```

Ili za sistemske procese:

```
Kao sistem,
želim automatski osvježavati sortDate za listings sa aktivnim AutoRenew-om,
kako bi promovirani listinzi ostali vidljivi prema ugovorenom intervalu.
```

### Kada izostaviti Backend Scope ili Frontend Scope?

Ove sekcije postoje da pomognu timu — ne da opterete svaku storiju.
Pravilo je jednostavno:

| Tip storije | Backend Scope | Frontend Scope |
|-------------|---------------|----------------|
| Fullstack (forma + API + DB) | ✅ Da | ✅ Da |
| Backend-only (seed data, migracija, background job) | ✅ Da | ❌ Izostavi |
| Frontend-only (layout, navigacija, čist UI) | ❌ Izostavi | ✅ Da |
| Infrastrukturna (repo setup, CI/CD, env config) | ❌ Izostavi | ❌ Izostavi |

Za backend-only storije, Backend Scope zamjenjuje potrebu za zasebnim
"API Endpoints" opisom. Za fullstack storije, Backend Scope daje frontend
devu jasan "contract" — koji endpoint poziva, šta šalje, šta dobija nazad.

---

## Kontrolna lista

Prije finalizacije epica ili storije, provjeri:

**Za epic:**
- [ ] Ima li excerpt koji objašnjava "zašto", ne samo "šta"?
- [ ] Je li scope jasno ograničen ("šta NE ulazi")?
- [ ] Da li referencira dokumentaciju umjesto da je duplicira?
- [ ] Je li Phase oznaka konzistentna sa MVP SCOPE dokumentom?
- [ ] Da li je jedna domena / jedno poglavlje?
- [ ] Da li je kreiran kao stranica u Confluence folderu EPICS AND STORIES?

**Za storiju:**
- [ ] Može li se pročitati bez poznavanja cijelog sistema?
- [ ] Da li su svi AC provjerljivi (DA/NE)?
- [ ] Ima li manje od 15 AC? (ako ne — razbij storiju)
- [ ] Da li kontekst objašnjava pretpostavke i prethodne korake?
- [ ] Da li tehničke napomene sadrže samo smjernice, ne implementacijske
      detalje?
- [ ] Da li testovi pokrivaju happy path + ključne edge case-ove?
- [ ] Da li je Phase i Journey milestone oznaka ispravna?
- [ ] Da li su Backend Scope i Frontend Scope dodani gdje je relevantno
      (fullstack storije — oboje; backend-only — samo backend; frontend-only
      — samo frontend; infrastrukturne — ni jedno)?
- [ ] Da li je kreirana kao podstranica svog epica na Confluenceu?
