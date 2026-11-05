"""run.sh of the NAS Storage Analyzer app (stable and beta): the options become the environment of the all-in-one image.

run.sh is started with a temporary data folder and, instead of the image's nasa-aio, `env`, so the environment it would hand over is
printed. It needs sh, jq and base64, as the image has.
"""
import base64
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEY = base64.b64encode(b"k" * 32).decode()


@unittest.skipUnless(shutil.which("jq") and shutil.which("sh"), "run.sh needs sh and jq")
class RunScriptTest(unittest.TestCase):
    folder = "nas-storage-analyzer"

    def setUp(self):
        self.data = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.data)

    def run_script(self, options=None, env=None):
        if options is not None:
            (self.data / "options.json").write_text(json.dumps(options), encoding="utf-8")
        environment = {"PATH": os.environ["PATH"], "HA_DATA_DIR": str(self.data), "HA_AIO_COMMAND": "env", **(env or {})}
        done = subprocess.run(["sh", str(ROOT / self.folder / "run.sh")], env=environment, capture_output=True, text=True, timeout=30)
        values = dict(line.split("=", 1) for line in done.stdout.splitlines() if "=" in line)
        return done, values

    def test_first_start_makes_a_key_and_keeps_it(self):
        done, env = self.run_script({"worker_parallel": 2, "update_check": True})
        self.assertEqual(done.returncode, 0, done.stderr)
        key = env["NASSA_ENCRYPTION_KEY"]
        self.assertEqual(len(base64.b64decode(key)), 32)
        self.assertEqual((self.data / "encryption.key").read_text().strip(), key)
        self.assertEqual(oct((self.data / "encryption.key").stat().st_mode & 0o777), "0o600")
        again, env2 = self.run_script({"worker_parallel": 2, "update_check": True})
        self.assertEqual(env2["NASSA_ENCRYPTION_KEY"], key, "a second start must use the same key")
        self.assertIn("made a new encryption key", done.stderr)
        self.assertNotIn("made a new encryption key", again.stderr)

    def test_options_become_variables(self):
        done, env = self.run_script({
            "setup_token": "SETUPTOKEN123456", "public_url": "https://nassa.example.com", "rp_id": "nassa.example.com",
            "rp_origins": "https://nassa.example.com", "trusted_proxies": "172.30.32.0/23", "worker_parallel": 4, "update_check": False,
        })
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(env["NASSA_SETUP_TOKEN"], "SETUPTOKEN123456")
        self.assertEqual(env["NASSA_PUBLIC_URL"], "https://nassa.example.com")
        self.assertEqual(env["NASSA_RP_ID"], "nassa.example.com")
        self.assertEqual(env["NASSA_RP_ORIGINS"], "https://nassa.example.com")
        self.assertEqual(env["NASSA_TRUSTED_PROXIES"], "172.30.32.0/23")
        self.assertEqual(env["NASSA_WORKER_PARALLEL"], "4")
        self.assertEqual(env["NASSA_UPDATE_CHECK"], "false")
        self.assertEqual(env["NASSA_SHARES_ROOT"], "/mnt/shares", "the mapped folders are below /mnt/shares")

    def test_empty_options_set_nothing(self):
        done, env = self.run_script({"setup_token": "", "rp_id": "", "worker_parallel": 2, "update_check": True})
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertNotIn("NASSA_SETUP_TOKEN", env)
        self.assertNotIn("NASSA_RP_ID", env)

    def test_no_options_file_still_starts(self):
        done, env = self.run_script()
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("NASSA_ENCRYPTION_KEY", env)

    def test_smaller_postgres_unless_told_otherwise(self):
        _, env = self.run_script({})
        self.assertEqual((env["PG_SHARED_BUFFERS"], env["PG_EFFECTIVE_CACHE_SIZE"]), ("256MB", "1GB"))
        _, env = self.run_script({}, {"PG_SHARED_BUFFERS": "1GB"})
        self.assertEqual(env["PG_SHARED_BUFFERS"], "1GB")

    def test_the_key_option_wins_and_is_checked(self):
        done, env = self.run_script({"encryption_key": KEY})
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(env["NASSA_ENCRYPTION_KEY"], KEY)
        self.assertFalse((self.data / "encryption.key").exists(), "a key given as option is not written")
        done, _ = self.run_script({"encryption_key": "not-a-key"})
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("encryption_key must be base64 of 32 bytes", done.stderr)

    def test_a_damaged_key_file_is_refused(self):
        (self.data / "encryption.key").write_text("garbage\n")
        done, _ = self.run_script({})
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("does not hold a valid key", done.stderr)

    def test_passkey_domain_needs_its_addresses(self):
        done, _ = self.run_script({"rp_id": "nassa.example.com"})
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("rp_origins is needed", done.stderr)

    def test_no_secret_in_the_log(self):
        done, env = self.run_script({"setup_token": "SETUPTOKEN123456", "encryption_key": KEY})
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertNotIn("SETUPTOKEN123456", done.stderr)
        self.assertNotIn(KEY, done.stderr)
        self.assertIn("options set: setup_token", done.stderr)


class BetaRunScriptTest(RunScriptTest):
    folder = "nas-storage-analyzer-beta"


if __name__ == "__main__":
    unittest.main()
