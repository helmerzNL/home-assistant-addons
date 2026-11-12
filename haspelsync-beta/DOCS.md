# HaspelSync (beta)

*English first · Nederlands hieronder.*

> **Beta.** The development version of the app, built from its `main` branch. New features and fixes arrive here first and it can be
> unstable. It has its own data folder and port, so it runs next to the stable app. Do not point it at the data of the stable app: a beta can
> change the database in ways the stable version cannot read.
>
> **Bèta.** De ontwikkelversie van de app, gebouwd vanaf de `main`-branch. Nieuwe functies en fixes komen hier eerst en het kan onstabiel zijn.
> Hij heeft een eigen data-map en poort, dus hij draait naast de stabiele app. Gebruik de data van de stabiele app niet voor de beta: een beta kan
> de database aanpassen op een manier die de stabiele versie niet kan lezen.

## English

This app runs [HaspelSync](https://github.com/Rdiger-36/HaspelSync) inside Home Assistant. It listens to your Bambu Lab printers and keeps
[Spoolman](https://github.com/Donkie/Spoolman) in step with them: which spool sits in which AMS slot, and what every print actually used, taken
from the sliced file. HaspelSync is made by Rdiger-36; this app only packages the published image. A problem in HaspelSync itself belongs in
[its repository](https://github.com/Rdiger-36/HaspelSync/issues); a problem with this app in
[this one](https://github.com/helmerzNL/home-assistant-addons/issues).

### Before you start

- **Spoolman** has to run. The **Spoolman** app from this repository is the simplest: its address is `http://<address of Home Assistant>:7912`.
- For every printer: its **serial number**, **IP address** and **access code** (on the printer's screen, under the network or LAN settings). Give
  the printer a fixed IP address in your router.
- Home Assistant has to reach the printer on port **8883** (MQTT, what the AMS holds) and **990** (FTPS, the sliced file). Cloud mode, LAN only mode
  and developer mode all work: nothing is read through the Bambu cloud.
- A **P2S**, an **H2** series printer or an **X2D** needs a USB stick in the printer: those models only offer the sliced file from the stick.
- In Bambu Studio turn on **Update remaining capacity**, so the AMS reports the remaining weight a spool is matched against.

### Install

1. In Home Assistant open **Settings > Apps > Install app** (older versions: **Settings > Add-ons > Add-on store**), then the menu (⋮) > **Repositories**, and add
   `https://github.com/helmerzNL/home-assistant-addons`.
2. Choose **HaspelSync (beta)** and **Install**. Home Assistant builds the app on your device, which takes a minute the first time.
3. **Start** the app and open it with **Open web UI** (it opens in a new window at `http://<address of Home Assistant>:4001`).
4. Under **Settings** enter the **Spoolman endpoint**, for the Spoolman app `http://<address of Home Assistant>:7912`, and test the connection.
5. Under **Printers** add each printer with name, serial number, IP address and access code. The dialog tests MQTT and FTPS before it saves.
6. Pick the **operation mode**, `automatic` or `manual`. Nothing has to be prepared in Spoolman: HaspelSync creates the extra field it needs.

An original Bambu Lab spool is recognised by its RFID tag. A spool of another brand is linked to a Spoolman spool once, in the web interface, and
is tracked from then on.

### Password

The web interface has **no password until you set one** under **Settings**: until then everybody who can reach port **4001** can change the
printers and their access codes. Set one right after the first start, and do not forward port 4001 on your router. Tools that talk to the API
(such as the HaspelSync integration for Home Assistant) use an API key, made under **Settings** as well.

HaspelSync answers on the IP address of Home Assistant and on names ending in `.local`, such as `homeassistant.local`. It refuses any other name,
to protect against DNS rebinding: to open it on a domain name (for example behind a reverse proxy), add that name under **Settings** > *Allowed host
names* first, from the IP address.

### Options

This app has no options: everything is set up in the web interface of HaspelSync. Its log follows the time zone of Home Assistant.

### Data, backups and moving

- The printers, settings, slot mappings, API keys and the state of a running print are JSON files in `/data/printers` in the app's data folder; the
  logs are in `/data/logs`. Home Assistant includes both in its backups and stops the app for a moment while it makes one.
- **Coming from a Docker installation?** Stop the app, copy the files of your old `printers` folder (in the Docker image `/app/printers`) into
  `/data/printers` of this app, for example with the Samba or SSH app, and start it again.

### Updating

A new release of HaspelSync shows up as an update of this app once its image is published. Updating rebuilds the app on your device and restarts
it. The architectures are **amd64** and **aarch64** (the published image is built for both, so it also runs on a Raspberry Pi 4/5 or an ARM mini PC).

## Nederlands

Deze app draait [HaspelSync](https://github.com/Rdiger-36/HaspelSync) in Home Assistant. Hij luistert naar je Bambu Lab-printers en houdt
[Spoolman](https://github.com/Donkie/Spoolman) daarmee gelijk: welke spoel in welk AMS-vak zit, en wat elke print echt gebruikte, gelezen uit het
geslicede bestand. HaspelSync is gemaakt door Rdiger-36; deze app verpakt alleen het gepubliceerde image. Een probleem in HaspelSync zelf hoort in
[zijn repository](https://github.com/Rdiger-36/HaspelSync/issues); een probleem met deze app in
[deze](https://github.com/helmerzNL/home-assistant-addons/issues).

### Voordat je begint

- **Spoolman** moet draaien. De app **Spoolman** uit deze repository is het eenvoudigst: het adres is `http://<adres van Home Assistant>:7912`.
- Van elke printer: het **serienummer**, het **IP-adres** en de **toegangscode** (op het scherm van de printer, bij de netwerk- of LAN-instellingen).
  Geef de printer een vast IP-adres in je router.
- Home Assistant moet de printer kunnen bereiken op poort **8883** (MQTT, wat de AMS bevat) en **990** (FTPS, het geslicede bestand). Cloudmodus,
  alleen-LAN-modus en ontwikkelaarsmodus werken allemaal: er wordt niets via de Bambu-cloud gelezen.
- Een **P2S**, een printer uit de **H2**-serie of een **X2D** heeft een USB-stick in de printer nodig: die modellen bieden het geslicede bestand
  alleen vanaf de stick aan.
- Zet in Bambu Studio **Update remaining capacity** aan, zodat de AMS het resterende gewicht doorgeeft waarop een spoel wordt gematcht.

### Installeren

1. Ga in Home Assistant naar **Instellingen > Apps > App installeren** (oudere versies: **Instellingen > Add-ons > Add-on store**), open het
   menu (⋮) > **Repositories** en voeg `https://github.com/helmerzNL/home-assistant-addons` toe.
2. Kies **HaspelSync (beta)** en klik op **Installeren**. Home Assistant bouwt de app op je apparaat; de eerste keer duurt dat een minuut.
3. **Start** de app en open hem met **Webinterface openen** (die opent in een nieuw venster op `http://<adres van Home Assistant>:4001`).
4. Vul onder **Settings** het **Spoolman endpoint** in, voor de Spoolman-app `http://<adres van Home Assistant>:7912`, en test de verbinding.
5. Voeg onder **Printers** elke printer toe met naam, serienummer, IP-adres en toegangscode. Het venster test MQTT en FTPS voordat het opslaat.
6. Kies de **operation mode**, `automatic` of `manual`. In Spoolman hoeft niets voorbereid te worden: HaspelSync maakt het extra veld dat hij nodig
   heeft zelf aan.

Een originele Bambu Lab-spoel wordt herkend aan zijn RFID-tag. Een spoel van een ander merk koppel je één keer aan een Spoolman-spoel in de
webinterface; daarna wordt hij gevolgd.

### Wachtwoord

De webinterface heeft **geen wachtwoord totdat je er een instelt** onder **Settings**: tot dan kan iedereen die poort **4001** bereikt de printers en
hun toegangscodes aanpassen. Stel er een in direct na de eerste start, en zet poort 4001 niet open in je router. Programma's die de API gebruiken
(zoals de HaspelSync-integratie voor Home Assistant) gebruiken een API-sleutel, die je ook onder **Settings** maakt.

HaspelSync antwoordt op het IP-adres van Home Assistant en op namen die eindigen op `.local`, zoals `homeassistant.local`. Elke andere naam weigert
hij, ter bescherming tegen DNS-rebinding: wil je hem op een domeinnaam openen (bijvoorbeeld achter een reverse proxy), voeg die naam dan eerst toe
onder **Settings** > *Allowed host names*, vanaf het IP-adres.

### Opties

Deze app heeft geen opties: alles stel je in in de webinterface van HaspelSync. Het logboek volgt de tijdzone van Home Assistant.

### Gegevens, back-ups en verhuizen

- De printers, instellingen, vak-koppelingen, API-sleutels en de stand van een lopende print zijn JSON-bestanden in `/data/printers` in de data-map
  van de app; de logs staan in `/data/logs`. Home Assistant neemt beide mee in zijn back-ups en stopt de app even tijdens een back-up.
- **Kom je van een Docker-installatie?** Stop de app, kopieer de bestanden uit je oude map `printers` (in het Docker-image `/app/printers`) naar
  `/data/printers` van deze app, bijvoorbeeld met de Samba- of SSH-app, en start hem weer.

### Updaten

Een nieuwe release van HaspelSync verschijnt als update van deze app zodra het image ervan gepubliceerd is. Bijwerken bouwt de app opnieuw op je
apparaat en herstart hem. De architecturen zijn **amd64** en **aarch64** (het gepubliceerde image is voor beide gebouwd, dus het draait ook op een
Raspberry Pi 4/5 of een ARM-minipc).
