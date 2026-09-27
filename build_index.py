#!/usr/bin/env python3
"""Generate the README gallery and the use-case / family pages from the style manifest."""

from pathlib import Path
import manifest

ROOT = manifest.ROOT
MANIFEST = manifest.load()
START, END = "<!-- styles:start -->", "<!-- styles:end -->"
COLUMNS = 4


def link(kind, key, prefix):
    group = MANIFEST[kind][key]
    folder = "use-cases" if kind == "use_cases" else "families"
    return f"[{group['title']}]({prefix}categories/{folder}/{key}.md)"


def gallery(styles, prefix):
    rows = []
    for i in range(0, len(styles), COLUMNS):
        cells = []
        for s in styles[i:i + COLUMNS]:
            base = f"{prefix}styles/{s['slug']}"
            cells.append(
                f'<td width="25%" align="center"><a href="{base}/{s["slug"]}.mp4">'
                f'<img src="{base}/preview.gif" alt="{s["name"]}" width="100%"></a><br>'
                f'<b>{s["number"]:02d} · {s["name"]}</b><br>'
                f'<a href="{base}/{s["slug"]}.mp4">video</a> · <a href="{base}">source</a></td>')
        rows.append("<tr>\n" + "\n".join(cells) + "\n</tr>")
    return "<table>\n" + "\n".join(rows) + "\n</table>"


def table(styles, prefix):
    lines = ["| # | Style | Feel | Best for | Family | Use cases |",
             "|---|---|---|---|---|---|"]
    for s in styles:
        uses = ", ".join(link("use_cases", u, prefix) for u in s["use_cases"])
        lines.append(
            f"| {s['number']:02d} | [{s['name']}]({prefix}styles/{s['slug']}/) | {s['feel']} "
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
    styles = [s for s in MANIFEST["styles"]
              if (key in s[field] if kind == "use_cases" else s[field] == key)]
    folder = "use-cases" if kind == "use_cases" else "families"
    label = "Use case" if kind == "use_cases" else "Visual family"
    body = (f"# {group['title']}\n\n{label} · {group['description']}\n\n"
            f"[← All styles](../../README.md)\n\n{nav('../../')}\n\n"
            f"{gallery(styles, '../../')}\n\n{table(styles, '../../')}\n")
    path = ROOT / "categories" / folder / f"{key}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body)


def validate():
    for s in MANIFEST["styles"]:
        assert s["family"] in MANIFEST["families"], s["slug"]
        assert all(u in MANIFEST["use_cases"] for u in s["use_cases"]), s["slug"]
        assert (ROOT / "styles" / s["slug"] / "preview.gif").is_file(), s["slug"]


def main():
    validate()
    styles = MANIFEST["styles"]
    for kind in ("use_cases", "families"):
        for key in MANIFEST[kind]:
            if any(key in (s["use_cases"] if kind == "use_cases" else [s["family"]]) for s in styles):
                write_page(kind, key)

    readme = ROOT / "README.md"
    text = readme.read_text()
    head, rest = text.split(START)
    _, tail = rest.split(END)
    block = f"{START}\n{nav('')}\n\n{gallery(styles, '')}\n\n{table(styles, '')}\n{END}"
    readme.write_text(head + block + tail)
    print(f"README + {len(MANIFEST['use_cases']) + len(MANIFEST['families'])} category pages, "
          f"{len(styles)} styles")


if __name__ == "__main__":
    main()
