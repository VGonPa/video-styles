"""Pinned release assets: the gallery works without downloading rendered media."""

from functools import lru_cache
import json
import re

import manifest


@lru_cache(maxsize=1)
def load():
    data = json.loads((manifest.ROOT / "media.json").read_text())
    assert data["base_url"] == (
        "https://github.com/VGonPa/video-styles/releases/download/" + data["release"]
    ), "media must use the pinned public release"
    slugs = {s["slug"] for s in manifest.load()["styles"]}
    assert set(data["styles"]) == slugs, "release assets must cover every style"
    for slug, assets in data["styles"].items():
        assert set(assets) == {"video", "preview"}, slug
        for kind, item in assets.items():
            expected = slug + (".mp4" if kind == "video" else "-preview.gif")
            assert item["file"] == expected, slug
            assert isinstance(item["size"], int) and item["size"] > 0, slug
            assert re.fullmatch(r"[0-9a-f]{64}", item["sha256"]), slug
    return data


def asset(slug, kind):
    return load()["styles"][slug][kind]


def url(slug, kind):
    return load()["base_url"] + "/" + asset(slug, kind)["file"]
