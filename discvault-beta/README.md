# DiscVault: Home Assistant app (beta)

*English first · Nederlands hieronder.*

> **Beta.** The development version of the app, built from its `beta` branch. New features and fixes arrive here first and it can be
> unstable. It has its own data folder and port, so it runs next to the stable app. Do not point it at the data of the stable app: a beta can
> change the database in ways the stable version cannot read.
>
> **Bèta.** De ontwikkelversie van de app, gebouwd vanaf de `beta`-branch. Nieuwe functies en fixes komen hier eerst en het kan onstabiel zijn.
> Hij heeft een eigen data-map en poort, dus hij draait naast de stabiele app. Gebruik de data van de stabiele app niet voor de beta: een beta kan
> de database aanpassen op een manier die de stabiele versie niet kan lezen.

## English

DiscVault is a self-hosted manager for your physical **4K UHD, Blu-ray and DVD** collection: barcode scanning, metadata lookup, posters,
watchlist, users and groups, passkey sign-in, backup and restore, and an MCP endpoint for AI assistants. This app brings its own
PostgreSQL database, so nothing else has to be installed.

**Quick start**

1. Install the app and fill in **rp_id** on the *Configuration* tab: the domain you will open DiscVault on.
2. Start the app (the first start takes a minute) and open it at `https://<your domain>`.
3. Go through the onboarding and create your passkey.

Passkeys need an **https** address on a domain name, so put a reverse proxy with a certificate in front of port **6181**. The full
explanation is on the *Documentation* tab.

## Nederlands

DiscVault is een zelf te hosten beheerder voor je fysieke **4K UHD-, Blu-ray- en dvd-collectie**: barcodes scannen, metadata opzoeken,
posters, kijklijst, gebruikers en groepen, inloggen met passkeys, back-up en terugzetten, en een MCP-eindpunt voor AI-assistenten. Deze app
brengt een eigen PostgreSQL-database mee, dus er hoeft niets anders geïnstalleerd te worden.

**Snel starten**

1. Installeer de app en vul op het tabblad *Configuratie* **rp_id** in: het domein waarop je DiscVault opent.
2. Start de app (de eerste start duurt een minuutje) en open hem op `https://<jouw domein>`.
3. Doorloop de onboarding en maak je passkey aan.

Passkeys vragen om een **https**-adres op een domeinnaam: zet dus een reverse proxy met certificaat voor poort **6181**. De volledige uitleg
staat op het tabblad *Documentatie*.
