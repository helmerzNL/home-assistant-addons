#!/usr/bin/env python3
"""Check that every add-on in this repository is complete and consistent.

Run `python scripts/check_addons.py`; exit code 1 and one line per problem when something is wrong. The tests and the CI workflow run it.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_KEYS = ("name", "version", "slug", "description", "url", "arch", "startup", "boot")
REQUIRED_FILES = ("config.yaml", "README.md", "DOCS.md", "CHANGELOG.md", "icon.png", "logo.png", "translations/en.yaml", "translations/nl.yaml")
LANGUAGES = ("en", "nl")


def addon_dirs(root: Path = ROOT) -> list[Path]:
    return sorted(p.parent for p in root.glob("*/config.yaml"))


def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def check_addon(folder: Path, sources: dict) -> list[str]:
    name = folder.name
    problems = [f"{name}: missing {f}" for f in REQUIRED_FILES if not (folder / f).is_file()]
    if problems:
        return problems
    config = load(folder / "config.yaml")
    problems += [f"{name}: config.yaml has no {key}" for key in REQUIRED_KEYS if not config.get(key)]
    if not re.fullmatch(r"[a-z0-9_]+", str(config.get("slug", ""))):
        problems.append(f"{name}: slug must be lowercase letters, digits and underscores")
    if not isinstance(config.get("version"), str):
        problems.append(f"{name}: version must be a quoted string")
    if name not in sources:
        problems.append(f"{name}: not listed in sources.json (nothing would keep its version up to date)")
    schema, options = config.get("schema") or {}, config.get("options") or {}
    problems += [f"{name}: option {key} is not in schema" for key in options if key not in schema]
    if config.get("image"):
        if (folder / "Dockerfile").exists():
            problems.append(f"{name}: has both an image and a Dockerfile")
    else:
        dockerfile = folder / "Dockerfile"
        if not dockerfile.is_file():
            problems.append(f"{name}: no image and no Dockerfile")
        else:
            wanted = f":{sources[name]['image_tag']}" if sources.get(name, {}).get("channel") == "beta" else "${BUILD_VERSION}"
            if not any(wanted in line for line in dockerfile.read_text(encoding="utf-8").splitlines() if line.startswith("FROM ")):
                problems.append(f"{name}: the FROM line of the Dockerfile must build on {wanted}")
    for language in LANGUAGES:
        translation = load(folder / "translations" / f"{language}.yaml")
        described = set((translation.get("configuration") or {}))
        if described != set(schema):
            problems.append(f"{name}: translations/{language}.yaml describes {sorted(described)}, the schema has {sorted(schema)}")
        for key, entry in (translation.get("configuration") or {}).items():
            if not (isinstance(entry, dict) and entry.get("name") and entry.get("description")):
                problems.append(f"{name}: translations/{language}.yaml: {key} needs a name and a description")
        ports = set((config.get("ports") or {}))
        if set((translation.get("network") or {})) != ports:
            problems.append(f"{name}: translations/{language}.yaml: network must describe the ports {sorted(ports)}")
    for doc in ("README.md", "DOCS.md"):
        text = (folder / doc).read_text(encoding="utf-8")
        for heading in ("## English", "## Nederlands"):
            if heading not in text:
                problems.append(f"{name}: {doc} has no '{heading}' section (explanations are in English and Dutch)")
    if "Quick start" not in (folder / "README.md").read_text(encoding="utf-8") or "Snel starten" not in (folder / "README.md").read_text(encoding="utf-8"):
        problems.append(f"{name}: README.md needs a short 'Quick start' and 'Snel starten'")
    if "Install" not in (folder / "DOCS.md").read_text(encoding="utf-8") or "Installeren" not in (folder / "DOCS.md").read_text(encoding="utf-8"):
        problems.append(f"{name}: DOCS.md needs an 'Install' and an 'Installeren' section")
    return problems


def check_repository(root: Path = ROOT) -> list[str]:
    problems = []
    if not (root / "repository.yaml").is_file():
        return ["repository.yaml is missing"]
    repository = load(root / "repository.yaml")
    problems += [f"repository.yaml has no {key}" for key in ("name", "url", "maintainer") if not repository.get(key)]
    sources = json.loads((root / "sources.json").read_text(encoding="utf-8"))
    folders = addon_dirs(root)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import derive_beta
    try:
        problems += [f"derived beta add-on: {line}" for line in derive_beta.differences(root)]
    except (AttributeError, SystemExit) as error:
        problems.append(f"derived beta add-on: cannot be made from its stable add-on ({error}); is the stable Dockerfile built on ${{BUILD_VERSION}}?")
    problems += [f"sources.json lists {name}, which is not an add-on folder" for name in sources if not (root / name / "config.yaml").is_file()]
    seen_slugs, seen_ports = {}, {}
    for folder in folders:
        problems += check_addon(folder, sources)
        config = load(folder / "config.yaml")
        slug = config.get("slug")
        if slug in seen_slugs:
            problems.append(f"{folder.name}: slug {slug} is also used by {seen_slugs[slug]}")
        seen_slugs[slug] = folder.name
        for container_port, host_port in (config.get("ports") or {}).items():
            if host_port in seen_ports:
                problems.append(f"{folder.name}: host port {host_port} is also used by {seen_ports[host_port]}")
            seen_ports[host_port] = folder.name
    return problems


if __name__ == "__main__":
    found = check_repository()
    print("\n".join(found) or f"All {len(addon_dirs())} add-ons are in order.")
    sys.exit(1 if found else 0)
