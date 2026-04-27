---
id: S03a-04
parent_epic: E03a
linear_id: ""
phase: MVP
journey_milestones: [J-02, J-04]
type: infra
---

# S03a-04 — Seed data — tagovi i aliasi

**Naslov:** Seed data — tagovi i aliasi

**Excerpt:** Popunjavanje baze inicijalnim tagovima za evente i mjesta, plus tabela aliasa za pretragu. Tagovi opisuju karakteristike (parking, wifi, besplatno), aliasi preusmjeravaju sinonime na prave kategorije (gym → Teretane).

**Phase:** MVP

**Journey milestones:** J-02, J-04

**User story:**  
Kao developer,  
želim imati inicijalne tagove i aliase u bazi,  
kako bi korisnici mogli označiti specifičnosti listinga, a pretraga razumjela lokalne sinonime.

**Kontekst:** Primjeri tagova su navedeni u Ch.04, sekcija 4.5 — EventTags (besplatno, za-djecu, online, radionica, festival, porodično) i PlaceTags (parking, wifi, pet-friendly, dostava, rezervacije, kartice). Aliasi su definisani u Ch.04, sekcija 4.4 — mapiranje alternativnih termina na kategorije (gym → Teretane i fitness, picerija → Restorani, itd.).

**Acceptance criteria:**

- [ ] EventTags seed: minimalno 6 tagova iz primjera u Ch.04 (besplatno, za-djecu, online, radionica, festival, porodično) sa ikonama i orderIndex-om
- [ ] PlaceTags seed: minimalno 6 tagova iz primjera u Ch.04 (parking, wifi, pet-friendly, dostava, rezervacije, kartice) sa ikonama i orderIndex-om
- [ ] `tagNameAlt` je popunjen engleskim prevodom gdje je očigledno
- [ ] Alias tabela postoji sa strukturom: aliasId, alias (tekst), categoryId (referenca na kategoriju)
- [ ] Inicijalni aliasi su popunjeni prema primjerima iz Ch.04, sekcija 4.4 (gym, picerija, diskoteka, birtija, shopping, doktor)
- [ ] Seed je idempotentna i odvojena od migracija
- [ ] Aliasi su konfigurabili po tenantu (struktura podržava tenant-specifične aliase)

**Testovi (MVP):**

- [ ] API vraća aktivne EventTags i PlaceTags sortirane po orderIndex
- [ ] Aliasi su u bazi i mogu se dohvatiti za lookup (gym → categoryId za "Teretane i fitness")
- [ ] Ponavljano pokretanje seed-a ne kreira duplikate

**Wireframe referenca:** —