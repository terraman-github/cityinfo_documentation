# Atlassian API — napomene za skriptanje

> Naučeno kroz praktičan rad na CityInfo projektu (april 2026).  
> Dodati u projektne instrukcije da se ne ponavljaju isti problemi.

---

## Konfiguracija

**Cloud ID** za `terraprojects.atlassian.net`: `45983047-331b-459e-b1a5-052825171c8c`

Sve Jira API pozive slati na:
```
https://api.atlassian.com/ex/jira/45983047-331b-459e-b1a5-052825171c8c/rest/api/3/...
```

**NE** koristiti `https://terraprojects.atlassian.net/rest/api/3/...` — vraća `410 Gone`.

Autentifikacija: Basic Auth sa `ATLASSIAN_EMAIL` + `ATLASSIAN_API_TOKEN` (env varijable).

---

## Jira API

### Kreiranje i ažuriranje issue-a

```python
# Kreiranje — POST
POST /rest/api/3/issue
body: { "fields": { "project": {"key": "CIT"}, "summary": "...", "issuetype": {"name": "Epic"} } }

# Ažuriranje opisa — PUT (vraća 204, nema body-ja)
PUT /rest/api/3/issue/{key}
body: { "fields": { "description": <ADF objekt> } }
```

### Hijerarhija Epic → Story

Projekt `CIT` koristi **classic** stil — Story se veže za Epic putem `parent` polja:
```python
"fields": { "parent": {"key": "CIT-1"} }
```
**Ne** koristiti `customfield_10014` (Epic Link) — ne postoji na ovom projektu.

### Jira search — NE RADI iz skripte

`GET /rest/api/3/search` i `POST /rest/api/3/search` vraćaju `410 Gone` pri Basic Auth pozivu iz Python skripte na ovom Jira planu. **Jedini search koji radi je putem Atlassian MCP-a u claude.ai.**

Workaround: umjesto dinamičkog search-a, koristiti **statičku ugrađenu mapu** `epic_key → [(story_key, story_title), ...]` koja se pripremi jednom ručno ili putem MCP-a.

### Confluence URL format za linkove

Ispravan URL koji uvijek radi (bez ovisnosti o space key-u):
```
https://terraprojects.atlassian.net/wiki/pages/viewpage.action?pageId={page_id}
```

**Ne** koristiti `/wiki/pages/{page_id}` — ne radi.

### Smart Link (inline card) u Jira opisu

Za prikaz Confluence stranice kao klikabilne kartice sa previewom u Jira opisu, koristiti ADF `inlineCard` node:

```python
{
    "version": 1,
    "type": "doc",
    "content": [
        {
            "type": "paragraph",
            "content": [{"type": "text", "text": "Tekst opisa..."}]
        },
        {
            "type": "paragraph",
            "content": [
                {
                    "type": "inlineCard",
                    "attrs": {"url": "https://terraprojects.atlassian.net/wiki/pages/viewpage.action?pageId=123456"}
                }
            ]
        }
    ]
}
```

**Ne** dodavati i tekstualni link i `inlineCard` za isti URL — link se pojavljuje dvaput. Koristiti samo `inlineCard`.

---

## Confluence API

### Dohvatanje sadržaja stranice

Koristiti **Confluence v1 REST API** sa `body.view` reprezentacijom:
```
GET /wiki/rest/api/content/{page_id}?expand=body.view
```

`body.view` vraća HTML koji se može parsirati. **Ne** koristiti `body.export_view` — vraća plain text bez strukture (bold markeri se gube, parsing sekcija poput `**Excerpt:**` ne radi).

### HTML → tekst konverter

Confluence `body.view` je HTML. Za parsing sekcija poput `**Excerpt:**` i `**User story:**` potrebno je HTML pretvoriti u tekst koji čuva `**bold**` markere:

```python
def html_to_text(html):
    text = re.sub(r"<br[^>]*>", "\n", html)
    text = re.sub(r"</p>", "\n", text)
    text = re.sub(r"</li>", "\n", text)
    text = re.sub(r"<li[^>]*>", "- ", text)
    text = re.sub(r"<strong>", "**", text)
    text = re.sub(r"</strong>", "**", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&amp;", "&").replace("&nbsp;", " ").replace("&#8212;", "—")
    # normalizacija praznina...
    return text.strip()
```

### Dohvatanje child stranica

Koristiti **Confluence v2 API**:
```
GET /wiki/api/v2/pages/{page_id}/children?limit=50
```
Podržava cursor paginaciju putem `_links.next` u odgovoru.

### Ažuriranje stranice

`updateConfluencePage` **zamjenjuje cijeli body** — uvijek dohvatiti trenutni sadržaj prije update-a. Za stranice ~50KB+, body pisati u lokalni fajl prije slanja. Uvijek uključiti `versionMessage`.

---

## Opšti savjeti

- **Testiraj na jednom issue-u** (`--epic CIT-1`) prije live runa na svim issue-ima.
- **Dry-run kao default** u svim skriptama — `--live` flag za stvarno pisanje.
- **Rate limiting**: dodati `time.sleep(0.3–0.4)` između PUT poziva pri bulk update-u (~95 issue-a = ~30s).
- **Statička mapa umjesto search-a**: kad Jira search ne radi, mapa `key → page_id` pripremljena jednom ručno (ili putem MCP-a u claude.ai) je pouzdaniji pristup.
- **Provjera sintakse** Python skripte prije distribucije: `python3 -c "import ast; ast.parse(open('script.py').read())"`.
