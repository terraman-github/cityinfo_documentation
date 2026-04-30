---
id: S01-06
confluence_page_id: "250970114"
parent_epic: E01
linear_id: "CIT2-6"
phase: MVP
journey_milestones: [J-01]
type: fullstack
---

# S01-06 — Korisnički profil — pregled i uređivanje

**Naslov:** Korisnički profil — pregled i uređivanje

**Excerpt:** Korisnik može pregledati i urediti svoje podatke — ime, telefon, jezičke preferencije. Neki podaci se ne mogu mijenjati (email, username), a promjena telefona zahtijeva revalidaciju. Profil je i kontrolna tačka — korisnik odavde vidi status verifikacija i može pristupiti svojim listinzima.

**Phase:** MVP

**Journey milestones:** **J-01**

**User story:**  
Kao registrovani korisnik,  
želim pregledati i ažurirati svoje profilne podatke,  
kako bih mogao držati informacije aktuelnim i prilagoditi platformu svojim preferencijama.

**Kontekst:** Korisnik pristupa profilu kroz navigaciju. Profil prikazuje informacije iz User entiteta (**Ch.03, sekcija 3.3**). Neka polja su read-only (email, username), neka se mogu slobodno mijenjati (fullName, locale, timezone), a neka zahtijevaju revalidaciju (phoneNumber). Endpoint: `GET/PATCH /users/me` (**Ch.03, sekcija 3.8**).

**Acceptance criteria:**

- [ ] Korisnik može vidjeti sve svoje profilne podatke
- [ ] Polja `fullName`, `locale`, `timezone` se mogu slobodno mijenjati
- [ ] Polja `email` i `username` su prikazana ali read-only (ne mogu se mijenjati)
- [ ] Promjena `phoneNumber` resetuje `phoneVerified = false` i zahtijeva novu verifikaciju ([S01-03](s01-03-verifikacija-telefona-sms.md))
- [ ] Korisnik vidi status svojih verifikacija (email verificiran ✅/❌, telefon verificiran ✅/❌)
- [ ] Korisnik može promijeniti lozinku (unos stare + nove lozinke)
- [ ] Promjena lozinke ne invalidira trenutnu sesiju, ali invalidira sve ostale
- [ ] Validacija na svim editabilnim poljima sa inline error porukama

**Backend Scope:**

- `GET /users/me` — vraća kompletni profil korisnika (svi atributi osim lozinke)
- `PATCH /users/me` — prima {fullName?, phoneNumber?, locale?, timezone?}, vraća ažurirani profil
- `POST /auth/change-password` — prima {currentPassword, newPassword}, vraća {success}
- Validacija: password policy za novu lozinku, provjera stare lozinke
- Side effects: promjena phoneNumber resetuje `phoneVerified = false`; promjena lozinke invalidira sve sesije osim trenutne

**Frontend Scope:**

- UI: profil stranica sa sekcijama — lični podaci (fullName, email read-only, username read-only), kontakt (phoneNumber sa verifikacioni status), preferencije (locale, timezone), sigurnost (promjena lozinke, 2FA status — link na [S01-08](s01-08-dvofaktorska-autentifikacija-2fa-za-korisnike.md))
- Klijentska validacija: obavezna polja, format telefona
- UX: inline editing sa "Sačuvaj" dugmetom; uspjeh → toast "Promjene sačuvane"; promjena telefona → upozorenje da će trebati nova verifikacija; promjena locale-a → odmah mijenja jezik sučelja

**Tehničke napomene:**

- `locale` kontroliše jezik sučelja — promjena odmah utiče na prikaz (**Ch.02, sekcija 2.2**).
- Profil stranica je i entry point za buduće funkcionalnosti (wallet, moji listinzi, notifikacije) — ali te sekcije dolaze u kasnijim epicima.

**Testovi (MVP):**

- [ ] Profil stranica prikazuje sve korisničke podatke korektno
- [ ] Izmjena fullName se uspješno čuva
- [ ] Promjena phoneNumber resetuje phoneVerified
- [ ] Promjena lozinke funkcioniše sa validnim starim passwordom
- [ ] Promjena lozinke sa netačnim starim passwordom je odbijena
- [ ] Promjena locale-a odmah mijenja jezik sučelja

**Wireframe referenca:** —