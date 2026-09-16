# Evaluating hardware skills

*English · [简体中文](EVALS.zh-CN.md)*

This is the method behind the badges in the [README](README.md): how a hardware skill proves it works, what an
eval package contains, what each verification level checks, and — just as important — which parts exist today
and which are still being built.

Why bother at all is argued in [GAPS.md](GAPS.md). The short version: frontier models score 0% deployment
success on real microcontrollers without hardware feedback, expert-written skills push success near 100%, and
nobody can tell a good hardware skill from a plausible one by reading it. Evals are how you tell.

## What exists today

Read this table before anything else. Every other section describes the full design, and it would be easy to
mistake a planned piece for a working one.

| Piece | Status | Where |
|---|---|---|
| Eval package format | Defined | `template/evals/`, and this document |
| `L0` static checks | **Working**, in CI | `scripts/l0_check.py skill <path>` |
| `L1` simulator runner | Not built | Design below |
| `L2` real-hardware attestation | **Working**, by hand | Issue template `.github/ISSUE_TEMPLATE/attestation.yml`; a maintainer records accepted attestations |
| `ΔPass` A/B runner | Not built | Design below |
| `stale` marking | Not built | Depends on the L1 runner |

The first third-party skill to ship a package in this format is
[fxp/m5stack-embedded-dev-skill](https://github.com/fxp/m5stack-embedded-dev-skill). It is used as the worked
example near the end.

## Principles

**Assert on physics, not prose.** A task passes when a script observes a side effect in the world: a line on
a UART, an edge on a GPIO, a packet on a bus, a message on a ROS topic, a response from an HTTP endpoint. It
never passes because a model or a person judged that the code looks right. Hardware is unusually good for
this, because almost everything a firmware does is observable from outside the chip.

**The prompt is the whole task.** The agent sees the prompt and nothing else. If a competent engineer would
need a hint to succeed, the hint belongs in the prompt or the task is under-specified.

**Every assertion must be able to fail.** An assertion that passes when the thing it checks is absent is worse
than no assertion, because it produces confidence it has not earned. This is the most common defect in real
eval packages and has its own section below.

**Say which levels you have not reached.** A package that declares `simulator: none` and explains why is more
useful than one that claims a simulator it has not actually run. Honest gaps are fine; unearned badges are not.

**Measure the skill, not the model.** A task that every model already passes without the skill measures
nothing about the skill. That is what `ΔPass` exists to catch.

## The eval package

An eval package is a directory named `evals/` inside the skill, next to `SKILL.md`:

```
my-skill/
├── SKILL.md
├── references/
└── evals/
    ├── manifest.yaml
    ├── tasks/
    │   ├── 01-easy-thing.yaml
    │   ├── 02-medium-thing.yaml
    │   └── 03-hard-thing.yaml
    └── fixtures/            # optional
```

Start by copying [`template/evals/`](template/evals/).

### manifest.yaml

| Field | Required | Meaning |
|---|---|---|
| `skill` | yes | Must equal `name` in the skill's SKILL.md frontmatter. |
| `version` | no | Version of the eval package, not of the skill. |
| `target.board` | yes | An exact board identifier — `esp32-c3-devkitm-1`, or an arduino-cli FQBN such as `esp32:esp32:m5stack_core2` — never a family name like "ESP32". |
| `target.framework` | yes | `esp-idf`, `arduino`, `zephyr`, `ros2`, and so on. |
| `target.framework_version` | yes | The version the tasks were authored and tested against. Hardware SDKs break between minor versions; this is what makes a result reproducible. |
| `target.toolchain` | no | What the agent is expected to invoke: `idf.py`, `arduino-cli`, `west`. |
| `simulator` | yes | Where L1 will run. One of `wokwi`, `renode`, `qemu`, `native_sim`, `gazebo`, `isaac`, `mujoco`, `webots`, `ha-demo`, `modbus-sim`, `opcua-sim`, or `none`. |
| `assertions_supported` | yes | Every assertion type any task in this package uses. |
| `verified.L0` | no | `{date, run}` once `l0_check.py` passes. |
| `verified.L1` | reserved | Written by the L1 runner. Leave `null`. |
| `verified.L2` | no | List of accepted attestations, added by a maintainer. |
| `ab.*` | reserved | Written by the A/B runner. Leave `null`. |

Use `simulator: none` when no public simulator models the hardware the tasks depend on, and say why in a
comment. The M5Stack package is a good model: the Core2's power-management IC is not modelled by any public
Wokwi or Renode board, so it declares `none` rather than claiming a simulator that would silently skip the
parts that matter.

### Task files

One YAML file per task in `tasks/`. The filename, minus `.yaml`, must equal the task's `id`.

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Equal to the filename stem. Prefix with a number so tasks sort by difficulty. |
| `level` | yes | `easy`, `medium` or `hard`. |
| `timeout_s` | no | Wall-clock budget for the agent's whole attempt. |
| `prompt` | yes | Everything the agent is told. Non-empty. |
| `build.cmd` | no | What the runner executes after the agent says it is done, e.g. `idf.py build`. |
| `build.cwd` | no | Relative to the agent's working directory. |
| `assertions` | yes | List of assertions. **All** must pass for the task to pass. |
| `fixtures` | no | Known-good reference outputs, e.g. an expected serial log. |

Aim for three tasks — one easy, one medium, one hard. One task says nothing about whether the skill
generalises; ten are expensive to run twice for every A/B comparison.

## Assertion types

Every assertion has a `type`. Any assertion may also set `l1_skippable: true`, meaning it needs real hardware
the simulator cannot provide — a BLE sniffer, a physical button, a sensor reading a real room. L1 skips it and
credits the rest; L2 attesters must still check it.

The set of valid types is enumerated in `scripts/l0_check.py`. Five have field schemas established by real
packages. Three are reserved: the name is accepted, but the fields are not defined yet, and the first package
that needs one defines them through a pull request to this document.

| Type | Observes | Fields |
|---|---|---|
| `compile_only` | `build.cmd` exits 0 | none |
| `serial_match` | UART output | `baud`, `pattern` (regular expression, matched per line), `min_matches`, `within_s` |
| `gpio_state` | Pin levels over time | `pin`, `expect` (e.g. `toggles`), `min_edges`, `within_s` |
| `bus_capture` | Traffic on a bus | `bus` (e.g. `ble`), `expect` (bus-specific map, e.g. `adv_name`, `service_uuid`, `char_uuid`, `notify_count_min`, `within_s`) |
| `exit_code` | Any script's result | `cmd` (shell), `expect` (exit status) |
| `network_probe` | A device's network endpoint | reserved |
| `ros_topic` | Messages on a ROS topic | reserved |
| `file_exists` | Artefacts on disk | reserved |

`compile_only` on its own proves almost nothing about hardware, which is why L0 requires every package to
contain at least one assertion stronger than it.

`exit_code` is the escape hatch for static properties of the generated code that no runtime observation
would catch. The M5Stack package uses it to check that the agent did *not* call `Wire.begin()` a second time:
the I2C scan still works on that board even when the rule is broken, so only a source check detects the
violation. Use it sparingly — a runtime assertion is almost always stronger when one is possible.

## Vacuous assertions

An assertion is vacuous when it passes because the thing it inspects is missing. It is the defect most worth
checking for, because it is invisible in a green run.

The pattern shows up most with `exit_code` checks that search source code. Consider a check that finds the
interrupt handler by matching `void IRAM_ATTR <name>(...)` and fails if that body contains `Serial.` or
`delay(`. If the agent writes the handler without `IRAM_ATTR`, the pattern finds nothing — and a script written
as "fail if found and bad" exits 0. That holds even when the handler calls `Serial.println` and `delay`, which
is the exact violation the check exists to catch: the agent makes the mistake, drops one attribute, and the
assertion goes green. The fix is to fail when the thing to inspect cannot be found:

```python
m = re.search(r'void\s+IRAM_ATTR\s+\w+\s*\([^)]*\)\s*\{(.*?)\n\}', src, re.S)
if not m:
    sys.exit(1)                     # no ISR found: the task was not done, so do not pass
sys.exit(1 if re.search(r'Serial\.|delay\(', m.group(1)) else 0)
```

Run against three small sketches — a blocking handler without `IRAM_ATTR`, an `IRAM_ATTR` handler that calls
`Serial`, and a correct handler that only sets a flag — the original check exits 0, 1 and 0: it passes the
first, broken sketch. With the guard it exits 1, 1 and 0.

Two quick tests catch almost every vacuous assertion before it is committed. Run each assertion against an
empty project, where every one of them should fail. Then run it against a deliberately wrong solution, where
the assertion targeting that mistake should fail and the others should not. Because assertions within a task
are ANDed, a vacuous one is sometimes covered by a neighbour — a missing `.ino` also fails `compile_only` — but
do not rely on that: each assertion should stand on its own.

## Level 0 — static checks

**Working.** Run it locally before opening a pull request:

```
python scripts/l0_check.py skill path/to/my-skill
```

It verifies, and only verifies, the following:

- `SKILL.md` exists and has YAML frontmatter with non-empty `name` and `description`.
- `description` is at least 80 characters — shorter descriptions rarely trigger reliably.
- `SKILL.md` contains nothing shaped like an API key or access token.
- `evals/manifest.yaml` exists, its `skill` equals the frontmatter `name`, `simulator` is a known id, every
  entry in `assertions_supported` is a known type, and `target.board`, `target.framework` and
  `target.framework_version` are set.
- `evals/tasks/` contains at least one task; every task's `id` equals its filename stem, `level` is valid, and
  `prompt` is non-empty.
- Every assertion's `type` is a known type and is declared in `assertions_supported`.
- At least one assertion in the package is stronger than `compile_only`.

It does **not** check the fields inside an assertion, the `build` block, whether a pattern is a valid regular
expression, or whether an assertion can fail. L0 means the package is well-formed, not that it is good.

## Level 1 — simulator

**Not built.** This section is the design the runner will follow.

For each task the runner gives the agent the prompt in a clean working directory with the skill installed,
waits for the agent to finish or for `timeout_s`, runs `build.cmd`, loads the artefact into the declared
simulator, and evaluates every assertion not marked `l1_skippable`. A package reaches L1 when every task passes
on a named model, recorded as `{date, simulator, tasks_passed, model}`.

Three decisions are already settled:

- **Reuse the simulator's own assertion layer.** Renode ships `renode-test` with Robot Framework keywords such as
  `Wait For Line On Uart`; Wokwi scenarios assert on serial text natively. The runner should translate
  `serial_match` into those rather than reimplement matching over scraped console output.
- **Measure time in the simulator, not on the wall clock.** `within_s` means simulated seconds. An emulator's
  deterministic virtual time is the entire reason to prefer it over a board in CI; a runner that sleeps
  and greps throws that away and becomes flaky.
- **Record which assertions were skipped.** An L1 badge must show how many assertions were credited, so that a
  package whose important checks are all `l1_skippable` cannot look as strong as one whose checks all ran.

Which simulator can support which assertion is summarised in the README's verification infrastructure section.
Renode lacks an agent-facing session interface, which is the top item in [GAPS.md](GAPS.md).

## Level 2 — real hardware

**Working, by hand.** Anyone who owns the target board can attest.

1. Install the skill and run each task exactly as written in `evals/tasks/`, giving the agent the prompt and
   nothing else.
2. Evaluate every assertion, including those marked `l1_skippable` — that is what L2 is for.
3. Save the complete, unedited agent transcript somewhere public.
4. Open an issue with the **L2 hardware attestation** template, which asks for the skill, the exact board and
   revision, the framework version, the agent model and harness, a `pass` or `fail` line per task, and the
   transcript link, and requires confirming that no hints were given and the transcript is unedited.

Attestations without a transcript are not accepted. Once accepted, a maintainer appends the attestation to
the package's `verified.L2`. The README shows `L2 ×N` for N independent attestations, where independent means
different people with different boards; three is the bar for the badge to carry weight.

## ΔPass — does the skill carry knowledge?

**Not built.** This section is the design the A/B runner will follow.

Every task runs twice on the same model and harness: once with the skill installed, and once with the skill
removed and its `description` replaced by a generic one-line placeholder, so that the only difference between
the arms is the skill's knowledge. The runner records two rates per arm — task pass rate, and first-compile-ok
rate, the share of attempts whose first build succeeds without the agent having to fix anything.

`ΔPass` is the with-skill pass rate minus the without-skill pass rate. A skill that moves neither rate by at
least 15 percentage points is marked `low-gain`. That is not a rejection, but a question: it probably restates
what the model already knows, and the maintainers will ask which non-obvious fact it is meant to carry.

First-compile-ok is tracked separately because it is where hardware skills earn their keep. Wrong register
names, a missing `sdkconfig` symbol, the wrong FQBN — models usually recover from these after two or three
failed builds, so pass rate alone can hide a skill that saves real iteration.

## Worked example

[fxp/m5stack-embedded-dev-skill](https://github.com/fxp/m5stack-embedded-dev-skill) targets the M5Stack Core2
with Arduino and M5Unified. Its package shows most of the method in three tasks:

- **`01-hello-serial-tick`** (easy) — print `tick` once a second. `compile_only` plus a `serial_match` requiring
  four lines matching `^tick$` within six seconds. The minimal honest task.
- **`02-i2c-scan-no-redundant-wire-begin`** (medium) — scan the internal I2C bus without calling `Wire.begin()`
  again. A `serial_match` for the power-management IC at `0x34`, plus an `exit_code` source check. It carries
  the skill's actual lesson, and it is a good case for `exit_code`: the scan succeeds on this board revision
  even when the rule is broken, so no runtime observation can catch the mistake.
- **`03-isr-safe-button-notify`** (hard) — notify the main loop from a GPIO interrupt without blocking calls.
  The `serial_match` needs a real button press, so it is correctly marked `l1_skippable`. The `exit_code` check
  is the example in the section on vacuous assertions: as published, it passes a handler that blocks, as long
  as the handler lacks `IRAM_ATTR`. This matters more than it looks, because with the serial assertion skipped
  at L1 it is the task's only substantive check there. Adding the `if not m: sys.exit(1)` guard fixes it.

The manifest declares `simulator: none` and explains that no public simulator models the Core2's PMIC. With
L1 unreachable by design, the package's path to a badge is L0 now and L2 attestations later.

## Extending the method

To add a simulator id or an assertion type, open a pull request that:

1. Adds it to `SIMULATORS` or `ASSERTION_TYPES` in `scripts/l0_check.py`.
2. For an assertion type, adds a row to the assertion table above defining its fields, and explains what makes
   it able to fail.
3. For a simulator, adds it to the README's verification infrastructure section with a note on how a runner
   drives it headlessly and which assertion types it can support.
4. Updates the translation in `EVALS.zh-CN.md`, or leaves the `translation-sync` job failing for a maintainer
   to fix.
