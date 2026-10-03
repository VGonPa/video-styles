# Agent skill

`animating-in-video-styles/` teaches a coding agent to make new videos in the catalog's styles: pick a style,
start from its film, swap in a new subject, length or format, and review the frames. It follows the open
[Agent Skills](https://agentskills.io/specification) format, so the same folder works in Claude Code, Codex,
Cursor, GitHub Copilot and other agents that read `SKILL.md`.

## Install

In a clone of this repository there is nothing to install: `.claude/skills/` (Claude Code) and
`.agents/skills/` (Codex and others) link to this folder.

Elsewhere, install it with the [skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add VGonPa/video-styles --skill animating-in-video-styles
```

or copy `skills/animating-in-video-styles/` into your agent's skills directory (`~/.claude/skills/`,
`~/.agents/skills/`). An installed copy downloads a style's code from GitHub when it needs it.

## Maintain

| File | Source |
|---|---|
| `SKILL.md`, `references/contract.md`, `references/review.md`, `scripts/` (find, fetch, contact sheet, embed image, env check) | Hand-written |
| `references/styles/<slug>.md` | One recipe per style, written against [RECIPE_TEMPLATE.md](../RECIPE_TEMPLATE.md) and reviewed by someone other than its author |
| `references/catalog.md`, `assets/catalog.json` | Generated from `styles/*/meta.json` by `build_index.py` |

`check_catalog.py` validates the skill's frontmatter (spec keys only), its file references, that the generated
catalog is current, the links under `.claude/skills/` and `.agents/skills/`, and every recipe: title, headings,
tables, and that the files, names, colours, cue names and style slugs it cites exist. `tests/test_skill.py` covers the search
and the recipe checks. While recipes are being written, `RECIPES_REQUIRED = False` in check_catalog.py reports a
missing recipe without failing; set it to `True` once every style has one.

## Release

An installed copy of the skill is a snapshot: its recipes describe the code as it was when it was installed,
and `fetch_style.py` downloads style code from the git ref in `assets/catalog.json`. Keep the two in step:

1. Merge the recipe and code changes to `main` and tag the commit, e.g. `git tag skill-v1.1.0 && git push --tags`.
2. Set `SKILL_CODE_REF` in `build_index.py` to that tag, run `python3 build_index.py && python3 check_catalog.py`,
   and merge the regenerated catalog. Until the first tag exists the ref is `main`.
