# HaspelSync: Home Assistant app (beta)

*English first · Nederlands hieronder.*

> **Beta.** The development version of the app, built from its `main` branch. New features and fixes arrive here first and it can be
> unstable. It has its own data folder and port, so it runs next to the stable app. Do not point it at the data of the stable app: a beta can
> change the database in ways the stable version cannot read.
>
> **Bèta.** De ontwikkelversie van de app, gebouwd vanaf de `main`-branch. Nieuwe functies en fixes komen hier eerst en het kan onstabiel zijn.
> Hij heeft een eigen data-map en poort, dus hij draait naast de stabiele app. Gebruik de data van de stabiele app niet voor de beta: een beta kan
> de database aanpassen op een manier die de stabiele versie niet kan lezen.

## English

Keeps [Spoolman](https://github.com/Donkie/Spoolman) in step with the AMS of your Bambu Lab printers: it sees which spool sits in which slot, and
books what every print actually used on that spool. HaspelSync is made by [Rdiger-36](https://github.com/Rdiger-36/HaspelSync); this app only
packages it for Home Assistant.

**Quick start**

1. Make sure Spoolman runs, for example the **Spoolman** app from this repository.
2. Install this app, start it and open it with **Open web UI** (`http://<address of Home Assistant>:4001`).
3. Under **Settings** enter the Spoolman endpoint (`http://<address of Home Assistant>:7912` for the Spoolman app) and set a password.
4. Under **Printers** add each printer with its serial number, IP address and access code.

Read the *Documentation* tab first: the printer has to be reachable on ports 8883 and 990, and some models need a USB stick.

## Nederlands

Houdt [Spoolman](https://github.com/Donkie/Spoolman) gelijk met de AMS van je Bambu Lab-printers: hij ziet welke spoel in welk vak zit, en boekt
wat elke print echt gebruikte op die spoel. HaspelSync is gemaakt door [Rdiger-36](https://github.com/Rdiger-36/HaspelSync); deze app verpakt hem
alleen voor Home Assistant.

**Snel starten**

1. Zorg dat Spoolman draait, bijvoorbeeld de app **Spoolman** uit deze repository.
2. Installeer deze app, start hem en open hem met **Webinterface openen** (`http://<adres van Home Assistant>:4001`).
3. Vul onder **Settings** het Spoolman-endpoint in (`http://<adres van Home Assistant>:7912` voor de Spoolman-app) en stel een wachtwoord in.
4. Voeg onder **Printers** elke printer toe met zijn serienummer, IP-adres en toegangscode.

Lees eerst het tabblad *Documentatie*: de printer moet bereikbaar zijn op poort 8883 en 990, en sommige modellen hebben een USB-stick nodig.
