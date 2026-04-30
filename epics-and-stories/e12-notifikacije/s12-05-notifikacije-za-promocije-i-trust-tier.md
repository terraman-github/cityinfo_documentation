---
id: S12-05
confluence_page_id: "252837889"
title: "S12-05 — Notifikacije za promocije i Trust Tier"
parent_epic: E12
linear_id: "CIT2-75"
phase: MVP
journey_milestones: [J-06]
type: backend-only
---

**Naslov:** Notifikacije za promocije i Trust Tier

**Excerpt:** Sistem obavještava korisnike kad im promocija uskoro ističe ili je istekla, kad je verifikacija vlasništva uspješna, i kad se promijeni Trust Tier nivo. Ove notifikacije pomažu korisnicima da pravovremeno reaguju na promjene koje utiču na vidljivost njihovog sadržaja i status na platformi.

**Phase:** MVP

**Journey milestones:** J-06

**User story:**  
Kao vlasnik listinga sa aktivnom promocijom,

želim biti obaviješten kad mi promocija ističe ili kad se promijeni moj Trust Tier status,

kako bih mogao pravovremeno obnoviti promociju ili razumjeti novi status na platformi.

**Kontekst:** Promocije imaju definisan endDate nakon kojeg prestaju. Sistem treba obavijestiti korisnika unaprijed (npr. 1 dan prije isteka) da ima vremena za akciju — produženje ili novu promociju. Trust Tier promjene (napredovanje ili degradacija) značajno utiču na korisnikovo iskustvo (pre-moderacija vs post-moderacija), pa je bitno da korisnik razumije šta se promijenilo. Detalji o promocijama → **Ch.06, sekcija 6.2**; Trust Tier → **Ch.03, sekcija 3.4**; tipovi notifikacija → **Ch.07, sekcija 7.2**.3.

**Acceptance criteria:**

- [ ] Kad promocija ističe u narednih 24h → korisnik prima promotion\_expiring notifikaciju sa imenom listinga i preostalim vremenom
- [ ] Kad promocija istekne → korisnik prima promotion\_expired notifikaciju
- [ ] Kad verifikacija vlasništva bude uspješna → korisnik prima verification\_approved notifikaciju
- [ ] Kad se korisnikov Trust Tier promijeni (napredovanje ili degradacija) → korisnik prima trust\_tier\_changed notifikaciju sa objašnjenjem šta novi tier znači
- [ ] trust\_tier\_changed notifikacija objašnjava praktičnu razliku (npr. "Vaš sadržaj više ne čeka odobrenje prije objave" za napredovanje na Tier 2)
- [ ] Sve notifikacije sadrže odgovarajući referenceType i referenceId za navigaciju
- [ ] Notifikacije se šalju i kao in-app i kao email

**Backend Scope:**

- Integracija sa PromoService — pri isteku promocije i pri promotion\_expiring provjeri (background job)
- Background job: periodična provjera promocija koje ističu u narednih 24h → kreira promotion\_expiring notifikaciju (jednom po promociji)
- Integracija sa TrustTierService — pri promjeni tier-a, kreira trust\_tier\_changed notifikaciju
- Integracija sa VerificationService — pri uspješnoj verifikaciji, kreira verification\_approved notifikaciju
- Side effects: kreira Notification zapise, triggeruje email slanje ([S12-03](s12-03-slanje-email-notifikacija.md))

**Frontend Scope:** —  
*(Backend-only storija. Frontend prikaz notifikacija je u [S12-02](s12-02-prikaz-notifikacija-i-badge-neprocitanih.md).)*

**Tehničke napomene:**

- promotion\_expiring se triggeruje background jobom koji provjerava promocije koje ističu u narednih 24h — job treba osigurati da se notifikacija šalje samo jednom (flag ili zapis)
- Trust Tier promjena notifikacija treba sadržavati human-readable objašnjenje novog tier-a, ne samo broj
- Verifikacija se odnosi na dokument review (ListingDocument workflow iz **Ch.04, sekcija 4.7**)

**Testovi (MVP):**

- [ ] Promocija ističe za 24h → korisnik prima promotion\_expiring notifikaciju
- [ ] Promocija istekla → korisnik prima promotion\_expired
- [ ] Korisnik napreduje sa Tier 1 na Tier 2 → prima trust\_tier\_changed sa objašnjenjem o post-moderaciji
- [ ] Korisnik degradira sa Tier 2 na Tier 1 → prima trust\_tier\_changed sa objašnjenjem o pre-moderaciji
- [ ] Verifikacija uspješna → korisnik prima verification\_approved
- [ ] promotion\_expiring se šalje samo jednom po promociji (ne pri svakom pokretanju background joba)

**Wireframe referenca:** —

**Implementacijske napomene:** Za promotion\_expiring, najjednostavniji pristup je dodati boolean flag `expiringNotificationSent` na Promo entitet ili zaseban zapis u notifikacijskoj tabeli da spriječi duplikatno slanje. Background job se pokreće jednom dnevno ili svakih par sati.