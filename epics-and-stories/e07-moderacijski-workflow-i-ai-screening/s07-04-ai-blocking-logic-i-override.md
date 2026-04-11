# S07-04 — AI blocking logic i override

**Naslov:** AI blocking logic i override

**Excerpt:** U ekstremnim slučajevima (hate speech, explicit nasilje, ilegalni sadržaj), AI može blokirati publikaciju sadržaja bez obzira na Trust Tier korisnika. Blokirani sadržaj ulazi u Urgent queue za hitni pregled. Moderator mora ručno pregledati i može override-ati AI odluku ako je bila false positive.

**Phase:** MVP

**Journey milestones:** J-03

**User story:**  
Kao sistem,  
želim automatski blokirati publikaciju sadržaja kada AI detektuje ekstreman rizik,  
kako bi platforma bila zaštićena od očigledno štetnog sadržaja čak i prije nego moderator stigne pogledati.

**Kontekst:** AI blocking se aktivira kada score za kritičnu kategoriju (hate speech, adult, violence, illegal) premaši konfigurisani blocking threshold. Ovo je "sigurnosna mreža" — sadržaj se ne objavljuje, listing prelazi u `hidden_by_system` i ulazi u Urgent queue za hitni pregled. Važno: AI ne donosi finalnu odluku — moderator mora pregledati i eksplicitno odobriti ili odbaciti. Korisnici višeg tiera dobijaju transparentniju poruku nego novi korisnici. Detalji → Ch.05, sekcije 5.3.4–5.3.6.

**Acceptance criteria:**

- [ ] AI automatski blokira publikaciju kada score premaši blocking threshold za kritične kategorije
- [ ] Blocking thresholds su konfiguracijski parametri po kategoriji (`AI_BLOCK_HATE_THRESHOLD`, itd.)
- [ ] Hate speech, adult content, violence explicit, illegal content — blocking važi za sve korisnike (Tier 0–4)
- [ ] Spam certainty — blocking važi samo za Tier 0 i 1 (pre-moderacija)
- [ ] Blokirani listing prelazi u `listingStatus = hidden_by_system`, nije vidljiv javno bez obzira na Trust Tier
- [ ] Blokirani listing ulazi u Urgent queue za hitni pregled
- [ ] CRITICAL risk level (više od 2 score > 0.7) zahtijeva pregled moderatora sa `can_manage_trust_tier` permisijom
- [ ] Moderator može override-ati AI blocking (`POST /api/moderation/listings/{id}/ai-override`)
- [ ] Override zahtijeva razlog i bilježi se u audit log
- [ ] Korisnik Tier 2+ dobija poruku: "Vaš sadržaj je automatski zadržan — moderator će pregledati u roku od 30 minuta"
- [ ] Korisnik Tier 0/1 dobija poruku: "Vaš sadržaj je poslan na pregled"
- [ ] Blokirani listing zahtijeva eksplicitno ljudsko odobrenje — ne može se automatski vratiti u prethodni status

**Backend Scope:**

- Logika u AI screening servisu: nakon scoring-a, provjera blocking thresholds
- Ako threshold premaši: listing prelazi u `listingStatus = hidden_by_system`
- Kreiranje Urgent stavke u moderacijskom queue-u
- `POST /api/moderation/listings/{id}/ai-override` — prima: `reason` (obavezno), `action` (approve/reject)
- Konfiguracijski parametri: `AI_BLOCK_HATE_THRESHOLD` (0.95), `AI_BLOCK_ADULT_THRESHOLD` (0.95), `AI_BLOCK_VIOLENCE_THRESHOLD` (0.95), `AI_BLOCK_ILLEGAL_THRESHOLD` (0.90), `AI_BLOCK_SPAM_THRESHOLD` (0.98)
- Side effect: notifikacija korisniku (različita po tier-u)

**Frontend Scope:**

- Moderator: vizualni indikator da je stavka AI-blocked (crveni banner u queue-u)
- Override UI: dugme "Override AI Block" sa obaveznim razlogom
- Za CRITICAL stavke: vizualni indikator da zahtijeva `can_manage_trust_tier` permisiju
- Korisnik: poruka u UI-u da je sadržaj zadržan za pregled (različita po tier-u)

**Tehničke napomene:**

- AI blocking je dio istog async screening procesa iz S07-03 — ne zahtijeva odvojeni poziv.
- Blocking thresholds su namjerno visoki (0.90–0.98) da minimiziraju false positives. Bolje je propustiti nešto u queue na normalan pregled nego blokirati legitimni sadržaj.
- CRITICAL risk level sa zahtjevom za `can_manage_trust_tier` je dodatna sigurnosna mjera — ne želi se da junior moderator sam odlučuje o potencijalno ilegalnom sadržaju.

**Testovi (MVP):**

- [ ] Listing sa hate speech score 0.96 → blokiran, `listingStatus = hidden_by_system`, ulazi u Urgent queue
- [ ] Listing sa hate speech score 0.93 → nije blokiran (ispod threshold-a 0.95), ali ima HIGH risk
- [ ] Blokirani listing Tier 4 korisnika → također blokiran (važi za sve)
- [ ] Spam score 0.99 za Tier 2 korisnika → nije blokiran (spam blocking samo za pre-mod)
- [ ] Moderator override AI block → listing prelazi u `published`, audit log kreiran
- [ ] CRITICAL stavka → vidljiva samo moderatorima sa `can_manage_trust_tier`
- [ ] Pokušaj publikacije blokiranog listinga bez override-a → odbijeno

**Wireframe referenca:** —