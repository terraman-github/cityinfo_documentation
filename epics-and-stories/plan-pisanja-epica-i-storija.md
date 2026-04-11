# Plan pisanja epica i storija

<a id="cityinfo-plan-pisanja-epica-i-storija"></a>

# CityInfo — Plan pisanja epica i storija

> **Verzija:** 1.8  
> **Datum:** 1.4.2026  
> **Namjena:** Continuation prompt za pisanje epica i storija kroz više sesija.  
> Ovaj dokument sadrži sve dogovorene odluke, finalnu listu epica, plan batcheva,  
> i status — tako da svaka nova sesija može krenuti odmah bez ponovnog objašnjavanja.

* * *

<a id="kako-koristiti-ovaj-dokument"></a>

## Kako koristiti ovaj dokument

Na početku svake sesije:

1. **Pročitaj ovaj dokument** — sadrži sve odluke i trenutni status
2. **Pročitaj instrukcije za pisanje epica i storija** — projektni fajl `cityinfo-epics-stories-instructions.md`
3. **Provjeri koji batch je sljedeći** u tabeli statusa (sekcija "Status po batchevima")
4. **Dohvati potrebne Confluence stranice** za taj batch (page ID-evi su navedeni)
5. **Piši epic + storije** prema dogovorenom formatu, prikaži za review, pa kreiraj na Confluenceu

* * *

<a id="dogovorene-odluke-ne-mijenjati-bez-eksplicitne-potvrde"></a>

## Dogovorene odluke (ne mijenjati bez eksplicitne potvrde)

<a id="tech-stack"></a>

### Tech stack

- **Backend:** .NET 10 (LTS) + MS SQL Server
- **Frontend:** Svelte 5 + SvelteKit + TailwindCSS + Flowbite
- **Tri odvojena frontend sistema:** User ([cityinfo.ba](http://cityinfo.ba)), Staff ([admin.cityinfo.ba](http://admin.cityinfo.ba)), GlobalAdmin ([master.cityinfo.ba](http://master.cityinfo.ba) — Faza 2)

<a id="grupacija-epica"></a>

### Grupacija epica

- **14 funkcionalnih epica** (E01–E14) sa hibridnom strukturom: funkcionalni epici + journey milestones (J-01 do J-09)
- **E03 je razdvojen** na E03a (entiteti + seed data, Sprint 0) i E03b (admin UI + CRUD, Sprint 5–6)
- **E13 prošireni scope** — uključuje Staff CRUD, role/permission dodjelu, tenant access konfiguraciju (ne samo shell + moderacijski UI)
- **Višejezičnost: hibridni pristup** — i18n infrastruktura (framework, fallback logika, locale management) u E14, a konkretna dvojezična polja (`nameAlt`, `descriptionAlt`, `excerptAlt`) kao AC-ovi u domensim epicima (E02, E03, E04, E05)
- **CI/CD pipeline** je zasebna storija (S14-07) koja nije Sprint 0 prioritet — ide kad tim procijeni

<a id="confluence-struktura"></a>

### Confluence struktura

- Epici i storije žive u folderu **EPICS AND STORIES** pod PROJECT SPECS
- Jedan epic = jedna Confluence stranica
- Storije = podstranice svog epica
- Format prati instrukcije iz `cityinfo-epics-stories-instructions.md`

<a id="pisanje-storija-ključni-principi"></a>

### Pisanje storija — ključni principi

- Bosanski (ijekavica), tehnički termini na engleskom
- AC-ovi su provjerljivi (DA/NE), ne dupliciraju dokumentaciju
- Testovi su optimizirani (happy path + ključni edge case), ne exhaustive
- Tehničke napomene su smjernice, ne specifikacije
- Referenciraj dokumentaciju umjesto kopiranja (`Ch.04, sekcija 4.8`)

<a id="listing-statusni-model"></a>

### Listing statusni model

> ✅ **Migracija završena 1.4.2026.** Svi epici i storije koriste **jednostatus model** (`listingStatus` sa 13 vrijednosti + `removedReason` + `isPublic` + `wasEverActive`). Stari dvostatus model (`lifecycleStatus` + `moderationStatus` + `closedReason`) je u potpunosti zamijenjen. Detalji migracije: [MIGRACIJA: Listing statusni model](/wiki/pages/createpage.action?spaceKey=GI&title=MIGRACIJA%3A%20Listing%20statusni%20model%20%E2%80%94%20jedan%20status&linkCreation=true&fromPageId=250970134).

* * *

<a id="finalna-lista-epica"></a>

## Finalna lista epica

| #   | Epic | Domena / Poglavlje | Journey milestones | Sprint | Stvarni broj storija |
| --- | --- | --- | --- | --- | --- |
| **E14** | Infrastruktura, i18n i pozadinski procesi | Ch.08, Ch.01 | J-08 | 0   | 7   |
| **E03a** | Kategorizacija sadržaja — entiteti i seed data | Ch.04 (4.4–4.5) | J-02, J-04 | 0   | 5   |
| **E01** | Korisnička registracija i profil | Ch.03 (3.2–3.3), Ch.02 (2.7) | J-01 | 1–2 | 8   |
| **E02** | Listing CRUD i lifecycle | Ch.04 (4.1–4.3, 4.7–4.8) | J-02 | 1–2 | 9   |
| **E06** | Trust Tier sistem | Ch.03 (3.4) | J-03, J-08 | 3–4 | 5   |
| **E07** | Moderacijski workflow i AI screening | Ch.05 (5.1–5.3) | J-03 | 3–4 | 6   |
| **E13** | Staff panel, autentifikacija i upravljanje osobljem | Ch.03 (3.5), Ch.05 (5.4) | J-08 | 3–4 | 7   |
| **E03b** | Kategorizacija sadržaja — admin upravljanje | Ch.04 (4.4–4.5) | J-08 | 5–6 | 4   |
| **E04** | Otkrivanje i pretraga sadržaja | Ch.02 (2.1–2.2, 2.4–2.5) | J-04 | 5–6 | 7   |
| **E05** | Prikaz sadržaja i korisničke interakcije | Ch.02 (2.3, 2.6), Ch.04 (4.9) | J-04, J-05 | 5–6 | 6   |
| **E08** | Komunikacija uz listing i dokumenti | Ch.07 (7.1) | J-03, J-07 | 7–8 | 5   |
| **E09** | Kreditni sistem i wallet | Ch.06 (6.1) | J-09 | 7–8 | 4   |
| **E10** | Promocije listinga | Ch.06 (6.2) | J-06 | 7–8 | 6   |
| **E11** | Display oglašavanje (MVP) | Ch.06 (6.3) | J-08 | 9–10 | 5   |
| **E12** | Notifikacije | Ch.07 (7.2) | Cross-cutting | 9–10 | 5   |

**Ukupno: 92 storije** (konačan broj — svi batchevi završeni)

* * *

<a id="plan-batcheva"></a>

## Plan batcheva

Svaki batch je jedna sesija. Na početku sesije: pročitaj ovaj dokument, dohvati potrebne Confluence stranice, piši, pregledaj sa Zoranom, kreiraj na Confluenceu.

| Batch | Epici | Confluence stranice za dohvat | Prioritet |
| --- | --- | --- | --- |
| **1** | E14 (Infra + i18n), E03a (Kategorije seed) | Ch.08 (`240189509`), Ch.04 (`240189477`) | Sprint 0 |
| **2** | E01 (Registracija i profil) | Ch.03 (`240156686`), Ch.02 (`240254995` — sekcija 2.7) | Sprint 1 |
| **3** | E02 (Listing CRUD i lifecycle) | Ch.04 (`240189477`), Ch.02 (`240254995` — sekcija 2.8) | Sprint 1–2 |
| **4** | E06 (Trust Tier), E07 (Moderacija) | Ch.03 (`240156686` — sekcija 3.4), Ch.05 (`240189485`) | Sprint 3–4 |
| **5** | E13 (Staff panel i upravljanje) | Ch.03 (`240156686` — sekcija 3.5), Ch.05 (`240189485` — sekcija 5.4) | Sprint 3–4 |
| **6** | E03b (Kategorije admin), E04 (Pretraga), E05 (Prikaz) | Ch.04 (`240189477`), Ch.02 (`240254995`) | Sprint 5–6 |
| **7** | E08 (Komunikacija), E09 (Wallet), E10 (Promocije) | Ch.07 (`240320540`), Ch.06 (`240222244`) | Sprint 7–8 |
| **8** | E11 (Display Ads), E12 (Notifikacije) | Ch.06 (`240222244` — sekcija 6.3), Ch.07 (`240320540` — sekcija 7.2) | Sprint 9–10 |

* * *

<a id="status-po-batchevima"></a>

## Status po batchevima

| Batch | Status | Datum | Napomene |
| --- | --- | --- | --- |
| **1** | ✅ Završeno — na Confluenceu | 30.3.2026 | E14 (7 storija, page `251199489`) + E03a (5 storija, page `251297793`). Uploadovano na Confluence pod EPICS AND STORIES folder (`250249231`). |
| **2** | ✅ Završeno — na Confluenceu | 30.3.2026 | E01 (8 storija, page `251232295`). Uploadovano na Confluence pod EPICS AND STORIES folder (`250249231`). |
| **3** | ✅ Završeno — na Confluenceu | 30.3.2026 | E02 (9 storija, page `251330580`). Uploadovano na Confluence pod EPICS AND STORIES folder (`250249231`). |
| **4** | ✅ Završeno — na Confluenceu | 30.3.2026 | E06 (5 storija, page `250478652`) + E07 (6 storija, page `251265065`). Uploadovano na Confluence pod EPICS AND STORIES folder (`250249231`). |
| **5** | ✅ Završeno — na Confluenceu | 30.3.2026 | E13 (7 storija, page `250970205`). Uploadovano na Confluence pod EPICS AND STORIES folder (`250249231`). |
| **6** | ✅ Završeno — na Confluenceu | 31.3.2026 | E03b (4 storije, page `251691009`) + E04 (7 storija, page `251854849`) + E05 (6 storija, page `252084225`). Uploadovano na Confluence pod EPICS AND STORIES folder (`250249231`). |
| **7** | ✅ Završeno — na Confluenceu | 31.3.2026 | E08 (5 storija, page `252018708`) + E09 (4 storije, page `252411905`) + E10 (6 storija, page `252280852`). Uploadovano na Confluence pod EPICS AND STORIES folder (`250249231`). |
| **8** | ✅ Završeno — na Confluenceu | 31.3.2026 | E11 (5 storija, page `252706817`) + E12 (5 storija, page `252575764`). Uploadovano na Confluence pod EPICS AND STORIES folder (`250249231`). |

> ✅ **SVI BATCHEVI ZAVRŠENI.** Ukupno 15 epica (E01–E14 + E03a/E03b) sa 92 storije kreirano na Confluenceu.
> 
> ✅ **MIGRACIJA NA JEDNOSTATUS MODEL ZAVRŠENA** (1.4.2026). Svi pogođeni epici i storije ažurirani — detalji u [migracijskom planu](/wiki/pages/createpage.action?spaceKey=GI&title=MIGRACIJA%3A%20Listing%20statusni%20model%20%E2%80%94%20jedan%20status&linkCreation=true&fromPageId=250970134).

* * *

<a id="sprint-raspored-kontekst-za-pisanje-storija"></a>

## Sprint raspored (kontekst za pisanje storija)

```
Sprint 0:  [E14-infra] + [E03a-kategorije seed] ────────────────────────────►
Sprint 1-2: [E01-registracija] → [E02-listing CRUD] ────────────────────────►
Sprint 3-4:                      [E06-trust tier] → [E07-moderacija] → [E13-staff]
Sprint 5-6:          [E03b-kat admin] → [E04-pretraga] → [E05-prikaz+interakcije]
Sprint 7-8:                                    [E08-komunikacija] → [E09-wallet] → [E10-promocije]
Sprint 9-10:                                                   [E11-display ads] → [E12-notifikacije]
```

**Ključne zavisnosti:**

- E01 (registracija) i E02 (listing CRUD) su na kritičnom putu — gotovo sve zavisi od njih
- E03a (kategorije seed) je preduslov za E02 (listing forma treba kategorije)
- E06 (Trust Tier) i E07 (moderacija) su usko povezani
- E09 (krediti) je preduslov za E10 (promocije)
- E14 (infra) je preduslov za sve

* * *

<a id="confluence-navigacija-brza-referenca"></a>

## Confluence navigacija (brza referenca)

| Stranica | ID  | Link |
| --- | --- | --- |
| PROJECT SPECS (root) | `15695888` | [link](https://terraprojects.atlassian.net/wiki/spaces/GI/pages/15695888/PROJECT+SPECS) |
| Projektni indeks | `240812033` | [link](https://terraprojects.atlassian.net/wiki/spaces/GI/pages/240812033/CityInfo+-+Projektni+indeks) |
| MVP SCOPE | `242188289` | [link](https://terraprojects.atlassian.net/wiki/spaces/GI/pages/242188289/MVP+SCOPE+Opseg+prve+verzije) |
| Ch.01 — Uvod i koncepti | `240156678` | [link](https://terraprojects.atlassian.net/wiki/spaces/GI/pages/240156678/01+-+UVOD+I+KONCEPTI) |
| Ch.02 — Korisnički doživljaj | `240254995` | [link](https://terraprojects.atlassian.net/wiki/spaces/GI/pages/240254995/02+-+KORISNI+KO+ISKUSTVO) |
| Ch.03 — Korisnici i pristup | `240156686` | [link](https://terraprojects.atlassian.net/wiki/spaces/GI/pages/240156686/03+-+KORISNICI+I+PRISTUP) |
| Ch.04 — Sadržaj | `240189477` | [link](https://terraprojects.atlassian.net/wiki/spaces/GI/pages/240189477/04+-+SADR+AJ) |
| Ch.05 — Moderacija | `240189485` | [link](https://terraprojects.atlassian.net/wiki/spaces/GI/pages/240189485/05+-+MODERACIJA) |
| Ch.06 — Monetizacija | `240222244` | [link](https://terraprojects.atlassian.net/wiki/spaces/GI/pages/240222244/06+-+MONETIZACIJA) |
| Ch.07 — Komunikacija | `240320540` | [link](https://terraprojects.atlassian.net/wiki/spaces/GI/pages/240320540/07+-+KOMUNIKACIJA) |
| Ch.08 — Infrastruktura | `240189509` | [link](https://terraprojects.atlassian.net/wiki/spaces/GI/pages/240189509/08+-+INFRASTRUKTURA) |
| Persone i putovanja | `243040257` | [link](https://terraprojects.atlassian.net/wiki/spaces/GI/pages/243040257/Persone+i+korisni+ka+putovanja) |
| EPICS AND STORIES folder | `250249231` | [link](../epics-and-stories.md) |
| Novi listing statusni model — specifikacija | `253526019` | [link](https://terraprojects.atlassian.net/wiki/spaces/GI/pages/253526019/Novi+listing+statusni+model+specifikacija) |
| MIGRACIJA: Listing statusni model | `253853698` | [link](/wiki/pages/createpage.action?spaceKey=GI&title=MIGRACIJA%3A%20Listing%20statusni%20model%20%E2%80%94%20jedan%20status&linkCreation=true&fromPageId=250970134) |
| Instrukcije za epice/storije | —   | Projektni fajl: `cityinfo-epics-stories-instructions.md` |

* * *

<a id="kreirani-epici-brza-referenca"></a>

## Kreirani epici (brza referenca)

| Epic | Page ID | Broj storija | Datum |
| --- | --- | --- | --- |
| E14 — Infrastruktura, i18n i pozadinski procesi | `251199489` | 7   | 30.3.2026 |
| E03a — Kategorizacija sadržaja — entiteti i seed data | `251297793` | 5   | 30.3.2026 |
| E01 — Korisnička registracija i profil | `251232295` | 8   | 30.3.2026 |
| E02 — Listing CRUD i lifecycle | `251330580` | 9   | 30.3.2026 |
| E06 — Trust Tier sistem | `250478652` | 5   | 30.3.2026 |
| E07 — Moderacijski workflow i AI screening | `251265065` | 6   | 30.3.2026 |
| E13 — Staff panel, autentifikacija i upravljanje osobljem | `250970205` | 7   | 30.3.2026 |
| E03b — Kategorizacija sadržaja — admin upravljanje | `251691009` | 4   | 31.3.2026 |
| E04 — Otkrivanje i pretraga sadržaja | `251854849` | 7   | 31.3.2026 |
| E05 — Prikaz sadržaja i korisničke interakcije | `252084225` | 6   | 31.3.2026 |
| E08 — Komunikacija uz listing i dokumenti | `252018708` | 5   | 31.3.2026 |
| E09 — Kreditni sistem i wallet | `252411905` | 4   | 31.3.2026 |
| E10 — Promocije listinga | `252280852` | 6   | 31.3.2026 |
| E11 — Display oglašavanje (MVP) | `252706817` | 5   | 31.3.2026 |
| E12 — Notifikacije | `252575764` | 5   | 31.3.2026 |

* * *

<a id="napomene-za-ai-asistenta"></a>

## Napomene za AI asistenta

- **Čitaj dokumentaciju, ne pretpostavljaj.** Svaki batch zahtijeva dohvat relevantnih Confluence stranica jer se dokumentacija može mijenjati između sesija.
- **Prikaži draft za review prije Confluence uploada.** Zoran pregledava sadržaj i daje feedback — tek nakon potvrde se kreira na Confluenceu.
- **Jedan epic po Confluence stranici, storije kao podstranice.** Ne stavljaj sve u jedan dokument.
- **Ažuriraj ovu stranicu** na kraju svake sesije — označi batch kao završen, zapiši datum, dodaj epic u "Kreirani epici" tabelu.
- **Tech stack je .NET 10 (LTS)**, ne .NET 8.
- **Format prati instrukcije** iz `cityinfo-epics-stories-instructions.md` — ne improvizuj format.
- **Ova stranica je SSoT za plan i status.** Ne koristi lokalne fajlove — dohvati ovu stranicu sa Confluencea na početku svake sesije.
- **Listing statusni model:** Koristiti `listingStatus` (jednostatus model sa 13 vrijednosti). Stari termini `lifecycleStatus`, `moderationStatus`, `closedReason` su zamijenjeni.