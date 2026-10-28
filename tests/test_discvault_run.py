import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("discvault_run", ROOT / "discvault" / "run.py")
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)

KEPT = {"postgres_password": "abc123", "jwt_secret": "s3cret"}


class SettingsTest(unittest.TestCase):
    def test_domain_becomes_passkey_settings(self):
        env = run.settings({"rp_id": "Vault.Example.com", "block_crawlers": False, "omdb_api_key": " key "}, KEPT)
        self.assertEqual(env["RP_ID"], "vault.example.com")
        self.assertEqual(env["RP_ORIGINS"], "https://vault.example.com")
        self.assertEqual(env["DATABASE_URL"], "postgresql://discvault:abc123@127.0.0.1:5432/discvault")
        self.assertEqual(env["JWT_SECRET"], "s3cret")
        self.assertEqual(env["DISCVAULT_BLOCK_CRAWLERS"], "false")
        self.assertEqual(env["OMDB_API_KEY"], "key")
        self.assertNotIn("TMDB_API_KEY", env)

    def test_explicit_origins_win(self):
        env = run.settings({"rp_id": "vault.example.com", "rp_origins": "https://a.example.com,https://b.example.com"}, KEPT)
        self.assertEqual(env["RP_ORIGINS"], "https://a.example.com,https://b.example.com")

    def test_missing_domain_stops_with_a_message(self):
        with self.assertRaises(SystemExit):
            run.settings({}, KEPT)

    def test_domain_with_scheme_or_port_is_refused(self):
        for bad in ("https://vault.example.com", "vault.example.com:6180", "vault.example.com/x"):
            with self.assertRaises(SystemExit):
                run.settings({"rp_id": bad}, KEPT)


if __name__ == "__main__":
    unittest.main()
