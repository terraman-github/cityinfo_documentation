---
id: S13-02
parent_epic: E13
linear_id: ""
phase: MVP
journey_milestones: [J-08]
type: fullstack
---

# S13-02 — Promjena lozinke i politika rotacije

**Naslov:** Promjena lozinke i politika rotacije

**Excerpt:** Staff članovi moraju mijenjati lozinku svakih 90 dana. Ova storija pokriva endpoint za promjenu lozinke, prisilnu rotaciju pri isteku, i upozorenje kada se rok približava.

**Phase:** MVP

**Journey milestones:** J-08

**User story:**  
Kao Staff član,  
želim moći promijeniti svoju lozinku i biti upozoren kada je rotacija obavezna,  
kako bih održavao sigurnost svog naloga u skladu sa politikom platforme.

**Kontekst:** Staff nalozi imaju obaveznu rotaciju lozinke svakih 90 dana (definisano u Ch.03, sekcija 3.7). Polje `passwordChangedAt` prati kada je lozinka posljednji put promijenjena. Kada istekne rok, Staff ne može nastaviti rad dok ne postavi novu lozinku — sistem ga preusmjerava na formu za promjenu.

**Acceptance criteria:**

- [ ] Staff može promijeniti lozinku unosom trenutne i nove lozinke
- [ ] Nova lozinka mora zadovoljiti minimalne sigurnosne zahtjeve (konfiguracijski parametri)
- [ ] Nova lozinka ne smije biti ista kao trenutna
- [ ] `passwordChangedAt` se ažurira nakon uspješne promjene
- [ ] Ako je prošlo 90+ dana od zadnje promjene, sistem prisilno traži novu lozinku pri sljedećem loginu
- [ ] Staff dobija upozorenje 7 dana prije isteka roka za rotaciju (prikazuje se u admin panelu)
- [ ] Promjena lozinke se loguje u audit log

**Backend Scope:**

- `POST /staff/auth/change-password` — prima {currentPassword, newPassword}, vraća {success}
- Validacija: provjera trenutne lozinke, nova lozinka ≠ trenutna, minimalni sigurnosni zahtjevi
- Side effects: ažurira passwordChangedAt, loguje u audit

**Frontend Scope:**

- UI: forma za promjenu lozinke (trenutna + nova + potvrda nove); banner upozorenja pri približavanju roka
- Klijentska validacija: obavezna polja, match provjera (nova = potvrda), minimalna dužina
- UX: prisilni redirect na promjenu lozinke ako je rok istekao; success toast nakon promjene; dismiss-able upozorenje 7 dana prije

**Tehničke napomene:**

- Rotacijski period (90 dana) i period upozorenja (7 dana) su konfiguracijski parametri
- Pri prisilnoj rotaciji, Staff je preusmjeren nakon uspješnog logina — ne može pristupiti nijednoj drugoj stranici dok ne promijeni lozinku

**Testovi (MVP):**

- [ ] Uspješna promjena lozinke sa ispravnom trenutnom
- [ ] Promjena odbijena ako je nova lozinka ista kao trenutna
- [ ] Prisilni redirect na promjenu ako je passwordChangedAt stariji od 90 dana
- [ ] Upozorenje se prikazuje 7 dana prije isteka

**Wireframe referenca:** —