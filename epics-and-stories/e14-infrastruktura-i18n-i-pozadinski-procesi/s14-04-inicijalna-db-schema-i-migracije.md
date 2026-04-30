---
id: S14-04
confluence_page_id: "250478595"
title: "S14-04 — Inicijalna DB schema i migracije"
parent_epic: E14
linear_id: "CIT2-86"
phase: MVP
journey_milestones: [J-08]
type: infra
---

**Naslov:** Inicijalna DB schema i migracije

**Excerpt:** Osnovna struktura baze podataka — tabele za User, Listing/Event/Place, Staff, Category, Tag. Bez ovoga ne postoji gdje čuvati podatke.

**Phase:** MVP

**Journey milestones:** J-08

**User story:**

*Kao developer,*  
*želim imati inicijalnu DB schema-u sa migration sistemom,*  
*kako bih mogao kreirati i evoluirati strukturu baze podataka na kontrolisan način.*

**Kontekst:** Baza je MS SQL Server — **Ch.08, sekcija 8.5**. U MVP-u je single-tenant (jedna baza za Sarajevo — **Ch.08, sekcija 8.1**). Schema treba pokriti osnovne entitete iz **Ch.03** (User, Staff) i **Ch.04** (Listing, Event, Place, Category, Tag, Image, ListingDocument). Ovo je skeleton — ne svi atributi, ali dovoljno za početak rada na [E01](../e01-korisnicka-registracija-i-profil.md) i [E02](../e02-listing-crud-i-lifecycle.md).

**Acceptance criteria:**

- [ ] Migration sistem je konfigurisan i funkcionalan (up/down migracije)
- [ ] Inicijalne migracije kreiraju tabele za: User, Staff, Listing, Event, Place, Category (Event + Place), Tag (Event + Place), Image, ListingDocument
- [ ] Migracije se mogu pokrenuti na praznoj bazi bez errora
- [ ] Migracije se mogu rollback-ovati (down migration)
- [ ] Connection string se čita iz konfiguracije, ne hardkodiran
- [ ] Seed skripta postoji kao zaseban korak (ne ugrađena u migraciju) — popunjava se u [E03a](../e03a-kategorizacija-sadrzaja-entiteti-i-seed-data.md) storijama

**Tehničke napomene:**

- Ovo je skeleton schema — ne moraju svi atributi iz dokumentacije biti prisutni. Fokus je na primarnim ključevima, osnovnim poljima i relacijama. Detalji atributa se dodaju u epicima koji ih koriste ([E01](../e01-korisnicka-registracija-i-profil.md), [E02](../e02-listing-crud-i-lifecycle.md), E03).

**Testovi (MVP):**

- [ ] Pokretanje migracija na praznoj bazi prolazi bez errora
- [ ] Rollback svih migracija prolazi bez errora
- [ ] Ponovo pokretanje migracija nakon rollback-a daje identičnu schema-u

**Wireframe referenca:** —