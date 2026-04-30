---
title: "02 - KORISNIČKO ISKUSTVO"
confluence_page_id: "240254995"
---

> **Verzija:** 3.6  
> **Datum:** 3.4.2026  
> **Status:** Završeno ✅

* * *
## O čemu je riječ?

Ovaj dokument opisuje kako korisnici percipiraju i koriste CityInfo platformu — od naslovne stranice i pretrage, preko prikaza sadržaja, do načina na koji se listinzi sortiraju i pozicioniraju. Fokus je na logici prikaza, ne na vizuelnom dizajnu ili implementaciji UI komponenti. Razumijevanje ovih koncepata pomaže i developerima koji grade funkcionalnosti i product ljudima koji definišu korisničko iskustvo.

Dokument pokriva čitav spektar korisnika — od neregistrovanih posjetilaca (visitors) koji samo pregledaju sadržaj, preko novih korisnika koji prolaze kroz onboarding, do iskusnih korisnika koji redovno objavljuju i promoviraju sadržaj.

* * *
## 2.1 Naslovna stranica

Naslovna stranica je ulazna tačka za većinu posjetilaca i **po defaultu prikazuje događaje** (režim "Događaji"). Ovo odražava primarni use case platforme — korisnici najčešće dolaze da vide šta se dešava u gradu. Struktura nije fiksna lista, već pametno složen prikaz koji uzima u obzir promocije, kategorije i sortDate vrijednosti.
### Prebacivanje režima

Iako naslovna prikazuje događaje, korisnik u svakom trenutku može prebaciti na režim "Mjesta" kroz jasno vidljivu navigaciju (tab, toggle ili slično). Ova opcija je uvijek dostupna i uočljiva kako bi korisnici koji traže mjesta mogli brzo promijeniti kontekst.

| Default | Alternativa |
| --- | --- |
| **Događaji** — šta se dešava | Mjesta — gdje otići |

> **💡 Praktična napomena:** Default na događaje ima smisla jer su oni vremenski osjetljivi — korisnik koji otvori aplikaciju u petak navečer vjerovatno traži "šta raditi večeras", ne "gdje je najbliža apoteka".
### Dvije grupe sadržaja na naslovnoj

Na naslovnoj stranici sadržaj se prikazuje u dvije prioritetne grupe:

| Grupa | Šta sadrži | Kako se sortira |
| --- | --- | --- |
| **Grupa 1** | Premium promocije sa opcijom "Prikaži na naslovnoj" | Po `sortDate` unutar grupe |
| **Grupa 2** | Svi ostali listinzi | Po `sortDate`, bez prioriteta |

Ključna stvar: grupa 1 ima **apsolutni prioritet** na naslovnoj. Čak i ako običan listing ima noviji `sortDate`, nikada neće "preskočiti" Premium+Homepage listing.

**Važno razlikovanje:** Premium promocije *bez* opcije "Prikaži na naslovnoj" nemaju prioritet na homepage-u — one imaju prioritet samo **unutar svoje kategorije** (vidi sekciju 2.4). Standard promocije nikada nemaju prioritet u sortiranju, već su samo vizuelno istaknute.
### Featured sekcije i kategorije

Pored dvije grupe, naslovna može sadržavati i tematske sekcije — npr. "Ovaj vikend", "Koncerti u blizini", ili "Novo otvoreno". Ove sekcije su konfigurisane od strane administratora i mogu se prilagođavati sezonski ili prema lokalnim potrebama.

> **💡 Praktična napomena:** Featured sekcije su alat za kuriranje sadržaja — omogućavaju isticanje relevantnih tema bez da korisnik mora aktivno pretraživati.

* * *
## 2.2 Pretraga i filteri

Korisnici dolaze na platformu sa različitim namjerama — neki znaju tačno šta traže, drugi samo "browsaju". Sistem pretrage i filtriranja mora podržati oba scenarija bez kompromisa na brzinu ili relevantnost.
### Dva režima: Događaji i Mjesta

CityInfo tretira događaje (Events) i mjesta (Places) kao **potpuno odvojene svjetove**. Korisnik u svakom trenutku radi u jednom od dva režima, a sučelje mu jasno stavlja do znanja koju opciju trenutno koristi.

| Aspekt | Režim "Događaji" | Režim "Mjesta" |
| --- | --- | --- |
| **Šta se pretražuje** | Samo Eventi | Samo Places |
| **Kategorije** | EventCategory lista | PlaceCategory lista |
| **Tagovi** | EventTags | PlaceTags |
| **Specifični filteri** | Datum odvijanja | —   |

**Prebacivanje režima** je uvijek dostupno — tipično kroz tab navigaciju ili toggle na vrhu stranice. Promjena režima resetuje aktivne filtere jer kategorije i tagovi nisu kompatibilni između režima.

> **💡 Praktična napomena:** Ova separacija nije samo tehnička — ona odražava različite korisničke namjere. Neko ko traži "gdje večerati" ima drugačiji mindset od nekoga ko traži "šta raditi večeras". Jasno razdvajanje pomaže korisnicima da brže dođu do cilja.
### Načini pronalaženja sadržaja

| Metoda | Opis | Tipičan korisnik |
| --- | --- | --- |
| **Quick search** | Tekstualna pretraga u search baru | Zna šta traži ("jazz koncert") |
| **Browse kategorije** | Klik na kategoriju, prolazak kroz listu | Istražuje opcije |
| **Filter kombinacije** | Datum + udaljenost + kategorija | Planira unaprijed |
### Autosuggest pri pretrazi

Dok korisnik kuca u search bar, sistem nudi prijedloge u **hijerarhijskom redoslijedu**. Ovo omogućava brži pristup željenom sadržaju bez potrebe za kompletnim unosom.

**Redoslijed prikazivanja rezultata:**

```
┌─────────────────────────────────────┐
│ 🔍 "teh"                            │
├─────────────────────────────────────┤
│ KATEGORIJE                          │
│   📁 Tehnika                        │
│   📁 Tehnologija                    │
├─────────────────────────────────────┤
│ TAGOVI                              │
│   🏷️ tehno-muzika                   │
├─────────────────────────────────────┤
│ LISTINZI                            │
│   📍 Tehno Shop Sarajevo            │
│   📍 Tehnika Servis Centar          │
│   📍 Tehnološki Park                │
└─────────────────────────────────────┘
```

**Šta se dešava pri kliku:**

| Tip rezultata | Akcija pri kliku |
| --- | --- |
| **Kategorija** | Aktivira se filter te kategorije, prikazuje se lista listinga |
| **Tag** | Aktivira se filter tog taga, prikazuje se lista listinga |
| **Listing** | Otvara se detaljna stranica tog listinga |

Autosuggest pretražuje samo sadržaj relevantan za trenutni režim — ako je korisnik u režimu "Mjesta", neće vidjeti EventCategory niti evente u rezultatima.

> **💡 Praktična napomena:** Hijerarhijski prikaz (kategorije → tagovi → listinzi) pomaže korisnicima da "suze" pretragu prije nego što vide konkretne rezultate. Ako neko traži "rest", vjerovatno želi kategoriju "Restorani", ne listing "Restoran Kod Muje".
### Glavne filter opcije

**Zajednički filteri (oba režima):**

- Kategorija (primarna ili bilo koja od sekundarnih)
- Tag (do `MAX_TAGS_PER_LISTING` po listingu)
- Udaljenost (od korisnikove lokacije)
- Tekstualna pretraga

**Event-specifični (samo režim "Događaji"):**

- Datum odvijanja — filter po jednom datumu, ne po intervalu. Ako događaj traje od 4. do 6. decembra, pojavit će se u rezultatima za bilo koji od ta tri datuma.
### Korisnikova lokacija i lokacijski dijalog

Mnoge funkcionalnosti platforme zavise od poznate lokacije korisnika — filter po udaljenosti, prikaz distance na karticama, featured sekcije tipa "U blizini". Lokacija nije obavezna za korištenje platforme, ali bez nje korisnik gubi dio iskustva. Sistem podržava dva načina postavljanja lokacije: automatski (GPS putem browser geolokacije) i ručni unos (pretraga grada/adrese ili pomjeranje pina na mapi).

Ručni unos nije samo "plan B" za slučaj odbijene dozvole — on pokriva i scenarij planiranja putovanja, kada korisnik želi istraživati ponudu u drugom gradu prije dolaska.

**Ključno pravilo:** Lokacijske funkcije (udaljenosti na karticama, filter po udaljenosti, sekcija "U blizini") su dostupne **isključivo** kada je korisnikova lokacija unutar zone pokrivenosti tenanta. Ako je lokacija van zone — bez obzira da li je postavljena putem GPS-a ili ručno — te funkcije se ne prikazuju.
#### Pristup lokaciji pri prvom dolasku

Kada korisnik prvi put otvori platformu, browser automatski prikazuje standardni location permission prompt. Nema prethodnog "soft prompta" od strane CityInfo-a — korisnik odmah vidi browser-ov upit za pristup lokaciji.

Browser prompt ima tri moguća ishoda:

| Ishod | Šta se dešava | Posljedica |
| --- | --- | --- |
| **Odobri** | GPS lokacija se dohvata, provjerava se zona tenanta | Ako je unutar zone — puna funkcionalnost; ako je van zone — lokacija poznata ali lokacijske funkcije nedostupne |
| **Odbije (Block)** | Browser trajno blokira pristup lokaciji za ovaj sajt | GPS opcija nedostupna; korisnik koristi ručni unos ili slijedi vizualno uputstvo za deblokiranje |
| **Ignoriše (dismiss)** | Prompt nestane, dozvola ostaje u neutralnom stanju | Kad korisnik kasnije klikne "Koristi moju lokaciju" u dijalogu, browser prompt se ponovo pojavi |

> **💡 Praktična napomena:** Razlika između "Odbije" i "Ignoriše" je bitna. Ako korisnik klikne "Block", web aplikacija ne može ponovo prikazati browser prompt — to je sigurnosno ograničenje svih modernih browsera. Ako samo zatvori prompt bez odgovora, dozvola ostaje neutralna i može se ponovo zatražiti.
#### Lokacijski indikator

U headeru aplikacije (blizu search bara) uvijek je vidljiv lokacijski indikator koji pokazuje trenutno stanje lokacije. Klik na indikator otvara lokacijski dijalog.

| Stanje | Indikator prikazuje | Lokacijske funkcije | Klik otvara |
| --- | --- | --- | --- |
| GPS lokacija unutar zone | 📍 Sarajevo | ✅ Dostupne | Lokacijski dijalog |
| Ručno postavljena, unutar zone | 📍 Baščaršija *(ručno)* | ✅ Dostupne | Lokacijski dijalog |
| GPS lokacija van zone | 📍 Zenica *(van područja)* | ❌ Nedostupne | Lokacijski dijalog sa porukom |
| Ručno postavljena, van zone | 📍 Beč *(van područja)* | ❌ Nedostupne | Lokacijski dijalog sa porukom |
| Lokacija nepoznata | 📍 Postavi lokaciju | ❌ Nedostupne | Lokacijski dijalog |
#### Lokacijski dijalog

Lokacijski dijalog je centralno mjesto za upravljanje lokacijom. Isti UI se koristi u svim situacijama — bilo da korisnik postavlja lokaciju prvi put, mijenja je, ili je uklanja.

**Elementi dijaloga:**

- **"Koristi moju lokaciju"** — triggeruje browser geolokaciju
- **Polje za pretragu** — autocomplete (Google Places) za unos grada ili adrese
- **Interaktivna mapa** — Google Maps sa vizuelno označenom zonom pokrivenosti tenanta i pinom koji korisnik može pomjerati
- **"Ukloni lokaciju"** — vraća korisnika u stanje "lokacija nepoznata"
- **"Primijeni"** — potvrđuje odabranu lokaciju
#### Zona pokrivenosti tenanta

Svaki tenant ima definisanu zonu pokrivenosti (centar + radijus). Provjera da li se lokacija nalazi unutar zone je binarna odluka:

| Lokacija | Rezultat |
| --- | --- |
| **Unutar zone** | Lokacijske funkcije dostupne |
| **Van zone** | Lokacijske funkcije nedostupne, indikator pokazuje *(van područja)* |

> **💡 Praktična napomena:** Radijus zone pokrivenosti je konfigurabilan na nivou tenanta. Operater ga može proširiti ili suziti po potrebi.
### Jezik sučelja

Korisnik može birati između dva jezika sučelja koja tenant podržava (npr. bosanski i engleski). Izbor jezika utiče na prikaz naziva, opisa, i UI elemenata — sadržaj se prikazuje na odabranom jeziku ako postoji prevod (`nameAlt`, `descriptionAlt`). Ako prevod ne postoji, prikazuje se sadržaj na primarnom jeziku tenanta.
### Kombiniranje filtera i pretrage

Filteri se mogu slobodno kombinovati — sistem koristi AND logiku između svih aktivnih filtera. Rezultati su presjek svih zadanih kriterija.

**Osnovna pravila:**

- **Svi filteri su sticky** — ostaju aktivni dok ih korisnik eksplicitno ne ukloni
- **Nema automatskog resetovanja** — promjena jednog filtera ne utiče na ostale
- **Aktivni filteri uvijek vidljivi** — prikazuju se kao chipovi sa opcijom uklanjanja (✕)

**Kada se šta resetuje:**

| Događaj | Filteri (kategorija, tag, datum, udaljenost, tekst) | Lokacija |
| --- | --- | --- |
| Promjena bilo kojeg filtera | Ostaju | Ostaje |
| "Očisti sve" | Resetuju se | Ostaje |
| Nova sesija (refresh, novi tab) | Resetuju se | Resetuje se |

**Prazni rezultati:**

Kada kombinacija filtera ne daje rezultate, sistem prikazuje prijedloge za relaksaciju — npr. "Ukloni filter X za Y rezultata".

> **💡 Praktična napomena:** Pretraga uključuje i `name`, `nameAlt`, `description`, i `descriptionAlt` polja, što omogućava pronalaženje sadržaja na oba jezika tenanta. Turist koji traži "restaurant" pronaći će i "restoran".

* * *
## 2.3 Listing prikaz

Listing se može prikazati u dva konteksta: kao **kartica** u listi/gridu i kao **detaljna stranica** kada korisnik klikne na njega. Oba prikaza dijele iste podatke, ali sa različitom dubinom informacija.
### Card komponenta (lista/grid)

| Element | Izvor | Napomena |
| --- | --- | --- |
| Slika | `featuredImageUrl` ili default iz kategorije | Aspect ratio konzistentan |
| Naziv | `name` (ili `nameAlt` ovisno o jeziku) | Skraćuje se ako je predugačak |
| Kratki opis | `excerpt` | Auto-generisan iz `description` ako nije ručno unesen |
| Kategorija | Iz `primaryCategoryData` snapshot-a | Prikazuje ime i boju |
| Tagovi | `primaryTagSlug`, `secondaryTagSlug` | Ako su dodijeljeni |
| Datum | `startDateTime` za Event | Lokalizovan format |
| Udaljenost | Kalkulisana od korisnikove lokacije | Prikazuje se samo ako je lokacija poznata **i unutar zone tenanta** |
| Broj lajkova | `totalAppreciations` | Socijalni signal |
| Promocijska oznaka | Ovisno o tipu promocije | Vizuelno isticanje |
| Verifikacija | Badge "✓ Potvrđen vlasnik" | Ako je `verificationStatus = verified` |
### Vizuelno razlikovanje promocija

- **Standard promocija:** Suptilan highlight (npr. blagi border ili pozadina)
- **Premium promocija:** Jače vizuelno isticanje (izraženija pozadina, border)
- **Premium + Homepage:** Isto kao Premium, dodatno istaknut na naslovnoj stranici
### Detaljna stranica

Kada korisnik klikne na listing, otvara se puna stranica sa svim dostupnim informacijama:

- Galerija slika (swipeable/carousel)
- Puni opis sa HTML formatiranjem
- Lokacija sa mapom (interaktivna)
- Kontakt informacije i vanjski link (`listingUrl`)
- Za evente: datum, vrijeme, i povezani Place (ako postoji)
- Za places: adresa, kontakt podaci
- Verifikacioni status (ako je verificiran)
- CTA elementi: lajkaj, spremi u favorite, podijeli, navigiraj
### Related content

Na dnu detaljne stranice prikazuju se povezani sadržaji koji pomažu korisniku da otkrije više relevantnog sadržaja. Logika odabira je sljedeća:

**Za Event:** sistem prikazuje do 6 stavki, birajući redom iz ovih izvora dok ne popuni listu: drugi eventi na istom Place-u (ako postoji veza), eventi iste primarne kategorije u narednih 14 dana, te eventi sa istim tagovima. Child eventi parent-a se ne prikazuju ovdje jer imaju zasebnu sekciju na parent stranici.

**Za Place:** sistem prikazuje do 6 stavki: nadolazeći eventi na tom mjestu (ako ih ima), te druga mjesta iste primarne kategorije u blizini (sortirana po udaljenosti, ako je lokacija korisnika poznata, inače po `sortDate`).

Promovirani listinzi nemaju prioritet u related content sekciji — cilj je relevantnost, ne monetizacija.

> **💡 Praktična napomena:** Related content algoritam ne mora biti savršen pri lansiranju — bitno je da postoji i da prikazuje nešto smisleno. Može se iterativno poboljšavati na osnovu podataka o klikovima.

* * *
## 2.4 Sortiranje i paginacija

Redoslijed prikazivanja listinga nije slučajan — kontroliše ga `sortDate` polje u kombinaciji sa promocijskim statusom.
### sortDate kao centralni mehanizam

`sortDate` je DateTime polje koje određuje poziciju listinga u svim sortiranim prikazima. Nije isto što i `createdAt` — može se osvježavati nezavisno.

**Kada se sortDate postavlja/osvježava:**

- Pri kreiranju listinga → postavlja se na trenutno vrijeme
- Pri objavljivanju (listing prelazi u `published` status) → može se osvježiti
- Kroz AutoRenew promociju → osvježava se automatski po definiranom intervalu
- Ručno od strane vlasnika → jednom u 24 sata (besplatno, svi korisnici)
### Uticaj promocija na pozicioniranje

| Kontekst | Premium listinzi | Standard + Obični |
| --- | --- | --- |
| **Na naslovnoj** | Samo sa "Prikaži na naslovnoj" opcijom imaju prioritet (Grupa 1) | Svi ostali u Grupi 2, sortirani po `sortDate` |
| **U kategoriji** | Uvijek na vrhu kategorije, sortirani po `sortDate` međusobno | Ispod Premium-a, sortirani po `sortDate` |
### AutoRenew i osvježavanje pozicije

AutoRenew automatski osvježava `sortDate` na odabranom intervalu. Dostupni intervali i njihov efekat:

| Interval | Osvježavanja dnevno | Efekat |
| --- | --- | --- |
| 24h | 1×  | Održava prisutnost |
| 8h  | 3×  | Pojačana vidljivost |
| 3h  | 8×  | Maksimalna ekspozicija |

> ⚠️ **Napomena:** Pricing model za AutoRenew opciju (množitelji bazne cijene, fiksni dodaci, ili drugi pristup) **još nije finaliziran**. Detalji o trenutnom stanju pricinga u [06 - Monetizacija, sekcija 6.2.4](../project-specs/06-monetizacija.md).
### Paginacija i infinite scroll

Za duge liste koristi se lazy loading pristup — učitava se inicijalni set rezultata, a dodatni se dohvataju kako korisnik skrola ili klikne "Prikaži više".

* * *
## 2.5 Mobile vs Desktop razlike

CityInfo je mobile-first platforma — većina korisnika dolazi sa mobilnih uređaja.
### Responzivni pristup

| Breakpoint | Uređaj | Karakteristike prikaza |
| --- | --- | --- |
| < 640px | Telefon | Jedna kolona, full-width kartice |
| 640–1024px | Tablet | Dvije kolone, kompaktnija navigacija |
| 1024px | Desktop | Višekolonski grid, sidebar navigacija |
### Mobile-specifični elementi

- Sticky header sa search barom
- Bottom navigation bar za brzi pristup ključnim sekcijama
- Floating action button za kreiranje novog sadržaja
- Simplified filtri u drawer/modal formatu

> **💡 Praktična napomena:** Testiranje novog feature-a uvijek treba prvo raditi na mobilnom uređaju. Ako funkcioniše dobro na telefonu, vjerovatno će raditi i na desktopu — obrnuto ne vrijedi.

* * *
## 2.6 Neregistrovani korisnici (Visitors)

Platforma je dizajnirana da bude korisna i za posjetioce koji ne žele kreirati račun. Visitors — neautentificirani korisnici — mogu pregledati sav javni sadržaj bez registracije. Ovo je posebno važno za turiste i casual posjetioce koji samo žele brzo pronaći informacije.
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

Detalji o Appreciation entitetu (za registrovane korisnike) i Favorite funkcionalnosti opisani su u [04 - Sadržaj, sekcija 4.9](../project-specs/04-sadrzaj.md).

> **💡 Praktična napomena:** Visitor lajkovi doprinose popularnosti listinga, ali bez pohrane ličnih podataka — u skladu sa GDPR zahtjevima. Ovo omogućava platformi da ima živu interakciju čak i sa korisnicima koji ne žele kreirati račun.

* * *
## 2.7 Registracija i onboarding

Prije nego korisnik može objavljivati sadržaj, mora proći kroz proces registracije i verifikacije. Cilj onboardinga je brzo dovesti korisnika do momenta kad može kreirati svoj prvi listing, uz minimalnu frikciju ali sa dovoljno provjera da se spriječi spam i zloupotreba.
### Koraci do prvog listinga

| Korak | Šta korisnik radi | Zašto je potrebno |
| --- | --- | --- |
| **Registracija** | Unosi email, username, lozinku | Osnovni identitet |
| **Email verifikacija** | Klikne link u email-u | Potvrda validne adrese |
| **GDPR saglasnost** | Prihvata uslove korištenja | Pravna obaveza |
| **Telefon verifikacija** | Unosi kod iz SMS-a | Potrebno prije kreiranja listinga |
### Trust Tier — šta to znači za korisnika

Novi korisnici počinju na **Tier 1 (Standard)** koji zahtijeva pregled sadržaja prije objavljivanja. Korisnik ne mora znati tehnički termin "Trust Tier", ali treba razumjeti:

- **Prvi sadržaji se pregledaju** prije nego postanu javni (pre-moderacija)
- **Nakon odobrenih sadržaja** buduće objave postaju vidljive odmah (napredovanje na Tier 2)
- **Ako sadržaj bude odbijen** vraća se na režim pregleda

| Tier | Naziv | Šta korisnik doživljava |
| --- | --- | --- |
| **1** | Standard | Svaki sadržaj čeka odobrenje (obično unutar 2h) |
| **2** | Trusted | Sadržaj odmah vidljiv, pregled naknadno |
| **3** | Established | Minimalna intervencija moderatora |

> **💡 Praktična napomena:** Onboarding poruke trebaju biti prijateljske i informativne, ne tehničke. Umjesto "Vaš trust tier je 1" bolje je "Vaš prvi sadržaj će pregledati naš tim prije objavljivanja — obično unutar nekoliko sati."

* * *
## 2.8 Objava sadržaja

Proces objave sadržaja razlikuje se ovisno o tome ima li korisnik "povjerenje" sistema ili je nov/ima istoriju odbijenih sadržaja.
### Dva moguća toka objave

**Tok A: Novi korisnik (Tier 1 — pre-moderacija)**

```
Korisnik kreira → Šalje na objavu → Čeka pregled → Moderator odlučuje → Objavljeno/Odbijeno
```

**Tok B: Iskusni korisnik (Tier 2+ — post-moderacija)**

```
Korisnik kreira → Šalje na objavu → Odmah vidljivo → Moderator može naknadno pregledati
```
### Šta korisnik vidi u svakom scenariju

| Scenarij | Poruka korisniku | Očekivano vrijeme |
| --- | --- | --- |
| **Poslano na pregled** | "Vaš sadržaj je poslan na pregled. Obavijestit ćemo vas čim bude odobren." | Do 2 sata |
| **Odmah objavljeno** | "Vaš sadržaj je objavljen! Naš tim će ga pregledati u narednim satima." | Instant (pregled naknadno) |
| **Potrebne izmjene** | "Potrebne su male izmjene prije objave. Pogledajte komentare ispod." | —   |
| **Odbijeno** | "Nažalost, ovaj sadržaj ne možemo objaviti. Razlog: \[specifičan razlog\]" | —   |
### Praćenje statusa objave

- **Draft** — još nije poslano na objavu
- **Čeka pregled** — poslano, čeka moderatora (`in_review`)
- **Potrebne izmjene** — moderator je ostavio komentare (`changes_requested`)
- **Objavljeno** — javno vidljivo (`published`)
- **Objavljeno — čeka pregled** — vidljivo, moderator pregleda naknadno (`published_under_review`)
- **Objavljeno — potrebne izmjene** — vidljivo, moderator traži blagu izmjenu (`published_needs_changes`)
- **Skriveno** — privremeno sakriveno od strane vlasnika, moderatora ili sistema (`hidden_by_owner`, `hidden_by_moderator`, `hidden_by_system`)
- **Otkazano** — vlasnik otkazao event, vidljivo sa badge-om "Otkazano" (`canceled`, samo Event)
- **Završeno** — event je prošao, vidljivo kao historijski zapis (`expired`, samo Event)
- **Odbijeno** — nije prošlo moderaciju, sa razlogom (`removed (rejected)`)

* * *
## 2.9 Wallet i promocije iz korisničke perspektive

Kreditni sistem je dizajniran da bude jednostavan za korištenje — korisnici kupuju kredite unaprijed, a zatim ih troše na promocije bez ponovnog prolaska kroz payment proces.
### Kupovina promocije — korisničko iskustvo

1. **Odabir listinga** — klik na "Promoviraj" na svom aktivnom listingu
2. **Odabir tipa** — Standard, Premium, ili Premium + Homepage
3. **Odabir trajanja** — 1, 3, 7, ili 30 dana
4. **AutoRenew opcija** — da li želi automatsko osvježavanje pozicije
5. **Pregled cijene** — jasno prikazan ukupni trošak u kreditima
6. **Potvrda** — instant aktivacija, bez čekanja

| Korak | Šta korisnik vidi |
| --- | --- |
| Nedovoljno kredita | "Potrebno je još X kredita. \[Kupi kredite\]" |
| Uspješna aktivacija | "Promocija aktivirana! Vaš listing je sada istaknut." |
| Aktivan listing sa promocijom | Badge + brojač preostalih dana |
### Praćenje efekata promocije

Korisnik može vidjeti kako promocija utiče na vidljivost:

- Broj pregleda (views)
- Broj klikova na detalje
- Poređenje sa periodom bez promocije

> **💡 Praktična napomena:** Korisnici često pitaju "da li se isplati promocija?". Transparentna statistika im pomaže donijeti informisanu odluku o budućim promocijama.

* * *
## Šta dalje?

- **Korisnici i pristup:** [03 - Korisnici i pristup](../project-specs/03-korisnici-i-pristup.md) — User entitet, Trust Tier sistem, registracija
- **Detalji o sadržaju:** [04 - Sadržaj](../project-specs/04-sadrzaj.md) — Listing, Event, Place entiteti i njihovi atributi
- **Moderacija:** [05 - Moderacija](../project-specs/05-moderacija.md) — Kako funkcioniše pregled i odobravanje sadržaja
- **Promocije i monetizacija:** [06 - Monetizacija](../project-specs/06-monetizacija.md) — Kreditni sistem i promocijski paketi

* * *
## Changelog

| Verzija | Datum | Opis promjene |
| --- | --- | --- |
| 3.6 | 3.4.2026 | **Optimizacija 13→12 statusa.** Reference ažurirane prema novom modelu. |
| 3.5 | 1.4.2026 | **MIGRACIJA — jednostatus model.** Sekcija 2.4: `waiting → active` terminologija zamijenjena sa `published` status terminologijom. |
| 3.4 | 28.3.2026 | Status → Završeno. AutoRenew množitelji uklonjeni iz tabele — pricing je draft/placeholder (referenca na Ch.06). Tagovi parametrizirani (`MAX_TAGS_PER_LISTING`). Related content logika definisana (2.3). Broken linkovi u "Šta dalje" sekciji popravljeni. Verifikacioni badge terminologija usklađena ("Potvrđen vlasnik"). Referenca na Ch.04 za Appreciation/Favorite entitete dodana u 2.6. |
| 3.3 | 26.3.2026 | 2.6: Visitor zaštita ažurirana — digitalni otisak preglednika (browser fingerprint) |
| 3.2 | 24.3.2026 | Dodana podsekcija "Korisnikova lokacija i lokacijski dijalog" u 2.2 |