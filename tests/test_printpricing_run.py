"""The stable and the beta add-on start without a domain (password sign-in), are published for arm64, and keep their data in SQLite:
PostgreSQL runs only for the one-off import of an earlier release."""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True      # do not leave a __pycache__ in the add-on folders


def load(folder: str):
    spec = importlib.util.spec_from_file_location(f"printpricing_run_{folder.replace('-', '_')}", ROOT / folder / "run.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


KEPT = {"postgres_password": "abc", "session_secret": "s", "setup_code": "c", "vapid_public_key": "p", "vapid_private_key": "k"}


class RelyingPartyTest(unittest.TestCase):
    def test_starts_without_a_domain(self):
        for folder in ("printpricing", "printpricing-beta"):
            env = load(folder).settings({}, KEPT)
            self.assertEqual((env["RP_ID"], env["RP_ORIGINS"]), ("", ""), folder)

    def test_a_domain_pins_the_relying_party(self):
        for folder in ("printpricing", "printpricing-beta"):
            env = load(folder).settings({"rp_id": "Print.Example.com"}, KEPT)
            self.assertEqual((env["RP_ID"], env["RP_ORIGINS"]), ("print.example.com", "https://print.example.com"), folder)

    def test_a_malformed_domain_is_still_refused(self):
        for folder in ("printpricing", "printpricing-beta"):
            with self.assertRaises(SystemExit):
                load(folder).settings({"rp_id": "https://print.example.com"}, KEPT)

    def test_the_app_gets_no_database_url_of_its_own(self):
        for folder in ("printpricing", "printpricing-beta"):
            env = load(folder).settings({}, KEPT)
            self.assertNotIn("DATABASE_URL", env, folder)
            self.assertNotIn("LEGACY_DATABASE_URL", env, folder)

    def test_postgresql_is_only_for_an_earlier_releases_data(self):
        import tempfile
        for folder in ("printpricing", "printpricing-beta"):
            module = load(folder)
            with tempfile.TemporaryDirectory() as tmp:
                data = Path(tmp)
                module.PGDATA, module.SQLITE = data / "postgres", data / "db" / "printpricing.sqlite3"
                self.assertFalse(module.has_old_database(), folder)                         # a new installation
                module.PGDATA.mkdir()
                (module.PGDATA / "PG_VERSION").write_text("17\n")
                self.assertTrue(module.has_old_database(), folder)                          # old data, not imported yet
                self.assertEqual(module.settings({}, KEPT)["LEGACY_DATABASE_URL"], "postgresql://printpricing:abc@127.0.0.1:5432/printpricing", folder)
                module.SQLITE.parent.mkdir()
                module.SQLITE.write_text("")
                self.assertFalse(module.has_old_database(), folder)                         # imported: the app alone
                self.assertNotIn("LEGACY_DATABASE_URL", module.settings({}, KEPT), folder)

    def test_both_are_offered_for_arm(self):
        import yaml
        for folder in ("printpricing", "printpricing-beta"):
            self.assertIn("aarch64", yaml.safe_load((ROOT / folder / "config.yaml").read_text())["arch"], folder)


if __name__ == "__main__":
    unittest.main()
