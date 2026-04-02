# 01 - UVOD I KONCEPTI

> **Verzija:** 3.3  
> **Datum:** 28.3.2026  
> **Status:** Završeno ✅

* * *

<a id="o-čemu-je-riječ"></a>

## O čemu je riječ?

Ovaj dokument predstavlja ulaznu tačku u CityInfo dokumentaciju. Sadržaj je strukturiran tako da pruži brzi pregled sistema — od vizije i poslovnog modela koji objašnjavaju *zašto* platforma postoji, preko arhitekture koja pokazuje *kako* je organizovana, do ključnih koncepata koji čine jezgro svega. Na kraju se nalaze praktični vodiči za različite uloge i persone koje pomažu u razumijevanju korisnika.

* * *

<a id="11-vizija-i-poslovni-model"></a>

## 1.1 Vizija i poslovni model

<a id="šta-je-cityinfo"></a>

### Šta je CityInfo?

CityInfo je platforma za otkrivanje i promociju lokalnih događaja i mjesta. Zamišljena je kao centralno mjesto gdje građani i posjetioci jednog grada mogu pronaći sve što se dešava oko njih — od koncerata i izložbi do novih restorana, frizerskih salona, kulturnih institucija i turističkih atrakcija. Za organizatore i vlasnike biznisa, CityInfo predstavlja način da dođu do publike bez velikih marketinških budžeta.

Platforma je dizajnirana kao **multi-tenant sistem**, što znači da svaki grad (Sarajevo, Zagreb, Ljubljana, Beograd...) ima svoju zasebnu instancu sa prilagođenim sadržajem, ali dijeli istu tehnološku osnovu. Sistem je **dvojezičan** — svaki tenant podržava primarni i sekundarni jezik, što omogućava lokalizaciju za različita tržišta i bolju dostupnost turistima. Ovakav pristup omogućava brzo širenje na nove gradove i države bez reinventiranja točka.

<a id="problem-koji-rješavamo"></a>

### Problem koji rješavamo

| Problem | Kako ga rješavamo |
| --- | --- |
| Informacije o lokalnim događajima su razbacane po društvenim mrežama, posterima i "od usta do usta" | Centralizovan, pretraživ katalog sa filterima |
| Turisti teško pronalaze lokalne sadržaje i događaje na jeziku koji razumiju | Dvojezični sistem sa prevedenim sadržajima |
| Ne postoji kategoriziran pregled mjesta, lokacija i organizacija koji bi posjetiocima omogućio brz pronalazak | Strukturirane kategorije sa tagovima i filterima |
| Mali organizatori nemaju budžet za promociju | Freemium model — besplatno objavljivanje, plaćana promocija |
| Vlasnici biznisa teško mjere ROI tradicionalnog oglašavanja | Mjerljive promocije sa statistikama pregleda |
| Korisnici ne znaju šta se dešava u njihovom komšiluku | Personalizovane preporuke i lokacijski filteri |

<a id="vrijednosna-propozicija"></a>

### Vrijednosna propozicija

**Za korisnike (posjetioce i turiste):**

- Besplatan pristup svim događajima i mjestima
- Filteri po datumu, udaljenosti/lokaciji, kategoriji i tagovima
- Dvojezični sadržaj za lakše snalaženje
- Spremanje favorita, dijeljenje sa prijateljima

**Za organizatore događaja:**

- Besplatno kreiranje i objavljivanje događaja
- Mogućnost povezivanja događaja sa mjestom (lokacijom) — povećava vidljivost oboje
- Plaćana promocija za veću vidljivost
- Statistike i uvid u performanse

**Za vlasnike biznisa i institucije (mjesta):**

- Besplatan profil sa osnovnim informacijama
- Povezivanje sa događajima koji se održavaju na lokaciji — dodatna vidljivost bez troška
- Premium opcije za isticanje u pretragama

<a id="poslovni-model"></a>

### Poslovni model

CityInfo koristi **freemium model** sa tri izvora prihoda:

| Izvor prihoda | Opis | Udio (projekcija) |
| --- | --- | --- |
| **Promocije** | Korisnici kupuju kredite koje troše na promociju svojih listinga (Standard, Premium, Premium+Homepage) | ~50% |
| **Display oglašavanje** | Reklamne zone za vanjske oglašivače | ~20% |
| **Franšiza (tenanti)** | Licenciranje platforme za nove gradove/regije — partneri plaćaju za korištenje sistema | ~30% |

**Kako funkcionišu krediti?** Korisnici kupuju pakete kredita (npr. 100 kredita za 10 BAM) koje zatim troše na promocije. Ovaj prepaid model smanjuje frikciju pri svakoj kupovini promocije i omogućava bolji cash flow za platformu.

> **💡 Praktična napomena:** Cijene kredita i promocija mogu varirati po gradovima (tenantima) ovisno o kupovnoj moći i konkurenciji. Ovo nije hardkodirano — lokalni administratori imaju fleksibilnost prilagodbe.

* * *

<a id="12-arhitektura-sistema"></a>

## 1.2 Arhitektura sistema

<a id="multi-tenant-pristup"></a>

### Multi-tenant pristup

CityInfo je od temelja dizajniran kao multi-tenant sistem. Svaki grad je zaseban "tenant" sa vlastitom bazom podataka i konfiguracijom, ali svi dijele isti kod i infrastrukturu. Dodavanje novog grada ne zahtijeva novi deployment — samo konfiguraciju novog tenanta.

```
CityInfo Platforma
├── Sarajevo Tenant (sarajevo.cityinfo.ba)
│   └── Vlastita baza, korisnici, sadržaj
├── Zagreb Tenant (zagreb.cityinfo.hr)
│   └── Vlastita baza, korisnici, sadržaj
├── Ljubljana Tenant (ljubljana.cityinfo.si)
│   └── Vlastita baza, korisnici, sadržaj
└── ... (novi gradovi se dodaju bez promjene koda)
```

<a id="tri-korisničke-zone"></a>

### Tri korisničke zone

Jedna od ključnih arhitektonskih odluka je **potpuna separacija tri tipa korisnika** u zasebne sisteme. Ovo nije samo organizaciona podjela — to su tri različite baze podataka, tri različita login sistema, i tri različite pristupne tačke.

| Zona | Ko su? | Pristup | Baza |
| --- | --- | --- | --- |
| 🌐 **User** | Građani, turisti, organizatori, vlasnici biznisa | [cityinfo.ba](http://cityinfo.ba) | Tenant baza |
| 💼 **Staff** | Moderatori, operatori, lokalni admini | [admin.cityinfo.ba](http://admin.cityinfo.ba) | Tenant baza |
| 🔧 **GlobalAdmin** | Sistemski administratori (2-5 osoba) | [master.cityinfo.ba](http://master.cityinfo.ba) | Master baza |

**Zašto ovakva separacija?**

- **Sigurnost:** Kompromitovanje User sistema ne ugrožava Staff ili GlobalAdmin
- **Skalabilnost:** User sistem može imati hiljade korisnika bez uticaja na admin performanse
- **Compliance:** Jasna separacija olakšava GDPR i audit zahtjeve

<a id="dijagram-arhitekture"></a>

### Dijagram arhitekture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      INTERNET                                    │
└─────────────┬───────────────┬───────────────┬───────────────────────┘
              │               │               │
     ┌────────▼────────┐ ┌────▼─────────┐ ┌───▼──────────────┐
     │  cityinfo.ba    │ │ admin.       │ │ master.          │
     │  (Public)       │ │ cityinfo.ba  │ │ cityinfo.ba      │
     │                 │ │ (Staff)      │ │ (GlobalAdmin)    │
     │ • User login    │ │ • Moderacija │ │ • Tenant mgmt    │
     │ • Pregled       │ │ • Izvještaji │ │ • Infrastruktura │
     │ • Kreiranje     │ │ • Operacije  │ │ • Monitoring     │
     └────────┬────────┘ └──────┬───────┘ └───────┬──────────┘
              │                 │                  │
     ┌────────▼─────────────────▼──────┐   ┌──────▼─────────────┐
     │      TENANT BAZA (npr. SA)      │   │  MASTER BAZA       │
     │  • Users  • Staff  • Content    │   │  • GlobalAdmin     │
     │  • Transactions • Messages      │   │  • TenantConfig    │
     └─────────────────────────────────┘   └────────────────────┘
```

> **💡 Praktična napomena:** Rad na User-facing funkcionalnostima ne podrazumijeva direktan pristup Staff ili GlobalAdmin sistemima. Svaki sistem ima svoje API-je i ne postoji "prečica" između njih — to je namjerno.

* * *

<a id="13-ključni-koncepti"></a>

## 1.3 Ključni koncepti

Prije ulaska u ostatak dokumentacije, bitno je razumjeti nekoliko centralnih koncepata koji se provlače kroz cijeli sistem.

<a id="listing-zajednički-entitet"></a>

### Listing — zajednički entitet

**Listing** je apstraktni pojam koji obuhvata sve što korisnici mogu kreirati i objaviti na platformi. Trenutno postoje dva tipa listinga:

| Tip | Šta predstavlja | Primjeri |
| --- | --- | --- |
| **Event** | Vremenski ograničen događaj | Koncert, izložba, radionica, festival, konferencija |
| **Place** | Stalna fizička lokacija | Restoran, kafić, frizerski salon, teretana, muzej, turistička organizacija, kulturna institucija |

Oba tipa dijele zajedničke karakteristike (naziv, opis, slike, kategorija, vlasnik), ali imaju i svoje specifičnosti. Event ima datum početka i kraja, dok Place ima radno vrijeme i adresu. Sistem je dvojezičan — svaki listing može imati naziv i opis na primarnom i sekundarnom jeziku tenanta.

> **Zašto "Listing"?** Ovaj zajednički koncept olakšava rad sa sadržajem — promocije, moderacija, pretraga i prikaz funkcionišu isto za Events i Places. Ako se u budućnosti doda novi tip (npr. "Job" za oglase za posao), većina sistema će raditi bez izmjena.

<a id="event-vs-place-ključne-razlike"></a>

### Event vs Place — ključne razlike

| Aspekt | Event | Place |
| --- | --- | --- |
| **Trajanje** | Ima početak i kraj | Trajan (dok vlasnik ne zatvori) |
| **Lokacija** | Može biti povezan sa Place-om ili imati custom lokaciju | Ima fiksnu adresu |
| **Automatsko zatvaranje** | Da, nakon završetka | Ne  |
| **Hijerarhija** | Može imati "child" evente (npr. dani festivala) | Ne  |
| **Veza** | Event može biti povezan sa Place-om (korist za oboje) | Place može "ugostiti" više Events-a |

**Povezivanje Event-a i Place-a:** Kada se event poveže sa mjestom (npr. "Jazz veče" u "Caffe Tito"), oboje dobijaju dodatnu vidljivost — event se prikazuje na profilu mjesta, a mjesto dobija kontekst aktivnosti koje nudi.

> **💡 Praktična napomena:** Event se može povezati sa Place-om **samo ako je isti korisnik vlasnik oba listinga**. Ako organizator želi održati event u tuđem prostoru, koristi ručnu adresu.

**Dva režima u korisničkom sučelju:**

Ova separacija se direktno odražava i na korisničko iskustvo — platforma tretira događaje i mjesta kao **dva odvojena svijeta**. Korisnik u svakom trenutku radi u jednom od dva režima ("Događaji" ili "Mjesta"), a sučelje jasno stavlja do znanja koji je aktivan. Naslovna stranica po defaultu prikazuje događaje jer su oni vremenski osjetljivi. Više o ovome u dokumentu [02 - Korisnički doživljaj](../project-specs/02-korisnicko-iskustvo.md).

<a id="kategorije-i-tagovi"></a>

### Kategorije i tagovi

Svaki listing pripada **jednoj primarnoj kategoriji** i može imati do `MAX_SECONDARY_CATEGORIES` **sekundarnih kategorija** (parametar — preporučena početna vrijednost: 10). Ovaj sistem omogućava fleksibilno pronalaženje sadržaja iz različitih uglova.

**Primjer:** Trgovački centar "BauMax" može imati:

- **Primarna kategorija:** Trgovački centri
- **Sekundarne kategorije:** Građevinski materijal, Bijela tehnika, Vrt i alati

Pored kategorija, postoje i **tagovi** — fleksibilniji način opisivanja karakteristika listinga. Korisnik može odabrati do `MAX_TAGS_PER_LISTING` tagova (parametar — preporučena početna vrijednost: 2), npr. "parking", "wifi", "besplatno", "za-djecu".

> **💡 Praktična napomena:** Eventi i Places imaju potpuno odvojene sisteme kategorija i tagova jer su semantički različiti — tag "parking" ima smisla za restoran, ali ne za koncert. Ova separacija se odražava i u korisničkom sučelju: prebacivanje između režima "Događaji" i "Mjesta" resetuje aktivne filtere jer kategorije i tagovi nisu međusobno kompatibilni.

<a id="trust-tier-sistem"></a>

### Trust Tier sistem

Trust Tier je mehanizam koji automatski prilagođava nivo moderacije prema ponašanju korisnika. Umjesto binarnog "vjerujemo / ne vjerujemo", sistem prepoznaje da korisnici grade povjerenje kroz konzistentno kvalitetan sadržaj.

| Tier | Naziv | Moderacija | Kako se dostiže |
| --- | --- | --- | --- |
| **0** | Restricted | Pre-moderacija, 100% pregled | Ručno (kršenje pravila) |
| **1** | Standard | Pre-moderacija, 100% pregled | Default za nove korisnike |
| **2** | Trusted | Post-moderacija, 100% pregled | Automatski (nakon X odobrenih objava) |
| **3** | Established | Post-moderacija, sampling | Automatski (nakon Y odobrenih objava) |
| **4** | Verified Partner | Post-moderacija, minimalni sampling | Ručno (ugovorni odnos) |

**U praksi:**

- Korisnik na Tier 1 kreira događaj → čeka odobrenje moderatora (obično 2h)
- Korisnik na Tier 2 kreira događaj → odmah je vidljiv, moderator pregleda naknadno
- Korisnik na Tier 3 → samo dio sadržaja se uopće pregleda (sampling)

Napredovanje kroz tier-ove je automatsko za nivoe 1→2 i 2→3, bazirano na broju uspješno odobrenih objava. Degradacija se dešava ako korisnik ima odbijene sadržaje.

> **💡 Praktična napomena:** Trust Tier direktno određuje koliko brzo korisnikov sadržaj postaje vidljiv. Za nove korisnike, fokus je na brzoj moderaciji kako ne bi čekali predugo.

<a id="visitors-neregistrovani-korisnici"></a>

### Visitors (neregistrovani korisnici)

Pored registrovanih korisnika, platforma podržava i **visitors** — neautentificirane posjetioce koji mogu pregledati javni sadržaj bez kreiranja računa. Visitors mogu:

- Pregledati sve javne listinge
- Koristiti pretragu i filtere
- Lajkati sadržaj (bez historije)
- Dijeliti linkove

Visitors **ne mogu** kreirati sadržaj, spremati favorite na profil, niti slati poruke. Ovo omogućava platformi da bude korisna i za casual posjetioce koji samo žele vidjeti šta se dešava u gradu.

<a id="promocije-i-monetizacija"></a>

### Promocije i monetizacija

Svaki listing može biti besplatno objavljen, ali za veću vidljivost korisnici mogu kupiti promociju. Postoje tri nivoa:

| Tip promocije | Pozicioniranje | Vizuelno | Cijena (primjer) |
| --- | --- | --- | --- |
| **Standard** | Miješa se sa običnim listinzima po sortDate | Blago isticanje (background, border) | 20 kredita/dan |
| **Premium** | Uvijek na vrhu kategorije, iznad svih običnih | Jako isticanje + "Premium" badge | 40 kredita/dan |
| **Premium + Homepage** | Apsolutni prioritet na naslovnoj stranici | Jako isticanje + "Premium" + "Featured" badge | 60 kredita/dan |

**Kako funkcioniše sortiranje:**

Sortiranje promocija funkcioniše različito na **naslovnoj stranici** i **unutar kategorija**:

**Na naslovnoj stranici (dvije grupe):**

- **Grupa 1** — Premium promocije sa opcijom "Prikaži na naslovnoj": apsolutni prioritet, međusobno sortirane po `sortDate`
- **Grupa 2** — Svi ostali listinzi (Premium bez homepage opcije, Standard, obični): sortirani po `sortDate` bez prioriteta

**Unutar kategorije (tri grupe):**

- **Premium sekcija** — Premium promocije su uvijek izdvojene na vrhu kategorije, međusobno sortirane po `sortDate`
- **Standard + obični** — ispod Premium sekcije, Standard promocije se miješaju sa običnim listinzima — prednost Standard promocije je samo vizuelna (isticanje), ne poziciona

**AutoRenew funkcionalnost:** AutoRenew automatski osvježava `sortDate` listinga na odabranom intervalu, čime se listing vraća na vrh svoje grupe. Dostupni intervali:

| Interval | Učestalost | Efekat |
| --- | --- | --- |
| **24h** | Jednom dnevno | Održava prisutnost |
| **8h** | Tri puta dnevno | Povećana vidljivost |
| **3h** | Osam puta dnevno | Maksimalna vidljivost |

AutoRenew se plaća kao dodatak na baznu cijenu promocije (konačan pricing model još nije finaliziran).

**Ručno osvježavanje:** Svi korisnici mogu besplatno osvježiti poziciju svog listinga jednom u 24 sata, bez obzira na promocije.

<a id="moderacijski-pristup"></a>

### Moderacijski pristup

CityInfo koristi hibridni pristup moderaciji koji kombinuje automatske provjere i ljudski pregled:

1. **AI pre-screening** — automatska provjera slika i teksta za očigledan spam ili neprimjeren sadržaj
2. **Trust-based routing** — viši tier korisnici idu direktno na objavu, niži na moderacijski red
3. **Human review** — moderatori pregledaju sadržaj i donose konačnu odluku
4. **Post-moderation** — čak i objavljeni sadržaj može biti prijavljen i naknadno pregledan

Moderatori mogu donijeti tri odluke:

- **Approve** — sadržaj je odobren i vidljiv
- **Request Changes** — potrebne izmjene, korisnik dobija feedback
- **Reject** — sadržaj je trajno odbijen

> **💡 Praktična napomena:** Moderacijski workflow nije statičan — pravila i pragovi se prilagođavaju kako platforma bude rasla. SLA za pre-moderaciju je 2 sata, za post-moderaciju 8 sati.

* * *

<a id="14-brzi-start-po-ulogama"></a>

## 1.4 Brzi start po ulogama

Ovisno o ulozi, različiti dijelovi dokumentacije će biti relevantni. Sljedeći vodiči pokazuju gdje početi.

<a id="za-developere"></a>

### 👨‍💻 Za developere

**Frontend development:**

1. [02 - Korisnički doživljaj](../project-specs/02-korisnicko-iskustvo.md) — razumijevanje UI tokova
2. [04 - Sadržaj](../project-specs/04-sadrzaj.md) — struktura Listing entiteta
3. API Endpoints sekcije u svakom poglavlju — integracija

**Backend development:**

1. [03 - Korisnici i pristup](../project-specs/03-korisnici-i-pristup.md) — autentifikacija i autorizacija
2. [08 - Infrastruktura](../project-specs/08-infrastruktura.md) — multi-tenant logika
3. Poslovna pravila (BR-\*) u svakom poglavlju — validacije

**Moderacija/admin panel:**

1. [05 - Moderacija](../project-specs/05-moderacija.md) — workflow i queue logika
2. [03 - Korisnici i pristup, sekcija Staff](../project-specs/03-korisnici-i-pristup.md) — uloge i ovlasti

<a id="za-moderatore"></a>

### 🛡️ Za moderatore

1. **Obavezno:** [05 - Moderacija](../project-specs/05-moderacija.md) — glavni priručnik
2. [03 - Korisnici i pristup](../project-specs/03-korisnici-i-pristup.md) — kako trust utiče na workflow
3. [07 - Komunikacija](../project-specs/07-komunikacija.md) — komunikacija sa korisnicima
4. [Persone i korisnička putovanja](../project-specs/persone-i-korisnicka-putovanja.md) — Lejla (moderator persona) i putovanje 5

<a id="za-product-managere"></a>

### 📊 Za product managere

1. Ovaj dokument (1.1 i 1.5) — big picture
2. [Persone i korisnička putovanja](../project-specs/persone-i-korisnicka-putovanja.md) — detaljne persone, korisnička putovanja i mapiranje na journey milestones
3. [02 - Korisnički doživljaj](../project-specs/02-korisnicko-iskustvo.md) — user flows
4. [06 - Monetizacija](../project-specs/06-monetizacija.md) — pricing i business model

<a id="za-operatore"></a>

### ⚙️ Za operatore

1. [06 - Monetizacija](../project-specs/06-monetizacija.md) — financijski tokovi
2. [03 - Korisnici i pristup](../project-specs/03-korisnici-i-pristup.md) — upravljanje osobljem
3. [08 - Infrastruktura](../project-specs/08-infrastruktura.md) — audit i logging
4. [Persone i korisnička putovanja](../project-specs/persone-i-korisnicka-putovanja.md) — Damir (operator persona) i putovanje 6

> **💡 Praktična napomena:** Dokumentacija je živi organizam. Ako nešto nedostaje ili nije jasno, preporuka je otvoriti issue u repo-u ili direktno kontaktirati vlasnika dokumenta.

* * *

<a id="15-persone-i-korisničke-priče"></a>

## 1.5 Persone i korisničke priče

> **📄 Detaljna verzija:** Kompletne persone sa ciljevima, frustracijama, "aha" momentima, i detaljnim korisničkim putovanjima (uključujući Staff persone — moderator i operator) dostupne su u zasebnom dokumentu: [**Persone i korisnička putovanja**](../project-specs/persone-i-korisnicka-putovanja.md). Taj dokument također sadrži mapiranje putovanja na journey milestones (J-01 do J-09) iz development plana.

Da bi se bolje razumjelo za koga se gradi platforma, definisano je šest reprezentativnih persona — četiri korisničke i dvije staff persone. Ovdje je sažeti pregled; za detalje pogledajte linkani dokument.

<a id="korisničke-persone"></a>

### Korisničke persone

| Persona | Uloga | Ključna potreba | Journey fokus |
| --- | --- | --- | --- |
| 🎭 **Milica** (28) | Mladi profesionalac | Brzo pronaći zanimljiv sadržaj bez puno filtriranja | J-04 Otkrivanje |
| 🎤 **Marko** (35) | Organizator događaja | Doći do publike bez velikog budžeta, pratiti efekte | J-02 Kreiranje, J-06 Monetizacija |
| 🍽️ **Ana** (42) | Vlasnica restorana | Jednostavan profil, biti pronađena, verified badge | J-02 Kreiranje, J-07 Verifikacija |
| 🧳 **Thomas** (45) | Turist iz Njemačke | Sadržaj na engleskom, filter po blizini, brzo | J-04 Otkrivanje |

<a id="staff-persone"></a>

### Staff persone

| Persona | Uloga | Ključna potreba | Journey fokus |
| --- | --- | --- | --- |
| 🛡️ **Lejla** (26) | Content moderator | Efikasan queue, konzistentne odluke, brze akcije | J-03 Moderacija |
| ⚙️ **Damir** (38) | Operations manager | Dashboard, parametri, analitika, minimalne manuelne intervencije | J-08 Operacije, J-09 Automatizacija |

<a id="ključni-user-journey-i"></a>

### Ključni user journey-i

Na osnovu persona, identificirano je šest ključnih putovanja kroz sistem:

| Putovanje | Persona | Prolazi kroz | Dokumentacija |
| --- | --- | --- | --- |
| Otkrivanje vikend plana | Milica | J-04 | [Persone i korisnička putovanja](../project-specs/persone-i-korisnicka-putovanja.md) |
| Objava koncerta i promocija | Marko | J-01 → J-02 → J-03 → J-06 → J-09 | [Persone i korisnička putovanja](../project-specs/persone-i-korisnicka-putovanja.md) |
| Kreiranje profila restorana | Ana | J-01 → J-02 → J-03 → J-07 | [Persone i korisnička putovanja](../project-specs/persone-i-korisnicka-putovanja.md) |
| Plan za večer u stranom gradu | Thomas | J-04 | [Persone i korisnička putovanja](../project-specs/persone-i-korisnicka-putovanja.md) |
| Obrada jutarnjeg queue-a | Lejla | J-03 → J-07 → J-08 | [Persone i korisnička putovanja](../project-specs/persone-i-korisnicka-putovanja.md) |
| Analiza i kalibracija parametara | Damir | J-08 → J-09 | [Persone i korisnička putovanja](../project-specs/persone-i-korisnicka-putovanja.md) |

> **💡 Praktična napomena:** Persone i journey-i nisu statični. Kako platforma bude rasla i kako se bude prikupljalo više podataka o stvarnom ponašanju korisnika, ovi profili će se ažurirati. Ako se primijeti da se stvarni korisnici ponašaju drugačije od opisanih persona, to je vrijedna informacija za Product tim.

* * *

<a id="šta-dalje"></a>

## Šta dalje?

Nakon čitanja ovog dokumenta, postoji solidna osnova za razumijevanje CityInfo platforme. Ovisno o ulozi, preporučeni su sljedeći koraci:

- **Detaljne persone i putovanja:** [Persone i korisnička putovanja](../project-specs/persone-i-korisnicka-putovanja.md)
- **Tehnički detalji o korisnicima:** [03 - Korisnici i pristup](../project-specs/03-korisnici-i-pristup.md)
- **Detaljni user flows:** [02 - Korisnički doživljaj](../project-specs/02-korisnicko-iskustvo.md)

* * *

<a id="changelog"></a>

## Changelog

| Verzija | Datum | Opis promjene |
| --- | --- | --- |
| 3.3 | 28.3.2026 | Status → Završeno. Korigirano sortiranje promocija — eksplicitno opisana razlika između homepage-a (2 grupe) i kategorija (3 grupe). Sekundarne kategorije parametrizirane (`MAX_SECONDARY_CATEGORIES`). Tagovi parametrizirani (`MAX_TAGS_PER_LISTING`). AutoRenew pricing referenca ažurirana. |
| 3.2 | Mart 2026 | Sekcija 1.5 prerađena: skraćeni pregled persona sa linkovima na detaljni dokument "Persone i korisnička putovanja". Dodane Staff persone (Lejla, Damir). Sekcija 1.4 ažurirana sa linkovima na novi dokument. |

* * *

*Posljednje ažuriranje: 28.3.2026*  
*Vlasnik dokumenta: CityInfo tim*