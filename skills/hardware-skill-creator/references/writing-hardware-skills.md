# Writing the hardware skill itself

Read this while drafting SKILL.md and its references for a board, SDK or instrument. General skill-writing
advice (progressive disclosure, explaining the why, imperative voice) applies; this file covers what is different
when the skill drives real hardware.

Contents: what belongs in a hardware skill · knowledge vs answers · safety · the description · structure

## What belongs in a hardware skill

The model already knows C, Python and the general shape of most SDKs. A hardware skill earns its place with facts
the model gets wrong or cannot see, and with the loop that lets the agent check its own work on the board:

- **Exact identity.** Board name and revision, module, chip, FQBN or build target, and how to tell it from look-alike
  boards ("Core2 vs Core2 v1.1", "DevKitM-1 vs DevKitC-02"). Wrong-target builds are the most common failure.
- **Pinned versions.** The framework version the skill was validated against, and what changed across versions the
  model may mix up (ESP-IDF 4.x vs 5.x driver APIs, Arduino-ESP32 2.x vs 3.x, NCS vs upstream Zephyr).
- **The board's traps.** Pins that are strapping, input-only, shared with flash or PSRAM, or wired to on-board
  parts; bus addresses already used on the board; peripherals a framework call already initialises; power rails
  gated by a PMIC; errata.
- **Build, flash, observe.** The exact commands, how to find the port, how to read serial after flashing, what a
  healthy boot log looks like, and what common failure logs mean. This is what turns the agent's attempt into a
  closed loop.
- **Recovery.** How to get the board back into download or bootloader mode when firmware breaks USB.

Put long material (pinout tables, register maps, log examples) in `references/` and point to it from SKILL.md with
a sentence saying when to read it.

## Knowledge vs answers

A skill must not contain a task's answer. The line is judgement, so reason about it explicitly with the author:

| Knowledge — keep | Answer — remove |
|---|---|
| "The Core2's AXP192 PMIC answers at I2C `0x34`." | "Print `found 0x34`." when a task asserts exactly that string |
| "`M5.begin()` already initialises the internal I2C bus; do not call `Wire.begin()` again." | A complete sketch that scans I2C the way task 02 wants |
| "GPIO8 drives the on-board LED on this board." | The blink task's reference `main.c` |
| A generic ISR-safe pattern (set a flag, handle it in the loop) | The reference solution of the ISR task, verbatim |

Test: would this sentence still be worth having if the eval did not exist? If yes, it is knowledge. If it only makes
sense next to one task's assertion, it is an answer. `check_package.py` flags verbatim overlaps as REVIEW lines;
the author decides and records `leakage_reviewed: true` only after reading them.

## Safety

Real boards can be damaged or locked, and some operations are permanent. The skill should make the agent:

- Ask before anything irreversible: eFuse burns, Secure Boot, Flash Encryption, readout protection, OTP writes,
  option bytes, bootloader replacement.
- Confirm the port and target before flashing when more than one board is attached.
- Respect electrical limits it states (pin voltage tolerance, current per pin, 3.3 V vs 5 V logic) and never
  suggest driving loads directly from GPIO beyond them.
- Never put credentials (Wi-Fi passwords, API keys) into the skill or examples; use placeholders.

## The description

The `description` decides whether the skill loads at all, and a skill that never loads measures as zero in Phase 3
(`trigger-weak`). Name the board, chip and framework, list what users actually say ("make it show up in nRF
Connect", "Guru Meditation", "the display stays black", part numbers), and say to use the skill even when the user
does not name the board but the project clearly targets it. Keep it specific enough not to fire on a different
board of the same family.

If the author has Claude's skill-creator available, its description-optimisation loop works for hardware skills;
build its should-not-trigger set from near-miss boards and frameworks (same vendor, other chip; same chip, other
SDK).

## Structure

```
<skill-name>/
├── SKILL.md                 # identity, versions, workflow, traps, safety; under ~300 lines
├── references/
│   ├── pinout.md            # per board revision
│   ├── <subsystem>.md       # i2c-and-power.md, ble.md, display.md ...
│   └── logs.md              # healthy boot log, common failure logs and their causes
├── scripts/                 # optional: port detection, log parsing
└── evals/                   # see eval-format.md; never shipped to the agent under test
```
