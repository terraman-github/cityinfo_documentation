---
id: S01-08
parent_epic: E01
linear_id: ""
phase: MVP
journey_milestones: [J-01]
type: fullstack
---

# S01-08 — Dvofaktorska autentifikacija (2FA) za korisnike

**Naslov:** Dvofaktorska autentifikacija (2FA) za korisnike

**Excerpt:** Korisnici mogu opcionalno uključiti 2FA za dodatnu sigurnost svog računa. Za razliku od Staff-a gdje je 2FA obavezan, za User-e je to lični izbor. Setup koristi standardnu TOTP aplikaciju (Google Authenticator, Authy i sl.).

**Phase:** MVP

**Journey milestones:** J-01

**User story:**  
Kao korisnik koji brine o sigurnosti,  
želim uključiti dvofaktorsku autentifikaciju na svom računu,  
kako bih zaštitio svoj nalog čak i ako mi lozinka bude kompromitovana.

**Kontekst:** 2FA za korisnike je opciona (Ch.03, sekcija 3.7 — `twoFactorEnabled` default: false). Korisnik pristupa 2FA setup-u kroz profil. Kad je aktiviran, pri svakom loginu se traži i TOTP kod uz email/password. API endpointi: `/auth/2fa/setup` i `/auth/2fa/verify` (Ch.03, sekcija 3.8).

**Acceptance criteria:**

- [ ] Korisnik može aktivirati 2FA kroz profil
- [ ] Setup prikazuje QR kod koji se skenira TOTP aplikacijom
- [ ] Korisnik mora unijeti validan TOTP kod da potvrdi uspješan setup
- [ ] Nakon aktivacije, `twoFactorEnabled = true`
- [ ] Svaki login zahtijeva TOTP kod uz email i lozinku
- [ ] Korisnik može deaktivirati 2FA (uz potvrdu lozinkom ili TOTP kodom)
- [ ] Recovery kodovi se generišu pri setup-u — korisnik ih može koristiti ako izgubi pristup TOTP aplikaciji
- [ ] Login sa pogrešnim TOTP kodom je odbijen (broji se u lockout pokušaje)

**Backend Scope:**

- `POST /auth/2fa/setup` — generira TOTP secret, vraća {qrCodeUrl, secret, recoveryCodes}
- `POST /auth/2fa/verify` — prima {totpCode}, potvrđuje setup i postavlja `twoFactorEnabled = true`
- `POST /auth/2fa/disable` — prima {password ili totpCode}, deaktivira 2FA
- `POST /auth/login` (modifikacija) — kad je 2FA aktivan, zahtijeva dodatni {totpCode} parametar
- Validacija: TOTP kod provjera (RFC 6238), recovery kod jednokratnost
- Side effects: generisanje recovery kodova pri setup-u; neuspjeli TOTP pokušaji se broje u lockout

**Frontend Scope:**

- UI: 2FA sekcija na profil stranici (status aktivan/neaktivan); setup wizard — (1) prikaz QR koda sa uputama za skeniranje, (2) unos TOTP koda za potvrdu, (3) prikaz recovery kodova sa upozorenjem da ih sačuva; login forma — dodatno polje za TOTP kod kad je 2FA aktivan
- UX: setup uspjeh → prikaz recovery kodova u modalu sa "Preuzmi" ili "Kopiraj" opcijom; deaktivacija → konfirmacioni modal sa unosom lozinke ili TOTP koda; login sa 2FA → nakon uspješnog email+password, prikazuje se drugi korak za TOTP kod

**Tehničke napomene:**

- TOTP standard (RFC 6238) — kompatibilan sa Google Authenticator, Authy, itd.
- Recovery kodovi su jednokratni — svaki se može koristiti samo jednom.

**Testovi (MVP):**

- [ ] 2FA setup uspješno aktivira dvofaktorsku autentifikaciju
- [ ] Login bez TOTP koda je odbijen kad je 2FA aktivan
- [ ] Login sa validnim TOTP kodom prolazi
- [ ] Recovery kod se može koristiti umjesto TOTP koda
- [ ] Recovery kod se može koristiti samo jednom
- [ ] Deaktivacija 2FA funkcioniše uz potvrdu

**Wireframe referenca:** —