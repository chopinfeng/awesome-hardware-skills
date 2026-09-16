# Contributing

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
`python scripts/l0_check.py links GAPS.md` if you touched that file.

The list also exists in Simplified Chinese as [README.zh-CN.md](README.zh-CN.md), and CI checks that both files
carry the same entries in the same order. If you read Chinese, add the translated line in the same place. If you
do not, just edit `README.md` — the `translation-sync` job will fail, and that is expected: a maintainer will
backfill the translation. CI runs the same check plus a weekly link-rot sweep.

Quality bar for listing at all:

- Real README and something a user can install or run today. No "coming soon".
- Not abandoned: at least one push in the last 12 months, unless it is the only option for a hardware category.
- For skills (SKILL.md form): the description must be specific enough to trigger reliably — a bare "helps with ESP32" does not qualify.

## Verification badges

Entries in the **Skills** sections carry a badge showing how far their `evals/` package has been verified:

| Badge | Meaning |
|---|---|
| `L0` | Static checks pass: frontmatter, description length, no secrets, links resolve, evals package is well-formed. |
| `L1 (wokwi)` | All tasks pass in the named simulator, run by our CI. |
| `L2 ×3` | Three independent people ran the tasks on real hardware and filed an attestation with a transcript. |
| `ΔPass +42%` | With-skill pass rate minus without-skill pass rate on the same tasks and model. |
| `stale` | L1 has not been re-run in 90 days. |

A skill without an `evals/` package can still be listed, but shows no badge. Add one by copying [`template/evals/`](template/evals/) into the skill and filling in `manifest.yaml` and at least one task with an assertion stronger than `compile_only`. `python scripts/l0_check.py skill path/to/skill` tells you if the package is well-formed.

### Writing good tasks

- The prompt is the *only* thing the agent sees. If a human needs a hint to do it, the task is under-specified.
- Assert on physical side effects a script can observe: serial output, GPIO edges, bus captures, a ROS topic, an HTTP probe. Never "the code looks right".
- Mark assertions that need real hardware (a BLE sniffer, a physical sensor) with `l1_skippable: true` so L1 can still run the rest.
- Three tasks — easy / medium / hard — is the sweet spot. One task tells us nothing about generalization; ten is too expensive to A/B.

### Filing an L2 attestation

Open an issue using the **L2 hardware attestation** template. Attestations are only merged when they include an unedited transcript link; the bot appends them to the skill's `manifest.yaml` under `verified.L2`.

### The A/B run

`ΔPass` comes from running every task twice against the same model: once with the skill installed, once with the skill removed and only the SKILL.md `description` replaced by a generic one-liner. A skill that does not move pass rate or first-compile-ok rate by at least 15 points is marked `low-gain` — it is probably restating what the model already knows, and the maintainer will ask what non-obvious knowledge it is meant to carry.

## Adding a simulator or assertion type

Simulator ids and assertion types are enumerated in `scripts/l0_check.py`. To add one, open a PR that extends those sets and adds a short section to `README.md` under **Verification infrastructure** explaining how the runner drives it.
