import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True      # do not leave a __pycache__ in the add-on folder
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

    def test_password_login_needs_no_domain(self):
        env = run.settings({"password_login": True}, KEPT)
        self.assertEqual(env["LEGACY_AUTH_ENABLED"], "true")
        self.assertNotIn("RP_ID", env)
        self.assertNotIn("RP_ORIGINS", env)

    def test_password_login_keeps_the_domain_when_set(self):
        env = run.settings({"password_login": True, "rp_id": "vault.example.com"}, KEPT)
        self.assertEqual(env["LEGACY_AUTH_ENABLED"], "true")
        self.assertEqual(env["RP_ID"], "vault.example.com")
        self.assertEqual(env["RP_ORIGINS"], "https://vault.example.com")

    def test_password_login_is_off_by_default(self):
        self.assertEqual(run.settings({"rp_id": "vault.example.com"}, KEPT)["LEGACY_AUTH_ENABLED"], "false")

    def test_password_login_still_refuses_a_malformed_domain(self):
        with self.assertRaises(SystemExit):
            run.settings({"password_login": True, "rp_id": "https://vault.example.com"}, KEPT)

    def test_missing_domain_stops_with_a_message(self):
        with self.assertRaises(SystemExit):
            run.settings({}, KEPT)

    def test_domain_with_scheme_or_port_is_refused(self):
        for bad in ("https://vault.example.com", "vault.example.com:6180", "vault.example.com/x"):
            with self.assertRaises(SystemExit):
                run.settings({"rp_id": bad}, KEPT)


OIDC = {"rp_id": "vault.example.com", "oidc_issuer": "https://id.example.com", "oidc_client_id": "abc", "oidc_client_secret": "shh"}


class OidcTest(unittest.TestCase):
    def test_off_by_default(self):
        env = run.settings({"rp_id": "vault.example.com"}, KEPT)
        self.assertFalse([name for name in env if "OIDC" in name])

    def test_the_three_options_switch_it_on(self):
        env = run.settings({**OIDC, "oidc_provider_name": " Pocket ID "}, KEPT)
        self.assertEqual(env["DISCVAULT_OIDC_ISSUER"], "https://id.example.com")
        self.assertEqual(env["DISCVAULT_OIDC_CLIENT_ID"], "abc")
        self.assertEqual(env["DISCVAULT_OIDC_CLIENT_SECRET"], "shh")
        self.assertEqual(env["DISCVAULT_OIDC_PROVIDER_NAME"], "Pocket ID")
        self.assertNotIn("DISCVAULT_OIDC_INSECURE_BACKCHANNEL_ORIGINS", env)

    def test_private_backchannel_origins_are_passed_on(self):
        env = run.settings({**OIDC, "oidc_insecure_backchannel_origins": "http://pocket-id.local:1411"}, KEPT)
        self.assertEqual(env["DISCVAULT_OIDC_INSECURE_BACKCHANNEL_ORIGINS"], "http://pocket-id.local:1411")

    def test_a_partial_set_up_is_refused(self):
        for missing in ("oidc_issuer", "oidc_client_id", "oidc_client_secret"):
            with self.assertRaises(SystemExit):
                run.settings({key: value for key, value in OIDC.items() if key != missing}, KEPT)

    def test_private_origins_alone_are_refused(self):
        with self.assertRaises(SystemExit):
            run.settings({"rp_id": "vault.example.com", "oidc_insecure_backchannel_origins": "http://x.local"}, KEPT)

    def test_an_issuer_without_https_is_refused(self):
        with self.assertRaises(SystemExit):
            run.settings({**OIDC, "oidc_issuer": "http://id.example.com"}, KEPT)

    def test_it_needs_the_address_the_app_is_opened_on(self):
        options = {key: value for key, value in OIDC.items() if key != "rp_id"}
        with self.assertRaises(SystemExit):
            run.settings({**options, "password_login": True}, KEPT)

    def test_the_callback_is_built_from_the_first_origin(self):
        import contextlib
        import io
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            run.settings({**OIDC, "rp_origins": "https://a.example.com/, https://b.example.com"}, KEPT)
        self.assertIn("https://a.example.com/api/next/auth/oidc/callback", out.getvalue())
        self.assertNotIn("shh", out.getvalue())


if __name__ == "__main__":
    unittest.main()
