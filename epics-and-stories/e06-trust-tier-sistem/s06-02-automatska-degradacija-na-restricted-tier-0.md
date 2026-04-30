---
id: S06-02
confluence_page_id: "251461679"
parent_epic: E06
linear_id: "CIT2-41"
phase: MVP
journey_milestones: [J-03, J-08]
type: backend-only
---

# S06-02 — Automatska degradacija na Restricted (Tier 0)

**Naslov:** Automatska degradacija na Restricted (Tier 0)

**Excerpt:** Kada korisnik dosegne konfigurisani prag odbijenih objava u definisanom vremenskom prozoru, sistem ga automatski degradira na Tier 0 (Restricted) i kreira review stavku u moderacijskom queue-u. Ovo je sigurnosna mreža koja štiti platformu i izvan radnog vremena — ali uvijek podliježe ljudskom pregledu.

**Phase:** MVP

**Journey milestones:** **J-03**, **J-08**

**User story:**  
Kao sistem,  
želim automatski degradirati korisnika na Tier 0 kada dosegne prag odbijenih objava,  
kako bi platforma bila zaštićena od korisnika koji ponavljano krše pravila, čak i kada moderatori nisu dostupni.

**Kontekst:** Automatska degradacija se triggeruje kada korisnik ima `TIER_REJECTED_THRESHOLD` odbijenih objava unutar `TIER_REJECTED_WINDOW_DAYS` dana. Ovo važi za korisnike na bilo kojem tier-u (1–4). Svaka automatska degradacija kreira review stavku u moderacijskom queue-u — moderator mora potvrditi ili revertovati odluku. Detalji → **Ch.03, sekcija 3.4** (Degradacija); **Ch.05, sekcija 5.1**.3.

**Acceptance criteria:**

- [ ] Sistem automatski degradira korisnika na Tier 0 kada ima `TIER_REJECTED_THRESHOLD` rejected objava unutar `TIER_REJECTED_WINDOW_DAYS` dana
- [ ] Degradacija važi za korisnike na bilo kojem tier-u (1, 2, 3 ili 4)
- [ ] Automatska degradacija kreira stavku "Trust Tier Auto-Degradation Review" u moderacijskom queue-u
- [ ] Review stavka sadrži: korisnikove podatke, prethodni tier, razlog degradacije, listu rejected objava koje su triggerovale degradaciju
- [ ] Moderator može potvrditi degradaciju (korisnik ostaje na Tier 0)
- [ ] Moderator može revertovati degradaciju (korisnik se vraća na prethodni tier)
- [ ] `TIER_REJECTED_THRESHOLD` i `TIER_REJECTED_WINDOW_DAYS` su konfiguracijski parametri
- [ ] Brojač se računa na osnovu rejected odluka u definisanom vremenskom prozoru (sliding window)
- [ ] Ako je korisnik već na Tier 0, nova degradacija se ne triggeruje (ali se i dalje loguje)

**Backend Scope:**

- Servis/metoda `EvaluateAutoDegradation(userId)` — poziva se nakon svake reject odluke
- Dohvat broja rejected odluka u zadnjih `TIER_REJECTED_WINDOW_DAYS` dana za korisnika
- Ako prag dostignut: update `trustTier = 0`, kreiranje review stavke u queue-u
- Konfiguracijski parametri: `TIER_REJECTED_THRESHOLD` (preporučeno: 3), `TIER_REJECTED_WINDOW_DAYS` (preporučeno: 30)
- `POST /api/moderation/reviews/{id}/confirm` — potvrda degradacije
- `POST /api/moderation/reviews/{id}/revert` — revert na prethodni tier

**Tehničke napomene:**

- Sliding window za rejected odluke: gledamo zadnjih N dana od trenutne odluke, ne kalendarski period.
- Review stavka koristi isti queue mehanizam kao moderacija listinga, ali sa drugačijim tipom (`type: trust_tier_auto_degradation`). Queue infrastruktura se gradi u [E07](../e07-moderacijski-workflow-i-ai-screening.md).
- Audit log treba zabilježiti: automatsku degradaciju, ko je pregledao, i da li je potvrđena ili revertovana.

**Testovi (MVP):**

- [ ] Korisnik na Tier 2 sa 3 rejected u zadnjih 30 dana → degradiran na Tier 0, review stavka kreirana
- [ ] Korisnik na Tier 3 sa 2 rejected u zadnjih 30 dana → nije degradiran (ispod praga)
- [ ] Korisnik na Tier 0 sa dodatnim rejected → ne triggeruje novu degradaciju
- [ ] Moderator potvrdi review → korisnik ostaje na Tier 0
- [ ] Moderator revertuje review → korisnik se vraća na prethodni tier
- [ ] Rejected objava starija od 30 dana → ne broji se u prozor

**Wireframe referenca:** —

**Implementacijske napomene:**

- Čuvanje prethodnog tier-a pri degradaciji omogućava revert. Razmotriti `previousTrustTier` polje ili log entry.
- Review stavke u queue-u trebaju imati viši prioritet od standardne post-moderacije jer se radi o sistemskoj odluci.