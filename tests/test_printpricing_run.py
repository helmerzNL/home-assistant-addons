"""The stable add-on follows the stable app (domain required); the beta add-on follows the beta app (domain optional)."""
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
    def test_stable_still_needs_a_domain(self):
        with self.assertRaises(SystemExit):
            load("printpricing").settings({}, KEPT)

    def test_beta_starts_without_a_domain(self):
        env = load("printpricing-beta").settings({}, KEPT)
        self.assertEqual((env["RP_ID"], env["RP_ORIGINS"]), ("", ""))

    def test_beta_with_a_domain_pins_it(self):
        env = load("printpricing-beta").settings({"rp_id": "Print.Example.com"}, KEPT)
        self.assertEqual((env["RP_ID"], env["RP_ORIGINS"]), ("print.example.com", "https://print.example.com"))

    def test_beta_still_refuses_a_malformed_domain(self):
        with self.assertRaises(SystemExit):
            load("printpricing-beta").settings({"rp_id": "https://print.example.com"}, KEPT)

    def test_only_the_beta_is_offered_for_arm(self):
        import yaml
        self.assertNotIn("aarch64", yaml.safe_load((ROOT / "printpricing" / "config.yaml").read_text())["arch"])
        self.assertIn("aarch64", yaml.safe_load((ROOT / "printpricing-beta" / "config.yaml").read_text())["arch"])


if __name__ == "__main__":
    unittest.main()
