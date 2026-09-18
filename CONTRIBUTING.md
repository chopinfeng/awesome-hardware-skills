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
link-rot sweep. Maintainers refresh stars and last-push dates with `python scripts/refresh_meta.py` (needs an
authenticated `gh`); it marks entries with no push in 12 months `stale since YYYY-MM`, follows renames, and
reports repositories that disappeared, then `python scripts/gen_catalog.py` rebuilds the tables in `CATALOG.md`.

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
shipping an `evals/` package inside the skill. Only `L2`, a run on a physical board, means the skill has
passed; `L0` and `L1` are pre-checks. The whole test plan is in **[EVALS.md](EVALS.md)**: the steps
of phases 0 to 3, how each assertion is measured on a real board, the run-record format, what reviewers check,
and the package format reference.

The short version:

1. Copy [`template/evals/`](template/evals/) into your skill and fill in `manifest.yaml` — or install
   [hardware-skill-creator](skills/hardware-skill-creator/), an Agent Skill that scaffolds the package, checks it,
   and walks you and your agent through every step below.
2. Write about three tasks — easy, medium, hard — whose assertions observe physical side effects, with at least
   one stronger than `compile_only`.
3. Run `python scripts/l0_check.py skill path/to/skill` until it passes.
4. **Phase 0 — validate the eval.** For each task add `reference/`, `broken/` and `spoof/` solutions under
   `evals/fixtures/<task-id>/`, and show on the board that the reference passes, an empty project fails every
   assertion, the broken and spoof solutions are caught, and an agent told to cheat is caught. Check that the skill
   contains no task's answer. Record it as `eval_validated` in the manifest. Add `evals/trigger_queries.json` for the
   trigger pre-check, which needs no board.
5. **Phases 1–2 — pass runs.** Between two passing bench self-tests, run each task on a physical board — or ask
   someone who owns one — with the skill installed *without* its `evals/`, the host restored to a baseline and
   the board fully reset before every run, review every passing run for faked work, and file an **L2 hardware
   attestation** issue with every run record.
   A task passes in two of at most three runs; until every task has, the skill has not passed.

A skill without an `evals/` package can still be listed; it simply shows no badge.

## Submitting test results

Results travel as evidence in git plus a claim a maintainer can review:

1. **Phase 0**, by the skill author: commit the fixtures and Phase 0 logs to the skill's repository and put that
   commit's permalink in `eval_validated.evidence`.
2. **Runs on a board**, by anyone: commit every run record, log, capture and transcript to a repository you control,
   with a `SHA256SUMS` file, and open an **L2 hardware attestation** issue with the commit permalink and the digest
   of `SHA256SUMS`. Replace secrets in transcripts with `[REDACTED]` before publishing; make no other edits.
3. **Badges**, by a maintainer: after accepting an attestation, the maintainer opens a pull request updating the
   entry's badge in both READMEs. Please do not edit badges in your own pull request.

The step-by-step commands, including the `gh` commands for the pull request, are in the
[hardware-skill-creator README](skills/hardware-skill-creator/README.md#submit-results).

## Adding a simulator or assertion type

See the last section of [EVALS.md](EVALS.md).
