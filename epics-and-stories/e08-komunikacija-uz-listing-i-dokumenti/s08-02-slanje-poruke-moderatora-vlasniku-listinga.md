---
id: S08-02
confluence_page_id: "252182548"
title: "S08-02 — Slanje poruke moderatora vlasniku listinga"
parent_epic: E08
linear_id: "CIT2-52"
phase: MVP
journey_milestones: [J-03, J-07]
type: fullstack
---

**Naslov:** Slanje poruke moderatora vlasniku listinga

**Excerpt:** Moderator pokreće komunikaciju sa vlasnikom listinga — šalje poruku koja aktivira thread i postavlja status na `waiting_owner`. Ovo je ključna akcija u moderacijskom workflow-u kad listing zahtijeva pojašnjenje, ispravku ili dokument.

**Phase:** MVP

**Journey milestones:** J-03, **J-07**

**User story:**

*Kao moderator,*  
*želim poslati poruku vlasniku listinga kroz message thread,*  
*kako bih mogao zatražiti pojašnjenje, ispravke ili dokumente bez korištenja eksternih kanala.*

**Kontekst:** Moderator pregledava listing u Staff panelu i odlučuje da treba kontaktirati vlasnika — npr. opis je nejasan, nedostaje informacija, ili treba dokaz vlasništva. Moderator piše poruku u thread-u koji već postoji za taj listing (kreiran automatski u [S08-01](s08-01-automatsko-kreiranje-message-thread-a-uz-listing.md)). Ako je thread u statusu `idle`, ovo je prva komunikacija; ako je u `waiting_moderator`, ovo je odgovor na korisnikov prethodni odgovor. U oba slučaja, thread prelazi u `waiting_owner`. Detalji o statusnom modelu i kontroli pristupa → **Ch.07, sekcija 7.1**.4.

**Acceptance criteria:**

- [ ] Moderator može poslati tekstualnu poruku u thread listinga
- [ ] Slanje poruke iz `idle` statusa mijenja thread status u `waiting_owner`
- [ ] Slanje poruke iz `waiting_moderator` statusa mijenja thread status u `waiting_owner`
- [ ] Slanje poruke iz `waiting_owner` statusa ne mijenja status (moderator dodaje pojašnjenje)
- [ ] Poruka se kreira sa `senderRole: moderator` i ispravnim `senderId`
- [ ] `messageCount` na thread-u se inkrementira, `lastMessageAt` i `lastMessageBy` se ažuriraju
- [ ] Ako je thread u `idle` statusu i nema dodijeljenog moderatora, `assignedTo` se postavlja na ID moderatora koji šalje prvu poruku
- [ ] Poruka ne može biti prazna (`messageText` obavezan, neprazan)
- [ ] Poruka se ne može poslati za listing koji je obrisan (soft deleted)

**Backend Scope:**

- `POST /threads/{threadId}/messages` — prima `{ messageText, documentIds? }`, vraća `{ messageId, threadId, sentAt, newThreadStatus }`
- Validacija: `messageText` neprazan, thread postoji, listing nije obrisan, pošiljaoc ima moderatorsku ulogu
- Side effects: ažurira thread status, `messageCount`, `lastMessageAt`, `lastMessageBy`, opciono `assignedTo`

**Frontend Scope:**

- UI: Textarea za poruku unutar thread prikaza na Staff panelu, dugme "Pošalji"
- Klijentska validacija: `messageText` neprazan prije slanja
- UX: nakon uspješnog slanja poruka se pojavljuje u thread-u, textarea se čisti; pri grešci inline poruka o grešci

**Tehničke napomene:**

- Moderator može slati poruku u bilo kojem statusu thread-a (vidi **Ch.07, sekcija 7.1**.4)
- Thread assignment (assignedTo) se postavlja samo pri prvoj poruci ako je thread bio idle — ne mijenja se ako je već dodijeljen

**Testovi (MVP):**

- [ ] Moderator šalje poruku u `idle` thread — status prelazi u `waiting_owner`, poruka je sačuvana
- [ ] Moderator šalje poruku u `waiting_moderator` thread — status prelazi u `waiting_owner`
- [ ] Moderator šalje dodatnu poruku u `waiting_owner` thread — status ostaje isti
- [ ] Pokušaj slanja prazne poruke vraća validacijsku grešku
- [ ] Poruka za obrisani listing vraća grešku
- [ ] `messageCount`, `lastMessageAt`, `lastMessageBy` su ispravno ažurirani

**Wireframe referenca:** —