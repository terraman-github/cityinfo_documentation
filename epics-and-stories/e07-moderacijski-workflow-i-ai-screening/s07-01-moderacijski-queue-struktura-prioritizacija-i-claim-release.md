---
id: S07-01
confluence_page_id: "251363387"
title: "S07-01 — Moderacijski queue — struktura, prioritizacija i claim/release"
parent_epic: E07
linear_id: "CIT2-45"
phase: MVP
journey_milestones: [J-03]
type: fullstack
---

**Naslov:** Moderacijski queue — struktura, prioritizacija i claim/release

**Excerpt:** Queue je centralno mjesto gdje moderatori vide sve što čeka pregled. Sadržaj nije samo lista — prioritiziran je tako da najhitnije stvari budu na vrhu. Moderator može "preuzeti" stavku (claim) da drugi ne rade na istoj, i "pustiti" je (release) ako ne može završiti.

**Phase:** MVP

**Journey milestones:** J-03

**User story:**  
Kao moderator,

želim vidjeti prioritiziranu listu sadržaja koji čeka moderaciju i preuzeti stavke za pregled,

kako bih efikasno radio bez da stalno odlučujem "šta sljedeće" i bez rizika da dva moderatora rade na istom sadržaju.

**Kontekst:** Queue se dijeli u četiri zone prema prioritetu: Urgent (AI blocking flag), High Priority (score > 75), Normal Priority (score 40–75), Low Priority (score < 40). Pored sadržaja za moderaciju, u queue ulaze i sistemske stavke: Trust Tier Auto-Degradation Review i Instant Block Review. Prioritizacija koristi različite formule za pre-moderaciju i post-moderaciju. Detalji o prioritizaciji → **Ch.05**, sekcije 5.2.1–5.2.2.

**Acceptance criteria:**

- [ ] Queue prikazuje listu sadržaja koji čeka moderaciju, sortiranu po prioritetu
- [ ] Queue sadrži i sistemske stavke (auto-degradation review, instant block review)
- [ ] Svaka stavka prikazuje: preview sadržaja, AI hints (ako postoje), Trust Tier korisnika, tip stavke
- [ ] Prioritet se računa po formuli za pre-moderaciju: AI Risk 50%, Vrijeme čekanja 40%, Tip sadržaja 10%
- [ ] Prioritet se računa po formuli za post-moderaciju: AI Risk 60%, Trust Tier 30%, Vrijeme od objave 10%
- [ ] Moderator može filtrirati queue po: tipu (pre-mod / post-mod / system review), prioritetu, tipu sadržaja (Event / Place)
- [ ] Moderator može "preuzeti" (claim) stavku — stavka se zaključava za tog moderatora
- [ ] Claimed stavka prikazuje ko je preuzeo i kada
- [ ] Moderator može "pustiti" (release) stavku natrag u queue
- [ ] Stavka se automatski release-a nakon konfigurabilnog timeout-a neaktivnosti
- [ ] Queue prikazuje statistiku: ukupan broj po prioritetu, prosječno vrijeme čekanja

**Backend Scope:**

- `GET /api/moderation/queue` — lista stavki sa filtriranjem, paginacijom, sortiranjem po prioritetu
- `GET /api/moderation/queue/stats` — statistika queue-a (broj po prioritetu, prosječno vrijeme)
- `GET /api/moderation/queue/{itemId}` — detalji jedne stavke (uključujući preview sadržaja, AI hints, korisnikovu historiju)
- `POST /api/moderation/queue/{itemId}/claim` — preuzimanje stavke (lock)
- `POST /api/moderation/queue/{itemId}/release` — puštanje stavke (unlock)
- Automatski release nakon timeout-a neaktivnosti (konfiguracijski parametar)
- Prioritet score kalkulacija na osnovu formula iz **Ch.05**

**Frontend Scope:**

- UI: lista stavki sa vizualnim indikatorima prioriteta (boja/ikona po zoni: urgent/high/normal/low)
- Preview: thumbnail slike, skraćeni tekst, ime korisnika, Trust Tier badge
- Filteri: tip moderacije, prioritet, tip sadržaja
- Claim/Release dugmad sa vizualnim feedbackom
- Stats panel: ukupno, po prioritetu, prosječno čekanje
- UX: stavka na koju moderator klikne automatski se claim-a; pri zatvaranju bez odluke — opcija release ili ostavi claimed

**Tehničke napomene:**

- Queue treba podržavati real-time ili near-real-time update (novi sadržaj, promjene prioriteta). WebSocket ili polling — odluka na timu.
- Claim mehanizam mora biti atomičan — dva moderatora ne smiju moći preuzeti istu stavku istovremeno.
- Queue infrastruktura se koristi i za sistemske review stavke iz [E06](../e06-trust-tier-sistem.md) — dizajn treba biti dovoljno generički.

**Testovi (MVP):**

- [ ] Queue prikazuje sadržaj sortiran po prioritetu (Urgent na vrhu)
- [ ] Claim stavke — drugi moderator vidi "claimed by X"
- [ ] Pokušaj claim-a već claimed stavke → greška
- [ ] Release stavke → vraća se u queue
- [ ] Pre-mod stavka sa AI risk HIGH i 2h čekanja → viši prioritet od stavke sa LOW i 30min
- [ ] Sistemska stavka (auto-degradation review) pojavljuje se u queue-u

**Wireframe referenca:** —

**Implementacijske napomene:**

- Razmisliti o "smart assignment" u budućnosti — ali za MVP je manuelni claim/release dovoljan.
- Stats panel je koristan za operativno praćenje (da li smo unutar SLA).