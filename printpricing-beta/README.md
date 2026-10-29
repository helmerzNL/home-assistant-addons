# 3D Print Pricing: Home Assistant app (beta)

*English first · Nederlands hieronder.*

> **Beta.** The development version of the app, built from its `beta` branch. New features and fixes arrive here first and it can be
> unstable. It has its own data folder and port, so it runs next to the stable app. Do not point it at the data of the stable app: a beta can
> change the database in ways the stable version cannot read.
>
> **Bèta.** De ontwikkelversie van de app, gebouwd vanaf de `beta`-branch. Nieuwe functies en fixes komen hier eerst en het kan onstabiel zijn.
> Hij heeft een eigen data-map en poort, dus hij draait naast de stabiele app. Gebruik de data van de stabiele app niet voor de beta: een beta kan
> de database aanpassen op een manier die de stabiele versie niet kan lezen.

## English

Cost price calculator and inventory for a 3D-print business: filament, parts, printer depreciation and energy. Its data is one SQLite file in
the app's folder, so nothing else has to be installed.

**Quick start**

1. Install the app and start it. Optionally fill in **rp_id** on the *Configuration* tab first: the domain you will open the app on.
2. Read the setup code in the *Log* tab.
3. Open the app (`https://<your domain>`, or `http://<address of Home Assistant>:6081` without a domain) and go through the onboarding: setup code, your name, a passkey or a password, and the recovery codes.

A password works on any address. Passkeys need an **https** address on a domain name, so for those put a reverse proxy with a certificate in
front of port **6081**. Read the *Documentation* tab before the first start.

## Nederlands

Kostprijscalculator en voorraadbeheer voor een 3D-printbedrijf: filament, onderdelen, afschrijving van de printer en energie. De gegevens
staan in één SQLite-bestand in de map van de app, dus er hoeft niets anders geïnstalleerd te worden.

**Snel starten**

1. Installeer de app en start hem. Vul eventueel eerst op het tabblad *Configuratie* **rp_id** in: het domein waarop je de app opent.
2. Lees de instelcode op het tabblad *Logboek*.
3. Open de app (`https://<jouw domein>`, of `http://<adres van Home Assistant>:6081` zonder domein) en doorloop de onboarding: instelcode, je naam, een passkey of een wachtwoord, en de herstelcodes.

Een wachtwoord werkt op elk adres. Passkeys vragen om een **https**-adres op een domeinnaam: zet daarvoor een reverse proxy met certificaat voor
poort **6081**. Lees het tabblad *Documentatie* vóór de eerste start.
