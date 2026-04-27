---
id: E12
linear_id: ""
phase: MVP
journey_milestones: [J-02, J-03, J-05, J-06]
personas: [Milica, Marko, Ana, Thomas]
story_count: 5
---

# E12 — Notifikacije

**Naslov:** Notifikacije

**Excerpt:** Notifikacije obavještavaju korisnike o bitnim događajima na platformi — od odobravanja listinga, preko novih poruka od moderatora, do isteka promocija. CityInfo u MVP-u koristi dva kanala: email notifikacije (za važne informacije sa trajnim zapisom) i in-app notifikacije (badge + lista unutar aplikacije). Push notifikacije i korisničke preference za kontrolu notifikacija planirane su za Fazu 2.

**Scope — šta ulazi:**

- Notification entitet sa tipovima, referencama i statusom čitanja
- In-app notifikacije: badge sa brojem nepročitanih, lista notifikacija, označavanje kao pročitano
- Email notifikacije: transakcijske (listing status promjene), moderacijske (nova poruka), promotivne (promocija ističe/istekla)
- Slanje notifikacija pri ključnim sistemskim događajima (listing odobren/odbijen/changes\_requested, nova poruka, promocija, Trust Tier promjena)
- Notifikacije prilagođene Trust Tier nivou korisnika

**Scope — šta NE ulazi:**

- Push notifikacije (Faza 2 — zahtijeva Firebase/APNs integraciju)
- Korisničke preference za kontrolu notifikacija (Faza 2)
- Digest emailovi — sedmični/dnevni pregledi (Faza 2)
- Quiet hours (Faza 2)
- Email template dizajn (dizajnerski posao, ne feature scope)

**Persone:** Milica (korisnica), Marko (organizator), Ana (vlasnica biznisa), Thomas (turista)

**Journey milestones:** Cross-cutting (J-02, J-03, J-05, J-06)

**Phase:** MVP

**Dokumentacijska referenca:** Ch.07, sekcija 7.2

**Tehničke napomene:**

- Notification entitet evidentira svaku in-app notifikaciju; email notifikacije se loguju kao zapis sa channel=email ali nisu vidljive u in-app listi
- Badge nepročitanih se računa kao COUNT WHERE isRead=false AND channel='in\_app'
- Notifikacije su prilagođene Trust Tier nivou — Tier 0-1 dobija obavijesti o čekanju na pregled, Tier 2+ samo ako moderator naknadno pronađe problem — detalji u Ch.07, sekcija 7.2.6
- Email template-i koriste predefinisane kategorije (transakcijski, moderacijski, promotivni, sistemski) i podržavaju primarni i sekundarni jezik tenanta — Ch.07, sekcija 7.2.5

**Success metrika:** Korisnik dobije email i in-app notifikaciju kad mu listing bude odobren/odbijen, kad moderator pošalje poruku, i kad mu promocija ističe — a badge u headeru prikazuje tačan broj nepročitanih notifikacija.

* * *

<a id="storije-u-ovom-epicu"></a>

## Storije u ovom epicu

| #   | Storija | Phase | Journey |
| --- | --- | --- | --- |
| S12-01 | Kreiranje i slanje in-app notifikacija | MVP | Cross-cutting |
| S12-02 | Prikaz notifikacija i badge nepročitanih | MVP | Cross-cutting |
| S12-03 | Slanje email notifikacija | MVP | Cross-cutting |
| S12-04 | Notifikacije za listing lifecycle događaje | MVP | J-02, J-03 |
| S12-05 | Notifikacije za promocije i Trust Tier | MVP | J-06 |