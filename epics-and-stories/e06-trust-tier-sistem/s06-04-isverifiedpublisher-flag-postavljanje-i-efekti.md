---
id: S06-04
parent_epic: E06
linear_id: "CIT2-43"
phase: MVP
journey_milestones: [J-03, J-07]
type: fullstack
---

# S06-04 — isVerifiedPublisher flag — postavljanje i efekti

**Naslov:** isVerifiedPublisher flag — postavljanje i efekti

**Excerpt:** Korisnici na Tier 3 (Established) mogu dobiti `isVerifiedPublisher` flag koji automatski daje verified status svim njihovim listinzima. Ovo rješava problem samplinga — kad se ne pregleda svaki listing, verifikacija na nivou korisnika je konzistentnija od verifikacije po listingu.

**Phase:** MVP

**Journey milestones:** **J-03**, **J-07**

**User story:**  
Kao moderator sa `can_manage_trust_tier` permisijom,  
želim postaviti `isVerifiedPublisher` flag na korisniku koji je dokazao legitimitet,  
kako bi svi njegovi listinzi automatski dobili verified badge bez potrebe za pojedinačnom verifikacijom.

**Kontekst:** Na Tier 3 moderacija koristi sampling — ne pregleda se svaki listing. Verifikacija per listing bi bila nekonzistentna jer listinzi koji ne uđu u sampling nikad ne bi imali priliku za verified status. Flag prebacuje verifikaciju na nivo korisnika. Moderator odlučuje da li će tražiti dokument — to je poslovna odluka (npr. vlasnik restorana sa već verificiranim Place-om ne treba ponovo dokazivati legitimitet za evente). Flag se automatski uklanja ako korisnik padne ispod Tier 3. Detalji → **Ch.03, sekcija 3.3** (isVerifiedPublisher); **Ch.05, sekcija 5.6**.3.

**Acceptance criteria:**

- [ ] Moderator sa `can_manage_trust_tier` permisijom može postaviti `isVerifiedPublisher = true` na korisniku koji je na Tier 3 ili višem
- [ ] Pokušaj postavljanja flaga na korisniku ispod Tier 3 → validacijska greška
- [ ] Postavljanje flaga automatski daje `verificationStatus = verified` svim budućim listinzima tog korisnika
- [ ] Postavljanje flaga retroaktivno ažurira `verificationStatus = verified` na svim postojećim aktivnim listinzima korisnika (batch update)
- [ ] Uklanjanje flaga uklanja badge sa budućih objava, ali ne dira postojeće listinge
- [ ] Degradacija korisnika ispod Tier 3 automatski uklanja `isVerifiedPublisher` flag
- [ ] Automatsko uklanjanje flaga pri degradaciji ne dira `verificationStatus` na postojećim listinzima
- [ ] Staff sa ulogom `local_admin` može postaviti/ukloniti flag bez eksplicitne permisije
- [ ] Audit log bilježi postavljanje i uklanjanje flaga

**Backend Scope:**

- `PATCH /staff/users/{userId}/verified-publisher` — prima: `isVerifiedPublisher` (Boolean)
- Validacija: korisnik mora biti na Tier 3+ za postavljanje flaga
- Validacija permisija: `can_manage_trust_tier` ili `local_admin`
- Pri postavljanju: batch update svih aktivnih listinga korisnika → `verificationStatus = verified`
- Pri uklanjanju: samo update flaga na korisniku, postojeći listinzi ostaju nepromijenjeni
- Side effect u Trust Tier logici: degradacija ispod Tier 3 → automatski `isVerifiedPublisher = false`
- Audit log entry

**Frontend Scope:**

- UI: toggle/switch za `isVerifiedPublisher` na korisničkom profilu u Staff panelu
- Vidljiv samo moderatorima sa `can_manage_trust_tier` ili local\_admin-u
- Vizualni indikator da je flag aktivan (badge ili oznaka na profilu korisnika)
- Prikaz broja listinga koji će biti ažurirani pri postavljanju flaga
- UX: potvrda prije izvršenja ("Ovo će ažurirati X aktivnih listinga"), toast nakon uspjeha

**Tehničke napomene:**

- Batch update na listinzima pri postavljanju flaga može uticati na performanse za korisnike sa puno listinga. Razmotriti async obradu za veći broj.
- Cross-cutting sa [S06-03](s06-03-rucna-promjena-trust-tier-a.md): degradacija ispod Tier 3 triggeruje uklanjanje flaga. Logika treba biti centralizirana u Trust Tier servisu.
- Kreiranje novog listinga treba provjeriti `isVerifiedPublisher` flag na vlasniku i automatski postaviti `verificationStatus` ako je flag aktivan.

**Testovi (MVP):**

- [ ] Postavljanje flaga na korisniku Tier 3 → uspješno, svi aktivni listinzi dobiju verified
- [ ] Postavljanje flaga na korisniku Tier 1 → validacijska greška
- [ ] Uklanjanje flaga → budući listinzi su unverified, postojeći ostaju verified
- [ ] Degradacija sa Tier 3 na Tier 2 → flag se automatski uklanja
- [ ] Korisnik sa flagom kreira novi listing → listing automatski ima `verificationStatus = verified`
- [ ] Moderator bez permisije pokušava postaviti flag → odbijeno (403)

**Wireframe referenca:** —