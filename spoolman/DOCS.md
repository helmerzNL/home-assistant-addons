# Spoolman

*English first · Nederlands hieronder.*

## English

This app runs [Spoolman](https://github.com/Donkie/Spoolman) inside Home Assistant: an inventory of your 3D-printer filament spools, with what
every print uses booked on the right spool. Spoolman is made by Donkie and its contributors; this app only packages the published image. A problem
in Spoolman itself belongs in [its repository](https://github.com/Donkie/Spoolman/issues); a problem with this app in
[this one](https://github.com/helmerzNL/home-assistant-addons/issues).

### Install

1. In Home Assistant open **Settings > Apps > Install app** (older versions: **Settings > Add-ons > Add-on store**), then the menu (⋮) > **Repositories**, and add
   `https://github.com/helmerzNL/home-assistant-addons`.
2. Choose **Spoolman** and **Install**. Home Assistant builds the app on your device, which takes a minute or two the first time.
3. **Start** the app and open it with **Open web UI** (it opens in a new window at `http://<address of Home Assistant>:7912`).
4. Add a filament and a spool, or pick the filament from SpoolmanDB, the community database of manufacturers and filaments.

### No login: keep it on your home network

Spoolman has **no login of its own**. Everybody who can reach port **7912** can read and change your inventory, and its API is open in the same way.
That is how Spoolman is meant to be run, on a home network, but it means:

- do not forward port 7912 on your router, and do not put it behind a reverse proxy on the internet without a login in front of it;
- if you do not need the port at all (for example because only HaspelSync on this Home Assistant talks to it), you can switch it off under
  *Network* on the app's *Configuration* tab. The tools then cannot reach Spoolman either, so leave it on when they run elsewhere.

### Connecting other tools

Every tool that books what a print uses talks to the same address, `http://<address of Home Assistant>:7912`:

- **HaspelSync** (also in this repository) keeps Spoolman in step with the AMS of a Bambu Lab printer. Enter that address as its *Spoolman
  endpoint*.
- **Klipper/Moonraker** (`[spoolman]` in `moonraker.conf`) and **OctoPrint** (the Spoolman plugin) take the same address.
- **3D Print Pricing** (also in this repository) has a *Spoolman address* option.

### Options

| Option | What it does |
|---|---|
| `automatic_backup` | Spoolman copies its database every night into the `backups` folder in the app's data folder. On by default. |
| `log_level` | How much Spoolman writes to the *Log* tab: `DEBUG`, `INFO` (default), `WARNING` or `ERROR`. |
| `update_check` | Spoolman asks GitHub whether a newer release exists and shows it in its web interface. The update itself comes as an update of this app. |

Spoolman uses its built-in SQLite database here. An external PostgreSQL or MySQL database is not offered by this app.

### Data, backups and moving

- Everything Spoolman keeps is in `/data/spoolman` in the app's data folder: the database `spoolman.db`, the nightly copies in `backups` and the
  logs. Home Assistant includes it in its backups and stops the app for a moment while it makes one, so the copy is consistent.
- **Coming from a Docker installation?** Stop the app, copy `spoolman.db` from your old data folder (in the Docker image
  `/home/app/.local/share/spoolman`) into `/data/spoolman` of this app, for example with the Samba or SSH app, and start it again.

### Updating

A new release of Spoolman shows up as an update of this app once its image is published. Updating rebuilds the app on your device and restarts it;
Spoolman upgrades its database on start. The architectures are **amd64** and **aarch64** (the published image is built for both, so it also runs on
a Raspberry Pi 4/5 or an ARM mini PC).

## Nederlands

Deze app draait [Spoolman](https://github.com/Donkie/Spoolman) in Home Assistant: een voorraad van je filamentspoelen voor de 3D-printer,
waarbij wat elke print gebruikt op de juiste spoel wordt geboekt. Spoolman is gemaakt door Donkie en zijn bijdragers; deze app verpakt alleen het
gepubliceerde image. Een probleem in Spoolman zelf hoort in [zijn repository](https://github.com/Donkie/Spoolman/issues); een probleem met deze app
in [deze](https://github.com/helmerzNL/home-assistant-addons/issues).

### Installeren

1. Ga in Home Assistant naar **Instellingen > Apps > App installeren** (oudere versies: **Instellingen > Add-ons > Add-on store**), open het
   menu (⋮) > **Repositories** en voeg `https://github.com/helmerzNL/home-assistant-addons` toe.
2. Kies **Spoolman** en klik op **Installeren**. Home Assistant bouwt de app op je apparaat; de eerste keer duurt dat een minuut of twee.
3. **Start** de app en open hem met **Webinterface openen** (die opent in een nieuw venster op `http://<adres van Home Assistant>:7912`).
4. Voeg een filament en een spoel toe, of kies het filament uit SpoolmanDB, de gedeelde database met fabrikanten en filamenten.

### Geen inlog: houd hem op je thuisnetwerk

Spoolman heeft **geen eigen inlog**. Iedereen die poort **7912** kan bereiken, kan je voorraad lezen en aanpassen, en de API is op dezelfde manier
open. Zo is Spoolman bedoeld, op een thuisnetwerk, maar het betekent:

- zet poort 7912 niet open in je router, en zet hem niet achter een reverse proxy op internet zonder een inlog ervoor;
- heb je de poort helemaal niet nodig (bijvoorbeeld omdat alleen HaspelSync op deze Home Assistant ermee praat), dan kun je hem uitzetten bij
  *Netwerk* op het tabblad *Configuratie* van de app. De andere programma's kunnen Spoolman dan ook niet bereiken, dus laat hem aan als die
  ergens anders draaien.

### Andere programma's koppelen

Elk programma dat verbruik boekt, praat met hetzelfde adres, `http://<adres van Home Assistant>:7912`:

- **HaspelSync** (ook in deze repository) houdt Spoolman gelijk met de AMS van een Bambu Lab-printer. Vul dat adres in als *Spoolman endpoint*.
- **Klipper/Moonraker** (`[spoolman]` in `moonraker.conf`) en **OctoPrint** (de Spoolman-plug-in) gebruiken hetzelfde adres.
- **3D Print Pricing** (ook in deze repository) heeft een optie *Spoolman-adres*.

### Opties

| Optie | Wat het doet |
|---|---|
| `automatic_backup` | Spoolman maakt elke nacht een kopie van zijn database in de map `backups` in de data-map van de app. Standaard aan. |
| `log_level` | Hoeveel Spoolman op het tabblad *Logboek* schrijft: `DEBUG`, `INFO` (standaard), `WARNING` of `ERROR`. |
| `update_check` | Spoolman vraagt GitHub of er een nieuwere release is en toont dat in zijn webinterface. De update zelf komt als update van deze app. |

Spoolman gebruikt hier zijn ingebouwde SQLite-database. Een externe PostgreSQL- of MySQL-database biedt deze app niet aan.

### Gegevens, back-ups en verhuizen

- Alles wat Spoolman bewaart staat in `/data/spoolman` in de data-map van de app: de database `spoolman.db`, de nachtelijke kopieën in `backups`
  en de logs. Home Assistant neemt die mee in zijn back-ups en stopt de app even tijdens een back-up, zodat de kopie klopt.
- **Kom je van een Docker-installatie?** Stop de app, kopieer `spoolman.db` uit je oude data-map (in het Docker-image
  `/home/app/.local/share/spoolman`) naar `/data/spoolman` van deze app, bijvoorbeeld met de Samba- of SSH-app, en start hem weer.

### Updaten

Een nieuwe release van Spoolman verschijnt als update van deze app zodra het image ervan gepubliceerd is. Bijwerken bouwt de app opnieuw op je
apparaat en herstart hem; Spoolman werkt zijn database bij bij het starten. De architecturen zijn **amd64** en **aarch64** (het gepubliceerde image
is voor beide gebouwd, dus het draait ook op een Raspberry Pi 4/5 of een ARM-minipc).
