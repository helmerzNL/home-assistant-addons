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
3. Fill in **rp_id** on the **Configuration** tab (see below), or turn on **password_login** to sign in with a username and password
   instead (see *Signing in with a password*). Save, and **Start** the app. The first start creates the database and applies all
   migrations, which takes a minute.
4. Open the app and go through the onboarding: your name and a passkey (at `https://<your domain>`), or a username and password; and save the recovery codes.

### Domain and https: needed for passkeys

Signing in uses passkeys. A browser only creates them on a page served over **https**, on a **domain name** (not an IP address and not
`http://homeassistant.local:6181`; `http://localhost` is the one exception). So DiscVault has to be reachable on an https address you
control, and that address is what you enter:

| Option | What to enter |
|---|---|
| **rp_id** | The domain only, for example `vault.example.com`. Required, unless **password_login** is on. Passkeys are bound to it: changing it later makes existing passkeys unusable. |
| **rp_origins** | The full address(es), comma separated, for example `https://vault.example.com`. Empty means `https://` plus the domain. |
| **trusted_proxies** | The address of your reverse proxy, so the client addresses in the audit log are right. |

Put a reverse proxy with a certificate in front of port **6181** of this app (for example the Nginx Proxy Manager or Caddy app, a
Cloudflare Tunnel, or Tailscale serve). Home Assistant Cloud (Nabu Casa) only forwards Home Assistant itself, not other ports. The app is
not offered through the Home Assistant sidebar (Ingress): it is made to be served from the root of its own domain, which is what passkeys are bound to.

### Signing in with a password

Without a domain and https there are no passkeys. Turn on **password_login** and DiscVault offers a password onboarding for the first
owner instead, the same way MealieShopper does: a username, a password of at least 15 characters, and an authenticator app (TOTP) with
recovery codes. **rp_id** may then stay empty.

- When you open the app on a local IP address (for example `http://192.168.1.10:6181`) and no domain is set, the authenticator app is optional.
  Over a domain or through a reverse proxy it is required.
- With both a domain (**rp_id**) and **password_login** you can use passkeys and the password side by side.
- This onboarding is for a brand-new installation. On an installation that already has users, an Owner or Admin turns password sign-in on
  in **Users & roles**, confirmed with a passkey.
- Do not expose the password login to the internet without https and a reverse proxy.

### Options

| Option | Meaning |
|---|---|
| **password_login** | Allow signing in with a username and password (plus TOTP) next to, or instead of, passkeys. Off by default. |
| **oidc_issuer**, **oidc_client_id**, **oidc_client_secret**, **oidc_provider_name**, **oidc_insecure_backchannel_origins** | Sign in through an OpenID Connect identity provider; see *Signing in through an identity provider*. |
| **rp_name** | The name your browser shows with a passkey (default DiscVault). |
| **omdb_api_key**, **tmdb_api_key** | Optional keys for movie metadata lookups (omdbapi.com, themoviedb.org). They can also be entered in the app. |
| **block_crawlers** | Keeps this instance out of search engines and AI crawlers (on by default). |

Changes take effect after a restart of the app. The secrets DiscVault needs (the signing secret and the database password) are made on the
first start and kept in `secrets.json` in the data folder. Do not delete that file: the signing secret also protects the keys stored in the database.

### Connecting an AI assistant (MCP)

The MCP endpoint is on the same address, under `/mcp`. Create a personal API key in DiscVault and give the assistant that address.

### Signing in through an identity provider (OpenID Connect)

DiscVault can sign people in through an OpenID Connect identity provider such as Pocket ID, Authentik or Keycloak. It is off until you fill in
the options below. Passkeys, the password and API keys keep working next to it.

1. Set **rp_id** (or **rp_origins**) to the https address DiscVault is opened on. The redirect address below is built from the first address in
   **rp_origins**, or from `https://` plus **rp_id**.
2. In your identity provider make a *confidential* OpenID Connect client and register this redirect URI, exactly like this (no trailing slash):
   `https://vault.example.com/api/next/auth/oidc/callback`. The Log tab prints the address for your set-up when the app starts.
3. Fill in **oidc_issuer** (an https address), **oidc_client_id** and **oidc_client_secret**, all three or none: the app does not start with a
   partial set-up and the Log tab says what is missing. **oidc_provider_name** is the name on the sign-in button (default OIDC).
4. Restart the app. A sign-in button for your provider appears, and an existing account can link or unlink its identity.

Only when your provider publishes *private http* addresses for token and key requests (for example Pocket ID inside a cluster) you also fill in
**oidc_insecure_backchannel_origins** with those exact origins, comma separated; leave it empty otherwise. The client secret is kept in the options
of this app (masked in the form), which Home Assistant includes in its backups.

### Data, backups and moving

- The database is in `postgres`, the posters, profiles and backups in `posters`, `profiles` and `backups` inside the data folder.
  Home Assistant stops the app while it makes a backup (a running database is not a consistent copy), so a backup takes DiscVault offline for a moment.
- DiscVault has its own backup and restore, which is the way to move an installation between this app and the Docker installation.
  It can also back up on a schedule (**Admin → Backup → Schedule**: how often, skip when nothing changed, keep the newest N) and sync your
  Jellyfin and Plex libraries (**Admin → Scheduled tasks**). Both are off until an admin turns them on. The scheduled backups are written to
  the `backups` folder, so Home Assistant includes them in its own backups.
- The database is PostgreSQL 17. A data folder cannot be opened by another major version; the app refuses to start rather than touch it.

### Updating

A new release shows up as an update of this app. Updating rebuilds the app on your device and restarts it; migrations run on start.
Some releases change the database (26.10 ran four migrations), so take a Home Assistant backup of this app first. If you restore or import a
library that was made with a version older than 26.10, open **Admin → Metadata**, find the **Vote counts** card and press **Fill in vote
counts** once: until then the *Minimum votes* filter leaves those films out. **Admin → Plugins** shows the installed plugin versions.

## Nederlands

Deze app draait [DiscVault](https://github.com/helmerzNL/DiscVault) (de stabiele lijn van DiscVault 26) in Home Assistant. De app, de
achtergrondtaken, het MCP-eindpunt en de PostgreSQL-database draaien samen in deze ene container; alles wat ze opslaan staat in de
data-map van deze app, die Home Assistant meeneemt in zijn back-ups.

### Installeren

1. Ga in Home Assistant naar **Instellingen > Apps > App installeren** (oudere versies: **Instellingen > Add-ons > Add-on store**), open het
   menu (⋮) > **Repositories** en voeg `https://github.com/helmerzNL/home-assistant-addons` toe.
2. Kies **DiscVault (beta)** en klik op **Installeren**. Home Assistant bouwt de app op je apparaat; de eerste keer duurt dat een paar minuten.
3. Vul op het tabblad **Configuratie** **rp_id** in (zie hieronder), of zet **password_login** aan om met een gebruikersnaam en wachtwoord
   in te loggen (zie *Inloggen met een wachtwoord*). Sla op en **Start** de app. De eerste start maakt de database aan en voert alle
   migraties uit; dat duurt een minuutje.
4. Open de app en doorloop de onboarding: je naam en een passkey (op `https://<jouw domein>`), of een gebruikersnaam en wachtwoord; en bewaar de herstelcodes.

### Domein en https: nodig voor passkeys

Inloggen gaat met passkeys. Een browser maakt die alleen aan op een pagina via **https**, op een **domeinnaam** (dus niet op een IP-adres en
niet op `http://homeassistant.local:6181`; `http://localhost` is de enige uitzondering). DiscVault moet dus bereikbaar zijn op een
https-adres dat je zelf beheert, en dat adres vul je in:

| Optie | Wat invullen |
|---|---|
| **rp_id** | Alleen het domein, bijvoorbeeld `vault.example.com`. Verplicht, tenzij **password_login** aanstaat. Passkeys zijn eraan gebonden: later wijzigen maakt bestaande passkeys onbruikbaar. |
| **rp_origins** | Het volledige adres (of adressen, kommagescheiden), bijvoorbeeld `https://vault.example.com`. Leeg betekent `https://` plus het domein. |
| **trusted_proxies** | Het adres van je reverse proxy, zodat de clientadressen in het auditlogboek kloppen. |

Zet een reverse proxy met certificaat voor poort **6181** van deze app (bijvoorbeeld de Nginx Proxy Manager- of Caddy-app, een Cloudflare
Tunnel of Tailscale serve). Home Assistant Cloud (Nabu Casa) stuurt alleen Home Assistant zelf door, geen andere poorten. De app wordt niet
via de zijbalk van Home Assistant (Ingress) aangeboden: hij is gemaakt om op de root van een eigen domein te draaien, en daaraan zijn passkeys gebonden.

### Inloggen met een wachtwoord

Zonder domein en https zijn er geen passkeys. Zet **password_login** aan en DiscVault biedt in plaats daarvan een wachtwoord-onboarding voor
de eerste eigenaar, zoals MealieShopper: een gebruikersnaam, een wachtwoord van minstens 15 tekens en een authenticator-app (TOTP) met
herstelcodes. **rp_id** mag dan leeg blijven.

- Open je de app op een lokaal IP-adres (bijvoorbeeld `http://192.168.1.10:6181`) en is er geen domein ingesteld, dan is de authenticator-app optioneel.
  Via een domein of reverse proxy is hij verplicht.
- Met zowel een domein (**rp_id**) als **password_login** kun je passkeys en wachtwoord naast elkaar gebruiken.
- Deze onboarding is voor een gloednieuwe installatie. Bij een installatie die al gebruikers heeft, zet een Owner of Admin inloggen met wachtwoord
  aan onder **Gebruikers & rollen**, bevestigd met een passkey.
- Zet het wachtwoord-inloggen niet zonder https en reverse proxy op internet.

### Opties

| Optie | Betekenis |
|---|---|
| **password_login** | Sta inloggen met gebruikersnaam en wachtwoord (plus TOTP) toe naast, of in plaats van, passkeys. Standaard uit. |
| **oidc_issuer**, **oidc_client_id**, **oidc_client_secret**, **oidc_provider_name**, **oidc_insecure_backchannel_origins** | Inloggen via een OpenID Connect-identiteitsprovider; zie *Inloggen via een identiteitsprovider*. |
| **rp_name** | De naam die je browser bij een passkey toont (standaard DiscVault). |
| **omdb_api_key**, **tmdb_api_key** | Optionele sleutels voor het opzoeken van filmgegevens (omdbapi.com, themoviedb.org). Ze kunnen ook in de app worden ingevuld. |
| **block_crawlers** | Houdt deze installatie uit zoekmachines en AI-crawlers (standaard aan). |

Wijzigingen gaan in na een herstart van de app. De geheimen die DiscVault nodig heeft (het ondertekeningsgeheim en het databasewachtwoord)
worden bij de eerste start gemaakt en bewaard in `secrets.json` in de data-map. Verwijder dat bestand niet: het ondertekeningsgeheim beschermt
ook de sleutels die in de database staan.

### Een AI-assistent koppelen (MCP)

Het MCP-eindpunt staat op hetzelfde adres, onder `/mcp`. Maak in DiscVault een persoonlijke API-sleutel aan en geef de assistent dat adres.

### Inloggen via een identiteitsprovider (OpenID Connect)

DiscVault kan mensen laten inloggen via een OpenID Connect-identiteitsprovider zoals Pocket ID, Authentik of Keycloak. Het staat uit totdat je
de onderstaande opties invult. Passkeys, het wachtwoord en API-sleutels blijven er gewoon naast werken.

1. Zet **rp_id** (of **rp_origins**) op het https-adres waarop DiscVault wordt geopend. Het redirect-adres hieronder wordt gemaakt van het eerste
   adres in **rp_origins**, of van `https://` plus **rp_id**.
2. Maak in je identiteitsprovider een *vertrouwelijke* OpenID Connect-client en registreer precies dit redirect-URI (zonder slash aan het eind):
   `https://vault.example.com/api/next/auth/oidc/callback`. Het tabblad Logboek toont het adres voor jouw opzet bij het starten van de app.
3. Vul **oidc_issuer** (een https-adres), **oidc_client_id** en **oidc_client_secret** in, alle drie of geen: de app start niet met een
   gedeeltelijke opzet en het Logboek zegt wat er ontbreekt. **oidc_provider_name** is de naam op de inlogknop (standaard OIDC).
4. Herstart de app. Er verschijnt een inlogknop voor je provider, en een bestaand account kan zijn identiteit koppelen of ontkoppelen.

Alleen als je provider *privé-http*-adressen publiceert voor token- en sleutelverzoeken (bijvoorbeeld Pocket ID binnen een cluster) vul je ook
**oidc_insecure_backchannel_origins** in met precies die origins, kommagescheiden; anders laat je het leeg. Het clientgeheim staat in de opties
van deze app (gemaskeerd in het formulier), die Home Assistant meeneemt in zijn back-ups.

### Gegevens, back-ups en verhuizen

- De database staat in `postgres`, de posters, profielen en back-ups in `posters`, `profiles` en `backups` in de data-map.
  Home Assistant stopt de app tijdens een back-up (een draaiende database is geen consistente kopie), dus DiscVault is daarbij even offline.
- DiscVault heeft een eigen back-up en terugzetten; daarmee verhuis je een installatie tussen deze app en de Docker-installatie.
  Hij kan ook volgens schema een back-up maken (**Beheer → Backup → Planning**: hoe vaak, overslaan als er niets is gewijzigd, de nieuwste N
  bewaren) en je Jellyfin- en Plex-bibliotheken synchroniseren (**Beheer → Geplande taken**). Beide staan uit totdat een beheerder ze aanzet. De
  geplande back-ups komen in de map `backups`, dus Home Assistant neemt ze mee in zijn eigen back-ups.
- De database is PostgreSQL 17. Een data-map kan niet door een andere hoofdversie worden geopend; de app weigert te starten in plaats van eraan te komen.

### Updaten

Een nieuwe release verschijnt als update van deze app. Bijwerken bouwt de app opnieuw op je apparaat en herstart hem; migraties draaien bij het starten.
Sommige releases wijzigen de database (26.10 voerde vier migraties uit), dus maak eerst een Home Assistant-back-up van deze app. Zet je een
bibliotheek terug of importeer je er een die met een oudere versie dan 26.10 is gemaakt, open dan **Beheer → Metadata**, zoek de kaart
**Stemmenaantallen** en druk eenmaal op **Stemmenaantallen invullen**: tot die tijd laat het filter *Minimaal aantal stemmen* die films weg. Onder **Beheer → Plugins** zie je de geïnstalleerde pluginversies.
