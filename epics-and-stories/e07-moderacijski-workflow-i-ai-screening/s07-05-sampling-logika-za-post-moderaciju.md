---
id: S07-05
parent_epic: E07
linear_id: "CIT2-49"
phase: MVP
journey_milestones: [J-03]
type: backend-only
---

# S07-05 — Sampling logika za post-moderaciju

**Naslov:** Sampling logika za post-moderaciju

**Excerpt:** Korisnici na Tier 2 imaju 100% post-moderaciju, ali za Tier 3 i 4 moderator pregleda samo nasumični uzorak sadržaja. Sampling značajno smanjuje opterećenje moderatora za provjerene korisnike, dok i dalje održava kontrolu kvaliteta — ako se u uzorku pronađe problem, korisnik može biti degradiran.

**Phase:** MVP

**Journey milestones:** **J-03**

**User story:**  
Kao sistem,  
želim primjenjivati sampling logiku na post-moderaciju za korisnike višeg Trust Tier-a,  
kako bi moderatori fokusirali vrijeme na novi i riskantniji sadržaj umjesto na rutinski pregled provjerenih korisnika.

**Kontekst:** Post-moderacija znači da je sadržaj već vidljiv — moderator ga pregleda naknadno. Za Tier 2 sav sadržaj se pregleda (100%). Za Tier 3 i 4, sistem nasumično odabire uzorak na osnovu konfigurabilnih procenata. Neodabrani sadržaj automatski prelazi u `published` bez pregleda. Ako se u pregledanom uzorku pronađe problem, moderator može degradirati korisnika, privremeno povećati sampling, ili reagovati na drugi način. Detalji → **Ch.05, sekcija 5.1**.3 (Sampling).

**Acceptance criteria:**

- [ ] Tier 2 korisnici: sav sadržaj (100%) ulazi u post-moderacijski queue
- [ ] Tier 3 korisnici: nasumični uzorak od `TIER3_SAMPLING_PERCENT`% ulazi u queue, ostalo se auto-publish
- [ ] Tier 4 korisnici: nasumični uzorak od `TIER4_SAMPLING_PERCENT`% ulazi u queue, ostalo se auto-publish
- [ ] `TIER3_SAMPLING_PERCENT` i `TIER4_SAMPLING_PERCENT` su konfiguracijski parametri
- [ ] Sadržaj koji nije odabran za sampling automatski prelazi u `listingStatus = published`
- [ ] Sampling odluka se donosi pri submitovanju — korisnik ne zna da li je njegov sadržaj odabran za pregled
- [ ] Ako se u sampliranom sadržaju pronađe problem, moderator može degradirati korisnika (→ [E06](../e06-trust-tier-sistem.md), [S06-03](../e06-trust-tier-sistem/s06-03-rucna-promjena-trust-tier-a.md))
- [ ] AI screening se i dalje pokreće za sav sadržaj (uključujući nesampliran) — AI blocking važi neovisno o samplingu
- [ ] Statistika samplinga je dostupna moderatorima (koliko je pregledano, koliko problema pronađeno)

**Backend Scope:**

- Logika pri submit-u za Tier 3/4: nasumična odluka (random) da li listing ulazi u queue ili auto-publish
- Konfiguracijski parametri: `TIER3_SAMPLING_PERCENT` (preporučeno: 50), `TIER4_SAMPLING_PERCENT` (preporučeno: 20)
- Auto-publish za nesamplirani sadržaj: `listingStatus = published`
- AI screening se pokreće neovisno — čak i za nesamplirani sadržaj, AI blocking može blokirati publikaciju
- `GET /api/moderation/stats/patterns` — uključuje sampling statistiku

**Tehničke napomene:**

- Sampling je nasumičan, ne round-robin ili baziran na sadržaju. Cilj je da korisnik ne može predvidjeti koji listing će biti pregledan.
- AI screening + blocking radi neovisno od samplinga. Čak i listing Tier 4 korisnika koji nije odabran za sampling može biti AI-blokiran i ići u Urgent queue.
- Za MVP, "privremeno povećanje samplinga za jednog korisnika" može biti ručno (moderator promijeni tier) umjesto automatskog mehanizma.

**Testovi (MVP):**

- [ ] Tier 2 listing → uvijek ulazi u post-mod queue (100%)
- [ ] Tier 3 listing sa `TIER3_SAMPLING_PERCENT = 50` → otprilike 50% ulazi u queue (statistički test)
- [ ] Tier 4 listing sa `TIER4_SAMPLING_PERCENT = 20` → otprilike 20% ulazi u queue
- [ ] Nesamplirani listing → `listingStatus = published` automatski
- [ ] AI blocking za nesamplirani listing → listing ipak ide u Urgent queue
- [ ] Promjena sampling parametra → odmah se primjenjuje na nove listinge

**Wireframe referenca:** —

**Implementacijske napomene:**

- Koristiti kriptografski siguran random za sampling odluku da se izbjegne predvidljivost.
- Sampling odluka se bilježi (da li je listing sampliran ili auto-published) za kasniju analizu kvaliteta.