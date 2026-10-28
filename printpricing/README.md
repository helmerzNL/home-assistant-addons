# 3D Print Pricing: Home Assistant app

*English first · Nederlands hieronder.*

## English

Cost price calculator and inventory for a 3D-print business: filament, parts, printer depreciation and energy. This app brings its own
PostgreSQL database, so nothing else has to be installed.

**Quick start**

1. Install the app and fill in **rp_id** on the *Configuration* tab: the domain you will open the app on.
2. Start the app and read the setup code in the *Log* tab.
3. Open `https://<your domain>` and go through the onboarding: setup code, your name, a passkey and the recovery codes.

Passkeys need an **https** address on a domain name, so put a reverse proxy with a certificate in front of port **6080**. Read the
*Documentation* tab before the first start.

## Nederlands

Kostprijscalculator en voorraadbeheer voor een 3D-printbedrijf: filament, onderdelen, afschrijving van de printer en energie. Deze app
brengt een eigen PostgreSQL-database mee, dus er hoeft niets anders geïnstalleerd te worden.

**Snel starten**

1. Installeer de app en vul op het tabblad *Configuratie* **rp_id** in: het domein waarop je de app opent.
2. Start de app en lees de instelcode op het tabblad *Logboek*.
3. Open `https://<jouw domein>` en doorloop de onboarding: instelcode, je naam, een passkey en de herstelcodes.

Passkeys vragen om een **https**-adres op een domeinnaam: zet dus een reverse proxy met certificaat voor poort **6080**. Lees het tabblad
*Documentatie* vóór de eerste start.
