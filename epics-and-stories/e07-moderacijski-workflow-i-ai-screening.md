# E07 — Moderacijski workflow i AI screening

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

- Trust Tier evaluacija i degradacija (→ E06 — ali E07 *poziva* E06 logiku nakon svake odluke)
- Staff panel UI shell, autentifikacija, CRUD osoblja (→ E13)
- Verifikacija vlasništva i dokumenti (→ E08)
- Blokiranje korisnika (→ dio E07 kao moderatorska akcija, ali detaljnija logika u E13)
- Template poruke i komunikacija sa korisnicima (→ E08)
- Instant block logika (→ E13, dio Staff panel funkcionalnosti)
- Display advertising moderacija (→ E11)

**Persone:** Emir (moderator), Amra (operatorka), Marko (organizator — čeka odobrenje)

**Journey milestones:** J-03 (Moderacija sadržaja)

**Phase:** MVP

**Dokumentacijska referenca:** Ch.05, sekcije 5.2 (Queue i workflow), 5.3 (AI Screening), 5.4 (Moderatorske akcije — bazne), 5.7 (API Endpoints)

**Tehničke napomene:**

- Moderacijski queue je centralna infrastruktura koju koriste i E06 (review stavke za auto-degradaciju) i budući epici (E08 za komunikaciju, E11 za display ads).
- AI screening je async proces — ne blokira kreiranje listinga, ali može blokirati publikaciju (`aiBlockingFlag`).
- E07 zavisi od E02 (Listing entitet i lifecycle) i E06 (Trust Tier logika za određivanje pre/post moderacije).
- SLA metrike (2h za pre-mod, 8h za post-mod) su ciljevi, ne enforcement — nema automatskog odobravanja.

**Success metrika:** Moderator može pregledati, odlučiti i finalizirati listing u manje od 2 minute. AI screening hvata >90% očigledno problematičnog sadržaja (hate speech, explicit content) i ispravno priorizira queue.

* * *

<a id="storije-u-ovom-epicu"></a>

## Storije u ovom epicu

| #   | Naslov | Phase | Journey |
| --- | --- | --- | --- |
| S07-01 | Moderacijski queue — struktura, prioritizacija i claim/release | MVP | J-03 |
| S07-02 | Moderatorske odluke (approve, reject, changes\_requested) | MVP | J-03 |
| S07-03 | AI content screening i scoring | MVP | J-03 |
| S07-04 | AI blocking logic i override | MVP | J-03 |
| S07-05 | Sampling logika za post-moderaciju | MVP | J-03 |
| S07-06 | Moderacija editovanog sadržaja | MVP | J-03 |