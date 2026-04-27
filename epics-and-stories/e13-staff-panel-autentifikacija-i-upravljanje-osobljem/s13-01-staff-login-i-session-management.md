---
id: S13-01
parent_epic: E13
linear_id: ""
phase: MVP
journey_milestones: [J-08]
type: fullstack
---

# S13-01 — Staff login i session management

**Naslov:** Staff login i session management

**Excerpt:** Omogućava Staff članu da se prijavi na admin panel sa email/password + obaveznom 2FA, uz stroge session politike (1 aktivan session, 8h idle timeout, auto-lockout). Ovo je preduslov za svaku drugu funkcionalnost Staff panela.

**Phase:** MVP

**Journey milestones:** J-08

**User story:**  
Kao moderator,  
želim se prijaviti na admin panel sa sigurnom autentifikacijom,  
kako bih mogao pristupiti moderacijskim alatima bez rizika od neovlaštenog pristupa.

**Kontekst:** Staff pristupa admin panelu na [admin.cityinfo.ba](http://admin.cityinfo.ba). Za razliku od User sistema, Staff autentifikacija zahtijeva obaveznu 2FA za sve naloge i ima strože session politike. Staff nalog mora biti `isActive = true` da bi login bio moguć. Detalji o sigurnosnim zahtjevima → Ch.03, sekcija 3.7. Staff entitet i atributi → Ch.03, sekcija 3.5.

**Acceptance criteria:**

- [ ] Staff se može prijaviti sa email + password + 2FA kod
- [ ] Login nije moguć ako je `isActive = false`
- [ ] Login nije moguć ako je `lockedUntil` u budućnosti
- [ ] Nakon 5 neuspjelih pokušaja, nalog se zaključava na 30 minuta (`lockedUntil` se postavlja)
- [ ] `failedLoginAttempts` se resetuje na 0 nakon uspješnog logina
- [ ] Samo 1 aktivan session po Staff nalogu — nova prijava automatski terminira prethodni
- [ ] Session ističe nakon 8 sati neaktivnosti (idle timeout)
- [ ] `lastLoginAt` i `lastLoginIp` se ažuriraju pri svakom uspješnom loginu
- [ ] Staff može izvršiti logout koji invalidira session
- [ ] Sve login/logout akcije se loguju u audit log

**Backend Scope:**

- `POST /staff/auth/login` — prima {email, password, mfaCode}, vraća {token, staffProfile}
- `POST /staff/auth/logout` — invalidira aktivan session
- Validacija: email format, isActive provjera, lockout provjera, 2FA verifikacija
- Side effects: ažurira lastLoginAt/lastLoginIp, resetuje failedLoginAttempts, loguje u audit

**Frontend Scope:**

- UI: login forma sa email, password i 2FA kod poljem; lockout poruka ako je nalog zaključan
- Klijentska validacija: obavezna polja, email format
- UX: redirect na dashboard nakon uspješnog logina; inline greške za neispravne kredencijale; prikaz preostalog vremena lockout-a

**Tehničke napomene:**

- Session politika (1 aktivan, 8h idle) je definisana u Ch.03, sekcija 3.7
- Lockout parametri (5 pokušaja, 30 min) su konfiguracijski — mogu se mijenjati bez izmjene koda
- Staff auth je potpuno odvojen od User auth — ne dijele tokene ni session store

**Testovi (MVP):**

- [ ] Uspješan login sa ispravnim email + password + 2FA
- [ ] Login odbijen za isActive = false nalog
- [ ] Login odbijen za zaključan nalog (lockedUntil u budućnosti)
- [ ] Nakon 5 neuspjelih pokušaja, nalog se zaključava
- [ ] Nova prijava terminira prethodni session
- [ ] Session ističe nakon 8h neaktivnosti

**Wireframe referenca:** —

**Implementacijske napomene:**

- Razmotriti shared auth middleware sa User sistemom na tehničkom nivou (isti JWT mehanizam, različite konfiguracije)
- Lockout timer se računa server-side — klijent samo prikazuje preostalo vrijeme