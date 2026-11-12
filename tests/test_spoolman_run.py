"""run.py of the Spoolman app (stable and beta): the options become Spoolman's variables, the data lives in /data/spoolman and belongs to the app's
user, and the script becomes the image's entrypoint.

The script is started with a temporary data folder and, instead of the image's entrypoint, `env`, so the environment it hands over is printed."""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True      # do not leave a __pycache__ in the add-on folders
FOLDERS = ("spoolman", "spoolman-beta")


def load(folder: str):
    spec = importlib.util.spec_from_file_location(f"spoolman_run_{folder.replace('-', '_')}", ROOT / folder / "run.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EnvironmentTest(unittest.TestCase):
    def test_defaults_without_options(self):
        for folder in FOLDERS:
            env = load(folder).build_env({})
            self.assertEqual(env["SPOOLMAN_DIR_DATA"], "/data/spoolman", folder)
            self.assertEqual((env["SPOOLMAN_HOST"], env["SPOOLMAN_PORT"]), ("0.0.0.0", "8000"), folder)
            self.assertEqual(env["SPOOLMAN_LOGGING_LEVEL"], "INFO", folder)
            self.assertEqual((env["SPOOLMAN_AUTOMATIC_BACKUP"], env["SPOOLMAN_UPDATE_CHECK"]), ("TRUE", "TRUE"), folder)

    def test_options_become_variables(self):
        for folder in FOLDERS:
            env = load(folder).build_env({"automatic_backup": False, "log_level": "debug", "update_check": False})
            self.assertEqual(env["SPOOLMAN_LOGGING_LEVEL"], "DEBUG", folder)
            self.assertEqual((env["SPOOLMAN_AUTOMATIC_BACKUP"], env["SPOOLMAN_UPDATE_CHECK"]), ("FALSE", "FALSE"), folder)

    def test_an_unknown_log_level_is_refused(self):
        for folder in FOLDERS:
            with self.assertRaises(SystemExit):
                load(folder).build_env({"log_level": "LOUD"})

    def test_no_database_settings(self):
        # Spoolman's own default is SQLite in SPOOLMAN_DIR_DATA; this app offers no external database.
        for folder in FOLDERS:
            self.assertFalse([key for key in load(folder).build_env({}) if key.startswith("SPOOLMAN_DB_")], folder)


class StartTest(unittest.TestCase):
    def setUp(self):
        self.data = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.data)

    def start(self, folder, options):
        (self.data / "options.json").write_text(json.dumps(options), encoding="utf-8")
        environment = {"PATH": os.environ["PATH"], "HA_DATA_DIR": str(self.data), "HA_APP_DIR": str(self.data),
                       "HA_APP_ENTRYPOINT": shutil.which("env")}
        done = subprocess.run([sys.executable, str(ROOT / folder / "run.py")], env=environment, capture_output=True, text=True, timeout=30)
        return done, dict(line.split("=", 1) for line in done.stdout.splitlines() if "=" in line)

    def test_hands_the_options_to_the_entrypoint(self):
        for folder in FOLDERS:
            done, env = self.start(folder, {"automatic_backup": False, "log_level": "WARNING", "update_check": True})
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertEqual(env["SPOOLMAN_DIR_DATA"], str(self.data / "spoolman"), folder)
            self.assertEqual((env["SPOOLMAN_LOGGING_LEVEL"], env["SPOOLMAN_AUTOMATIC_BACKUP"]), ("WARNING", "FALSE"), folder)
            self.assertTrue((self.data / "spoolman").is_dir(), folder)

    @unittest.skipUnless(hasattr(os, "geteuid") and os.geteuid() == 0, "handing the folder over needs root, as in the app")
    def test_the_data_folder_belongs_to_the_apps_user(self):
        (self.data / "spoolman" / "backups").mkdir(parents=True)
        (self.data / "spoolman" / "spoolman.db").write_text("")
        done, _ = self.start("spoolman", {})
        self.assertEqual(done.returncode, 0, done.stderr)
        for path in (self.data / "spoolman", self.data / "spoolman" / "backups", self.data / "spoolman" / "spoolman.db"):
            self.assertEqual((path.stat().st_uid, path.stat().st_gid), (1000, 1000), path)
        self.assertEqual((self.data / "options.json").stat().st_uid, 0, "only the app's own folder is handed over")


if __name__ == "__main__":
    unittest.main()
