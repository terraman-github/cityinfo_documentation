---
id: S04-01
confluence_page_id: "251887617"
title: "S04-01 — Naslovna stranica sa dva režima i promocijskim prioritetima"
parent_epic: E04
linear_id: "CIT2-27"
phase: MVP
journey_milestones: [J-04]
type: fullstack
---

**Naslov:** Naslovna stranica sa dva režima i promocijskim prioritetima

**Excerpt:** Naslovna stranica je ulazna tačka za većinu posjetilaca. Po defaultu prikazuje događaje, a korisnik može prebaciti na mjesta. Sadržaj se prikazuje u dvije grupe: Premium+Homepage listinzi imaju apsolutni prioritet, a svi ostali se sortiraju po sortDate.

**Phase:** MVP

**Journey milestones:** J-04

**User story:**  
Kao posjetilac (visitor ili registrovan korisnik),

želim vidjeti relevantne listinge čim otvorim platformu,

kako bih brzo saznao šta se dešava u gradu ili gdje otići.

**Kontekst:** Korisnik otvara [cityinfo.ba](http://cityinfo.ba). Naslovna po defaultu prikazuje Events režim jer su događaji vremenski osjetljivi. Korisnik može prebaciti na Places režim kroz vidljivu navigaciju. Sadržaj je podijeljen u dvije grupe prema **Ch.02, sekcija 2.1** — Grupa 1 su Premium+Homepage promocije (apsolutni prioritet), Grupa 2 su svi ostali listinzi sortirani po sortDate. Featured sekcije (npr. "Ovaj vikend") su za MVP hardkodirane.

**Acceptance criteria:**

- [ ] Naslovna stranica se učitava sa Events režimom kao default
- [ ] Vidljiva navigacija (tab ili toggle) omogućava prebacivanje na Places režim i nazad
- [ ] Promjena režima resetuje aktivne filtere (kategorija, tag, datum) jer nisu kompatibilni između režima
- [ ] Sadržaj u Events režimu prikazuje Grupu 1 (Premium+Homepage promocije) iznad Grupe 2 (ostali)
- [ ] Unutar svake grupe, listinzi su sortirani po `sortDate` (najnoviji prvi)
- [ ] Premium promocije bez opcije "Prikaži na naslovnoj" nemaju prioritet na homepage-u — pripadaju Grupi 2
- [ ] Sadržaj u Places režimu prati istu logiku dviju grupa
- [ ] Prikazuju se samo javno vidljivi listinzi (`isPublic = true`)
- [ ] Za Events: prikazuju se samo budući eventi i oni koji su još u toku (endDateTime >= now)
- [ ] Naslovna sadrži barem jednu featured sekciju (hardkodirana za MVP — npr. "Ovaj vikend")
- [ ] Nazivi i opisi se prikazuju na jeziku koji je korisnik odabrao, sa fallback-om na primarni jezik tenanta

**Backend Scope:**

- `GET /events` — vraća listu javnih evenata sa podrškom za sortiranje po promotion grupi + sortDate, paginacijom
- `GET /places` — isto za mjesta
- Logika sortiranja: Grupa 1 (Premium+Homepage) uvijek ispred Grupe 2, unutar grupe po sortDate desc
- Featured sekcija: za MVP može biti poseban endpoint ili parametar na postojećem (npr. `GET /events?featured=this-weekend`)

**Frontend Scope:**

- UI: Naslovna sa header-om, search bar-om, lokacijskim indikatorom, tab navigacijom (Events/Places)
- UI: Grid/lista kartica — svaka kartica prikazuje elemente prema **Ch.02, sekcija 2.3** (slika, naziv, excerpt, kategorija, datum, itd.)
- UI: Featured sekcija — horizontalni carousel ili grid za tematski kurirane listinge
- UX: Smooth prebacivanje između režima bez reload-a cijele stranice
- UX: Skeleton loading za kartice dok se podaci učitavaju

**Tehničke napomene:**

- Bez [E10](../e10-promocije-listinga.md) (Promocije), sortiranje se radi samo po sortDate — promocijski prioriteti se dodaju kad [E10](../e10-promocije-listinga.md) bude implementiran.
- Featured sekcije za MVP mogu biti hardkodirane query-ji (npr. "eventi sa startDateTime u naredna 3 dana").

**Testovi (MVP):**

- [ ] Naslovna se otvara sa Events režimom — prikazuju se samo eventi
- [ ] Prebacivanje na Places — prikazuju se samo mjesta, filteri su resetovani
- [ ] Premium+Homepage listing se prikazuje iznad non-premium listinga
- [ ] Expired eventi se ne prikazuju na naslovnoj
- [ ] Prebacivanje jezika — nazivi se mijenjaju na sekundarni jezik (gdje postoji nameAlt)

**Wireframe referenca:** —