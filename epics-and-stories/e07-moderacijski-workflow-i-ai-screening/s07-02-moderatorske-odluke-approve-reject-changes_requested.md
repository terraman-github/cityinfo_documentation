---
id: S07-02
confluence_page_id: "251297831"
parent_epic: E07
linear_id: "CIT2-46"
phase: MVP
journey_milestones: [J-03]
type: fullstack
---

# S07-02 — Moderatorske odluke (approve, reject, changes_requested)

**Naslov:** Moderatorske odluke (approve, reject, changes\_requested)

**Excerpt:** Tri osnovna ishoda moderacije: odobri sadržaj, odbaci ga, ili vrati na doradu sa konkretnim feedbackom. Svaka odluka pokreće lanac efekata — od promjene vidljivosti listinga do evaluacije Trust Tier napredovanja vlasnika.

**Phase:** MVP

**Journey milestones:** **J-03**

**User story:**  
Kao moderator,  
želim donijeti odluku o sadržaju (odobriti, odbaciti ili tražiti izmjene) i da sistem automatski primijeni sve posljedice te odluke,  
kako bih mogao efikasno raditi bez ručnog praćenja statusnih tranzicija i Trust Tier kalkulacija.

**Kontekst:** Moderator pregleda stavku iz queue-a i donosi jednu od tri odluke. Approve i reject su finalne odluke koje utiču na Trust Tier statistiku korisnika. Changes\_requested nije finalna — korisnik dobija povratnu informaciju i priliku da ispravi sadržaj. Svaka odluka osim approve zahtijeva obrazloženje. Nakon finalne odluke, sistem evaluira Trust Tier napredovanje (→ [E06](../e06-trust-tier-sistem.md), [S06-01](../e06-trust-tier-sistem/s06-01-automatska-evaluacija-trust-tier-napredovanja.md)) i auto-degradaciju (→ [E06](../e06-trust-tier-sistem.md), [S06-02](../e06-trust-tier-sistem/s06-02-automatska-degradacija-na-restricted-tier-0.md)). Detalji → **Ch.05**, sekcije 5.2.3–5.2.4.

**Acceptance criteria:**

- [ ] Moderator može odobriti listing (approve) — listing prelazi u `published` (pre-mod) ili ostaje vidljiv i prelazi u `published` (post-mod)
- [ ] Moderator može odbaciti listing (reject) — listing prelazi u `rejected` (terminalni status)
- [ ] Moderator može tražiti izmjene (changes\_requested) — listing prelazi u `changes_requested`, korisnik dobija poruku sa feedbackom
- [ ] Reject i changes\_requested zahtijevaju unos razloga (obavezno polje)
- [ ] Moderator može koristiti template poruku (iz biblioteke) ili napisati custom tekst
- [ ] Moderator može dodati internu napomenu (vidljivu samo staff-u, ne korisniku)
- [ ] Uz approve, moderator može opciono postaviti `verificationStatus` (verified ili unverified)
- [ ] Nakon approve ili reject, sistem poziva Trust Tier evaluaciju ([E06](../e06-trust-tier-sistem.md) logika)
- [ ] Nakon reject, sistem provjerava auto-degradaciju ([E06](../e06-trust-tier-sistem.md) logika)
- [ ] `changes_requested` ne utiče na Trust Tier statistiku
- [ ] Moderator može override-ati odluku drugog moderatora (uz logging)
- [ ] Svaka odluka se bilježi u audit log sa: moderator ID, odluka, razlog, timestamp

**Backend Scope:**

- `POST /api/moderation/listings/{id}/approve` — prima: `reason` (opciono), `internalNote` (opciono), `verificationStatus` (opciono)
- `POST /api/moderation/listings/{id}/reject` — prima: `reason` (obavezno), `templateId` (opciono), `internalNote` (opciono)
- `POST /api/moderation/listings/{id}/request-changes` — prima: `reason` (obavezno), `templateId` (opciono), `internalNote` (opciono)
- `POST /api/moderation/listings/{id}/override` — promjena prethodne odluke, obavezno `reason`
- Side effects: tranzicija `listingStatus` (approve → `published`, reject → `rejected`, changes\_requested → `changes_requested`), notifikacija korisniku
- Integration: poziv `EvaluateTrustTierProgression()` nakon approve/reject; poziv `EvaluateAutoDegradation()` nakon reject

**Frontend Scope:**

- UI: tri action dugmeta na stavci queue-a (Approve, Request Changes, Reject)
- Modalni dialog za reject/changes\_requested: polje za razlog, dropdown za template, checkbox za internu napomenu
- Za approve: opcioni dropdown za verificationStatus
- Preview sadržaja sa side-by-side AI hints
- UX: nakon odluke, automatski prelazak na sljedeću stavku u queue-u; toast sa potvrdom

**Tehničke napomene:**

- Override prethodne odluke je rijetka ali bitna operacija — treba biti logovana sa razlogom. UI ne treba olakšavati override (ne stavljati ga pored primarnih akcija).
- Integration sa [E06](../e06-trust-tier-sistem.md): moderacijska odluka je "trigger point" za Trust Tier evaluaciju. Logika napredovanja/degradacije živi u [E06](../e06-trust-tier-sistem.md), ali se poziva iz E07 workflow-a.
- `changes_requested` listing se vraća korisniku ali ostaje u sistemu — korisnik ga može ispraviti i resubmitovati, ili ga ignorisati (timeout → auto-reject, BR-MOD-14).

**Testovi (MVP):**

- [ ] Approve listinga na pre-moderaciji → listing prelazi u `published`, vidljiv posjetiocima
- [ ] Approve listinga na post-moderaciji → listing ostaje vidljiv, `listingStatus` prelazi iz `published_under_review` u `published`
- [ ] Reject listinga → `listingStatus = rejected`, korisnik notificiran, razlog vidljiv
- [ ] Changes\_requested → `listingStatus = changes_requested`, korisnik dobija poruku, listing nevidljiv
- [ ] Reject bez razloga → validacijska greška
- [ ] Override prethodnog approve → listing ponovo u queue-u, audit log kreiran
- [ ] Nakon approve, Trust Tier evaluacija se pokreće za vlasnika listinga

**Wireframe referenca:** —

**Implementacijske napomene:**

- Razmotriti keyboard shortcut-ove za moderatorske akcije (npr. A za approve, R za reject) — značajno ubrzava rad.
- Template poruke se čuvaju na nivou tenanta — različiti gradovi mogu imati različite template-e.