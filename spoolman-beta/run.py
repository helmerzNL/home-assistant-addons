#!/usr/bin/env python3
"""Start Spoolman inside a Home Assistant app.

The options of the app (/data/options.json) become Spoolman's own variables (SPOOLMAN_*), and everything it keeps (the SQLite database spoolman.db,
its automatic backups and its logs) lives in /data/spoolman, the app's own folder that Home Assistant includes in its backups. The image's
entrypoint runs the app as its user `app` (uid 1000) and drops root, while Home Assistant creates /data for root, so that folder is handed to the
app's user first. Then this process becomes the image's entrypoint, which becomes uvicorn: the Supervisor's watchdog sees the app itself.
"""
import json
import os
import sys
from pathlib import Path

DATA = Path(os.environ.get("HA_DATA_DIR", "/data"))
OPTIONS = Path(os.environ.get("HA_OPTIONS_FILE", DATA / "options.json"))
APP_DIR = os.environ.get("HA_APP_DIR", "/home/app/spoolman")
ENTRYPOINT = os.environ.get("HA_APP_ENTRYPOINT", "/home/app/spoolman/entrypoint.sh")
APP_UID = APP_GID = 1000          # the image's user `app`; its entrypoint keeps these ids unless PUID/PGID say otherwise
LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR")


def log(message: str) -> None:
    print(f"[spoolman] {message}", flush=True)


def fail(message: str) -> None:
    print(f"[spoolman] ERROR: {message}", file=sys.stderr, flush=True)
    raise SystemExit(1)


def read_options() -> dict:
    try:
        return json.loads(OPTIONS.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}


def flag(value, default: bool) -> str:
    """Spoolman reads TRUE/FALSE; an option that is not set keeps Spoolman's own default."""
    return "TRUE" if (default if value is None else bool(value)) else "FALSE"


def build_env(options: dict) -> dict:
    level = str(options.get("log_level") or "INFO").upper()
    if level not in LEVELS:
        fail(f"log_level must be one of {', '.join(LEVELS)}, not {level!r}.")
    return {
        "SPOOLMAN_DIR_DATA": str(DATA / "spoolman"),
        "SPOOLMAN_HOST": "0.0.0.0",
        "SPOOLMAN_PORT": "8000",
        "SPOOLMAN_LOGGING_LEVEL": level,
        "SPOOLMAN_AUTOMATIC_BACKUP": flag(options.get("automatic_backup"), True),
        "SPOOLMAN_UPDATE_CHECK": flag(options.get("update_check"), True),
    }


def give_to_app(folder: Path) -> None:
    """Create the data folder and hand it, with everything in it, to the app's user (only root can, and only root needs to)."""
    folder.mkdir(parents=True, exist_ok=True)
    if os.geteuid() != 0:
        return
    for root, dirs, files in os.walk(folder):
        for path in (root, *(os.path.join(root, name) for name in dirs + files)):
            os.lchown(path, APP_UID, APP_GID)


def main() -> None:
    env = build_env(read_options())
    give_to_app(Path(env["SPOOLMAN_DIR_DATA"]))
    log(f"data in {env['SPOOLMAN_DIR_DATA']}; log level {env['SPOOLMAN_LOGGING_LEVEL']}; "
        f"automatic backup {env['SPOOLMAN_AUTOMATIC_BACKUP'].lower()}; update check {env['SPOOLMAN_UPDATE_CHECK'].lower()}")
    os.chdir(APP_DIR)
    os.execvpe(ENTRYPOINT, [ENTRYPOINT], {**os.environ, **env})


if __name__ == "__main__":
    main()
