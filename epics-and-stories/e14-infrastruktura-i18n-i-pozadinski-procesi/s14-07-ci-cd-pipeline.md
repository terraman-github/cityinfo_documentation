---
id: S14-07
confluence_page_id: "251166722"
parent_epic: E14
linear_id: "CIT2-89"
phase: MVP
journey_milestones: [J-08]
type: infra
---

# S14-07 — CI/CD pipeline

**Naslov:** CI/CD pipeline

**Excerpt:** Automatski build i test pipeline koji se pokreće na svaki push. Pipeline je prilagođen monorepo strukturi (backend + frontend u istom repu) i koristi path filtere da ne troši CI resurse na nepromjenjene dijelove. Nije strogi prioritet za Sprint 0, ali preporuka je uvući ga u Sprint 0 jer je investicija mala (pola dana) a koristi se pojavljuju odmah u Sprint 1.

**Phase:** MVP (preporuka: Sprint 0; fallback: kad tim procijeni da je potrebno)

**Journey milestones:** **J-08**

**User story:**
Kao developer,
želim imati CI/CD pipeline koji automatski bildi i testira kod na svaki push,
kako bih dobio brzi feedback o tome da li moje promjene rade ispravno — bez čekanja na nepromjenjene dijelove monorepoa.

**Kontekst:** Pipeline treba podržavati .NET 10 backend build + test i SvelteKit frontend build unutar monorepo strukture (`backend/`, `frontend/`, `db/seed/`). U monorepu CI bez path filtera nepotrebno vrti oba stacka na svaki PR (~5 min), što usporava dev loop. Cilj ove storije je pipeline koji vrti **samo ono što se tiče izmjene** (~2 min na single-stack PR, ~5 min na end-to-end PR). Ova storija je namjerno odvojena od repo setupa ([S14-01](s14-01-postavljanje-repozitorija-i-razvojnog-okruzenja.md)) jer CI/CD nije preduslov za početak razvoja, ali se preporučuje da uđe u Sprint 0 dok se postavlja ostatak infrastrukture.

**Acceptance criteria:**

- [ ] CI pipeline se automatski pokreće na svaki push i pull request
- [ ] Zasebni workflow fajlovi za backend i frontend, svaki sa vlastitim `paths:` filterom (`backend/**`, `frontend/**`)
- [ ] Backend pipeline uključuje: restore dependencies → build → run tests za .NET 10
- [ ] Frontend pipeline uključuje: `pnpm install` → `pnpm -r build` → (opciono) `pnpm -r test`
- [ ] Path filter preskače irelevantne jobove (npr. čista `docs/**` ili `**/*.md` izmjena ne pokreće build)
- [ ] "Umbrella" ci-gate job postoji kao required status check — prolazi uvijek i reprezentuje ukupni status primjenjivih jobova (rješava GitHub required-checks problem sa preskočenim jobovima)
- [ ] Neuspješan build ili test blokira merge u develop/main branch
- [ ] Single-stack PR (samo backend ili samo frontend) završava ispod 3 minute
- [ ] End-to-end PR (oba stacka) završava ispod 5 minuta

**Tehničke napomene:**

- Preporučeni alat: **GitHub Actions** sa `paths:` trigger filterima ili `dorny/paths-filter@v3` akcijom za granularniju kontrolu unutar jednog joba.
- Ako se koristi `dorny/paths-filter`, jedan job može unutar sebe uslovno pokrenuti backend i frontend korake — to olakšava "required check" konfiguraciju jer postoji tačno jedan job koji se uvijek pokreće.
- Alternativa je umbrella `ci-gate` job bez path filtera, koji kroz `needs:` čeka konkretne backend/frontend jobove i prolazi samo kad svi primjenjivi jobovi prođu.
- Required status checks u branch protection rule-u treba postaviti na umbrella job, **ne na konkretne backend/frontend jobove** — inače PR-ovi koji ne diraju određen stack se ne mogu mergeati.
- Monorepo struktura dozvoljava **nezavisan deploy** — CI artefakti (backend DLL, frontend build output) se mogu publishati i deployati odvojeno iako žive u istom repu.
- Početna lista workflow fajlova: `backend-ci.yml`, `frontend-ci.yml`, `ci-gate.yml`. Dodatni workflows (OpenAPI sync, DB migration validation, markdown lint) se dodaju inkrementalno.
- GitHub Actions free tier (2000 min/mjesec za privatne repozitorije) je dovoljan za tim od 2–3 programera ovog obima.

**Testovi (MVP):**

- [ ] Push na feature branch triggeruje samo relevantan pipeline (backend-only PR ne pokreće frontend build)
- [ ] PR koji dira samo `docs/**` ili `**/*.md` ne troši CI minute na build jobove
- [ ] Namjerno broken .NET build pada na pipeline-u sa jasnom error porukom
- [ ] Namjerno failed frontend test blokira pull request merge
- [ ] End-to-end PR (backend + frontend izmjene) pokreće oba pipeline-a i oba moraju proći prije merge-a
- [ ] Umbrella ci-gate job prolazi i na "samo docs" PR-u (inače se takvi PR-ovi ne mogu mergeati)

**Wireframe referenca:** —
