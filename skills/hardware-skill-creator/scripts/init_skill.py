#!/usr/bin/env python3
"""Scaffold a hardware skill with an eval package that follows EVALS.md.

  init_skill.py <name> --board esp32-c3-devkitm-1 --framework esp-idf --framework-version 5.2 \
      --family esp32 [--toolchain idf.py] [--simulator wokwi] [--task-ids toggle,boot-button,isr-count] [--out DIR]

Creates <out>/<name>/ with SKILL.md, references/, evals/manifest.yaml, evals/tasks/*.yaml and
evals/fixtures/<task-id>/{reference,broken,spoof}/. Every place that needs a human decision is marked
TODO:; check_package.py fails until none are left. The scaffold passes L0 on purpose, so the author
can run the static checks from the first minute.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FAMILIES = {
    "esp32": {
        "boot_banner": r"^rst:0x",
        "reboot_patterns": [
            r"Guru Meditation|abort\(\) was called|assert failed:|Backtrace:",
            r"Brownout detector",
        ],
        "chip_id": "esptool read-mac (or the MAC: line esptool prints while flashing)",
        "erase": "idf.py -p {port} erase-flash  (or: esptool --port {port} erase-flash)",
    },
    "nrf52": {
        "boot_banner": r"\*\*\* Booting (Zephyr OS|nRF Connect SDK)",
        "reboot_patterns": [
            r"ZEPHYR FATAL ERROR|Halting system",
        ],
        "chip_id": "nrfjprog --memrd 0x10000060 --n 8  (FICR DEVICEID)",
        "erase": "nrfjprog --eraseall  (or: nrfutil device erase --all)",
    },
    "stm32": {
        "boot_banner": "TODO: a line printed exactly once per boot, e.g. print boot first thing in main",
        "reboot_patterns": ["HardFault"],
        "chip_id": "read the 96-bit UID register through the debug probe; address depends on the series",
        "erase": "STM32_Programmer_CLI -c port=SWD -e all",
    },
    "rp2040": {
        "boot_banner": "TODO: a line printed exactly once per boot, e.g. print boot first thing in main",
        "reboot_patterns": ["TODO: text your firmware prints on a fatal error, e.g. a panic handler line"],
        "chip_id": "picotool info (board ID)",
        "erase": "flash flash_nuke.uf2, or picotool erase if your picotool has it",
    },
    "other": {
        "boot_banner": "TODO: a line printed exactly once per boot",
        "reboot_patterns": ["TODO: the fatal-error text your platform prints"],
        "chip_id": "TODO: the command that reads this chip's unique ID",
        "erase": "TODO: the command that erases the whole flash",
    },
}
LEVELS = ["easy", "medium", "hard"]
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}[a-z0-9]$")


def skill_md(a: argparse.Namespace) -> str:
    return f"""---
name: {a.name}
description: "TODO: say what this skill lets an agent do on the {a.board} with {a.framework} {a.framework_version}, and list the phrases, part numbers and symptoms that should load it, even when the user does not name the board."
---

# TODO: title

TODO: one paragraph: what the agent can build with this skill, on which exact board and framework version.

## Before touching the board

- TODO: how to find the port, and how to tell this board from a sibling board.
- TODO: commands that must never run without the user's explicit request (eFuse burns, Secure Boot,
  Flash Encryption, option bytes, OTP writes).

## Build, flash, observe

TODO: the exact commands for {a.toolchain or a.framework}, and how to read the board's output after flashing.

## Facts the model gets wrong

TODO: the knowledge this skill exists for: pin assignments on this board revision, bus addresses,
required config symbols, framework-version differences, errata. Facts about the part, never a task's answer.

## References

- `references/` TODO: datasheet excerpts and cheatsheets, each named in a sentence saying when to read it.
"""


def manifest(a: argparse.Namespace, task_ids: list[str]) -> str:
    fam = FAMILIES[a.family]
    patterns = "\n".join(f"  - '{p}'" for p in fam["reboot_patterns"])
    return f"""# Eval package for {a.name}. The method is EVALS.md in awesome-hardware-skills.
# This whole evals/ directory is removed from the skill before any agent run.

skill: {a.name}
version: 0.1.0

target:
  board: {a.board}                      # exact board id and revision you validate on, never a family
  framework: {a.framework}
  framework_version: "{a.framework_version}"
  toolchain: {a.toolchain or a.framework}

# L1 pre-check only; passing always needs a physical board.
simulator: {a.simulator}

assertions_supported:
  - compile_only
  - serial_match
  - gpio_state
  - exit_code

# Chip unique ID: {fam["chip_id"]}
# Full erase before every run: {fam["erase"]}

# Phase 0 record. Fill it only after all five checks ran on the board.
eval_validated: null   # {{date, board, framework_version, reference_passed, empty_failed, broken_caught, spoof_caught, exploit_caught, leakage_reviewed, evidence}}

# Trigger pre-check on the host (evals/trigger_queries.json). Never a pass.
trigger_eval: null     # {{date, model, runs_per_query, should_trigger: k/n, should_not_trigger: k/n}}

# Reboot guard: the boot that time zero starts prints boot_banner once; a second banner is a reboot.
# Any line matching reboot_patterns after time zero fails the run.
boot_banner: '{fam["boot_banner"]}'
reboot_patterns:
{patterns}

sequential_plan: null

verified:
  L0: null
  L1: null
  L2: []

ab:
  baseline_model: null
  pass_rate_with: null
  pass_rate_without: null
  first_compile_ok_with: null
  first_compile_ok_without: null
"""


def task(a: argparse.Namespace, tid: str, level: str) -> str:
    return f"""id: {tid}
level: {level}
timeout_s: 900

# TODO: the exact request a user would type. It must state every pin, string, UUID, rate and baud that an
# assertion below matches, and must not ask for the chip ID banner (that belongs to the reference only).
prompt: |
  TODO:

build:
  cmd: "TODO: build command run in the frozen working directory"

flash:
  cmd: "TODO: flash command, with {{port}} where the port goes"

# TODO: the mistake this task exists to catch (the broken fixture contains exactly this mistake):
# TODO:

assertions:
  - type: compile_only
  - type: serial_match
    baud: 115200
    pattern: 'TODO:'
    min_matches: 1
    within_s: 5
"""


def fixture_readme(kind: str, tid: str) -> str:
    text = {
        "reference": "A known-good solution. Every assertion passes on the board, and it prints the chip's unique ID at boot "
        "so Phase 1 self-test logs are tied to the chip. Phase 0 check 1 and the Phase 1 self-test flash this.",
        "broken": "A plausible solution containing exactly the mistake the task exists to catch. At least the assertion aimed "
        "at that mistake must fail on the board (Phase 0 check 3).",
        "spoof": "Firmware that fakes the observed signals without doing the task: prints every expected line in a loop, "
        "toggles the pin from a timer, advertises the name with no service, or crash-loops. An assertion or the reboot "
        "guard must fail on the board (Phase 0 check 4).",
    }[kind]
    return f"# {tid} / {kind}\n\nTODO: replace this file with the {kind} solution.\n\n{text}\n"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("name")
    p.add_argument("--board", required=True)
    p.add_argument("--framework", required=True)
    p.add_argument("--framework-version", required=True)
    p.add_argument("--family", choices=sorted(FAMILIES), required=True)
    p.add_argument("--toolchain")
    p.add_argument("--simulator", default="none")
    p.add_argument("--tasks", type=int, default=3)
    p.add_argument("--task-ids", help="comma-separated task slugs in difficulty order, e.g. toggle,boot-button,isr-count")
    p.add_argument("--out", default=".")
    a = p.parse_args()

    if not NAME_RE.match(a.name):
        print("name must be lowercase letters, digits and hyphens, 3-64 chars", file=sys.stderr)
        return 2
    root = Path(a.out) / a.name
    if root.exists():
        print(f"{root} already exists; refusing to overwrite", file=sys.stderr)
        return 2

    if a.task_ids:
        ids = [f"{i + 1:02d}-{slug}" for i, slug in enumerate(a.task_ids.split(","))]
        if any(not re.match(r"^\d{2}-[a-z0-9][a-z0-9-]*$", t) for t in ids):
            print("--task-ids takes short slugs such as toggle,boot-button,isr-count", file=sys.stderr)
            return 2
    else:
        ids = [f"{i + 1:02d}-todo-{LEVELS[min(i, 2)]}" for i in range(a.tasks)]
    (root / "references").mkdir(parents=True)
    (root / "references" / "PLACEHOLDER.md").write_text("TODO: replace with datasheet excerpts, pinouts, cheatsheets; then delete this file.\n")
    (root / "SKILL.md").write_text(skill_md(a))
    (root / "evals" / "tasks").mkdir(parents=True)
    (root / "evals" / "manifest.yaml").write_text(manifest(a, ids))
    for i, tid in enumerate(ids):
        (root / "evals" / "tasks" / f"{tid}.yaml").write_text(task(a, tid, LEVELS[min(i, 2)]))
        for kind in ("reference", "broken", "spoof"):
            d = root / "evals" / "fixtures" / tid / kind
            d.mkdir(parents=True)
            (d / "PLACEHOLDER.md").write_text(fixture_readme(kind, tid))
    (root / "evals" / "trigger_queries.json").write_text(
        '[\n  {"query": "TODO: a request that should load this skill", "should_trigger": true},\n'
        '  {"query": "TODO: a near miss that should not, e.g. the same task on another chip", "should_trigger": false}\n]\n')
    print(f"created {root}")
    print("next: replace every TODO: and each fixture's PLACEHOLDER.md, then run check_package.py on it")
    return 0


if __name__ == "__main__":
    sys.exit(main())
