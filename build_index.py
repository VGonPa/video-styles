#!/usr/bin/env python3
"""Generate the README gallery, the use-case / family pages and the skill's catalog from the style manifest."""

import json
from pathlib import Path
import manifest
import media

ROOT = manifest.ROOT
MANIFEST = manifest.load()
START, END = "<!-- styles:start -->", "<!-- styles:end -->"
COLUMNS = 4
REPO = "VGonPa/video-styles"


def link(kind, key, prefix):
    group = MANIFEST[kind][key]
    folder = "use-cases" if kind == "use_cases" else "families"
    return f"[{group['title']}]({prefix}categories/{folder}/{key}.md)"


def credits(s, prefix, sep=" · "):
    parts = []
    for c in s.get("credits", []):
        name = f'<a href="{c["url"]}">{c["name"]}</a>' if "url" in c else c["name"]
        parts.append(f'{c["role"]} {name}')
    return sep.join(parts)


def gallery(styles, prefix):
    rows = []
    for i in range(0, len(styles), COLUMNS):
        cells = []
        for s in styles[i:i + COLUMNS]:
            base = f"{prefix}styles/{s['slug']}"
            video = media.url(s["slug"], "video")
            preview = media.url(s["slug"], "preview")
            cells.append(
                f'<td width="25%" align="center"><a href="{video}">'
                f'<img src="{preview}" alt="{s["name"]}" width="100%"></a><br>'
                f'<b>{s["name"]}</b><br>'
                + (f'<sub>{credits(s, prefix, "<br>")}</sub><br>' if s.get("credits") else "")
                + f'<a href="{video}">video</a> · <a href="{base}">source</a></td>')
        rows.append("<tr>\n" + "\n".join(cells) + "\n</tr>")
    return "<table>\n" + "\n".join(rows) + "\n</table>"


def table(styles, prefix):
    lines = ["| Style | Feel | Best for | Family | Use cases |",
             "|---|---|---|---|---|"]
    for s in styles:
        uses = ", ".join(link("use_cases", u, prefix) for u in s["use_cases"])
        lines.append(
            f"| [{s['name']}]({prefix}styles/{s['slug']}/) | {s['feel']} "
            f"| {s['best_for']} | {link('families', s['family'], prefix)} | {uses} |")
    return "\n".join(lines)


def nav(prefix):
    def row(kind):
        items = []
        for key in MANIFEST[kind]:
            count = sum(key in (s["use_cases"] if kind == "use_cases" else [s["family"]])
                        for s in MANIFEST["styles"])
            if count:
                items.append(f"{link(kind, key, prefix)} ({count})")
        return " · ".join(items)
    return f"**By use case:** {row('use_cases')}\n\n**By visual family:** {row('families')}"


def write_page(kind, key):
    group = MANIFEST[kind][key]
    field = "use_cases" if kind == "use_cases" else "family"
    styles = manifest.alphabetical([s for s in MANIFEST["styles"]
                                    if (key in s[field] if kind == "use_cases" else s[field] == key)])
    folder = "use-cases" if kind == "use_cases" else "families"
    label = "Use case" if kind == "use_cases" else "Visual family"
    body = (f"# {group['title']}\n\n{label} · {group['description']}\n\n"
            f"[← All styles](../../README.md)\n\n{nav('../../')}\n\n"
            f"{gallery(styles, '../../')}\n\n{table(styles, '../../')}\n")
    path = ROOT / "categories" / folder / f"{key}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body)


def write_style_page(s):
    """styles/<slug>/README.md: what GitHub shows when someone opens the style's folder."""
    folder = ROOT / "styles" / s["slug"]
    uses = ", ".join(link("use_cases", u, "../../") for u in s["use_cases"])
    files = [f"[`anim.html`](anim.html)"]
    if (folder / "build.sh").is_file():
        files.append("rebuild with `./build.sh`")
    lines = [f"# {s['name']}", "", "[← All styles](../../README.md)", "",
             f'<a href="{media.url(s["slug"], "video")}"><img src="{media.url(s["slug"], "preview")}" alt="{s["name"]}" width="640"></a>', "",
             f"**Feel:** {s['feel']}  ", f"**Best for:** {s['best_for']}  ",
             f"**Visual family:** {link('families', s['family'], '../../')}  ",
             f"**Use cases:** {uses}", ""]
    if s.get("credits"):
        lines += ["**Credits:** " + credits(s, "../../"), ""]
    lines += [f"▶ [Watch the clip]({media.url(s['slug'], 'video')}) · Source: " + " · ".join(files), ""]
    (folder / "README.md").write_text("\n".join(lines))


# Git ref an installed copy of the skill downloads style code from. Keep "main" until a release tag is cut
# with the skill (see skills/README.md, "Release"), then set it to that tag so recipes and code stay in step.
SKILL_CODE_REF = "main"


def uses_webgl(slug):
    """True when the style draws with WebGL (raw or three.js), which renders slowly without a GPU."""
    code = "".join(f.read_text(errors="ignore") for f in manifest.style_sources(slug))
    return "getContext('webgl" in code or 'getContext("webgl' in code or "THREE." in code


def skill_catalog():
    """The agent skill's style index: (assets/catalog.json, references/catalog.md) as text."""
    skill = manifest.SKILL
    styles = MANIFEST["styles"]
    entries = []
    for s in styles:
        render = ROOT / "styles" / s["slug"] / "render.json"
        entries.append({
            "slug": s["slug"], "number": s["number"], "name": s["name"], "feel": s["feel"],
            "best_for": s["best_for"], "family": s["family"], "use_cases": s["use_cases"],
            "credits": [manifest.credit_text(c) for c in s.get("credits", [])],
            "webgl": uses_webgl(s["slug"]),
            "render": json.loads(render.read_text()) if render.is_file() else {},
            "recipe": (skill / "references" / "styles" / f"{s['slug']}.md").is_file(),
            "preview": media.url(s["slug"], "preview"), "video": media.url(s["slug"], "video"),
        })
    data = {"repository": REPO, "ref": SKILL_CODE_REF,
            "use_cases": {k: {"title": v["title"], "description": v["description"]}
                          for k, v in MANIFEST["use_cases"].items()},
            "families": {k: {"title": v["title"], "description": v["description"]}
                         for k, v in MANIFEST["families"].items()},
            "styles": entries}
    by_slug = {e["slug"]: e for e in entries}

    families = [(k, f) for k, f in MANIFEST["families"].items() if any(s["family"] == k for s in styles)]
    lines = ["# Style catalog", "",
             f"{len(styles)} styles, grouped by visual family. Each line: `slug` **name** — feel. Best for … "
             "· use cases · credits · markers. Markers: *WebGL* (renders slowly without a GPU), "
             "*no recipe yet* (work from the code; see SKILL.md step 3). The recipe for a style is "
             "`styles/<slug>.md` next to this file. Generated by `build_index.py`; do not edit by hand.", "",
             "Families: " + " · ".join(f"{f['title']} ({sum(s['family'] == k for s in styles)})"
                                       for k, f in families), "",
             "Use cases: " + " · ".join(f"`{k}` {v['title']}" for k, v in MANIFEST["use_cases"].items()), ""]
    for key, family in families:
        lines += [f"## {family['title']} (`{key}`)", "", family["description"], ""]
        for s in manifest.alphabetical([s for s in styles if s["family"] == key]):
            extra = [manifest.credit_text(c) for c in s.get("credits", [])]
            extra += ["*WebGL*"] if by_slug[s["slug"]]["webgl"] else []
            extra += [] if by_slug[s["slug"]]["recipe"] else ["*no recipe yet*"]
            lines.append(f"- `{s['slug']}` **{s['name']}** — {s['feel']}. Best for {s['best_for'][0].lower()}"
                         f"{s['best_for'][1:]} · {', '.join(s['use_cases'])}"
                         + "".join(f" · {x}" for x in extra))
        lines.append("")
    return json.dumps(data, indent=1, ensure_ascii=False) + "\n", "\n".join(lines)


def write_skill_catalog():
    catalog_json, catalog_md = skill_catalog()
    (manifest.SKILL / "assets").mkdir(parents=True, exist_ok=True)
    (manifest.SKILL / "assets" / "catalog.json").write_text(catalog_json)
    (manifest.SKILL / "references").mkdir(parents=True, exist_ok=True)
    (manifest.SKILL / "references" / "catalog.md").write_text(catalog_md)


def validate():
    media.load()
    for s in MANIFEST["styles"]:
        assert s["family"] in MANIFEST["families"], s["slug"]
        assert all(u in MANIFEST["use_cases"] for u in s["use_cases"]), s["slug"]
        for c in s.get("credits", []):
            assert {"role", "name"} <= c.keys() <= {"role", "name", "url"}, s["slug"]


def main():
    validate()
    styles = MANIFEST["styles"]
    for s in styles:
        write_style_page(s)
    for kind in ("use_cases", "families"):
        for key in MANIFEST[kind]:
            if any(key in (s["use_cases"] if kind == "use_cases" else [s["family"]]) for s in styles):
                write_page(kind, key)

    write_skill_catalog()

    readme = ROOT / "README.md"
    text = readme.read_text()
    head, rest = text.split(START)
    _, tail = rest.split(END)
    # The main gallery is shuffled so no family or era clusters; category pages are alphabetical.
    order = manifest.shuffled(styles)
    block = f"{START}\n{nav('')}\n\n{gallery(order, '')}\n\n{table(order, '')}\n{END}"
    readme.write_text(head + block + tail)
    print(f"README + {len(MANIFEST['use_cases']) + len(MANIFEST['families'])} category pages + skill catalog, "
          f"{len(styles)} styles")


if __name__ == "__main__":
    main()
