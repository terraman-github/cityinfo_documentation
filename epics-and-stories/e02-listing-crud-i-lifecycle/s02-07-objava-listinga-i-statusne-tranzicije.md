---
id: S02-07
confluence_page_id: "251265045"
title: "S02-07 — Objava listinga i statusne tranzicije"
parent_epic: E02
linear_id: "CIT2-15"
phase: MVP
journey_milestones: [J-02, J-03]
type: fullstack
---

<a id="s02-07-objava-listinga-i-statusne-tranzicije"></a>

# S02-07 — Objava listinga i statusne tranzicije

**Naslov:** Objava listinga i statusne tranzicije

**Excerpt:** Pokriva centralni tok od drafta do javno vidljivog listinga — submit na moderaciju, statusne tranzicije (draft → in\_review → published za pre-mod; draft → published\_under\_review → published za post-mod), te changes\_requested timeout mehanizam. `listingStatus` je jedini status field koji kontrolira vidljivost i stanje listinga.

**Phase:** MVP

**Journey milestones:** J-02, **J-03**

**User story:**

*Kao korisnik platforme,*  
*želim objaviti svoj pripremljeni listing tako da postane vidljiv javnosti,*  
*kako bi posjetioci mogli pronaći moj događaj ili mjesto.*

**Kontekst:** Korisnik je kreirao listing ([S02-01](s02-01-kreiranje-event-listinga-sa-osnovnim-podacima.md) ili [S02-02](s02-02-kreiranje-place-listinga-sa-osnovnim-podacima.md)), dodao lokaciju (za Event — [S02-03](s02-03-lokacija-event-a-povezivanje-sa-place-om-ili-rucna-adresa.md)), i opciono uploadovao slike/dokumente. Sada klikće "Objavi". Dalji tok zavisi od Trust Tier-a korisnika — pre-moderacija (Tier 0–1: listing čeka odobrenje) ili post-moderacija (Tier 2+: listing odmah vidljiv uz naknadni pregled). `isPublic` se derivira iz `listingStatus` — nije zasebno polje koje se upisuje. Statusni dijagram → **Ch.04, sekcija 4.8**. Korisničko iskustvo objave → **Ch.02, sekcija 2.8**.

**Acceptance criteria:**

- [ ] Korisnik može kliknuti "Objavi" na draft listingu
- [ ] Validacija pri submitu: svi obavezni podaci moraju biti popunjeni (uključujući lokaciju za Event)
- [ ] **Pre-moderacija (Tier 0, 1):** listing prelazi u `listingStatus = in_review`
- [ ] Korisnik vidi poruku: "Vaš sadržaj je poslan na pregled. Obavijestit ćemo vas čim bude odobren."
- [ ] **Post-moderacija (Tier 2+):** listing prelazi u `listingStatus = published_under_review` — odmah vidljiv posjetiocima, uz naknadni pregled
- [ ] Korisnik vidi poruku: "Vaš sadržaj je objavljen! Naš tim će ga pregledati u narednim satima."
- [ ] Kada moderator vrati listing na doradu, listing prelazi u `listingStatus = changes_requested` — nevidljiv posjetiocima
- [ ] Korisnik vidi poruku: "Potrebne su male izmjene prije objave. Pogledajte komentare."
- [ ] Korisnik može resubmitovati listing iz `changes_requested` → prelazi u `in_review`
- [ ] Timeout za `changes_requested`: ako korisnik ne reaguje unutar `CHANGES_REQUESTED_TIMEOUT_DAYS` dana → listing automatski prelazi u `rejected`
- [ ] Reminder notifikacija se šalje `CHANGES_REQUESTED_REMINDER_DAYS` dana prije isteka
- [ ] `isPublic` se automatski derivira iz `listingStatus` — ne postavlja se ručno
- [ ] Korisnik može pratiti status svojih listinga na profilu (draft, čeka pregled, objavljen, odbijen, itd.)
- [ ] Korisnik može povući submission iz `in_review` nazad u `draft`

**Backend Scope:**

- `POST /events/{id}/submit` — validira kompletnost, postavlja `listingStatus` ovisno o Trust Tier-u (`in_review` za Tier 0–1, `published_under_review` za Tier 2+)
- `POST /places/{id}/submit` — ista logika za Place
- `POST /events/{id}/withdraw` — povlači submission iz `in_review` nazad u `draft`
- `POST /places/{id}/withdraw` — isto za Place
- Validacija: svi obavezni atributi popunjeni, za Event obavezna lokacija (placeId ili ručna adresa), listing mora biti u `draft` ili `changes_requested` statusu za submit, u `in_review` za withdraw
- Side effects: za pre-mod — kreira stavku u moderacijskom redu; za post-mod — listing odmah vidljiv, kreira stavku za naknadni pregled po sampling logici; za `changes_requested` — pokreće timeout timer; šalje reminder notifikaciju prije isteka; pri post-mod submitu — `wasEverActive` se postavlja na `true`
- Background job: `ChangesRequestedTimeoutChecker` — periodično provjerava istekle listinge i prebacuje ih u `rejected`

**Frontend Scope:**

- UI: "Objavi" dugme na draft stranici; "Povuci" dugme za listing u `in_review`; status indikator na profilu i listing stranici; poruke korisniku ovisno o scenariju (**Ch.02**, 2.8)
- Klijentska validacija: provjera da su svi obavezni podaci popunjeni prije slanja submit zahtjeva
- UX: nakon submita — poruka prilagođena scenariju (pre-mod vs post-mod); na profilu — lista listinga sa statusima; za `changes_requested` — vidljiv countdown do isteka sa linkom na komentare

**Tehničke napomene:**

- Trust Tier provjera se radi na backend-u — frontend ne odlučuje o pre/post moderaciji, samo prikazuje rezultat
- Moderatorski dio workflow-a (approve, reject, changes\_requested akcije) pripada [E07](../e07-moderacijski-workflow-i-ai-screening.md)
- Timeout background job treba biti idempotent i otporan na restarte
- `CHANGES_REQUESTED_TIMEOUT_DAYS` i `CHANGES_REQUESTED_REMINDER_DAYS` su parametri iz konfiguracije (preporučene početne vrijednosti: 7 i 5 dana)
- `listingStatus` je jedini status field — nema odvojenog `lifecycleStatus` ni `moderationStatus`

**Testovi (MVP):**

- [ ] Happy path (pre-mod): submit draft-a kao Tier 1 korisnik → `listingStatus = in_review`, poruka o čekanju
- [ ] Happy path (post-mod): submit draft-a kao Tier 2+ korisnik → `listingStatus = published_under_review`, poruka o objavi
- [ ] Submit sa nepopunjenim obaveznim poljem → validacijska greška, listing ostaje draft
- [ ] Submit Event-a bez lokacije → validacijska greška
- [ ] Resubmit iz `changes_requested` → `listingStatus = in_review`
- [ ] Withdraw iz `in_review` → `listingStatus = draft`
- [ ] `changes_requested` timeout istekao → listing automatski `rejected`
- [ ] `changes_requested` reminder → notifikacija poslana na `CHANGES_REQUESTED_REMINDER_DAYS` dan
- [ ] `isPublic` derivacija: `published`/`published_under_review`/`published_needs_changes` → true; ostalo → false
- [ ] Korisnik može vidjeti status svih svojih listinga na profilu

**Wireframe referenca:** —

**Implementacijske napomene:**

- Pre/post moderacija logika može koristiti Strategy pattern — isti submit endpoint, različito ponašanje ovisno o tier-u
- Timeout checker može biti implementiran kao periodični background service ili scheduler