---
id: S10-02
confluence_page_id: "252510228"
title: "S10-02 — Prikaz promotivnih listinga (sortiranje i vizualno isticanje)"
parent_epic: E10
linear_id: "CIT2-61"
phase: MVP
journey_milestones: [J-06]
type: fullstack
---

**Naslov:** Prikaz promotivnih listinga (sortiranje i vizualno isticanje)

**Excerpt:** Promotivni listinzi se ističu vizualno i poziciono u listama i na naslovnoj stranici. Premium listinzi su izdvojeni na vrhu kategorije, Standard su izmiješani sa običnim ali vizualno istaknuti. Na naslovnoj, Premium+Homepage imaju apsolutni prioritet. Ovo je "vidljivi" dio promotivnog sistema — ono što korisnici i posjetioci zapravo vide.

**Phase:** MVP

**Journey milestones:** J-06

**User story:**  
Kao posjetilac platforme,

želim vidjeti istaknute listinge na naslovnoj i u kategorijama,

kako bih mogao otkriti najrelevantnije i najaktuelnije sadržaje.

**Kontekst:** Kada korisnik pregledava naslovnu stranicu ili listu listinga u kategoriji, sistem prikazuje tri grupe sadržaja: Premium sekcija na vrhu (sortirani po sortDate), zatim Standard i obični izmiješani (također po sortDate). Na naslovnoj stranici, Premium+Homepage ima dodatni apsolutni prioritet. Svaki promotivni listing ima vizualno isticanje — badge, border, pozadina. Detalji o sortiranju → **Ch.06, sekcija 6.2**.3; naslovna → **Ch.02, sekcija 2.1**.

**Acceptance criteria:**

- [ ] U kategorijskoj listi: Premium listinzi su izdvojeni u zasebnu sekciju na vrhu, međusobno sortirani po `sortDate` (noviji prvo)
- [ ] U kategorijskoj listi: Standard promocije i obični listinzi su izmiješani ispod premium sekcije, svi sortirani po `sortDate`
- [ ] Na naslovnoj: Premium+Homepage listinzi su u prvoj grupi (apsolutni prioritet), ostali Premium u drugoj, Standard+obični u trećoj
- [ ] Standard promocija ima blagi vizualni highlight (border ili pozadina) ali bez "Premium" badge-a
- [ ] Premium promocija ima jak vizualni highlight + "Premium" badge
- [ ] Premium+Homepage ima "Premium" + "Featured" badge
- [ ] Pauzirana promocija ne prikazuje promotivno isticanje — listing se tretira kao obični
- [ ] Istekla promocija (`status: expired`) ne prikazuje isticanje

**Backend Scope:**

- Postojeći listing query endpoint-i (iz [E04](../e04-otkrivanje-i-pretraga-sadrzaja.md)) prošireni sa promotion-aware sortiranjem
- Query vraća `promotionInfo` za svaki listing: `{ promoType, showOnHomepage, isActive }` ili `null` ako nema promocije
- Sortiranje: Premium (`promoType: premium` + `status: active`) na vrh, zatim ostali po `sortDate`

**Frontend Scope:**

- UI: Premium sekcija vizualno odvojena od ostatka liste (separator ili drugačija pozadina)
- UI: Badge komponente: "Standard" (blagi), "Premium" (jak), "Featured" (naslovnica)
- UI: Kartice sa promotivnim listingom imaju vizualno isticanje (border, shadow, badge)
- UX: Korisnik jasno razlikuje promotivne od običnih listinga bez da se osjeti "spammy"

**Tehničke napomene:**

- Sortiranje mora uzeti u obzir i promoType i sortDate — nije dovoljno sortirati samo po jednom
- Premium sekcija ima fiksno mjesto (vrh) — ne paginirano zajedno sa običnim listinzima
- Naslovnica ima specifičnu logiku za tri grupe — vidi **Ch.02, sekcija 2.1**

**Testovi (MVP):**

- [ ] Kategorijska lista prikazuje Premium listinge na vrhu, sortirane po sortDate
- [ ] Standard promocija se prikazuje izmiješano sa običnim ali sa vizuelnim highlight-om
- [ ] Naslovnica prikazuje tri grupe u ispravnom redoslijedu
- [ ] Pauzirana promocija se ne prikazuje sa isticanjem
- [ ] Istekla promocija se ne prikazuje sa isticanjem
- [ ] Listing bez promocije nema nikakvo isticanje

**Wireframe referenca:** —