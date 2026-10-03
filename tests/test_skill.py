"""The agent skill's search, the recipe checks and the catalog it is generated from."""

import importlib.util
import json
from pathlib import Path
import unittest

import build_index
import check_catalog
import manifest

SCRIPTS = manifest.SKILL / "scripts"


def script(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SearchTests(unittest.TestCase):
    find = script("find_style")

    def test_words_split_hyphens_and_possessives(self):
        self.assertEqual(self.find.words("Clay stop-motion, Wes Anderson's"),
                         ["clay", "stop", "motion", "wes", "anderson"])

    def test_prefix_matches_related_words_only(self):
        hit = self.find.hit
        self.assertTrue(hit("science", {"scientific"}))
        self.assertTrue(hit("math", {"mathematical"}))
        self.assertTrue(hit("children", {"child"}))
        self.assertFalse(hit("data", {"dark"}))
        self.assertFalse(hit("noir", {"noise"}))
        self.assertFalse(hit("art", {"artist"}))


class RecipeCheckTests(unittest.TestCase):
    code = "const LN = '232,241,255'; const BG = '#1F5AA6'; function dimension(vertical, at) {}"
    flat = code.replace(" ", "")

    def test_colours_match_hex_or_rgb_numbers(self):
        ok = check_catalog.colour_in_code
        self.assertTrue(ok("#1f5aa6", self.code, self.flat))
        self.assertTrue(ok("#e8f1ff", self.code, self.flat))          # 232,241,255
        self.assertTrue(ok("rgb(31, 90, 166)", self.code, self.flat))  # #1f5aa6
        self.assertFalse(ok("#123456", self.code, self.flat))

    def test_cited_identifiers_must_exist(self):
        problems = []
        folder = manifest.ROOT / "styles" / "blueprint"
        check_catalog.cited_names("`anim.html` → `dimension(vertical, at)`", folder, self.code, problems, "x")
        self.assertEqual(problems, [])
        check_catalog.cited_names("`ghost.js`, `nope(at)`", folder, self.code, problems, "x")
        self.assertEqual(len(problems), 2)

    def test_template_and_checker_agree_on_headings(self):
        template = (manifest.ROOT / "RECIPE_TEMPLATE.md").read_text()
        block = template.split("```markdown", 1)[1].split("```", 1)[0]
        headings = [l[3:].strip() for l in block.splitlines() if l.startswith("## ")]
        self.assertEqual(headings, check_catalog.RECIPE_HEADINGS)


class CatalogTests(unittest.TestCase):
    def test_skill_catalog_covers_every_style(self):
        catalog_json, catalog_md = build_index.skill_catalog()
        data = json.loads(catalog_json)
        slugs = [s["slug"] for s in manifest.load()["styles"]]
        self.assertEqual([s["slug"] for s in data["styles"]], slugs)
        for slug in slugs:
            self.assertIn(f"- `{slug}` ", catalog_md)

    def test_webgl_detection(self):
        self.assertTrue(build_index.uses_webgl("low-poly"))      # three.js
        self.assertTrue(build_index.uses_webgl("liquid-glass"))  # raw WebGL2, no render.json
        self.assertFalse(build_index.uses_webgl("neon-sign"))    # GPU raster only


if __name__ == "__main__":
    unittest.main()
