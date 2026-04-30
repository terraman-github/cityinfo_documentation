---
id: S13-04
confluence_page_id: "251166775"
title: "S13-04 — Pregled i upravljanje Staff nalozima"
parent_epic: E13
linear_id: "CIT2-79"
phase: MVP
journey_milestones: [J-08]
type: fullstack
---

**Naslov:** Pregled i upravljanje Staff nalozima

**Excerpt:** Local\_admin i operator trebaju vidjeti listu svih Staff članova, pregledati njihove detalje, editovati podatke i deaktivirati naloge. Ova storija pokriva CRUD operacije nad Staff entitetom — osim kreiranja koje je u [S13-03](s13-03-kreiranje-staff-naloga.md).

**Phase:** MVP

**Journey milestones:** J-08

**User story:**  
Kao local\_admin,

želim pregledati, editovati i deaktivirati Staff naloge u svom tenantu,

kako bih mogao upravljati timom i reagovati kada neki član napusti organizaciju.

**Kontekst:** Staff entitet koristi `isActive` boolean umjesto accountStatus enum-a — deaktivacija je jedini način "brisanja" naloga (nema soft/hard delete kao kod User-a). Svi Staff atributi → **Ch.03, sekcija 3.5**. Local\_admin vidi samo Staff za tenante kojima ima pristup. Deaktiviran Staff se ne može prijaviti.

**Acceptance criteria:**

- [ ] Local\_admin može pregledati listu svih Staff članova za svoje tenante
- [ ] Lista je filtrable po ulozi (moderator, operator, local\_admin) i statusu (aktivan/neaktivan)
- [ ] Lista podržava paginaciju i pretragu po imenu/emailu
- [ ] Local\_admin može pregledati detalje pojedinog Staff-a (svi atributi osim lozinke)
- [ ] Local\_admin može editovati: fullName, phoneNumber, department, supervisorId
- [ ] Local\_admin ne može promijeniti role, email ni permissions (role je fiksna nakon kreiranja; permissions ima zasebnu storiju [S13-05](s13-05-dodjela-i-oduzimanje-moderatorskih-permisija.md))
- [ ] Local\_admin može deaktivirati Staff nalog (`isActive = false`)
- [ ] Deaktivirani Staff se ne može prijaviti — aktivan session se terminira pri deaktivaciji
- [ ] Local\_admin može reaktivirati prethodno deaktiviran nalog (`isActive = true`)
- [ ] Sve izmjene se loguju u audit log sa before/after vrijednostima

**Backend Scope:**

- `GET /staff/manage/staff` — lista Staff članova, prima {filters, pagination, search}, vraća {items, total}
- `GET /staff/manage/staff/{staffId}` — detalji jednog Staff-a
- `PATCH /staff/manage/staff/{staffId}` — editovanje dozvoljenih polja
- `PATCH /staff/manage/staff/{staffId}/status` — aktivacija/deaktivacija, prima {isActive}
- Validacija: provjera tenant pristupa, dozvoljena polja za edit, ne može deaktivirati sam sebe
- Side effects: terminira session pri deaktivaciji, audit log za sve izmjene

**Frontend Scope:**

- UI: tabela Staff članova sa filterima (role, status) i pretragom; detail panel/modal; edit forma za dozvoljena polja
- Klijentska validacija: obavezna polja pri editu
- UX: confirmation dialog pri deaktivaciji ("Jeste li sigurni?"); success/error toast; lista se osvježava nakon akcije

**Tehničke napomene:**

- Local\_admin ne može deaktivirati sam sebe — to bi moglo dovesti do situacije bez admina
- Deaktivacija ne briše podatke — nalog ostaje u bazi za audit i historiju
- Before/after logging za svaku izmjenu je obavezan prema **Ch.03, sekcija 3.7**

**Testovi (MVP):**

- [ ] Local\_admin vidi listu Staff-a samo za svoje tenante
- [ ] Filtriranje po ulozi ispravno sužava rezultate
- [ ] Edit obaveznih polja se sprema i reflektuje u listi
- [ ] Deaktivirani Staff se ne može prijaviti
- [ ] Local\_admin ne može deaktivirati sam sebe
- [ ] Reaktivacija omogućava ponovni login

**Wireframe referenca:** —