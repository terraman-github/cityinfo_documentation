---
id: S14-02
confluence_page_id: "251232257"
parent_epic: E14
linear_id: "CIT2-84"
phase: MVP
journey_milestones: [J-08]
type: infra
---

# S14-02 — Inicijalni .NET 10 API projekat sa middleware-om

**Naslov:** Inicijalni .NET 10 API projekat sa middleware-om

**Excerpt:** Skeleton backend API koji može primiti HTTP request, rutirati ga i vratiti odgovor. Osnova na koju se nadograđuju svi endpoint-i.

**Phase:** MVP

**Journey milestones:** **J-08**

**User story:**  
Kao developer,  
želim imati funkcionalan .NET 10 API projekat sa bazičnim middleware-om,  
kako bih mogao početi graditi endpoint-e za korisničke i sadržajne funkcionalnosti.

**Kontekst:** Ovo se radi paralelno ili odmah nakon [S14-01](s14-01-postavljanje-repozitorija-i-razvojnog-okruzenja.md) (repo setup). API koristi RESTful stil sa JSON-om — **Ch.08, sekcija 8.5**. Projekat treba podržavati tri odvojena API sistema (User, Staff, GlobalAdmin) od starta, čak i ako se u MVP-u gradi samo User i Staff.

**Acceptance criteria:**

- [ ] .NET 10 Web API projekat se bilda i pokreće lokalno
- [ ] Health check endpoint (`/api/health`) vraća 200 OK
- [ ] Bazični middleware je konfigurisan: exception handling, request logging, CORS
- [ ] Projekat koristi konfiguraciju iz environment varijabli (ne hardkodirane vrijednosti)
- [ ] Swagger/OpenAPI dokumentacija se automatski generira za sve endpoint-e
- [ ] Struktura projekta podržava separaciju User/Staff/GlobalAdmin API-ja (namespace ili area)

**Tehničke napomene:**

- Tri korisnička sistema koriste odvojene API-je i auth mehanizme — **Ch.03, sekcija 3.1**. Strukturu projekta treba postaviti tako da ova separacija bude jasna od početka.

**Testovi (MVP):**

- [ ] `GET /api/health` vraća 200 sa statusom "healthy"
- [ ] Nepostojeći endpoint vraća standardiziran 404 JSON odgovor
- [ ] Unhandled exception vraća 500 sa generičkom porukom (bez stack trace-a u produkciji)