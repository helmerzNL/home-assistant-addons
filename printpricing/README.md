# 3D Print Pricing: Home Assistant app

*English first · Nederlands hieronder.*

## English

Cost price calculator and inventory for a 3D-print business: filament, parts, printer depreciation and energy. This app brings its own
PostgreSQL database, so nothing else has to be installed.

**Quick start**

1. Install the app and start it. Optionally fill in **rp_id** on the *Configuration* tab first: the domain you will open the app on.
2. Read the setup code in the *Log* tab.
3. Open the app (`https://<your domain>`, or `http://<address of Home Assistant>:6080` without a domain) and go through the onboarding: setup code, your name, a passkey or a password, and the recovery codes.

A password works on any address. Passkeys need an **https** address on a domain name, so for those put a reverse proxy with a certificate in
front of port **6080**. Read the *Documentation* tab before the first start.

## Nederlands

Kostprijscalculator en voorraadbeheer voor een 3D-printbedrijf: filament, onderdelen, afschrijving van de printer en energie. Deze app
brengt een eigen PostgreSQL-database mee, dus er hoeft niets anders geïnstalleerd te worden.

**Snel starten**

1. Installeer de app en start hem. Vul eventueel eerst op het tabblad *Configuratie* **rp_id** in: het domein waarop je de app opent.
2. Lees de instelcode op het tabblad *Logboek*.
3. Open de app (`https://<jouw domein>`, of `http://<adres van Home Assistant>:6080` zonder domein) en doorloop de onboarding: instelcode, je naam, een passkey of een wachtwoord, en de herstelcodes.

Een wachtwoord werkt op elk adres. Passkeys vragen om een **https**-adres op een domeinnaam: zet daarvoor een reverse proxy met certificaat voor
poort **6080**. Lees het tabblad *Documentatie* vóór de eerste start.
