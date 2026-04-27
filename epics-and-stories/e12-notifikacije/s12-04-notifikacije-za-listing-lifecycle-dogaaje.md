---
id: S12-04
parent_epic: E12
linear_id: ""
phase: MVP
journey_milestones: [J-02, J-03]
type: backend-only
---

# S12-04 — Notifikacije za listing lifecycle događaje

**Naslov:** Notifikacije za listing lifecycle događaje

**Excerpt:** Sistem automatski obavještava vlasnika listinga kad se desi promjena statusa — odobrenje, odbijanje, zahtjev za izmjenama, ili podsjetnik da rok za izmjene ističe. Notifikacije su prilagođene Trust Tier nivou korisnika — Tier 0-1 dobija sve moderacijske obavijesti, dok Tier 2+ dobija obavijesti samo ako moderator naknadno pronađe problem.

**Phase:** MVP

**Journey milestones:** J-02, J-03

**User story:**  
Kao vlasnik listinga,  
želim biti obaviješten kad moderator donese odluku o mom listingu,  
kako bih mogao reagovati na vrijeme — bilo da je listing odobren, treba doradu, ili je odbijen.

**Kontekst:** Listing lifecycle prolazi kroz moderacijski workflow (Ch.05) gdje moderator donosi jednu od tri odluke: approved, changes\_requested, rejected. Svaka od ovih odluka triggeruje notifikaciju vlasniku (in-app + email). Dodatno, ako je listing u statusu changes\_requested i korisnik nije reagovao, sistem šalje podsjetnik (changes\_timeout\_reminder). Notifikacije su prilagođene Trust Tier nivou — Ch.07, sekcija 7.2.6.

**Acceptance criteria:**

- [ ] Kad moderator odobri listing → vlasnik prima in-app i email notifikaciju tipa listing\_approved sa imenom listinga i linkom
- [ ] Kad moderator odbije listing → vlasnik prima notifikaciju tipa listing\_rejected sa razlogom odbijanja i linkom
- [ ] Kad moderator zatraži izmjene → vlasnik prima notifikaciju tipa listing\_changes\_requested sa opisom šta treba promijeniti i linkom
- [ ] Kad listing čeka izmjene duže od konfigurabilnog perioda → sistem šalje changes\_timeout\_reminder notifikaciju
- [ ] Tier 0-1 korisnici primaju notifikaciju o čekanju na pregled kad listing uđe u moderacijski queue
- [ ] Tier 2+ korisnici primaju notifikaciju samo kad moderator naknadno pronađe problem (post-moderacija)
- [ ] Notifikacija za novu poruku od moderatora (new\_message) se šalje kad moderator pošalje poruku kroz Message sistem (Ch.07, sekcija 7.1)
- [ ] Sve notifikacije sadrže referenceType='listing' i referenceId=listingId za navigaciju

**Backend Scope:**

- Integracija sa ModerationService — pri svakoj moderacijskoj odluci, poziva NotificationService.CreateNotification()
- Integracija sa MessageService — pri slanju poruke od moderatora, kreira new\_message notifikaciju
- Trust Tier aware logika: provjera korisnikovog Trust Tier-a za određivanje tipova notifikacija
- Background job za changes\_timeout\_reminder — periodična provjera listinga u changes\_requested statusu
- Side effects: kreira Notification zapise, triggeruje email slanje (S12-03)

**Frontend Scope:** —  
*(Ovo je backend-only storija za integraciju notifikacija sa listing lifecycle-om. Frontend prikaz notifikacija je u S12-02.)*

**Tehničke napomene:**

- Trust Tier aware notifikacije ne zahtijevaju složenu logiku — jednostavna provjera korisnikovog tier-a pri kreiranju notifikacije
- changes\_timeout\_reminder se može realizirati kroz postojeći background job infrastrukturu (E14)
- Razmotriti konfigurabilni period za timeout reminder (npr. 5 dana od changes\_requested)

**Testovi (MVP):**

- [ ] Moderator odobri listing Tier 1 korisnika → korisnik prima in-app + email notifikaciju listing\_approved
- [ ] Moderator odbije listing → korisnik prima listing\_rejected sa razlogom
- [ ] Moderator zatraži izmjene → korisnik prima listing\_changes\_requested
- [ ] Listing čeka izmjene 5+ dana → korisnik prima changes\_timeout\_reminder
- [ ] Tier 2 korisnik objavi listing (post-moderacija) → ne prima notifikaciju o čekanju na pregled
- [ ] Moderator pošalje poruku → vlasnik prima new\_message notifikaciju

**Wireframe referenca:** —

**Implementacijske napomene:** Integracija sa moderacijskim workflowom treba biti labavo vezana — NotificationService se poziva nakon što je moderacijska odluka uspješno zapisana, ne kao dio iste transakcije. Ovo osigurava da neuspješno slanje notifikacije ne rollbackuje moderacijsku odluku.