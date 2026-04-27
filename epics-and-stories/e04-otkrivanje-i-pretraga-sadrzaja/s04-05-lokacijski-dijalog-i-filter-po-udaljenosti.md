---
id: S04-05
parent_epic: E04
linear_id: ""
phase: MVP
journey_milestones: [J-04]
type: fullstack
---

# S04-05 — Lokacijski dijalog i filter po udaljenosti

**Naslov:** Lokacijski dijalog i filter po udaljenosti

**Excerpt:** Korisnik postavlja svoju lokaciju putem GPS-a ili ručnog unosa — sistem provjerava da li je unutar zone pokrivenosti tenanta i omogućava filter po udaljenosti. Lokacijski indikator u headeru uvijek pokazuje trenutno stanje, a klik otvara dijalog za promjenu.

**Phase:** MVP

**Journey milestones:** J-04

**User story:**  
Kao posjetilac,  
želim postaviti svoju lokaciju i filtrirati sadržaj po udaljenosti,  
kako bih pronašao mjesta i događaje koji su mi blizu.

**Kontekst:** Lokacija nije obavezna za korištenje platforme, ali bez nje korisnik gubi filter po udaljenosti i prikaz distance na karticama. Sistem podržava GPS (browser geolokacija) i ručni unos (pretraga adrese/grada). Zona pokrivenosti tenanta je definisana kao centar + radijus. Detalji u Ch.02, sekcija 2.2 (lokacijski dijalog).

**Acceptance criteria:**

- [ ] Lokacijski indikator je uvijek vidljiv u headeru blizu search bara
- [ ] Indikator prikazuje stanje prema tabeli iz Ch.02, sekcija 2.2: naziv lokacije + status (unutar zone, van područja, nepoznata)
- [ ] Klik na indikator otvara lokacijski dijalog
- [ ] Dijalog sadrži: "Koristi moju lokaciju" (GPS), polje za pretragu (autocomplete), interaktivnu mapu sa zonom pokrivenosti, "Ukloni lokaciju", "Primijeni"
- [ ] "Koristi moju lokaciju" triggeruje browser geolocation API
- [ ] Ako korisnik odobri GPS i lokacija je unutar zone tenanta — lokacijske funkcije dostupne
- [ ] Ako korisnik odobri GPS ali lokacija je van zone — indikator prikazuje "(van područja)", lokacijske funkcije nedostupne
- [ ] Ako korisnik blokira GPS — prikazuje se vizualno uputstvo za deblokiranje, ostaje opcija ručnog unosa
- [ ] Ručni unos koristi autocomplete (Google Places) za pretragu grada ili adrese
- [ ] Interaktivna mapa prikazuje vizuelno označenu zonu pokrivenosti tenanta i pin koji korisnik može pomjerati
- [ ] "Ukloni lokaciju" vraća korisnika u stanje "lokacija nepoznata"
- [ ] Kad je lokacija postavljena i unutar zone, korisnik može filtrirati po udaljenosti
- [ ] Filter po udaljenosti prikazuje samo listinge unutar odabranog radijusa od korisnikove pozicije
- [ ] Na karticama listinga prikazuje se udaljenost od korisnikove lokacije (samo kad je lokacija unutar zone)

**Backend Scope:**

- `GET /events?lat={lat}&lng={lng}&radius={km}` — filtriranje po udaljenosti
- `GET /places?lat={lat}&lng={lng}&radius={km}` — isto za mjesta
- Backend računa udaljenost između korisnikove pozicije i lokacije listinga
- Provjera zone pokrivenosti: API prima koordinate i vraća {inZone: boolean, zoneName: string}

**Frontend Scope:**

- UI: Lokacijski indikator u headeru sa dinamičnim tekstom
- UI: Lokacijski dijalog (modal) sa svim elementima prema Ch.02
- UI: Google Maps komponenta sa označenom zonom pokrivenosti
- UI: Udaljenost na karticama listinga (npr. "1.2 km")
- UI: Filter po udaljenosti (slider ili predefinisani radijusi: 1km, 5km, 10km, 25km)
- Klijentska validacija: koordinate moraju biti validne
- UX: Lokacija se persiste u sesiji — ostaje dok korisnik ne ukloni ili promijeni
- UX: Promjena lokacije odmah osvježava udaljenosti na karticama

**Tehničke napomene:**

- Google Maps API i Places API zahtijevaju API ključ — konfigurisan kao tenant parametar.
- Zona pokrivenosti tenanta (centar + radijus) je konfigurabilan parametar.
- Filter po udaljenosti se može implementirati sa jednostavnom Haversine formulom na backend-u.

**Testovi (MVP):**

- [ ] GPS odobren, lokacija unutar zone — indikator prikazuje naziv, udaljenosti vidljive na karticama
- [ ] GPS odobren, lokacija van zone — indikator prikazuje "(van područja)", filter po udaljenosti nedostupan
- [ ] Ručni unos "Baščaršija" — lokacija se postavlja, udaljenosti se prikazuju
- [ ] "Ukloni lokaciju" — indikator se vraća na "Postavi lokaciju", udaljenosti nestaju
- [ ] Filter po udaljenosti 5km — prikazuju se samo listinzi unutar 5km

**Wireframe referenca:** —

**Implementacijske napomene:** Za MVP, predefinisani radijusi (1/5/10/25 km) su dovoljni umjesto slobodnog slider-a. Google Maps se učitava lazy — ne blokira učitavanje stranice.