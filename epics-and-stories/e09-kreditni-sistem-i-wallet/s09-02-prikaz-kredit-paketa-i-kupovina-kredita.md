---
id: S09-02
confluence_page_id: "252477441"
parent_epic: E09
linear_id: "CIT2-57"
phase: MVP
journey_milestones: [J-09]
type: fullstack
---

# S09-02 — Prikaz kredit paketa i kupovina kredita

**Naslov:** Prikaz kredit paketa i kupovina kredita

**Excerpt:** Korisnik bira jedan od ponuđenih kredit paketa, prolazi kroz payment proces, i krediti se dodaju na wallet. Ovo je centralni tok monetizacije — od odluke o kupovini do kredita na računu. Pokriva prikaz paketa, payment gateway integraciju, i kreiranje PaymentHistory + CreditTransaction zapisa.

**Phase:** MVP

**Journey milestones:** **J-09**

**User story:**  
Kao korisnik platforme,  
želim kupiti paket kredita kroz jednostavan payment proces,  
kako bih imao kredite za promociju svojih listinga.

**Kontekst:** Korisnik pristupa stranici za kupovinu kredita (direktno iz navigacije ili kroz redirect kad nema dovoljno kredita za promociju). Vidi listu dostupnih paketa sa cijenama i popustima. Bira paket, prolazi kroz payment formu (gateway integracija), i po uspješnom plaćanju krediti se dodaju na wallet. Cijeli proces od PaymentHistory do wallet update-a je atomska transakcija. Detalji o paketima → **Ch.06, sekcija 6.1**.3; workflow kupovine → **Ch.06, sekcija 6.1**.6.

**Acceptance criteria:**

- [ ] Korisnik vidi listu aktivnih kredit paketa sa: naziv, broj kredita, cijena, popust (ako postoji), cijena po kreditu
- [ ] Paketi su sortirani po `sortOrder` i označen je "best value" paket (`isPromoted: true`)
- [ ] Korisnik bira paket i prelazi na payment formu
- [ ] Po uspješnom plaćanju: kreira se PaymentHistory zapis sa `status: success`, kreira se CreditTransaction sa `type: purchase`, wallet balance se ažurira
- [ ] Sve tri operacije (PaymentHistory, CreditTransaction, wallet update) su atomska transakcija
- [ ] Po neuspješnom plaćanju: kreira se PaymentHistory sa `status: failed`, wallet se ne mijenja, korisnik vidi poruku o grešci sa opcijom retry
- [ ] Samo aktivni paketi (`isActive: true`) su vidljivi korisniku
- [ ] Korisnik ne može kupiti paket koji ne postoji ili nije aktivan

**Backend Scope:**

- `GET /credit-packages` — lista aktivnih paketa za trenutni tenant, sortiranih po `sortOrder`
- `POST /credit-packages/{id}/purchase` — inicira kupovinu: validira paket, procesira payment, kreira PaymentHistory + CreditTransaction, ažurira wallet
- Response: `{ paymentId, transactionId, newBalance }`
- Side effects: PaymentHistory zapis, CreditTransaction zapis, wallet balance update
- Validacija: paket aktivan, korisnik autentificiran

**Frontend Scope:**

- UI: Stranica "Kupovina kredita" sa karticama paketa — naziv, krediti, cijena, popust badge, "best value" badge
- UI: Payment forma (integracija sa gateway widget-om — specifičan provider TBD)
- Klijentska validacija: korisnik mora odabrati paket prije nastavka
- UX: Loading stanje tokom payment processinga; po uspjehu redirect na wallet stranicu sa success toast-om; po neuspjehu error poruka sa retry opcijom

**Tehničke napomene:**

- Payment gateway provider još nije odabran — frontend treba biti dizajniran da podrži zamjenu gateway-a bez velikih promjena
- Atomska transakcija je kritična — ne smije se desiti da se wallet ažurira bez CreditTransaction zapisa ili obrnuto
- Cijene u paketima su u lokalnoj valuti (BAM za MVP)

**Testovi (MVP):**

- [ ] Lista paketa prikazuje samo aktivne pakete sortirane po `sortOrder`
- [ ] Uspješna kupovina kreira PaymentHistory + CreditTransaction i ažurira wallet balance
- [ ] Neuspješno plaćanje kreira PaymentHistory sa `failed` statusom, wallet ostaje nepromijenjen
- [ ] Pokušaj kupovine neaktivnog paketa vraća grešku
- [ ] Wallet balance nakon kupovine = prethodno stanje + krediti iz paketa
- [ ] "Best value" badge se prikazuje na paketu sa `isPromoted: true`

**Wireframe referenca:** —

**Implementacijske napomene:** Payment gateway integracija se može inicijalno mockati za development — koristiti test mode gateway-a ili in-memory simulaciju dok se ne finalizira izbor providera.