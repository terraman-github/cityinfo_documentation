# S14-01 — Postavljanje repozitorija i razvojnog okruženja

**Naslov:** Postavljanje repozitorija i razvojnog okruženja

**Excerpt:** Bazični dev environment — repo struktura, branch strategija i upute za lokalno pokretanje. Bez ovoga niko ne može početi kodirati.

**Phase:** MVP

**Journey milestones:** J-08

**User story:**  
Kao developer,  
želim imati konfigurisan repozitorij sa jasnom strukturom i uputama za lokalno pokretanje,  
kako bih mogao klonirati projekat i početi raditi u roku od 30 minuta.

**Kontekst:** Ovo je prva storija na projektu — nema prethodnih koraka. Repo treba sadržavati .NET 10 backend i SvelteKit frontend u istom repozitoriju (monorepo) ili u jasno odvojenim repozitorijima — zavisi od odluke tima. Stack je definisan u Ch.08, sekcija 8.5.

**Acceptance criteria:**

- [ ] Git repozitorij je kreiran sa definisanom branch strategijom (main + develop + feature branches)
- [ ] Struktura foldera je jasna i dokumentovana (backend, frontend, shared)
- [ ] README sa uputama za lokalno pokretanje postoji u root-u projekta
- [ ] `.gitignore` je konfigurisan za .NET i Node.js projekte
- [ ] Novi developer može klonirati repo i pokrenuti projekat lokalno prateći README

**Testovi (MVP):**

- [ ] Novi developer može klonirati repo i pokrenuti backend + frontend lokalno prateći README
- [ ] `.gitignore` ispravno ignorira build artefakte, `node_modules`, `.env` fajlove

**Wireframe referenca:** —