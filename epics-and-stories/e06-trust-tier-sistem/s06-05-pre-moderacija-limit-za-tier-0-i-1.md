---
id: S06-05
confluence_page_id: "251494410"
parent_epic: E06
linear_id: "CIT2-44"
phase: MVP
journey_milestones: [J-02, J-03]
type: fullstack
---

# S06-05 — Pre-moderacija limit za Tier 0 i 1

**Naslov:** Pre-moderacija limit za Tier 0 i 1

**Excerpt:** Korisnici na Tier 0 i 1 (pre-moderacija) imaju ograničen broj objava koje mogu čekati pregled istovremeno. Ovo sprečava flood — korisnik ne može poslati 50 listinga odjednom i zagušiti moderacijski queue.

**Phase:** MVP

**Journey milestones:** **J-02**, **J-03**

**User story:**  
Kao sistem,  
želim ograničiti broj istovremenih objava koje čekaju moderaciju za korisnike na pre-moderaciji,  
kako bi moderacijski queue ostao upravljiv i korisnici bili poticani da kreiraju kvalitetan sadržaj umjesto masovnog postanja.

**Kontekst:** Korisnici na Tier 0 i 1 su na pre-moderaciji — svaki sadržaj čeka odobrenje prije nego postane vidljiv. Bez limita, korisnik bi mogao poslati veliki broj listinga odjednom, zagušiti queue i otežati rad moderatorima. Parametar `TIER_PRE_MOD_MAX_PENDING` definira maksimalan broj objava u statusu `in_review` istovremeno. Korisnik mora sačekati odluku na jednoj od postojećih objava prije slanja nove. Detalji → **Ch.03, sekcija 3.4**; **Ch.05, sekcija 5.1**.3.

**Acceptance criteria:**

- [ ] Korisnici na Tier 0 i 1 ne mogu imati više od `TIER_PRE_MOD_MAX_PENDING` listinga u statusu `in_review` istovremeno
- [ ] Pokušaj submitovanja novog listinga kada je limit dostignut → jasna greška sa porukom koliko objava čeka i da treba sačekati
- [ ] Limit se provjerava pri tranziciji listinga u `in_review` status (submit za pregled)
- [ ] Korisnici na Tier 2+ nisu ograničeni ovim limitom (post-moderacija)
- [ ] `TIER_PRE_MOD_MAX_PENDING` je konfiguracijski parametar
- [ ] Kada moderator donese odluku (approve/reject/changes\_requested) na jednoj od pending objava, korisnik može submitovati novu
- [ ] Listing koji je u statusu `changes_requested` (korisnik ga ispravlja) ne broji se u pending limit

**Backend Scope:**

- Validacija pri `POST /listings/{id}/submit` (ili ekvivalentni endpoint za slanje na pregled)
- Dohvat broja listinga korisnika u statusu `in_review`
- Ako count >= `TIER_PRE_MOD_MAX_PENDING` → reject request sa odgovarajućim error kodom
- Konfiguracijski parametar: `TIER_PRE_MOD_MAX_PENDING` (preporučena početna vrijednost: 3)

**Frontend Scope:**

- Prikaz broja slobodnih "slotova" za objavu na korisničkom dashboardu (npr. "2 od 3 objave čekaju pregled")
- Jasna poruka kada je limit dostignut: šta se dešava, koliko čeka, i šta korisnik treba raditi
- Submit dugme disabled ili sa tooltipom kada je limit dostignut
- UX: kada moderator odobri jednu objavu, UI se osvježava i korisnik može nastaviti

**Tehničke napomene:**

- Limit se primjenjuje samo na `in_review` status — draft listinzi (još nisu submitovani) se ne broje.
- `changes_requested` listinzi se ne broje jer je korisnik na njima aktivan — cilj je spriječiti flood, ne kažnjavati aktivnu saradnju.
- Razmisliti o race condition-u: dva simultana submita od istog korisnika. Potrebna atomična provjera.

**Testovi (MVP):**

- [ ] Korisnik Tier 1 sa 3 listinga u `in_review` → submit novog odbijen sa jasnom porukom
- [ ] Korisnik Tier 1 sa 2 listinga u `in_review` → submit uspješan
- [ ] Korisnik Tier 0 sa 3 listinga u `in_review` → submit odbijen (isti limit važi)
- [ ] Korisnik Tier 2 sa 10 pending listinga → submit uspješan (nema limita za post-mod)
- [ ] Moderator odobri jedan listing u `in_review` → korisnik može submitovati novi
- [ ] Listing u `changes_requested` statusu → ne broji se u pending limit

**Wireframe referenca:** —

**Implementacijske napomene:**

- Početna vrijednost od 3 je konzervativna. Može se povećati nakon launcha ako se pokaže da je previše restriktivno.
- Poruka korisniku treba biti pozitivna: "Vaše objave čekaju pregled — moderator će ih pogledati uskoro" umjesto "Dostigli ste limit".