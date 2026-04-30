---
id: E13
confluence_page_id: "250970205"
title: "E13 — Staff panel, autentifikacija i upravljanje osobljem"
linear_id: ""
phase: MVP
journey_milestones: [J-08]
personas: [Amra, Dino, lokalni admin]
story_count: 7
---

**Naslov:** Staff panel, autentifikacija i upravljanje osobljem

**Excerpt:** Bez admin panela nema moderacije, bez moderacije nema kvalitetnog sadržaja. Ovaj epic pokriva kompletnu infrastrukturu za Staff sistem — od autentifikacije sa obaveznom 2FA, preko kreiranja i upravljanja Staff nalozima, do shell-a admin panela kroz koji moderatori, operatori i lokalni admini svakodnevno rade. Cilj je da Staff tim ima siguran, funkcionalan radni prostor prije nego što moderacijski workflow ([E07](e07-moderacijski-workflow-i-ai-screening.md)) bude pušten u produkciju.

**Scope — šta ulazi:**

- Staff autentifikacija (login sa obaveznom 2FA, session management, lockout)
- Promjena lozinke i politika rotacije
- Kreiranje Staff naloga (local\_admin kreira moderatore)
- Pregled, editovanje i deaktivacija Staff naloga
- Dodjela i oduzimanje granularnih moderatorskih permisija (`can_manage_trust_tier`, `can_manage_tags`)
- Upravljanje tenant pristupom (`tenantAccess` lista)
- Admin panel shell — layout, navigacija, tenant switcher

**Scope — šta NE ulazi:**

- Moderacijski workflow (queue, odluke, AI screening) — pokriveno u [E07](e07-moderacijski-workflow-i-ai-screening.md)
- Trust Tier logika i evaluacija — pokriveno u [E06](e06-trust-tier-sistem.md)
- Upravljanje korisnicima (User entitet) iz Staff panela — pokriveno u [E06](e06-trust-tier-sistem.md)/[E07](e07-moderacijski-workflow-i-ai-screening.md)
- Upravljanje kategorijama i tagovima — pokriveno u [E03b](e03b-kategorizacija-sadrzaja-admin-upravljanje.md)
- Finansijski izvještaji i upravljanje cijenama — pokriveno u [E09](e09-kreditni-sistem-i-wallet.md)/[E10](e10-promocije-listinga.md)
- GlobalAdmin sistem ([master.cityinfo.ba](http://master.cityinfo.ba)) — Phase 2

**Persone:** Amra (moderatorica), Dino (operater), lokalni admin

**Journey milestones:** J-08

**Phase:** MVP

**Dokumentacijska referenca:** Ch.03 (sekcija 3.5 — Staff entitet, uloge, permisije, matrica ovlasti), **Ch.05** (sekcija 5.4 — moderatorske akcije i permisije), **Ch.03** (sekcija 3.7 — sigurnost i pristup)

**Tehničke napomene:**

- Staff sistem koristi odvojeni set API-ja sa prefiksom `/staff/` — potpuno odvojen od User API-ja
- Obavezna 2FA za sve Staff naloge — bez izuzetaka
- Staff nalog se ne može samo-registrovati; kreira ga isključivo local\_admin za svoj tenant
- Session je ograničen na 1 aktivan po Staff nalogu (nova prijava automatski gasi prethodni session)
- Ovisi o [E14](e14-infrastruktura-i18n-i-pozadinski-procesi.md) (infrastruktura) i [E01](e01-korisnicka-registracija-i-profil.md) (auth mehanizmi koji se mogu dijeliti na tehničkom nivou)
- Staff panel ([admin.cityinfo.ba](http://admin.cityinfo.ba)) je odvojen SvelteKit projekat — ne dijeli UI sa User frontend-om

**Success metrika:** Local admin može kreirati moderatora, dodijeliti mu permisije i tenant pristup, a moderator se može prijaviti sa 2FA i vidjeti admin panel shell — sve u manje od 5 minuta.

* * *

<a id="storije-u-ovom-epicu"></a>

## Storije u ovom epicu

| #   | Storija | Phase | Journey |
| --- | --- | --- | --- |
| [S13-01](e13-staff-panel-autentifikacija-i-upravljanje-osobljem/s13-01-staff-login-i-session-management.md) | Staff login i session management | MVP | **J-08** |
| [S13-02](e13-staff-panel-autentifikacija-i-upravljanje-osobljem/s13-02-promjena-lozinke-i-politika-rotacije.md) | Promjena lozinke i politika rotacije | MVP | **J-08** |
| [S13-03](e13-staff-panel-autentifikacija-i-upravljanje-osobljem/s13-03-kreiranje-staff-naloga.md) | Kreiranje Staff naloga | MVP | **J-08** |
| [S13-04](e13-staff-panel-autentifikacija-i-upravljanje-osobljem/s13-04-pregled-i-upravljanje-staff-nalozima.md) | Pregled i upravljanje Staff nalozima | MVP | **J-08** |
| [S13-05](e13-staff-panel-autentifikacija-i-upravljanje-osobljem/s13-05-dodjela-i-oduzimanje-moderatorskih-permisija.md) | Dodjela i oduzimanje moderatorskih permisija | MVP | **J-08** |
| [S13-06](e13-staff-panel-autentifikacija-i-upravljanje-osobljem/s13-06-upravljanje-tenant-pristupom-za-staff.md) | Upravljanje tenant pristupom za Staff | MVP | **J-08** |
| [S13-07](e13-staff-panel-autentifikacija-i-upravljanje-osobljem/s13-07-staff-panel-shell-i-navigacija.md) | Staff panel shell i navigacija | MVP | **J-08** |