# S02-05 — Upload i upravljanje slikama listinga

<a id="s02-05-upload-i-upravljanje-slikama-listinga"></a>

# S02-05 — Upload i upravljanje slikama listinga

**Naslov:** Upload i upravljanje slikama listinga

**Excerpt:** Korisnik može uploadovati do 5 slika za svoj listing — jednu kao glavnu (featured) i ostale za galeriju. Svaka slika prolazi validaciju formata i veličine, automatsku optimizaciju u više verzija, i AI screening za neprimjeren sadržaj.

**Phase:** MVP

**Journey milestones:** J-02

**User story:**  
Kao vlasnik listinga,  
želim dodati slike svom listingu — glavnu sliku i galeriju,  
kako bi listing bio vizuelno atraktivniji i privlačio više posjetilaca.

**Kontekst:** Korisnik ima kreiran listing (Event ili Place) u bilo kojem statusu osim terminalnih (`removed`, `rejected`, `expired`). Slike se uploaduju na stranicu drafta ili na edit stranici objavljenog listinga. Sistem automatski generiše optimizirane verzije (thumbnail, medium, original, WebP). Detalji o Image entitetu → Ch.04, sekcija 4.6. Default slika kategorije služi kao fallback ako listing nema vlastitu sliku (hijerarhija slika → Ch.04, 4.6).

**Acceptance criteria:**

- [ ] Korisnik može uploadovati do 5 slika po listingu
- [ ] Prihvaćeni formati: JPG, PNG, WebP
- [ ] Maksimalna veličina po slici: 5 MB
- [ ] Minimalna rezolucija: 800×600 piksela
- [ ] Maksimalna rezolucija: 4000×4000 piksela
- [ ] Prva uploadovana slika se automatski označava kao featured (`isFeatured = true`)
- [ ] Korisnik može promijeniti koja slika je featured
- [ ] Korisnik može promijeniti redoslijed slika u galeriji (drag & drop ili slično)
- [ ] Korisnik može obrisati bilo koju sliku
- [ ] Sistem automatski generiše thumbnail (300×200), medium (800×600) i WebP verzije
- [ ] Svaka slika prolazi AI screening za neprimjeren sadržaj (async)
- [ ] Slike koje ne prođu AI screening se automatski odbiju ili označe za review
- [ ] `featuredImageUrl` na Listing entitetu se sinhronizuje sa featured Image entitetom
- [ ] Ako listing nema sliku, koristi se `defaultImageUrl` iz primarne kategorije kao fallback
- [ ] Validacijske greške (format, veličina, rezolucija) se prikazuju odmah

**Backend Scope:**

- `POST /listings/{id}/images` — prima multipart file upload, vraća Image entitet sa generisanim URL-ovima
- `DELETE /images/{id}` — briše sliku i ažurira redoslijed
- `POST /images/{id}/set-featured` — postavlja sliku kao featured
- `PUT /listings/{id}/images/reorder` — prima novi redoslijed (lista ID-ova)
- `GET /listings/{id}/images` — vraća listu slika za listing
- Validacija: format, veličina, rezolucija, maksimalan broj (5), korisnik mora biti vlasnik listinga
- Side effects: generisanje thumbnail/medium/WebP verzija (async), AI screening (async), sinhronizacija `featuredImageUrl` na Listing-u

**Frontend Scope:**

- UI: zona za upload (drag & drop ili file picker), galerija pregled sa thumbnail-ovima, star/featured oznaka, dugmad za brisanje i reorder
- Klijentska validacija: format, veličina, rezolucija — provjera prije slanja na server
- UX: progress bar za upload; toast pri uspjehu/greški; ako AI screening odbije sliku — poruka korisniku sa objašnjenjem; drag & drop za promjenu redoslijeda

**Tehničke napomene:**

- Generisanje verzija slika i AI screening su asinhroni — slika se uploaduje odmah, ali verzije i screening se procesiraju u pozadini
- CDN integracija za serviranje slika — zavisnost na E14 (infrastruktura)

**Testovi (MVP):**

- [ ] Happy path: upload jedne JPG slike → automatski featured, thumbnail/medium generisani
- [ ] Upload 5 slika → sve sačuvane sa ispravnim redoslijedom
- [ ] Pokušaj uploada 6. slike → greška "Maksimalan broj slika dostignut"
- [ ] Upload slike veće od 5 MB → validacijska greška
- [ ] Upload slike manje od 800×600 → validacijska greška
- [ ] Upload nevalidnog formata (npr. GIF) → validacijska greška
- [ ] Promjena featured slike → stara izgubi oznaku, nova dobije
- [ ] Brisanje featured slike → sljedeća po redu postaje featured (ili nema featured)
- [ ] Reorder slika → `orderIndex` ažuriran

**Wireframe referenca:** —

**Implementacijske napomene:**

- Razmotriti chunked upload za veće fajlove radi bolje UX-a na sporijim konekcijama
- WebP konverzija može koristiti server-side processing (Sharp, ImageMagick, ili cloud servis)
- `altText` i `altTextAlt` polja mogu se dodati naknadno u edit modu — ne moraju biti dio inicijalnog uploada