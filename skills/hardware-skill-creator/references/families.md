# Chip family bench notes

Read the section for the target board's family when you fill in `boot_banner`, `reboot_patterns`, the reset
procedure and the chip-ID step. Tool syntax changes between releases: confirm each command with the installed
tool's `--help` before writing it into a task or telling a tester to run it, and prefer what the user's own
toolchain prints over this file.

Contents: ESP32 series · nRF52 · STM32 · RP2040 / RP2350 · battery-powered boards · anything else

## ESP32 series (ESP32, -S2, -S3, -C3, -C6, -H2)

| Need | How |
|---|---|
| Chip ID | `esptool read-mac` (esptool v4: `esptool.py read_mac`); esptool also prints `MAC:` while flashing. In firmware, `esp_efuse_mac_get_default()` returns the same factory base MAC; print that, not an interface MAC from `esp_read_mac()`, which can differ |
| Full erase | `idf.py -p PORT erase-flash` or `esptool --port PORT erase-flash` |
| eFuse snapshot | `espefuse summary` at both self-tests |
| `boot_banner` | `^rst:0x` — the ROM prints one `rst:0x..` line per boot |
| `reboot_patterns` | `Guru Meditation\|abort\(\) was called\|assert failed:\|Backtrace:` and `Brownout detector`; add `Task watchdog got triggered` unless a task expects a watchdog |

- Panic output differs by core. Xtensa chips (ESP32, S2, S3) print `Backtrace:`; RISC-V chips (C3, C6, H2) print a
  register dump with `MEPC` instead. Both print `Guru Meditation Error`, which is the pattern to rely on.
- Dev boards with a USB-UART bridge (ESP32-C3-DevKitM-1 and the DevKitC boards, for example; check the board's user
  guide) wire RTS to EN and DTR to the boot strapping pin: GPIO0 on ESP32, S2 and S3, GPIO9 on C3. Opening a port
  with default DTR/RTS can reset the chip or hold it in download mode; hold both inactive, then reset deliberately
  (`bench.py capture --reset rts`). Confirm the wiring on the board's schematic before relying on it.
- Boards using the chip's own USB-Serial/JTAG re-enumerate on reset; the first lines can be lost. Have reference
  firmware print its banner and chip ID repeatedly for a few seconds.
- Strapping pins are a classic model mistake and good task material. They differ per chip, so never carry a list
  across: ESP32 uses GPIO0, 2, 5, 12 and 15; ESP32-S3 uses GPIO0, 3, 45 and 46; ESP32-C3 uses GPIO2, 8 and 9. Check
  the exact chip's datasheet before relying on this list.
- ESP-IDF projects build for `esp32` unless told otherwise. Put `CONFIG_IDF_TARGET="esp32c3"` (or the right chip) in
  each fixture's `sdkconfig.defaults` so `idf.py build` produces firmware for the board with no extra step.
- Before any check that builds, confirm the environment is loaded: `idf.py --version` must print a version. The
  export script picks a Python interpreter from `PATH` and can fail quietly when it finds one without the ESP-IDF
  virtual environment.
- Never burn eFuses, enable Secure Boot or Flash Encryption as part of a task: they are irreversible and make the
  board unusable for attestation. A skill should tell the agent the same.

## nRF52 (nRF52832, nRF52833, nRF52840; Zephyr / nRF Connect SDK)

| Need | How |
|---|---|
| Chip ID | FICR DEVICEID: `nrfjprog --memrd 0x10000060 --n 8` (nrfjprog is being replaced by nRF Util; use its equivalent read if nrfjprog is absent) |
| Full erase | `nrfjprog --eraseall`, or nRF Util's device erase |
| `boot_banner` | `\*\*\* Booting (Zephyr OS\|nRF Connect SDK)` |
| `reboot_patterns` | `ZEPHYR FATAL ERROR\|Halting system` |

- Development kits expose the UART through the on-board debugger's virtual COM port, which stays enumerated when
  the target resets — good for capturing from time zero.
- Newer silicon revisions ship with access-port protection enabled; recovering it erases the chip. Record whether
  the board needed recovery, and never enable protection in a task.
- The banner only prints if `CONFIG_BOOT_BANNER` is on (the default); the reference fixture must keep it.

## STM32

| Need | How |
|---|---|
| Chip ID | 96-bit unique ID register via the debug probe, e.g. OpenOCD `mdw <addr> 3` |
| UID address | F0/F3 `0x1FFFF7AC`, F1 `0x1FFFF7E8`, F2/F4 `0x1FFF7A10`, L4 `0x1FFF7590`, H7 `0x1FF1E800` — confirm in the series reference manual |
| Full erase | `STM32_Programmer_CLI -c port=SWD -e all`, or OpenOCD's mass-erase for the series |
| `boot_banner` | None by default: make the reference and the prompt print a fixed line first thing in `main` |
| `reboot_patterns` | Whatever your fault handler prints, e.g. `HardFault` |

- Without a banner line in firmware the reboot guard cannot see a reset. If the task prompt cannot reasonably ask
  for one, add a `gpio_state` or bus assertion whose timing breaks on a reset instead.
- Never change readout protection to level 2 or write option bytes in a task; level 2 is permanent.
- Renode's STM32F4 platform script gives a UID that changes between runs; a changing UID in an attestation is a red
  flag.

## RP2040 / RP2350 (Pico SDK, Arduino-Pico, MicroPython)

| Need | How |
|---|---|
| Chip ID | `picotool info` on the connected board; RP2040 has no chip ID and uses the flash chip's unique ID as board ID, so also print `pico_get_unique_board_id_string()` from the reference |
| Full erase | Copy `flash_nuke.uf2` in BOOTSEL mode, or `picotool erase` where available |
| `boot_banner` | None by default: print a fixed line at start-up in the reference and ask for it in the prompt only if the task naturally has one |
| `reboot_patterns` | Your panic handler's text |

- USB CDC stdio re-enumerates on every reset; UART stdio through a debug probe does not. Prefer UART for evals.
- RP2350 has OTP memory. Never write OTP in a task.

## Battery-powered boards

Unplugging USB does not remove power. Use the board's power-off and confirm the display or LED is dark:

- M5Stack Core2: hold the power button for 6 s (internal battery, AXP192 PMIC).
- Other M5Stack and similar boards: check the vendor docs for the power-off gesture or hold pin, and write it into
  the manifest comments so every tester does the same.

## Anything else

Before writing the package, find out and write down, from the vendor's docs:

1. A command that reads a per-chip unique ID, and whether simulators of this part fake it.
2. A command that erases all non-volatile memory the firmware can use, including external flash and filesystems.
3. What the platform prints once per boot, and on a fatal error.
4. Which operations are irreversible (fuses, OTP, protection levels) — the skill must steer agents away from them.
5. Whether the serial port survives a target reset.
