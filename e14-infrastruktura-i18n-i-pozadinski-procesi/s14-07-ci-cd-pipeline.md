# S14-07 — CI/CD pipeline

**Naslov:** CI/CD pipeline

**Excerpt:** Automatski build i test pipeline koji se pokreće na svaki push. Nije prioritet za Sprint 0, ali treba biti spreman kad tim počne raditi na feature branchevima.

**Phase:** MVP (nije Sprint 0 — ide kad tim procijeni da je potrebno)

**Journey milestones:** J-08

**User story:**  
Kao developer,  
želim imati CI/CD pipeline koji automatski bildi i testira kod na svaki push,  
kako bih dobio brzi feedback o tome da li moje promjene rade ispravno.

**Kontekst:** Pipeline treba podržavati .NET 10 backend build + test i SvelteKit frontend build. Ova storija je namjerno odvojena od repo setupa (S14-01) jer CI/CD nije preduslov za početak razvoja — mali tim može početi raditi i bez njega, a pipeline se postavlja kad se pojavi potreba.

**Acceptance criteria:**

- [ ] CI pipeline se automatski pokreće na svaki push i pull request
- [ ] Pipeline uključuje: restore dependencies → build → run tests za .NET backend
- [ ] Pipeline uključuje: install → build za SvelteKit frontend
- [ ] Neuspješan build ili test blokira merge u develop/main branch
- [ ] Pipeline završava u razumnom vremenu (ciljno ispod 5 minuta)

**Testovi (MVP):**

- [ ] Push na feature branch triggeruje pipeline i završava uspješno
- [ ] Namjerno broken build pada na pipeline-u sa jasnom error porukom
- [ ] Failed test blokira pull request merge

**Wireframe referenca:** —