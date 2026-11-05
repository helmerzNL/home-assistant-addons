# NAS Storage Analyzer: Home Assistant app (beta)

*English first · Nederlands hieronder.*

> **Beta.** The development version of the app, built from its `beta` branch. New features and fixes arrive here first and it can be
> unstable. It has its own data folder and port, so it runs next to the stable app. Do not point it at the data of the stable app: a beta can
> change the database in ways the stable version cannot read.
>
> **Bèta.** De ontwikkelversie van de app, gebouwd vanaf de `beta`-branch. Nieuwe functies en fixes komen hier eerst en het kan onstabiel zijn.
> Hij heeft een eigen data-map en poort, dus hij draait naast de stabiele app. Gebruik de data van de stabiele app niet voor de beta: een beta kan
> de database aanpassen op een manier die de stabiele versie niet kan lezen.

## English

See how much space your data uses, per share, folder and file type, and find what you can clean up. The app scans **read-only**: the
folders of Home Assistant (`share`, `media`, and network storage you added to Home Assistant), or NFS and SMB servers it mounts itself. It
never reads the contents of a file and never changes anything on a share. The database (PostgreSQL) runs inside the app.

**Quick start**

1. Install and start the app, and read the setup token in the *Log* tab (look for `setup_token`).
2. Open the app with **Open web UI** (`http://<address of Home Assistant>:6481`).
3. Enter the setup token, create the administrator with a password, and set up an authenticator app (or, over https, a passkey).
4. Add a share (**Shares → Add share**, for example `/mnt/shares/media`) and click **Scan now** on the dashboard.

The app needs extra rights to mount NFS and SMB shares itself; the *Documentation* tab says which and why.

## Nederlands

Zie hoeveel ruimte je data inneemt, per share, map en bestandstype, en vind wat je kunt opruimen. De app scant **alleen-lezen**: de mappen
van Home Assistant (`share`, `media` en netwerkopslag die je aan Home Assistant hebt toegevoegd), of NFS- en SMB-servers die hij zelf mount.
Hij leest nooit de inhoud van een bestand en verandert nooit iets op een share. De database (PostgreSQL) draait in de app.

**Snel starten**

1. Installeer en start de app en lees de setup-token op het tabblad *Logboek* (zoek `setup_token`).
2. Open de app met **Webinterface openen** (`http://<adres van Home Assistant>:6481`).
3. Voer de setup-token in, maak de beheerder met een wachtwoord en stel een authenticator-app in (of, via https, een passkey).
4. Voeg een share toe (**Shares → Share toevoegen**, bijvoorbeeld `/mnt/shares/media`) en klik op **Scan nu** op het dashboard.

De app heeft extra rechten nodig om zelf NFS- en SMB-shares te mounten; het tabblad *Documentatie* zegt welke en waarom.
