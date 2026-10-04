"""Load the style catalog: groups from styles.json, one styles/<slug>/meta.json per style."""

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
# The agent skill that teaches other agents to reuse these styles (see skills/README.md).
SKILL = ROOT / "skills" / "animating-in-video-styles"


def load():
    manifest = json.loads((ROOT / "styles.json").read_text())
    styles = [{"slug": meta.parent.name, **json.loads(meta.read_text())}
              for meta in (ROOT / "styles").glob("*/meta.json")]
    manifest["styles"] = sorted(styles, key=lambda s: s["number"])
    numbers = [s["number"] for s in manifest["styles"]]
    assert len(numbers) == len(set(numbers)), f"duplicate style numbers: {numbers}"
    return manifest


# Files that hold a style's own code (anim.html, its scripts, shaders, audio.py, fonts.css, render.json).
CODE_SUFFIXES = {".html", ".js", ".mjs", ".py", ".css", ".json", ".glsl", ".frag", ".vert"}
NOT_STYLE_CODE = {"render.mjs", "events.mjs", "meta.json", "events.json"}


def style_sources(slug):
    """Every file of the style's own code, in subfolders too (some styles keep scripts in js/), without the
    shared scripts, generated files, fonts and vendored libraries."""
    folder = ROOT / "styles" / slug
    return sorted(f for f in folder.rglob("*")
                  if f.is_file() and f.suffix in CODE_SUFFIXES and f.name not in NOT_STYLE_CODE
                  and not {"vendor", "fonts"} & set(f.relative_to(folder).parts[:-1]))


def shuffled(styles):
    """Random-looking but stable order: a new style lands in place without reshuffling the rest."""
    return sorted(styles, key=lambda s: hashlib.sha256(s["slug"].encode()).hexdigest())


def alphabetical(styles):
    return sorted(styles, key=lambda s: s["name"].casefold())


def credit_text(credit):
    """Plain-text credit line, e.g. 'Originally developed by Yasin Özmen'."""
    return f"{credit['role']} {credit['name']}"
