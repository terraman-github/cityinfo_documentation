---
id: E07
confluence_page_id: "251265065"
linear_id: ""
phase: MVP
journey_milestones: [J-03]
personas: [Emir, Amra, Marko]
story_count: 6
---

**Naslov:** Moderacijski workflow i AI screening

**Excerpt:** Moderacija je srce sistema kvaliteta — osigurava da korisnici dobijaju tačan, koristan i primjeren sadržaj. Ovaj epic pokriva kompletni moderacijski pipeline: od trenutka kada korisnik submituje listing, preko AI screening-a koji prioritizira queue, do moderatorskih odluka i njihovih efekata. AI pomaže ali ne zamjenjuje ljudske odluke — osim u ekstremnim slučajevima gdje automatski blokira očigledno problematičan sadržaj.

**Scope — šta ulazi:**

- Moderacijski queue — struktura, prioritizacija, claim/release mehanizam
- Moderatorske odluke (approve, reject, changes\_requested) sa efektima na listing lifecycle
- AI content screening — analiza teksta i slika, scoring po kategorijama, risk level
- AI blocking logic — automatsko blokiranje publikacije u ekstremnim slučajevima
- Sampling logika za post-moderaciju (Tier 2, 3, 4)
- Moderacija editovanog sadržaja (različito ponašanje po tier-u)

**Scope — šta NE ulazi:**

- Trust Tier evaluacija i degradacija (→ [E06](e06-trust-tier-sistem.md) — ali E07 *poziva* [E06](e06-trust-tier-sistem.md) logiku nakon svake odluke)
- Staff panel UI shell, autentifikacija, CRUD osoblja (→ [E13](e13-staff-panel-autentifikacija-i-upravljanje-osobljem.md))
- Verifikacija vlasništva i dokumenti (→ [E08](e08-komunikacija-uz-listing-i-dokumenti.md))
- Blokiranje korisnika (→ dio E07 kao moderatorska akcija, ali detaljnija logika u [E13](e13-staff-panel-autentifikacija-i-upravljanje-osobljem.md))
- Template poruke i komunikacija sa korisnicima (→ [E08](e08-komunikacija-uz-listing-i-dokumenti.md))
- Instant block logika (→ [E13](e13-staff-panel-autentifikacija-i-upravljanje-osobljem.md), dio Staff panel funkcionalnosti)
- Display advertising moderacija (→ [E11](e11-display-oglasavanje-mvp.md))

**Persone:** Emir (moderator), Amra (operatorka), Marko (organizator — čeka odobrenje)

**Journey milestones:** J-03 (Moderacija sadržaja)

**Phase:** MVP

**Dokumentacijska referenca:** Ch.05, sekcije 5.2 (Queue i workflow), 5.3 (AI Screening), 5.4 (Moderatorske akcije — bazne), 5.7 (API Endpoints)

**Tehničke napomene:**

- Moderacijski queue je centralna infrastruktura koju koriste i [E06](e06-trust-tier-sistem.md) (review stavke za auto-degradaciju) i budući epici ([E08](e08-komunikacija-uz-listing-i-dokumenti.md) za komunikaciju, [E11](e11-display-oglasavanje-mvp.md) za display ads).
- AI screening je async proces — ne blokira kreiranje listinga, ali može blokirati publikaciju (`aiBlockingFlag`).
- E07 zavisi od [E02](e02-listing-crud-i-lifecycle.md) (Listing entitet i lifecycle) i [E06](e06-trust-tier-sistem.md) (Trust Tier logika za određivanje pre/post moderacije).
- SLA metrike (2h za pre-mod, 8h za post-mod) su ciljevi, ne enforcement — nema automatskog odobravanja.

**Success metrika:** Moderator može pregledati, odlučiti i finalizirati listing u manje od 2 minute. AI screening hvata >90% očigledno problematičnog sadržaja (hate speech, explicit content) i ispravno priorizira queue.

* * *

<a id="storije-u-ovom-epicu"></a>

## Storije u ovom epicu

| #   | Naslov | Phase | Journey |
| --- | --- | --- | --- |
| [S07-01](e07-moderacijski-workflow-i-ai-screening/s07-01-moderacijski-queue-struktura-prioritizacija-i-claim-release.md) | Moderacijski queue — struktura, prioritizacija i claim/release | MVP | **J-03** |
| [S07-02](e07-moderacijski-workflow-i-ai-screening/s07-02-moderatorske-odluke-approve-reject-changes_requested.md) | Moderatorske odluke (approve, reject, changes\_requested) | MVP | **J-03** |
| [S07-03](e07-moderacijski-workflow-i-ai-screening/s07-03-ai-content-screening-i-scoring.md) | AI content screening i scoring | MVP | **J-03** |
| [S07-04](e07-moderacijski-workflow-i-ai-screening/s07-04-ai-blocking-logic-i-override.md) | AI blocking logic i override | MVP | **J-03** |
| [S07-05](e07-moderacijski-workflow-i-ai-screening/s07-05-sampling-logika-za-post-moderaciju.md) | Sampling logika za post-moderaciju | MVP | **J-03** |
| [S07-06](e07-moderacijski-workflow-i-ai-screening/s07-06-moderacija-editovanog-sadrzaja.md) | Moderacija editovanog sadržaja | MVP | **J-03** |