# Test plan, condensed

The operational core of EVALS.md in awesome-hardware-skills
(https://github.com/chopinfeng/awesome-hardware-skills/blob/main/EVALS.md). When the two differ, EVALS.md wins.
Read this when you reach Phase 0 with the author, or when you guide a tester through Phase 1-3.

Contents: the rule · isolation · Phase 0 · Phase 1 · Phase 2 (one run, reset, reboot guard, verdict,
failed vs invalid) · Phase 3 · run record · attestation and review

## The rule

A skill passes only when its tasks ran on a physical board and every assertion held, including ones marked
`l1_skippable`. Static checks (L0) and simulators (L1) are pre-checks. Hosted virtual boards do not count; a
remote farm that flashes a real board does. Never tell a user their skill "passed" on anything less.

Two questions, answered separately: does the skill work (Phase 2, the L2 badge), and does it add anything over
no skill (Phase 3, `ΔPass`). Neither means anything until the eval itself is shown trustworthy (Phase 0).

## Keeping the eval out of reach

Agents read graders and answer keys when they can (METR measured it in 30.4% of runs on one suite, and asking
them not to barely helped). So:

1. **Install the skill without `evals/` and `.git`.** `scripts/bench.py install <skill> <dest>` does this and
   prints the tree hash. Keep the eval package and grading scripts where the agent's harness cannot read.
2. **Detect tampering.** Hash the installed skill before and after (`bench.py hash`). A difference, or a
   transcript showing the agent reading or editing an eval file, fails the run with `failure_class: tampered`.
3. **No answers in the skill.** Knowledge about the part is the point of a skill; a task's reference code, file
   names, or an output string written exactly as an assertion matches it is an answer. A judgement, not a
   regex: `check_package.py` prints REVIEW lines to look at, and the author decides.
4. **The prompt states every value an assertion matches** — pin, string, UUID, rate, baud. Otherwise a correct
   solution with a different valid choice fails and the eval measures guesswork.

## Phase 0 — validate the eval (author, once per eval version)

For every task, on the real board:

| Check | Fixture | Must happen | Catches |
|---|---|---|---|
| 1 reference passes | `fixtures/<id>/reference/` | every assertion passes | impossible task, over-strict assertion |
| 2 empty project fails | an empty directory | every assertion fails | checks that pass when nothing was built |
| 3 broken is caught | `fixtures/<id>/broken/` | the assertion aimed at the mistake fails | checks that pass when the wrong thing was built |
| 4 spoof is caught | `fixtures/<id>/spoof/` | an assertion or the reboot guard fails | signals faked without doing the task |

Checks 2, 3 and 4 find different defects; a package needs all of them. The reference prints the chip's unique ID
at boot (so Phase 1 logs bind to the chip); task prompts never ask for this.

`check_package.py --run-empty` does the host half of check 2 for `exit_code` and `build.cmd`. Serial, GPIO and bus
assertions against an empty project are trivially failing only if nothing else is on the board, so the author
still erases the board and observes once.

Typical spoofs to write: print every expected line in a loop; toggle the pin from a timer; advertise the name with
no GATT service; crash-loop so a boot line repeats. If nothing catches a spoof, add an assertion tied to real
behaviour: a bus capture, an edge timed against an input, a value that depends on a sensor.

Record in `manifest.yaml`:

```yaml
eval_validated:
  date: 2026-09-20
  board: esp32-c3-devkitm-1 ESP32-C3-MINI-1
  framework_version: "5.2.2"
  reference_passed: true
  empty_failed: true
  broken_caught: true
  spoof_caught: true
  leakage_reviewed: true
  evidence: https://...        # logs and captures from the four checks
```

Bump `version` and redo Phase 0 whenever a task or assertion changes.

## Phase 1 — bench self-test (tester, start and end of every session)

Flash each task's reference, evaluate its assertions with no agent. All must pass, and the chip ID the reference
prints must equal the one the flash tool reported. ESP32 series: record `espefuse summary` at both. One photo per
session of the board cabled to the host with the terminal visible.

If the closing self-test fails, every run in the session is invalid and is rerun. If the eFuse summary changed,
the run that burned it fails and the board is retired.

## Phase 2 — pass runs (tester, per attestation)

### One run

1. Record metadata and assign the next run number.
2. **Reset the board** (see below).
3. **Restore the host baseline** (a fresh OS user, container image or VM snapshot with the pinned toolchain) and
   install the skill without `evals/`. Harness memory (`~/.claude/`, `CLAUDE.md`), library caches and shell
   history otherwise leak between runs. Record the baseline id and the skill hash.
4. Start the agent and transcript. Give the prompt verbatim, nothing else.
5. Let it work until it declares done or `timeout_s` passes (timeout = failed, not invalid).
6. **Freeze**: `bench.py freeze <workdir> run-NN.tar.gz`; hash the installed skill again.
7. **Build** the frozen copy with `build.cmd`. If it fails, `compile_only` fails, the rest are `not-run`.
8. **Flash**: erase, then `flash.cmd`. Keep the output lines that show the detected chip and its ID.
9. **Observe**: start every capture before releasing reset. Time zero = reset released. Do each `human_action`
   at its stated time and log it.
10. **Decide validity from bench evidence alone, before reading any assertion result.**
11. Evaluate each assertion; keep raw evidence (`serial.log`, `.sr`, `.pcapng`).
12. Record `pass` / `fail` / `not-run` per assertion; one `failure_class` for a failed run:
    `build | flash | crash | behaviour | timeout | tampered`.

### Board reset

- Full flash erase, keep the output. If erase is refused because Secure Boot or Flash Encryption is on, the board
  cannot be used for attestation.
- Remove all power, batteries included, for at least 5 s, and confirm it is off (LED dark or a current reading).
  Hub port-power commands count only with that confirmation. Battery boards need their own power-off (M5Stack
  Core2: hold power 6 s).
- Remove or reformat SD cards; reset externally powered peripherals.

### Reboot and panic guard

A crash loop reprints boot output and can satisfy `min_matches` alone. After time zero the run fails if:

- `boot_banner` (a line printed exactly once per boot) matches more than once — the boot time zero starts is
  expected, a second one is a reboot; or
- any line matches `reboot_patterns` (panics, fatal errors, brown-outs); or
- a native-USB port re-enumerates.

Tasks that legitimately reset set `expect_reset: true`. `bench.py serial` implements this.

### Verdict

- **Run** passes if every assertion passed and the guard held.
- **Task** passes when two of at most three runs pass: run twice; if they agree that decides it; if they split,
  a third decides. `stats.py task pass fail pass` computes it.
- **Package** passes if every task passes → L2.
- Report each task's `k/n` and the pooled pass rate with a 95% Wilson interval (`stats.py wilson K N`).
- `L2 ×N` counts passes on distinct chips (by chip ID) from distinct accounts.
- Every run started is reported, in order. Choosing runs is not allowed.

### Failed or invalid

| Invalid — rerun | Failed — counts |
|---|---|
| closing self-test failed | agent timed out |
| model API or harness crashed, unrelated to the task | agent flashed the wrong port or target |
| board physically disconnected (noted when) | build or flash failed on the frozen copy |
| tester gave information not in the prompt | board left unbootable by the agent's firmware |
| run did not start from the recorded host baseline | reboot guard fired |
| | agent read or changed the eval (`tampered`) |
| | any assertion failed |

## Phase 3 — A/B for ΔPass (optional)

1. Each task five times per arm, same board, model and harness, host baseline restored every run.
   With skill (without its eval) vs. no skill at all.
2. Alternate arms: with, without, with, without.
3. Record `skill_invoked` from each with-skill transcript. Invoked in fewer than 4 of 5 → `trigger-weak`: fix the
   `description`, not the body.
4. Per arm: pass rate and first-compile-ok rate as `k/n` with Wilson intervals; per run builds, flashes, tokens,
   cost, wall time.
5. Report `ΔPass` = with − without, with a 95% Newcombe interval: `stats.py delta KW NW KO NO`.
   - `gain`: lower bound > 0
   - `low-gain`: upper bound < +15 pts
   - `inconclusive`: otherwise

At 15 v 15 most results are `inconclusive`, and `low-gain` needs roughly 100+ runs per arm. Say so; do not round
a noisy +20 into "the skill helps". Combine benches by pooling each bench's `ΔPass`, never raw runs. Early
stopping (e.g. STEP) only with error rate and max runs pre-registered in `sequential_plan`.

## Run record

`assets/run-record.yaml` is the template. Every run, self-tests and invalid runs included, gets one. Commit the
records with their evidence and a `SHA256SUMS` covering all files.

## Attestation and review

The tester opens the **L2 hardware attestation** issue form in awesome-hardware-skills: skill + commit, board +
revision, chip ID, framework version, model + harness, both self-tests, every run, hardware evidence, bench photos,
a commit permalink to the records and the SHA-256 of `SHA256SUMS`.

A maintainer checks: `eval_validated` covers the tested version; self-tests passed; the same chip ID everywhere and
not a known simulator value (Wokwi ESP32 MAC `24:0a:c4:00:01:10`, all zeros, Renode nRF52840 `0xAABBCCDD`, an STM32
UID that changes between runs); digests match; runs follow the two-of-three rule; at least one run per task
re-scored from raw evidence; transcripts show verbatim prompts, no help, no eval reading, matching skill hashes.
