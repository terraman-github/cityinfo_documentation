---
id: S02-06
confluence_page_id: "250478633"
title: "S02-06 — Upload i upravljanje dokumentima listinga"
parent_epic: E02
linear_id: "CIT2-14"
phase: MVP
journey_milestones: [J-02, J-07]
type: fullstack
---

<a id="s02-06-upload-i-upravljanje-dokumentima-listinga"></a>

# S02-06 — Upload i upravljanje dokumentima listinga

**Naslov:** Upload i upravljanje dokumentima listinga

**Excerpt:** Korisnik može priložiti dokumente uz listing — za verifikaciju vlasništva, pojašnjenja tražena od moderatora, ili druge svrhe. Dokumenti prolaze automatski virus scanning i centralizirani su u ListingDocument entitetu.

**Phase:** MVP

**Journey milestones:** J-02, **J-07**

**User story:**  
Kao vlasnik listinga,

želim priložiti dokumente uz svoj listing (npr. dokaz vlasništva ili dozvolu za događaj),

kako bih ubrzao proces moderacije i dobio verifikacioni badge.

**Kontekst:** Korisnik ima kreiran listing u bilo kojem statusu osim terminalnih (`removed`, `rejected`, `expired`). Dokumenti se mogu uploadovati pri kreiranju ili naknadno. ListingDocument je SSoT za sve dokumente vezane za listing — **Ch.04** (sekcija 4.7) je autoritativna referenca za ovaj entitet. Verifikacija vlasništva nije obavezna za objavu ali donosi prednosti (brža moderacija, badge). Detalji o verifikaciji → **Ch.04, sekcija 4.7**.

**Acceptance criteria:**

- [ ] Korisnik može uploadovati do 3 dokumenta po listingu
- [ ] Prihvaćeni formati: PDF, JPG, PNG
- [ ] Maksimalna veličina po dokumentu: 10 MB
- [ ] Korisnik bira `purpose` pri uploadu: `verification`, `clarification`, `other`
- [ ] Svaki dokument prolazi automatski virus scanning (async)
- [ ] `virusScanStatus` se inicijalno postavlja na `pending`, a zatim na `clean` ili `infected`
- [ ] Inficirani dokumenti postaju nedostupni i korisnik dobija obavještenje
- [ ] `documentStatus` se inicijalno postavlja na `pending` (čeka pregled moderatora)
- [ ] Korisnik može obrisati vlastiti dokument
- [ ] Korisnik može vidjeti listu svojih dokumenata sa statusima (pending/accepted/rejected)
- [ ] Dokumenti su privatni — vidljivi samo vlasniku i moderatorima

**Backend Scope:**

- `POST /listings/{id}/documents` — prima multipart file + purpose, vraća ListingDocument sa `virusScanStatus = pending`
- `GET /listings/{id}/documents` — vraća listu dokumenata (filtrirano po ownerId — korisnik vidi samo svoje)
- `GET /documents/{id}` — download/detalji dokumenta
- `DELETE /documents/{id}` — brisanje (samo vlasnik)
- Validacija: format, veličina, maksimalan broj (3), korisnik mora biti vlasnik listinga
- Side effects: triggeruje async virus scanning; pri `virusScanStatus = infected` — dokument nedostupan

**Frontend Scope:**

- UI: upload zona sa file picker-om, izbor purpose-a (dropdown/radio), lista uploadovanih dokumenata sa statusima
- Klijentska validacija: format, veličina
- UX: progress bar za upload; status indikatori (⏳ skeniranje, ✅ čist, ❌ inficiran, ⏳ čeka pregled, ✅ prihvaćen, ❌ odbijen); toast pri uspjehu/greški

**Tehničke napomene:**

- Virus scanning je async — ne blokira upload response
- Moderatorski pregled dokumenata (accepted/rejected) nije dio ove storije — to je [E07](../e07-moderacijski-workflow-i-ai-screening.md) (moderacija)
- `documentStatus` terminologija: `accepted`/`rejected`, ne `verified` — da se izbjegne zabuna sa `verificationStatus` na listingu (**Ch.04**, 4.7 napomena o terminologiji)

**Testovi (MVP):**

- [ ] Happy path: upload PDF dokumenta sa purpose `verification` → dokument kreiran, `virusScanStatus = pending`
- [ ] Upload 3 dokumenta → svi sačuvani
- [ ] Pokušaj uploada 4. dokumenta → greška "Maksimalan broj dokumenata"
- [ ] Upload fajla većeg od 10 MB → greška
- [ ] Upload nevalidnog formata (npr. .exe) → greška
- [ ] Brisanje dokumenta → dokument uklonjen iz liste
- [ ] Inficirani dokument → `virusScanStatus = infected`, korisnik obaviješten
- [ ] Korisnik ne može vidjeti dokumente tuđeg listinga

**Wireframe referenca:** —

**Implementacijske napomene:**

- Upload endpoint je generički `/listings/{id}/documents` i funkcioniše za oba tipa listinga
- Dokumenti se čuvaju na zaštićenom storage-u (ne javno dostupni URL-ovi)