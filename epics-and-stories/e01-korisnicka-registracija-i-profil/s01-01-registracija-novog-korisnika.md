---
id: S01-01
parent_epic: E01
linear_id: "CIT2-1"
phase: MVP
journey_milestones: [J-01]
type: fullstack
---

# S01-01 — Registracija novog korisnika

**Naslov:** Registracija novog korisnika

**Excerpt:** Prvi korak na platformi — korisnik kreira račun sa emailom, username-om i lozinkom, i prihvata GDPR saglasnost. Nakon uspješne registracije dobija Tier 1 (Standard) i može pregledati sadržaj, ali ne može kreirati listinge dok ne verificira email i telefon.

**Phase:** MVP

**Journey milestones:** **J-01**

**User story:**  
Kao posjetilac CityInfo platforme,  
želim kreirati korisnički račun unosom osnovnih podataka,  
kako bih mogao pristupiti funkcionalnostima koje zahtijevaju registraciju.

**Kontekst:** Korisnik dolazi na platformu prvi put. Može pregledati javni sadržaj kao visitor, ali kad želi kreirati listing, sačuvati favorite ili koristiti naprednije funkcije — mora se registrovati. Registracijska forma traži minimalne podatke; telefon se verificira naknadno ([S01-03](s01-03-verifikacija-telefona-sms.md)), a email odmah nakon registracije ([S01-02](s01-02-email-verifikacija.md)). Detalji o User entitetu → **Ch.03, sekcija 3.3**. Onboarding flow → **Ch.02, sekcija 2.7**.

**Acceptance criteria:**

- [ ] Korisnik može kreirati račun unosom: email, username, puno ime (fullName), lozinka
- [ ] Email mora biti jedinstven unutar sistema — duplikat vraća jasnu grešku
- [ ] Username mora biti jedinstven unutar sistema
- [ ] Lozinka prolazi kroz bazičnu validaciju (minimalna dužina, kompleksnost)
- [ ] GDPR saglasnost (checkbox) je obavezna — registracija ne prolazi bez nje
- [ ] `gdprConsentAt` se bilježi u momentu prihvatanja
- [ ] Novi korisnik dobija default vrijednosti: `accountStatus = active`, `accessStatus = allowed`, `trustTier = 1`, `walletBalance = 0.00`, `isVerifiedPublisher = false`, `emailVerified = false`, `phoneVerified = false`
- [ ] `locale` i `timezone` se postavljaju na tenant default vrijednosti
- [ ] Nakon uspješne registracije, sistem šalje verifikacioni email (veza sa [S01-02](s01-02-email-verifikacija.md))
- [ ] Validacijske greške se prikazuju inline uz relevantna polja

**Backend Scope:**

- `POST /auth/register` — prima {email, username, fullName, password, gdprConsent}, vraća {userId, accessToken, refreshToken}
- Validacija: email unikatnost, username unikatnost, password policy (minimalna dužina, kompleksnost), gdprConsent = true
- Side effects: kreira User entitet sa default vrijednostima, bilježi `gdprConsentAt`, triggeruje slanje verifikacionog emaila ([S01-02](s01-02-email-verifikacija.md))
- Lozinka se hashira prije pohranjivanja

**Frontend Scope:**

- UI: registracijska forma sa poljima — email, username, fullName, password, confirm password, GDPR checkbox (sa linkom na uslove)
- Klijentska validacija: format emaila, password match (password vs confirm), minimalna dužina lozinke, obavezna polja, GDPR checkbox
- UX: nakon uspjeha — redirect na stranicu "Provjerite vaš email"; greške — inline poruke uz relevantna polja (duplikat emaila, slab password, itd.)

**Tehničke napomene:**

- `createdAt` se automatski popunjava.
- Registracija kreira User entitet u tenant bazi (ne u master bazi) — **Ch.03, sekcija 3.1**.

**Testovi (MVP):**

- [ ] Registracija sa validnim podacima uspješno kreira račun i šalje verifikacioni email
- [ ] Registracija sa duplikatom emaila vraća odgovarajuću grešku
- [ ] Registracija sa duplikatom username-a vraća odgovarajuću grešku
- [ ] Registracija bez GDPR saglasnosti ne prolazi
- [ ] Registracija sa preslabom lozinkom vraća validacijsku grešku

**Wireframe referenca:** —