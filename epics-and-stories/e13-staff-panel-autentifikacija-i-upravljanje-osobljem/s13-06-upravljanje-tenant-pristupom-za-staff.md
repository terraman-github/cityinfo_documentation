---
id: S13-06
parent_epic: E13
linear_id: ""
phase: MVP
journey_milestones: [J-08]
type: fullstack
---

# S13-06 — Upravljanje tenant pristupom za Staff

**Naslov:** Upravljanje tenant pristupom za Staff

**Excerpt:** Staff može pristupiti samo tenantima koji su eksplicitno navedeni u `tenantAccess` listi. Ova storija pokriva upravljanje tom listom — dodavanje i uklanjanje tenanta kojima Staff ima pristup.

**Phase:** MVP

**Journey milestones:** J-08

**User story:**  
Kao local\_admin,  
želim upravljati kojim tenantima Staff članovi imaju pristup,  
kako bih mogao kontrolisati da moderator iz Sarajeva ne vidi podatke iz Banja Luke — osim ako mu je to eksplicitno dodijeljeno.

**Kontekst:** CityInfo je multi-tenant platforma — svaki grad ima svoju bazu. Staff vidi samo podatke tenanta kojima ima pristup (`tenantAccess` lista). Čak i local\_admin za jedan grad ne može vidjeti podatke drugog. Detalji → Ch.03, sekcija 3.5. U MVP-u postoji samo jedan tenant (Sarajevo), ali sistem mora biti spreman za multi-tenant scenarij.

**Acceptance criteria:**

- [ ] Local\_admin može vidjeti listu tenanta kojima Staff član ima pristup
- [ ] Local\_admin može dodati tenant u `tenantAccess` listu Staff-a
- [ ] Local\_admin može dodati samo tenante kojima sam ima pristup
- [ ] Local\_admin može ukloniti tenant iz `tenantAccess` liste
- [ ] Staff mora imati barem jedan tenant u listi — ne može se ukloniti zadnji
- [ ] Promjena tenant pristupa se odmah reflektuje — Staff vidi/gubi pristup bez re-logina
- [ ] Svaka promjena se loguje u audit log

**Backend Scope:**

- `GET /staff/manage/staff/{staffId}/tenant-access` — trenutna lista tenanta
- `PATCH /staff/manage/staff/{staffId}/tenant-access` — prima {tenantIds: string\[\]}, vraća {updatedTenantAccess}
- Validacija: kreator mora imati pristup tenantima koje dodjeljuje, lista ne smije biti prazna
- Side effects: audit log

**Frontend Scope:**

- UI: sekcija u Staff detalj prikazu sa listom tenanta (checkbox ili multi-select); oznaka aktivnog tenanta
- Klijentska validacija: ne dozvoli uklanjanje zadnjeg tenanta
- UX: inline save; toast pri uspjehu; upozorenje pri uklanjanju tenanta ("Staff će izgubiti pristup podacima ovog grada")

**Tehničke napomene:**

- U MVP-u postoji samo Sarajevo tenant — ali UI i API moraju biti dizajnirani za multi-tenant od starta
- Tenant pristup se provjerava na svakom API pozivu — nije cachiran u tokenu
- Tenant switcher u shell-u (S13-07) koristi ovu listu za prikaz dostupnih tenanta

**Testovi (MVP):**

- [ ] Local\_admin uspješno dodaje tenant Staff članu
- [ ] Dodavanje tenanta kojem local\_admin nema pristup je odbijeno
- [ ] Uklanjanje zadnjeg tenanta iz liste je odbijeno
- [ ] Staff nakon gubitka tenant pristupa ne vidi podatke tog grada

**Wireframe referenca:** —