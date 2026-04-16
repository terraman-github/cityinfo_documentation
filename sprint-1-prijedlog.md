# Sprint 1 — Prijedlog

> **Verzija:** 1.0
> **Datum:** 16.4.2026
> **Status:** Draft — čeka review tima
> **Autor:** Claude (agent)
> **Kontekst:** Sprint raspored iz `epics-and-stories/plan-pisanja-epica-i-storija.md` (Sprint 1–2 = E01 + E02). Ovaj dokument razdvaja taj opseg na konkretan **Sprint 1** i ostavlja ostatak za **Sprint 2**.

---

## TL;DR

Sprint 1 je **auth temelj + otvaranje prvog drafta**. Do kraja sprinta korisnik se može registrovati, verificirati email i telefon, prijaviti se, urediti profil, i kreirati (ali ne još objaviti) Event ili Place draft. Objava, slike, dokumenti i lifecycle akcije idu u Sprint 2.

**Sprint goal:** *Registrovan i verificiran korisnik može kreirati svoj prvi Event ili Place draft kroz produkcijski frontend.*

**Trajanje:** 2 sedmice (pretpostavka — prilagoditi ako tim radi drugačije)

---

## Preduvjeti (iz Sprint 0)

Prije Sprint 1 startа, ovo **mora biti zatvoreno** iz E14 i E03a:

- **E14** — S14-01 (repo + dev env), S14-02 (.NET 10 API skelet + middleware), S14-03 (SvelteKit frontend skelet), S14-04 (DB schema + migracije), S14-05 (single-tenant config za Sarajevo), S14-06 (i18n framework)
- **E03a** — S03a-01 (Category entiteti), S03a-02 (Tag entiteti), S03a-03 (seed kategorija), S03a-04 (seed tagova), S03a-05 (read endpointi za kategorije/tagove)

**Vanjski preduvjeti** (nabaviti prije sprinta):
- Email provider (Postmark / SendGrid / SMTP) — za verifikaciju i reset — preduslov za S01-02, S01-05
- SMS provider (Infobip / Twilio) — za verifikaciju telefona — preduslov za S01-03
- Staging okruženje sa test mail/SMS mod-om za QA

> Ako SMS provider kasni, S01-03 se može odraditi sa mock provider-om iza feature flaga; ne blokira ostale storije.

---

## Sprint 1 — Commitovane storije

| ID | Naslov | Epic | Procijenjena veličina | Ovisnost |
|----|--------|------|----------------------|----------|
| S01-01 | Registracija novog korisnika | E01 | S | — (E14, E03a) |
| S01-02 | Email verifikacija | E01 | S | S01-01, email provider |
| S01-03 | Verifikacija telefona (SMS) | E01 | M | S01-01, SMS provider |
| S01-04 | Login, logout i session management | E01 | M | S01-01 |
| S01-05 | Zaboravljena lozinka i reset | E01 | S | S01-01, email provider |
| S01-06 | Korisnički profil — pregled i uređivanje | E01 | M | S01-04 |
| S02-01 | Kreiranje Event listinga sa osnovnim podacima | E02 | M | S01-03, E03a |
| S02-02 | Kreiranje Place listinga sa osnovnim podacima | E02 | M | S01-03, E03a |

**Ukupno: 8 storija** (S = small, M = medium, L = large — po procjeni; tim može preračunati u story pointe/ idealne dane)

### Zašto baš ove

- **Cijeli E01 "Sprint 1" blok** iz epica (S01-01 do S01-04) — bez njih nema nijedne druge akcije na platformi.
- **S01-05 (reset lozinke)** — mali trošak, ogroman UX benefit; sav email tooling je ionako gotov kroz S01-02. Držati u Sprint 1 umjesto da "curi" u Sprint 2.
- **S01-06 (profil)** — zatvara E2E onboarding story ("Mogu se registrovati i vidjeti svoj profil"), otključava demo na kraju sprinta.
- **S02-01 i S02-02** — kritična su za vrijednost Sprint 2 jer sve ostale E02 storije (lokacija, slike, dokumenti, objava) rade nad **postojećim draftom**. Ako ih ostavimo za Sprint 2, Sprint 2 postaje prenapuhan.

### Šta svjesno **ne** ide u Sprint 1

- **S01-07 Brisanje računa (GDPR)** — nije na kritičnom putu za demo; 30-dnevni soft delete timer ne može se ionako testirati u jednom sprintu. → Sprint 2.
- **S01-08 2FA** — opciona funkcionalnost, ne blokira ništa. → Sprint 2.
- **S02-03 Lokacija Event-a** — zavisi od S02-02 (Place povezivanje); može se uraditi ranije samo "ručna adresa" varijanta, ali cijena je dupli prolaz. → Sprint 2, prvi red.
- **S02-04 Event hijerarhija** — složena (parent/child pravila), nije potrebna za MVP demo. → Sprint 2.
- **S02-05 Slike** — AI screening pipeline zahtijeva integraciju vanjskog servisa + asinhrone jobove. Bolje raditi sa fokusiranim danima u Sprint 2. → Sprint 2.
- **S02-06 Dokumenti** — virus scanning integracija, rjeđe korišteno. → Sprint 2.
- **S02-07 Objava i statusne tranzicije** — treba lokaciju (S02-03) i najbolje slike (S02-05) da bi imala smisla. Trust Tier tok je stub (default Tier 1 → pre-mod); puna logika dolazi u E06 (Sprint 3–4). → Sprint 2.
- **S02-08, S02-09** — edit/hide/cancel, sortDate refresh, praćenje statusa → Sprint 2.

---

## Plan za Sprint 2 (nastavak, radi konteksta)

> Nije commit Sprint 1, ali dokumentujem da jasno vidimo da E01+E02 stanu u dva sprinta.

| ID | Naslov | Napomena |
|----|--------|----------|
| S01-07 | Brisanje računa (GDPR soft delete) | Background job tek iz E14 mora biti live |
| S01-08 | 2FA za korisnike | Može biti stretch i ako se probije |
| S02-03 | Lokacija Event-a (Place ili ručna adresa) | Prvi red Sprint 2 |
| S02-04 | Event hijerarhija (parent/child) | — |
| S02-05 | Upload i upravljanje slikama | AI screening kroz vanjski servis |
| S02-06 | Upload i upravljanje dokumentima | Virus scanning kroz vanjski servis |
| S02-07 | Objava i statusne tranzicije | Trust Tier stub (Tier 1 default) dok ne dođe E06 |
| S02-08 | Edit / brisanje / sakrivanje listinga | Poštovati `wasEverActive` pravila |
| S02-09 | Ručni sortDate refresh i praćenje statusa | Zatvara E02 |

---

## Sprint 1 Definition of Done

Sprint se smatra uspješnim ako **sve** ovo vrijedi:

1. Svih 8 commitovanih storija je merge-ovano na `main`, sa zelenim CI-em.
2. Svaka storija prolazi svoje MVP testove definisane u story fajlu (`epics-and-stories/e01-.../s01-*.md`, `e02-.../s02-*.md`).
3. Postoji live staging deployment gdje se može reprodukovati E2E tok: **registracija → email verifikacija → SMS verifikacija → login → profil → kreiranje Event drafta → kreiranje Place drafta**.
4. API dokumentacija (OpenAPI/Swagger) pokriva sve nove endpointe.
5. Svi parametri (password policy, session trajanje, SMS kod trajanje, itd.) su u konfiguraciji, ne hardkodovani.
6. Audit logging za `login` i `register` radi i retencija od 90 dana (Ch.03, 3.7) je konfigurisana.
7. Svi novi endpoint-i respektuju `accountStatus` + `accessStatus` provjere (Ch.03, 3.3).
8. Dvojezična polja na listing formi (`nameAlt`, `descriptionAlt`, `excerptAlt`) su funkcionalna — povezana sa i18n frameworkom iz E14.

---

## Rizici i mitigacije

| Rizik | Vjerovatnoća | Impact | Mitigacija |
|-------|--------------|--------|------------|
| SMS provider integracija kasni ili ima neočekivane troškove | Srednja | Srednji | S01-03 iza feature flaga sa mock provider-om; pustiti pravi provider kad bude dogovoren. Ne blokira ostale storije. |
| Session management (refresh token, multi-device) složeniji nego što izgleda | Srednja | Srednji | U Sprint 1 implementirati **minimalnu** varijantu: jedan refresh token, single-device logout. "Odjava sa svih uređaja" odgoditi u Sprint 2 ako treba. |
| Dvojezična polja u listing formi (S02-01, S02-02) otkriju rupe u i18n frameworku iz Sprint 0 | Niska | Srednji | Prvi dan sprinta: integration test koji provjerava da i18n framework vraća `descriptionAlt` kroz API i renderuje ga na forma. Ako propadne, prioritet je fix u E14 prije ostatka. |
| Password policy i session politika nisu finalizirane u Ch.03 | Niska | Nizak | Sprint startuje sa preporučenim defaultima iz Ch.03, sekcija 3.7: min 8 karaktera + kombinacija, 30-dnevni refresh token. Promjena preko konfiguracije bez koda. |
| `accountStatus` i `accessStatus` middleware nije izgrađen u Sprint 0 | Niska | Visok | Provjeriti prvog dana sprinta — ako nedostaje, dodati kao **first task** u S01-04 (login već mora poštovati oba polja). |

---

## Pretpostavke koje treba potvrditi sa timom

1. **Trajanje sprinta:** 2 sedmice. Ako tim radi 1- ili 3-sedmične sprintove, spisak storija treba skalirati proporcionalno.
2. **Veličina tima:** prijedlog je kalibriran za tim od **2–3 backend + 1–2 frontend developera + 1 QA**. Sa manjim timom, S01-05 ili S01-06 izbaciti iz commit-a u stretch.
3. **Sprint 0 je zaista završen** — prije planning meetinga provjeriti da su sve E14 i E03a storije merged i deployed na staging.
4. **Trust Tier stub:** u S02-01/02 draft kreiranje **ne** treba Trust Tier logiku. Ali kad u Sprint 2 krene S02-07 (objava), treba minimum "svi novi korisnici su Tier 1 → pre-moderacija". Puna automatska progresija/degradacija tek u E06 (Sprint 3–4). Potvrditi da je tim svjestan ovog stuba.
5. **Listing statusni model:** sve storije koriste jednostatus model (`listingStatus` sa 12 vrijednosti + `removedReason` + `isPublic` + `wasEverActive`). Bez referenci na stari `lifecycleStatus`/`moderationStatus`/`closedReason`.

---

## Stretch (ako tim završi rano)

Po prioritetu:

1. **S02-03 Lokacija Event-a** — otključava S02-07 u Sprint 2.
2. **S01-07 Brisanje računa** — rasterećuje Sprint 2.
3. **Pripremni spike za S02-05 (slike + AI screening)** — istraživanje providera, nikakav produkcijski kod, samo spike dokument.

---

## Referenca — linkovi na story fajlove

Storije commitovane u Sprint 1:

- `epics-and-stories/e01-korisnicka-registracija-i-profil/s01-01-registracija-novog-korisnika.md`
- `epics-and-stories/e01-korisnicka-registracija-i-profil/s01-02-email-verifikacija.md`
- `epics-and-stories/e01-korisnicka-registracija-i-profil/s01-03-verifikacija-telefona-sms.md`
- `epics-and-stories/e01-korisnicka-registracija-i-profil/s01-04-login-logout-i-session-management.md`
- `epics-and-stories/e01-korisnicka-registracija-i-profil/s01-05-zaboravljena-lozinka-i-reset.md`
- `epics-and-stories/e01-korisnicka-registracija-i-profil/s01-06-korisnicki-profil-pregled-i-ureivanje.md`
- `epics-and-stories/e02-listing-crud-i-lifecycle/s02-01-kreiranje-event-listinga-sa-osnovnim-podacima.md`
- `epics-and-stories/e02-listing-crud-i-lifecycle/s02-02-kreiranje-place-listinga-sa-osnovnim-podacima.md`

---

## Changelog

| Verzija | Datum | Opis |
| --- | --- | --- |
| 1.0 | 16.4.2026 | Inicijalni prijedlog — razdvajanje Sprint 1–2 opsega (E01 + E02) na konkretan Sprint 1 od 8 storija + Sprint 2 plan. |
