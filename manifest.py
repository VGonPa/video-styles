"""Load the style catalog: groups from styles.json, one styles/<slug>/meta.json per style."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def load():
    manifest = json.loads((ROOT / "styles.json").read_text())
    styles = [{"slug": meta.parent.name, **json.loads(meta.read_text())}
              for meta in (ROOT / "styles").glob("*/meta.json")]
    manifest["styles"] = sorted(styles, key=lambda s: s["number"])
    numbers = [s["number"] for s in manifest["styles"]]
    assert len(numbers) == len(set(numbers)), f"duplicate style numbers: {numbers}"
    return manifest
