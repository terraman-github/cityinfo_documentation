---
id: S12-03
confluence_page_id: "251887641"
parent_epic: E12
linear_id: "CIT2-73"
phase: MVP
journey_milestones: [J-02, J-03, J-05, J-06]
type: backend-only
---

**Naslov:** Slanje email notifikacija

**Excerpt:** Sistem šalje email notifikacije korisnicima pri ključnim događajima — odobrenje/odbijanje listinga, nova poruka od moderatora, istek promocije. Email-ovi koriste predefinisane template-e sa konzistentnim brandingom i podrškom za dva jezika.

**Phase:** MVP

**Journey milestones:** Cross-cutting

**User story:**  
Kao registrovani korisnik,

želim primiti email kad se desi nešto bitno sa mojim listingom ili promocijom,

kako bih mogao reagovati čak i kad nisam na platformi.

**Kontekst:** Email notifikacije su drugi kanal pored in-app notifikacija. Šalju se automatski kad se dese ključni sistemski događaji. U MVP-u, svi korisnici dobijaju sve email notifikacije — nema preferenci za kontrolu tipova ili frekvencije (to dolazi u Fazi 2). Email template-i podržavaju primarni i sekundarni jezik tenanta. Detalji → **Ch.07, sekcija 7.2**.2 i 7.2.5.

**Acceptance criteria:**

- [ ] Sistem šalje email pri sljedećim događajima: listing odobren, listing odbijen, listing changes\_requested, nova poruka od moderatora, promocija uskoro ističe, promocija istekla, verifikacija uspješna, Trust Tier promjena
- [ ] Email koristi predefinisani template sa naslovom, tijelom i brandingom tenanta
- [ ] Email se šalje na registrovanu email adresu korisnika
- [ ] Template podržava primarni i sekundarni jezik (email se šalje na jeziku korisnikove preference ili primarnom jeziku tenanta)
- [ ] Email sadrži link koji vodi korisnika na relevantan dio aplikacije (listing, thread, promocija)
- [ ] Neuspješno slanje email-a ne blokira glavni proces (async slanje)
- [ ] Email notifikacija se loguje kao Notification zapis sa channel='email' (za audit, ne za in-app prikaz)

**Backend Scope:**

- EmailNotificationService — interni servis koji šalje email-ove koristeći email provider (SMTP ili transakcijski email servis)
- Integracija sa NotificationService ([S12-01](s12-01-kreiranje-i-slanje-in-app-notifikacija.md)) — kad se kreira notifikacija, paralelno se triggeruje email slanje
- Template engine: generiše email HTML na osnovu tipa notifikacije i konteksta
- Side effects: šalje email, kreira Notification zapis sa channel='email'

**Frontend Scope:** —  
*(Ovo je backend-only storija. Email se šalje automatski iz backend-a.)*

**Tehničke napomene:**

- Email slanje mora biti async — ne smije usporiti glavni proces (moderacijska odluka, kreiranje promocije itd.)
- Template-i su kategorizirani: transakcijski, moderacijski, promotivni, sistemski — **Ch.07, sekcija 7.2**.5
- Retry logika za neuspješno slanje — razmotriti jednostavan retry (1-2 pokušaja) za MVP
- Email provider se koristi kroz apstrakciju — lako zamjenjiv bez promjene poslovne logike

**Testovi (MVP):**

- [ ] Listing odobren → korisnik prima email sa naslovom, imenom listinga i linkom
- [ ] Nova poruka od moderatora → email sa obavijesti i linkom na thread
- [ ] Email sadrži branding tenanta i ispravan jezik
- [ ] Neuspješno slanje email-a → glavni proces nastavlja normalno (greška se loguje)
- [ ] Email notifikacija se loguje kao Notification zapis sa channel='email'

**Wireframe referenca:** —

**Implementacijske napomene:** Za MVP, transakcijski email servis (poput SendGrid ili sličnog) je preporučen nad čistim SMTP-om jer pruža bolju deliverability i monitoring. Template-i se mogu čuvati kao fajlovi ili u bazi — fajlovi su jednostavniji za MVP, baza je fleksibilnija dugoročno.