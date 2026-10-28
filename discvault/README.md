# DiscVault: Home Assistant app

*English first · Nederlands hieronder.*

## English

DiscVault is a self-hosted manager for your physical **4K UHD, Blu-ray and DVD** collection: barcode scanning, metadata lookup, posters,
watchlist, users and groups, passkey sign-in, backup and restore, and an MCP endpoint for AI assistants. This app brings its own
PostgreSQL database, so nothing else has to be installed.

**Quick start**

1. Install the app and, on the *Configuration* tab, either fill in **rp_id** (the domain you will open DiscVault on) or turn on **password_login**.
2. Start the app (the first start takes a minute) and open it at `https://<your domain>`, or at `http://<ip>:6180` with password login.
3. Go through the onboarding and create your passkey, or your username, password and authenticator app.

Passkeys need an **https** address on a domain name, so put a reverse proxy with a certificate in front of port **6180**. Password login
works without. The full explanation is on the *Documentation* tab.

## Nederlands

DiscVault is een zelf te hosten beheerder voor je fysieke **4K UHD-, Blu-ray- en dvd-collectie**: barcodes scannen, metadata opzoeken,
posters, kijklijst, gebruikers en groepen, inloggen met passkeys, back-up en terugzetten, en een MCP-eindpunt voor AI-assistenten. Deze app
brengt een eigen PostgreSQL-database mee, dus er hoeft niets anders geïnstalleerd te worden.

**Snel starten**

1. Installeer de app en vul op het tabblad *Configuratie* **rp_id** in (het domein waarop je DiscVault opent) of zet **password_login** aan.
2. Start de app (de eerste start duurt een minuutje) en open hem op `https://<jouw domein>`, of met wachtwoord-inloggen op `http://<ip>:6180`.
3. Doorloop de onboarding en maak je passkey aan, of je gebruikersnaam, wachtwoord en authenticator-app.

Passkeys vragen om een **https**-adres op een domeinnaam: zet dus een reverse proxy met certificaat voor poort **6180**. Wachtwoord-inloggen
werkt ook zonder. De volledige uitleg staat op het tabblad *Documentatie*.
