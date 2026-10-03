"""The agent skill's search, the recipe checks and the catalog it is generated from."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import build_index
import check_catalog
import manifest

SCRIPTS = manifest.SKILL / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "recipes"
STYLES = {s["slug"]: s for s in manifest.load()["styles"]}


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


    def top(self, *query):
        result = subprocess.run([sys.executable, str(SCRIPTS / "find_style.py"), *query],
                                capture_output=True, text=True)
        return [l.split()[0] for l in result.stdout.splitlines() if l and not l.endswith(":")]

    def test_ranking_puts_the_obvious_style_first(self):
        self.assertEqual(self.top("graphite")[0], "pencil-sketch")
        self.assertEqual(self.top("ink")[0], "ink-wash")
        self.assertEqual(set(self.top("anime")[:2]), {"anime-80s", "lofi-anime"})
        self.assertEqual(self.top("explainer", "video", "for", "kids")[0], "felt-stopmotion")
        self.assertEqual(self.top("clay", "stop-motion")[0], "clay")


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

    def check(self, skill_dir, slug):
        problems, notes = [], []
        with patch.object(manifest, "SKILL", skill_dir):
            check_catalog.check_recipe(STYLES[slug], problems, notes)
        return problems

    def test_correct_recipes_pass(self):
        # Code in js/ (cave-painting), three.js 0x colours and vendor/ (low-poly), digit-led hex strings
        # (kawaii, anime-80s), placeholders, font strings and directories.
        for slug in ("cave-painting", "low-poly", "kawaii", "anime-80s", "sunday-strip", "cosmic-epic",
                     "bayeux-tapestry", "neon-sign", "oscilloscope", "nes-8bit", "persian-miniature",
                     "absurd-webcomic", "voxel"):
            with self.subTest(slug=slug):
                self.assertEqual(self.check(FIXTURES / "good", slug), [])

    def test_wrong_recipe_fails(self):
        problems = self.check(FIXTURES / "wrong", "blueprint")
        for expected in ("give the colour value", "hsl(12,80%,50%)", "0x123456", "#fff", "`bogus`",
                         "in backticks", "drawGhostTitle", "loadTitleFont", "drawGhostCard", "`Futura`",
                         "`tone` is not defined in anim.html", "`retro-terminal` is not a style"):
            self.assertTrue(any(expected in p for p in problems), (expected, problems))
        self.assertFalse(any("ground()" in p for p in problems), problems)   # prose after a non-call span

    def test_invented_facts_in_a_correct_recipe_fail(self):
        problems = self.check(FIXTURES / "wrong", "sunday-strip")
        for expected in ("'paper': give the colour value", "`Bangers`", "`whoosh` is not a cue kind",
                         "`brush` is not defined in js/fantasy.js", "`easeOutElastic`", "`SHADOW`"):
            self.assertTrue(any(expected in p for p in problems), (expected, problems))

    def test_fenced_code_is_code_to_write(self):
        recipe = (FIXTURES / "good" / "references" / "styles" / "voxel.md").read_text()
        recipe = recipe.replace("## Adapting\n", "## Adapting\n```js\nfunction drawLogoBlocks(t) { mirroredCallout(t); }\n```\n", 1)
        with tempfile.TemporaryDirectory() as tmp:
            styles = Path(tmp) / "references" / "styles"
            styles.mkdir(parents=True)
            (styles / "voxel.md").write_text(recipe)
            self.assertEqual(self.check(Path(tmp), "voxel"), [])

    def test_shell_commands_cite_skill_scripts_and_style_files(self):
        problems = []
        folder = manifest.ROOT / "styles" / "blueprint"
        check_catalog.cited_names("`python3 <skill>/scripts/check_audio.py audio.wav 4`, `node render.mjs a 30 0 4 1 2`, "
                                  "`<skill>/scripts/contact_sheet.sh`", folder, self.code, problems, "x")
        self.assertEqual(problems, [])
        check_catalog.cited_names("`python3 <skill>/scripts/ghost.py`, `node ghost.mjs`", folder, self.code, problems, "x")
        self.assertEqual(len(problems), 2)

    def test_glsl_definitions_count(self):
        self.assertTrue(check_catalog.defines("nebula", "vec3 nebula(vec3 d){"))
        self.assertTrue(check_catalog.defines("uScol", "uniform vec3 uSd, uScol;"))
        self.assertFalse(check_catalog.defines("ghost", "vec3 nebula(vec3 d){"))

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
        self.assertTrue(build_index.uses_webgl("cave-painting")) # WebGL2 in js/scene.js
        self.assertFalse(build_index.uses_webgl("neon-sign"))    # GPU raster only


class AudioCheckTests(unittest.TestCase):
    """check_audio.py on the shapes audio.py writes: 16-bit stereo, and NaN turned to zeros by astype."""

    def run_check(self, samples, *args, right=None):
        import numpy as np
        import wave
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "audio.wav"
            pcm = (np.clip(np.stack([samples, samples if right is None else right], axis=1), -1, 1) * 32767)
            with wave.open(str(path), "wb") as w:
                w.setnchannels(2); w.setsampwidth(2); w.setframerate(48000)
                w.writeframes(pcm.astype(np.int16).tobytes())
            return subprocess.run([sys.executable, str(SCRIPTS / "check_audio.py"), str(path), *args],
                                  capture_output=True, text=True)

    def test_sound_of_the_right_length_passes(self):
        import numpy as np
        t = np.arange(48000 * 4) / 48000
        result = self.run_check(0.5 * np.sin(2 * np.pi * 440 * t), "4")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("peak 0.500", result.stdout)

    def test_silent_short_or_early_tracks_are_flagged(self):
        import numpy as np
        self.assertIn("silent", self.run_check(np.zeros(48000 * 4)).stdout)
        t = np.arange(48000 * 4) / 48000
        self.assertIn("expected 10.00 s", self.run_check(0.5 * np.sin(2 * np.pi * 440 * t), "10").stdout)
        early = np.where(t < 1.5, 0.5 * np.sin(2 * np.pi * 440 * t), 0)
        self.assertIn("nothing sounds after 1.50 s", self.run_check(early, "4").stdout)
        tone = 0.5 * np.sin(2 * np.pi * 440 * t)
        result = self.run_check(tone, "4", right=np.where(t < 1, tone, 0))   # a NaN zeroed one channel at 1 s
        self.assertIn("channel R goes silent at 1.00 s", result.stdout)
        self.assertEqual(result.returncode, 1)


class FetchTests(unittest.TestCase):
    """fetch_style.py from the local clone: no network needed."""

    def run_fetch(self, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / "fetch_style.py"), *args],
                              capture_output=True, text=True, cwd=manifest.ROOT)

    def test_project_from_local_clone(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "jrpg-test"
            result = self.run_fetch("jrpg", str(dest), "--repo", str(manifest.ROOT), "--no-reference")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((dest / "anim.html").is_file())
            self.assertFalse((dest / "meta.json").exists())
            self.assertTrue(os.access(dest / "build.sh", os.X_OK))
            self.assertIn("python3 audio.py", (dest / "build.sh").read_text())
            self.assertEqual(sorted(x.name for x in (dest / "_licenses").iterdir()),
                             ["Apache-2.0.txt", "FONTS.md", "LICENSE-video-styles.txt", "OFL-1.1.txt"])
            self.assertIn("(styles/jrpg)", (dest / "_licenses" / "FONTS.md").read_text())

    def test_rejects_bad_destinations(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertNotEqual(self.run_fetch("clay", str(Path(tmp) / "my video")).returncode, 0)
        self.assertNotEqual(self.run_fetch("clay", str(manifest.SKILL / "proj")).returncode, 0)
        self.assertFalse((manifest.SKILL / "proj").exists())

    def test_old_uv_line_is_rewritten(self):
        fetch = script("fetch_style")
        old = "node events.mjs && uv run --no-project --with numpy --index-url https://pypi.org/simple python audio.py"
        self.assertEqual(fetch.UV_LINE.sub("python3 audio.py", old), "node events.mjs && python3 audio.py")


if __name__ == "__main__":
    unittest.main()
