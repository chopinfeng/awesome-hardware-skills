# hardware-skill-creator

*English · [简体中文](README.zh-CN.md)*

An Agent Skill that helps hardware developers write their own skill for a board, SDK or instrument, together with
an eval package that proves it on the physical board. It does for hardware what Claude's
[skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) does for skills in general,
and it follows the test plan in [EVALS.md](../../EVALS.md).

The rule it enforces: **a skill passes only when its tasks ran on a physical board and every assertion held.**

## What it does with you

1. Captures the exact board, revision, framework version, instruments and the mistakes models make on that board.
2. Drafts the SKILL.md around facts the model gets wrong, keeping task answers out of it.
3. Designs three tasks (easy, medium, hard), each built around one mistake, with assertions a board can show.
4. Scaffolds the package and writes the reference, broken and spoof fixtures.
5. Runs static checks, including the defects L0 cannot see.
6. Runs Phase 0 on the board with you: the reference passes, an empty project fails, the broken and spoof
   fixtures are caught.
7. Uses development runs to improve the skill, then guides bench runs, the L2 attestation and ΔPass statistics.

## Install

Copy the skill without its own `evals/` into your agent's skills directory. For Claude Code:

```bash
rsync -a --exclude evals skills/hardware-skill-creator ~/.claude/skills/
```

Then ask for it in your own words, for example "turn my notes on the Core2's power IC into a skill with evals".
The scripts need Python 3.9+ and `pyyaml`. Serial capture also needs `pyserial`.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/init_skill.py` | Scaffold a skill and eval package for `esp32`, `nrf52`, `stm32`, `rp2040` or `other` |
| `scripts/check_package.py` | Checks L0 does not: leftover TODOs, prompt values, fixtures, vacuous commands, leakage hints |
| `scripts/l0_check.py` | A copy of this repository's L0 checker; CI keeps the two identical |
| `scripts/bench.py` | Install without `evals/`, hash, freeze, serial capture, serial assertions with the reboot guard |
| `scripts/stats.py` | Two-of-three task verdict, Wilson interval, ΔPass with Newcombe interval |

`scripts/test_skill_creator.py` at the repository root tests them in CI.

## Status

This skill has its own eval package in `evals/`: three tasks on an ESP32-C3-DevKitM-1 in which the agent must
produce a package whose reference firmware works on the board. Phase 0 has not been done for it. Its status is
`L0`, and it has not passed.
