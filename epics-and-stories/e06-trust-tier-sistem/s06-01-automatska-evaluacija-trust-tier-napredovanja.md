---
id: S06-01
parent_epic: E06
linear_id: "CIT2-40"
phase: MVP
journey_milestones: [J-03]
type: backend-only
---

# S06-01 — Automatska evaluacija Trust Tier napredovanja

**Naslov:** Automatska evaluacija Trust Tier napredovanja

**Excerpt:** Sistem automatski provjerava da li korisnik ispunjava uslove za napredovanje na viši Trust Tier nakon svake moderatorske odluke. Ovo je osnova Trust Tier mehanizma — bez evaluacije, korisnici bi zauvijek ostali na Tier 1 i svaki sadržaj bi čekao ručno odobrenje.

**Phase:** MVP

**Journey milestones:** **J-03**

**User story:**  
Kao sistem,  
želim automatski evaluirati da li korisnik ispunjava uslove za napredovanje kroz Trust Tier nivoe,  
kako bi korisnici koji konzistentno objavljuju kvalitetan sadržaj automatski dobili manje restriktivnu moderaciju.

**Kontekst:** Evaluacija se pokreće nakon svake moderatorske odluke (approve ili reject) na listingu. Sistem provjerava tri parametrizirana uslova istovremeno: minimalni broj odobrenih objava, minimalni procenat uspješnosti, i minimalnu starost računa. Sva tri moraju biti ispunjena da bi napredovanje bilo okidano. `changes_requested` se ne broji — samo finalna odluka po listingu utiče na statistiku. Detalji o pragovima i logici → **Ch.03, sekcija 3.4**.

**Acceptance criteria:**

- [ ] Nakon approve ili reject odluke moderatora, sistem evaluira Trust Tier korisnika
- [ ] Napredovanje 1→2 se okida kada su sva tri uslova ispunjena istovremeno: `TIER1_MIN_APPROVED`, `TIER1_MIN_SUCCESS_RATE`, `TIER1_MIN_ACCOUNT_AGE_DAYS`
- [ ] Napredovanje 2→3 se okida kada su sva tri uslova ispunjena istovremeno: `TIER2_MIN_APPROVED`, `TIER2_MIN_SUCCESS_RATE`, `TIER2_MIN_ACCOUNT_AGE_DAYS`
- [ ] Procenat uspješnosti računa samo finalne odluke po listingu (approved / ukupno finalizovanih)
- [ ] `changes_requested` ne utiče na procenat uspješnosti — broji se samo finalna odluka
- [ ] Listing koji je još u `changes_requested` statusu (nema finalne odluke) se ne broji u statistiku
- [ ] Svi pragovi su konfiguracijski parametri koji se mogu mijenjati bez deploya
- [ ] Pri napredovanju, `trustTier` na User entitetu se ažurira
- [ ] Napredovanje se ne okida za Tier 0 (Restricted) — izlaz iz Restricted-a je samo ručni
- [ ] Napredovanje na Tier 4 ne postoji automatski — Tier 4 je isključivo ručno

**Backend Scope:**

- Servis/metoda `EvaluateTrustTierProgression(userId)` — poziva se iz moderacijskog workflow-a nakon svake finalne odluke
- Dohvat korisnikove statistike: broj approved, broj finalizovanih, starost računa
- Provjera sva tri uslova prema konfiguracijskim parametrima
- Update `trustTier` na User entitetu ako su uslovi ispunjeni
- Konfiguracijski parametri: `TIER1_MIN_APPROVED`, `TIER1_MIN_SUCCESS_RATE`, `TIER1_MIN_ACCOUNT_AGE_DAYS`, `TIER2_MIN_APPROVED`, `TIER2_MIN_SUCCESS_RATE`, `TIER2_MIN_ACCOUNT_AGE_DAYS`

**Tehničke napomene:**

- Evaluacija treba biti idempotentna — ako se pozove dva puta za istog korisnika, rezultat je isti.
- Statistika se računa iz moderacijskih odluka, ne iz listing statusa — jer listing može promijeniti status nakon moderacije (npr. expired). Relevantno je šta je moderator odlučio.
- Preporučene početne vrijednosti su u **Ch.03, sekcija 3.4**, ali su samo polazna tačka.

**Testovi (MVP):**

- [ ] Korisnik sa 5 approved, 0 rejected, račun stariji od 7 dana → napreduje 1→2
- [ ] Korisnik sa 4 approved, 1 rejected (80%), račun stariji od 7 dana → na granici, napreduje 1→2
- [ ] Korisnik sa 4 approved, 2 rejected (67%), račun stariji od 7 dana → ne napreduje (procenat ispod 80%)
- [ ] Korisnik sa 5 approved, 0 rejected, račun star 3 dana → ne napreduje (starost računa)
- [ ] Korisnik na Tier 0 sa ispunjenim uslovima → ne napreduje automatski
- [ ] `changes_requested` → `approved` broji se kao 1 approved, ne kao 2 odluke
- [ ] Listing u `changes_requested` bez finalne odluke → ne ulazi u statistiku

**Wireframe referenca:** —

**Implementacijske napomene:**

- Razmisliti o keširanju korisnikove statistike da se ne računa iz scratch-a pri svakoj evaluaciji — ali validirati da keš nije stale nakon moderatorske odluke.
- Logika za `changes_requested` neutralnost: pratiti samo finalne odluke (approved/rejected) per listing, ignorisati međukorake.