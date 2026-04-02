# Audit izvještaj — konzistentnost CityInfo dokumentacije

> **Datum:** 2.4.2026  
> **Autor:** Claude Code agent  
> **Scope:** Svih 10 markdown fajlova dokumentacije (Ch.01–Ch.08, statusni model specifikacija, MVP scope)

---

## Sažetak

| Severity | Broj nalaza |
|----------|-------------|
| **Critical** | 4 |
| **Minor** | 10 |
| **Info** | 5 |

---

## Critical nalazi

### C-01: .NET 8 umjesto .NET 10 (LTS) u Ch.08

**Lokacija:** `08-infrastruktura.md`, sekcija 8.5 "Technology Stack", linija 363

**Opis:** Tabela technology stacka navodi `.NET 8 (C#, ASP.NET Core)` kao backend runtime. Prema CLAUDE.md i projektnim odlukama, ispravan tech stack je **.NET 10 (LTS)**.

**Takođe:** Changelog zapis na liniji 500 referira na `.NET 8 / MS SQL / Svelte 5`, što perpetuira grešku.

**Preporuka:** Zamijeniti `.NET 8` sa `.NET 10 (LTS)` u tabeli technology stacka. Changelog ne treba mijenjati jer dokumentuje historijsku promjenu.

---

### C-02: Kontradikcija o efektu ručnog blokiranja korisnika na sadržaj (Ch.03 vs Ch.04/Ch.05)

**Lokacija:**
- `03-korisnici-i-pristup.md`, sekcija 3.7 "Efekt blokiranja na sadržaj korisnika", linije 588–593
- `04-sadrzaj.md`, sekcija 4.8, linije 1021–1024
- `05-moderacija.md`, sekcija 5.4.4 "Ručno blokiranje", linije 551–555

**Opis:** Tri poglavlja opisuju različito ponašanje **Opcije 2** pri ručnom blokiranju korisnika:

| Poglavlje | Opcija 2 ručnog blokiranja | Status listinga | Reverzibilno? |
|-----------|---------------------------|-----------------|---------------|
| **Ch.03** | "Listinzi se uklanjaju" | `removed` sa `removedReason = owner_blocked` | ❌ Terminalno |
| **Ch.04** | "Listinzi se sakrivaju" | `hidden_by_system` | ✅ Automatski pri odblokiranju |
| **Ch.05** | "Listinzi se sakrivaju" | `hidden_by_system` | ✅ Vraćaju se u `published` |

Ch.04 i Ch.05 su međusobno konzistentni (sakrivanje → `hidden_by_system`), ali Ch.03 tvrdi da je ovo terminalna akcija sa `removed` statusom. Ovo je fundamentalna kontradikcija — ili je akcija reverzibilna ili nije.

**Preporuka:** Uskladiti Ch.03 sa Ch.04/Ch.05. Opcija 2 ručnog blokiranja bi trebala koristiti `hidden_by_system` (reverzibilno), jer to je logičnija opcija za ručno blokiranje — moderator već ima mogućnost trajnog uklanjanja kao zasebnu opciju. Ch.03 bi također trebao dodati treću opciju za trajno uklanjanje (`removed` sa `owner_blocked`) ako je to namjerno ponašanje, ili ga ostaviti samo za instant/sistem blokiranje.

---

### C-03: Kontradikcija o timeout ishodu za `changes_requested` (Ch.04 vs Ch.05/Ch.08)

**Lokacija:**
- `04-sadrzaj.md`, sekcija 4.8, linije 1036–1037
- `05-moderacija.md`, BR-MOD-14, linija 1036
- `08-infrastruktura.md`, sekcija 8.3.1, ChangesRequestedTimeoutChecker, linija 234

**Opis:** Kada korisnik ne odgovori na `changes_requested` u zadanom roku:

| Poglavlje | Ishod timeout-a |
|-----------|-----------------|
| **Ch.04** | Listing prelazi u `removed` sa `removedReason = inappropriate` |
| **Ch.05 (BR-MOD-14)** | Listing prelazi u `rejected` |
| **Ch.08** | Listing prelazi u `rejected` |

Ch.05 i Ch.08 su konzistentni (`rejected`), ali Ch.04 kaže `removed`. Ovo je bitna razlika jer `rejected` i `removed` su oba terminalna, ali imaju različitu semantiku — `rejected` znači "sadržaj nije prihvaćen", dok `removed` sa `inappropriate` znači "trajno uklonjeno zbog kršenja pravila".

**Preporuka:** Uskladiti Ch.04 sa Ch.05/Ch.08 — timeout bi trebao rezultirati u `rejected` status jer korisnik nije odgovorio, a ne `removed` koji implicira aktivno kršenje pravila. Ažurirati liniju 1036–1037 u `04-sadrzaj.md`.

---

### C-04: Stari termin `lifecycleStatus` u epics-stories-instructions.md

**Lokacija:** `cityinfo-epics-stories-instructions.md`, linija 83

**Opis:** Fajl navodi `lifecycleStatus` kao primjer tehničkog termina koji se ne prevodi:
```
lifecycleStatus, sortDate, Trust Tier, endpoint — ne prevodi ih
```

Ovaj termin je zamijenjen sa `listingStatus` u novom jednostatus modelu. Instrukcijski fajl za pisanje epica i storija ne bi smio navoditi depreciran termin kao primjer, jer će autori epica koristiti pogrešnu terminologiju.

**Preporuka:** Zamijeniti `lifecycleStatus` sa `listingStatus` u listi primjera.

---

## Minor nalazi

### M-01: Pogrešne cross-reference na sekcije Ch.03 u MVP scope dokumentu

**Lokacija:** `mvp-scope-opseg-prve-verzije.md`, linije 53–56, 136

**Opis:** Četiri reference na poglavlje 03 pokazuju na pogrešne sekcije:

| Funkcionalnost | Navedena referenca | Stvarna sekcija |
|---------------|-------------------|-----------------|
| User registracija | 03 - Korisnici **(3.2)** | **3.3** (User entitet) — sekcija 3.2 je "Visitors" |
| Staff panel | 03 - Korisnici **(3.3)** | **3.5** (Staff entitet) — sekcija 3.3 je "User entitet" |
| Trust Tier sistem | 03 - Korisnici **(3.5)** | **3.4** (Trust Tier) — sekcija 3.5 je "Staff entitet" |
| GlobalAdmin portal | 03 - Korisnici **(3.4)** | **3.6** (GlobalAdmin) — sekcija 3.4 je "Trust Tier" |

Sve četiri su pomjerene — izgleda da je referenca bazirana na stariju verziju Ch.03 prije nego je dodana sekcija 3.2 za Visitors.

**Preporuka:** Ispraviti reference: User registracija → (3.3), Staff panel → (3.5), Trust Tier → (3.4), GlobalAdmin → (3.6).

---

### M-02: MVP scope referenca za ListingDocument pokazuje na pogrešno poglavlje

**Lokacija:** `mvp-scope-opseg-prve-verzije.md`, linija 38

**Opis:** ListingDocument funkcionalnost referira na `07 - Komunikacija (7.1.6–7.1.7)`, ali SSoT (Single Source of Truth) za ListingDocument entitet je **`04 - Sadržaj, sekcija 4.7`**. Poglavlje 07 samo referencira Ch.04 za ovaj entitet.

**Preporuka:** Promijeniti referencu u `04 - Sadržaj (4.7)` ili dodati obje reference: `04 - Sadržaj (4.7), 07 - Komunikacija (7.1.7)`.

---

### M-03: Nekonzistentni API endpoint prefiksi između poglavlja

**Lokacija:**
- `03-korisnici-i-pristup.md`, sekcija 3.8
- `05-moderacija.md`, sekcija 5.7
- `06-monetizacija.md`, sekcija 6.6

**Opis:** API endpointi koriste različite konvencije za prefiks putanja:

| Poglavlje | Primjer endpointa | Prefiks |
|-----------|-------------------|---------|
| Ch.03 | `/staff/moderation/queue` | Bez `/api` prefiksa |
| Ch.05 | `/api/moderation/queue` | Sa `/api` prefiksom |
| Ch.06 | `/api/wallet`, `/api/promotions` | Sa `/api` prefiksom |
| Ch.03 | `/wallet/balance`, `/wallet/purchase` | Bez `/api` prefiksa |
| Ch.04 | `/events`, `/places` | Bez `/api` prefiksa |

Nema jasne konvencije — neki endpointi imaju `/api` prefiks, neki nemaju. Takođe, moderacijski endpointi su duplirani između Ch.03 i Ch.05 sa različitim putanjama (`/staff/moderation/{listingId}/approve` vs `/api/moderation/listings/{id}/approve`).

**Preporuka:** Definisati jednu konvenciju za API prefikse i uskladiti sve endpointe. Moderacijske endpointe definisati na jednom mjestu (SSoT u Ch.05) i referencirati iz Ch.03.

---

### M-04: MVP scope naslovna stranica — "tri grupe" umjesto "dvije grupe"

**Lokacija:** `mvp-scope-opseg-prve-verzije.md`, linija 67

**Opis:** MVP opis za naslovnu stranicu kaže:
> "Tri grupe sadržaja: Premium+Homepage, ostali Premium, Standard+obični."

Ali Ch.01 (sekcija 1.3) i Ch.02 (sekcija 2.1) jasno definišu **dvije grupe** na naslovnoj:
- **Grupa 1:** Premium sa opcijom "Prikaži na naslovnoj"
- **Grupa 2:** Svi ostali (uključujući Premium bez homepage opcije, Standard i obični)

Tri grupe (Premium sekcija, Standard, obični) važe **unutar kategorije** (Ch.02, sekcija 2.4), ne na naslovnoj.

**Preporuka:** Ispraviti na "Dvije grupe sadržaja na naslovnoj: Premium+Homepage (prioritet), svi ostali. Unutar kategorija: Premium sekcija na vrhu, Standard+obični ispod."

---

### M-05: Ch.02 sekcija 2.8 koristi zastarjelu terminologiju u praćenju statusa

**Lokacija:** `02-korisnicko-iskustvo.md`, sekcija 2.8 "Praćenje statusa objave", linije 499–504

**Opis:** Lista statusa za korisničko praćenje koristi generičke nazive koji ne odgovaraju novom statusnom modelu:

| Prikazano u Ch.02 | Odgovarajući `listingStatus` |
|-------------------|------------------------------|
| Draft | `draft` ✅ |
| Čeka pregled | `in_review` ✅ |
| Potrebne izmjene | `changes_requested` ✅ |
| **Aktivno** | `published` (ali nedostaju `published_under_review` i `published_needs_changes`) |
| Odbijeno | `rejected` ✅ |

Termin "Aktivno" je generičan i ne odražava da listing može biti `published`, `published_under_review` ili `published_needs_changes`. Nedostaju i `hidden_by_*` statusi, te `canceled` i `expired` za evente.

**Preporuka:** Ažurirati listu tako da reflektuje korisničku perspektivu novog modela: "Objavljeno", "Objavljeno — čeka pregled", "Potrebne izmjene", "Skriveno", "Otkazano", "Završeno (istekao)", "Odbijeno".

---

### M-06: Tier 4 sampling opis — "Minimalno" vs konfigurisani parametar

**Lokacija:**
- `03-korisnici-i-pristup.md`, sekcija 3.4, linija 243: Tier 4 sampling je "Minimalno"
- `05-moderacija.md`, sekcija 5.1.3, linija 96: Tier 4 sampling je "Konfigurisano"

**Opis:** Ch.03 opisuje Tier 4 sampling kao "Minimalno", a Ch.05 kao "Konfigurisano" (sa parametrom `TIER4_SAMPLING_PERCENT` i preporučenom vrijednošću 20%). Oba su tehnički tačna, ali Ch.03 daje utisak da je sampling fiksan i minimalan, dok Ch.05 jasno kaže da je to konfiguracijski parametar.

**Preporuka:** Uskladiti terminologiju — Ch.03 treba navesti "Konfigurisano (minimalni sampling)" ili dodati napomenu o `TIER4_SAMPLING_PERCENT` parametru.

---

### M-07: Visitor sekcija u Ch.01 — nedostaje informacija o "Prijaviti neprikladan sadržaj"

**Lokacija:** `01-uvod-i-koncepti.md`, sekcija 1.3, linije 236–243

**Opis:** Ch.01 opisuje šta Visitors mogu i ne mogu, ali **ne navodi** da Visitors ne mogu prijaviti neprikladan sadržaj. Ch.02 (sekcija 2.6) i Ch.03 (sekcija 3.2) eksplicitno navode ovo ograničenje u tabeli. Ch.01 bi trebao biti konzistentan kao uvodni dokument.

**Preporuka:** Dodati "Prijaviti neprikladan sadržaj" u listu stvari koje Visitor ne može u Ch.01.

---

### M-08: BR-MOD-30 zahtijeva `can_manage_trust_tier` za CRITICAL AI risk, ali Ch.05 sekcija 5.3.3 ne specificira

**Lokacija:**
- `05-moderacija.md`, BR-MOD-30, linija 1052: "CRITICAL AI risk level zahtijeva pregled moderatora sa `can_manage_trust_tier` permisijom"
- `05-moderacija.md`, sekcija 5.3.3, linija 395: CRITICAL je opisan kao "Urgent + obavezan pregled moderatora sa `can_manage_trust_tier`"

**Opis:** Sekcija 5.3.3 navodi ovo, ali sekcija 5.3.4 (AI Blocking Logic) i sekcija 5.3.5 (kako moderator vidi AI rezultate) ne spominju ovo ograničenje. Moderator bez `can_manage_trust_tier` permisije bi mogao pregledati CRITICAL stavku u queue-u jer queue interfejs ne filtrira po permisijama.

**Preporuka:** U sekciji 5.3.4 ili 5.3.5 eksplicitno napomenuti da CRITICAL stavke zahtijevaju moderatora sa `can_manage_trust_tier` permisijom i da queue interfejs treba filtrirati/označiti ove stavke.

---

### M-09: Nepotpuna referenca u Ch.01 za sekciju 1.5

**Lokacija:** `01-uvod-i-koncepti.md`, sekcija 1.4, linija 344

**Opis:** Tekst kaže "Ovaj dokument (1.1 i 1.5)" ali u zagradi navodi samo za product managere — ne pojašnjava da 1.5 sadrži persone. Manja nedosljednost: sekcija 1.5 je navedena kao "Persone i korisničke priče" ali naslov sekcije kaže "Persone i korisničke priče" — ovo je konzistentno, ali referenca na zasebni dokument "Persone i korisnička putovanja" koristi drugačiji naziv ("korisnička putovanja" vs "korisničke priče").

**Preporuka:** Uskladiti terminologiju — koristiti "Persone i korisnička putovanja" konzistentno, ili jasno razlikovati da sekcija 1.5 sadrži sažetak, a zasebni dokument kompletne persone.

---

### M-10: Pauziranje promocije pri `canceled` — nekonzistentno između Ch.04 i Ch.06

**Lokacija:**
- `04-sadrzaj.md`, sekcija 4.8, linije 879–880: "Aktivne promocije se **pauziraju**"
- `06-monetizacija.md`, sekcija 6.2.7, linija 394: "Ako listing izgubi javnu vidljivost... promocija automatski prestaje bez refunda"

**Opis:** Ch.04 kaže da se pri prelasku u `canceled` promocije **pauziraju** (timer se zaustavlja, mogu se nastaviti pri reaktivaciji). Ch.06 generalno kaže da kad listing izgubi javnu vidljivost, promocija **prestaje** bez refunda. Međutim, `canceled` je `isPublic = true`, pa pravilo iz Ch.06 tehnički ne važi. Ali konfuzija ostaje jer Ch.06 ne specificira posebno ponašanje za `canceled`.

**Preporuka:** U Ch.06, sekcija 6.2.7, dodati eksplicitno pravilo: "Poseban slučaj za `canceled`: promocija se pauzira (ne prestaje) — detalji u Ch.04, sekcija 4.8."

---

## Info nalazi

### I-01: Changelog zapisi spominju stare termine — očekivano i ispravno

**Lokacija:** Changelozi u Ch.03, Ch.04, Ch.05, Ch.06, Ch.08, MVP scope

**Opis:** Stari termini (`lifecycleStatus`, `moderationStatus`, `closedReason`) pojavljuju se u changelog zapisima koji opisuju migraciju. Ovo je ispravno jer changelozi dokumentuju šta se promijenilo i iz čega.

**Preporuka:** Nikakva akcija nije potrebna.

---

### I-02: Napomena u Ch.05 eksplicitno označava stari `moderationStatus` kao depreciran

**Lokacija:** `05-moderacija.md`, linije 1126–1127

**Opis:** Ch.05 ima jasnu napomenu:
> "Stari `moderationStatus` atribut... više ne postoji."

Ovo je korisno jer pomaže developerima koji čitaju stari kod.

**Preporuka:** Nikakva akcija — ovo je primjer dobre prakse.

---

### I-03: Statusna specifikacija navodi stare termine u kontekstu migracije

**Lokacija:** `novi-listing-statusni-model-specifikacija.md`, linije 10, 530–532

**Opis:** Specifikacija migracije koristi stare termine u kontekstu objašnjenja šta zamjenjuju (sekcija 10: "Zamjenjena polja"). Ovo je ispravno i korisno.

**Preporuka:** Nikakva akcija.

---

### I-04: Trust Tier parametri su konzistentni između Ch.03 i Ch.05

**Lokacija:**
- `03-korisnici-i-pristup.md`, sekcija 3.4
- `05-moderacija.md`, sekcija 5.1.3

**Opis:** Parametri za napredovanje (TIER1_MIN_APPROVED=5, TIER1_MIN_SUCCESS_RATE=80%, TIER1_MIN_ACCOUNT_AGE_DAYS=7, TIER2_MIN_APPROVED=20, TIER2_MIN_SUCCESS_RATE=85%, TIER2_MIN_ACCOUNT_AGE_DAYS=30) i degradaciju (TIER_REJECTED_THRESHOLD=3, TIER_REJECTED_WINDOW_DAYS=30) su identični u oba poglavlja.

**Preporuka:** Nikakva akcija — konzistentnost je zadovoljavajuća.

---

### I-05: Statusni opisi u Ch.04 i statusnoj specifikaciji su konzistentni

**Lokacija:**
- `04-sadrzaj.md`, sekcija 4.8
- `novi-listing-statusni-model-specifikacija.md`, sekcija 2

**Opis:** Svih 13 statusa, njihovi opisi, `isPublic` vrijednosti i terminal oznake su identični u oba dokumenta. Dijagrami tranzicija su takođe jednaki.

**Preporuka:** Nikakva akcija — konzistentnost je zadovoljavajuća.

---

## Pregled po kategorijama

### Terminologija (stari termini)
- **C-04**: `lifecycleStatus` u epics-stories-instructions.md
- **I-01, I-02, I-03**: Stari termini u changelogima i napomenama o migraciji — ispravno

### Cross-reference greške
- **M-01**: Četiri pogrešne sekcije u MVP scope referencama na Ch.03
- **M-02**: ListingDocument referenca na pogrešno poglavlje u MVP scope

### Konzistentnost podataka
- **C-02**: Kontradikcija o ručnom blokiranju (Ch.03 vs Ch.04/Ch.05)
- **C-03**: Kontradikcija o timeout ishodu za `changes_requested` (Ch.04 vs Ch.05/Ch.08)
- **I-04**: Trust Tier parametri konzistentni ✅
- **I-05**: Statusni opisi konzistentni ✅

### API endpointi
- **M-03**: Nekonzistentni prefiksi i duplirani moderacijski endpointi

### Kontradikcije
- **C-02**: Ručno blokiranje — `removed` vs `hidden_by_system`
- **C-03**: Timeout `changes_requested` — `removed` vs `rejected`
- **M-04**: Naslovna stranica — dvije vs tri grupe
- **M-10**: Promocija pri `canceled` — pauzira vs prestaje

### Tech stack
- **C-01**: .NET 8 umjesto .NET 10 (LTS) u Ch.08

### MVP scope
- **M-01**: Pogrešne cross-reference na Ch.03
- **M-02**: Pogrešna referenca za ListingDocument
- **M-04**: Pogrešan opis grupa na naslovnoj

---

*Izvještaj generisan: 2.4.2026*
