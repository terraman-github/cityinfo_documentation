---
title: "04 - SADRŽAJ"
confluence_page_id: "240189477"
---

> **Verzija:** 2.2  
> **Datum:** 3.4.2026  
> **Status:** Završeno ✅

* * *
## O čemu je riječ?

Ovaj dokument opisuje srce CityInfo platforme — sadržaj koji korisnici kreiraju i konzumiraju. Objašnjava kako su organizovani događaji (Events) i mjesta (Places), šta im je zajedničko, a šta specifično. Također pokriva sisteme za organizaciju sadržaja (sektori, kategorije i tagovi), multimediju, verifikaciju vlasništva, korisničke interakcije (lajkovi, favoriti, dijeljenje), te životni ciklus svakog listinga od nacrta do arhive.

Dokument je namijenjen developerima koji grade funkcionalnosti vezane za sadržaj, ali i product ljudima koji trebaju razumjeti kako sistem funkcioniše "ispod haube".

* * *
## 4.1 Listing — zajednički entitet
### Šta je Listing?

Listing je apstraktni koncept koji obuhvata sve što korisnici mogu kreirati na platformi. Umjesto da Event i Place budu potpuno odvojeni sistemi sa dupliciranom logikom, oni dijele zajedničku osnovu — Listing. Ovo omogućava da promocije, moderacija, pretraga i statistike funkcionišu uniformno, bez obzira na tip sadržaja.

Trenutno postoje dva tipa listinga: **Event** (vremenski ograničen događaj) i **Place** (stalna fizička lokacija). Arhitektura je dizajnirana tako da se novi tipovi mogu dodati u budućnosti bez velikih izmjena postojećeg koda.
### Osnovni atributi

Svaki listing, bez obzira da li je Event ili Place, ima sljedeće zajedničke karakteristike:

| Atribut | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| name | String | Naziv na primarnom jeziku tenanta | ✅   | —   |
| nameAlt | String | Naziv na sekundarnom jeziku tenanta | ❌   | Za turiste i dvojezične prikaze |
| excerpt | String | Kratak opis za prikaz u listama | ❌   | Auto-generisan iz description ako nije unesen |
| excerptAlt | String | Kratak opis na sekundarnom jeziku | ❌   | —   |
| description | String | Detaljni opis sa podrškom za formatiranje | ✅   | Minimum 50 karaktera |
| descriptionAlt | String | Detaljni opis na sekundarnom jeziku | ❌   | —   |
| ownerId | String | Identifikator korisnika koji je kreirao listing | ✅   | Ne može se mijenjati |
| featuredImageUrl | String | URL glavne slike | ❌   | Sinhronizuje se sa Image entitetom |
| listingUrl | String | Vanjski link (web, booking, meni) | ❌   | —   |

> **📝 Napomena o dvojezičnosti:** Korisnik sam popunjava polja za oba jezika. Polja `name`, `description`, `excerpt` odgovaraju primarnom jeziku tenanta, a `nameAlt`, `descriptionAlt`, `excerptAlt` sekundarnom. Sistem prikazuje odgovarajuću verziju prema jeziku koji je posjetilac odabrao u interfejsu.
### Kategorizacija

Sadržaj na platformi je organizovan u tri nivoa: **Sektor → Kategorija → Tagovi**. Sektor je široka grupa (npr. "Hrana i piće", "Kupovina"), kategorija je konkretan tip unutar sektora (npr. "Restorani", "Baumarketi"), a tagovi su slobodne oznake koje opisuju specifičnosti listinga (npr. "parking", "wifi", "veganski").

Svaki listing pripada **jednoj primarnoj** i opcionalno **više sekundarnih kategorija** (maksimalan broj je definisan parametrom `MAX_SECONDARY_CATEGORIES`). Primarna kategorija definira "šta je" listing, dok sekundarne proširuju njegovu vidljivost u pretrazi. Sve kategorije pripadaju istom tipu (EventCategory ili PlaceCategory) — korisnik ne može miješati kategorije za evente i mjesta.

**Važno:** Eventi i Places imaju **potpuno odvojene sisteme kategorija**. Event koristi `EventCategory`, Place koristi `PlaceCategory` — to su zasebne tabele koje se ne miješaju.

**Arhitektura čuvanja:**

Sve kategorije listinga čuvaju se u **relacionoj tabeli** (`EventListingCategories` ili `PlaceListingCategories`). Dodatno, podaci o primarnoj kategoriji su **denormalizovani** direktno u Listing entitetu radi performansi pri prikazivanju lista.

```
┌─────────────────┐         ┌─────────────────────────┐
│     Listing     │         │   ListingCategories     │
├─────────────────┤         ├─────────────────────────┤
│ primaryCat...   │◄────────│ listingId               │
│ (denormalized)  │         │ categoryId              │
└─────────────────┘         │ isPrimary (bool)        │
                            └─────────────────────────┘
```

**Denormalizovani atributi u Listing entitetu:**

| Atribut | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| primaryCategoryId | String | ID primarne kategorije | ✅\* | \*Obavezno za sve osim draft statusa |
| primaryCategoryData | Object | Snapshot primarne kategorije | ✅\* | Sadrži `name`, `color` i `sectorName` za brzi prikaz |

**Relaciona tabela (ListingCategories):**

| Atribut | Tip | Opis |
| --- | --- | --- |
| listingId | String | ID listinga |
| categoryId | String | ID kategorije |
| isPrimary | Boolean | Da li je ovo primarna kategorija |

**Primjer višestrukih kategorija:**

Baumarket "Penny Shop" ima širok asortiman koji pokriva više kategorija:

- **Primarna kategorija:** Kupovina → Baumarketi
- **Sekundarne kategorije:** Kupovina → Bijela tehnika, Kupovina → Građevinski materijal, Kupovina → Alati, Kupovina → Sanitarije, Kupovina → Namještaj

Korisnik koji pretražuje "baumarketi" pronalazi Penny Shop kroz primarnu kategoriju. Korisnik koji pretražuje "bijela tehnika" pronalazi ga kroz sekundarnu kategoriju. Oba pristupa vode do istog listinga. Još specifičnije pretrage poput "frižider" ili "laminat" pokrivaju se fulltext pretragom po opisu listinga i tagovima — kategorije ostaju na nivou odjela, ne pojedinačnih proizvoda.
### Tagovi (denormalizovano)

Tagovi opisuju karakteristike listinga (npr. "besplatno", "parking", "wifi"). Korisnik može odabrati do `MAX_TAGS_PER_LISTING` tagova (parametar — preporučena početna vrijednost: 2). Slugovi tagova se čuvaju direktno u Listing entitetu radi brzog pristupa.

**Važno:** Eventi koriste `EventTags`, Places koriste `PlaceTags` — odvojeni sistemi. Više o tagovima u sekciji 4.5.

| Atribut | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| primaryTagSlug | String | Slug prvog taga | ❌   | Referenca na EventTags ili PlaceTags |
| secondaryTagSlug | String | Slug drugog taga | ❌   | —   |
### Status i vidljivost

CityInfo koristi **jednostatus model** sa jednim poljem `listingStatus` koje obuhvata kompletan životni ciklus listinga — i fazu i moderacijski status. Ovaj pristup eliminiše nevalidne kombinacije statusa i pojednostavljuje logiku vidljivosti.

| Atribut | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| listingStatus | Enum | Kompletan status listinga | ✅   | 12 vrijednosti — vidi sekciju 4.8 |
| removedReason | Enum | Razlog trajnog uklanjanja | ❌   | Samo kad je listingStatus = `removed` |
| verificationStatus | Enum | Status verifikacije vlasništva | ✅   | unverified, pending, verified |
| isPublic | Boolean | Da li je vidljiv javnosti | ✅   | Kalkulisano polje — automatski se održava |
| wasEverActive | Boolean | Da li je ikad bio javno vidljiv | ✅   | Jednom true, uvijek true |
| internalNote | String | Interna napomena za moderatore | ❌   | Nije vidljiva autorima |
### Vremenske oznake

| Atribut | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| sortDate | DateTime | Datum za sortiranje u listama | ✅   | Ključno za pozicioniranje |
| lastManualRefreshAt | DateTime | Vrijeme zadnjeg ručnog osvježavanja | ❌   | Za provjeru 24h cooldown-a |
| createdAt | DateTime | Datum kreiranja | ✅   | Automatski |
| updatedAt | DateTime | Datum zadnje izmjene | ✅   | Automatski |
### Metrike

| Atribut | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| viewCount | Number | Broj pregleda | ✅   | Denormalizovano za performanse |
| totalAppreciations | Number | Broj lajkova | ✅   | Denormalizovano za performanse |

> **📝 Napomena:** Lista atributa nije konačna i može se proširivati u skladu sa potrebama proizvoda.

> **💡 Praktična napomena:** Polje `sortDate` je centralno za kontrolu gdje se listing pojavljuje u listama. Promocije i osvježavanje sadržaja manipulišu upravo ovim poljem. Korisnici mogu besplatno ručno osvježiti poziciju jednom u 24 sata. Više o tome u poglavlju [06 - Monetizacija](06-monetizacija.md).

* * *
## 4.2 Event entitet
### Šta je Event?

Event predstavlja vremenski ograničenu aktivnost — koncert, festival, izložbu, radionicu, konferenciju, sportski događaj. Za razliku od Place-a koji postoji kontinuirano, Event ima jasno definisan početak i kraj, nakon čega automatski prelazi u `expired` status.

Eventi nasljeđuju sve atribute od Listing entiteta i dodaju specifičnosti vezane za vrijeme, lokaciju listinga i hijerarhiju događaja. Zanimljiva karakteristika je mogućnost kreiranja **hijerarhije događaja** — festival može imati pojedinačne koncerte kao pod-događaje, gdje svaki može imati svoju promociju.
### Specifični atributi Event-a

| Atribut | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| eventId | String | Jedinstveni identifikator | ✅   | —   |
| startDateTime | DateTime | Početak događaja | ✅   | Ne može biti u prošlosti pri kreiranju |
| endDateTime | DateTime | Kraj događaja | ✅   | Default: isti dan kao startDateTime |
| placeId | String | Veza sa mjestom | ❌\* | \*Obavezno jedno od: placeId ili ručna lokacija |
| manualAddress | String | Ručno unesena adresa | ❌\* | Alternativa za placeId |
| latitude | Number | Geografska širina lokacije listinga | ❌\* | Za mapni prikaz |
| longitude | Number | Geografska dužina lokacije listinga | ❌\* | Za mapni prikaz |
| placeSnapshot | Object | Snapshot mjesta ako je obrisano | ❌   | Automatski se popunjava |
| parentEventId | String | ID nadređenog događaja | ❌   | Za child evente (festivali) |
| hasChildren | Boolean | Da li ovaj event ima pod-događaje | ✅   | Default: false |

**Napomena o trajanju:** Ako korisnik ne unese `endDateTime`, sistem automatski postavlja kraj događaja na isti dan kao početak — podrazumijevano trajanje je jedan dan.
### Lokacija listinga događaja

Svaki event mora imati definisanu lokaciju gdje se održava. Postoje dvije opcije:

**Opcija 1: Povezivanje sa Place-om**

Event se može povezati sa postojećim Place-om **samo ako je isti korisnik vlasnik oba listinga**. Ovo pojednostavljuje sistem i daje jasnu kontrolu — ko kreira mjesto, taj na njemu organizuje događaje.

| Kada koristiti | Primjer |
| --- | --- |
| Vlasnik ima svoj Place i organizuje event tamo | Ana ima restoran i organizuje degustaciju vina |
| Vlasnik želi cross-promotion između mjesta i eventa | Na stranici restorana se prikazuju nadolazeći eventi |

**Opcija 2: Ručna adresa**

Kada organizator nema vlastiti Place u sistemu, ili održava event na lokaciji koju ne posjeduje, koristi ručnu adresu sa koordinatama.

| Kada koristiti | Primjer |
| --- | --- |
| Event je na javnom prostoru | Koncert na trgu, maraton kroz grad |
| Lokacija nije registrovana u sistemu | Privatna kuća, privremeni prostor |
| Organizator koristi tuđi prostor | Bend svira u klubu koji nije njihov |

> **💡 Praktična napomena:** Ako organizator želi održati event u tuđem prostoru (npr. bend u klubu), koristi ručnu adresu. Alternativno, može kontaktirati vlasnika mjesta i zamoliti ga da on kreira event — na taj način oboje dobijaju benefit cross-promocije.
### Hijerarhija događaja

Sistem podržava dvonivovsku hijerarhiju događaja koja je korisna za festivale, konferencije sa više sesija, ili višednevne događaje:

```
Festival (parent, hasChildren = true)
├── Koncert 1 (child, parentEventId = Festival)
├── Koncert 2 (child, parentEventId = Festival)
└── Koncert 3 (child, parentEventId = Festival)
```

**Ključna pravila:**

- Maksimalno 2 nivoa (parent → child, nema grandchildren)
- **Samo vlasnik parent događaja može kreirati child događaje**
- Child događaj mora biti unutar vremenskog okvira parent događaja
- Svaki događaj (parent ili child) može imati svoju promociju
- Brisanje parent-a briše i sve child događaje (prema istoj logici brisanja — vidi tabelu ispod)
- `parentEventId` i `hasChildren` su **međusobno isključivi** — event ne može istovremeno biti child (imati `parentEventId`) i parent (imati `hasChildren = true`). Ovo je garancija dvonivovske hijerarhije.

**Zašto** `hasChildren`? Ovaj flag omogućava sistemu da na karticama označi parent evente (npr. "Festival — više događaja") i da pri povlačenju detalja zna treba li dohvatiti child evente — bez skeniranja baze za svaki prikaz.
### Brisanje događaja

Mogućnost brisanja ovisi o tome da li je event ikad bio javno vidljiv (`wasEverActive`):

| Uslov | Šta se dešava |
| --- | --- |
| `wasEverActive = false` (draft, in\_review, changes\_requested) | Korisnik može obrisati → prelazi u `removed` sa `removedReason = account_deleted` |
| `wasEverActive = true` | Direktno brisanje nije dostupno; korisnik može otkazati event (`canceled`) ili ga sakriti (`hidden_by_owner`) |

**Brisanje parent eventa:** Kad vlasnik briše parent event (a `wasEverActive = false`), svi child eventi prolaze istu logiku — oni sa `wasEverActive = false` prelaze u `removed` sa `account_deleted`. Child eventi koji su ikad bili aktivni ne mogu biti obrisani — korisnik ih mora otkazati ili sakriti.

**Napomena:** Eventi koji su ikad bili javno vidljivi (`wasEverActive = true`) ne brišu se trajno — zadržavaju se radi integriteta podataka (statistike, historija, favoriti). Korisnik ih više ne vidi u svom profilu, ali sistem čuva zapis.
### Automatski procesi

- **Istek događaja:** Kad `endDateTime` prođe, event automatski prelazi u `expired` status i ostaje javno vidljiv kao historijski zapis sa oznakom "Završeno"
- **Istek otkazanog eventa:** Ako event ostane u `canceled` statusu dok `endDateTime` prođe, automatski prelazi u `expired`
- **Snapshot mjesta:** Ako se povezani Place obriše, event čuva snapshot lokacijskih podataka sa svim potrebnim informacijama za prikaz

* * *
## 4.3 Place entitet
### Šta je Place?

Place predstavlja stalnu fizičku lokaciju — restoran, prodavnica, muzej, frizerski salon, sportski klub, institucija, organizacija i slično. Za razliku od Event-a, Place nema vremensko ograničenje i ostaje aktivan dok ga vlasnik ili moderator ne zatvori.

Places nasljeđuju sve atribute od Listing entiteta i dodaju specifičnosti vezane za fizičku adresu i geolokaciju. Vlasnik Place-a može kreirati Events povezane sa tim mjestom, što omogućava cross-promotion — na stranici mjesta se prikazuju nadolazeći događaji.
### Specifični atributi Place-a

| Atribut | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| placeId | String | Jedinstveni identifikator | ✅   | —   |
| addressLine | String | Ulica i broj | ✅   | —   |
| city | String | Grad | ✅   | —   |
| latitude | Number | Geografska širina lokacije listinga | ✅   | Za mapni prikaz |
| longitude | Number | Geografska dužina lokacije listinga | ✅   | Za mapni prikaz |
| googlePlusCode | String | Google Plus Code | ✅   | Automatski iz Google Maps API |

**Napomena o Google Plus Code:** Plus Code se automatski generira na osnovu koordinata putem Google Maps integracije. Ovo osigurava preciznu i standardiziranu identifikaciju lokacije, posebno korisnu za mjesta koja nemaju jasnu adresu.
### Place vs Event — ključne razlike

| Aspekt | Event | Place |
| --- | --- | --- |
| Vremensko ograničenje | Da (startDateTime, endDateTime) | Ne  |
| Automatski istek | Da (`expired`) | Ne  |
| Može imati hijerarhiju | Da (parent/child) | Ne  |
| Može biti otkazan | Da (`canceled`) | Ne  |
| Povezani eventi | Može biti vezan za Place (istog vlasnika) | Prikazuje evente vlasnika |
| Lokacija listinga | Obavezna (Place ili ručna) | Obavezna (adresa + koordinate) |
### Brisanje Place-a

Brisanje mjesta je kontrolisano zbog povezanih događaja:

1. **Ima evente u aktivnim statusima** (`published`, `published_under_review`, `published_needs_changes`)? → Brisanje blokirano. Poruka: "Prvo otkažite ili sakrijte aktivne događaje."
2. **Nema aktivnih evenata:**
  - Ako je Place `wasEverActive = false`: prelazi u `removed` sa `removedReason = account_deleted`
  - Ako je Place `wasEverActive = true`: direktno brisanje nije dostupno — vlasnik može koristiti `hidden_by_owner` ili zatražiti od moderatora trajno uklanjanje
  - Prošli eventi (`expired`) zadržavaju snapshot lokacije

> **💡 Praktična napomena:** Snapshot čuva sve potrebne podatke (naziv, adresa, koordinate) tako da prošli eventi i dalje mogu prikazati gdje su se održali, čak i kad originalni Place više ne postoji.

* * *
## 4.4 Kategorije
### Šta su kategorije?

Kategorije su osnovna struktura za organizaciju sadržaja na platformi. Organizovane su u dva nivoa: **sektori** (široke grupe poput "Hrana i piće" ili "Kupovina") i **kategorije** (konkretni tipovi unutar sektora, poput "Restorani" ili "Baumarketi"). Svaki listing mora pripadati barem jednoj kategoriji (primarnoj), a može pripadati i dodatnim sekundarnim kategorijama (maksimalan broj definisan parametrom `MAX_SECONDARY_CATEGORIES`). Kategorije su **kontrolisane od strane administratora** — korisnici ih ne mogu kreirati, samo odabrati iz ponuđene liste.

Korisnik pri kreiranju listinga bira sektor (za lakše snalaženje), zatim kategoriju unutar tog sektora. Sekundarne kategorije može birati iz bilo kojeg sektora istog tipa (Place ili Event).

**Važno:** Eventi i Places imaju **potpuno odvojene sisteme kategorija**:

- Eventi koriste `EventCategory` i `EventListingCategories`
- Places koriste `PlaceCategory` i `PlaceListingCategories`

Više o arhitekturi čuvanja kategorija (relaciona tabela + denormalizacija) opisano je u sekciji 4.1.
### Struktura kategorije

| Atribut | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| categoryId | String | Jedinstveni identifikator | ✅   | —   |
| slug | String | URL-friendly identifikator | ✅   | Immutable — ne može se mijenjati |
| name | String | Naziv na primarnom jeziku | ✅   | —   |
| nameAlt | String | Naziv na sekundarnom jeziku | ❌   | —   |
| sectorSlug | String | Slug sektora kojem kategorija pripada | ✅   | Npr. "hrana-i-pice", "kupovina" |
| sectorName | String | Naziv sektora na primarnom jeziku | ✅   | Npr. "Hrana i piće", "Kupovina" |
| sectorNameAlt | String | Naziv sektora na sekundarnom jeziku | ❌   | —   |
| description | String | Opis kategorije | ❌   | —   |
| icon | String | Emoji ili ikona | ❌   | Za vizualni prikaz |
| color | String | Hex kod boje | ❌   | Za UI elemente |
| defaultImageUrl | String | Default slika za listinge bez vlastite slike | ❌   | Fallback u hijerarhiji slika |
| sortOrder | Number | Redoslijed prikaza | ✅   | —   |
| isActive | Boolean | Da li je aktivna | ✅   | —   |

> **📝 Napomena:** Sektor nije zaseban entitet — `sectorSlug` i `sectorName` su denormalizovani atributi na kategoriji. Ovo pojednostavljuje model jer sektori služe isključivo za UI grupiranje, nemaju vlastitu poslovnu logiku.
### Primarna vs sekundarne kategorije

| Aspekt | Primarna | Sekundarne |
| --- | --- | --- |
| Obaveznost | Obavezna za svaki listing | Opcione |
| Broj | Tačno jedna | Do `MAX_SECONDARY_CATEGORIES` |
| Glavna svrha | Definira "šta je" listing | Proširuje vidljivost u pretrazi |
| Prikaz | Uvijek vidljiva na kartici | Vidljive u detaljima i filterima |
| Čuvanje | Denormalizovano u Listing + relaciona tabela | Samo relaciona tabela |
### Kategorije mjesta (PlaceCategory)

16 sektora pokriva sve tipove mjesta na platformi:

| #   | Sektor | Kategorije |
| --- | --- | --- |
| 1   | 🍽️ **Hrana i piće** | Restorani · Kafići · Barovi · Pub-ovi · Lounge barovi · Pekare · Fast food · Slastičarne · Ćevabdžinice i ašćinice |
| 2   | 🎉 **Zabava** | Noćni život · Kladionice · Escape room · Bowling |
| 3   | 🛍️ **Kupovina** | Tržni centri · Supermarketi · Robne kuće · Baumarketi · Bijela tehnika · Namještaj · Građevinski materijal · Alati · Sanitarije · Bašta i vrt · Tehnika i elektronika · Odjeća i obuća · Sportska oprema · Knjižare · Suvenirnice · Kiosci i trafike · Pijace i tržnice · Ostale prodavnice |
| 4   | 🏥 **Zdravlje** | Bolnice i klinike · Apoteke · Stomatologija · Fizioterapija · Optike · Laboratorije |
| 5   | 💆 **Ljepota i wellness** | Frizeri · Kozmetika · Barberi · Spa i wellness · Manikir i pedikir |
| 6   | 🏃 **Sport i rekreacija** | Teretane i fitness · Sportski klubovi · Bazeni · Sportski tereni · Parkovi · Planinarski domovi |
| 7   | 🎭 **Kultura** | Muzeji · Galerije · Pozorište · Kino · Biblioteke · Kulturni centri · Znamenitosti i spomenici |
| 8   | 📚 **Obrazovanje** | Škole · Fakulteti · Predškolske ustanove · Autoškole · Kursevi i edukacija |
| 9   | 🏨 **Smještaj** | Hoteli · Hosteli · Apartmani · Pansioni · Moteli |
| 10  | 🚕 **Transport** | Taksi službe · Autobuske stanice · Željezničke stanice · Rent-a-car · Aerodromi · Parking |
| 11  | 🔧 **Usluge** | Automehaničari · Autopraonice · Vulkanizeri · Krojači · Ključari · Štamparije i kopirnice · Brze pošte · Staklorezači · Hemijsko čišćenje · Nekretnine · Turizam · Coworking |
| 12  | 🏛️ **Javne ustanove** | Općina i gradska uprava · Pošta · MUP i lična dokumenta · Policija · Sudovi · Ambasade i konzulati |
| 13  | 🏦 **Finansije** | Banke · Mjenjačnice · Osiguranja |
| 14  | 👶 **Djeca i porodica** | Igraonice · Dječija oprema · Zabavni parkovi |
| 15  | 🐕 **Životinje** | Veterinari · Pet shopovi · Grooming |
| 16  | 🕌 **Vjerski objekti** | Džamije · Crkve · Katedrale · Sinagoge · Groblja i memorijali |
### Kategorije događaja (EventCategory)

11 sektora pokriva sve tipove događaja na platformi:

| #   | Sektor | Kategorije |
| --- | --- | --- |
| 1   | 🎵 **Muzika** | Koncerti · Festivali · Akustične/live svirke · DJ eventi |
| 2   | 🎭 **Kultura i umjetnost** | Izložbe · Pozorišne predstave · Filmske projekcije · Književne večeri · Premijere · Festivali |
| 3   | ⚽ **Sport** | Utakmice · Turniri · Maratoni i trke · Sportska takmičenja |
| 4   | 📚 **Edukacija** | Radionice · Predavanja · Seminari · Konferencije · Kursevi |
| 5   | 🎉 **Zabava** | Žurke · Stand-up komedija · Pub kvizovi · Karaoke večeri · Escape room eventi |
| 6   | 👨‍👩‍👧 **Za djecu i porodicu** | Dječije predstave · Kreativne radionice · Animacije · Porodični izleti · Cirkus |
| 7   | 💼 **Biznis i sajmovi** | Sajmovi · Poslovni meetupi · Startup eventi · Prezentacije · Sajmovi zapošljavanja · Rasprodaje i akcije · Otvaranja · Aukcije |
| 8   | 🏔️ **Outdoor i avantura** | Organizovani izleti · Planinarske ture · Biciklističke ture · Kampovanja |
| 9   | 🍕 **Gastro događaji** | Food festivali · Degustacije · Kulinarski workshopovi |
| 10  | ❤️ **Humanitarno i zajednica** | Humanitarne akcije · Volontiranje · Građanske inicijative · Obilježavanja |
| 11  | 🕌 **Vjerski i tradicija** | Ramazanski i bajramski programi · Božićni programi · Vjerska predavanja · Tradicionalne manifestacije |

> **📝 Napomena:** Ove liste su početne i mogu se proširivati po potrebi. Dodavanje nove kategorije u postojeći sektor je jednostavna operacija. Dodavanje novog sektora zahtijeva definisanje `sectorSlug` i `sectorName` na novim kategorijama. Kategorija "Festivali" pojavljuje se pod Muzika i pod Kultura jer festivali mogu biti muzički ili kulturni — organizator bira primarnu kategoriju prema prirodi svog festivala.
### Princip kategorizacije: Sektor → Kategorija → Tagovi

Tri nivoa organizacije imaju jasno razdvojene uloge:

| Nivo | Čemu služi | Ko upravlja | Primjer |
| --- | --- | --- | --- |
| **Sektor** | Široka grupa za brzu navigaciju | Sistem (fiksno) | Kupovina, Zdravlje, Hrana i piće |
| **Kategorija** | Konkretan tip mjesta/događaja — korisnik bira pri kreiranju listinga | local\_admin | Baumarketi, Apoteke, Restorani |
| **Tagovi** | Slobodne oznake za specifičnosti — vlasnik dodaje po izboru | can\_manage\_tags / local\_admin | parking, wifi, veganski, besplatan ulaz |

Kategorije su na nivou **odjela** — dovoljno specifične da korisnik lako pronađe šta traži, ali ne toliko granularne da stvaraju dileme pri odabiru. Specifičnosti poput pojedinog proizvoda, usluge ili karakteristike pokrivaju tagovi i fulltext pretraga po opisu listinga.
### Aliasi i sinonimi

Korisnici često pretražuju koristeći različite termine za isti koncept — "gym" umjesto "teretana", "picerija" umjesto "restorani", "diskoteka" umjesto "noćni život". Sistem održava **tabelu mapiranja aliasa** koja nevidljivo preusmjerava takve pretrage na odgovarajuću kategoriju.

Aliasi su nevidljivi korisnicima — korisnik vidi samo čiste nazive kategorija, ali pretraga razumije varijante. Staff korisnici (local\_admin) upravljaju aliasima kroz admin panel.

| Alias | Mapira se na |
| --- | --- |
| gym | Teretane i fitness |
| picerija | Restorani |
| diskoteka | Noćni život |
| birtija | Barovi |
| shopping | Tržni centri |
| doktor | Bolnice i klinike |

> **💡 Praktična napomena:** Tabela aliasa je konfigurabilan parametar po tenantu — svaki grad može imati lokalne sinonime. Aliasi se mogu dodavati iterativno na osnovu podataka iz pretrage (npr. analizom "nula rezultata" upita).
### Upravljanje kategorijama

Kategorijama upravljaju **Staff korisnici sa ulogom local\_admin**. Obični korisnici ne mogu kreirati, mijenjati niti brisati kategorije. Kategorije imaju veće implikacije od tagova — slug je immutable, boja i ikona utiču na branding, a deaktivacija utiče na sve listinge koji koriste tu kategoriju — zato je upravljanje ograničeno na administrativnu ulogu.

**Kreiranje kategorije:**

- Definiše se naziv, slug, sektor, ikona, boja
- Slug se automatski generiše iz naziva, ali može se prilagoditi
- Jednom kreiran slug se **ne može mijenjati** (koristi se u URL-ovima)
- Kategorija se dodjeljuje sektoru putem `sectorSlug`

**Deaktivacija kategorije:**

- Kategorija se ne briše, već deaktivira (`isActive = false`)
- Postojeći listinzi zadržavaju vezu sa kategorijom
- Kategorija se više ne prikazuje pri kreiranju novih listinga
- Ovo štiti integritet postojećih podataka

**Brisanje kategorije:**

- Moguće samo ako **nijedan listing** ne koristi tu kategoriju
- U praksi se rijetko koristi — preferira se deaktivacija
### Default slike kategorija

Kada listing nema vlastitu sliku, sistem koristi hijerarhiju za određivanje koja slika će se prikazati:

1. **featuredImageUrl** listinga (ako postoji)
2. **defaultImageUrl** primarne kategorije (atribut na kategoriji — ako postoji)
3. Generic placeholder slika sistema

Ovo osigurava vizualno bogat sadržaj čak i kad korisnici ne uploaduju slike. `defaultImageUrl` se postavlja pri konfiguraciji kategorije od strane Staff korisnika, i tipično prikazuje reprezentativnu sliku za tu vrstu sadržaja (npr. generička slika koncerta za kategoriju "Muzika").

> **💡 Praktična napomena:** Slug kategorije se ne može mijenjati nakon kreiranja jer se koristi u URL-ovima. Ako se želi promijeniti slug, potrebno je kreirati novu kategoriju i migrirati sadržaj — što je kompleksna operacija.

* * *
## 4.5 Tagovi
### Šta su tagovi?

Tagovi omogućavaju **dodatnu, fleksibilniju klasifikaciju** sadržaja. Za razliku od kategorija koje definiraju "šta je" listing, tagovi opisuju njegove **karakteristike i osobine**. Tagovi su opcioni — listing može postojati bez ijednog taga.

Korisnik može odabrati do `MAX_TAGS_PER_LISTING` tagova (parametar — preporučena početna vrijednost: 2). Slugovi odabranih tagova čuvaju se denormalizovano direktno u Listing entitetu (`primaryTagSlug`, `secondaryTagSlug`) radi brzog pristupa.
### Zašto odvojene tabele?

Eventi i Places imaju **potpuno odvojene sisteme tagova**:

- Eventi koriste `EventTags`
- Places koriste `PlaceTags`

Razlog je jednostavan — tagovi su semantički različiti:

| EventTags (opisuju događaj) | PlaceTags (opisuju mjesto) |
| --- | --- |
| besplatno, za-djecu | parking, wifi |
| online, uživo | pet-friendly, dostava |
| radionica, predavanje | halal, vegetarijanski |
| festival, višednevni | rezervacije, kartice |

Gotovo nema preklapanja, a odvojene tabele sprječavaju greške (npr. da neko tagira koncert sa "parking").
### EventTags entitet

| Atribut | Tip | Opis | Obavezno |
| --- | --- | --- | --- |
| tagSlug | String | Jedinstveni identifikator (PK) | ✅   |
| tagName | String | Naziv na primarnom jeziku | ✅   |
| tagNameAlt | String | Naziv na sekundarnom jeziku | ❌   |
| tagIcon | String | Emoji ili ikona (npr. "🎟️") | ❌   |
| orderIndex | Number | Redoslijed prikaza u UI | ✅   |
| isActive | Boolean | Da li je tag dostupan za odabir | ✅   |
### PlaceTags entitet

| Atribut | Tip | Opis | Obavezno |
| --- | --- | --- | --- |
| tagSlug | String | Jedinstveni identifikator (PK) | ✅   |
| tagName | String | Naziv na primarnom jeziku | ✅   |
| tagNameAlt | String | Naziv na sekundarnom jeziku | ❌   |
| tagIcon | String | Emoji ili ikona (npr. "🅿️") | ❌   |
| orderIndex | Number | Redoslijed prikaza u UI | ✅   |
| isActive | Boolean | Da li je tag dostupan za odabir | ✅   |
### Primjeri tagova

**EventTags:**

| Slug | Naziv | Ikona |
| --- | --- | --- |
| besplatno | Besplatan ulaz | 🎟️ |
| za-djecu | Za djecu | 👶  |
| online | Online događaj | 💻  |
| radionica | Radionica | 🛠️ |
| festival | Festival | 🎪  |
| porodicno | Porodično | 👨‍👩‍👧 |

**PlaceTags:**

| Slug | Naziv | Ikona |
| --- | --- | --- |
| parking | Parking | 🅿️ |
| wifi | Besplatan WiFi | 📶  |
| pet-friendly | Pet friendly | 🐕  |
| dostava | Dostava | 🚚  |
| rezervacije | Rezervacije | 📅  |
| kartice | Kartično plaćanje | 💳  |
### Upravljanje tagovima

Tagovima upravljaju **moderatori sa** `can_manage_tags` permisijom ili local\_admin. Za razliku od kategorija koje su ekskluzivna odgovornost local\_admin-a, tagovi su bliži svakodnevnom radu sa sadržajem — moderatori koji pregledaju listinge najbolje vide koje tagove korisnici trebaju. Permisiju `can_manage_tags` dodjeljuje Operator.

**Kreiranje taga:**

- Definiše se slug, naziv, ikona i redoslijed
- Slug mora biti jedinstven unutar tabele (EventTags ili PlaceTags)
- Novi tagovi su odmah dostupni za odabir (`isActive = true`)

**Deaktivacija taga:**

- Tag se može deaktivirati (`isActive = false`)
- Postojeći listinzi zadržavaju tag
- Tag se više ne prikazuje pri kreiranju/editovanju listinga

**Brisanje taga:**

- Tag se može obrisati
- Listinzi koji su koristili obrisani tag ostaju bez tog taga (polje postaje NULL)
- Ovo je sigurna operacija — ne utiče na vidljivost listinga
### Spajanje tagova

Kada postoje tagovi sa istim ili sličnim značenjem (npr. "wifi" i "wi-fi", ili "za-djecu" i "porodicno" nakon odluke da se objedine), moderator sa `can_manage_tags` permisijom (ili local\_admin) može pokrenuti spajanje. Proces je sljedeći:

1. Odabere **source** tag (koji će biti uklonjen) i **target** tag (koji ostaje kao master)
2. Sistem pronalazi sve listinge koji koriste source tag — bilo kao `primaryTagSlug` ili `secondaryTagSlug`
3. Za svaki pogođeni listing, source slug se zamjenjuje target slugom na odgovarajućoj poziciji
4. Ako listing već koristi target tag na drugoj poziciji (npr. ima source kao primary i target kao secondary), pozicija source taga se čisti (NULL) kako ne bi došlo do duplikata
5. Source tag se trajno briše iz sistema
6. Cijela operacija se loguje za audit, uključujući listu pogođenih listinga

> **💡 Praktična napomena:** Trenutni model je namjerno jednostavan. Ako se u budućnosti pokaže potreba za vezivanjem tagova uz specifične kategorije (npr. tag "halal" samo za kategoriju "Restorani"), model se može proširiti bez breaking changes.

* * *
## 4.6 Multimedija sistem
### Kako funkcionišu slike?

Sistem multimedije omogućava korisnicima da dodaju vizuelni sadržaj — glavnu sliku (featured) i galeriju do 5 slika. Svaka uploadovana slika prolazi kroz automatsku validaciju i AI screening prije nego što postane vidljiva.

Arhitektura je dizajnirana za performanse: slike se automatski optimizuju u više verzija za različite uređaje, čuvaju na CDN-u, i lazy-loadaju gdje je moguće.
### Image entitet

| Atribut | Tip | Opis | Obavezno |
| --- | --- | --- | --- |
| imageId | String | Jedinstveni identifikator | ✅   |
| listingId | String | Povezani listing | ✅   |
| url | String | Putanja do originalne slike | ✅   |
| thumbnailUrl | String | Thumbnail verzija | ✅   |
| mediumUrl | String | Srednja verzija | ✅   |
| altText | String | Alternativni tekst | ❌   |
| altTextAlt | String | Alt tekst na sekundarnom jeziku | ❌   |
| width | Number | Širina u pikselima | ✅   |
| height | Number | Visina u pikselima | ✅   |
| sizeKb | Number | Veličina u KB | ✅   |
| format | Enum | jpg, png, webp | ✅   |
| isFeatured | Boolean | Da li je glavna slika | ✅   |
| orderIndex | Number | Redoslijed u galeriji (0-4) | ✅   |
| uploadedAt | DateTime | Datum uploada | ✅   |
### Verzije slika

Sistem automatski generiše optimizirane verzije:

| Verzija | Dimenzije | Upotreba |
| --- | --- | --- |
| Thumbnail | 300×200 | Liste, kartice |
| Medium | 800×600 | Glavni prikaz |
| Original | Kao uploadovano | Full screen |
| WebP | Sve verzije | Moderni browseri |
### Upload validacije

| Provjera | Pravilo |
| --- | --- |
| Format | JPG, PNG, WebP |
| Maksimalna veličina | 5 MB |
| Minimalna rezolucija | 800×600 piksela |
| Maksimalna rezolucija | 4000×4000 piksela |
### AI Content Screening

Svaka slika prolazi automatsku provjeru neprimjerenog sadržaja. Sistem koristi AI za detekciju:

- **Adult content** → Automatski odbaci
- **Violence** → Automatski odbaci
- **Offensive text** → Označi za manual review
- **Personal info** → Upozorenje korisniku

> **💡 Praktična napomena:** Korisnici čija se slika odbije dobijaju jasno objašnjenje zašto. Ponovljeni pokušaji uploada neprimjerenog sadržaja mogu rezultirati suspenzijom naloga.

* * *
## 4.7 Dokumenti listinga i verifikacija vlasništva
### Zašto dokumenti?

Korisnici mogu uploadovati dokumente vezane za listing — bilo za verifikaciju vlasništva, pojašnjenja tražena od moderatora, ili druge svrhe. Svi dokumenti su centralizirani u jednom entitetu (**ListingDocument**) koji služi kao jedini izvor istine za sve dokumente vezane za listing, bez obzira na svrhu.

Dokument se može uploadovati pri kreiranju listinga (npr. vlasnik odmah prilaže verifikacioni dokument) ili naknadno kroz Message sistem (npr. moderator traži pojašnjenje). U oba slučaja koristi se isti entitet i isti upload mehanizam.

Centralizirani pristup ima značajne prednosti:

- **Jedno mjesto** — svi dokumenti listinga su na jednom mjestu, bez obzira na svrhu
- **Virus scanning** — skeniranje se radi jednom, pri uploadu
- **Jednostavnije upravljanje** — brisanje, pristup, GDPR compliance
- **Poruke su lakše** — samo referenciraju dokument, ne sadrže ga direktno
### ListingDocument entitet

| Atribut | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| documentId | String | Jedinstveni identifikator | ✅   | —   |
| listingId | String | ID povezanog listinga | ✅   | —   |
| uploadedBy | String | ID korisnika koji je uploadao | ✅   | —   |
| purpose | Enum | Svrha dokumenta | ✅   | `verification`, `clarification`, `other` |
| fileName | String | Originalni naziv fajla | ✅   | —   |
| fileUrl | String | Putanja do dokumenta | ✅   | —   |
| mimeType | String | MIME tip fajla | ✅   | —   |
| fileSizeKb | Number | Veličina u KB | ✅   | —   |
| virusScanStatus | Enum | Status skeniranja | ✅   | `pending`, `clean`, `infected` |
| virusScannedAt | DateTime | Vrijeme skeniranja | ❌   | —   |
| documentStatus | Enum | Status pregleda dokumenta | ✅   | `pending`, `accepted`, `rejected` |
| reviewedAt | DateTime | Datum pregleda | ❌   | —   |
| reviewNote | String | Napomena moderatora o dokumentu | ❌   | —   |
| uploadedAt | DateTime | Datum uploada | ✅   | —   |

> ⚠️ **Napomena o terminologiji:** `documentStatus` koristi termine `accepted` / `rejected` (umjesto `verified`) da se izbjegne zabuna sa `verificationStatus` na listingu. Dokument može biti `accepted` (moderator je pregledao i prihvatio), a listing `verified` (vlasništvo je potvrđeno). To su dva odvojena koncepta — listing može biti `verified` i bez ikakvih dokumenata, a dokument može biti `accepted` kao dio procesa ali nije jedini osnov za verifikaciju.

> **📝 Napomena:** Lista atributa nije konačna i može se proširivati prema potrebama proizvoda. Dokumenti su privatni — vidljivi samo vlasniku listinga i moderatorima.
#### Svrhe dokumenata (purpose)

| Svrha | Opis | Tipični dokumenti |
| --- | --- | --- |
| `verification` | Dokaz vlasništva/prava upravljanja | Vlasnički list, ugovor, licenca, rješenje o registraciji |
| `clarification` | Pojašnjenje za moderatora | Programi, dodatne informacije, dozvole |
| `other` | Ostalo | Različito |
### Upload i virus scanning

Svi uploadovani dokumenti prolaze kroz automatsko skeniranje prije nego postanu dostupni. Workflow je jednostavan:

1. Korisnik uploada dokument → `virusScanStatus = pending`
2. Sistem skenira fajl (asinhrono)
3. Ako je čist → `virusScanStatus = clean`, dokument dostupan
4. Ako je inficiran → `virusScanStatus = infected`, dokument nedostupan, korisnik obaviješten

**Ograničenja uploada:**

| Parametar | Vrijednost |
| --- | --- |
| Dozvoljeni formati | PDF, JPG, PNG |
| Maksimalna veličina | 10 MB po dokumentu |
| Maksimalan broj | 3 dokumenta po listingu |
### Verifikacija vlasništva

Upload dokumenta **nije obavezan** za objavu listinga, ali donosi značajne prednosti i direktno utiče na životni ciklus listinga:

- **Brža moderacija** — listinzi sa dokumentacijom prolaze prioritetno
- **Veće povjerenje** — verifikovani sadržaj se vizualno ističe korisnicima (badge "✓ Potvrđen vlasnik")
- **Zaštita od sporova** — dokumentacija služi kao dokaz u slučaju reklamacija
#### verificationStatus

Verifikacija je dio Listing entiteta — svaki listing ima `verificationStatus` atribut koji prati status verifikacije:

| Status | Značenje | Vizualni prikaz |
| --- | --- | --- |
| `unverified` | Vlasništvo nije potvrđeno | Bez oznake |
| `pending` | Dokumentacija čeka pregled moderatora | "U procesu verifikacije" |
| `verified` | Vlasništvo potvrđeno | ✓ Potvrđen vlasnik (badge) |
#### Kako verifikacija utiče na listing

Verifikacija nije odvojen proces — integrisana je u standardnu moderaciju listinga. Moderator može postaviti `verificationStatus = verified` na osnovu priloženog dokumenta, ali i na osnovu drugih informacija — dokument **nije obavezan uslov** za verified status. Moderator koristi vlastitu procjenu.

| Listing odluka | Osnova za verifikaciju | Rezultat za verificationStatus |
| --- | --- | --- |
| Approve | Validan dokument priložen | `verified` |
| Approve | Moderator ima drugog osnova (poznaje biznis, email potvrda, itd.) | `verified` |
| Approve | Nema osnova za verifikaciju | `unverified` |
| Approve | Nevalidan/nedovoljan dokument | `unverified` + feedback korisniku |
| Reject | Bilo koji | Nije relevantno (listing odbijen) |
#### Verifikacija po Trust Tier-u

Mehanizam verifikacije se razlikuje po Trust Tier-u korisnika:

| Tier | Mehanizam | Dokument |
| --- | --- | --- |
| **0–2** | Na nivou listinga — moderator odlučuje per listing | Poslovna odluka moderatora |
| **3 (Established)** | Na nivou korisnika — `isVerifiedPublisher` flag | Poslovna odluka moderatora |
| **4 (Verified Partner)** | Automatska — ugovorni odnos | Nije potreban |

Za Tier 3, `isVerifiedPublisher` flag na nivou korisnika automatski daje `verified` status svim listinzima tog korisnika — bez potrebe za uploadom dokumenata po svakom listingu. Za Tier 4, svi listinzi automatski dobijaju `verified` jer ugovorni odnos već uključuje potvrdu identiteta. Detalji u [05 - Moderacija, sekcija 5.6.3](05-moderacija.md).
#### Naknadno traženje dokumentacije

Moderatori mogu zatražiti dokumentaciju za **bilo koji aktivan listing** ako postoji sumnja u legitimnost. U tom slučaju:

- Listing ostaje vidljiv (ako je već aktivan)
- Korisnik dobija notifikaciju sa zahtjevom
- Ima `CHANGES_REQUESTED_TIMEOUT_DAYS` dana za dostavu dokumentacije (parametar — preporučena početna vrijednost: 7 dana)
- Nedostavljanje može rezultirati skrivanjem listinga
#### Primjeri prihvatljivih dokumenata

**Za Event:** ugovor sa lokacijom, dozvola za održavanje, ovlaštenje organizatora, potvrda zakupa prostora

**Za Place:** vlasnički list, izvod iz registra, ugovor o zakupu, ovlaštenje za upravljanje, rješenje o registraciji obrta/firme

> **💡 Praktična napomena:** Za Places, verifikacioni status ima veću težinu jer predstavljaju stalne poslovne subjekte. Dokumenti stariji od 2 godine od zatvaranja listinga mogu biti automatski obrisani radi usklađenosti sa GDPR-om. Detalji o workflow-u verifikacije iz moderatorske perspektive opisani su u [05 - Moderacija, sekcija 5.6](05-moderacija.md).

* * *
## 4.8 Lifecycle i vidljivost
### Novi statusni model

CityInfo koristi **jednostatus model** koji opisuje kompletan životni ciklus listinga kroz jedno polje `listingStatus` sa 12 eksplicitnih vrijednosti. Ovaj model zamjenjuje stari dvostatus pristup (lifecycleStatus + moderationStatus + closedReason) koji je generisao nevalidne kombinacije statusa i kompleksnu kalkulacijsku logiku.

Ideja je jednostavna: svako stanje u kojem se listing može naći ima svoju eksplicitnu vrijednost — nema skrivene logike koja se izvodi iz kombinacije dva polja. Dijagram tranzicija i narativni scenariji dostupni su u [Novi listing statusni model — specifikacija](novi-listing-statusni-model-specifikacija.md).
### Pregled statusa

| Status | Opis | isPublic | Terminalan? |
| --- | --- | --- | --- |
| `draft` | Korisnik priprema, nije submitovao | ❌   | Ne  |
| `in_review` | Čeka pregled moderatora (pre-mod ili resubmit) | ❌   | Ne  |
| `changes_requested` | Moderator vratio, nevidljiv, čeka popravku | ❌   | Ne  |
| `published` | Vidljiv i aktivan, sve OK | ✅   | Ne  |
| `published_under_review` | Vidljiv, čeka naknadni pregled (post-mod tok) | ✅   | Ne  |
| `published_needs_changes` | Vidljiv, moderator traži blagu izmjenu | ✅   | Ne  |
| `hidden_by_owner` | Korisnik privremeno sakrio, može sam vratiti | ❌   | Ne  |
| `hidden_by_moderator` | Moderator sakrio bez zahtjeva prema vlasniku (moderator istražuje sam) | ❌   | Ne  |
| `hidden_by_system` | AI blokada ili korisnik blokiran; zahtijeva moderatorski pregled | ❌   | Ne  |
| `expired` | Event prošao; ostaje vidljiv kao historijski zapis | ✅   | ✅   |
| `canceled` | Vlasnik otkazao event; vidljiv sa ograničenjima (vidi ispod) | ✅\* | Ne\*\* |
| `removed` | Trajno uklonjeno; ne može se vratiti | ❌   | ✅   |

\* `canceled` je `isPublic = true` ali sa ograničenom vidljivošću.  
\*\* `canceled` je reverzibilan ako `endDateTime > NOW()`.

**Napomena:** `canceled` važi samo za **Event listing** — Place ne može biti `canceled`.
### Vidljivost za `canceled` status

Event u `canceled` statusu ostaje javno dostupan, ali sa važnim ograničenjima:

- Prikazuje se sa badge-om "Otkazano"
- **Uključen u:** pretragu (sa badge-om), direktan link, korisnikov profil, favoriti
- **Isključen iz:** naslovne stranice, feed-ova, promoted listi i "nadolazeći događaji" sekcija

Aktivne promocije se **pauziraju** pri prelasku u `canceled` — promotivni timer se zaustavlja i ne troši plaćeni period. Ako vlasnik reaktivira event (a promotivni period nije istekao), promocija se automatski nastavlja od tačke gdje je pauzirana.
### isPublic derivacija

`isPublic` je **kalkulisano polje** — nikad se ne upisuje direktno. Derivira se iz `listingStatus`:

```
isPublic = listingStatus IN (
  'published',
  'published_under_review',
  'published_needs_changes',
  'expired',
  'canceled'
)
```

Svi ostali statusi rezultuju u `isPublic = false`.
### wasEverActive

`wasEverActive` postaje `true` čim listing prvi put uđe u bilo koji `isPublic = true` status. Jednom kad postane `true`, nikad se ne vraća na `false` — čak ni ako listing naknadno pređe u `hidden` ili `removed` status.

Praktična implikacija je na **mogućnost brisanja**:

- `wasEverActive = false` → korisnik može trajno obrisati listing (`removed` sa `account_deleted`)
- `wasEverActive = true` → direktno brisanje nije dostupno; korisnik može sakriti ili otkazati (za evente)

Razlog: listinzi koji su bili vidljivi mogli su biti favorisani, komentirani ili dijeljeni — "brisanje" bi narušilo korisničko iskustvo osoba koje su interagovale sa sadržajem.
### Dijagram tranzicija

```
stateDiagram-v2
    [*] --> draft : Kreiranje listinga

    draft --> in_review : Submit (Tier 0-1)
    draft --> published_under_review : Submit (Tier 2+)
    draft --> removed : Brisanje (wasEverActive=false)

    in_review --> published : Moderator odobrava
    in_review --> changes_requested : Moderator traži izmjene
    in_review --> removed : Moderator odbija (removedReason: rejected)
    in_review --> hidden_by_system : AI blokira
    in_review --> draft : Korisnik povlači

    changes_requested --> in_review : Resubmit
    changes_requested --> removed : Brisanje (wasEverActive=false)

    published --> hidden_by_owner : Korisnik sakriva
    published --> in_review : Izmjena (Tier 0-1)
    published --> published_under_review : Izmjena (Tier 2+)
    published --> canceled : Korisnik otkazuje event
    published --> expired : endDateTime prošao
    published --> hidden_by_moderator : Moderator sakriva
    published --> hidden_by_system : AI/sistem blokira
    published --> removed : Moderator uklanja

    published_under_review --> published : Moderator odobrava
    published_under_review --> published_needs_changes : Moderator traži izmjenu
    published_under_review --> hidden_by_moderator : Moderator sakriva
    published_under_review --> removed : Moderator odbija (removedReason: rejected)
    published_under_review --> hidden_by_owner : Korisnik sakriva
    published_under_review --> canceled : Korisnik otkazuje
    published_under_review --> expired : endDateTime prošao

    published_needs_changes --> published_under_review : Korisnik submita popravku
    published_needs_changes --> hidden_by_owner : Korisnik sakriva
    published_needs_changes --> hidden_by_moderator : Moderator eskalira

    hidden_by_owner --> published : Korisnik prikazuje
    hidden_by_owner --> hidden_by_moderator : Moderator eskalira
    hidden_by_owner --> removed : Moderator uklanja

    hidden_by_moderator --> in_review : Korisnik resubmituje
    hidden_by_moderator --> published : Moderator vraća
    hidden_by_moderator --> removed : Moderator uklanja

    hidden_by_system --> published : Moderator odobrava
    hidden_by_system --> removed : Moderator odbija (removedReason: rejected)
    hidden_by_system --> removed : Moderator uklanja

    canceled --> published : Reaktivacija (endDateTime > NOW)
    canceled --> expired : endDateTime prošao
    canceled --> removed : Moderator uklanja

    expired --> [*]
    removed --> [*]
```
### Tok po Trust Tier-u

Korisnikov Trust Tier direktno određuje **koji tok listing prolazi** pri objavi. Kompletna specifikacija Trust Tier sistema je u [03 - Korisnici i pristup](03-korisnici-i-pristup.md), a moderacijski workflow u [05 - Moderacija](05-moderacija.md). Ovdje je prikazan praktični efekat na listing:

**Pre-moderacija (Tier 0 — Restricted, Tier 1 — Standard):**

Korisnik klikne "Objavi" → listing prelazi u `in_review` → čeka u moderacijskom redu → moderator odlučuje → tek nakon odobrenja listing prelazi u `published` i postaje vidljiv.

- Korisnik može imati maksimalno `TIER_PRE_MOD_MAX_PENDING` objava koje istovremeno čekaju pregled
- Ciljno vrijeme odluke: 2 sata (detaljni SLA prioriteti u [05 - Moderacija, sekcija 5.2.4](05-moderacija.md))

**Post-moderacija (Tier 2 — Trusted, Tier 3 — Established, Tier 4 — Verified Partner):**

Korisnik klikne "Objavi" → listing **odmah prelazi u** `published_under_review` i postaje vidljiv → moderator pregleda naknadno. Ako moderator pronađe problem, može sakriti listing ili zatražiti izmjene.

- Tier 2: sav sadržaj se pregleda naknadno (100%)
- Tier 3 i 4: pregleda se samo uzorak sadržaja (sampling — konfiguracijski parametri)
- Ciljno vrijeme naknadnog pregleda: 8 sati

> **💡 Praktična napomena:** Novi korisnici počinju kao Tier 1. Automatski napreduju prema Tier 2 kada ispune konfigurisane pragove (minimum odobrenih objava, procenat uspješnosti, starost računa). Detalji o napredovanju i degradaciji u [03 - Korisnici i pristup, sekcija 3.4](03-korisnici-i-pristup.md).
### Ažuriranje aktivnog listinga

Korisnik može editovati listing koji je već vidljiv javnosti. Ponašanje pri editu ovisi o Trust Tier-u — važno je balansirati dvije potrebe: da promjene budu brzo vidljive i da kvalitet sadržaja ostane pod kontrolom.

**Tier 0, 1 (pre-moderacija):**

Listing se pri editu **skriva** (prelazi u `in_review`) i šalje na moderaciju. Korisnik dobija poruku da će listing ponovo postati vidljiv nakon odobrenja. Ovo osigurava da korisnici sa nižim nivoom povjerenja ne mogu zaobići moderaciju kroz naknadne izmjene.

**Tier 2+ (post-moderacija):**

Listing **ostaje vidljiv** tokom i nakon edita — prelazi u `published_under_review`. Izmjene su odmah primijenjene. Moderator pregleda naknadno; ako utvrdi problem, može sakriti listing ili zatražiti izmjene.

> **💡 Praktična napomena:** Ovaj pristup omogućava Verified Partner-u da ispravi radno vrijeme restorana bez čekanja odobrenja, dok novi korisnik ne može zaobići kontrolu kvaliteta izmjenom sadržaja nakon inicijalnog odobrenja.
### Šta se dešava sa listinzima blokiranog korisnika

Kada se korisnik blokira (vidi [03 - Korisnici i pristup, sekcija 3.7](03-korisnici-i-pristup.md)), ponašanje ovisi o tipu blokiranja:

**Ručno blokiranje (moderator):** Moderator pri blokiranju bira šta se dešava sa sadržajem:

- **Opcija 1 — Listinzi ostaju vidljivi (default):** Aktivni listinzi ostaju javno vidljivi, ali korisnik ne može kreirati nove niti editovati postojeće. Aktivne promocije se otkazuju bez povrata kredita.
- **Opcija 2 — Listinzi se sakrivaju:** Svi aktivni listinzi prelaze u `hidden_by_system`. Pri odblokiranju se automatski reaktiviraju.

**Instant blokiranje (sistem):** Kod automatskog blokiranja (hate speech, spam, malicious sadržaj), **default je sakrivanje sadržaja** — svi aktivni listinzi automatski prelaze u `hidden_by_system`. Moderator pri pregledu može reaktivirati sadržaj.

**Trajno blokiranje:** Ako se korisnik trajno blokira sa uklanjanjem sadržaja, svi aktivni listinzi prelaze u `hidden_by_system`. Moderator pri pregledu odlučuje o daljem statusu svakog listinga.

Detalji o razlici između ručnog i instant blokiranja u [05 - Moderacija, sekcija 5.4.4](05-moderacija.md).
### Timeout za changes\_requested

Kada moderator vrati listing na doradu (`changes_requested`), korisnik ima ograničeno vrijeme za odgovor. Ako ne reaguje u roku od `CHANGES_REQUESTED_TIMEOUT_DAYS` dana (parametar — preporučena početna vrijednost: 7 dana), listing automatski prelazi u `removed` (removedReason: `rejected`).

Sistem šalje reminder notifikaciju korisniku na `CHANGES_REQUESTED_REMINDER_DAYS` dana prije isteka (parametar — preporučena početna vrijednost: 2 dana prije isteka, tj. 5. dan).

> **💡 Praktična napomena:** Timeout sprječava nakupljanje "zombie" listinga koji beskonačno stoje u `changes_requested` statusu. Korisnik uvijek može kreirati novi listing ako propusti rok.
### Detaljnija specifikacija

Za kompletnu tabelu dozvoljenih tranzicija, zabranjene tranzicije, detaljna pravila za `removedReason`, `wasEverActive` granične slučajeve, i narativne scenarije (12 scenarija koji pokrivaju sve tipične tokove), vidi: [Novi listing statusni model — specifikacija](novi-listing-statusni-model-specifikacija.md).

* * *
## 4.9 Korisničke interakcije
### Šta su korisničke interakcije?

Pored kreiranja sadržaja, korisnici mogu interagovati sa listinzima na tri načina: **lajkovanje** (appreciation), **spremanje u favorite** i **dijeljenje**. Ove interakcije obogaćuju korisničko iskustvo i pružaju socijalne signale koji pomažu u otkrivanju kvalitetnog sadržaja.
### Lajkovi (Appreciation)

Lajk je najjednostavnija forma interakcije — korisnik izražava pozitivan stav prema listingu. Sistem podržava lajkove i za registrovane korisnike i za neregistrovane posjetioce (visitors), ali sa različitom logikom.
#### Registrovani korisnici

Za registrovane korisnike, lajkovi se trajno evidentiraju i korisnik može vidjeti historiju svojih lajkova. Korisnik može unlike-ovati listing — lajk se uklanja i `totalAppreciations` se dekrementira.

**Appreciation entitet:**

| Atribut | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| appreciationId | String | Jedinstveni identifikator | ✅   | —   |
| userId | String | ID registrovanog korisnika | ✅   | —   |
| listingId | String | ID lajkovanog listinga | ✅   | —   |
| createdAt | DateTime | Vrijeme lajka | ✅   | —   |

> **📝 Napomena:** Lista atributa nije konačna. Kombinacija `userId + listingId` je jedinstvena — korisnik može lajkati isti listing samo jednom.
#### Neregistrovani korisnici (Visitors)

Visitors mogu lajkati listinge, ali na jednostavniji način:

- **Samo brojač:** Lajk se samo dodaje na `totalAppreciations` listinga
- **Bez historije:** Ne čuva se informacija o tome ko je lajkao
- **Zaštita od zloupotrebe:** Sistem kombinuje IP adresu i digitalni otisak preglednika kako bi prepoznao i ignorisao ponavljane interakcije

Visitor lajkovi ne kreiraju Appreciation zapis — samo inkrementiraju `totalAppreciations` na listingu.

> ⚠️ **Smjernica za implementaciju:** Sistem ne čuva IP adresu ni fingerprint podatke u sirovom obliku. Za detekciju duplikata koristi se jednosmjerni hash kombinacije identifikacionih signala i listingId — ovaj hash nije reverzibilan i ne predstavlja lični podatak u smislu GDPR-a. Ne praviti tabelu sa sirovim visitor podacima.

> **💡 Praktična napomena:** `totalAppreciations` uključuje i registrovane i visitor lajkove, čime se listing broj uvijek reflektuje ukupnu popularnost. Za preciznu statistiku, može se prebrojati Appreciation entitete (registrovani) i oduzeti od ukupnog broja (razlika su visitor lajkovi).
### Favoriti (Saved listings)

Registrovani korisnici mogu spremiti listinge u listu favorita za kasniji pristup. Ovo je korisno za planiranje — npr. korisnik pronađe zanimljive evente za vikend i spremi ih dok ne odluči koji da posjeti.

**Favorite entitet:**

| Atribut | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| favoriteId | String | Jedinstveni identifikator | ✅   | —   |
| userId | String | ID registrovanog korisnika | ✅   | —   |
| listingId | String | ID spremljenog listinga | ✅   | —   |
| createdAt | DateTime | Vrijeme spremanja | ✅   | —   |

> **📝 Napomena:** Kombinacija `userId + listingId` je jedinstvena. Visitors ne mogu koristiti favorite — to zahtijeva registraciju.

**Ponašanje:**

- Korisnik može dodati i ukloniti listing iz favorita
- Lista favorita je dostupna u korisnikovom profilu
- Ako se listing zatvori ili obriše, zapis ostaje u favoritima ali se prikazuje kao "Više nije dostupan" (graceful degradation)
- Favoriti su privatni — samo korisnik vidi svoju listu
### Dijeljenje (Share)

Korisnici (uključujući visitors) mogu podijeliti listing putem linka. Mehanizam dijeljenja koristi **native share API** preglednika/uređaja gdje je dostupan (mobilni uređaji), a kao fallback nudi **copy-to-clipboard** opciju.

**Šta se dijeli:**

- Direktan URL na detaljnu stranicu listinga
- URL uključuje meta tagove za social media preview (Open Graph) — naslov, sliku, kratki opis

**Praktična napomena:** Dijeljenje ne zahtijeva nikakvu autentifikaciju. Dijeljeni link vodi na javnu stranicu listinga koju može vidjeti bilo ko, uključujući visitors.

* * *
## 4.10 API Endpoints
### Event operacije

| Metoda | Putanja | Opis |
| --- | --- | --- |
| GET | `/events` | Lista evenata sa filterima |
| GET | `/events/{id}` | Detalji pojedinačnog eventa |
| POST | `/events` | Kreiranje novog eventa |
| PUT | `/events/{id}` | Ažuriranje eventa |
| DELETE | `/events/{id}` | Brisanje eventa (`wasEverActive = false`) |
| POST | `/events/{id}/submit` | Slanje na moderaciju |
| POST | `/events/{id}/withdraw` | Povlačenje submission-a (`in_review` → `draft`) |
| POST | `/events/{id}/cancel` | Otkazivanje eventa (`published` → `canceled`) |
| POST | `/events/{id}/reactivate` | Reaktivacija otkazanog eventa (`canceled` → `published`) |
| POST | `/events/{id}/hide` | Privremeno sakrivanje (`published` → `hidden_by_owner`) |
| POST | `/events/{id}/unhide` | Ponovno prikazivanje (`hidden_by_owner` → `published`) |
| POST | `/events/{id}/children` | Kreiranje child eventa |
| GET | `/events/{id}/children` | Lista child evenata |
| POST | `/events/{id}/refresh` | Ručno osvježavanje sortDate (jednom u 24h) |
### Place operacije

| Metoda | Putanja | Opis |
| --- | --- | --- |
| GET | `/places` | Lista mjesta sa filterima |
| GET | `/places/{id}` | Detalji pojedinačnog mjesta |
| GET | `/places/{id}/events` | Eventi povezani sa mjestom |
| POST | `/places` | Kreiranje novog mjesta |
| PUT | `/places/{id}` | Ažuriranje mjesta |
| DELETE | `/places/{id}` | Brisanje mjesta (`wasEverActive = false`) |
| POST | `/places/{id}/submit` | Slanje na moderaciju |
| POST | `/places/{id}/withdraw` | Povlačenje submission-a (`in_review` → `draft`) |
| POST | `/places/{id}/hide` | Sakrivanje mjesta (`published` → `hidden_by_owner`) |
| POST | `/places/{id}/unhide` | Ponovno prikazivanje (`hidden_by_owner` → `published`) |
| POST | `/places/{id}/refresh` | Ručno osvježavanje sortDate (jednom u 24h) |
### Kategorije

| Metoda | Putanja | Opis |
| --- | --- | --- |
| GET | `/event-categories` | Lista kategorija za evente |
| GET | `/place-categories` | Lista kategorija za mjesta |
| POST | `/event-categories` | Kreiranje kategorije (local\_admin) |
| PUT | `/event-categories/{id}` | Ažuriranje kategorije (local\_admin) |
| DELETE | `/event-categories/{id}` | Brisanje kategorije (local\_admin) |
### Tagovi

| Metoda | Putanja | Opis |
| --- | --- | --- |
| GET | `/event-tags` | Lista tagova za evente |
| GET | `/event-tags/active` | Samo aktivni tagovi za evente |
| POST | `/event-tags` | Kreiranje taga (can\_manage\_tags / local\_admin) |
| PUT | `/event-tags/{slug}` | Ažuriranje taga (can\_manage\_tags / local\_admin) |
| DELETE | `/event-tags/{slug}` | Brisanje taga (can\_manage\_tags / local\_admin) |
| POST | `/event-tags/merge` | Spajanje dva taga (can\_manage\_tags / local\_admin) |
| GET | `/place-tags` | Lista tagova za mjesta |
| GET | `/place-tags/active` | Samo aktivni tagovi za mjesta |
| POST | `/place-tags` | Kreiranje taga (can\_manage\_tags / local\_admin) |
| PUT | `/place-tags/{slug}` | Ažuriranje taga (can\_manage\_tags / local\_admin) |
| DELETE | `/place-tags/{slug}` | Brisanje taga (can\_manage\_tags / local\_admin) |
| POST | `/place-tags/merge` | Spajanje dva taga (can\_manage\_tags / local\_admin) |
### Aliasi kategorija

| Metoda | Putanja | Opis |
| --- | --- | --- |
| GET | `/category-aliases` | Lista svih aliasa |
| POST | `/category-aliases` | Kreiranje aliasa (local\_admin) |
| DELETE | `/category-aliases/{id}` | Brisanje aliasa (local\_admin) |
### Slike

Endpoint-i za slike koriste generički `/listings/{id}/...` path koji funkcioniše za oba tipa listinga (Event i Place).

| Metoda | Putanja | Opis |
| --- | --- | --- |
| GET | `/listings/{id}/images` | Lista slika za listing |
| POST | `/listings/{id}/images` | Upload nove slike |
| DELETE | `/images/{id}` | Brisanje slike |
| POST | `/images/{id}/set-featured` | Postavljanje kao glavne slike |
| PUT | `/listings/{id}/images/reorder` | Promjena redoslijeda |
### Dokumenti listinga

Kao i slike, dokumenti koriste generički `/listings/{id}/...` path.

| Metoda | Putanja | Opis |
| --- | --- | --- |
| GET | `/listings/{id}/documents` | Lista dokumenata za listing |
| POST | `/listings/{id}/documents` | Upload novog dokumenta |
| GET | `/documents/{id}` | Detalji/download dokumenta |
| DELETE | `/documents/{id}` | Brisanje dokumenta |

**Osnovni request/response shape za upload:**

```
POST /listings/{id}/documents
Request: { file (multipart), purpose }
Response: { documentId, virusScanStatus, uploadedAt }
```
### Korisničke interakcije

| Metoda | Putanja | Opis |
| --- | --- | --- |
| POST | `/listings/{id}/appreciate` | Lajkaj listing |
| DELETE | `/listings/{id}/appreciate` | Ukloni lajk |
| GET | `/users/me/appreciations` | Lista lajkovanih listinga |
| POST | `/listings/{id}/favorite` | Spremi u favorite |
| DELETE | `/listings/{id}/favorite` | Ukloni iz favorita |
| GET | `/users/me/favorites` | Lista favorita |
| GET | `/listings/{id}/share` | Generiši share URL sa meta podacima |

> **📝 Napomena:** Ova lista predstavlja osnovne operacije. Detaljni request/response formati, validacije i error kodovi dokumentovani su u API specifikaciji.

* * *
## Šta dalje?

Nakon razumijevanja strukture sadržaja, preporučeni sljedeći koraci:

- **Moderacija sadržaja:** [05 - Moderacija](05-moderacija.md) — workflow pregleda i odluka
- **Promocije i vidljivost:** [06 - Monetizacija](06-monetizacija.md) — kako promocije utiču na sortDate
- **Korisnički doživljaj:** [02 - Korisnički doživljaj](02-korisnicko-iskustvo.md) — kako se sadržaj prikazuje korisnicima

* * *
## Changelog

| Verzija | Datum | Opis |
| --- | --- | --- |
| 2.2 | 3.4.2026 | **Optimizacija 13→12 statusa.** `rejected` uklonjen kao zaseban `listingStatus`, dodan kao `removedReason`. `user_delete` → `account_deleted`. `owner_blocked` uklonjen (blokiranje → `hidden_by_system`). Pojašnjena `hidden_by_moderator` semantika. |
| 2.1 | 1.4.2026 | Migracija na jednostatus model: sekcija 4.1 — zamijenjena tabela "Status i vidljivost" (lifecycleStatus + moderationStatus + closedReason → listingStatus + removedReason). Sekcija 4.2 — ažurirana tabela brisanja (wasEverActive logika) i automatski procesi (expired tranzicija). Sekcija 4.3 — ažurirano brisanje Place-a (status reference). Sekcija 4.8 — kompletna zamjena: novi statusni model sa 13 stanja, isPublic formula, wasEverActive, Mermaid dijagram, tok po Trust Tier-u, blokiranje korisnika. Sekcija 4.10 — dodani withdraw endpointi za Event i Place. |
| 2.0 | 30.3.2026 | Sekcija 4.4: Liste kategorija mjesta i događaja preformatovane u tabele po sektoru za bolju preglednost. |
| 1.9 | 30.3.2026 | Sekcija 4.4: Uvedena trostruka organizacija Sektor → Kategorija → Tagovi. Dodate kompletne liste kategorija mjesta (16 sektora) i kategorija događaja (11 sektora). Dodan alias/sinonim mehanizam za pretragu. Atributi kategorije prošireni sa `sectorSlug`, `sectorName`, `sectorNameAlt`. API endpoints prošireni za aliase. Primjer kategorizacije ažuriran (BauMax → Penny Shop sa sektorima). Sekcija 4.1: `primaryCategoryData` snapshot proširen sa `sectorName`. |
| 1.8 | 30.3.2026 | Sekcija 4.9: Dodana implementacijska smjernica za visitor lajkove — jednosmjerni hash umjesto čuvanja sirovih podataka (GDPR compliance). |
| 1.7 | 29.3.2026 | Upravljanje kategorijama precizirano — ekskluzivno local\_admin (ispravka: prethodno navedeno 'operatora ili local\_admin'). Upravljanje tagovima precizirano — moderator sa `can_manage_tags` permisijom ili local\_admin. Spajanje tagova ažurirano. API endpoint opisi usklađeni sa permisijama. |
| 1.6 | 28.3.2026 | Status → Završeno. |
| 1.5 | Mart 2026 | Nova sekcija 4.9: Korisničke interakcije — Appreciation entitet, Favorite entitet, Share mehanizam. Tagovi parametrizirani (`MAX_TAGS_PER_LISTING`). Dodan `CHANGES_REQUESTED_TIMEOUT_DAYS` parametar u lifecycle sekciju (4.8). API endpoints prošireni za interakcije. Sekcije renumerisane (API → 4.10). |
| 1.4 | Mart 2026 | VerificationDocument → ListingDocument (SSoT). Ujedinjen entitet sa atributima iz poglavlja 07. |