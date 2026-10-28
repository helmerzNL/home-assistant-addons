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
        self.assertEqual(names, {"discvault", "discvault-beta", "doorbell-map", "doorbell-map-beta", "mealieshopper", "mealieshopper-beta", "printpricing", "printpricing-beta"})


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

    def test_addon_without_source(self):
        (self.tmp / "sources.json").write_text('{"discvault": {}}', encoding="utf-8")
        self.assertTrue(any("sources.json" in p for p in self.problems()))


if __name__ == "__main__":
    unittest.main()
