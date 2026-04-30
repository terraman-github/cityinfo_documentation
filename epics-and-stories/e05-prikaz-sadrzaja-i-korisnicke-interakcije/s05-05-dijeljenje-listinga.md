---
id: S05-05
confluence_page_id: "252248065"
parent_epic: E05
linear_id: "CIT2-38"
phase: MVP
journey_milestones: [J-05]
type: fullstack
---

# S05-05 — Dijeljenje listinga

**Naslov:** Dijeljenje listinga

**Excerpt:** Korisnici i visitors mogu podijeliti listing putem linka. Na mobilnom se koristi native share API uređaja, a na desktopu copy-to-clipboard. Dijeljeni link vodi na javnu detail stranicu sa ispravnim Open Graph meta tagovima za preview na socijalnim mrežama.

**Phase:** MVP

**Journey milestones:** **J-05**

**User story:**  
Kao posjetilac (registrovan ili visitor),  
želim podijeliti zanimljiv listing sa prijateljima,  
kako bih im preporučio mjesto ili događaj bez potrebe da im objašnjavam detalje.

**Kontekst:** Dijeljenje ne zahtijeva autentifikaciju — dostupno je svima. Mehanizam koristi native share API preglednika gdje je dostupan (tipično mobilni), a copy-to-clipboard kao fallback (tipično desktop). Dijeljeni URL vodi na javnu detail stranicu. Open Graph meta tagovi su definirani u [S05-02](s05-02-detaljna-stranica-listinga.md). Detalji u **Ch.04, sekcija 4.9**.

**Acceptance criteria:**

- [ ] Share dugme je dostupno na kartici i detail stranici za sve korisnike (uključujući visitors)
- [ ] Na uređajima sa native share API-jem (mobilni): klik otvara sistemski share sheet (WhatsApp, Viber, SMS, email, itd.)
- [ ] Na uređajima bez native share API-ja (desktop): klik kopira URL u clipboard sa feedback porukom "Link kopiran!"
- [ ] Dijeljeni URL je direktan link na detail stranicu listinga
- [ ] URL uključuje meta tagove za social media preview: naslov (name), sliku (featuredImageUrl), kratki opis (excerpt)
- [ ] Dijeljeni link vodi na javnu stranicu koju može vidjeti bilo ko, uključujući visitors
- [ ] Ako listing više nije javan kad neko otvori dijeljeni link — prikazuje se poruka "Ovaj sadržaj više nije dostupan"

**Backend Scope:**

- `GET /listings/{id}/share` — vraća {url, title, description, imageUrl} za share mehanizam
- Open Graph meta tagovi se renderaju server-side na detail stranici (pokriveno u [S05-02](s05-02-detaljna-stranica-listinga.md))

**Frontend Scope:**

- UI: Share dugme (ikona) na kartici i detail stranici
- UX: Na mobilnom: `navigator.share()` sa fallback-om na clipboard
- UX: Na desktopu: `navigator.clipboard.writeText()` sa toast "Link kopiran!"
- UX: Share dugme nema disabled stanje — uvijek dostupno

**Testovi (MVP):**

- [ ] Na mobilnom: klik na share otvara sistemski share sheet
- [ ] Na desktopu: klik na share kopira URL u clipboard, prikazuje se "Link kopiran!"
- [ ] Dijeljeni link na WhatsApp/Viber prikazuje ispravan preview (naslov + slika)
- [ ] Otvaranje dijeljenog linka za aktivan listing — prikazuje detail stranicu
- [ ] Otvaranje dijeljenog linka za zatvoren listing — prikazuje "Ovaj sadržaj više nije dostupan"

**Wireframe referenca:** —