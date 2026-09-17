# Eval package format

Read this while filling in `evals/manifest.yaml` and `evals/tasks/*.yaml`. The authoritative version is the
Reference section of EVALS.md in awesome-hardware-skills; `scripts/l0_check.py` is a copy of that repo's L0 checker.

Contents: layout · manifest.yaml · task files · assertion types and how each is measured · designing tasks ·
assertions that can fail

## Layout

```
my-skill/
├── SKILL.md
├── references/ scripts/ ...       # the skill itself
└── evals/                         # removed from the skill before every agent run
    ├── manifest.yaml
    ├── tasks/
    │   ├── 01-<easy>.yaml
    │   ├── 02-<medium>.yaml
    │   └── 03-<hard>.yaml
    └── fixtures/<task-id>/
        ├── reference/             # Phase 0 check 1 and the Phase 1 self-test
        ├── broken/                # Phase 0 check 3
        └── spoof/                 # Phase 0 check 4
```

Three tasks: one says nothing about generalising, many make Phase 3 expensive.

## manifest.yaml

| Field | Required | Meaning |
|---|---|---|
| `skill` | yes | Equal to `name` in SKILL.md. |
| `version` | no | Eval package version. Bump on any task or assertion change; redo Phase 0. |
| `target.board` | yes | Exact board id or arduino-cli FQBN, never a family name. |
| `target.framework` | yes | `esp-idf`, `arduino`, `zephyr`, `ros2`, ... |
| `target.framework_version` | yes | The version the tasks were validated against. |
| `target.toolchain` | no | What the agent is expected to invoke: `idf.py`, `arduino-cli`, `west`. |
| `simulator` | yes | L1 pre-check target: `wokwi`, `renode`, `qemu`, `native_sim`, `gazebo`, `isaac`, `mujoco`, `webots`, `ha-demo`, `modbus-sim`, `opcua-sim`, `none`. No bearing on passing. |
| `assertions_supported` | yes | Every assertion type any task uses. |
| `boot_banner` | yes for the guard | Regex matching a line printed exactly once per boot. A second match after time zero is a reboot. |
| `reboot_patterns` | yes for the guard | Regexes for fatal output (panic, fault, brown-out). Any match after time zero fails the run. |
| `eval_validated` | for L2 | Phase 0 record. |
| `sequential_plan` | no | Pre-registered error rate and max runs per arm, if Phase 3 stops early. |
| `verified.L0/L1/L2` | no | Filled by CI, the future L1 runner, and maintainers from accepted attestations. |
| `ab.*` | no | Phase 3 results. |

## Task files

The filename stem equals `id`.

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Numbered so tasks sort by difficulty. |
| `level` | yes | `easy`, `medium`, `hard`. |
| `timeout_s` | yes | Wall-clock budget for the agent. |
| `prompt` | yes | Everything the agent is told, including every value an assertion matches. |
| `build.cmd`, `build.cwd` | yes in practice | Build run on the frozen copy; `cwd` is relative to the agent's working directory, which is the root of the frozen copy. |
| `flash.cmd` | no | Flash command; `{port}` is replaced by the tester. |
| `human_action` | no | A physical action and its time, e.g. `press the button on GPIO39 once, 5 s after time zero`. |
| `expect_reset` | no | `true` if the task legitimately resets the board; disables the reboot guard. |
| `assertions` | yes | All must pass. |
| `fixtures` | no | Paths to reference outputs, e.g. an expected serial log. |

## Assertion types

Any assertion may set `l1_skippable: true` when a simulator cannot evaluate it. On a board, every assertion runs.

### compile_only

No fields. Passes if `build.cmd` exits 0 on the frozen copy. Proves almost nothing on its own; every package needs
something stronger.

### serial_match

Fields: `baud`, `pattern` (Python regex, searched per line), `min_matches`, `within_s`, and optionally
`max_matches` and `after_human_action: true`.

- Open the port before releasing reset, with DTR and RTS held so opening does not reset the board or hold it in
  the bootloader (`bench.py capture` does this). On ESP32 dev boards RTS drives EN and DTR drives GPIO0.
- Native-USB boards re-enumerate on reset; capture resumes when the port returns and output in the gap is lost, so
  such tasks should print repeatedly.
- Pass if at least `min_matches` and, when set, at most `max_matches` lines match within `within_s` of time zero.
- `after_human_action: true` makes it a control-window assertion: any match before the human action fails it.
  Use it on the output the action is meant to trigger, so firmware that prints without the stimulus is caught.
- Within 10 s after the window closes, read the chip ID on the same port without unplugging.
- `bench.py serial LOG TASK --manifest MANIFEST [--action-at 5,8,11]` evaluates these and the reboot guard; the
  control window ends at the first action.

### gpio_state

Fields: `pin`, `expect` (e.g. `toggles`), `min_edges`, `within_s`, optionally `max_edges`.
Logic analyser on the pin with common ground, sampling at ≥10× the fastest edge rate (1 MHz is ample below a few
kHz), from time zero for at least `within_s`. Save the raw capture (e.g. sigrok `.sr`). For `toggles`, pass if the
edge count in the window is at least `min_edges` and, when set, at most `max_edges`. Set both bounds whenever the
prompt fixes a rate, so a pin toggled ten times too fast fails.

### bus_capture

Fields: `bus` (`ble`, `can`, `i2c`, `spi`), `expect` (bus-specific).
- BLE `expect`: `adv_name`, `service_uuid`, `char_uuid`, `notify_count_min`, `within_s`. Sniffer (e.g. nRF52840
  dongle with nRF Sniffer) started before time zero; a central must connect and the sniffer must follow the
  connection to see notifications. Save `.pcapng`, evaluate with packet filters.
- CAN/I2C/SPI: adapter or logic analyser with protocol decoder; evaluate decoded frames against `expect`.
- Usually `l1_skippable`, which is why Phase 2 exists.

### exit_code

Fields: `cmd`, `expect` (default 0). Runs on the frozen copy. Use it only for properties no observation catches,
such as a forbidden call that does not visibly break the board. Must be shown to fail on an empty project.

### Reserved

`network_probe`, `ros_topic`, `file_exists` pass L0 but have no field schema yet; define one in a pull request to
EVALS.md before using it.

## Designing tasks

Start from mistakes, not features. For each task, name the specific error a model makes on this board without the
skill: wrong strapping pin, redundant `Wire.begin()`, missing `sdkconfig` symbol, blocking call in an ISR, wrong
FQBN, a notify payload truncated before MTU exchange. The task is a realistic request where that mistake happens,
the `broken` fixture contains exactly it, and at least one assertion fails because of it.

- **easy**: the board's basic loop works — right port, right FQBN or target, flash, visible output.
- **medium**: one peripheral or bus with a board-specific trap.
- **hard**: timing, interrupts, a radio, or two subsystems at once, where a plausible solution fails at runtime.

**Make the prompt unambiguous, not just complete.** "Toggle at 2 Hz" can mean two toggles or two full cycles per
second; write "toggle GPIO5 every 500 ms" instead. "Print tick" can mean a bare line or a log line with a prefix;
say which, and make the pattern agree. The rule that the prompt states every matched value is about meaning, and
`check_package.py` can only check the literal part.

Prefer a runtime observation to `exit_code`. Size `within_s` from the reference's measured timing with margin
(2× is a reasonable start), and put any `human_action` after the output that must precede it. Keep `timeout_s`
generous (600-900 s); a timeout is a fail, not a signal about the eval.

## Assertions that can fail

An assertion is vacuous when it passes because the thing it inspects is missing. Fix: absence is a failure.

```python
# vacuous: passes when no IRAM_ATTR handler exists
m = re.search(r'void\s+IRAM_ATTR\s+\w+\s*\([^)]*\)\s*\{(.*?)\n\}', src, re.S)
sys.exit(1 if m and re.search(r'Serial\.|delay\(', m.group(1)) else 0)

# sound
if not m:
    sys.exit(1)
sys.exit(1 if re.search(r'Serial\.|delay\(', m.group(1)) else 0)
```

```sh
# vacuous: passes in an empty directory
! grep -q "Wire.begin(" *.ino
# sound
ls *.ino >/dev/null 2>&1 && ! grep -q "Wire.begin(" *.ino
```

A check can also be too narrow: the sound version above still passes a blocking handler written *without*
`IRAM_ATTR`. Only the broken fixture (Phase 0 check 3) exposes that, which is why it must contain the realistic
mistake, not a caricature of it.

## When the schema cannot catch a spoof

The assertion types are deliberately few, and some spoofs get past them: firmware that prints and toggles from two
unrelated timers, or that waits a fixed delay after time zero and then prints what the button should have
triggered. When a spoof you wrote is not caught:

1. **Change the task so the observable depends on the behaviour.** Several presses at stated times with the output
   counting them (`^count=3$` only after the third), a pin whose edges are timed against a serial line, a sensor
   value that changes when the tester acts. This is almost always possible and is the best fix.
2. **Add bounds.** `max_matches` and `max_edges` catch output that is too fast or too plentiful.
3. **Add an `exit_code` check on the source** for the structural part (a handler exists and does not print), made
   sound as described above. It supplements a runtime observation; it never replaces one.
4. **If nothing works, record it.** Keep the spoof in `fixtures/`, set `spoof_caught: false` with a note in the
   evidence, and do not ask for attestations until it is caught. If a new assertion type would catch it, propose
   one in a pull request to EVALS.md.

## Building fixtures without polluting the package

Building inside `fixtures/<id>/reference/` writes `build/`, `sdkconfig` and similar files into the package. Build
out of tree instead, for ESP-IDF with `idf.py -C <fixture> -B <scratch>/build -D SDKCONFIG=<scratch>/sdkconfig build`,
or add those paths to the package's `.gitignore`. A full ESP-IDF configure and build takes minutes per fixture;
tell the user before starting nine of them.

