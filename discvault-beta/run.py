#!/usr/bin/env python3
"""Start DiscVault inside a Home Assistant app: PostgreSQL first, then the image's own supervisord (API with migrations, worker, MCP).

Home Assistant runs one container per app, and DiscVault needs PostgreSQL, so this container holds both. /data is the data folder of
DiscVault: the database in /data/postgres, the posters, profiles and backups next to it. The options of the app (/data/options.json)
become the variables of the .env file of the Docker installation; the secrets that .env would hold are made once and kept in
/data/secrets.json. If either process stops, the other is stopped and this exits non-zero, so the Supervisor's watchdog restarts the app.
"""
import glob
import json
import os
import secrets
import signal
import subprocess
import sys
import time
from pathlib import Path

DATA = Path(os.environ.get("DATA_PATH", "/data"))
OPTIONS = Path(os.environ.get("OPTIONS_FILE", DATA / "options.json"))
SECRETS = DATA / "secrets.json"
PGDATA = DATA / "postgres"
PGSOCKET = Path(os.environ.get("PG_SOCKET_DIR", "/run/postgresql"))
PGPORT = "5432"
DB_NAME = DB_USER = "discvault"
APP_COMMAND = os.environ.get("APP_COMMAND", "/usr/bin/supervisord -c /etc/supervisor/conf.d/discvault-v26.conf").split()
PG_USER = os.environ.get("PG_RUN_USER", "postgres")
PG_START_SECONDS = 180          # after a hard stop PostgreSQL replays its log before it answers
APP_STOP_SECONDS = 25
PG_STOP_SECONDS = 25
DATA_FOLDERS = ("posters", "profiles", "backups", "avatars")


def log(message: str) -> None:
    print(f"[discvault] {message}", flush=True)


def fail(message: str) -> "None":
    print(f"[discvault] ERROR: {message}", file=sys.stderr, flush=True)
    raise SystemExit(1)


def read_options() -> dict:
    try:
        return json.loads(OPTIONS.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}


def settings(options: dict, kept: dict) -> dict:
    """The environment of the app, from the options and the kept secrets. Stops with a readable message when neither a domain nor password login is set."""
    rp_id = str(options.get("rp_id") or "").strip().lower()
    if "://" in rp_id or "/" in rp_id or ":" in rp_id:
        fail("rp_id must be a domain name only, without https://, a path or a port (for example vault.example.com).")
    origins = str(options.get("rp_origins") or "").strip() or (f"https://{rp_id}" if rp_id else "")
    password_login = bool(options.get("password_login", False))
    if not password_login and (not rp_id or not origins):
        fail("Set rp_id (the domain DiscVault is opened on, for example vault.example.com) on the Configuration tab of this app, then start it again. "
             "Passkeys are bound to that domain and only work over https (see the Documentation tab). "
             "Or turn on password_login to sign in with a username and password instead.")
    env = {
        "DATABASE_URL": f"postgresql://{DB_USER}:{kept['postgres_password']}@127.0.0.1:{PGPORT}/{DB_NAME}",
        "JWT_SECRET": kept["jwt_secret"],
        "RP_NAME": str(options.get("rp_name") or "").strip() or "DiscVault",
        "LEGACY_AUTH_ENABLED": "true" if password_login else "false",
        "DISCVAULT_LEGACY_DATA_DIR": str(DATA),
        "DISCVAULT_DATA_DIR": str(DATA),
        "DISCVAULT_BLOCK_CRAWLERS": "true" if options.get("block_crawlers", True) else "false",
    }
    # Without a domain the app finds no valid passkey set-up and offers the password onboarding only.
    if rp_id:
        env["RP_ID"] = rp_id
    if origins:
        env["RP_ORIGINS"] = origins
    for option, variable in (("trusted_proxies", "DISCVAULT_TRUSTED_PROXIES"), ("omdb_api_key", "OMDB_API_KEY"), ("tmdb_api_key", "TMDB_API_KEY")):
        value = str(options.get(option) or "").strip()
        if value:
            env[variable] = value
    return env


def kept_secrets() -> dict:
    """Secrets that .env would hold, made on the first start and kept, so sessions and the database login survive a restart.

    JWT_SECRET also encrypts the connection keys stored in the database (DiscVault falls back to it), so it must never change."""
    kept = {}
    if SECRETS.exists():
        kept = json.loads(SECRETS.read_text(encoding="utf-8"))
    changed = False
    for name, make in (("postgres_password", lambda: secrets.token_hex(16)), ("jwt_secret", lambda: secrets.token_urlsafe(48))):
        if not kept.get(name):
            kept[name], changed = make(), True
    if changed:
        DATA.mkdir(parents=True, exist_ok=True)
        tmp = SECRETS.with_suffix(".tmp")
        tmp.write_text(json.dumps(kept, indent=2), encoding="utf-8")
        tmp.chmod(0o600)
        tmp.replace(SECRETS)
    return kept


# --- PostgreSQL ---------------------------------------------------------------------------------------------------------------

def pg_bin() -> Path:
    if os.environ.get("PG_BIN"):
        return Path(os.environ["PG_BIN"])
    found = sorted(glob.glob("/usr/lib/postgresql/*/bin"), key=lambda p: int(Path(p).parent.name))
    if not found:
        fail("PostgreSQL is not installed in this image.")
    return Path(found[-1])


def as_pg(command: list) -> list:
    """Run a command as the postgres user (PostgreSQL refuses to run as root); a test that is not root runs it as itself."""
    if os.geteuid() != 0:
        return command
    return ["setpriv", f"--reuid={PG_USER}", f"--regid={PG_USER}", "--init-groups", *command]


def chown_pg(path: Path) -> None:
    if os.geteuid() == 0:
        import pwd
        entry = pwd.getpwnam(PG_USER)
        os.chown(path, entry.pw_uid, entry.pw_gid)


def prepare_cluster(binary: Path) -> None:
    PGSOCKET.mkdir(parents=True, exist_ok=True)
    chown_pg(PGSOCKET)
    PGDATA.mkdir(parents=True, exist_ok=True)
    chown_pg(PGDATA)
    PGDATA.chmod(0o700)
    version_file = PGDATA / "PG_VERSION"
    if version_file.exists():
        have, want = version_file.read_text().strip().split(".")[0], binary.parent.name
        if have != want:
            fail(f"The database in /data/postgres was made by PostgreSQL {have}, this app runs {want}, and a data folder cannot be opened by "
                 f"another major version. Restore a backup of DiscVault into a fresh installation instead.")
        return
    log("Creating the database cluster (first start).")
    subprocess.run(as_pg([str(binary / "initdb"), "-D", str(PGDATA), "--encoding=UTF8", "--locale=C.UTF-8", "--username=postgres",
                          "--auth-local=trust", "--auth-host=scram-sha-256"]), check=True, stdout=subprocess.DEVNULL)


def start_postgres(binary: Path) -> subprocess.Popen:
    log("Starting PostgreSQL.")
    return subprocess.Popen(as_pg([str(binary / "postgres"), "-D", str(PGDATA), "-c", "listen_addresses=127.0.0.1", "-c", f"port={PGPORT}",
                                   "-c", f"unix_socket_directories={PGSOCKET}", "-c", "max_connections=60"]))


def psql(binary: Path, sql: str, database: str = "postgres") -> str:
    done = subprocess.run(as_pg([str(binary / "psql"), "-h", str(PGSOCKET), "-p", PGPORT, "-U", "postgres", "-d", database, "-X", "-A", "-t",
                                 "-v", "ON_ERROR_STOP=1", "-c", sql]), capture_output=True, text=True)
    if done.returncode != 0:
        fail(f"PostgreSQL refused a set-up statement: {done.stderr.strip()}")
    return done.stdout.strip()


def wait_ready(binary: Path, postgres: subprocess.Popen) -> None:
    deadline = time.monotonic() + PG_START_SECONDS
    while time.monotonic() < deadline:
        if postgres.poll() is not None:
            fail("PostgreSQL stopped while starting; see the lines above.")
        ready = subprocess.run(as_pg([str(binary / "pg_isready"), "-h", str(PGSOCKET), "-p", PGPORT, "-q"]))
        if ready.returncode == 0:
            return
        time.sleep(1)
    fail(f"PostgreSQL did not accept connections within {PG_START_SECONDS} seconds.")


def ensure_database(binary: Path, password: str) -> None:
    """The login and the database of the app; the password is rewritten at every start so it always matches secrets.json. The password is hex."""
    if not psql(binary, f"SELECT 1 FROM pg_roles WHERE rolname = '{DB_USER}'"):
        psql(binary, f"CREATE ROLE {DB_USER} LOGIN")
    psql(binary, f"ALTER ROLE {DB_USER} PASSWORD '{password}'")
    if not psql(binary, f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'"):
        psql(binary, f"CREATE DATABASE {DB_NAME} OWNER {DB_USER}")


# --- the processes ------------------------------------------------------------------------------------------------------------

def stop(process: subprocess.Popen, signum: int, seconds: int, name: str) -> None:
    if process.poll() is not None:
        return
    process.send_signal(signum)
    try:
        process.wait(timeout=seconds)
    except subprocess.TimeoutExpired:
        log(f"{name} did not stop in {seconds} seconds; killing it.")
        process.kill()
        process.wait()


def main() -> int:
    options = read_options()
    kept = kept_secrets()
    env = settings(options, kept)
    binary = pg_bin()

    for folder in DATA_FOLDERS:
        (DATA / folder).mkdir(parents=True, exist_ok=True)
    prepare_cluster(binary)
    postgres = start_postgres(binary)
    app = None
    stopping = []

    def on_signal(signum, _frame):
        stopping.append(signum)

    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)
    try:
        wait_ready(binary, postgres)
        ensure_database(binary, kept["postgres_password"])
        log("Starting DiscVault (the first start applies all database migrations, which takes a minute).")
        app = subprocess.Popen(APP_COMMAND, env={**os.environ, **env})
        while not stopping and postgres.poll() is None and app.poll() is None:
            time.sleep(0.5)
        if stopping:
            log("Stopping.")
            code = 0
        else:
            log("A process stopped by itself; stopping the other one so the app is restarted.")
            code = 1
    finally:
        if app is not None:
            stop(app, signal.SIGTERM, APP_STOP_SECONDS, "DiscVault")
        stop(postgres, signal.SIGINT, PG_STOP_SECONDS, "PostgreSQL")        # SIGINT is a fast shutdown: it does not wait for open connections
    return code


if __name__ == "__main__":
    raise SystemExit(main())
