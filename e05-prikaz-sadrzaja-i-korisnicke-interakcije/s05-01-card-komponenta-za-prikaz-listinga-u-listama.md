# S05-01 — Card komponenta za prikaz listinga u listama

**Naslov:** Card komponenta za prikaz listinga u listama

**Excerpt:** Kartica je osnovna "jedinica prikaza" — svaki listing se u listama/gridovima prikazuje kao kompaktna kartica sa slikom, nazivom, kategorijom, datumom, udaljenošću i socijalnim signalima. Tri nivoa promocije se vizuelno razlikuju. Ista komponenta se koristi na naslovnoj, u pretrazi, i u related contentu.

**Phase:** MVP

**Journey milestones:** J-04

**User story:**  
Kao posjetilac,  
želim vidjeti pregled listinga u kompaktnom formatu sa ključnim informacijama,  
kako bih brzo mogao procijeniti da li me listing zanima prije nego kliknem na detalje.

**Kontekst:** Card komponenta se koristi svuda gdje se prikazuje lista listinga — naslovna, pretraga, filteri, related content, favoriti. Elementi kartice su definirani u Ch.02, sekcija 2.3. Ista komponenta za Event i Place, ali sa razlikama u prikazanim podacima (Event ima datum, Place nema).

**Acceptance criteria:**

- [ ] Kartica prikazuje: featured sliku (ili default iz kategorije), naziv (na odabranom jeziku), excerpt, primarnu kategoriju (naziv + boja), tagove (ako postoje), broj lajkova
- [ ] Za Event kartice: prikazuje se startDateTime u lokalizovanom formatu
- [ ] Za Place kartice: nema datuma
- [ ] Udaljenost se prikazuje samo kad je korisnikova lokacija poznata i unutar zone tenanta
- [ ] Verifikacioni badge "✓ Potvrđen vlasnik" se prikazuje kad je `verificationStatus = verified`
- [ ] Tri nivoa promocijskog isticanja prema Ch.02, sekcija 2.3: Standard (suptilan highlight), Premium (jače isticanje), Premium+Homepage (isto kao Premium)
- [ ] Naziv se skraćuje ako je predugačak za karticu (ellipsis)
- [ ] Klik na karticu otvara detaljnu stranicu listinga
- [ ] Kartica je responsive — full-width na mobilnom, u gridu na tabletu/desktopu
- [ ] Slika koristi thumbnail verziju (300×200) za performanse
- [ ] Ako listing nema sliku, prikazuje se default slika iz kategorije, a ako ni ta ne postoji — generic placeholder

**Frontend Scope:**

- UI: Reusable Svelte komponenta `<ListingCard>` sa props-ima za listing podatke
- UI: Varijante za Event i Place (ista komponenta, uvjetni prikaz)
- UI: Promocijske varijante (CSS klase za Standard/Premium/Premium+Homepage)
- UX: Hover efekt na desktopu, touch feedback na mobilnom
- UX: Lazy loading slika sa blur placeholder-om
- UX: Konzistentan aspect ratio slike

**Tehničke napomene:**

- Ovo je frontend-only storija — koristi podatke iz API-ja definisanog u E02/E04.
- Komponenta treba biti optimizirana za performanse jer se prikazuje mnogo puta na jednoj stranici (20+ kartica).
- `primaryCategoryData` snapshot na listingu sadrži sve podatke potrebne za prikaz kategorije na kartici (ime, boja, sektor) — ne treba dodatni API poziv.

**Testovi (MVP):**

- [ ] Event kartica prikazuje datum, Place kartica ne prikazuje datum
- [ ] Kartica sa verifikacijom prikazuje badge
- [ ] Premium listing ima vizuelno jače isticanje od Standard-a
- [ ] Listing bez slike prikazuje default sliku kategorije
- [ ] Naziv duži od kartice se skraćuje sa ellipsis-om
- [ ] Udaljenost se ne prikazuje kad lokacija nije poznata

**Wireframe referenca:** —