# 08 - INFRASTRUKTURA

> **Verzija:** 2.3  
> **Datum:** 1.4.2026  
> **Status:** Završeno ✅

* * *

<a id="o-čemu-je-riječ"></a>

## O čemu je riječ?

Ovaj dokument opisuje tehničku infrastrukturu koja omogućava rad CityInfo platforme. Fokus je na konceptima i principima koji su bitni za razumijevanje sistema, a ne na implementacijskim detaljima koji su ionako podložni čestim promjenama. Ako radiš na backendu ili ops poslovima, ovdje ćeš naći pregled ključnih komponenti — od multi-tenant arhitekture i izolacije podataka, preko audit sistema i automatskih procesa, do eksternih integracija koje platforma koristi.

* * *

<a id="81-multi-tenant-arhitektura"></a>

## 8.1 Multi-tenant arhitektura

<a id="šta-je-tenant-i-zašto-nam-treba"></a>

### Šta je tenant i zašto nam treba?

CityInfo je od samog početka dizajniran kao multi-tenant sistem. Svaki grad (Sarajevo, Zagreb, Ljubljana…) predstavlja zaseban "tenant" — logički i fizički odvojen prostor sa svojim korisnicima, sadržajem i konfiguracijom. Ovakav pristup omogućava da jedan deployment aplikacije služi više gradova, bez potrebe za zasebnim instancama za svaki grad. Dodavanje novog grada je stvar konfiguracije, ne novog deploya.

```
CityInfo Platforma
├── Sarajevo Tenant (sarajevo.cityinfo.ba)
│   └── Vlastita baza, korisnici, sadržaj, konfiguracija
├── Zagreb Tenant (zagreb.cityinfo.hr)
│   └── Vlastita baza, korisnici, sadržaj, konfiguracija
├── Ljubljana Tenant (ljubljana.cityinfo.si)
│   └── Vlastita baza, korisnici, sadržaj, konfiguracija
└── ... (novi gradovi se dodaju bez promjene koda)
```

**Praktična napomena:** Cijene kredita, promocija, pa čak i neka pravila moderacije mogu varirati po tenantima. Ovo nije hardkodirano — lokalni administratori imaju fleksibilnost prilagodbe svog tržišta.

* * *

<a id="811-database-izolacija"></a>

### 8.1.1 Database izolacija

Jedna od ključnih arhitektonskih odluka je potpuna separacija baza podataka. Sistem koristi dvije vrste baza:

| Tip baze | Šta sadrži | Ko pristupa | Primjer |
| --- | --- | --- | --- |
| **Master baza** | GlobalAdmin nalozi, TenantRegistry, globalna konfiguracija | Samo GlobalAdmin sistem | `cityinfo_master_db` |
| **Tenant baza** | User, Staff, Events, Places, transakcije, poruke | User i Staff sistemi za taj tenant | `sarajevo_db`, `zagreb_db` |

Ovakva separacija znači da:

- Kompromitovanje jednog tenanta ne ugrožava podatke drugih gradova
- Svaki grad može rasti nezavisno bez uticaja na performanse drugih
- GDPR zahtjevi se lakše ispunjavaju jer su podaci fizički odvojeni
- Backup i restore se mogu raditi per-tenant

```
┌─────────────────────────────────────────────────────────────────┐
│                        MASTER BAZA                              │
│  • GlobalAdmin nalozi                                           │
│  • TenantRegistry (lista svih gradova)                         │
│  • Globalna konfiguracija                                       │
└─────────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  SARAJEVO DB    │  │   ZAGREB DB     │  │  LJUBLJANA DB   │
│  • Users        │  │  • Users        │  │  • Users        │
│  • Staff        │  │  • Staff        │  │  • Staff        │
│  • Events       │  │  • Events       │  │  • Events       │
│  • Places       │  │  • Places       │  │  • Places       │
│  • Transactions │  │  • Transactions │  │  • Transactions │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

**Praktična napomena:** GlobalAdmin nikada ne pristupa direktno tenant bazama za čitanje korisničkih podataka. Sva komunikacija ide kroz definirane API-je, što održava jasnu separaciju odgovornosti.

* * *

<a id="812-tenant-registry"></a>

### 8.1.2 Tenant Registry

TenantRegistry je centralna tabela u master bazi koja drži informacije o svim aktivnim gradovima. Ovo je "izvor istine" za sve što se tiče konfiguracije tenanta.

| Atribut | Tip | Opis | Napomena |
| --- | --- | --- | --- |
| tenantId | String | Jedinstveni identifikator | Koristi se interno |
| name | String | Naziv grada | Za prikaz korisnicima |
| domain | String | Primarna domena | Npr. `sarajevo.cityinfo.ba` |
| databaseConnection | String | Connection info | Enkriptovano |
| primaryLanguage | String | Primarni jezik | ISO kod |
| secondaryLanguage | String | Sekundarni jezik | Opciono |
| timezone | String | Vremenska zona | Za cron jobove |
| currency | String | Valuta | Za monetizaciju |
| isActive | Boolean | Da li je tenant aktivan | Za maintenance mode |
| configOverrides | Object | Tenant-specifične postavke | JSON format |
| createdAt | DateTime | Datum kreiranja | Auto |

> ⚠️ Lista atributa nije konačna i može se proširivati prema potrebama sistema.

**Praktična napomena:** Kad se kreira novi tenant, GlobalAdmin koristi wizard koji automatski postavlja bazu, inicijalne kategorije, default cijene i prvog local\_admin-a.

* * *

<a id="813-cross-tenant-operacije"></a>

### 8.1.3 Cross-tenant operacije

Iako su tenanti izolovani, postoje situacije kada je potrebna komunikacija ili agregacija podataka:

| Operacija | Ko izvršava | Kako | Primjer |
| --- | --- | --- | --- |
| **Kreiranje tenanta** | GlobalAdmin | Master API | Novi grad |
| **Health monitoring** | GlobalAdmin | Read-only queries | Dashboard |
| **Globalni izvještaji** | GlobalAdmin | Agregacija | Ukupan promet |
| **Backup** | Sistem | Direct DB access | Scheduled |
| **Disaster recovery** | GlobalAdmin | Restore procedure | Emergency |

**Važno:** Ne postoji mehanizam za "dijeljenje" sadržaja između tenanta. Event kreiran u Sarajevu ne može se prikazati u Zagrebu. Ovo je namjerna odluka radi jednostavnosti i jasne separacije.

* * *

<a id="82-audit-i-logging"></a>

## 8.2 Audit i logging

<a id="zašto-logujemo-sve"></a>

### Zašto logujemo sve?

Audit sistem je kičma operativne sigurnosti platforme. Bez njega, ne bismo mogli odgovoriti na pitanja poput "ko je blokirao ovog korisnika?" ili "kada je promijenjena cijena promocije?". Osim operativnih potreba, audit logovi su i pravni zahtjev — GDPR i lokalni zakoni traže da možemo rekonstruisati istoriju pristupa podacima.

* * *

<a id="821-šta-se-loguje-po-sistemima"></a>

### 8.2.1 Šta se loguje po sistemima

CityInfo koristi tri nivoa logovanja, prilagođena tipu korisnika i osjetljivosti akcija:

| Sistem | Šta se loguje | Nivo detalja | Retention |
| --- | --- | --- | --- |
| **User** | Login, kreiranje sadržaja, transakcije | IP, user agent, success/fail | 90 dana |
| **Staff** | Sve akcije nad podacima | Full request/response, before/after | 1 godina |
| **GlobalAdmin** | Apsolutno sve | Command history, network info | 7 godina |

Razlog za različite retention periode je praktičan:

- User logovi su volumenom najveći, ali pojedinačno manje kritični
- Staff logovi su ključni za razumijevanje moderacijskih odluka
- GlobalAdmin logovi su nepromjenjivi (immutable) jer dokumentuju kritične sistemske promjene

**Praktična napomena:** Audit logovi se automatski anonimiziraju nakon isteka retention perioda — IP adrese i lični podaci se uklanjaju, ali statistički podaci ostaju za analizu.

* * *

<a id="822-struktura-audit-loga"></a>

### 8.2.2 Struktura audit loga

Svaki audit zapis ima konzistentnu strukturu koja omogućava lako pretraživanje i analizu:

| Polje | Tip | Opis | Primjer |
| --- | --- | --- | --- |
| timestamp | DateTime | Vrijeme akcije | `2025-01-31T10:30:45.123Z` |
| actorId | String | ID korisnika koji izvršava | UUID |
| actorType | Enum | Tip aktera | `user`, `staff`, `globaladmin`, `system` |
| action | String | Šta je urađeno | `user.block`, `listing.approve` |
| targetId | String | ID entiteta nad kojim se djeluje | UUID |
| targetType | String | Tip entiteta | `user`, `listing`, `transaction` |
| ipAddress | String | IP adresa | Hash za User, plain za Staff |
| sessionId | String | Session identifikator | Za grupiranje akcija |
| changes | Object | Before/after vrijednosti | JSON diff |
| metadata | Object | Dodatni kontekst | Razlog, trajanje, itd. |

**Primjer audit zapisa:**

```
Akcija: Moderator blokira korisnika
─────────────────────────────────
timestamp: 2025-01-31T10:30:45Z
actorType: staff
action: user.block
changes: { before: {accessStatus: "allowed"}, after: {accessStatus: "blocked"} }
metadata: { reason: "SPAM_CONTENT", duration: "7d" }
```

* * *

<a id="823-compliance-zahtjevi"></a>

### 8.2.3 Compliance zahtjevi

Audit sistem je dizajniran da zadovolji više regulatornih okvira:

| Standard | Zahtjev | Kako ispunjavamo |
| --- | --- | --- |
| **GDPR** | Pravo na pristup, brisanje | Export funkcija, anonimizacija |
| **Lokalni zakoni** | Čuvanje poslovne dokumentacije | Retention politike |
| **PCI DSS** | Audit trail za payment operacije | Detaljno logovanje transakcija |

**Praktična napomena:** Kad korisnik zatraži GDPR export, sistem automatski generiše paket svih podataka vezanih za tog korisnika, uključujući audit logove (sa redaktovanim podacima trećih strana).

* * *

<a id="83-background-procesi"></a>

## 8.3 Background procesi

<a id="zašto-automatizacija"></a>

### Zašto automatizacija?

Platforma se oslanja na niz automatskih procesa koji održavaju sistem zdravim, čiste zastarjele podatke i osiguravaju konzistentnost. Bez ovih jobova, moderatori bi morali ručno pratiti istekle promocije, a baza bi rasla neograničeno.

* * *

<a id="831-scheduled-jobovi"></a>

### 8.3.1 Scheduled jobovi

Ovo su regularni procesi koji se izvršavaju po rasporedu:

| Job | Učestalost | Šta radi | Kritičnost |
| --- | --- | --- | --- |
| **ExpiredEventProcessor** | Svakih 15 min | Pronalazi evente čiji je `endDateTime` prošao i prebacuje ih u `expired` status. Places nemaju automatsko istjecanje. | Visoka |
| **PendingSubmissionReminder** | Dnevno, 9:00 | Šalje reminder za sadržaj na čekanju >24h | Srednja |
| **PromotionExpiryHandler** | Svakih 5 min | Deaktivira istekle promocije, ističe pauzirane preko `PROMO_MAX_PAUSE_DAYS` | Visoka |
| **AutoRenewProcessor** | Svakih 5 min | Osvježava `sortDate` za listinge sa aktivnim AutoRenew-om čiji `nextAutoRenewAt` je prošao. Ažurira `nextAutoRenewAt` za sljedeći ciklus i inkrementira `autoRenewsCompleted`. | Visoka |
| **ChangesRequestedTimeoutChecker** | Dnevno, 10:00 | Provjerava listinge u `changes_requested` statusu. Šalje reminder na `CHANGES_REQUESTED_REMINDER_DAYS` dana prije isteka. Nakon `CHANGES_REQUESTED_TIMEOUT_DAYS` dana bez odgovora, listing automatski prelazi u `rejected` status. | Srednja |
| **CreditExpiryProcessor** | Dnevno, 00:00 | Procesira istekle kredite (ako je konfigurisano) | Srednja |
| **TrustScoreRecalculator** | Sedmično | Recalculates trust scores bazirano na aktivnosti | Niska |
| **AuditLogArchiver** | Dnevno, 02:00 | Arhivira stare audit logove | Srednja |
| **ImageCleanup** | Dnevno, 03:00 | Briše slike orphan listinga | Niska |
| **DigestEmailSender** | Sedmično, ponedjeljak 10:00 | Šalje weekly digest korisnicima | Srednja |

**Retry logika:** Svi kritični jobovi imaju automatski retry (3 pokušaja sa exponential backoff). Ako job i dalje pada, šalje se alert ops timu.

**Praktična napomena:** Jobovi se mogu manualno pokrenuti kroz admin panel u slučaju potrebe (npr. ako se desila greška i treba ponovo procesirati).

* * *

<a id="832-event-driven-procesi"></a>

### 8.3.2 Event-driven procesi

Pored scheduled jobova, postoje i procesi koji se pokreću kao reakcija na događaje u sistemu:

| Trigger | Proces | Rezultat |
| --- | --- | --- |
| Novi listing submission | AI Content Screening | Slika se provjerava, listing ide u queue |
| Listing approved | Notification sender | Korisnik dobija email/in-app notifikaciju |
| User blocked | Session invalidator + Content remover + Promo canceller | Sve aktivne sesije se terminiraju. Ako je odabrana opcija uklanjanja sadržaja, svi javno vidljivi listinzi prelaze u `removed` sa `removedReason = owner_blocked`. Aktivne promocije se otkazuju. |
| Payment callback | Credit processor | Krediti se dodaju na wallet |
| Trust level change | Permission updater + Notification sender | Ažuriraju se dozvole korisnika, korisnik se obavještava |
| Promotion paused/resumed | AutoRenew controller | Suspenduje ili reaktivira AutoRenew za tu promociju |

> **📌 Praktična napomena:** U starom modelu postojao je "User unblocked → Listing reactivator" proces koji je automatski reaktivirao listinge pri odblokiranju. U novom jednostatus modelu, `removed` je terminalni status pa automatska reaktivacija nije moguća. Ako se korisnik odblokira, moderator donosi odluku o sadržaju na osnovu konkretne situacije.

**Praktična napomena:** Event-driven arhitektura omogućava loose coupling — komponente ne moraju znati jedna za drugu, samo "reaguju" na događaje.

* * *

<a id="833-monitoring-jobova"></a>

### 8.3.3 Monitoring jobova

Svaki job ima svoj health status koji se može pratiti:

| Status | Značenje | Akcija |
| --- | --- | --- |
| ✅ **Healthy** | Zadnje izvršavanje uspješno | Ništa |
| ⚠️ **Warning** | Zadnje izvršavanje sporo ili djelimično | Provjeri logove |
| ❌ **Failed** | Zadnje izvršavanje neuspješno | Intervencija potrebna |
| ⏸️ **Paused** | Job manualno pauziran | Očekivano |

**Praktična napomena:** Dashboard prikazuje agregiran health svih jobova. Ako bilo koji job uđe u Failed stanje, ops tim dobija alert.

* * *

<a id="84-eksterne-integracije"></a>

## 8.4 Eksterne integracije

<a id="princip-best-of-breed"></a>

### Princip "best of breed"

CityInfo ne pokušava reinventirati točak. Za funkcionalnosti koje nisu core business (plaćanja, email, storage…), koristimo provjerene eksterne servise. Ovo ubrzava development i smanjuje održavanje, a arhitektura je dizajnirana da servisi budu zamjenjivi ako se ukaže potreba.

* * *

<a id="841-payment-gateway"></a>

### 8.4.1 Payment gateway

Monetizacija (kupovina kredita) prolazi kroz eksterni payment gateway.

| Aspekt | Detalji |
| --- | --- |
| **Integracija** | Server-side, redirect flow |
| **Flow** | User → Naš sistem → Gateway → Banka → Callback → Krediti |
| **Podržane metode** | Kartice, PayPal, bankarski transfer (zavisi od tenanta) |
| **Sigurnost** | PCI DSS compliant, tokenizirani podaci |

**Praktična napomena:** Gateway je zamjenjiv — sistem je dizajniran da može raditi sa različitim providerima. Konkretni provider može varirati po tržištima.

<a id="842-email-servis"></a>

### 8.4.2 Email servis

Platforma šalje značajan broj email-ova — od verifikacija i notifikacija do digest sumarizacija.

| Tip emaila | Trigger | Primjer |
| --- | --- | --- |
| **Transakcijski** | Sistemski event | Potvrda registracije, reset lozinke |
| **Notifikacijski** | Akcija na platformi | "Vaš sadržaj je odobren" |
| **Digest** | Scheduled job | Sedmični pregled aktivnosti |
| **Marketing** | Manualno/kampanja | Novi features, promocije |

<a id="843-push-notification-servis"></a>

### 8.4.3 Push notification servis

Za mobilne korisnike, platforma podržava push notifikacije (Faza 2).

<a id="844-storage-servis"></a>

### 8.4.4 Storage servis

Slike i dokumenti se čuvaju u eksternom cloud storage servisu sa CDN-om za brzo učitavanje.

<a id="845-ai-content-screening"></a>

### 8.4.5 AI Content Screening

Slike koje korisnici uploaduju prolaze kroz automatsku provjeru sadržaja putem eksternih AI servisa. Detalji o scoring komponentama i blocking logici u [05 - Moderacija, sekcija 5.3](../project-specs/05-moderacija.md).

<a id="846-virus-scanning"></a>

### 8.4.6 Virus Scanning

Dokumenti koji se uploaduju prolaze kroz virus scan. Detalji o workflow-u u [04 - Sadržaj, sekcija 4.7](../project-specs/04-sadrzaj.md).

* * *

<a id="85-technology-stack-pregled"></a>

## 8.5 Technology Stack (pregled)

<a id="odlučeni-stack"></a>

### Odlučeni stack

CityInfo koristi jasno definisan technology stack koji balansira performanse, ecosystem i dostupnost developera na lokalnom tržištu. Izbor je finaliziran i ovdje je konceptualni pregled. Za operativne detalje (konkretne verzije, environment varijable, deployment procedure), pogledaj odvojene ops dokumente.

| Komponenta | Tehnologija | Zašto |
| --- | --- | --- |
| **Backend runtime** | .NET 8 (C#, [ASP.NET](http://ASP.NET) Core) | Odličan za enterprise sisteme, jak typing, brz razvoj API-ja, širok ecosystem biblioteka |
| **API stil** | RESTful sa JSON | Jednostavnost, široka kompatibilnost, dobra tooling podrška |
| **Baza podataka** | MS SQL Server | ACID garancije, kompleksni upiti, provedena ekspertiza u timu |
| **Frontend** | Svelte 5 + SvelteKit | Reaktivan, kompaktan output, brz development, server-side rendering |
| **UI framework** | TailwindCSS + Flowbite | Utility-first CSS, gotov design system, konzistentan UI |
| **Asinhrone operacije** | Background services (.NET) | Hosted services za scheduled jobove, event-driven procesiranje |

**Tri odvojena frontend sistema:**

| Sistem | URL | Stack |
| --- | --- | --- |
| **User app** | [cityinfo.ba](http://cityinfo.ba) | SvelteKit + TailwindCSS + Flowbite |
| **Staff panel** | [admin.cityinfo.ba](http://admin.cityinfo.ba) | SvelteKit + TailwindCSS + Flowbite |
| **GlobalAdmin** | [master.cityinfo.ba](http://master.cityinfo.ba) | SvelteKit + TailwindCSS + Flowbite (MVP može biti minimalan) |

> **💡 Praktična napomena:** Svi frontend sistemi koriste isti stack i dijele komponentnu biblioteku, ali su zasebne SvelteKit aplikacije sa odvojenim routingom, autentifikacijom i API pozivima. Ovo odražava arhitekturu tri korisničke zone iz [01 - Uvod, sekcija 1.2](../project-specs/01-uvod-i-koncepti.md).

<a id="cache-i-pretraga"></a>

### Cache i pretraga

| Komponenta | Status | Namjena |
| --- | --- | --- |
| **Cache layer** | Može se dodati po potrebi | Sesije, česti upiti, rate limiting |
| **Search engine** | Opciono, po potrebi | Full-text pretraga ako SQL Server FTS ne bude dovoljan |

**Praktična napomena:** Cache nije "must have" za prvi release, ali značajno poboljšava performanse kad korisnika bude više. Dizajniraj API tako da se cache može dodati kasnije bez promjene interface-a.

<a id="cloud-infrastruktura"></a>

### Cloud infrastruktura

Platforma je dizajnirana za cloud deployment. Konkretni cloud provider nije vezan — arhitektura koristi standardne interface-e gdje god je moguće.

<a id="devops"></a>

### DevOps

| Kategorija | Pristup |
| --- | --- |
| **Containerization** | Docker za konzistentnost između okruženja |
| **CI/CD** | Automatski build, test, deploy pipeline |
| **Monitoring** | Centralizovane metrike, alerting, dashboards |
| **Logging** | Centralizovani logging za agregaciju i debug |
| **Error tracking** | Real-time error reporting |

<a id="reference-za-operativne-detalje"></a>

### Reference za operativne detalje

Za konkretne verzije, konfiguracije i deployment procedure, pogledaj:

| Dokument | Šta sadrži |
| --- | --- |
| `TECH-STACK.md` | Konkretne verzije svih komponenti |
| `DEPLOYMENT.md` | Deploy procedure, rollback planovi |
| `ENV-VARIABLES.md` | Sve environment varijable i njihovo značenje |
| `RUNBOOK.md` | Operativne procedure za incidente |

* * *

<a id="86-api-endpoints"></a>

## 8.6 API Endpoints

Infrastrukturne operacije su dostupne kroz nekoliko API endpoint-a. Većina je rezervisana za GlobalAdmin sistem, dok su neki dostupni i Staff korisnicima.

<a id="tenant-management"></a>

### Tenant Management

| Metoda | Endpoint | Opis |
| --- | --- | --- |
| `GET` | `/api/master/tenants` | Lista svih tenanta |
| `GET` | `/api/master/tenants/{id}` | Detalji tenanta |
| `POST` | `/api/master/tenants` | Kreiranje novog tenanta |
| `PUT` | `/api/master/tenants/{id}` | Ažuriranje konfiguracije |
| `POST` | `/api/master/tenants/{id}/activate` | Aktivacija tenanta |
| `POST` | `/api/master/tenants/{id}/deactivate` | Deaktivacija (maintenance) |

<a id="audit-logs"></a>

### Audit Logs

| Metoda | Endpoint | Opis |
| --- | --- | --- |
| `GET` | `/api/audit/logs` | Pretraga audit logova |
| `GET` | `/api/audit/logs/{id}` | Detalji log zapisa |
| `GET` | `/api/audit/user/{userId}` | Svi logovi za korisnika |
| `POST` | `/api/audit/export` | Export za GDPR zahtjeve |

<a id="background-jobs"></a>

### Background Jobs

| Metoda | Endpoint | Opis |
| --- | --- | --- |
| `GET` | `/api/jobs/status` | Status svih jobova |
| `POST` | `/api/jobs/{jobName}/trigger` | Manualno pokretanje |
| `GET` | `/api/jobs/{jobName}/history` | Istorija izvršavanja |

<a id="health-monitoring"></a>

### Health & Monitoring

| Metoda | Endpoint | Opis |
| --- | --- | --- |
| `GET` | `/api/health` | Osnovni health check |
| `GET` | `/api/health/detailed` | Detaljan status svih komponenti |
| `GET` | `/api/metrics` | Prometheus-compatible metrike |

* * *

<a id="zaključak"></a>

## Zaključak

Infrastruktura CityInfo platforme je dizajnirana sa nekoliko ključnih principa na umu:

- **Izolacija** — Tenanti su potpuno odvojeni, kako podacima tako i konfiguracijom
- **Transparentnost** — Sve akcije se loguju, ništa ne prolazi nezapaženo
- **Automatizacija** — Background jobovi održavaju sistem zdravim bez manualnih intervencija
- **Fleksibilnost** — Eksterni servisi su zamjenjivi, sistem nije vezan za konkretne providere
- **Pragmatičnost** — Tehnološki izbori su vođeni potrebama, ne trendovima

Ovaj dokument daje konceptualni pregled. Za implementacijske detalje, pogledaj relevantne tehničke specifikacije ili se obrati DevOps timu.

* * *

<a id="changelog"></a>

## Changelog

| Verzija | Datum | Opis |
| --- | --- | --- |
| 2.3 | 1.4.2026 | **MIGRACIJA — jednostatus model.** `ExpiredListingArchiver` preimenovan u `ExpiredEventProcessor` (samo eventi imaju automatski expired prelaz). `ChangesRequestedTimeoutChecker` ažuriran (listing prelazi u `rejected`, ne "zatvara se"). Event-driven "User blocked" ažuriran sa `removed` + `removedReason = owner_blocked`. Uklonjen "User unblocked → Listing reactivator" (jer je `removed` terminalan). Dodana napomena o moderatorskoj odluci pri odblokiranju. |
| 2.2 | 28.3.2026 | Status → Završeno. |
| 2.1 | Mart 2026 | Sekcija 8.5 konkretizirana — .NET 8 / MS SQL / Svelte 5 stack umjesto generičkog opisa. Dodani AutoRenewProcessor i ChangesRequestedTimeoutChecker u scheduled jobove (8.3.1). Event-driven procesi prošireni (User unblocked, Promotion paused/resumed). Sekcije 8.4.2-8.4.6 skraćene sa referencama na SSoT poglavlja. |
| 2.0 | Mart 2026 | Inicijalna verzija |