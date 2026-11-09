# Doorbell Map

*English first · Nederlands hieronder.*

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
2. Choose **Doorbell Map** and **Install**. Home Assistant builds the app on your device, which takes a minute the first time.
3. **Start** the app and open the **Log** tab: the setup code for the admin is printed there (or type your own under *Setup code*).
4. Open the app with **Open web UI** (it opens in a new window at `http://<address of Home Assistant>:9888`) or at `https://<your domain>`.
   The map is at the root; the admin is at `/beheer`.
5. Enter the setup code, choose a username and sign in with a **password** or, on an https address, a **passkey**.

### Password or passkey

The app works on any address. How the admin signs in depends on it:

- **A username and password** work everywhere, also on `http://<address of Home Assistant>:9888` on your own network. Choose this on the first screen of
  `/beheer`; you can turn on two-step verification (MFA) later, and add a passkey once the app is reachable over https.
- **A passkey** is more secure and easier, but a browser only creates one on a page served over **https**, on a **domain name** (not an IP
  address and not `http://homeassistant.local:9888`; `http://localhost` is the one exception). The first screen only offers it where it works.

For passkeys, installing the map as an app on a phone and notifications, put a reverse proxy with a certificate in front of port **9888** of
this app (for example the Nginx Proxy Manager or Caddy app, a Cloudflare Tunnel, or Tailscale serve). Home Assistant Cloud (Nabu Casa) only
forwards Home Assistant itself, not other ports. The app is not offered through the Home Assistant sidebar (Ingress): it is made to be served
from the root of its own address.

Without **origin** the app follows the address it is opened on (behind a proxy through `X-Forwarded-Proto` and `X-Forwarded-Host`), and the links
in the QR codes get the address you open the admin on. Fill in **origin** when the map should only be reachable on one address; changes from any
other address are then refused, so open the map on that address instead of with **Open web UI**.

### Options

| Option | Meaning |
|---|---|
| **origin** | Optional. The full address the map is opened on, for example `https://map.example.com`. Empty means the address in the browser. Older versions of the app still need it; the Log says so. |
| **rp_id** | The domain for passkeys. Empty means the host name of *origin* (or of the address in the browser), which is almost always right. Changing it makes existing passkeys unusable. |
| **site_title** | Name of the site until you change it in the admin. |
| **setup_token** | Typed once for the very first passkey or password. Empty makes one and prints it in the Log. |
| **session_hours** | How long the admin stays signed in (default 12). |
| **max_backups** | How many of the app's own backups are kept (default 50); older ones are removed, also at start-up. |

Changes take effect after a restart of the app.

### Data, backups and moving

- The houses, passkeys, settings and the app's automatic backups are in the data folder of this app; the generated secrets (session key,
  setup code) are in `secrets.json` next to them. Home Assistant stops the app for a moment while it makes a backup.
- To move between this app and the Docker installation, copy the data folder (or use a backup from the admin).
- The app keeps its newest 50 backups (one ZIP each, in `backups`) and removes older ones, also when it starts. Before version 2.0 it
  kept 200: set **max_backups** before updating from 1.x if you want to keep more.

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
2. Kies **Doorbell Map** en klik op **Installeren**. Home Assistant bouwt de app op je apparaat; de eerste keer duurt dat een minuutje.
3. **Start** de app en open het tabblad **Logboek**: daar staat de instelcode voor de beheerder (of typ zelf een code bij *Instelcode*).
4. Open de app met **Webinterface openen** (die opent in een nieuw venster op `http://<adres van Home Assistant>:9888`) of op
   `https://<jouw domein>`. De kaart staat op de root, het beheer op `/beheer`.
5. Voer de instelcode in, kies een gebruikersnaam en log in met een **wachtwoord** of, op een https-adres, een **passkey**.

### Wachtwoord of passkey

De app werkt op elk adres. Hoe de beheerder inlogt, hangt ervan af:

- **Een gebruikersnaam en wachtwoord** werken overal, ook op `http://<adres van Home Assistant>:9888` in je eigen netwerk. Kies dit op het eerste scherm van
  `/beheer`; later kun je tweestapsverificatie (MFA) aanzetten, en een passkey toevoegen als de app via https bereikbaar is.
- **Een passkey** is veiliger en makkelijker, maar een browser maakt die alleen aan op een pagina via **https**, op een **domeinnaam** (dus niet
  op een IP-adres en niet op `http://homeassistant.local:9888`; `http://localhost` is de enige uitzondering). Het eerste scherm biedt hem alleen
  aan waar hij werkt.

Voor passkeys, het installeren van de kaart als app op een telefoon en meldingen zet je een reverse proxy met certificaat voor poort **9888** van
deze app (bijvoorbeeld de Nginx Proxy Manager- of Caddy-app, een Cloudflare Tunnel of Tailscale serve). Home Assistant Cloud (Nabu Casa) stuurt
alleen Home Assistant zelf door, geen andere poorten. De app wordt niet via de zijbalk van Home Assistant (Ingress) aangeboden: hij is gemaakt om
op de root van een eigen adres te draaien.

Zonder **origin** volgt de app het adres waarop hij wordt geopend (achter een proxy via `X-Forwarded-Proto` en `X-Forwarded-Host`), en krijgen
de links in de QR-codes het adres waarop je het beheer opent. Vul **origin** in als de kaart maar op één adres bereikbaar hoort te zijn; wijzigingen
vanaf een ander adres worden dan geweigerd, dus open de kaart dan op dat adres in plaats van met **Webinterface openen**.

### Opties

| Optie | Betekenis |
|---|---|
| **origin** | Optioneel. Het volledige adres waarop de kaart wordt geopend, bijvoorbeeld `https://kaart.example.com`. Leeg betekent het adres in de browser. Oudere versies van de app hebben het nog nodig; het Logboek zegt het dan. |
| **rp_id** | Het domein voor passkeys. Leeg betekent de hostnaam van *origin* (of van het adres in de browser), wat bijna altijd goed is. Wijzigen maakt bestaande passkeys onbruikbaar. |
| **site_title** | Naam van de site totdat je die in het beheer aanpast. |
| **setup_token** | Eenmalig nodig voor de allereerste passkey of het eerste wachtwoord. Leeg maakt er een en toont die in het Logboek. |
| **session_hours** | Hoe lang de beheerder ingelogd blijft (standaard 12). |
| **max_backups** | Hoeveel eigen back-ups van de app bewaard blijven (standaard 50); oudere worden opgeruimd, ook bij het starten. |

Wijzigingen gaan in na een herstart van de app.

### Gegevens, back-ups en verhuizen

- De huizen, passkeys, instellingen en de automatische back-ups van de app staan in de data-map van deze app; de gegenereerde geheimen
  (sessiesleutel, instelcode) staan ernaast in `secrets.json`. Home Assistant stopt de app even tijdens een back-up.
- Om tussen deze app en de Docker-installatie te verhuizen kopieer je de data-map (of gebruik je een back-up uit het beheer).
- De app bewaart zijn nieuwste 50 back-ups (elk één ZIP, in `backups`) en ruimt oudere op, ook bij het starten. Vóór versie 2.0 waren
  dat er 200: zet **max_backups** vóór het bijwerken vanaf 1.x als je er meer wilt houden.

### Updaten

Een nieuwe release verschijnt als update van deze app. Bijwerken bouwt de app opnieuw op je apparaat en herstart hem.
