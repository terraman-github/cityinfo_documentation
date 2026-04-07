# CLAUDE.md — CityInfo: Optimizacija listingStatus 13 → 12

> **Zadatak:** Spajanje `rejected` statusa u `removed(rejected)` + prateće korekcije
> **Datum:** 3.4.2026

---

## ŠTA SE MIJENJA

Dokumentacija trenutno koristi jednostatus model sa **13 `listingStatus` vrijednosti**.
Optimiziramo na **12 vrijednosti** spajanjem `rejected` u `removed`.

### Promjena 1: `rejected` → `removed` sa `removedReason: rejected`

`rejected` prestaje biti zaseban `listingStatus`. Postaje vrijednost u `removedReason` enum-u.

**Prije (13 statusa):**
```
listingStatus: draft, in_review, changes_requested, published, 
  published_under_review, published_needs_changes, hidden_by_owner, 
  hidden_by_moderator, hidden_by_system, rejected, expired, canceled, removed
```

**Poslije (12 statusa):**
```
listingStatus: draft, in_review, changes_requested, published, 
  published_under_review, published_needs_changes, hidden_by_owner, 
  hidden_by_moderator, hidden_by_system, expired, canceled, removed
```

Gdje god dokumentacija kaže:
- "listingStatus = rejected" → zamijeni sa "listingStatus = removed sa removedReason = rejected"
- "prelazi u rejected" → zamijeni sa "prelazi u removed (removedReason: rejected)"
- "status rejected" → zamijeni sa "removed (rejected)"

### Promjena 2: `removedReason` enum — korekcija

**Prije:**
```
removedReason: spam, inappropriate, duplicate, user_delete, owner_blocked
```

**Poslije:**
```
removedReason: rejected, spam, inappropriate, duplicate, account_deleted
```

Promjene:
- **Dodano:** `rejected` (moderator odbio listing — prethodno bio zaseban status)
- **Preimenovano:** `user_delete` → `account_deleted` (jasnije — account vlasnika je obrisan, ne "user obrisao listing")
- **Uklonjeno:** `owner_blocked` (blokiranje korisnika koristi `hidden_by_system`, ne `removed`)

### Promjena 3: `hidden_by_moderator` semantika

Pojasniti: `hidden_by_moderator` je **bez zahtjeva prema vlasniku**. Moderator
istražuje sam i sam odlučuje. Za zahtjeve prema vlasniku postoje `changes_requested`
(nevidljiv) i `published_needs_changes` (vidljiv).

Iz `hidden_by_moderator`, moderator može:
- Vratiti u `published` (lažna uzbuna)
- Prebaciti u `changes_requested` ili `published_needs_changes` (utvrđen problem, traži popravku)
- Prebaciti u `removed` (spam, inappropriate, rejected, duplicate)

### Promjena 4: `canceled` pravila

Pojasniti/dodati ako još ne postoji:

**Vidljivost:**
- `isPublic = true` ali **isključen iz naslovne, feed-ova i promoted lista**
- Vidljiv u pretrazi (sa badge-om "Otkazano"), direktan link, favoriti, profil vlasnika

**Promocije:**
- Pauziraju se pri cancelovanju (timer stoji)
- Nastavljaju automatski pri reaktivaciji ako period nije istekao
- Ako period istekao tokom cancelovanja — ne obnavlja se

**Reaktivacija:**
- Reverzibilan samo ako `endDateTime > NOW()`
- Kad datum prođe → ostaje `canceled` (terminalni status), `isPublic` se gasi (nema tranzicije u `expired`)

### Promjena 5: Blokiranje korisnika

Pojasniti: blokiranje korisnika šalje listinge u `hidden_by_system` (reverzibilno),
**ne** u `removed` (terminalno). `owner_blocked` se NE koristi u `removedReason`.
Pri odblokiranju, listinzi se automatski vraćaju.

### Promjena 6: Ažuriranje broja statusa

Svugdje gdje piše "13 statusa/vrijednosti" → zamijeniti sa "12".
Svugdje gdje se nabraja lista svih statusa → ukloniti `rejected` iz liste.

---

## TABELA STATUSA (FINALNA — 12 VRIJEDNOSTI)

Za referencu pri obradi. Ovo je finalni model koji svi fajlovi trebaju reflektovati:

| Status | Opis | isPublic | Terminal? |
|--------|------|----------|-----------|
| `draft` | Korisnik priprema, nije submitovao | ❌ | Ne |
| `in_review` | Čeka moderatora (pre-mod ili resubmit) | ❌ | Ne |
| `changes_requested` | Moderator vratio, nevidljiv, čeka popravku | ❌ | Ne |
| `published` | Vidljiv, sve OK | ✅ | Ne |
| `published_under_review` | Vidljiv, čeka naknadni pregled (post-mod) | ✅ | Ne |
| `published_needs_changes` | Vidljiv, moderator traži blagu izmjenu | ✅ | Ne |
| `hidden_by_owner` | Vlasnik sakrio, može sam vratiti | ❌ | Ne |
| `hidden_by_moderator` | Moderator sakrio, istražuje/odlučuje | ❌ | Ne |
| `hidden_by_system` | AI blokada ili korisnik blokiran | ❌ | Ne |
| `expired` | Event prošao (vidljiv kao historija) | ✅ | ✅ |
| `canceled` | Vlasnik otkazao event (vidljiv sa badge-om dok `endDateTime > NOW()`) | ✅* | ✅** |
| `removed` | Trajno uklonjeno (razlog u removedReason) | ❌ | ✅ |

## `removedReason` ENUM (FINALNI — 5 VRIJEDNOSTI)

| Vrijednost | Značenje | Ko pokreće |
|---|---|---|
| `rejected` | Moderator odbio listing | Moderator |
| `spam` | Spam sadržaj | Moderator ili sistem |
| `inappropriate` | Neprimjeren sadržaj | Moderator |
| `duplicate` | Duplikat postojećeg listinga | Moderator |
| `account_deleted` | Account vlasnika je obrisan | Sistem |

## `isPublic` DERIVACIJA

```
isPublic = listingStatus IN ('published', 'published_under_review', 
                              'published_needs_changes', 'expired')
           OR (listingStatus = 'canceled' AND endDateTime > NOW())
```

---

## FAJLOVI ZA OBRADU

Obradi fajlove ovim redoslijedom. Prilagodi nazive ako se razlikuju od navedenih.

### 1. Specifikacija novog modela (SSoT)
**Fajl:** `novi-listing-statusni-model.md` (ili sličan naziv)
**Promjene:**
- Ukloni `rejected` iz tabele listingStatus vrijednosti
- Dodaj `rejected` u removedReason tabelu
- Zamijeni `user_delete` sa `account_deleted` u removedReason
- Ukloni `owner_blocked` iz removedReason
- Ažuriraj broj statusa: 13 → 12
- Ažuriraj tranzicije: svugdje gdje piše "→ rejected" zamijeni sa "→ removed (removedReason: rejected)"
- Ažuriraj Mermaid dijagram: ukloni `rejected` čvor, dodaj tranzicije prema `removed`
- Dodaj napomenu o `hidden_by_moderator` semantici (bez zahtjeva prema vlasniku)
- Dodaj/ažuriraj canceled pravila (vidljivost, promocije, reaktivacija)
- Dodaj napomenu o blokiranju (hidden_by_system, ne removed)

### 2. Ch.04 — Sadržaj
**Fajl:** `ch04-sadrzaj.md` (ili sličan naziv)
**Promjene:**
- **Tabela atributa (4.1):** Ažuriraj opis `listingStatus` (12 vrijednosti umjesto 13), ažuriraj `removedReason` opis
- **Brisanje događaja (4.2):** Ako referencira "rejected" kao status → "removed (rejected)"
- **Brisanje mjesta (4.3):** Isto
- **Lifecycle sekcija (4.8):** 
  - Tabela statusa: ukloni `rejected` red, ažuriraj opis `removed`
  - Tranzicije: "→ rejected" → "→ removed (removedReason: rejected)"
  - Dijagram: ukloni `rejected`, dodaj tranzicije prema `removed`
  - Narativni scenariji: zamijeni "rejected" sa "removed (rejected)"
  - removedReason tabela: dodaj `rejected`, zamijeni `user_delete` → `account_deleted`, ukloni `owner_blocked`
  - Dodaj `hidden_by_moderator` pojašnjenje ako nedostaje
  - Dodaj/ažuriraj canceled sekciju
  - Dodaj pojašnjenje o blokiranju → hidden_by_system
- **Changelog:** Dodaj unos

### 3. Ch.05 — Moderacija
**Fajl:** `ch05-moderacija.md` (ili sličan naziv)
**Promjene:**
- **Odluke moderatora (5.2.3):** "Reject → rejected" → "Reject → removed (removedReason: rejected)"
- **AI Screening (5.3):** Ako referencira "rejected" kao status
- **Moderatorske akcije (5.4):** Ažuriraj za hidden_by_moderator semantiku
- **Blokiranje (5.4.4):** Osiguraj da kaže `hidden_by_system`, ne `removed(owner_blocked)`
- **Poslovna pravila:** Ažuriraj BR-MOD-xx koji referenciraju `rejected` status
- **Changelog:** Dodaj unos

### 4. Ch.03 — Korisnici i pristup
**Fajl:** `ch03-korisnici-i-pristup.md` (ili sličan naziv)
**Promjene:**
- **Trust Tier (3.4):** Degradacija "→ rejected" → "→ removed (rejected)"
- **Blokiranje (3.7):** Osiguraj `hidden_by_system`, ne `removed(owner_blocked)`
- **Changelog:** Dodaj unos

### 5. Ch.06 — Monetizacija
**Fajl:** `ch06-monetizacija.md` (ili sličan naziv)
**Promjene:**
- Canceled pravila za promocije (pauziranje, nastavak pri reaktivaciji)
- Bilo koji "rejected" referenca → "removed (rejected)"
- **Changelog:** Dodaj unos

### 6. Ostali fajlovi (Ch.01, Ch.02, Ch.07, Ch.08, MVP SCOPE)
**Promjene:** Uglavnom search-and-replace:
- "rejected" kao status → "removed (rejected)" ili "removed (removedReason: rejected)"
- "13 statusa" → "12 statusa"
- "user_delete" → "account_deleted" (ako se pojavljuje)
- "owner_blocked" kao removedReason → ukloniti/zamijeniti sa "hidden_by_system"
- **Changelog:** Dodaj unos na svaki ažurirani fajl

### 7. Epici i storije (ako postoje kao .md fajlovi u repozitoriju)
Iste zamjene kao gore. Fokus na E02 (Lifecycle), E07 (Moderacija), E06 (Trust Tier).

---

## PRAVILA

1. **Ne mijenjaj strukturu dokumenata** — samo sadržaj koji je pogođen promjenama.
2. **Stari termini u changelog sekcijama su OK** — ne diraj historijske changelog unose.
3. **Kontekst je bitan** — ne radi slijepi replace. "Rejected" u prozi može značiti
   "moderator je odbio" (ok, ne treba mijenjati glagol) ili "status rejected" 
   (treba zamijeniti sa "removed (rejected)").
4. **Zadrži ton** — bosanski (ijekavica), opušteno-profesionalno.

## GREP PROVJERA NA KRAJU

```bash
# Traži preostale reference na stari model
grep -rn '"rejected"' docs/ --include="*.md" | grep -v "removedReason" | grep -v "Changelog" | grep -v "changelog"
grep -rn 'user_delete' docs/ --include="*.md" | grep -v "Changelog" | grep -v "changelog"
grep -rn 'owner_blocked' docs/ --include="*.md" | grep -v "Changelog" | grep -v "changelog"
grep -rn '13 statusa\|13 vrijednosti\|13 eksplicitnih' docs/ --include="*.md" | grep -v "Changelog" | grep -v "changelog"
```

Dozvoljeni rezultati: SAMO u changelog sekcijama. Sve ostalo mora biti ažurirano.

---

## KONTROLNA LISTA

Za svaki obrađeni fajl:
- [ ] `rejected` kao zaseban listingStatus → zamijenjeno sa `removed (removedReason: rejected)`
- [ ] `user_delete` u removedReason → zamijenjeno sa `account_deleted`
- [ ] `owner_blocked` u removedReason → uklonjeno (blokiranje koristi `hidden_by_system`)
- [ ] "13 statusa" → "12 statusa"
- [ ] `hidden_by_moderator` semantika pojašnjena (bez zahtjeva prema vlasniku)
- [ ] `canceled` pravila prisutna (vidljivost, promocije, reaktivacija)
- [ ] Blokiranje = `hidden_by_system` (ne `removed`)
- [ ] Changelog dodan
