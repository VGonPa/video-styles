#!/usr/bin/env python3
"""Search the style catalog by words, use case, family or render needs.

  python3 scripts/find_style.py ukiyo                    # a style by (part of) its name, slug or credit
  python3 scripts/find_style.py --use-case explainer --family technical
  python3 scripts/find_style.py kids science             # every word, or a word sharing its first 4+ letters
  python3 scripts/find_style.py --no-gpu --use-case social
  python3 scripts/find_style.py --list                   # families and use cases with their counts
  python3 scripts/find_style.py --json clay              # full entries, including preview and video URLs

Words are matched against the slug, name, feel, "best for", credits, family and use cases; filler words
("a", "for", "video", "style"…) are ignored. Pass one to three content words, not a sentence. When no style
matches every word, the closest partial matches are listed instead (exit code 1). Needs only Python 3.8+; reads
../assets/catalog.json, which the catalog repository generates.
"""

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path

CATALOG = Path(__file__).resolve().parent.parent / "assets" / "catalog.json"
# Words that say nothing about a style; dropped from queries such as "an explainer video for kids".
STOPWORDS = {"a", "an", "the", "for", "of", "to", "and", "or", "in", "on", "with", "about", "my", "our", "your",
             "video", "videos", "clip", "clips", "style", "styles", "animation", "animated", "something", "like"}
SYNONYMS = {"children": "kids", "child": "kids", "kid": "kids", "childrens": "kids"}


def load():
    try:
        return json.loads(CATALOG.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"catalog not found at {CATALOG}; reinstall the skill or run build_index.py in the repository")


def words(text):
    return [SYNONYMS.get(w, w) for w in re.findall(r"[a-z0-9]+", text.casefold().replace("’", "'").replace("'s", ""))]


def name_tokens(style):
    """Words of the style's slug and name (they rank highest)."""
    return set(words(f"{style['slug']} {style['name']}"))


def own_tokens(style):
    """Words that describe the style itself."""
    return set(words(" ".join([style["feel"], style["best_for"], *style["credits"]])))


def context_tokens(style, catalog):
    """Words it shares with its whole family or use cases (they rank below the style's own words)."""
    family = catalog["families"][style["family"]]
    return set(words(" ".join([style["family"], family["title"], family["description"], *style["use_cases"],
                               *(catalog["use_cases"][u]["title"] for u in style["use_cases"])])))


def match(word, toks):
    """1 for an exact word, 0.6 for a related one (one is a prefix of the other, or they share five or more
    leading letters covering all but the last two of the shorter: science ~ scientific, child ~ children,
    not anime ~ animals), else 0."""
    if word in toks:
        return 1.0
    if len(word) < 4:
        return 0.0
    for t in toks:
        if len(t) >= 4 and (t.startswith(word) or word.startswith(t)):
            return 0.6
        if len(os.path.commonprefix([word, t])) >= max(5, min(len(word), len(t)) - 2):
            return 0.6
    return 0.0


def hit(word, toks):
    return match(word, toks) > 0


def label(style, catalog):
    marks = []
    if style["webgl"]:
        marks.append("WebGL: slow without a GPU")
    elif style["render"].get("gpu"):
        marks.append("GPU raster")
    marks += style["credits"]
    if not style["recipe"]:
        marks.append("NO RECIPE YET")
    head = f"{style['slug']:<24} {style['name']} — {style['feel']}. Best for {style['best_for']}."
    tags = [catalog["families"][style["family"]]["title"], ", ".join(style["use_cases"]), *marks]
    return f"{head} [{'; '.join(tags)}]"


def facet(values, known, kind):
    out = []
    for value in values:
        key = value.casefold().replace(" ", "-")
        if key not in known:
            sys.exit(f"unknown {kind} {value!r}; choose from: {', '.join(known)}")
        out.append(key)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("query", nargs="*", help="words to look for (case-insensitive; hyphens count as spaces)")
    parser.add_argument("--use-case", action="append", default=[], help="keep styles tagged with this use case")
    parser.add_argument("--family", action="append", default=[], help="keep styles of this visual family")
    parser.add_argument("--no-gpu", action="store_true", help="skip WebGL styles, which render slowly without a GPU")
    parser.add_argument("--list", action="store_true", help="list families and use cases, then exit")
    parser.add_argument("--json", action="store_true", help="print full JSON entries")
    args = parser.parse_args()
    catalog = load()
    styles = catalog["styles"]

    if args.list:
        print("Use cases:")
        for key, use in catalog["use_cases"].items():
            print(f"  {key:<12} {use['title']} ({sum(key in s['use_cases'] for s in styles)}): {use['description']}")
        print("Families:")
        for key, fam in catalog["families"].items():
            print(f"  {key:<14} {fam['title']} ({sum(s['family'] == key for s in styles)}): {fam['description']}")
        return

    uses = facet(args.use_case, catalog["use_cases"], "use case")
    fams = facet(args.family, catalog["families"], "family")
    pool = [s for s in styles
            if (not uses or any(u in s["use_cases"] for u in uses))
            and (not fams or s["family"] in fams)
            and not (args.no_gpu and s["webgl"])]
    query = [w for w in words(" ".join(args.query)) if w not in STOPWORDS]
    exact = " ".join(args.query).casefold()
    # Score each word by where it matches (slug or name 2, the style's description and credits 1, family and
    # use-case words 0.25) and by how rare it is in the catalog, so "kids" outweighs "explainer".
    name = {st["slug"]: name_tokens(st) for st in styles}
    own = {st["slug"]: own_tokens(st) for st in styles}
    ctx = {st["slug"]: context_tokens(st, catalog) for st in styles}
    def score(word, st):
        return max(2 * match(word, name[st["slug"]]), match(word, own[st["slug"]]), 0.25 * match(word, ctx[st["slug"]]))
    # Rarity counts only styles whose own words match: a family description ("paper, graphite, ink, clay")
    # would otherwise make every word in it look common.
    def described(word, st):
        return match(word, name[st["slug"]]) > 0 or match(word, own[st["slug"]]) > 0
    weight = {w: math.log((1 + len(styles)) / (1 + sum(described(w, st) for st in styles))) + 0.1 for w in query}
    scored = []
    for s in pool:
        scores = [score(w, s) for w in query]
        first = exact in (s["slug"], s["name"].casefold())
        scored.append((not first, -sum(weight[w] * x for w, x in zip(query, scores)), s["name"].casefold(), s,
                       sum(x > 0 for x in scores)))
    scored.sort(key=lambda x: x[:3])
    full = [x for x in scored if x[4] == len(query)]

    if full:
        found, partial = [x[3] for x in full], False
    else:
        found, partial = [x[3] for x in scored if x[4] > 0][:5], True
    # Few full matches: also offer the best partial ones, so a narrow query still shows alternatives.
    extra = [x[3] for x in scored if 0 < x[4] < len(query)][:5] if not partial and len(full) < 3 and len(query) > 1 else []

    # Exit 0 for full matches, 1 for partial or no matches, in both output modes.
    if args.json:
        print(json.dumps(found, indent=1, ensure_ascii=False))
        sys.exit(0 if found and not partial else 1)
    if not found:
        print("no style matches; try other words, or --list to see families and use cases", file=sys.stderr)
        sys.exit(1)
    if partial:
        print(f"no style matches all {len(query)} words; closest partial matches:")
    for x in (scored if partial else full):
        if x[3] in found:
            print(label(x[3], catalog) + (f"  ({x[4]} of {len(query)} words)" if partial else ""))
    if extra:
        print("\nalso close (not every word):")
        for x in scored:
            if x[3] in extra:
                print(label(x[3], catalog) + f"  ({x[4]} of {len(query)} words)")
    print(f"\n{len(found)} of {len(styles)} styles", file=sys.stderr)
    sys.exit(1 if partial else 0)


if __name__ == "__main__":
    main()
