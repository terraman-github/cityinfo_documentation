# CityInfo — Pisanje Epica i User Storija

> **Verzija:** 1.2  
> **Namjena:** Instrukcija za pisanje Jira epica i user storija — služi i kao
> referenca za tim (Confluence) i kao prompt instrukcija za AI-asistiranu izradu.  
> **Ažurirano:** 30.4.2026.

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

**Markdown u GitHub repou je SSoT za epice i storije.** Confluence služi kao
"view layer" za stakeholdere bez GitHub pristupa, a sinhronizacija ide
**one-way: markdown → Confluence** kroz `md2conf` alat (vidi sekciju
"Sinhronizacija sa Confluenceom" niže). Jira je execution tracker — sadrži
linkove na Confluence stranice, ne kopije sadržaja.

Sav sadržaj epica i storija mora biti utemeljen na dokumentaciji
(poglavlja 01–08) i MVP SCOPE dokumentu. Ako nešto nije pokriveno u
dokumentaciji — to je signal da prvo treba dopuniti specifikaciju, ne
izmišljati u storiji.

### Repo struktura

Epici i storije žive u folderu `epics-and-stories/` u GitHub repou
`cityinfo_documentation`. Struktura prati princip: **jedan epic = jedan
markdown fajl + folder istog imena za storije**.

```
📁 epics-and-stories/
├── 📄 e01-korisnicka-registracija-i-profil.md   ← epic fajl
├── 📁 e01-korisnicka-registracija-i-profil/     ← folder za storije
│   ├── 📄 s01-01-registracija-novog-korisnika.md
│   ├── 📄 s01-02-email-verifikacija.md
│   └── 📄 ...
├── 📄 e02-listing-crud-i-lifecycle.md
├── 📁 e02-listing-crud-i-lifecycle/
│   └── ...
└── 📄 .mdignore                                  ← isključuje plan i instrukcije
```

**Tok rada:**

1. Kreirati epic markdown fajl u `epics-and-stories/` sa kompletnim frontmatter-om
   (vidi sekciju "Format frontmatter-a")
2. Kreirati folder istog imena (bez `.md` ekstenzije)
3. Kreirati story fajlove kao `s##-##-naziv.md` unutar tog foldera
4. Pokrenuti `md2conf` push — Confluence stranice se kreiraju ili ažuriraju
   automatski, page ID se upisuje nazad u markdown frontmatter
5. Sve buduće izmjene scope-a, AC-a ili konteksta rade se **u markdown-u** —
   Confluence se sinhronizuje pri sljedećem push-u

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
  `lifecycleStatus`, `sortDate`, `Trust Tier`, `endpoint` — ne prevodi ih
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

## Format frontmatter-a (kritično za md2conf)

Svaki epic i story fajl **mora** imati YAML frontmatter na vrhu fajla. Format
je striktan jer ga koriste md2conf, Jira sync skripte i drugi alati.

### Frontmatter za epic

```yaml
---
id: E01
phase: MVP
journey_milestones: [J-01]
personas: [Marko, Ana, Thomas, Lejla]
story_count: 8
title: "E01 — Korisnička registracija i profil"
confluence_page_id: ""
---
```

### Frontmatter za story

```yaml
---
id: S01-01
parent_epic: E01
phase: MVP
journey_milestones: [J-01]
type: fullstack
title: "S01-01 — Registracija novog korisnika"
confluence_page_id: ""
---
```

### Pravila za frontmatter

1. **`id`** je obavezan i mora odgovarati imenu fajla (npr. `id: E03a` u
   `e03a-...md`, `id: S01-01` u `s01-01-...md`).

2. **`title`** je obavezan i mora biti **identičan** Confluence page title-u.
   Format: `"<ID> — <Naslov>"`. Npr. `"E01 — Korisnička registracija i profil"`.
   md2conf ga koristi kao Confluence page title.

3. **`confluence_page_id`** ostaje prazan string `""` pri kreiranju novog
   fajla. md2conf ga automatski popunjava nakon prvog push-a.

4. **`phase`** je jedan od: `MVP`, `Phase 2`, `Phase 3`, `Backlog`.

5. **`journey_milestones`** je YAML lista u flow stilu: `[J-01, J-02]`.

6. **`type`** je samo na storijama (ne na epicima). Vrijednosti:
   - `fullstack` — ima i backend i frontend
   - `backend-only` — samo backend
   - `frontend-only` — samo frontend
   - `infra` — infrastruktura, repo setup, CI/CD i sl.

7. **`parent_epic`** je samo na storijama, vrijednost je `id` epica.

8. **`personas`** je opciono na epicima, lista bez navodnika oko imena:
   `[Marko, Ana, Thomas, Lejla]`.

9. **`story_count`** je opciono na epicima, broj storija u epicu.

### Šta ne ide u frontmatter

- **NE pisati H1 heading u tijelu fajla** (`# E01 — ...`) — to dupliciraju
  naslov koji već dolazi iz `title` polja u frontmatter-u. Tijelo fajla
  počinje **direktno sa `**Naslov:**` linijom**.

- **NE koristiti `linear_id` ili druge stara polja.** Linear nije u upotrebi.

---

## Format epica

### Šablon

````
---
id: [E##]
phase: [MVP | Phase 2 | Phase 3]
journey_milestones: [J-##]
personas: [...]
story_count: [broj]
title: "[E##] — [Naslov]"
confluence_page_id: ""
---

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
````

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

7. **Bold label sa vrijednošću u istoj liniji — bez drugog bold-a.**
   Pisati `**Phase:** MVP`, NE `**Phase:** **MVP**`. Drugi bold close kvari
   Confluence rendering (linije se zalijepe bez razmaka).

### Primjer epica

> ⚠️ Ovo je ilustrativni primjer formata — ne predstavlja stvarni epic
> iz projekta.

````markdown
---
id: E01
phase: MVP
journey_milestones: [J-01]
personas: [Marko, Ana, Thomas, Lejla]
story_count: 8
title: "E01 — Korisnička registracija i profil"
confluence_page_id: ""
---

**Naslov:** Korisnička registracija i profil

**Excerpt:** Bez korisnika nema sadržaja, bez sadržaja nema platforme.
Ovaj epic pokriva kompletni tok od anonimnog posjetioca do registrovanog
korisnika sa verificiranim emailom, potvrđenim telefonom i funkcionalnim
profilom.

**Scope — šta ulazi:**

- Funkcionalna cjelina 1
- Funkcionalna cjelina 2

**Scope — šta NE ulazi:**

- Trust Tier logika i automatsko napredovanje — [E06](../e06-trust-tier-sistem.md)
- Wallet i kreditni sistem — [E09](../e09-kreditni-sistem-i-wallet.md)

**Persone:** Marko (organizator), Ana (vlasnica biznisa), Thomas (turist)

**Journey milestones:** J-01

**Phase:** MVP

**Dokumentacijska referenca:** Ch.03, sekcije 3.2–3.3, 3.7

**Tehničke napomene:**

- Ovaj epic je na kritičnom putu — gotovo svaki drugi epic zavisi od
  User entiteta i autentifikacije.

**Success metrika:** Korisnik se može registrovati, verificirati email,
potvrditi telefon, prijaviti se i obrisati račun — kompletan self-service
lifecycle bez intervencije.
````

---

## Format user storije

### Šablon

````
---
id: [S##-##]
parent_epic: [E##]
phase: [MVP | Phase 2 | Phase 3]
journey_milestones: [J-##]
type: [fullstack | backend-only | frontend-only | infra]
title: "[S##-##] — [Naslov]"
confluence_page_id: ""
---

**Naslov:** [Kratki opisni naslov — glagolska radnja iz perspektive korisnika]

**Excerpt:** [1–2 rečenice — šta storija pokriva i zašto postoji.]

**Phase:** [MVP | Phase 2 | Phase 3]

**Journey milestones:** [J-## oznake]

**User story:**

*Kao [tip korisnika],*  
*želim [cilj — šta korisnik želi postići],*  
*kako bih [benefit — zašto mu je to bitno].*

**Kontekst:** [Gdje i kada se ova storija dešava u sistemu. Koji koraci
prethode, šta korisnik očekuje, koje pretpostavke postoje. Referencira
dokumentaciju gdje je relevantno. 2–5 rečenica.]

**Acceptance criteria:**

- [ ] Kriterij 1
- [ ] Kriterij 2
- [ ] ...

**Backend Scope:** [Šta backend treba isporučiti za ovu storiju.
Opciono — izostaviti za frontend-only ili infra storije.]

- `POST /endpoint` — prima {polja}, vraća {rezultat}
- Validacija: šta se provjerava na serveru
- Side effects: šta se dešava kao posljedica

**Frontend Scope:** [Šta frontend treba isporučiti.
Opciono — izostaviti za backend-only ili infra storije.]

- UI: forma/lista/modal sa poljima
- Klijentska validacija
- UX: ponašanje nakon uspjeha/greške

**Tehničke napomene:** [Bitne smjernice. Opciono.]

**Testovi (MVP):** [Optimizirani testovi — happy path + ključni edge case-ovi.]

- [ ] Test 1
- [ ] Test 2

**Wireframe referenca:** [Link ili "—" ako ne postoji]

**Implementacijske napomene:** [Opciono]
````

### Format User story sekcije — striktna pravila

User story sekcija ima **specifičan format zbog Confluence rendering-a**:

1. **Prazna linija ispod headera `**User story:**`**.
2. **Svaka linija sadržaja u italicu** (`*Kao ...,*`).
3. **Trailing 2 razmaka** na kraju svake linije OSIM zadnje (soft line break).
4. **Bez praznih linija između rečenica** unutar User story bloka.

```markdown
**User story:**

*Kao [tip korisnika],*  ← 2 razmaka na kraju
*želim [cilj],*  ← 2 razmaka na kraju
*kako bih [benefit].*  ← bez razmaka, kraj bloka
```

Razlog: ovaj format renderuje na Confluenceu kao kurzivni paragraf sa
linijskim prelomima (kao da je pritisnuto Shift+Enter), a ne kao tri
zasebna paragrafa.

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
    Ove sekcije su opcione — vidi pravila za izostavljanje u "Česta
    pitanja".

12. **Bold label sa vrijednošću — bez drugog bold-a.** Pisati
    `**Phase:** MVP`, ne `**Phase:** **MVP**`. Isto pravilo kao za epic.

### Primjer user storije

> ⚠️ Ilustrativni primjer formata — ne predstavlja stvarnu storiju iz projekta.

````markdown
---
id: S01-01
parent_epic: E01
phase: MVP
journey_milestones: [J-01]
type: fullstack
title: "S01-01 — Registracija novog korisnika"
confluence_page_id: ""
---

**Naslov:** Registracija novog korisnika

**Excerpt:** Prvi korak na platformi — korisnik kreira račun sa emailom,
username-om i lozinkom, i prihvata GDPR saglasnost.

**Phase:** MVP

**Journey milestones:** J-01

**User story:**

*Kao posjetilac CityInfo platforme,*  
*želim kreirati korisnički račun unosom osnovnih podataka,*  
*kako bih mogao pristupiti funkcionalnostima koje zahtijevaju registraciju.*

**Kontekst:** Korisnik dolazi na platformu prvi put. Može pregledati javni
sadržaj kao visitor, ali kad želi kreirati listing — mora se registrovati.
Detalji o User entitetu → **Ch.03, sekcija 3.3**.

**Acceptance criteria:**

- [ ] Korisnik može kreirati račun unosom: email, username, fullName, password
- [ ] Email mora biti jedinstven — duplikat vraća jasnu grešku
- [ ] GDPR saglasnost je obavezna — registracija ne prolazi bez nje
- [ ] Validacijske greške se prikazuju inline uz relevantna polja

**Backend Scope:**

- `POST /auth/register` — prima {email, username, fullName, password,
  gdprConsent}, vraća {userId, accessToken, refreshToken}
- Validacija: email unikatnost, username unikatnost, password policy
- Side effects: kreira User entitet, bilježi gdprConsentAt, šalje
  verifikacioni email

**Frontend Scope:**

- UI: registracijska forma sa poljima — email, username, fullName,
  password, confirm password, GDPR checkbox
- Klijentska validacija: format emaila, password match
- UX: nakon uspjeha — redirect na "Provjerite email"; greške — inline poruke

**Tehničke napomene:**

- `createdAt` se automatski popunjava
- Lozinka se hashira prije pohranjivanja

**Testovi (MVP):**

- [ ] Registracija sa validnim podacima uspješno kreira račun
- [ ] Registracija sa duplikatom emaila vraća odgovarajuću grešku
- [ ] Registracija bez GDPR saglasnosti ne prolazi

**Wireframe referenca:** —
````

---

## Linkovi između dokumenata

### Linkovi između epica i storija

Koristi **relativne markdown linkove**. md2conf ih automatski konvertuje
u Confluence linkove pri push-u.

```markdown
Vidi [E06](../e06-trust-tier-sistem.md) za detalje o Trust Tier-u.
Detalji u [S06-01](../e06-trust-tier-sistem/s06-01-automatska-evaluacija.md).
```

Iz storije, linkovi na druge epice idu sa `../`, na storije unutar drugog
epica sa `../<epic-folder>/<story>.md`.

### Linkovi na chapter dokumente

Iz `epics-and-stories/` folder, linkovi na root chapter fajlove:

```markdown
Detalji u [Ch.04, sekcija 4.5](../../04-sadrzaj.md).
```

Ovaj pattern će raditi tek kad se cijeli repo pushira iz root-a sa
`md2conf "."`. Za sad je sigurnije referencirati u tekstu bez markdown
linka:

```markdown
Detalji o Listing entitetu → **Ch.04, sekcija 4.1**.
```

### Linkovi na vanjske Confluence stranice

Ako stranica postoji na Confluenceu ali NE postoji kao markdown fajl u
repou, koristi direktni Confluence URL:

```markdown
[Persone i korisnička putovanja](https://terraprojects.atlassian.net/wiki/spaces/GI/pages/243040257)
```

### Stale `../project-specs/` linkovi

**Stari format `[X](../project-specs/Y.md)` se NE koristi.** Ako naletiš na
takav link u postojećim fajlovima, popravi ga (vidi `fix_project_specs_links.py`
u `md2conf-tooling/`).

---

## Sinhronizacija sa Confluenceom

### One-way sync: markdown → Confluence

Repo `cityinfo_documentation` je SSoT. Confluence stranice se generišu iz
markdown-a kroz `md2conf` alat. **Niko ne uređuje stranice direktno na
Confluenceu** — svaka izmjena ide kroz git i sljedeći push.

### Workflow za novi epic ili storiju

1. **Kreiraj markdown fajl** sa kompletnim frontmatter-om (uključujući
   `title`, `phase`, `id`; `confluence_page_id` ostaje prazan).

2. **Commit u git** sa porukom tipa `feat(docs): add S01-09 ...`.

3. **Pokreni md2conf** iz repo root-a:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   md2conf "." --no-generated-by -l info
   ```

4. md2conf:
   - Detektuje novi fajl (jer nema `confluence_page_id`)
   - Kreira novu Confluence stranicu pod EPICS AND STORIES folderom
   - Upisuje page ID nazad u markdown frontmatter
   - Konvertuje sve relativne linkove u Confluence URL-ove

5. **Commit rezultat** (`confluence_page_id` koji je md2conf upisao):

   ```powershell
   git add .
   git commit -m "chore(docs): record confluence_page_id for new pages"
   git push
   ```

### Workflow za izmjenu postojećeg fajla

1. **Uredi markdown fajl.**

2. **Commit u git.**

3. **Pokreni md2conf** — detektuje izmjenu, ažurira Confluence stranicu.

   ```powershell
   md2conf "." --no-generated-by -l info
   ```

   md2conf koristi checksum da preskoči stranice koje nisu mijenjane —
   idempotentno.

### Tooling u `md2conf-tooling/`

| Skripta | Kada se koristi |
|---------|-----------------|
| `build_page_id_map.py` | Jednom — gradi mapu logičkih ID → page ID iz Confluence-a |
| `inject_page_ids.py` | Jednom (legacy) — popunjava `confluence_page_id` iz mape |
| `inject_titles.py` | Jednom (legacy) — popunjava `title` iz Confluence-a |
| `markdown_cleanup.py` | Po potrebi — uklanja H1, popravlja bold-bold pattern |
| `markdown_userstory_format.py` | Po potrebi — pretvara User story u italic format |
| `fix_project_specs_links.py` | Po potrebi — popravlja stale `../project-specs/` linkove |

Ove skripte nisu potrebne za normalan workflow ako se novi fajlovi pišu
po ovoj instrukciji od početka.

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

```markdown
**User story:**

*Kao developer,*  
*želim imati konfigurisan CI/CD pipeline,*  
*kako bih mogao pouzdano deployati promjene bez manualnih koraka.*
```

Ili za sistemske procese:

```markdown
**User story:**

*Kao sistem,*  
*želim automatski osvježavati sortDate za listings sa aktivnim AutoRenew-om,*  
*kako bi promovirani listinzi ostali vidljivi prema ugovorenom intervalu.*
```

### Kada izostaviti Backend Scope ili Frontend Scope?

Ove sekcije postoje da pomognu timu — ne da opterete svaku storiju.
Pravilo je jednostavno:

| Tip storije (`type`) | Backend Scope | Frontend Scope |
|---------------------|---------------|----------------|
| `fullstack` | ✅ Da | ✅ Da |
| `backend-only` | ✅ Da | ❌ Izostavi |
| `frontend-only` | ❌ Izostavi | ✅ Da |
| `infra` | ❌ Izostavi | ❌ Izostavi |

Za `backend-only` storije, Backend Scope zamjenjuje potrebu za zasebnim
"API Endpoints" opisom. Za `fullstack` storije, Backend Scope daje frontend
devu jasan "contract" — koji endpoint poziva, šta šalje, šta dobija nazad.

### Šta ako sam zaboravio neki dio frontmatter-a?

md2conf će prijaviti grešku ili ignorisati fajl. Najčešći problemi:

- **Bez `title`** → md2conf koristi prvu liniju kao title, što obično daje
  duplikate ili pogrešne naslove.
- **Bez `id`** → automatske skripte za sync (npr. Jira) ne mogu mapirati fajl.
- **`confluence_page_id` se ne upisuje sam** → provjeri da li md2conf ima
  write-back permisije (`--keep-update` flag, koji je default).

---

## Kontrolna lista

Prije commit-anja epica ili storije, provjeri:

**Za epic:**

- [ ] Frontmatter ima sve obavezna polja: `id`, `phase`, `title`,
      `confluence_page_id` (prazan ili popunjen)
- [ ] Tijelo NE počinje sa `# Naslov` (H1 heading)
- [ ] Excerpt objašnjava "zašto", ne samo "šta"
- [ ] Scope je jasno ograničen ("šta NE ulazi")
- [ ] Referencira dokumentaciju umjesto da je duplicira
- [ ] Phase oznaka konzistentna sa MVP SCOPE dokumentom
- [ ] Jedna domena / jedno poglavlje
- [ ] `**Label:** Value` format (ne `**Label:** **Value**`)

**Za storiju:**

- [ ] Frontmatter ima sve obavezna polja: `id`, `parent_epic`, `phase`,
      `type`, `title`, `confluence_page_id`
- [ ] Tijelo NE počinje sa `# Naslov` (H1 heading)
- [ ] Može se pročitati bez poznavanja cijelog sistema
- [ ] User story sekcija u italic + soft break formatu
- [ ] Svi AC su provjerljivi (DA/NE)
- [ ] Manje od 15 AC (ako više — razbij storiju)
- [ ] Kontekst objašnjava pretpostavke i prethodne korake
- [ ] Tehničke napomene su smjernice, ne implementacijski detalji
- [ ] Testovi pokrivaju happy path + ključne edge case-ove
- [ ] Phase i Journey milestone oznake ispravne
- [ ] Backend Scope i Frontend Scope dodati prema `type` field-u
- [ ] `**Label:** Value` format (ne `**Label:** **Value**`)
- [ ] Linkovi na druge fajlove su relativni markdown linkovi

---

## Changelog

| Verzija | Datum | Opis |
|---------|-------|------|
| 1.2 | 30.4.2026. | **md2conf integracija.** Dodana sekcija "Format frontmatter-a" sa eksplicitnim definicijama `title` i `confluence_page_id`. Uklonjen H1 heading iz template-a (duplikat title-a). Dodana striktna pravila za User story format (italic + soft breaks). Dodano pravilo o `**Label:** **Value**` patternu. Dodana sekcija "Linkovi između dokumenata" i "Sinhronizacija sa Confluenceom". Workflow za novi epic/story sa md2conf-om. Repo struktura ažurirana (markdown SSoT, ne Confluence). |
| 1.1 | 30.3.2026. | Dodana podjela na Backend Scope / Frontend Scope. Dodana Confluence struktura kao SSoT. |
| 1.0 | 30.3.2026. | Inicijalna verzija — format epica i storija, SSoT princip, pravila, šabloni, FAQ, kontrolne liste. |
