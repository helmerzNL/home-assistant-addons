# Doorbell Map: Home Assistant app

*English first · Nederlands hieronder.*

## English

An interactive map of your neighbourhood on which every house is **green**, **red** or **unmarked**: who wants a visit at the door on
St. Martin's Day, Halloween or another door-to-door event, and who does not. Visitors open the map in the browser or as a phone app; the
admin draws the houses and manages everything, protected by a **passkey**.

**Quick start**

1. Install the app and fill in **origin** on the *Configuration* tab: the https address you will open the map on.
2. Start the app and read the setup code in the *Log* tab.
3. Open `<origin>/beheer`, enter the setup code and create your passkey.

Passkeys need an **https** address on a domain name, so put a reverse proxy with a certificate in front of port **9888**. The full
explanation is on the *Documentation* tab.

## Nederlands

Een interactieve kaart van je wijk waarop elk huis **groen**, **rood** of **niet gemarkeerd** is: wie wil er wel of niet dat er wordt
aangebeld met Sint Maarten, Halloween of een andere deur-aan-deur-actie. Bezoekers openen de kaart in de browser of als app op hun
telefoon; de beheerder tekent de huizen en beheert alles, beveiligd met een **passkey**.

**Snel starten**

1. Installeer de app en vul op het tabblad *Configuratie* **origin** in: het https-adres waarop je de kaart opent.
2. Start de app en lees de instelcode op het tabblad *Logboek*.
3. Open `<origin>/beheer`, voer de instelcode in en maak je passkey aan.

Passkeys vragen om een **https**-adres op een domeinnaam: zet dus een reverse proxy met certificaat voor poort **9888**. De volledige uitleg
staat op het tabblad *Documentatie*.
