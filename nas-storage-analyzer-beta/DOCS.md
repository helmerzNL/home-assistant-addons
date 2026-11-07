# NAS Storage Analyzer (beta)

*English first · Nederlands hieronder.*

> **Beta.** The development version of the app, built from its `beta` branch. New features and fixes arrive here first and it can be
> unstable. It has its own data folder and port, so it runs next to the stable app. Do not point it at the data of the stable app: a beta can
> change the database in ways the stable version cannot read.
>
> **Bèta.** De ontwikkelversie van de app, gebouwd vanaf de `beta`-branch. Nieuwe functies en fixes komen hier eerst en het kan onstabiel zijn.
> Hij heeft een eigen data-map en poort, dus hij draait naast de stabiele app. Gebruik de data van de stabiele app niet voor de beta: een beta kan
> de database aanpassen op een manier die de stabiele versie niet kan lezen.

## English

NAS Storage Analyzer scans shares **read-only** and shows how much space the data uses per share, folder and file type: a dashboard
with growth over time, a treemap, and lists of the largest and the longest-unused files and folders. It only lists folders and reads file
sizes and dates; it never opens a file and never writes to a share. To clean up, it writes a delete script that you run yourself. This app runs the all-in-one image of the app: the web interface, the scan worker and
the PostgreSQL database in one container.

### Install

1. Add this repository to Home Assistant (see its README) and choose **NAS Storage Analyzer** in the app store; click **Install**.
2. Start the app. On the first start it makes its database and an encryption key; the *Log* tab shows a line with `setup_token`.
3. Click **Open web UI**, or go to `http://<address of Home Assistant>:6481`.
4. Enter the setup token and create the administrator: a username, a password, and a second factor. The second factor is mandatory:
   an authenticator app (you get recovery codes, shown once) or a passkey.
5. Choose **Shares → Add share**, pick a folder with **Browse…**, and click **Scan now** on the dashboard.

### Signing in, password or passkey

A password with an authenticator-app code works on any address, also `http://homeassistant.local:6481`. A **passkey** only works on
an https address with a domain name: put a reverse proxy with a certificate in front of port 6481, and set the options `rp_id` and
`rp_origins` (and `trusted_proxies` for the proxy). The app has no ingress: it refuses to be shown inside another page, so it opens in
its own tab.

### What it can scan

- **Folders of Home Assistant.** `share` and `media` are mapped read-only as `/mnt/shares/share` and `/mnt/shares/media`. Network
  storage you add under **Settings > System > Storage** (usage *Media* or *Share*) appears inside them. Add a share of type
  *Mounted path* and click **Browse…** to pick a folder.
- **An NFS or SMB server directly.** Add a share of type *NFS* or *SMB* with the server, the export or share name and, for SMB, a
  username and password (stored encrypted). The worker mounts it read-only for the scan and unmounts it afterwards. This route works
  in the app but has not been tested against every NAS; NFSv4 or SMB is the safest choice.

### Rights the app asks for

To mount NFS and SMB shares itself, the worker needs the Linux capability **`SYS_ADMIN`**, and the default AppArmor profile, which forbids
mounting, is switched off (`apparmor: false`). SMB also needs **`DAC_READ_SEARCH`**: the SMB mount helper (`mount.cifs`) asks for it at
start-up and stops without it, so with `SYS_ADMIN` alone only NFS would work. These rights lower the security rating Home Assistant shows
for the app. The web interface and the database run as their own users without those rights; only the scan worker runs as root. The folders
of Home Assistant are mapped read-only, and every mount is read-only too.

### Options

| Option | What it does |
|---|---|
| `setup_token` | Typed once to create the first administrator. Empty makes one and prints it in the log. |
| `public_url` | The address others use, for the invitation links. Optional. |
| `rp_id`, `rp_origins` | Only for passkeys: the domain name, and the full https address(es). Set both or neither. |
| `trusted_proxies` | IP addresses or ranges of a reverse proxy in front of the app. |
| `worker_parallel` | How many scans run at once (1 to 8, default 2). |
| `update_check` | Tell the administrator about a newer release. Home Assistant shows app updates itself. |
| `encryption_key` | Leave empty. Only to move an installation: the key it used there. |

### Data, backups and moving

Everything is in the data folder of the app: the database in `/data/postgres` and the encryption key in `/data/encryption.key`. The key
seals the stored SMB passwords. It is part of the backups of this app, which Home Assistant encrypts; without it, the stored SMB passwords
cannot be read. The app is stopped during a backup (a running database is not a consistent file copy), so a backup interrupts a running scan.

The app also has its own backup (**Settings → Backup**): a small file with your shares, file types and preferences, without passwords or
scan results. It is the way to move between this app and a Docker installation. To move the whole database instead, copy `/data/postgres`
of a stopped installation, and set the option `encryption_key` to the key of that installation.

### Updating

Home Assistant offers an update when a new version of the app is released, and makes a backup of the app first if you let it. A release
can change the database; a newer database may not run on an older version, so keep that backup until the new version works.

## Nederlands

NAS Storage Analyzer scant shares **alleen-lezen** en laat zien hoeveel ruimte de data inneemt per share, map en bestandstype: een dashboard
met de groei in de tijd, een treemap, en lijsten van de grootste en de langst ongebruikte bestanden en mappen. Hij leest alleen mappen en de
grootte en datums van bestanden; hij opent nooit een bestand en schrijft nooit naar een share. Om op te ruimen schrijft hij een
verwijderscript dat je zelf draait. Deze app draait het all-in-one image van de app: de
webinterface, de scan-worker en de PostgreSQL-database in één container.

### Installeren

1. Voeg deze repository toe aan Home Assistant (zie de README) en kies **NAS Storage Analyzer** in de app-store; klik op **Installeren**.
2. Start de app. Bij de eerste start maakt hij zijn database en een encryptiesleutel; op het tabblad *Logboek* staat een regel met
   `setup_token`.
3. Klik op **Webinterface openen**, of ga naar `http://<adres van Home Assistant>:6481`.
4. Voer de setup-token in en maak de beheerder: een gebruikersnaam, een wachtwoord en een tweede factor. De tweede factor is verplicht:
   een authenticator-app (je krijgt herstelcodes, één keer getoond) of een passkey.
5. Kies **Shares → Share toevoegen**, kies een map met **Bladeren…** en klik op **Scan nu** op het dashboard.

### Inloggen: wachtwoord of passkey

Een wachtwoord met een code uit een authenticator-app werkt op elk adres, ook `http://homeassistant.local:6481`. Een **passkey** werkt
alleen op een https-adres met een domeinnaam: zet een reverse proxy met certificaat voor poort 6481 en vul de opties `rp_id` en
`rp_origins` in (en `trusted_proxies` voor de proxy). De app heeft geen ingress: hij weigert in een andere pagina te worden getoond en opent
dus in een eigen tabblad.

### Wat hij kan scannen

- **Mappen van Home Assistant.** `share` en `media` zijn alleen-lezen gekoppeld als `/mnt/shares/share` en `/mnt/shares/media`.
  Netwerkopslag die je toevoegt onder **Instellingen > Systeem > Opslag** (gebruik *Media* of *Share*) verschijnt daarin. Voeg een share
  toe van het type *Gemount pad* en klik op **Bladeren…** om een map te kiezen.
- **Rechtstreeks een NFS- of SMB-server.** Voeg een share toe van het type *NFS* of *SMB* met de server, de export of sharenaam en, voor
  SMB, een gebruikersnaam en wachtwoord (versleuteld opgeslagen). De worker mount hem alleen-lezen voor de scan en ontkoppelt hem daarna.
  Deze route werkt in de app maar is niet tegen elke NAS getest; NFSv4 of SMB is de veiligste keuze.

### Rechten die de app vraagt

Om zelf NFS- en SMB-shares te mounten heeft de worker de Linux-capability **`SYS_ADMIN`** nodig, en het standaard AppArmor-profiel, dat
mounten verbiedt, staat uit (`apparmor: false`). SMB heeft daarnaast **`DAC_READ_SEARCH`** nodig: het SMB-mounthulpje (`mount.cifs`) vraagt
die bij het starten en stopt zonder, dus met alleen `SYS_ADMIN` zou alleen NFS werken. Door die rechten geeft Home Assistant de app een
lagere beveiligingsscore. De webinterface en de database draaien als eigen gebruikers zonder die rechten; alleen de scan-worker draait als
root. De mappen van Home Assistant zijn alleen-lezen gekoppeld, en elke mount is ook alleen-lezen.

### Opties

| Optie | Wat het doet |
|---|---|
| `setup_token` | Eén keer ingetypt om de eerste beheerder te maken. Leeg maakt er een en zet hem in het logboek. |
| `public_url` | Het adres dat anderen gebruiken, voor de uitnodigingslinks. Optioneel. |
| `rp_id`, `rp_origins` | Alleen voor passkeys: de domeinnaam, en de volledige https-adressen. Vul beide in of geen van beide. |
| `trusted_proxies` | IP-adressen of reeksen van een reverse proxy voor de app. |
| `worker_parallel` | Hoeveel scans tegelijk lopen (1 tot 8, standaard 2). |
| `update_check` | De beheerder melden dat er een nieuwere release is. Home Assistant toont updates van apps zelf. |
| `encryption_key` | Laat leeg. Alleen om een installatie te verhuizen: de sleutel die daar werd gebruikt. |

### Data, back-ups en verhuizen

Alles staat in de data-map van de app: de database in `/data/postgres` en de encryptiesleutel in `/data/encryption.key`. De sleutel
versleutelt de opgeslagen SMB-wachtwoorden. Hij zit in de back-ups van deze app, die Home Assistant versleutelt; zonder sleutel zijn de
opgeslagen SMB-wachtwoorden niet meer te lezen. Tijdens een back-up staat de app stil (een draaiende database is geen consistente kopie),
dus een back-up onderbreekt een lopende scan.

De app heeft ook een eigen back-up (**Instellingen → Back-up**): een klein bestand met je shares, bestandstypen en voorkeuren, zonder
wachtwoorden en zonder scanresultaten. Daarmee verhuis je tussen deze app en een Docker-installatie. Wil je de hele database verhuizen,
kopieer dan `/data/postgres` van een gestopte installatie en vul de optie `encryption_key` in met de sleutel van die installatie.

### Updaten

Home Assistant biedt een update aan zodra er een nieuwe versie van de app is, en maakt eerst een back-up van de app als je dat toestaat.
Een release kan de database aanpassen; een nieuwere database draait misschien niet op een oudere versie, dus bewaar die back-up tot de nieuwe
versie werkt.
