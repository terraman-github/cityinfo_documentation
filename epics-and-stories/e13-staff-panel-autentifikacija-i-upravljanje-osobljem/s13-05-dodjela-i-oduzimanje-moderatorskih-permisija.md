# S13-05 — Dodjela i oduzimanje moderatorskih permisija

**Naslov:** Dodjela i oduzimanje moderatorskih permisija

**Excerpt:** Moderatori imaju bazne ovlasti po defaultu, ali osjetljive akcije (Trust Tier upravljanje, tag upravljanje) zahtijevaju eksplicitne granularne permisije. Ova storija pokriva UI i endpoint za dodjelu/oduzimanje `can_manage_trust_tier` i `can_manage_tags` permisija.

**Phase:** MVP

**Journey milestones:** J-08

**User story:**  
Kao operator,  
želim dodijeliti ili oduzeti specifične permisije moderatorima,  
kako bih mogao kontrolisati ko ima pristup osjetljivim akcijama poput promjene Trust Tier-a ili upravljanja tagovima.

**Kontekst:** Permisije se čuvaju u `permissions` polju Staff entiteta kao lista stringova. Trenutno postoje dvije permisije: `can_manage_trust_tier` i `can_manage_tags`. Operator i local\_admin mogu dodijeljivati permisije moderatorima. Local\_admin ima inherentno sve permisije bez potrebe za eksplicitnim dodavanjem. Detalji → Ch.03, sekcija 3.5 (moderatorske permisije) i Ch.05, sekcija 5.4.1.

**Acceptance criteria:**

- [ ] Operator može dodijeliti `can_manage_trust_tier` permisiju moderatoru
- [ ] Operator može dodijeliti `can_manage_tags` permisiju moderatoru
- [ ] Operator može oduzeti obje permisije
- [ ] Local\_admin može dodijeliti/oduzeti permisije (inherentna ovlast)
- [ ] Permisije se mogu dodijeliti samo Staff-u sa ulogom `moderator` — ne operatoru ni local\_adminu
- [ ] Promjena permisija se odmah reflektuje — moderator vidi/gubi pristup osjetljivim akcijama bez ponovnog logina
- [ ] UI jasno prikazuje koje permisije moderator trenutno ima
- [ ] Svaka promjena permisija se loguje u audit log sa before/after

**Backend Scope:**

- `PATCH /staff/manage/staff/{staffId}/permissions` — prima {permissions: string\[\]}, vraća {updatedPermissions}
- Validacija: samo operator/local\_admin može mijenjati, cilj mora biti moderator, permisije moraju biti iz dozvoljene liste
- Side effects: audit log sa detaljima promjene

**Frontend Scope:**

- UI: sekcija u Staff detalj prikazu sa checkbox-ovima za svaku permisiju; oznaka "(inherentno)" za local\_admin naloge
- Klijentska validacija: ne prikazuj permisije za Staff koji nije moderator
- UX: inline save (bez forme/submit-a); toast pri uspjehu/grešci; disabled stanje za Staff koji nisu moderatori

**Tehničke napomene:**

- Lista permisija se može proširivati — dizajnirati UI fleksibilno, ne hardcode-ovati samo dvije permisije
- Permisije ne zahtijevaju re-login — provjeravaju se pri svakom API pozivu, ne pri izdavanju tokena
- Ovo ne pokriva šta permisije omogućavaju (to je dio E06/E07) — samo dodjelu i oduzimanje

**Testovi (MVP):**

- [ ] Operator uspješno dodjeljuje can\_manage\_trust\_tier moderatoru
- [ ] Operator uspješno oduzima permisiju
- [ ] Dodjela permisije ne-moderatoru je odbijena
- [ ] Moderator bez permisije ne može pristupiti osjetljivim akcijama
- [ ] Audit log bilježi promjenu sa before/after

**Wireframe referenca:** —