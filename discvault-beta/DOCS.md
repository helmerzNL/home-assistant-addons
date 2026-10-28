# DiscVault (beta)

*English first · Nederlands hieronder.*

> **Beta.** The development version of the app, built from its `beta` branch. New features and fixes arrive here first and it can be
> unstable. It has its own data folder and port, so it runs next to the stable app. Do not point it at the data of the stable app: a beta can
> change the database in ways the stable version cannot read.
>
> **Bèta.** De ontwikkelversie van de app, gebouwd vanaf de `beta`-branch. Nieuwe functies en fixes komen hier eerst en het kan onstabiel zijn.
> Hij heeft een eigen data-map en poort, dus hij draait naast de stabiele app. Gebruik de data van de stabiele app niet voor de beta: een beta kan
> de database aanpassen op een manier die de stabiele versie niet kan lezen.

## English

This app runs [DiscVault](https://github.com/helmerzNL/DiscVault) (the DiscVault 26 stable line) inside Home Assistant. The app, its
background worker, the MCP endpoint and the PostgreSQL database run in this one container; everything they store lives in the data
folder of this app, which Home Assistant includes in its backups.

### Install

1. In Home Assistant open **Settings > Apps > Install app** (older versions: **Settings > Add-ons > Add-on store**), then the menu (⋮) >
   **Repositories**, and add `https://github.com/helmerzNL/home-assistant-addons`.
2. Choose **DiscVault (beta)** and **Install**. Home Assistant builds the app on your device, which takes a few minutes the first time.
3. Fill in **rp_id** on the **Configuration** tab (see below), save, and **Start** the app. The first start creates the database and
   applies all migrations, which takes a minute.
4. Open the app at `https://<your domain>` and go through the onboarding: your name, a passkey, and save the recovery codes.

### Domain and https: needed for passkeys

Signing in uses passkeys. A browser only creates them on a page served over **https**, on a **domain name** (not an IP address and not
`http://homeassistant.local:6181`; `http://localhost` is the one exception). So DiscVault has to be reachable on an https address you
control, and that address is what you enter:

| Option | What to enter |
|---|---|
| **rp_id** | The domain only, for example `vault.example.com`. Required. Passkeys are bound to it: changing it later makes existing passkeys unusable. |
| **rp_origins** | The full address(es), comma separated, for example `https://vault.example.com`. Empty means `https://` plus the domain. |
| **trusted_proxies** | The address of your reverse proxy, so the client addresses in the audit log are right. |

Put a reverse proxy with a certificate in front of port **6181** of this app (for example the Nginx Proxy Manager or Caddy app, a
Cloudflare Tunnel, or Tailscale serve). Home Assistant Cloud (Nabu Casa) only forwards Home Assistant itself, not other ports. The app is
not offered through the Home Assistant sidebar (Ingress): it is made to be served from the root of its own domain, which is what passkeys are bound to.

### Options

| Option | Meaning |
|---|---|
| **rp_name** | The name your browser shows with a passkey (default DiscVault). |
| **omdb_api_key**, **tmdb_api_key** | Optional keys for movie metadata lookups (omdbapi.com, themoviedb.org). They can also be entered in the app. |
| **block_crawlers** | Keeps this instance out of search engines and AI crawlers (on by default). |

Changes take effect after a restart of the app. The secrets DiscVault needs (the signing secret and the database password) are made on the
first start and kept in `secrets.json` in the data folder. Do not delete that file: the signing secret also protects the keys stored in the database.

### Connecting an AI assistant (MCP)

The MCP endpoint is on the same address, under `/mcp`. Create a personal API key in DiscVault and give the assistant that address.

### Data, backups and moving

- The database is in `postgres`, the posters, profiles and backups in `posters`, `profiles` and `backups` inside the data folder.
  Home Assistant stops the app while it makes a backup (a running database is not a consistent copy), so a backup takes DiscVault offline for a moment.
- DiscVault has its own backup and restore, which is the way to move an installation between this app and the Docker installation.
- The database is PostgreSQL 17. A data folder cannot be opened by another major version; the app refuses to start rather than touch it.

### Updating

A new release shows up as an update of this app. Updating rebuilds the app on your device and restarts it; migrations run on start.
This app follows the stable line; the beta is not offered here.

## Nederlands

Deze app draait [DiscVault](https://github.com/helmerzNL/DiscVault) (de stabiele lijn van DiscVault 26) in Home Assistant. De app, de
achtergrondtaken, het MCP-eindpunt en de PostgreSQL-database draaien samen in deze ene container; alles wat ze opslaan staat in de
data-map van deze app, die Home Assistant meeneemt in zijn back-ups.

### Installeren

1. Ga in Home Assistant naar **Instellingen > Apps > App installeren** (oudere versies: **Instellingen > Add-ons > Add-on store**), open het
   menu (⋮) > **Repositories** en voeg `https://github.com/helmerzNL/home-assistant-addons` toe.
2. Kies **DiscVault (beta)** en klik op **Installeren**. Home Assistant bouwt de app op je apparaat; de eerste keer duurt dat een paar minuten.
3. Vul op het tabblad **Configuratie** **rp_id** in (zie hieronder), sla op en **Start** de app. De eerste start maakt de database aan en
   voert alle migraties uit; dat duurt een minuutje.
4. Open de app op `https://<jouw domein>` en doorloop de onboarding: je naam, een passkey, en bewaar de herstelcodes.

### Domein en https: nodig voor passkeys

Inloggen gaat met passkeys. Een browser maakt die alleen aan op een pagina via **https**, op een **domeinnaam** (dus niet op een IP-adres en
niet op `http://homeassistant.local:6181`; `http://localhost` is de enige uitzondering). DiscVault moet dus bereikbaar zijn op een
https-adres dat je zelf beheert, en dat adres vul je in:

| Optie | Wat invullen |
|---|---|
| **rp_id** | Alleen het domein, bijvoorbeeld `vault.example.com`. Verplicht. Passkeys zijn eraan gebonden: later wijzigen maakt bestaande passkeys onbruikbaar. |
| **rp_origins** | Het volledige adres (of adressen, kommagescheiden), bijvoorbeeld `https://vault.example.com`. Leeg betekent `https://` plus het domein. |
| **trusted_proxies** | Het adres van je reverse proxy, zodat de clientadressen in het auditlogboek kloppen. |

Zet een reverse proxy met certificaat voor poort **6181** van deze app (bijvoorbeeld de Nginx Proxy Manager- of Caddy-app, een Cloudflare
Tunnel of Tailscale serve). Home Assistant Cloud (Nabu Casa) stuurt alleen Home Assistant zelf door, geen andere poorten. De app wordt niet
via de zijbalk van Home Assistant (Ingress) aangeboden: hij is gemaakt om op de root van een eigen domein te draaien, en daaraan zijn passkeys gebonden.

### Opties

| Optie | Betekenis |
|---|---|
| **rp_name** | De naam die je browser bij een passkey toont (standaard DiscVault). |
| **omdb_api_key**, **tmdb_api_key** | Optionele sleutels voor het opzoeken van filmgegevens (omdbapi.com, themoviedb.org). Ze kunnen ook in de app worden ingevuld. |
| **block_crawlers** | Houdt deze installatie uit zoekmachines en AI-crawlers (standaard aan). |

Wijzigingen gaan in na een herstart van de app. De geheimen die DiscVault nodig heeft (het ondertekeningsgeheim en het databasewachtwoord)
worden bij de eerste start gemaakt en bewaard in `secrets.json` in de data-map. Verwijder dat bestand niet: het ondertekeningsgeheim beschermt
ook de sleutels die in de database staan.

### Een AI-assistent koppelen (MCP)

Het MCP-eindpunt staat op hetzelfde adres, onder `/mcp`. Maak in DiscVault een persoonlijke API-sleutel aan en geef de assistent dat adres.

### Gegevens, back-ups en verhuizen

- De database staat in `postgres`, de posters, profielen en back-ups in `posters`, `profiles` en `backups` in de data-map.
  Home Assistant stopt de app tijdens een back-up (een draaiende database is geen consistente kopie), dus DiscVault is daarbij even offline.
- DiscVault heeft een eigen back-up en terugzetten; daarmee verhuis je een installatie tussen deze app en de Docker-installatie.
- De database is PostgreSQL 17. Een data-map kan niet door een andere hoofdversie worden geopend; de app weigert te starten in plaats van eraan te komen.

### Updaten

Een nieuwe release verschijnt als update van deze app. Bijwerken bouwt de app opnieuw op je apparaat en herstart hem; migraties draaien bij het starten.
Deze app volgt de stabiele lijn; de beta wordt hier niet aangeboden.
