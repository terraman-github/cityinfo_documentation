---
id: E09
confluence_page_id: "252411905"
title: "E09 — Kreditni sistem i wallet"
linear_id: ""
phase: MVP
journey_milestones: [J-09]
personas: [Marko, Ana]
story_count: 4
---

**Naslov:** Kreditni sistem i wallet

**Excerpt:** Kreditni sistem je temelj monetizacije CityInfo platforme — korisnici kupuju kredite unaprijed, a zatim ih troše na promocije listinga. Ovaj prepaid model smanjuje friction pri svakoj akciji i omogućava instant aktivaciju usluga. Epic pokriva wallet, kupovinu kredit paketa, transakcijski log, i admin operacije.

**Scope — šta ulazi:**

- Automatsko kreiranje wallet-a pri registraciji korisnika (početno stanje 0)
- Prikaz dostupnih kredit paketa (CreditPackage entitet)
- Kupovina kredit paketa kroz payment gateway
- Wallet stanje vidljivo u header-u aplikacije
- Historija transakcija (CreditTransaction entitet) sa filtrima i paginacijom
- PaymentHistory za audit realnih finansijskih transakcija
- Admin operacije: dodavanje i oduzimanje kredita
- Atomske transakcije — svaka promjena balansa evidentirana u CreditTransaction

**Scope — šta NE ulazi:**

- Trošenje kredita na promocije ([E10](e10-promocije-listinga.md) — Promocije listinga)
- Display oglašavanje ([E11](e11-display-oglasavanje-mvp.md))
- Pricing prilagođavanje po tenantu (Backlog)
- A/B testiranje cijena (Backlog)
- Loyalty program i nagrade (post-MVP)

**Persone:** Marko (organizator događaja), Ana (vlasnica biznisa)

**Journey milestones:** J-09 (Wallet i plaćanje)

**Phase:** MVP

**Dokumentacijska referenca:** Ch.06, sekcije 6.1.1–6.1.7

**Tehničke napomene:**

- Wallet balance ne može biti negativan — ovo je kritično poslovno pravilo
- Svaka promjena balansa mora imati CreditTransaction zapis (atomska operacija)
- PaymentHistory je odvojen od CreditTransaction jer prati novac, ne kredite
- Kredit paketi su tenant-specifični (za MVP jedan tenant, ali struktura podržava više)
- Payment gateway integracija zahtijeva vanjski servis — specifičan provider još nije odabran

**Success metrika:** Korisnik može kupiti kredit paket, vidjeti stanje wallet-a u header-u, i pregledati kompletnu historiju transakcija — sve u manje od 3 koraka.

* * *

<a id="storije-u-ovom-epicu"></a>

## Storije u ovom epicu

| #   | Naslov | Phase | Journey |
| --- | --- | --- | --- |
| [S09-01](e09-kreditni-sistem-i-wallet/s09-01-kreiranje-wallet-a-pri-registraciji-korisnika.md) | Kreiranje wallet-a pri registraciji korisnika | MVP | **J-09** |
| [S09-02](e09-kreditni-sistem-i-wallet/s09-02-prikaz-kredit-paketa-i-kupovina-kredita.md) | Prikaz kredit paketa i kupovina kredita | MVP | **J-09** |
| [S09-03](e09-kreditni-sistem-i-wallet/s09-03-prikaz-wallet-stanja-i-historije-transakcija.md) | Prikaz wallet stanja i historije transakcija | MVP | **J-09** |
| [S09-04](e09-kreditni-sistem-i-wallet/s09-04-admin-upravljanje-kreditima.md) | Admin upravljanje kreditima | MVP | **J-09** |