---
title: "07 - KOMUNIKACIJA"
confluence_page_id: "240320540"
---

> **Verzija:** 1.5  
> **Status:** Završeno ✅  
> **Datum:** 3.4.2026

* * *
## Pregled poglavlja

Komunikacija je krvotok svakog sistema koji povezuje korisnike sa sadržajem i timom koji stoji iza platforme. U CityInfo ekosistemu, komunikacija služi dvama ključnim ciljevima: omogućava moderatorskom timu da efikasno komunicira s vlasnicima listinga kad nešto treba ispraviti ili verificirati, i pruža korisnicima jasan kanal za podršku kad naiđu na problem.

Ovaj dokument pokriva tri glavna komunikacijska podsistema: **Message sistem** (komunikacija vezana za listing), **Notifikacije** (obavještenja korisnicima o bitnim događajima) i **Support sistem** (opća podrška korisnicima). Svaki od ovih sistema ima jasnu svrhu i pravila, ali svi dijele istu filozofiju — komunikacija treba biti korisna, pravovremena i bez nepotrebnog šuma.
### Sekcije u ovom poglavlju

| Sekcija | Opis | Ciljna publika | MVP status |
| --- | --- | --- | --- |
| **7.1 Message sistem** | Thread-based komunikacija moderator ↔ vlasnik | Dev + Ops | ✅ MVP |
| **7.2 Notifikacije** | Email, push, in-app obavještenja, Notification entitet | Dev + Product | ✅ MVP (base) |
| **7.3 Support sistem** | Ticket-based podrška korisnicima | Ops + Dev | ⏳ Faza 3 |
| **7.4 API Endpoints** | Lista endpointa za komunikaciju | Dev | —   |
### Povezani dokumenti

- [03 - Korisnici i pristup](../project-specs/03-korisnici-i-pristup.md) — Trust Tier sistem, blokiranje korisnika
- [04 - Sadržaj](../project-specs/04-sadrzaj.md) — Listing lifecycle, ListingDocument entitet (SSoT, sekcija 4.7), korisničke interakcije (sekcija 4.9), API endpointi za dokumente (sekcija 4.10)
- [05 - Moderacija](../project-specs/05-moderacija.md) — Moderacijski workflow, AI screening

* * *
## 7.1 Message sistem
### 7.1.1 Šta je Message sistem

Message sistem omogućava strukturiranu komunikaciju između moderatora i vlasnika listinga. Za razliku od generičkog chata ili email podrške, ove poruke su uvijek vezane za konkretan listing (Event ili Place), što osigurava da svaka komunikacija ima jasan kontekst i svrhu.

Ključna karakteristika sistema je **moderator-first pristup** — samo moderator može započeti novu komunikaciju. Ovo nije ograničenje, već svjesna odluka koja sprječava spam i osigurava da svaka komunikacija ima legitimnu svrhu vezanu za moderaciju sadržaja.
### 7.1.2 Kada se koristi

Message sistem se aktivira u nekoliko tipičnih scenarija vezanih za moderacijski workflow:

| Scenarij | Primjer | Tipičan ishod |
| --- | --- | --- |
| **Potrebne izmjene** | Listing ima nepotpune informacije | Korisnik dopuni, moderator odobri |
| **Verifikacija vlasništva** | Sumnja u legitimnost mjesta | Korisnik dostavi dokument, moderator pregleda |
| **Pojašnjenja** | Nejasan opis događaja | Korisnik pojasni, sadržaj ostaje ili se doradi |
| **Napomene uz odobrenje** | Listing odobren, ali treba pažnja | Korisnik informisan, bez akcije |

**Praktična napomena:** Message sistem je usko vezan za moderacijski workflow opisan u dokumentu 05 - Moderacija. Moderator koristi ovaj sistem kada listing zahtijeva komunikaciju prije donošenja odluke (`approved`, `changes_requested`, ili `removed (rejected)`).
### 7.1.3 Jedan thread po listingu

Arhitektura Message sistema je namjerno jednostavna: **svaki listing ima tačno jedan thread koji postoji dok postoji listing**. Nema otvaranja i zatvaranja thread-ova — samo se status mijenja ovisno o tome ko čeka čiji odgovor.

Ovaj pristup ima nekoliko prednosti:

- **Kompletna historija** — sva komunikacija o listingu je na jednom mjestu
- **Jednostavnost** — nema razmišljanja "da li otvoriti novi thread"
- **Kontinuitet** — ako za 6 mjeseci treba nova komunikacija, isti thread, nova poruka

```
stateDiagram-v2
    [*] --> idle: Thread kreiran sa listingom
    idle --> waiting_owner: Moderator šalje poruku
    waiting_owner --> waiting_moderator: Korisnik odgovara
    waiting_moderator --> waiting_owner: Moderator odgovara
    waiting_owner --> idle: Tema riješena
    waiting_moderator --> idle: Tema riješena
```

**Praktična napomena:** Thread se kreira automatski kada se kreira listing. Status `idle` znači da nema aktivne komunikacije — thread postoji, ali "spava". Kada moderator pošalje prvu (ili novu) poruku, status se aktivira.
### 7.1.4 Ko može slati poruke i kada

Statusni model thread-a direktno kontroliše ko može slati poruke u datom trenutku. Ovo je mehanizam koji osigurava "moderator-first" pristup bez potrebe za složenom logikom:

| Status thread-a | Moderator može slati? | Vlasnik može slati? | Obrazloženje |
| --- | --- | --- | --- |
| `idle` | ✅ Da | ❌ Ne | Samo moderator može pokrenuti komunikaciju |
| `waiting_owner` | ✅ Da | ✅ Da | Čeka se odgovor vlasnika, ali moderator može dodati pojašnjenje |
| `waiting_moderator` | ✅ Da | ✅ Da | Čeka se moderator, ali vlasnik može dopuniti prethodni odgovor |

Kada je thread u `idle` statusu, API odbija zahtjeve za slanje poruka od vlasnika listinga. Tek kada moderator pošalje prvu poruku i thread pređe u `waiting_owner`, vlasnik dobija mogućnost odgovora. Na taj način se "samo odgovaranje" reguliše kroz sam statusni model — nije potrebna dodatna logika ili posebna pravila pristupa.

**Praktična napomena:** Sistemske poruke (`system` role) mogu se slati u bilo kojem statusu thread-a jer služe za automatske obavijesti (npr. "Moderator čeka vaš odgovor već 5 dana"). Sistemske poruke ne mijenjaju status thread-a.
### 7.1.5 ListingMessageThread entitet

Thread predstavlja komunikacijski kanal za listing — jedan thread, jedna historija, promjenjiv status.

| Atribut | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| threadId | String | Jedinstveni identifikator thread-a | Da  | —   |
| listingId | String | ID povezanog listinga | Da  | Event ili Place |
| status | Enum | Trenutni status thread-a | Da  | Vidi statusni model |
| assignedTo | String | ID dodijeljenog moderatora | Ne  | Može biti NULL kad je idle |
| messageCount | Number | Ukupan broj poruka | Da  | Denormalizovano za performanse |
| lastMessageAt | DateTime | Vrijeme zadnje poruke | Ne  | —   |
| lastMessageBy | String | Ko je poslao zadnju poruku | Ne  | —   |
| createdAt | DateTime | Vrijeme kreiranja | Da  | Obično isto kad i listing |

> 📝 Lista atributa nije konačna i može se proširivati prema potrebama sistema.
#### Thread statusi

| Status | Značenje | Šta se očekuje |
| --- | --- | --- |
| `idle` | Nema aktivne komunikacije | Thread "spava", niko ne čeka ništa |
| `waiting_owner` | Čeka se korisnik | Moderator je poslao poruku, korisnik treba odgovoriti |
| `waiting_moderator` | Čeka se moderator | Korisnik je odgovorio, moderator treba pregledati |

**Praktična napomena:** Za razliku od prethodne verzije, nema `open` i `closed` statusa. Thread nikad nije "zatvoren" — samo je aktivan ili neaktivan (`idle`). Ovo pojednostavljuje logiku i omogućava kontinuitet komunikacije kroz vrijeme.
### 7.1.6 ListingMessage entitet

Svaka pojedinačna poruka u thread-u. Poruke mogu slati vlasnik listinga, moderator ili sistem (automatske notifikacije).

| Atribut | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| messageId | String | Jedinstveni identifikator poruke | Da  | —   |
| threadId | String | ID thread-a kojem pripada | Da  | —   |
| senderId | String | ID pošiljaoca | Da  | —   |
| senderRole | Enum | Uloga pošiljaoca | Da  | `owner`, `moderator`, `system` |
| messageText | String | Tekst poruke | Da  | —   |
| documentIds | List | Lista ID-eva priloženih dokumenata | Ne  | Reference na ListingDocument |
| sentAt | DateTime | Vrijeme slanja | Da  | —   |

> 📝 Lista atributa nije konačna i može se proširivati prema potrebama sistema.
### 7.1.7 Dokumenti u porukama

Poruke mogu referencirati dokumente vezane za listing. Dokumenti se ne čuvaju u poruci, već u centraliziranom **ListingDocument** entitetu koji je definisan u [04 - Sadržaj, sekcija 4.7](../project-specs/04-sadrzaj.md). Poruka samo sadrži listu `documentIds` koji referenciraju postojeće dokumente. API endpointi za dokumente žive u [04 - Sadržaj, sekcija 4.10](../project-specs/04-sadrzaj.md).
### 7.1.8 Ključna pravila

Nekoliko pravila osigurava da Message sistem funkcioniše kako treba:

| Pravilo | Obrazloženje |
| --- | --- |
| **Samo moderator započinje komunikaciju** | Korisnik može odgovoriti tek kad moderator aktivira thread (vidi sekciju 7.1.4) |
| **Jedan thread po listingu** | Thread postoji dok postoji listing |
| **Thread se nikad ne "zatvara"** | Samo prelazi u `idle` kad nema aktivne teme |
| **Dokumenti su centralizirani** | Svi na jednom mjestu (ListingDocument u poglavlju 04), poruke samo referenciraju |
| **Virus scan obavezan** | Dokument nije dostupan dok ne prođe skeniranje |

* * *
## 7.2 Notifikacije
### 7.2.1 Šta su notifikacije

Notifikacije su način da sistem obavijesti korisnike o bitnim događajima — bilo da je listing odobren, da je stigla nova poruka, da ističe promocija, ili bilo šta drugo što zahtijeva korisnikovu pažnju. Dobra notifikacija je informativna, pravovremena i ne preopterećuje korisnika.

CityInfo koristi tri kanala za notifikacije: **email**, **push notifikacije** (mobilne) i **in-app notifikacije** (unutar same aplikacije).
### 7.2.2 Kanali notifikacija

| Kanal | Kada se koristi | Karakteristike |
| --- | --- | --- |
| **Email** | Važne informacije, sumarizacije | Trajan zapis, može sadržavati detalje |
| **Push** | Hitne informacije, real-time | Kratko, zahtijeva pažnju odmah |
| **In-app** | Manje hitne informacije | Vidi se pri sljedećem korištenju aplikacije |
#### Tipični scenariji

| Događaj | Email | Push | In-app |
| --- | --- | --- | --- |
| Listing odobren | ✅   | ✅   | ✅   |
| Listing odbijen | ✅   | ✅   | ✅   |
| Potrebne izmjene (changes\_requested) | ✅   | ✅   | ✅   |
| Nova poruka od moderatora | ✅   | ✅   | ✅   |
| Promocija ističe | ✅   | ⚙️  | ✅   |
| Verifikacija uspješna | ✅   | ⚙️  | ✅   |
| Sedmični pregled | ✅   | ❌   | ❌   |

*⚙️ = zavisi od korisničkih postavki (Faza 2)*

**Praktična napomena:** U MVP-u, sistem šalje sve notifikacije po default konfiguraciji — svi kanali aktivni za sve tipove događaja. Korisničke preference za kontrolu notifikacija planirane su za Fazu 2 (vidi sekciju 7.2.4).
### 7.2.3 Notification entitet

Svaka notifikacija koja se prikazuje korisniku u in-app interfejsu se evidentira kao zapis u bazi. Ovo omogućava badge sa brojem nepročitanih, listu notifikacija u profilu, i praćenje da li je korisnik vidio važne informacije.

| Atribut | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| notificationId | String | Jedinstveni identifikator | Da  | —   |
| userId | String | ID korisnika koji prima notifikaciju | Da  | —   |
| type | Enum | Tip notifikacije | Da  | Vidi tipove ispod |
| title | String | Naslov notifikacije | Da  | Prikazuje se u listi |
| body | String | Tekst notifikacije | Da  | Kratki opis događaja |
| referenceType | String | Tip povezanog entiteta | Ne  | `listing`, `promotion`, `thread`, `system` |
| referenceId | String | ID povezanog entiteta | Ne  | Za navigaciju pri kliku |
| isRead | Boolean | Da li je pročitana | Da  | Default: false |
| readAt | DateTime | Kad je pročitana | Ne  | —   |
| channel | Enum | Koji kanal je korišten | Da  | `in_app`, `email`, `push` |
| sentAt | DateTime | Kad je poslana | Da  | —   |
| createdAt | DateTime | Kad je kreirana | Da  | —   |

> 📝 Lista atributa nije konačna i može se proširivati prema potrebama sistema. Za email notifikacije, `channel = email` i notifikacija služi kao log zapis (korisnik ne vidi u in-app listi). In-app notifikacije (`channel = in_app`) su vidljive u korisnikovom profilu.
#### Tipovi notifikacija (type)

| Tip | Opis | Tipični referenceType |
| --- | --- | --- |
| `listing_approved` | Listing odobren | `listing` |
| `listing_rejected` | Listing odbijen | `listing` |
| `listing_changes_requested` | Potrebne izmjene | `listing` |
| `new_message` | Nova poruka od moderatora | `thread` |
| `promotion_expiring` | Promocija uskoro ističe | `promotion` |
| `promotion_expired` | Promocija istekla | `promotion` |
| `verification_approved` | Verifikacija uspješna | `listing` |
| `trust_tier_changed` | Promjena Trust Tier-a | —   |
| `changes_timeout_reminder` | Podsjetnik za `changes_requested` timeout | `listing` |
| `system_announcement` | Sistemska obavijest | —   |

> **💡 Praktična napomena:** Badge sa brojem nepročitanih notifikacija se računa kao `COUNT WHERE isRead = false AND channel = 'in_app'`. Email notifikacije ne ulaze u badge jer korisnik ih vidi u inboxu.
### 7.2.4 Korisničke preference

> ⏳ **Faza 2:** Korisničke preference notifikacija nisu dio MVP-a. U MVP-u, sistem koristi default konfiguraciju za sve korisnike. Sekcija ispod opisuje planirani dizajn za Fazu 2.

Svaki korisnik će moći podesiti:

- Koje tipove notifikacija želi primati
- Kojim kanalima (email, push, in-app)
- Frekvenciju digest emailova (dnevno, sedmično, nikad)
- "Quiet hours" — periode kad ne želi push notifikacije

**Praktična napomena:** Sistem pamti kada je notifikacija poslata i pročitana, omogućavajući analitiku o efektivnosti komunikacije i izbjegavanje duplikata.
### 7.2.5 Email template-i

Email notifikacije koriste predefinisane template-e koji osiguravaju konzistentan branding i jasnu komunikaciju. Template-i su lokalizirani i prilagođeni kontekstu tenanta (podržavaju primarni i sekundarni jezik).

Tipične kategorije template-a:

- **Transakcijski** — Potvrde akcija, promjene statusa (`approved`, `removed (rejected)`, `changes_requested`)
- **Moderacijski** — Komunikacija vezana za sadržaj, verifikacija
- **Promotivni** — Informacije o promocijama i ponudama
- **Sistemski** — Tehnička obavještenja, sigurnosne informacije
### 7.2.6 Notifikacije vezane za Trust Tier

Sistem notifikacija je svjestan Trust Tier sistema i prilagođava komunikaciju:

| Trust Tier | Notifikacije o moderaciji |
| --- | --- |
| **Tier 0-1** (pre-moderacija) | Obavijest o čekanju na pregled, odobrenju/odbijanju |
| **Tier 2-4** (post-moderacija) | Obavijest samo ako moderator pronađe problem naknadno |

Za korisnike koji napreduju u viši tier, sistem šalje obavijest o novom statusu s objašnjenjem šta to znači za njihovo iskustvo.

* * *
## 7.3 Support sistem

> ⏳ **Faza 3:** Support sistem sa ticket-based podrškom, SLA tracking-om i satisfaction rating-om planiran je za Fazu 3 (skaliranje). Sekcija ispod opisuje planirani dizajn. U MVP-u, korisnička podrška se pruža kroz direktnu email komunikaciju.
### 7.3.1 Šta je Support sistem

Dok Message sistem služi za komunikaciju vezanu za specifičan listing, Support sistem je tu za sve ostalo — opća pitanja, tehnički problemi, žalbe, prijedlozi. Ovo je klasičan ticket-based support sistem prilagođen potrebama CityInfo platforme.

Filozofija support sistema je jednostavna: **user-first**. Svaki upit zaslužuje brz i koristan odgovor, jasnu komunikaciju o statusu i praćenje do rješenja.
### 7.3.2 Support kanali

```
graph LR
    A[Korisnik] --> B{Kanal}
    B --> C[In-app forma]
    B --> D[Email]
    C --> E[Ticket sistem]
    D --> E
    E --> F[Agent]
```

Korisnici mogu kontaktirati podršku kroz in-app formu ili direktno emailom. Oba kanala završavaju u istom ticket sistemu, osiguravajući konzistentan tretman.

**Praktična napomena:** Prije nego što korisnik otvori ticket, sistem mu nudi relevantne FAQ članke bazirane na ključnim riječima. Mnogi problemi se riješe bez potrebe za human interakcijom.
### 7.3.3 SupportTicket entitet

Ticket predstavlja jedan korisnički upit od otvaranja do zatvaranja.

| Atribut | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| ticketId | String | Jedinstveni identifikator | Da  | —   |
| ticketNumber | String | Broj čitljiv korisniku | Da  | Npr. "TKT-2025-00142" |
| userId | String | ID registrovanog korisnika | Ne  | Može biti NULL za anonimne |
| email | String | Email kontakt | Da  | —   |
| category | Enum | Kategorija problema | Da  | —   |
| subcategory | String | Podkategorija | Ne  | —   |
| subject | String | Naslov ticketa | Da  | —   |
| description | String | Opis problema | Da  | —   |
| status | Enum | Status ticketa | Da  | —   |
| priority | Enum | Prioritet | Da  | —   |
| assignedTo | String | Dodijeljeni agent | Ne  | —   |
| resolution | String | Opis rješenja | Ne  | Popunjava se pri zatvaranju |
| satisfactionRating | Number | Ocjena korisnika (1-5) | Ne  | —   |
| createdAt | DateTime | Vrijeme kreiranja | Da  | —   |
| firstResponseAt | DateTime | Vrijeme prvog odgovora | Ne  | Za SLA tracking |
| resolvedAt | DateTime | Vrijeme rješenja | Ne  | —   |
| closedAt | DateTime | Vrijeme zatvaranja | Ne  | —   |

> 📝 Lista atributa nije konačna i može se proširivati prema potrebama sistema.
#### Ticket statusi

```
stateDiagram-v2
    [*] --> new: Korisnik kreira
    new --> assigned: Dodijeljen agentu
    assigned --> in_progress: Agent radi
    in_progress --> waiting_customer: Potrebne dodatne informacije
    in_progress --> resolved: Rješenje pronađeno
    waiting_customer --> in_progress: Korisnik odgovorio
    resolved --> closed: Potvrđeno / timeout
    closed --> reopened: Korisnik ponovo otvara
    reopened --> in_progress: Nastavak rada
```
### 7.3.4 Kategorije i prioriteti
#### Kategorije ticketa

| Kategorija | Tipični problemi | Početni prioritet |
| --- | --- | --- |
| `account` | Prijava, verifikacija, postavke | Normal |
| `listing` | Kreiranje, uređivanje, moderacija | Normal |
| `payment` | Krediti, refund, fakture | High |
| `technical` | Bugovi, greške, performanse | High |
| `content` | Neprimjeren sadržaj, copyright | Urgent |
| `feature` | Prijedlozi, feedback | Low |
| `other` | Ostalo | Normal |
#### Prioriteti

| Prioritet | Opis | Ciljni response time | Ciljno rješenje |
| --- | --- | --- | --- |
| `urgent` | Blokira korištenje sistema | 30 minuta | 4 sata |
| `high` | Ozbiljan problem | 2 sata | 24 sata |
| `normal` | Standardni zahtjev | 4 sata | 48 sati |
| `low` | Pitanje ili prijedlog | 24 sata | 7 dana |

**Praktična napomena:** Prioritet se automatski kalkuliše na osnovu kategorije i sadržaja ticketa, ali agent ga može ručno promijeniti ako procijeni drugačije.
### 7.3.5 Eskalacija

Kada ticket ne napreduje očekivanom brzinom ili zahtijeva veće ovlasti, sistem ga eskalira na viši nivo.

| Nivo | Ko  | Kada | Ovlasti |
| --- | --- | --- | --- |
| L1  | Support Agent | Prvi kontakt | Osnovni problemi |
| L2  | Senior Agent | Složeni slučajevi | Napredne akcije |
| L3  | Team Lead | Eskalacije, SLA breach | Većina akcija |
| L4  | Management | Kritični slučajevi | Sve, uključujući refund |
#### Automatski eskalacijski triggeri

- SLA breach na 50% — upozorenje agentu i team leadu
- SLA breach na 80% — pre-eskalacija na L2
- SLA breach na 100% — automatska eskalacija
- 3+ razmjene bez rješenja — review od strane seniora
### 7.3.6 TicketMessage entitet

Poruke unutar ticketa — od korisnika, agenta ili sistema.

| Atribut | Tip | Opis | Obavezno | Napomena |
| --- | --- | --- | --- | --- |
| messageId | String | Jedinstveni identifikator | Da  | —   |
| ticketId | String | ID ticketa | Da  | —   |
| senderId | String | ID pošiljaoca | Ne  | NULL za anonimne |
| senderType | Enum | Tip pošiljaoca | Da  | `customer`, `agent`, `system` |
| messageText | String | Tekst poruke | Da  | —   |
| isInternal | Boolean | Interna napomena | Da  | Vidljivo samo agentima |
| createdAt | DateTime | Vrijeme slanja | Da  | —   |

> 📝 Lista atributa nije konačna i može se proširivati prema potrebama sistema.

**Praktična napomena:** Interne napomene (`isInternal: true`) služe za komunikaciju između agenata i nisu vidljive korisniku. Korisne su za bilješke pri primopredaji ticketa ili eskalaciji.
### 7.3.7 SLA i metrike
#### Ključne metrike

| Metrika | Formula | Cilj |
| --- | --- | --- |
| First Response Time | Prosjek (firstResponseAt - createdAt) | < 2 sata |
| Resolution Time | Prosjek (resolvedAt - createdAt) | < 24 sata |
| SLA Compliance | (Zadovoljeni SLA / Ukupno) × 100% | 95% |
| Customer Satisfaction | Prosjek ocjena | 4.0 / 5.0 |
| Escalation Rate | (Eskalirani / Ukupno) × 100% | < 10% |

**Praktična napomena:** Ove metrike se prate na nivou agenta, tima i cijelog sistema. Koriste se za identifikaciju uskih grla, potreba za obukom i poboljšanje procesa.

* * *
## 7.4 API Endpoints

Ova sekcija navodi ključne API endpoint-e za komunikacijski modul. Endpoint-i su grupisani po funkcionalnosti i opisani na konceptualnom nivou.

> ⚠️ **Napomena:** Ovo nije kompletna API specifikacija. Za detalje o autentifikaciji, autorizaciji i error handling-u, pogledati odvojenu API dokumentaciju.
### 7.4.1 Message sistem

| Metoda | Putanja | Opis |
| --- | --- | --- |
| `GET` | `/listings/{listingId}/thread` | Dohvati thread za listing |
| `GET` | `/threads/{threadId}` | Detalji thread-a |
| `PATCH` | `/threads/{threadId}` | Ažuriranje thread-a (npr. assign, status) |
| `GET` | `/threads/{threadId}/messages` | Poruke u thread-u |
| `POST` | `/threads/{threadId}/messages` | Slanje nove poruke |

**Osnovni request/response shape za slanje poruke:**

```
POST /threads/{threadId}/messages
Request: { messageText, documentIds? }
Response: { messageId, threadId, sentAt, newThreadStatus }
```

> 📝 **Napomena o dokumentima:** API endpointi za upload i upravljanje dokumentima listinga (ListingDocument) definisani su u [04 - Sadržaj, sekcija 4.10](../project-specs/04-sadrzaj.md). Poruke samo referenciraju postojeće dokumente kroz `documentIds` polje.
### 7.4.2 Notifikacije

| Metoda | Putanja | Opis |
| --- | --- | --- |
| `GET` | `/notifications` | Lista notifikacija korisnika (paginirano) |
| `GET` | `/notifications/unread-count` | Broj nepročitanih |
| `PATCH` | `/notifications/{notificationId}` | Označavanje kao pročitano |
| `POST` | `/notifications/mark-all-read` | Označavanje svih kao pročitano |
| `GET` | `/notification-preferences` | Korisničke preference (Faza 2) |
| `PUT` | `/notification-preferences` | Ažuriranje preferenci (Faza 2) |
### 7.4.3 Support sistem (Faza 3)

> ⏳ Endpointi ispod su planirani za Fazu 3.

| Metoda | Putanja | Opis |
| --- | --- | --- |
| `GET` | `/tickets` | Lista ticketa (s filtrima) |
| `GET` | `/tickets/{ticketId}` | Detalji ticketa |
| `POST` | `/tickets` | Kreiranje novog ticketa |
| `PATCH` | `/tickets/{ticketId}` | Ažuriranje ticketa |
| `GET` | `/tickets/{ticketId}/messages` | Poruke u ticketu |
| `POST` | `/tickets/{ticketId}/messages` | Slanje poruke |
| `POST` | `/tickets/{ticketId}/rate` | Ocjena zadovoljstva |

**Osnovni request/response shape za kreiranje ticketa:**

```
POST /tickets
Request: { email, category, subject, description }
Response: { ticketId, ticketNumber, status, createdAt }
```

* * *
## Sažetak

| Sistem | Svrha | Ko koristi | MVP status |
| --- | --- | --- | --- |
| **Message sistem** | Komunikacija vezana za listing | Moderatori ↔ Vlasnici listinga | ✅ MVP |
| **Notifikacije** | Obavještenja o događajima | Svi korisnici | ✅ MVP (base) |
| **Support sistem** | Opća podrška | Svi korisnici ↔ Support tim | ⏳ Faza 3 |

Ključne karakteristike:

- **Jedan thread po listingu** — thread postoji dok postoji listing, nema zatvaranja/otvaranja
- **Centralizirani dokumenti** — ListingDocument entitet definisan u [04 - Sadržaj](../project-specs/04-sadrzaj.md), poruke samo referenciraju
- **Pojednostavljen statusni model** — `idle`, `waiting_owner`, `waiting_moderator`
- **Statusni model kontroliše pristup** — ko može slati poruke zavisi od statusa thread-a (sekcija 7.1.4)
- **Notification entitet** — svaka in-app notifikacija je zapis sa tipom, referencom i statusom čitanja

Komunikacijski sistemi su dizajnirani da budu dovoljno fleksibilni za različite scenarije, ali dovoljno strukturirani da osiguraju kvalitetu i dosljednost.

* * *
## Changelog

| Verzija | Datum | Opis |
| --- | --- | --- |
| 1.5 | 3.4.2026 | **Optimizacija 13→12 statusa.** Reference ažurirane prema novom modelu. |
| 1.4 | 28.3.2026 | Status → Završeno. |
| 1.3 | Mart 2026 | Dodan Notification entitet (7.2.3) sa atributima i tipovima notifikacija. Sekcija 7.1.7 skraćena (SSoT referenca na Ch.04). Referenca na dokument API ispravljena na 4.10. Sekcije renumerisane. |
| 1.2 | Mart 2026 | ListingDocument uklonjen (SSoT u poglavlju 04). Support sistem označen kao Faza 3. Notification preferences označene kao Faza 2. |