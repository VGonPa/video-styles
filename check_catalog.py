#!/usr/bin/env python3
"""Check that every style is complete: metadata, clip specs, preview, and index pages.

Run after build_index.py. Add --media to also validate downloaded or rebuilt clips and GIFs.
"""

import argparse
import builtins
import json
import re
import subprocess
import sys

import build_index
import manifest
import media

ROOT = manifest.ROOT
MANIFEST = manifest.load()
FONTS_MD = (ROOT / "FONTS.md").read_text()
REQUIRED = {"number", "name", "feel", "best_for", "family", "use_cases"}
# Every style folder carries an unmodified copy of these shared scripts from tools/.
SHARED_SCRIPTS = ["render.mjs", "events.mjs"]
# The hand-drawn styles also share tools/common.js.
COMMON_JS_STYLES = {"whiteboard", "chalkboard", "blueprint", "single-line"}
# Headings every recipe keeps, in order (RECIPE_TEMPLATE.md).
RECIPE_HEADINGS = ["Signature", "Palette", "Typography and copy", "Texture and finish", "Shapes, line and figures",
                   "Composition and camera", "Motion", "Film grammar", "Sound", "Reuse map", "Adapting",
                   "Boundaries", "Technical notes"]
SKILL_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
# False while the recipes are being written: a missing recipe is reported but does not fail the check.
RECIPES_REQUIRED = False


def probe(clip):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_type,codec_name,width,height,r_frame_rate,pix_fmt,color_range,sample_rate,channels"
         ":format=duration", "-of", "json", str(clip)],
        capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def check_clip(s, problems):
    clip = ROOT / "styles" / s["slug"] / f"{s['slug']}.mp4"
    if not clip.is_file():
        problems.append("missing clip")
        return
    info = probe(clip)
    video = [x for x in info["streams"] if x["codec_type"] == "video"]
    audio = [x for x in info["streams"] if x["codec_type"] == "audio"]
    duration = float(info["format"]["duration"])
    if not 8 <= duration <= 10.5:
        problems.append(f"duration {duration:.2f}s")
    if not video:
        problems.append("no video stream")
    else:
        v = video[0]
        expected = {"codec_name": "h264", "width": 1920, "height": 1080, "r_frame_rate": "30/1"}
        problems += [f"{k}={v.get(k)}" for k, want in expected.items() if v.get(k) != want]
        # The original clips are encoded full range from JPEG frames.
        if v.get("pix_fmt") != "yuvj420p" and v.get("color_range") != "pc":
            problems.append(f"range {v.get('pix_fmt')}/{v.get('color_range')} (want full range)")
    if not audio:
        problems.append("no audio stream")
    elif audio[0].get("codec_name") != "aac" or audio[0].get("sample_rate") != "48000" \
            or audio[0].get("channels") != 2:
        problems.append("audio is not AAC 48 kHz stereo")


def check_pages(s, problems):
    target = media.url(s["slug"], "preview")
    video = media.url(s["slug"], "video")
    pages = [ROOT / "README.md", ROOT / "categories" / "families" / f"{s['family']}.md"]
    pages += [ROOT / "categories" / "use-cases" / f"{u}.md" for u in s["use_cases"]]
    for page in pages:
        if not page.is_file() or target not in page.read_text() or video not in page.read_text():
            problems.append(f"not listed in {page.relative_to(ROOT)}")
    style_page = ROOT / "styles" / s["slug"] / "README.md"
    if not style_page.is_file() or f"# {s['name']}\n" not in style_page.read_text() \
            or target not in style_page.read_text() or video not in style_page.read_text():
        problems.append("missing or stale styles/<slug>/README.md")


def check_fonts_listed(s, problems):
    fonts = ROOT / "styles" / s["slug"] / "fonts"
    if fonts.is_dir() and any(fonts.iterdir()) and f"(styles/{s['slug']})" not in FONTS_MD:
        problems.append("fonts/ not listed in FONTS.md")


def check_shared_scripts(s, problems):
    folder = ROOT / "styles" / s["slug"]
    build = folder / "build.sh"
    # audio.py needs only python3 + NumPy; other launchers (uv, a private index) break the skill's projects.
    if build.is_file() and "python3 audio.py" not in build.read_text():
        problems.append("build.sh must run `python3 audio.py`")
    names = SHARED_SCRIPTS + (["common.js"] if s["slug"] in COMMON_JS_STYLES else [])
    for name in names:
        copy = folder / name
        if not copy.is_file():
            problems.append(f"missing {name}")
        elif copy.read_bytes() != (ROOT / "tools" / name).read_bytes():
            problems.append(f"{name} differs from tools/{name}")


def style_code(slug):
    """Everything a recipe may cite: the style's own code (see manifest.style_sources)."""
    return "\n".join(f.read_text(errors="ignore") for f in manifest.style_sources(slug))


def section(text, heading):
    match = re.search(rf"^## {re.escape(heading)}[ \t]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return match.group(1) if match else ""


SEPARATOR = re.compile(r"^\|\s*:?-{3,}")
# A fenced code block in a recipe is code the reader writes (a helper the style lacks), so it is not checked.
FENCED = re.compile(r"^```.*?^```[^\n]*$", re.S | re.M)
# The tables the checks read; each must be present with this exact header.
TABLES = {"Palette": ["Role", "Colour", "In code"],
          "Film grammar": ["Time (s)", "What happens", "In code"],
          "Reuse map": ["Piece", "Where", "Call / key params", "Reuse"]}


def table_rows(block):
    """Cells of the body rows of every markdown table in a block (header and separator rows skipped)."""
    lines = [l.strip() for l in block.splitlines()]
    rows = []
    for i, line in enumerate(lines):
        if not line.startswith("|") or SEPARATOR.match(line) \
                or (i + 1 < len(lines) and SEPARATOR.match(lines[i + 1])):
            continue
        rows.append([c.strip() for c in line.strip("|").split("|")])
    return rows


def recipe_table(text, heading, problems):
    """Body rows of a required table, reporting a missing table, a wrong header or short rows."""
    block = section(text, heading)
    headers = [[c.strip() for c in l.strip().strip("|").split("|")] for l in block.splitlines()
               if l.strip().startswith("|") and not SEPARATOR.match(l.strip())]
    if TABLES[heading] not in headers:
        problems.append(f"recipe {heading} needs its table with the header | {' | '.join(TABLES[heading])} |")
        return []
    rows = table_rows(block)
    if not rows:
        problems.append(f"recipe {heading} table has no rows")
    for row in rows:
        if len(row) < len(TABLES[heading]):
            problems.append(f"recipe {heading} row '{row[0]}' has {len(row)} columns, expected {len(TABLES[heading])}")
    return [r for r in rows if len(r) >= len(TABLES[heading])]


COLOUR = re.compile(r"#[0-9a-fA-F]{8}\b|#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3,4}\b|0x[0-9a-fA-F]{6}\b"
                    r"|rgba?\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}|(?<![\w.])\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}(?![\w.])")
# A file or folder path relative to the style folder; `*` globs allowed (`fonts/*.woff2`).
FILE = re.compile(r"(?<![\w./*-])([\w.*][\w.*-]*(?:/[\w.*-]+)*\.(?:html|js|mjs|py|json|css|md|sh|txt|woff2?|ttf|otf|glsl|frag|vert))\b"
                  r"|(?<![\w./*-])(\w[\w-]*(?:/[\w-]+)*/)(?![\w])")
# Members of browser and JavaScript globals (a recipe may say "never `performance.now()`").
GLOBAL_MEMBER = re.compile(r"\b(?:window|document|Math|Date|performance|JSON|Number|Object|Array|String|Promise|"
                           r"console|THREE)\.[\w$]+")


# Calls a recipe may name without the style defining them: CSS and GLSL colour functions, browser built-ins.
CALL_OK = {"rgb", "rgba", "hsl", "hsla", "url", "var", "calc", "vec2", "vec3", "vec4",
           "requestAnimationFrame", "setTimeout", "setInterval", "fetch", "Image",
           # Canvas 2D methods, which a recipe may forbid ("never `arc()`") in a style that never calls them.
           "arc", "arcTo", "bezierCurveTo", "quadraticCurveTo", "moveTo", "lineTo", "ellipse", "rect", "roundRect",
           "fill", "stroke", "clip", "fillText", "strokeText", "measureText", "drawImage", "getImageData",
           "putImageData", "createLinearGradient", "createRadialGradient", "createPattern", "save", "restore",
           "translate", "rotate", "scale", "setTransform"}
PY_BUILTINS = set(vars(builtins)) | {"ndarray"}
SLUGS = {s["slug"] for s in MANIFEST["styles"]}


def rgb_of(colour):
    """(r, g, b) of a #rgb, #rgba, #rrggbb, #rrggbbaa, 0xrrggbb, rgb(…) or bare r,g,b colour."""
    c = colour.strip().lower()
    if c.startswith("#") or c.startswith("0x"):
        h = c[1:] if c.startswith("#") else c[2:]
        h = "".join(ch * 2 for ch in h) if len(h) in (3, 4) else h
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    return tuple(int(x) for x in re.findall(r"\d+", c)[:3])


def colour_in_code(colour, code, flat):
    """True if the code writes this colour in any form: #rrggbb, #rgb, 0xrrggbb or r,g,b (whole numbers)."""
    r, g, b = rgb_of(colour)
    h = f"{r:02x}{g:02x}{b:02x}"
    forms = [rf"#{h}(?:[0-9a-f]{{2}})?(?![0-9a-f])", rf"0x{h}(?![0-9a-f])"]     # alpha suffix allowed
    if h[0] == h[1] and h[2] == h[3] and h[4] == h[5]:
        forms.append(rf"#{h[0]}{h[2]}{h[4]}[0-9a-f]?(?![0-9a-f])")
    lower = code.lower()
    return any(re.search(f, lower) for f in forms) or bool(re.search(rf"(?<![\d.]){r},{g},{b}(?![\d.])", flat))


COMMAND = re.compile(r"\s*(?:python3|bash|node|cd|KEYS=\S*|DUR=\S*|WORKERS=\S*)\s")
SKILL_SCRIPT = re.compile(r"(?:<skill>/)?scripts/([\w.-]+\.(?:py|sh))")


def cited_names(cell, folder, code, problems, where):
    """Files, folders and identifiers in a cell's backticks must exist in the style. A shell command
    (`python3 <skill>/scripts/check_audio.py audio.wav 4`) is checked for the files it names only: the skill's
    scripts in the skill, the rest in the style."""
    for token in re.findall(r"`([^`]+)`", cell):
        if COMMAND.match(token + " ") or "<skill>/" in token:
            for name in SKILL_SCRIPT.findall(token):
                if not (manifest.SKILL / "scripts" / name).is_file():
                    problems.append(f"recipe {where} cites missing skill script scripts/{name}")
            for found in FILE.finditer(SKILL_SCRIPT.sub(" ", token)):
                path = found.group(1) or found.group(2)
                if path.endswith((".mjs", ".html", ".js")) and not (folder / path).exists():
                    problems.append(f"recipe {where} cites missing file {path}")
            continue
        for found in FILE.finditer(token):
            path = found.group(1) or found.group(2)
            if not (any(folder.glob(path)) if "*" in path else (folder / path).exists()):
                problems.append(f"recipe {where} cites missing file {path}")
        token = FILE.sub(" ", token)
        token = re.sub(r"<[^<>]*>", " ", token)                    # placeholders such as T.<beat>
        token = re.sub(r"'[^']*'|\"[^\"]*\"", lambda m: " " + " ".join(re.findall(r"(?<![\w$])[A-Za-z_$][\w$]*", m.group(0)))
                       if not COLOUR.search(m.group(0)) else " ", token)   # keep words in strings (not 64px), drop colours
        token = GLOBAL_MEMBER.sub(" ", COLOUR.sub(" ", token))
        # Numbers with their unit (`12 fps`, `4 px`) and hyphenated keywords (`ease-out`) are not code names.
        token = re.sub(r"0x[0-9a-fA-F]+|(?<![\w$])\d[\w.%]*(?:\s+[A-Za-z]+\b)?", " ", token)
        token = re.sub(r"(?<![\w$-])[A-Za-z]+(?:-[A-Za-z]+)+(?![\w$-])", " ", token)
        for ident in re.findall(r"[A-Za-z_$][\w$]*", token):
            if len(ident) > 1 and ident not in SLUGS and ident not in PY_BUILTINS and ident not in CALL_OK \
                    and not re.search(rf"(?<![\w$]){re.escape(ident)}(?![\w$])", code):
                problems.append(f"recipe {where} cites `{ident}`, not found in the code")


def expression_in_code(expr, code):
    """True if the code contains this expression, ignoring whitespace, as a whole (not inside a longer name)."""
    body = r"\s*".join(re.escape(ch) for ch in re.sub(r"\s+", "", expr))
    return bool(re.search(rf"(?<![\w$]){body}(?![\w$])", code))


def defines(name, text):
    """True if the text defines name: a function, class, variable, method, object key, Python def, or a GLSL
    function or uniform."""
    n = re.escape(name)
    glsl = r"(?:void|float|int|bool|[biu]?vec[234]|mat[234])"
    return bool(re.search(rf"\bfunction\s*\*?\s*{n}\b|\bclass\s+{n}\b|(?<![\w$]){n}\s*[:=](?!=)"
                          rf"|^\s*(?:async\s+)?{n}\s*\([^)]*\)\s*\{{|\bdef\s+{n}\b"
                          rf"|^\s*(?:(?:highp|mediump|lowp)\s+)?{glsl}\s+{n}\s*\("          # GLSL function
                          rf"|\buniform\s+\w+\s+(?:\w+\s*,\s*)*{n}\b", text, re.M))      # GLSL uniform


def names_in_named_file(cell, folder, problems, where):
    """In `path` → `name`, that file must define the name (where it lives), not merely use it."""
    for path, target in re.findall(r"`([\w./-]+\.(?:html|js|mjs|py|css|json|glsl|frag|vert))`\s*→\s*`([^`]+)`", cell):
        source = folder / path
        if source.is_file():
            text = source.read_text(errors="ignore")
            target = re.sub(r"^\s*(?:window|document|globalThis)\.", "", target)
            name = re.match(r"\s*([A-Za-z_$][\w$]*)", target)       # `name(args)` or `name.key` → name
            if name and len(name.group(1)) > 1 and not defines(name.group(1), text):
                problems.append(f"recipe {where}: `{name.group(1)}` is not defined in {path}")


def check_sound(slug, text, problems):
    """Cue kinds and fields named in Sound must be strings that audio.py (or render.json) reads: a cue that only
    anim.html mentions is silent in the film. audio.py's own variables and functions (`bars`, `wet`) are fine
    unless the film also emits that name as a cue."""
    folder = ROOT / "styles" / slug
    audio = (folder / "audio.py").read_text() if (folder / "audio.py").is_file() else ""
    reads = audio + "\n" + ((folder / "render.json").read_text() if (folder / "render.json").is_file() else "")
    film = "\n".join(f.read_text(errors="ignore") for f in manifest.style_sources(slug) if f.suffix != ".py")
    for token in re.findall(r"`([^`]+)`", section(text, "Sound")):
        if not re.fullmatch(r"[a-z_][a-z0-9_]+", token):
            continue        # calls, files, expressions, constants and one-letter fields
        if re.search(rf"^\s*(?:import|from)\b.*\b{token}\b", reads, re.M):
            continue        # a module audio.py imports (`wave`)
        if re.search(rf"['\"]{token}['\"]", reads):
            continue        # a cue kind or field audio.py reads
        if defines(token, audio) and not re.search(rf"['\"`]{token}['\"`]", film):
            continue        # audio.py's own variable or function, not a cue the film emits
        problems.append(f"recipe sound: `{token}` is not a cue kind or field audio.py reads; "
                        "write functions as `name()`")


def check_palette(text, folder, code, names, problems):
    flat = re.sub(r"\s+", "", code)
    for row in recipe_table(text, "Palette", problems):
        role, cell = row[0], row[1]
        colours = COLOUR.findall(cell)
        for colour in colours:
            if not colour_in_code(colour, code, flat):
                problems.append(f"recipe palette colour {colour.strip()} ({role}) not found in the code")
        if not colours:
            # A computed colour: its expression, in backticks, must appear in the code as written.
            literals = [re.sub(r"\s+", "", lit) for lit in re.findall(r"`([^`]+)`", cell)]
            expressions = [lit for lit in literals if re.search(r"[(\[,]", lit)]
            if not expressions:
                problems.append(f"recipe palette row '{role}': give the colour value or the expression that computes it")
            elif not any(expression_in_code(lit, code) for lit in expressions):
                problems.append(f"recipe palette row '{role}': {expressions[0]} not found in the code")
        cited_names(row[2], folder, names, problems, "palette")


def check_recipe(s, problems, notes):
    recipe = manifest.SKILL / "references" / "styles" / f"{s['slug']}.md"
    if not recipe.is_file():
        (problems if RECIPES_REQUIRED else notes).append("no recipe")
        return
    text = recipe.read_text()
    if not text.startswith(f"# {s['name']} (`{s['slug']}`)\n"):
        problems.append("recipe title must be '# <name> (`<slug>`)'")
    found = re.findall(r"^## (.+?)\s*$", text, re.M)
    if found != RECIPE_HEADINGS:
        problems.append(f"recipe headings {found} differ from RECIPE_TEMPLATE.md")
        return
    # Derived from the code: cited files, identifiers and colours must exist in the style's code.
    folder, code = ROOT / "styles" / s["slug"], style_code(s["slug"])
    # Identifiers may also be library API the reader finds in vendor/ (three.js); colours must be the style's own.
    names = code + "\n" + "\n".join(f.read_text(errors="ignore") for f in sorted((folder / "vendor").glob("*.js")))
    check_palette(text, folder, code, names, problems)
    for row in recipe_table(text, "Film grammar", problems):
        cited_names(row[2], folder, names, problems, "film grammar")
    for row in recipe_table(text, "Reuse map", problems):
        if "`" not in row[1]:
            problems.append(f"recipe reuse map row '{row[0]}': put where it lives in backticks")
        cited_names(row[1], folder, names, problems, "reuse map")
        cited_names(row[2], folder, names, problems, "reuse map")
        cited_names(row[3], folder, names, problems, "reuse map")
        names_in_named_file(row[1], folder, problems, "reuse map")
    # Names in backticks in the prose sections are facts the reader acts on (Technical notes stays out: it
    # names things a style lacks, such as "no `render.json`").
    for heading in ("Signature", "Palette", "Typography and copy", "Texture and finish", "Shapes, line and figures",
                    "Composition and camera", "Motion", "Film grammar", "Sound", "Adapting"):
        prose = "\n".join(l for l in FENCED.sub("", section(text, heading)).splitlines()
                          if not l.lstrip().startswith("|"))
        cited_names(prose, folder, names, problems, heading.split(",")[0].split()[0].lower())
    check_sound(s["slug"], text, problems)
    # "Poor fit: use `x`" sends the reader to another style, which must exist.
    for token in re.findall(r"`([^`]+)`", section(text, "Boundaries")):
        if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", token) and token not in SLUGS:
            problems.append(f"recipe boundaries: `{token}` is not a style in the catalog")
    # Calls in backticks anywhere, tables included (`drawTitle()`), must exist; each code span is checked whole.
    prose = FENCED.sub("", text)
    for span in re.findall(r"`([^`\n]+)`", prose):
        span = GLOBAL_MEMBER.sub(" ", re.sub(r"'[^']*'|\"[^\"]*\"", " ", span))
        for call in re.findall(r"([A-Za-z_$][\w$]*)\s*\(", span):
            if call not in CALL_OK and call not in PY_BUILTINS \
                    and not re.search(rf"(?<![\w$]){re.escape(call)}(?![\w$])", names):
                problems.append(f"recipe cites `{call}()`, not found in the code")
    problems[:] = list(dict.fromkeys(problems))    # one report per wrong name


def check_skill():
    """The agent skill: Agent Skills frontmatter, a catalog that covers every style, its own links."""
    problems = []
    skill = manifest.SKILL
    text = (skill / "SKILL.md").read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return ["SKILL.md has no frontmatter"]
    front, parent = {}, None
    for line in match.group(1).splitlines():
        key = re.match(r"^([A-Za-z0-9_-]+):[ \t]*(.*)$", line)
        if key:
            parent = key.group(1)
            value = key.group(2).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
                value = value[1:-1]
            front[parent] = value
        elif line.strip() and parent != "metadata":
            problems.append(f"frontmatter {parent} continues on another line; keep it on one line")
    problems += [f"frontmatter key {k!r} is not in the Agent Skills spec" for k in front if k not in SKILL_KEYS]
    problems += [f"frontmatter {k} uses a block scalar; write it on one line" for k, v in front.items()
                 if v in {">", "|", ">-", "|-", ">+", "|+"}]
    if front.get("name") != skill.name:
        problems.append(f"name {front.get('name')!r} must match the folder {skill.name!r}")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", front.get("name", "")) or len(front.get("name", "")) > 64:
        problems.append("name must be lowercase words joined by single hyphens, at most 64 characters")
    if not 0 < len(front.get("description", "")) <= 1024:
        problems.append("description must be 1-1024 characters")
    if len(front.get("compatibility", "")) > 500:
        problems.append("compatibility must be at most 500 characters")
    if len(text.splitlines()) > 500:
        problems.append("SKILL.md is over 500 lines")
    for ref in sorted(set(re.findall(r"`((?:scripts|references|assets)/[\w./-]+)`", text))):
        if "<" not in ref and not (skill / ref).exists():
            problems.append(f"SKILL.md mentions missing {ref}")
    catalog_json, catalog_md = build_index.skill_catalog()
    for name, want in (("assets/catalog.json", catalog_json), ("references/catalog.md", catalog_md)):
        path = skill / name
        if not path.is_file() or path.read_text() != want:
            problems.append(f"{name} is stale: run build_index.py")
    ref = build_index.SKILL_CODE_REF
    if ref != "main":
        if subprocess.run(["git", "rev-parse", "--verify", "--quiet", f"refs/tags/{ref}"],
                          capture_output=True, cwd=ROOT).returncode:
            problems.append(f"SKILL_CODE_REF {ref} is not a tag in this clone")
        else:
            for s in MANIFEST["styles"]:
                recipe = skill / "references" / "styles" / f"{s['slug']}.md"
                if recipe.is_file() and subprocess.run(["git", "diff", "--quiet", ref, "HEAD", "--",
                                                        f"styles/{s['slug']}"], cwd=ROOT).returncode:
                    problems.append(f"recipe for {s['slug']} describes code newer than {ref}; cut a new tag")
    for link in (".claude/skills", ".agents/skills"):
        path = ROOT / link / skill.name
        if not path.is_symlink() or path.resolve() != skill.resolve():
            problems.append(f"{link}/{skill.name} must be a symlink to skills/{skill.name}")
    return problems


# The unlicensed original catalog; our code must not carry it forward. A tag rather than a
# commit hash, so it survives history rewrites (git filter-repo rewrites tags with the commits).
ORIGINAL = "original-catalog"


def require_original():
    """Fail loudly when the original is unreachable: without it the derived-code check is void."""
    found = subprocess.run(["git", "rev-parse", "--verify", "--quiet", f"{ORIGINAL}^{{commit}}"],
                           capture_output=True, cwd=ROOT).returncode == 0
    if not found:
        sys.exit(f"tag {ORIGINAL} not found: run `git fetch --tags` (a full, non-shallow clone "
                 "is needed to check styles against the original catalog)")


def derived_lines(slug):
    """Lines (over 15 chars) of anim.html that also appear in the original catalog's version."""
    try:
        old = subprocess.run(["git", "show", f"{ORIGINAL}:styles/{slug}/anim.html"],
                             capture_output=True, text=True, check=True, cwd=ROOT).stdout
    except subprocess.CalledProcessError:
        return 0  # style not in the original
    orig = {l.strip() for l in old.splitlines() if len(l.strip()) > 15}
    cur = (ROOT / "styles" / slug / "anim.html").read_text().splitlines()
    return sum(1 for l in cur if l.strip() in orig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--media", action="store_true", help="also probe local clips and check GIFs")
    args = parser.parse_args()
    media.load()
    require_original()
    failed = False
    missing_recipes = 0
    for s in MANIFEST["styles"]:
        problems, notes = [], []
        missing = REQUIRED - s.keys()
        if missing:
            problems.append(f"meta.json missing {sorted(missing)}")
        if s.get("family") not in MANIFEST["families"]:
            problems.append(f"unknown family {s.get('family')}")
        problems += [f"unknown use case {u}" for u in s.get("use_cases", [])
                     if u not in MANIFEST["use_cases"]]
        if args.media and not (ROOT / "styles" / s["slug"] / "preview.gif").is_file():
            problems.append("missing preview.gif")
        check_shared_scripts(s, problems)
        if args.media:
            check_clip(s, problems)
        check_pages(s, problems)
        if (n := derived_lines(s["slug"])) > 5:
            problems.append(f"{n} lines shared with the original catalog")
        check_fonts_listed(s, problems)
        check_recipe(s, problems, notes)
        missing_recipes += bool(notes)
        status = "ok" if not problems else "; ".join(problems)
        failed |= bool(problems)
        print(f"{s['number']:02d} {s['slug']:<20} {status}")
    skill_problems = check_skill()
    failed |= bool(skill_problems)
    print(f"skill {manifest.SKILL.name} " + ("ok" if not skill_problems else "; ".join(skill_problems)))
    if missing_recipes:
        print(f"note: {missing_recipes} styles have no recipe yet (see RECIPE_TEMPLATE.md)")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
