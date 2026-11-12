# Spoolman: Home Assistant app (beta)

*English first · Nederlands hieronder.*

> **Beta.** The development version of the app, built from its `master` branch. New features and fixes arrive here first and it can be
> unstable. It has its own data folder and port, so it runs next to the stable app. Do not point it at the data of the stable app: a beta can
> change the database in ways the stable version cannot read.
>
> **Bèta.** De ontwikkelversie van de app, gebouwd vanaf de `master`-branch. Nieuwe functies en fixes komen hier eerst en het kan onstabiel zijn.
> Hij heeft een eigen data-map en poort, dus hij draait naast de stabiele app. Gebruik de data van de stabiele app niet voor de beta: een beta kan
> de database aanpassen op een manier die de stabiele versie niet kan lezen.

## English

Keep track of your 3D-printer filament spools: what you have, where it is, how much is left and what every print used. Its data is one SQLite
file in the app's folder, so nothing else has to be installed. Spoolman is made by [Donkie](https://github.com/Donkie/Spoolman); this app only
packages it for Home Assistant.

**Quick start**

1. Install the app and start it.
2. Open it with **Open web UI** (`http://<address of Home Assistant>:7913`) and add your first filament and spool, or pick them from SpoolmanDB.
3. Point the tools that book usage at the same address: HaspelSync for a Bambu Lab printer, Klipper/Moonraker, OctoPrint, or 3D Print Pricing.

Spoolman has **no login of its own**: everybody who can reach port **7913** can change your inventory. Keep it on your home network and read the
*Documentation* tab before the first start.

## Nederlands

Houd je filamentspoelen voor de 3D-printer bij: wat je hebt, waar het ligt, hoeveel er nog op zit en wat elke print gebruikte. De gegevens
staan in één SQLite-bestand in de map van de app, dus er hoeft niets anders geïnstalleerd te worden. Spoolman is gemaakt door
[Donkie](https://github.com/Donkie/Spoolman); deze app verpakt hem alleen voor Home Assistant.

**Snel starten**

1. Installeer de app en start hem.
2. Open hem met **Webinterface openen** (`http://<adres van Home Assistant>:7913`) en voeg je eerste filament en spoel toe, of kies ze uit SpoolmanDB.
3. Laat de programma's die verbruik boeken naar hetzelfde adres wijzen: HaspelSync voor een Bambu Lab-printer, Klipper/Moonraker, OctoPrint of 3D Print Pricing.

Spoolman heeft **geen eigen inlog**: iedereen die poort **7913** kan bereiken, kan je voorraad aanpassen. Houd hem op je thuisnetwerk en lees het
tabblad *Documentatie* vóór de eerste start.
