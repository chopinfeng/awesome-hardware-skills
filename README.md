# Awesome Hardware Skills

> Skills, MCP servers, simulators, benchmarks and CI infrastructure that let AI coding agents (Claude Code, Codex, Cursor, OpenClaw, …) build, flash, debug and control physical hardware — with a verification ladder so you can tell which ones actually work on a board.

Most "awesome MCP" lists tell you a hardware server *exists*. This list also tracks whether anyone has proven it works: every skill entry can carry a badge from a three-level ladder (static checks → simulator run → real-hardware attestation) plus a with-skill / without-skill delta. See [How entries are verified](#how-entries-are-verified).

Snapshot: 2026-09-15. Stars and last-push dates are from that day. `stale` marks projects with no push in 12+ months.

## Contents

- [How entries are verified](#how-entries-are-verified)
- [Skills (SKILL.md form)](#skills)
  - [Official vendor skills](#official-vendor-skills)
  - [MCU / Embedded](#mcu--embedded)
  - [RTOS (Zephyr / FreeRTOS / NCS)](#rtos)
  - [Robotics (ROS / Isaac / drones)](#robotics)
  - [EDA / PCB](#eda--pcb)
  - [FPGA / HDL](#fpga--hdl)
  - [SBC / Linux (Jetson / Raspberry Pi)](#sbc--linux)
  - [Wireless (BLE / Zigbee / Matter)](#wireless)
  - [Industrial / IoT / 3D printing](#industrial--iot--3d-printing)
  - [Smart Home](#smart-home)
- [MCP servers and bridges](#mcp-servers-and-bridges)
- [Agent frameworks and on-device runtimes](#agent-frameworks-and-on-device-runtimes)
- [Verification infrastructure](#verification-infrastructure)
  - [Simulators and emulators](#simulators-and-emulators)
  - [Virtual hardware and device farms](#virtual-hardware-and-device-farms)
- [Benchmarks and evals](#benchmarks-and-evals)
- [Papers and articles](#papers-and-articles)
- [Agent-ready docs (llms.txt)](#agent-ready-docs)
- [Gaps — what does not exist yet](#gaps)
- [Related lists](#related-lists)
- [Contributing](#contributing)

## How entries are verified

Hardware skills are hard to validate in CI because the CI runner does not own the board. So this list uses a ladder instead of a single green check:

| Badge | Meaning |
|---|---|
| `L0` | Static checks pass: SKILL.md frontmatter, description specific enough to trigger, no secrets, links resolve, `evals/` package well-formed. |
| `L1 (wokwi)` | Every task in the skill's `evals/` passes in the named simulator, run by this repo's CI. |
| `L2 ×3` | Three independent people ran the tasks on real hardware and filed an [attestation](.github/ISSUE_TEMPLATE/attestation.yml) with an unedited transcript. |
| `ΔPass +42%` | With-skill minus without-skill task pass rate on the same model — proves the skill carries knowledge the model did not already have. |
| `stale` | No L1 re-run in 90 days, or no upstream push in 12 months. |

Tasks assert on physical side effects a script can observe (serial output, GPIO edges, bus captures, ROS topics, HTTP probes), never on "the code looks right". The eval package format lives in [`template/evals/`](template/evals/); the static checker is [`scripts/l0_check.py`](scripts/l0_check.py). Details in [CONTRIBUTING.md](CONTRIBUTING.md).

This is the launch snapshot: no entry has an `evals/` package yet, so no badges are shown. The first targets for L1 are the ESP32, Zephyr and Arduino skills below, because Wokwi, Renode and `native_sim` can run them without a board.

## Skills

Entries in the [Agent Skills](https://agentskills.io) format: a folder with a `SKILL.md` (frontmatter `name` + `description`) and optional `references/` and `scripts/`. Installable into Claude Code, Codex, Cursor and others. `coll` = a collection of several skills; a path after the repo name points at one skill inside a monorepo.

### Official vendor skills

First-party skills published by the company that makes the hardware or the SDK. Rare, so listed together.

- [NVIDIA/skills](https://github.com/nvidia/skills) - 330+ skills mirrored from NVIDIA product repos; the hardware clusters are `jetson-*` (BSP customization, pinmux, flashing, memory audit, LLM serving on-device), `hsb-*` (Holoscan Sensor Bridge FPGA flashing), `i4h-*` (Isaac for Healthcare robot data collection and RL) and `physical-ai-*`. Jetson skills are the most-installed hardware skills on skills.sh. (official · coll · ★3.3k · 2026-09)
- [isaac-sim/IsaacSim `.claude/skills/`](https://github.com/isaac-sim/IsaacSim/tree/main/.claude/skills) - 40 skills for Isaac Sim: headless deployment, ROS 2 bridge, URDF/MJCF → USD, manipulation IK, navigation primitives, occupancy maps, data collection. (official · coll · ★4.1k · 2026-09)
- [PX4/PX4-Autopilot `.agents/skills/build-px4`](https://github.com/PX4/PX4-Autopilot/tree/main/.agents/skills/build-px4) - Build PX4 board firmware inside the px4-dev container, worktree-aware; no flashing. (official · ★12.6k · 2026-09)
- [project-chip/connectedhomeip `.agents/skills/`](https://github.com/project-chip/connectedhomeip/tree/master/.agents/skills) - 14 Matter SDK contributor skills: ZAP cluster generation, code-driven cluster TDD, chip-tool testing, binary size comparison. (official · coll · ★8.9k · 2026-09)
- [home-assistant/core `.claude/skills/`](https://github.com/home-assistant/core/tree/dev/.claude/skills) - `ha-integration-knowledge`, `ha-quality-scale-verify`, `ha-review` for writing Home Assistant integrations. (official · coll · ★90k · 2026-09)
- [anthropics/claude-plugins-official `cwc-makers`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/cwc-makers) - `m5-onboard` detects an M5Stack Cardputer/Core/CoreS3 on USB, flashes UIFlow 2.0 and a MicroPython bundle; `cardputer-buddy` iterates on apps over serial with one-shot REPL. (official · coll · ★36k · 2026-09)
- [SmartThingsCommunity/SmartThingsEdgeDrivers `.agents/skills/`](https://github.com/SmartThingsCommunity/SmartThingsEdgeDrivers/tree/main/.agents/skills) - Samsung's skills for writing Zigbee / Z-Wave / Matter Lua edge drivers: profiles, libraries, test workflow. (official · coll · ★346 · 2026-09)
- [openvinotoolkit/physicalai](https://github.com/openvinotoolkit/physicalai/tree/main/skills) - Intel's runtime for running VLA policies on robots: add a robot integration, add a camera backend, configure the inference pipeline. (official · coll · ★27 · 2026-09)
- [Seeed-Studio/ai-skills](https://github.com/Seeed-Studio/ai-skills) - `schematic-analyzer` traces KiCad and OrCAD/Allegro schematics; `ee-datasheet-master` extracts pinouts, I2C addresses and register maps from PDFs; SG200x/CV181x media and ONNX → cvimodel skills. (official · coll · ★25 · 2026-09)
- [adafruit/LLM-Recipes](https://github.com/adafruit/LLM-Recipes/tree/main/circuitpython) - Run code on an attached CircuitPython board, write and run hardware tests, and validate an I2C driver by comparing Arduino vs CircuitPython bus traffic. (official · coll · ★3 · 2026-06)
- [edgeimpulse/agent-tools](https://github.com/edgeimpulse/agent-tools/tree/main/skills) - Integrate exported Edge Impulse model libraries into Arduino, Zephyr, STM32 and Raspberry Pi firmware, plus Arduino UNO Q app-lab builds. (official · coll · ★3 · 2026-09)
- [wirenboard/wb-ai-skills](https://github.com/wirenboard/wb-ai-skills) - Wiren Board PLC vendor skills: talk to controllers over MQTT and Modbus, write wb-rules, manage Zigbee and serial devices, root-cause analysis. (official · coll · ★3 · 2026-09)
- [espressif/skills](https://github.com/espressif/skills) - Espressif's official skills repo, created 2026-04 and installable via `npx skills add espressif/skills` — but it contains no SKILL.md yet. Listed so you can watch it. (official · placeholder · ★2 · 2026-04)

### MCU / Embedded

- [Jeffallan/claude-skills `embedded-systems`](https://github.com/Jeffallan/claude-skills/tree/main/skills/embedded-systems) - STM32 / ESP32 / FreeRTOS / bare-metal workflow: peripherals, ISRs, DMA, power; the most-installed generic embedded skill (~6k installs on skills.sh). (★11.5k · 2026-08)
- [FastLED/FastLED `.claude/skills/`](https://github.com/FastLED/FastLED/tree/master/.claude/skills) - Project-internal but real: ESP-IDF v5 RMT5 driver expert, ESP32 log triage and test-plan skills, Xtensa and RISC-V assembly code review, timing analysis. (coll · ★7.5k · 2026-09)
- [hathach/tinyusb `.claude/skills/`](https://github.com/hathach/tinyusb/tree/master/.claude/skills) - `hil` drives the TinyUSB hardware-in-the-loop rig; `target-debug`, `rtt`, `etm-trace`, `usb-sniffer`, `usbmon` interpret on-target USB stack behaviour. The best example of an agent skill wired to a real HIL bench. (coll · ★7.1k · 2026-09)
- [LeoKemp223/embed-ai-tool](https://github.com/LeoKemp223/embed-ai-tool) - About 25 skills with bundled scripts covering the whole MCU toolchain: build with Keil / IAR / CMake / ESP-IDF / PlatformIO, flash with OpenOCD / J-Link / idf.py, debug with GDB, plus CAN, Modbus, VISA and RTOS debugging. Chinese descriptions. (coll · ★919 · 2026-08)
- [zhinkgit/embeddedskills](https://github.com/zhinkgit/embeddedskills) - Probe detection, flashing, GDB server, telnet debug, semihosting and ITM capture across OpenOCD, J-Link, probe-rs, Keil and EIDE. Chinese. (coll · ★664 · 2026-09)
- [Mindrally/skills `embedded-stm32`](https://github.com/Mindrally/skills/tree/main/embedded-stm32) - STM32 HAL skill derived from Cursor rules: CubeMX, DMA, SWD conventions. (★259 · 2026-09)
- [mohitmishra786/low-level-dev-skills](https://github.com/mohitmishra786/low-level-dev-skills) - Bare-metal fundamentals with datasheet-reading guidance: STM32 bare-metal, GPIO, UART, I2C/SPI bus drivers, DMA, bootloaders, OpenOCD/JTAG, embedded Rust, QEMU simulation, FreeRTOS, Zephyr. (coll · ★210 · 2026-06)
- [SensorsIot/Embedded-AI-Harness `esp-idf-handling`](https://github.com/SensorsIot/Embedded-AI-Harness/tree/main/.claude/skills/esp-idf-handling) - Closed-loop ESP-IDF: build, flash over local USB or an RFC2217 remote testbench, monitor, OTA, crash recovery. One of the few skills that closes the flash → observe → iterate loop. (★175 · 2026-08)
- [magnus919/agent-skills `esp32-development`](https://github.com/magnus919/agent-skills/tree/main/esp32-development) - Identify the ESP32 board, choose between ESP-IDF, Arduino, MicroPython, CircuitPython, ESPHome, Zephyr, Rust and NuttX, wire, flash, recover. (★82 · 2026-09)
- [kukucaiCndy/embedded_ai_skills](https://github.com/kukucaiCndy/embedded_ai_skills) - Setup / project-init / debug triplets for ESP32 (IDF and Arduino), STM32 and Nordic NCS, plus ZMK keyboard and EasyEDA drawing skills. (coll · ★54 · 2026-07)
- [ezrover/ESP32-AI-Agent-Skill](https://github.com/ezrover/ESP32-AI-Agent-Skill/tree/main/skills/esp32) - Chip selection (S3 / C3 / C6), PSRAM and MMU notes, the GPIO12 strapping-pin trap, ESP-IDF and PlatformIO setup, LVGL and Waveshare display references. (★37 · 2026-08)
- [easyzoom/aix-skills](https://github.com/easyzoom/aix-skills) - Integration-focused MCU skills: ESP-IDF, STM32 HAL/LL, FreeRTOS kernel debug, FreeRTOS+TCP, OpenOCD / J-Link / ST-Link. (coll · ★32 · 2026-07)
- [JasonYANG170/esp-dev-skill](https://github.com/JasonYANG170/esp-dev-skill) - One sub-skill per Espressif repo: esp-idf, arduino-esp32, esp-adf, esp-dl, esp-zigbee-sdk, esp-at, esp-brookesia, esp-claw, connectedhomeip. (coll · ★27 · 2026-08)
- [EricSun787/stm32-development-workflow](https://github.com/EricSun787/stm32-development-workflow) - STM32CubeCLT command-line flow: toolchain, HAL, build, ST-Link flash, common error fixes. Chinese. (★24 · 2026-02)
- [wedsamuel1230/arduino-skills](https://github.com/wedsamuel1230/arduino-skills) - 30 Arduino and maker skills: code generator, arduino-cli, serial monitor, pin assignment, I2C bring-up diagnostician, wiring safety check, power budget, BOM, OTA guardian. (coll · ★21 · 2026-08)
- [claudius-ars/embedded-agent-skills `gpio-config`](https://github.com/claudius-ars/embedded-agent-skills/tree/main/embedded-agent-skills/gpio-config) - GPIO / I2C / SPI / UART / PWM pin assignment with conflict checks for Raspberry Pi (device-tree overlays, config.txt) and ESP32 (sdkconfig). (★19 · 2026-02)
- [alexex1993/mcu-skills](https://github.com/alexex1993/mcu-skills) - One skill per board (19): RP2040 Pico, RP2350, ESP32-WROOM 30/36/38-pin, ESP32-S3-CAM, ESP32-C6, ESP32-P4, nRF52840 ProMicro, STM32F411 BlackPill, STM32H750, ATmega328P Nano, ESP8266 — pinout, peripherals, power. (coll · ★17 · 2026-09)
- [o2scale/electronics-agent-kit](https://github.com/o2scale/electronics-agent-kit/tree/main/.agent/skills) - PlatformIO project / config / debug for Arduino, ESP-IDF and STM32, plus kicad-cli and KiCad file-format skills. (coll · ★12 · 2026-02)
- [varo6/reTerminal-sticky-skill](https://github.com/varo6/reTerminal-sticky-skill/tree/main/skills/sticky-device) - Seeed reTerminal Sticky (ESP32-S3 e-ink): pin map, ESP-IDF patterns, ePaper refresh rules. (★7 · 2026-08)
- [PatrickJS/awesome-cursorrules `embedded-stm32-hal`](https://github.com/PatrickJS/awesome-cursorrules/blob/main/rules/embedded-stm32-hal.mdc) - Cursor rule, not a skill: embedded C/C++ on STM32 HAL, ISR, DMA and memory-constraint conventions. (cursor-rules · ★40.8k · 2026-05)

### RTOS

- [a5c-ai/babysitter `embedded-systems`](https://github.com/a5c-ai/babysitter/tree/main/library/specializations/embedded-systems/skills) - 29 short skills: Zephyr, FreeRTOS, Nordic nRF, STM32 HAL, Cortex-M, JTAG/SWD, linker scripts, CAN, USB stack, OTA, motor control, MISRA, Unity/Ceedling. Breadth over depth. (coll · ★1.8k · 2026-09)
- [beriberikix/zephyr-agent-skills](https://github.com/beriberikix/zephyr-agent-skills) - The most complete Zephyr catalog (21 skills): foundations, board bring-up (HWMv2), devicetree, build system, kernel, BLE / IP / USB / CAN connectivity, IoT protocols, multicore, `native_sim`, power, security updates, storage, testing; a keyword / Kconfig / compatible-scored router picks the right one. (coll · ★64 · 2026-05)
- [ksachdeva/zephyr-rtos-ai](https://github.com/ksachdeva/zephyr-rtos-ai/tree/main/skills) - 25 per-subsystem Zephyr API skills: BLE (GAP roles, GATT, pairing, NUS), devicetree, Kconfig, GPIO, I2C, SPI, UART, ISR, threads, sync, power management, settings, storage, sockets, Wi-Fi, SMF, shell, testing, memory. (coll · ★23 · 2026-06)
- [chshzh/charlie-skills](https://github.com/chshzh/charlie-skills) - 27 Nordic nRF Connect SDK skills covering the PRD → spec → code → test lifecycle, NCS 3.x migration, nRF70 Wi-Fi throughput and firmware stats, Memfault. (coll · ★0 · 2026-08)
- [goliothlabs/golioth-firmware-skill](https://github.com/goliothlabs/golioth-firmware-skill/tree/main/skills/golioth-firmware) - Golioth SDK on Zephyr, ESP-IDF, NCS and ModusToolbox: greenfield and brownfield integration, OTA, the six cloud services. (★1 · 2026-03)

### Robotics

- [earthtojake/text-to-cad `urdf` / `srdf` / `sdf`](https://github.com/earthtojake/text-to-cad/tree/main/skills/urdf) - Robot description formats inside a CAD/CAM skill library that also covers G-code and Bambu printers. (coll · ★15.8k · 2026-09)
- [rerun-io/rerun `rerun-lerobot`](https://github.com/rerun-io/rerun/tree/main/skills/rerun-lerobot) - Visualize LeRobot datasets in Rerun. (★11.4k · 2026-09)
- [arpitg1304/robotics-agent-skills](https://github.com/arpitg1304/robotics-agent-skills) - Production ROS 1/2 practice: QoS, lifecycle nodes, colcon, DDS, robot bring-up, perception, testing, security, Docker dev, web integration. (coll · ★358 · 2026-08)
- [dbwls99706/ros2-engineering-skills](https://github.com/dbwls99706/ros2-engineering-skills) - Single progressive-disclosure skill: rclcpp / rclpy, QoS / DDS, tf2 / URDF, ros2_control, Nav2, MoveIt 2, real-time, hardware safety. (★175 · 2026-09)
- [MIUAV/vibe-coding-ros2](https://github.com/MIUAV/vibe-coding-ros2) - PX4 + ROS 2 Humble drone development: MAVLink, offboard mode, firmware build, module dev, airframes, sensor config, multicopter tuning, vision nav. Chinese. (coll · ★26 · 2026-05)
- [adityakamath/ros2-skill](https://github.com/adityakamath/ros2-skill) - Runtime control rather than code generation: drive topics, services, actions, params, lifecycle, ros2_control and Nav2 on a live robot via bundled rclpy scripts. (★18 · 2026-07)
- [wimblerobotics/ros2-copilot-skills](https://github.com/wimblerobotics/ros2-copilot-skills) - 158 Nav2 / behavior-tree / SLAM / Teensy-PlatformIO skills for Copilot; quality is uneven. (coll · ★18 · 2026-04)
- [robium-ai/robium](https://github.com/robium-ai/robium) - ROS 2 / Nav2 / Gazebo / MuJoCo / Isaac / LeRobot plugin with a versioned SKILL.md archive. (coll · ★13 · 2026-09)
- [PatrickJS/awesome-cursorrules `ros-ros2`](https://github.com/PatrickJS/awesome-cursorrules/blob/main/rules/ros-ros2.mdc) - Cursor rule for ROS / ROS 2 packages, nodes, launch files, messages, URDF/xacro. (cursor-rules · ★40.8k · 2026-05)

### EDA / PCB

- [atopile/atopile `.claude/skills/`](https://github.com/atopile/atopile/tree/main/.claude/skills) - Code-defined PCB design; `ato` and `ato-language` are user-facing, the rest are compiler / solver / library contributor skills. (coll · ★3.9k · 2026-06)
- [aklofas/kicad-happy](https://github.com/aklofas/kicad-happy) - Analyze KiCad projects and PDF schematics, DRC / ERC / DFM, EMC pre-compliance, SPICE, part sourcing on DigiKey / Mouser / LCSC / element14, JLCPCB and PCBWay prep. (coll · ★1.2k · 2026-09)
- [diodeinc/pcb](https://github.com/diodeinc/pcb/tree/main/skills) - Zener code-to-PCB language plus `datasheet-reader`, `librarian`, registry search and SPICE simulation skills. (coll · ★448 · 2026-09)
- [zhoushoujianwork/easyeda-agent](https://github.com/zhoushoujianwork/easyeda-agent) - Drive EasyEDA Pro (JLC EDA) through a local CLI / daemon: schematic, netlist check, PCB placement and routing, DRC, fab export; ships as CLI + skill + MCP. (★438 · 2026-09)
- [American-Embedded/kistack](https://github.com/American-Embedded/kistack) - Human-written KiCad skill stack: schematic, symbol, footprint, PCB layout, gerbers, panelization, BOM, export, product render. (coll · ★383 · 2026-09)
- [oaslananka/kicad-mcp-pro](https://github.com/oaslananka/kicad-mcp-pro/tree/main/skills) - `pcb-design` and `kicad-design-review` skills that sit on top of a KiCad MCP: placement, routing, stackup, quality gates. (coll · ★91 · 2026-09)
- [Zane456/PCB-Agent-Teams](https://github.com/Zane456/PCB-Agent-Teams) - Multi-agent KiCad pipeline from topology to Gerber with HV / LV / isolation partitioning. (coll · ★66 · 2026-07)
- [l3wi/claude-eda](https://github.com/l3wi/claude-eda) - `eda-architect`, `eda-schematics`, `eda-pcb`, `eda-drc`, `eda-research` for KiCad. (coll · ★15 · 2026-01)

### FPGA / HDL

- [a5c-ai/babysitter `fpga-programming`](https://github.com/a5c-ai/babysitter/tree/main/library/specializations/fpga-programming/skills) - 19 short skills: Verilog / SV / VHDL, timing constraints, CDC, SVA, UVM, HLS, place-and-route, synthesis, debugging. (coll · ★1.8k · 2026-09)
- [Eriemon/verilog-generator](https://github.com/Eriemon/verilog-generator) - Readable Verilog-2001 generation, review and annotation, testbench scaffolds, local or remote Vivado. (★282 · 2026-08)
- [Mindrally/skills `fpga` / `systemverilog`](https://github.com/Mindrally/skills) - Cursor-rule-derived FPGA and SystemVerilog skills, ~1k installs each. (★259 · 2026-09)
- [codejunkie99/Gateflow-Plugin](https://github.com/codejunkie99/Gateflow-Plugin) - SystemVerilog design → verify (cocotb, formal) → deliver on the open-source toolchain, with FuseSoC and IP packaging. (coll · ★113 · 2026-05)
- [TONGJI-EDA-LAB/RTL-CLAW](https://github.com/TONGJI-EDA-LAB/RTL-CLAW) - Academic Verilog partition / optimization (Yosys + Verible) / merge skills on OpenClaw. (coll · ★64 · 2026-04)
- [bjwanneng/veriflow-cc](https://github.com/bjwanneng/veriflow-cc) - Architect → RTL → iverilog / Yosys pipeline with cocotb coverage. (★51 · 2026-08)
- [LilithSemi/claude-for-hardware](https://github.com/LilithSemi/claude-for-hardware) - The only FPGA collection with physical bring-up: bitstream over bit-banged JTAG from a Raspberry Pi, synthesis fit, area / timing, bare-metal boot chain, ROHD gotchas. (coll · ★21 · 2026-08)
- [londey/claude-skill-verilog](https://github.com/londey/claude-skill-verilog) - Verilog working skill. (★18 · 2026-04)

### SBC / Linux

- [D-Robotics/moss `jetson-knowledge`](https://github.com/D-Robotics/moss) - Orin / Xavier specs, JetPack / L4T, Super Mode, TensorRT engine builds, alongside D-Robotics RDK skills. (coll · ★142 · 2026-08)
- [NVIDIA-AI-IOT/jetson-device-skills](https://github.com/NVIDIA-AI-IOT/jetson-device-skills) - Canonical source of the `jetson-diagnostic`, `jetson-memory-audit`, `jetson-llm-serve`, `jetson-video-*` skills mirrored into NVIDIA/skills. (official · coll · ★135 · 2026-08)
- [NVIDIA-AI-IOT/jetson-bsp-skills](https://github.com/NVIDIA-AI-IOT/jetson-bsp-skills) - Canonical source of the `jetson-customize-*` BSP skills: pinmux, PCIe, USB, clocks, fan, carrier derivation, image validation and flashing. (official · coll · ★59 · 2026-06)
- [Seeed-Projects/Seeed-Jetson-DevelopTool](https://github.com/Seeed-Projects/Seeed-Jetson-DevelopTool/tree/main/skills/openclaw) - Seeed reComputer / Jetson support skills: JetPack overview, Docker setup, AI tools, L4T differences, YOLO on Jetson, FAQ. (coll · ★55 · 2026-09)

### Wireless

- [BrownFineSecurity/iothackbot](https://github.com/BrownFineSecurity/iothackbot) - IoT pentest with physical tools: JTAG probing, logic-analyzer / MSO capture, picocom UART consoles, telnet shells, chipsec, ONVIF and network scans, jadx / apktool. (coll · ★841 · 2026-06)
- [ksachdeva/zephyr-rtos-ai `zephyr-bluetooth-le`](https://github.com/ksachdeva/zephyr-rtos-ai/tree/main/skills/zephyr-bluetooth-le) - GAP / GATT / advertising / pairing / NUS in Zephyr. (★23 · 2026-06)
- [beriberikix/zephyr-agent-skills `connectivity-ble`](https://github.com/beriberikix/zephyr-agent-skills/tree/main/skills/connectivity-ble) - Zephyr BLE plus the `iot-protocols` sibling for MQTT / CoAP / LwM2M. (★64 · 2026-05)
- [JasonYANG170/esp-dev-skill `esp-zigbee-sdk`](https://github.com/JasonYANG170/esp-dev-skill/tree/main/repos/esp-zigbee-sdk) - ESP Zigbee SDK sub-skill. (★27 · 2026-08)

### Industrial / IoT / 3D printing

- [earthtojake/text-to-cad `bambu-labs` / `gcode`](https://github.com/earthtojake/text-to-cad/tree/main/skills/bambu-labs) - Bambu printer control and G-code generation; `bambu-labs` has ~6.7k installs on skills.sh. (★15.8k · 2026-09)
- [LeoKemp223/embed-ai-tool `modbus-debug` / `can-debug` / `visa-debug`](https://github.com/LeoKemp223/embed-ai-tool/tree/master/skills/modbus-debug) - Bus-level debugging with scripts; the only CAN and VISA/SCPI skills found. (★919 · 2026-08)
- [santiagomoneta/3d-printing-skills](https://github.com/santiagomoneta/3d-printing-skills) - Klipper config, diagnostics and calibration through the Moonraker API, plus OrcaSlicer. (coll · ★4 · 2026-03)
- [studioxvii/modbus-skills](https://github.com/studioxvii/modbus-skills/tree/main/plugins/modbus-skills/skills) - 20 read-only Modbus engineering skills: extract a register map from an OEM PDF, normalize it, check byte order, plan reads, build modpoll / ModScan / Node-RED packs, analyze captures. Small but well-structured. (coll · ★1 · 2026-09)

### Smart Home

- [komal-SkyNET/claude-skill-homeassistant](https://github.com/komal-SkyNET/claude-skill-homeassistant/tree/main/skills/home-assistant-manager) - Manage Home Assistant via its API: modern automation YAML (2024.10+), dashboards, a verification protocol before applying changes. (★957 · 2026-07)
- [homeassistant-ai/skills `home-assistant-best-practices`](https://github.com/homeassistant-ai/skills/tree/main/skills/home-assistant-best-practices) - Automations, helpers, scripts, dashboards, blueprints; the most-installed hardware-adjacent skill on skills.sh (~7k). (★746 · 2026-09)
- [bradsjm/hassio-addons](https://github.com/bradsjm/hassio-addons) - Seven HA skills published through an add-on: automation scripts, dashboard cards, entities and services, ESPHome, integrations, custom integrations, AWTRIX. (coll · ★45 · 2026-07)
- [nodnarbnitram/claude-code-extensions `esphome-config-helper`](https://github.com/nodnarbnitram/claude-code-extensions) - ESPHome YAML generation, validation and troubleshooting. (★16 · 2026-04)

## MCP servers and bridges

Tool servers an agent calls at runtime. Best current surveys of this space are Veecle's [August 2026 review](https://veecle.ai/blog/hardware-mcp-servers-reviewed) and [vendor follow-up](https://veecle.ai/blog/hardware-mcp-servers-2026); [beriberikix/awesome-mcp-hardware](https://github.com/beriberikix/awesome-mcp-hardware) is the upstream list.

### MCU / Embedded (MCP)

- [78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) - ESP32 voice-AI chatbot firmware built on MCP: the device exposes its own tools to the LLM. Paired with [xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server) (★10.6k). (★29.9k · 2026-09)
- [golioth/tinymcp](https://github.com/golioth/tinymcp) - Let LLMs control constrained embedded devices via MCP proxied through Golioth cloud RPC. Experimental. (official · ★157 · 2025-07)
- [horw/esp-mcp](https://github.com/horw/esp-mcp) - ESP-IDF build, flash and automatic build-error fixing. (★157 · 2025-12)
- [jl-codes/platformio-mcp](https://github.com/jl-codes/platformio-mcp) - Build, upload and monitor across the 1000+ PlatformIO boards. (★51 · 2026-09)
- [AaronWander/EmbedMCP](https://github.com/AaronWander/EmbedMCP) - C library to run an MCP server on the microcontroller itself (STM32, ESP32, nRF, Raspberry Pi). (★31 · 2026-02)
- [shieldyguy/stm32-mcp](https://github.com/shieldyguy/stm32-mcp) - Build, flash and talk to STM32 over SWD and serial. (★25 · 2026-08)
- [espressif/esp-rainmaker-mcp](https://github.com/espressif/esp-rainmaker-mcp) - Control ESP RainMaker devices through the RainMaker CLI. (official · ★18 · 2025-07)
- [hardware-mcp/arduino-mcp-server](https://github.com/hardware-mcp/arduino-mcp-server) - Wraps arduino-cli: compile, upload, serial sessions. (★17 · 2026-08)
- [Oliver0804/arduino-cli-mcp](https://github.com/Oliver0804/arduino-cli-mcp) - Arduino CLI for VS Code / Claude: compile, upload, library management. (★13 · 2026-05)
- [jaklys/Lvgl-mcp-esp32](https://github.com/jaklys/Lvgl-mcp-esp32) - MCP plus LVGL UI on ESP32. (★12 · 2026-07)
- [Volt23/mcp-arduino-server](https://github.com/Volt23/mcp-arduino-server) - Arduino CLI bridge: sketch, board, library and file management. (★10 · 2026-01)
- [SWITCHSCIENCE/mcp-micropython-bridge](https://github.com/SWITCHSCIENCE/mcp-micropython-bridge) - Bridge to a MicroPython REPL on ESP32 / RP2040 over USB serial. Japanese docs. (★9 · 2026-04)
- [Wokwi MCP mode](https://docs.wokwi.com/wokwi-ci/mcp-support) - `wokwi-cli mcp` exposes hosted Wokwi simulation to an agent: run Arduino / ESP32 / RP2040 firmware and read serial without a board. Source in [wokwi/wokwi-cli](https://github.com/wokwi/wokwi-cli). (official · ★66 · 2026-06)

### Serial / bus / debug (MCP)

- [mcp2everything/mcp2mqtt](https://github.com/mcp2everything/mcp2mqtt) - MCP → MQTT bridge for hardware control; the most-cited early work, but unmaintained. (★371 · stale since 2024-12)
- [Adancurusul/embedded-debugger-mcp](https://github.com/Adancurusul/embedded-debugger-mcp) - 24-tool debugger over probe-rs / OpenOCD for Cortex-M, RISC-V and Xtensa, with a bundled Claude / Codex skill. Veecle's top pick. (★187 · 2026-07)
- [Adancurusul/serial-mcp-server](https://github.com/Adancurusul/serial-mcp-server) - Rust serial / UART MCP and CLI with JSON macro automation and agent skills. (★91 · 2026-07)
- [mcp2everything/mcp2serial](https://github.com/mcp2everything/mcp2serial) - PySerial-based MCP for serial devices such as the Pico. (★49 · stale since 2024-12)
- [Ipiano/gdb-mcp](https://github.com/Ipiano/gdb-mcp) - Drives GDB/MI directly for embedded and native targets. (★48 · 2026-03)
- [es617/dbgprobe-mcp-server](https://github.com/es617/dbgprobe-mcp-server) - Symbol-aware (ELF / SVD) on-chip debug through J-Link, CMSIS-DAP and ST-Link. (★10 · 2026-03)
- [daedalus/mcp-canbus](https://github.com/daedalus/mcp-canbus) - CAN bus MCP; the only CAN entry found. (★0 · 2026-03)

### Robotics (MCP)

- [dimensionalOS/dimos](https://github.com/dimensionalOS/dimos) - Agentic OS for physical space: command humanoids, Unitree quadrupeds, xArm and MAVLink drones in natural language. (★4.5k · 2026-09)
- [robotmcp/ros-mcp-server](https://github.com/robotmcp/ros-mcp-server) - Connect Claude / GPT to ROS and ROS 2 robots via rosbridge; client counterpart [robotmcp_client](https://github.com/robotmcp/robotmcp_client). (★1.5k · 2026-09)
- [Extelligence-ai/bagel](https://github.com/Extelligence-ai/bagel) - Query robotics, drone and IoT telemetry (ROS bags, MCAP, PX4 logs) in plain English with an edge data-reduction pipeline. (★396 · 2026-09)
- [omni-mcp/isaac-sim-mcp](https://github.com/omni-mcp/isaac-sim-mcp) - Natural-language control of NVIDIA Isaac Sim scenes and robots. (★190 · 2025-04)
- [wise-vision/ros2_mcp](https://github.com/wise-vision/ros2_mcp) - ROS 2 MCP with image streaming and automatic QoS matching. (★88 · 2026-08)
- [lpigeon/unitree-go2-mcp-server](https://github.com/lpigeon/unitree-go2-mcp-server) - Control a Unitree Go2 robot dog through ROS 2. (★87 · 2026-06)
- [kakimochi/ros2-mcp-server](https://github.com/kakimochi/ros2-mcp-server) - Topic-based ROS 2 control. (★83 · 2025-06)
- [IliaLarchenko/robot_MCP](https://github.com/IliaLarchenko/robot_MCP) - SO-ARM100 / 101 and LeKiwi arm control in the LeRobot ecosystem. (★83 · 2025-08)
- [groundlight/mcp-vision](https://github.com/groundlight/mcp-vision) - Zero-shot vision models as MCP tools for robot perception. (★62 · 2025-05)
- [Yutarop/ros-mcp](https://github.com/Yutarop/ros-mcp) - ROS topics, services and actions as MCP tools. (★36 · 2025-08)
- [jackccrawford/reachy-mini-mcp](https://github.com/jackccrawford/reachy-mini-mcp) - Pollen Robotics Reachy Mini control. (★29 · 2026-07)
- [binabik-ai/mcp-rosbags](https://github.com/binabik-ai/mcp-rosbags) - Offline rosbag analysis. (★28 · 2025-09)
- [robotmem/robotmem](https://github.com/robotmem/robotmem) - Persistent hybrid + spatial memory for MCP-controlled robots. (★28 · 2026-03)
- [0xKoda/drone-mcp](https://github.com/0xKoda/drone-mcp) - DJI Tello drone control. (★25 · 2025-04)
- [ion-g-ion/MAVLinkMCP](https://github.com/ion-g-ion/MAVLinkMCP) - PX4 / ArduPilot drones via MAVLink. (★23 · 2026-08)
- [showkeyjar/robot-mcp-server](https://github.com/showkeyjar/robot-mcp-server) - Unitree and DJI drone motion control. (★12 · 2026-03)
- [phospho-app/phospho-mcp-server](https://github.com/phospho-app/phospho-mcp-server) - VLA bridge for SO-100 / 101 arms. (★10 · 2025-09)
- [monteslu/robot-mcp](https://github.com/monteslu/robot-mcp) - Johnny-Five MCP: Arduino and Raspberry Pi servos and hardware. (★7 · 2026-02)
- [RoversX/universal-robot-mcp](https://github.com/RoversX/universal-robot-mcp) - Universal Robots cobot control; the only industrial-arm entry. (★5 · 2025-09)

### Industrial IoT (MCP)

- [ThingsPanel/thingspanel-mcp](https://github.com/ThingsPanel/thingspanel-mcp) - ThingsPanel IoT platform device control and data analysis. (★47 · 2025-11)
- [kukapay/opcua-mcp](https://github.com/kukapay/opcua-mcp) - Connect to OPC UA systems: monitor, analyze and control nodes. (★28 · 2025-10)
- [kukapay/modbus-mcp](https://github.com/kukapay/modbus-mcp) - Standardize and contextualize Modbus registers for agents. (★24 · 2025-05)
- [lwsinclair/IoT-Edge-MCP-Server](https://github.com/lwsinclair/IoT-Edge-MCP-Server) - Unifies MQTT, Modbus and InfluxDB for SCADA / PLC work. (★3 · 2025-11)
- [daedalus/mcp-snap7](https://github.com/daedalus/mcp-snap7) - Siemens S7 PLC via python-snap7; the only Siemens entry. (★0 · 2026-04)

### Smart Home (MCP)

- [home-assistant/core `mcp_server`](https://www.home-assistant.io/integrations/mcp_server/) - Built-in MCP server integration exposing the Assist API over Streamable HTTP. (official · ★90k · 2026-09)
- [homeassistant-ai/ha-mcp](https://github.com/homeassistant-ai/ha-mcp) - 86 tools; the most feature-rich Home Assistant MCP. (★4.7k · 2026-09)
- [tevonsb/homeassistant-mcp](https://github.com/tevonsb/homeassistant-mcp) - Home Assistant MCP with SSE real-time updates. (★576 · 2026-01)
- [voska/hass-mcp](https://github.com/voska/hass-mcp) - Token-efficient Home Assistant control and query. (★340 · 2026-08)
- [jango-blockchained/advanced-homeassistant-mcp](https://github.com/jango-blockchained/advanced-homeassistant-mcp) - 50+ Home Assistant tools over three transports. (★56 · 2026-06)
- [ykhli/mcp-light-control](https://github.com/ykhli/mcp-light-control) - Philips Hue control. (★22 · 2025-03)
- [scald/tesla-mcp](https://github.com/scald/tesla-mcp) - Tesla vehicle control via the Fleet API. (★15 · 2025-03)
- [ichbinder/MCP2ZigBee2MQTT](https://github.com/ichbinder/MCP2ZigBee2MQTT) - Zigbee2MQTT device discovery and control. (★12 · 2025-10)
- [genm/switchbot-mcp](https://github.com/genm/switchbot-mcp) - SwitchBot device control. (★7 · 2026-09)
- [noboru-i/nature-remo-mcp-server](https://github.com/noboru-i/nature-remo-mcp-server) - Nature Remo IR hub. (★7 · 2025-04)
- [veonua/smartthings-mcp](https://github.com/veonua/smartthings-mcp) - Samsung SmartThings rooms, devices and commands. (★5 · 2025-07)

### Lab instruments (MCP)

- [Netlist-Studio/scope-mcp](https://github.com/Netlist-Studio/scope-mcp) - Keysight / Agilent oscilloscope over Ethernet, tested on an MSOX2024A. (★11 · 2026-02)
- [sandraschi/sdr-mcp](https://github.com/sandraschi/sdr-mcp) - RTL-SDR: spectrum, waterfall, FM demodulation, GNU Radio. (★7 · 2026-09)
- [roomi-fields/osc-bridge](https://github.com/roomi-fields/osc-bridge) - OSC ↔ MIDI / SysEx bridge for hundreds of hardware synths. (★7 · 2026-08)
- [hsoffar/saleae-logic2-mcp](https://github.com/hsoffar/saleae-logic2-mcp) - Saleae Logic 2 logic-analyzer automation. (★3 · 2026-03)

### EDA / PCB / CAD (MCP)

- [mixelpixx/KiCAD-MCP-Server](https://github.com/mixelpixx/KiCAD-MCP-Server) - Edit KiCad schematics and PCBs directly from Claude. (★2.2k · 2026-09)
- [daobataotie/CAD-MCP](https://github.com/daobataotie/CAD-MCP) - Natural-language CAD operations across AutoCAD, GstarCAD and ZWCAD. (★548 · 2025-07)
- [lamaalrajih/kicad-mcp](https://github.com/lamaalrajih/kicad-mcp) - KiCad project management, DRC, BOM and netlist analysis. (★521 · 2025-10)
- [salitronic/eda-agent](https://github.com/salitronic/eda-agent) - 290+ tools driving a live Altium Designer session, optionally KiCad / EasyEDA Pro. (★199 · 2026-09)
- [jhacksman/OpenSCAD-MCP-Server](https://github.com/jhacksman/OpenSCAD-MCP-Server) - Text or image → parametric OpenSCAD 3D models. (★190 · 2026-09)
- [coffeenmusic/altium-mcp](https://github.com/coffeenmusic/altium-mcp) - Altium Designer PCB query and manipulation. (★158 · 2026-09)
- [Seeed-Studio/kicad-mcp-server](https://github.com/Seeed-Studio/kicad-mcp-server) - Seeed-maintained KiCad MCP: pin-level connectivity tracing and design editing. (official · ★129 · 2026-09)
- [circuit-synth/kicad-sch-api](https://github.com/circuit-synth/kicad-sch-api) - Python API for KiCad schematic s-expressions, with an [MCP wrapper](https://github.com/circuit-synth/mcp-kicad-sch-api). (★52 · 2025-12)
- [Netlist-Studio/kicad-mcp](https://github.com/Netlist-Studio/kicad-mcp) - KiCad 9 control over its IPC API. (★18 · 2026-02)
- [octoco-ltd/sheetsdata-mcp](https://github.com/octoco-ltd/sheetsdata-mcp) - Component datasheets: specs, pinouts and absolute-maximum ratings from PDFs. (★11 · 2026-04)

### SBC and 3D printing (MCP)

- [DMontgomery40/mcp-3D-printer-server](https://github.com/DMontgomery40/mcp-3D-printer-server) - OctoPrint, Klipper, Duet, Repetier, Prusa, Bambu and Creality plus STL operations. (★236 · 2026-07)
- [axonixtools/PocketMCP](https://github.com/axonixtools/PocketMCP) - Turn an Android phone into an MCP server exposing its sensors. (★17 · 2026-08)
- [grammy-jiang/RaspberryPiOS-MCP](https://github.com/grammy-jiang/RaspberryPiOS-MCP) - Raspberry Pi OS: GPIO, I2C, camera. The only Pi-specific MCP found. (★0 · 2026-03)

## Agent frameworks and on-device runtimes

- [openclaw/openclaw](https://github.com/openclaw/openclaw) - Ships `robot` and `esp32` skills (ROS 2 wiring, GPIO pitfalls); community ports such as [openclaw-esp32](https://github.com/hrwtech/openclaw-esp32) run the agent loop on ESP32 boards. (★390k · 2026-09)
- [huggingface/lerobot](https://github.com/huggingface/lerobot) - End-to-end robot learning: datasets, ACT / Diffusion / VLA policies, drivers for SO-100 / 101, Koch and LeKiwi. (★27.5k · 2026-09)
- [isaac-sim/IsaacLab](https://github.com/isaac-sim/IsaacLab) - Unified robot-learning framework on Isaac Sim: RL, imitation, sim-to-real. (★8.1k · 2026-09)
- [NVIDIA/Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T) - GR00T foundation model for generalist humanoids with fine-tuning and inference stack. (★8.1k · 2026-08)
- [openvla/openvla](https://github.com/openvla/openvla) - 7B open vision-language-action model for manipulation; the reference VLA, now frozen. (★7k · 2025-03)
- [espressif/esp-claw](https://github.com/espressif/esp-claw) - Agent runtime that runs on ESP32-S3 / P4 / C5: capabilities in C, skills in Lua, bidirectional MCP, event router. The 43 skills in [esp-claw-skills-lab](https://github.com/espressif/esp-claw-skills-lab) are Lua apps, not SKILL.md. (official · ★2.1k · 2026-09)
- [nasa-jpl/rosa](https://github.com/nasa-jpl/rosa) - LangChain agent that inspects, diagnoses and operates ROS 1 / 2 robots by natural language. (★1.6k · 2026-03)
- [acon96/home-llm](https://github.com/acon96/home-llm) - Home Assistant integration plus fine-tuned local models for device control. (★1.4k · 2026-09)
- [Home Assistant LLM API](https://developers.home-assistant.io/docs/core/llm/) - The official Assist LLM API: integrations register tools any conversation agent can call. (official)
- [arm/mcp](https://github.com/arm/mcp) - Arm's official MCP: docs search, migration analysis, assembly performance analysis. Nordic, Microchip, Silicon Labs, TI and ADI have shipped similar docs-only vendor MCPs. (official · ★91 · 2026-09)
- [automatika-robotics/embodied-agents](https://github.com/automatika-robotics/embodied-agents) - ROS 2-native framework for interactive physical agents with LLM / VLM components. (★67 · 2026-09)

## Verification infrastructure

What you need to run a hardware skill's `evals/` without owning the board — and how far each option gets you.

### Simulators and emulators

- [wokwi/wokwi-cli](https://github.com/wokwi/wokwi-cli) - ESP32 family, AVR, RP2040, nRF52, partial STM32, plus sensors and displays. YAML scenarios assert on serial text and set pins; GitHub Action; free CI token for open source; experimental MCP mode. The simulator core is hosted and closed. Our `L1 (wokwi)` backend. (★66 · 2026-06)
- [renode/renode](https://github.com/renode/renode) - Cortex-M / A / R, RISC-V, Xtensa, whole boards and multi-node networks; `.resc` scripts, Robot Framework harness, Zephyr twister integration, deterministic. MIT. No MCP server exists yet — the biggest gap in this list. Our `L1 (renode)` backend. (★2.9k · 2026-09)
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
- [jumpstarter-dev/jumpstarter](https://github.com/jumpstarter-dev/jumpstarter) - Red Hat-backed HIL framework for real or virtual targets, local or remote, Kubernetes-native, explicitly designed for "human, automated or agentic" drivers; power, serial and flashing drivers. The strongest fit for an L2 device farm. (★219 · 2026-09)
- [labgrid-project/labgrid](https://github.com/labgrid-project/labgrid) - Pengutronix board-control library (power, serial, USB, network boot) with pytest integration. (★527 · 2026-09)
- [kernelci/kernelci-core](https://github.com/kernelci/kernelci-core) - Community hardware labs with an open API; labs donated by Collabora, BayLibre and others. (★120 · 2026-09)
- [Linaro LAVA](https://gitlab.com/lava/lava) - Board-farm scheduler used by KernelCI and Linaro labs; self-hostable. (★82 · 2026-09)
- [Zephyr twister device testing](https://docs.zephyrproject.org/latest/develop/test/twister.html) - `twister --device-testing --hardware-map` runs the test suite on attached boards; [golioth/zephyr_twister_hil_testing](https://github.com/golioth/zephyr_twister_hil_testing) shows it on a GitHub self-hosted runner. (official)
- [Wokwi CI](https://docs.wokwi.com/wokwi-ci/getting-started) - Hosted simulation inside GitHub Actions; free token for open-source projects. (official)
- [OpenHiL](https://openhil.github.io/) - Community hub for open hardware-in-the-loop tooling.

## Benchmarks and evals

Only the first two validate on physical MCUs; everything else is compile-only or sim-only.

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
- [Securing LLM-Generated Embedded Firmware through AI Agent-Driven Validation and Patching](https://arxiv.org/abs/2509.09970) - FreeRTOS on QEMU with a fuzzing, static-analysis and agent-patching loop.
- [Embedded Arena: Iterative Optimization via Hardware Feedback](https://arxiv.org/abs/2606.16190) - Hardware feedback flips 0% to success in three iterations.
- [Toward a Modular Architecture for Embedded AI Agent Systems at the Edge](https://arxiv.org/abs/2606.02862) - On-device agent runtime design; compare with esp-claw.
- [Coscientist](https://github.com/gomesgroup/coscientist) - GPT-4 agent driving an Opentrons liquid handler and Emerald Cloud Lab. Nature 2023. (★211 · 2025-08)
- [Autonomous Chemistry and Materials Innovation Driven by Scientific Agents](https://pubs.acs.org/doi/10.1021/jacsau.6c00213) - Survey of LLM-run self-driving labs. JACS Au 2026.

## Agent-ready docs

Vendor documentation that serves `llms.txt` — verified live and plain-text on 2026-09-15. Useful as `references/` for a skill.

- [Arduino](https://docs.arduino.cc/llms.txt) - 181 KB index plus `llms-full.txt`; the only MCU-vendor llms.txt found.
- [NVIDIA Jetson](https://docs.nvidia.com/jetson/llms.txt) - Also `docs.omniverse.nvidia.com/llms.txt`.
- [Silicon Labs](https://docs.silabs.com/llms.txt) - 36 MB full dump covering EFR32, BLE, Zigbee and Matter.
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

Checked and absent (404 or HTML): Zephyr, Espressif, Nordic, ST, PlatformIO, KiCad, ROS docs, Golioth, Home Assistant, ESPHome, MicroPython, CircuitPython, Raspberry Pi, Seeed wiki, Isaac Sim / Lab, Embassy, BeagleBoard, ThingsBoard.

## Gaps

Where no good skill exists as of the snapshot. If you build one of these, it is the fastest route onto this list.

- **First-party MCU skills.** Nothing from Espressif (placeholder repo), STMicro, Nordic (MCP only), Raspberry Pi / Pico SDK, NXP, Renesas, Microchip or TI. Everything MCU-side is community.
- **Zephyr Project, KiCad, Open Robotics and Arduino** publish no skills; Zephyr and KiCad also have no llms.txt.
- **Hardware-in-the-loop from the agent's side** — flash → run → read serial → iterate. Only tinyusb `hil`, SensorsIot's harness, LeoKemp's toolkit and cwc-makers close this loop. Highest value, least covered.
- **MicroPython / CircuitPython.** Adafruit's four test skills and scattered one-offs; no general skill of quality.
- **Raspberry Pi Linux.** No serious skill beyond `gpio-config`; Pico / RP2040 has only per-board pinout skills.
- **Wireless.** No dedicated BLE central / peripheral skill outside the Zephyr collections; nothing for LoRa / LoRaWAN, Thread, device-side Matter, or Wi-Fi provisioning. BLE has no real MCP either.
- **Industrial.** Modbus is covered (read-only). OPC UA, CAN / CANopen, EtherCAT, PROFINET and IEC 61131 PLC programming are effectively empty; the only CAN entries are one skill and one 0-star MCP.
- **Test and measurement.** No skill for oscilloscopes, logic analyzers or SCPI instruments beyond `logicmso` and `visa-debug`; MCPs cover one Keysight scope and one Saleae.
- **Embedded Linux.** Nothing for Yocto, Buildroot or device tree beyond generic pattern skills.
- **Renode MCP server.** The most agent-shaped OSS emulator has no MCP, so L1 for Cortex-M skills currently means Wokwi's hosted service or a custom runner.
- **Drones.** Only PX4's build skill and one Chinese PX4 collection; nothing for ArduPilot.

## Related lists

- [beriberikix/awesome-mcp-hardware](https://github.com/beriberikix/awesome-mcp-hardware) - Upstream list of hardware MCP servers; this list's MCP section started from it.
- [TensorBlock/awesome-mcp-servers — hardware & IoT](https://github.com/TensorBlock/awesome-mcp-servers/blob/main/docs/hardware--iot.md) - Hardware category of a general MCP list.
- [fouad1233/amazing-robotics-skills](https://github.com/fouad1233/amazing-robotics-skills) - Licence-aware index of 1,039 NVIDIA-ecosystem skills across 35 repos.
- [heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills) - General Agent Skills directory.
- [skillmatic-ai/awesome-agent-skills](https://github.com/skillmatic-ai/awesome-agent-skills) - General Agent Skills directory.
- [skills.sh](https://skills.sh) - Skill registry with install counts; the numbers quoted above come from here.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Short version: one line per entry in the right category, run `python scripts/l0_check.py readme README.md`, and if you are adding a skill you maintain, copy [`template/evals/`](template/evals/) into it so it can climb the ladder.

## License

[CC0 1.0](LICENSE).
