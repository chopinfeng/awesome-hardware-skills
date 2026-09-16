# Awesome Hardware Skills [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

*English · [简体中文](README.zh-CN.md)*

> Skills, MCP servers, on-device agent runtimes, simulators, benchmarks and CI infrastructure that let AI coding agents (Claude Code, Codex, Cursor, OpenClaw, …) build, flash, debug and control physical hardware — with a verification ladder so you can tell which ones actually work on a board.

Most "awesome MCP" lists tell you a hardware server *exists*. This list also tracks whether anyone has proven it works: every skill entry can carry a badge from a three-level ladder (static checks → simulator run → real-hardware attestation) plus a with-skill / without-skill delta. The ladder is explained in the first section below.

A companion file, [GAPS.md](GAPS.md), tracks what does **not** exist yet — each gap with the evidence
behind it, the closest artifact that does exist so the claim can be falsified, and scoped first
contributions with the eval assertions to aim at.

Snapshot: 2026-09-16. Stars, last-push dates and skills.sh / ClawHub install counts are from that day. `stale` marks projects with no push in 12+ months. `official` marks repos under the hardware or SDK vendor's own GitHub org.

## Contents

- [How entries are verified](#how-entries-are-verified)
- [Skills](#skills)
  - [MCU / Embedded](#mcu--embedded)
  - [RTOS](#rtos)
  - [MicroPython / CircuitPython](#micropython--circuitpython)
  - [Embedded Rust](#embedded-rust)
  - [Vendor SDKs](#vendor-sdks)
  - [SBC / Linux](#sbc--linux)
  - [Robotics](#robotics)
  - [Drones](#drones)
  - [Space and aerospace](#space-and-aerospace)
  - [Edge AI / NPU](#edge-ai--npu)
  - [EDA / PCB](#eda--pcb)
  - [FPGA / HDL](#fpga--hdl)
  - [Wireless](#wireless)
  - [Hardware security](#hardware-security)
  - [Automotive](#automotive)
  - [Industrial / PLC](#industrial--plc)
  - [Pro AV and building systems](#pro-av-and-building-systems)
  - [Lab instruments](#lab-instruments)
  - [Digital fabrication](#digital-fabrication)
  - [Smart Home](#smart-home)
- [MCP servers and bridges](#mcp-servers-and-bridges)
- [Agent protocols and on-device runtimes](#agent-protocols-and-on-device-runtimes)
- [Verification infrastructure](#verification-infrastructure)
- [Benchmarks and evals](#benchmarks-and-evals)
- [Papers and articles](#papers-and-articles)
- [Agent-ready docs](#agent-ready-docs)
- [Gaps](#gaps)
- [Related lists](#related-lists)

## How entries are verified

Hardware skills are hard to validate in CI because the CI runner does not own the board. So this list uses a ladder instead of a single green check.

**`L0`** — Static checks pass: SKILL.md frontmatter, description specific enough to trigger, no secrets, links resolve, `evals/` package well-formed. Enforced today by `scripts/l0_check.py` in CI.

**`L1 (wokwi)`** — Every task in the skill's `evals/` passes in the named simulator (Wokwi, Renode, `native_sim`, …), run by this repo's CI. Coming soon.

**`L2 ×3`** — Three independent people ran the tasks on real hardware and filed an attestation issue with an unedited transcript.

**`ΔPass +42%`** — With-skill minus without-skill task pass rate on the same model, proving the skill carries knowledge the model did not already have. Coming soon.

**`stale`** — No L1 re-run in 90 days, or no upstream push in 12 months.

Tasks assert on physical side effects a script can observe (serial output, GPIO edges, bus captures, ROS topics, HTTP probes), never on "the code looks right". The eval package format lives in `template/evals/`; see the Contributing section at the end for how to add one.

This is the launch snapshot: no entry has an `evals/` package yet, so no badges are shown. The first targets for L1 are the ESP32, Zephyr and Arduino skills below, because Wokwi, Renode and `native_sim` can run them without a board.

## Skills

Entries in the [Agent Skills](https://agentskills.io) format: a folder with a `SKILL.md` (frontmatter `name` + `description`) and optional `references/` and `scripts/`. Installable into Claude Code, Codex, Cursor and others. `coll` = a collection of several skills; a path after the repo name points at one skill inside a monorepo. Within a category, entries are ordered by usefulness, not stars — a 15k-star monorepo that happens to contain one small skill does not outrank a focused 50-star one.

Vendor-official skills are tagged `official` in place. As of the snapshot they come from NVIDIA, Espressif (on-device only), Adafruit, Seeed, M5Stack, Arm, Renesas, Texas Instruments, Bouffalo, Ai-Thinker, SiFli, Luat, LilyGO, RT-Thread, Xiaomi Vela, Tuya, EasyEDA, Hailo, Horizon, D-Robotics, Luxonis, Intel, Google, Meta, Pollen, AgiBot, Wandelbots, Viam, PX4, the Matter SDK, Home Assistant, SmartThings, Z-Wave JS, Meshtastic, SimpleBLE, Reolink, Elgato, CSS Electronics, EcuBus, Nominal, Joulescope, DAQiFi, Qualcomm, Ångström, openEuler, Anthropic and Nebius — and from no MCU silicon vendor except Renesas and Arm.

### MCU / Embedded

- [Jeffallan/claude-skills `embedded-systems`](https://github.com/Jeffallan/claude-skills/tree/main/skills/embedded-systems) - STM32 / ESP32 / FreeRTOS / bare-metal workflow: peripherals, ISRs, DMA, power; the most-installed generic embedded skill (~6k installs on skills.sh). (★11.5k · 2026-08)
- [hathach/tinyusb `.claude/skills/`](https://github.com/hathach/tinyusb/tree/master/.claude/skills) - `hil` drives the TinyUSB hardware-in-the-loop rig; `target-debug`, `rtt`, `etm-trace`, `usb-sniffer`, `usbmon` interpret on-target USB stack behaviour. The best example of an agent skill wired to a real HIL bench. (coll · ★7.1k · 2026-09)
- [FastLED/FastLED `.claude/skills/`](https://github.com/FastLED/FastLED/tree/master/.claude/skills) - Project-internal but real: ESP-IDF v5 RMT5 driver expert, ESP32 log triage and test-plan skills, Xtensa and RISC-V assembly code review, timing analysis. (coll · ★7.5k · 2026-09)
- [LeoKemp223/embed-ai-tool](https://github.com/LeoKemp223/embed-ai-tool) - About 25 skills with bundled scripts covering the whole MCU toolchain: build with Keil / IAR / CMake / ESP-IDF / PlatformIO, flash with OpenOCD / J-Link / idf.py, debug with GDB, plus CAN, Modbus, VISA and RTOS debugging. Chinese descriptions. (coll · ★919 · 2026-08)
- [zhinkgit/embeddedskills](https://github.com/zhinkgit/embeddedskills) - Probe detection, flashing, GDB server, telnet debug, semihosting and ITM capture across OpenOCD, J-Link, probe-rs, Keil and EIDE. Chinese. (coll · ★664 · 2026-09)
- [DunCanYounG-1/auto-embedded](https://github.com/DunCanYounG-1/auto-embedded) - STM32 / ESP32 / GD32 / MSPM0 development framework with 24 tool skills, injected into seven agent platforms. Chinese. (coll · ★243 · 2026-09)
- [Mindrally/skills `embedded-stm32`](https://github.com/Mindrally/skills/tree/main/embedded-stm32) - STM32 HAL skill derived from Cursor rules: CubeMX, DMA, SWD conventions. (★259 · 2026-09)
- [mohitmishra786/low-level-dev-skills](https://github.com/mohitmishra786/low-level-dev-skills) - Bare-metal fundamentals with datasheet-reading guidance: STM32 bare-metal, GPIO, UART, I2C/SPI bus drivers, DMA, bootloaders, OpenOCD/JTAG, embedded Rust, QEMU simulation, FreeRTOS, Zephyr. (coll · ★210 · 2026-06)
- [SensorsIot/Embedded-AI-Harness `esp-idf-handling`](https://github.com/SensorsIot/Embedded-AI-Harness/tree/main/.claude/skills/esp-idf-handling) - Closed-loop ESP-IDF: build, flash over local USB or an RFC2217 remote testbench, monitor, OTA, crash recovery. One of the few skills that closes the flash → observe → iterate loop. (★175 · 2026-08)
- [Gundry-Consultancy/sbc-mcu-dut-controller `.agent/skills/`](https://github.com/Gundry-Consultancy/sbc-mcu-dut-controller/tree/main/.agent/skills) - A real HIL bench as skills: `hil-job-api`, `hil-author-test`, `hil-firmware-compare`, `hil-bisect`, `hil-camera-proof` over ESP32 / RP2040 / SAMD flashing, power relays and an I2C mux. (coll · ★0 · 2026-07)
- [magnus919/agent-skills `esp32-development`](https://github.com/magnus919/agent-skills/tree/main/esp32-development) - Identify the ESP32 board, choose between ESP-IDF, Arduino, MicroPython, CircuitPython, ESPHome, Zephyr, Rust and NuttX, wire, flash, recover. (★82 · 2026-09)
- [CY-CHENYUE/esp-idf-cy](https://github.com/CY-CHENYUE/esp-idf-cy) - Install ESP-IDF from Chinese mirrors, then build → flash → monitor with device naming. (★40 · 2026-07)
- [kukucaiCndy/embedded_ai_skills](https://github.com/kukucaiCndy/embedded_ai_skills) - Setup / project-init / debug triplets for ESP32 (IDF and Arduino), STM32 and Nordic NCS, plus ZMK keyboard and EasyEDA drawing skills. (coll · ★54 · 2026-07)
- [ezrover/ESP32-AI-Agent-Skill](https://github.com/ezrover/ESP32-AI-Agent-Skill/tree/main/skills/esp32) - Chip selection (S3 / C3 / C6), PSRAM and MMU notes, the GPIO12 strapping-pin trap, ESP-IDF and PlatformIO setup, LVGL and Waveshare display references. (★37 · 2026-08)
- [easyzoom/aix-skills](https://github.com/easyzoom/aix-skills) - Integration-focused MCU skills: ESP-IDF, STM32 HAL/LL, FreeRTOS kernel debug, FreeRTOS+TCP, OpenOCD / J-Link / ST-Link. (coll · ★32 · 2026-07)
- [JasonYANG170/esp-dev-skill](https://github.com/JasonYANG170/esp-dev-skill) - One sub-skill per Espressif repo: esp-idf, arduino-esp32, esp-adf, esp-dl, esp-zigbee-sdk, esp-at, esp-brookesia, esp-claw, connectedhomeip. (coll · ★27 · 2026-08)
- [ylongw/embedded-review](https://github.com/ylongw/embedded-review) - Dual-model firmware review for ISR, RTOS and memory mistakes; ~1.8k ClawHub installs. (★48 · 2026-03)
- [EricSun787/stm32-development-workflow](https://github.com/EricSun787/stm32-development-workflow) - STM32CubeCLT command-line flow: toolchain, HAL, build, ST-Link flash, common error fixes. Chinese. (★24 · 2026-02)
- [wedsamuel1230/arduino-skills](https://github.com/wedsamuel1230/arduino-skills) - 30 Arduino and maker skills: code generator, arduino-cli, serial monitor, pin assignment, I2C bring-up diagnostician, wiring safety check, power budget, BOM, OTA guardian. (coll · ★21 · 2026-08)
- [claudius-ars/embedded-agent-skills `gpio-config`](https://github.com/claudius-ars/embedded-agent-skills/tree/main/embedded-agent-skills/gpio-config) - GPIO / I2C / SPI / UART / PWM pin assignment with conflict checks for Raspberry Pi (device-tree overlays, config.txt) and ESP32 (sdkconfig). (★19 · 2026-02)
- [alexex1993/mcu-skills](https://github.com/alexex1993/mcu-skills) - One skill per board (19): RP2040 Pico, RP2350, ESP32-WROOM 30/36/38-pin, ESP32-S3-CAM, ESP32-C6, ESP32-P4, nRF52840 ProMicro, STM32F411 BlackPill, STM32H750, ATmega328P Nano, ESP8266 — pinout, peripherals, power. (coll · ★17 · 2026-09)
- [Loclove/Electronics-Design-Competition-Skill-2](https://github.com/Loclove/Electronics-Design-Competition-Skill-2) - The 电赛 (China undergraduate electronics design contest) MCU skill with agents and references. (★14 · 2026-07)
- [o2scale/electronics-agent-kit](https://github.com/o2scale/electronics-agent-kit/tree/main/.agent/skills) - PlatformIO project / config / debug for Arduino, ESP-IDF and STM32, plus kicad-cli and KiCad file-format skills. (coll · ★12 · 2026-02)
- [grumat/glossy-msp430 `.claude/skills/`](https://github.com/grumat/glossy-msp430/tree/master/.claude/skills) - Decode MSP430 JTAG logic-analyzer captures and run unit tests; the only TI MSP430 skill found. (coll · ★15 · 2026-07)
- [varo6/reTerminal-sticky-skill](https://github.com/varo6/reTerminal-sticky-skill/tree/main/skills/sticky-device) - Seeed reTerminal Sticky (ESP32-S3 e-ink): pin map, ESP-IDF patterns, ePaper refresh rules. (★7 · 2026-08)
- [BlueAndi/Pixelix `.github/skills/`](https://github.com/BlueAndi/Pixelix/tree/master/.github/skills) - MISRA-oriented embedded C++14 rules for ESP32 firmware, in GitHub Copilot skill form. (copilot · ★442 · 2026-09)
- [fxp/m5stack-embedded-dev-skill](https://github.com/fxp/m5stack-embedded-dev-skill) - Arduino + M5Unified first M5Stack/ESP32 skill: board-to-FQBN catalog, GPIO safety split by chip generation, I2C/PMIC gotchas, FreeRTOS/ISR rules, crash triage; ships a `serial_match`/`exit_code` evals package, L0-verified locally. New and unstarred — listed here for the evals package shape, not track record. (★0 · 2026-09)
- [PatrickJS/awesome-cursorrules `embedded-stm32-hal`](https://github.com/PatrickJS/awesome-cursorrules/blob/main/rules/embedded-stm32-hal.mdc) - Cursor rule, not a skill: embedded C/C++ on STM32 HAL, ISR, DMA and memory-constraint conventions. (cursor-rules · ★40.8k · 2026-05)

### RTOS

- [beriberikix/zephyr-agent-skills](https://github.com/beriberikix/zephyr-agent-skills) - The most complete Zephyr catalog (21 skills): foundations, board bring-up (HWMv2), devicetree, build system, kernel, BLE / IP / USB / CAN connectivity, IoT protocols, multicore, `native_sim`, power, security updates, storage, testing; a keyword / Kconfig / compatible-scored router picks the right one. (coll · ★64 · 2026-05)
- [ksachdeva/zephyr-rtos-ai](https://github.com/ksachdeva/zephyr-rtos-ai/tree/main/skills) - 25 per-subsystem Zephyr API skills: BLE (GAP roles, GATT, pairing, NUS), devicetree, Kconfig, GPIO, I2C, SPI, UART, ISR, threads, sync, power management, settings, storage, sockets, Wi-Fi, SMF, shell, testing, memory. (coll · ★23 · 2026-06)
- [a5c-ai/babysitter `embedded-systems`](https://github.com/a5c-ai/babysitter/tree/main/library/specializations/embedded-systems/skills) - 29 short skills: Zephyr, FreeRTOS, Nordic nRF, STM32 HAL, Cortex-M, JTAG/SWD, linker scripts, CAN, USB stack, OTA, motor control, MISRA, Unity/Ceedling. Breadth over depth. (coll · ★1.8k · 2026-09)
- [RT-Thread/rtthread-skills](https://github.com/RT-Thread/rtthread-skills) - RT-Thread's own skills: create a BSP, create a package, env setup, code review, simplification, Git workflow. (official · coll · ★3 · 2026-07)
- [open-vela/.claude](https://github.com/open-vela/.claude) - Xiaomi Vela (NuttX) device development: driver development, build, Kconfig tweaks, memdump, code size, driver review, PCM audio (15 skills). (official · coll · ★5 · 2026-09)
- [chshzh/charlie-skills](https://github.com/chshzh/charlie-skills) - 27 Nordic nRF Connect SDK skills covering the PRD → spec → code → test lifecycle, NCS 3.x migration, nRF70 Wi-Fi throughput and firmware stats, Memfault. (coll · ★0 · 2026-08)
- [gevico/rt-claw `.agents/skills/`](https://github.com/gevico/rt-claw) - Port and diagnose an RT-Thread-based on-device agent runtime: platform port, OSAL review, diagnose. (coll · ★11 · 2026-06)
- [eduardojvieira/ZPLC `stm32-freertos-developer`](https://github.com/eduardojvieira/ZPLC) - STM32 + FreeRTOS development skill inside a soft-PLC project; the only FreeRTOS-specific skill with any depth. (★6 · 2026-09)
- [goliothlabs/golioth-firmware-skill](https://github.com/goliothlabs/golioth-firmware-skill/tree/main/skills/golioth-firmware) - Golioth SDK on Zephyr, ESP-IDF, NCS and ModusToolbox: greenfield and brownfield integration, OTA, the six cloud services. (★1 · 2026-03)
- [toppers/asp3_pico_sdk `.claude/skills/`](https://github.com/toppers/asp3_pico_sdk) - TOPPERS/ASP3 RTOS on RP2350 (Cortex-M33 and Hazard3 RISC-V) with OpenOCD and GDB; siblings cover NXP MCUXpresso and Renesas FSP ports. Japanese. (official · ★0 · 2026-09)

### MicroPython / CircuitPython

- [FreakStudioCN/MicroPython_Skills](https://github.com/FreakStudioCN/MicroPython_Skills) - The largest MicroPython collection (60+): mpremote operations, firmware flashing, deploy, driver generation from a spec, hardware selection, wiring, simulation. Chinese. (coll · ★5 · 2026-09)
- [andrewleech/claude-mpy-marketplace](https://github.com/andrewleech/claude-mpy-marketplace) - Skills for mpremote device interaction, file transfer and live sessions, plus MicroPython contributor skills, by a MicroPython core maintainer. (coll · ★2 · 2026-09)
- [m5stack/uiflow-micropython `tools/knowledge-base/`](https://github.com/m5stack/uiflow-micropython/tree/master/tools/knowledge-base) - `uiflow2-coder` and `uiflow2-ui-designer` for UIFlow2 MicroPython with bundled official docs. (official · coll · ★208 · 2026-09)
- [adafruit/LLM-Recipes](https://github.com/adafruit/LLM-Recipes/tree/main/circuitpython) - Run code on an attached CircuitPython board, write and run hardware tests, and validate an I2C driver by comparing Arduino vs CircuitPython bus traffic. (official · coll · ★3 · 2026-06)
- [adafruit/Adafruit_Learning_System_Guides `embodiment-kit`](https://github.com/adafruit/Adafruit_Learning_System_Guides/tree/main/Embodiment_Kit/agent_skill/embodiment-kit) - Drive a CircuitPython "embodiment kit" (display, NeoPixel, sensors) through Adafruit IO with before/after sensor proof. (official · ★1.1k · 2026-09)
- [rockets-cn/unihiker-k10-skills](https://github.com/rockets-cn/unihiker-k10-skills) - DFRobot UNIHIKER K10 flashing and APIs for MicroPython, Arduino and PlatformIO, plus OTA and a compile server; ~2k ClawHub installs each. (coll · ★6 · 2026-08)
- [MakerClassCZ/picogame `skills/`](https://github.com/MakerClassCZ/picogame/tree/main/skills) - CircuitPython Pico board bring-up: settings.toml, GPIO, display. (★25 · 2026-09)
- [Cerwor/jlc-k230-lushan-pi](https://github.com/Cerwor/jlc-k230-lushan-pi) - JLC 嘉立创庐山派 K230 CanMV MicroPython: camera, LCD, YOLO, mpremote deploy. (★4 · 2026-09)

### Embedded Rust

- [actionbook/rust-skills `domain-embedded`](https://github.com/actionbook/rust-skills/tree/main/skills/domain-embedded) - `no_std`, Embassy and RTIC constraints with an injected `.cargo/config.toml`; ~2.4k installs, the most-installed embedded-Rust skill. Sibling `domain-iot`. (★1.5k · 2026-08)
- [OutlineDriven/odin-claude-plugin `odin-native`](https://github.com/OutlineDriven/odin-claude-plugin/tree/main/plugins/odin-native/skills) - Firmware with cortex-m-rt / probe-rs / defmt / RTIC, OpenOCD JTAG, FreeRTOS and QEMU-for-kernel skills. (coll · ★36 · 2026-09)
- [ch32-rs/ch32-rs `.claude/skills/`](https://github.com/ch32-rs/ch32-rs) - Turn a vendor SVD into a PAC crate for WCH RISC-V parts. (★170 · 2026-05)
- [hispark-rs/hisi-riscv-rs `.agents/skills/`](https://github.com/hispark-rs/hisi-riscv-rs) - `hil-smoke` and `hil-regression`: flash a real HiSilicon ws63 board, read UART, assert a marker. (coll · ★3 · 2026-09)
- [bitscrafts/EFR32MG2X-RS](https://github.com/bitscrafts/EFR32MG2X-RS) - Silicon Labs EFR32MG24 Rust HAL expert skill. (★6 · 2026-06)
- [Microbiosis/esp-rust-skills](https://github.com/Microbiosis/esp-rust-skills) - The esp-hal peripherals, Wi-Fi / BLE / ESP-NOW, toolchain. Chinese. (coll · ★1 · 2026-06)

### Vendor SDKs

- [Open-CMSIS-Pack/CMSIS-Developer-Assistant](https://github.com/Open-CMSIS-Pack/CMSIS-Developer-Assistant) - Arm's CMSIS skills plus an MCP: bring-up, live debug, pack and project creation, board layers for Cortex-M. (official · coll · ★2 · 2026-09)
- [TexasInstruments/C2000-IDEA `docs/skills/c2000-idea`](https://github.com/TexasInstruments/C2000-IDEA/tree/main/docs/skills/c2000-idea) - F28x device migration phased across four reference documents, bitfield-to-driverlib conversion and SysConfig ePWM migration; drives a local `idea-mcp` endpoint alongside CCS Project, SysConfig and TI assembly MCP servers. The third silicon vendor to ship a host-side skill. (official · ★20 · 2026-09)
- [renesas/renesas-skills](https://github.com/renesas/renesas-skills) - `configure-renesas-debug` writes VS Code launch.json for J-Link / E2 / E2Lite / IECUBE; the only silicon-vendor skill repo besides Arm's. (official · ★5 · 2026-07)
- [bouffalolab/bouffalo_sdk `.agents/skills/`](https://github.com/bouffalolab/bouffalo_sdk/tree/master/.agents/skills) - Bouffalo SDK development guide for BL602 / BL616 / BL808, changelog and test-manual skills. (official · coll · ★498 · 2026-09)
- [bouffalolab/bouffalolab-skills](https://github.com/bouffalolab/bouffalolab-skills) - Bouffalo's second skills repo: BL616 low-power IO guide and Wi-Fi low-power collection. (official · ★0 · 2026-09)
- [Ai-Thinker-Open/skills](https://github.com/Ai-Thinker-Open/skills) - Ai-Thinker (安信可) module skills (14): Ai-M62/M61 (BL616), Ai-WB2 (BL602), Ra-01SC LoRa, coredump, OTA generator, module selector; a FlashKey MCP flash/debug device is a sibling. (official · coll · ★8 · 2026-09)
- [Ai-Thinker-Open/FlashKey-skills](https://github.com/Ai-Thinker-Open/FlashKey-skills) - Skills for the FlashKey flash-and-debug device, paired with the `emMCP` UART-to-MCP protocol generation library. (official · ★0 · 2026-08)
- [OpenSiFli/SiFli-SDK `skills/`](https://github.com/OpenSiFli/SiFli-SDK/tree/main/skills) - SiFli SF32 BLE SoC: Windows build, code review, crash-dump triage, USB register-dump analyzer. (official · coll · ★182 · 2026-09)
- [OpenSiFli/SiFli-Skills](https://github.com/OpenSiFli/SiFli-Skills) - SiFli's standalone skills repo, separate from the set inside the SDK. (official · ★1 · 2026-09)
- [openLuat/LuatOS `skill-packs/`](https://github.com/openLuat/LuatOS/tree/master/skill-packs) - Luat (合宙) LuatOS Lua firmware (Air780 / Air101): dev, docs and demo-spec skills over 72 core libraries. (official · coll · ★589 · 2026-09)
- [Xinyuan-LilyGO/lilygo-skills](https://github.com/Xinyuan-LilyGO/lilygo-skills) - LilyGO T-Display / T-Watch / T-Beam pinouts and Arduino / IDF / SF32 builds behind a router skill. (official · ★6 · 2026-07)
- [tuya/TuyaOpen-dev-skills](https://github.com/tuya/TuyaOpen-dev-skills) - TuyaOpen firmware loop: env setup, project config, build, debug helper, dev loop, device auth, add a board, CLI debug, crash decode. (official · coll · ★16 · 2026-07)
- [espressif/esp-claw-skills-lab](https://github.com/espressif/esp-claw-skills-lab) - Espressif's first real skill repo, but device-side: 43 SKILL.md + Lua scripts executed on the ESP32 by the esp-claw runtime (JSON frontmatter, not the agentskills.io format). (official · coll · ★32 · 2026-09)
- [espressif/skills](https://github.com/espressif/skills) - Espressif's host-side skills repo, created 2026-04 and installable via `npx skills add espressif/skills` — still no SKILL.md. (official · placeholder · ★2 · 2026-04)
- [arm/agent-resources](https://github.com/arm/agent-resources) - Arm's registry of agent resources — schema, validator and four registry YAMLs, but no SKILL.md yet. The second vendor placeholder. (official · ★0 · 2026-09)
- [0xchaihu/nxp-mcu-build-verify](https://github.com/0xchaihu/nxp-mcu-build-verify) - Command-line builds for IAR, Keil, MCUXpresso IDE and VS Code MCUX projects. (★28 · 2026-04)
- [JasonYANG170/ch57x-dev-skill](https://github.com/JasonYANG170/ch57x-dev-skill) - WCH CH57x BLE firmware. (★12 · 2026-06)
- [ClarkJ-Infineon/mtb-workspace-template `.github/skills/`](https://github.com/ClarkJ-Infineon/mtb-workspace-template/tree/main/.github/skills) - 19 ModusToolbox Copilot skills by an Infineon engineer (personal repo): BLE setup, Wi-Fi MQTT, OpenOCD debug, dual-core, PSoC 6 → Edge migration, radar DSP. (copilot · coll · ★0 · 2026-05)
- [ailyProject/aily-blockly `public/skills/`](https://github.com/ailyProject/aily-blockly) - Blockly best-practice and library-migration skills for the aily Arduino AI IDE. (coll · ★3.8k · 2026-09)

### SBC / Linux

- [NVIDIA-AI-IOT/jetson-device-skills](https://github.com/NVIDIA-AI-IOT/jetson-device-skills) - Canonical source of `jetson-diagnostic`, `jetson-memory-audit`, `jetson-llm-serve`, `jetson-video-*` and friends, mirrored into NVIDIA/skills; the most-installed hardware skills on skills.sh. (official · coll · ★135 · 2026-08)
- [NVIDIA-AI-IOT/jetson-bsp-skills](https://github.com/NVIDIA-AI-IOT/jetson-bsp-skills) - Canonical source of the `jetson-customize-*` BSP skills: pinmux, PCIe, USB, clocks, fan, carrier derivation, image validation and flashing. (official · coll · ★59 · 2026-06)
- [D-Robotics/moss `jetson-knowledge`](https://github.com/D-Robotics/moss) - Orin / Xavier specs, JetPack / L4T, Super Mode, TensorRT engine builds, alongside D-Robotics RDK skills. (coll · ★142 · 2026-08)
- [Seeed-Projects/Seeed-Jetson-DevelopTool](https://github.com/Seeed-Projects/Seeed-Jetson-DevelopTool/tree/main/skills/openclaw) - Seeed reComputer / Jetson support skills: JetPack overview, Docker setup, AI tools, L4T differences, YOLO on Jetson, FAQ. (coll · ★55 · 2026-09)
- [sammcj/agentic-coding `raspberry-pi-pico2`](https://github.com/sammcj/agentic-coding/tree/main/Skills/raspberry-pi) - RP2350 with a Debug Probe: pico-sdk CMake, ARM and RISC-V, picotool, OpenOCD / GDB / RTT references. (★161 · 2026-09)
- [irfanmuhammedharis/raspberry-pi-skills-suite](https://github.com/irfanmuhammedharis/raspberry-pi-skills-suite) - The only broad Raspberry Pi suite: Pico MicroPython and C SDK, GPIO sensors and actuators, Linux setup, debugging, edge-AI vision, networking, robotics, power. Thin (~3 KB each). (coll · ★0 · 2026-03)
- [TheYoctoJester/dutler](https://github.com/TheYoctoJester/dutler) - A Pico as a USB-serial DUT console bridge and power relay for board farms, with a `run-dutler` skill. (★21 · 2026-07)
- [qualcomm-linux/qcom-linux-skills](https://github.com/qualcomm-linux/qcom-linux-skills) - Qualcomm Linux / meta-qcom / Dragonwing boards: Yocto image build, prebuilt download, LAVA CI report, pre-PR checks, Debian image build. (official · coll · ★6 · 2026-09)
- [prashantdivate/awesome-yocto-ai-agent-skills](https://github.com/prashantdivate/awesome-yocto-ai-agent-skills) - The broadest Yocto suite (12): BSP bring-up, build debug, kas CI builds, deploy and flash, image analysis, kernel BSP, recipe maintenance, security / OTA / SBOM. (coll · ★4 · 2026-07)
- [Higangssh/yocto-agent-skills](https://github.com/Higangssh/yocto-agent-skills) - Official-doc-first, CI-validated Yocto skills: doc router, BSP kernel, image rootfs, layer and recipe review, security SBOM. (coll · ★9 · 2026-08)
- [Angstrom-distribution/meta-angstrom `skills/`](https://github.com/Angstrom-distribution/meta-angstrom) - `boot-validate` boots images on all twelve oe-core QEMU machines plus BeagleBone QEMU and asserts systemd and networking. (official · ★51 · 2026-09)
- [processmission/oh-my-qemu](https://github.com/processmission/oh-my-qemu) - Model boards and peripherals in QEMU: U-Boot build, Linux boot, board and peripheral modeling (17 skills). (coll · ★57 · 2026-07)
- [angelwzr/linux-phone-porting](https://github.com/angelwzr/linux-phone-porting) - Mainline Linux bring-up on Android phones: device tree, bootloader. (★48 · 2026-09)
- [LittleNewton/openwrt-compile-skills](https://github.com/LittleNewton/openwrt-compile-skills) - OpenWrt build runner, feed and package sync, target-switch hygiene. (coll · ★8 · 2026-05)
- [100askTeam/aibsp-imx6ull-pro_linux5.4.47 `.trae/skills/`](https://github.com/100askTeam/aibsp-imx6ull-pro_linux5.4.47) - 100ASK (百问网) i.MX6ULL Buildroot / eMMC / LVGL9 / uuu serial auto-flash skills in TRAE format. (official · coll · ★12 · 2026-05)
- [realsenseai/realsense_mipi_platform_driver `.claude/skills/`](https://github.com/realsenseai/realsense_mipi_platform_driver) - Build, deploy and verify the RealSense MIPI kernel driver on Jetson. (official · coll · ★51 · 2026-09)
- [openharmonyinsight/openharmony-skills](https://github.com/openharmonyinsight/openharmony-skills) - OpenHarmony source build, CI, C++, download, unit tests, security review. (coll · ★34 · 2026-09)
- [anthropics/claude-plugins-official `cwc-makers`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/cwc-makers) - `m5-onboard` detects an M5Stack Cardputer / Core / CoreS3 on USB, flashes UIFlow 2.0 and a MicroPython bundle; `cardputer-buddy` iterates on apps over serial with one-shot REPL. (official · coll · ★36k · 2026-09)

### Robotics

- [NVIDIA/skills](https://github.com/nvidia/skills) - 350+ skills mirrored from NVIDIA product repos; the hardware clusters are `jetson-*` (BSP customization, pinmux, flashing, memory audit, LLM serving on-device), `hsb-*` (Holoscan Sensor Bridge FPGA flashing), `i4h-*` (Isaac for Healthcare robot data collection and RL) and `physical-ai-*`. (official · coll · ★3.3k · 2026-09)
- [isaac-sim/IsaacSim `.claude/skills/`](https://github.com/isaac-sim/IsaacSim/tree/main/.claude/skills) - 43 skills for Isaac Sim: headless deployment, ROS 2 bridge, URDF/MJCF → USD, manipulation IK, navigation primitives, occupancy maps, data collection. (official · coll · ★4.1k · 2026-09)
- [isaac-sim/IsaacLab-Arena `skills/`](https://github.com/isaac-sim/IsaacLab-Arena/tree/main/skills) - Set up the arena, run experiments, and stand up π0 (`serve-openpi-policy`) or GR00T (`serve-gr00t-policy`) policy servers for closed-loop evaluation. (official · coll · ★565 · 2026-09)
- [google-deepmind/mujoco `doc/skills/`](https://github.com/google-deepmind/mujoco/tree/main/doc/skills) - Six official MuJoCo skills: python, rendering, accelerated (MJX / Warp), spec editing, GUI, Studio. (official · coll · ★15.1k · 2026-09)
- [AgibotTech/genie_sim `skills/`](https://github.com/AgibotTech/genie_sim/tree/main/source/geniesim_ros/skills) - Eight AgiBot skills: build workspace, launch scene, MoveIt whole-body control, add a robot from URDF, teleop bridge, record episodes, debug physics. (official · coll · ★1.4k · 2026-09)
- [pollen-robotics/reachy_mini `skills/`](https://github.com/pollen-robotics/reachy_mini/tree/main/skills) - 13 official Reachy Mini skills referenced from AGENTS.md: create an app, safe torque, control loops, symbolic motion, REST API, AI integration. Plain `.md`, no frontmatter. (official · coll · ★1.5k · 2026-09)
- [NVIDIA-AI-IOT/reachy-mini-jetson-assistant](https://github.com/NVIDIA-AI-IOT/reachy-mini-jetson-assistant) - Local voice + vision assistant for Reachy Mini Lite on an Orin Nano, with a `reachy-jetson-deploy` skill. (official · ★33 · 2026-09)
- [wandelbotsgmbh/wandelbots-nova `nova-api-v2`](https://github.com/wandelbotsgmbh/wandelbots-nova/tree/main/.agents/skills/nova-api-v2) - Wandelbots NOVA robot-agnostic motion planning for UR / KUKA / FANUC / ABB / Yaskawa: plan trajectories, limits, models. (official · ★46 · 2026-09)
- [viam-devrel/agent-skills](https://github.com/viam-devrel/agent-skills) - Nine Viam skills: machine config, modules and fleet, local viam-server, Python / Go / C++ / TS SDKs, ML, motion and vision. (official · coll · ★2 · 2026-08)
- [openvinotoolkit/physicalai](https://github.com/openvinotoolkit/physicalai/tree/main/skills) - Intel's runtime for running VLA policies on robots: add a robot integration, add a camera backend, configure the inference pipeline. (official · coll · ★27 · 2026-09)
- [OpenRAL/openral](https://github.com/OpenRAL/openral) - "Robot Agentic Layer": the LLM emits typed tool calls that dispatch rSkills (SmolVLA, π0.5, GR00T, OpenVLA-OFT, MoveIt / Nav2 actions) behind a deny-by-default C++ safety kernel; 50 rSkill SKILL.md files including `rskill-smolvla-so101`. (coll · ★44 · 2026-09)
- [harunkurtdev/ros2-claude-code-template](https://github.com/harunkurtdev/ros2-claude-code-template) - 29 ROS 2 skills including eight for Nav2: costmaps, planners, controllers, behavior trees, plugin authoring. (coll · ★214 · 2026-06)
- [arpitg1304/robotics-agent-skills](https://github.com/arpitg1304/robotics-agent-skills) - Production ROS 1/2 practice: QoS, lifecycle nodes, colcon, DDS, robot bring-up, perception, testing, security, Docker dev, web integration. (coll · ★358 · 2026-08)
- [dbwls99706/ros2-engineering-skills](https://github.com/dbwls99706/ros2-engineering-skills) - Single progressive-disclosure skill: rclcpp / rclpy, QoS / DDS, tf2 / URDF, ros2_control, Nav2, MoveIt 2, real-time, hardware safety. (★175 · 2026-09)
- [adityakamath/ros2-skill](https://github.com/adityakamath/ros2-skill) - Runtime control rather than code generation: drive topics, services, actions, params, lifecycle, ros2_control and Nav2 on a live robot via bundled rclpy scripts. (★18 · 2026-07)
- [j3soon/ros2-essentials `.agents/skills/`](https://github.com/j3soon/ros2-essentials) - TurtleBot3 and Gazebo workspace-testing skills for AMRs. (coll · ★47 · 2026-07)
- [zh-plus/unitree-g1-dev-copilot](https://github.com/zh-plus/unitree-g1-dev-copilot) - Doc-grounded Unitree G1 skill: SDK2, DDS, ROS 2, high- vs low-level motion, D435i head camera; ships its own `evals/`. (★6 · 2026-07)
- [earthtojake/text-to-cad `urdf` / `srdf` / `sdf`](https://github.com/earthtojake/text-to-cad/tree/main/skills/urdf) - Robot description formats inside a CAD/CAM skill library that also covers G-code and Bambu printers. (coll · ★15.8k · 2026-09)
- [rerun-io/rerun `rerun-lerobot`](https://github.com/rerun-io/rerun/tree/main/skills/rerun-lerobot) - Visualize LeRobot datasets in Rerun; siblings `rerun-urdf` and `rerun-mcap`. (official · ★11.4k · 2026-09)
- [Flaminis/Dalaran](https://github.com/Flaminis/Dalaran) - Rerun-alternative robotics visualization and data infra with `dalaran-lerobot` and `dalaran-mcap` skills. (coll · ★777 · 2026-08)
- [nebius/nebius-physical-ai](https://github.com/nebius/nebius-physical-ai) - 38 cloud-tied skills: LeRobot, GR00T, Isaac Lab, Genesis, mjlab, cuRobo, Foxglove, RoboCasa, retargeting. (official · coll · ★29 · 2026-09)
- [aws-samples/sample-embodied-ai-platform `training/gr00t`](https://github.com/aws-samples/sample-embodied-ai-platform) - Fine-tune GR00T from teleop data and deploy to an SO-101 arm. (official · ★15 · 2026-09)
- [NVlabs/RoboLab](https://github.com/NVlabs/RoboLab) - Scene-generation and task-generation skills for policy benchmarking; sibling [GraspGenX](https://github.com/NVlabs/GraspGenX) ships a grasp-generation skill. (official · coll · ★501 · 2026-09)
- [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) - `openpi`, `openvla-oft`, `cosmos-policy` and `tensorrt-llm` skills inside a large general research-skill library. (coll · ★12.7k · 2026-06)
- [ForgeCAD/forgecad-public-kit `forgecad-verify-mujoco`](https://github.com/ForgeCAD/forgecad-public-kit) - Verify CAD-generated robots in MuJoCo. (★934 · 2026-06)
- [wimblerobotics/ros2-copilot-skills](https://github.com/wimblerobotics/ros2-copilot-skills) - 158 Nav2 / behavior-tree / SLAM / Teensy-PlatformIO skills for Copilot; quality is uneven. (coll · ★18 · 2026-04)
- [robium-ai/robium](https://github.com/robium-ai/robium) - ROS 2 / Nav2 / Gazebo / MuJoCo / Isaac / LeRobot plugin with a versioned SKILL.md archive. (coll · ★13 · 2026-09)
- [PatrickJS/awesome-cursorrules `ros-ros2`](https://github.com/PatrickJS/awesome-cursorrules/blob/main/rules/ros-ros2.mdc) - Cursor rule for ROS / ROS 2 packages, nodes, launch files, messages, URDF/xacro. (cursor-rules · ★40.8k · 2026-05)

### Drones

- [PX4/PX4-Autopilot `build-px4`](https://github.com/PX4/PX4-Autopilot/tree/main/.agents/skills/build-px4) - Build PX4 board firmware inside the px4-dev container, worktree-aware; no flashing. (official · ★12.6k · 2026-09)
- [fossuav/aap](https://github.com/fossuav/aap) - "ArduPilot AI Playbooks": build, SITL and Lua scripting skills for Claude, Codex and Gemini. (coll · ★19 · 2026-09)
- [pelageech/ardupilot-agent-toolkit](https://github.com/pelageech/ardupilot-agent-toolkit) - Seven ArduPilot skills: direct control, SITL, Gazebo Harmonic, pymavlink, Pixhawk 6C, mission planning, flight diagnostics. (coll · ★0 · 2026-09)
- [raylanlin/smarttune-cli](https://github.com/raylanlin/smarttune-cli) - Flight-log tuning advisor for ArduPilot, Betaflight and PX4, shipped as skill and MCP. (★29 · 2026-09)
- [SebGalina/betaflight-claude-skill](https://github.com/SebGalina/betaflight-claude-skill) - Betaflight configuration, PID tuning, blackbox analysis, troubleshooting; the author's `betaflight-mcp` talks MSP over USB. (★29 · 2026-09)
- [sensei-hacker/inav-claude](https://github.com/sensei-hacker/inav-claude) - Development workflow for the iNAV flight controller including a hardware-in-the-loop link-testing skill. (coll · ★4 · 2026-09)
- [MIUAV/vibe-coding-ros2](https://github.com/MIUAV/vibe-coding-ros2) - PX4 + ROS 2 Humble drone development: MAVLink, offboard mode, firmware build, module dev, airframes, sensor config, multicopter tuning, vision nav, RKNN. Chinese. (coll · ★26 · 2026-05)
- [castacks/AirStack](https://github.com/castacks/AirStack) - CMU AirLab's "agent-native" ROS 2 aerial autonomy stack with `.agents/skills`. (★91 · 2026-09)

### Space and aerospace

- [esa/nanosat-mo-framework](https://github.com/esa/nanosat-mo-framework) - ESA's CCSDS Mission Operations flight-software framework, with a `mo-xml` skill for authoring its service definitions. The only space-agency-official agent skill found. (official · ★123 · 2026-09)
- [devideamax/aerospace-team](https://github.com/devideamax/aerospace-team) - Twelve satellite-mission skills: GNC, power systems, satellite communications, ground systems and launch operations. (coll · ★21 · 2026-02)

### Edge AI / NPU

- [hailo-ai/hailo-apps `.claude/skills/`](https://github.com/hailo-ai/hailo-apps/tree/main/.claude/skills) - Twelve Hailo skills: camera, build pipeline / LLM / VLM / voice / agent app, model management, monitoring, validate. (official · coll · ★500 · 2026-04)
- [hailo-ai/hailo_model_zoo `.claude/skills/`](https://github.com/hailo-ai/hailo_model_zoo/tree/master/.claude/skills) - `hailo-parse`, `hailo-optimize`, `hailo-compile` for the Dataflow Compiler toolchain. (official · coll · ★708 · 2026-09)
- [hailo-ai/hailo15-agentic-coding](https://github.com/hailo-ai/hailo15-agentic-coding) - Twelve skills and agents for the Hailo-15 vision processor: connect, board status, swap model, cross-compile, deploy to the board — closes the flash → run loop. (official · coll · ★0 · 2026-06)
- [HorizonRobotics/OE-Skills](https://github.com/HorizonRobotics/OE-Skills) - 37 skills for Horizon HBDK compile, HMCT quantization, UCP on-board inference and LLM compression. (official · coll · ★19 · 2026-07)
- [D-Robotics/rdk-device-skills](https://github.com/D-Robotics/rdk-device-skills) - 26 on-device RDK skills (diagnostic, memory audit, camera, BPU model deploy and benchmark, GPIO, TROS); siblings `oe-skills-x5`, `bsp-skills` and `rdk-docs-mcp`. (official · coll · ★2 · 2026-09)
- [luxonis/skills](https://github.com/luxonis/skills) - OAK camera router skill plus seven specialists (app, device setup, inspect, model, record, troubleshoot, workspace) with MCP config and `oakctl`. (official · coll · ★16 · 2026-09)
- [PyTorch ExecuTorch `.claude/skills/`](https://github.com/pytorch/executorch/tree/main/.claude/skills) - Nine ExecuTorch skills: export, building, Cortex-M, Zephyr, Qualcomm, profile, binary size, knowledge base. (official · coll · ★5k · 2026-09)
- [google-ai-edge/litert-samples `skills/`](https://github.com/google-ai-edge/litert-samples/tree/main/skills) - Six LiteRT skills: conversion workflow, accuracy-safe quantization, GPU-clean conversion, on-device verification. (official · coll · ★431 · 2026-09)
- [Dengdxx/PaddleYOLO-RKNN `rknn-flow`](https://github.com/Dengdxx/PaddleYOLO-RKNN) - Rockchip RKNN model conversion flow. Chinese. (★8 · 2026-08)
- [gregm123456/raspberry_pi_hailo_ai_services](https://github.com/gregm123456/raspberry_pi_hailo_ai_services) - Raspberry Pi 5 + Hailo AI HAT services with a Copilot skill. (copilot · ★11 · 2026-09)

### EDA / PCB

- [aklofas/kicad-happy](https://github.com/aklofas/kicad-happy) - Analyze KiCad projects and PDF schematics, DRC / ERC / DFM, EMC pre-compliance, SPICE, part sourcing on DigiKey / Mouser / LCSC / element14, JLCPCB and PCBWay prep. (coll · ★1.2k · 2026-09)
- [autodesk-platform-services/skills](https://github.com/autodesk-platform-services/skills) - Autodesk's official skills for AutoCAD ARX and the Autodesk Platform Services APIs; CAD rather than hardware, and the largest vendor skills repo found. (official · ★46 · 2026-08)
- [easyeda/easyeda-api-skill](https://github.com/easyeda/easyeda-api-skill) - JLC 嘉立创EDA Pro: 120+ API classes plus a WebSocket bridge into the running client. (official · ★708 · 2026-09)
- [zhoushoujianwork/easyeda-agent](https://github.com/zhoushoujianwork/easyeda-agent) - Drive EasyEDA Pro through a local CLI / daemon: schematic, netlist check, PCB placement and routing, DRC, fab export; ships as CLI + skill + MCP. (★438 · 2026-09)
- [diodeinc/pcb](https://github.com/diodeinc/pcb/tree/main/skills) - Zener code-to-PCB language plus `datasheet-reader`, `librarian`, registry search and SPICE simulation skills. (coll · ★448 · 2026-09)
- [atopile/atopile `.claude/skills/`](https://github.com/atopile/atopile/tree/main/.claude/skills) - Code-defined PCB design; `ato` and `ato-language` are user-facing, the rest are compiler / solver / library contributor skills. (coll · ★3.9k · 2026-06)
- [American-Embedded/kistack](https://github.com/American-Embedded/kistack) - Human-written KiCad skill stack: schematic, symbol, footprint, PCB layout, gerbers, panelization, BOM, export, product render. (coll · ★383 · 2026-09)
- [drandyhaas/KiCadRoutingTools](https://github.com/drandyhaas/KiCadRoutingTools) - `plan-pcb-routing` produces a fanout and differential-pair routing plan from a `.kicad_pcb`. (★428 · 2026-09)
- [Seeed-Studio/ai-skills](https://github.com/Seeed-Studio/ai-skills) - `schematic-analyzer` traces KiCad and OrCAD/Allegro schematics; `ee-datasheet-master` extracts pinouts, I2C addresses and register maps from PDFs; SG200x/CV181x media and ONNX → cvimodel skills. (official · coll · ★25 · 2026-09)
- [Tansuo2021/ADtoKeil](https://github.com/Tansuo2021/ADtoKeil) - Read an Altium schematic as evidence, generate Keil firmware for the board it describes, verify over serial. Windows. (coll · ★172 · 2026-06)
- [oaslananka/kicad-mcp-pro](https://github.com/oaslananka/kicad-mcp-pro/tree/main/skills) - `pcb-design` and `kicad-design-review` skills that sit on top of a KiCad MCP: placement, routing, stackup, quality gates. (coll · ★91 · 2026-09)
- [Zane456/PCB-Agent-Teams](https://github.com/Zane456/PCB-Agent-Teams) - Multi-agent KiCad pipeline from topology to Gerber with HV / LV / isolation partitioning. (coll · ★66 · 2026-07)
- [Cognitohazard/ltspice-mcp](https://github.com/Cognitohazard/ltspice-mcp) - LTspice and ngspice MCP with `ltspice`, `ngspice`, `spice-bench-craft` and `spice-experiments` skills. (coll · ★43 · 2026-09)
- [Arcadia-1/gmoverid-skill](https://github.com/Arcadia-1/gmoverid-skill) - Analog IC design on ngspice with SKY130 / PTM models: gm/ID, transistor models, LDO / op-amp / comparator; siblings cover Verilog-A and a Razavi benchmark. (coll · ★122 · 2026-07)
- [SpiceSharp/SpiceSharpParser `.agents/skills/`](https://github.com/SpiceSharp/SpiceSharpParser) - Test-driven netlist design with `.MEAS` verification. (official · ★33 · 2026-08)
- [fireostendere/mcp_diptrace](https://github.com/fireostendere/mcp_diptrace) - DipTrace MCP plus a signal-integrity review skill. (★22 · 2026-09)
- [akiselev/altium-cli `.agents/skills/`](https://github.com/akiselev/altium-cli) - Rust CLI for SchDoc / PcbDoc / libraries with validation, rules review, data review and GUI-control skills. (coll · ★14 · 2026-08)
- [l3wi/claude-eda](https://github.com/l3wi/claude-eda) - `eda-architect`, `eda-schematics`, `eda-pcb`, `eda-drc`, `eda-research` for KiCad. (coll · ★15 · 2026-01)
- [pjcau/esp32-emu-turbo `.claude/skills/`](https://github.com/pjcau/esp32-emu-turbo) - The only DFM skills that drive JLCPCB's DFM tool: upload, validate, PCB review, PCBA readiness. (coll · ★4 · 2026-09)

### FPGA / HDL

- [Shinei-Nouzen-Arch/FPGA-Agent](https://github.com/Shinei-Nouzen-Arch/FPGA-Agent) - The best Vivado / Vitis skill set: synth, impl, sim, Tcl, constraints, debug, analysis, timing closure via RapidWright. (coll · ★170 · 2026-09)
- [hdl-tools/digital-chip-design-agents](https://github.com/hdl-tools/digital-chip-design-agents) - 16 plugins across the chip pipeline: RTL, verification, synthesis, STA, PD, DFT, FPGA, HLS, formal; sibling `analog-chip-design-agents`. (coll · ★203 · 2026-09)
- [Eriemon/verilog-generator](https://github.com/Eriemon/verilog-generator) - Readable Verilog-2001 generation, review and annotation, testbench scaffolds, local or remote Vivado. (★282 · 2026-08)
- [Mindrally/skills `fpga` / `systemverilog`](https://github.com/Mindrally/skills) - Cursor-rule-derived FPGA and SystemVerilog skills, ~1k installs each. (★259 · 2026-09)
- [codejunkie99/Gateflow-Plugin](https://github.com/codejunkie99/Gateflow-Plugin) - SystemVerilog design → verify (cocotb, formal) → deliver on the open-source toolchain, with FuseSoC and IP packaging. (coll · ★113 · 2026-05)
- [one-ware/OneWare](https://github.com/one-ware/OneWare) - `fpga-toolchain-yosys` for Yosys / nextpnr inside ONE WARE Studio. (official · ★143 · 2026-09)
- [a2fpga/a2fpga_core `.claude/skills/`](https://github.com/a2fpga/a2fpga_core) - Gowin Tang Nano 20K bitstream build and flash plus BL616 MCU flash. (coll · ★75 · 2026-08)
- [TONGJI-EDA-LAB/RTL-CLAW](https://github.com/TONGJI-EDA-LAB/RTL-CLAW) - Academic Verilog partition / optimization (Yosys + Verible) / merge skills on OpenClaw. (coll · ★64 · 2026-04)
- [bjwanneng/veriflow-cc](https://github.com/bjwanneng/veriflow-cc) - Architect → RTL → iverilog / Yosys pipeline with cocotb coverage. (★51 · 2026-08)
- [LilithSemi/claude-for-hardware](https://github.com/LilithSemi/claude-for-hardware) - The only FPGA collection with physical bring-up: bitstream over bit-banged JTAG from a Raspberry Pi, synthesis fit, area / timing, bare-metal boot chain, ROHD gotchas. (coll · ★21 · 2026-08)
- [a5c-ai/babysitter `fpga-programming`](https://github.com/a5c-ai/babysitter/tree/main/library/specializations/fpga-programming/skills) - 19 short skills: Verilog / SV / VHDL, timing constraints, CDC, SVA, UVM, HLS, place-and-route, synthesis, debugging. (coll · ★1.8k · 2026-09)
- [wweiyi2004/minifpga-quartus-skill](https://github.com/wweiyi2004/minifpga-quartus-skill) - Quartus Cyclone IV Codex skill; the only Quartus skill with traction. (★8 · 2026-06)
- [Tomer-Harari/claude-fpga-skills](https://github.com/Tomer-Harari/claude-fpga-skills) - Headless vendor flows: Vivado batch, ModelSim headless, cocotb testbench, CDC formal, timing closure, AXI-Stream verification. (coll · ★1 · 2026-08)
- [londey/claude-skill-verilog](https://github.com/londey/claude-skill-verilog) - Verilog working skill. (★18 · 2026-04)

### Wireless

- [simpleble/simpleble `simpleaible`](https://github.com/simpleble/simpleble/tree/main/simpleaible) - SimpleBLE's own MCP and skill: scan, connect, GATT read and notify from the host. (official · ★1.1k · 2026-09)
- [meshtastic/meshtastic-mcp](https://github.com/meshtastic/meshtastic-mcp) - Official Meshtastic MCP with three bundled skills: discover, configure, flash and monitor radios over serial / TCP, end-to-end tests, emulators. (official · coll · ★15 · 2026-09)
- [project-chip/connectedhomeip `.agents/skills/`](https://github.com/project-chip/connectedhomeip/tree/master/.agents/skills) - 14 Matter SDK contributor skills: ZAP cluster generation, code-driven cluster TDD, chip-tool testing, binary size comparison. (official · coll · ★8.9k · 2026-09)
- [SmartThingsCommunity/SmartThingsEdgeDrivers `.agents/skills/`](https://github.com/SmartThingsCommunity/SmartThingsEdgeDrivers/tree/main/.agents/skills) - Samsung's skills for writing Zigbee / Z-Wave / Matter Lua edge drivers: profiles, libraries, test workflow. (official · coll · ★346 · 2026-09)
- [zwave-js/zwave-js `.agents/skills/`](https://github.com/zwave-js/zwave-js) - `author-config-from-web` writes a Z-Wave device config file from a product page. (official · ★887 · 2026-09)
- [BrownFineSecurity/iothackbot](https://github.com/BrownFineSecurity/iothackbot) - IoT pentest with physical tools: JTAG probing, logic-analyzer / MSO capture, picocom UART consoles, telnet shells, chipsec, ONVIF and network scans, jadx / apktool. (coll · ★841 · 2026-06)
- [BasedHardware/omi `.cursor/skills/`](https://github.com/BasedHardware/omi) - `omi-firmware-patterns` for the Omi wearable's nRF / ESP32 Zephyr BLE audio firmware. (cursor-rules · ★7.6k · 2026-09)
- [veonua/SmartThingsEdge-Xiaomi `.agents/skills/`](https://github.com/veonua/SmartThingsEdge-Xiaomi) - Zigbee device onboarding for SmartThings Edge drivers. (★82 · 2026-09)
- [ksachdeva/zephyr-rtos-ai `zephyr-bluetooth-le`](https://github.com/ksachdeva/zephyr-rtos-ai/tree/main/skills/zephyr-bluetooth-le) - GAP / GATT / advertising / pairing / NUS in Zephyr. (★23 · 2026-06)
- [beriberikix/zephyr-agent-skills `connectivity-ble`](https://github.com/beriberikix/zephyr-agent-skills/tree/main/skills/connectivity-ble) - Zephyr BLE plus the `iot-protocols` sibling for MQTT / CoAP / LwM2M. (★64 · 2026-05)
- [wangjianjq/Skill `.agents/skills/`](https://github.com/wangjianjq/Skill) - BLE debugging with Python and Wireshark, plus a Tektronix scope skill. (coll · ★24 · 2026-02)
- [rnd-southerniot/rak3112-rs485-node `.claude/skills/`](https://github.com/rnd-southerniot/rak3112-rs485-node) - LoRaWAN OTAA provisioning, deprovisioning and join verification in ChirpStack for RAK3172 / RAK3112. (coll · ★1 · 2026-07)
- [JasonYANG170/esp-dev-skill `esp-zigbee-sdk`](https://github.com/JasonYANG170/esp-dev-skill/tree/main/repos/esp-zigbee-sdk) - ESP Zigbee SDK sub-skill. (★27 · 2026-08)
- [SnailSploit/Claude-Red `Skills/wireless`](https://github.com/SnailSploit/Claude-Red) - Offensive BLE, LoRaWAN / sub-GHz, Zigbee / Thread / Matter and Z-Wave skills; security-side only. (coll · ★5.1k · 2026-08)

### Hardware security

- [solokeys/solo2](https://github.com/solokeys/solo2) - Solo 2 FIDO2 security-key firmware shipping `solo2-cli` and `solo2-examples` skills for provisioning the key itself. (official · coll · ★713 · 2026-08)
- [dslsdzc/rev-skills](https://github.com/dslsdzc/rev-skills) - 122 reverse-engineering skills including `re-hardware-io` for UART, SPI and JTAG work and `re-javacard`. (coll · ★58 · 2026-09)
- [keycard-tech/keycard-cli](https://github.com/keycard-tech/keycard-cli) - Keycard smartcard CLI with `keycard-admin` and `keycard-signing` skills. (official · coll · ★57 · 2026-09)
- [nemanjan00/claude-code-skills](https://github.com/nemanjan00/claude-code-skills) - Small personal set that happens to hold the only Bus Pirate and smartcard skills in existence. (coll · ★0 · 2026-08)

### Automotive

- [CSS-Electronics/can-bus-reverse-engineering-skills](https://github.com/CSS-Electronics/can-bus-reverse-engineering-skills) - Three skills that reverse-engineer live CAN traffic into DBC files using the CANsub USB / Ethernet interface on a real OBD2 port. (official · coll · ★168 · 2026-08)
- [ecubus/EcuBus-Pro `resources/skills/`](https://github.com/ecubus/EcuBus-Pro/tree/master/resources/skills) - EcuBus-Pro TypeScript scripting API (UDS, CAN-TP, DoIP, LIN, bus events) for its own USB CAN / LIN adapters. (official · ★871 · 2026-09)
- [philipkocanda/canair](https://github.com/philipkocanda/canair) - WiCAN OBD-II Wi-Fi / BLE dongle toolkit with skills for signal reverse-engineering and the WiCAN protocol. (coll · ★25 · 2026-08)
- [spawahh/openpilot-claude-kit](https://github.com/spawahh/openpilot-claude-kit) - Four Claude Code plugins for openpilot including a read-only comma device API and SSH device work. (coll · ★1 · 2026-08)
- [JiaxI2/Codex-Skills `ethercat-cia402`](https://github.com/JiaxI2/Codex-Skills) - EtherCAT slave / CiA 402 / TwinCAT NC diagnosis. Chinese. (★1 · 2026-09)

### Industrial / PLC

- [bulaofen0036-coder/TIA_Portal_Openness_MCP](https://github.com/bulaofen0036-coder/TIA_Portal_Openness_MCP) - Siemens TIA Portal V20 / V21: create, compile and download STEP 7 and WinCC projects through MCP, with a bundled skill. (★241 · 2026-09)
- [Czarnak/totally-integrated-claude](https://github.com/Czarnak/totally-integrated-claude) - Routed TIA Openness plugin (20+ skills): PLC operations, import / export, networks, HMI, Python, MAC module builder. (coll · ★61 · 2026-08)
- [huahaizo/tia-portal-openness-ai](https://github.com/huahaizo/tia-portal-openness-ai) - TIA Openness V15–V21 C# / PowerShell scaffold. (★65 · 2026-05)
- [MichielVanwelsenaere/HomeAutomation.CoDeSys3 `.claude/skills/`](https://github.com/MichielVanwelsenaere/HomeAutomation.CoDeSys3) - Headless CODESYS via ScriptEngine: compile-check a binary `.project`, troubleshoot PLC exceptions. (coll · ★147 · 2026-09)
- [ArthurkaX/cds-text-sync](https://github.com/ArthurkaX/cds-text-sync) - CODESYS ↔ Structured Text sync CLI with an IDE daemon and PLC download, plus a visu-SVG skill. (coll · ★95 · 2026-09)
- [midea-ai/SemaPLC](https://github.com/midea-ai/SemaPLC) - Midea's agentic PLC IDE with a `plc-spec-review` skill. (official · ★83 · 2026-09)
- [MIGO-OvO/plc-skill](https://github.com/MIGO-OvO/plc-skill) - Vendor-neutral IEC 61131-3 ST / LD / FBD / SFC with vendor routing; ~1k ClawHub installs. (★23 · 2026-05)
- [Navifra-Sally/vda5050-skill](https://github.com/Navifra-Sally/vda5050-skill) - VDA 5050 AGV and AMR fleet protocol: spec facts, JSON schemas and a message validator. (★0 · 2026-09)
- [eponce00/twincat-mcp](https://github.com/eponce00/twincat-mcp) - TwinCAT 3 build, deploy, TcUnit and ADS inspection over MCP. (★29 · 2026-09)
- [TechIndustryX/twincat-agent](https://github.com/TechIndustryX/twincat-agent) - TwinCAT Structured Text rules plus an MCP executable. (coll · ★28 · 2026-06)
- [SionVerhoef/twincat-st](https://github.com/SionVerhoef/twincat-st) - TwinCAT 3 / CODESYS ST with an executable `st_review.py` (blocking loops, float equality). (★1 · 2026-09)
- [FREEZONEX/ia2](https://github.com/FREEZONEX/ia2) - Agent-first IEC 61131-3 IDE and runtime with Modbus, EtherCAT, OPC UA, CANopen and HMI. (★4 · 2026-09)
- [gmantoha/ctrlx-os-agent-skills](https://github.com/gmantoha/ctrlx-os-agent-skills) - Bosch Rexroth ctrlX OS / CORE snaps, Data Layer, PLC. (★6 · 2026-09)
- [Meisterschulen-am-Ostbahnhof-Munchen/4diac_training1 `.agents/skills/`](https://github.com/Meisterschulen-am-Ostbahnhof-Munchen/4diac_training1) - IEC 61499 function blocks, adapters and systems for Eclipse 4diac. (★1 · 2026-09)
- [OPCFoundation/UA-.NETStandard `.agents/skills/`](https://github.com/OPCFoundation/UA-.NETStandard) - `opcua-v20-migration` for the OPC Foundation's .NET stack. (official · ★2.4k · 2026-09)
- [riclolsen/json-scada `.agents/skills/`](https://github.com/riclolsen/json-scada) - `protocol-driver-development` for adding Modbus / DNP3 / IEC 60870 / IEC 61850 drivers to JSON-SCADA. (official · ★423 · 2026-08)
- [studioxvii/modbus-skills](https://github.com/studioxvii/modbus-skills/tree/main/plugins/modbus-skills/skills) - 20 read-only Modbus engineering skills: extract a register map from an OEM PDF, normalize it, check byte order, plan reads, build modpoll / ModScan / Node-RED packs, analyze captures. (coll · ★1 · 2026-09)
- [wirenboard/wb-ai-skills](https://github.com/wirenboard/wb-ai-skills) - Wiren Board PLC vendor skills: talk to controllers over MQTT and Modbus, write wb-rules, manage Zigbee and serial devices, root-cause analysis. (official · coll · ★3 · 2026-09)
- [TuojianLYU/openplc-codex-skill](https://github.com/TuojianLYU/openplc-codex-skill) - Generate an OpenPLC v4 project with ladder `.ld` files. (★1 · 2026-06)

### Pro AV and building systems

- [shorty456132/av-module-maker](https://github.com/shorty456132/av-module-maker) - Generates Q-SYS, Extron and Crestron control modules, with SIMPL+, SIMPL# and SIMPL# Pro skills. (coll · ★9 · 2026-09)
- [Crestron/CrestronAISkills](https://github.com/Crestron/CrestronAISkills) - Crestron's own agent-skill plugin and Copilot variant for AV control programming; the only pro-AV vendor to ship skills. (official · coll · ★4 · 2026-09)

### Lab instruments

- [nominal-io/instro](https://github.com/nominal-io/instro) - Typed multi-vendor instrument library (PSU, DMM, scope, DAQ, e-load) whose skills scaffold new drivers and validate them against real instruments. (official · coll · ★704 · 2026-09)
- [ma-compbio-lab/SkillFoundry](https://github.com/ma-compbio-lab/SkillFoundry) - Scientific-agent skill framework whose `qcodes-parameter-sweep-starter` is the only QCoDeS instrument-sweep skill found. (coll · ★39 · 2026-09)
- [RRGGZZ/Zurich_Instruments_Skills](https://github.com/RRGGZZ/Zurich_Instruments_Skills) - Zurich Instruments MFLI lock-in amplifier. (★1 · 2026-07)
- [jetperch/pyjoulescope_ui `ui-remote`](https://github.com/jetperch/pyjoulescope_ui/tree/main/.claude/skills/ui-remote) - Drive the Joulescope power-analyzer UI over its TCP remote-control interface. (official · ★109 · 2026-08)
- [Scaxlibur/WaveBench](https://github.com/Scaxlibur/WaveBench) - SCPI bench-instrument skill set. (★62 · 2026-08)
- [Erlla/DS1202ZE-skills](https://github.com/Erlla/DS1202ZE-skills) - Rigol DS1202Z-E scope over USBTMC with a Python CLI; sibling `DM3058E-skills` for the DMM. (★1 · 2026-07)
- [K-Dense-AI/scientific-agent-skills `opentrons-integration`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/opentrons-integration) - Opentrons Protocol API v2 authoring for real OT-2 / Flex robots, inside a very large general science-skill library (stars are library-wide). (★45k · 2026-09)
- [KRATSZ/labscriptai-ot](https://github.com/KRATSZ/labscriptai-ot) - Opentrons plugin: MCP server, seven skills, safety policy, protocol library. (coll · ★2 · 2026-07)
- [DCC-Lab/PyHardwareLibrary](https://github.com/DCC-Lab/PyHardwareLibrary) - USB / serial lab-device library (spectrometers, stages, lasers, DAQ) with a driver-authoring skill. (★12 · 2026-08)
- [deepmodeling/Uni-Lab-OS](https://github.com/deepmodeling/Uni-Lab-OS) - Self-driving-lab platform with AGENTS.md and an `add-device` Cursor skill. (cursor-rules · ★177 · 2026-09)

### Digital fabrication

- [codeofaxel/Kiln](https://github.com/codeofaxel/Kiln) - One 3D-printing MCP across OctoPrint, Moonraker, Bambu, Prusa Link, Elegoo, Duet and Marlin plus headless PrusaSlicer / Orca / Bambu slicing; `pip install kiln3d`, ships a SKILL.md. (★57 · 2026-09)
- [earthtojake/text-to-cad `bambu-labs` / `gcode`](https://github.com/earthtojake/text-to-cad/tree/main/skills/bambu-labs) - Bambu printer control and G-code generation; `bambu-labs` has ~6.7k installs on skills.sh. (★15.8k · 2026-09)
- [santiagomoneta/3d-printing-skills](https://github.com/santiagomoneta/3d-printing-skills) - Klipper config, diagnostics and calibration through the Moonraker API, plus OrcaSlicer. (coll · ★4 · 2026-03)
- [George-RD/cli-anything-meerk40t](https://github.com/George-RD/cli-anything-meerk40t) - Wraps the real MeerK40t kernel (GRBL / Ruida / Lihuiyu) for headless agent-driven laser jobs. (★2 · 2026-08)
- [jl-codes/laser-skills](https://github.com/jl-codes/laser-skills) - LightBurn design, preflight and job skills; design-only, never fires the laser. (coll · ★0 · 2026-08)
- [Lordgrimz/escpos-skill](https://github.com/Lordgrimz/escpos-skill) - Byte-accurate ESC/POS command streams for thermal receipt printers, derived from the canonical specification. (★0 · 2026-04)
- [johncattrall/keymap-ai](https://github.com/johncattrall/keymap-ai) - Audit and generate ZMK / QMK keymaps (home-row mods, layers). (★22 · 2026-08)

### Smart Home

- [home-assistant/core `.claude/skills/`](https://github.com/home-assistant/core/tree/dev/.claude/skills) - `ha-integration-knowledge`, `ha-quality-scale-verify`, `ha-review` for writing Home Assistant integrations. (official · coll · ★90k · 2026-09)
- [komal-SkyNET/claude-skill-homeassistant](https://github.com/komal-SkyNET/claude-skill-homeassistant/tree/main/skills/home-assistant-manager) - Manage Home Assistant via its API: modern automation YAML (2024.10+), dashboards, a verification protocol before applying changes. (★957 · 2026-07)
- [homeassistant-ai/skills `home-assistant-best-practices`](https://github.com/homeassistant-ai/skills/tree/main/skills/home-assistant-best-practices) - Automations, helpers, scripts, dashboards, blueprints; the most-installed hardware-adjacent skill on skills.sh (~7k). (★746 · 2026-09)
- [tuya/tuya-openclaw-skills](https://github.com/tuya/tuya-openclaw-skills) - `tuya-smart-control` drives Tuya devices from OpenClaw through a tuya.ai key (cloud-side). (official · ★510 · 2026-04)
- [jtenniswood/espcontrol `.agents/skills/`](https://github.com/jtenniswood/espcontrol) - `flash-displays` for ESPHome OTA and USB flashing of ESP32 display boards. (★1k · 2026-09)
- [bradsjm/hassio-addons](https://github.com/bradsjm/hassio-addons) - Seven HA skills published through an add-on: automation scripts, dashboard cards, entities and services, ESPHome, integrations, custom integrations, AWTRIX. (coll · ★45 · 2026-07)
- [nodnarbnitram/claude-code-extensions `esphome-config-helper`](https://github.com/nodnarbnitram/claude-code-extensions) - ESPHome YAML generation, validation and troubleshooting. (★16 · 2026-04)

## MCP servers and bridges

Tool servers an agent calls at runtime. The best current surveys of this space are Veecle's two August 2026 reviews (linked under Papers and articles); beriberikix/awesome-mcp-hardware (under Related lists) is the upstream list this section started from.

### MCU / Embedded (MCP)

- [78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) - ESP32 voice-AI chatbot firmware built on MCP: the device exposes its own tools to the LLM. Paired with [xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server) (★10.6k). (★29.9k · 2026-09)
- [horw/esp-mcp](https://github.com/horw/esp-mcp) - ESP-IDF build, flash and automatic build-error fixing. (★157 · 2025-12)
- [golioth/tinymcp](https://github.com/golioth/tinymcp) - Let LLMs control constrained embedded devices via MCP proxied through Golioth cloud RPC. Experimental. (official · ★157 · 2025-07)
- [jl-codes/platformio-mcp](https://github.com/jl-codes/platformio-mcp) - Build, upload and monitor across the 1000+ PlatformIO boards. (★51 · 2026-09)
- [shieldyguy/stm32-mcp](https://github.com/shieldyguy/stm32-mcp) - Build, flash and talk to STM32 over SWD and serial. (★25 · 2026-08)
- [espressif/esp-rainmaker-mcp](https://github.com/espressif/esp-rainmaker-mcp) - Control ESP RainMaker devices through the RainMaker CLI. (official · ★18 · 2025-07)
- [hardware-mcp/arduino-mcp-server](https://github.com/hardware-mcp/arduino-mcp-server) - Wraps arduino-cli: compile, upload, serial sessions. (★17 · 2026-08)
- [Oliver0804/arduino-cli-mcp](https://github.com/Oliver0804/arduino-cli-mcp) - Arduino CLI for VS Code / Claude: compile, upload, library management. (★13 · 2026-05)
- [Volt23/mcp-arduino-server](https://github.com/Volt23/mcp-arduino-server) - Arduino CLI bridge: sketch, board, library and file management. (★10 · 2026-01)
- [SWITCHSCIENCE/mcp-micropython-bridge](https://github.com/SWITCHSCIENCE/mcp-micropython-bridge) - Bridge to a MicroPython REPL on ESP32 / RP2040 over USB serial. Japanese docs. (★9 · 2026-04)
- [neusse/Codex-Circuitpython-MCP](https://github.com/neusse/Codex-Circuitpython-MCP) - CircuitPython board discovery, file deployment, serial read, interrupt and reset. (★7 · 2026-05)
- [ctrlpi/pico-bay](https://github.com/ctrlpi/pico-bay) - Manage Raspberry Pi Pico and ESP32 boards over USB running either MicroPython or CircuitPython. (★5 · 2026-09)
- [Wokwi MCP mode](https://docs.wokwi.com/wokwi-ci/mcp-support) - `wokwi-cli mcp` exposes hosted Wokwi simulation to an agent: run Arduino / ESP32 / RP2040 firmware and read serial without a board. (official)

### On-device MCP servers

MCP servers that run on the microcontroller or SBC itself, so the device is the tool provider.

- [espressif/esp-iot-solution `mcp-c-sdk`](https://github.com/espressif/esp-iot-solution/tree/master/components/mcp-c-sdk) - C for ESP-IDF 5.4+: Streamable HTTP, SSE and custom transports; tools, resources, prompts, completions, async tasks. ~24k downloads on the ESP Component Registry; what esp-claw is built on. (official · ★2.7k · 2026-07)
- [Zephyr MCP server library](https://docs.zephyrproject.org/latest/services/connectivity/networking/api/mcp.html) - Upstream `subsys/net/lib/mcp`, NXP-authored and merged 2026-06: the first RTOS with an in-tree MCP server (HTTP with SSE fallback, tools only, experimental). (official)
- [emqx/esp-mcp-over-mqtt](https://github.com/emqx/esp-mcp-over-mqtt) - ESP-IDF component serving MCP over MQTT 5.0 per the MCP-over-MQTT spec. (official · ★8 · 2025-12)
- [servoagents/mcp-c](https://github.com/servoagents/mcp-c) - Transport-neutral C99 core with POSIX, Zephyr and ESP32 examples; HTTP, stdio, MQTT 5, experimental CoAP. (★2 · 2026-09)
- [solnera/esp32-mcpserver](https://github.com/solnera/esp32-mcpserver) - Arduino / ESP32 HTTP JSON-RPC over AsyncTCP with mDNS and worker-task tool calls; PlatformIO `ESP32-MCPServer`, siblings add BLE transport. (★11 · 2026-08)
- [AaronWander/EmbedMCP](https://github.com/AaronWander/EmbedMCP) - C library to run an MCP server on STM32, ESP32, nRF or Raspberry Pi. (★31 · 2026-02)
- [navado/ESP32MCPServer](https://github.com/navado/ESP32MCPServer) - ESP32 WebSocket MCP server exposing NMEA2000 / NMEA0183 / OBD-II sensors. (★60 · 2026-03)
- [rzeldent/esp32-cam-ai](https://github.com/rzeldent/esp32-cam-ai) - MCP server baked into ESP32-CAM firmware. (★28 · 2026-08)
- [ThanabordeeN/MCP-U_Arduino](https://github.com/ThanabordeeN/MCP-U_Arduino) - Arduino Library Manager `MCP-U`: JSON-RPC over any `Stream` on AVR / ESP / RP2040 exposing GPIO, PWM, ADC and I2C, with an npm client translating to spec MCP. (★4 · 2026-05)
- [PedroFnseca/esp32-mcp](https://github.com/PedroFnseca/esp32-mcp) - Arduino Library Manager `ESP32-MCP`: stateless MCP 2026-07-28 with host unit tests and CI. (★1 · 2026-08)
- [matta-pie/micro-mcp](https://github.com/matta-pie/micro-mcp) - MicroPython MCP server verified on Pico W / Pico 2 W; HTTP and stdio-over-USB transports. (★1 · 2026-02)
- [solnera/esp32-ble-mcp-server](https://github.com/solnera/esp32-ble-mcp-server) - The one real MCP-over-BLE GATT transport: ESP32 server plus FastMCP / TS / Swift BLE client transports. (★1 · 2026-02)

### Serial / bus / debug (MCP)

- [Adancurusul/embedded-debugger-mcp](https://github.com/Adancurusul/embedded-debugger-mcp) - 24-tool debugger over probe-rs / OpenOCD for Cortex-M, RISC-V and Xtensa, with a bundled Claude / Codex skill. Veecle's top pick. (★187 · 2026-07)
- [Adancurusul/serial-mcp-server](https://github.com/Adancurusul/serial-mcp-server) - Rust serial / UART MCP and CLI with JSON macro automation and agent skills. (★91 · 2026-07)
- [Ipiano/gdb-mcp](https://github.com/Ipiano/gdb-mcp) - Drives GDB/MI directly for embedded and native targets. (★48 · 2026-03)
- [YaoIsAI/SerialRUN](https://github.com/YaoIsAI/SerialRUN) - Rust serial debugger for Modbus / PLC / CAN / I2C / SPI with a 15-tool MCP server. (★38 · 2026-06)
- [es617/dbgprobe-mcp-server](https://github.com/es617/dbgprobe-mcp-server) - Symbol-aware (ELF / SVD) on-chip debug through J-Link, CMSIS-DAP and ST-Link. (★10 · 2026-03)
- [Leonezz/openbaud](https://github.com/Leonezz/openbaud) - Serial devices as typed, auditable MCP tools: decode, capture, replay. (★6 · 2026-09)
- [magnusmalm/smolmux](https://github.com/magnusmalm/smolmux) - C11 serial and GDB-SWD multiplexer with an MCP server, so one probe serves several consumers. (★2 · 2026-08)
- [Pan-Robotics/bus-mcp](https://github.com/Pan-Robotics/bus-mcp) - Raspberry Pi CAN / CAN-FD, RS-485 / UART, I2C, SPI and GPIO as MCP tools, read-only by default. (★2 · 2026-06)
- [mcp2everything/mcp2mqtt](https://github.com/mcp2everything/mcp2mqtt) - MCP → MQTT bridge for hardware control; the most-cited early work, but unmaintained. Siblings `mcp2serial` and `mcp2tcp` are equally stale. (★371 · stale since 2024-12)

### Robotics (MCP)

- [robotmcp/ros-mcp-server](https://github.com/robotmcp/ros-mcp-server) - Connect Claude / GPT to ROS and ROS 2 robots via rosbridge; client counterpart [robotmcp_client](https://github.com/robotmcp/robotmcp_client). (★1.5k · 2026-09)
- [Rerun viewer-mcp](https://rerun.io/docs/reference/viewer/mcp) - Official `rerun viewer-mcp` subcommand drives a running or headless Rerun Viewer over gRPC. (official)
- [Foxglove Desktop MCP server](https://docs.foxglove.dev/docs/agents/mcp-server) - Built into Foxglove Desktop: inspect data, build layouts, write user scripts, playback, docs search; local endpoint, needs a Pro / Enterprise / Academic seat. (official)
- [Roboflow MCP](https://blog.roboflow.com/mcp-server/) - Hosted `mcp.roboflow.com`: training, Workflows, hosted inference and edge-device provisioning; [computer-vision-skills](https://github.com/roboflow/computer-vision-skills) ships ten skills as a Claude / Codex plugin. (official)
- [Extelligence-ai/bagel](https://github.com/Extelligence-ai/bagel) - Query robotics, drone and IoT telemetry (ROS bags, MCAP, PX4 logs) in plain English with an edge data-reduction pipeline. (★396 · 2026-09)
- [rokbenko/quackd](https://github.com/rokbenko/quackd) - One CLI / MCP for seven bodies (Microduck, Open Duck, SO-101, XLeRobot, AlohaMini, ToddlerBot, rosbridge) with per-robot skill contracts; sim and mock so far. (★200 · 2026-09)
- [omni-mcp/isaac-sim-mcp](https://github.com/omni-mcp/isaac-sim-mcp) - Natural-language control of NVIDIA Isaac Sim scenes and robots. (★190 · 2025-04)
- [wise-vision/ros2_mcp](https://github.com/wise-vision/ros2_mcp) - ROS 2 MCP with image streaming and automatic QoS matching. (★88 · 2026-08)
- [lpigeon/unitree-go2-mcp-server](https://github.com/lpigeon/unitree-go2-mcp-server) - Control a Unitree Go2 robot dog through ROS 2. (★87 · 2026-06)
- [kakimochi/ros2-mcp-server](https://github.com/kakimochi/ros2-mcp-server) - Topic-based ROS 2 control. (★83 · 2025-06)
- [IliaLarchenko/robot_MCP](https://github.com/IliaLarchenko/robot_MCP) - SO-ARM100 / 101 and LeKiwi arm control in the LeRobot ecosystem. (★83 · 2025-08)
- [Yutarop/ros-mcp](https://github.com/Yutarop/ros-mcp) - ROS topics, services and actions as MCP tools. (★36 · 2025-08)
- [agentculture/reachy-mini-mcp](https://github.com/agentculture/reachy-mini-mcp) - Single-tool Reachy Mini MCP with sequence mode for the real server or sim; the companion CLI ships a `find-reachy` skill. (★32 · 2026-07)
- [jackccrawford/reachy-mini-mcp](https://github.com/jackccrawford/reachy-mini-mcp) - Pollen Robotics Reachy Mini control. (★29 · 2026-07)
- [binabik-ai/mcp-rosbags](https://github.com/binabik-ai/mcp-rosbags) - Offline rosbag analysis. (★28 · 2025-09)
- [phospho-app/phospho-mcp-server](https://github.com/phospho-app/phospho-mcp-server) - VLA bridge for SO-100 / 101 arms. (★10 · 2025-09)
- [neka-nat/mycobot-mcp](https://github.com/neka-nat/mycobot-mcp) - Elephant Robotics myCobot; the only one for that vendor. (★8 · 2025-05)
- [nonead/Nonead-Universal-Robots-MCP](https://github.com/nonead/Nonead-Universal-Robots-MCP) - Universal Robots cobot MCP middleware (zh / en / jp docs). (★7 · 2026-09)
- [monteslu/robot-mcp](https://github.com/monteslu/robot-mcp) - Johnny-Five MCP: Arduino and Raspberry Pi servos and hardware. (★7 · 2026-02)
- [eliasbitsch/abb-robotstudio-mcp](https://github.com/eliasbitsch/abb-robotstudio-mcp) - ABB RobotStudio SDK add-in plus Robot Web Services on real controllers. (★6 · 2026-05)
- [RoversX/universal-robot-mcp](https://github.com/RoversX/universal-robot-mcp) - Universal Robots cobot control. (★5 · 2025-09)
- [ros-claw/unitree-sdk2-mcp](https://github.com/ros-claw/unitree-sdk2-mcp) - Unitree G1 / Go2 / H1 / B2 / A2 / R1 over DDS with no ROS; the ros-claw org holds ~35 sibling MCPs (RealSense, Vicon, Nav2, MoveIt 2, UR, LIMO, Inspire hand). (★4 · 2026-04)
- [gtoff/moveit-mcp-server](https://github.com/gtoff/moveit-mcp-server) - MoveIt 2 planning as MCP tools. (★4 · 2026-03)
- [ros-claw/inspire-rh56-mcp](https://github.com/ros-claw/inspire-rh56-mcp) - Inspire RH56 dexterous hand over CAN, revalidated on a physical hand. (★1 · 2026-07)
- [erh/viam-mcp-server](https://github.com/erh/viam-mcp-server) - MCP as a Viam module: per-method tools generated from each component's Go interface, by Viam's CEO. (★0 · 2026-04)

### Drones (MCP)

- [ion-g-ion/MAVLinkMCP](https://github.com/ion-g-ion/MAVLinkMCP) - PX4 / ArduPilot drones via MAVLink. (★23 · 2026-08)
- [ysznai/dji-waypoint-mcp](https://github.com/ysznai/dji-waypoint-mcp) - DJI waypoint and route planning (大疆航线规划); the only DJI server beyond the Tello. (★7 · 2025-07)
- [0xKoda/drone-mcp](https://github.com/0xKoda/drone-mcp) - DJI Tello drone control. (★25 · 2025-04)
- [showkeyjar/robot-mcp-server](https://github.com/showkeyjar/robot-mcp-server) - Unitree and DJI drone motion control. (★12 · 2026-03)
- [hfujikawa77/ardupilot-mcp-server](https://github.com/hfujikawa77/ardupilot-mcp-server) - ArduPilot control over MAVLink TCP. Japanese. (★9 · 2026-05)
- [rmeadomavic/ardupilot-mcp](https://github.com/rmeadomavic/ardupilot-mcp) - SITL-first, safety-gated ArduPilot MAVLink MCP. (★2 · 2026-08)
- [starlordz12/inav-mcp](https://github.com/starlordz12/inav-mcp) - Setup, diagnosis and tuning of iNAV fixed-wing flight controllers over USB. (★2 · 2026-08)
- [bvandevliet/betaflight-mcp](https://github.com/bvandevliet/betaflight-mcp) - Live Betaflight CLI configuration and PID assistant with a bundled tuning skill. (★1 · 2026-08)

### Simulators (MCP)

- [kvgork/gazebo-mcp](https://github.com/kvgork/gazebo-mcp) - Gazebo: spawn TurtleBot3, multi-robot fleets, world generation, sensor data. (★17 · 2026-07)
- [robotlearning123/mujoco-mcp](https://github.com/robotlearning123/mujoco-mcp) - 65 MuJoCo tools: trajectory optimization, contact analysis, video export, viewer. (★9 · 2026-06)
- [Rongxuan-Zhou/mujoco-mcp-server](https://github.com/Rongxuan-Zhou/mujoco-mcp-server) - Simulate, render, analyze and build RL environments in MuJoCo from Claude Code. (★8 · 2026-03)
- [nullbyte91/nvidia-isaac-mcp](https://github.com/nullbyte91/nvidia-isaac-mcp) - Isaac Sim extension plus external MCP, with Isaac Lab hooks. (★8 · 2026-02)
- [game4automation/io.realvirtual.mcp](https://github.com/game4automation/io.realvirtual.mcp) - Unity digital-twin MCP: drives, sensors, PLC signals, robot IK. (official · ★15 · 2026-07)
- [mergeos-bounties/gazebo-mcp](https://github.com/mergeos-bounties/gazebo-mcp) - Gazebo (gz-sim) worlds, models, poses and stepping with a full offline mock for CI. (★4 · 2026-07)
- [SchiopuAndreiViorel/coppelia-mcp](https://github.com/SchiopuAndreiViorel/coppelia-mcp) - Claude ↔ CoppeliaSim. (★4 · 2026-03)
- [lyuai/genesis-mcp](https://github.com/lyuai/genesis-mcp) - Genesis World simulator MCP with visualization. (★5 · 2025-03)
- [punithkrishnakeepudi/webots-mcp-server](https://github.com/punithkrishnakeepudi/webots-mcp-server) - Webots launch, monitor, RL training and scene manipulation; the only Webots MCP found. (★0 · 2026-04)

### Industrial IoT (MCP)

- [anviod/edgeCore](https://github.com/anviod/edgeCore) - Industrial edge runtime speaking Modbus, BACnet, OPC UA, S7 and EtherNet/IP, deployed on the plant floor. (★126 · 2026-09)
- [rivie13/studio5000-AI-Assistant](https://github.com/rivie13/studio5000-AI-Assistant) - Rockwell Automation SDK and internal documentation as MCP tools for Studio 5000. (★35 · 2025-12)
- [Nodeblue-AI/studio5000-mcp-server](https://github.com/Nodeblue-AI/studio5000-mcp-server) - Parses Studio 5000 L5X project exports for Rockwell and Allen-Bradley PLCs; the sibling `bridge-mcp-server` correlates them with Ignition SCADA. (★19 · 2026-08)
- [ThingsPanel/thingspanel-mcp](https://github.com/ThingsPanel/thingspanel-mcp) - ThingsPanel IoT platform device control and data analysis. (★47 · 2025-11)
- [chewcw/tia-portal-openness-mcpserver](https://github.com/chewcw/tia-portal-openness-mcpserver) - Siemens TIA Portal Openness MCP. (★37 · 2026-05)
- [kukapay/opcua-mcp](https://github.com/kukapay/opcua-mcp) - Connect to OPC UA systems: monitor, analyze and control nodes. (★28 · 2025-10)
- [midhunxavier/OPCUA-MCP](https://github.com/midhunxavier/OPCUA-MCP) - OPC UA MCP server. (★25 · 2026-09)
- [kukapay/modbus-mcp](https://github.com/kukapay/modbus-mcp) - Standardize and contextualize Modbus registers for agents. (★24 · 2025-05)
- [OPCFoundation/UA-for-AI-Prototype](https://github.com/OPCFoundation/UA-for-AI-Prototype) - OPC UA for AI working group: specs turned into RAG chunks and a hosted MCP at reference.opcfoundation.org/mcp, with a plan to cover 430+ companion specs. (official · ★14 · 2026-06)
- [efranceschetti/festo-codesys-mcp](https://github.com/efranceschetti/festo-codesys-mcp) - Festo / CODESYS MCP with ST authoring, PLCopen XML, motion control and error-diagnosis skills. (★1 · 2026-09)
- [lwsinclair/IoT-Edge-MCP-Server](https://github.com/lwsinclair/IoT-Edge-MCP-Server) - Unifies MQTT, Modbus and InfluxDB for SCADA / PLC work. (★3 · 2025-11)
- [daedalus/mcp-snap7](https://github.com/daedalus/mcp-snap7) - Siemens S7 PLC via python-snap7. (★0 · 2026-04)

### Automotive (MCP)

- [farzadnadiri/MCP-CAN](https://github.com/farzadnadiri/MCP-CAN) - OBD-II (J1979), UDS and J1939 diagnostics over SocketCAN / vcan; pip-installable. (★16 · 2026-08)
- [hexsecs/canarchy](https://github.com/hexsecs/canarchy) - Stream-first CAN / J1939 toolkit (python-can, SocketCAN) with built-in MCP server, TUI and fuzzing. (★4 · 2026-09)
- [HadiCherkaoui/klartext](https://github.com/HadiCherkaoui/klartext) - Native Rust BMW F-series diagnostics over an ENET cable (HSFZ / UDS) with an MCP server. (★5 · 2026-08)
- [chrisbray85/headless-ista](https://github.com/chrisbray85/headless-ista) - An agent drives BMW ISTA+ via MCP and reads faults and test plans as text. (★4 · 2026-09)
- [petrpatek/obd2-mcp-server](https://github.com/petrpatek/obd2-mcp-server) - ELM327 over Bluetooth or USB: DTCs and live PIDs, with a `--mock` mode. (★3 · 2026-05)
- [awtoau/awto-can](https://github.com/awtoau/awto-can) - SocketCAN MCP daemon: DBC-aware TX / RX, ISO-TP, capture and replay, live DBC validation. (★0 · 2026-04)
- [mikehaller/kuksa-mcp-server](https://github.com/mikehaller/kuksa-mcp-server) - Read and write COVESA VSS signals through the Eclipse Kuksa Databroker; the only VSS MCP found. (★0 · 2026-06)
- [cyrusdavirusss/j2534-mcp-server](https://github.com/cyrusdavirusss/j2534-mcp-server) - J2534 PassThru UDS / OBD-II; the only J2534 MCP found. Windows. (★0 · 2026-09)
- [daedalus/mcp-canbus](https://github.com/daedalus/mcp-canbus) - Minimal CAN bus MCP. (★0 · 2026-03)

### Building automation and energy (MCP)

- [knx-ai/knx-ets-mcp](https://github.com/knx-ai/knx-ets-mcp) - MCP into ETS 5 / 6 through an ETS add-in: inspect and edit projects, program and scan devices. Windows. (★31 · 2026-08)
- [NickoScope/nickol-knx-mcp](https://github.com/NickoScope/nickol-knx-mcp) - Design-time KNX / ETS validator and repair (DPT, Secure, Matter). (★24 · 2026-09)
- [ezhuk/bacnet-mcp](https://github.com/ezhuk/bacnet-mcp) - BACnet property read and write; `pip install bacnet-mcp`. (★5 · 2026-09)
- [chappo/rusty-bacnet-mcp](https://github.com/chappo/rusty-bacnet-mcp) - Rust BACnet MCP: discovery, sensors, setpoints; read-only by default, single binary. (★0 · 2026-08)
- [lubosstrejcek/victron-tcp](https://github.com/lubosstrejcek/victron-tcp) - Victron GX over local Modbus TCP and MQTT, 32 tools over 900+ registers; sibling `victron-vrm-mcp` for the cloud. (★3 · 2026-09)
- [flowiesner/fronius-mcp](https://github.com/flowiesner/fronius-mcp) - Fronius Solar API: PV, battery, grid feed-in. (★1 · 2026-04)
- [mregen/shelly-em-mcp](https://github.com/mregen/shelly-em-mcp) - Shelly Pro 3EM / EM / Plus PM local energy readings. (★1 · 2026-09)
- [mrksmts/homewizard-mcp-server](https://github.com/mrksmts/homewizard-mcp-server) - HomeWizard P1 smart-meter local API, read-only. (★1 · 2026-04)
- [gkoenig/anker-solix-mcp](https://github.com/gkoenig/anker-solix-mcp) - Anker Solix Solarbank and smart meter. (★1 · 2026-09)
- [bjeans/homelab-mcp](https://github.com/bjeans/homelab-mcp) - Homelab bundle whose UPS server speaks the NUT protocol directly to the hardware. (★43 · 2026-06)
- [javierojan/askacharge-mcp](https://github.com/javierojan/askacharge-mcp) - Operate a fleet of OCPP charge points. (★0 · 2026-09)
- [cr2007/mcp-helvarnet](https://github.com/cr2007/mcp-helvarnet) - Helvar DALI lighting via HelvarNet; the only DALI MCP found. (★0 · 2026-01)
- [SAP/e-mobility-charging-stations-simulator `skills/`](https://github.com/SAP/e-mobility-charging-stations-simulator) - EVSE-simulator skill for SAP's OCPP-J simulator; simulation, not hardware. (official · ★225 · 2026-09)

### Smart Home (MCP)

- [home-assistant/core `mcp_server`](https://www.home-assistant.io/integrations/mcp_server/) - Built-in MCP server integration exposing the Assist API over Streamable HTTP. (official · ★90k · 2026-09)
- [homeassistant-ai/ha-mcp](https://github.com/homeassistant-ai/ha-mcp) - 87 tools; the most feature-rich Home Assistant MCP. (★4.7k · 2026-09)
- [tevonsb/homeassistant-mcp](https://github.com/tevonsb/homeassistant-mcp) - Home Assistant MCP with SSE real-time updates. (★576 · 2026-01)
- [voska/hass-mcp](https://github.com/voska/hass-mcp) - Token-efficient Home Assistant control and query. (★340 · 2026-08)
- [openHAB MCP add-on](https://www.openhab.org/addons/integrations/mcp/) - Built-in openHAB 5.x add-on: items, things, rules, subscriptions; [tdeckers/openhab-mcp](https://github.com/tdeckers/openhab-mcp) is the standalone option. (official)
- [Homey MCP](https://mcp.athom.com) - Athom's hosted remote MCP for Homey, launched 2025-11; no public repo. (official)
- [aqara/aqara-mcp-server](https://github.com/aqara/aqara-mcp-server) - Remote Streamable-HTTP MCP with 24 tools over devices, scenes, automations, energy and firmware. (official · ★42 · 2026-06)
- [Yeelight/yeelight-iot-mcp](https://github.com/Yeelight/yeelight-iot-mcp) - Yeelight Pro cloud: homes, rooms, devices, groups, scenes. (official · ★9 · 2026-07)
- [ecovacs-ai/ecovacs-mcp](https://github.com/ecovacs-ai/ecovacs-mcp) - Deebot vacuums: clean, dock, status; needs an open-platform key. (official · ★23 · 2025-04)
- [tuya/tuya-mcp-sdk](https://github.com/tuya/tuya-mcp-sdk) - The inverse direction: a Python / Go / C# SDK to register your own tools into Tuya's agent platform, not to control Tuya devices. (official · ★67 · 2026-04)
- [Do1e/mijia-api](https://github.com/Do1e/mijia-api) - Mi Home (米家) cloud API, CLI and MCP (`uvx mijiaAPI mcp`): QR login, device properties, actions, scenes. Xiaomi has no official server; this is the de-facto standard. (★799 · 2026-08)
- [mihai-dinculescu/tapo](https://github.com/mihai-dinculescu/tapo) - Rust / Python TP-Link Tapo library with a first-class MCP server: plugs, bulbs, hubs, cameras. (★802 · 2026-09)
- [sirkirby/unifi-mcp](https://github.com/sirkirby/unifi-mcp) - UniFi Network / Protect / Access MCP suite; the Protect server alone has 62 tools. (★820 · 2026-09)
- [shenjingnan/xiaozhi-client](https://github.com/shenjingnan/xiaozhi-client) - Aggregates many standard MCP servers into one Xiaozhi endpoint connection with a web config UI. (★338 · 2026-09)
- [c1pher-cn/ha-mcp-for-xiaozhi](https://github.com/c1pher-cn/ha-mcp-for-xiaozhi) - Home Assistant integration exposing HA as an MCP server to Xiaozhi devices. (★268 · 2026-09)
- [xinnan-tech/mcp-endpoint-server](https://github.com/xinnan-tech/mcp-endpoint-server) - The Xiaozhi MCP 接入点: a WebSocket registration hub that local MCP servers dial out to, so they cannot be spawned by a host client directly. (official · ★166 · 2026-06)
- [78/mcp-calculator](https://github.com/78/mcp-calculator) - Canonical reverse-connect MCP sample for Xiaozhi by the firmware's author. (official · ★444 · 2026-02)
- [toddpan/xiaozhi-esp32-mcp](https://github.com/toddpan/xiaozhi-esp32-mcp) - Firmware-side MCP client library for registering ESP32 tools with Xiaozhi. (★71 · 2025-10)
- [jango-blockchained/advanced-homeassistant-mcp](https://github.com/jango-blockchained/advanced-homeassistant-mcp) - 50+ Home Assistant tools over three transports. (★56 · 2026-06)
- [alexpfau/zigbee2mqtt-mcp](https://github.com/alexpfau/zigbee2mqtt-mcp) - Zigbee2MQTT administration: mesh health, OTA, pairing, binding. (★29 · 2026-09)
- [loryanstrant/ESPHome-MCP](https://github.com/loryanstrant/ESPHome-MCP) - ESPHome MCP including the 2026.6 Device Builder. (★26 · 2026-08)
- [gehaiyi/xiaomi-home-mcp](https://github.com/gehaiyi/xiaomi-home-mcp) - Standalone Xiaomi cloud MCP with automatic model mapping and speaker control. (★24 · 2026-04)
- [ykhli/mcp-light-control](https://github.com/ykhli/mcp-light-control) - Philips Hue control. (★22 · 2025-03)
- [kingpanther13/Hubitat-local-MCP-server](https://github.com/kingpanther13/Hubitat-local-MCP-server) - Groovy MCP server running on the Hubitat hub itself: 116 tools, rule engine. (★18 · 2026-09)
- [scald/tesla-mcp](https://github.com/scald/tesla-mcp) - Tesla vehicle control via the Fleet API. (★15 · 2025-03)
- [ichbinder/MCP2ZigBee2MQTT](https://github.com/ichbinder/MCP2ZigBee2MQTT) - Zigbee2MQTT device discovery and control. (★12 · 2025-10)
- [0x1abin/matter-controller-mcp](https://github.com/0x1abin/matter-controller-mcp) - Matter controller MCP: discover, commission, control. (★8 · 2025-08)
- [MatterCoder/matter-mcp-server](https://github.com/MatterCoder/matter-mcp-server) - Matter device control; the other half of the controller-side Matter coverage. (★7 · 2025-03)
- [TimCinel/homekit-mcp](https://github.com/TimCinel/homekit-mcp) - HomeKit (HAP) MCP; alternatives exist for the native macOS HomeKit framework and Homebridge. (★8 · 2026-03)
- [genm/switchbot-mcp](https://github.com/genm/switchbot-mcp) - SwitchBot device control. (★7 · 2026-09)
- [noboru-i/nature-remo-mcp-server](https://github.com/noboru-i/nature-remo-mcp-server) - Nature Remo IR hub. (★7 · 2025-04)
- [caroliny1031/midea-mcp](https://github.com/caroliny1031/midea-mcp) - Midea air conditioners, LAN-first with cloud fallback. (★5 · 2026-08)
- [veonua/smartthings-mcp](https://github.com/veonua/smartthings-mcp) - Samsung SmartThings rooms, devices and commands. (★5 · 2025-07)
- [sandraschi/dreame-mcp](https://github.com/sandraschi/dreame-mcp) - Dreame robot vacuums via the DreameHome cloud with optional local miIO. (★4 · 2026-09)
- [cacack/mcp-server-zwave-js-ui](https://github.com/cacack/mcp-server-zwave-js-ui) - Z-Wave JS UI WebSocket MCP: values, config, inclusion and exclusion. (★0 · 2026-08)
- [Buggy1111/shelly-mcp](https://github.com/Buggy1111/shelly-mcp) - Shelly Gen1–4 and BLU devices, local-first; one of the very few smart-home servers in the official MCP registry. (★0 · 2026-08)

### Lab instruments (MCP)

- [lagerdata/lager](https://github.com/lagerdata/lager) - Hardware test automation from laptop or CI with an MCP server; Rigol, Keysight, Keithley. (★7 · 2026-09)
- [JanGoebel/LabVIEW-MCP-Server-Toolkit](https://github.com/JanGoebel/LabVIEW-MCP-Server-Toolkit) - Host MCP servers from LabVIEW so VIs become tools. (★55 · 2026-07)
- [Zuehlke/labview-mcp](https://github.com/Zuehlke/labview-mcp) - Read, write and run LabVIEW VIs via NI gRPC; installs as a Claude plugin. (★29 · 2026-09)
- [erebusnz/rigol-mcp](https://github.com/erebusnz/rigol-mcp) - Rigol DS1000Z / MSO1000Z / DHO scopes over LAN or USB. (★28 · 2026-07)
- [lucasgerads/lecroy-mcp](https://github.com/lucasgerads/lecroy-mcp) - LeCroy WaveSurfer / HDO / WaveRunner / WavePro via VXI-11 or USB. (★11 · 2026-04)
- [Netlist-Studio/scope-mcp](https://github.com/Netlist-Studio/scope-mcp) - Keysight / Agilent oscilloscope over Ethernet, tested on an MSOX2024A. (★11 · 2026-02)
- [Anai-Guo/LabAgent](https://github.com/Anai-Guo/LabAgent) - 68 instrument models from 26 vendors over GPIB / USB / serial, with MCP, web and CLI. (★8 · 2026-09)
- [MagnusJohansson/siglent-sds-mcp](https://github.com/MagnusJohansson/siglent-sds-mcp) - Siglent SDS1000X-E over SCPI TCP. (★7 · 2026-02)
- [techmanual-ai/lablink-mcp](https://github.com/techmanual-ai/lablink-mcp) - Unified lab-equipment MCP over VISA / SCPI, SSH, REST and serial; tested on a Tek MSO44, Siglent SDG and Keysight PSU. (★5 · 2026-06)
- [Keysight/cyperf-mcp](https://github.com/Keysight/cyperf-mcp) - Keysight's official MCP for driving CyPerf traffic-generation agents. (official · ★1 · 2026-04)
- [daqifi/daqifi-core](https://github.com/daqifi/daqifi-core) - A .NET SDK and MCP server for DAQiFi Nyquist wireless DAQ. (official · ★5 · 2026-09)
- [KenosInc/dwf-mcp-server](https://github.com/KenosInc/dwf-mcp-server) - Digilent Analog Discovery 3 (scope, AWG, logic, PSU) via the WaveForms SDK. (★3 · 2026-08)
- [armchairdeity/mcp-server-scpi](https://github.com/armchairdeity/mcp-server-scpi) - SCPI / VISA MCP with high-level tools and a Rigol DS1054Z backend. (★3 · 2026-07)
- [JacobBeningo/devsignal](https://github.com/JacobBeningo/devsignal) - Siglent SDG signal generators CLI and MCP. (★3 · 2026-07)
- [hsoffar/saleae-logic2-mcp](https://github.com/hsoffar/saleae-logic2-mcp) - Saleae Logic 2 logic-analyzer automation. (★3 · 2026-03)
- [TECTOS-JP/lab-visa-mcp](https://github.com/TECTOS-JP/lab-visa-mcp) - PyVISA MCP with YAML-defined instrument command sets and safety ranges; sibling `lab-modbus-mcp` for chillers and temperature controllers. (★0 · 2026-08)
- [yerbymatey/opentrons-mcp](https://github.com/yerbymatey/opentrons-mcp) - Opentrons OT-2 / Flex control via the HTTP API. (★7 · 2025-06)
- [nygmeta/OpenLabAI](https://github.com/nygmeta/OpenLabAI) - MCP servers for Opentrons OT-2, Hamilton STAR, Biomek FXP and Cellario with human-approval gates. (★0 · 2026-09)
- [ghollyer/AMADEUS](https://github.com/ghollyer/AMADEUS) - Gatan / DigitalMicrograph electron microscope: stage, beam, STEM, EDS over ZMQ. (★4 · 2026-07)
- [sandraschi/sdr-mcp](https://github.com/sandraschi/sdr-mcp) - RTL-SDR: spectrum, waterfall, FM demodulation, GNU Radio. (★7 · 2026-09)

### Cameras (MCP)

- [reolink/reolink-cli](https://github.com/reolink/reolink-cli) - LAN-only Reolink CLI with a built-in MCP stdio server and SKILL.md: snapshots, PTZ, RTSP. (official · ★97 · 2026-09)
- [evalstate/mcp-webcam](https://github.com/evalstate/mcp-webcam) - Webcam capture as tool and resource. (★121 · 2025-10)
- [jakekeeys/frigate-mcp](https://github.com/jakekeeys/frigate-mcp) - Frigate NVR, 90 tools mapped one-to-one onto the HTTP API. (★11 · 2026-09)
- [sandraschi/tapo-mcp](https://github.com/sandraschi/tapo-mcp) - TP-Link Tapo cameras: PTZ, snapshot, streaming. (★2 · 2026-09)
- [ros-claw/librealsense-mcp](https://github.com/ros-claw/librealsense-mcp) - A pyrealsense2 wrapper with 26 tools: depth, point cloud, calibration, multi-camera. (★1 · 2026-07)
- [oneshot2001/onvif-pp-cli](https://github.com/oneshot2001/onvif-pp-cli) - ONVIF Profile S / T / G / M CLI and MCP, 64 commands, smoke-tested on Axis cameras. (★0 · 2026-05)

### Wireless and SDR (MCP)

- [es617/ble-mcp-server](https://github.com/es617/ble-mcp-server) - Cross-platform BLE via bleak: scan, connect, GATT read and notify. (★17 · 2026-03)
- [stass/blew](https://github.com/stass/blew) - BLE CLI and MCP for macOS, including peripheral mode. (★16 · 2026-05)
- [mr-tbot/mesh-api](https://github.com/mr-tbot/mesh-api) - Off-grid AI router for Meshtastic and MeshCore with an MCP server and OpenClaw skill. (★173 · 2026-07)
- [busse/flipperzero-mcp](https://github.com/busse/flipperzero-mcp) - Flipper Zero over USB or Wi-Fi. (★32 · 2025-12)
- [Wet-wr-Labs/claupper](https://github.com/Wet-wr-Labs/claupper) - A Flipper Zero `.fap` that acts as a one-handed BLE / USB remote to approve or deny agent actions. (★27 · 2026-05)
- [roostercoopllc/flipper-mcp](https://github.com/roostercoopllc/flipper-mcp) - MCP server running on the Flipper's ESP32-S2 Wi-Fi devboard, bridging ~30 tools (Sub-GHz, NFC, RFID, IR, BLE, GPIO) over UART. (★17 · 2026-03)
- [jonastbrg/FlipperAgent](https://github.com/jonastbrg/FlipperAgent) - Flipper MCP and agent with 67 tools, ESP32 Marauder bridge and skills. (★10 · 2026-03)
- [N-Erickson/AetherLink-SDR-MCP](https://github.com/N-Erickson/AetherLink-SDR-MCP) - RTL-SDR and HackRF: ADS-B, AIS, POCSAG, Meteor LRPT. (★23 · 2026-07)
- [thehappydinoa/hackrf-mcp](https://github.com/thehappydinoa/hackrf-mcp) - Wraps hackrf_tools: sweep, IQ capture and transmit. (★2 · 2026-08)
- [mplogas/pm3-mcp](https://github.com/mplogas/pm3-mcp) - Proxmark3 (Iceman) RFID / NFC identify and read. (★3 · 2026-06)
- [oliveres/chirpstack-mcp-server](https://github.com/oliveres/chirpstack-mcp-server) - ChirpStack v4 LoRaWAN over gRPC with live uplink debugging. (★0 · 2026-08)
- [swannman/openthread-mcp](https://github.com/swannman/openthread-mcp) - OpenThread CLI MCP and Prometheus exporter on an Arduino Nano Matter; the only Thread MCP found. (★1 · 2026-03)
- [koolsb/zwavejs-mcp](https://github.com/koolsb/zwavejs-mcp) - Z-Wave JS UI maintenance: heal, interview, diagnose, with lock-safety redaction. (★0 · 2026-06)

### USB, HID and KVM (MCP)

- [verygoodplugins/streamdeck-mcp](https://github.com/verygoodplugins/streamdeck-mcp) - Elgato Stream Deck via profile files, with a skill. (★43 · 2026-08)
- [tinqiao-oss/clawtouch-mcp](https://github.com/tinqiao-oss/clawtouch-mcp) - Exposes a real USB-HID keyboard and mouse on a Raspberry Pi Pico 2 as MCP tools. (★10 · 2026-09)
- [Oliver0804/cynthion-mcp](https://github.com/Oliver0804/cynthion-mcp) - Drives a Cynthion USB test instrument: sniff, decode and emulate USB traffic. (★5 · 2026-05)
- [bsu-tool/bsu-tool](https://github.com/bsu-tool/bsu-tool) - "Behavioral Sleuth for USB": capture, decode and analyse USB protocols on Linux, as a CLI and an MCP server. (★5 · 2026-08)
- [elgatosf/elgato-mcp-server](https://github.com/elgatosf/elgato-mcp-server) - Elgato's official MCP for automating its apps. (official · ★10 · 2026-09)
- [sunasaji/mcp-serial-hid-kvm](https://github.com/sunasaji/mcp-serial-hid-kvm) - CH9329 USB-HID plus HDMI capture: an agent drives a physical PC as a KVM, with OCR. (★3 · 2026-04)
- [yindia/qmkmcp](https://github.com/yindia/qmkmcp) - Any QMK / VIA keyboard over raw HID: lighting, keymaps, macros. (★0 · 2026-08)
- [Kevin-HYX/kvmctl](https://github.com/Kevin-HYX/kvmctl) - V4L2 plus USB-gadget HID KVM control service on an Orange Pi, CLI and MCP. (★0 · 2026-09)

### EDA / PCB / CAD (MCP)

- [mixelpixx/KiCAD-MCP-Server](https://github.com/mixelpixx/KiCAD-MCP-Server) - Edit KiCad schematics and PCBs directly from Claude. (★2.2k · 2026-09)
- [Arcadia-1/virtuoso-bridge-lite](https://github.com/Arcadia-1/virtuoso-bridge-lite) - Bridge between an LLM agent and Cadence Virtuoso for agentic analog and mixed-signal design; by a wide margin the most-starred vendor-EDA bridge. (★728 · 2026-09)
- [gokeshenzhen/TraceWeave](https://github.com/gokeshenzhen/TraceWeave) - Evidence-driven MCP for RTL simulation debugging: correlates VCS and Xcelium logs with VCD and FSDB waveforms. (★107 · 2026-09)
- [qfliuyang/hipilot](https://github.com/qfliuyang/hipilot) - VLSI physical-design copilot with MCP servers for Synopsys ICC2 and Cadence Innovus. (★7 · 2026-03)
- [lamaalrajih/kicad-mcp](https://github.com/lamaalrajih/kicad-mcp) - KiCad project management, DRC, BOM and netlist analysis. (★521 · 2025-10)
- [salitronic/eda-agent](https://github.com/salitronic/eda-agent) - 290+ tools driving a live Altium Designer session, optionally KiCad / EasyEDA Pro. (★199 · 2026-09)
- [jhacksman/OpenSCAD-MCP-Server](https://github.com/jhacksman/OpenSCAD-MCP-Server) - Text or image → parametric OpenSCAD 3D models. (★190 · 2026-09)
- [coffeenmusic/altium-mcp](https://github.com/coffeenmusic/altium-mcp) - Altium Designer PCB query and manipulation. (★158 · 2026-09)
- [Seeed-Studio/kicad-mcp-server](https://github.com/Seeed-Studio/kicad-mcp-server) - Seeed-maintained KiCad MCP: pin-level connectivity tracing and design editing. (official · ★129 · 2026-09)
- [mapleleavessssssss-wq/vivado-mcp](https://github.com/mapleleavessssssss-wq/vivado-mcp) - 30-tool Vivado MCP with GUI, Tcl and attach modes. (★127 · 2026-08)
- [circuit-synth/kicad-sch-api](https://github.com/circuit-synth/kicad-sch-api) - Python API for KiCad schematic s-expressions, with an [MCP wrapper](https://github.com/circuit-synth/mcp-kicad-sch-api). (★52 · 2025-12)
- [Netlist-Studio/kicad-mcp](https://github.com/Netlist-Studio/kicad-mcp) - KiCad 9 control over its IPC API. (★18 · 2026-02)
- [octoco-ltd/sheetsdata-mcp](https://github.com/octoco-ltd/sheetsdata-mcp) - Component datasheets: specs, pinouts and absolute-maximum ratings from PDFs. (★11 · 2026-04)
- [WangErShao/SynthAid_quartus_mcp](https://github.com/WangErShao/SynthAid_quartus_mcp) - 22-tool Intel Quartus MCP. (★3 · 2026-06)

### Edge AI and SBC (MCP)

- [Zalmotek/jetson-mcp](https://github.com/Zalmotek/jetson-mcp) - Monitor and remote-control a Jetson over SSH. (★11 · 2025-04)
- [axonixtools/PocketMCP](https://github.com/axonixtools/PocketMCP) - Turn an Android phone into an MCP server exposing its sensors. (★17 · 2026-08)
- [edgeimpulse/ei-agentic-claude](https://github.com/edgeimpulse/ei-agentic-claude) - Source of the official `@edgeimpulse/mcp-server` npm package; a Studio-workflow proof of concept, no device deploy. (official · ★3 · 2026-02)
- [marc-shade/coral-tpu-mcp](https://github.com/marc-shade/coral-tpu-mcp) - Google Coral Edge TPU inference; the only Coral entry. (★1 · 2026-02)
- [dmmdea/Hailo-8L-Analysis-Pipelines](https://github.com/dmmdea/Hailo-8L-Analysis-Pipelines) - 14-tool MCP running face detection, OCR and CLIP on a Hailo-8L. (★0 · 2026-08)
- [grammy-jiang/RaspberryPiOS-MCP](https://github.com/grammy-jiang/RaspberryPiOS-MCP) - Raspberry Pi OS: GPIO, I2C, camera. (★0 · 2026-03)

### Digital fabrication (MCP)

- [DMontgomery40/mcp-3D-printer-server](https://github.com/DMontgomery40/mcp-3D-printer-server) - OctoPrint, Klipper, Duet, Repetier, Prusa, Bambu and Creality plus STL operations. (★236 · 2026-07)
- [DMontgomery40/bambu-printer-mcp](https://github.com/DMontgomery40/bambu-printer-mcp) - Bambu local MQTT / FTPS plus BambuStudio slicing and STL operations. (★140 · 2026-07)
- [griches/bambu-mcp](https://github.com/griches/bambu-mcp) - Bambu LAN-only MQTT / FTPS fleet management. (★45 · 2026-03)
- [OctoEverywhere/mcp](https://github.com/OctoEverywhere/mcp) - Free 3D-printing MCP: live state, webcam snapshots, control. (★36 · 2025-07)
- [Charleslotto/klipper-mcp](https://github.com/Charleslotto/klipper-mcp) - Klipper via Moonraker with 100+ tools including toolchangers and an "armed" flag for dangerous operations. (★23 · 2026-08)
- [bjan/pycentauri](https://github.com/bjan/pycentauri) - Elegoo Centauri Carbon (SDCP WebSocket / MQTT) client, CLI and MCP. (★22 · 2026-07)
- [schwarztim/bambu-mcp](https://github.com/schwarztim/bambu-mcp) - Bambu local MQTT + FTPS + X.509 with camera and AMS, 25 tools. (★19 · 2026-09)
- [GLechevalier/OpenGalatea](https://github.com/GLechevalier/OpenGalatea) - Prusa via PrusaLink: Printables search, auto-slice, full job control. (★19 · 2026-04)
- [Noosbai/PrusaMCP](https://github.com/Noosbai/PrusaMCP) - PrusaSlicer MCP with 17 tools, an FDM recommendation engine and mesh analysis. (★8 · 2026-02)
- [zackpeters93/ugs-mcp](https://github.com/zackpeters93/ugs-mcp) - GRBL CNC via the Universal GCode Sender Pendant REST API, token-gated motion. (★5 · 2026-06)
- [damione1/maslow-desktop](https://github.com/damione1/maslow-desktop) - Maslow CNC (FluidNC) control panel with MCP. (★3 · 2026-07)
- [bleugreen/openpnp-mcp](https://github.com/bleugreen/openpnp-mcp) - OpenPnP; the only pick-and-place MCP found. (★0 · 2026-03)

### Audio, lighting and bio (MCP)

- [roomi-fields/osc-bridge](https://github.com/roomi-fields/osc-bridge) - OSC ↔ MIDI / SysEx bridge for hundreds of hardware synths, with a companion skill. (★7 · 2026-08)
- [NeuroSkill-com/skill](https://github.com/NeuroSkill-com/skill) - Desktop BCI app for 20+ EEG devices (Emotiv, OpenBCI, Muse) with an agent skill. (official · ★103 · 2026-09)
- [enkhbold470/bci-mcp](https://github.com/enkhbold470/bci-mcp) - Live EEG brain-state from OpenBCI / Muse via BrainFlow and LSL. (★17 · 2026-09)
- [kieranklaassen/farmbot-agent-cli-mcp](https://github.com/kieranklaassen/farmbot-agent-cli-mcp) - FarmBot hardware control via MQTT / CeleryScript RPC. (★3 · 2026-05)
- [tamengual/neptune-apex-mcp](https://github.com/tamengual/neptune-apex-mcp) - Neptune Apex aquarium controller: probes, outlets, feed, program edit. (★2 · 2026-03)
- [prmichaelsen/dmx-mcp](https://github.com/prmichaelsen/dmx-mcp) - DMX lighting via OLA and an Enttec USB adapter. (★0 · 2026-03)
- [jamiew/digitakt-digitone-mcp](https://github.com/jamiew/digitakt-digitone-mcp) - Elektron Digitakt / Digitone over MIDI, 43 tools each. (★0 · 2026-07)

### Space and ground stations (MCP)

- [alti3/stk-mcp](https://github.com/alti3/stk-mcp) - Drives Ansys STK Desktop and Engine: scenarios, satellites, access analysis. (★42 · 2026-01)
- [dsi012/mcp-server-cFS](https://github.com/dsi012/mcp-server-cFS) - Natural-language control of a NASA core Flight System software bus. (★1 · 2025-10)
- [Pranav-d33/gnuradio-mcp-server](https://github.com/Pranav-d33/gnuradio-mcp-server) - Build and run GNU Radio flowgraphs. (★1 · 2026-06)
- [harris-mohamed/satnogs-mcp](https://github.com/harris-mohamed/satnogs-mcp) - The SatNOGS satellite ground-station network. (★0 · 2026-04)

### Marine, aviation and rail (MCP)

- [VesselSense/signalk-mcp-server](https://github.com/VesselSense/signalk-mcp-server) - A SignalK server as MCP: vessel state, AIS and NMEA-derived paths. (★11 · 2025-11)
- [cyanheads/noaa-marine-mcp-server](https://github.com/cyanheads/noaa-marine-mcp-server) - NOAA tide stations and NDBC buoy hardware feeds. (★1 · 2026-08)
- [HO44-PROJECT/MrJ-JMRI-MCP](https://github.com/HO44-PROJECT/MrJ-JMRI-MCP) - JMRI for DCC model railroads: turnouts, throttles, routes. (★1 · 2026-08)
- [pipeworx-io/mcp-opensky](https://github.com/pipeworx-io/mcp-opensky) - ADS-B aircraft tracking through the OpenSky Network. (★0 · 2026-09)
- [deanjbrown/geotab-mcp](https://github.com/deanjbrown/geotab-mcp) - MyGeotab fleet telematics: device status, faults, tachograph files, fuel. (★0 · 2026-09)

### Semiconductor and science instruments (MCP)

- [vibeic/vibe-ic](https://github.com/vibeic/vibe-ic) - AI-native IC design plugin with an MCP-EDA path from intent to verified silicon. (★25 · 2026-09)
- [Jacky1-Jiang/EPICS-MCP-Server](https://github.com/Jacky1-Jiang/EPICS-MCP-Server) - EPICS process-variable read and write, the control system behind most accelerators and large telescopes. (★4 · stale since 2025-05)
- [seikaikyo/secsgem-mcp-server](https://github.com/seikaikyo/secsgem-mcp-server) - SECS/GEM semiconductor equipment control. (★1 · 2026-09)
- [BCDA-APS/bait_mcp](https://github.com/BCDA-APS/bait_mcp) - Advanced Photon Source beamline control through a Bluesky queueserver. (official · ★1 · 2026-09)
- [Oekalegon/indi-mcp](https://github.com/Oekalegon/indi-mcp) - Astrophotography mounts and cameras over INDI on a Raspberry Pi. (★0 · 2026-09)

### Pro AV, access control and signage (MCP)

- [Z-bit-Systems-LLC/OSDP-Embedded](https://github.com/Z-bit-Systems-LLC/OSDP-Embedded) - Its `osdp-mcp` exposes a virtual OSDP peripheral so an agent can act as a card reader against a real access-control panel under test — the hardware-in-the-loop pattern, in physical security. (★5 · 2026-08)
- [reowens/qsys-tools](https://github.com/reowens/qsys-tools) - QSC Q-SYS over QRC as CLI, TypeScript client and MCP server, tested against a real Core. (★3 · 2026-07)
- [DaScheife/Sklera-Digital-Signage-MCP-Server](https://github.com/DaScheife/Sklera-Digital-Signage-MCP-Server) - Sklera digital-signage screens. (★2 · 2026-06)
- [tkrisztian95/eink-mcp-server](https://github.com/tkrisztian95/eink-mcp-server) - Draw dashboards or raw pixels on a Waveshare e-ink panel. (★0 · 2026-04)

### Medical and retail devices (MCP)

- [ChristianHinge/dicom-mcp](https://github.com/ChristianHinge/dicom-mcp) - Query, read and C-MOVE against PACS archives and DICOM modalities. (★100 · 2026-09)
- [Kovinda/mirth_connect_mcp](https://github.com/Kovinda/mirth_connect_mcp) - Mirth Connect, the HL7 interface engine hospitals hang devices off. (★5 · 2026-02)
- [NyxToolsDev/dicom-hl7-mcp-server](https://github.com/NyxToolsDev/dicom-hl7-mcp-server) - Combined DICOM and HL7 interoperability. (★4 · 2026-07)
- [bhandzo/mcposprint](https://github.com/bhandzo/mcposprint) - Prints to ESC/POS receipt printers over USB. (★1 · 2026-03)
- [gian-reto/print-blocks](https://github.com/gian-reto/print-blocks) - ESC/POS thermal printing over HTTP or MCP. (★1 · 2026-09)

## Agent protocols and on-device runtimes

What sits between the model and the device besides a host-side MCP server: wire protocols, agent loops that run on the MCU or SBC, and robot / home agent frameworks.

### Protocols and transports

A2A (Agent2Agent) has no real hardware implementation seventeen months after launch: the official samples and every A2A directory contain zero physical agents, and robotics settled on MCP plus skills. The entries below are what actually exists.

- [mqtt-ai/mcp-over-mqtt](https://github.com/mqtt-ai/mcp-over-mqtt) - The MCP-over-MQTT specification: broker-side discovery, load balancing, topic ACLs; EMQX ships [TypeScript](https://github.com/emqx/mcp-typescript-sdk) and Python SDKs and broker plugins. The only alternative MCP transport with a spec, SDKs and vendor firmware. (★12 · 2026-01)
- [arm/device-connect](https://github.com/arm/device-connect) - Arm's open protocol for agents to discover, call and orchestrate devices and robots over a network. (official · ★94 · 2026-08)
- [device-context-protocol/dcp](https://github.com/device-context-protocol/dcp) - "Device Context Protocol": sub-50-byte CBOR frames, 27.6 KB flash and 0.6 KB RAM on ESP32, capability-scoped manifests, HMAC, dry-run, with a DCP ↔ MCP bridge. (★57 · 2026-05)
- [macc-n/wot-mcp](https://github.com/macc-n/wot-mcp) - W3C Web of Things Thing Description → MCP: properties become getter / setter tools, actions become tools, events become resources, over HTTP / CoAP / MQTT. (★9 · 2026-02)
- [w3c-cg/webagents](https://github.com/w3c-cg/webagents) - W3C "Autonomous Agents on the Web" community group: hypermedia multi-agent systems over WoT and Linked Data. (★47 · 2026-08)
- [agenticros/agenticros](https://github.com/agenticros/agenticros) - ROS 2 plugin for OpenClaw, Claude Code, Codex and Gemini: robots expose typed capability verbs (`drive_base`, `find_object`) whose manifest is shaped to double as an ACP / A2A agent card; A2A on the wire is a roadmap item. (★148 · 2026-09)
- [win4r/openclaw-a2a-gateway](https://github.com/win4r/openclaw-a2a-gateway) - OpenClaw plugin implementing A2A v0.3 (JSON-RPC / REST / gRPC, mDNS, agent cards); software only, but the natural front end for agenticros. (★555 · 2026-07)
- [strands-labs/robots](https://github.com/strands-labs/robots) - Natural-language control of 70+ robots via Strands Agents; robots meshed as Zenoh peers with fleet bridging over AWS IoT Core. (★157 · 2026-09)
- [agntcy/slim](https://github.com/agntcy/slim) - AGNTCY's Secure Low-Latency Interactive Messaging; with `slim-a2a-*` and A2A's own SLIM-RPC extension it is the only low-latency transport binding A2A has. (★218 · 2026-09)
- [QUSD-ai/m5stick-nanda](https://github.com/QUSD-ai/m5stick-nanda) - ESP32 firmware for an M5StickC Plus 2 serving an agent card and JSON-RPC from the device itself; it keyword-matches instead of dispatching on the protocol's methods, and was abandoned the day it appeared. Listed because it is the closest artifact to A2A-on-hardware that exists. (★0 · 2026-01)
- [r1marcus/TinyA2A](https://github.com/r1marcus/TinyA2A) - C11 agentic-intent library for STM32 and ESP-IDF with an MQTT JSON profile and a 64-byte CAN-FD frame profile. Shares the name but not the wire format with Linux Foundation A2A. (★2 · 2026-05)

### On-device agent runtimes

Agent loops that run on the microcontroller or SBC itself, with tool calling, rather than on a host.

- [espressif/esp-claw](https://github.com/espressif/esp-claw) - Agent runtime on ESP32-S3 / P4 / C5: capabilities in C, skills in Lua, bidirectional MCP, event router. (official · ★2.1k · 2026-09)
- [memovai/mimiclaw](https://github.com/memovai/mimiclaw) - C / ESP-IDF on ESP32-S3 with no OS: Anthropic tool-use ReAct loop, Telegram, local memory. The leader of the MCU-claw family. (★5.7k · 2026-08)
- [sipeed/picoclaw](https://github.com/sipeed/picoclaw) - Single Go binary under 10 MB RAM for LicheeRV-Nano / MaixCAM / Pi Zero with a full MCP and skills loop. (official · ★30k · 2026-09)
- [zeroclaw-labs/zeroclaw](https://github.com/zeroclaw-labs/zeroclaw) - Rust rewrite (3.4 MB) for Pi-class SBCs; [nullclaw](https://github.com/nullclaw/nullclaw) (Zig, 678 KB) adds Pi GPIO and STM32 / Nucleo peripheral tools. (★32.8k · 2026-09)
- [M64GitHub/WireClaw](https://github.com/M64GitHub/WireClaw) - Arduino / PlatformIO on ESP32-C3 / C6 / S3: the LLM calls `gpio_write` and `rule_create` for offline automation; Telegram, Serial, NATS; web flasher. (★188 · 2026-02)
- [jetpax/pycoclaw](https://github.com/jetpax/pycoclaw) - MicroPython on ESP32-S3 / P4 / C6 with recursive tool calling, an MCP client and GPIO / I2C / CAN tools; the agent core is not yet published. (★164 · 2026-04)
- [wireless-tag-com/EmbedClaw](https://github.com/wireless-tag-com/EmbedClaw) - C / ESP-IDF on ESP32-S3 with a JSON-schema tool registry and ReAct loop for Qwen / DeepSeek / Doubao / Kimi; the first module-vendor fork. (official · ★45 · 2026-04)
- [laurenvil/Uno-QClaw](https://github.com/laurenvil/Uno-QClaw) - A picoclaw fork on an Arduino UNO Q running a local Qwen3.5-0.8B: writes, compiles and flashes its own MCU via OpenOCD, camera, I2C scan, fully offline. (★19 · 2026-06)
- [hrwtech/openclaw-esp32](https://github.com/hrwtech/openclaw-esp32) - OpenClaw's agent loop ported to ESP32 boards; OpenClaw itself bundles no hardware skills. (★10 · 2026-02)
- [espressif/esp-brookesia](https://github.com/espressif/esp-brookesia) - AIoT HMI framework with an agent manager exposing Function Calling and MCP adapters for Coze, OpenAI and Xiaozhi. (official · ★788 · 2026-09)
- [tuya/TuyaOpen](https://github.com/tuya/TuyaOpen) - C SDK for T2 / T3 / T5AI and ESP32 with an on-device inference engine; the agent brain stays in Tuya's cloud Agent Hub. (official · ★1.8k · 2026-09)
- [XiaoMi/xiaomi-miloco](https://github.com/XiaoMi/xiaomi-miloco) - OpenClaw plugin with MiMo: home-camera perception drives Mi Home device control; needs a 4 GB+ host, not an MCU. (official · ★3.3k · 2026-09)
- [NVIDIA-AI-IOT/jetson-ai-lab](https://github.com/NVIDIA-AI-IOT/jetson-ai-lab) - The official OpenClaw-on-Jetson path: Ollama on Orin Nano, vLLM on AGX / Thor. (official · ★207 · 2026-09)
- [HeyWillow/willow](https://github.com/HeyWillow/willow) - ESP32-S3 voice-device firmware that streams to a server which executes the tools; like esp-ai and ElatoAI, no on-device agent loop. (★3.1k · 2026-09)

### Robot and embodied agent frameworks

- [dimensionalOS/dimos](https://github.com/dimensionalOS/dimos) - Agentic OS for physical space: command humanoids, Unitree quadrupeds, xArm and MAVLink drones in natural language. (★4.5k · 2026-09)
- [ros-claw/rosclaw](https://github.com/ros-claw/rosclaw) - "Trustworthy physical execution runtime": fail-closed policy, receipts, MCP tool discovery, safety envelope, ROS 2; alpha, UR5e sim-verified. (★197 · 2026-09)
- [Grigorij-Dudnik/RoboCrew](https://github.com/Grigorij-Dudnik/RoboCrew) - `pip install robocrew`: an LLM agent with movement tools, VLA policies and sensor scans; XLeRobot demo. (★139 · 2026-08)
- [Hugging Face LeRobot](https://github.com/huggingface/lerobot) - End-to-end robot learning: datasets, ACT / Diffusion / VLA policies, drivers for SO-100 / 101, Koch and LeKiwi; ships an agent-facing `AGENT_GUIDE.md`. (★27.5k · 2026-09)
- [isaac-sim/IsaacLab](https://github.com/isaac-sim/IsaacLab) - Unified robot-learning framework on Isaac Sim: RL, imitation, sim-to-real. (★8.1k · 2026-09)
- [NVIDIA/Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T) - GR00T foundation model for generalist humanoids with fine-tuning and inference stack and an `AGENTS.md`. (★8.1k · 2026-08)
- [openvla/openvla](https://github.com/openvla/openvla) - 7B open vision-language-action model for manipulation; the reference VLA, now frozen. (★7k · 2025-03)
- [nasa-jpl/rosa](https://github.com/nasa-jpl/rosa) - LangChain agent that inspects, diagnoses and operates ROS 1 / 2 robots by natural language. (★1.6k · 2026-03)
- [FlagOpen/RoboOS](https://github.com/FlagOpen/RoboOS) - BAAI's brain–cerebellum embodied OS: RoboBrain MLLM, skill library and shared memory for multi-robot. (official · ★622 · 2025-12)
- [automatika-robotics/embodied-agents](https://github.com/automatika-robotics/embodied-agents) - ROS 2-native framework for interactive physical agents with LLM / VLM components. (★67 · 2026-09)

### Smart-home and device platforms

- [Home Assistant LLM API](https://developers.home-assistant.io/docs/core/llm/) - The official Assist LLM API: integrations register tools any conversation agent can call. (official)
- [acon96/home-llm](https://github.com/acon96/home-llm) - Home Assistant integration plus fine-tuned local models for device control. (★1.4k · 2026-09)
- [arm/mcp](https://github.com/arm/mcp) - Arm's official MCP: docs search, migration analysis, assembly performance analysis. Nordic, Microchip, Silicon Labs, TI and ADI have shipped similar docs-only vendor MCPs. (official · ★91 · 2026-09)

## Verification infrastructure

What you need to run a hardware skill's `evals/` without owning the board — and how far each option gets you.

### Simulators and emulators

- [wokwi/wokwi-cli](https://github.com/wokwi/wokwi-cli) - ESP32 family, AVR, RP2040, nRF52, partial STM32, plus sensors and displays. YAML scenarios assert on serial text and set pins; GitHub Action; free CI token for open source. The simulator core is hosted and closed. Our `L1 (wokwi)` backend. (★66 · 2026-06)
- [renode/renode](https://github.com/renode/renode) - Cortex-M / A / R, RISC-V, Xtensa, whole boards and multi-node networks; `.resc` scripts, Robot Framework harness, Zephyr twister integration, deterministic. MIT. The assertion layer already exists — `renode-test` drives Robot Framework with keywords like `Wait For Line On Uart` — but nothing wraps a live session for an agent. Our `L1 (renode)` backend. (★2.9k · 2026-09)
- [qemu/qemu](https://github.com/qemu/qemu) - ARM `mps2` and friends, RISC-V, x86; [Espressif's fork](https://github.com/espressif/qemu) adds Xtensa / ESP32. QMP JSON API and GDB stub. Used for FreeRTOS fuzz-and-patch loops in the literature. (★13.7k · 2026-09)
- [Zephyr native_sim](https://docs.zephyrproject.org/latest/boards/native/native_sim/doc/index.html) - Build any Zephyr app as a host Linux binary with emulated I2C / SPI / GPIO and BabbleSim BLE; `twister -p native_sim`. The cheapest L1 for Zephyr skills. (official)
- [gazebosim/gz-sim](https://github.com/gazebosim/gz-sim) - Robot worlds with ROS 2 bridge and sensors; `gz sim -s -r world.sdf` runs headless. (★1.5k · 2026-09)
- [google-deepmind/mujoco](https://github.com/google-deepmind/mujoco) - Articulated-body physics with Python bindings and MJX GPU version; backbone of LIBERO and most VLA evals. (★15.1k · 2026-09)
- [isaac-sim/IsaacSim](https://github.com/isaac-sim/IsaacSim) - Photoreal robot sim; `--headless` and Python standalone scripts; source public since 5.0, RTX GPU required. Nightly rather than per-PR material. (★4.1k · 2026-09)
- [cyberbotics/webots](https://github.com/cyberbotics/webots) - Robots with ROS 2 bridge; `webots --batch --no-rendering`. (★4.6k · 2026-09)
- [mani-skill/ManiSkill](https://github.com/mani-skill/ManiSkill) - GPU-parallel manipulation sim on SAPIEN with offscreen Vulkan; doubles as a benchmark. (★3.3k · 2026-08)
- [pymodbus-dev/pymodbus](https://github.com/pymodbus-dev/pymodbus) - `pymodbus.simulator` serves a Modbus TCP / RTU device from a JSON register definition, with an HTTP control API. Our `L1 (modbus-sim)` backend. (★2.8k · 2026-09)
- [open62541/open62541](https://github.com/open62541/open62541) - OPC UA server / client; example servers make a usable PLC stand-in. (★3.2k · 2026-09)
- [Home Assistant demo mode](https://www.home-assistant.io/integrations/demo/) - `hass --demo-mode` creates fake lights, climate and sensors behind the real REST / WebSocket API. Our `L1 (ha-demo)` backend. (official)
- [micropython/micropython unix port](https://github.com/micropython/micropython/tree/master/ports/unix) - MicroPython VM on the host; logic-level checks only, no peripherals. (★22k · 2026-09)
- [ARM-software/AVH](https://github.com/ARM-software/AVH) - Arm Virtual Hardware: Cortex-M FVPs (Corstone-300 / 310 / 315) with GitHub Actions examples; free for open source and evaluation. (official · ★54 · 2026-09)

Not viable for CI, listed so nobody re-checks: Tinkercad Circuits (no API), SimulIDE (GUI only), Proteus VSM (commercial, GUI-centric), Simulavr (dormant since 2023).

### Virtual hardware and device farms

- [veecle/chiplab](https://github.com/veecle/chiplab) - Hosted virtual STM32 and Nordic Cortex-M boards exposed only through MCP: upload an ELF, read UART. Built specifically for coding agents. (★16 · 2026-08)
- [eust-w/agentic-embedded-lab](https://github.com/eust-w/agentic-embedded-lab) - Agent-native embedded lab with pluggable simulation backends and evidence-driven validation; the closest thing to a Renode-backed harness. (★33 · 2026-09)
- [EliasOenal/term-cli](https://github.com/EliasOenal/term-cli) - Interactive terminals for agents, built for the prompts you cannot auto-approve: SSH with MFA, GRUB and U-Boot consoles, debconf. (★101 · 2026-08)
- [jumpstarter-dev/jumpstarter](https://github.com/jumpstarter-dev/jumpstarter) - Red Hat-backed HIL framework for real or virtual targets, local or remote, Kubernetes-native, explicitly designed for "human, automated or agentic" drivers; power, serial and flashing drivers. The strongest fit for an L2 device farm. (★219 · 2026-09)
- [labgrid-project/labgrid](https://github.com/labgrid-project/labgrid) - Pengutronix board-control library (power, serial, USB, network boot) with pytest integration. (★527 · 2026-09)
- [kernelci/kernelci-core](https://github.com/kernelci/kernelci-core) - Community hardware labs with an open API; labs donated by Collabora, BayLibre and others. (★120 · 2026-09)
- [Linaro LAVA](https://gitlab.com/lava/lava) - Board-farm scheduler used by KernelCI and Linaro labs; self-hostable. (★82 · 2026-09)
- [Zephyr twister device testing](https://docs.zephyrproject.org/latest/develop/test/twister.html) - `twister --device-testing --hardware-map` runs the test suite on attached boards; [golioth/zephyr_twister_hil_testing](https://github.com/golioth/zephyr_twister_hil_testing) shows it on a GitHub self-hosted runner. (official)
- [Wokwi CI](https://docs.wokwi.com/wokwi-ci/getting-started) - Hosted simulation inside GitHub Actions; free token for open-source projects. (official)
- [OpenHiL](https://openhil.github.io/) - Community hub for open hardware-in-the-loop tooling.

## Benchmarks and evals

Only the first two have published results on physical MCUs; everything else is compile-only or sim-only.

- [iot-agent/iot-skillsbench](https://github.com/iot-agent/iot-skillsbench) - 42 HIL tasks on ATmega2560 / Arduino, ESP32-S3 / ESP-IDF and nRF52840 / Zephyr across 23 peripherals and 3 difficulty levels; compares no-skills vs LLM-generated vs expert-written skills on real boards. Its 30 expert skills are single-file `.md` with frontmatter, trivially convertible to SKILL.md. Paper: [arXiv 2603.19583](https://arxiv.org/abs/2603.19583). (★41 · 2026-07)
- [ubicomplab/embedded-arena](https://github.com/ubicomplab/embedded-arena) - HIL arena: the agent edits model and firmware, the harness compiles, flashes and scores deployability, current, energy and temperature. Frontier models score 0% without hardware feedback and succeed within three iterations with it. Paper: [arXiv 2606.16190](https://arxiv.org/abs/2606.16190). (★11 · 2026-07)
- [cezman/ironharness](https://github.com/cezman/ironharness) - A pass@k benchmark for firmware agents on Wokwi, Renode or real hardware behind a sandboxed MCP I/O harness. Very early. (★2 · 2026-09)
- [EmbedBench / EmbedAgent](https://arxiv.org/abs/2506.11003) - 126 cases over 9 components on Uno / ESP32 / Pico with Programmer, Architect and Integrator roles; no public repo.
- [EmbedGenius](https://arxiv.org/abs/2412.09058) - Embedded IoT software generation with hardware-aware retrieval.
- [Closed-loop evaluation of LLM agents for embedded software development](https://www.sciencedirect.com/science/article/pii/S1383762126002559) - Five embedded-control tasks under four feedback regimes: one-shot, self-verification, CI red/green, oracle.
- [NVlabs/verilog-eval](https://github.com/NVlabs/verilog-eval) - Verilog completion and spec-to-RTL, iverilog-checked pass@k. (★469 · 2025-07)
- [hkust-zhiyao/RTLLM](https://github.com/hkust-zhiyao/RTLLM) - Natural language → RTL: syntax, functionality, PPA. (★227 · 2026-08)
- [HardSecBench](https://arxiv.org/abs/2601.13864) - Security awareness of LLM-generated RTL and C firmware.
- [EmbodiedBench/EmbodiedBench](https://github.com/EmbodiedBench/EmbodiedBench) - 1,128 tasks over ALFRED, Habitat, navigation and manipulation for multimodal embodied agents. (★341 · 2026-05)
- [StanfordVL/BEHAVIOR-1K](https://github.com/StanfordVL/BEHAVIOR-1K) - 1,000 household activities in OmniGibson. (★1.7k · 2026-09)
- [Lifelong-Robot-Learning/LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO) - 130 lifelong-manipulation tasks; the de facto VLA eval. (★2.3k · 2025-03)
- [stepjam/RLBench](https://github.com/stepjam/RLBench) - 100 manipulation tasks in CoppeliaSim. (★1.8k · 2025-01)
- [holi-lab/SimuHome](https://github.com/holi-lab/SimuHome) - Matter-grounded, time-accelerated smart-home simulator with 600 episodes including scheduling and implicit intent. ICLR 2026 oral. (★34 · 2026-04)
- [SMH-Bench](https://arxiv.org/abs/2606.01912) - 1,100 smart-home tasks in homes of up to 135 devices; code not yet released.

## Papers and articles

- [Skilled AI Agents for Embedded and IoT Systems Development](https://arxiv.org/abs/2603.19583) - Introduces IoT-SkillsBench; expert-written skills reach near-perfect HIL success where bare models fail. ACM AIAS 2026.
- [Every hardware MCP server I could find, and what each one actually does](https://veecle.ai/blog/hardware-mcp-servers-reviewed) - Veecle, 2026-08. 42 servers in six tiers; only three can run firmware without local hardware.
- [The chip vendors showed up: hardware MCP servers, six months later](https://veecle.ai/blog/hardware-mcp-servers-2026) - Veecle, 2026-08. Seven vendors' official MCPs; none offer simulated execution.
- [LLMs write good firmware. They can't prove it.](https://veecle.ai/blog/llms-write-good-firmware-cant-prove-it) - The case for verification infrastructure over better prompts — the argument this list's ladder is built on.
- [What the LLM-for-embedded benchmarks actually measure](https://veecle.ai/blog/what-llm-embedded-benchmarks-measure) - Critical read of EmbedBench and IoT-SkillsBench metrics.
- [Device Context Protocol: an agent protocol for constrained devices](https://arxiv.org/abs/2605.26159) - The paper behind DCP: why MCP is too heavy for MCUs and what a 27 KB alternative looks like.
- [LAP: An Agent-to-Instrument Protocol for Autonomous Science](https://arxiv.org/abs/2606.03755) - Names the agent-to-instrument edge that neither MCP nor A2A models, and proposes instrument cards, exclusive reservations, safety-fence handshakes and measurements typed with uncertainty. The strongest argument for why agent-to-agent protocols do not reach hardware.
- [Robot Context Protocol](https://arxiv.org/abs/2506.11650) - A middleware-agnostic robot-control protocol that places A2A in an adapter on the client edge rather than on the control path.
- [Agentic IoT: a survey](https://arxiv.org/abs/2607.04219) - Survey of LLM agents meeting IoT devices, protocols and edge constraints.
- [Securing LLM-Generated Embedded Firmware through AI Agent-Driven Validation and Patching](https://arxiv.org/abs/2509.09970) - FreeRTOS on QEMU with a fuzzing, static-analysis and agent-patching loop.
- [Embedded Arena: Iterative Optimization via Hardware Feedback](https://arxiv.org/abs/2606.16190) - Hardware feedback flips 0% to success in three iterations.
- [SemaPLC: an agentic IDE for PLC programming](https://arxiv.org/abs/2608.18565) - Midea's spec-to-PLC agent pipeline with review skills.
- [Toward a Modular Architecture for Embedded AI Agent Systems at the Edge](https://arxiv.org/abs/2606.02862) - On-device agent runtime design; compare with esp-claw and the claw family.
- [Coscientist](https://github.com/gomesgroup/coscientist) - GPT-4 agent driving an Opentrons liquid handler and Emerald Cloud Lab. Nature 2023. (★211 · 2025-08)
- [Autonomous Chemistry and Materials Innovation Driven by Scientific Agents](https://pubs.acs.org/doi/10.1021/jacsau.6c00213) - Survey of LLM-run self-driving labs. JACS Au 2026.

## Agent-ready docs

Vendor documentation that serves `llms.txt` — verified live and plain-text on 2026-09-16, with HTML pages served under that name rejected. Useful as `references/` for a skill.

- [Arduino](https://docs.arduino.cc/llms.txt) - 181 KB index plus `llms-full.txt`; the only MCU-vendor llms.txt found.
- [NVIDIA Jetson](https://docs.nvidia.com/jetson/llms.txt) - Also `docs.omniverse.nvidia.com/llms.txt`.
- [Silicon Labs](https://docs.silabs.com/llms.txt) - 36 MB full dump covering EFR32, BLE, Zigbee and Matter.
- [Renesas](https://www.renesas.com/llms.txt) - Corporate and product index, 6.7 KB.
- [Nordic nRF Cloud](https://docs.nrfcloud.com/llms.txt) - 50 KB; Nordic's device docs sit behind a challenge page, this one does not.
- [DFRobot](https://wiki.dfrobot.com/llms.txt) - 2.2 MB of product wiki, tutorials, manuals and datasheets — the largest hardware llms.txt found.
- [Radxa](https://docs.radxa.com/llms.txt) - Product and technical documentation index.
- [Edge Impulse](https://docs.edgeimpulse.com/llms.txt) - TinyML pipeline docs.
- [Particle](https://docs.particle.io/llms.txt) - Device OS and cloud.
- [Memfault](https://docs.memfault.com/llms.txt) - Observability SDK.
- [Blues Notecard](https://dev.blues.io/llms.txt) - Cellular / LoRa Notecard API.
- [balena](https://docs.balena.io/llms.txt) - Fleet management for Linux SBCs.
- [Viam](https://docs.viam.com/llms.txt) - Robotics platform.
- [Foxglove](https://docs.foxglove.dev/llms.txt) - Robotics observability.
- [Luxonis](https://docs.luxonis.com/llms.txt) - OAK cameras.
- [LeRobot](https://huggingface.co/docs/lerobot/llms.txt) - Hugging Face robot learning.
- [Adafruit Learn](https://learn.adafruit.com/llms.txt) - Guides for Adafruit boards and breakouts.
- [Tuya](https://developer.tuya.com/llms.txt) - IoT platform.
- [Flux.ai](https://docs.flux.ai/llms.txt) - Browser EDA.

Checked and absent (404 or HTML): Zephyr, Espressif, Nordic, ST, PlatformIO, KiCad, ROS docs, Golioth, Home Assistant, ESPHome, MicroPython, CircuitPython, Raspberry Pi, Seeed wiki, Isaac Sim / Lab, Embassy, BeagleBoard, ThingsBoard. Zephyr ships an `AGENTS.md`, a `CLAUDE.md` and a `copilot-instructions.md` instead; nRF Connect SDK has none of the three at HEAD.

## Gaps

What does not exist yet is tracked in **`GAPS.md`**, with the evidence behind each claim, the closest
artifact that does exist so the claim stays falsifiable, and five scoped first contributions complete with the
eval assertions to aim at. Headlines:

**A2A never reached hardware.** Seventeen months after launch, no repository implements the Linux Foundation
A2A spec end to end against a physical device. The 3,618-line specification contains zero occurrences of
*robot*, *actuator*, *sensor* or *embedded*, and none of its 1,721 issues asks for device control. This looks
like a design consequence rather than an oversight: a device is exclusively owned, physically irreversible and
deadline-bound, while A2A models a retryable conversation between opaque peers. Every device-side protocol
effort since — MCP-over-MQTT, Arm Device Connect, DCP — attached itself to MCP instead.

**Vendors have barely shown up.** Three silicon vendors have published a host-side skill: Arm, Renesas and
Texas Instruments. STMicroelectronics has 786 public repos and none; Infineon has 2,301; NXP 221; Raspberry Pi
115 with the Pico SDK bare. `espressif/skills` is an official repo whose README tells you to install it and
whose tree is `README.md` plus `skills/.gitkeep`, created and abandoned within three hours on 2026-04-24. Seven
vendors ship an MCP server and not one of them can execute anything in simulation.

**Renode has no agent-facing interface.** The emulator is not the limitation: it is deterministic, runs
headless, and already ships an assertion harness in `renode-test` and Robot Framework. What is missing is
something that holds a live session for an agent, so that interactive firmware debugging and the L1 runner
share one integration rather than each re-deriving a brittle shell recipe. Still the single
highest-leverage thing missing from this list.

**Hardware-in-the-loop remains the least-covered pattern** — flash, run, read serial, iterate — even though it
is the one with published evidence behind it: frontier models score 0% deployment success without hardware
feedback and beat human experts within seven iterations with it.

Also empty, each verified rather than assumed: Wi-Fi provisioning, Raspberry Pi 5 Linux, device tree and
U-Boot, Thread and device-side Matter, non-offensive NFC, Lattice FPGA tooling, VLA policies as agent tools,
Boston Dynamics Spot, and generic USB control (USB *analysis* is now covered).

## Related lists

- [beriberikix/awesome-mcp-hardware](https://github.com/beriberikix/awesome-mcp-hardware) - Upstream list of hardware MCP servers; this list's MCP section started from it.
- [TensorBlock/awesome-mcp-servers — hardware & IoT](https://github.com/TensorBlock/awesome-mcp-servers/blob/main/docs/hardware--iot.md) - Hardware category of a general MCP list.
- [fouad1233/amazing-robotics-skills](https://github.com/fouad1233/amazing-robotics-skills) - Licence-aware index of 1,039 NVIDIA-ecosystem skills across 35 repos.
- [ros-claw](https://github.com/ros-claw) - Org holding ~35 robot and sensor MCPs plus a skill catalog format (SKILL.md + skill.yaml + behavior tree).
- [heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills) - General Agent Skills directory.
- [skillmatic-ai/awesome-agent-skills](https://github.com/skillmatic-ai/awesome-agent-skills) - General Agent Skills directory.
- [skills.sh](https://skills.sh) - Skill registry with install counts; the numbers quoted above come from here.
- [ClawHub](https://www.clawhub.ai) - OpenClaw's skill registry; hosts hardware skills with no GitHub source (esp32, arduino, raspberry, bambu-cli, meshtastic) whose install counts are quoted above.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Short version: one line per entry in the right category, run `python scripts/l0_check.py readme README.md`, and if you are adding a skill you maintain, copy [`template/evals/`](template/evals/) into it and file an [L2 attestation](.github/ISSUE_TEMPLATE/attestation.yml) once you have run it on a board.
