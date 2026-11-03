# Doorbell Map: Home Assistant app (beta)

*English first · Nederlands hieronder.*

> **Beta.** The development version of the app, built from its `beta` branch. New features and fixes arrive here first and it can be
> unstable. It has its own data folder and port, so it runs next to the stable app. Do not point it at the data of the stable app: a beta can
> change the database in ways the stable version cannot read.
>
> **Bèta.** De ontwikkelversie van de app, gebouwd vanaf de `beta`-branch. Nieuwe functies en fixes komen hier eerst en het kan onstabiel zijn.
> Hij heeft een eigen data-map en poort, dus hij draait naast de stabiele app. Gebruik de data van de stabiele app niet voor de beta: een beta kan
> de database aanpassen op een manier die de stabiele versie niet kan lezen.

## English

An interactive map of your neighbourhood on which every house is **green**, **red** or **unmarked**: who wants a visit at the door on
St. Martin's Day, Halloween or another door-to-door event, and who does not. Visitors open the map in the browser or as a phone app; the
admin draws the houses and manages everything, protected by a **password** or a **passkey**.

**Quick start**

1. Install and start the app, and read the setup code in the *Log* tab.
2. Open the app with **Open web UI** (`http://<address of Home Assistant>:9889`) or at your https address, and go to `/beheer`.
3. Enter the setup code, choose a username and a password (or, over https, a passkey).

Passkeys need an **https** address on a domain name: put a reverse proxy with a certificate in front of port **9889** and you can add one
later. The full explanation is on the *Documentation* tab.

## Nederlands

Een interactieve kaart van je wijk waarop elk huis **groen**, **rood** of **niet gemarkeerd** is: wie wil er wel of niet dat er wordt
aangebeld met Sint Maarten, Halloween of een andere deur-aan-deur-actie. Bezoekers openen de kaart in de browser of als app op hun
telefoon; de beheerder tekent de huizen en beheert alles, beveiligd met een **wachtwoord** of een **passkey**.

**Snel starten**

1. Installeer en start de app en lees de instelcode op het tabblad *Logboek*.
2. Open de app met **Webinterface openen** (`http://<adres van Home Assistant>:9889`) of op je https-adres, en ga naar `/beheer`.
3. Voer de instelcode in en kies een gebruikersnaam en een wachtwoord (of, via https, een passkey).

Passkeys vragen om een **https**-adres op een domeinnaam: zet een reverse proxy met certificaat voor poort **9889**, dan kun je er later een
toevoegen. De volledige uitleg staat op het tabblad *Documentatie*.
