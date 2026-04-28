---
id: E08
linear_id: ""
phase: MVP
journey_milestones: [J-03, J-07]
personas: [Lejla, Marko, Ana]
story_count: 5
---

# E08 — Komunikacija uz listing i dokumenti

**Naslov:** Komunikacija uz listing i dokumenti

**Excerpt:** Message sistem omogućava strukturiranu komunikaciju između moderatora i vlasnika listinga — svaki listing ima jedan trajni thread koji prati kompletnu historiju razgovora. Bez ovog sistema, moderatori nemaju način da zatraže pojašnjenja ili dokumente prije donošenja odluke, a vlasnici nemaju kanal za odgovor. Epic pokriva kreiranje thread-ova, slanje i primanje poruka, referenciranje dokumenata, i Staff UI za upravljanje komunikacijom.

**Scope — šta ulazi:**

- Automatsko kreiranje ListingMessageThread-a uz listing
- Slanje poruka (moderator → vlasnik, vlasnik → moderator, sistemske poruke)
- Statusni model thread-a (idle, waiting\_owner, waiting\_moderator) sa kontrolom pristupa
- Referenciranje ListingDocument-a u porukama (documentIds)
- Staff UI za pregled thread-ova, slanje poruka i upravljanje komunikacijom
- User UI za pregled primljenih poruka i odgovaranje
- Paginacija poruka unutar thread-a

**Scope — šta NE ulazi:**

- Notifikacije o novim porukama ([E12](e12-notifikacije.md) — Notifikacije)
- Upload i upravljanje dokumentima ([E02](e02-listing-crud-i-lifecycle.md) — Listing CRUD, ListingDocument je definisan u **Ch.04**)
- Support ticket sistem (Faza 3, **Ch.07** sekcija 7.3)
- Korisnik-korisnik komunikacija (nije planirana)

**Persone:** Lejla (moderator), Marko (organizator događaja), Ana (vlasnica biznisa)

**Journey milestones:** **J-03** (Moderacija sadržaja), **J-07** (Verifikacija vlasništva)

**Phase:** MVP

**Dokumentacijska referenca:** **Ch.07**, sekcije 7.1.1–7.1.8; **Ch.04, sekcija 4.7** (ListingDocument SSoT)

**Tehničke napomene:**

- Thread se kreira automatski pri kreiranju listinga — nema manualnog otvaranja/zatvaranja
- Kontrola pristupa (ko može slati poruke) je regulisana kroz statusni model thread-a, ne kroz posebna pravila
- Poruke referenciraju dokumente kroz `documentIds` — ne uploadaju ih direktno
- Sistemske poruke (`system` role) mogu se slati u bilo kojem statusu i ne mijenjaju status thread-a

**Success metrika:** Moderator može pokrenuti komunikaciju sa vlasnikom listinga, zatražiti pojašnjenje ili dokument, i pratiti kompletnu historiju komunikacije na jednom mjestu — bez potrebe za eksternim kanalima (email, telefon).

* * *

<a id="storije-u-ovom-epicu"></a>

## Storije u ovom epicu

| #   | Naslov | Phase | Journey |
| --- | --- | --- | --- |
| [S08-01](e08-komunikacija-uz-listing-i-dokumenti/s08-01-automatsko-kreiranje-message-thread-a-uz-listing.md) | Automatsko kreiranje message thread-a uz listing | MVP | **J-03** |
| [S08-02](e08-komunikacija-uz-listing-i-dokumenti/s08-02-slanje-poruke-moderatora-vlasniku-listinga.md) | Slanje poruke moderatora vlasniku listinga | MVP | **J-03**, **J-07** |
| [S08-03](e08-komunikacija-uz-listing-i-dokumenti/s08-03-odgovor-vlasnika-listinga-na-poruku-moderatora.md) | Odgovor vlasnika listinga na poruku moderatora | MVP | **J-03**, **J-07** |
| [S08-04](e08-komunikacija-uz-listing-i-dokumenti/s08-04-referenciranje-dokumenata-u-porukama.md) | Referenciranje dokumenata u porukama | MVP | **J-07** |
| [S08-05](e08-komunikacija-uz-listing-i-dokumenti/s08-05-pregled-i-upravljanje-thread-ovima-u-staff-panelu.md) | Pregled i upravljanje thread-ovima u Staff panelu | MVP | **J-03** |