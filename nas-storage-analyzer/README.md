# NAS Storage Analyzer: Home Assistant app

*English first · Nederlands hieronder.*

## English

See how much space your data uses, per share, folder and file type, and find what you can clean up. The app scans **read-only**: the
folders of Home Assistant (`share`, `media`, and network storage you added to Home Assistant), or NFS and SMB servers it mounts itself. It
never reads the contents of a file and never changes anything on a share. The database (PostgreSQL) runs inside the app.

**Quick start**

1. Install and start the app, and read the setup token in the *Log* tab (look for `setup_token`).
2. Open the app with **Open web UI** (`http://<address of Home Assistant>:6480`).
3. Enter the setup token, create the administrator with a password, and set up an authenticator app (or, over https, a passkey).
4. Add a share (**Shares → Add share**, for example `/mnt/shares/media`) and click **Scan now** on the dashboard.

The app needs extra rights to mount NFS and SMB shares itself; the *Documentation* tab says which and why.

## Nederlands

Zie hoeveel ruimte je data inneemt, per share, map en bestandstype, en vind wat je kunt opruimen. De app scant **alleen-lezen**: de mappen
van Home Assistant (`share`, `media` en netwerkopslag die je aan Home Assistant hebt toegevoegd), of NFS- en SMB-servers die hij zelf mount.
Hij leest nooit de inhoud van een bestand en verandert nooit iets op een share. De database (PostgreSQL) draait in de app.

**Snel starten**

1. Installeer en start de app en lees de setup-token op het tabblad *Logboek* (zoek `setup_token`).
2. Open de app met **Webinterface openen** (`http://<adres van Home Assistant>:6480`).
3. Voer de setup-token in, maak de beheerder met een wachtwoord en stel een authenticator-app in (of, via https, een passkey).
4. Voeg een share toe (**Shares → Share toevoegen**, bijvoorbeeld `/mnt/shares/media`) en klik op **Scan nu** op het dashboard.

De app heeft extra rechten nodig om zelf NFS- en SMB-shares te mounten; het tabblad *Documentatie* zegt welke en waarom.
