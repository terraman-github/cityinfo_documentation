# Novi listing statusni model — specifikacija

<a id="novi-listing-statusni-model-specifikacija"></a>

# Novi listing statusni model — specifikacija

> **Verzija:** 1.0  
> **Datum:** 1.4.2026  
> **Status:** Draft za review  
> **Kontekst:** Dio migracije sa dvostatus modela (lifecycleStatus + moderationStatus + closedReason) na jednostatus model.

* * *

<a id="1-uvod"></a>

## 1\. Uvod

CityInfo prelazi na **jednostatus model** koji opisuje kompletan životni ciklus listinga kroz jedan enum `listingStatus` sa 13 eksplicitnih vrijednosti. Novi model eliminiše nevalidne kombinacije starih statusa, pojednostavljuje `isPublic` derivaciju i omogućava čist state machine pattern.

Tri komplementarna polja dopunjuju `listingStatus`:

- `removedReason` — razlog trajnog uklanjanja (samo kad je status `removed`)
- `isPublic` — kalkulisano Boolean polje, derivira se iz statusa
- `wasEverActive` — Boolean koji kontrolira mogućnost brisanja

* * *

<a id="2-svi-statusi-detaljni-opisi"></a>

## 2\. Svi statusi — detaljni opisi

<a id="pregled"></a>

### Pregled

| Status | Opis | isPublic | Terminal? |
| --- | --- | --- | --- |
| `draft` | Korisnik priprema listing, nije ga submitovao | ❌   | Ne  |
| `in_review` | Čeka pregled moderatora (pre-mod ili resubmit) | ❌   | Ne  |
| `changes_requested` | Moderator vratio, nevidljiv, čeka popravku od korisnika | ❌   | Ne  |
| `published` | Vidljiv i aktivan, sve OK | ✅   | Ne  |
| `published_under_review` | Vidljiv, ali čeka naknadni pregled (post-mod tok) | ✅   | Ne  |
| `published_needs_changes` | Vidljiv, moderator traži blagu izmjenu | ✅   | Ne  |
| `hidden_by_owner` | Korisnik privremeno sakrio, može sam vratiti | ❌   | Ne  |
| `hidden_by_moderator` | Moderator sakrio, čeka popravku + pregled | ❌   | Ne  |
| `hidden_by_system` | AI blokada ili korisnik blokiran; zahtijeva moderatorski pregled | ❌   | Ne  |
| `rejected` | Finalno odbijeno — listing ne može biti objavljen | ❌   | ✅   |
| `expired` | Event je prošao; ostaje vidljiv kao historijski zapis | ✅   | ✅   |
| `canceled` | Vlasnik otkazao event; vidljiv sa ograničenjima (vidi ispod) | ✅\* | Ne\*\* |
| `removed` | Trajno uklonjeno; ne može se vratiti | ❌   | ✅   |

\* `canceled` je `isPublic = true` ali sa ograničenom vidljivošću.  
\*\* `canceled` je reverzibilan ako `endDateTime > NOW()`.

* * *

<a id="detaljni-opisi"></a>

### Detaljni opisi

<a id="draft"></a>

#### `draft`

Listing je u pripremi. Korisnik popunjava sadržaj, ali ga još nije submitovao na pregled. Listing nije vidljiv nikome osim vlasniku. Korisnik može slobodno uređivati, brisati ili submitovati. Nema vremenskog ograničenja u MVP-u (Phase 2: draft timeout na 30 dana).

<a id="in_review"></a>

#### `in_review`

Listing čeka moderatorski pregled. Do ovog statusa se dolazi na dva načina: (1) Korisnik sa Tier 0 ili Tier 1 submita novi listing ili izmjenu, ili (2) korisnik resubmituje listing koji je bio u `changes_requested` ili `hidden_by_moderator`. Listing nije vidljiv posjetiocima dok je u ovom stanju.

<a id="changes_requested"></a>

#### `changes_requested`

Moderator je pregledao listing i vratio ga korisniku na popravku. Listing je nevidljiv. Korisnik dobija notifikaciju sa moderatorskim komentarom, vrši izmjene i ponovo submita — čime listing prelazi u `in_review`.

<a id="published"></a>

#### `published`

Listing je aktivan i vidljiv svim posjetiocima. Prošao je kroz moderacijski proces ili je automatski objavljen kroz post-mod tok (Tier 2+) i moderator nije imao primjedbi. Ovo je "happy state" svakog listinga.

<a id="published_under_review"></a>

#### `published_under_review`

Listing je vidljiv posjetiocima, ali je istovremeno na moderatorskom pregledu. Do ovog statusa dolazi na dva načina: (1) Korisnik sa Tier 2+ Trust Tier-om submita novi listing koji odmah ide live uz naknadni pregled, ili (2) korisnik sa Tier 2+ uredi postojeći listing — izmjena je odmah vidljiva, ali čeka moderatorsku potvrdu.

<a id="published_needs_changes"></a>

#### `published_needs_changes`

Listing je vidljiv, ali moderator je identifikovao manju nekonzistentnost i traži blagorečenu izmjenu. Za razliku od `changes_requested` (gdje je listing skriven), ovdje listing ostaje dostupan posjetiocima dok korisnik priprema popravku. Korisnik dobija notifikaciju i može urediti listing, nakon čega prelazi u `published_under_review`.

<a id="hidden_by_owner"></a>

#### `hidden_by_owner`

Korisnik je privremeno sakrio listing. Razlozi mogu biti različiti: event je otkazan ali ne želi koristiti `canceled` status, listing je privremeno nedostupan, ili korisnik želi napraviti izmjene bez pritiska. Korisnik može sam vratiti listing u prethodni aktivni status (`published`) bez moderatorske intervencije.

<a id="hidden_by_moderator"></a>

#### `hidden_by_moderator`

Moderator je sakrio listing jer krši pravila ili sadržaj treba korekciju. Listing nije vidljiv posjetiocima. Korisnik dobija notifikaciju sa objašnjenjem. Nakon što korisnik izvrši tražene izmjene i resubmituje, listing prelazi u `in_review` za moderatorsku potvrdu.

<a id="hidden_by_system"></a>

#### `hidden_by_system`

Automatski sakrivanje — dešava se u dva scenarija: (1) AI screening je detektovao problematičan sadržaj i blokirao listing, ili (2) korisnik je blokiran i sav njegov sadržaj je automatski skriven. U oba slučaja, listing zahtijeva eksplicitnu moderatorsku akciju — ne može se automatski vratiti.

<a id="rejected"></a>

#### `rejected`

Moderator je finalno odbio listing. Ovo je terminalni status — listing ne može biti reaktiviran niti objavljen. Korisnik može kreirati novi listing, ali ovaj je zatvoren. Rejection je praćen moderatorskim komentarom koji korisnik dobija putem notifikacije.

<a id="expired"></a>

#### `expired`

Event je prošao — `endDateTime` je u prošlosti. Listing ostaje vidljiv kao historijski zapis sa oznakom "Završeno". Ovo je terminalni status za normalan slučaj: nema reaktivacije. Posjetioci koji su favorisali event ili imaju direktan link i dalje mogu pristupiti informacijama.

<a id="canceled"></a>

#### `canceled`

Vlasnik je otkazao event. Listing je vidljiv sa badge-om "Otkazano" i sljedećim pravilima:

**Vidljivost:**

- `isPublic = true` — dostupan putem direktnog linka, pretrage i favorita
- Prikazuje se sa badge-om "Otkazano"
- **Isključen iz:** naslovne stranice, feed-ova, promoted listi i "nadolazeći događaji" sekcija
- **Uključen u:** pretragu (sa badge-om), direktan link, korisnikov profil, favoriti

**Reverzibilnost:** Ako `endDateTime > NOW()`, vlasnik može reaktivirati event → `published`. Kad `endDateTime` prođe, automatska tranzicija u `expired`.

**Promocije:** Aktivne promocije se pauziraju pri prelasku u `canceled`. Promotivni timer se pauzira (ne troši se plaćeni period). Ako vlasnik reaktivira event i promotivni period nije istekao, promocija se automatski nastavlja.

**Napomena:** `canceled` važi samo za Event listing — Place ne može biti `canceled`.

<a id="removed"></a>

#### `removed`

Listing je trajno uklonjen. Nije vidljiv nikome, ne pojavljuje se u pretragama, direktan link vraća 404 ili "Listing nije dostupan". Ovo je terminalni status bez mogućnosti povratka. Razlog uklanjanja je pohranjen u `removedReason` polju.

* * *

<a id="3-dodatna-polja"></a>

## 3\. Dodatna polja

<a id="removedreason"></a>

### `removedReason`

Enum polje — postoji samo kad je `listingStatus = removed`. Opisuje razlog trajnog uklanjanja.

| Vrijednost | Opis | Inicijator |
| --- | --- | --- |
| `spam` | Sadržaj identifikovan kao spam | Moderator / AI |
| `inappropriate` | Krši pravila zajednice | Moderator |
| `duplicate` | Duplikat postojećeg listinga | Moderator |
| `user_delete` | Korisnik obrisao vlastiti listing (samo ako `wasEverActive = false`) | Korisnik |
| `owner_blocked` | Korisnik blokiran — sav sadržaj uklonjen | Sistem (automatski) |
| `abandoned` | *(Phase 2)* Draft bez izmjena 30+ dana | Sistem (automatski) |

<a id="ispublic"></a>

### `isPublic`

Boolean — **kalkulisano polje**, derivira se iz `listingStatus`. Nikad se ne upisuje direktno.

```
isPublic = listingStatus IN (
  'published',
  'published_under_review',
  'published_needs_changes',
  'expired',
  'canceled'
)
```

Svi ostali statusi rezultuju u `isPublic = false`.

<a id="waseveractive"></a>

### `wasEverActive`

Boolean — postaje `true` čim listing prvi put uđe u bilo koji `isPublic = true` status. Nikad se ne vraća na `false`.

**Uticaj na brisanje:**

- `wasEverActive = false` → korisnik može trajno obrisati listing (`removed` sa `user_delete`)
- `wasEverActive = true` → korisnik ne može "obrisati" listing u klasičnom smislu; može ga samo sakriti (`hidden_by_owner`) ili zatvoriti moderatorskim putem

Razlog: listinzi koji su bili vidljivi mogli su biti favorisani, komentirani ili dijeljeni — brisanje bi narušilo korisničko iskustvo osoba koje su interagovale sa listingom.

* * *

<a id="4-dozvoljene-tranzicije"></a>

## 4\. Dozvoljene tranzicije

<a id="kompletna-tabela-tranzicija"></a>

### Kompletna tabela tranzicija

| Od statusa | Okidač / Akcija | Do statusa | Ko inicira |
| --- | --- | --- | --- |
| `draft` | Korisnik submita (Tier 0–1) | `in_review` | Korisnik |
| `draft` | Korisnik submita (Tier 2+) | `published_under_review` | Korisnik |
| `draft` | Korisnik briše (`wasEverActive = false`) | `removed` (`user_delete`) | Korisnik |
| `in_review` | Moderator odobrava | `published` | Moderator |
| `in_review` | Moderator traži izmjene | `changes_requested` | Moderator |
| `in_review` | Moderator finalno odbija | `rejected` | Moderator |
| `in_review` | AI screening blokira | `hidden_by_system` | Sistem |
| `in_review` | Korisnik povlači submission | `draft` | Korisnik |
| `changes_requested` | Korisnik resubmituje | `in_review` | Korisnik |
| `changes_requested` | Korisnik briše (`wasEverActive = false`) | `removed` (`user_delete`) | Korisnik |
| `published` | Korisnik sakriva | `hidden_by_owner` | Korisnik |
| `published` | Korisnik uređuje (Tier 0–1) | `in_review` | Korisnik |
| `published` | Korisnik uređuje (Tier 2+) | `published_under_review` | Korisnik |
| `published` | Korisnik otkazuje event | `canceled` | Korisnik |
| `published` | `endDateTime` prošao | `expired` | Sistem |
| `published` | Moderator sakriva | `hidden_by_moderator` | Moderator |
| `published` | AI ili sistem blokira | `hidden_by_system` | Sistem |
| `published` | Moderator trajno uklanja | `removed` | Moderator |
| `published_under_review` | Moderator odobrava | `published` | Moderator |
| `published_under_review` | Moderator traži manje izmjene | `published_needs_changes` | Moderator |
| `published_under_review` | Moderator sakriva | `hidden_by_moderator` | Moderator |
| `published_under_review` | Moderator finalno odbija | `rejected` | Moderator |
| `published_under_review` | Korisnik sakriva | `hidden_by_owner` | Korisnik |
| `published_under_review` | Korisnik otkazuje event | `canceled` | Korisnik |
| `published_under_review` | `endDateTime` prošao | `expired` | Sistem |
| `published_needs_changes` | Korisnik submita popravku | `published_under_review` | Korisnik |
| `published_needs_changes` | Korisnik sakriva | `hidden_by_owner` | Korisnik |
| `published_needs_changes` | Moderator sakriva (eskalacija) | `hidden_by_moderator` | Moderator |
| `hidden_by_owner` | Korisnik prikazuje | `published` | Korisnik |
| `hidden_by_owner` | Moderator sakriva (eskalacija) | `hidden_by_moderator` | Moderator |
| `hidden_by_owner` | Moderator trajno uklanja | `removed` | Moderator |
| `hidden_by_moderator` | Korisnik resubmituje (nakon popravke) | `in_review` | Korisnik |
| `hidden_by_moderator` | Moderator vraća (bez zahtijeva za izmjenom) | `published` | Moderator |
| `hidden_by_moderator` | Moderator trajno uklanja | `removed` | Moderator |
| `hidden_by_system` | Moderator odobrava (lažni alarm) | `published` | Moderator |
| `hidden_by_system` | Moderator finalno odbija | `rejected` | Moderator |
| `hidden_by_system` | Moderator trajno uklanja | `removed` | Moderator |
| `canceled` | Korisnik reaktivira (`endDateTime > NOW()`) | `published` | Korisnik |
| `canceled` | `endDateTime` prošao | `expired` | Sistem |
| `canceled` | Moderator trajno uklanja | `removed` | Moderator |
| `rejected` | *(terminalni status)* | —   | —   |
| `expired` | *(terminalni status)* | —   | —   |
| `removed` | *(terminalni status)* | —   | —   |

<a id="zabrane-i-nevažeće-tranzicije"></a>

### Zabrane i nevažeće tranzicije

Sljedeće tranzicije su **eksplicitno zabranjene** — sistem ih ne smije dopustiti:

| Od → Do | Razlog zabrane |
| --- | --- |
| `rejected` → bilo koji status | Terminalni status; korisnik mora kreirati novi listing |
| `expired` → bilo koji status | Terminalni status za prošle evente |
| `removed` → bilo koji status | Terminalni status; nema povratka |
| Bilo koji → `expired` (manualnom akcijom) | Expired je isključivo automatska sistemska tranzicija |
| `hidden_by_system` → direktno korisniku | Korisnik ne može samovoljno izaći iz system block-a |
| `canceled` → `published` (kad `endDateTime < NOW()`) | Ne može reaktivirati event koji je prošao |
| Tranzicija na `canceled` za Place listing | `canceled` važi samo za Event |
| Direktan upis `isPublic` | `isPublic` je kalkulisano; direktan upis je zabranjen |

* * *

<a id="5-waseveractive-pravila-i-granični-slučajevi"></a>

## 5\. `wasEverActive` — pravila i granični slučajevi

<a id="definicija"></a>

### Definicija

`wasEverActive` postaje `true` pri prvoj tranziciji u **bilo koji** od sljedećih statusa:

- `published`
- `published_under_review`
- `published_needs_changes`
- `canceled`
- `expired`

Jednom kad postane `true`, **nikada se ne vraća na** `false` — čak ni ako listing naknadno pređe u `hidden` ili `removed` status.

<a id="praktične-implikacije"></a>

### Praktične implikacije

| `wasEverActive` | Korisnička akcija brisanja | Rezultat |
| --- | --- | --- |
| `false` | Korisnik klikne "Obriši" | `removed` sa `user_delete` — instant, bez potvrde moderatora |
| `true` | Korisnik klikne "Obriši" | Akcija nije dostupna — korisnik može samo sakriti ili zatvoriti listing |

Moderator uvijek može izvršiti `removed` akciju, bez obzira na `wasEverActive`.

* * *

<a id="6-removedreason-detaljna-pravila"></a>

## 6\. `removedReason` — detaljna pravila

`spam`

- Inicira: moderator (manualnom akcijom) ili sistem (automatski, Phase 2)
- Primjer: listing koji oglašava neovlaštene proizvode, ponavljajući spam unosi
- Korisnik prima notifikaciju sa generalnim objašnjenjem (ne detaljima o detekciji)

`inappropriate`

- Inicira: moderator
- Primjer: uvredljiv sadržaj, narušavanje privatnosti, dezinformacije
- Korisnik prima notifikaciju

`duplicate`

- Inicira: moderator
- Primjer: isti event prijavljen dva puta od strane istog ili različitih korisnika
- Moderator označava koji listing se briše, a koji ostaje

`user_delete`

- Inicira: korisnik
- Uslov: `wasEverActive = false` — listing nikad nije bio vidljiv javnosti
- Instant akcija — nije potrebno moderatorsko odobrenje
- Korisnik ne dobija notifikaciju (sam inicira)

`owner_blocked`

- Inicira: sistem automatski pri blokiranju korisnika
- Svi listinzi blokiranog korisnika dobijaju `removed` sa ovim razlogom
- Instant primjena; sadržaj se uklanja bez dodatne moderatorske akcije

`abandoned` *(Phase 2)*

- Inicira: sistem automatski
- Draft listing bez izmjena 30+ dana → `removed` sa `abandoned`
- 7 dana ranije šalje se reminder notifikacija korisniku

* * *

<a id="7-mermaid-state-dijagram"></a>

## 7\. Mermaid state dijagram

```
stateDiagram-v2
    [*] --> draft : Kreiranje listinga

    draft --> in_review : Submit (Tier 0-1)
    draft --> published_under_review : Submit (Tier 2+)
    draft --> removed : Brisanje (wasEverActive=false)

    in_review --> published : Moderator odobrava
    in_review --> changes_requested : Moderator traži izmjene
    in_review --> rejected : Moderator odbija
    in_review --> hidden_by_system : AI blokira
    in_review --> draft : Korisnik povlači

    changes_requested --> in_review : Resubmit
    changes_requested --> removed : Brisanje (wasEverActive=false)

    published --> hidden_by_owner : Korisnik sakriva
    published --> in_review : Izmjena (Tier 0-1)
    published --> published_under_review : Izmjena (Tier 2+)
    published --> canceled : Korisnik otkazuje event
    published --> expired : endDateTime prošao
    published --> hidden_by_moderator : Moderator sakriva
    published --> hidden_by_system : AI/sistem blokira
    published --> removed : Moderator uklanja

    published_under_review --> published : Moderator odobrava
    published_under_review --> published_needs_changes : Moderator traži izmjenu
    published_under_review --> hidden_by_moderator : Moderator sakriva
    published_under_review --> rejected : Moderator odbija
    published_under_review --> hidden_by_owner : Korisnik sakriva
    published_under_review --> canceled : Korisnik otkazuje
    published_under_review --> expired : endDateTime prošao

    published_needs_changes --> published_under_review : Korisnik submita popravku
    published_needs_changes --> hidden_by_owner : Korisnik sakriva
    published_needs_changes --> hidden_by_moderator : Moderator eskalira

    hidden_by_owner --> published : Korisnik prikazuje
    hidden_by_owner --> hidden_by_moderator : Moderator eskalira
    hidden_by_owner --> removed : Moderator uklanja

    hidden_by_moderator --> in_review : Korisnik resubmituje
    hidden_by_moderator --> published : Moderator vraća
    hidden_by_moderator --> removed : Moderator uklanja

    hidden_by_system --> published : Moderator odobrava
    hidden_by_system --> rejected : Moderator odbija
    hidden_by_system --> removed : Moderator uklanja

    canceled --> published : Reaktivacija (endDateTime > NOW)
    canceled --> expired : endDateTime prošao
    canceled --> removed : Moderator uklanja

    rejected --> [*]
    expired --> [*]
    removed --> [*]
```

* * *

<a id="8-narativni-scenariji"></a>

## 8\. Narativni scenariji

<a id="scenarij-1-tier-1-kreiranje-i-odobravanje"></a>

### Scenarij 1: Tier 1 — kreiranje i odobravanje

Marko (Trust Tier 1) kreira event "Jazz večer u Pivnici". Popunjava sve obavezne podatke i klikne "Pošalji na pregled". Listing prelazi iz `draft` → `in_review`. Moderator Lejla pregleda listing, sve je u redu, i odobrava ga. Listing prelazi u `published` i postaje vidljiv svim posjetiocima. Marko dobija notifikaciju "Tvoj listing je objavljen".

<a id="scenarij-2-tier-2-post-mod-tok"></a>

### Scenarij 2: Tier 2 — post-mod tok

Ana (Trust Tier 2) kreira novu kafeteriju "Balkan Brew". Popunjava podatke i submita. Listing odmah prelazi u `published_under_review` — vidljiv posjetiocima, ali u moderatorskom redu. Lejla pregleda listing narednih sat vremena, sve je ispravno, klikne "Odobri". Listing prelazi u `published`. Posjetioci koji su u međuvremenu naišli na listing vidjeli su ga i nisu primijetili razliku.

<a id="scenarij-3-tier-1-izmjena-objavljenog-listinga"></a>

### Scenarij 3: Tier 1 — izmjena objavljenog listinga

Marko želi promijeniti opis svog jazz eventa. Klikne "Uredi" na objavljenom listingu. Sistem detektuje da je Marko Tier 1 i listing šalje na ponovni pregled — prelazi iz `published` → `in_review` i postaje nevidljiv posjetiocima. Lejla pregleda izmjenu i odobrava. Listing se vraća u `published`.

<a id="scenarij-4-tier-2-izmjena-bez-prekida-vidljivosti"></a>

### Scenarij 4: Tier 2 — izmjena bez prekida vidljivosti

Ana želi ažurirati radno vrijeme za "Balkan Brew". Klikne "Uredi" i sačuva izmjenu. Kao Tier 2 korisnik, listing ostaje vidljiv ali prelazi u `published_under_review`. Lejla pregleda izmjenu, potvrdi da je OK, odobrava. Listing prelazi u `published`. Posjetioci nisu primijetili prekid.

<a id="scenarij-5-zahtjev-za-izmjenom-i-resubmit"></a>

### Scenarij 5: Zahtjev za izmjenom i resubmit

Marko submita listing za festival, ali moderator Lejla primijeti da nedostaje adresa. Šalje ga nazad sa komentarom "Molimo dodajte tačnu adresu." Listing prelazi u `changes_requested`, Marko dobija notifikaciju. Dopunjava podatke i ponovo submita → `in_review`. Lejla odobrava → `published`.

<a id="scenarij-6-odbijanje"></a>

### Scenarij 6: Odbijanje

Korisnik submita listing koji je potpuni spam — ponavljajuća reklama bez relevantnog sadržaja. Moderator pregleda i finalno odbija: `rejected`. Korisnik prima notifikaciju s objašnjenjem. Listing ostaje trajno odbijen; korisnik može kreirati novi, ispravan listing.

<a id="scenarij-7-moderator-sakriva-vidljivi-listing"></a>

### Scenarij 7: Moderator sakriva vidljivi listing

Anonimna prijava upućuje na problem sa objavljenim listingom. Moderator Lejla pregleda i zaključuje da je sadržaj nepotpun i potencijalno obmanjujuć. Klikne "Sakrij" → listing prelazi iz `published` → `hidden_by_moderator`. Korisnik dobija notifikaciju s traženim izmjenama. Korisnik popravlja sadržaj i resubmituje → `in_review`. Lejla pregleda, odobrava → `published`.

<a id="scenarij-8-ai-blokada-i-moderatorski-pregled"></a>

### Scenarij 8: AI blokada i moderatorski pregled

AI screening skenira novi listing i detektuje potencijalni spam pattern. Listing automatski prelazi u `hidden_by_system` bez obzira na Tier korisnika. Listing se pojavljuje u moderatorskom redu sa oznakom "AI blokada". Lejla pregleda, zaključuje da je lažni alarm, klikne "Odobri" → `published`. Ako bi zaključila da je spam opravdan → `rejected` ili `removed`.

<a id="scenarij-9-korisnik-blokiran-instant-uklanjanje-sadržaja"></a>

### Scenarij 9: Korisnik blokiran — instant uklanjanje sadržaja

Damir (ops manager) prima prijavu o zloupotrebi. Blokira korisnika na admin panelu. Sistem automatski prolazi kroz sve listinze blokiranog korisnika i svakog prebacuje u `removed` sa `removedReason = owner_blocked`. Ako su listinzi bili vidljivi, odmah nestaju sa platforme.

<a id="scenarij-10-event-otkazan-i-reaktiviran"></a>

### Scenarij 10: Event otkazan i reaktiviran

Marko planira jazz concert ali mora ga otkazati zbog bolesti svirača. Klikne "Otkaži event". Listing prelazi u `canceled` — ostaje vidljiv sa badge-om "Otkazano", ali nestaje s naslovnice i feed-ova. Aktivna promocija se pauzira. Tjedan dana prije termina, svirač se oporavi. Marko reaktivira event — listing prelazi u `published`, promocija se automatski nastavlja. Posjetioci koji su favorisali event primaju notifikaciju "Event reaktiviran".

<a id="scenarij-11-event-istekao"></a>

### Scenarij 11: Event istekao

Jazz večer je uspješno održan. Dan nakon `endDateTime`, sistem automatski prebacuje listing iz `published` → `expired`. Listing ostaje vidljiv sa oznakom "Završeno". Posjetioci koji traže "jazz Sarajevo" i dalje mogu pronaći historijski zapis. Vlasnik ne dobija notifikaciju — normalan, očekivan tok.

<a id="scenarij-12-korisnik-briše-draft-koji-nikad-nije-bio-živ"></a>

### Scenarij 12: Korisnik briše draft (koji nikad nije bio živ)

Marko je počeo kreirati listing ali se predomislio. Listing je u statusu `draft`, `wasEverActive = false`. Klikne "Obriši" — sistem trenutno prebacuje listing u `removed` sa `user_delete`. Listing nestaje iz Markovog profila. Nema potrebe za moderatorskim odobrenjem jer listing nikad nije bio javno vidljiv.

* * *

<a id="9-c-enum-mapping"></a>

## 9\. C# enum mapping

U backend implementaciji, `listingStatus` se mapira na PascalCase C# enum:

```
draft                   → Draft
in_review               → InReview
changes_requested       → ChangesRequested
published               → Published
published_under_review  → PublishedUnderReview
published_needs_changes → PublishedNeedsChanges
hidden_by_owner         → HiddenByOwner
hidden_by_moderator     → HiddenByModerator
hidden_by_system        → HiddenBySystem
rejected                → Rejected
expired                 → Expired
canceled                → Canceled
removed                 → Removed
```

API i DB serializacija koriste snake\_case. Naming konvencija definisana u migracijskom planu (odluka 6).

* * *

<a id="10-zamjenjena-polja"></a>

## 10\. Zamjenjena polja

Novi model u potpunosti zamjenjuje sljedeće:

| Staro polje | Zamjena |
| --- | --- |
| `lifecycleStatus` | `listingStatus` (integrisano) |
| `moderationStatus` | `listingStatus` (integrisano) |
| `closedReason` | `listingStatus` (semantika stanja) + `removedReason` (razlog uklanjanja) |

Stara polja se ne smiju koristiti ni u jednom dijelu sistema nakon migracije.