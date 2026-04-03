# 03 - KORISNICI I PRISTUP

> **Verzija:** 2.1  
> **Datum:** 3.4.2026  
> **Status:** Završeno ✅

* * *
## O čemu je riječ?

CityInfo koristi arhitekturu sa **tri potpuno odvojena korisnička sistema** — umjesto tradicionalnog pristupa gdje sve uloge žive u jednoj tabeli. Ova separacija nije slučajna: različite grupe korisnika imaju fundamentalno različite potrebe, sigurnosne zahtjeve i načine rada. Kompromitovanje jednog sistema ne ugrožava druge, svaki grad (tenant) može rasti nezavisno, a GDPR compliance je značajno jednostavniji kada su podaci jasno razdvojeni.

| Sistem | Ko pristupa | Gdje | Tipičan broj |
| --- | --- | --- | --- |
| **User** | Građani, organizatori, vlasnici biznisa | [cityinfo.ba](http://cityinfo.ba) | Hiljade po gradu |
| **Staff** | Moderatori, operatori, lokalni admini | [admin.cityinfo.ba](http://admin.cityinfo.ba) | 5–20 po gradu |
| **GlobalAdmin** | Tehničko osoblje CityInfo kompanije | [master.cityinfo.ba](http://master.cityinfo.ba) | 2–5 ukupno |

**📌 Praktična napomena:** Novi developer treba razumjeti da ova tri sistema koriste odvojene baze, odvojene autentifikacijske mehanizme i odvojene API-je. Ne postoji način da se User token iskoristi za pristup admin panelu — to je by design.

* * *
## 3.1 Pregled korisničkih sistema
### Zašto tri odvojena sistema?

Separacija korisnika nije samo tehnička odluka već reflektuje stvarne operativne potrebe. Običan korisnik koji kreira događaje ima potpuno drugačije potrebe od moderatora koji pregledava sadržaj ili sistemskog administratora koji postavlja nove gradove. Držanjem ovih sistema odvojenim dobijamo:

- **Sigurnost** — kompromitovan User nalog ne može pristupiti admin funkcijama
- **Skalabilnost** — User baza može rasti eksponencijalno dok Staff ostaje mali
- **Compliance** — jasna separacija podataka olakšava GDPR zahtjeve
- **Fleksibilnost** — različite konfiguracije i sigurnosne politike po sistemu
### Arhitektura na visokom nivou

User i Staff podaci žive zajedno u istoj tenant bazi — svaki grad ima svoju vlastitu bazu koja sadrži i korisnike i osoblje tog grada. GlobalAdmin je jedini koji ima zasebnu, globalnu bazu (master) koja ne sadrži podatke ni jednog tenanta, već samo infrastrukturne informacije poput registra gradova.

Mermaid diagram syntax - use it for diagram generation

```
graph TD
    GA[⚙️ GlobalAdmin<br/>master.cityinfo.ba] --> GADB[(Master DB<br/>GlobalAdmin nalozi<br/>TenantRegistry)]

    U1[👤 User / Sarajevo] --> SJJ[(Sarajevo DB<br/>Users · Staff<br/>Events · Places)]
    S1[🛡️ Staff / Sarajevo] --> SJJ

    U2[👤 User / Zagreb] --> ZGB[(Zagreb DB<br/>Users · Staff<br/>Events · Places)]
    S2[🛡️ Staff / Zagreb] --> ZGB
```
### Pristupne tačke

| Sistem | URL | Namjena |
| --- | --- | --- |
| **User** | [cityinfo.ba](http://cityinfo.ba) | Javni web, pregled i kreiranje sadržaja |
| **Staff** | [admin.cityinfo.ba](http://admin.cityinfo.ba) | Moderacija, operacije, lokalna administracija |
| **GlobalAdmin** | [master.cityinfo.ba](http://master.cityinfo.ba) | Infrastruktura, tenanti, sistemske postavke |

**📌 Praktična napomena:** Svaki od ovih sistema ima vlastiti set API-ja. Staff ne može koristiti User API za autentifikaciju, niti obrnuto. Ovo je namjerno i predstavlja prvu liniju odbrane.

* * *
## 3.2 Neregistrovani korisnici (Visitors)
### O čemu se radi?

Visitor nije pohranjen u bazi podataka — to je konceptualna uloga koja opisuje neautentificirane posjetioce platforme. Važno je razumjeti ovu grupu jer može činiti značajan dio ukupnog prometa, posebno kod korisnika koji istražuju sadržaj prije nego se odluče registrovati.

Za razliku od registrovanih korisnika, visitors nemaju profil, ne mogu kreirati sadržaj i ne prolaze kroz trust sistem. Međutim, platforma im omogućava smislenu interakciju sa javnim sadržajem.
### Šta visitor može i ne može

| Može ✅ | Ne može ❌ |
| --- | --- |
| Pregledati javne listinge (eventi, mjesta) | Kreirati sadržaj |
| Koristiti pretragu i filtere | Sačuvati favorite na profilu |
| Pregledati mapu | Slati poruke vlasnicima listinga |
| Vidjeti detalje listinga | Kupovati kredite ili promocije |
| Podijeliti listing (share link) | Prijaviti neprikladan sadržaj |
| Lajkati listinge | Pristupiti historiji lajkova |
### Lajkovanje bez registracije

Visitors mogu lajkati listinge, ali na jednostavniji način nego registrovani korisnici:

- **Samo brojač:** Lajk se samo dodaje na ukupan broj lajkova listinga
- **Bez historije:** Ne čuva se informacija o tome ko je lajkao — visitor ne može vidjeti "svoje" lajkove
- **Zaštita od zloupotrebe:** Sistem kombinuje IP adresu i digitalni otisak preglednika (tip preglednika, jezik, ostali pasivno dostupni meta-podaci) kako bi prepoznao i ignorisao ponavljane interakcije sa iste "lokacije" — čak i kada se IP adresa mijenja

**📌 Praktična napomena:** API endpoints za javni sadržaj moraju raditi bez autentifikacije. Visitor lajkovi doprinose popularnosti listinga, ali bez pohrane ličnih podataka — u skladu sa GDPR zahtjevima.

* * *
## 3.3 User entitet
### Šta je User?

User predstavlja fizičko ili pravno lice koje koristi CityInfo platformu — bilo da pregledava događaje, kreira vlastite listinge ili kupuje promocije. Svaki User pripada tačno jednom tenantu (gradu) i ima definisan Trust Tier koji određuje kako se njegov sadržaj moderira.

Dva su ključna koncepta za razumijevanje User entiteta:

- **Trust Tier** — određuje da li sadržaj ide na pre-moderaciju ili se objavljuje odmah
- **Access status** — kontroliše može li se korisnik uopšte prijaviti na platformu
### Atributi

Lista atributa nije konačna i može se proširivati prema potrebama.

| Naziv | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| userId | String | Jedinstveni identifikator | Da  | Automatski generisan |
| fullName | String | Puno ime i prezime | Da  |     |
| email | String | Email za prijavu i komunikaciju | Da  | Jedinstven unutar sistema |
| emailVerified | Boolean | Da li je email potvrđen | Da  | Default: false |
| phoneNumber | String | Kontakt telefon | Ne  |     |
| phoneVerified | Boolean | Da li je telefon verificiran | Da  | Default: false |
| username | String | Jedinstveno korisničko ime | Da  |     |
| accountStatus | Enum | Status računa | Da  | active, inactive, deleted |
| accessStatus | Enum | Status pristupa | Da  | allowed, blocked |
| trustTier | Number | Nivo povjerenja (0–4) | Da  | Default: 1 (Standard) |
| isVerifiedPublisher | Boolean | Da li je verifikovani izdavač | Da  | Default: false. Samo za Tier 3+. |
| walletBalance | Money | Trenutni balans kredita | Da  | Default: 0.00 |
| locale | String | Preferirani jezik | Da  | Default: tenant postavka |
| timezone | String | Vremenska zona | Da  | Default: tenant postavka |
| twoFactorEnabled | Boolean | Da li je 2FA aktivan | Da  | Default: false |
| gdprConsent | Boolean | GDPR saglasnost | Da  |     |
| gdprConsentAt | DateTime | Kada je data saglasnost | Ne  |     |
| lastLoginAt | DateTime | Zadnja prijava | Ne  |     |
| createdAt | DateTime | Registracija | Da  |     |
| blockedAt | DateTime | Kada je blokiran | Ne  | Popunjeno ako je blocked |
| blockedReason | Enum | Razlog blokiranja | Ne  | Obavezno ako je blocked |
| blockedDetails | Object/JSON | Dodatni detalji uz razlog blokiranja | Ne  | Obavezno kada je blockedReason = OTHER |
| blockedUntil | DateTime | Do kada traje blokada | Ne  | NULL = trajna |
### isVerifiedPublisher flag

Korisnici na Tier 3 (Established) mogu dobiti `isVerifiedPublisher = true` flag koji znači da su potvrđeni izdavači. Kada je ovaj flag aktivan, svi listinzi tog korisnika automatski dobijaju `verificationStatus = verified` — bez potrebe za uploadom dokumenata po svakom listingu.

Ovo rješava problem samplinga: na Tier 3 moderacija funkcioniše sa samplingom, pa verifikacija na nivou pojedinačnog listinga ne bi bila konzistentna. Flag prebacuje verifikaciju na nivo korisnika umjesto listinga.

Flag postavlja moderator sa `can_manage_trust_tier` permisijom. Dokument nije obavezan — moderator koristi vlastitu procjenu (npr. vlasnik restorana sa verifikovanim Place-om koji organizuje evente ne treba ponovo dokazivati legitimitet). Flag se automatski uklanja ako korisnik bude degradiran ispod Tier 3.

Više o verifikaciji po tier-u u [05 - Moderacija, sekcija 5.6.3](../project-specs/05-moderacija.md).
### Statusi
#### accountStatus — životni ciklus računa

| Status | Šta znači | Kada se koristi |
| --- | --- | --- |
| **active** | Račun je aktivan i funkcionalan | Normalno stanje |
| **inactive** | Korisnik je privremeno deaktivirao račun | Korisnik sam "pauzira" nalog |
| **deleted** | Soft delete, čuva se 30 dana pa se trajno briše | Korisnik želi brisanje (GDPR) |
#### accessStatus — kontrola pristupa

| Status | Šta znači | Ko postavlja |
| --- | --- | --- |
| **allowed** | Normalan pristup platformi | Sistem (default) |
| **blocked** | Blokiran pristup zbog kršenja pravila | Moderator ili sistem |

Blokiran korisnik **ne može se prijaviti** bez obzira na accountStatus. Pri blokiranju je obavezno unijeti razlog (blockedReason).
### Ortogonalnost statusa

Jedan od ključnih koncepata za razumijevanje User entiteta je da statusi kontrolišu **potpuno različite aspekte** i mogu se kombinovati nezavisno:

| Status | Šta kontroliše | Pitanje na koje odgovara |
| --- | --- | --- |
| **accountStatus** | Životni ciklus računa | "Da li račun postoji?" |
| **accessStatus** | Pristup platformi | "Može li se prijaviti?" |
| **trustTier** | Moderacijski workflow | "Kako se tretira njegov sadržaj?" |

Ovo znači da su moguće razne kombinacije koje na prvi pogled djeluju neobično, ali imaju smisla:

| accountStatus | accessStatus | trustTier | Situacija |
| --- | --- | --- | --- |
| active | allowed | 2 (Trusted) | Normalan korisnik sa dobrom historijom |
| active | blocked | 2 (Trusted) | Blokiran zbog npr. vrijeđanja u porukama, ali ima dobru historiju sadržaja |
| active | allowed | 0 (Restricted) | Može se prijaviti, ali sadržaj uvijek ide na pre-moderaciju |
| inactive | allowed | 2 (Trusted) | Sam pauzirao račun; kad se vrati, zadržava trusted status |

**📌 Praktična napomena:** Pri provjeri pristupa, uvijek treba provjeriti **oba** statusa — accountStatus I accessStatus. Korisnik sa `accountStatus=active` i `accessStatus=blocked` ne smije moći pristupiti platformi.

* * *
## 3.4 Trust Tier sistem
### O čemu se radi?

Trust Tier je mehanizam koji automatski prilagođava nivo moderacije prema ponašanju korisnika. Umjesto binarnog pristupa "vjerujemo / ne vjerujemo", sistem prepoznaje da korisnici grade povjerenje kroz konzistentno kvalitetan sadržaj.

Novi korisnici počinju na **Tier 1 (Standard)** — njihov sadržaj ide na pre-moderaciju. Nakon što pokažu da prave kvalitetan sadržaj, automatski napreduju na **Tier 2 (Trusted)** i njihove objave se odmah prikazuju. Ako prekrše pravila, mogu biti degradirani ili čak zaključani na **Tier 0 (Restricted)**.
### Pet nivoa povjerenja

| Tier | Naziv | Moderacija | Sampling | Kako se dostiže |
| --- | --- | --- | --- | --- |
| **0** | Restricted | Pre-moderacija | 100% | Ručno ili automatski (kršenje pravila) |
| **1** | Standard | Pre-moderacija | 100% | Default za nove korisnike |
| **2** | Trusted | Post-moderacija | 100% | Automatski (konfigurisani pragovi) |
| **3** | Established | Post-moderacija | Konfigurisano | Automatski (konfigurisani pragovi) |
| **4** | Verified Partner | Post-moderacija | Konfigurisano (`TIER4_SAMPLING_PERCENT`, preporučeno 20%) | Ručno — moderator sa `can_manage_trust_tier` permisijom |

**Objašnjenje nivoa:**

- **Restricted (0):** Korisnici koji su ozbiljno ili višestruko prekršili pravila. Zaključani na pre-moderaciju bez mogućnosti automatskog napredovanja. Izlaz je moguć samo kroz ručnu intervenciju moderatora sa `can_manage_trust_tier` permisijom.
- **Standard (1):** Svi novi korisnici počinju ovdje. Svaki sadržaj čeka odobrenje moderatora prije nego postane vidljiv. Cilj je što prije napredovati u Trusted.
- **Trusted (2):** Korisnici koji su dokazali da prave kvalitetan sadržaj. Njihov sadržaj ide live odmah, a moderator ga pregleda naknadno. Sav sadržaj se i dalje pregleda (100%).
- **Established (3):** Korisnici sa dugom istorijom kvalitetnog sadržaja. Post-moderacija sa samplingom — moderator pregleda samo dio njihovog sadržaja. Ostatak prolazi automatski.
- **Verified Partner (4):** Ugovorni partneri platforme (kino kompleksi, kulturni centri, gradske institucije). Najniži sampling. Postavlja se ručno od strane moderatora sa `can_manage_trust_tier` permisijom, nakon uspostavljanja poslovnog odnosa. Ovo je osjetljiva akcija jer direktno mijenja moderacijski workflow za korisnika.
### Kako Trust Tier utiče na workflow

| Trust Tier | Pri objavi sadržaja | Efekat |
| --- | --- | --- |
| **0, 1** | Pre-moderacija | Sadržaj čeka odobrenje prije postajanja vidljiv |
| **2, 3, 4** | Post-moderacija | Sadržaj odmah postaje vidljiv, pregled naknadno |

**Ograničenje za pre-moderaciju:** Korisnici na Tier 0 i 1 mogu imati maksimalno `TIER_PRE_MOD_MAX_PENDING` objava koje čekaju pregled istovremeno. Moraju sačekati odluku prije slanja novog sadržaja.
### Napredovanje kroz tier-ove

Napredovanje je automatsko za nivoe 1→2 i 2→3. Sistem provjerava uslove nakon svake moderatorske odluke. Sva tri uslova moraju biti ispunjena **istovremeno** da bi napredovanje bilo okidano — procenat sam za sebe nije dovoljan jer bi korisnik sa jednom odobrenom objavom matematički imao 100% uspješnost.

| Prijelaz | Parametar | Preporučena početna vrijednost | Opis |
| --- | --- | --- | --- |
| **Tier 1 → 2** | `TIER1_MIN_APPROVED` | 5   | Minimalan broj odobrenih objava |
|     | `TIER1_MIN_SUCCESS_RATE` | 80% | Minimalni procenat odobrenih (approved / ukupno submitted) |
|     | `TIER1_MIN_ACCOUNT_AGE_DAYS` | 7   | Minimalna starost računa u danima |
| **Tier 2 → 3** | `TIER2_MIN_APPROVED` | 20  | Minimalan broj odobrenih objava |
|     | `TIER2_MIN_SUCCESS_RATE` | 85% | Minimalni procenat odobrenih |
|     | `TIER2_MIN_ACCOUNT_AGE_DAYS` | 30  | Minimalna starost računa u danima |

Preporučene vrijednosti su polazna tačka — treba ih tune-ovati na osnovu stvarnih podataka nakon launcha. Sve vrijednosti su konfiguracijski parametri koji se mogu mijenjati bez izmjene koda.

**Zašto starost računa?** Sprječava gaming — kreiranje novog naloga, brzo objavljivanje minimalnog broja listinga i automatsko napredovanje. Korisnik mora biti prisutan na platformi određeni period da bi stekao viši nivo povjerenja.
### Efekt odbijenih objava na napredovanje

Odbijen listing ne mijenja Trust Tier direktno za Tier 1 korisnika (nema kuda pasti osim na Restricted, što je rezervisano za ozbiljna kršenja). Međutim, **spušta procenat uspješnosti i time blokira ili odgađa napredovanje prema Tier 2**.

Primjer: korisnik sa 4 approved i 1 rejected ima uspješnost 80% (4/5). Uz `TIER1_MIN_SUCCESS_RATE = 80%`, tačno je na granici — mora skupiti još jednu odobrenu objavu da procenat ostane iznad praga. Nema resetovanja brojača niti posebnih kazni — matematika sama reguliše napredovanje.
### Efekt `changes_requested` na napredovanje

`changes_requested` je kvalitativno drugačiji signal od `rejected` — moderator ne odbija sadržaj, nego poziva korisnika na saradnju i ispravku. Penalizovati korisnika koji aktivno popravlja sadržaj bilo bi kontraproduktivno, pa `changes_requested` sam po sebi **ne utiče na Trust Tier ni na procenat uspješnosti**.

Ono što se broji je isključivo **finalna odluka** po listingu — bez obzira koliko puta je sadržaj prolazio kroz `changes_requested` u međuvremenu. Jedan listing uvijek rezultira jednim ishodom za statistiku.

| Scenarij | Šta se broji |
| --- | --- |
| `changes_requested` → korisnik popravlja → `approved` | 1 approved |
| `changes_requested` → korisnik popravlja → `removed (removedReason: rejected)` | 1 rejected |
| Više iteracija `changes_requested` → na kraju `approved` | 1 approved — broj iteracija nije relevantan |
| `changes_requested` → korisnik ne reaguje, listing ostaje u draftu | Ništa — nema finalne odluke, ne broji se |

**📌 Praktična napomena:** Ovakav pristup potiče zdravu interakciju između korisnika i moderatora. Korisnik koji dobije povratnu informaciju i ispravi sadržaj ne smije biti u goroj poziciji od onoga koji je odmah pogodio — važno je samo da sadržaj na kraju bude kvalitetan.
### Degradacija

Korisnik može pasti za tier ako moderacija otkrije problematičan sadržaj. Degradacija može biti **automatska** (sistem detektuje jasno definisan prag) ili **ručna** (moderator procjenjuje situaciju).

**Automatska degradacija:**

Sistem automatski degradira korisnika kada su ispunjeni nedvosmisleni, mjerljivi uslovi. Svaka automatska degradacija kreira posebnu stavku u moderacijskom queue-u tipa "Trust Tier Auto-Degradation Review" — moderator mora pregledati i potvrditi ili revertovati odluku. Ovo je sigurnosna mreža koja sprečava da automatika pogrešno kazni korisnika.

| Situacija | Akcija | Queue stavka |
| --- | --- | --- |
| `TIER_REJECTED_THRESHOLD` rejected u `TIER_REJECTED_WINDOW_DAYS` dana | Automatski pad na Restricted (Tier 0) | Da — moderator pregleda i potvrđuje/revertuje |

Preporučene početne vrijednosti: `TIER_REJECTED_THRESHOLD = 3`, `TIER_REJECTED_WINDOW_DAYS = 30`.

> 💡 **Praktična napomena:** Automatska degradacija postoji da bi se sistem mogao zaštititi i izvan radnog vremena, ali uvijek podliježe ljudskom pregledu. Moderator koji pregleda auto-degradaciju može je revertovati ako procijeni da je bila nepravedna — npr. ako su rejected odluke bile sporne ili je korisnik već popravio probleme.

**Ručna degradacija:**

Situacije koje zahtijevaju ljudsku procjenu. Ručna degradacija na Tier 0 (Restricted) zahtijeva `can_manage_trust_tier` permisiju.

| Situacija | Akcija | Potrebna permisija |
| --- | --- | --- |
| 1 rejected (bilo koji tier) | Upozorenje, tier se ne mijenja — ali procenat pada i može blokirati napredovanje | Standardna |
| Problem u samplingu (Tier 3) | Moderator odlučuje o padu sa Established na Trusted (Tier 2) | Standardna |
| Ozbiljno kršenje (hate speech, spam, ilegalni sadržaj) | Moderator postavlja direktno na Restricted (Tier 0), bez međufaza | `can_manage_trust_tier` |
### Dijagram prelaza

Mermaid diagram syntax - use it for diagram generation

```
stateDiagram-v2
    [*] --> Standard: Registracija
    Standard --> Trusted: Automatski (konfigurisani pragovi)
    Trusted --> Established: Automatski (konfigurisani pragovi)
    Established --> VerifiedPartner: Ručno (can_manage_trust_tier)
    
    Standard --> Restricted: Ozbiljno kršenje (can_manage_trust_tier)
    Trusted --> Standard: Rejected sadržaj (prag)
    Trusted --> Restricted: Ozbiljno kršenje (can_manage_trust_tier)
    Established --> Trusted: Problem u samplingu
    Established --> Restricted: Ozbiljno kršenje (can_manage_trust_tier)
    
    Restricted --> Standard: Ručno (can_manage_trust_tier)
```

**📌 Praktična napomena:** Trust Tier je odvojen od access statusa. Korisnik može biti na Tier 2 (Trusted) ali blocked (npr. ima dobar sadržaj ali je vrijeđao u porukama), ili na Tier 0 (Restricted) ali allowed (može se prijaviti, ali svaki sadržaj ide na pregled). Detalji o moderacijskom workflow-u degradacije u [05 - Moderacija, sekcija 5.1.3](../project-specs/05-moderacija.md).

* * *
## 3.5 Staff entitet
### Šta je Staff?

Staff predstavlja zaposlenika koji radi na održavanju i upravljanju CityInfo platformom. To mogu biti moderatori koji pregledaju sadržaj, operatori koji upravljaju poslovnim aspektima ili lokalni administratori koji konfigurišu postavke za svoj grad.

Ključna razlika od User entiteta: Staff pristupa kroz **odvojeni admin panel** sa strožim sigurnosnim mjerama, uključujući obaveznu dvofaktorsku autentifikaciju i kraće sesije.
### Zašto isActive (Boolean) umjesto accountStatus (Enum)?

Za razliku od User entiteta koji koristi `accountStatus` enum sa tri stanja, Staff koristi jednostavan `isActive` boolean. Ovo nije slučajnost:

| Aspekt | User (accountStatus enum) | Staff (isActive boolean) |
| --- | --- | --- |
| Ko kontroliše | Korisnik sam + sistem | Samo admin |
| GDPR brisanje | Kritično (soft delete → hard delete) | Manje relevantno (zaposlenici) |
| Self-service | Da (inactive = sam pauzirao) | Ne  |
| Potreba za detaljima | Zašto neaktivan? | Aktivan ili nije — dovoljno |

Ako je potrebno pratiti **zašto** je Staff deaktiviran, koriste se polja `terminatedAt` i notes, a ne dodatna enum stanja. Ovo održava model jednostavnim za tipične operacije (aktivacija/deaktivacija) dok i dalje omogućava audit trail.
### Atributi

Lista atributa nije konačna i može se proširivati.

| Naziv | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| staffId | String | Jedinstveni identifikator | Da  |     |
| email | String | Email za prijavu | Da  |     |
| fullName | String | Ime i prezime | Da  |     |
| role | Enum | Uloga u sistemu | Da  | moderator, operator, local\_admin |
| permissions | List | Lista dodatnih permisija | Da  | Default: \[\] (prazna lista) |
| isActive | Boolean | Da li nalog može pristupiti | Da  | Default: true |
| tenantAccess | List | Lista tenanta kojima ima pristup | Da  |     |
| mfaEnabled | Boolean | Da li je 2FA aktivan | Da  | Obavezno za sve |
| phoneNumber | String | Kontakt telefon | Da  |     |
| department | String | Odjel/tim | Ne  | npr. "Moderation", "Operations" |
| supervisorId | String | Nadređeni (Staff) | Ne  |     |
| lastLoginAt | DateTime | Zadnja prijava | Ne  |     |
| lastLoginIp | String | IP adresa zadnje prijave | Ne  |     |
| failedLoginAttempts | Number | Broj neuspjelih pokušaja | Da  | Default: 0 |
| lockedUntil | DateTime | Zaključan do | Ne  | Nakon 5 neuspjelih pokušaja |
| passwordChangedAt | DateTime | Zadnja promjena lozinke | Da  | Rotacija svakih 90 dana |
| hiredAt | DateTime | Datum zaposlenja | Da  |     |
| createdAt | DateTime | Kreiranje naloga | Da  |     |
| createdBy | String | Ko je kreirao nalog | Da  |     |
### Moderatorske permisije

Svi moderatori dijele iste bazne ovlasti za svakodnevni rad (approve, reject, request changes, blokiranje korisnika). Za osjetljive akcije koje imaju veći uticaj na korisnike ili strukturu sadržaja, postoje granularne permisije koje se čuvaju u `permissions` polju.

| Permisija | Šta omogućava | Ko dodjeljuje |
| --- | --- | --- |
| `can_manage_trust_tier` | Postavljanje Tier 4 (Verified Partner), ručna degradacija na Tier 0 (Restricted), postavljanje `isVerifiedPublisher` flaga na korisniku | Staff sa ulogom Operator |
| `can_manage_tags` | Kreiranje, editovanje, deaktivacija, brisanje i spajanje tagova (EventTags i PlaceTags) | Staff sa ulogom Operator |

Ovo nije hijerarhija — moderator sa dodatnim permisijama nema "viši rang" od ostalih. To je jednostavno pristup akcijama koje zahtijevaju dodatno povjerenje. Lista permisija se može proširivati prema potrebama sistema.

> ⚠️ **Napomena o local\_admin:** Staff sa ulogom `local_admin` ima šire sistemske ovlasti i može izvršavati sve akcije koje pokrivaju `can_manage_trust_tier` i `can_manage_tags` bez potrebe za eksplicitnim permisijama u `permissions` polju. Permisije su relevantne samo za Staff sa ulogom `moderator`.

Detalji o moderatorskim akcijama i permisijama opisani su u [05 - Moderacija, sekcija 5.4](../project-specs/05-moderacija.md).
### Uloge i ovlasti
#### Pregled uloga

| Uloga | Šta radi | Tipični zadaci |
| --- | --- | --- |
| **moderator** | Pregleda i odobrava sadržaj | Moderacija listinga, komunikacija s korisnicima, upravljanje Trust Tier-om, upravljanje tagovima (sa permisijom) |
| **operator** | Upravlja poslovnim aspektima | Cijene, promocije, izvještaji, komunikacija sa oglašivačima, dodjela moderatorskih permisija |
| **local\_admin** | Administrira jedan ili više tenanta | Kategorije, tagovi, postavke, kreiranje moderatora |
#### Matrica ovlasti

| Funkcionalnost | moderator | operator | local\_admin |
| --- | --- | --- | --- |
| Pregled moderation queue | ✅   | ❌   | ✅   |
| Odobravanje/odbacivanje sadržaja | ✅   | ❌   | ✅   |
| Komunikacija sa korisnicima | ✅   | ❌   | ✅   |
| Komunikacija sa oglašivačima | ❌   | ✅   | ✅   |
| Mijenjanje Trust Tier-a (bazno) | ✅   | ❌   | ✅   |
| Postavljanje Tier 4 / degradacija na Tier 0 | ✅\* | ❌   | ✅\*\* |
| Blokiranje korisnika | ✅   | ❌   | ✅   |
| Upravljanje tagovima | ✅\*\*\*\* | ❌   | ✅\*\* |
| Dodjela moderatorskih permisija | ❌   | ✅   | ✅   |
| Pregled finansijskih izvještaja | ❌   | ✅   | ✅   |
| Upravljanje cijenama | ❌   | ✅   | ✅   |
| Kreiranje promo kodova | ❌   | ✅   | ✅   |
| Upravljanje kategorijama | ❌   | ❌   | ✅   |
| Tenant postavke | ❌   | ❌   | ✅   |
| Kreiranje staff naloga | ❌   | ❌   | ✅\*\*\* |

\*Zahtijeva `can_manage_trust_tier` permisiju  
\*\*Inherentna ovlast — ne zahtijeva eksplicitnu permisiju  
\*\*\*local\_admin može kreirati samo moderator naloge za svoj tenant  
\*\*\*\*Zahtijeva `can_manage_tags` permisiju

**📌 Praktična napomena:** Staff može pristupiti **samo tenantima navedenim u tenantAccess**. Čak i local\_admin za Sarajevo ne može vidjeti podatke iz Banja Luke — osim ako mu nije eksplicitno dodijeljen pristup.

* * *
## 3.6 GlobalAdmin entitet
### Šta je GlobalAdmin?

GlobalAdmin je sistemski administrator sa maksimalnim ovlastima koji upravlja CityInfo infrastrukturom. Ova uloga je rezervisana isključivo za tehničko osoblje CityInfo kompanije — tipično samo 2-5 osoba.

Ključno ograničenje: GlobalAdmin **nikada ne pristupa direktno tenant podacima**. Može kreirati nove gradove, postaviti prvog local\_admin-a i konfigurirati infrastrukturu, ali ne može npr. odobriti listing ili blokirati korisnika. To je namjerno — separation of concerns.
### Atributi

Lista atributa nije konačna.

| Naziv | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| globalAdminId | String | Jedinstveni identifikator | Da  |     |
| email | String | Email za prijavu | Da  | Mora biti @cityinfo.ba domena |
| fullName | String | Ime i prezime | Da  |     |
| phoneNumber | String | Kontakt za hitne slučajeve | Da  |     |
| isActive | Boolean | Da li nalog može pristupiti | Da  |     |
| mfaRequired | Boolean | Obavezna MFA | Da  | Uvijek true |
| mfaBackupCodes | Object | Backup kodovi za recovery | Ne  | Obavezni uz MFA |
| sshPublicKey | String | SSH ključ za CLI pristup | Ne  |     |
| apiKey | String | API ključ za automatizaciju | Ne  |     |
| lastLoginAt | DateTime | Zadnja prijava | Ne  |     |
| lastLoginIp | String | IP adresa | Ne  |     |
| failedLoginAttempts | Number | Neuspjeli pokušaji | Da  |     |
| lockedUntil | DateTime | Zaključan do | Ne  |     |
| passwordChangedAt | DateTime | Zadnja promjena lozinke | Da  | Rotacija svakih 60 dana |
| createdAt | DateTime | Kreiranje naloga | Da  |     |
| createdBy | String | Ko je kreirao | Ne  | NULL za prvog admina |
### Ekskluzivne ovlasti

| Ovlast | Šta znači | Nivo rizika |
| --- | --- | --- |
| Kreiranje tenanta | Dodavanje novih gradova/regiona | Visok |
| Konfiguracija infrastrukture | Server, database, network postavke | Kritičan |
| Upravljanje prvim Staff nalozima | Kreiranje local\_admin za nove tenante | Srednji |
| Master API pristup | Programski pristup master bazi | Kritičan |
| Backup i restore | Sistem-wide backup operacije | Kritičan |
| Security monitoring | Pristup svim audit logovima | Visok |
### Ograničenja

GlobalAdmin **ne može**:

- Pristupati tenant podacima direktno (korisnici, listinzi, poruke)
- Moderirati sadržaj
- Komunicirati direktno sa User-ima
- Izvršiti kritične akcije bez odobrenja drugog GlobalAdmin-a (dual approval)

**📌 Praktična napomena:** Ako GlobalAdmin treba pogledati specifičan problem sa listingom u Sarajevu, mora zatražiti od local\_admin-a da mu dostavi relevantne informacije. Ovo štiti od "single point of failure" scenarija.

* * *
## 3.7 Sigurnost i pristup
### Autentifikacija po sistemima

Svaki od tri sistema ima vlastite sigurnosne zahtjeve prilagođene riziku i načinu korištenja.

| Aspekt | User | Staff | GlobalAdmin |
| --- | --- | --- | --- |
| **2FA** | Opcionalno | Obavezno | Obavezno + backup kodovi |
| **Rotacija lozinke** | Preporučeno | Svakih 90 dana | Svakih 60 dana |
| **Session timeout** | 30 dana | 8 sati neaktivnosti | 4 sata neaktivnosti |
| **Lockout** | 10 pokušaja → 15 min | 5 pokušaja → 30 min | 3 pokušaja → 1 sat |
| **IP restrikcije** | Ne  | Opciono | Preporučeno (whitelist) |
### Blokiranje korisnika

Kada se User blokira (accessStatus = blocked), sistem zahtijeva unos razloga i opcionalnih detalja. Razlog se bira iz predefinisanog skupa vrijednosti:

| blockedReason | Kada se koristi |
| --- | --- |
| **SPAM\_CONTENT** | Masovno objavljivanje nepoželjnog sadržaja |
| **MALICIOUS\_CONTENT** | Štetni ili ilegalni sadržaj |
| **HARASSMENT** | Uznemiravanje drugih korisnika |
| **FRAUD** | Pokušaj prevare |
| **TOS\_VIOLATION** | Kršenje uslova korištenja (generalno) |
| **OTHER** | Ostalo — obavezno popuniti `blockedDetails` |

Uz razlog se opciono unose i `blockedDetails` (slobodan tekst ili strukturirani podaci za interno praćenje) te `blockedUntil` (do kada traje blokada — ako je NULL, blokada je trajna).
### Efekt blokiranja na sadržaj korisnika

Ponašanje pri blokiranju razlikuje se za **ručno blokiranje** (moderator) i **instant blokiranje** (sistem).

**Ručno blokiranje (moderator):**

Pri ručnom blokiranju, moderator bira šta se dešava sa listinzima korisnika:

- **Opcija 1 — Listinzi ostaju vidljivi (default):** Aktivni listinzi ostaju javno vidljivi, ali korisnik ne može kreirati nove niti editovati postojeće dok je blokiran. Aktivne promocije se otkazuju bez povrata kredita.
- **Opcija 2 — Listinzi se sakrivaju:** Svi javno vidljivi listinzi prelaze u `hidden_by_system`. Pri odblokiranju korisnika, ovi listinzi se automatski vraćaju u `published`. Aktivne promocije se otkazuju bez povrata kredita.

Moderator bira opciju na osnovu procjene — ako je blokada zbog neprimjerenih poruka ali je sadržaj kvalitetan, listinzi tipično ostaju vidljivi. Ako je blokada zbog lažnog sadržaja ili prevare, moderator sakriva sve.

**Instant blokiranje (sistem):**

Sistem automatski blokira korisnika u slučajevima koji zahtijevaju hitnu reakciju (hate speech, nasilje, spam, malicious sadržaj). Kod instant blokiranja, **default ponašanje je sakrivanje sadržaja** — svi javno vidljivi listinzi automatski prelaze u `hidden_by_system`. Instant block kreira stavku "Instant Block Review" u moderacijskom queue-u, gdje moderator može potvrditi blokadu ili revertovati ako je bila false positive.

> **📌 Praktična napomena:** Pri ručnom blokiranju, sakriveni listinzi (`hidden_by_system`) se automatski reaktiviraju pri odblokiranju. Ako moderator želi **trajno** ukloniti sadržaj (npr. u slučaju prevare ili ilegalnog sadržaja), to je zasebna akcija — moderator može listinge prebaciti u `removed` sa odgovarajućim `removedReason` prije ili nakon blokiranja. Detalji o `listingStatus` vrijednostima i `removedReason` opisani su u [04 - Sadržaj, sekcija 4.8](../project-specs/04-sadrzaj.md). Detalji o razlici između ručnog i instant blokiranja u [05 - Moderacija, sekcija 5.4.4](../project-specs/05-moderacija.md).
### Session politike

| Sistem | Trajanje | Concurrent sessions | Logout opcije |
| --- | --- | --- | --- |
| **User** | 30 dana refresh | Neograničeno | Pojedinačni ili svi uređaji |
| **Staff** | 8h idle timeout | 1 aktivan session | Automatski pri novoj prijavi |
| **GlobalAdmin** | 4h idle timeout | 1 aktivan session | Obavezan logout pri kraju rada |
### Audit logging

Sve akcije se loguju, ali sa različitim nivoom detalja i retencijom:

| Sistem | Šta se loguje | Koliko se čuva |
| --- | --- | --- |
| **User** | Login, kreiranje sadržaja, transakcije | 90 dana |
| **Staff** | Sve akcije, pristup podacima, IP/user agent | 1 godina |
| **GlobalAdmin** | Apsolutno sve, immutable log | 7 godina |

**📌 Praktična napomena:** Staff audit log uključuje "before/after" vrijednosti za sve izmjene. Ako moderator promijeni Trust Tier korisnika, log pokazuje prethodnu i novu vrijednost, vrijeme, IP adresu i razlog (ako je unesen).

* * *
## 3.8 API Endpoints

Ova sekcija daje pregled ključnih endpoint-a za upravljanje korisnicima. Prikazane su samo putanje i osnovni opisi — detaljna dokumentacija sa request/response shemama nalazi se u API specifikaciji.
### User sistem
#### Autentifikacija

| Metoda | Putanja | Opis |
| --- | --- | --- |
| POST | `/auth/register` | Registracija novog korisnika |
| POST | `/auth/login` | Prijava (email + password) |
| POST | `/auth/logout` | Odjava (invalidira session) |
| POST | `/auth/refresh` | Osvježavanje tokena |
| POST | `/auth/verify-email` | Potvrda email adrese |
| POST | `/auth/verify-phone` | Potvrda telefona (SMS kod) |
| POST | `/auth/forgot-password` | Zahtjev za reset lozinke |
| POST | `/auth/reset-password` | Postavljanje nove lozinke |
| POST | `/auth/2fa/setup` | Postavljanje 2FA |
| POST | `/auth/2fa/verify` | Verifikacija 2FA koda |
#### Profil

| Metoda | Putanja | Opis |
| --- | --- | --- |
| GET | `/users/me` | Dohvat profila trenutnog korisnika |
| PATCH | `/users/me` | Ažuriranje profila |
| DELETE | `/users/me` | Brisanje računa (soft delete) |
| GET | `/users/me/listings` | Listinzi trenutnog korisnika |
| GET | `/users/me/transactions` | Historija transakcija |
#### Wallet

| Metoda | Putanja | Opis |
| --- | --- | --- |
| GET | `/wallet/balance` | Trenutni balans kredita |
| POST | `/wallet/purchase` | Kupovina kredita |
| GET | `/wallet/transactions` | Historija wallet transakcija |
### Staff sistem
#### Autentifikacija

| Metoda | Putanja | Opis |
| --- | --- | --- |
| POST | `/staff/auth/login` | Prijava (email + password + 2FA) |
| POST | `/staff/auth/logout` | Odjava |
| POST | `/staff/auth/change-password` | Promjena lozinke |
#### Upravljanje korisnicima

| Metoda | Putanja | Opis |
| --- | --- | --- |
| GET | `/staff/users` | Lista korisnika (filtriranje, paginacija) |
| GET | `/staff/users/{userId}` | Detalji korisnika |
| PATCH | `/staff/users/{userId}/trust-tier` | Promjena Trust Tier-a (za Tier 0 i 4 zahtijeva `can_manage_trust_tier`) |
| PATCH | `/staff/users/{userId}/access-status` | Blokiranje/odblokiranje (uključuje opciju za sadržaj) |
| PATCH | `/staff/users/{userId}/verified-publisher` | Postavi/ukloni `isVerifiedPublisher` flag (zahtijeva `can_manage_trust_tier`) |
| GET | `/staff/users/{userId}/audit-log` | Audit log korisnika |
#### Moderacija

| Metoda | Putanja | Opis |
| --- | --- | --- |
| GET | `/staff/moderation/queue` | Red za moderaciju |
| POST | `/staff/moderation/{listingId}/approve` | Odobrenje listinga |
| POST | `/staff/moderation/{listingId}/reject` | Odbijanje listinga |
| POST | `/staff/moderation/{listingId}/request-changes` | Vraćanje na doradu sa povratnom informacijom |
### GlobalAdmin sistem

| Metoda | Putanja | Opis |
| --- | --- | --- |
| POST | `/master/auth/login` | Prijava (sa MFA) |
| GET | `/master/tenants` | Lista svih tenanta |
| POST | `/master/tenants` | Kreiranje novog tenanta |
| GET | `/master/tenants/{tenantId}` | Detalji tenanta |
| PATCH | `/master/tenants/{tenantId}` | Ažuriranje tenanta |
| POST | `/master/tenants/{tenantId}/staff` | Kreiranje local\_admin za tenant |
| GET | `/master/audit-log` | Globalni audit log |
| GET | `/master/system/health` | Status sistema |

**📌 Praktična napomena:** Ovi endpoint-i su grupisani po logičkim cjelinama, ali u implementaciji mogu biti organizovani drugačije. Verzioniranje API-ja (npr. `/v1/auth/login`) nije prikazano radi jednostavnosti.

* * *
## Sažetak

Tri korisnička sistema CityInfo platforme — User, Staff i GlobalAdmin — dizajnirana su sa jasnom separacijom odgovornosti:

| Sistem | Fokus | Ključna karakteristika |
| --- | --- | --- |
| **User** | Kreiranje i pregled sadržaja | Trust Tier za automatsku moderaciju |
| **Staff** | Održavanje platforme | Role-based pristup + granularne permisije, tenant ograničenja |
| **GlobalAdmin** | Infrastruktura | Maksimalna sigurnost, bez pristupa podacima |

Ova arhitektura omogućava platformi da skalira — od jednog grada sa stotinu korisnika do desetina gradova sa stotinama hiljada korisnika — uz održavanje sigurnosti i operativne efikasnosti.

* * *
## Changelog

| Verzija | Datum | Opis |
| --- | --- | --- |
| 2.1 | 3.4.2026 | **Optimizacija 13→12 statusa.** `rejected` uklonjen kao zaseban `listingStatus`, dodan kao `removedReason`. Blokiranje pojašnjeno — koristi `hidden_by_system`. |
| 2.0 | 1.4.2026 | **MIGRACIJA — jednostatus model.** Sekcija 3.7 "Efekt blokiranja na sadržaj korisnika" ažurirana: `closed` sa `closedReason = OWNER_BLOCKED` → `removed` sa `removedReason = owner_blocked`. Uklonjena referenca na `MOD_HIDE`. Automatska reaktivacija pri odblokiranju zamijenjena objašnjenjem da je `removed` terminalan status. Reference na Ch.04 ažurirane (`listingStatus` umjesto `closedReason`). |
| 1.9 | 29.3.2026 | Dodana permisija `can_manage_tags` za moderatore (kreiranje, editovanje, deaktivacija, brisanje, spajanje tagova). Matrica ovlasti proširena sa redom "Upravljanje tagovima". Upravljanje kategorijama ostaje ekskluzivno za local\_admin. Napomena o local\_admin inherentnim ovlastima ažurirana da uključi obje permisije. |
| 1.8 | 28.3.2026 | Status → Završeno. Dodana praktična napomena o revert mogućnosti za auto-degradaciju. Napomena o local\_admin inherentnim ovlastima u matrici i permisijama. Dodan `blockedDetails`, `isVerifiedPublisher`. Parametrizirano Trust Tier napredovanje. Ispravljen dijagram arhitekture (Staff u tenant bazi). OWNER\_BLOCKED i opcija za sadržaj pri blokiranju. |

* * *

*Posljednje ažuriranje: 3.4.2026*  
*Vlasnik dokumenta: CityInfo tim*

‌