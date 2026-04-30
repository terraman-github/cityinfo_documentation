---
id: S02-09
confluence_page_id: "251428910"
title: "S02-09 — Ručno osvježavanje sortDate i praćenje statusa objave"
parent_epic: E02
linear_id: "CIT2-17"
phase: MVP
journey_milestones: [J-02]
type: fullstack
---

<a id="s02-09-ručno-osvježavanje-sortdate-i-praćenje-statusa-objave"></a>

# S02-09 — Ručno osvježavanje sortDate i praćenje statusa objave

**Naslov:** Ručno osvježavanje sortDate i praćenje statusa objave

**Excerpt:** Svaki korisnik može besplatno osvježiti poziciju svog listinga jednom u 24 sata. Uz to, ova storija pokriva i korisnički dashboard za praćenje statusa svih listinga — pregled draftova, listinga na pregledu, objavljenih, sakrivenih i uklonjenih listinga na jednom mjestu.

**Phase:** MVP

**Journey milestones:** J-02

**User story:**  
Kao vlasnik listinga,

želim moći osvježiti poziciju svog listinga u rezultatima i pratiti status svih svojih objava,

kako bih imao pregled i kontrolu nad vidljivošću svog sadržaja.

**Kontekst:** `sortDate` je centralni mehanizam za pozicioniranje listinga u svim sortiranim prikazima (**Ch.02**, 2.4). Ručno osvježavanje postavlja `sortDate` na trenutno vrijeme — efektivno "bumpujući" listing na vrh. Dostupno svim korisnicima, jednom u 24 sata, besplatno. Korisničko iskustvo praćenja statusa → **Ch.02, sekcija 2.8**.

**Acceptance criteria:**

**Ručno osvježavanje sortDate:**

- [ ] Korisnik može kliknuti "Osvježi poziciju" na objavljenom listingu
- [ ] `sortDate` se postavlja na trenutno vrijeme
- [ ] `lastManualRefreshAt` se ažurira
- [ ] Cooldown: korisnik ne može ponovo osvježiti isti listing unutar 24 sata od zadnjeg osvježavanja
- [ ] Ako je cooldown aktivan, dugme je disabled sa prikazom preostalog vremena ("Možete osvježiti za X sati")
- [ ] Osvježavanje je dostupno samo za listinge sa `listingStatus` u javno vidljivom statusu (`published`, `published_under_review`, `published_needs_changes`)

**Praćenje statusa objave (korisnički dashboard):**

- [ ] Na korisničkom profilu postoji sekcija "Moji listinzi"
- [ ] Listinzi su grupisani ili filtrirani po statusnoj grupi: draft, čeka pregled (`in_review`), objavljen (`published`, `published_under_review`, `published_needs_changes`), sakriven (`hidden_by_owner`), potrebne izmjene (`changes_requested`), odbijen/istekao/uklonjen
- [ ] Svaki listing prikazuje: naziv, tip (Event/Place), `listingStatus` u čitljivom formatu, datum kreiranja/ažuriranja
- [ ] Za objavljen listing: prikazuje se `sortDate` i opcija za ručno osvježavanje
- [ ] Za listing u `changes_requested`: prikazuje se countdown do isteka timeout-a i link na komentare moderatora
- [ ] Za `hidden_by_owner`: prikazuje se opcija za prikazivanje (unhide)
- [ ] Za `canceled` event: prikazuje se opcija za reaktivaciju (ako `endDateTime > NOW()`)

**Backend Scope:**

- `POST /events/{id}/refresh` — osvježava `sortDate`, provjerava 24h cooldown
- `POST /places/{id}/refresh` — ista logika za Place
- `GET /users/me/listings` — vraća listu korisnikovih listinga sa statusima (paginacija, filtriranje po statusu)
- Validacija: listing mora biti u javno vidljivom statusu (`isPublic = true`), 24h cooldown od `lastManualRefreshAt`, korisnik mora biti vlasnik
- Side effects: ažurira `sortDate` i `lastManualRefreshAt`

**Frontend Scope:**

- UI: "Osvježi poziciju" dugme na objavljenom listingu sa cooldown indikatorom; dashboard sekcija "Moji listinzi" na profilu sa tabelom/kartama
- Klijentska validacija: nema — cooldown se provjerava na serveru
- UX: pri uspješnom osvježavanju toast "Pozicija osvježena!"; cooldown countdown u realnom vremenu; filteri po statusnoj grupi na dashboardu

**Tehničke napomene:**

- AutoRenew (automatsko osvježavanje) pripada [E10](../e10-promocije-listinga.md) (promocije) — ova storija pokriva samo ručno, besplatno osvježavanje
- Dashboard za praćenje statusa je osnovni — napredna statistika (views, klikovi) može doći u kasnijoj fazi

**Testovi (MVP):**

- [ ] Happy path: osvježavanje objavljenog listinga → `sortDate` ažuriran na trenutno vrijeme
- [ ] Pokušaj osvježavanja unutar 24h → greška sa preostalim vremenom
- [ ] Osvježavanje draft/in\_review listinga → greška
- [ ] Osvježavanje tuđeg listinga → greška
- [ ] Dashboard prikazuje listinge po statusnim grupama sa ispravnim informacijama
- [ ] Dashboard za listing sa `changes_requested` prikazuje countdown
- [ ] Dashboard za `hidden_by_owner` prikazuje unhide opciju

**Wireframe referenca:** —

**Implementacijske napomene:**

- Cooldown provjera: `DateTime.Now - lastManualRefreshAt >= 24h`
- Dashboard može koristiti lazy loading za performanse ako korisnik ima mnogo listinga
- Razmotriti WebSocket/SSE za real-time countdown na `changes_requested` (ili jednostavniji polling)