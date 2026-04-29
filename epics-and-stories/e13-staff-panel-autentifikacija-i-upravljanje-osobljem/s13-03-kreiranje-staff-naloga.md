---
id: S13-03
parent_epic: E13
linear_id: "CIT2-78"
phase: MVP
journey_milestones: [J-08]
type: fullstack
---

# S13-03 — Kreiranje Staff naloga

**Naslov:** Kreiranje Staff naloga

**Excerpt:** Staff nalozi se ne mogu samo-registrovati — kreira ih isključivo local\_admin za svoj tenant. Ova storija pokriva formu i endpoint za kreiranje novog Staff člana sa odabranom ulogom i inicijalnim postavkama.

**Phase:** MVP

**Journey milestones:** **J-08**

**User story:**  
Kao local\_admin,  
želim kreirati novi Staff nalog za moderatora ili operatora,  
kako bih mogao proširiti tim za upravljanje platformom u svom gradu.

**Kontekst:** Staff naloge kreira isključivo local\_admin — ne postoji self-registration. Pri kreiranju se bira uloga (moderator, operator) i dodjeljuje pristup jednom ili više tenanta. Novi Staff član dobija inicijalne kredencijale i mora postaviti 2FA pri prvom loginu. Matrica ovlasti po ulogama → **Ch.03, sekcija 3.5**. Local\_admin može kreirati samo naloge za tenante kojima sam ima pristup.

**Acceptance criteria:**

- [ ] Local\_admin može kreirati novi Staff nalog sa obaveznim poljima (email, fullName, phoneNumber, role)
- [ ] Dostupne uloge za kreiranje su: moderator i operator
- [ ] Local\_admin ne može kreirati drugi local\_admin nalog
- [ ] Email mora biti jedinstven unutar Staff sistema
- [ ] Novi nalog se kreira sa `isActive = true` i praznom `permissions` listom
- [ ] `tenantAccess` se inicijalno postavlja na tenant(e) local\_admin-a koji kreira nalog
- [ ] `createdBy` se automatski popunjava sa ID-em local\_admin-a koji kreira nalog
- [ ] `hiredAt` i `createdAt` se automatski postavljaju
- [ ] Novi Staff član dobija email sa inicijalnim kredencijalima i uputstvom za 2FA setup
- [ ] Kreiranje se loguje u audit log

**Backend Scope:**

- `POST /staff/manage/staff` — prima {email, fullName, phoneNumber, role, department?, tenantAccess?}, vraća {staffId, initialCredentials}
- Validacija: email unikatnost, role ∈ {moderator, operator}, tenant pristup kreatorovog naloga
- Side effects: šalje welcome email sa kredencijalima, loguje u audit, postavlja hiredAt/createdAt/createdBy

**Frontend Scope:**

- UI: forma za kreiranje Staff-a sa poljima za email, fullName, phoneNumber, role (dropdown), department (opciono)
- Klijentska validacija: obavezna polja, email format, telefon format
- UX: success modal sa potvrdom da je email poslan; inline greška za duplikat emaila; forma se resetuje nakon uspješnog kreiranja

**Tehničke napomene:**

- Local\_admin može kreirati naloge samo za tenante kojima ima pristup — ovo se provjerava server-side
- Inicijalni kredencijali se generišu server-side i šalju emailom — ne prikazuju se u UI
- Novi Staff mora obavezno postaviti 2FA pri prvom loginu — dok to ne uradi, ne može pristupiti panelu

**Testovi (MVP):**

- [ ] Local\_admin uspješno kreira moderatora sa svim obaveznim poljima
- [ ] Kreiranje odbijeno za duplikat emaila
- [ ] Local\_admin ne može kreirati local\_admin ulogu
- [ ] Novi Staff prima email sa inicijalnim kredencijalima
- [ ] CreatedBy se ispravno popunjava

**Wireframe referenca:** —