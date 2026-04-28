---
id: S05-03
parent_epic: E05
linear_id: ""
phase: MVP
journey_milestones: [J-05]
type: fullstack
---

# S05-03 — Lajkovi za registrovane korisnike i visitore

**Naslov:** Lajkovi za registrovane korisnike i visitore

**Excerpt:** Registrovani korisnici lajkuju listing i mogu vidjeti historiju svojih lajkova. Visitors mogu lajkati ali bez historije — samo brojač raste. Zaštita od zloupotrebe koristi jednosmjerni hash za visitor detekciju. Ukupan broj lajkova (`totalAppreciations`) kombinuje obje grupe.

**Phase:** MVP

**Journey milestones:** **J-05**

**User story:**  
Kao posjetilac (registrovan ili visitor),  
želim lajkovati listing koji mi se sviđa,  
kako bih izrazio pozitivan stav i pomogao drugima da prepoznaju kvalitetan sadržaj.

**Kontekst:** Lajk je dostupan na kartici i na detaljnoj stranici. Registrovani korisnici imaju Appreciation entitet (**Ch.04**, 4.9) — lajk se trajno evidentira, korisnik može unlike-ovati. Visitors dobijaju samo inkrement brojača bez zapisa. Zaštita od visitor duplikata koristi jednosmjerni hash identifikacionih signala + listingId.

**Acceptance criteria:**

- [ ] Registrovan korisnik može lajkati listing klikom na lajk ikonu (srce ili slično)
- [ ] Registrovan korisnik može unlike-ovati — lajk se uklanja, `totalAppreciations` se dekrementira
- [ ] Lajk ikona vizuelno pokazuje stanje (lajkovan / nije lajkovan) za registrovane korisnike
- [ ] Registrovan korisnik može vidjeti historiju svojih lajkova na `/users/me/appreciations`
- [ ] Kombinacija userId + listingId je jedinstvena — duplikat lajk se ne kreira
- [ ] Visitor može lajkati listing — `totalAppreciations` se inkrementira
- [ ] Visitor lajk ne kreira Appreciation zapis — samo uvećava brojač
- [ ] Visitor ne može unlike-ovati — nema tog koncepta za visitore
- [ ] Zaštita od visitor duplikata: sistem prepoznaje ponovljeni lajk sa iste "lokacije" i ignorira ga
- [ ] `totalAppreciations` na kartici i detail stranici uvijek reflektuje ukupan broj (registrovani + visitor)
- [ ] Lajk je instant — ne čeka se server odgovor za vizuelni feedback (optimistic UI)

**Backend Scope:**

- `POST /listings/{id}/appreciate` — registrovan korisnik: kreira Appreciation zapis, inkrementira `totalAppreciations`; visitor: provjerava hash za duplikat, inkrementira `totalAppreciations` ako nije duplikat
- `DELETE /listings/{id}/appreciate` — registrovan korisnik: briše Appreciation, dekrementira counter
- `GET /users/me/appreciations` — lista lajkovanih listinga za registrovanog korisnika
- Visitor zaštita: jednosmjerni hash (identifikacioni signali + listingId) — ne čuvati sirove podatke

**Frontend Scope:**

- UI: Lajk dugme (srce ikona) na kartici i detail stranici
- UI: Broj lajkova pored ikone
- UI: Stranica "Moji lajkovi" u korisničkom profilu
- Klijentska validacija: visitor ne vidi unlike opciju
- UX: Optimistic UI — ikona se odmah mijenja, revert ako server vrati grešku
- UX: Animacija pri lajku (kratka pulse animacija na ikoni)

**Tehničke napomene:**

- Visitor identifikacioni signali za hash: kombinacija pasivno dostupnih meta-podataka (browser tip, jezik, itd.) + IP indikator — ne koristiti fingerprinting biblioteke.
- Jednosmjerni hash se čuva privremeno za provjeru duplikata — retention period je konfigurabilan parametar.
- Ne čuvati sirove visitor podatke — samo hash (GDPR compliance, **Ch.04**, 4.9).

**Testovi (MVP):**

- [ ] Registrovan korisnik lajkuje listing — `totalAppreciations` raste, Appreciation zapis postoji
- [ ] Registrovan korisnik unlike-uje — `totalAppreciations` pada, zapis obrisan
- [ ] Duplikat lajk od registrovanog korisnika — ne kreira novi zapis
- [ ] Visitor lajkuje — `totalAppreciations` raste, nema Appreciation zapisa
- [ ] Visitor lajkuje isti listing ponovo (isti browser) — ne mijenja se brojač
- [ ] "Moji lajkovi" stranica prikazuje listu lajkovanih listinga

**Wireframe referenca:** —