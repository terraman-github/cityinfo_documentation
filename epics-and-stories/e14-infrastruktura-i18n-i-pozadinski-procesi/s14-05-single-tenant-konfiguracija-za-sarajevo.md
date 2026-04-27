---
id: S14-05
parent_epic: E14
linear_id: ""
phase: MVP
journey_milestones: [J-08]
type: infra
---

# S14-05 — Single-tenant konfiguracija za Sarajevo

**Naslov:** Single-tenant konfiguracija za Sarajevo

**Excerpt:** Konfiguracija prvog (i u MVP-u jedinog) tenanta — Sarajevo, sa svim parametrima potrebnim za funkcionisanje sistema.

**Phase:** MVP

**Journey milestones:** **J-08**

**User story:**  
Kao developer,  
želim imati konfigurisan tenant za Sarajevo sa svim potrebnim parametrima,  
kako bi sistem znao koji grad opslužuje, koje jezike podržava i koji su operativni parametri.

**Kontekst:** MVP radi sa jednim tenantom (Sarajevo) bez TenantRegistry-a i multi-tenant infrastrukture — **MVP SCOPE**. Konfiguracija se čita iz config fajla ili environment varijabli. Parametri pokrivaju identitet tenanta, jezike, zonu pokrivenosti i operativne vrijednosti. Preporuka iz **MVP SCOPE**: koristiti konfiguracijske parametre umjesto hardkodiranja, čime se olakšava kasnija tranzicija na multi-tenant.

**Acceptance criteria:**

- [ ] Konfiguracija tenanta sadrži: naziv grada, domena, primarni jezik (bs), sekundarni jezik (en), vremenska zona, valuta (BAM)
- [ ] Zona pokrivenosti je definisana (centar + radijus) za lokacijske funkcije — **Ch.02, sekcija 2.2**
- [ ] Operativni parametri su konfigurabili: `TIER_PRE_MOD_MAX_PENDING`, `TIER1_MIN_APPROVED`, `TIER1_MIN_SUCCESS_RATE`, `TIER1_MIN_ACCOUNT_AGE_DAYS`, `TIER2_MIN_APPROVED`, `TIER2_MIN_SUCCESS_RATE`, `TIER2_MIN_ACCOUNT_AGE_DAYS`, `CHANGES_REQUESTED_TIMEOUT_DAYS`, `CHANGES_REQUESTED_REMINDER_DAYS`, `MAX_SECONDARY_CATEGORIES`, `MAX_TAGS_PER_LISTING`
- [ ] Parametri imaju default vrijednosti iz dokumentacije (preporučene početne vrijednosti)
- [ ] API može dohvatiti konfiguraciju tenanta za prikaz na frontendu (naziv, jezici, valuta)
- [ ] Svi tenant-specifični parametri se čitaju iz konfiguracije, ne iz koda

**Tehničke napomene:**

- Ne graditi TenantRegistry — jedan config fajl ili sekcija u appsettings je dovoljno za MVP. Struktura treba biti takva da je migracija na TenantRegistry (Faza 2) što bezbolnija.

**Testovi (MVP):**

- [ ] API vraća konfiguraciju tenanta sa ispravnim nazivom, jezicima i valutom
- [ ] Promjena parametra u konfiguraciji (npr. `TIER1_MIN_APPROVED`) se reflektuje bez ponovnog builda
- [ ] Zona pokrivenosti (centar + radijus) je ispravno definisana za Sarajevo

**Wireframe referenca:** —