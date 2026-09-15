# Contributing

## Adding an entry to the list

One line per entry, in the right category, sorted by stars descending:

```
- [Name](https://github.com/owner/repo) - One sentence, starts uppercase, ends with a period.
```

Then run `python scripts/l0_check.py readme README.md` before opening the PR. CI runs the same check plus a weekly link-rot sweep.

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
