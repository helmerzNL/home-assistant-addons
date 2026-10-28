#!/usr/bin/env python3
"""Make the beta add-ons from their stable add-ons, so the two cannot drift apart.

`sources.json` marks a beta add-on with `"stable": "<folder>"`. Its folder is the stable folder with these differences: its own name, slug,
host port (the stable one plus one) and data folder, a Dockerfile that builds on the `beta` image of the app, and a notice in the
documentation. Its `version` is not touched here: scripts/sync_versions.py owns it. Everything else (start script, translations, icons) is a copy.

Usage:
    python scripts/derive_beta.py            write the beta folders
    python scripts/derive_beta.py --check    report folders that differ from what would be written (exit code 1)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GENERATED = ("config.yaml", "Dockerfile", "README.md", "DOCS.md", "CHANGELOG.md")
NOTICE = (
    "> **Beta.** The development version of the app, built from its `beta` branch. New features and fixes arrive here first and it can be\n"
    "> unstable. It has its own data folder and port, so it runs next to the stable app. Do not point it at the data of the stable app: a beta can\n"
    "> change the database in ways the stable version cannot read.\n"
    ">\n"
    "> **Bèta.** De ontwikkelversie van de app, gebouwd vanaf de `beta`-branch. Nieuwe functies en fixes komen hier eerst en het kan onstabiel zijn.\n"
    "> Hij heeft een eigen data-map en poort, dus hij draait naast de stabiele app. Gebruik de data van de stabiele app niet voor de beta: een beta kan\n"
    "> de database aanpassen op een manier die de stabiele versie niet kan lezen.\n"
)


def beta_pairs(root: Path = ROOT) -> dict[str, str]:
    sources = json.loads((root / "sources.json").read_text(encoding="utf-8"))
    return {name: source["stable"] for name, source in sources.items() if source.get("stable")}


def _line(text: str, pattern: str, replacement: str) -> str:
    text, count = re.subn(pattern, replacement, text, count=1, flags=re.M)
    if not count:
        raise SystemExit(f"no line matches {pattern!r}")
    return text


def beta_config(stable: str, current: str | None, folder: str) -> tuple[str, str]:
    """The config.yaml of the beta add-on, and the host port it uses (the stable one plus one)."""
    name = re.search(r"^name: (.*)$", stable, flags=re.M).group(1).strip()
    text = _line(stable, r"^name: .*$", f"name: {name} (beta)")
    text = _line(text, r"^slug: (\S+)$", r"slug: \1_beta")
    text = _line(text, r"^description: (.*)$", r"description: Development version (beta). \1")
    text = _line(text, r'^version: ".*"$', re.search(r'^version: ".*"$', current, flags=re.M).group(0) if current else 'version: "0.0.0-beta.0"')
    host_port = int(re.search(r"^  \d+/tcp: (\d+)$", text, flags=re.M).group(1)) + 1
    text = _line(text, r"^(  \d+/tcp: )\d+$", rf"\g<1>{host_port}")
    head, rest = text.split("\nname:", 1)
    header = (f"# DERIVED from ../{folder} by `python scripts/derive_beta.py`: change the stable add-on, not this file. The beta add-on runs the `beta` image of the app;\n"
              "# its `version` ends in -beta.<build time of that image> and is raised by `scripts/sync_versions.py`, so Home Assistant offers an update for every new beta build.")
    return "\n".join([header, "name:" + rest]), str(host_port)


def beta_dockerfile(stable: str) -> str:
    image = re.search(r"^FROM (\S+?):v?\$\{BUILD_VERSION\}$", stable, flags=re.M).group(1)
    text = _line(stable, r"^FROM \S+$", f"FROM {image}:beta")
    text = text.replace("ENV PRINTPRICING_TAG=${BUILD_VERSION}", "ENV PRINTPRICING_TAG=beta")
    if "DOORBELL_MAP_TAG" not in text and "doorbell-map" in image:
        text = text.replace(f"FROM {image}:beta\n", f"FROM {image}:beta\n\n# The app shows a BETA label for this tag.\nENV DOORBELL_MAP_TAG=beta\n", 1)
    comment = ("# Home Assistant app, beta: the `beta` image of the app, which moves with every build of its beta branch. The Supervisor builds this on the\n"
               "# device and pulls the base image again for every update; `version` in config.yaml is only the marker of the build.\n")
    return comment + text.split("\n", 2)[2] if text.startswith("# Home Assistant app") else comment + text


def beta_doc(stable: str, name: str, stable_port: str, beta_port: str) -> str:
    text = _line(stable, r"^# (.*)$", r"# \1 (beta)")
    text = re.sub(rf"\b(Choose|Kies) \*\*{re.escape(name)}\*\*", rf"\1 **{name} (beta)**", text)
    text = re.sub(rf"\b{stable_port}\b", beta_port, text)
    return _line(text, r"^(\*English first.*)$", r"\1\n\n" + NOTICE.replace("\\", "\\\\").rstrip("\n"))


def beta_changelog(stable: str, repo: str) -> str:
    return ("# Changelog\n\nBeta builds follow the `beta` branch of the app and have no release notes of their own; see the commits: "
            f"https://github.com/{repo}/commits/beta\n"
            f"Beta-builds volgen de `beta`-branch van de app en hebben geen eigen release-teksten; zie de commits: https://github.com/{repo}/commits/beta\n")


def expected_files(root: Path = ROOT) -> dict[Path, bytes]:
    sources = json.loads((root / "sources.json").read_text(encoding="utf-8"))
    files = {}
    for beta, stable_name in beta_pairs(root).items():
        stable, target = root / stable_name, root / beta
        read = lambda folder, name: (folder / name).read_text(encoding="utf-8")
        current = read(target, "config.yaml") if (target / "config.yaml").is_file() else None
        config, beta_port = beta_config(read(stable, "config.yaml"), current, stable_name)
        stable_port = re.search(r"^  \d+/tcp: (\d+)$", read(stable, "config.yaml"), flags=re.M).group(1)
        name = re.search(r"^name: (.*)$", read(stable, "config.yaml"), flags=re.M).group(1).strip()
        files[target / "config.yaml"] = config.encode()
        files[target / "Dockerfile"] = beta_dockerfile(read(stable, "Dockerfile")).encode()
        for doc in ("README.md", "DOCS.md"):
            files[target / doc] = beta_doc(read(stable, doc), name, stable_port, beta_port).encode()
        files[target / "CHANGELOG.md"] = beta_changelog(read(stable, "CHANGELOG.md"), sources[stable_name]["repo"]).encode()
        for source in sorted(stable.rglob("*")):
            relative = source.relative_to(stable)
            if source.is_file() and relative.as_posix() not in GENERATED:
                files[target / relative] = source.read_bytes()
    return files


def differences(root: Path = ROOT) -> list[str]:
    expected = expected_files(root)
    problems = []
    for path, content in expected.items():
        if not path.is_file():
            problems.append(f"missing: {path.relative_to(root)}")
        elif path.read_bytes() != content:
            problems.append(f"differs: {path.relative_to(root)}")
    for beta in beta_pairs(root):
        for path in sorted((root / beta).rglob("*")) if (root / beta).is_dir() else []:
            if path.is_file() and path not in expected:
                problems.append(f"does not belong: {path.relative_to(root)}")
    return problems


def write(root: Path = ROOT) -> None:
    for path, content in expected_files(root).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


if __name__ == "__main__":
    if "--check" in sys.argv[1:]:
        found = differences()
        print("\n".join(found) or "The beta add-ons match their stable add-ons.")
        sys.exit(1 if found else 0)
    write()
    print("Written:", ", ".join(beta_pairs()))
