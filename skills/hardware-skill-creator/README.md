# hardware-skill-creator

*English · [简体中文](README.zh-CN.md)*

An Agent Skill that helps hardware developers write their own skill for a board, SDK or instrument, together with
an eval package that proves it on the physical board. It does for hardware what Claude's
[skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) does for skills in general,
and it follows the test plan in [EVALS.md](../../EVALS.md).

The rule it enforces: **a skill passes only when its tasks ran on a physical board and every assertion held.**

## Install

**Claude Code, as a plugin.** This repository is a plugin marketplace. In Claude Code:

```
/plugin marketplace add chopinfeng/awesome-hardware-skills
/plugin install hardware-skill-creator@awesome-hardware-skills
```

From a shell, the same thing:

```bash
claude plugin marketplace add chopinfeng/awesome-hardware-skills
claude plugin install hardware-skill-creator@awesome-hardware-skills
```

Update later with `claude plugin marketplace update awesome-hardware-skills`, then
`claude plugin update hardware-skill-creator@awesome-hardware-skills`.

**Any agent that reads SKILL.md folders**, by copying the directory:

```bash
git clone https://github.com/chopinfeng/awesome-hardware-skills
rsync -a --exclude evals awesome-hardware-skills/skills/hardware-skill-creator ~/.claude/skills/
```

Point the destination at your agent's skills directory. The `evals/` folder is this skill's own test and is not
needed for normal use.

**Requirements.** Python 3.9+ with `pyyaml` for the scripts, `pyserial` for serial capture, and your board's
toolchain (ESP-IDF, arduino-cli, west, …) on `PATH`.

## Use

Ask in your own words. The skill works out which stage you are at and continues from there.

| You have | Say something like |
|---|---|
| Know-how, no skill yet | "Turn my notes on the M5Stack Core2's power IC into a skill with evals." |
| A skill without evals | "Add an eval package to `./my-esp32-skill` for the ESP32-S3-DevKitC-1." |
| An eval package | "Check whether the assertions in `./my-skill/evals` can actually fail." |
| A board on the desk | "Run Phase 0 for task 02 on the board at /dev/ttyUSB0." |
| Test runs done | "Work out the task verdicts and ΔPass from these run records." |

A typical session:

1. **Target.** You give the exact board, framework version, instruments, and the mistakes models make on it.
2. **Skill.** The agent drafts SKILL.md and `references/` with facts about the part, keeping task answers out.
3. **Tasks.** It proposes three tasks built around those mistakes, with assertions the board can show. You approve.
4. **Package.** It scaffolds `evals/` and writes the reference, broken and spoof firmware for each task.
5. **Static checks.** L0 plus the checks L0 cannot do, such as assertions that pass on an empty project.
6. **Phase 0 on the board.** It asks which port is the test board, then flashes each fixture and evaluates the
   assertions with you. Logic analyser, sniffer and button presses are your hands.
7. **Improve and test.** Development runs show where the skill is weak; the bench runs of Phases 1-3 decide.

The scripts also work without an agent:

```bash
S=skills/hardware-skill-creator/scripts
python $S/init_skill.py my-skill --board esp32-c3-devkitm-1 --framework esp-idf --framework-version 5.2 \
    --family esp32 --toolchain idf.py --task-ids toggle,boot-button,isr-count --out .
python $S/check_package.py my-skill --run-empty
python $S/bench.py capture --port /dev/ttyUSB0 --seconds 15 --out run.log --reset rts
python $S/bench.py serial run.log my-skill/evals/tasks/01-toggle.yaml --manifest my-skill/evals/manifest.yaml
python $S/stats.py delta 12 15 6 15
```

## Submit results

There are three kinds of submission, and they go to different places. Evidence always lives in a git commit, so
anyone can check it later against a hash.

| What | Who | Where it goes |
|---|---|---|
| A skill with an eval package | Skill author | Pull request adding the entry to this list |
| Phase 0 validation | Skill author | Commit in the skill's own repository |
| Test runs on a board (L2) | Anyone with the board | Records in a git repository, then an attestation issue here |

### 1. List your skill (pull request)

```bash
gh repo fork chopinfeng/awesome-hardware-skills --clone
cd awesome-hardware-skills
git checkout -b add-my-skill
# Add one line to the right category of README.md, in the format CONTRIBUTING.md gives.
# If you read Chinese, add the translated line at the same place in README.zh-CN.md.
python scripts/l0_check.py readme README.md
python scripts/l0_check.py skill /path/to/my-skill
git commit -am "Add my-skill"
git push -u origin add-my-skill
gh pr create --repo chopinfeng/awesome-hardware-skills --title "Add my-skill" \
    --body "Skill with an evals/ package. L0 passes locally. Phase 0: not yet done / done at <permalink>."
```

A new skill is listed at `L0`. It has not passed until an attestation is accepted.

### 2. Record Phase 0 (commit in your skill's repository)

Commit the fixtures and the Phase 0 evidence (serial logs, captures, the flash tool output) to your skill's
repository, for example under `evals/phase0/<eval-version>/`. Put that commit's permalink in `eval_validated.evidence`
and commit again. A permalink contains the commit SHA, not a branch name:

```
https://github.com/<you>/<skill-repo>/tree/<commit-sha>/evals/phase0/0.1.0
```

If the skill is already listed, open a pull request here that mentions Phase 0 in the entry's description.

### 3. Report test runs on a board (records, then an attestation issue)

1. **Save the records in a repository you control.** Fork the skill's repository, or use any repository of yours.
   Put one session's files in one directory: a run record per run (template in `assets/run-record.yaml`), the
   build and flash logs, serial logs, `.sr` and `.pcapng` captures, bench photos and agent transcripts.

   ```
   evals/runs/2026-09-20-esp32-c3-devkitm-1-<your-github-name>/
   ├── runs/01/record.yaml  build.log  flash.log  serial.log  gpio5.sr  transcript.jsonl
   ├── runs/02/...
   ├── self-test-start/ and self-test-end/
   └── bench.jpg
   ```

2. **Check transcripts before publishing.** They can contain API keys, tokens, Wi-Fi passwords, home directory
   paths and other private data. Redact secrets by replacing them with `[REDACTED]` and say so in the issue; any
   other edit makes the transcript unusable as evidence.

3. **Hash, commit and push.**

   ```bash
   cd evals/runs/2026-09-20-esp32-c3-devkitm-1-<you>
   find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 shasum -a 256 > SHA256SUMS
   shasum -a 256 SHA256SUMS            # this digest goes into the issue
   git add . && git commit -m "L2 runs: esp32-c3-devkitm-1, 2026-09-20" && git push
   git rev-parse HEAD                  # this SHA goes into the permalink
   ```

4. **Open the attestation issue** at
   <https://github.com/chopinfeng/awesome-hardware-skills/issues/new?template=attestation.yml>. It asks for the
   skill and the commit you tested, the board, the chip ID, versions, every run in order with its result, the
   self-tests, hardware evidence, photos, the records permalink and the `SHA256SUMS` digest.
   This skill's `stats.py task` and `stats.py wilson` produce the numbers it asks for.

5. **Optionally, open a pull request to the skill's repository** adding your records directory, so the author keeps
   a copy.

What happens next: a maintainer reviews the issue against the checklist in EVALS.md, re-scores at least one run per
task from your raw files, and asks for anything missing. Once accepted, the maintainer opens a pull request here
that sets the entry's badge (for example `L2 ×1`, and `ΔPass` if you ran Phase 3), and asks the skill author to
append the attestation to `verified.L2` in the manifest. Testers do not edit badges themselves.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/init_skill.py` | Scaffold a skill and eval package for `esp32`, `nrf52`, `stm32`, `rp2040` or `other` |
| `scripts/check_package.py` | Checks L0 does not: leftover TODOs, prompt values, fixtures, vacuous or unrunnable commands, leakage hints |
| `scripts/l0_check.py` | A copy of this repository's L0 checker; CI keeps the two identical |
| `scripts/bench.py` | Install without `evals/`, hash, freeze, serial capture, serial assertions with the reboot guard |
| `scripts/stats.py` | Two-of-three task verdict, Wilson interval, ΔPass with Newcombe interval |

`scripts/test_skill_creator.py` at the repository root tests them in CI.

## Status

This skill has its own eval package in `evals/`: three tasks on an ESP32-C3-DevKitM-1 in which the agent must
produce a package whose reference firmware works on the board. Phase 0 has not been done for it. Its status is
`L0`, and it has not passed.
