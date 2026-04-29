# Page ID Inventory za md2conf

Skripta `build_page_id_map.py` skenira Confluence sub-tree pod `EPICS AND STORIES`
folderom i pravi `page-id-map.json` fajl koji mapira logičke ID-eve (E01, S01-01,
itd.) na Confluence page ID-eve.

Ovaj mapping se zatim koristi u sljedećoj fazi (Faza 1) za upisivanje
`confluence_page_id` field-a u YAML frontmatter svakog markdown fajla.

## Smještaj u repou

Predlažem da skriptu staviš u poseban folder uz ostali tooling:

```
cityinfo_documentation/
├── jira-sync/                  ← postojeći Jira tooling
│   └── ...
└── md2conf-tooling/            ← NOVO
    ├── build_page_id_map.py
    ├── page-id-map.json        ← generisani output (commit-uj u git)
    ├── requirements.txt
    └── README.md
```

`page-id-map.json` se commit-uje u git da bi tim imao referentnu mapu, ali se
regeneriše po potrebi (npr. kad se kreiraju novi epici/storije).

## Preduslovi

```bash
pip install requests
```

Environment varijable (iste kao za Jira sync):

```bash
ATLASSIAN_EMAIL=tvoj.email@example.com
ATLASSIAN_API_TOKEN=tvoj_api_token
```

Na Windowsu (PowerShell):

```powershell
$env:ATLASSIAN_EMAIL = "tvoj.email@example.com"
$env:ATLASSIAN_API_TOKEN = "tvoj_token"
```

Ili ih učitaj iz `.env` fajla (vidi glavni README repoa).

## Pokretanje

```bash
cd md2conf-tooling
python build_page_id_map.py
```

Output se zapisuje u `page-id-map.json` u istom direktorijumu. Možeš ga preusmjeriti:

```bash
python build_page_id_map.py --output ../md2conf-config/page-id-map.json
```

## Šta dobijaš

`page-id-map.json` ima strukturu:

```json
{
  "generated_at": "2026-04-29T15:30:00",
  "cloud_id": "45983047-331b-459e-b1a5-052825171c8c",
  "epics_and_stories_root": "250249231",
  "root_pages": {
    "Ch.01": "240156678",
    "Ch.02": "240254995",
    ...
    "MVP-SCOPE": "242188289",
    "STATUS-MODEL-SPEC": "253526019"
  },
  "epics_and_stories": {
    "E01": "251232295",
    "E02": "251330580",
    ...
    "S01-01": "251396116",
    "S01-02": "251166741",
    ...
  },
  "unmapped": [
    {
      "id": "251068418",
      "title": "Pisanje Epica i User Storija — Instrukcija",
      "reason": "naslov ne počinje sa E##/S##-## patternom"
    },
    {
      "id": "250970134",
      "title": "Plan pisanja epica i storija",
      "reason": "naslov ne počinje sa E##/S##-## patternom"
    }
  ],
  "duplicates": {}
}
```

## Šta provjeriti nakon prvog run-a

1. **Brojevi u sažetku:** Trebao bi imati 15 epica + 89 storija = 104 mapirane stavke
   pod `epics_and_stories`. Ako je broj manji — nešto fali (provjeri `unmapped`).

2. **Unmapped lista:** Tu trebaju biti samo meta stranice ("Plan pisanja epica i
   storija", "Pisanje Epica i User Storija — Instrukcija"). Ako se tu pojavi
   bilo koji epic ili story — naslov mu nije u očekivanom formatu i regex ga je
   propustio. Treba ručno popraviti naslov na Confluenceu ili dopuniti regex.

3. **Duplicates:** Treba biti prazno. Ako nije — neko je vjerovatno slučajno
   kreirao dvije stranice sa istim ID-om u naslovu, treba ručno riješiti.

## Sljedeći korak

Kad ovaj fajl izgleda OK, prelazi se u Fazu 1: skripta `inject_page_ids.py`
koja čita `page-id-map.json` i upisuje `confluence_page_id` u YAML frontmatter
svakog markdown fajla u repou.
