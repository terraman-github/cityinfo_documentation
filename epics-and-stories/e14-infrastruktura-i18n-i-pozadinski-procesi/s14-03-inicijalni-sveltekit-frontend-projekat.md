---
id: S14-03
confluence_page_id: "250642457"
title: "S14-03 — Inicijalni SvelteKit frontend projekat"
parent_epic: E14
linear_id: "CIT2-85"
phase: MVP
journey_milestones: [J-08]
type: infra
---

**Naslov:** Inicijalni SvelteKit frontend projekat

**Excerpt:** Skeleton frontend aplikacije za korisnike ([cityinfo.ba](http://cityinfo.ba)). Osnova za sve UI komponente i stranice koje dolaze u narednim epicima.

**Phase:** MVP

**Journey milestones:** J-08

**User story:**

*Kao developer,*  
*želim imati funkcionalan SvelteKit frontend projekat sa TailwindCSS i Flowbite-om,*  
*kako bih mogao početi graditi korisničke stranice i komponente.*

**Kontekst:** Frontend koristi Svelte 5 + SvelteKit sa TailwindCSS i Flowbite design systemom — **Ch.08, sekcija 8.5**. U MVP-u se gradi User app ([cityinfo.ba](http://cityinfo.ba)) i Staff panel ([admin.cityinfo.ba](http://admin.cityinfo.ba)) kao zasebne SvelteKit aplikacije. Ova storija pokriva samo User app — Staff panel dolazi u [E13](../e13-staff-panel-autentifikacija-i-upravljanje-osobljem.md).

**Acceptance criteria:**

- [ ] SvelteKit projekat se bildi i pokreće lokalno
- [ ] TailwindCSS i Flowbite su konfigurisani i funkcionalni
- [ ] Bazična layout komponenta postoji (header, content area, footer)
- [ ] Routing je konfigurisan sa primjerom stranice
- [ ] Projekat se može buildati za produkciju (`npm run build`)
- [ ] Zajednička komponentna biblioteka je strukturirana tako da se može dijeliti sa Staff panelom

**Testovi (MVP):**

- [ ] `npm run dev` pokreće aplikaciju na localhost
- [ ] Primjer stranice renderuje Flowbite komponentu ispravno
- [ ] Produkcijski build završava bez errora

**Wireframe referenca:** —