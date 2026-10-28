# 3D Print Pricing (beta)

*English first · Nederlands hieronder.*

> **Beta.** The development version of the app, built from its `beta` branch. New features and fixes arrive here first and it can be
> unstable. It has its own data folder and port, so it runs next to the stable app. Do not point it at the data of the stable app: a beta can
> change the database in ways the stable version cannot read.
>
> **Bèta.** De ontwikkelversie van de app, gebouwd vanaf de `beta`-branch. Nieuwe functies en fixes komen hier eerst en het kan onstabiel zijn.
> Hij heeft een eigen data-map en poort, dus hij draait naast de stabiele app. Gebruik de data van de stabiele app niet voor de beta: een beta kan
> de database aanpassen op een manier die de stabiele versie niet kan lezen.

## English

This app runs [3D Print Pricing](https://github.com/Flux76HQ/3dprint_pricing) inside Home Assistant. The app and its PostgreSQL database
run in this one container; everything they store lives in the app's own data folder, which Home Assistant includes in its backups.

### Install

1. In Home Assistant open **Settings > Apps > Install app** (older versions: **Settings > Add-ons > Add-on store**), then the menu (⋮) > **Repositories**, and add
   `https://github.com/helmerzNL/home-assistant-addons`.
2. Choose **3D Print Pricing (beta)** and **Install**. Home Assistant builds the app on your device, which takes a few minutes the first time.
3. Optionally fill in **rp_id** on the **Configuration** tab (see below), save, and **Start** the app.
4. Open the **Log** tab: the setup code for the first screen is printed there (or type your own under *Setup code*).
5. Open the app (`https://<your domain>` with a domain, otherwise `http://<address of Home Assistant>:6081`) and go through the onboarding: setup code, your name, a passkey or a password, and save the 8 recovery codes.

### Passkey or password

The app works on any address. How you sign in depends on it:

- **A password** works everywhere, also on `http://<address of Home Assistant>:6081` on your own network. Choose it on the first screen; you can add
  two-step verification with an authenticator app later, under Settings.
- **A passkey** is more secure and easier, but a browser only creates one on a page served over **https**, on a **domain name** (not an IP address and not
  `http://homeassistant.local:6081`; `http://localhost` is the one exception). For that the app has to be reachable on an https address you control, and that
  address is what you enter below. The first screen tells you when a passkey cannot work on the address you are using.

| Option | What to enter |
|---|---|
| **rp_id** | Optional. The domain only, for example `print.example.com`. Leave it empty to follow the address the app is opened on. Passkeys are bound to it: changing it later makes existing passkeys unusable (recovery codes still work). Set it once you use passkeys. |
| **rp_origins** | Optional. The full address(es), comma separated, for example `https://print.example.com`. Empty means `https://` plus the domain, or the address the app is opened on when there is no domain. When set, writes from any other address are refused. |
| **proxy_hops** | `1` when one reverse proxy sits in front of the app (the usual case), `0` when the app is opened on its port directly. |

For passkeys put a reverse proxy with a certificate in front of port **6081** of this app (for example the Nginx Proxy Manager or Caddy app, a
Cloudflare Tunnel, or Tailscale serve). Home Assistant Cloud (Nabu Casa) only forwards Home Assistant itself, not other ports. The app is
not offered through the Home Assistant sidebar (Ingress): it is made to be served from the root of its own domain, which is what passkeys are bound to.

### Options

| Option | Meaning |
|---|---|
| **setup_code** | Typed once on the first screen. Empty makes one and prints it in the Log. |
| **max_upload_mb** | Largest STL/3MF upload. A proxy in front has to allow at least as much. |
| **ai_images_enabled** | Switches on the optional AI product images. The OpenAI key is entered in the app, under *Settings → AI images*. |
| **spoolman_url** | Address of a Spoolman, for example `http://homeassistant.local:7912`. Empty: type it in the app (*Settings → Filaments*, in the *Spoolman* card, which is folded at first). |
| **update_check** | The app asks GitHub whether a newer release exists and tells the owner. It never updates anything; updating is done here, in Home Assistant. |

Changes take effect after a restart of the app.

### Data, backups and moving

- The database is in `/data/postgres`, the uploads in `/data/uploads` and the generated secrets (session key, database password, push keys)
  in `/data/secrets.json`. Home Assistant stops the app while it makes a backup (a running database is not a consistent copy), so a backup
  takes the app offline for a moment.
- The app also has its own backup and restore (*Settings → System*), which is the way to move an installation between this app and the Docker
  Compose installation, in either direction. A backup file never contains passkeys or users: the person restoring signs up again.
- The database is PostgreSQL 17. A data folder cannot be opened by another major version; the app refuses to start rather than touch it.

### Updating

A new release shows up as an update of this app. Updating rebuilds the app on your device and restarts it; migrations run on start. The
architectures are **amd64** and **aarch64** (the published image is built for both, so it also runs on a Raspberry Pi 4/5 or an ARM mini PC).

## Nederlands

Deze app draait [3D Print Pricing](https://github.com/Flux76HQ/3dprint_pricing) in Home Assistant. De app en de PostgreSQL-database draaien
samen in deze ene container; alles wat ze opslaan staat in de eigen data-map van de app, die Home Assistant meeneemt in zijn back-ups.

### Installeren

1. Ga in Home Assistant naar **Instellingen > Apps > App installeren** (oudere versies: **Instellingen > Add-ons > Add-on store**), open het
   menu (⋮) > **Repositories** en voeg `https://github.com/helmerzNL/home-assistant-addons` toe.
2. Kies **3D Print Pricing (beta)** en klik op **Installeren**. Home Assistant bouwt de app op je apparaat; de eerste keer duurt dat een paar minuten.
3. Vul op het tabblad **Configuratie** eventueel **rp_id** in (zie hieronder), sla op en **Start** de app.
4. Open het tabblad **Logboek**: daar staat de instelcode voor het eerste scherm (of typ zelf een code bij *Instelcode*).
5. Open de app (`https://<jouw domein>` met een domein, anders `http://<adres van Home Assistant>:6081`) en doorloop de onboarding: instelcode, je naam, een passkey of een wachtwoord, en bewaar de 8 herstelcodes.

### Passkey of wachtwoord

De app werkt op elk adres. Hoe je inlogt hangt daarvan af:

- **Een wachtwoord** werkt overal, ook op `http://<adres van Home Assistant>:6081` in je eigen netwerk. Kies het op het eerste scherm; later kun je
  onder Instellingen tweestapsverificatie met een authenticator-app toevoegen.
- **Een passkey** is veiliger en makkelijker, maar een browser maakt die alleen aan op een pagina via **https**, op een **domeinnaam** (dus niet op een
  IP-adres en niet op `http://homeassistant.local:6081`; `http://localhost` is de enige uitzondering). Daarvoor moet de app bereikbaar zijn op een
  https-adres dat je zelf beheert, en dat adres vul je hieronder in. Het eerste scherm meldt het als een passkey op het adres dat je gebruikt niet kan werken.

| Optie | Wat invullen |
|---|---|
| **rp_id** | Optioneel. Alleen het domein, bijvoorbeeld `print.example.com`. Leeg betekent het adres waarop de app wordt geopend. Passkeys zijn eraan gebonden: later wijzigen maakt bestaande passkeys onbruikbaar (herstelcodes werken nog). Vul het in zodra je passkeys gebruikt. |
| **rp_origins** | Optioneel. Het volledige adres (of adressen, kommagescheiden), bijvoorbeeld `https://print.example.com`. Leeg betekent `https://` plus het domein, of het adres waarop de app wordt geopend als er geen domein is. Als het is ingevuld, worden wijzigingen vanaf een ander adres geweigerd. |
| **proxy_hops** | `1` als er één reverse proxy voor de app staat (het gebruikelijke geval), `0` als de app rechtstreeks op zijn poort wordt geopend. |

Voor passkeys: zet een reverse proxy met certificaat voor poort **6081** van deze app (bijvoorbeeld de Nginx Proxy Manager- of Caddy-app, een Cloudflare
Tunnel of Tailscale serve). Home Assistant Cloud (Nabu Casa) stuurt alleen Home Assistant zelf door, geen andere poorten. De app wordt niet
via de zijbalk van Home Assistant (Ingress) aangeboden: hij is gemaakt om op de root van een eigen domein te draaien, en daaraan zijn passkeys gebonden.

### Opties

| Optie | Betekenis |
|---|---|
| **setup_code** | Eenmalig in het eerste scherm in te typen. Leeg maakt er een en toont die in het Logboek. |
| **max_upload_mb** | Grootste STL/3MF-upload. Een proxy ervoor moet minstens zoveel toestaan. |
| **ai_images_enabled** | Schakelt de optionele AI-productafbeeldingen in. De OpenAI-sleutel voer je in de app in, onder *Instellingen → AI-afbeeldingen*. |
| **spoolman_url** | Adres van een Spoolman, bijvoorbeeld `http://homeassistant.local:7912`. Leeg: typ het in de app (*Instellingen → Filamenten*, in de kaart *Spoolman*, die eerst ingeklapt is). |
| **update_check** | De app vraagt GitHub of er een nieuwere release is en meldt dat aan de eigenaar. Hij werkt nooit zelf bij; bijwerken doe je hier, in Home Assistant. |

Wijzigingen gaan in na een herstart van de app.

### Gegevens, back-ups en verhuizen

- De database staat in `/data/postgres`, de uploads in `/data/uploads` en de gegenereerde geheimen (sessiesleutel, databasewachtwoord,
  pushsleutels) in `/data/secrets.json`. Home Assistant stopt de app tijdens een back-up (een draaiende database is geen consistente kopie),
  dus een back-up haalt de app even offline.
- De app heeft ook een eigen back-up en terugzetten (*Instellingen → Systeem*); daarmee verhuis je een installatie tussen deze app en de
  Docker Compose-installatie, in beide richtingen. Een back-upbestand bevat nooit passkeys of gebruikers: wie terugzet, meldt zich opnieuw aan.
- De database is PostgreSQL 17. Een data-map kan niet door een andere hoofdversie worden geopend; de app weigert te starten in plaats van eraan te komen.

### Updaten

Een nieuwe release verschijnt als update van deze app. Bijwerken bouwt de app opnieuw op je apparaat en herstart hem; migraties draaien bij
het starten. De architecturen zijn **amd64** en **aarch64** (het gepubliceerde image is voor beide gebouwd, dus het draait ook op een Raspberry Pi 4/5 of een ARM-minipc).
