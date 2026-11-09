import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_addons  # noqa: E402


class RepositoryTest(unittest.TestCase):
    def test_repository_is_in_order(self):
        self.assertEqual(check_addons.check_repository(), [])

    def test_every_app_has_an_addon(self):
        names = {folder.name for folder in check_addons.addon_dirs()}
        self.assertEqual(names, {"discvault", "discvault-beta", "doorbell-map", "doorbell-map-beta", "mealieshopper", "mealieshopper-beta", "nas-storage-analyzer", "nas-storage-analyzer-beta", "printpricing", "printpricing-beta"})


class AddonContentTest(unittest.TestCase):
    """Things an add-on needs that check_addons.py cannot know from the structure alone."""

    def config(self, name):
        return check_addons.load(ROOT / name / "config.yaml")

    def test_nas_storage_analyzer_may_mount_smb(self):
        # mount.cifs asks for CAP_DAC_READ_SEARCH next to CAP_SYS_ADMIN and stops without it: with SYS_ADMIN alone only NFS works
        # (helmerzNL/NAS-Storage-Analyzer 1fecd43). CAP_DAC_OVERRIDE, the third one it asks for, is in Docker's default set.
        for name in ("nas-storage-analyzer", "nas-storage-analyzer-beta"):
            with self.subTest(name):
                self.assertLessEqual({"SYS_ADMIN", "DAC_READ_SEARCH"}, set(self.config(name).get("privileged") or []))

    def test_mealieshopper_beta_keeps_the_options_of_the_stable_addon(self):
        # derive_beta.py does not cover MealieShopper; its two add-ons are kept in step by hand. The options and their names stay the same;
        # a description may differ, because the beta describes a newer app (for example stores the stable version does not have yet).
        stable, beta = self.config("mealieshopper"), self.config("mealieshopper-beta")
        self.assertEqual(stable.get("schema"), beta.get("schema"))
        for language in ("en", "nl"):
            with self.subTest(language):
                names = [{key: entry.get("name") for key, entry in (check_addons.load(ROOT / name / "translations" / f"{language}.yaml")
                                                                    .get("configuration") or {}).items()}
                         for name in ("mealieshopper", "mealieshopper-beta")]
                self.assertEqual(names[0], names[1])

    def test_doorbell_map_can_keep_more_backups(self):
        # Since 2.0.0 Doorbell Map keeps 50 backups (it was 200) and removes older ones at start-up; run.js passes max_backups on as MAX_BACKUPS.
        for name in ("doorbell-map", "doorbell-map-beta"):
            with self.subTest(name):
                self.assertIn("max_backups", self.config(name).get("schema") or {})

    def test_mealieshopper_offers_another_ai_address(self):
        # MealieShopper 3.14.0 reads anthropic_base_url and openai_base_url from options.json (docker-entrypoint.py, OPTION_ENV).
        self.assertLessEqual({"anthropic_base_url", "openai_base_url"}, set(self.config("mealieshopper").get("schema") or {}))


class DefectsAreCaughtTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        for item in ROOT.iterdir():
            if item.name in (".git", "__pycache__", "node_modules"):
                continue
            (shutil.copytree if item.is_dir() else shutil.copy)(item, self.tmp / item.name)


    def problems(self):
        return check_addons.check_repository(self.tmp)

    def test_bytecode_cache_in_a_stable_folder_is_not_a_difference(self):
        cache = self.tmp / "discvault" / "__pycache__"
        cache.mkdir()
        (cache / "run.cpython-312.pyc").write_bytes(b"\0")
        self.assertEqual(self.problems(), [])

    def test_missing_dutch_section(self):
        doc = self.tmp / "doorbell-map" / "DOCS.md"
        doc.write_text(doc.read_text(encoding="utf-8").replace("## Nederlands", "## Dutch"), encoding="utf-8")
        self.assertTrue(any("Nederlands" in p for p in self.problems()))

    def test_untranslated_option(self):
        translation = self.tmp / "discvault" / "translations" / "nl.yaml"
        translation.write_text(translation.read_text(encoding="utf-8").replace("  omdb_api_key:", "  omdb_sleutel:"), encoding="utf-8")
        self.assertTrue(any("nl.yaml" in p for p in self.problems()))

    def test_port_clash(self):
        config = self.tmp / "discvault" / "config.yaml"
        config.write_text(config.read_text(encoding="utf-8").replace("5000/tcp: 6180", "5000/tcp: 9888"), encoding="utf-8")
        self.assertTrue(any("9888" in p for p in self.problems()))

    def test_dockerfile_not_on_version(self):
        dockerfile = self.tmp / "doorbell-map" / "Dockerfile"
        dockerfile.write_text(dockerfile.read_text(encoding="utf-8").replace(":v${BUILD_VERSION}", ":latest"), encoding="utf-8")
        self.assertTrue(any("BUILD_VERSION" in p for p in self.problems()))

    def test_beta_that_drifted_from_its_stable_addon(self):
        run = self.tmp / "doorbell-map-beta" / "run.js"
        run.write_text(run.read_text(encoding="utf-8") + "\n// edited by hand\n", encoding="utf-8")
        self.assertTrue(any("run.js" in p for p in self.problems()))

    def test_beta_dockerfile_must_build_on_the_beta_image(self):
        dockerfile = self.tmp / "discvault-beta" / "Dockerfile"
        dockerfile.write_text(dockerfile.read_text(encoding="utf-8").replace("discvault:beta", "discvault:latest"), encoding="utf-8")
        self.assertTrue(any("beta" in p for p in self.problems()))

    def test_every_addon_opens_from_its_page(self):
        import yaml
        for folder in check_addons.addon_dirs():
            self.assertIn("[PORT:", yaml.safe_load((folder / "config.yaml").read_text()).get("webui", ""), folder.name)

    def test_addon_without_web_ui_button(self):
        config = self.tmp / "doorbell-map" / "config.yaml"
        config.write_text("\n".join(l for l in config.read_text(encoding="utf-8").splitlines() if not l.startswith("webui:")) + "\n", encoding="utf-8")
        self.assertTrue(any("webui" in p for p in self.problems()))

    def test_addon_without_source(self):
        (self.tmp / "sources.json").write_text('{"discvault": {}}', encoding="utf-8")
        self.assertTrue(any("sources.json" in p for p in self.problems()))


if __name__ == "__main__":
    unittest.main()
