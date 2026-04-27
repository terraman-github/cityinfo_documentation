---
id: S03a-02
parent_epic: E03a
linear_id: ""
phase: MVP
journey_milestones: [J-02]
type: backend-only
---

# S03a-02 — Tag entiteti

**Naslov:** Tag entiteti

**Excerpt:** Kreiranje EventTags i PlaceTags tabela. Tagovi su lakši entiteti od kategorija — slug kao PK, naziv, ikona i redoslijed.

**Phase:** MVP

**Journey milestones:** J-02

**User story:**  
Kao developer,  
želim imati Tag entitete za evente i mjesta,  
kako bih mogao omogućiti korisnicima da označe specifičnosti svojih listinga.

**Kontekst:** Tagovi opisuju karakteristike listinga (parking, wifi, besplatno, za-djecu). Odvojeni su za evente i mjesta jer su semantički različiti — Ch.04, sekcija 4.5. Slugovi tagova se čuvaju denormalizovano u Listing entitetu (`primaryTagSlug`, `secondaryTagSlug`).

**Acceptance criteria:**

- [ ] EventTags tabela postoji sa atributima: tagSlug (PK), tagName, tagNameAlt, tagIcon, orderIndex, isActive
- [ ] PlaceTags tabela postoji sa identičnom strukturom
- [ ] Listing entitet ima polja `primaryTagSlug` i `secondaryTagSlug` (nullable stringovi)
- [ ] tagSlug je jedinstven unutar tabele

**Testovi (MVP):**

- [ ] Migracija prolazi uspješno
- [ ] Tag se može kreirati sa svim atributima
- [ ] Listing može referencirati tag slug-ove koji postoje u odgovarajućoj tabeli

**Wireframe referenca:** —