---
id: S01-04
confluence_page_id: "251297812"
parent_epic: E01
linear_id: "CIT2-4"
phase: MVP
journey_milestones: [J-01]
type: fullstack
---

**Naslov:** Login, logout i session management

**Excerpt:** Korisnik se prijavljuje emailom i lozinkom, dobija session koji traje do 30 dana, i može se odjaviti sa jednog ili svih uređaja. Sistem provjerava i accountStatus i accessStatus pri svakoj prijavi — blokirani ili neaktivni korisnici ne mogu pristupiti.

**Phase:** MVP

**Journey milestones:** J-01

**User story:**  
Kao registrovani korisnik,

želim se prijaviti na platformu i ostati prijavljen na svim svojim uređajima,

kako bih mogao koristiti platformu bez stalnog ponovnog prijavljivanja.

**Kontekst:** Login je ulazna tačka za sve autentificirane funkcionalnosti. Session politika za User: 30 dana refresh token, neograničene concurrent sessions (**Ch.03, sekcija 3.7**). Pri prijavi, sistem provjerava oba statusa — accountStatus i accessStatus. Korisnik sa `accountStatus = active` ali `accessStatus = blocked` ne smije moći pristupiti (**Ch.03, sekcija 3.3** — ortogonalnost statusa). Lockout nakon 10 neuspjelih pokušaja na 15 minuta (**Ch.03**, 3.7).

**Acceptance criteria:**

- [ ] Korisnik se prijavljuje sa email + lozinka
- [ ] Uspješna prijava vraća access token + refresh token
- [ ] Neuspješna prijava prikazuje generičku poruku (ne otkriva da li email postoji)
- [ ] Korisnik sa `accessStatus = blocked` ne može se prijaviti — dobija poruku o blokadi
- [ ] Korisnik sa `accountStatus = inactive` ne može se prijaviti — dobija poruku o deaktiviranom računu
- [ ] Korisnik sa `accountStatus = deleted` ne može se prijaviti
- [ ] Refresh token omogućava dobijanje novog access tokena bez ponovne prijave
- [ ] Session traje do 30 dana (refresh token expiry) — konfigurisano, ne hardkodirano
- [ ] Neograničen broj concurrent sesija (korisnik može biti prijavljen na više uređaja)
- [ ] Logout invalidira trenutni session
- [ ] Opcija "Odjavi se sa svih uređaja" invalidira sve aktivne sesije
- [ ] `lastLoginAt` se ažurira pri svakoj uspješnoj prijavi
- [ ] Lockout nakon konfigurisanog broja neuspjelih pokušaja (preporučeno: 10) na konfigurisano vrijeme (preporučeno: 15 min)

**Backend Scope:**

- `POST /auth/login` — prima {email, password}, vraća {accessToken, refreshToken, user}. Provjerava accountStatus, accessStatus i lockout.
- `POST /auth/logout` — prima {refreshToken}, invalidira taj session
- `POST /auth/refresh` — prima {refreshToken}, vraća novi {accessToken, refreshToken}
- `POST /auth/logout-all` — invalidira sve aktivne sesije korisnika
- Validacija: kredencijali, accountStatus (active/inactive/deleted), accessStatus (allowed/blocked), lockout status
- Side effects: ažuriranje `lastLoginAt`, inkrement `failedLoginAttempts`, postavljanje `lockedUntil` pri lockout-u

**Frontend Scope:**

- UI: login forma sa email + password poljima, "Zaboravljena lozinka?" link, "Registruj se" link; "Odjavi se sa svih uređaja" opcija u profilu/podešavanjima
- Klijentska validacija: obavezna polja (email, password)
- UX: uspješan login → redirect na dashboard/homepage; neuspješan → generička greška "Pogrešan email ili lozinka"; blocked → specifična poruka o blokadi; lockout → poruka sa preostalim vremenom; token refresh transparentan za korisnika

**Tehničke napomene:**

- Access token je kratkoživući, refresh token je dugoživući — standardni OAuth2 pattern.
- Audit log bilježi sve login pokušaje (uspješne i neuspješne) sa retencijom 90 dana (**Ch.03**, 3.7).

**Testovi (MVP):**

- [ ] Uspješan login sa validnim kredencijalima vraća tokene
- [ ] Login sa pogrešnom lozinkom vraća generičku grešku
- [ ] Login sa `accessStatus = blocked` je odbijen sa odgovarajućom porukom
- [ ] Login sa `accountStatus = inactive` ili `deleted` je odbijen
- [ ] Refresh token uspješno produžava sesiju
- [ ] Logout invalidira session — kasniji zahtjevi sa istim tokenom su odbijeni
- [ ] "Odjavi se sa svih uređaja" invalidira sve sesije
- [ ] Lockout se aktivira nakon konfiguriranog broja neuspjelih pokušaja

**Wireframe referenca:** —