---
id: S01-03
confluence_page_id: "251461633"
title: "S01-03 — Verifikacija telefona (SMS)"
parent_epic: E01
linear_id: "CIT2-3"
phase: MVP
journey_milestones: [J-01]
type: fullstack
---

**Naslov:** Verifikacija telefona (SMS)

**Excerpt:** Telefon se verificira unosom SMS koda. Ovo je preduslov za kreiranje listinga — korisnik bez verificiranog telefona može pregledati sadržaj i koristiti bazične funkcije, ali ne može objavljivati. Cilj je spriječiti masovne spam račune.

**Phase:** MVP

**Journey milestones:** J-01

**User story:**  
Kao registrovani korisnik,

želim verificirati svoj telefonski broj unosom koda koji sam primio putem SMS-a,

kako bih mogao kreirati i objavljivati sadržaj na platformi.

**Kontekst:** Verifikacija telefona je odvojena od registracije — korisnik može kreirati račun i bez telefona, ali kreiranje listinga zahtijeva `phoneVerified = true` (**Ch.02, sekcija 2.7** — korak "Telefon verifikacija"). Korisnik unosi broj telefona, prima SMS sa kodom, i unosi kod na platformi. Broj telefona se čuva u `phoneNumber` polju User entiteta (**Ch.03, sekcija 3.3**).

**Acceptance criteria:**

- [ ] Korisnik može unijeti telefonski broj na svom profilu ili tokom onboardinga
- [ ] Sistem šalje SMS sa verifikacionim kodom na uneseni broj
- [ ] Korisnik unosi primljeni kod — uspješan unos postavlja `phoneVerified = true`
- [ ] Kod ima vremensko ograničenje (npr. 10 minuta) — konfigurisano, ne hardkodirano
- [ ] Pogrešan kod prikazuje jasnu grešku; višestruki neuspjeli pokušaji su rate limited
- [ ] Korisnik može zatražiti novi kod (resend) sa rate limitingom
- [ ] Promjena telefonskog broja resetuje `phoneVerified` na false i zahtijeva novu verifikaciju
- [ ] Korisnik koji pokuša kreirati listing bez verificiranog telefona dobija jasnu poruku sa linkom na verifikaciju

**Backend Scope:**

- `POST /auth/verify-phone` — prima {phoneNumber}, šalje SMS kod. Rate limited.
- `POST /auth/verify-phone/confirm` — prima {phoneNumber, code}, vraća {success}. Postavlja `phoneVerified = true`.
- Validacija: format broja, kod validnost (istekao? pogrešan?), rate limiting za slanje i pokušaje
- Side effects: slanje SMS-a putem vanjskog servisa; promjena phoneNumber resetuje `phoneVerified = false`

**Frontend Scope:**

- UI: dva koraka — (1) unos telefonskog broja sa "Pošalji kod" dugmetom; (2) unos primljenog koda sa countdown timerom i "Pošalji ponovo" opcijom
- Klijentska validacija: format telefona prije slanja
- UX: uspjeh → potvrda "Telefon verificiran ✅" + ažuriran status na profilu; greška → inline poruka (pogrešan kod, istekao, rate limited); pokušaj kreiranja listinga bez verificiranog telefona → modal/banner sa linkom na verifikaciju

**Tehničke napomene:**

- SMS slanje koristi vanjski servis (provider se bira pri implementaciji) — nije custom razvoj.
- Telefonski broj se validira na format prije slanja SMS-a.

**Testovi (MVP):**

- [ ] Unos validnog koda uspješno verificira telefon
- [ ] Istekli kod ne prolazi verifikaciju i nudi resend
- [ ] Promjena broja resetuje verifikaciju
- [ ] Pokušaj kreiranja listinga bez verificiranog telefona je blokiran sa jasnom porukom
- [ ] Rate limiting sprečava spamovanje SMS zahtjeva

**Wireframe referenca:** —