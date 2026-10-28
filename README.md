# helmerzNL Home Assistant add-ons

*English first · Nederlands hieronder.*

[![Add this repository to your Home Assistant](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FhelmerzNL%2Fhome-assistant-addons)

## English

Home Assistant apps (add-ons) for the self-hosted apps of helmerzNL and Flux76. Every add-on runs the same published app image as the Docker version.

### Install

1. In Home Assistant open **Settings > Apps > Install app** (older versions: **Settings > Add-ons > Add-on store**).
2. Open the menu (⋮) > **Repositories** and add `https://github.com/helmerzNL/home-assistant-addons` (or press the button above).
3. Pick an app from the list below, **Install** it, and read its **Documentation** tab. Each app also has a quick start on its first page.

### The apps

| App | What it does | Port | Architectures | Database |
|---|---|---|---|---|
| [**DiscVault**](discvault/DOCS.md) | Manager for your 4K UHD, Blu-ray and DVD collection | 6180 | amd64, aarch64 | PostgreSQL, built in |
| [**MealieShopper**](mealieshopper/DOCS.md) | Week menu from Mealie to your supermarket basket | 5959 | amd64, aarch64 | SQLite |
| [**MealieShopper (beta)**](mealieshopper-beta/DOCS.md) | The development version, next to the stable one | 5960 | amd64, aarch64 | SQLite |
| [**3D Print Pricing**](printpricing/DOCS.md) | Cost price calculator and inventory for a 3D-print business | 6080 | amd64 | PostgreSQL, built in |
| [**Doorbell Map**](doorbell-map/DOCS.md) | Neighbourhood map of houses that do or do not want a visit | 9888 | amd64, aarch64 | files |

DiscVault, 3D Print Pricing and Doorbell Map sign in with **passkeys**, which only work on an **https** address with a domain name: put a
reverse proxy with a certificate in front of them. The documentation of each app explains what to enter.

### How updates work

An update shows up in Home Assistant when `version` in an add-on's `config.yaml` changes. `scripts/sync_versions.py` (run daily by the
*Update add-on versions* workflow) compares that version with the newest release of each app and **only raises it once the image of that release
is published**; the workflow then opens a pull request. Merge it and Home Assistant offers the update. `sources.json` says which repository,
tag pattern and image belong to which add-on.

### Maintaining this repository

```bash
pip install pyyaml
python scripts/check_addons.py           # every add-on complete, translated (en/nl), documented in English and Dutch, no port clashes
python -m unittest discover -s tests     # Python tests
node --test tests/*.test.js              # Doorbell Map start script
python scripts/sync_versions.py --check  # which versions would be raised
```

To add an app: make a folder with `config.yaml`, `README.md` and `DOCS.md` (each with an English and a Dutch section, and a quick start /
install section), `CHANGELOG.md`, `icon.png` (128 px), `logo.png` (256 px) and `translations/en.yaml` and `nl.yaml`; add it to `sources.json`
and to the lists in `.github/workflows/ci.yml`. `check_addons.py` tells you what is missing.

## Nederlands

Home Assistant-apps (add-ons) voor de zelf te hosten apps van helmerzNL en Flux76. Elke add-on draait hetzelfde gepubliceerde app-image als de Docker-versie.

### Installeren

1. Ga in Home Assistant naar **Instellingen > Apps > App installeren** (oudere versies: **Instellingen > Add-ons > Add-on store**).
2. Open het menu (⋮) > **Repositories** en voeg `https://github.com/helmerzNL/home-assistant-addons` toe (of druk op de knop hierboven).
3. Kies hieronder een app, **installeer** hem en lees het tabblad **Documentatie**. Elke app heeft ook een korte "Snel starten" op de eerste pagina.

### De apps

Zie de tabel hierboven: DiscVault (collectiebeheer voor 4K UHD, Blu-ray en dvd), MealieShopper (weekmenu naar boodschappenmandje, ook als beta),
3D Print Pricing (kostprijs en voorraad voor 3D-printen) en Doorbell Map (wijkkaart voor deur-aan-deur-acties).

DiscVault, 3D Print Pricing en Doorbell Map loggen in met **passkeys**. Die werken alleen op een **https**-adres met een domeinnaam: zet er een
reverse proxy met certificaat voor. De documentatie van elke app legt uit wat je invult.

### Hoe updates werken

Een update verschijnt in Home Assistant zodra `version` in de `config.yaml` van een add-on verandert. `scripts/sync_versions.py` (dagelijks gedraaid
door de workflow *Update add-on versions*) vergelijkt die versie met de nieuwste release van elke app en **verhoogt hem pas als het image van die
release gepubliceerd is**; de workflow opent dan een pull request. Merge die en Home Assistant biedt de update aan. In `sources.json` staat welke
repository, tag en welk image bij welke add-on horen.

### Beheer van deze repository

De commando's staan hierboven bij *Maintaining this repository*. Een nieuwe app toevoegen: maak een map met `config.yaml`, `README.md` en `DOCS.md`
(elk met een Engelse en een Nederlandse sectie en een snelstart/installatie), `CHANGELOG.md`, `icon.png`, `logo.png` en `translations/en.yaml` en
`nl.yaml`; zet hem in `sources.json` en in de lijsten van `.github/workflows/ci.yml`. `check_addons.py` meldt wat er nog ontbreekt.
