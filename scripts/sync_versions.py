#!/usr/bin/env python3
"""Raise the version of every add-on to the newest release of its app, once the image of that release exists.

Home Assistant offers an update of an add-on when `version` in its config.yaml changes, and the Supervisor then pulls (or builds on) the
image `<image>:<version>`. So the version may only be raised when that image is really published: the release tag of an app is often set
before its image is built. `sources.json` says, per add-on, which repository and tag pattern give the version and which image carries it.

Usage:
    python scripts/sync_versions.py            raise the versions and add a line to the CHANGELOG.md of each
    python scripts/sync_versions.py --check    only report what would change (exit code 0)

GITHUB_TOKEN (optional) raises the rate limit of the GitHub API.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_TYPES = ", ".join((
    "application/vnd.oci.image.index.v1+json", "application/vnd.docker.distribution.manifest.list.v2+json",
    "application/vnd.oci.image.manifest.v1+json", "application/vnd.docker.distribution.manifest.v2+json"))


def version_key(version: str) -> tuple:
    """Sort key for X.Y.Z and X.Y.Z-beta (numbers compared as numbers)."""
    return tuple(int(part) for part in re.findall(r"\d+", version))


def newest(tags: list[str], pattern: str) -> str | None:
    """The highest version among the tags that match the pattern (its first group is the version), or None."""
    versions = [m.group(1) for tag in tags if (m := re.fullmatch(pattern, tag))]
    return max(versions, key=version_key) if versions else None


def current_version(config_text: str) -> str:
    match = re.search(r'^version:\s*"([^"]+)"\s*$', config_text, flags=re.M)
    if not match:
        raise SystemExit('config.yaml has no line of the form: version: "X.Y.Z"')
    return match.group(1)


def with_version(config_text: str, version: str) -> str:
    return re.sub(r'^(version:\s*)"[^"]+"', lambda m: f'{m.group(1)}"{version}"', config_text, count=1, flags=re.M)


def changelog_with(text: str, version: str, repo: str) -> str:
    """Add a section for the version after the title, when the changelog keeps one section per version. A pointer-only changelog stays as it is."""
    if not re.search(r"^## ", text, flags=re.M):
        return text
    section = f"## {version}\n\n- Updated to version {version} of the app. / Bijgewerkt naar versie {version} van de app.\n  https://github.com/{repo}/releases/tag/v{version}\n\n"
    first = re.search(r"^## ", text, flags=re.M).start()
    return text[:first] + section + text[first:]


def _get(url: str, headers: dict | None = None, method: str = "GET"):
    request = urllib.request.Request(url, headers={"User-Agent": "home-assistant-addons-sync", **(headers or {})}, method=method)
    return urllib.request.urlopen(request, timeout=30)


def repo_tags(repo: str) -> list[str]:
    headers = {"Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    tags, page = [], 1
    while True:
        with _get(f"https://api.github.com/repos/{repo}/tags?per_page=100&page={page}", headers) as response:
            batch = json.load(response)
        tags += [t["name"] for t in batch]
        if len(batch) < 100 or page >= 5:
            return tags
        page += 1


def image_exists(image: str, tag: str) -> bool:
    """Whether the (public) image has this tag, asked of the registry without logging in."""
    host, _, name = image.partition("/")
    token_url = f"https://{host}/token?service={host}&scope={urllib.parse.quote(f'repository:{name}:pull')}"
    with _get(token_url) as response:
        token = json.load(response)["token"]
    try:
        with _get(f"https://{host}/v2/{name}/manifests/{tag}", {"Authorization": f"Bearer {token}", "Accept": MANIFEST_TYPES}, "HEAD"):
            return True
    except urllib.error.HTTPError as error:
        if error.code in (401, 403, 404):
            return False
        raise


def sync(root: Path = ROOT, write: bool = True, tags_of=repo_tags, exists=image_exists) -> list[str]:
    """Raise the versions; returns one line per add-on that changed (or would change)."""
    sources = json.loads((root / "sources.json").read_text(encoding="utf-8"))
    report = []
    for name, source in sorted(sources.items()):
        config_path = root / name / "config.yaml"
        text = config_path.read_text(encoding="utf-8")
        have = current_version(text)
        latest = newest(tags_of(source["repo"]), source["tag"])
        if latest is None or version_key(latest) <= version_key(have):
            continue
        tag = source["image_tag"].format(version=latest)
        if not exists(source["image"], tag):
            report.append(f"{name}: {latest} is released, but the image {source['image']}:{tag} is not published yet; staying on {have}")
            continue
        report.append(f"{name}: {have} -> {latest}")
        if write:
            config_path.write_text(with_version(text, latest), encoding="utf-8")
            changelog = root / name / "CHANGELOG.md"
            changelog.write_text(changelog_with(changelog.read_text(encoding="utf-8"), latest, source["repo"]), encoding="utf-8")
    return report


if __name__ == "__main__":
    lines = sync(write="--check" not in sys.argv[1:])
    print("\n".join(lines) or "All add-ons are on the newest published version.")
