# Doorbell Map (beta)

*English first · Nederlands hieronder.*

> **Beta.** The development version of the app, built from its `beta` branch. New features and fixes arrive here first and it can be
> unstable. It has its own data folder and port, so it runs next to the stable app. Do not point it at the data of the stable app: a beta can
> change the database in ways the stable version cannot read.
>
> **Bèta.** De ontwikkelversie van de app, gebouwd vanaf de `beta`-branch. Nieuwe functies en fixes komen hier eerst en het kan onstabiel zijn.
> Hij heeft een eigen data-map en poort, dus hij draait naast de stabiele app. Gebruik de data van de stabiele app niet voor de beta: een beta kan
> de database aanpassen op een manier die de stabiele versie niet kan lezen.

## English

This app runs [Doorbell Map](https://github.com/helmerzNL/Doorbell-Map) inside Home Assistant: the same app as the Docker version, with
its data in the data folder of this app, which Home Assistant includes in its backups.

### What it is

An interactive map (OpenStreetMap, no API key) on which every house is green, red or unmarked. Visitors look at the map, print a PDF or
install it as an app; residents change the status of their own house, which the admin approves; the admin draws the houses, makes QR codes
per house and manages everything under `/beheer`.

### Install

1. In Home Assistant open **Settings > Apps > Install app** (older versions: **Settings > Add-ons > Add-on store**), then the menu (⋮) >
   **Repositories**, and add `https://github.com/helmerzNL/home-assistant-addons`.
2. Choose **Doorbell Map (beta)** and **Install**. Home Assistant builds the app on your device, which takes a minute the first time.
3. Fill in **origin** on the **Configuration** tab (see below) and save.
4. **Start** the app and open the **Log** tab: the setup code for the first passkey is printed there (or type your own under *Setup code*).
5. Open `<origin>/beheer`, enter the setup code, and create your passkey. The map itself is at `<origin>`.

### Address and https: needed for the admin's passkey

The admin signs in with a passkey. A browser only creates one on a page served over **https**, on a **domain name** (not an IP address and
not `http://homeassistant.local:9889`; `http://localhost` is the one exception). So the app has to be reachable on an https address you
control, and that address is what you enter as **origin**. It has to be exactly the address in the browser bar, or changes are refused.

Put a reverse proxy with a certificate in front of port **9889** of this app (for example the Nginx Proxy Manager or Caddy app, a
Cloudflare Tunnel, or Tailscale serve). Home Assistant Cloud (Nabu Casa) only forwards Home Assistant itself, not other ports. The app is
not offered through the Home Assistant sidebar (Ingress): it is made to be served from the root of its own address.

### Options

| Option | Meaning |
|---|---|
| **origin** | The full address the map is opened on, for example `https://map.example.com`. Required. |
| **rp_id** | The domain for passkeys. Empty means the host name of *origin*, which is almost always right. Changing it makes existing passkeys unusable. |
| **site_title** | Name of the site until you change it in the admin. |
| **setup_token** | Typed once for the very first passkey. Empty makes one and prints it in the Log. |
| **session_hours** | How long the admin stays signed in (default 12). |

Changes take effect after a restart of the app.

### Data, backups and moving

- The houses, passkeys, settings and the app's automatic backups are in the data folder of this app; the generated secrets (session key,
  setup code) are in `secrets.json` next to them. Home Assistant stops the app for a moment while it makes a backup.
- To move between this app and the Docker installation, copy the data folder (or use a backup from the admin).

### Updating

A new release shows up as an update of this app. Updating rebuilds the app on your device and restarts it.

## Nederlands

Deze app draait [Doorbell Map](https://github.com/helmerzNL/Doorbell-Map) in Home Assistant: dezelfde app als de Docker-versie, met de
gegevens in de data-map van deze app. Home Assistant neemt die mee in zijn back-ups.

### Wat is het

Een interactieve kaart (OpenStreetMap, geen API-sleutel) waarop elk huis groen, rood of niet gemarkeerd is. Bezoekers bekijken de kaart,
maken een pdf of installeren hem als app; bewoners wijzigen de status van hun eigen huis, wat de beheerder goedkeurt; de beheerder tekent de
huizen, maakt QR-codes per huis en beheert alles onder `/beheer`.

### Installeren

1. Ga in Home Assistant naar **Instellingen > Apps > App installeren** (oudere versies: **Instellingen > Add-ons > Add-on store**), open het
   menu (⋮) > **Repositories** en voeg `https://github.com/helmerzNL/home-assistant-addons` toe.
2. Kies **Doorbell Map (beta)** en klik op **Installeren**. Home Assistant bouwt de app op je apparaat; de eerste keer duurt dat een minuutje.
3. Vul op het tabblad **Configuratie** **origin** in (zie hieronder) en sla op.
4. **Start** de app en open het tabblad **Logboek**: daar staat de instelcode voor de eerste passkey (of typ zelf een code bij *Instelcode*).
5. Open `<origin>/beheer`, voer de instelcode in en maak je passkey aan. De kaart zelf staat op `<origin>`.

### Adres en https: nodig voor de passkey van de beheerder

De beheerder logt in met een passkey. Een browser maakt die alleen aan op een pagina via **https**, op een **domeinnaam** (dus niet op een
IP-adres en niet op `http://homeassistant.local:9889`; `http://localhost` is de enige uitzondering). De app moet dus bereikbaar zijn op een
https-adres dat je zelf beheert, en dat adres vul je in bij **origin**. Het moet precies het adres in de adresbalk zijn, anders worden
wijzigingen geweigerd.

Zet een reverse proxy met certificaat voor poort **9889** van deze app (bijvoorbeeld de Nginx Proxy Manager- of Caddy-app, een Cloudflare
Tunnel of Tailscale serve). Home Assistant Cloud (Nabu Casa) stuurt alleen Home Assistant zelf door, geen andere poorten. De app wordt niet
via de zijbalk van Home Assistant (Ingress) aangeboden: hij is gemaakt om op de root van een eigen adres te draaien.

### Opties

| Optie | Betekenis |
|---|---|
| **origin** | Het volledige adres waarop de kaart wordt geopend, bijvoorbeeld `https://kaart.example.com`. Verplicht. |
| **rp_id** | Het domein voor passkeys. Leeg betekent de hostnaam van *origin*, wat bijna altijd goed is. Wijzigen maakt bestaande passkeys onbruikbaar. |
| **site_title** | Naam van de site totdat je die in het beheer aanpast. |
| **setup_token** | Eenmalig nodig voor de allereerste passkey. Leeg maakt er een en toont die in het Logboek. |
| **session_hours** | Hoe lang de beheerder ingelogd blijft (standaard 12). |

Wijzigingen gaan in na een herstart van de app.

### Gegevens, back-ups en verhuizen

- De huizen, passkeys, instellingen en de automatische back-ups van de app staan in de data-map van deze app; de gegenereerde geheimen
  (sessiesleutel, instelcode) staan ernaast in `secrets.json`. Home Assistant stopt de app even tijdens een back-up.
- Om tussen deze app en de Docker-installatie te verhuizen kopieer je de data-map (of gebruik je een back-up uit het beheer).

### Updaten

Een nieuwe release verschijnt als update van deze app. Bijwerken bouwt de app opnieuw op je apparaat en herstart hem.
