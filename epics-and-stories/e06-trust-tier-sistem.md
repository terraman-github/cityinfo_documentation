---
id: E06
confluence_page_id: "250478652"
linear_id: ""
phase: MVP
journey_milestones: [J-03, J-08]
personas: [Marko, Lejla, Emir, Amra]
story_count: 5
---

**Naslov:** Trust Tier sistem

**Excerpt:** Trust Tier je mehanizam koji automatski prilagođava nivo moderacije prema ponašanju korisnika — umjesto binarnog "vjerujemo / ne vjerujemo", sistem prepoznaje da se povjerenje gradi kroz konzistentno kvalitetan sadržaj. Ovaj epic pokriva kompletnu backend logiku za evaluaciju napredovanja, automatsku i ručnu degradaciju, `isVerifiedPublisher` flag, te ograničenja za pre-moderaciju. Bez Trust Tier-a, moderacijski workflow nema osnovu na kojoj donosi odluke.

**Scope — šta ulazi:**

- Automatska evaluacija napredovanja (Tier 1→2, Tier 2→3) sa parametriziranim pragovima
- Automatska degradacija na Tier 0 (Restricted) sa kreiranjem review stavke u moderacijskom queue-u
- Ručna promjena Trust Tier-a (uključujući Tier 4 postavljanje i degradaciju na Tier 0 sa `can_manage_trust_tier` permisijom)
- `isVerifiedPublisher` flag — postavljanje, uklanjanje, retroaktivni batch update na listinge
- Pre-moderacija limit (`TIER_PRE_MOD_MAX_PENDING`) za Tier 0 i 1

**Scope — šta NE ulazi:**

- Moderacijski queue UI i workflow (→ [E07](e07-moderacijski-workflow-i-ai-screening.md))
- AI screening logika (→ [E07](e07-moderacijski-workflow-i-ai-screening.md))
- Sampling logika za post-moderaciju (→ [E07](e07-moderacijski-workflow-i-ai-screening.md), dio moderacijskog workflow-a)
- Staff panel i autentifikacija (→ [E13](e13-staff-panel-autentifikacija-i-upravljanje-osobljem.md))
- Blokiranje korisnika i efekti na sadržaj (→ [E07](e07-moderacijski-workflow-i-ai-screening.md), moderatorske akcije)
- Verifikacija vlasništva — upload dokumenata, document workflow (→ [E08](e08-komunikacija-uz-listing-i-dokumenti.md))

**Persone:** Marko (organizator), Lejla (posjetioc koja postaje kreator), Emir (moderator), Amra (operatorka)

**Journey milestones:** J-03 (Moderacija sadržaja), **J-08** (Operativno upravljanje)

**Phase:** MVP

**Dokumentacijska referenca:** Ch.03, sekcija 3.4 (Trust Tier sistem); **Ch.05, sekcija 5.1**.3 (Trust Tier u kontekstu moderacije)

**Tehničke napomene:**

- Trust Tier je atribut na User entitetu (`trustTier`, Number 0–4). [E01](e01-korisnicka-registracija-i-profil.md) je već definisao ovaj atribut — ovaj epic dodaje logiku oko njega.
- Svi pragovi su konfiguracijski parametri (ne hardkodirani) — promjena ne zahtijeva deploy.
- Evaluacija napredovanja se triggeruje nakon svake moderatorske odluke (approve/reject), što znači da [E07](e07-moderacijski-workflow-i-ai-screening.md) (moderacijski workflow) poziva Trust Tier logiku. Zavisnost je jednosmjerna: moderacija poziva Trust Tier evaluaciju, ne obrnuto.
- `isVerifiedPublisher` flag direktno utiče na `verificationStatus` listinga — zahtijeva koordinaciju sa Listing entitetom iz [E02](e02-listing-crud-i-lifecycle.md).
- Automatska degradacija kreira stavku u moderacijskom queue-u — queue infrastruktura dolazi iz [E07](e07-moderacijski-workflow-i-ai-screening.md), ali E06 definira payload i uslove kreiranja.

**Success metrika:** Korisnik koji konzistentno objavljuje kvalitetan sadržaj automatski napreduje kroz tier-ove bez ikakve ručne intervencije. Moderator može u manje od 30 sekundi promijeniti Trust Tier korisnika i vidjeti efekte odmah.

* * *

<a id="storije-u-ovom-epicu"></a>

## Storije u ovom epicu

| #   | Naslov | Phase | Journey |
| --- | --- | --- | --- |
| [S06-01](e06-trust-tier-sistem/s06-01-automatska-evaluacija-trust-tier-napredovanja.md) | Automatska evaluacija Trust Tier napredovanja | MVP | **J-03** |
| [S06-02](e06-trust-tier-sistem/s06-02-automatska-degradacija-na-restricted-tier-0.md) | Automatska degradacija na Restricted (Tier 0) | MVP | **J-03**, **J-08** |
| [S06-03](e06-trust-tier-sistem/s06-03-rucna-promjena-trust-tier-a.md) | Ručna promjena Trust Tier-a | MVP | **J-03**, **J-08** |
| [S06-04](e06-trust-tier-sistem/s06-04-isverifiedpublisher-flag-postavljanje-i-efekti.md) | isVerifiedPublisher flag — postavljanje i efekti | MVP | **J-03**, **J-07** |
| [S06-05](e06-trust-tier-sistem/s06-05-pre-moderacija-limit-za-tier-0-i-1.md) | Pre-moderacija limit za Tier 0 i 1 | MVP | **J-02**, **J-03** |