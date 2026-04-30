---
id: S07-03
confluence_page_id: "250478672"
parent_epic: E07
linear_id: "CIT2-47"
phase: MVP
journey_milestones: [J-03]
type: fullstack
---

**Naslov:** AI content screening i scoring

**Excerpt:** Kada korisnik submituje sadržaj, sistem pokreće brzi AI scan koji analizira tekst i slike, dodjeljuje score za različite kategorije problema (hate speech, adult, violence, spam, kontakt info, duplikat), i na osnovu toga određuje risk level i prioritet u moderacijskom queue-u. AI ne donosi finalne odluke — služi kao pomoćni alat za moderatore.

**Phase:** MVP

**Journey milestones:** J-03

**User story:**  
Kao sistem,

želim automatski skenirati svaki submitovani sadržaj i dodijeliti mu score rizika po kategorijama,

kako bi moderatori vidjeli potencijalne probleme odmah i mogli efikasnije prioritizirati svoj rad.

**Kontekst:** AI screening se pokreće automatski pri svakom submitovanju listinga. Proces mora biti brz (max 3 sekunde) da ne blokira korisnikov flow. AI analizira tekst (naslov, opis) i slike, dodjeljuje score (0.0–1.0) za svaku kategoriju, i na osnovu toga računa ukupni risk level (LOW/MEDIUM/HIGH/CRITICAL). Rezultati se prikazuju moderatoru kao "hints" — korisni ali ne obavezujući. Detalji → **Ch.05**, sekcije 5.3.1–5.3.3.

**Acceptance criteria:**

- [ ] AI screening se pokreće automatski pri svakom submitovanju listinga (novo kreiranje ili resubmit nakon changes\_requested)
- [ ] AI analizira tekstualni sadržaj (naslov, opis) i priložene slike
- [ ] AI dodjeljuje nezavisne score (0.0–1.0) za kategorije: hate speech, adult content, violence, spam patterns, contact info, duplicate
- [ ] Na osnovu pojedinačnih score-ova, sistem računa ukupni risk level: LOW (svi < 0.3), MEDIUM (bilo koji 0.3–0.7), HIGH (bilo koji > 0.7), CRITICAL (više od 2 score > 0.7)
- [ ] AI rezultati se čuvaju kao metadata uz listing
- [ ] AI rezultati se prikazuju moderatoru u queue-u kao "hints" sa vizualnim indikatorima
- [ ] AI screening ne blokira kreiranje listinga — listing se kreira normalno, scan je async
- [ ] Screening završava u max 3 sekunde
- [ ] Moderator može pokrenuti ručni rescan (`/ai-screening/rescan`)
- [ ] Verzija AI modela se bilježi uz rezultate

**Backend Scope:**

- Async servis koji se pokreće pri submit-u listinga
- Analiza teksta: hate speech, violence, spam pattern detection, contact info extraction
- Analiza slika: adult content, violence detection
- Duplicate detection: sličnost sa postojećim sadržajem
- Storage AI rezultata: `listingId`, `scanDate`, `scores` (Object), `riskLevel` (Enum), `flags` (List), `suggestedAction`, `version`
- `GET /api/moderation/listings/{id}/ai-screening` — dohvat AI rezultata
- `POST /api/moderation/listings/{id}/ai-screening/rescan` — ponovi scan
- Cache sloj: TTL 24h, invalidacija pri novom scanu

**Frontend Scope:**

- Prikaz AI hints u moderatorskom queue-u: ikone/boje po kategoriji i score-u
- Vizualni indikatori: crveno za > 0.7, žuto za 0.3–0.7, zeleno za < 0.3
- Suggested action tekst (npr. "Review carefully", "Likely spam")
- AI hints panel uz preview sadržaja u detaljnom pregledu stavke

**Tehničke napomene:**

- AI screening je async — listing se kreira i (za Tier 2+) objavljuje odmah, AI rezultati dolaze naknadno i ažuriraju prioritet u queue-u.
- Za MVP, AI servis može biti simplificiran (keyword matching + basic image classification) sa planom za sofisticiraniju implementaciju u kasnijim fazama.
- Thresholds za kategorije su konfiguracijski parametri — treba ih tune-ati na osnovu false positive rate-a.
- Contact info detection treba prepoznati telefone i emaile u opisu (koji trebaju biti u posebnim poljima).

**Testovi (MVP):**

- [ ] Listing sa čistim sadržajem → svi score < 0.3, risk level LOW
- [ ] Listing sa sumnjivim tekstom → odgovarajući score > 0.3, risk level MEDIUM ili HIGH
- [ ] Listing sa više problematičnih kategorija → risk level CRITICAL
- [ ] AI rezultati vidljivi moderatoru u queue-u
- [ ] Rescan nakon izmjene sadržaja → novi rezultati zamjenjuju stare
- [ ] AI screening završava unutar 3 sekunde

**Wireframe referenca:** —

**Implementacijske napomene:**

- Za duplicate detection, razmotriti cosine similarity na vektorizovanom tekstu — ali za MVP, simpleiji pristup (n-gram matching) može biti dovoljan.
- Contact info detection: regex za telefone i email adrese u tekstu opisa.