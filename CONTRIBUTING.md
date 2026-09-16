# Contributing

*English · [简体中文](CONTRIBUTING.zh-CN.md)*

## Where to start

If you want to build rather than catalogue, [GAPS.md](GAPS.md) lists what is missing, with evidence and five
scoped first contributions. Filling one of those and listing it here is the most useful PR you can open.

If you find something that contradicts a gap, that is equally welcome: move it into the README and edit the
gap in the same PR.

## Adding an entry to the list

One line per entry, in the right category. Within a category, entries are ordered by how useful the maintainers judge them, not by stars — a 15k-star monorepo that happens to contain one small skill should not outrank a focused 50-star skill. Format:

```
- [Name](https://github.com/owner/repo) - One sentence, starts uppercase, ends with a period. (tags · ★stars · YYYY-MM)
```

Tags in the trailing parenthesis: `official` (repo lives under the vendor's own org), `coll` (a collection of several skills), `cursor-rules`, `placeholder`, `stale since YYYY-MM`. Use `k` for thousands of stars.

Then run `python scripts/l0_check.py readme README.md` before opening the PR — and
`python scripts/l0_check.py links GAPS.md` if you touched that file. CI runs the same checks plus a weekly
link-rot sweep.

The list also exists in Simplified Chinese as [README.zh-CN.md](README.zh-CN.md), and CI checks that both files
carry the same entries in the same order. If you read Chinese, add the translated line in the same place. If you
do not, just edit `README.md` — the `translation-sync` job will fail, and that is expected: a maintainer will
backfill the translation. The same applies to `GAPS.md` and this file, whose translations are
[GAPS.zh-CN.md](GAPS.zh-CN.md) and [CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md).

Quality bar for listing at all:

- Real README and something a user can install or run today. No "coming soon".
- Not abandoned: at least one push in the last 12 months, unless it is the only option for a hardware category.
- For skills (SKILL.md form): the description must be specific enough to trigger reliably — a bare "helps with ESP32" does not qualify.

## Adding an evals package

Entries in the **Skills** sections can carry verification badges — `L0`, `L1`, `L2 ×N`, `ΔPass` — earned by
shipping an `evals/` package inside the skill. The whole method is in **[EVALS.md](EVALS.md)**: the package
format, every assertion type and its fields, what each level checks, which levels exist today, and how to
avoid assertions that pass without checking anything.

The short version:

1. Copy [`template/evals/`](template/evals/) into your skill and fill in `manifest.yaml`.
2. Write about three tasks — easy, medium, hard — whose assertions observe physical side effects, with at least
   one stronger than `compile_only`.
3. Check that each assertion fails against an empty project.
4. Run `python scripts/l0_check.py skill path/to/skill` until it passes.
5. If you own the board, run the tasks and file an **L2 hardware attestation** issue with an unedited transcript.

A skill without an `evals/` package can still be listed; it simply shows no badge.

## Adding a simulator or assertion type

See the last section of [EVALS.md](EVALS.md).
