---
id: E14
confluence_page_id: "251199489"
title: "E14 — Infrastruktura, i18n i pozadinski procesi"
linear_id: ""
phase: MVP
journey_milestones: [J-08]
personas: [Svi]
story_count: 7
---

**Naslov:** Infrastruktura, i18n i pozadinski procesi

**Excerpt:** Sve ostalo stoji na ovom epicu. Prije nego ijedan korisnik kreira listing ili moderator odobri sadržaj, mora postojati funkcionalan razvojni okruženje, baza podataka, i18n framework za dvojezičnost, konfiguracija tenanta i skeleton aplikacije. Ovaj epic postavlja tehničke temelje bez kojih nijedan drugi epic ne može početi.

**Scope — šta ulazi:**

- Inicijalni setup razvojnog okruženja (repo, branch strategija, lokalni dev environment)
- Skeleton .NET 10 API projekta sa osnovnim middleware-om
- Skeleton SvelteKit frontend aplikacije (User app)
- Inicijalna DB schema (migracije za osnovne entitete)
- Single-tenant konfiguracija za Sarajevo (parametri, jezici, zona pokrivenosti)
- i18n framework — tenant language konfiguracija, locale management, fallback logika (ako `nameAlt` ne postoji → prikaži `name`)
- Framework za lokalizaciju UI stringova (primarni + sekundarni jezik tenanta)
- CI/CD pipeline (kad tim procijeni da je potrebno — nije prioritet za Sprint 0)

**Scope — šta NE ulazi:**

- Multi-tenant infrastruktura, TenantRegistry, GlobalAdmin portal — Faza 2 (**MVP SCOPE**)
- Staff panel frontend ([E13](e13-staff-panel-autentifikacija-i-upravljanje-osobljem.md))
- Background jobovi za poslovnu logiku (auto-expiry, AutoRenew, cleanup) — dolaze u Sprint 9–10 kao dio ovog epica ili zasebno
- Monitoring, alerting, production deployment — operativni zadaci van MVP scope-a epica
- Audit logging sistem — dolazi naknadno

**Persone:** Svi (indirektno — ovo je fundament za sve)

**Journey milestones:** J-08

**Phase:** MVP

**Dokumentacijska referenca:** Ch.08, sekcije 8.1 (single-tenant aspekt), 8.5 (tech stack); **Ch.01, sekcija 1.1** (dvojezičnost)

**Tehničke napomene:**

- Stack je decidiran: .NET 10 + MS SQL Server backend, Svelte 5 + SvelteKit + TailwindCSS + Flowbite frontend — **Ch.08, sekcija 8.5**.
- Tri odvojena frontend sistema (User, Staff, GlobalAdmin) dijele komponentnu biblioteku ali su zasebne SvelteKit aplikacije. U MVP-u se gradi User app i Staff panel; GlobalAdmin je Faza 2.
- i18n framework se mora postaviti prije Listing CRUD epica ([E02](e02-listing-crud-i-lifecycle.md)) jer dvojezična polja prolaze kroz sve entitete.
- Izbjegavati hardkodiranje tenant-specifičnih vrijednosti — koristiti konfiguracijske parametre od starta (preporuka iz **MVP SCOPE**).

**Success metrika:** Developer može lokalno pokrenuti API i frontend, kreirati migraciju, i vidjeti stranicu na oba jezika tenanta.

* * *

<a id="storije-u-ovom-epicu"></a>

## Storije u ovom epicu

| ID  | Naslov | Phase | Sprint |
| --- | --- | --- | --- |
| [S14-01](e14-infrastruktura-i18n-i-pozadinski-procesi/s14-01-postavljanje-repozitorija-i-razvojnog-okruzenja.md) | Postavljanje repozitorija i razvojnog okruženja | MVP | 0   |
| [S14-02](e14-infrastruktura-i18n-i-pozadinski-procesi/s14-02-inicijalni-net-10-api-projekat-sa-middleware-om.md) | Inicijalni .NET 10 API projekat sa middleware-om | MVP | 0   |
| [S14-03](e14-infrastruktura-i18n-i-pozadinski-procesi/s14-03-inicijalni-sveltekit-frontend-projekat.md) | Inicijalni SvelteKit frontend projekat | MVP | 0   |
| [S14-04](e14-infrastruktura-i18n-i-pozadinski-procesi/s14-04-inicijalna-db-schema-i-migracije.md) | Inicijalna DB schema i migracije | MVP | 0   |
| [S14-05](e14-infrastruktura-i18n-i-pozadinski-procesi/s14-05-single-tenant-konfiguracija-za-sarajevo.md) | Single-tenant konfiguracija za Sarajevo | MVP | 0   |
| [S14-06](e14-infrastruktura-i18n-i-pozadinski-procesi/s14-06-i18n-framework-i-lokalizacija.md) | i18n framework i lokalizacija | MVP | 0   |
| [S14-07](e14-infrastruktura-i18n-i-pozadinski-procesi/s14-07-ci-cd-pipeline.md) | CI/CD pipeline | MVP | Kad tim procijeni |