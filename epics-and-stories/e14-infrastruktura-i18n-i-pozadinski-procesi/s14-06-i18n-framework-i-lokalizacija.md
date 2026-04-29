---
id: S14-06
parent_epic: E14
linear_id: "CIT2-88"
phase: MVP
journey_milestones: [J-08]
type: infra
---

# S14-06 — i18n framework i lokalizacija

**Naslov:** i18n framework i lokalizacija

**Excerpt:** Sistem za upravljanje jezicima — da frontend zna prikazati UI na bosanskom ili engleskom, i da sadržaj sa `nameAlt`/`descriptionAlt` poljima ispravno fallback-uje na primarni jezik.

**Phase:** MVP

**Journey milestones:** **J-08**

**User story:**  
Kao developer,  
želim imati i18n framework za frontend i backend,  
kako bi sistem mogao prikazivati sadržaj i UI elemente na oba jezika tenanta.

**Kontekst:** CityInfo je od početka dvojezična platforma — svaki tenant podržava primarni i sekundarni jezik (**Ch.01, sekcija 1.1**). Dvojezičnost ima dvije dimenzije: (1) UI stringovi — labele, poruke, navigacija — koji se lokalizuju kroz i18n framework, i (2) korisnički sadržaj — `name`/`nameAlt`, `description`/`descriptionAlt` — koji koristi fallback logiku (ako alt ne postoji, prikaži primarni). Korisnik bira jezik sučelja — **Ch.02, sekcija 2.2**.

**Acceptance criteria:**

- [ ] Frontend i18n framework je konfigurisan sa dva lokala: `bs` (bosanski) i `en` (engleski)
- [ ] UI stringovi su eksternalizirani u resource fajlove (ne hardkodirani u komponentama)
- [ ] Korisnik može prebaciti jezik sučelja i promjena se odmah reflektuje
- [ ] Odabrani jezik se persistira (cookie ili localStorage) tako da se čuva između sesija
- [ ] Backend API podržava `Accept-Language` header za jezički kontekst
- [ ] Fallback logika za sadržaj: ako `nameAlt` ne postoji, prikaži `name` (isto za description, excerpt)
- [ ] API odgovor za listinge uključuje oba jezika (primarni i alt polja) — frontend odlučuje šta prikazati

**Tehničke napomene:**

- i18n framework na frontendu treba podržavati lazy loading translation fajlova (da ne učitava oba jezika odjednom).
- Backend ne prevodi sadržaj — samo vraća oba seta polja. Fallback logika je na frontendu.

**Testovi (MVP):**

- [ ] Stranica se renderuje na bosanskom kad je `locale=bs`
- [ ] Prebacivanje na engleski mijenja sve UI stringove
- [ ] Listing bez `nameAlt` prikazuje `name` na engleskom interfejsu (fallback)
- [ ] Listing sa `nameAlt` prikazuje `nameAlt` na engleskom interfejsu
- [ ] Odabrani jezik se čuva nakon refresha stranice

**Wireframe referenca:** —