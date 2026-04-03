# MVP SCOPE — Opseg prve verzije

> **Verzija:** 1.5  
> **Datum:** 3.4.2026  
> **Status:** Draft — čeka review tima

* * *
## O čemu je riječ?

Ovaj dokument definiše **opseg prve verzije (MVP)** CityInfo platforme — šta ulazi u lansiranje, šta je uključeno ali u jednostavnijem obliku, i šta svjesno ostavljamo za kasnije faze. Cilj MVP-a nije "napraviti sve", nego dokazati da platforma donosi vrijednost korisnicima i organizatorima u jednom gradu prije nego se širi i nadograđuje.

Odluke su donesene na osnovu analize kompletne dokumentacije (sekcije 01–08) sa fokusom na tri pitanja: da li je funkcionalnost neophodna za osnovni user journey, koliko košta u razvoju, i koliki je rizik ako je izostavimo.

**MVP u jednoj rečenici:** Korisnik može kreirati Event ili Place sa slikama i dvojezičnim sadržajem, kategorizirati ga, poslati na moderaciju (uz AI screening i automatsko Trust napredovanje), i promovirati ga kroz Standard, Premium ili Premium+Homepage promociju sa AutoRenew opcijom koristeći prepaid kredite — u jednom gradu, sa email/in-app notifikacijama i ručno upravljanim display oglašavanjem.

* * *
## MVP core — ulazi u prvu verziju

Ovo su funkcionalnosti bez kojih platforma ne funkcioniše. Svaka od njih je na kritičnom putu za barem jedan ključni user journey (objavljivanje sadržaja, otkrivanje sadržaja, ili moderacija).
### Sadržaj i organizacija

| Funkcionalnost | Šta uključuje | Referenca |
| --- | --- | --- |
| **Listing CRUD** | Kreiranje, uređivanje, brisanje Events i Places sa upload slika (featured + galerija do 5). Bazična validacija formata i veličine. | 04 - Sadržaj (4.1–4.3) |
| **Dvojezičnost** | Svaki listing podržava primarni i sekundarni jezik — `nameAlt`, `descriptionAlt`, `excerptAlt`. Logika prikaza na osnovu korisničkih postavki ili jezičke preferencije. | 01 - Uvod (1.1), 04 - Sadržaj (4.1) |
| **Kategorije i tagovi** | Odvojeni sistemi za Event i Place kategorije. Primarna + do 10 sekundarnih kategorija. Do 2 taga po listingu. Admin upravljanje kategorijama i tagovima. | 04 - Sadržaj (4.4–4.5) |
| **Listing status i vidljivost** | Jednostatus model sa 12 eksplicitnih `listingStatus` vrijednosti (`draft`, `in_review`, `published`, `hidden_by_owner`, `removed`, itd.). `isPublic` derivacija iz statusa. `removedReason` za trajno uklanjanje. `wasEverActive` kontrola brisanja. | 04 - Sadržaj (4.8) |
| **Event hijerarhija** | Parent/child veza za festivale i višednevne događaje (max 2 nivoa). Samo vlasnik parent-a kreira child evente. | 04 - Sadržaj (4.2) |
| **ListingDocument** | Upload dokumenata za verifikaciju vlasništva/prava upravljanja. Moderator može zatražiti i pregledati dokument. Ograničeni formati (PDF, JPG, PNG) i veličina. Automatski virus scanning putem vanjskog servisa. | 04 - Sadržaj (4.7) |
| **sortDate mehanizam** | Centralno polje za sortiranje. Besplatni ručni refresh jednom u 24h za sve korisnike. | 04 - Sadržaj (4.1), 06 - Monetizacija (6.2) |

**Praktična napomena:** Event hijerarhija je u MVP-u jer višednevni događaji poput Sarajevo Film Festivala predstavljaju ključnu priliku za promociju platforme pri lansiranju. Bez ove funkcionalnosti gubimo najvrednije content partnere.

**Praktična napomena:** ListingDocument je u MVP-u jer štiti integritet platforme. Bez mogućnosti da moderator zatraži dokaz vlasništva, nemamo mehanizam za sprječavanje lažnih listinga — a jedan lažni profil restorana sa pogrešnim informacijama može narušiti povjerenje korisnika i samih biznisa u platformu. Virus scanning za uploadovane dokumente koristi vanjski servis i ne zahtijeva značajan custom razvoj.

**Praktična napomena:** Dvojezičnost je od starta jer su polja za sekundarni jezik jednostavno opciona polja na postojećim entitetima — ne opterećuju UI niti zahtijevaju posebnu logiku osim prikaza na osnovu jezičke preferencije. Turisti su jedna od ključnih persona (Thomas), a platforma je od početka zamišljena kao dvojezična.
### Korisnici i pristup

| Funkcionalnost | Šta uključuje | Referenca |
| --- | --- | --- |
| **User registracija** | Email registracija, login, bazični profil. | 03 - Korisnici (3.3) |
| **Visitor pristup** | Neregistrovani korisnici mogu pregledati javni sadržaj, koristiti pretragu, lajkati i dijeliti — bez kreiranja računa. | 01 - Uvod (1.3) |
| **Trust Tier sistem (svih 5 nivoa)** | Tier 0 (Restricted) do Tier 4 (Verified Partner). Pre-moderacija za Tier 0–1, post-moderacija za Tier 2+. Sampling za Tier 3. **Uključuje automatsko napredovanje i degradaciju.** | 03 - Korisnici (3.4) |
| **Staff panel** | Interfejs za moderatore: pregled queue-a, donošenje odluka, upravljanje korisnicima, kategorijama i tagovima. | 03 - Korisnici (3.5) |

**Praktična napomena:** Trust Tier sa automatskim napredovanjem/degradacijom mora biti u MVP-u jer bez toga moderatori moraju ručno pratiti i mijenjati tier za svakog korisnika — što je neodrživo čim platforma dobije i nekoliko desetina aktivnih korisnika. Automatski mehanizam (napredovanje nakon X odobrenih objava, degradacija nakon odbijenih) je jednostavan za implementaciju, a drastično smanjuje operativno opterećenje.
### Korisnički doživljaj

| Funkcionalnost | Šta uključuje | Referenca |
| --- | --- | --- |
| **Pretraga i filteri** | Filter po kategoriji, datumu, lokaciji/mapi. Dva odvojena režima (Događaji / Mjesta). | 02 - Korisnički doživljaj (2.2) |
| **Naslovna stranica** | Dvije grupe sadržaja na naslovnoj: Premium+Homepage (prioritet), svi ostali. Unutar kategorija: Premium sekcija na vrhu, Standard+obični ispod. Default na Events režim. | 02 - Korisnički doživljaj (2.1) |
| **Listing prikaz** | Kartice u listama, detail stranica, galerija slika. | 02 - Korisnički doživljaj (2.3) |
| **Responsive UI** | Mobile-first dizajn, prilagođen za touch i desktop. | 02 - Korisnički doživljaj (2.5) |
### Moderacija

| Funkcionalnost | Šta uključuje | Referenca |
| --- | --- | --- |
| **Moderacijski workflow** | Queue sa prioritizacijom. Tri odluke: approve, changes\_requested, removed (rejected). SLA smjernice (2h pre, 8h post). | 05 - Moderacija (5.2) |
| **AI screening** | Automatska provjera slika i teksta putem vanjskih servisa. Detekcija adult contenta, nasilja, offensive texta. Automatsko blokiranje uploada koji ne prođe screening. Konfigurisani thresholds sa `aiBlockingFlag`. | 05 - Moderacija (5.3) |
| **Message sistem** | Jedan thread po listingu. Moderator započinje komunikaciju. Statusi: idle, waiting\_owner, waiting\_moderator. Tekstualne poruke + reference na ListingDocument. | 07 - Komunikacija (7.1) |

**Praktična napomena:** AI screening ulazi u MVP u punom obliku jer se oslanja na vanjske servise (cloud API pozivi) — vlastiti razvoj je minimalan, a zaštita od neprimjerenog sadržaja je kritična za reputaciju platforme od prvog dana. Trošak po pozivu je nizak i predvidljiv.
### Monetizacija

| Funkcionalnost | Šta uključuje | Referenca |
| --- | --- | --- |
| **Kreditni sistem** | Wallet sa stanjem, kupovina paketa kredita (3–4 fiksna paketa sa cijenama), CreditTransaction za audit trail. | 06 - Monetizacija (6.1) |
| **Promocije (sva tri tipa)** | Standard (20kr/dan), Premium (40kr/dan), Premium+Homepage (60kr/dan). Vizualno isticanje. Tri grupe sortiranja na naslovnoj i u kategorijama. | 06 - Monetizacija (6.2) |
| **AutoRenew mehanizam** | Automatsko osvježavanje `sortDate` na odabranom intervalu (3h/8h/24h). Background job za automatsko osvježavanje. Pricing model za AutoRenew još nije finaliziran — vidi 06 - Monetizacija (6.2.4). | 06 - Monetizacija (6.2.4) |
| **Display oglašavanje (ručno upravljanje)** | Staff ručno postavlja banner oglase (DisplayAd entitet) kroz admin panel. Predefinisane zone (header, sidebar, in-feed, mobile). Round-robin prikaz po prioritetu (`sortOrder`). Praćenje impressions/clicks za izvještavanje. Bez self-service-a, kampanja, biddinga ili targetinga. | 06 - Monetizacija (6.3) |

**Praktična napomena:** AutoRenew je prirodni dio promotivnog sistema — bez njega, korisnici koji kupe Premium promociju na 7+ dana moraju se ručno vraćati da osvježe poziciju, što je loše korisničko iskustvo i smanjuje vrijednost plaćene promocije. Implementacijski je to jedan background job koji periodično ažurira `sortDate`.

**Praktična napomena:** Display Advertising je u MVP-u jer će u ranoj fazi biti primarni izvor prihoda — dok korisnici još ne vide dovoljno traffica da investiraju u promocije listinga, lokalni biznisi su spremni platiti banner ako im se pokaže posjećenost. MVP verzija koristi ručno postavljanje oglasa od strane Staffa, što daje potpunu kontrolu timu i zahtijeva minimalan razvoj. Napredni sistem (Advertiser profili, kampanje, CPC bidding, targeting, fraud detection) je planiran za Fazu 2 kada broj oglašivača preraste kapacitet ručnog upravljanja.
### Komunikacija

| Funkcionalnost | Šta uključuje | Referenca |
| --- | --- | --- |
| **Email notifikacije** | Transakcijske (listing odobren/odbijen/changes\_requested), moderacijske (nova poruka od moderatora), promotivne (promocija ističe). | 07 - Komunikacija (7.2) |
| **In-app notifikacije** | Badge sa brojem nepročitanih, lista notifikacija, označavanje kao pročitano. | 07 - Komunikacija (7.2) |
### Infrastruktura

| Funkcionalnost | Šta uključuje | Referenca |
| --- | --- | --- |
| **Jedan tenant** | Jedan grad (Sarajevo), jedna baza, jedna konfiguracija. Bez tenant registry-a i izolacije. | 08 - Infrastruktura (8.1) |
| **Background jobs** | Automatski expiry evenata, soft delete cleanup, AutoRenew boost, auto-close threadova. | 08 - Infrastruktura (8.3) |

* * *
## Šta je na čekanju — planirane funkcionalnosti za post-MVP faze

Ove funkcionalnosti su dokumentirane i specifikacijski promišljene, ali svjesno ih ostavljamo za buduće iteracije. Razlozi variraju — neke zahtijevaju obim korisnika koji MVP još nema, neke su skupe za razvoj uz nisku početnu vrijednost, a neke su optimizacije koje imaju smisla tek na većem obimu.
### Faza 2 — nadogradnja nakon lansiranja

Ovo su funkcionalnosti koje očekujemo da će trebati relativno brzo nakon lansiranja — bilo kroz korisnički feedback ili kroz poslovne prilike.

| Funkcionalnost | Zašto čeka | Okidač za uključivanje | Referenca |
| --- | --- | --- | --- |
| **Napredni Display Ads** | Advertiser entitet, AdCampaign sa CPC biddingom, targeting po kategorijama, weighted random selection, fraud detection, self-service portal za oglašivače. | Kad broj oglašivača preraste kapacitet ručnog upravljanja (okvirno 10+ istovremenih oglašivača). | 06 - Monetizacija (6.3.6) |
| **Push notifikacije** | Firebase/APNs integracija, device token management. | Kad analitika pokaže da korisnici ne reaguju dovoljno brzo na email/in-app notifikacije, posebno za time-sensitive sadržaj. | 07 - Komunikacija (7.2) |
| **Korisničke preference za notifikacije** | Kontrola tipova notifikacija po kanalima, frekvencija digest emailova, quiet hours. | Kad korisnici počnu davati feedback o previše notifikacija. | 07 - Komunikacija (7.2.3) |
| **Multi-tenant infrastruktura** | Tenant registry, database izolacija, tenant konfiguracija, cross-tenant operacije. Vidi napomenu ispod. | Kad se pojavi konkretan drugi grad / partner — ili ranije ako se procijeni da je jeftinije graditi multi-tenant od starta nego refaktorisati naknadno. | 08 - Infrastruktura (8.1) |
| **GlobalAdmin portal** | Zasebna aplikacija ([master.cityinfo.ba](http://master.cityinfo.ba)) za 2–5 sistemskih admina. | Kad postoje 2+ tenanta i kad Staff panel više nije dovoljan za cross-tenant upravljanje. | 03 - Korisnici (3.6) |

> ⚠️ **Napomena o multi-tenant funkcionalnostima**
> 
> Multi-tenant infrastruktura, GlobalAdmin portal i franšizno poslovanje nisu opcione optimizacije — to su **preduvjeti za pokretanje drugog grada** kroz zajedničku platformu. Bez njih, jedina alternativa je pokretanje zasebnih instanci (klonirani deployment) po gradu. To je izvodljivo za 2–3 grada, ali operativno neodrživo dugoročno jer svaki bug fix, patch i novi feature mora se deployati na svaku instancu odvojeno, konfiguracije divergiraju, a infrastrukturni troškovi rastu linearno.
> 
> Ove funkcionalnosti su svrstane u Fazu 2 jer se ne isplati graditi tenant infrastrukturu za jedan grad — ali **mogu postati prioritet ranije od očekivanog** ako se pojavi konkretan partner ili tržišna prilika za drugi grad. U tom slučaju, bolje je uložiti u multi-tenant infrastrukturu odmah nego klonirati sistem i duplirati troškove održavanja. Odluka zavisi od timinga: ako se drugi grad pojavi u prvih 6 mjeseci, multi-tenant se gradi kao dio Faze 2. Ako se pojavi tek nakon 12+ mjeseci, može se raditi i kao dio Faze 3 sa više iskustva i stabilnijim codebase-om.
> 
> **Preporuka:** Čak i dok MVP radi sa jednim tenantom, korisno je u kodu izbjegavati hardkodiranje tenant-specifičnih vrijednosti (URL-ovi, valuta, nazivi) i umjesto toga koristiti konfiguracijske parametre. Ovo ne košta gotovo ništa u razvoju, a drastično olakšava kasniju tranziciju na multi-tenant arhitekturu.
### Faza 3 — skaliranje

Ove funkcionalnosti imaju smisla kad platforma ima stabilan operativni model i značajan obim.

| Funkcionalnost | Zašto čeka | Okidač za uključivanje | Referenca |
| --- | --- | --- | --- |
| **Franšizno poslovanje** | Setup fee, revenue share model, white-label branding, partner onboarding, obuka. Zahtijeva dokazan poslovni model i operativnu zrelost. | Kad platforma profitabilno radi u barem jednom gradu i kad se pojavi konkretan zainteresovani partner. | 06 - Monetizacija (6.4) |
| **Support ticket sistem** | `SupportTicket` entitet, 4 nivoa eskalacije (L1–L4), SLA tracking, satisfaction rating, canned responses. | Kad support tim naraste na 3+ ljudi i email inbox postane neodrživ. | 07 - Komunikacija (7.3) |
| **SLA tracking i metrike** | `firstResponseAt`, compliance rate, eskalacijski triggeri (50%/80%/100%). | Kad postoji support ticket sistem i kad je obim dovoljno velik da zahtijeva automatizovano praćenje. | 07 - Komunikacija (7.3.7) |
| **Satisfaction rating** | Ocjena korisničke podrške (1–5 zvjezdica) po zatvaranju ticketa. | Kad postoji support ticket sistem. | 07 - Komunikacija (7.3.3) |
### Backlog — korisno, ali nema vremenski pritisak

| Funkcionalnost | Zašto čeka | Referenca |
| --- | --- | --- |
| **A/B testiranje cijena** | MVP treba fiksne, razumne cijene. Prilagođavanje na osnovu ručnog feedbacka. | 06 - Monetizacija (6.5) |
| **Pricing po tenantu** | Prilagođavanje cijena po kupovnoj moći, konkurenciji, sezonalnosti. Nema smisla za jedan grad. | 06 - Monetizacija (6.5.4) |
| **Scheduled promotions** | Zakazivanje promocija unaprijed (umjesto instant aktivacije). | 06 - Monetizacija (6.2.2) |
| **Kompletan audit log** | Strukturiran audit trail sa retention politikama i compliance zahtjevima. | 08 - Infrastruktura (8.2) |
| **Tag spajanje** | Mogućnost spajanja sličnih tagova ("wifi" i "wi-fi") sa automatskom migracijom listinga. | 04 - Sadržaj (4.5) |

* * *
## Šta MVP NE pokriva (a dokumentacija opisuje)

Radi kompletnosti, ovo su stavke koje su u dokumentaciji ali nisu ni u MVP-u ni u "na čekanju" listama — jer su ili previše granularne za ovaj nivo planiranja, ili su operativne prakse koje se definišu kroz korištenje:

- **Persone i user journey-i** (1.5) — korisne za razumijevanje, ali nisu "feature" za razvoj
- **Brzi start vodiči** (1.4) — dokumentacija, ne funkcionalnost
- **Canned responses za podršku** — operativna praksa, ne sistemska funkcionalnost
- **Detaljni email template-i** — dizajnerski posao, ne feature scope
- **Dijagram arhitekture** (1.2) — referenca, ne deliverable

* * *
## Kako čitati ovaj dokument

Svaka funkcionalnost u "na čekanju" sekciji ima **okidač za uključivanje** — konkretan uvjet koji signalizira da je došlo vrijeme za implementaciju. Ovo nije "jednog dana ćemo", nego "kad se desi X, onda gradimo Y". Okidači nisu isključivi — ako se više njih aktivira istovremeno, prioritizacija se radi na osnovu poslovnog impakta i razvojnog troška.

Faze nisu strogo sekvencijalne. Multi-tenant funkcionalnosti su nominalno u Fazi 2, ali se mogu aktivirati i ranije ako se pojavi poslovna prilika — ili odložiti ako prvi grad zahtijeva više pažnje nego što se očekivalo. Ključno je da su preduvjeti dokumentirani i da tim razumije trade-offove.

Dokument je živ i ažuriraće se kako MVP bude napredovao.

* * *
## Changelog

| Verzija | Datum | Opis |
| --- | --- | --- |
| 1.5 | 3.4.2026 | **Optimizacija 13→12 statusa.** Reference ažurirane prema novom modelu. |
| 1.4 | 1.4.2026 | **Migracija na jednostatus model:** Red "Lifecycle i vidljivost" ažuriran na "Listing status i vidljivost" sa novom terminologijom — 13 `listingStatus` vrijednosti umjesto starog `draft → waiting → active → closed` flow-a. `closedReason` zamijenjen sa `removedReason`. Dodani `wasEverActive` i `isPublic` derivacija. |
| 1.0 | Mart 2026 | Inicijalna verzija na osnovu analize sekcija 01–08 |
| 1.1 | Mart 2026 | Vraćeno u MVP: AutoRenew, napredni AI screening, automatsko Trust napredovanje, virus scanning, dvojezičnost. Smanjena "na čekanju" lista. |
| 1.2 | Mart 2026 | Multi-tenant i GlobalAdmin pomjereni iz Faze 3 u Fazu 2 sa detaljnom napomenom o preduvjetima i trade-offovima. Franšiza ostaje u Fazi 3. Pojašnjena filozofija faziranja — faze nisu strogo sekvencijalne. |
| 1.3 | Mart 2026 | Display Ads opis usklađen sa novim MVP pristupom — ručno upravljanje bannerima (DisplayAd entitet) umjesto kampanja. AutoRenew referenca ažurirana (pricing još nije finaliziran). Napredni Display Ads okidač i referenca ažurirani (6.3.6). |

* * *

*Vlasnik dokumenta: CityInfo tim*