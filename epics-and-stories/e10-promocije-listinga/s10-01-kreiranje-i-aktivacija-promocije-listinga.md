---
id: S10-01
confluence_page_id: "252542977"
title: "S10-01 — Kreiranje i aktivacija promocije listinga"
parent_epic: E10
linear_id: "CIT2-60"
phase: MVP
journey_milestones: [J-06]
type: fullstack
---

**Naslov:** Kreiranje i aktivacija promocije listinga

**Excerpt:** Korisnik bira tip promocije (Standard, Premium, ili Premium+Homepage), trajanje, i opciono AutoRenew — sistem naplaćuje kredite iz wallet-a i instant aktivira promociju. Ovo je centralni tok promotivnog sistema koji povezuje wallet sa vidljivošću listinga.

**Phase:** MVP

**Journey milestones:** J-06

**User story:**  
Kao vlasnik listinga,

želim kreirati promociju za svoj listing birajući tip i trajanje,

kako bi moj listing bio istaknutiji i vidljiviji potencijalnim posjetiocima.

**Kontekst:** Korisnik pristupa opciji promocije kroz listing detail stranicu ili kroz "Moji listinzi" pregled. Bira tip promocije (Standard/Premium/Premium+Homepage), trajanje (1/3/7/30 dana), i opciono AutoRenew interval. Sistem kalkuliše ukupnu cijenu u kreditima, provjerava wallet balance, i po potvrdi instant aktivira promociju. Listing mora biti javno vidljiv (`isPublic = true`). Detalji o tipovima → **Ch.06, sekcija 6.2**.3; workflow → **Ch.06, sekcija 6.2**.6; poslovna pravila → **Ch.06, sekcija 6.2**.7.

**Acceptance criteria:**

- [ ] Korisnik može kreirati promociju birajući: tip (standard/premium), trajanje, showOnHomepage (samo za premium), autoRenewEnabled, autoRenewInterval
- [ ] Sistem kalkuliše ukupnu cijenu na osnovu tipa i trajanja (vidi pricing tabelu **Ch.06, sekcija 6.5**.3)
- [ ] Ako korisnik nema dovoljno kredita, prikazuje se poruka sa linkom na kupovinu kredita
- [ ] Po potvrdi: kreira se Promo entitet sa `status: active`, kreira se CreditTransaction sa `type: promo_purchase`, wallet balance se umanjuje
- [ ] Promocija se aktivira instant — `startDate = NOW()`, `endDate = NOW() + trajanje`
- [ ] Samo javno vidljivi listinzi (`isPublic = true`) mogu imati promociju
- [ ] Listing ne može imati više od jedne aktivne promocije istovremeno
- [ ] `showOnHomepage` opcija je dostupna samo za `promoType: premium`
- [ ] Ako je AutoRenew enabled, postavljaju se `autoRenewInterval` i `nextAutoRenewAt`
- [ ] Kreiranje promocije atomski ažurira listing `sortDate` na NOW()

**Backend Scope:**

- `POST /promotions` — prima `{ targetType, targetId, promoType, durationDays, showOnHomepage, autoRenewEnabled, autoRenewInterval? }`, vraća `{ promoId, status, startDate, endDate, creditsCost }`
- `GET /promotions/pricing` — vraća pricing tabelu za sve kombinacije tipa i trajanja
- Validacija: listing javno vidljiv (`isPublic = true`), nema aktivne promocije, dovoljno kredita, showOnHomepage samo za premium
- Side effects: Promo kreiran, CreditTransaction kreiran, wallet balance ažuriran, listing sortDate ažuriran

**Frontend Scope:**

- UI: Promotion wizard / forma: korak 1 — odabir tipa sa opisom razlika; korak 2 — trajanje i opcije; korak 3 — pregled i potvrda sa prikazom cijene
- UI: Cijena se dinamički ažurira pri promjeni opcija
- UI: "Nedovoljno kredita" stanje sa CTA za kupovinu
- Klijentska validacija: tip odabran, trajanje odabrano, showOnHomepage samo za premium
- UX: Po uspjehu redirect na listing sa success toast-om; listing odmah prikazuje promotivno isticanje

**Tehničke napomene:**

- Prepaid model — nema pending payment-a, sve se naplaćuje instant iz wallet-a
- Atomska operacija: Promo + CreditTransaction + wallet update + sortDate update moraju biti u istoj transakciji
- AutoRenew pricing još nije finaliziran — za sada koristiti baznu cijenu bez AutoRenew dodatka

**Testovi (MVP):**

- [ ] Kreiranje Standard promocije na 7 dana: Promo kreiran, wallet umanjen za 140 kredita, listing sortDate ažuriran
- [ ] Kreiranje Premium+Homepage: showOnHomepage = true, ispravna cijena
- [ ] Pokušaj promocije sa nedovoljno kredita vraća grešku sa porukom
- [ ] Pokušaj promocije za listing koji nije javno vidljiv (`isPublic = false`) vraća grešku
- [ ] Pokušaj kreiranja druge promocije za listing koji već ima aktivnu vraća grešku
- [ ] Pokušaj showOnHomepage za Standard tip vraća validacijsku grešku
- [ ] AutoRenew enabled postavlja `nextAutoRenewAt` na `NOW() + interval`

**Wireframe referenca:** —