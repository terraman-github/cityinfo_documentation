---
id: S03b-03
parent_epic: E03b
linear_id: "CIT2-25"
phase: MVP
journey_milestones: [J-08]
type: fullstack
---

# S03b-03 — Spajanje tagova

**Naslov:** Spajanje tagova

**Excerpt:** Kad se pojave tagovi sa istim ili sličnim značenjem (npr. "wifi" i "wi-fi"), moderator može spojiti source tag u target tag — svi pogođeni listinzi se automatski ažuriraju, source tag se trajno briše, a operacija se loguje za audit. Ovo je specijalizirana operacija odvojena od standardnog CRUD-a tagova.

**Phase:** MVP

**Journey milestones:** **J-08**

**User story:**  
Kao moderator sa `can_manage_tags` permisijom,  
želim spojiti dva taga u jedan,  
kako bih očistio duplikate i poboljšao konzistentnost kategorizacije bez ručnog ažuriranja svakog listinga.

**Kontekst:** Moderator je primijetio da postoje dva taga sa sličnim značenjem (npr. "besplatno" i "free-entry" ili "za-djecu" i "porodicno"). Želi zadržati jedan (target) i prebaciti sve listinge sa drugog (source) na target. Detaljni proces spajanja opisan u **Ch.04, sekcija 4.5** — uključuje zamjenu slug-ova na listinzima, čišćenje duplikata, i brisanje source taga.

**Acceptance criteria:**

- [ ] Moderator može odabrati source tag (koji će biti uklonjen) i target tag (koji ostaje)
- [ ] Source i target moraju biti iz iste tabele (oba EventTags ili oba PlaceTags)
- [ ] Sistem prikazuje preview: koliko listinga koristi source tag i koliko će biti pogođeno
- [ ] Nakon potvrde, svi listinzi koji koriste source tag dobijaju target tag na odgovarajućoj poziciji (primaryTagSlug ili secondaryTagSlug)
- [ ] Ako listing već koristi target tag na drugoj poziciji, source pozicija se čisti (NULL) — nema duplikata
- [ ] Source tag se trajno briše iz sistema
- [ ] Operacija se loguje za audit (source slug, target slug, broj pogođenih listinga, ko je pokrenuo, kada)
- [ ] Moderator dobija potvrdu sa brojem ažuriranih listinga

**Backend Scope:**

- `POST /event-tags/merge` — prima {sourceSlug, targetSlug}, vraća {mergedCount, deletedTag}
- `POST /place-tags/merge` — isto za place tagove
- Validacija: oba slug-a moraju postojati, ne smiju biti isti
- Side effects: ažuriranje `primaryTagSlug` i `secondaryTagSlug` na pogođenim listinzima, brisanje source taga, audit log zapis
- Cijela operacija je atomična (transakcija)

**Frontend Scope:**

- UI: Merge akcija dostupna iz liste tagova (npr. "Spoji sa..." akcija na tagu)
- UI: Modal/dijalog za odabir target taga (dropdown sa svim ostalim tagovima istog tipa)
- UI: Preview prikaz: "X listinga će biti ažurirano. Source tag 'Y' će biti obrisan."
- Klijentska validacija: source i target ne smiju biti isti
- UX: Confirmation korak prije izvršenja (operacija je nepovratna)
- UX: Success poruka sa brojem ažuriranih listinga

**Tehničke napomene:**

- Merge je atomična operacija — ili se sve ažurira ili ništa. Koristiti DB transakciju.
- Za MVP očekujemo mali broj pogođenih listinga pa je sinhrona operacija dovoljna.

**Testovi (MVP):**

- [ ] Spajanje dva taga gdje nijedan listing nema oba — svi source listinzi dobijaju target slug
- [ ] Spajanje dva taga gdje neki listing već ima target tag — source pozicija se čisti (NULL), nema duplikata
- [ ] Source tag ne postoji u sistemu nakon spajanja
- [ ] Audit log sadrži zapis o operaciji
- [ ] Pokušaj spajanja taga samog sa sobom — prikazuje grešku

**Wireframe referenca:** —