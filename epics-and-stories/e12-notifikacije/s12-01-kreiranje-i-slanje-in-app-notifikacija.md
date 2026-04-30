---
id: S12-01
confluence_page_id: "252084245"
parent_epic: E12
linear_id: "CIT2-71"
phase: MVP
journey_milestones: [J-02, J-03, J-05, J-06]
type: backend-only
---

# S12-01 — Kreiranje i slanje in-app notifikacija

**Naslov:** Kreiranje i slanje in-app notifikacija

**Excerpt:** Backend infrastruktura za kreiranje Notification zapisa u bazi i njihovo slanje kao in-app notifikacije. Ovo je temelj notifikacijskog sistema — svaki sistemski događaj koji zahtijeva korisnikovu pažnju kreira Notification zapis koji se prikazuje u aplikaciji.

**Phase:** MVP

**Journey milestones:** Cross-cutting

**User story:**  
Kao sistem,  
želim kreirati i pohraniti notifikaciju svaki put kad se desi bitan događaj za korisnika,  
kako bi korisnik bio obaviješten o promjenama na svojim listinzima, porukama i promocijama.

**Kontekst:** Notification entitet evidentira svaku notifikaciju sa tipom, referencom na povezani entitet, statusom čitanja i kanalom. In-app notifikacije (channel='in\_app') su vidljive korisniku u aplikaciji; email notifikacije (channel='email') se loguju ali nisu vidljive u in-app listi. Svaki tip notifikacije ima predefinisan naslov i tijelo koje se generira na osnovu konteksta događaja. Detalji o Notification entitetu → **Ch.07, sekcija 7.2**.3.

**Acceptance criteria:**

- [ ] Notification entitet se kreira sa svim atributima iz specifikacije: notificationId, userId, type, title, body, referenceType, referenceId, isRead, channel, sentAt
- [ ] Podržani tipovi notifikacija: listing\_approved, listing\_rejected, listing\_changes\_requested, new\_message, promotion\_expiring, promotion\_expired, verification\_approved, trust\_tier\_changed, changes\_timeout\_reminder, system\_announcement
- [ ] Svaka in-app notifikacija ima referenceType i referenceId za navigaciju pri kliku (npr. referenceType='listing', referenceId=listingId)
- [ ] Notifikacija se kreira sa isRead=false
- [ ] Naslov i tijelo notifikacije su generirani na osnovu tipa i konteksta (npr. "Listing odobren" + ime listinga)
- [ ] Notifikacije podržavaju primarni i sekundarni jezik tenanta

**Backend Scope:**

- Interni servis (NotificationService) sa metodom `CreateNotification(userId, type, referenceType?, referenceId?, additionalContext?)` — kreira Notification zapis u bazi
- Notification entitet prema specifikaciji iz **Ch.07, sekcija 7.2**.3
- Servis generiše title i body na osnovu tipa i konteksta (template pattern)
- Side effects: kreira zapis u bazi; u budućim storijama ([S12-03](s12-03-slanje-email-notifikacija.md)) triggeruje i email slanje

**Frontend Scope:** —  
*(Ovo je backend-only storija. Frontend prikaz je u [S12-02](s12-02-prikaz-notifikacija-i-badge-neprocitanih.md).)*

**Tehničke napomene:**

- NotificationService je centralna tačka za kreiranje svih notifikacija — ostali servisi (ListingService, ModerationService, PromoService) ga pozivaju kad se dese relevantni događaji
- Template-i za naslov/tijelo su konfigurisani — ne hardkodirani u kodu
- Notification entitet podržava channel polje za budući multi-channel pristup (email, push)

**Testovi (MVP):**

- [ ] Kreiranje notifikacije tipa listing\_approved → zapis u bazi sa ispravnim tipom, naslovom, tijelom i referencom
- [ ] Kreiranje notifikacije → isRead=false po defaultu
- [ ] Kreiranje sa referenceType='listing' i referenceId → ispravno pohranjeno
- [ ] Kreiranje notifikacije na sekundarnom jeziku → naslov i tijelo na sekundarnom jeziku

**Wireframe referenca:** —

**Implementacijske napomene:** NotificationService treba biti dovoljno generičan da podrži nove tipove notifikacija bez promjene koda — samo dodavanje novog template-a. Razmotriti async kreiranje notifikacija (queue) ako se pokaže da sinhrone operacije usporavaju glavne tokove.