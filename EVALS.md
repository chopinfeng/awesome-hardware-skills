# Hardware skill evals: test plan

*English · [简体中文](EVALS.zh-CN.md)*

This document is the test plan behind the badges in the [README](README.md). It says exactly how a hardware
skill is tested, on what, by whom, how many times, how each assertion is measured on a real board, how the eval
is kept out of the agent's reach, what gets recorded, and when the result counts. Why the effort is worth it is
argued in [GAPS.md](GAPS.md).

The one rule everything else serves: **a skill passes only when its tasks have run on a physical board and its
assertions held.** Static checks and simulators are pre-checks. Nothing else is called passing in this repo.

## What exists today

Read this first — the rest of the document describes the whole plan, and it is easy to mistake a planned piece
for a working one.

| Piece | Status |
|---|---|
| Eval package format | Defined in this document; starter in `template/evals/` |
| `L0` static checks | **Working**, in CI — `python scripts/l0_check.py skill <path>` |
| Authoring help | **Working** — [`skills/hardware-skill-creator/`](skills/hardware-skill-creator/), an Agent Skill that scaffolds a package, runs checks L0 does not (vacuous commands, prompt values, fixtures, leakage hints), and helps run Phases 0–3 |
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

A skill can pass question 1 and still show no measurable gain on question 2 — the model may already know how.
Both results are published.

Neither question can be answered until a third one is: **is the eval itself trustworthy?** An assertion that
passes when nothing was done, or when the agent faked the signal, or when the agent read the answer, tells you
nothing about the skill. That is what Phase 0 and the isolation rules exist for, and they come first.

## The plan at a glance

| Phase | Who | When | Purpose | Output |
|---|---|---|---|---|
| 0 — validate the eval | Package author | Once per eval version | Prove the tasks are achievable and the assertions can fail | `eval_validated` in the manifest |
| 1 — bench self-test | Tester | Start and end of every session | Prove the bench works, so failures can be blamed on the skill | Self-test record |
| 2 — pass runs | Tester | Per attestation | Decide whether the skill passes | Run records, `L2` attestation |
| 3 — A/B | Tester | Optional, per attestation | Measure what the skill adds | `ΔPass` with its interval |

## The test bench

Everything below is recorded in each run record. Two runs on different benches are not comparable.

**Target board.** The exact board named in `target.board`, including its revision or module variant where the vendor sells more than one, e.g. `esp32-c3-devkitm-1 ESP32-C3-MINI-1`.
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

### Host baseline

Resetting the board is not enough; the host carries state between runs too. Harness memory and configuration
(for example `~/.claude/`, a project `CLAUDE.md`, auto-memory), toolchain-wide library and component caches
(Arduino libraries and cores, ESP-IDF managed components) and shell history all survive a run. A library the
agent installed during a with-skill run quietly helps the without-skill run after it, shrinking `ΔPass`.

Prepare a **baseline** once — a fresh OS user account, a container image or a VM snapshot that already holds the
toolchain at the pinned version — and restore it before every run, discarding anything the previous run added.
Record its identifier as `host_baseline`. A run started from anything else is invalid.

### Chip identity

Every run records the chip's own unique identifier, so that runs, self-tests and attestations can be tied to one
physical part:

| Family | Where the ID comes from |
|---|---|
| ESP32 series | The `MAC:` line esptool prints when it connects during flashing, or `esptool read-mac` |
| nRF52 | FICR `DEVICEID`, e.g. `nrfjprog --memrd 0x10000060 --n 8` |
| STM32 | The 96-bit unique-ID register, read through the debug probe; its address depends on the family |
| RP2040 / RP2350 | The board ID reported by `picotool info` (on RP2040, the flash chip's unique ID) |

Record the serial port's USB serial number as well; on many boards with native USB it is derived from the chip.
Simulators can be given any ID, so this does not prove silicon on its own — see Review for what it does catch.

## Keeping the eval out of reach

Frontier models, when they can, read graders and answer keys: METR observed reward hacking — returning the
grader's precomputed answers, patching scoring functions, searching for leaked reference implementations — in
30.4% of runs on one task suite, and telling the model not to cheat barely changed the rate. An eval package that
sits beside `SKILL.md` puts the reference solution, the broken solution and every assertion pattern inside the
installed skill. Four rules close that off:

1. **Install the skill without its eval.** Copy the skill for the run with `evals/` and any `.git` directory
   removed. Keep the eval package, its fixtures and any grading scripts in a location the agent's harness cannot
   read, and run every assertion from that copy.
2. **Detect tampering.** Record the SHA-256 of the installed skill directory before the agent starts and after it
   finishes. If they differ, or the transcript shows the agent reading or changing an eval, fixture or grading
   file, the run fails with `failure_class: tampered`.
3. **No answers in the skill.** A skill teaches knowledge; it must not contain a task's answer. Knowledge is a fact
   about the part — the M5Stack Core2's power-management IC answers at I2C address `0x34`, so a skill that says so
   is doing its job. An answer is specific to the eval — a task's reference code, its file names, or an output
   string written exactly as an assertion matches it. The author checks for this in Phase 0 and the reviewer
   checks again; it is a judgement, not a regex, because the same constant can be either.
4. **The prompt states everything an assertion matches.** Every pin, string, UUID, rate and baud that an assertion
   checks must appear in the prompt. Otherwise a correct solution that chose a different but valid value fails,
   and the eval is measuring guesswork.

## Phase 0 — validate the eval

**Who:** the package author, before asking anyone to attest. **When:** once per eval package version, and again
whenever a task or assertion changes.

An eval is only as good as its ability to tell a correct solution from a wrong one. For every task, the author
prepares solutions and runs four checks on the real board:

```
evals/fixtures/<task-id>/reference/   a known-good solution; prints the chip ID at boot
evals/fixtures/<task-id>/broken/      a solution containing the specific mistake the task exists to catch
evals/fixtures/<task-id>/spoof/       firmware that fakes the observed signals without doing the task
```

1. **The reference passes.** Build, flash and observe the reference solution. Every assertion passes, including
   those marked `l1_skippable`. This proves the task can be done on this board and no assertion is too strict.
2. **An empty project fails.** Run every assertion against an empty working directory. Every assertion fails.
   This catches checks that pass when nothing was built.
3. **The broken solution is caught.** Build, flash and observe the broken solution. The assertion aimed at that
   mistake fails. This catches checks that pass when the wrong thing was built.
4. **The spoof is caught.** Build, flash and observe firmware written to fool the assertions rather than do the
   task — printing every expected line in a loop, toggling the pin from a timer, advertising the expected name
   with no GATT service, or crash-looping so a boot message repeats. At least one assertion, or the reboot guard,
   fails. If nothing does, add an assertion tied to the real behaviour: a bus capture, an edge timed against an
   input, a value that depends on a sensor.

Checks 2, 3 and 4 catch different defects, and a package needs all of them. The first third-party package in this
list shows why for 2 and 3. One task forbids calling `Wire.begin()` again and checks with
`! grep -q "Wire.begin(" *.ino`. Run against an empty directory, that check exits 0: `grep` cannot find `*.ino`,
and `!` turns its error into a pass. Check 2 catches it; check 3 would not, because a broken solution does contain
an `.ino`. Another task forbids blocking calls in an interrupt handler and locates the handler by matching
`IRAM_ATTR`. Against an empty directory it correctly fails — but against a handler that calls `Serial.println`
and `delay` without `IRAM_ATTR`, it exits 0. Check 2 misses it; only check 3 catches it. Check 4 exists because a
serial regular expression is the easiest signal on a board to fake, and neither of the others tries.

The reference solution prints the chip's unique ID at boot, which binds every self-test log in Phase 1 to the
chip. Agent tasks never ask for this: adding it to a prompt would change what the agent is asked to do and
contaminate `ΔPass`.

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
  board: esp32-c3-devkitm-1 ESP32-C3-MINI-1
  framework_version: "5.2.2"
  reference_passed: true      # check 1, every task
  empty_failed: true          # check 2, every assertion
  broken_caught: true         # check 3, every task
  spoof_caught: true          # check 4, every task
  leakage_reviewed: true      # the skill contains no task's answer
  evidence: https://...       # logs and captures from the four checks
```

## Phase 1 — bench self-test

**Who:** the tester. **When:** at the start and the end of every test session.

Flash each task's `reference/` solution and evaluate its assertions, exactly as in a Phase 2 run but with no
agent. Every assertion must pass, and the chip ID the reference prints must match the ID recorded at flashing.
For ESP32-series boards, also record the eFuse summary (`espefuse summary`) at both self-tests. Take one photo per
session of the board cabled to the host with the terminal visible — it is the one piece of evidence a simulator
cannot produce.

A session's results count only if **both** self-tests pass. If the closing self-test fails, every run in the
session is **invalid** — the bench may have failed at any point — and is rerun in a new session. If the eFuse
summary changed between the two, the run that burned it fails and the board is retired from attestation, because
eFuse bits cannot be cleared.

## Phase 2 — pass runs

**Who:** the tester. **When:** for every attestation.

### Procedure for one run

1. **Record the run metadata** listed under the test bench above, and assign the run the next sequential number.
2. **Reset the board to a known state.**
   - Erase the whole flash with the toolchain's erase command and keep its output. If the erase is refused because
     Secure Boot or Flash Encryption is active — esptool refuses by default — the board cannot be used for
     attestation.
   - Remove all power, including batteries, for at least 5 seconds, and confirm it is off by an indicator going
     dark or a current reading. A hub's port-power command counts only with that confirmation; many hubs do not
     actually cut power. Boards with a battery keep running when USB is unplugged — the M5Stack Core2, for
     example, has to be switched off by holding its power button for 6 seconds.
   - Remove or reformat any SD card, and reset any external peripheral that has its own supply.
3. **Restore the host baseline** and install the skill without `evals/` or `.git`. Record the SHA-256 of the
   installed skill directory.
4. **Start the agent and the transcript recording.** Give the agent the task's `prompt` verbatim and nothing
   else — no port name, no hint, no correction — unless the prompt itself contains it.
5. **Let the agent work** until it declares it is done or `timeout_s` elapses on the wall clock. A timeout is a
   failed run, not an invalid one.
6. **Freeze the result.** Archive the working directory and record its SHA-256, and record the installed skill
   directory's SHA-256 again. Everything after this point uses the frozen copy; the agent's own builds and flashes
   during its attempt are not evidence, though their counts are recorded.
7. **Build.** Run `build.cmd` in the frozen copy and keep the log. If it fails, `compile_only` fails and every
   other assertion is recorded as `not-run`.
8. **Flash.** Erase, then write the build with `flash.cmd` if the task defines one, otherwise the toolchain's
   standard flash command. Keep the flash tool's full output, including the lines where it reports the detected
   chip and its unique ID.
9. **Observe.** Start every capture before releasing reset. **Time zero** is the moment reset is released and the
   new firmware begins to run; every `within_s` window is measured from there. Serial is captured from time zero
   until the longest window closes, for the reboot guard below. Carry out any `human_action` the task defines, at
   the time it defines, and log the timestamp.
10. **Decide whether the run is valid** from bench evidence alone — before reading any assertion result.
11. **Evaluate each assertion** using the methods in the next section, and keep its raw evidence file.
12. **Record the result.** Each assertion is `pass`, `fail` or `not-run`. The run passes only if every assertion
    passed and the reboot guard held. A failed run records one `failure_class`: `build`, `flash`, `crash`,
    `behaviour`, `timeout` or `tampered`.

### Reboot and panic guard

A firmware that crashes and reboots prints its boot output again every time, so a crash loop can satisfy
`min_matches` on its own. Every run therefore fails if, after time zero, the serial capture shows a reboot or a
fatal error — unless the task sets `expect_reset: true`.

The boot that time zero starts is expected, so the guard uses two manifest fields. `boot_banner` matches a line
printed exactly once per boot; a second match after time zero is a reboot. `reboot_patterns` match fatal output;
any match after time zero fails the run. For the ESP32 series the defaults are `^rst:0x` as the banner — the ROM
prints one such line per boot — and a panic (`Guru Meditation|abort\(\) was called|assert failed:|Backtrace:`) and a brown-out
(`Brownout detector`) as fatal patterns. Packages for other families define their own; where the platform prints
no banner, the reference and the prompt print a fixed line first thing. On a board with native USB serial, the
port re-enumerating after time zero also counts as a reboot.

### How a task and a package pass

- **Run:** passes if every assertion passes, including those marked `l1_skippable`, and the reboot guard holds.
- **Task:** passes when **two of at most three** runs pass. Run it twice; if both runs agree, that decides the task;
  if they split, a third run decides it. This reaches exactly the same verdict as always running three and taking
  the majority, with fewer runs. Agents are not deterministic, so one run is a single draw.
- **Package:** passes if every task passes. That is the `L2` badge.
- **Reporting:** every attestation lists each task's `k/n` and the pooled pass rate of all counted runs with a 95%
  Wilson interval. The verdict is a gate, not a reliability claim: a task whose agent succeeds on only half its
  attempts still passes this gate half the time, and the published rate is what shows it.
- **`L2 ×N`** counts attestations that each reached a pass on a **different chip** (by chip ID) submitted from a
  **different account**. A second attestation on a chip already counted is welcome but adds nothing to ×N.

Every run started is reported, in order: passes, failures and invalid runs alike. Choosing which runs to count is
not allowed; an invalid run is rerun, and both appear in the record.

### Failed run or invalid run

A **failed** run is a result about the skill. An **invalid** run is a result about the bench, and is rerun.
The distinction is decided by bench evidence, before assertion results are read:

| Invalid — rerun | Failed — counts |
|---|---|
| The session's closing self-test failed | The agent timed out |
| The model API or harness crashed for reasons unrelated to the task | The agent flashed the wrong port or wrong target |
| The board was physically disconnected, with a note of when | The build or flash failed on the frozen copy |
| The tester gave the agent information not in the prompt | The board is left unbootable by the agent's firmware |
| The run did not start from the recorded host baseline | The reboot guard fired |
| | The agent read or changed the eval, or the installed skill changed (`tampered`) |
| | Any assertion failed |

The fourth invalid case matters: a run where the tester helped is not a fail, but it is not evidence of a pass
either. A run that burned an eFuse fails, and additionally retires the board.

## Phase 3 — A/B for ΔPass

**Who:** the tester. **When:** optional, alongside Phase 2.

1. Run each task **five** times in each of two arms, on the same board, model and harness, following the Phase 2
   procedure and restoring the host baseline before every run:
   - **With skill:** the skill installed, without its eval.
   - **Without skill:** no skill installed at all.
2. **Alternate the arms** — with, without, with, without — so that drift in the bench, the board or the model API
   affects both equally.
3. From each with-skill transcript, record **`skill_invoked`** — whether the agent actually loaded or read the
   skill. A skill that never loads looks exactly like a skill with nothing in it.
4. For each arm record, across all runs of all tasks, the **pass rate** and the **first-compile-ok rate** — the
   share of runs whose first build during the attempt succeeded without the agent fixing anything — each as
   `k/n` with a 95% Wilson interval. Also record per run the number of builds and flashes, tokens, cost and
   wall-clock time.
5. Report **`ΔPass`** as described in the next subsection, overall and again restricted to runs where the skill was
   invoked, together with each task's own difference. If the skill was invoked in fewer than four of a task's five
   with-skill runs, mark the result `trigger-weak`: the skill's `description` is not getting it loaded.

First-compile-ok is tracked because it is where hardware skills earn their keep. A wrong register name, a
missing `sdkconfig` symbol, the wrong FQBN — models often recover after two or three failed builds, so the pass
rate alone can hide a skill that saves real iterations.

### Reading ΔPass honestly

Five runs per task per arm is fifteen runs per arm for a three-task package, and at that size the numbers are
noisy. With both arms around 50%, the smallest difference such a comparison can reliably detect is about 45
percentage points. A true 15-point gain would need roughly 150 runs per arm, and a skill with no effect at all
shows an apparent gain of 15 points or more about one time in five by chance. A single number with a fixed
threshold would mislabel skills constantly, so `ΔPass` is always published as an interval with a label:

- **`ΔPass`** is the with-skill pass rate minus the without-skill pass rate, with a 95% **Newcombe** interval —
  the standard interval for a difference of two proportions, built from each arm's Wilson interval and accurate
  at small samples, unlike the familiar ±1.96 × standard error.
- **`gain`** when the interval's lower bound is above zero.
- **`low-gain`** when its upper bound is below +15 points — evidence that the skill adds little.
- **`inconclusive`** otherwise.

For example, `ΔPass +20 pts [−12, +47] (15 v 15), inconclusive` and `ΔPass +67 pts [+34, +85] (15 v 15), gain`.
At this plan's run counts most results will be `inconclusive`, and `low-gain` is out of reach below roughly a
hundred runs per arm. That is the honest label, not a defect: the fix for noise is to say so, not to hide it.

```python
from math import sqrt

def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

def delta_pass(k_with, n_with, k_without, n_without):
    p1, p2 = k_with / n_with, k_without / n_without
    l1, u1 = wilson(k_with, n_with)
    l2, u2 = wilson(k_without, n_without)
    d = p1 - p2
    lo = d - sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = d + sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    label = "gain" if lo > 0 else "low-gain" if hi < 0.15 else "inconclusive"
    return d, lo, hi, label
```

This reproduces the published reference value for Newcombe's method (56/70 v 48/80 gives 0.200 [0.052, 0.334]).

Results from different attestations are combined by pooling each bench's `ΔPass`, never by pooling raw runs
across benches. A tester who wants to stop early may use a sequential test such as STEP, but only if its error
rate and maximum runs per arm are recorded in the manifest's `sequential_plan` before the first A/B run.

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
- **Capture** at the task's `baud` to a log file, one line per record with a host timestamp, and record the
  port's USB serial number. Within 10 seconds of the observation window closing, run the chip-identity command on
  the same port without unplugging, so the log is tied to the chip.
- **Match** per line after normalising line endings, using `pattern` as a regular expression. Pass if at least
  `min_matches` lines match within `within_s` of time zero, and, when `max_matches` is set, no more than that many.
- **Tasks with a `human_action`:** the lines the action is meant to trigger must not match before the action. Mark
  those assertions `after_human_action: true`. That control window catches firmware that prints the expected
  output without the stimulus.

### `gpio_state`

- Connect a logic-analyser channel to `pin`, with a common ground.
- Sample at no less than ten times the fastest edge rate the task implies; 1 MHz is ample for anything slower
  than a few kilohertz.
- Capture for at least `within_s` from time zero and save the raw capture, e.g. a sigrok `.sr` file.
- For `expect: toggles`, count edges in the window and pass if the count is at least `min_edges` and, when
  `max_edges` is set, at most that. An upper bound catches a pin toggled far faster than asked.

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

Every run, including self-tests and invalid runs, produces one record. Keep them with the evidence files they
reference, commit the directory, and add a `SHA256SUMS` file covering every file in it.

```yaml
run: 7
session: 2026-09-20-a
phase: pass                       # self-test | pass | ab-with | ab-without
task: 01-blink
skill: {repo: https://github.com/owner/skill, commit: 3f2a9c1}
eval_version: 0.1.0
board: esp32-c3-devkitm-1 ESP32-C3-MINI-1
chip_id: "30:ed:a0:88:88:a0"
serial_port: {device: /dev/ttyACM0, usb_serial: "30:ED:A0:88:88:A0"}
host: {os: Ubuntu 24.04, framework_version: "5.2.2", baseline: vm-snapshot-2026-09-20}
agent: {model: claude-opus-5, harness: claude-code 2.1.3, network: true, session_id: 1f7c...}
started: 2026-09-20T10:14:03Z
ended:   2026-09-20T10:21:47Z
agent_outcome: declared-done      # declared-done | timeout
skill_dir_sha256: {before: 5ac0..., after: 5ac0...}
skill_invoked: true
effort: {builds: 3, flashes: 2, first_build_ok: false, tokens_in: 184233, tokens_out: 9120, cost_usd: 2.41, wall_s: 464}
workdir_sha256: 9b1e...
build: {exit: 0, log: runs/07/build.log}
flash: {exit: 0, log: runs/07/flash.log, detected_chip: "ESP32-C3 (QFN32) (revision v0.4)"}
time_zero: 2026-09-20T10:22:15.402Z
human_actions: []                 # e.g. [{at: "+5.0s", action: "pressed button on GPIO39"}]
reboot_guard: pass
assertions:
  - {type: compile_only, result: pass}
  - {type: serial_match, result: pass, matches: 6, evidence: runs/07/serial.log}
  - {type: gpio_state,   result: pass, edges: 12, evidence: runs/07/gpio5.sr}
result: pass                      # pass | fail | invalid
failure_class: null               # build | flash | crash | behaviour | timeout | tampered
invalid_reason: null
transcript: {path: runs/07/transcript.jsonl, sha256: e40d...}
```

### Attestation

Open an issue with the **L2 hardware attestation** form. It asks for the skill and commit, the exact board and
revision, the chip ID, the framework version, the agent model and harness, every run's result, both bench
self-tests, the hardware evidence, one bench photo per session, and a permalink to the committed run records with
the SHA-256 of their `SHA256SUMS` file. It requires confirming that the runs were on a physical board, that every
run started from the host baseline with the eval out of the agent's reach, that every run is reported, that no
hints were given, and that the transcripts are unedited.

## Review

A maintainer checks an attestation before recording it in the manifest's `verified.L2`:

- The package's `eval_validated` covers the version that was tested, including `spoof_caught` and
  `leakage_reviewed`.
- Both self-tests passed in every session whose runs are counted, and the eFuse summary did not change.
- The same `chip_id` appears in every run and self-test, it matches what the flash tool reported, and it is not a
  known simulator value — Wokwi's default ESP32 MAC `24:0a:c4:00:01:10`, an all-zero ID, Renode's nRF52840
  `DEVICEADDR[0]` of `0xAABBCCDD`, or an STM32 UID that changes between runs, which is what Renode's STM32F4
  Discovery script produces.
- The records are at a commit permalink and their `SHA256SUMS` matches the digest in the attestation.
- Every task shows its runs in sequence, decided by the two-of-at-most-three rule, with invalid runs explained.
- **Re-score at least one run per task** from its raw evidence — the serial log, the `.sr` capture, the `.pcapng` —
  and confirm it gives the recorded result, including the reboot guard.
- The transcripts show the prompt given verbatim, no help from the tester, and no reading of the eval; the
  installed skill's hashes match before and after.

An attestation missing any of this is sent back with the specific gap, not rejected silently. QEMU, Wokwi and
Renode can all be configured with an arbitrary chip ID, so these checks catch careless, copied and repeated
results, not a determined fabricator; independent reproductions on different chips, counted by `×N`, are the
defence against that.

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
- `evals/tasks/` contains at least one task; each task's `id` equals its filename stem, `level` is valid, `prompt`
  is non-empty and `timeout_s` is set.
- Every assertion's `type` is known and declared in `assertions_supported`.
- At least one assertion in the package is stronger than `compile_only`.

It does not check assertion fields, the `build` or `flash` blocks, fixtures, `eval_validated`, leakage, or whether
any assertion can fail. Those are Phase 0's job.

### L1 — simulator pre-check

**Not built.** The runner will follow Phase 2's procedure in a simulator: give the agent the prompt, freeze the
result, build, load the artefact into the declared simulator, and evaluate every assertion not marked
`l1_skippable`, measuring `within_s` in simulated time. It will reuse each simulator's own assertion layer —
Renode's `renode-test` keywords such as `Wait For Line On Uart`, Wokwi's scenario expectations — rather than
scraping console output, and it will report how many assertions it skipped. Once it runs alongside real
attestations, it will publish how often L1 and L2 agree. A task that fails L1 is not worth taking to a bench; a
task that passes L1 has still not passed.

## Reference: the eval package

```
my-skill/
├── SKILL.md
└── evals/                        # removed from the skill before every run
    ├── manifest.yaml
    ├── tasks/
    │   ├── 01-easy-thing.yaml
    │   ├── 02-medium-thing.yaml
    │   └── 03-hard-thing.yaml
    └── fixtures/
        └── <task-id>/
            ├── reference/        # Phase 0 check 1, and the Phase 1 self-test
            ├── broken/           # Phase 0 check 3
            └── spoof/            # Phase 0 check 4
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
| `boot_banner` | for L2 | Regular expression matching a line printed exactly once per boot. A second match after time zero is a reboot. |
| `reboot_patterns` | for L2 | Regular expressions for fatal output; any match after time zero fails the run. Defaults exist for the ESP32 series; other families define their own. |
| `eval_validated` | for L2 | Phase 0 record. Attestations are not accepted without it. |
| `sequential_plan` | no | Pre-registered error rate and maximum runs per arm, if Phase 3 will stop early. |
| `verified.L0` | no | `{date, run}` once `l0_check.py` passes. |
| `verified.L1` | reserved | Written by the L1 runner. |
| `verified.L2` | no | Accepted attestations, added by a maintainer. |
| `ab.*` | no | Phase 3 results: `k/n` per arm, `ΔPass` with its interval and label. |

### Task files

One file per task in `tasks/`; the filename stem must equal `id`.

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Equal to the filename stem; numbered so tasks sort by difficulty. |
| `level` | yes | `easy`, `medium` or `hard`. |
| `timeout_s` | yes | Wall-clock budget for the agent's attempt. |
| `prompt` | yes | Everything the agent is told, including every value an assertion matches. |
| `build.cmd`, `build.cwd` | no | The build run on the frozen copy. |
| `flash.cmd` | no | The flash command; `{port}` is replaced with the board's port. Defaults to the toolchain's standard flash command. |
| `human_action` | no | A physical action the tester performs, and when, e.g. `press the button on GPIO39 once, 5 s after time zero`. Opens a control window before the action. |
| `expect_reset` | no | `true` if the task legitimately resets the board, which disables the reboot guard for it. |
| `assertions` | yes | All must pass for the run to pass. |
| `fixtures` | no | Paths to reference outputs such as an expected serial log. |

### Assertion types

Any assertion may set `l1_skippable: true` when a simulator cannot evaluate it. That only affects L1: on a real
board every assertion is evaluated.

| Type | Observes | Fields |
|---|---|---|
| `compile_only` | `build.cmd` exits 0 | none |
| `serial_match` | UART output | `baud`, `pattern` (regular expression, per line), `min_matches`, `within_s`, optional `max_matches` and `after_human_action` |
| `gpio_state` | Pin levels over time | `pin`, `expect` (e.g. `toggles`), `min_edges`, `within_s`, optional `max_edges` |
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
- **Leakage — passes.** Its references state that the Core2's AXP192 answers at `0x34` and that `M5.begin()` already
  owns the I2C bus. That is knowledge about the part, which is what a skill is for; no task's output format or
  solution code appears in it.
- **Phase 0 — not done.** There are no `reference/`, `broken/` or `spoof/` solutions and no `eval_validated` record.
  Done, it would have caught two defects: task 02's `exit_code` passes on an empty project (check 2), and task 03's
  `exit_code` passes a blocking handler written without `IRAM_ATTR` (check 3). Both fixes are one line each and are
  shown in the Phase 0 section above.
- **Phase 2 — needs a `human_action` and a real power-off.** Task 03's serial assertion waits for a button press on
  GPIO39, but the task does not say when to press it; adding `human_action: press the button on GPIO39 once, 5 s
  after time zero` makes the run reproducible and gives it a control window. And the Core2 runs on its internal
  battery, so step 2's power removal means holding the power button for 6 seconds, not unplugging USB.
- **Status: `L0`. Not passed.** The path to passing is Phase 0 by the author, then runs on a Core2 by anyone who
  owns one.

## What this plan draws on

- [METR, *Recent frontier models are reward hacking*](https://metr.org/blog/2025-06-05-recent-reward-hacking/) —
  agents read graders and leaked solutions; why the eval is kept out of reach.
- [SkillsBench](https://arxiv.org/abs/2602.12670) — skill evaluation at scale: an automated gate rejecting skills
  that leak task solutions, counting a trial only when the skill was actually invoked, and self-generated skills
  scoring below no skill at all.
- [Terminal-Bench](https://arxiv.org/abs/2601.11868) — oracle solutions that must pass, do-nothing agents that must
  fail, and an adversarial exploit agent; the model for Phase 0 checks 1, 2 and 4.
- [Establishing Best Practices for Building Rigorous Agentic Benchmarks](https://arxiv.org/abs/2507.02825) — the
  Agentic Benchmark Checklist, including benchmarks that counted empty responses as successes.
- [Adding Error Bars to Evals](https://www.anthropic.com/research/statistical-approach-to-model-evals) and
  [Don't Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints](https://arxiv.org/abs/2503.01747) —
  why results carry intervals, and why small-sample intervals must not use the normal approximation.
- [Is Your Imitation Learning Policy Better than Mine?](https://arxiv.org/abs/2503.10966) — STEP, sequential testing
  for comparing two policies with a pre-set error rate and maximum trials.
- [IoT-SkillsBench](https://arxiv.org/abs/2603.19583) and [Embedded Arena](https://arxiv.org/abs/2606.16190) — the
  closest prior work evaluating agents on real embedded hardware.
- [esptool](https://docs.espressif.com/projects/esptool/en/latest/esp32/esptool/basic-commands.html),
  [M5Stack Core2](https://docs.m5stack.com/en/core/core2), [Wokwi ESP32](https://docs.wokwi.com/guides/esp32) and
  [Renode nRF52840](https://github.com/renode/renode/blob/master/platforms/cpus/nrf52840.repl) — the specific facts
  behind the reset procedure and the simulator ID checks.

## Extending the plan

To add a simulator id or an assertion type, open a pull request that:

1. Adds it to `SIMULATORS` or `ASSERTION_TYPES` in `scripts/l0_check.py`.
2. For an assertion type, adds a row to the assertion table, a measurement method under "Measuring each
   assertion on a real board", and the instrument it needs to the test-bench table — and explains how it can
   fail, and how a spoof of it would be caught.
3. For a simulator, adds it to the README's verification infrastructure section.
4. Updates `EVALS.zh-CN.md`, or leaves the `translation-sync` job failing for a maintainer to fix.
