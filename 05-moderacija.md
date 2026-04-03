# 05 - MODERACIJA

> **Verzija:** 2.0  
> **Status:** Završeno ✅  
> **Datum:** 1.4.2026

* * *

<a id="pregled-poglavlja"></a>

## Pregled poglavlja

Moderacija je srce sistema kvaliteta na CityInfo platformi. Ovdje se ne radi o cenzuri, već o osiguranju da korisnici dobijaju tačan, koristan i primjeren sadržaj. Moderatori su profesionalni zaposlenici platforme — ne volonteri, ne algoritmi koji samostalno odlučuju.

Ovo poglavlje objašnjava kako moderacija funkcioniše, ko ima koje ovlasti, i kako AI pomaže (ali ne zamjenjuje) ljudske odluke. Također pokriva komunikaciju sa korisnicima jer način na koji pričamo sa ljudima direktno utiče na kvalitet zajednice.

<a id="sekcije-u-ovom-poglavlju"></a>

### Sekcije u ovom poglavlju

| Sekcija | Opis | Ciljna publika |
| --- | --- | --- |
| **5.1 Filozofija moderacije** | Principi, Trust Tier sistem | Svi |
| **5.2 Moderacijski workflow** | Queue, prioritizacija, odluke | Dev + Ops |
| **5.3 AI Screening** | Automatska detekcija, blocking logic | Dev + Ops |
| **5.4 Moderatorske akcije** | Šta može/ne može, permisije, blokiranje | Ops |
| **5.5 Komunikacija sa korisnicima** | Template poruke, ton | Ops |
| **5.6 Verifikacija vlasništva** | Dokumenti, workflow, verifikacija po tier-u | Ops + Dev |
| **5.7 API Endpoints** | Lista endpointa za moderaciju | Dev |

<a id="povezani-dokumenti"></a>

### Povezani dokumenti

- [03 - Korisnici i pristup](../project-specs/03-korisnici-i-pristup.md) — Trust Tier sistem, parametri napredovanja
- [04 - Sadržaj](../project-specs/04-sadrzaj.md) — Listing statusni model (`listingStatus`), ListingDocument entitet (SSoT, sekcija 4.7), korisničke interakcije (sekcija 4.9), API endpointi (sekcija 4.10)
- [07 - Komunikacija](../project-specs/07-komunikacija.md) — Message sistem

* * *

<a id="51-filozofija-moderacije"></a>

## 5.1 Filozofija moderacije

Moderacija na CityInfo-u nije gatekeeping — to je osiguranje kvaliteta. Cilj nije blokirati sadržaj, već pomoći korisnicima da ga učine boljim. Kada nekome kažemo "potrebne su izmjene", to nije kazna već prilika da njihov sadržaj zasija.

Sistem balansira potrebu za brzinom (korisnici ne žele čekati) sa potrebom za kvalitetom (platforma mora ostati korisna). Zato korisnici višeg trust tiera objavljuju odmah pa se pregledaju naknadno, dok novi korisnici čekaju odobrenje — ali nikad predugo.

<a id="511-ključni-principi"></a>

### 5.1.1 Ključni principi

| Princip | Šta to znači u praksi |
| --- | --- |
| **Kvalitet prije kvantitete** | Bolje manje dobrih oglasa nego puno loših. Korisnici dolaze jer mogu pronaći ono što traže. |
| **Edukacija umjesto cenzure** | Ne kažemo "odbačeno" bez objašnjenja. Kažemo zašto i kako popraviti. |
| **Konzistentnost** | Isti standardi za sve — lokalni kafić i velika franšiza se tretiraju jednako. |
| **Brzina** | Pre-moderacija unutar 2h, post-moderacija unutar 8h. |
| **Transparentnost** | Korisnik uvijek zna zašto je nešto odbačeno ili vraćeno na izmjenu. |
| **Pozitivna komunikacija** | "Primijetili smo…" je bolje od "Morate…". Ton gradi zajednicu. |
| **Kulturna osjetljivost** | Sarajevo nije Berlin — lokalni kontekst je bitan. |

<a id="512-moderacijski-ciklus"></a>

### 5.1.2 Moderacijski ciklus

```
EDUKACIJA → PREVENCIJA → INTERVENCIJA → EVALUACIJA
    ↑                                        ↓
    ←────────────────────────────────────────
```

- **Edukacija**: Jasne smjernice, primjeri dobrog sadržaja, tooltips u formi
- **Prevencija**: AI screening hvata očigledne probleme, trust sistem filtrira
- **Intervencija**: Ljudska moderacija sa fokusom na poboljšanje, ne kažnjavanje
- **Evaluacija**: Pratimo patterne, učimo, poboljšavamo proces

> 💡 **Praktična napomena:** Filozofija nije samo "lijepe riječi" — ovi principi se reflektuju u svakom template-u, svakoj odluci, svakom UX elementu. Moderatori prolaze trening upravo na ovim principima.

<a id="513-trust-tier-sistem"></a>

### 5.1.3 Trust Tier sistem

CityInfo koristi sistem nivoa povjerenja (Trust Tier) koji određuje kako se sadržaj korisnika moderira. Umjesto binarnog pristupa "vjerujemo / ne vjerujemo", sistem prepoznaje da korisnici grade povjerenje kroz konzistentno kvalitetan sadržaj. Detaljna specifikacija Trust Tier sistema — uključujući sve konfiguracijske parametre — nalazi se u [03 - Korisnici i pristup](../project-specs/03-korisnici-i-pristup.md). Ovdje je prikazan sažetak relevantan za moderacijski workflow.

<a id="trust-tier-nivoi"></a>

#### Trust Tier nivoi

| Tier | Naziv | Moderacija | Sampling | Kako se dostiže |
| --- | --- | --- | --- | --- |
| **0** | Restricted | Pre-moderacija | 100% | Ručno ili automatski (kršenje pravila) |
| **1** | Standard | Pre-moderacija | 100% | Default za nove korisnike |
| **2** | Trusted | Post-moderacija | 100% | Automatski (konfigurisani pragovi) |
| **3** | Established | Post-moderacija | Konfigurisano | Automatski (konfigurisani pragovi) |
| **4** | Verified Partner | Post-moderacija | Konfigurisano | Ručno — moderator sa `can_manage_trust_tier` permisijom |

> ⚠️ **Napomena:** Sampling procenti za Tier 3 i Tier 4 su konfiguracijski parametri (`TIER3_SAMPLING_PERCENT`, `TIER4_SAMPLING_PERCENT`). Početne preporučene vrijednosti su 50% i 20%, ali mogu se prilagoditi na osnovu operativnog iskustva.

**Objašnjenje nivoa:**

- **Restricted (0)**: Korisnici koji su ozbiljno ili višestruko prekršili pravila. Zaključani na pre-moderaciju bez mogućnosti automatskog napredovanja. Izlaz je moguć samo kroz ručnu intervenciju moderatora sa `can_manage_trust_tier` permisijom.
- **Standard (1)**: Svi novi korisnici počinju ovdje. Svaki sadržaj čeka odobrenje moderatora prije nego postane vidljiv. Cilj je što prije napredovati u Trusted.
- **Trusted (2)**: Korisnici koji su dokazali da prave kvalitetan sadržaj. Njihov sadržaj ide live odmah, a moderator ga pregleda naknadno. Sav sadržaj se i dalje pregleda (100%).
- **Established (3)**: Korisnici sa dugom istorijom kvalitetnog sadržaja. Post-moderacija sa samplingom — moderator pregleda samo dio njihovog sadržaja. Ostatak prolazi automatski.
- **Verified Partner (4)**: Ugovorni partneri platforme (kino kompleksi, kulturni centri, gradske institucije). Najniži sampling. Postavlja se ručno od strane moderatora sa `can_manage_trust_tier` permisijom, nakon uspostavljanja poslovnog odnosa. Ovo je osjetljiva akcija jer direktno mijenja moderacijski workflow za korisnika.

<a id="sampling"></a>

#### Sampling

Sampling znači da se ne pregleda svaki sadržaj, već nasumični uzorak. Ovo značajno smanjuje opterećenje moderatora za provjerene korisnike, dok i dalje održava kontrolu kvaliteta.

Ako se u pregledanom uzorku pronađe problem:

- Sadržaj se označava/skriva kao i obično
- Korisnik može biti degradiran za tier
- Sistem može privremeno povećati sampling procenat za tog korisnika

<a id="napredovanje"></a>

#### Napredovanje

Napredovanje kroz tier-ove je automatsko za nivoe 1→2 i 2→3. Sistem provjerava uslove nakon svake moderatorske odluke. Sva tri uslova moraju biti ispunjena **istovremeno** — procenat sam za sebe nije dovoljan jer bi korisnik sa jednom odobrenom objavom matematički imao 100% uspješnost.

| Prijelaz | Parametar | Preporučena početna vrijednost | Opis |
| --- | --- | --- | --- |
| **Tier 1 → 2** | `TIER1_MIN_APPROVED` | 5   | Minimalan broj odobrenih objava |
|     | `TIER1_MIN_SUCCESS_RATE` | 80% | Minimalni procenat odobrenih (approved / ukupno submitted) |
|     | `TIER1_MIN_ACCOUNT_AGE_DAYS` | 7   | Minimalna starost računa u danima |
| **Tier 2 → 3** | `TIER2_MIN_APPROVED` | 20  | Minimalan broj odobrenih objava |
|     | `TIER2_MIN_SUCCESS_RATE` | 85% | Minimalni procenat odobrenih |
|     | `TIER2_MIN_ACCOUNT_AGE_DAYS` | 30  | Minimalna starost računa u danima |

Preporučene vrijednosti su polazna tačka — treba ih tune-ovati na osnovu stvarnih podataka nakon launcha. Sve vrijednosti su konfiguracijski parametri koji se mogu mijenjati bez izmjene koda.

> 💡 **Praktična napomena:** Parametri su podložni promjeni na osnovu iskustva. Početne vrijednosti su konzervativne — bolje je početi strože pa olabaviti nego obrnuto.

<a id="efekt-changes_requested-na-napredovanje"></a>

#### Efekt `changes_requested` na napredovanje

`changes_requested` je kvalitativno drugačiji signal od `rejected` — moderator ne odbija sadržaj, nego poziva korisnika na saradnju i ispravku. Penalizovati korisnika koji aktivno popravlja sadržaj bilo bi kontraproduktivno, pa `changes_requested` sam po sebi **ne utiče na Trust Tier ni na procenat uspješnosti**.

Ono što se broji je isključivo **finalna odluka** po listingu — bez obzira koliko puta je sadržaj prolazio kroz `changes_requested` u međuvremenu.

| Scenarij | Šta se broji |
| --- | --- |
| `changes_requested` → korisnik popravlja → listing prelazi u `published` | 1 approved |
| `changes_requested` → korisnik popravlja → listing prelazi u `rejected` | 1 rejected |
| Više iteracija `changes_requested` → na kraju listing prelazi u `published` | 1 approved — broj iteracija nije relevantan |
| `changes_requested` → korisnik ne reaguje, listing ostaje u tom statusu | Ništa — nema finalne odluke, ne broji se |

<a id="degradacija"></a>

#### Degradacija

Korisnik može pasti za tier ako moderacija otkrije problematičan sadržaj. Degradacija može biti **automatska** (sistem detektuje jasno definisan prag) ili **ručna** (moderator procjenjuje situaciju). Pragovi za automatsku degradaciju su konfiguracijski parametri.

**Automatska degradacija:**

Sistem automatski degradira korisnika kada su ispunjeni nedvosmisleni, mjerljivi uslovi. Svaka automatska degradacija kreira posebnu stavku u moderacijskom queue-u tipa "Trust Tier Auto-Degradation Review" — moderator mora pregledati i potvrditi ili revertovati odluku. Ovo je sigurnosna mreža koja sprečava da automatika pogrešno kazni korisnika.

| Situacija | Akcija | Queue stavka |
| --- | --- | --- |
| `TIER_REJECTED_THRESHOLD` rejected u `TIER_REJECTED_WINDOW_DAYS` dana | Automatski pad na Restricted (Tier 0) | Da — moderator pregleda i potvrđuje/revertuje |

Preporučene početne vrijednosti: `TIER_REJECTED_THRESHOLD = 3`, `TIER_REJECTED_WINDOW_DAYS = 30`.

**Ručna degradacija:**

Situacije koje zahtijevaju ljudsku procjenu — moderator odlučuje da li je degradacija opravdana. Ručna degradacija na Tier 0 (Restricted) zahtijeva `can_manage_trust_tier` permisiju.

| Situacija | Akcija | Potrebna permisija |
| --- | --- | --- |
| 1 rejected (bilo koji tier) | Upozorenje, tier se ne mijenja — ali procenat pada i može blokirati napredovanje | Standardna |
| Problem u samplingu (Tier 3) | Moderator odlučuje o padu sa Established na Trusted (Tier 2) | Standardna |
| Ozbiljno kršenje (hate speech, spam, ilegalni sadržaj) | Moderator postavlja direktno na Restricted (Tier 0), bez međufaza | `can_manage_trust_tier` |

> 💡 **Praktična napomena:** Automatska degradacija postoji da bi se sistem mogao zaštititi i izvan radnog vremena, ali uvijek podliježe ljudskom pregledu. Moderator koji pregleda auto-degradaciju može je revertovati ako procijeni da je bila nepravedna — npr. ako su rejected odluke bile sporne ili je korisnik već popravio probleme.

<a id="pre-moderacija-vs-post-moderacija"></a>

#### Pre-moderacija vs Post-moderacija

Tier direktno određuje koji tip moderacije se primjenjuje:

**Pre-moderacija (Tier 0, 1):**

- Sadržaj čeka u queue-u dok moderator ne odobri
- Listing je u statusu `in_review` — nije vidljiv javnosti dok moderator ne odobri (→ `published`)
- SLA: 2 sata
- **Ograničenje:** Korisnik može imati maksimalno `TIER_PRE_MOD_MAX_PENDING` objava koje čekaju pregled istovremeno. Mora sačekati odluku prije slanja novog sadržaja.

**Post-moderacija (Tier 2, 3, 4):**

- Sadržaj je odmah vidljiv nakon objave — listing prelazi u `published_under_review`
- Moderator pregleda naknadno (sampling po tieru) i odobrava (→ `published`) ili traži izmjene (→ `published_needs_changes`)
- SLA: 8 sati

```
┌─────────────┐
│ RESTRICTED  │ ← Tier 0: Zaključan, ne može napredovati automatski
│  (Tier 0)   │   Pre-mod, 100% pregled
└─────────────┘

┌──────────┐    ┌───────────┐    ┌─────────────┐    ┌───────────────────┐
│ STANDARD │ →  │  TRUSTED  │ →  │ ESTABLISHED │ →  │ VERIFIED PARTNER  │
│ (Tier 1) │    │  (Tier 2) │    │   (Tier 3)  │    │     (Tier 4)      │
└──────────┘    └───────────┘    └─────────────┘    └───────────────────┘
  Pre-mod         Post-mod         Post-mod           Post-mod
  100%            100%             Sampling (param)   Sampling (param)
  Automatski →    Automatski →                        Ručno (can_manage_trust_tier)
```

* * *

<a id="52-moderacijski-workflow"></a>

## 5.2 Moderacijski workflow

Moderation queue je centralno mjesto gdje moderatori vide sve što čeka pregled. Nije to obična lista — sadržaj je prioritiziran tako da najhitnije stvari budu na vrhu, a moderatori mogu efikasno raditi bez da stalno donose odluke "šta sljedeće".

<a id="521-queue-struktura"></a>

### 5.2.1 Queue struktura

Queue se dijeli u četiri zone prema prioritetu:

```
Moderation Queue
├── 🔴 Urgent (AI blocking flag) — Mora se pregledati odmah
├── 🟠 High Priority (score > 75) — Potencijalni problemi
├── 🟡 Normal Priority (score 40-75) — Standardna obrada
└── 🟢 Low Priority (score < 40) — Post-moderacija, rutinski pregled
```

Pored sadržaja koji čeka moderaciju, u queue se pojavljuju i **sistemske stavke** koje zahtijevaju pregled moderatora:

- **Trust Tier Auto-Degradation Review** — sistem je automatski degradirao korisnika; moderator potvrđuje ili revertuje
- **Instant Block Review** — sistem je automatski blokirao korisnika; moderator pregleda i odlučuje o sadržaju

Za svaki item u queue-u, moderator vidi:

- Preview sadržaja (tekst, slike)
- AI hints (ako postoje)
- Istorija korisnika (prethodni sadržaji, trust tier)
- Quick actions (Approve, Request Changes, Reject)

<a id="522-prioritizacija"></a>

### 5.2.2 Prioritizacija

Prioritet se računa automatski na osnovu nekoliko faktora. Logika je različita za pre-moderaciju i post-moderaciju.

**Pre-moderacija (Tier 0, 1):**

Svi korisnici koji čekaju da im sadržaj postane vidljiv imaju jednak bazni prioritet. Razlikovanje se vrši samo po AI riziku i vremenu čekanja — ne po tieru. Bilo bi nepravedno da novi korisnik čeka duže samo zato što je nov.

| Faktor | Težina | Logika |
| --- | --- | --- |
| **AI Risk Level** | 50% | CRITICAL > HIGH > MEDIUM > LOW |
| **Vrijeme čekanja** | 40% | Stariji sadržaj ima veći prioritet |
| **Tip sadržaja** | 10% | Event > Place (eventi su vremenski osjetljivi) |

**Post-moderacija (Tier 2, 3, 4):**

Sadržaj je već live, pa je manje hitan. Viši tier = niži prioritet jer sampling znači da se dio sadržaja uopće ne pregleda.

| Faktor | Težina | Logika |
| --- | --- | --- |
| **AI Risk Level** | 60% | CRITICAL > HIGH > MEDIUM > LOW |
| **Trust Tier** | 30% | Niži tier = viši prioritet (Tier 2 prije Tier 4) |
| **Vrijeme od objave** | 10% | Stariji sadržaj ima veći prioritet |

> 💡 **Praktična napomena:** Formule nisu fiksirane — ako se pokaže da ne rade dobro, mogu se prilagoditi. Bitno je pratiti metriku "vrijeme do prve odluke" po kategorijama.

<a id="523-odluke-moderatora"></a>

### 5.2.3 Odluke moderatora

Svaka moderatorska odluka vodi listing u određeni `listingStatus`. Postoje tri osnovne odluke, a svaka ima svoje implikacije.

| Odluka | Rezultirajući `listingStatus` | Šta se dešava | Kada koristiti |
| --- | --- | --- | --- |
| **Approve** | `published` | Listing postaje vidljiv (ili ostaje vidljiv ako je bio u post-mod toku) | Sadržaj zadovoljava standarde |
| **Request Changes** | `changes_requested` (pre-mod tok) ili `published_needs_changes` (post-mod tok) | Korisnik dobija poruku šta treba popraviti | Sadržaj ima potencijal, treba doradu |
| **Reject** | `rejected` | Listing se trajno zatvara — terminalni status | Ozbiljno kršenje pravila, nepopravljivi problemi |

**Razlika između pre-mod i post-mod toka pri "Request Changes":**

- **Pre-mod tok** (listing u `in_review`): moderator vraća listing → `changes_requested`. Listing je nevidljiv javnosti dok korisnik ne popravi i resubmituje.
- **Post-mod tok** (listing u `published_under_review`): moderator traži manje izmjene → `published_needs_changes`. Listing ostaje vidljiv javnosti dok korisnik priprema popravku.

```
flowchart LR
    A[Listing u queue] --> B{Moderator pregleda}
    B -->|Approve| C[published → vidljivo]
    B -->|Request Changes pre-mod| D[changes_requested → nevidljivo, korisnik popravlja]
    B -->|Request Changes post-mod| D2[published_needs_changes → vidljivo, korisnik popravlja]
    B -->|Reject| E[rejected → terminalno zatvoreno]
    D -->|Korisnik resubmituje| A
    D2 -->|Korisnik submita popravku| A
```

Moderator može takođe **sakriti** listing (`hidden_by_moderator`) ili ga **trajno ukloniti** (`removed`) u slučajevima koji zahtijevaju hitnu ili konačnu akciju. Ove akcije su opisane detaljnije u sekciji 5.4.

<a id="524-sla-vrijeme-odgovora"></a>

### 5.2.4 SLA vrijeme odgovora

SLA (Service Level Agreement) definiše maksimalno vrijeme od trenutka kada listing uđe u moderacijski queue do trenutka kada moderator donese prvu odluku. Ciljevi su različiti za pre-moderaciju i post-moderaciju.

**Pre-moderacija (Tier 0, 1):**

| Prioritet | Target vrijeme | Mjerenje | Eskalacija |
| --- | --- | --- | --- |
| **Urgent** (AI block) | < 30 minuta | percentil | Alert supervisor ako kasni > 15min |
| **High** (AI risk) | < 1 sat | percentil | Alert ako kasni > 30min |
| **Normal** | < 2 sata | percentil | Review ako kasni > 1h |

**Post-moderacija (Tier 2, 3, 4):**

| Trust Tier | Target vrijeme | Sampling | Napomena |
| --- | --- | --- | --- |
| **Tier 2** (Trusted) | < 8 sati | 100% | Sav sadržaj se pregleda |
| **Tier 3** (Established) | < 8 sati | `TIER3_SAMPLING_PERCENT` | Nasumični uzorak |
| **Tier 4** (Verified Partner) | < 8 sati | `TIER4_SAMPLING_PERCENT` | Minimalni pregled |

> 💡 **Praktična napomena:** SLA za pre-moderaciju je stroži jer korisnik čeka da mu sadržaj postane vidljiv. Post-moderacija je manje hitna jer je sadržaj već live, ali i dalje treba biti završena u razumnom roku. Target vrijeme se mjeri kao 95. percentil — znači da 95% sadržaja mora biti pregledano unutar navedenog vremena.

<a id="525-moderacija-editovanog-sadržaja"></a>

### 5.2.5 Moderacija editovanog sadržaja

Kada korisnik edituje aktivan listing, ponašanje zavisi od Trust Tier-a vlasnika i direktno utiče na `listingStatus`:

**Tier 0, 1 (pre-moderacija):** Editovani listing prelazi iz `published` u `in_review` — postaje nevidljiv javnosti i ulazi u queue kao nova stavka za pregled. Korisnik dobija poruku da će listing ponovo postati vidljiv nakon odobrenja.

**Tier 2+ (post-moderacija):** Editovani listing prelazi iz `published` u `published_under_review` — ostaje vidljiv javnosti. Sistem kreira novu stavku u moderacijskom queue-u za naknadni pregled, po istoj sampling logici kao za nove objave tog tier-a.

> 💡 **Praktična napomena:** Ovo je važno za konzistentnost moderacije — korisnik na Tier 1 ne smije moći zaobići kontrolu kvaliteta izmjenom sadržaja nakon inicijalnog odobrenja. Istovremeno, Verified Partner ne bi trebao čekati odobrenje za ispravku radnog vremena. Kompletna tabela tranzicija opisana je u [04 - Sadržaj, sekcija 4.8](../project-specs/04-sadrzaj.md).

* * *

<a id="53-ai-screening"></a>

## 5.3 AI Screening

AI screening nije zamjena za ljudsku moderaciju — to je pomoćni alat koji ubrzava proces i hvata očigledne probleme. AI ne donosi finalne odluke (osim u ekstremnim slučajevima), ali značajno pomaže prioritizirati queue i usmjeriti pažnju moderatora.

<a id="531-kako-ai-screening-funkcioniše"></a>

### 5.3.1 Kako AI screening funkcioniše

Kada korisnik submituje sadržaj, sistem pokreće brzi AI scan (max 3 sekunde). AI analizira tekst i slike, dodjeljuje score za različite kategorije problema, i na osnovu toga određuje prioritet u queue-u.

```
flowchart TD
    A[Korisnik submituje] --> B[Brzi AI scan]
    B --> C{Kritični sadržaj?}
    C -->|Score > 0.95| D[listingStatus = hidden_by_system]
    C -->|Score < 0.95| E[Normalan tok]
    D --> F[Urgent queue]
    E --> G[Određuje prioritet]
    G --> H[Ulazi u queue]
```

<a id="532-ai-scoring-komponente"></a>

### 5.3.2 AI scoring komponente

AI računa nekoliko nezavisnih score-ova, svaki za drugu kategoriju problema. Ovi rezultati se čuvaju kao metadata i služe moderatorima kao "hint".

| Komponenta | Raspon | Threshold | Šta detektuje |
| --- | --- | --- | --- |
| **Hate speech** | 0.0 - 1.0 | 0.7 | Govor mržnje, diskriminacija |
| **Adult content** | 0.0 - 1.0 | 0.7 | Eksplicitan sadržaj, neprimjerene slike |
| **Violence** | 0.0 - 1.0 | 0.7 | Nasilje, prijetnje |
| **Spam patterns** | 0.0 - 1.0 | 0.8 | Ponavljanje, SEO spam, mass posting |
| **Contact info** | 0.0 - 1.0 | 0.9 | Telefoni/emaili u opisu (trebaju biti u posebnim poljima) |
| **Duplicate** | 0.0 - 1.0 | 0.85 | Sličnost sa postojećim sadržajem |

<a id="533-ai-risk-level"></a>

### 5.3.3 AI Risk Level

Na osnovu pojedinačnih score-ova, AI računa ukupni risk level koji određuje prioritet u queue-u.

| Risk Level | Uslovi | Prioritet u queue |
| --- | --- | --- |
| **LOW** | Svi score < 0.3 | Normalan |
| **MEDIUM** | Bilo koji score 0.3 - 0.7 | Povišen |
| **HIGH** | Bilo koji score > 0.7 | Visok |
| **CRITICAL** | Više od 2 score > 0.7 | Urgent + obavezan pregled moderatora sa `can_manage_trust_tier` |

<a id="534-ai-blocking-logic"></a>

### 5.3.4 AI Blocking Logic

U ekstremnim slučajevima, AI može blokirati publikaciju sadržaja bez obzira na trust tier korisnika. Kada AI blokira listing, on prelazi u `hidden_by_system` — ovo je sigurnosna mjera za situacije kada je AI "veoma siguran" da je sadržaj problematičan.

| Tip problema | Blocking threshold | Primjena |
| --- | --- | --- |
| **Hate speech** | Parametar | Svi korisnici |
| **Adult explicit** | Parametar | Svi korisnici |
| **Violence explicit** | Parametar | Svi korisnici |
| **Illegal content** | Parametar | Svi korisnici |
| **Spam certainty** | Parametar | Samo pre-moderacija (Tier 0, 1) |

> ⚠️ **Napomena:** Blocking thresholds su konfiguracijski parametri (npr. `AI_BLOCK_HATE_THRESHOLD`, `AI_BLOCK_SPAM_THRESHOLD`). Preporučene početne vrijednosti su 0.95 za hate/adult/violence, 0.90 za illegal content, i 0.98 za spam. Vrijednosti se mogu prilagoditi na osnovu false positive rate-a.

> ⚠️ **Napomena o CRITICAL risk level:** Kada AI dodijeli CRITICAL risk level (više od 2 score-a > 0.7), stavka u queue-u zahtijeva pregled moderatora sa `can_manage_trust_tier` permisijom (vidi sekcija 5.3.3 i BR-MOD-30). Queue interfejs treba filtrirati ili označiti ove stavke kako bi bile dodijeljene odgovarajućem moderatoru.

Kada AI blokira sadržaj:

1. Listing prelazi u `hidden_by_system`
2. Listing nije vidljiv javno, bez obzira na trust tier
3. Ulazi u Urgent queue za hitni pregled
4. Moderator mora ručno pregledati i odlučiti: odobrava (→ `published`) ili odbija (→ `rejected`) ili uklanja (→ `removed`)

<a id="535-kako-moderator-vidi-ai-rezultate"></a>

### 5.3.5 Kako moderator vidi AI rezultate

AI rezultati se prikazuju kao "hints" u moderatorskom interfejsu — korisni, ali ne obavezujući.

```
┌─────────────────────────────────────────────────┐
│ Moderation Queue Item                           │
├─────────────────────────────────────────────────┤
│ Status: in_review / hidden_by_system            │
│ Priority: HIGH                                  │
│                                                 │
│ AI Hints:                                       │
│   🔴 Possible hate speech (0.82)                │
│   ⚠️ Contact info detected in description       │
│   ✓ No adult content                            │
│                                                 │
│ Suggested Action: "Review carefully"            │
│                                                 │
│ [Approve] [Request Changes] [Reject]            │
└─────────────────────────────────────────────────┘
```

<a id="536-komunikacija-pri-ai-blokadi"></a>

### 5.3.6 Komunikacija pri AI blokadi

Korisnici dobijaju različite poruke ovisno o trust tieru — korisnici višeg tiera zaslužuju transparentnije objašnjenje.

**Za korisnike Tier 2+ (post-moderacija):**

> "Vaš sadržaj je automatski zadržan zbog sigurnosne provjere. Moderator će pregledati u roku od 30 minuta. Ovo ne utiče na vaš trust tier."

**Za korisnike Tier 0, 1 (pre-moderacija):**

> "Vaš sadržaj je poslan na pregled. Obavijestit ćemo vas kada bude pregledan."

> 💡 **Praktična napomena:** AI je alat, ne sudija. Moderatori mogu i trebaju override-ati AI sugestije kada imaju dobar razlog. Međutim, listing u `hidden_by_system` zahtijeva eksplicitnu moderatorsku odluku — ne može se automatski vratiti u prethodni status.

* * *

<a id="54-moderatorske-akcije"></a>

## 5.4 Moderatorske akcije

Moderatori na CityInfo-u imaju jasno definirane ovlasti. Sistem koristi ravnu strukturu za svakodnevne operacije — svi moderatori imaju iste bazne moći za odobravanje, odbijanje i traženje izmjena. Za osjetljive akcije koje imaju veći uticaj na korisnike ili strukturu sadržaja, postoje granularne permisije koje Operator dodjeljuje odabranim moderatorima.

<a id="541-moderatorske-permisije"></a>

### 5.4.1 Moderatorske permisije

Svi moderatori dijele iste bazne ovlasti za svakodnevni rad. Dodatne permisije pokrivaju osjetljive akcije koje zahtijevaju veći nivo odgovornosti.

| Permisija | Šta omogućava | Ko dodjeljuje |
| --- | --- | --- |
| **Bazne ovlasti** (svi moderatori) | Approve, Reject, Request Changes, override AI sugestija, slanje poruka, blokiranje korisnika, sakrivanje listinga (`hidden_by_moderator`), trajno uklanjanje (`removed`) | Automatski sa Staff ulogom Moderator |
| `can_manage_trust_tier` | Postavljanje Tier 4 (Verified Partner), ručna degradacija na Tier 0 (Restricted), postavljanje `isVerifiedPublisher` flaga | Operator |
| `can_manage_tags` | Kreiranje, editovanje, deaktivacija, brisanje i spajanje tagova (EventTags i PlaceTags) | Operator |

> 💡 **Praktična napomena:** Ovo nije hijerarhija — moderator sa dodatnim permisijama nema "viši rang" od ostalih. To je jednostavno pristup akcijama koje zahtijevaju dodatno povjerenje. U praksi, to će biti moderatori sa više iskustva koji su pokazali dobar sud u donošenju odluka.

> ⚠️ **Napomena o local\_admin:** Staff sa ulogom `local_admin` ima šire sistemske ovlasti i može izvršavati sve akcije koje pokrivaju `can_manage_trust_tier` i `can_manage_tags` bez potrebe za dodatnim permisijama. Permisije su relevantne samo za Staff sa ulogom `moderator`. Detalji o matrici ovlasti po ulogama u [03 - Korisnici i pristup, sekcija 3.5](../project-specs/03-korisnici-i-pristup.md).

<a id="542-šta-moderator-može"></a>

### 5.4.2 Šta moderator MOŽE

✅ **Sadržaj:**

- Odobriti listing (→ `published`)
- Zatražiti izmjene (→ `changes_requested` ili `published_needs_changes`, zavisno od toka)
- Odbaciti listing (→ `rejected`)
- Sakriti listing (→ `hidden_by_moderator`)
- Trajno ukloniti listing (→ `removed` sa odgovarajućim `removedReason`)
- Override AI sugestije (osim `hidden_by_system` bez ručnog pregleda)
- Postaviti `verificationStatus = verified` na listingu (poslovna odluka moderatora — dokument nije obavezan)

✅ **Korisnici:**

- Blokirati korisnika (`accessStatus → blocked`) — uz opciju za sadržaj (vidi 5.4.4)
- Pregledati istoriju korisnikovih aktivnosti
- Pregledati i potvrditi/revertovati automatske degradacije

✅ **Sa** `can_manage_trust_tier` permisijom:

- Postaviti korisnika na Tier 4 (Verified Partner)
- Ručno degradirati korisnika na Tier 0 (Restricted)
- Postaviti `isVerifiedPublisher` flag na korisniku (Tier 3)

✅ **Sa** `can_manage_tags` permisijom:

- Kreirati, editovati, deaktivirati i brisati tagove (EventTags i PlaceTags)
- Pokrenuti spajanje tagova

✅ **Operacije:**

- Slati poruke autorima sadržaja
- Override odluke drugog moderatora (uz logging)

<a id="543-šta-moderator-ne-može"></a>

### 5.4.3 Šta moderator NE MOŽE

❌ Mijenjati sadržaj direktno (tekst, slike)  
❌ Brisati korisnike  
❌ Mijenjati sistemske postavke  
❌ Pristupati finansijskim podacima  
❌ Ignorisati `hidden_by_system` status bez pregleda  
❌ Upravljati kategorijama (ekskluzivna ovlast local\_admin-a)

<a id="544-blokiranje-korisnika"></a>

### 5.4.4 Blokiranje korisnika

Moderatori mogu blokirati korisnike koji predstavljaju prijetnju kvalitetu platforme. Blokiranje je ozbiljna mjera i koristi se samo kada je potrebno. Ponašanje se razlikuje za ručno blokiranje (moderator) i instant blokiranje (sistem).

<a id="ručno-blokiranje-moderator"></a>

#### Ručno blokiranje (moderator)

Moderator blokira korisnika na osnovu vlastite procjene ili nakon što sistem predloži blokadu.

| Situacija | Akcija | Napomena |
| --- | --- | --- |
| `TIER_REJECTED_THRESHOLD`\+ rejected sadržaja | Automatski prijedlog za block | Moderator odlučuje |
| Procjena moderatora | Ručni block | Dokumentovan razlog obavezan |

**Efekti na sadržaj — opcija moderatora:**

Pri ručnom blokiranju, moderator bira šta se dešava sa listinzima korisnika:

- **Opcija 1 — Listinzi ostaju vidljivi (default):** Aktivni listinzi (sa `isPublic = true`) ostaju javno vidljivi, ali korisnik ne može kreirati nove niti editovati postojeće dok je blokiran.
- **Opcija 2 — Listinzi se sakrivaju:** Svi aktivni listinzi prelaze u `hidden_by_system`. Pri odblokiranju, ovi listinzi se automatski vraćaju u `published`.

Moderator bira opciju na osnovu procjene — ako je blokada zbog neprimjerenih poruka ali je sadržaj kvalitetan, listinzi tipično ostaju vidljivi. Ako je blokada zbog lažnog sadržaja ili prevare, moderator sakriva sve.

<a id="instant-blokiranje-sistem"></a>

#### Instant blokiranje (sistem)

Sistem automatski blokira korisnika u slučajevima koji zahtijevaju hitnu reakciju — hate speech, nasilje, spam, malicious sadržaj. Kod instant blokiranja, **default ponašanje je sakrivanje sadržaja** jer je razlog blokiranja dovoljno ozbiljan da opravdava uklanjanje svih listinga.

| Situacija | Akcija | Default za sadržaj |
| --- | --- | --- |
| **Hate speech / violence** | Instant block | Svi listinzi prelaze u `hidden_by_system` |
| **Spam / malicious** | Instant block | Svi listinzi prelaze u `hidden_by_system` |

Instant block kreira stavku "Instant Block Review" u moderacijskom queue-u. Moderator pregleda situaciju i može:

- Potvrditi blokadu i ostaviti sadržaj u `hidden_by_system`
- Potvrditi blokadu ali reaktivirati sadržaj (→ `published`, ako je sadržaj sam po sebi kvalitetan)
- Revertovati blokadu u cijelosti — korisnik se odblokira, listinzi se vraćaju u `published` (ako je instant block bio false positive)

> 💡 **Praktična napomena:** Razlika u default-u između ručnog i instant blokiranja je namjerna. Kod ručnog, moderator već procjenjuje situaciju i svjesno bira. Kod instant, sistem reaguje na ozbiljnu prijetnju pa je sigurnije sakriviti sve i pustiti moderatora da odluči šta reaktivirati.

**Efekti blokiranja na korisnika (zajedničko za oba tipa):**

- `accessStatus` → `blocked`
- Korisnik ne može pristupiti sistemu (login onemogućen)
- Ako je korisnik ulogovan u trenutku blokiranja, automatski se odloguje
- Aktivne promocije se otkazuju bez povrata kredita

Detalji o `hidden_by_system` statusu i blokiranju korisnika opisani su u [04 - Sadržaj, sekcija 4.8](../project-specs/04-sadrzaj.md).

* * *

<a id="55-komunikacija-sa-korisnicima"></a>

## 5.5 Komunikacija sa korisnicima

Način na koji pričamo sa korisnicima direktno utiče na to kako percipiraju platformu. CityInfo koristi template poruke za konzistentnost, ali uvijek sa ljudskim dodirom. Poruke su na primarnom jeziku tenanta i imaju prijateljski ali profesionalan ton.

<a id="551-principi-komunikacije"></a>

### 5.5.1 Principi komunikacije

| Princip | Objašnjenje |
| --- | --- |
| **Pozitivan ton** | Počnemo sa zahvalom, završimo sa ohrabrenjem |
| **Konkretnost** | Kažemo tačno šta treba popraviti, ne općenito |
| **Akcija** | Svaka poruka ima jasan sljedeći korak |
| **Empatija** | Razumijemo da je korisnik uložio trud |

<a id="552-ton-komunikacije"></a>

### 5.5.2 Ton komunikacije

✅ **Dobro:**

- "Primijetili smo…"
- "Preporučujemo…"
- "Hvala što…"
- "Evo kako možete poboljšati…"

❌ **Izbjegavati:**

- "Morate…"
- "Zabranjeno je…"
- "Pogrešno ste…"
- "Vaš sadržaj je loš…"

<a id="553-template-biblioteka"></a>

### 5.5.3 Template biblioteka

<a id="template-1-nedostaju-osnovne-informacije"></a>

#### Template 1: Nedostaju osnovne informacije

```
Pozdrav {ime},

Hvala što doprinosite našoj platformi! Primijetili smo da 
vašem sadržaju "{naslov}" nedostaju neke važne informacije 
koje bi pomogle korisnicima:

{lista_nedostajućih}

Molimo vas da dodate ove informacije kako bi vaš sadržaj 
bio što korisniji.

Kada završite sa izmjenama, kliknite "Pošalji ponovo".

Hvala na razumijevanju!
```

<a id="template-2-kvalitet-fotografija"></a>

#### Template 2: Kvalitet fotografija

```
Pozdrav {ime},

Vaš sadržaj "{naslov}" ima odličan opis! Međutim, fotografije 
bi mogle biti kvalitetnije da bi bolje predstavile ono što nudite.

Preporučujemo:
• Minimalna rezolucija 800x600px
• Dobro osvjetljenje
• Fokus na glavnom subjektu
• Izbjegavajte watermark-ove

Radujemo se vašem poboljšanom sadržaju!
```

<a id="template-3-kontakt-informacije-u-opisu"></a>

#### Template 3: Kontakt informacije u opisu

```
Pozdrav {ime},

U opisu sadržaja "{naslov}" primijetili smo direktne kontakt 
informacije. Ove informacije trebaju biti u posebnim poljima, 
ne u opisu.

Molimo:
1. Uklonite telefon/email/web iz opisa
2. Dodajte ih u odgovarajuća polja forme
3. Opis koristite za predstavljanje sadržaja

Ovo pomaže korisnicima da lakše pronađu kontakt informacije 
na standardnom mjestu.

Hvala!
```

<a id="template-4-duplikat-sadržaja"></a>

#### Template 4: Duplikat sadržaja

```
Pozdrav {ime},

Izgleda da sadržaj "{naslov}" već postoji na našoj platformi:
{link_na_postojeći}

Ako ste vlasnik postojećeg sadržaja, molimo ažurirajte 
postojeći umjesto kreiranja novog.

Ako smatrate da ovo nije duplikat, molimo objasnite razliku 
u odgovoru.

Hvala na razumijevanju!
```

<a id="template-5-odbacivanje-kršenje-pravila"></a>

#### Template 5: Odbacivanje — kršenje pravila

```
Pozdrav {ime},

Nažalost, moramo odbaciti sadržaj "{naslov}" jer krši naša 
pravila korištenja:

{razlog}

Ova odluka je finalna za ovaj sadržaj. Međutim, pozivamo vas 
da kreirate novi sadržaj koji je u skladu sa našim smjernicama:
{link_na_smjernice}

Ako imate pitanja, slobodno nas kontaktirajte.

S poštovanjem,
Moderatorski tim
```

<a id="template-6-odobravanje-sa-savjetom"></a>

#### Template 6: Odobravanje sa savjetom

```
Pozdrav {ime},

Odlične vijesti! Vaš sadržaj "{naslov}" je odobren i sada je 
vidljiv svima! 🎉

Mali savjet za još bolju vidljivost:
{savjet}

Hvala što činite našu platformu boljom!
```

> 💡 **Praktična napomena:** Template-i su polazna tačka, ne konačni tekst. Moderatori mogu i trebaju personalizirati poruke, posebno kada situacija zahtijeva više konteksta. Međutim, ton i struktura ostaju konzistentni.

* * *

<a id="56-verifikacija-vlasništva"></a>

## 5.6 Verifikacija vlasništva

Korisnici mogu uploadovati dokumente koji dokazuju njihovo pravo upravljanja sadržajem — bilo da je riječ o događaju koji organizuju ili mjestu koje vode. Verifikacija nije obavezna za objavu, ali donosi značajne prednosti i pomaže u izgradnji povjerenja na platformi.

Mehanizam verifikacije se razlikuje po Trust Tier-u — od verifikacije pojedinačnih listinga za nove korisnike, preko flaga na nivou korisnika za provjerene izdavače, do potpuno automatskog statusa za ugovorne partnere.

<a id="561-zašto-verifikacija"></a>

### 5.6.1 Zašto verifikacija?

| Problem | Kako verifikacija pomaže |
| --- | --- |
| **Lažne objave** | Dokument dokazuje da osoba ima pravo objaviti sadržaj |
| **Kvalitet podataka** | Verifikovani sadržaji obično imaju tačnije informacije |
| **Povjerenje korisnika** | Posjetitelji više vjeruju verifikovanim mjestima |

<a id="562-verification-status-listinga"></a>

### 5.6.2 Verification status listinga

Svaki listing ima `verificationStatus` koji označava da li je vlasništvo nad sadržajem potvrđeno.

| Status | Značenje | Vizualni prikaz |
| --- | --- | --- |
| `unverified` | Vlasništvo nije potvrđeno | Bez oznake |
| `pending` | Dokumentacija čeka pregled moderatora | "U procesu verifikacije" |
| `verified` | Vlasništvo potvrđeno | ✓ Potvrđen vlasnik (badge) |

<a id="principi-vizuelnog-označavanja"></a>

#### Principi vizuelnog označavanja

Verification badge treba dizajnirati pažljivo jer ima uticaj na percepciju svih korisnika:

- **Suptilan dizajn:** Badge treba biti mali indikator, ne dominantan element kartice. Cilj je informacija, ne promocija.
- **Jasan značaj:** Badge znači "vlasnik je potvrdio svoj identitet", ne "platforma preporučuje ovaj sadržaj". Na detaljnoj stranici, korisnicima se objašnjava šta badge znači.
- **Terminologija:** Koristimo "Potvrđen vlasnik" umjesto "Verifikovano" da izbjegnemo implikaciju da je neverifikovano = nepouzdano.
- **Odsustvo badge-a nije negativan signal:** Ne prikazujemo "Nepotvrđeno" za listinge bez verifikacije — jednostavno ne prikazujemo ništa. Mnogi legitimni biznisi nemaju vremena ili resursa za verifikaciju i ne treba ih za to penalizovati.

> 💡 **Praktična napomena:** Za Places, verifikacioni status ima veću težinu jer predstavljaju stalne poslovne subjekte. Badge motiviše vlasnike da prođu verifikaciju, ali ne smije stvarati percepciju da su neverifikovani listinzi "manje legitimni". Vizualni detalji implementacije opisani su u [02 - Korisnički doživljaj](../project-specs/02-korisnicko-iskustvo.md).

<a id="563-verifikacija-po-trust-tier-u"></a>

### 5.6.3 Verifikacija po Trust Tier-u

Mehanizam verifikacije se razlikuje po Trust Tier-u korisnika. Ovo odražava činjenicu da korisnici višeg tiera već imaju uspostavljen odnos povjerenja sa platformom.

| Tier | Mehanizam | Nivo | Dokument |
| --- | --- | --- | --- |
| **0–2** | Na nivou listinga — moderator odlučuje per listing | Listing | Poslovna odluka moderatora |
| **3 (Established)** | Na nivou korisnika — `isVerifiedPublisher` flag | Korisnik | Poslovna odluka moderatora |
| **4 (Verified Partner)** | Automatska — ugovorni odnos | Korisnik | Nije potreban |

<a id="tier-02-verifikacija-po-listingu"></a>

#### Tier 0–2: Verifikacija po listingu

Moderator može postaviti `verificationStatus = verified` na pojedinačnom listingu. Dokument **nije obavezan** — moderator koristi vlastitu procjenu. Dokaz vlasništva može biti predočen na razne načine: uploadovan dokument, telefonski razgovor, email, lični kontakt, ili drugi kanal van sistema.

Ako korisnik uploada dokument, moderator ga pregleda kao dio standardne moderacije listinga. Ali i bez dokumenta, moderator može odobriti verified status ako ima dovoljno osnova za to.

<a id="tier-3-established-isverifiedpublisher-flag"></a>

#### Tier 3 (Established): `isVerifiedPublisher` flag

Za korisnike na Tier 3, moderacija funkcioniše sa samplingom — ne pregleda se svaki listing. Verifikacija na nivou pojedinačnog listinga tokom moderacije bi bila nekonzistentna jer listinzi koji ne uđu u sampling uzorak nikad ne bi imali priliku za verified status.

Zato za Tier 3 postoji `isVerifiedPublisher` flag na nivou korisnika. Kada moderator sa `can_manage_trust_tier` permisijom postavi ovaj flag:

- Svi **budući** listinzi tog korisnika automatski dobijaju `verificationStatus = verified`
- Svi **postojeći** aktivni listinzi tog korisnika retroaktivno dobijaju `verified` status (batch update)
- Flag se može ukloniti, što uklanja badge sa budućih objava (ali ne dira postojeće)

Moderator odlučuje da li će tražiti dokument ili ne — to je poslovna odluka. Primjer: vlasnik restorana koji već ima verifikovan Place i organizuje evente u svom prostoru može dobiti `isVerifiedPublisher` bez dodatnog dokumenta za svaki event. U drugim situacijama, moderator može zatražiti dokument ako smatra da je potrebno.

<a id="tier-4-verified-partner-automatska-verifikacija"></a>

#### Tier 4 (Verified Partner): Automatska verifikacija

Ugovorni odnos već uključuje potvrdu identiteta i prava na sadržaj. Svi listinzi Verified Partner-a automatski dobijaju `verificationStatus = verified` bez ikakvih dodatnih koraka.

<a id="564-prihvatljivi-dokumenti"></a>

### 5.6.4 Prihvatljivi dokumenti

Upload dokumenta je opcija za sve korisnike, ali nikad obavezan uslov za verified status. Dokumenti pomažu moderatoru u donošenju odluke, ali moderator može koristiti i druge izvore informacija.

**Za Event (događaj):**

- Ugovor sa lokacijom održavanja
- Dozvola za javni skup
- Ovlaštenje organizatora
- Potvrda zakupa prostora
- Službena korespondencija sa institucijom

**Za Place (mjesto):**

- Vlasnički list ili izvod iz zemljišnih knjiga
- Izvod iz sudskog/poslovnog registra
- Ugovor o zakupu prostora
- Ovlaštenje za upravljanje
- Rješenje o registraciji obrta/firme

**Tehnička ograničenja:**

| Parametar | Vrijednost |
| --- | --- |
| Dozvoljeni formati | PDF, JPG, PNG |
| Maksimalna veličina | 10 MB po dokumentu |
| Maksimalan broj | 3 dokumenta po listingu |
| Virus scan | Obavezan prije čuvanja |

<a id="565-workflow-verifikacije"></a>

### 5.6.5 Workflow verifikacije

```
flowchart TD
    A[Korisnik kreira listing] --> B{Uploada dokument?}
    B -->|Da| C[verificationStatus = pending]
    B -->|Ne| D[verificationStatus = unverified]
    C --> E[Moderator pregleda listing + dokument]
    D --> F[Moderator pregleda listing]
    E --> G{Dokument validan?}
    G -->|Da| H[verificationStatus = verified]
    G -->|Ne| I[Ostaje unverified + feedback]
    F --> J{Sumnja u legitimnost?}
    J -->|Da| K[Moderator traži dokumentaciju]
    J -->|Ne| L{Moderator ima osnova za verifikaciju?}
    L -->|Da| M[verificationStatus = verified, bez dokumenta]
    L -->|Ne| N[Nastavlja normalnu moderaciju]
    K --> O[Korisnik dobija notifikaciju]
    O --> P[Rok za dostavu dokumenta]
```

<a id="566-verifikacija-kao-dio-moderacije-listinga"></a>

### 5.6.6 Verifikacija kao dio moderacije listinga

Verifikacija nije odvojen proces — to je dio standardne moderacije listinga. Kada moderator pregleda listing:

1. Pregleda sadržaj listinga (kao i obično)
2. Pregleda priloženi dokument (ako postoji)
3. Donosi odluku o listingu (approve/reject/changes\_requested)
4. Odlučuje o verification statusu — na osnovu dokumenta, ili na osnovu drugih informacija/poznavanja situacije

**Moguće kombinacije:**

| Listing odluka | Osnova za verifikaciju | verificationStatus |
| --- | --- | --- |
| Approve (→ `published`) | Validan dokument | `verified` |
| Approve (→ `published`) | Moderator ima drugog osnova (poznaje biznis, email potvrda, itd.) | `verified` |
| Approve (→ `published`) | Nema osnova za verifikaciju | `unverified` |
| Approve (→ `published`) | Dokument nevalidan/nedovoljan | `unverified` + feedback korisniku |
| Reject (→ `rejected`) | Bilo koji | Nije relevantno (listing odbijen) |

<a id="567-listingdocument-entitet"></a>

### 5.6.7 ListingDocument entitet

Kompletna specifikacija ListingDocument entiteta — uključujući atribute, svrhe dokumenata (`purpose`), upload ograničenja i virus scanning workflow — definisana je u [04 - Sadržaj, sekcija 4.7](../project-specs/04-sadrzaj.md). Poglavlje 04 je jedini izvor istine (SSoT) za ovaj entitet.

Ovdje je relevantan sažetak za moderacijski kontekst:

- Dokumenti koriste `documentStatus` sa vrijednostima `pending`, `accepted`, `rejected` — terminološki odvojeno od `verificationStatus` na listingu da se izbjegne zabuna
- Dokument može biti `accepted` (moderator je pregledao i prihvatio), a listing `verified` (vlasništvo potvrđeno) — to su dva odvojena koncepta
- Listing može biti `verified` i bez ikakvih dokumenata — moderator koristi vlastitu procjenu
- Dokumenti su privatni — vidljivi samo vlasniku listinga i moderatorima
- Dokumenti stariji od 2 godine od zatvaranja listinga mogu biti obrisani radi GDPR usklađenosti

* * *

<a id="57-api-endpoints"></a>

## 5.7 API Endpoints

Ova sekcija navodi ključne API endpoint-e za moderacijski modul. Endpoint-i su grupisani po funkcionalnosti i opisani na konceptualnom nivou.

> ⚠️ **Napomena:** Ovo nije kompletna API specifikacija. Za detalje o autentifikaciji, autorizaciji, error handling-u i primjerima poziva, pogledati odvojenu API dokumentaciju.

<a id="571-queue-operacije"></a>

### 5.7.1 Queue operacije

| Metoda | Putanja | Opis |
| --- | --- | --- |
| `GET` | `/api/moderation/queue` | Dohvati listu sadržaja za moderaciju |
| `GET` | `/api/moderation/queue/stats` | Statistika queue-a (broj po prioritetu, prosječno vrijeme) |
| `GET` | `/api/moderation/queue/{itemId}` | Detalji jedne stavke u queue-u |
| `POST` | `/api/moderation/queue/{itemId}/claim` | Preuzmi stavku za moderaciju (lock) |
| `POST` | `/api/moderation/queue/{itemId}/release` | Oslobodi stavku (unlock) |

<a id="572-odluke-moderatora"></a>

### 5.7.2 Odluke moderatora

| Metoda | Putanja | Opis |
| --- | --- | --- |
| `POST` | `/api/moderation/listings/{id}/approve` | Odobri listing (→ `published`) |
| `POST` | `/api/moderation/listings/{id}/request-changes` | Vrati na doradu (→ `changes_requested` ili `published_needs_changes`) |
| `POST` | `/api/moderation/listings/{id}/reject` | Odbaci listing (→ `rejected`) |
| `POST` | `/api/moderation/listings/{id}/hide` | Sakrij listing (→ `hidden_by_moderator`) |
| `POST` | `/api/moderation/listings/{id}/remove` | Trajno ukloni listing (→ `removed` sa `removedReason`) |
| `POST` | `/api/moderation/listings/{id}/override` | Promijeni prethodnu odluku |

**Osnovni request shape za odluku:**

```
{
  reason: String (obavezno za reject, request-changes, hide, remove),
  templateId: String (opciono),
  internalNote: String (opciono),
  notifyUser: Boolean (default: true),
  verificationStatus: Enum (opciono, samo za approve — "verified" ili "unverified"),
  removedReason: Enum (obavezno za remove — "spam", "inappropriate", "duplicate")
}
```

<a id="573-ai-screening"></a>

### 5.7.3 AI Screening

| Metoda | Putanja | Opis |
| --- | --- | --- |
| `GET` | `/api/moderation/listings/{id}/ai-screening` | Dohvati AI rezultate za listing |
| `POST` | `/api/moderation/listings/{id}/ai-screening/rescan` | Ponovo pokreni AI scan |
| `POST` | `/api/moderation/listings/{id}/ai-override` | Override — moderator odobrava listing iz `hidden_by_system` |

<a id="574-korisničke-akcije"></a>

### 5.7.4 Korisničke akcije

| Metoda | Putanja | Opis |
| --- | --- | --- |
| `GET` | `/api/moderation/users/{id}/history` | Istorija moderacije korisnika |
| `POST` | `/api/moderation/users/{id}/trust-tier` | Promijeni trust tier (zahtijeva `can_manage_trust_tier` za Tier 0 i 4) |
| `POST` | `/api/moderation/users/{id}/block` | Blokiraj korisnika (uključuje opciju za sadržaj — `hidden_by_system` ili ostavi vidljivo) |
| `POST` | `/api/moderation/users/{id}/verified-publisher` | Postavi/ukloni `isVerifiedPublisher` flag (zahtijeva `can_manage_trust_tier`) |

<a id="575-sistemske-review-stavke"></a>

### 5.7.5 Sistemske review stavke

| Metoda | Putanja | Opis |
| --- | --- | --- |
| `POST` | `/api/moderation/reviews/{id}/confirm` | Potvrdi automatsku degradaciju ili instant block |
| `POST` | `/api/moderation/reviews/{id}/revert` | Revertuj automatsku degradaciju ili instant block |

<a id="576-statistike-i-reporting"></a>

### 5.7.6 Statistike i reporting

| Metoda | Putanja | Opis |
| --- | --- | --- |
| `GET` | `/api/moderation/stats/overview` | Pregled statistike moderacije |
| `GET` | `/api/moderation/stats/moderator/{id}` | Statistika po moderatoru |
| `GET` | `/api/moderation/stats/patterns` | Prepoznati obrasci (česti razlozi, problematični korisnici) |

<a id="577-verifikacija"></a>

### 5.7.7 Verifikacija

Verifikacija se odvija kroz standardne listing moderation endpointe (5.7.2). Traženje dokumentacije koristi isti `/request-changes` endpoint kao i bilo koji drugi zahtjev za izmjenama. API endpointi za dokumente listinga definisani su u [04 - Sadržaj, sekcija 4.10](../project-specs/04-sadrzaj.md).

* * *

<a id="poslovna-pravila"></a>

## Poslovna pravila

| Pravilo | Opis | Prioritet |
| --- | --- | --- |
| **BR-MOD-01** | Pre-moderacija unutar 2h, post-moderacija unutar 8h | Visok |
| **BR-MOD-02** | Svaka odluka osim approve mora imati obrazloženje | Visok |
| **BR-MOD-03** | Slični sadržaji moraju imati slične odluke (konzistentnost) | Srednji |
| **BR-MOD-04** | `TIER_REJECTED_THRESHOLD` rejected u `TIER_REJECTED_WINDOW_DAYS` dana → automatski pad na Restricted (Tier 0) sa obaveznim review-om moderatora | Visok |
| **BR-MOD-05** | Max pending objava za Tier 0/1 je `TIER_PRE_MOD_MAX_PENDING` (parametar) | Visok |
| **BR-MOD-06** | Komunikacija na primarnom jeziku tenanta | Visok |
| **BR-MOD-07** | Moderator ne može direktno mijenjati sadržaj | Visok |
| **BR-MOD-08** | Override prethodne odluke mora biti logovan | Srednji |
| **BR-MOD-09** | Listing u `hidden_by_system` zahtijeva eksplicitnu moderatorsku odluku — ne može se automatski vratiti | Kritičan |
| **BR-MOD-10** | Min 10 minuta između resubmission-a | Nizak |
| **BR-MOD-11** | Blokiranje korisnika zahtijeva dokumentovan razlog i izbor opcije za sadržaj | Visok |
| **BR-MOD-12** | Priloženi dokument mora biti pregledan kao dio moderacije listinga | Srednji |
| **BR-MOD-13** | Ako dokument nije dovoljan za verified status, korisniku se daje feedback | Srednji |
| **BR-MOD-14** | Ako korisnik ne odgovori na `changes_requested` u roku od `CHANGES_REQUESTED_TIMEOUT_DAYS` dana (preporučena početna vrijednost: 7), listing automatski prelazi u `rejected`. Sistem šalje reminder notifikaciju `CHANGES_REQUESTED_REMINDER_DAYS` dana prije isteka (preporučena početna vrijednost: 2 dana prije). Detalji u [04 - Sadržaj, sekcija 4.8](../project-specs/04-sadrzaj.md). | Srednji |
| **BR-MOD-15** | Dokumenti se automatski skeniraju na viruse prije čuvanja | Kritičan |
| **BR-MOD-16** | Trust tier napredovanje (1→2, 2→3) zahtijeva ispunjenje sva tri uslova istovremeno (min approved, min success rate, min starost računa) | Srednji |
| **BR-MOD-17** | Verified Partner (Tier 4) se postavlja isključivo ručno od moderatora sa `can_manage_trust_tier` permisijom | Visok |
| **BR-MOD-18** | Sampling procenti za Tier 3 i 4 su konfiguracijski parametri | Srednji |
| **BR-MOD-19** | Problem pronađen u sampling-u može rezultirati degradacijom tiera (Tier 3 → Tier 2) | Visok |
| **BR-MOD-20** | `changes_requested` ne utiče na Trust Tier ni procenat uspješnosti — broji se samo finalna odluka po listingu | Srednji |
| **BR-MOD-21** | Edit aktivnog listinga za Tier 0/1: listing prelazi u `in_review` (nevidljiv do ponovnog odobrenja); za Tier 2+: listing prelazi u `published_under_review` (ostaje vidljiv uz naknadni pregled) | Visok |
| **BR-MOD-22** | Pri odblokiranju korisnika, listinzi u `hidden_by_system` (nastali blokiranjem) se automatski vraćaju u `published` | Visok |
| **BR-MOD-23** | Instant block automatski prebacuje sve listinge korisnika u `hidden_by_system`; moderator može reaktivirati pri pregledu | Visok |
| **BR-MOD-24** | Svaka automatska degradacija tiera kreira review stavku u queue-u koju moderator mora potvrditi ili revertovati | Visok |
| **BR-MOD-25** | Ručna degradacija na Tier 0 i postavljanje Tier 4 zahtijeva `can_manage_trust_tier` permisiju | Visok |
| **BR-MOD-26** | `isVerifiedPublisher` flag na korisniku (Tier 3) automatski daje `verified` status svim listinzima tog korisnika; zahtijeva `can_manage_trust_tier` permisiju | Visok |
| **BR-MOD-27** | Tier 4 (Verified Partner) listinzi automatski dobijaju `verified` status bez dokumentacije | Visok |
| **BR-MOD-28** | Moderator može postaviti `verificationStatus = verified` na listingu bez uploadovanog dokumenta — dokument nije obavezan uslov, odluka je na moderatoru | Srednji |
| **BR-MOD-29** | Document status koristi `accepted` / `rejected` termine (odvojeno od listing `verificationStatus`) | Nizak |
| **BR-MOD-30** | CRITICAL AI risk level zahtijeva pregled moderatora sa `can_manage_trust_tier` permisijom | Visok |
| **BR-MOD-31** | Upravljanje tagovima zahtijeva `can_manage_tags` permisiju za moderatore; local\_admin ima inherentnu ovlast | Srednji |

* * *

<a id="metrike-i-kpi"></a>

## Metrike i KPI

| Metrika | Target | Mjerenje |
| --- | --- | --- |
| **Response Time - Pre-mod** | < 2h | percentil |
| **Response Time - Post-mod** | < 8h | percentil |
| **Decisions per Hour** | 15-20 | Prosjek po moderatoru |
| **Consistency Rate** | 90% | Slični sadržaji, iste odluke |
| **False Positive Rate (AI)** | < 5% | Approved nakon AI flag |
| **User Satisfaction** | 80% | Feedback nakon moderacije |
| **Resubmission Success** | 70% | Approved nakon changes\_requested |
| **Tier Progression Rate** | 60% | Korisnici koji napreduju 1→2 u 30 dana |
| **Sampling Issue Rate** | < 2% | Problemi pronađeni u sampling pregledu |
| **Auto-Degradation Revert Rate** | < 10% | Revertovane automatske degradacije |

> 💡 **Praktična napomena:** Metrike se prate sedmično i mjesečno. Ako konzistentno promašujemo targete, to je signal za review procesa ili povećanje kapaciteta — ne za spuštanje standarda. Nova metrika "Auto-Degradation Revert Rate" prati preciznost automatskog sistema — ako je revert rate visok, pragovi su preoštri.

* * *

<a id="napomene-za-implementaciju"></a>

## Napomene za implementaciju

<a id="trust-tier-model"></a>

### Trust Tier model

Korisnik ima `trustTier` atribut sa vrijednostima 0–4. Napredovanje je automatsko za nivoe 1→2 i 2→3, bazirano na parametrima definisanim u [03 - Korisnici i pristup](../project-specs/03-korisnici-i-pristup.md). Sva tri uslova (min approved, min success rate, min starost računa) moraju biti ispunjena istovremeno.

<a id="moderatorske-permisije"></a>

### Moderatorske permisije

Moderator entitet u Staff sistemu ima `permissions` polje (lista) koje može sadržavati:

- `can_manage_trust_tier` — omogućava postavljanje Tier 4, ručnu degradaciju na Tier 0, i upravljanje `isVerifiedPublisher` flagom
- `can_manage_tags` — omogućava kreiranje, editovanje, deaktivaciju, brisanje i spajanje tagova (EventTags i PlaceTags)

Permisije dodjeljuje Staff sa ulogom Operator. Lista permisija se može proširivati prema potrebama sistema. Staff sa ulogom `local_admin` ima inherentno sve ove ovlasti bez potrebe za eksplicitnim permisijama.

<a id="isverifiedpublisher-flag"></a>

### isVerifiedPublisher flag

Korisnik na Tier 3 može imati `isVerifiedPublisher = true`. Ovaj flag:

- Automatski postavlja `verificationStatus = verified` na sve nove listinge korisnika
- Retroaktivno ažurira postojeće aktivne listinge pri postavljanju flaga
- Može biti uklonjen od strane moderatora sa `can_manage_trust_tier` permisijom
- Automatski se uklanja ako korisnik bude degradiran ispod Tier 3

<a id="statusni-model-listingstatus"></a>

### Statusni model — `listingStatus`

Moderacija koristi jedinstveni `listingStatus` enum na Listing entitetu. Kompletna specifikacija sa svim tranzicijama opisana je u [04 - Sadržaj, sekcija 4.8](../project-specs/04-sadrzaj.md). Statusi relevantni za moderacijski kontekst:

- `in_review` — listing čeka moderatora (pre-mod tok za Tier 0/1, ili resubmit)
- `changes_requested` — moderator vratio listing korisniku, nevidljiv, čeka popravku
- `published` — listing odobren i vidljiv
- `published_under_review` — listing vidljiv ali čeka naknadni pregled (post-mod tok za Tier 2+)
- `published_needs_changes` — listing vidljiv, moderator traži blagu izmjenu
- `hidden_by_moderator` — moderator sakrio listing, čeka popravku + resubmit
- `hidden_by_system` — AI blokada ili korisnik blokiran; zahtijeva eksplicitnu moderatorsku odluku
- `rejected` — finalno odbijeno, terminalni status
- `removed` — trajno uklonjeno sa `removedReason`, terminalni status

> ⚠️ **Napomena:** Stari `moderationStatus` atribut (`none`, `pending_review`, `changes_requested`, `approved`, `rejected`) više ne postoji. Sve moderacijske tranzicije su integrisane u `listingStatus`. Za kompletnu tabelu tranzicija i Mermaid dijagram vidjeti Ch.04, sekcija 4.8.

<a id="ai-rezultati-storage"></a>

### AI rezultati storage

AI rezultati se čuvaju u zasebnoj tabeli/kolekciji sa sljedećim konceptualnim atributima:

| Atribut | Tip | Opis | Obavezno |
| --- | --- | --- | --- |
| id  | String | Jedinstveni identifikator | Da  |
| listingId | String | Referenca na listing | Da  |
| scanDate | DateTime | Vrijeme skeniranja | Da  |
| scores | Object | Score-ovi po kategorijama | Da  |
| riskLevel | Enum | LOW/MEDIUM/HIGH/CRITICAL | Da  |
| aiBlockingFlag | Boolean | Da li je AI blokirao listing (→ `hidden_by_system`) | Da  |
| flags | List | Lista detektovanih problema | Ne  |
| suggestedAction | String | Preporučena akcija | Ne  |
| version | String | Verzija AI modela | Da  |

> ⚠️ **Napomena:** Lista atributa nije konačna i može se proširivati prema potrebama sistema.

<a id="cache-sloj"></a>

### Cache sloj

Za performanse u moderatorskom interfejsu, AI rezultati se keširaju:

- TTL: 24 sata (dok traje aktivna moderacija)
- Invalidacija: pri novom scanu ili promjeni statusa
- Key pattern: `ai_scan:{listingId}:latest`

* * *

<a id="changelog"></a>

## Changelog

| Verzija | Datum | Opis |
| --- | --- | --- |
| 2.0 | 1.4.2026 | **Migracija na jednostatus model.** Sve reference na stari dvostatus model (`moderationStatus` + `lifecycleStatus` + `closedReason`) zamijenjene novim `listingStatus` enum-om sa 13 vrijednosti. Ključne promjene: sekcija 5.1.3 (pre/post-mod opisi ažurirani sa `in_review`/`published_under_review`), sekcija 5.2.3 (moderatorske odluke mapiraju na `listingStatus` tranzicije), sekcija 5.2.5 (edit tok sa novim statusima), sekcija 5.3.1/5.3.4 (AI blocking → `hidden_by_system`), sekcija 5.4 (moderatorske akcije uključuju `hidden_by_moderator` i `removed`; blokiranje korisnika koristi `hidden_by_system` umjesto `OWNER_BLOCKED` closedReason), sekcija 5.7 (novi endpointi `/hide` i `/remove`), BR-MOD-09/14/21/22/23 ažurirani sa novim statusima, napomene za implementaciju potpuno revidirane. |
| 1.7 | 29.3.2026 | Dodana permisija `can_manage_tags` u sekciju 5.4.1 (tabela permisija) i 5.4.2 (šta moderator može). Sekcija 5.4.3 proširena — upravljanje kategorijama eksplicitno navedeno kao ograničenje. Napomena o local\_admin ažurirana da uključi obje permisije. BR-MOD-31 dodan. Implementacijske napomene ažurirane sa `can_manage_tags`. |
| 1.6 | 28.3.2026 | Status → Završeno. |
| 1.5 | Mart 2026 | BR-MOD-14 ažuriran sa eksplicitnim parametrima (`CHANGES_REQUESTED_TIMEOUT_DAYS`, `CHANGES_REQUESTED_REMINDER_DAYS`) i referencom na Ch.04. Sekcija 5.7.7 referenca ispravljena na 4.10. Povezani dokumenti ažurirani sa referencama na renumerisane sekcije Ch.04. |
| 1.4 | Mart 2026 | Restauracija + izmjene. Sekcija 5.6.7 → referenca na ListingDocument SSoT u poglavlju 04. |

* * *