# Confluence → Jira sync skripte

Skripte za automatizovano kreiranje i ažuriranje Jira issue-a (Epika i Storija) na osnovu sadržaja iz Confluence dokumentacije.

Skripte su dio CityInfo projekta i nalaze se u repozitoriju `cityinfo_documentation`.

---

## Fajlovi

| Fajl | Svrha |
|---|---|
| `confluence_to_jira.py` | Kreira nove Jira issue-e iz Confluencea (inicijalni run) |
| `confluence_to_jira_fix.py` | Ažurira opise postojećih Jira issue-a (fix/refresh run) |

---

## Preduslovi

**Python 3.10+** i jedna zavisnost:

```
py -m pip install requests
```

**Env varijable** — postavi prije svakog pokretanja u PowerShell terminalu:

```powershell
$env:ATLASSIAN_EMAIL="tvoj@email.com"
$env:ATLASSIAN_API_TOKEN="tvoj-api-token"
```

API token se generiše na: https://id.atlassian.com/manage-profile/security/api-tokens

---

## confluence_to_jira.py — kreiranje issue-a

Čita strukturu epica i storija iz Confluence foldera **EPICS AND STORIES** i kreira odgovarajuće issue-e u Jira projektu `CIT`.

**Šta kreira:**
- Jira **Epic** za svaku Confluence stranicu čiji naslov počinje sa `E##`
- Jira **Story** za svaku podstranicu čiji naslov počinje sa `S##-##`, vezanu za parent epic putem `parent` polja

**Šta upisuje u opis:**
- Epic: excerpt iz Confluence stranice + Smart Link kartica na Confluence stranicu
- Story: user story citat (blockquote) + Smart Link kartica na Confluence stranicu

### Pokretanje

```powershell
# Dry-run — provjeri šta bi se kreiralo (nema pisanja u Jiru)
py confluence_to_jira.py

# Dry-run samo za jedan epic
py confluence_to_jira.py --epic E01

# Live run — stvarno kreira issue-e
py confluence_to_jira.py --live

# Live run samo za jedan epic
py confluence_to_jira.py --live --epic E01
```

> ⚠️ Pokreni dry-run i provjeri output prije live runa. Skript ne provjerava da li issue već postoji — pokretanje dva puta kreira duplikate.

---

## confluence_to_jira_fix.py — ažuriranje opisa

Ažurira opise **postojećih** Jira issue-a svježim sadržajem iz Confluencea. Koristi se kad se sadržaj na Confluenceu promijeni, ili kad inicijalni run nije upisao ispravan opis.

Za razliku od `confluence_to_jira.py`, ovaj skript **ne kreira** nove issue-e — samo radi PUT update na postojećim.

### Pokretanje

```powershell
# Dry-run sve (prikaži šta bi se ažuriralo)
py confluence_to_jira_fix.py

# Dry-run jedan epic i njegove storije
py confluence_to_jira_fix.py --epic CIT-1

# Dry-run jedna storija
py confluence_to_jira_fix.py --story CIT-42

# Live run — ažuriraj sve
py confluence_to_jira_fix.py --live

# Live run jedan epic
py confluence_to_jira_fix.py --epic CIT-1 --live

# Live run jedna storija
py confluence_to_jira_fix.py --story CIT-42 --live
```

### Referenca argumenata

| Argument | Opis |
|---|---|
| *(bez argumenata)* | Dry-run sve issue-e |
| `--live` | Stvarno upiši u Jiru (bez ovoga uvijek dry-run) |
| `--epic CIT-X` | Filtriraj po epicu i svim njegovim storijama |
| `--story CIT-X` | Filtriraj na jednu storiju |

---

## Confluence struktura koju skripte očekuju

```
📁 EPICS AND STORIES/             ← page ID: 250249231
├── 📄 E01 — Naziv epica          ← epic stranica
│   ├── 📄 S01-01 — Naziv storije ← story podstranica
│   ├── 📄 S01-02 — Naziv storije
│   └── ...
├── 📄 E02 — Naziv epica
│   └── ...
└── ...
```

Naslovi stranica **moraju** počinjati sa prefiksom `E##` (epici) ili `S##-##` (storije) — skripte filtriraju po ovom obrascu.

---

## Napomene

- Skripte imaju ugrađenu pauzu od `0.4s` između Jira API poziva kako bi se izbjegao rate limiting.
- Jira search API (`/rest/api/3/search`) **ne radi** sa Basic Auth na ovom Jira planu — skripte koriste statičku mapu `Jira key → Confluence page ID` umjesto dinamičkog searcha.
- Ispravan Confluence URL format za linkove: `https://terraprojects.atlassian.net/wiki/pages/viewpage.action?pageId={page_id}`
- Detaljna tehnička dokumentacija o Atlassian API specifičnostima: `ATLASSIAN-SCRIPTING-NOTES.md`
