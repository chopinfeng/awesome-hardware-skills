# Hardware skill evals: test plan

*English · [简体中文](EVALS.zh-CN.md)*

This document is the test plan behind the badges in the [README](README.md). It says exactly how a hardware
skill is tested, on what, by whom, how many times, how each assertion is measured on a real board, what gets
recorded, and when the result counts. Why the effort is worth it is argued in [GAPS.md](GAPS.md).

The one rule everything else serves: **a skill passes only when its tasks have run on a physical board and its
assertions held.** Static checks and simulators are pre-checks. Nothing else is called passing in this repo.

## What exists today

Read this first — the rest of the document describes the whole plan, and it is easy to mistake a planned piece
for a working one.

| Piece | Status |
|---|---|
| Eval package format | Defined in this document; starter in `template/evals/` |
| `L0` static checks | **Working**, in CI — `python scripts/l0_check.py skill <path>` |
| `L1` simulator pre-check runner | Not built, and never a pass |
| Phases 0–3 on real hardware | **Working, by hand** — every step below can be done today with a board and the tools listed |
| `L2` attestation form | **Working** — `.github/ISSUE_TEMPLATE/attestation.yml` (it was invalid YAML until 2026-09-16; CI now checks it) |
| Automated A/B runner for `ΔPass` | Not built; the manual procedure in Phase 3 stands in for it |
| `stale` marking | Not built; applied by a maintainer from attestation dates |

As of 2026-09-16 one listed skill ships an eval package, and **no listed skill has passed.**

## What the tests answer

Two questions, answered separately:

1. **Does the skill work?** With the skill installed, can an agent complete each task on the real board?
   Answered by Phase 2. A yes is the `L2` badge.
2. **Does the skill carry knowledge?** Does installing it change the outcome compared with not installing it?
   Answered by Phase 3. The difference is `ΔPass`.

A skill can pass question 1 and still show no gain on question 2 — the model may already know how. Both results
are published.

Neither question can be answered until a third one is: **is the eval itself trustworthy?** An assertion that
passes when nothing was done tells you nothing about the skill. That is Phase 0, and it comes first.

## The plan at a glance

| Phase | Who | When | Purpose | Output |
|---|---|---|---|---|
| 0 — validate the eval | Package author | Once per eval version | Prove the tasks are achievable and the assertions can fail | `eval_validated` in the manifest |
| 1 — bench self-test | Tester | Start and end of every session | Prove the bench works, so failures can be blamed on the skill | Self-test record |
| 2 — pass runs | Tester | Per attestation | Decide whether the skill passes | Run records, `L2` attestation |
| 3 — A/B | Tester | Optional, per attestation | Measure what the skill adds | `ΔPass` with its sample size |

## The test bench

Everything below is recorded in each run record. Two runs on different benches are not comparable.

**Target board.** The exact board named in `target.board`, including revision, e.g. `esp32-c3-devkitm-1 rev 1.1`.
Not a sibling from the same family.

**Host.** Operating system and version, and the toolchain at exactly `target.framework_version`. Power the board
from a powered USB hub or a bench supply — a weak USB port causes brown-out resets that look like firmware bugs.

**Observation instruments**, required according to the assertion types the package uses:

| Assertion type | Instrument | Notes |
|---|---|---|
| `compile_only`, `exit_code` | none | Runs on the host |
| `serial_match` | The board's USB-UART, or a separate USB-UART adapter | Captured with host timestamps |
| `gpio_state` | Logic analyser (a sigrok-compatible one is enough) | Shared ground with the board |
| `bus_capture` (BLE) | BLE sniffer — e.g. an nRF52840 dongle with nRF Sniffer, or a Sniffle-compatible board | Must follow the connection to see notifications |
| `bus_capture` (CAN, I2C, SPI) | CAN adapter or logic analyser with a protocol decoder | |

**Agent.** Model ID, harness and its version, and the harness's tool permissions. The agent runs on the host with
the board attached and may build, flash and read serial during its attempt — that closed loop is how skills are
used, and what a pass claims. Record whether the agent had network access.

**Skill under test.** The skill's repository and commit SHA, and the eval package `version`. A result belongs to
that commit, not to the skill in general.

## Phase 0 — validate the eval

**Who:** the package author, before asking anyone to attest. **When:** once per eval package version, and again
whenever a task or assertion changes.

An eval is only as good as its ability to tell a correct solution from a wrong one. For every task, the author
prepares two solutions and runs three checks on the real board:

```
evals/fixtures/<task-id>/reference/   a known-good solution
evals/fixtures/<task-id>/broken/      a solution containing the specific mistake the task exists to catch
```

1. **The reference passes.** Build, flash and observe the reference solution. Every assertion passes, including
   those marked `l1_skippable`. This proves the task can be done on this board and no assertion is too strict.
2. **An empty project fails.** Run every assertion against an empty working directory. Every assertion fails.
   This catches checks that pass when nothing was built.
3. **The broken solution is caught.** Build, flash and observe the broken solution. The assertion aimed at that
   mistake fails; the rest behave as the mistake predicts. This catches checks that pass when the wrong thing
   was built.

Checks 2 and 3 catch different defects, and a package needs both. The first third-party package in this list
shows why. One task forbids calling `Wire.begin()` again and checks with `! grep -q "Wire.begin(" *.ino`. Run
against an empty directory, that check exits 0: `grep` cannot find `*.ino`, and `!` turns its error into a pass.
Check 2 catches it; check 3 would not, because a broken solution does contain an `.ino`. Another task forbids
blocking calls in an interrupt handler and locates the handler by matching `IRAM_ATTR`. Against an empty
directory it correctly fails — but against a handler that calls `Serial.println` and `delay` without
`IRAM_ATTR`, it exits 0. Check 2 misses it; only check 3 catches it.

### Writing assertions that can fail

An assertion is **vacuous** when it passes because the thing it inspects is missing. It is invisible in a green
run, which is why Phase 0 exists. The fix is always the same: fail when the thing to inspect cannot be found.

```python
# vacuous: passes when no IRAM_ATTR handler exists
m = re.search(r'void\s+IRAM_ATTR\s+\w+\s*\([^)]*\)\s*\{(.*?)\n\}', src, re.S)
sys.exit(1 if m and re.search(r'Serial\.|delay\(', m.group(1)) else 0)

# sound: absence is a failure
if not m:
    sys.exit(1)
sys.exit(1 if re.search(r'Serial\.|delay\(', m.group(1)) else 0)
```

```sh
# vacuous: passes in an empty directory
! grep -q "Wire.begin(" *.ino

# sound: require the file before checking what is absent from it
ls *.ino >/dev/null 2>&1 && ! grep -q "Wire.begin(" *.ino
```

### Recording Phase 0

Record the result in the manifest. Attestations are only accepted for a package whose current version has been
validated.

```yaml
eval_validated:
  date: 2026-09-20
  board: esp32-c3-devkitm-1 rev 1.1
  framework_version: "5.2.2"
  reference_passed: true      # check 1, every task
  empty_failed: true          # check 2, every assertion
  broken_caught: true         # check 3, every task that has a broken/ solution
  evidence: https://...       # logs and captures from the three checks
```

## Phase 1 — bench self-test

**Who:** the tester. **When:** at the start and the end of every test session.

Flash each task's `reference/` solution and evaluate its assertions, exactly as in a Phase 2 run but with no
agent. Every assertion must pass. This proves the serial capture, the logic analyser, the sniffer, the power and
the toolchain all work.

A session's results count only if **both** self-tests pass. If the closing self-test fails, every run in the
session is **invalid** — the bench may have failed at any point — and is rerun in a new session. This is what
separates "the bench broke" from "the skill failed" with evidence rather than opinion.

## Phase 2 — pass runs

**Who:** the tester. **When:** for every attestation.

### Procedure for one run

1. **Record the run metadata** listed under the test bench above, and assign the run the next sequential number.
2. **Reset the board to a known state.** Erase the flash with the toolchain's erase command, then power-cycle.
3. **Prepare a clean working directory** with the skill installed and nothing else from previous runs.
4. **Start the agent and the transcript recording.** Give the agent the task's `prompt` verbatim and nothing
   else — no port name, no hint, no correction — unless the prompt itself contains it.
5. **Let the agent work** until it declares it is done or `timeout_s` elapses on the wall clock. A timeout is a
   failed run, not an invalid one.
6. **Freeze the result.** Archive the working directory and record its SHA-256. Everything after this point
   uses the frozen copy; the agent's own builds and flashes during its attempt are not evidence.
7. **Build.** Run `build.cmd` in the frozen copy and keep the log. If it fails, `compile_only` fails and every
   other assertion is recorded as `not-run`.
8. **Flash.** Erase, then write the build with `flash.cmd` if the task defines one, otherwise the toolchain's
   standard flash command. Keep the flash tool's full output, including the line where it reports the chip it
   detected.
9. **Observe.** Start every capture before releasing reset. **Time zero** is the moment reset is released and the
   new firmware begins to run; every `within_s` window is measured from there. Carry out any `human_action` the
   task defines, at the time it defines, and log the timestamp.
10. **Evaluate each assertion** using the methods in the next section, and keep its raw evidence file.
11. **Record the result.** Each assertion is `pass`, `fail` or `not-run`. The run passes only if every assertion
    passed.

### How a task and a package pass

- **Run:** passes if every assertion passes, including those marked `l1_skippable`.
- **Task:** is run **three** times, each from step 2. It passes if **at least two** of the three runs pass. Agents
  are not deterministic, so a single run can pass by luck or fail by bad luck; two of three is the smallest
  sample that is not one draw.
- **Package:** passes if every task passes. That is the `L2` badge. `L2 ×N` counts independent attestations —
  different people, different boards — that each reached a pass.

Every run is reported, in order: passes, failures and invalid runs alike. Choosing the best three of more runs is
not allowed; if a run is invalid it is rerun, and both appear in the record.

### Failed run or invalid run

A **failed** run is a result about the skill. An **invalid** run is a result about the bench, and is rerun.
The distinction is decided by evidence, never by preference:

| Invalid — rerun | Failed — counts |
|---|---|
| The session's closing self-test failed | The agent timed out |
| The model API or harness crashed for reasons unrelated to the task | The agent flashed the wrong port or wrong target |
| The board was physically disconnected, with a note of when | The build or flash failed on the frozen copy |
| The tester gave the agent information not in the prompt | The board is left unbootable by the agent's firmware |
| | Any assertion failed |

The fourth invalid case matters: a run where the tester helped is not a fail, but it is not evidence of a pass
either. It is rerun.

## Phase 3 — A/B for ΔPass

**Who:** the tester. **When:** optional, alongside Phase 2.

1. Run each task **five** times in each of two arms, on the same board, model and harness, following the Phase 2
   procedure:
   - **With skill:** the skill installed.
   - **Without skill:** the skill removed, with its `description` replaced by a generic one-line placeholder, so
     that the only difference between the arms is the skill's knowledge.
2. **Alternate the arms** — with, without, with, without — rather than running one arm then the other, so that
   drift in the bench, the board or the model API affects both arms equally.
3. For each arm record two rates across all runs of all tasks: the **pass rate**, and the **first-compile-ok
   rate** — the share of runs whose first build during the agent's attempt succeeded without the agent fixing
   anything.
4. **`ΔPass`** is the with-skill pass rate minus the without-skill pass rate, always published with its sample
   size, e.g. `ΔPass +40% (15 v 15)`.
5. A skill that moves neither rate by at least **15 percentage points** is marked `low-gain`. That is a question
   rather than a rejection: it probably restates what the model already knows.

First-compile-ok is tracked because it is where hardware skills earn their keep. A wrong register name, a
missing `sdkconfig` symbol, the wrong FQBN — models often recover after two or three failed builds, so the pass
rate alone can hide a skill that saves real iterations.

Five runs per arm per task on a three-task package is thirty runs. The numbers are noisy at that size, which is
why the sample size is always shown next to the result.

## Measuring each assertion on a real board

### `compile_only`

Run `build.cmd` in the frozen copy. Passes if it exits 0. Keep the full build log.

### `serial_match`

- **Open the port before releasing reset**, or early output is lost. Configure the port so that opening it does
  not itself reset the board or hold it in the bootloader — on many ESP32 boards DTR and RTS drive EN and GPIO0
  — then reset the board deliberately and log that timestamp as time zero.
- **Boards with native USB serial** (for example ESP32-S3 or ESP32-C3 using USB-Serial/JTAG) re-enumerate the
  port on reset. Start the clock at reset, begin capture as soon as the port reappears, and note the gap. Output
  printed during that gap is lost, so tasks for these boards should print repeatedly rather than once.
- **Capture** at the task's `baud` to a log file, one line per record with a host timestamp.
- **Match** per line after normalising line endings, using `pattern` as a regular expression. Pass if at least
  `min_matches` lines match within `within_s` of time zero.

### `gpio_state`

- Connect a logic-analyser channel to `pin`, with a common ground.
- Sample at no less than ten times the fastest edge rate the task implies; 1 MHz is ample for anything slower
  than a few kilohertz.
- Capture for at least `within_s` from time zero and save the raw capture, e.g. a sigrok `.sr` file.
- For `expect: toggles`, count edges in the window and pass if the count is at least `min_edges`.

### `bus_capture`

- **BLE.** Start the sniffer before time zero. A sniffer sees advertising on its own, but it only sees GATT
  notifications if it follows the connection, so connect a central (for example a phone with nRF Connect)
  after the device is advertising and confirm the sniffer followed it. Save a `.pcapng`. Evaluate with a
  packet filter — the advertised name, the service and characteristic UUIDs, and the count of Handle Value
  Notifications in the window.
- **CAN, I2C, SPI.** Capture with an adapter or a logic analyser with the protocol decoder enabled, save the raw
  capture, and evaluate the decoded frames against `expect`.
- Assertions of this type are usually `l1_skippable`, which makes them the ones Phase 2 exists for.

### `exit_code`

Run `cmd` in the frozen copy with the task's shell. Passes if the exit status equals `expect`. This assertion
must have been shown to fail on an empty project in Phase 0 check 2.

### Reserved types

`network_probe`, `ros_topic` and `file_exists` are accepted by the checker but have no field schema yet. A package
that needs one defines its fields and measurement method in a pull request to this document, before it is used.

## Recording and submitting

### Run record

Every run, including self-tests and invalid runs, produces one record. Keep them in a directory with the evidence
files they reference, and link that directory from the attestation.

```yaml
run: 7
session: 2026-09-20-a
phase: pass                       # self-test | pass | ab-with | ab-without
task: 01-blink
skill: {repo: https://github.com/owner/skill, commit: 3f2a9c1}
eval_version: 0.1.0
board: esp32-c3-devkitm-1 rev 1.1
host: {os: Ubuntu 24.04, framework_version: "5.2.2"}
agent: {model: claude-opus-5, harness: claude-code 2.1.3, network: true}
started: 2026-09-20T10:14:03Z
ended:   2026-09-20T10:21:47Z
agent_outcome: declared-done      # declared-done | timeout
workdir_sha256: 9b1e...
build: {exit: 0, log: runs/07/build.log}
flash: {exit: 0, log: runs/07/flash.log, detected_chip: "ESP32-C3 (QFN32) (revision v0.4)"}
time_zero: 2026-09-20T10:22:15.402Z
human_actions: []                 # e.g. [{at: "+5.0s", action: "pressed button on GPIO39"}]
assertions:
  - {type: compile_only, result: pass}
  - {type: serial_match, result: pass, matches: 6, evidence: runs/07/serial.log}
  - {type: gpio_state,   result: pass, edges: 12, evidence: runs/07/gpio8.sr}
result: pass                      # pass | fail | invalid
invalid_reason: null
transcript: runs/07/transcript.jsonl
```

### Attestation

Open an issue with the **L2 hardware attestation** form. It asks for the skill and commit, the exact board and
revision, the framework version, the agent model and harness, the three run results per task, both bench
self-test results, the hardware evidence — the flash tool's chip-detection output and a serial log — and a link
to the run records and transcripts. It requires confirming that the runs were on a physical board, that every
run is reported, that no hints were given and that the transcripts are unedited.

## Review

A maintainer checks an attestation before recording it in the manifest's `verified.L2`:

- The package's `eval_validated` covers the version that was tested.
- Both self-tests passed in every session whose runs are counted.
- The chip reported by the flash tool matches the claimed board.
- Every task has three counted runs, numbered in sequence, with invalid runs explained and rerun.
- The serial logs and captures agree with the pass or fail recorded for each assertion.
- The transcripts show the prompt given verbatim and no help from the tester.

An attestation missing any of this is sent back with the specific gap, not rejected silently. Nothing here makes
fabrication impossible; independent reproductions, counted by `×N`, are the defence.

## Pre-checks: L0 and L1

Pre-checks catch problems before anyone spends an afternoon at a bench. Neither is a pass.

### L0 — static checks

**Working.** Run `python scripts/l0_check.py skill path/to/my-skill`. It verifies, and only verifies:

- `SKILL.md` exists with YAML frontmatter containing non-empty `name` and `description`, and the description is
  at least 80 characters.
- `SKILL.md` contains nothing shaped like an API key or access token.
- `evals/manifest.yaml` exists; `skill` equals the frontmatter `name`; `simulator` is a known id; every entry in
  `assertions_supported` is a known type; `target.board`, `target.framework` and `target.framework_version` are
  set.
- `evals/tasks/` contains at least one task; each task's `id` equals its filename stem, `level` is valid and
  `prompt` is non-empty.
- Every assertion's `type` is known and declared in `assertions_supported`.
- At least one assertion in the package is stronger than `compile_only`.

It does not check assertion fields, the `build` or `flash` blocks, fixtures, `eval_validated`, or whether any
assertion can fail. Those are Phase 0's job.

### L1 — simulator pre-check

**Not built.** The runner will follow Phase 2's procedure in a simulator: give the agent the prompt, freeze the
result, build, load the artefact into the declared simulator, and evaluate every assertion not marked
`l1_skippable`, measuring `within_s` in simulated time. It will reuse each simulator's own assertion layer —
Renode's `renode-test` keywords such as `Wait For Line On Uart`, Wokwi's scenario expectations — rather than
scraping console output, and it will report how many assertions it skipped. A task that fails L1 is not worth
taking to a bench; a task that passes L1 has still not passed.

## Reference: the eval package

```
my-skill/
├── SKILL.md
└── evals/
    ├── manifest.yaml
    ├── tasks/
    │   ├── 01-easy-thing.yaml
    │   ├── 02-medium-thing.yaml
    │   └── 03-hard-thing.yaml
    └── fixtures/
        └── <task-id>/
            ├── reference/        # Phase 0 check 1, and the Phase 1 self-test
            └── broken/           # Phase 0 check 3
```

Aim for three tasks — easy, medium, hard. One task says nothing about whether the skill generalises; many more
make Phase 3 expensive.

### manifest.yaml

| Field | Required | Meaning |
|---|---|---|
| `skill` | yes | Equal to `name` in the SKILL.md frontmatter. |
| `version` | no | Version of the eval package. Bump it whenever a task or assertion changes; Phase 0 must be redone. |
| `target.board` | yes | Exact board identifier or arduino-cli FQBN — never a family name. |
| `target.framework` | yes | `esp-idf`, `arduino`, `zephyr`, `ros2`, and so on. |
| `target.framework_version` | yes | The version the tasks were validated against. |
| `target.toolchain` | no | What the agent is expected to invoke: `idf.py`, `arduino-cli`, `west`. |
| `simulator` | yes | Where L1 pre-checks will run: `wokwi`, `renode`, `qemu`, `native_sim`, `gazebo`, `isaac`, `mujoco`, `webots`, `ha-demo`, `modbus-sim`, `opcua-sim`, or `none`. It has no bearing on passing, and `none` costs nothing. |
| `assertions_supported` | yes | Every assertion type any task uses. |
| `eval_validated` | for L2 | Phase 0 record. Attestations are not accepted without it. |
| `verified.L0` | no | `{date, run}` once `l0_check.py` passes. |
| `verified.L1` | reserved | Written by the L1 runner. |
| `verified.L2` | no | Accepted attestations, added by a maintainer. |
| `ab.*` | no | Phase 3 results with sample sizes. |

### Task files

One file per task in `tasks/`; the filename stem must equal `id`.

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Equal to the filename stem; numbered so tasks sort by difficulty. |
| `level` | yes | `easy`, `medium` or `hard`. |
| `timeout_s` | no | Wall-clock budget for the agent's attempt. |
| `prompt` | yes | Everything the agent is told. If a competent engineer would need a hint, put it here. |
| `build.cmd`, `build.cwd` | no | The build run on the frozen copy. |
| `flash.cmd` | no | The flash command; `{port}` is replaced with the board's port. Defaults to the toolchain's standard flash command. |
| `human_action` | no | A physical action the tester performs, and when, e.g. `press the button on GPIO39 once, 5 s after time zero`. |
| `assertions` | yes | All must pass for the run to pass. |
| `fixtures` | no | Paths to reference outputs such as an expected serial log. |

### Assertion types

Any assertion may set `l1_skippable: true` when a simulator cannot evaluate it. That only affects L1: on a real
board every assertion is evaluated.

| Type | Observes | Fields |
|---|---|---|
| `compile_only` | `build.cmd` exits 0 | none |
| `serial_match` | UART output | `baud`, `pattern` (regular expression, per line), `min_matches`, `within_s` |
| `gpio_state` | Pin levels over time | `pin`, `expect` (e.g. `toggles`), `min_edges`, `within_s` |
| `bus_capture` | Traffic on a bus | `bus` (e.g. `ble`), `expect` (bus-specific, e.g. `adv_name`, `service_uuid`, `char_uuid`, `notify_count_min`, `within_s`) |
| `exit_code` | A script's result | `cmd`, `expect` |
| `network_probe`, `ros_topic`, `file_exists` | — | Reserved; defined by the first package that needs one |

`compile_only` alone proves almost nothing about hardware, so every package needs at least one assertion
stronger than it. Prefer a runtime observation to `exit_code` whenever one exists; use `exit_code` for properties
no observation can catch, such as the absence of a forbidden call that happens not to break the board.

## Worked example

[fxp/m5stack-embedded-dev-skill](https://github.com/fxp/m5stack-embedded-dev-skill) targets the M5Stack Core2 with
Arduino and M5Unified, and is the first listed skill with an eval package. Measured against this plan:

- **Package shape — good.** Three tasks at three levels; exact FQBN; `simulator: none` with the reason stated;
  assertions that observe serial output rather than judging code.
- **Phase 0 — not done.** There are no `reference/` or `broken/` solutions and no `eval_validated` record. Done,
  it would have caught two defects: task 02's `exit_code` passes on an empty project (check 2), and task 03's
  `exit_code` passes a blocking handler written without `IRAM_ATTR` (check 3). Both fixes are one line each and
  are shown in the Phase 0 section above.
- **Phase 2 — needs a `human_action`.** Task 03's serial assertion waits for a real button press on GPIO39, but
  the task does not say when to press it. Adding `human_action: press the button on GPIO39 once, 5 s after time
  zero` makes the run reproducible.
- **Status: `L0`. Not passed.** The path to passing is Phase 0 by the author, then three runs per task on a Core2
  by anyone who owns one.

## Extending the plan

To add a simulator id or an assertion type, open a pull request that:

1. Adds it to `SIMULATORS` or `ASSERTION_TYPES` in `scripts/l0_check.py`.
2. For an assertion type, adds a row to the assertion table, a measurement method under "Measuring each
   assertion on a real board", and the instrument it needs to the test-bench table — and explains how it can
   fail.
3. For a simulator, adds it to the README's verification infrastructure section.
4. Updates `EVALS.zh-CN.md`, or leaves the `translation-sync` job failing for a maintainer to fix.
