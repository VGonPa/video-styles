#!/usr/bin/env python3
"""Generate the README gallery and the use-case / family pages from the style manifest."""

from pathlib import Path
import manifest
import media

ROOT = manifest.ROOT
MANIFEST = manifest.load()
START, END = "<!-- styles:start -->", "<!-- styles:end -->"
COLUMNS = 4


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

    readme = ROOT / "README.md"
    text = readme.read_text()
    head, rest = text.split(START)
    _, tail = rest.split(END)
    # The main gallery is shuffled so no family or era clusters; category pages are alphabetical.
    order = manifest.shuffled(styles)
    block = f"{START}\n{nav('')}\n\n{gallery(order, '')}\n\n{table(order, '')}\n{END}"
    readme.write_text(head + block + tail)
    print(f"README + {len(MANIFEST['use_cases']) + len(MANIFEST['families'])} category pages, "
          f"{len(styles)} styles")


if __name__ == "__main__":
    main()
