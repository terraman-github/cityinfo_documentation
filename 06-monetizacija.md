---
title: "06 - MONETIZACIJA"
confluence_page_id: "240222244"
---

# 06 - MONETIZACIJA

> **Verzija:** 1.5  
> **Datum:** 3.4.2026  
> **Status:** Završeno ✅

* * *
## Pregled poglavlja

CityInfo koristi **freemium model** sa tri glavna prihoda: promocije listinga, display oglašavanje i franšizno poslovanje. Filozofija je jednostavna — korisnici kupuju kredite unaprijed, a zatim ih troše na usluge bez ponovnog prolaska kroz payment proces. Ovaj pristup smanjuje friction pri svakoj akciji i pomaže konverziji.

Monetizacija je dizajnirana da bude fer prema malim organizatorima (pristupačne cijene, jasne koristi) dok istovremeno omogućava skaliranje za veće korisnike kroz volume popuste i premium opcije. Franšizno poslovanje otvara vrata internacionalnom tržištu i potencijalno predstavlja najveći revenue stream.

| Sekcija | Opis | Ciljna publika |
| --- | --- | --- |
| **6.1 Kreditni sistem** | Wallet, kupovina, trošenje | Product + Dev |
| **6.2 Promocije listinga** | Standard, Premium, Homepage opcija, Refresh, AutoRenew, Pause/Resume | Product + Ops |
| **6.3 Display oglašavanje** | MVP pristup — ručno postavljeni banneri | Ops + Dev |
| **6.4 Franšizno poslovanje** | Licenciranje platforme partnerima | Business + Ops |
| **6.5 Pricing strategija** | Cijene, paketi, konverzije | Product |
| **6.6 API Endpoints** | Lista endpointa za monetizaciju | Dev |

* * *
## 6.1 Kreditni sistem
### 6.1.1 Koncept i filozofija

Kreditni sistem omogućava **prepaid model** gdje korisnici jednom kupe kredite, a zatim ih koriste za različite usluge na platformi. Umjesto da korisnik prolazi kroz payment formu svaki put kad želi nešto promovirati, jednostavno potroši kredite koje već ima na računu.

Ovaj pristup donosi nekoliko ključnih prednosti: brža aktivacija usluga (instant umjesto čekanja payment processinga), bolja kontrola troškova (korisnik vidi tačno koliko ima i troši), te psihološki "lock-in" efekat koji povećava retention — krediti na računu su razlog za povratak.

**Praktična napomena:** Platforma koristi jedinstvenu valutu (krediti) umjesto realnih novčanih iznosa za interne operacije. Konverzija u lokalnu valutu se dešava samo pri kupovini paketa.
### 6.1.2 Wallet koncept

Svaki korisnik ima virtualni novčanik (wallet) koji prati trenutno stanje kredita. Wallet se automatski kreira pri registraciji sa početnim stanjem od 0 kredita. Sva trošenja i dopune se evidentiraju kroz transakcijski log koji omogućava potpunu transparentnost.

| Aspekt | Opis |
| --- | --- |
| **Početno stanje** | 0 kredita pri registraciji |
| **Minimalni balans** | Ne može biti negativan |
| **Valuta** | Krediti (interna jedinica) |
| **Vidljivost** | Uvijek prikazano u header-u aplikacije |
| **Historija** | Kompletna historija transakcija dostupna korisniku |
### 6.1.3 CreditPackage entitet

Paketi kredita definišu šta korisnici mogu kupiti. Svaki tenant može imati prilagođene pakete, ali tipično se koristi standardni set sa progresivnim popustima za veće količine.

| Naziv | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| packageId | String | Jedinstveni identifikator paketa | ✅   | —   |
| tenantId | String | Poveznica na grad/region | ✅   | Paketi su tenant-specifični |
| name | String | Naziv paketa za prikaz | ✅   | npr. "Standard", "Premium" |
| credits | Number | Broj kredita u paketu | ✅   | —   |
| price | Money | Cijena paketa | ✅   | U lokalnoj valuti |
| currency | String | Valuta (ISO kod) | ✅   | npr. "BAM", "EUR" |
| discount | Number | Popust u procentima | ❌   | 0 ako nema popusta |
| isActive | Boolean | Da li je dostupan za kupovinu | ✅   | —   |
| validityDays | Number | Koliko dana krediti važe | ❌   | NULL = ne ističu |
| isPromoted | Boolean | Da li je istaknut u UI | ❌   | Za "best value" označavanje |
| sortOrder | Number | Redoslijed prikaza | ✅   | —   |
| createdAt | DateTime | Datum kreiranja | ✅   | —   |

> 📝 **Napomena:** Lista atributa nije konačna i može se proširivati prema potrebama proizvoda.
#### Standardni paketi (primjer)

| Paket | Krediti | Cijena (BAM) | Popust | Po kreditu |
| --- | --- | --- | --- | --- |
| Starter | 100 | 10  | 0%  | 0.10 |
| Standard | 500 | 45  | 10% | 0.09 |
| Premium | 1000 | 80  | 20% | 0.08 |
| Business | 5000 | 350 | 30% | 0.07 |

**Praktična napomena:** Progresivni popusti su dizajnirani da ohrabre veće kupovine. "Best value" badge se tipično stavlja na srednji paket koji ima najbolji omjer cijene i popusta.
### 6.1.4 CreditTransaction entitet

Svaka promjena stanja wallet-a evidentira se kroz transakciju. Ovo omogućava potpunu reviziju troškova i zarade, kao i rješavanje eventualnih sporova sa korisnicima.

| Naziv | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| transactionId | String | Jedinstveni identifikator | ✅   | —   |
| userId | String | Korisnik koji vrši transakciju | ✅   | —   |
| type | Enum | Tip transakcije | ✅   | Vidi tabelu ispod |
| amount | Number | Broj kredita (+/-) | ✅   | Pozitivno za dopunu, negativno za trošenje |
| balanceBefore | Number | Stanje prije transakcije | ✅   | Za audit |
| balanceAfter | Number | Stanje poslije transakcije | ✅   | Za audit |
| referenceType | String | Tip reference | ❌   | npr. "Promo", "Package" |
| referenceId | String | ID povezanog entiteta | ❌   | —   |
| description | String | Opis transakcije | ✅   | Čitljiv opis za korisnika |
| createdAt | DateTime | Vrijeme transakcije | ✅   | —   |

> 📝 **Napomena:** Lista atributa nije konačna i može se proširivati prema potrebama proizvoda.
#### Tipovi transakcija

| Tip | Opis | Amount |
| --- | --- | --- |
| **purchase** | Kupovina kredita |     |
| **promo\_purchase** | Troškovi promocije |     |
| **promo\_autorenew** | AutoRenew aktivacija |     |
| **refund** | Povrat kredita |     |
| **admin\_credit** | Admin dodaje kredite |     |
| **admin\_debit** | Admin oduzima kredite |     |
| **reward** | Nagrada (loyalty, bonus) |     |
### 6.1.5 PaymentHistory entitet

Zapis o stvarnim finansijskim transakcijama (kupovinama paketa kredita). Odvojen je od CreditTransaction jer prati različite informacije — PaymentHistory se bavi novcem, CreditTransaction se bavi kreditima.

| Naziv | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| paymentId | String | Jedinstveni identifikator | ✅   | —   |
| userId | String | Korisnik koji plaća | ✅   | —   |
| packageId | String | Kupljeni paket | ✅   | —   |
| amount | Money | Iznos plaćanja | ✅   | —   |
| currency | String | Valuta | ✅   | —   |
| paymentMethod | Enum | Metoda plaćanja | ✅   | card/paypal/bank |
| status | Enum | Status plaćanja | ✅   | pending/success/failed |
| gatewayResponse | Object | Sirovi response od gateway-a | ❌   | Za debugging |
| processedAt | DateTime | Vrijeme procesiranja | ❌   | —   |
| createdAt | DateTime | Vrijeme inicijacije | ✅   | —   |

> 📝 **Napomena:** Lista atributa nije konačna i može se proširivati prema potrebama proizvoda.
### 6.1.6 Workflow kupovine kredita

```
flowchart TD
    A[Korisnik bira paket] --> B[Payment forma]
    B --> C[Gateway procesiranje]
    C --> D{Uspješno?}
    D -->|Ne| E[Retry ili otkaz]
    D -->|Da| F[Kreiraj PaymentHistory]
    F --> G[Kreiraj CreditTransaction]
    G --> H[Update wallet balance]
    H --> I[Pošalji notifikaciju]
    I --> J[Redirect na wallet]
```

> 📝 **Napomena:** Backend validira dostupnost i status paketa prije procesiranja, ali u normalnom toku korisnik vidi samo aktivne pakete pa ova provjera rijetko pada. Cijeli proces od PaymentHistory do wallet update-a je atomska transakcija — ili se sve desi, ili se ništa ne desi.
### 6.1.7 Ključna poslovna pravila

| Pravilo | Opis | Prioritet |
| --- | --- | --- |
| **Minimalni balans** | Wallet balance ne može biti negativan | Kritičan |
| **Atomske transakcije** | Svaka promjena balansa mora imati CreditTransaction zapis | Kritičan |
| **Nema refunda** | Krediti su non-refundable nakon kupovine | Visok |
| **Promocije pri blokiranju** | Ako korisnik bude blokiran, aktivne promocije se otkazuju bez povrata | Visok |

* * *
## 6.2 Promocije listinga
### 6.2.1 Koncept i svrha

Promocije omogućavaju listing-ima bolju vidljivost kroz plaćeno isticanje. Postoje dva osnovna tipa — Standard i Premium — sa različitim nivoima vidljivosti i cijenom. Dodatno, Premium promocije mogu uključiti opciju prikaza na naslovnoj stranici.

Ključna razlika: Standard promocije se **miješaju** sa običnim listinzima (samo su vizuelno istaknute), dok Premium promocije imaju **garantovanu poziciju na vrhu** liste u svojoj kategoriji.
### 6.2.2 Promo entitet

| Naziv | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| promoId | String | Jedinstveni identifikator | ✅   | —   |
| targetType | Enum | Tip listinga | ✅   | event/place |
| targetId | String | ID promoviranog listing-a | ✅   | —   |
| promoType | Enum | Tip promocije | ✅   | standard/premium |
| status | Enum | Status promocije | ✅   | Vidi ispod |
| startDate | DateTime | Početak promocije | ✅   | —   |
| endDate | DateTime | Kraj promocije | ✅   | —   |
| pausedAt | DateTime | Kad je pauzirana | ❌   | NULL ako nije pauzirana |
| remainingDays | Number | Preostali dani pri pauziranju | ❌   | Kalkulisano pri pauzi |
| showOnHomepage | Boolean | Premium opcija za naslovnu | ✅   | Samo za premium |
| autoRenewEnabled | Boolean | Da li je AutoRenew aktivan | ✅   | —   |
| autoRenewInterval | Enum | Interval osvježavanja | ❌   | 3h/8h/24h, NULL ako nije enabled |
| nextAutoRenewAt | DateTime | Sljedeće automatsko osvježavanje | ❌   | NULL ako nije enabled |
| autoRenewsCompleted | Number | Broj izvršenih osvježavanja | ❌   | Za statistiku |
| createdBy | String | Korisnik koji je kreirao | ✅   | —   |
| createdAt | DateTime | Vrijeme kreiranja | ✅   | —   |

> 📝 **Napomena:** Lista atributa nije konačna. Troškovi promocije se prate kroz CreditTransaction entitet sa odgovarajućim referenceType i referenceId.
#### Status promocije

| Status | Opis |
| --- | --- |
| **active** | Trenutno aktivna — listing je promoviran |
| **paused** | Privremeno pauzirana — efekat promocije je zamrznut |
| **expired** | Istekla — endDate je prošao |
| **cancelled** | Otkazana (npr. listing uklonjen/`removed`, korisnik blokiran — `hidden_by_system`) |

> 📝 **Napomena za V1:** Promocije se aktiviraju instant pri kreiranju (prepaid model). Scheduled promotions (zakazivanje unaprijed) može se dodati u budućim verzijama.
### 6.2.3 Standard vs Premium promocija

Izbor između Standard i Premium promocije zavisi od budžeta i cilja. Standard je pristupačniji i pogodan za kontinuiranu prisutnost, dok Premium garantuje maksimalnu vidljivost za važne objave.

| Karakteristika | Standard | Premium | Premium + Homepage |
| --- | --- | --- | --- |
| **Cijena/dan** | 20 kredita | 40 kredita | 60 kredita |
| **Pozicija u listi** | Izmiješana sa običnim | Izdvojena na vrhu | Izdvojena na vrhu |
| **Sortiranje** | Po sortDate kao obični | Uvijek na vrhu kategorije | Uvijek na vrhu kategorije |
| **Vizuelni highlight** | Blagi (border, pozadina) | Jak + "Premium" badge | Jak + "Premium" + "Featured" badge |
| **Homepage prioritet** | ❌   | ❌   | ✅ Apsolutni prioritet |
| **Statistike** | Osnovne (views, clicks) | Detaljne + demographics | Detaljne + homepage stats |
#### Kako izgleda sortiranje u praksi

**U kategoriji:**

Premium listinzi su uvijek izdvojeni na vrhu i **međusobno su sortirani po** `sortDate` (noviji prvo). Ispod premium sekcije, Standard promocije i obični listinzi su izmiješani — također sortirani po `sortDate`.

```
═══════════════════════════════════
PREMIUM SEKCIJA (uvijek na vrhu, sortirani po sortDate — noviji prvo):
[⭐ PREMIUM] Event 1 (sortDate: danas 14:00)
[⭐ PREMIUM+HOME] Event 2 (sortDate: danas 10:00)  
═══════════════════════════════════

STANDARD + OBIČNI (izmiješani po sortDate):
Regular Event 3 (sortDate: danas 16:00)
[STANDARD] Event 4 (sortDate: danas 15:00) ← vizuelno istaknut
Regular Event 5 (sortDate: danas 12:00)
```

**Na naslovnoj stranici:**

```
═══════════════════════════════════
GRUPA 1 - Premium sa "Prikaži na naslovnoj":
[⭐🏠 PREMIUM+HOME] Event A
[⭐🏠 PREMIUM+HOME] Event B
═══════════════════════════════════

GRUPA 2 - Svi ostali (ako ima mjesta):
[⭐ PREMIUM] Event C
Regular Event D
[STANDARD] Event E
```

**Praktična napomena:** Standard promocije su dobar izbor za kontinuiranu prisutnost uz manji budžet. Premium + Homepage je rezervisan za najvažnije objave gdje je kritično da ih vidi što više ljudi. AutoRenew ima posebnu vrijednost za Premium promocije jer osvježavanjem `sortDate` utječe na poziciju i unutar premium sekcije.
### 6.2.4 Osvježavanje pozicije (Refresh i AutoRenew)

Osvježavanje `sortDate` je mehanizam koji listing "podiže" na višu poziciju kao da je tek objavljen. Postoje dva načina: besplatni ručni refresh i plaćeni automatski refresh (AutoRenew) kroz promociju.
#### Ručni refresh (besplatno, svi korisnici)

- Dostupan jednom u 24 sata
- Samo za aktivne listinge
- Korisnik klikne "Osvježi poziciju" → sortDate = NOW()
- Listing ima polje `lastManualRefreshAt` koje prati kad je korisnik zadnji put ručno osvježio poziciju — koristi se za provjeru 24h cooldown-a
#### AutoRenew kroz promociju (plaćeno)

AutoRenew automatski osvježava `sortDate` na odabranom intervalu. Ovo je **plaćena automatizacija** istog mehanizma koji korisnici mogu koristiti ručno, ali bez 24h ograničenja — plaćeni AutoRenew može osvježavati poziciju do 8× dnevno (3h interval).

| Interval | Osvježavanja/dan | Use case |
| --- | --- | --- |
| **24h** | 1× dnevno | Kontinuirana prisutnost |
| **8h** | 3× dnevno | Važni eventi |
| **3h** | 8× dnevno | Kritični eventi |

> ⚠️ **Draft napomena — pricing AutoRenew-a:** Način obračuna cijene za AutoRenew opciju (množitelji bazne cijene, fiksni dodaci, ili drugi model) **još nije konačno definisan**. Vrijednosti navedene u sekciji 6.5 su ilustrativni placeholderi i biće finalizirane prije MVP-a. Princip ostaje: češći interval = veća cijena.

**Praktična napomena:** AutoRenew ima smisla za promocije duže od par dana. Za jednodnevnu promociju, ručni refresh je obično dovoljan. Korisnik koji ima aktivnu promociju sa AutoRenew može i dalje ručno refreshati (ako želi dodatno osvježavanje), ali to rijetko ima smisla.
### 6.2.5 Pauziranje i nastavak promocije

Korisnik može privremeno pauzirati aktivnu promociju. Ovo je korisno kad korisnik želi "sačuvati" preostale dane — npr. restoran zatvoren za renovaciju, ili organizator želi sačekati bolji termin.
#### Šta se dešava pri pauziranju

Kada korisnik pauzira promociju:

- Status prelazi u `paused`, `pausedAt` se postavlja na trenutno vrijeme
- **sortDate se ne mijenja** — listing zadržava svoju trenutnu poziciju, ali gubi promotivno isticanje (vizuelno i poziciono)
- **AutoRenew se suspenduje** — `nextAutoRenewAt` se briše, background job preskače ovaj listing
- **Listing gubi promotivni status** u sortiranju — tretira se kao običan listing dok je promocija pauzirana
- **endDate se zamrzava** — sistem bilježi preostale dane (`remainingDays`) i ne troši ih dok je promocija pauzirana
- **Krediti se ne vraćaju** — promocija je prepaid, pauza ne generira refund
#### Šta se dešava pri nastavku

Kada korisnik nastavi (resume) pauziranu promociju:

- Status se vraća na `active`
- **endDate se preračunava** na osnovu `remainingDays` — npr. ako je pauzirana sa 5 preostalih dana, novi endDate je NOW() + 5 dana
- **AutoRenew se reaktivira** (ako je bio enabled) — `nextAutoRenewAt` se postavlja na osnovu intervala
- **sortDate se osvježava** na NOW() — listing se efektivno vraća na vrh kao da je tek promoviran
- `pausedAt` i `remainingDays` se čiste
#### Ograničenja

| Pravilo | Opis |
| --- | --- |
| **Samo korisnik može pauzirati** | Staff ne može pauzirati promocije (ali može otkazati) |
| **Minimalno trajanje pauze** | Nema — korisnik može odmah nastaviti |
| **Maksimalno trajanje pauze** | `PROMO_MAX_PAUSE_DAYS` (parametar — preporučena početna vrijednost: 30 dana). Nakon isteka, promocija automatski prelazi u `expired`. |
| **Jedna pauza za vrijeme trajanja** | Bez ograničenja broja pauza — korisnik može pauzirati i nastaviti proizvoljan broj puta |

> **💡 Praktična napomena:** Pauza je korisna funkcija za korisnike koji su kupili višednevnu promociju ali ne mogu iskoristiti sve dane zaredom. Bez nje, korisnik gubi plaćene dane — što dovodi do frustracije i smanjene spremnosti za buduće kupovine.
### 6.2.6 Workflow promocija

```
flowchart TD
    A[Korisnik bira promociju] --> B[Provjera listing statusa]
    B --> C{Listing aktivan?}
    C -->|Ne| D[Prikaži error: Samo aktivni listinzi]
    C -->|Da| E[Provjera kredita]
    E --> F{Dovoljno kredita?}
    F -->|Ne| G[Redirect na kupovinu kredita]
    F -->|Da| H[Instant aktivacija]
    H --> I[CreditTransaction: naplaćivanje]
    I --> J{AutoRenew?}
    J -->|Da| K[Kreiraj PromoAutoRenew]
    K --> L[CronJob aktivira renewal]
    J -->|Ne| M[Jednokratna promocija]
    L --> N[Osvježava sortDate]
    M --> O[Promocija završena]
    N --> P{Još renewal-a?}
    P -->|Da| N
    P -->|Ne| O
```
### 6.2.7 Ključna poslovna pravila

| Pravilo | Opis | Prioritet |
| --- | --- | --- |
| **Samo javno vidljivi listinzi** | Promocija moguća samo za listing sa `listingStatus` u jednom od javno vidljivih statusa: `published`, `published_under_review` ili `published_needs_changes` | Visok |
| **Prepaid model** | Sve promocije se naplaćuju unaprijed iz wallet balansa | Kritičan |
| **No refund policy** | Promocije su non-refundable nakon aktivacije | Visok |
| **Jedna aktivna po listingu** | Listing može imati samo jednu aktivnu promociju | Visok |
| **Homepage samo za Premium** | Opcija "Prikaži na naslovnoj" dostupna samo za Premium | Visok |
| **Vezano za listing status** | Ako listing izgubi javnu vidljivost (uklonjen, istekao ili sakriven — uključujući `removed` sa bilo kojim `removedReason`, npr. `rejected`), promocija automatski prestaje bez refunda. **Izuzetak:** pri prelasku u `canceled`, promocija se **pauzira** (ne prestaje) — pri ponovnoj aktivaciji (`published`), promocija se automatski nastavlja sa preostalim danima. Detalji u Ch.04, sekcija 4.8. | Visok |
| **Ručni refresh cooldown** | Korisnik može ručno osvježiti poziciju jednom u 24h (besplatno) | Srednji |
| **AutoRenew zaobilazi cooldown** | Plaćeni AutoRenew nije ograničen 24h cooldown-om | Srednji |
| **Pauza zamrzava dane** | Pri pauziranju, preostali dani se čuvaju i troše se tek nakon nastavka | Visok |
| **Maksimalna pauza** | Pauzirana promocija automatski ističe nakon `PROMO_MAX_PAUSE_DAYS` dana | Srednji |
| **Resume osvježava sortDate** | Pri nastavku, sortDate se osvježava na NOW() | Srednji |

* * *
## 6.3 Display oglašavanje
### 6.3.1 MVP pristup

Display oglašavanje u MVP-u koristi **maksimalno pojednostavljen model**: Staff ručno postavlja banner oglase kroz admin panel, a sistem ih prikazuje na predefinisanim pozicijama. Nema self-service-a za oglašivače, nema CPC biddinga, nema targetinga po kategorijama, i nema fraud detectiona.

Razlog za ovaj pristup: u ranoj fazi platforma nema dovoljno traffica ni oglašivača da opravda kompleksan ad-serving sistem. Ručno postavljanje daje potpunu kontrolu timu i dovoljan je za prvih 5–10 oglašivača koji se očekuju u prvim mjesecima.

**Praktična napomena:** Display oglašavanje će vjerovatno biti primarni izvor prihoda u ranoj fazi — dok korisnici još ne vide dovoljno traffica da investiraju u promocije listinga, lokalni biznisi su spremni platiti banner ako im se pokaže posjećenost. Jednostavnost ovog modela omogućava brz go-to-market.
### 6.3.2 DisplayAd entitet

Svaki banner oglas je jednostavan zapis koji Staff kreira i održava. Nema kampanja, biddinga ni složene logike — samo slika, link, zona i vremenski okvir.

| Naziv | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| adId | String | Jedinstveni identifikator | ✅   | —   |
| tenantId | String | Poveznica na grad/region | ✅   | —   |
| name | String | Interni naziv oglasa | ✅   | Za Staff pregled, nije javno vidljiv |
| bannerUrl | String | URL do banner slike | ✅   | —   |
| targetUrl | String | Destination URL (kuda vodi klik) | ✅   | —   |
| zoneId | String | Pozicija za prikaz | ✅   | Vidi tabelu zona |
| isActive | Boolean | Da li se oglas prikazuje | ✅   | Staff uključuje/isključuje po potrebi |
| sortOrder | Number | Prioritet prikaza unutar zone | ✅   | Manji broj = veći prioritet |
| startDate | DateTime | Od kad se prikazuje | ❌   | NULL = odmah aktivan |
| endDate | DateTime | Do kad se prikazuje | ❌   | NULL = dok se ručno ne isključi |
| impressions | Number | Broj prikaza | ✅   | Automatski se inkrementira |
| clicks | Number | Broj klikova | ✅   | Automatski se inkrementira |
| createdBy | String | Staff koji je kreirao | ✅   | —   |
| createdAt | DateTime | Vrijeme kreiranja | ✅   | —   |

> 📝 **Napomena:** Lista atributa nije konačna i može se proširivati prema potrebama proizvoda.
### 6.3.3 Reklamne zone

Platforma ima predefinisane pozicije za prikazivanje oglasa. Za MVP koristimo smanjeni set zona — dovoljno za pokrivanje ključnih pozicija bez prevelike kompleksnosti.

| Zone ID | Naziv | Lokacija | Dimenzije | Tip |
| --- | --- | --- | --- | --- |
| Z-001 | Header Banner | Vrh stranice | 728×90 | Leaderboard |
| Z-002 | Sidebar | Desni sidebar | 300×250 | Medium Rectangle |
| Z-003 | In-Feed | Između listinga | 600×100 | Custom |
| Z-004 | Mobile Banner | Mobile vrh ili dno | 320×50 | Mobile Banner |

**Praktična napomena:** Zone su konfigurisane po tenantu i mogu se dodavati ili mijenjati bez promjene koda. In-Feed (Z-003) je najvrednija pozicija jer se pojavljuje direktno među sadržajem.
### 6.3.4 Logika prikaza

Prikaz oglasa u MVP-u je namjerno jednostavan:

1. Za traženu zonu, dohvati sve aktivne oglase čiji datumski okvir uključuje danas (ili nemaju definisan okvir)
2. Sortiraj po `sortOrder` (manji broj = veći prioritet)
3. Ako ima više oglasa za istu zonu, prikaži onaj sa najvećim prioritetom; ostale rotiraj pri svakom učitavanju stranice (round-robin)
4. Ako za zonu nema aktivnog oglasa, ne prikazuj ništa (zona je prazna)

**Praktična napomena:** Ovaj pristup ne zahtijeva nikakav scoring, bidding ni fraud detection. Staff ima potpunu kontrolu — ako neki oglas treba biti istaknutiji, jednostavno mu postavi niži `sortOrder`.
### 6.3.5 Ključna poslovna pravila

| Pravilo | Opis | Prioritet |
| --- | --- | --- |
| **Samo Staff postavlja oglase** | Korisnici ne mogu sami kreirati display oglase u MVP-u | Visok |
| **Impressions i clicks se broje** | Osnovne metrike se prate automatski za izvještavanje prema oglašivačima | Visok |
| **Datumski okvir** | Oglas se prikazuje samo unutar definisanog perioda (ako je definisan) | Srednji |
| **Prazna zona je OK** | Ako nema oglasa za zonu, zona se ne prikazuje — nema placeholder sadržaja | Srednji |
### 6.3.6 Napredni Display Ads — planirano za Fazu 2

Kada broj oglašivača i kampanja preraste kapacitet ručnog upravljanja (okvirno 10+ istovremenih kampanja), planirano je proširenje na napredni sistem koji uključuje:

- **Advertiser entitet** — zaseban profil za oglašivače sa vlastitim balansom
- **AdCampaign entitet** — kampanje sa CPC biddingom, budžetima i targetingom
- **Targeting po kategorijama** — prikazivanje oglasa samo u relevantnim kategorijama
- **Weighted random selection** — veći CPC bid = veća šansa za prikaz
- **Fraud detection** — automatska detekcija sumnjivih klikova
- **Self-service portal** — oglašivači sami kreiraju i upravljaju kampanjama

> 📝 **Napomena:** Detaljan dizajn naprednog sistema je dokumentiran i biće osnova za Fazu 2 kada se aktivira okidač (vidi MVP SCOPE dokument).

* * *
## 6.4 Franšizno poslovanje
### 6.4.1 Pregled i potencijal

Franšizno poslovanje omogućava licenciranje CityInfo platforme partnerima koji žele pokrenuti lokalnu verziju u svom gradu ili regionu. Ovo je potencijalno **najveći revenue stream** jer nema geografskih ograničenja — tržište je internacionalno.

Dok promocije i display oglašavanje generišu prihod unutar pojedinačnih tenanta, franšiza monetizira samu platformu kao proizvod. Svaki novi partner znači novi tenant, novu bazu korisnika, i kontinuirani revenue share.

**Praktična napomena:** Za razliku od operativnih prihoda (promocije, oglasi) koji rastu linearno sa aktivnošću korisnika, franšiza ima potencijal eksponencijalnog rasta kroz mrežu partnera.
### 6.4.2 Poslovni model

Franšiza koristi kombinaciju jednokratne naknade i revenue share modela:

| Komponenta | Opis | Primjer |
| --- | --- | --- |
| **Jednokratna naknada** | Setup fee za pokretanje novog tenanta | 5,000 - 20,000 EUR (zavisno od veličine tržišta) |
| **Revenue share** | Procenat od svih prihoda tenanta | 15-25% mjesečno |

**Šta određuje cijenu:**

- Veličina tržišta (broj stanovnika, turistički potencijal)
- Ekskluzivnost (jedan partner po gradu vs. konkurencija)
- Nivo podrške i prilagođavanja

> 📝 **Napomena:** Navedene cijene su ilustrativne. Stvarne cijene se definišu kroz pregovore i zavise od specifičnosti svakog partnerstva.
### 6.4.3 Šta franšiza uključuje

| Komponenta | Opis |
| --- | --- |
| **Pristup platformi** | Potpuno funkcionalan tenant sa izoliranom bazom podataka |
| **Branding opcije** | White-label (potpuno prilagođen brand) ili co-branding (CityInfo + partner) |
| **Obuka** | Onboarding za administratore i moderatore, dokumentacija, best practices |
| **Tehnička podrška** | Ongoing support, maintenance, updates platforme |
| **Lokalizacija** | Podrška za lokalni jezik i valutu |

**Šta franšiza NE uključuje:**

- Marketing materijale (partner je odgovoran za lokalnu promociju)
- Garanciju uspjeha (partner preuzima poslovni rizik)
- Ekskluzivni development (custom features se dodatno naplaćuju)
### 6.4.4 Profil idealnog partnera

Franšiza je otvorena za različite profile partnera, uz ispunjavanje osnovnih kriterija:

| Tip partnera | Prednosti | Primjer |
| --- | --- | --- |
| **Lokalni poduzetnici** | Poznavanje tržišta, motivacija | Tech-savvy pojedinci sa poslovnim iskustvom |
| **Medijske kuće** | Postojeća publika, credibility | Lokalni portali, radio stanice |
| **Turističke organizacije** | Institucionalna podrška, funding | DMO, turističke zajednice |
| **Gradske uprave** | Resursi, legitimitet | Smart city inicijative |

**Ključni kriteriji:**

- Finansijska sposobnost (setup fee + operativni troškovi prvih 6-12 mjeseci)
- Razumijevanje lokalnog tržišta
- Kapacitet za moderaciju i korisničku podršku
- Dugoročna vizija i commitment
### 6.4.5 Proces partnerstva

```
flowchart TD
    A[Inicijalni kontakt] --> B[Evaluacija partnera]
    B --> C{Ispunjava kriterije?}
    C -->|Ne| D[Odbijanje sa feedbackom]
    C -->|Da| E[Pregovori i ugovor]
    E --> F[Jednokratna naknada]
    F --> G[Tenant setup]
    G --> H[Obuka tima]
    H --> I[Soft launch]
    I --> J[Go-live]
    J --> K[Ongoing: Revenue share + Podrška]
```

**Praktična napomena:** Cijeli proces od inicijalnog kontakta do go-live tipično traje 4-8 sedmica, zavisno od kompleksnosti prilagođavanja i spremnosti partnera.
### 6.4.6 Revenue share mehanizam

Revenue share se obračunava mjesečno na osnovu svih prihoda koje tenant generiše:

| Izvor prihoda | Uključeno u revenue share |
| --- | --- |
| Prodaja kredit paketa | ✅ Da |
| Promocije listinga | ✅ Da (indirektno, kroz kredite) |
| Display oglašavanje | ✅ Da |

**Obračun:**

- Partner dostavlja mjesečni izvještaj o prihodima
- Platforma ima pristup agregatnim podacima za verifikaciju
- Isplata revenue share-a do 15. u mjesecu za prethodni mjesec

> 📝 **Napomena za V1:** Inicijalno se oslanjamo na povjerenje i transparentnost partnera. Automatizovani revenue tracking može se implementirati u budućim verzijama.

* * *
## 6.5 Pricing strategija
### 6.5.1 Pregled

CityInfo koristi value-based pricing koji balansira dostupnost za male organizatore sa profitabilnošću za platformu. Ključni principi su jednostavnost (jasne cijene), skalabilnost (od malih do velikih), i lokalnost (prilagođeno kupovnoj moći).

Cijene nisu "zakovane" — očekuje se da će se prilagođavati kroz A/B testiranje i feedback tržišta. Dokumentirane vrijednosti su početne smjernice.
### 6.5.2 Kredit paketi

| Paket | Krediti | Cijena (BAM) | Popust | Po kreditu | Target |
| --- | --- | --- | --- | --- | --- |
| Starter | 100 | 10  | 0%  | 0.10 | Prvi korisnici |
| Standard | 500 | 45  | 10% | 0.09 | Redovni korisnici |
| Premium | 1000 | 80  | 20% | 0.08 | Aktivni organizatori |
| Business | 5000 | 350 | 30% | 0.07 | Profesionalci |
| Enterprise | 10000 | 600 | 40% | 0.06 | Velike organizacije |
### 6.5.3 Promocijski paketi (u kreditima)

> ⚠️ **Draft napomena:** Cijene AutoRenew opcije u ovoj tabeli su **ilustrativni placeholderi**. Konačan model obračuna (množitelji, fiksni dodaci, ili drugi pristup) biće definisan prije MVP-a. Bazne cijene promocija (bez AutoRenew) su stabilnije ali također podložne promjeni.

| Trajanje | Standard | Premium | Premium + Homepage |
| --- | --- | --- | --- |
| 1 dan | 20 kr | 40 kr | 60 kr |
| 3 dana | 60 kr | 120 kr | 180 kr |
| 7 dana | 140 kr | 280 kr | 420 kr |
| 30 dana | 600 kr | 1200 kr | 1800 kr |

> 📝 **AutoRenew dodaci:** Cijene za AutoRenew opciju (24h/8h/3h intervali) biće dodane u ovu tabelu kada se finalizira pricing model. Princip: češći interval = veća cijena.
### 6.5.4 Prilagođavanje po tenantu

Cijene se mogu prilagođavati po gradu/regionu na osnovu nekoliko faktora:

| Faktor | Range | Primjer |
| --- | --- | --- |
| **Kupovna moć** | 0.5-1.5× | Sarajevo 1.0×, Trebinje 0.7× |
| **Konkurencija** | 0.8-1.2× | Više konkurenata = niže cijene |
| **Veličina tržišta** | 0.7-1.3× | Veći grad = veće cijene |
| **Sezonalnost** | 0.8-1.5× | Turistička sezona = veće |
### 6.5.5 ROI primjeri

**Za organizatore događaja (koncert sa 200 mjesta):**

- Potencijalni prihod: 5,000 BAM (200 karata × 25 BAM)
- Premium promo 7 dana: 280 kredita = 28 BAM
- ROI: ~180×

**Za biznise (restoran, mjesečna promocija):**

- Dodatni prihod: 1,500 BAM (50 novih gostiju × 30 BAM)
- Standard promo 30 dana: 600 kredita = 60 BAM
- ROI: ~25×

**Praktična napomena:** Ovi primjeri su optimistični i služe za prodajne materijale. Stvarni ROI varira značajno zavisno od kvalitete sadržaja i atraktivnosti ponude.
### 6.5.6 Pricing evolucija

| Faza | Period | Fokus |
| --- | --- | --- |
| **Launch** | 0-6 mjeseci | Agresivne promocije, free trial, volume focus |
| **Growth** | 6-18 mjeseci | Postupno smanjenje popusta, loyalty program |
| **Maturity** | 18+ mjeseci | Stabilne cijene, premium tiers, value-added services |

* * *
## 6.6 API Endpoints
### 6.6.1 Wallet operacije

| Metoda | Putanja | Opis |
| --- | --- | --- |
| GET | `/api/wallet` | Dohvati trenutno stanje wallet-a |
| GET | `/api/wallet/transactions` | Lista transakcija (paginirano) |
| GET | `/api/wallet/transactions/{id}` | Detalji pojedinačne transakcije |
### 6.6.2 Kredit paketi

| Metoda | Putanja | Opis |
| --- | --- | --- |
| GET | `/api/credit-packages` | Lista dostupnih paketa |
| GET | `/api/credit-packages/{id}` | Detalji paketa |
| POST | `/api/credit-packages/{id}/purchase` | Kupovina paketa |
### 6.6.3 Promocije

| Metoda | Putanja | Opis |
| --- | --- | --- |
| GET | `/api/promotions` | Lista korisnikovih promocija |
| GET | `/api/promotions/{id}` | Detalji promocije |
| POST | `/api/promotions` | Kreiranje nove promocije |
| POST | `/api/promotions/{id}/pause` | Pauziranje promocije |
| POST | `/api/promotions/{id}/resume` | Nastavak promocije |
| DELETE | `/api/promotions/{id}` | Otkazivanje promocije |
| GET | `/api/promotions/pricing` | Dohvati cijene promocija |
### 6.6.4 Display oglašavanje (Staff admin)

| Metoda | Putanja | Opis |
| --- | --- | --- |
| GET | `/api/admin/display-ads` | Lista svih oglasa |
| GET | `/api/admin/display-ads/{id}` | Detalji oglasa |
| POST | `/api/admin/display-ads` | Kreiranje novog oglasa |
| PUT | `/api/admin/display-ads/{id}` | Ažuriranje oglasa |
| DELETE | `/api/admin/display-ads/{id}` | Brisanje oglasa |
| GET | `/api/admin/display-ads/{id}/stats` | Statistika oglasa (impressions, clicks) |
| GET | `/api/ad-zones` | Lista dostupnih zona |
| GET | `/api/ads/zone/{zoneId}` | Dohvati oglas za prikaz u zoni (javni endpoint) |
### 6.6.5 Admin operacije

| Metoda | Putanja | Opis |
| --- | --- | --- |
| POST | `/api/admin/credits/add` | Admin dodavanje kredita |
| POST | `/api/admin/credits/deduct` | Admin oduzimanje kredita |
| GET | `/api/admin/revenue/summary` | Revenue izvještaj |
| GET | `/api/admin/promotions` | Sve promocije (admin view) |

* * *
## Changelog

| Verzija | Datum | Opis |
| --- | --- | --- |
| 1.5 | 3.4.2026 | **Optimizacija 13→12 statusa.** Reference ažurirane prema novom modelu (12 statusa). |
| 1.4 | 1.4.2026 | **MIGRACIJA — jednostatus model.** Sekcija 6.2.7: `lifecycleStatus = active` → `listingStatus: published, published_under_review ili published_needs_changes`. "Vezano za lifecycle" → "Vezano za listing status" sa opisom gubitka javne vidljivosti. Status promocije `cancelled` opis ažuriran ("listing uklonjen" umjesto "listing obrisan"). |
| 1.3 | 28.3.2026 | Status → Završeno. |
| 1.0 | Mart 2026 | Inicijalna verzija |
| 1.1 | Mart 2026 | Flowchart kupovine pojednostavljen; sortiranje unutar premium sekcije eksplicirano; sekcije 6.2.4 i 6.2.5 spojene; AutoRenew množitelji označeni kao draft/placeholder; Display Ads prepisano za MVP; sekcije renumerisane |
| 1.2 | Mart 2026 | Nova sekcija 6.2.5: Pauziranje i nastavak promocije — definisana pause/resume logika, efekti na sortDate/AutoRenew/endDate, PROMO\_MAX\_PAUSE\_DAYS parametar. Promo entitet proširen sa pausedAt i remainingDays atributima. Poslovna pravila proširena. Sekcije renumerisane. |