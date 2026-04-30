---
id: E01
confluence_page_id: "251232295"
title: "E01 — Korisnička registracija i profil"
linear_id: ""
phase: MVP
journey_milestones: [J-01]
personas: [Marko, Ana, Thomas, Lejla]
story_count: 8
---

**Naslov:** Korisnička registracija i profil

**Excerpt:** Bez korisnika nema sadržaja, bez sadržaja nema platforme. Ovaj epic pokriva kompletni tok od anonimnog posjetioca do registrovanog korisnika sa verificiranim emailom, potvrđenim telefonom i funkcionalnim profilom. Uključuje i mehanizme zaštite — session management, reset lozinke, GDPR brisanje — jer registracija bez tih temelja nije ozbiljna.

**Scope — šta ulazi:**

- Registracija novog korisnika (email + username + password)
- GDPR saglasnost pri registraciji
- Email verifikacija (link u emailu)
- Verifikacija telefona (SMS kod) — preduslov za kreiranje listinga
- Login i logout sa session management-om
- Zaboravljena lozinka / reset password flow
- Korisnički profil — pregled i uređivanje podataka
- Soft delete računa sa GDPR pravilima (30 dana → trajno brisanje)
- Opcionalna dvofaktorska autentifikacija (2FA)
- accountStatus i accessStatus logika — provjera pristupa pri svakom requestu
- Visitor pristup — javni endpoint-i rade bez autentifikacije

**Scope — šta NE ulazi:**

- Trust Tier logika i automatsko napredovanje/degradacija — [E06](e06-trust-tier-sistem.md)
- Wallet i kreditni sistem — [E09](e09-kreditni-sistem-i-wallet.md)
- Staff registracija, login i admin panel — [E13](e13-staff-panel-autentifikacija-i-upravljanje-osobljem.md)
- GlobalAdmin portal — Faza 2
- Blokiranje korisnika od strane moderatora — [E07](e07-moderacijski-workflow-i-ai-screening.md)/[E13](e13-staff-panel-autentifikacija-i-upravljanje-osobljem.md) (accessStatus logika se implementira ovdje, ali UI i workflow za blokiranje dolaze u moderacijskom epicu)
- Push notifikacije — Faza 2
- Social login (Google, Facebook, Apple) — Backlog

**Persone:** Marko (organizator događaja), Ana (vlasnica biznisa), Thomas (turist), Lejla (studentica) — svi prolaze kroz registraciju

**Journey milestones:** J-01

**Phase:** MVP

**Dokumentacijska referenca:** Ch.03, sekcije 3.2–3.3, 3.7; **Ch.02, sekcija 2.7**

**Tehničke napomene:**

- User entitet sa svim atributima iz **Ch.03, sekcija 3.3** — uključujući `trustTier` polje (default: 1), ali bez logike napredovanja/degradacije (dolazi u [E06](e06-trust-tier-sistem.md)).
- `isVerifiedPublisher` polje postoji na entitetu (default: false), ali logika postavljanja dolazi u [E07](e07-moderacijski-workflow-i-ai-screening.md)/[E13](e13-staff-panel-autentifikacija-i-upravljanje-osobljem.md).
- `walletBalance` polje postoji (default: 0.00), ali wallet operacije dolaze u [E09](e09-kreditni-sistem-i-wallet.md).
- accountStatus (active/inactive/deleted) i accessStatus (allowed/blocked) su ortogonalni — oba se moraju provjeriti pri svakom autentificiranom requestu (**Ch.03**, 3.3).
- Session politika za User: 30 dana refresh token, neograničene concurrent sessions, mogućnost odjave sa pojedinog ili svih uređaja (**Ch.03**, 3.7).
- Audit logging za User akcije (login, registracija) sa retencijom 90 dana (**Ch.03**, 3.7).
- Ovaj epic je na kritičnom putu — gotovo svaki drugi epic zavisi od User entiteta i autentifikacije.

**Success metrika:** Korisnik se može registrovati, verificirati email, potvrditi telefon, prijaviti se, urediti profil i obrisati račun — kompletan self-service lifecycle bez potrebe za intervencijom.

* * *

<a id="storije-u-ovom-epicu"></a>

## Storije u ovom epicu

| ID  | Naslov | Phase | Sprint |
| --- | --- | --- | --- |
| [S01-01](e01-korisnicka-registracija-i-profil/s01-01-registracija-novog-korisnika.md) | Registracija novog korisnika | MVP | 1   |
| [S01-02](e01-korisnicka-registracija-i-profil/s01-02-email-verifikacija.md) | Email verifikacija | MVP | 1   |
| [S01-03](e01-korisnicka-registracija-i-profil/s01-03-verifikacija-telefona-sms.md) | Verifikacija telefona (SMS) | MVP | 1   |
| [S01-04](e01-korisnicka-registracija-i-profil/s01-04-login-logout-i-session-management.md) | Login, logout i session management | MVP | 1   |
| [S01-05](e01-korisnicka-registracija-i-profil/s01-05-zaboravljena-lozinka-i-reset.md) | Zaboravljena lozinka i reset | MVP | 1–2 |
| [S01-06](e01-korisnicka-registracija-i-profil/s01-06-korisnicki-profil-pregled-i-uredivanje.md) | Korisnički profil — pregled i uređivanje | MVP | 1–2 |
| [S01-07](e01-korisnicka-registracija-i-profil/s01-07-brisanje-korisnickog-racuna-gdpr.md) | Brisanje korisničkog računa (GDPR) | MVP | 2   |
| [S01-08](e01-korisnicka-registracija-i-profil/s01-08-dvofaktorska-autentifikacija-2fa-za-korisnike.md) | Dvofaktorska autentifikacija (2FA) za korisnike | MVP | 2   |