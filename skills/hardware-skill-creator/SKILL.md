---
name: hardware-skill-creator
description: Create or improve an Agent Skill for a microcontroller board, SDK, robot or instrument together with an eval package that is proven on the physical board — tasks with observable serial, GPIO and bus assertions, reference/broken/spoof fixtures, Phase 0 validation, bench runs, L2 attestation and ΔPass A/B statistics, following the awesome-hardware-skills EVALS.md test plan. Use this whenever someone wants to write a SKILL.md for ESP32, nRF52, STM32, RP2040, Arduino, Zephyr, ESP-IDF, M5Stack or any embedded target, add evals to an existing hardware skill, check whether hardware eval assertions can actually fail, run or record tests of a skill on a real board, or compute pass rates and ΔPass for one — even if they only say "turn this firmware know-how into a skill" or "how do I prove my skill works on the board".
---

# Hardware Skill Creator

Helps a hardware developer turn what they know about a board into an Agent Skill, and prove it works with an
eval package that runs on the real board. It follows the test plan in EVALS.md of
[awesome-hardware-skills](https://github.com/chopinfeng/awesome-hardware-skills); a package built this way can be
listed there and attested.

The whole method rests on one rule, and everything you say to the user must respect it: **a skill passes only when
its tasks ran on a physical board and every assertion held.** Static checks and simulators are pre-checks. Never
call a skill passing, validated or verified on the strength of anything less, and never write a result, chip ID,
log line or `eval_validated` field that did not come from an actual observation.

**When the user is not there to answer**, keep going: make the conventional choice, write every decision you made
on their behalf into `evals/DECISIONS.md` (task designs, interpretations of the request, facts you could not
verify), and list them in your reply so they can overturn any of them. Proposals that normally wait for agreement
still get written down; they just do not block.

Talk to the user in their language. Hardware developers know UART, strapping pins and logic analysers; they may not
know eval vocabulary, so define *assertion*, *fixture*, *Phase 0* and *ΔPass* in a sentence the first time.

## Where is the user?

Find the stage, then start there. Check the conversation and the filesystem before asking.

| What exists | Start at |
|---|---|
| An idea, or know-how in chat, notes or a firmware repo | 1 Capture the target |
| A SKILL.md with no `evals/` | 1 briefly, then 3 Design tasks |
| An `evals/` package | 5 Static checks, then fix what they find |
| Tasks plus filled `reference/`, `broken/`, `spoof/` fixtures | 6 Phase 0 on the board |
| `eval_validated` recorded | 8 Bench runs, attestation, ΔPass |

## 1. Capture the target

Pull answers out of the conversation first (commands the user ran, boards they named, errors they hit), then ask
only for what is missing. You need:

1. **Exact board and revision**, and the chip family (`esp32`, `nrf52`, `stm32`, `rp2040`, other).
2. **Framework, exact version, toolchain** (`esp-idf 5.2.2` + `idf.py`; `arduino-esp32 3.0.4` + `arduino-cli` + FQBN).
3. **What agents should be able to do with the skill**, and the mistakes models make today on this board. Those
   mistakes become the tasks, so push for concrete ones.
4. **Instruments on the bench**: USB serial only, logic analyser, BLE sniffer, CAN adapter. Assertions are limited
   to what can be observed.
5. **Power**: battery on board? How is it switched fully off?
6. **Boards available** and whether the user can dedicate one to testing. Every run erases it.

## 2. Draft or review the skill

Read `references/writing-hardware-skills.md`. Write SKILL.md and `references/` around exact identity, pinned
versions, the board's traps, the build-flash-observe loop, recovery and safety. Research the vendor's datasheets
and docs where you can; cite what you rely on. Keep the knowledge-vs-answer line in mind from the start — it is
much cheaper than removing answers after the tasks exist.

## 3. Design three tasks

Read `references/eval-format.md` ("Designing tasks"). For each of easy, medium and hard, propose to the user:

| | Task | Mistake it catches | Assertions (instrument) | human_action |
|---|---|---|---|---|

Write each prompt as a real user would, but with **every value an assertion matches stated in it**: pin, string,
UUID, rate, baud. State them unambiguously: "toggle GPIO5 every 500 ms", not "at 2 Hz", which can mean toggles or
cycles. Give rates both bounds (`max_matches`, `max_edges`) so output that is far too fast fails. Prefer runtime
observations over `exit_code`. Get the user's agreement on the table before writing files; a wrong task costs a
Phase 0 session on the bench.

## 4. Scaffold and fill

```bash
python scripts/init_skill.py <name> --board <board> --framework <fw> --framework-version <ver> \
    --family <esp32|nrf52|stm32|rp2040|other> --toolchain <tool> --task-ids <easy>,<medium>,<hard> --out <dir>
```

Skip the scaffold when the skill already exists; copy only `evals/` from a scratch scaffold into it. Then:

- Replace every `TODO:` and delete each `PLACEHOLDER.md` as you fill its directory. Check `boot_banner` and
  `reboot_patterns` against `references/families.md` for the exact chip, not just the family.
- Write the fixtures. **reference/**: a complete, buildable, known-good solution that also prints the chip's unique
  ID at boot. **broken/**: the realistic version of the task's target mistake, not a caricature. **spoof/**:
  firmware that fakes the observed signals without doing the task (see `references/test-plan.md`, Phase 0).
- Build every fixture on the host if the toolchain is installed, out of tree so the package stays clean (see
  "Building fixtures" in `references/eval-format.md`). A reference that does not compile wastes a bench session.
- If a spoof slips past every assertion, follow "When the schema cannot catch a spoof" in the same file.

## 5. Static checks

First confirm the toolchain actually runs (`idf.py --version`, `arduino-cli version`, `west --version`). With it
missing, every build "fails in an empty directory" for the wrong reason; `check_package.py` reports exit 126/127 as
an error for that reason.

```bash
python scripts/l0_check.py skill <skill-dir>          # the awesome list's L0 gate (needs pyyaml)
python scripts/check_package.py <skill-dir> --run-empty
```

`--run-empty` executes the package's `exit_code` and build commands in an empty directory. Run it on packages you
or the user wrote; read the commands first if the package came from elsewhere.

Before a board is available, you can still test the serial assertion logic: write short synthetic logs for the
reference, the spoof and a crash loop in the format `bench.py` documents, and run `bench.py serial` on them. That
finds wrong windows and patterns early. Synthetic logs are never evidence, and never go into `eval_validated`.

Fix every ERROR. Go through every REVIEW line with the user — leakage and prompt wording are judgements, and the
user owns them. Neither script can tell whether an assertion catches the broken or spoof fixture; only the board
can.

## 6. Phase 0 on the board

Read `references/test-plan.md` (Phase 0 and "Board reset"). For each task: reference passes, empty project fails
every assertion, broken is caught, spoof is caught.

**Erasing and flashing destroys whatever is on the board.** Before the first erase or flash, confirm with the user
which port and board are the test board. After that, within the session, you may drive the loop yourself when the
board is attached:

```bash
idf.py -C evals/fixtures/<id>/reference -p <port> flash            # or the task's own build/flash commands
python scripts/bench.py capture --port <port> --baud 115200 --seconds 15 --out p0-<id>-reference.log --reset rts
python scripts/bench.py serial p0-<id>-reference.log evals/tasks/<id>.yaml --manifest evals/manifest.yaml
```

GPIO and bus assertions need the user's instruments; tell them exactly what to capture, for how long, and which
file to hand back, then evaluate it together. Power removal and button presses are the user's hands.

When a check fails, decide with the user whether the eval or the fixture is wrong, fix it, and repeat that check.
When all four hold for every task, write `eval_validated` with the date, board revision, framework version and a
link or path to the logs. If some check could not be run (no sniffer, say), leave the record empty and say which
check is missing.

## 7. Improve the skill

Development runs tell you where the skill is weak. With the board attached, give an agent a task prompt with the
skill installed through `bench.py install` (which strips `evals/`), then the same prompt with no skill. Run them
one at a time — one board, one run. Read the transcripts, not only the result:

- Where did the agent guess, retry builds, or pick the wrong pin? Add the missing **knowledge**, never the answer.
- Did it read the skill at all? If not, the `description` is the problem.
- Did every run write the same helper (port finder, log parser)? Bundle it in the skill's `scripts/`.

These runs share your filesystem with the eval, so they are development signal only. Never report them as passes or
as ΔPass. Any change to a task or assertion bumps `version` and sends you back to step 6.

## 8. Bench runs, attestation, ΔPass

For the real test — by the author or, better, by other people with their own boards — walk the tester through
`references/test-plan.md`: host baseline, board reset, verbatim prompt, freeze, build, flash, observe, validity
before results, one record per run from `assets/run-record.yaml`.

```bash
python scripts/stats.py task pass fail pass          # two of at most three
python scripts/stats.py wilson 5 6                   # pooled pass rate with interval
python scripts/stats.py delta 12 15 6 15             # ΔPass with Newcombe interval and label
```

Report ΔPass as the interval and label the script prints. At five runs per task per arm most results are
`inconclusive`; say so plainly rather than calling a +20 a gain.

The tester files the **L2 hardware attestation** issue in awesome-hardware-skills with the records permalink and
SHA256SUMS digest. A maintainer reviews it and records `verified.L2`.

## 9. Triggering and publishing

- If the user has Claude's skill-creator, use its description optimisation loop, with near-miss boards and SDKs as
  should-not-trigger queries.
- Publish the skill in its own repository with `evals/` included (it is stripped at run time, not at publish time),
  and add `l0_check.py` to its CI.
- Add it to awesome-hardware-skills with a pull request following that repo's CONTRIBUTING.md. Its status is L0
  until an attestation is accepted.

## Files in this skill

| Path | Read or run when |
|---|---|
| `references/writing-hardware-skills.md` | Drafting SKILL.md: what to include, knowledge vs answers, safety, description |
| `references/eval-format.md` | Writing manifest and tasks: fields, assertion types and how each is measured, designing tasks, vacuous checks |
| `references/test-plan.md` | Phase 0-3, isolation, board reset, reboot guard, verdicts, attestation |
| `references/families.md` | Chip ID, erase, boot banner and fatal patterns per chip family |
| `assets/run-record.yaml` | Template for one run record |
| `scripts/init_skill.py` | Scaffold a skill with an eval package |
| `scripts/check_package.py` | Checks L0 does not: TODOs, prompt states matched values, fixtures, vacuous commands, leakage hints |
| `scripts/l0_check.py` | Copy of the awesome list's L0 checker (`skill` mode) |
| `scripts/bench.py` | Install without evals, hash, freeze, serial capture, serial assertions + reboot guard |
| `scripts/stats.py` | Task verdict, Wilson interval, ΔPass with Newcombe interval |

Paths above are relative to this skill's directory; call the scripts by their full path from the user's project.
Scripts need Python 3.9+ and `pyyaml`; `bench.py capture` also needs `pyserial`.
