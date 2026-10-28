import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import sync_versions as sv  # noqa: E402


class PureFunctionsTest(unittest.TestCase):
    def test_newest_compares_numbers_not_text(self):
        tags = ["v1.0.9", "v1.0.30", "v1.0.4", "latest", "v0.9.99"]
        self.assertEqual(sv.newest(tags, r"^v(\d+\.\d+\.\d+)$"), "1.0.30")

    def test_newest_separates_the_beta_line(self):
        tags = ["v2.81.0", "v2.81.0-beta", "v2.82.0-beta", "v2.80.2-beta"]
        self.assertEqual(sv.newest(tags, r"^v(\d+\.\d+\.\d+)$"), "2.81.0")
        self.assertEqual(sv.newest(tags, r"^v(\d+\.\d+\.\d+-beta)$"), "2.82.0-beta")

    def test_newest_without_match(self):
        self.assertIsNone(sv.newest(["latest"], r"^v(\d+\.\d+\.\d+)$"))

    def test_version_is_replaced_only_on_its_own_line(self):
        text = '# version: "0.0.1" in a comment\nname: X\nversion: "1.2.3"\nslug: x\n'
        self.assertEqual(sv.current_version(text), "1.2.3")
        self.assertEqual(sv.with_version(text, "1.2.4"), '# version: "0.0.1" in a comment\nname: X\nversion: "1.2.4"\nslug: x\n')

    def test_changelog_with_sections_gets_a_new_one_on_top(self):
        text = "# Changelog\n\nLink\n\n## 1.0.0\n\n- First\n"
        result = sv.changelog_with(text, "1.0.1", "o/r")
        self.assertLess(result.index("## 1.0.1"), result.index("## 1.0.0"))
        self.assertIn("https://github.com/o/r/releases/tag/v1.0.1", result)

    def test_pointer_changelog_stays(self):
        text = "# Changelog\n\nSee GitHub.\n"
        self.assertEqual(sv.changelog_with(text, "1.0.1", "o/r"), text)


class SyncTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        shutil.copy(ROOT / "sources.json", self.tmp / "sources.json")
        for name in ("doorbell-map", "mealieshopper"):
            shutil.copytree(ROOT / name, self.tmp / name)
        import json
        sources = json.loads((self.tmp / "sources.json").read_text())
        (self.tmp / "sources.json").write_text(json.dumps({k: v for k, v in sources.items() if k in ("doorbell-map", "mealieshopper")}))

    def run_sync(self, tags, published, write=True):
        return sv.sync(self.tmp, write=write, tags_of=lambda repo: tags[repo], exists=lambda image, tag: (image, tag) in published)

    def test_raises_when_the_image_exists(self):
        tags = {"helmerzNL/Doorbell-Map": ["v1.0.31", "v1.0.30"], "helmerzNL/MealieShopper": ["v2.81.0"]}
        report = self.run_sync(tags, {("ghcr.io/helmerznl/doorbell-map", "v1.0.31")})
        self.assertEqual(report, ["doorbell-map: 1.0.30 -> 1.0.31"])
        self.assertIn('version: "1.0.31"', (self.tmp / "doorbell-map" / "config.yaml").read_text())
        self.assertIn("## 1.0.31", (self.tmp / "doorbell-map" / "CHANGELOG.md").read_text())

    def test_waits_for_the_image(self):
        tags = {"helmerzNL/Doorbell-Map": ["v1.0.31"], "helmerzNL/MealieShopper": ["v2.81.0"]}
        report = self.run_sync(tags, set())
        self.assertIn("not published yet", report[0])
        self.assertIn('version: "1.0.30"', (self.tmp / "doorbell-map" / "config.yaml").read_text())

    def test_check_changes_nothing(self):
        tags = {"helmerzNL/Doorbell-Map": ["v1.0.31"], "helmerzNL/MealieShopper": ["v2.81.0"]}
        before = (self.tmp / "doorbell-map" / "config.yaml").read_text()
        self.run_sync(tags, {("ghcr.io/helmerznl/doorbell-map", "v1.0.31")}, write=False)
        self.assertEqual((self.tmp / "doorbell-map" / "config.yaml").read_text(), before)

    def test_never_goes_back(self):
        tags = {"helmerzNL/Doorbell-Map": ["v1.0.2"], "helmerzNL/MealieShopper": ["v2.0.0"]}
        self.assertEqual(self.run_sync(tags, set()), [])


if __name__ == "__main__":
    unittest.main()
