# Awesome Hardware Skills [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

*[English](README.md) · 简体中文*

> 让 AI 编程 Agent（Claude Code、Codex、Cursor、OpenClaw 等）构建、烧录、调试和控制物理硬件的 Skill、MCP server、端侧 Agent 运行时、模拟器、评测基准与 CI 基础设施——并配一套验证阶梯，让你能分辨哪些是真的能在板子上跑起来的。

大多数"awesome MCP"列表只告诉你某个硬件 server **存在**。这份列表还追踪有没有人证明过它能用：每个 Skill 条目都可以带上三级阶梯的徽章——静态检查、模拟器预检、在真实板子上运行——而且**只有在真实板子上运行才算通过**。阶梯的含义见下面第一节。

配套文件 [GAPS.zh-CN.md](GAPS.zh-CN.md) 追踪的是**尚不存在**的东西——每条空白都附上核查证据、现存最接近的东西（好让这条声明可被证伪），以及带有 eval 断言的、范围明确的首次贡献建议。

快照时间：2026-09-18。星数、最近推送时间以及 skills.sh / ClawHub 的安装量均取自当天。`stale` 表示 12 个月以上没有推送；`official` 表示仓库位于硬件或 SDK 厂商自己的 GitHub 组织下。

> 本文档译自 [README.md](README.md)。如两者有出入，以英文版为准。

更喜欢表格？[CATALOG.zh-CN.md](CATALOG.zh-CN.md) 把同样的条目按分类做成了表格，标签、星数和最近更新各占一列。它由本文件自动生成。

## 目录

- [条目如何验证](#条目如何验证)
- [Skills](#skills)
  - [MCU / 嵌入式](#mcu--嵌入式)
  - [RTOS](#rtos)
  - [MicroPython / CircuitPython](#micropython--circuitpython)
  - [嵌入式 Rust](#嵌入式-rust)
  - [厂商 SDK](#厂商-sdk)
  - [SBC / Linux](#sbc--linux)
  - [机器人](#机器人)
  - [无人机](#无人机)
  - [航空航天](#航空航天)
  - [边缘 AI / NPU](#边缘-ai--npu)
  - [EDA / PCB](#eda--pcb)
  - [FPGA / HDL](#fpga--hdl)
  - [无线](#无线)
  - [硬件安全](#硬件安全)
  - [汽车](#汽车)
  - [工业 / PLC](#工业--plc)
  - [专业 AV 与楼宇系统](#专业-av-与楼宇系统)
  - [实验室仪器](#实验室仪器)
  - [数字制造](#数字制造)
  - [智能家居](#智能家居)
- [MCP server 与桥接](#mcp-server-与桥接)
- [Agent 协议与端侧运行时](#agent-协议与端侧运行时)
- [验证基础设施](#验证基础设施)
- [评测基准](#评测基准)
- [论文与文章](#论文与文章)
- [Agent 友好文档（llms.txt）](#agent-友好文档llmstxt)
- [空白](#空白)
- [相关列表](#相关列表)

## 条目如何验证

一个 Skill 只有在它的任务于真实板子上运行、且每一条断言都成立时，才算通过。静态检查和模拟器有助于尽早发现问题，但两者都永远不算通过：一个没有建模电源管理芯片、射频或闪存时序的模拟器，会放行那些在真实芯片上出错的固件。所以这份列表是一套由若干预检通往唯一一项真正算数的测试的阶梯。

**`L0`** —— 结构正确。SKILL.md frontmatter 合法、description 具体到足以稳定触发、不含密钥、链接可达、`evals/` 包结构正确。目前由 CI 中的 `scripts/l0_check.py` 强制执行。这是预检，不是通过。

**`L1 (wokwi)`** —— 模拟器预检。模拟器能评估的那些断言在指定模拟器（Wokwi、Renode、`native_sim` 等）中通过，由本仓库的 CI 运行。它能在有人动用板子之前拦下问题，但永远不算通过。即将推出。

**`L2 ×N`** —— **通过。** 先在板子上验证了 eval 本身——参考方案通过、空工程上每条断言都失败、故意写错的方案与伪造固件都被抓住——然后每个任务在真实板子上最多三次运行中有两次通过；每次运行前 eval 都不在 Agent 可触及范围内、主机与板子都已复位，且每一条断言都成立，包括模拟器会跳过的那些。测试者提交背书，附上全部运行记录、两次通过的测试台自检、芯片唯一 ID 与串口日志。`×N` 统计的是来自不同的人、不同芯片的背书数量。Wokwi、Chiplab 这类托管的虚拟板不算；远程烧录真实板子的设备农场算。

**`ΔPass +42%`** —— 同一模型下、在真实板子上、每组每个任务交替运行五次测得的，装了 Skill 与不装 Skill 的任务通过率之差，发布时附 95% 置信区间和 `gain`、`harm`、`low-gain` 或 `inconclusive` 标签，以免把噪声当成证据。它用来说明这个 Skill 确实携带了模型原本不具备的知识。即将推出。

**`stale`** —— 最近一次通过的背书已超过 12 个月，或该 Skill 的任务在背书之后发生了变化，或上游 12 个月没有推送。

任务的断言针对的是脚本可观测的物理副作用（串口输出、GPIO 跳变、总线抓包、ROS topic、HTTP 探测），绝不是"代码看起来对"。完整的测试方案——每个阶段的具体步骤、每种断言在真实板子上怎么测、运行记录格式以及审核标准——见 [EVALS.zh-CN.md](EVALS.zh-CN.md)。

截至本次快照，列表中有一个 Skill 提供了 `evals/` 包，处于 `L0`。**列表中还没有任何 Skill 通过**，因为通过需要有人在板子上把任务跑一遍。如果你手上有下面某块板子，这就是你能做的最有价值的贡献。

想自己做一个带 eval 包的 Skill，或者在自己的板子上测试某个 Skill，可以安装 [hardware-skill-creator](skills/hardware-skill-creator/README.zh-CN.md)。它是本仓库里的一个 Agent Skill，作用相当于硬件版的 Claude skill-creator。在 Claude Code 中输入：

```
/plugin marketplace add chopinfeng/awesome-hardware-skills
/plugin install hardware-skill-creator@awesome-hardware-skills
```

它的 README 说明了怎么使用，以及怎么提交结果：收录 Skill 发 Pull Request，阶段 0 提交到 Skill 自己的仓库，板上测试则提交运行记录并开一个背书 issue。

## Skills

采用 [Agent Skills](https://agentskills.io) 格式的条目：一个包含 `SKILL.md`（frontmatter 含 `name` 与 `description`）的目录，可选 `references/` 和 `scripts/`。可安装进 Claude Code、Codex、Cursor 等。`coll` 表示这是多个 Skill 的合集；仓库名后面的路径指向 monorepo 中的某一个 Skill。同一分类内按有用程度排序，而非星数——一个恰好包含一个小 Skill 的 1.5 万星 monorepo，不应该排在一个专注的 50 星仓库前面。

厂商官方 Skill 就地标注 `official`。截至本次快照，它们来自 NVIDIA、乐鑫、Adafruit、矽递、M5Stack、Arm、瑞萨、德州仪器、博流、安信可、思澈、合宙、LilyGO、RT-Thread、小米 Vela、涂鸦、嘉立创 EDA、Hailo、地平线、D-Robotics、Luxonis、Intel、Google、Meta、Pollen、智元、Wandelbots、Viam、PX4、Matter SDK、Home Assistant、SmartThings、Z-Wave JS、Meshtastic、SimpleBLE、Reolink、Elgato、CSS Electronics、EcuBus、Nominal、Joulescope、DAQiFi、高通、Ångström、openEuler、Anthropic、Nebius、华为昇腾、算能、进迭时空、瑞莎、ADI、NI、MathWorks、Ultralytics、wolfSSL、TOPPERS、华秋、SunFounder、Wendy Labs、Yoe、FaBo、I2RT、Dorna、Cyberwave、PickNik、Tidybot、高德、XLeRobot、Ranch Hand Robotics、GaP、ARK Electronics、Elodin、RAKwireless、Opentrons、Fracktal Works、FLUX、SCADAvis 与 CRCibernetica。MCU 芯片厂商中，只有瑞萨、Arm、德州仪器、乐鑫、博流和思澈在列。

### MCU / 嵌入式

- [Jeffallan/claude-skills `embedded-systems`](https://github.com/Jeffallan/claude-skills/tree/main/skills/embedded-systems) - STM32 / ESP32 / FreeRTOS / 裸机工作流：外设、中断服务程序、DMA、功耗；安装量最高的通用嵌入式 Skill（skills.sh 上约 6000 次）。(★11.5k · 2026-08)
- [hathach/tinyusb `.claude/skills/`](https://github.com/hathach/tinyusb/tree/master/.claude/skills) - `hil` 驱动 TinyUSB 的硬件在环测试台；`target-debug`、`rtt`、`etm-trace`、`usb-sniffer`、`usbmon` 解读目标板上的 USB 协议栈行为。Agent Skill 接真实 HIL 测试台的最佳范例。(coll · ★7.1k · 2026-09)
- [FastLED/FastLED `.claude/skills/`](https://github.com/FastLED/FastLED/tree/master/.claude/skills) - 项目内部但货真价实：ESP-IDF v5 RMT5 驱动专家、ESP32 日志分诊与测试计划 Skill、Xtensa 与 RISC-V 汇编代码审查、时序分析。(coll · ★7.5k · 2026-09)
- [LeoKemp223/embed-ai-tool](https://github.com/LeoKemp223/embed-ai-tool) - 约 25 个自带脚本的 Skill，覆盖整条 MCU 工具链：用 Keil / IAR / CMake / ESP-IDF / PlatformIO 构建，用 OpenOCD / J-Link / idf.py 烧录，用 GDB 调试，另有 CAN、Modbus、VISA 与 RTOS 调试。中文。(coll · ★935 · 2026-08)
- [zhinkgit/embeddedskills](https://github.com/zhinkgit/embeddedskills) - 跨 OpenOCD、J-Link、probe-rs、Keil 与 EIDE 的探针识别、烧录、GDB server、telnet 调试、半主机与 ITM 抓取。中文。(coll · ★685 · 2026-09)
- [DunCanYounG-1/auto-embedded](https://github.com/DunCanYounG-1/auto-embedded) - STM32 / ESP32 / GD32 / MSPM0 开发框架，含 24 个工具 Skill，可注入七种 Agent 平台。中文。(coll · ★243 · 2026-09)
- [Mindrally/skills `embedded-stm32`](https://github.com/Mindrally/skills/tree/main/embedded-stm32) - 由 Cursor rules 演化而来的 STM32 HAL Skill：CubeMX、DMA、SWD 约定。(★259 · 2026-09)
- [mohitmishra786/low-level-dev-skills](https://github.com/mohitmishra786/low-level-dev-skills) - 带数据手册阅读指引的裸机基本功：STM32 裸机、GPIO、UART、I2C/SPI 总线驱动、DMA、Bootloader、OpenOCD/JTAG、嵌入式 Rust、QEMU 仿真、FreeRTOS、Zephyr。(coll · ★216 · 2026-06)
- [SensorsIot/Embedded-AI-Harness `esp-idf-handling`](https://github.com/SensorsIot/Embedded-AI-Harness/tree/main/.claude/skills/esp-idf-handling) - 闭环 ESP-IDF：构建、通过本地 USB 或 RFC2217 远程测试台烧录、监视、OTA、崩溃恢复。少数真正闭合"烧录 → 观测 → 迭代"回路的 Skill 之一。(★177 · 2026-08)
- [Gundry-Consultancy/sbc-mcu-dut-controller `.agent/skills/`](https://github.com/Gundry-Consultancy/sbc-mcu-dut-controller/tree/main/.agent/skills) - 把一套真实 HIL 测试台做成 Skill：`hil-job-api`、`hil-author-test`、`hil-firmware-compare`、`hil-bisect`、`hil-camera-proof`，覆盖 ESP32 / RP2040 / SAMD 烧录、继电器电源与 I2C 复用器。(coll · ★0 · 2026-07)
- [magnus919/agent-skills `esp32-development`](https://github.com/magnus919/agent-skills/tree/main/esp32-development) - 识别 ESP32 板型，在 ESP-IDF、Arduino、MicroPython、CircuitPython、ESPHome、Zephyr、Rust 与 NuttX 之间做选择，接线、烧录、救砖。(★85 · 2026-09)
- [CY-CHENYUE/esp-idf-cy](https://github.com/CY-CHENYUE/esp-idf-cy) - 用国内镜像安装 ESP-IDF，然后构建 → 烧录 → 监视，并带设备命名。(★40 · 2026-07)
- [kukucaiCndy/embedded_ai_skills](https://github.com/kukucaiCndy/embedded_ai_skills) - ESP32（IDF 与 Arduino）、STM32 与 Nordic NCS 的"环境搭建 / 工程初始化 / 调试"三件套，另含 ZMK 键盘与嘉立创 EDA 绘图 Skill。(coll · ★54 · 2026-07)
- [ezrover/ESP32-AI-Agent-Skill](https://github.com/ezrover/ESP32-AI-Agent-Skill/tree/main/skills/esp32) - 选型（S3 / C3 / C6）、PSRAM 与 MMU 注意事项、GPIO12 启动引脚陷阱、ESP-IDF 与 PlatformIO 配置、LVGL 与微雪屏幕资料。(★37 · 2026-08)
- [easyzoom/aix-skills](https://github.com/easyzoom/aix-skills) - 偏集成的 MCU Skill：ESP-IDF、STM32 HAL/LL、FreeRTOS 内核调试、FreeRTOS+TCP、OpenOCD / J-Link / ST-Link。(coll · ★33 · 2026-07)
- [JasonYANG170/esp-dev-skill](https://github.com/JasonYANG170/esp-dev-skill) - 乐鑫每个仓库一个子 Skill：esp-idf、arduino-esp32、esp-adf、esp-dl、esp-zigbee-sdk、esp-at、esp-brookesia、esp-claw、connectedhomeip。(coll · ★27 · 2026-08)
- [ylongw/embedded-review](https://github.com/ylongw/embedded-review) - 针对中断、RTOS 与内存问题的双模型固件审查；ClawHub 约 1800 次安装。(★48 · 2026-03)
- [EricSun787/stm32-development-workflow](https://github.com/EricSun787/stm32-development-workflow) - STM32CubeCLT 命令行流程：工具链、HAL、构建、ST-Link 烧录、常见报错修复。中文。(★25 · 2026-02)
- [wedsamuel1230/arduino-skills](https://github.com/wedsamuel1230/arduino-skills) - 30 个 Arduino 与创客 Skill：代码生成、arduino-cli、串口监视、引脚分配、I2C 上电诊断、接线安全检查、功耗预算、BOM、OTA 守卫。(coll · ★21 · 2026-08)
- [claudius-ars/embedded-agent-skills `gpio-config`](https://github.com/claudius-ars/embedded-agent-skills/tree/main/embedded-agent-skills/gpio-config) - 树莓派（设备树 overlay、config.txt）与 ESP32（sdkconfig）的 GPIO / I2C / SPI / UART / PWM 引脚分配与冲突检查。(★19 · 2026-02)
- [alexex1993/mcu-skills](https://github.com/alexex1993/mcu-skills) - 一板一 Skill（共 19 个）：RP2040 Pico、RP2350、ESP32-WROOM 30/36/38 脚、ESP32-S3-CAM、ESP32-C6、ESP32-P4、nRF52840 ProMicro、STM32F411 BlackPill、STM32H750、ATmega328P Nano、ESP8266——引脚图、外设、供电。(coll · ★17 · 2026-09)
- [Loclove/Electronics-Design-Competition-Skill-2](https://github.com/Loclove/Electronics-Design-Competition-Skill-2) - 全国大学生电子设计竞赛（电赛）单片机 Skill，含 agents 与参考资料。(★14 · 2026-07)
- [o2scale/electronics-agent-kit](https://github.com/o2scale/electronics-agent-kit/tree/main/.agent/skills) - 面向 Arduino、ESP-IDF 与 STM32 的 PlatformIO 工程 / 配置 / 调试，外加 kicad-cli 与 KiCad 文件格式 Skill。(coll · ★12 · 2026-02)
- [grumat/glossy-msp430 `.claude/skills/`](https://github.com/grumat/glossy-msp430/tree/master/.claude/skills) - 解码 MSP430 JTAG 逻辑分析仪抓包并跑单元测试；目前找到的唯一 TI MSP430 Skill。(coll · ★15 · 2026-07)
- [varo6/reTerminal-sticky-skill](https://github.com/varo6/reTerminal-sticky-skill/tree/main/skills/sticky-device) - 矽递 reTerminal Sticky（ESP32-S3 墨水屏）：引脚映射、ESP-IDF 写法、电子纸刷新规则。(★7 · 2026-08)
- [BlueAndi/Pixelix `.github/skills/`](https://github.com/BlueAndi/Pixelix/tree/master/.github/skills) - 面向 ESP32 固件的 MISRA 风格嵌入式 C++14 规约，以 GitHub Copilot skill 形式提供。(copilot · ★443 · 2026-09)
- [fxp/m5stack-embedded-dev-skill](https://github.com/fxp/m5stack-embedded-dev-skill) - 以 Arduino + M5Unified 为先的 M5Stack/ESP32 Skill：板型到 FQBN 的对照表、按芯片代际区分的 GPIO 安全规则、I2C 与 PMIC 的坑、FreeRTOS 与中断规则、崩溃分诊；自带 `serial_match` / `exit_code` 断言的 evals 包，已在本地通过 L0。新项目、尚无星标——收录它是因为 evals 包的形态，而非过往记录。(★0 · 2026-09)
- [PatrickJS/awesome-cursorrules `embedded-stm32-hal`](https://github.com/PatrickJS/awesome-cursorrules/blob/main/rules/embedded-stm32-hal.mdc) - 是 Cursor rule 而非 Skill：STM32 HAL 上的嵌入式 C/C++、中断、DMA 与内存约束规范。(cursor-rules · ★40.8k · 2026-05)
- [rovinax/embedded-skills](https://github.com/rovinax/embedded-skills) - 六个固件工程 skill，强制分层 APP→MODULE→INTERFACE→BSP→PLATFORM 架构，涵盖 C 代码规范、驱动/RTOS/ISR 设计与文档，面向 STM32、GD32、ESP32、RP2040、NXP 与 Nordic。(coll · ★8 · 2026-05)
- [full-stack-skills/firmware-skills](https://github.com/full-stack-skills/firmware-skills) - 二十个可验证的固件 Agent Skill，分为 OpenWrt 网关和 ESP32（esp32-idf、freertos、ota、secureboot、wifi-provision）两大族，外加 toolchain/emulation/HIL 与发布门禁，可用 npx skills 安装。(coll · ★1 · 2026-09)
- [Sonder4/STM32-BFD-Kit](https://github.com/Sonder4/STM32-BFD-Kit) - 以 CLI 为主的 STM32F4/H7 调试工具包，含约 16 个 Claude 与 Codex skill，覆盖 IOC 解析、CubeMX 代码生成、ST-Link/J-Link 烧录、RTT 日志、寄存器/故障采集与调试编排。(coll · ★27 · 2026-05)
- [laurigates/mcu-tinkering-lab](https://github.com/laurigates/mcu-tinkering-lab) - 二十多个 .claude skill，涵盖 ESP-IDF 环境搭建、build/flash/monitor、esp32 调试、sdkconfig 审计、wifi-sta 配置与固件评审，面向 ESP32、Arduino 与 STM32 工程。(coll · ★7 · 2026-09)
- [su5176/Mklink-AI-Probe](https://github.com/su5176/Mklink-AI-Probe) - 面向 Cortex-M 的一体化调试 CLI，把 MKLink/MicroLink 探针桥接给 agent，提供可安装的 SKILL.md 完成固件烧录、RTT/SystemView、内存/寄存器访问、HardFault 与 Modbus，支持 MCP。(★37 · 2026-09)
- [HermeticOrmus/LibreEmbed-Claude-Code](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code) - 十五个面向嵌入式的 Claude Code 插件，包含 ARM Cortex-M、裸机、bootloader 设计、通信总线、调试/跟踪、固件升级与嵌入式测试等模式 skill。(coll · ★47 · 2026-05)
- [AmethystLuna/embedded-workbench](https://github.com/AmethystLuna/embedded-workbench) - 嵌入式 C/C++ 插件，含固件开发、FreeRTOS、Keil MDK 构建、HardFault 定位、状态机设计与调试方法论等 skill。(coll · ★12 · 2026-09)
- [captainluzik/oh-my-embedded](https://github.com/captainluzik/oh-my-embedded) - 面向嵌入式工程的 OpenCode 插件，含 embedded-engineer、firmware-debugger、circuit-simulator、component-sourcer 与 pcb-designer 等 skill，覆盖 ESP32、STM32 与 FreeRTOS。(coll · ★26 · 2026-03)
- [shangliny10-lab/embedded-skills](https://github.com/shangliny10-lab/embedded-skills) - 八个面向学习的嵌入式 skill，涵盖 STM32、Arduino/ESP32、FreeRTOS、RT-Thread、Zephyr、通信协议、嵌入式 Linux 与调试，附可运行示例。(coll · ★17 · 2026-09)
- [0xchaihu/mcu-debug-probe](https://github.com/0xchaihu/mcu-debug-probe) - 基于 pyOCD 的 SWD/JTAG 探针控制 skill，让终端 agent 在不打开完整 IDE 的情况下检查 Cortex-M、烧录镜像、复位 MCU 并读取寄存器/内存。(★12 · 2026-08)
- [BakeSheep/EmberProbe-MCU-Flash-Debug](https://github.com/BakeSheep/EmberProbe-MCU-Flash-Debug) - 基于 OpenOCD 的 Cortex-M VS Code 扩展，附带九个 agent skill，涵盖芯片信息、CubeMX 代码生成、烧录、调试控制、ELF 分析、故障分析与外设调试。(coll · ★5 · 2026-09)
- [ripred/arduino-cli-skills](https://github.com/ripred/arduino-cli-skills) - 模块化的 Arduino CLI skill 集合，含路由式 suite skill，覆盖板卡操作、core/库管理、sketch/profile 工作流、编译上传与调试/监控，附真实命令记录。(coll · ★4 · 2026-06)
- [bahaabdelwahed/embedded-claude-plugin](https://github.com/bahaabdelwahed/embedded-claude-plugin) - STM32 固件插件，含 5 个 agent 与 9 个 skill，覆盖外设配置、内存布局、RTOS 模式、启动/调试配置、安全分析、ST 数据手册提取与 STM32 代码评审。(coll · ★5 · 2026-03)
- [xentron-bit/stm32-embedded-skill](https://github.com/xentron-bit/stm32-embedded-skill) - STM32 开发 skill，覆盖裸机、Keil RTX5/CMSIS-RTOS2 与 FreeRTOS，含 I2C/SPI/UART/FDCAN、QSPI/OCTOSPI、UDS ISO14229、J1939 与 Modbus RTU 参考文档。(★4 · 2026-07)
- [clolckliang/embedded-agent-skillpac](https://github.com/clolckliang/embedded-agent-skillpac) - 通用嵌入式框架知识 SkillPack，为 Claude Code、Codex、opencode 等提供适配器，避免 agent 混淆 FreeRTOS/POSIX 或裸机/Linux GPIO 约定。(coll · ★2 · 2026-04)
- [zc110747/MCU-Agent](https://github.com/zc110747/MCU-Agent) - 研究 AI agent 做真实 MCU 工程的项目，含 .workbuddy skill：ESP-IDF Windows 构建、ESP32 cortex 调试、STM32 Keil 移植、CMSIS-DAP 探针、外设驱动与 Zephyr-STM32 移植。(coll · ★2 · 2026-09)
- [shark0304/personal-embeded-debug-skill](https://github.com/shark0304/personal-embeded-debug-skill) - 以证据为先的嵌入式调试工作台，把固件故障转化为项目记忆、调试数据包、排序假设与可验证修复，含 10 种项目适配器。(★3 · 2026-07)
- [CRCibernetica/espressif-ideaboard](https://github.com/CRCibernetica/espressif-ideaboard) - CRCibernetica IdeaBoard 的原生 ESP-IDF C 固件，附一个 agent skill，讲解该板、ESP-IDF 工作流、引脚图、已验证外设代码与跨平台安装。(official · ★0 · 2026-09)
- [Open-CMSIS-Pack/cmsis-skills](https://github.com/Open-CMSIS-Pack/cmsis-skills) - Open-CMSIS-Pack 组织下社区维护的 CMSIS skill，覆盖 MCU 工程创建（CMSIS 与 Zephyr）、板卡 bring-up、pyOCD 调试/跟踪拓扑、软件包调试序列、Ethos-U 评估与 csolution CI。(coll · ★2 · 2026-09)
- [yukina0079/ai-mcu-auto-debug](https://github.com/yukina0079/ai-mcu-auto-debug) - 面向 AI agent 的 MCU 自动调试工具链，用适配器把 CMake、Keil、ESP-IDF、OpenOCD、J-Link、pyOCD 与 probe-rs 统一暴露为 CLI、Python API、MCP 工具与可安装 skill。(★2 · 2026-07)
- [pedrominatel/esp-workshops](https://github.com/pedrominatel/esp-workshops) - 工作坊仓库，含 esp-idf agent skill，覆盖 ESP-IDF 构建、组件管理、esp-sr 语音识别与 ESP-IDF v6 迁移。(★3 · 2026-06)
- [H1D/agent-skills-esp32](https://github.com/H1D/agent-skills-esp32) - 两个通过 USB 串口调试 ESP32 与嵌入式设备的 agent skill：实时串口日志监控，以及发送串口命令模拟按键。(★9 · 2026-01)

### RTOS

- [beriberikix/zephyr-agent-skills](https://github.com/beriberikix/zephyr-agent-skills) - 最完整的 Zephyr 目录（21 个 Skill）：基础、板级 bring-up（HWMv2）、设备树、构建系统、内核、BLE / IP / USB / CAN 连接、IoT 协议、多核、`native_sim`、功耗、安全更新、存储、测试；一个按关键词 / Kconfig / compatible 打分的路由器负责挑选。(coll · ★64 · 2026-05)
- [ksachdeva/zephyr-rtos-ai](https://github.com/ksachdeva/zephyr-rtos-ai/tree/main/skills) - 25 个按子系统划分的 Zephyr API Skill：BLE（GAP 角色、GATT、配对、NUS）、设备树、Kconfig、GPIO、I2C、SPI、UART、中断、线程、同步、电源管理、settings、存储、socket、Wi-Fi、状态机框架、shell、测试、内存。(coll · ★23 · 2026-06)
- [a5c-ai/babysitter `embedded-systems`](https://github.com/a5c-ai/babysitter/tree/main/library/specializations/embedded-systems/skills) - 29 个短 Skill：Zephyr、FreeRTOS、Nordic nRF、STM32 HAL、Cortex-M、JTAG/SWD、链接脚本、CAN、USB 协议栈、OTA、电机控制、MISRA、Unity/Ceedling。广度优先，深度不足。(coll · ★1.8k · 2026-09)
- [RT-Thread/rtthread-skills](https://github.com/RT-Thread/rtthread-skills) - RT-Thread 官方 Skill：创建 BSP、创建软件包、env 配置、代码审查、精简、Git 工作流。(official · coll · ★3 · 2026-07)
- [open-vela/.claude](https://github.com/open-vela/.claude) - 小米 Vela（NuttX）设备开发：驱动开发、构建、Kconfig 调整、内存转储、代码体积、驱动审查、PCM 音频（共 15 个 Skill）。(official · coll · ★5 · 2026-09)
- [chshzh/claude](https://github.com/chshzh/claude) - 27 个 Nordic nRF Connect SDK Skill，覆盖 PRD → 规格 → 编码 → 测试全流程、NCS 3.x 迁移、nRF70 Wi-Fi 吞吐与固件统计、Memfault。(coll · ★0 · 2026-08)
- [gevico/rt-claw `.agents/skills/`](https://github.com/gevico/rt-claw) - 移植与诊断基于 RT-Thread 的端侧 Agent 运行时：平台移植、OSAL 审查、诊断。(coll · ★12 · 2026-06)
- [eduardojvieira/ZPLC `stm32-freertos-developer`](https://github.com/eduardojvieira/ZPLC) - 软 PLC 项目中的 STM32 + FreeRTOS 开发 Skill；唯一一个有实质深度的 FreeRTOS 专项 Skill。(★6 · 2026-09)
- [goliothlabs/golioth-firmware-skill](https://github.com/goliothlabs/golioth-firmware-skill/tree/main/skills/golioth-firmware) - Zephyr、ESP-IDF、NCS 与 ModusToolbox 上的 Golioth SDK：全新接入与存量改造、OTA、六项云服务。(★1 · 2026-03)
- [toppers/asp3_pico_sdk `.claude/skills/`](https://github.com/toppers/asp3_pico_sdk) - RP2350（Cortex-M33 与 Hazard3 RISC-V）上的 TOPPERS/ASP3 RTOS，配 OpenOCD 与 GDB；同系列另有 NXP MCUXpresso 与瑞萨 FSP 移植。日文。(official · ★0 · 2026-09)
- [mssaleh/zephyr-ai](https://github.com/mssaleh/zephyr-ai) - 面向 Zephyr RTOS 的 grounded Claude Code 插件，含 14 个 skill，覆盖 west 构建/烧录、devicetree、Kconfig、驱动/传感器、RTOS 模式、功耗与测试，配合工程级 SQLite 索引与 MCP 工具。(coll · ★0 · 2026-08)
- [solitasroh/rkit](https://github.com/solitasroh/rkit) - 以 PDCA 驱动的 Claude Code 插件，自动识别 MCU/MPU/WPF 领域并激活 FreeRTOS、NXP MCUXpresso、CMake-embedded、MISRA-C、i.MX BSP 与 Yocto/Buildroot 等 skill。(coll · ★2 · 2026-05)
- [toppers/asp3_stm32cube](https://github.com/toppers/asp3_stm32cube) - TOPPERS ASP3 RTOS 针对 STM32Cube 的移植，附一个把 ASP3 移植到 STM32 目标的 skill。(official · ★2 · 2026-09)
- [2939387245/agent-skill_stm32-freertos](https://github.com/2939387245/agent-skill_stm32-freertos) - 用于在 FreeRTOS 上开发 STM32 固件的 agent skill。(★15 · 2026-01)
- [toppers/asp3_mcuxsdk](https://github.com/toppers/asp3_mcuxsdk) - TOPPERS ASP3 RTOS 针对 NXP MCUXpresso SDK 的移植，含 ASP3-MCUXSDK 操作与把 ASP3 移植到 NXP 目标的 skill。(official · ★0 · 2026-09)

### MicroPython / CircuitPython

- [FreakStudioCN/MicroPython_Skills](https://github.com/FreakStudioCN/MicroPython_Skills) - 最大的 MicroPython 合集（60+）：mpremote 操作、固件烧录、部署、按规格生成驱动、选型、接线、仿真。中文。(coll · ★5 · 2026-09)
- [andrewleech/claude-mpy-marketplace](https://github.com/andrewleech/claude-mpy-marketplace) - mpremote 设备交互、文件传输与实时会话 Skill，外加 MicroPython 贡献者 Skill，作者是 MicroPython 核心维护者。(coll · ★2 · 2026-09)
- [m5stack/uiflow-micropython `tools/knowledge-base/`](https://github.com/m5stack/uiflow-micropython/tree/master/tools/knowledge-base) - 面向 UIFlow2 MicroPython 的 `uiflow2-coder` 与 `uiflow2-ui-designer`，内置官方文档。(official · coll · ★208 · 2026-09)
- [adafruit/LLM-Recipes](https://github.com/adafruit/LLM-Recipes/tree/main/circuitpython) - 在已连接的 CircuitPython 板上运行代码、编写并执行硬件测试，并通过对比 Arduino 与 CircuitPython 的总线波形来验证 I2C 驱动。(official · coll · ★3 · 2026-06)
- [adafruit/Adafruit_Learning_System_Guides `embodiment-kit`](https://github.com/adafruit/Adafruit_Learning_System_Guides/tree/main/Embodiment_Kit/agent_skill/embodiment-kit) - 通过 Adafruit IO 驱动 CircuitPython "embodiment kit"（显示屏、NeoPixel、传感器），并带前后传感器读数作为证据。(official · ★1.1k · 2026-09)
- [rockets-cn/unihiker-k10-skills](https://github.com/rockets-cn/unihiker-k10-skills) - DFRobot 行空板 K10 的烧录与 API，覆盖 MicroPython、Arduino 与 PlatformIO，另含 OTA 与编译服务；各约 2000 次 ClawHub 安装。(coll · ★6 · 2026-08)
- [MakerClassCZ/picogame `skills/`](https://github.com/MakerClassCZ/picogame/tree/main/skills) - CircuitPython Pico 板级 bring-up：settings.toml、GPIO、显示。(★25 · 2026-09)
- [Cerwor/jlc-k230-lushan-pi](https://github.com/Cerwor/jlc-k230-lushan-pi) - 嘉立创庐山派 K230 CanMV MicroPython：摄像头、LCD、YOLO、mpremote 部署。(★4 · 2026-09)
- [PyDevices/mpftp](https://github.com/PyDevices/mpftp) - MicroPython/CircuitPython 工具，其基于 MCP 的 board-tools skill 通过真实串口会话完成文件传输、REPL/exec、不打断运行的输出捕获与固件构建/烧录，支持 ESP32、RP2040、SAMD。(★1 · 2026-09)
- [FreakStudioCN/browser-micropython-skills](https://github.com/FreakStudioCN/browser-micropython-skills) - 面向 Blockless Web Builder 的 27 个浏览器原生 MicroPython skill，覆盖设备串口部署、分析、自动修复、绘图与文档抓取，无需本地 shell。(coll · ★1 · 2026-07)
- [zhoushoujianwork/lvgl-preview-skill](https://github.com/zhoushoujianwork/lvgl-preview-skill) - 用于设计嵌入式 LVGL（MicroPython）UI 的 Claude Code skill，采用无头渲染成 PNG 的反馈回路，自动适配 LVGL 8.x/9.x，让 agent 无需硬件即可看到并自我修正 UI。(★3 · 2026-05)
- [johnlindquist/badger-2350-plugin](https://github.com/johnlindquist/badger-2350-plugin) - 面向 Universe 2025（Tufty）徽章的 Claude Code 插件，含八个 skill，包括 micropython-repl 以及徽章硬件、部署、诊断与 MonaOS 应用创建。(coll · ★8 · 2025-10)

### 嵌入式 Rust

- [actionbook/rust-skills `domain-embedded`](https://github.com/actionbook/rust-skills/tree/main/skills/domain-embedded) - `no_std`、Embassy 与 RTIC 约束，并自动注入 `.cargo/config.toml`；约 2400 次安装，是安装量最高的嵌入式 Rust Skill。另有姊妹 Skill `domain-iot`。(★1.5k · 2026-08)
- [OutlineDriven/odin-claude-plugin `odin-native`](https://github.com/OutlineDriven/odin-claude-plugin/tree/main/plugins/odin-native/skills) - 基于 cortex-m-rt / probe-rs / defmt / RTIC 的固件开发，外加 OpenOCD JTAG、FreeRTOS 与 QEMU 跑内核的 Skill。(coll · ★37 · 2026-09)
- [ch32-rs/ch32-rs `.claude/skills/`](https://github.com/ch32-rs/ch32-rs) - 把厂商 SVD 转成沁恒 RISC-V 芯片的 PAC crate。(★170 · 2026-05)
- [hispark-rs/hisi-riscv-rs `.agents/skills/`](https://github.com/hispark-rs/hisi-riscv-rs) - `hil-smoke` 与 `hil-regression`：烧录真实海思 ws63 板、读串口、断言特征字符串。(coll · ★3 · 2026-09)
- [bitscrafts/EFR32MG2X-RS](https://github.com/bitscrafts/EFR32MG2X-RS) - Silicon Labs EFR32MG24 的 Rust HAL 专家 Skill。(★6 · 2026-06)
- [Microbiosis/esp-rust-skills](https://github.com/Microbiosis/esp-rust-skills) - esp-hal 外设、Wi-Fi / BLE / ESP-NOW、工具链。中文。(coll · ★1 · 2026-06)
- [full-stack-skills/rust-skills](https://github.com/full-stack-skills/rust-skills) - Rust 语言 skill 集合，其中 rust-embedded skill 提供 golden no_std 示例、HAL/并发参考与裸机固件的硬件验证指南。(coll · ★5 · 2026-09)
- [psytraxx/esp32-homecontrol-no-std-rs](https://github.com/psytraxx/esp32-homecontrol-no-std-rs) - no_std Rust 的 ESP32 自动浇水固件，附带 esp32-rust-embedded skill，讲解在真实硬件上使用 esp-hal 的 async no_std 工作流。(★3 · 2026-09)
- [njfdev/ncssm_hpr_2025_payload](https://github.com/njfdev/ncssm_hpr_2025_payload) - 火箭载荷固件，含基于 Embassy 的 skill（embassy、embassy-rp、pico-tooling、pico-logger），用于在 RP2040/RP2350 飞控上做 async no_std 开发。(coll · ★2 · 2026-04)
- [chrisprice/embassy-rp2040-harness](https://github.com/chrisprice/embassy-rp2040-harness) - 面向 Embassy RP2040 固件的 agent harness，含 embassy 最佳实践、项目结构、新项目脚手架、pico-firmware 与项目评审等 skill。(coll · ★0 · 2026-04)
- [hkjolhede/embassy_copilot](https://github.com/hkjolhede/embassy_copilot) - Embassy 的全系统设计撰写 skill，指导使用 embassy-executor、embassy-time 与 embassy-sync 的 async no_std 架构。(★0 · 2026-03)

### 厂商 SDK

- [Open-CMSIS-Pack/CMSIS-Developer-Assistant](https://github.com/Open-CMSIS-Pack/CMSIS-Developer-Assistant) - Arm 的 CMSIS Skill 外加一个 MCP：bring-up、实时调试、pack 与工程创建、Cortex-M 板级层。(official · coll · ★2 · 2026-09)
- [TexasInstruments/C2000-IDEA `docs/skills/c2000-idea`](https://github.com/TexasInstruments/C2000-IDEA/tree/main/docs/skills/c2000-idea) - F28x 器件迁移分四份参考文档推进、位域到 driverlib 的转换、SysConfig ePWM 迁移；驱动本地 `idea-mcp` 端点以及 CCS Project、SysConfig 与 TI 汇编 MCP server。第三家发布宿主侧 Skill 的芯片厂商。(official · ★21 · 2026-09)
- [renesas/renesas-skills](https://github.com/renesas/renesas-skills) - `configure-renesas-debug` 为 J-Link / E2 / E2Lite / IECUBE 生成 VS Code launch.json；除 Arm 外唯一的芯片厂商 Skill 仓库。(official · ★6 · 2026-07)
- [bouffalolab/bouffalo_sdk `.agents/skills/`](https://github.com/bouffalolab/bouffalo_sdk/tree/master/.agents/skills) - 博流 SDK 开发指南，覆盖 BL602 / BL616 / BL808，另有变更日志与测试手册 Skill。(official · coll · ★501 · 2026-09)
- [bouffalolab/bouffalolab-skills](https://github.com/bouffalolab/bouffalolab-skills) - 博流的第二个 Skill 仓库：BL616 低功耗 IO 指南与 Wi-Fi 低功耗采集。(official · ★0 · 2026-09)
- [Ai-Thinker-Open/skills](https://github.com/Ai-Thinker-Open/skills) - 安信可模组 Skill（14 个）：Ai-M62/M61（BL616）、Ai-WB2（BL602）、Ra-01SC LoRa、coredump、OTA 生成、选型；配套还有 FlashKey MCP 烧录调试设备。(official · coll · ★9 · 2026-09)
- [Ai-Thinker-Open/FlashKey-skills](https://github.com/Ai-Thinker-Open/FlashKey-skills) - FlashKey 烧录调试设备的 Skill，搭配 `emMCP` 这个 UART 转 MCP 的协议生成库。(official · ★0 · 2026-08)
- [OpenSiFli/SiFli-SDK `skills/`](https://github.com/OpenSiFli/SiFli-SDK/tree/main/skills) - 思澈 SF32 蓝牙 SoC：Windows 构建、代码审查、崩溃转储分诊、USB 寄存器转储分析。(official · coll · ★182 · 2026-09)
- [OpenSiFli/SiFli-Skills](https://github.com/OpenSiFli/SiFli-Skills) - 思澈独立的 Skill 仓库，与 SDK 内那套分开维护。(official · ★1 · 2026-09)
- [openLuat/LuatOS `skill-packs/`](https://github.com/openLuat/LuatOS/tree/master/skill-packs) - 合宙 LuatOS Lua 固件（Air780 / Air101）：覆盖 72 个核心库的开发、文档与示例规格 Skill。(official · coll · ★590 · 2026-09)
- [Xinyuan-LilyGO/lilygo-skills](https://github.com/Xinyuan-LilyGO/lilygo-skills) - LilyGO T-Display / T-Watch / T-Beam 的引脚图与 Arduino / IDF / SF32 构建，前面挂一个路由 Skill。(official · ★6 · 2026-07)
- [tuya/TuyaOpen-dev-skills](https://github.com/tuya/TuyaOpen-dev-skills) - TuyaOpen 固件闭环：环境搭建、工程配置、构建、调试助手、开发循环、设备授权、新增板型、CLI 调试、崩溃解析。(official · coll · ★16 · 2026-07)
- [espressif/esp-claw-skills-lab](https://github.com/espressif/esp-claw-skills-lab) - 乐鑫第一个真正的 Skill 仓库，但是端侧的：43 个 SKILL.md 加 Lua 脚本，由 esp-claw 运行时在 ESP32 上执行（JSON frontmatter，并非 agentskills.io 格式）。(official · coll · ★33 · 2026-09)
- [espressif/skills](https://github.com/espressif/skills) - 乐鑫的宿主侧 Skill 仓库，2026-04 创建，README 里写着可用 `npx skills add espressif/skills` 安装——至今没有任何 SKILL.md。(official · placeholder · ★2 · 2026-04)
- [arm/agent-resources](https://github.com/arm/agent-resources) - Arm 的 Agent 资源注册表——schema、校验器和四个注册表 YAML，但还没有 SKILL.md。第二个厂商占位仓库。(official · ★0 · 2026-09)
- [0xchaihu/nxp-mcu-build-verify](https://github.com/0xchaihu/nxp-mcu-build-verify) - 用命令行构建 IAR、Keil、MCUXpresso IDE 与 VS Code MCUX 工程。(★28 · 2026-04)
- [JasonYANG170/ch57x-dev-skill](https://github.com/JasonYANG170/ch57x-dev-skill) - 沁恒 CH57x 蓝牙固件。(★12 · 2026-06)
- [ClarkJ-Infineon/mtb-workspace-template `.github/skills/`](https://github.com/ClarkJ-Infineon/mtb-workspace-template/tree/main/.github/skills) - 英飞凌工程师个人仓库里的 19 个 ModusToolbox Copilot Skill：BLE 配置、Wi-Fi MQTT、OpenOCD 调试、双核、PSoC 6 到 Edge 的迁移、雷达 DSP。(copilot · coll · ★0 · 2026-05)
- [ailyProject/aily-blockly `public/skills/`](https://github.com/ailyProject/aily-blockly) - aily Arduino AI IDE 的 Blockly 最佳实践与库迁移 Skill。(coll · ★3.8k · 2026-09)
- [espressif/esp-dl](https://github.com/espressif/esp-dl) - Espressif 的深度学习库自带 agent skill，覆盖 espdl operator 与量化闭环，以及 ESP32-P4/S3 PIE-SIMD 内核开发。(official · coll · ★1.1k · 2026-09)
- [wolfSSL/wolfHAL](https://github.com/wolfSSL/wolfHAL) - wolfSSL 的轻量级嵌入式硬件抽象层（C 语言），含生成驱动模板与把 HAL 移植到 STM32 平台的 skill。(official · ★21 · 2026-09)
- [bouffalolab/vela-vendor-bouffalolab](https://github.com/bouffalolab/vela-vendor-bouffalolab) - Bouffalo Lab 的 Vela SDK 驱动公开仓库，含 agent skill：模块复位与设计 Bouffalo SDK 到 OpenVela 的移植任务。(official · ★0 · 2026-09)
- [TigerSillion/RenesasMcuMaster](https://github.com/TigerSillion/RenesasMcuMaster) - Renesas RX MCU skill 包，含 rx-uart-mvp skill 与上位机示波器（Qt/WPF）skill，用于 RX 固件 bring-up。(coll · ★0 · 2026-02)
- [water-freemind/rasc-configure-ra](https://github.com/water-freemind/rasc-configure-ra) - 用于安全配置与验证 Renesas RA/FSP configuration.xml 文件的 Codex skill。(★0 · 2026-09)
- [XIAOMANSDK/B6x](https://github.com/XIAOMANSDK/B6x) - 面向 B61/B62/B63/B66（ARM M0+）芯片的蓝牙 LE SDK，含 15 个 skill，覆盖构建、CMake 初始化、工程创建、SRAM/功耗分析、硬件校验与代码评审。(coll · ★10 · 2026-06)

### SBC / Linux

- [NVIDIA-AI-IOT/jetson-device-skills](https://github.com/NVIDIA-AI-IOT/jetson-device-skills) - `jetson-diagnostic`、`jetson-memory-audit`、`jetson-llm-serve`、`jetson-video-*` 等的权威来源，会镜像进 NVIDIA/skills；skills.sh 上安装量最高的硬件 Skill。(official · coll · ★141 · 2026-08)
- [NVIDIA-AI-IOT/jetson-bsp-skills](https://github.com/NVIDIA-AI-IOT/jetson-bsp-skills) - `jetson-customize-*` 系列 BSP Skill 的权威来源：pinmux、PCIe、USB、时钟、风扇、载板衍生、镜像校验与烧录。(official · coll · ★60 · 2026-06)
- [D-Robotics/moss `jetson-knowledge`](https://github.com/D-Robotics/moss) - Orin / Xavier 规格、JetPack / L4T、Super Mode、TensorRT engine 构建，同仓库还有 D-Robotics RDK 的 Skill。(coll · ★142 · 2026-09)
- [Seeed-Projects/Seeed-Jetson-DevelopTool](https://github.com/Seeed-Projects/Seeed-Jetson-DevelopTool/tree/main/skills/openclaw) - 矽递 reComputer / Jetson 支持 Skill：JetPack 概览、Docker 配置、AI 工具、L4T 版本差异、Jetson 上跑 YOLO、FAQ。(coll · ★56 · 2026-09)
- [sammcj/agentic-coding `raspberry-pi-pico2`](https://github.com/sammcj/agentic-coding/tree/main/Skills/raspberry-pi) - RP2350 配 Debug Probe：pico-sdk CMake、ARM 与 RISC-V、picotool、OpenOCD / GDB / RTT 资料。(★161 · 2026-09)
- [irfanmuhammedharis/raspberry-pi-skills-suite](https://github.com/irfanmuhammedharis/raspberry-pi-skills-suite) - 唯一一套覆盖面较广的树莓派合集：Pico MicroPython 与 C SDK、GPIO 传感器与执行器、Linux 配置、调试、边缘 AI 视觉、网络、机器人、供电。偏薄（每个约 3 KB）。(coll · ★0 · 2026-03)
- [TheYoctoJester/dutler](https://github.com/TheYoctoJester/dutler) - 把 Pico 当作板卡农场的 USB 串口控制台桥与电源继电器，配 `run-dutler` Skill。(★22 · 2026-07)
- [qualcomm-linux/qcom-linux-skills](https://github.com/qualcomm-linux/qcom-linux-skills) - 高通 Linux / meta-qcom / Dragonwing 板卡：Yocto 镜像构建、预编译下载、LAVA CI 报告、PR 前检查、Debian 镜像构建。(official · coll · ★6 · 2026-09)
- [prashantdivate/awesome-yocto-ai-agent-skills](https://github.com/prashantdivate/awesome-yocto-ai-agent-skills) - 覆盖最广的 Yocto 合集（12 个）：BSP bring-up、构建调试、kas CI 构建、部署与烧录、镜像分析、内核 BSP、recipe 维护、安全 / OTA / SBOM。(coll · ★4 · 2026-07)
- [Higangssh/yocto-agent-skills](https://github.com/Higangssh/yocto-agent-skills) - 以官方文档为准、经 CI 验证的 Yocto Skill：文档路由、BSP 内核、镜像 rootfs、layer 与 recipe 审查、安全 SBOM。(coll · ★9 · 2026-08)
- [Angstrom-distribution/meta-angstrom `skills/`](https://github.com/Angstrom-distribution/meta-angstrom) - `boot-validate` 在全部十二台 oe-core QEMU 机型加上 BeagleBone QEMU 上启动镜像，并断言 systemd 与网络正常。(official · ★51 · 2026-09)
- [processmission/oh-my-qemu](https://github.com/processmission/oh-my-qemu) - 在 QEMU 中建模板卡与外设：U-Boot 构建、Linux 启动、板级与外设建模（17 个 Skill）。(coll · ★56 · 2026-07)
- [angelwzr/linux-phone-porting](https://github.com/angelwzr/linux-phone-porting) - 在安卓手机上做主线 Linux bring-up：设备树、bootloader。(★49 · 2026-09)
- [LittleNewton/openwrt-compile-skills](https://github.com/LittleNewton/openwrt-compile-skills) - OpenWrt 构建执行器、feed 与软件包同步、切换 target 时的清理规范。(coll · ★8 · 2026-05)
- [100askTeam/aibsp-imx6ull-pro_linux5.4.47 `.trae/skills/`](https://github.com/100askTeam/aibsp-imx6ull-pro_linux5.4.47) - 百问网 i.MX6ULL 的 Buildroot / eMMC / LVGL9 / uuu 串口自动烧录 Skill，TRAE 格式。(official · coll · ★12 · 2026-05)
- [realsenseai/realsense_mipi_platform_driver `.claude/skills/`](https://github.com/realsenseai/realsense_mipi_platform_driver) - 在 Jetson 上构建、部署并验证 RealSense MIPI 内核驱动。(official · coll · ★51 · 2026-09)
- [openharmonyinsight/openharmony-skills](https://github.com/openharmonyinsight/openharmony-skills) - OpenHarmony 源码构建、CI、C++、下载、单元测试、安全审查。(coll · ★34 · 2026-09)
- [anthropics/claude-plugins-official `cwc-makers`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/cwc-makers) - `m5-onboard` 通过 USB 识别 M5Stack Cardputer / Core / CoreS3，烧录 UIFlow 2.0 与一套 MicroPython 包；`cardputer-buddy` 通过串口迭代应用并提供一次性 REPL。(official · coll · ★36.5k · 2026-09)
- [BenGardiner/bitbake-yocto-agent-skills](https://github.com/BenGardiner/bitbake-yocto-agent-skills) - 七个面向 Yocto/BitBake 的 skill：recipe 定位与覆盖、依赖调试、dry-run 诊断、Python 打包以及 qemu 用户态运行。(coll · ★1 · 2026-03)
- [themactep/thingino-skills](https://github.com/themactep/thingino-skills) - 面向 Thingino 开源 IP 摄像头固件的 skill 集：构建与 OTA 部署、NFS 开发部署、U-Boot 补丁流程、设备冒烟循环、诊断采集和 RTSP 压测。(coll · ★5 · 2026-09)
- [sunfounder/pironman5 `skill/`](https://github.com/sunfounder/pironman5/tree/v1/skill) - SunFounder 官方为 Pironman 5 系列树莓派 5 机箱（含 Mini、Max、Pro Max）提供的 skill：调用 pironman5 CLI、修改配置，控制 OLED、RGB 灯、风扇和红外接收器。(official · coll · ★133 · 2026-09)
- [dshanpi/T153MX-Tina5SDK_OmniGate `overlay/skills/`](https://github.com/dshanpi/T153MX-Tina5SDK_OmniGate/tree/main/overlay/skills) - 面向 Tina5 SDK 上 Allwinner T153 OmniGate 板的 skill：串口连接与 FEL/FES 烧录及恢复、C906 AMP/RPMsg 调通、LVGL UI 示例和串口 agent 守护进程。(coll · ★2 · 2026-09)
- [bitshelf/tina_agents](https://github.com/bitshelf/tina_agents) - 两个 Allwinner Tina Linux skill：构建 T527 SDK（内核、U-Boot、Buildroot、RTOS、固件打包），以及用 sunxi-fel 通过 USB FEL 烧录镜像。(coll · ★0 · 2026-07)
- [analogdevicesinc/analog-attach `packages/attach-cli/`](https://github.com/analogdevicesinc/analog-attach/tree/main/packages/attach-cli) - Analog Devices 官方为 attach CLI 编写的 skill，引导 agent 为 ADI 器件配置 Linux 设备树 overlay，包括器件查找、父总线建议和按 schema 校验属性。(official · ★2 · 2026-09)
- [yoebuild/yoe `.claude/skills/`](https://github.com/yoebuild/yoe/tree/main/.claude/skills) - Yoe 嵌入式 Linux 构建系统官方自带的 skill：创建、更新和审计 Starlark unit，拉取 Alpine 软件包以及诊断构建问题。(coll · official · ★61 · 2026-09)
- [D-Robotics/rdk-skills](https://github.com/D-Robotics/rdk-skills) - 地瓜机器人（D-Robotics）官方为 RDK 开发板提供的 skill：BSP 环境搭建，RDK X3/X5 的内核、bootloader、rootfs 与整机镜像构建；面向 RDK X5 与 S 系列的模型量化、编译和板端部署工具链 skill；另含文档检索和具身 LeRobot 应用。(official · coll · ★3 · 2026-09)
- [wendylabsinc/claude-skills](https://github.com/wendylabsinc/claude-skills) - Wendy Labs 官方为 WendyOS 边缘设备提供的 skill：用 wendy CLI 把应用部署到 NVIDIA Jetson 和树莓派、为 ARM64 交叉编译 Swift，以及设备注册与证书管理。(official · coll · ★62 · 2026-09)
- [luckyegg168/openwrt-skill](https://github.com/luckyegg168/openwrt-skill) - 结构化的 OpenWrt 路由器开发 skill，涵盖构建系统、软件包和设备端调试。(★3 · 2026-03)
- [majay123/my-embedded-skills](https://github.com/majay123/my-embedded-skills) - 嵌入式 Linux skill 集：内核驱动与设备树开发、应用开发、内核模块、交叉 GCC 构建以及 strace/ltrace 调试。(coll · ★4 · 2026-06)
- [the78mole/skills `skills/yocto-build-and-flash/`](https://github.com/the78mole/skills/tree/main/skills/yocto-build-and-flash) - 为 MYiR MYD-YF13X（STM32MP135）开发板构建 Yocto myir-image-core 镜像并用 STM32CubeProgrammer 烧录的 skill。(★0 · 2026-07)
- [radxa-docs/skills](https://github.com/radxa-docs/skills) - Radxa 官方 skill：识别 agent 所在的 Radxa 开发板型号，并在做板级操作前对应到正确的产品文档。(official · coll · ★1 · 2026-03)
- [HBConline/orangepi4pro-skill](https://github.com/HBConline/orangepi4pro-skill) - 面向 Orange Pi 4 Pro（Allwinner A733）的 agent skill：嵌入式 Linux、wiringOP GPIO、3 TOPS NPU 和 Android 13 AOSP。(★3 · 2026-06)
- [1nuoiscute/Taishan-RK3566-Skill](https://github.com/1nuoiscute/Taishan-RK3566-Skill) - 面向电赛视觉的泰山派 RK3566 Codex/Claude Code skill，从板端探测到 OpenCV/V4L2、UART/GPIO 和 RKNN 验证。(★5 · 2026-08)
- [FaBoAI/JetsonSkills](https://github.com/FaBoAI/JetsonSkills) - 面向 JetPack 7.2 上 Jetson Orin 的官方安装类 skill：部署 FaBo JetRacer 和 LeRobot 0.6.0（含 SO-101 SDK）、支持 CUDA 的 OpenCV、PyTorch 以及 GPIO/舵机库。(coll · official · ★0 · 2026-08)
- [xzl01/agent-debugboard `skills/radxa-linkr-debugger/`](https://github.com/xzl01/agent-debugboard/tree/main/skills/radxa-linkr-debugger) - Radxa Linkr Debugger 的 skill，通过 USB NCM HTTP 控制目标板供电、ADC 电流监测、GPIO、TF/SD 切换、看门狗恢复和 RP2350 BOOTSEL。(★4 · 2026-09)

### 机器人

- [NVIDIA/skills](https://github.com/nvidia/skills) - 从 NVIDIA 各产品仓库镜像而来的 350+ 个 Skill；硬件相关的集群是 `jetson-*`（BSP 定制、pinmux、烧录、内存审计、端侧 LLM 服务）、`hsb-*`（Holoscan Sensor Bridge FPGA 烧录）、`i4h-*`（Isaac for Healthcare 机器人数据采集与强化学习）以及 `physical-ai-*`。(official · coll · ★3.3k · 2026-09)
- [isaac-sim/IsaacSim `.claude/skills/`](https://github.com/isaac-sim/IsaacSim/tree/main/.claude/skills) - Isaac Sim 的 43 个 Skill：无头部署、ROS 2 桥、URDF/MJCF 转 USD、机械臂 IK、导航原语、占据栅格图、数据采集。(official · coll · ★4.1k · 2026-09)
- [isaac-sim/IsaacLab-Arena `skills/`](https://github.com/isaac-sim/IsaacLab-Arena/tree/main/skills) - 搭建 arena、跑实验，并为闭环评测拉起 π0（`serve-openpi-policy`）或 GR00T（`serve-gr00t-policy`）策略服务。(official · coll · ★571 · 2026-09)
- [google-deepmind/mujoco `doc/skills/`](https://github.com/google-deepmind/mujoco/tree/main/doc/skills) - 六个官方 MuJoCo Skill：python、渲染、加速（MJX / Warp）、spec 编辑、GUI、Studio。(official · coll · ★15.2k · 2026-09)
- [AgibotTech/genie_sim `skills/`](https://github.com/AgibotTech/genie_sim/tree/main/source/geniesim_ros/skills) - 智元的八个 Skill：构建工作区、启动场景、MoveIt 全身控制、从 URDF 添加机器人、遥操作桥、录制 episode、物理调试。(official · coll · ★1.4k · 2026-09)
- [pollen-robotics/reachy_mini `skills/`](https://github.com/pollen-robotics/reachy_mini/tree/main/skills) - AGENTS.md 中引用的 13 个官方 Reachy Mini Skill：创建应用、安全力矩、控制循环、符号化运动、REST API、AI 集成。纯 `.md`，无 frontmatter。(official · coll · ★1.5k · 2026-09)
- [NVIDIA-AI-IOT/reachy-mini-jetson-assistant](https://github.com/NVIDIA-AI-IOT/reachy-mini-jetson-assistant) - 在 Orin Nano 上为 Reachy Mini Lite 做本地语音 + 视觉助手，配 `reachy-jetson-deploy` Skill。(official · ★33 · 2026-09)
- [wandelbotsgmbh/wandelbots-nova `nova-api-v2`](https://github.com/wandelbotsgmbh/wandelbots-nova/tree/main/.agents/skills/nova-api-v2) - Wandelbots NOVA 面向 UR / KUKA / FANUC / ABB / 安川的机型无关运动规划：轨迹规划、限位、模型。(official · ★46 · 2026-09)
- [viam-devrel/agent-skills](https://github.com/viam-devrel/agent-skills) - 九个 Viam Skill：机器配置、模块与机队、本地 viam-server、Python / Go / C++ / TS SDK、机器学习、运动与视觉。(official · coll · ★2 · 2026-08)
- [openvinotoolkit/physicalai](https://github.com/openvinotoolkit/physicalai/tree/main/skills) - Intel 在机器人上运行 VLA 策略的运行时：接入新机型、接入相机后端、配置推理流水线。(official · coll · ★28 · 2026-09)
- [OpenRAL/openral](https://github.com/OpenRAL/openral) - "Robot Agentic Layer"：LLM 发出带类型的工具调用，在默认拒绝的 C++ 安全内核之后派发 rSkill（SmolVLA、π0.5、GR00T、OpenVLA-OFT、MoveIt / Nav2 动作）；含 50 个 rSkill 的 SKILL.md，例如 `rskill-smolvla-so101`。(coll · ★46 · 2026-09)
- [harunkurtdev/ros2-claude-code-template](https://github.com/harunkurtdev/ros2-claude-code-template) - 29 个 ROS 2 Skill，其中八个是 Nav2 相关：代价地图、规划器、控制器、行为树、插件开发。(coll · ★215 · 2026-06)
- [arpitg1304/robotics-agent-skills](https://github.com/arpitg1304/robotics-agent-skills) - 生产级 ROS 1/2 实践：QoS、生命周期节点、colcon、DDS、机器人 bring-up、感知、测试、安全、Docker 开发、Web 集成。(coll · ★362 · 2026-08)
- [dbwls99706/ros2-engineering-skills](https://github.com/dbwls99706/ros2-engineering-skills) - 单个渐进式披露的 Skill：rclcpp / rclpy、QoS / DDS、tf2 / URDF、ros2_control、Nav2、MoveIt 2、实时性、硬件安全。(★176 · 2026-09)
- [adityakamath/ros2-skill](https://github.com/adityakamath/ros2-skill) - 面向运行时控制而非代码生成：通过内置 rclpy 脚本在真实机器人上操作 topic、service、action、参数、生命周期、ros2_control 与 Nav2。(★18 · 2026-07)
- [j3soon/ros2-essentials `.agents/skills/`](https://github.com/j3soon/ros2-essentials) - 面向 AMR 的 TurtleBot3 与 Gazebo 工作区测试 Skill。(coll · ★47 · 2026-09)
- [zh-plus/unitree-g1-dev-copilot](https://github.com/zh-plus/unitree-g1-dev-copilot) - 有文档依据的宇树 G1 Skill：SDK2、DDS、ROS 2、高层与底层运动、D435i 头部相机；自带 `evals/`。(★6 · 2026-07)
- [earthtojake/text-to-cad `urdf` / `srdf` / `sdf`](https://github.com/earthtojake/text-to-cad/tree/main/skills/urdf) - CAD/CAM Skill 库中的机器人描述格式，该库还覆盖 G-code 与拓竹打印机。(coll · ★16.1k · 2026-09)
- [rerun-io/rerun `rerun-lerobot`](https://github.com/rerun-io/rerun/tree/main/skills/rerun-lerobot) - 在 Rerun 中可视化 LeRobot 数据集；同系列还有 `rerun-urdf` 与 `rerun-mcap`。(official · ★11.5k · 2026-09)
- [Flaminis/Dalaran](https://github.com/Flaminis/Dalaran) - Rerun 的替代品，机器人可视化与数据基础设施，带 `dalaran-lerobot` 与 `dalaran-mcap` Skill。(coll · ★760 · 2026-08)
- [nebius/nebius-physical-ai](https://github.com/nebius/nebius-physical-ai) - 38 个与云绑定的 Skill：LeRobot、GR00T、Isaac Lab、Genesis、mjlab、cuRobo、Foxglove、RoboCasa、动作重定向。(official · coll · ★29 · 2026-09)
- [aws-samples/sample-embodied-ai-platform `training/gr00t`](https://github.com/aws-samples/sample-embodied-ai-platform) - 用遥操作数据微调 GR00T 并部署到 SO-101 机械臂。(official · ★15 · 2026-09)
- [NVlabs/RoboLab](https://github.com/NVlabs/RoboLab) - 面向策略评测的场景生成与任务生成 Skill；姊妹项目 [GraspGenX](https://github.com/NVlabs/GraspGenX) 提供抓取生成 Skill。(official · coll · ★505 · 2026-09)
- [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) - 大型通用科研 Skill 库中的 `openpi`、`openvla-oft`、`cosmos-policy` 与 `tensorrt-llm`。(coll · ★12.8k · 2026-06)
- [ForgeCAD/forgecad-public-kit `forgecad-verify-mujoco`](https://github.com/ForgeCAD/forgecad-public-kit) - 在 MuJoCo 中验证由 CAD 生成的机器人。(★936 · 2026-06)
- [wimblerobotics/ros2-copilot-skills](https://github.com/wimblerobotics/ros2-copilot-skills) - 面向 Copilot 的 158 个 Nav2 / 行为树 / SLAM / Teensy-PlatformIO Skill；质量参差。(coll · ★19 · 2026-04)
- [robium-ai/robium](https://github.com/robium-ai/robium) - ROS 2 / Nav2 / Gazebo / MuJoCo / Isaac / LeRobot 插件，带版本化的 SKILL.md 归档。(coll · ★13 · 2026-09)
- [PatrickJS/awesome-cursorrules `ros-ros2`](https://github.com/PatrickJS/awesome-cursorrules/blob/main/rules/ros-ros2.mdc) - 面向 ROS / ROS 2 包、节点、launch 文件、消息与 URDF/xacro 的 Cursor rule。(cursor-rules · ★40.8k · 2026-05)
- [nvidia-isaac/cuVSLAM `cuvslam-skills/`](https://github.com/nvidia-isaac/cuVSLAM/tree/main/cuvslam-skills) - NVIDIA 官方 skill：构建、安装并运行 cuVSLAM/PyCuVSLAM，覆盖双目、单目、惯性和多相机跟踪模式，另含故障排查与 CI。(official · coll · ★1.8k · 2026-09)
- [NVlabs/GraspGenX](https://github.com/NVlabs/GraspGenX) - 用于操作 GraspGenX（跨本体 6-DOF 抓取生成模型）的 skill：安装、推理示例、夹爪与规划器选择、ZMQ 客户端/服务端、MCP server 以及接入新夹爪。(official · ★219 · 2026-07)
- [NVlabs/COMPASS `.claude/skills/`](https://github.com/NVlabs/COMPASS/tree/main/.claude/skills) - 面向 COMPASS 跨本体移动策略的 skill：训练、评估、SAGE 场景流程、OSMO 提交、诊断 skill 以及接入新机器人本体。(official · coll · ★142 · 2026-09)
- [HorizonRobotics/HoloMotion `.agents/skills/`](https://github.com/HorizonRobotics/HoloMotion/tree/master/.agents/skills) - 面向 HoloMotion 人形机器人全身控制模型的 skill：在真机上部署和排查策略、测延迟、准备动作数据以及诊断训练。(official · coll · ★710 · 2026-09)
- [PlaiPin/rosclaw `extensions/openclaw-plugin/skills/`](https://github.com/PlaiPin/rosclaw/tree/main/extensions/openclaw-plugin/skills) - OpenClaw 插件自带的 skill，从聊天应用控制 ROS 2 机器人：导航到指定位置、抓取物体、拍照和查看机器人状态。(coll · ★632 · 2026-03)
- [spacemit-robotics/robot-skills](https://github.com/spacemit-robotics/robot-skills) - SpacemiT Robot SDK 官方 skill：SDK 初始化与构建、机械臂控制、抓取、LeRobot 应用与 ONNX 推理、外设（IMU、激光雷达、LED、GPIO、5G、NFC）以及远程访问。(official · coll · ★0 · 2026-07)
- [i2rt-robotics/i2rt `.agents/skills/`](https://github.com/i2rt-robotics/i2rt/tree/main/.agents/skills) - I2RT 机器人 SDK 自带的 skill：转换 Onshape 导出的 URDF，并让 MuJoCo MJCF 模型与 URDF 的运动学、质量和惯量保持一致。(official · coll · ★158 · 2026-09)
- [sunfounder/picrawler `picrawler-control/`](https://github.com/sunfounder/picrawler/tree/main/picrawler-control) - SunFounder 官方 skill，用于控制 PiCrawler 四足机器人：行走、转向、摆姿态、读取传感器、播放声音和摄像头视觉。(official · ★39 · 2026-09)
- [dorna-robotics/workspace `.claude/skills/`](https://github.com/dorna-robotics/workspace/tree/main/.claude/skills) - Dorna 机器人工作区自带的 skill：添加由本进程或另一台 Pi 上的守护进程驱动的设备、自定义组件以及行为树动作。(official · coll · ★1 · 2026-09)
- [cyberwave-os/driver-skill](https://github.com/cyberwave-os/driver-skill) - Cyberwave 官方 skill，为硬件设备生成新驱动脚手架，使其接入 Cyberwave 平台。(official · ★1 · 2026-09)
- [matlab/matlab-agentic-toolkit](https://github.com/matlab/matlab-agentic-toolkit) - MathWorks 官方的 MATLAB skill 目录，包括机器人与自主系统相关 skill：通过 MAVLink 连接、构建 UAV 场景、惯性传感器融合、GNSS 定位解算、机器人运动学建模以及发现测试硬件。(official · coll · ★1.1k · 2026-09)
- [open-edge-platform/physical-ai-studio `skills/`](https://github.com/open-edge-platform/physical-ai-studio/tree/main/skills) - Intel Physical AI Studio 自带的模仿学习机器人 skill：编写机器人插件和驱动、添加策略、基准测试，以及导出和验证训练好的模型。(official · coll · ★88 · 2026-09)
- [amap-cvlab/ABot-Claw `openclaw_layer/skills/`](https://github.com/amap-cvlab/ABot-Claw/tree/main/openclaw_layer/skills) - ABot-Claw 具身智能框架官方 OpenClaw 层 skill：机器人连接、Piper/Unitree G1/Go2 的硬件分工、SDK 发现、任务执行与进度评判。(coll · official · ★212 · 2026-04)
- [TidyBot-Services/Tidybot-Universe `skill-agent-setup/`](https://github.com/TidyBot-Services/Tidybot-Universe/tree/master/skill-agent-setup) - 面向 Tidybot 移动操作机器人的官方 Claude Code 与 OpenClaw skill：机器人连接、硬件与 SDK 参考、仿真管理，以及把 skill 打包成脚本提交给机器人的执行 API。(coll · official · ★56 · 2026-06)
- [graph-robots/open-robot-skills](https://github.com/graph-robots/open-robot-skills) - 为 GaP（graph as policy）准备的官方 Agent Skills 格式操作库，含多个操作 skill 和 8 个工具包，例如轮廓抓取、特征配合和持物运动。(coll · official · ★44 · 2026-09)
- [fan-ziqi/unitree-docs](https://github.com/fan-ziqi/unitree-docs) - 从 support.unitree.com 检索、浏览和获取所有 Unitree 机器人、组件与 SDK 官方文档的 skill。(★2 · 2026-07)
- [dongsheng123132/go2-openclaw-skill](https://github.com/dongsheng123132/go2-openclaw-skill) - OpenClaw skill，通过 CycloneDDS 网关（无需 ROS 2）用自然语言控制 Unitree Go2 机器狗：移动、停止、执行动作和查看电量。(★7 · 2026-03)
- [LooperRobotics/OpenClaw-Robotics](https://github.com/LooperRobotics/OpenClaw-Robotics) - OpenClaw skill，控制四足、双足、轮式和空中机器人，支持 Unitree 机器人和 Insight9 双目相机。(★48 · 2026-02)
- [EverNightCN/ur5-rtde-skill](https://github.com/EverNightCN/ur5-rtde-skill) - 通过 ur-rtde 以 RTDE 协议控制 Universal Robots UR5 的独立 skill（moveL、moveJ），带可配置的软围栏检查。(★1 · 2026-03)
- [Sazabi06/Openarm_Skills](https://github.com/Sazabi06/Openarm_Skills) - 面向 OpenArm V10 双臂机器人的 skill：达妙电机与 CAN-FD 硬件配置、标定与安全限位、阻抗控制、IK 运动规划、相机视觉和 VLA 集成。(coll · ★0 · 2026-06)
- [ambient-robots/xlerobot_pinc `.codex/skills/`](https://github.com/ambient-robots/xlerobot_pinc/tree/main/.codex/skills) - 基于 XLeRobot 平台的官方 Codex skill：硬件上电调试（udev 串口链接、电机板、摄像头）、标定流程以及与 LeRobot 同步。(coll · official · ★12 · 2026-06)
- [PickNikRoboticsServices/robot_configuration_setup](https://github.com/PickNikRoboticsServices/robot_configuration_setup) - 用于创建 MoveIt Pro 机器人配置包的官方 skill：config.yaml、URDF/xacro、mock/仿真/实机配置、objective 以及移动底盘导航设置。(official · ★0 · 2026-09)
- [wzyn20051216/ros-robotics-skill](https://github.com/wzyn20051216/ros-robotics-skill) - ROS 1 / ROS 2 工程 skill，涵盖 catkin/colcon、launch、URDF/Xacro、TF、Nav2、ros2_control、串口与 CAN、MCU 和 micro-ROS。(★59 · 2026-03)
- [Leehyunbin0131/claude-ros2-skills](https://github.com/Leehyunbin0131/claude-ros2-skills) - 面向 ROS 2 Jazzy、强调对照已安装系统验证的 Claude Code skill：micro-ROS agent、rclc 与自定义传输，以及 ROS 2 故障排查。(coll · ★19 · 2026-08)
- [enesbirlik/claude-code-robotics](https://github.com/enesbirlik/claude-code-robotics) - Claude Code skill：ROS 2 工作空间、URDF/Xacro 构建、Nav2 与 MoveIt 2 配置，以及 STM32 通过 UART 或 CAN 接入的 micro-ROS 桥接。(coll · ★2 · 2026-09)
- [Ranch-Hand-Robotics/rde-urdf `assets/skills/`](https://github.com/Ranch-Hand-Robotics/rde-urdf/tree/main/assets/skills) - RDE URDF 编辑器（VS Code 扩展）官方附带的 skill，涵盖 URDF/Xacro 基础、几何、Xacro 转换和 OpenSCAD 零件建模。(coll · official · ★16 · 2026-09)
- [coolbeevip/mujoco-skills](https://github.com/coolbeevip/mujoco-skills) - 用于构建、校验和控制 MuJoCo MJCF 机器人场景的 skill，支持可复现的无头仿真、执行器实验和强化学习环境准备。(★18 · 2026-09)

### 无人机

- [PX4/PX4-Autopilot `build-px4`](https://github.com/PX4/PX4-Autopilot/tree/main/.agents/skills/build-px4) - 在 px4-dev 容器内构建 PX4 板级固件，支持 worktree；不负责烧录。(official · ★12.7k · 2026-09)
- [fossuav/aap](https://github.com/fossuav/aap) - "ArduPilot AI Playbooks"：面向 Claude、Codex 与 Gemini 的构建、SITL 与 Lua 脚本 Skill。(coll · ★19 · 2026-09)
- [pelageech/ardupilot-agent-toolkit](https://github.com/pelageech/ardupilot-agent-toolkit) - 七个 ArduPilot Skill：直接控制、SITL、Gazebo Harmonic、pymavlink、Pixhawk 6C、任务规划、飞行诊断。(coll · ★0 · 2026-09)
- [raylanlin/smarttune-cli](https://github.com/raylanlin/smarttune-cli) - 面向 ArduPilot、Betaflight 与 PX4 的飞行日志调参顾问，同时提供 Skill 与 MCP。(★29 · 2026-09)
- [SebGalina/betaflight-claude-skill](https://github.com/SebGalina/betaflight-claude-skill) - Betaflight 配置、PID 调参、黑匣子分析、排障；作者的 `betaflight-mcp` 通过 USB 走 MSP 协议。(★29 · 2026-09)
- [sensei-hacker/inav-claude](https://github.com/sensei-hacker/inav-claude) - iNAV 飞控开发流程，含一个硬件在环链路测试 Skill。(coll · ★4 · 2026-09)
- [MIUAV/vibe-coding-ros2](https://github.com/MIUAV/vibe-coding-ros2) - PX4 + ROS 2 Humble 无人机开发：MAVLink、offboard 模式、固件构建、模块开发、机架、传感器配置、多旋翼调参、视觉导航、RKNN。中文。(coll · ★26 · 2026-05)
- [castacks/AirStack](https://github.com/castacks/AirStack) - CMU AirLab 的"Agent 原生" ROS 2 空中自主栈，带 `.agents/skills`。(★92 · 2026-09)
- [LuweiLiao/ardupilot-skill](https://github.com/LuweiLiao/ardupilot-skill) - 27 个面向 ArduPilot 固件开发的 skill：ChibiOS hwdef 板级移植、HAL、waf 构建、EKF 导航、DroneCAN、MAVLink 地面站、bootloader、SITL 自动测试和移植手册。(coll · ★1 · 2026-05)
- [LeaderOnePro/mavctl](https://github.com/LeaderOnePro/mavctl) - 以 ArduPilot 为主的无界面 MAVLink 地面站 CLI，附带 skill，让 agent 执行连接、解锁、切换模式、起飞、降落、返航和读取遥测；已在 ArduPilot SITL 上验证，尚未在真实飞行器上证实。(★0 · 2026-09)
- [ARK-Electronics/px4-log-analysis `.claude/skills/`](https://github.com/ARK-Electronics/px4-log-analysis/tree/main/.claude/skills) - ARK Electronics 官方的 PX4 ULog 分析 Claude Code skill：加速度计振动、气压计受压、GPS 信号质量以及按 topic 统计日志体积。(official · coll · ★3 · 2026-04)
- [HansF/betaflight-skill](https://github.com/HansF/betaflight-skill) - 通过 USB 串口连接 Betaflight 飞控的 skill：执行 CLI 命令、带校验地读写参数、备份与恢复配置、读取 MSP 遥测并解码黑匣子日志。(★0 · 2026-09)
- [archat-hash/FlyCLI](https://github.com/archat-hash/FlyCLI) - 控制 Betaflight 飞控的命令行工具，附带 skill，告诉 agent 如何获取上下文并通过串口执行 FlyCLI 命令。(★5 · 2026-07)
- [paulnurkkala/ardufleetcheck](https://github.com/paulnurkkala/ardufleetcheck) - 用于 ArduPilot 装机后整机检查的 Claude Code skill：烧录 .apj 并恢复参数、推送 OSD 布局与字体、执行图传、遥控和解锁就绪检查，并上传 QGroundControl 航线。(coll · ★0 · 2026-05)
- [aero-oli/ardupilot-binlog-analysis](https://github.com/aero-oli/ardupilot-binlog-analysis) - 分析 ArduPilot DataFlash .bin 日志的 skill：故障诊断、调参复查、振动/FFT、EKF/GPS、电源、电机/电调、AutoTune 以及前后对比。(★1 · 2026-05)
- [BeastAyyG/ardupilot-log-diagnosis](https://github.com/BeastAyyG/ardupilot-log-diagnosis) - 结合规则引擎与 XGBoost 的 ArduPilot 飞行日志分析器（为 GSoC 2026 申请而写），附带 skill 诊断 .BIN 日志中坠机、GPS 与 IMU 故障的根因。(★6 · 2026-08)
- [rwoneill/claude-ardupilot](https://github.com/rwoneill/claude-ardupilot) - 即用型 ArduPilot 助手模板：SKILL.md 涵盖固件、Lua 脚本、参数、dataflash 日志和飞控硬件，另附供 Claude Code 项目使用的 CLAUDE.md。(★0 · 2026-04)
- [hfujikawa77/claw-sitl-ops](https://github.com/hfujikawa77/claw-sitl-ops) - OpenClaw skill，通过 MAVLink 操作 ArduPilot SITL：启动与停止、解锁、起飞、切换模式、读写参数并汇报飞行器状态。(★3 · 2026-03)
- [learnsyslab/crazyflow](https://github.com/learnsyslab/crazyflow) - 基于 JAX 的可扩展 Crazyflie 无人机仿真器，其 SKILL.md 说明新增动力学模型或平台、把控制器复用于状态估计或 MPC 时的陷阱与约定。(★175 · 2026-09)

### 航空航天

- [esa/nanosat-mo-framework](https://github.com/esa/nanosat-mo-framework) - 欧空局的 CCSDS 任务运行飞行软件框架，带一个用于编写服务定义的 `mo-xml` Skill。目前找到的唯一由航天机构官方发布的 Agent Skill。(official · ★123 · 2026-09)
- [devideamax/aerospace-team](https://github.com/devideamax/aerospace-team) - 十二个卫星任务 Skill：制导导航控制、电源系统、卫星通信、地面系统与发射运行。(coll · ★22 · 2026-02)
- [elodin-sys/elodin `.cursor/skills/`](https://github.com/elodin-sys/elodin/tree/main/.cursor/skills) - Elodin 官方仿真与飞行软件 monorepo 中的 skill：把 AlephOS 部署到 Jetson Orin 飞控计算机、编写支持 SITL/HITL 的 6DOF 仿真、蒙特卡洛运行和无头录制。(coll · official · ★544 · 2026-09)
- [LunCoSim/space-engineering-skills](https://github.com/LunCoSim/space-engineering-skills) - 用于设计卫星与地表任务的航天工程 skill：星座设计、通信与载荷评估、AIT 管理、环控生保（ECLSS）和成本建模。(coll · ★10 · 2026-03)
- [jclark/satpulse `.claude/skills/`](https://github.com/jclark/satpulse/tree/master/.claude/skills) - SatPulse（GPS 接收机授时工具）仓库中的 Claude Code skill：新增和测试 GPS 配置消息，并依据日志驱动 satpulsed 守护进程。(coll · ★63 · 2026-09)
- [Official-MoonDao/LORS `skills/`](https://github.com/Official-MoonDao/LORS/tree/main/skills) - 月球开源巡视器标准（LORS）的 skill，引导 agent 查询月球车、着陆器、任务和相关公司的知识。(coll · ★10 · 2026-03)

### 边缘 AI / NPU

- [hailo-ai/hailo-apps `.claude/skills/`](https://github.com/hailo-ai/hailo-apps/tree/main/.claude/skills) - 十二个 Hailo Skill：相机、构建流水线 / LLM / VLM / 语音 / Agent 应用、模型管理、监控、校验。(official · coll · ★499 · 2026-04)
- [hailo-ai/hailo_model_zoo `.claude/skills/`](https://github.com/hailo-ai/hailo_model_zoo/tree/master/.claude/skills) - 面向 Dataflow Compiler 工具链的 `hailo-parse`、`hailo-optimize`、`hailo-compile`。(official · coll · ★709 · 2026-09)
- [hailo-ai/hailo15-agentic-coding](https://github.com/hailo-ai/hailo15-agentic-coding) - Hailo-15 视觉处理器的十二个 Skill 与 agent：连接、板卡状态、换模型、交叉编译、部署到板子——闭合了"烧录 → 运行"回路。(official · coll · ★0 · 2026-06)
- [HorizonRobotics/OE-Skills](https://github.com/HorizonRobotics/OE-Skills) - 地平线 HBDK 编译、HMCT 量化、UCP 板上推理与 LLM 压缩的 37 个 Skill。(official · coll · ★20 · 2026-07)
- [D-Robotics/rdk-device-skills](https://github.com/D-Robotics/rdk-device-skills) - 26 个端侧 RDK Skill（诊断、内存审计、相机、BPU 模型部署与跑分、GPIO、TROS）；同系列还有 `oe-skills-x5`、`bsp-skills` 与 `rdk-docs-mcp`。(official · coll · ★2 · 2026-09)
- [luxonis/skills](https://github.com/luxonis/skills) - OAK 相机路由 Skill 加七个专项（应用、设备配置、检查、模型、录制、排障、工作区），配 MCP 配置与 `oakctl`。(official · coll · ★16 · 2026-09)
- [PyTorch ExecuTorch `.claude/skills/`](https://github.com/pytorch/executorch/tree/main/.claude/skills) - 九个 ExecuTorch Skill：导出、构建、Cortex-M、Zephyr、高通、性能分析、二进制体积、知识库。(official · coll · ★5k · 2026-09)
- [google-ai-edge/litert-samples `skills/`](https://github.com/google-ai-edge/litert-samples/tree/main/skills) - 六个 LiteRT Skill：转换流程、保精度量化、GPU 干净转换、端侧验证。(official · coll · ★435 · 2026-09)
- [Dengdxx/PaddleYOLO-RKNN `rknn-flow`](https://github.com/Dengdxx/PaddleYOLO-RKNN) - 瑞芯微 RKNN 模型转换流程。中文。(★8 · 2026-08)
- [gregm123456/raspberry_pi_hailo_ai_services](https://github.com/gregm123456/raspberry_pi_hailo_ai_services) - 树莓派 5 + Hailo AI HAT 服务，带一个 Copilot Skill。(copilot · ★11 · 2026-06)
- [hailo-ai/hailo-media-library `.claude/skills/`](https://github.com/hailo-ai/hailo-media-library/tree/1.12.1/.claude/skills) - Hailo 官方为 Hailo-15 视觉应用提供的 skill：连接 H15 板、交叉编译、部署、检查板卡状态、替换 HEF 模型，以及修改媒体管线、码流和叠加层。(official · coll · ★8 · 2026-08)
- [nvidia-holoscan/holoscan-sdk `skills/`](https://github.com/nvidia-holoscan/holoscan-sdk/tree/main/skills) - NVIDIA Holoscan SDK 官方 skill：检查主机、评估平台兼容性，并通过 Debian 包、wheel、conda、容器或源码安装该传感器处理 SDK。(official · coll · ★222 · 2026-09)
- [ultralytics/skills](https://github.com/ultralytics/skills) - Ultralytics 官方 YOLO skill：模型、数据集、训练、推理与导出，包括部署到 TensorRT、OpenVINO 以及 RKNN、QNN、Hailo、Ascend 等 NPU。(official · coll · ★23 · 2026-09)
- [openvinotoolkit/openvino `.claude/skills/`](https://github.com/openvinotoolkit/openvino/tree/master/.claude/skills) - OpenVINO 仓库内置的 skill：调试精度、性能、编译与内存问题，导出张量和 IR，新增 GGUF 架构支持以及面向贡献者的 agent 工作流。(official · coll · ★10.9k · 2026-09)
- [Seeed-Studio/recamera-pro-ext-api `skill/recamera-pysdk/`](https://github.com/Seeed-Studio/recamera-pro-ext-api/tree/main/skill/recamera-pysdk) - Seeed 官方 skill，为 reCamera Pro（RV1126B）构建并打包 Python SDK 应用，含离线验证和随包附带的设备兼容 wheel。(official · ★1 · 2026-09)
- [mjq2020/reCamera_skill](https://github.com/mjq2020/reCamera_skill) - reCamera（RV1126B）Web API 参考 skill：认证、设备管理、音视频配置、录像、AI 模型推理、日志以及 SenseCraft 云端模型转换。(★4 · 2026-03)
- [kornia/vision-rt `.claude/skills/`](https://github.com/kornia/vision-rt/tree/main/.claude/skills) - 面向 Jetson Orin 的 Rust + TensorRT 视觉库中的 skill：重建与调试 TensorRT 引擎、按功耗模式规范做基准测试、组合管线以及编写 CUDA kernel。(coll · ★18 · 2026-08)
- [SharpAI/DeepCamera `skills/`](https://github.com/SharpAI/DeepCamera/tree/master/skills) - 开源 AI 摄像头 skill 平台，含 Coral TPU 与 OpenVINO 上的 YOLO 检测、Reolink/Tapo/Eufy 等摄像头接入、go2rtc 推流以及家庭安防基准测试等 skill。(coll · ★3.1k · 2026-09)
- [LudovicoYIN/skills `deploy-skills/`](https://github.com/LudovicoYIN/skills/tree/master/deploy-skills) - 面向端侧 NPU 与推理框架的模型部署 skill：RKNN、高通 QNN 与 SNPE、联发科以及 llama.cpp，涵盖转换、算子问题和与 ONNX 的精度对比。(coll · ★0 · 2026-07)
- [zhao123xiao/openvino-skills](https://github.com/zhao123xiao/openvino-skills) - OpenVINO 标准作业 skill：模型转换、量化、部署、冒烟测试、基准测试、设备选择和故障排查。(★1 · 2026-05)
- [mayukh4/huskylens-agent](https://github.com/mayukh4/huskylens-agent) - 让 Hermes Agent 在树莓派 5 上拥有实体的 skill：通过 I2C 接入 HuskyLens V2 摄像头做人脸、情绪和手势识别，在 DSI 屏上显示动画人脸并提供语音管线。(★13 · 2026-04)
- [Ascend/agent-skills](https://github.com/Ascend/agent-skills) - 华为昇腾官方 agent skill，面向 NPU 开发，例如安装 NPU 驱动与固件、配置昇腾 Docker 以及指导推理仓库使用。(official · coll · ★42 · 2026-05)
- [ascend-ai-coding/awesome-ascend-skills](https://github.com/ascend-ai-coding/awesome-ascend-skills) - 以 200 多个 Agent Skill 组织的华为昇腾 NPU 开发知识库，覆盖 CANN、torch 自定义算子和昇腾工具链。(coll · ★170 · 2026-09)
- [sophgo/sophon-demo `.claude/skills/`](https://github.com/sophgo/sophon-demo/tree/release/.claude/skills) - 算能（SOPHGO）sophon-demo 仓库的 skill：按步骤把模型从 ONNX 导出移植到 SOPHON 芯片 SoC 上部署，另含示例测试和自动化测试。(official · coll · ★527 · 2026-09)
- [sophgo/sophon-tools `source/pbmssm/build/se-series-skill/`](https://github.com/sophgo/sophon-tools/tree/main/source/pbmssm/build/se-series-skill) - 算能（SOPHGO）为 SE 系列边缘 AI 盒子提供的知识库 skill，收录在 sophon-tools 仓库中。(official · ★27 · 2026-09)

### EDA / PCB

- [aklofas/kicad-happy](https://github.com/aklofas/kicad-happy) - 分析 KiCad 工程与 PDF 原理图、DRC / ERC / DFM、EMC 预兼容、SPICE、在 DigiKey / Mouser / 立创 / element14 上选料、JLCPCB 与 PCBWay 制板准备。(coll · ★1.3k · 2026-09)
- [autodesk-platform-services/skills](https://github.com/autodesk-platform-services/skills) - Autodesk 官方面向 AutoCAD ARX 与 Autodesk Platform Services API 的 Skill；属 CAD 而非硬件，也是找到的最大厂商 Skill 仓库。(official · ★53 · 2026-08)
- [easyeda/easyeda-api-skill](https://github.com/easyeda/easyeda-api-skill) - 嘉立创 EDA 专业版：120+ 个 API 类，外加一座通往运行中客户端的 WebSocket 桥。(official · ★723 · 2026-09)
- [zhoushoujianwork/easyeda-agent](https://github.com/zhoushoujianwork/easyeda-agent) - 通过本地 CLI / 守护进程驱动嘉立创 EDA 专业版：原理图、网表检查、PCB 布局布线、DRC、制造文件导出；同时提供 CLI + Skill + MCP。(★465 · 2026-09)
- [diodeinc/pcb](https://github.com/diodeinc/pcb/tree/main/skills) - Zener 代码转 PCB 语言，外加 `datasheet-reader`、`librarian`、元件库检索与 SPICE 仿真 Skill。(coll · ★451 · 2026-09)
- [atopile/atopile `.claude/skills/`](https://github.com/atopile/atopile/tree/main/.claude/skills) - 用代码定义 PCB 设计；`ato` 与 `ato-language` 面向用户，其余是编译器 / 求解器 / 库的贡献者 Skill。(coll · ★3.9k · 2026-06)
- [American-Embedded/kistack](https://github.com/American-Embedded/kistack) - 人工编写的 KiCad Skill 栈：原理图、符号、封装、PCB 布局、Gerber、拼板、BOM、导出、产品渲染。(coll · ★386 · 2026-09)
- [drandyhaas/KiCadRoutingTools](https://github.com/drandyhaas/KiCadRoutingTools) - `plan-pcb-routing` 从 `.kicad_pcb` 生成扇出与差分对布线方案。(★465 · 2026-09)
- [Seeed-Studio/ai-skills](https://github.com/Seeed-Studio/ai-skills) - `schematic-analyzer` 追踪 KiCad 与 OrCAD/Allegro 原理图；`ee-datasheet-master` 从 PDF 中提取引脚图、I2C 地址与寄存器映射；另有 SG200x/CV181x 多媒体与 ONNX 转 cvimodel 的 Skill。(official · coll · ★25 · 2026-09)
- [Tansuo2021/ADtoKeil](https://github.com/Tansuo2021/ADtoKeil) - 把 Altium 原理图当作依据读取，为其描述的板子生成 Keil 固件，再通过串口验证。仅 Windows。(coll · ★172 · 2026-06)
- [oaslananka/kicad-mcp-pro](https://github.com/oaslananka/kicad-mcp-pro/tree/main/skills) - 架在 KiCad MCP 之上的 `pcb-design` 与 `kicad-design-review`：布局、布线、叠层、质量门禁。(coll · ★94 · 2026-09)
- [Zane456/PCB-Agent-Teams](https://github.com/Zane456/PCB-Agent-Teams) - 从拓扑到 Gerber 的多 Agent KiCad 流水线，带高压 / 低压 / 隔离分区。(coll · ★66 · 2026-07)
- [Cognitohazard/ltspice-mcp](https://github.com/Cognitohazard/ltspice-mcp) - LTspice 与 ngspice 的 MCP，配 `ltspice`、`ngspice`、`spice-bench-craft` 与 `spice-experiments` Skill。(coll · ★44 · 2026-09)
- [Arcadia-1/gmoverid-skill](https://github.com/Arcadia-1/gmoverid-skill) - 基于 ngspice 与 SKY130 / PTM 模型的模拟 IC 设计：gm/ID、晶体管模型、LDO / 运放 / 比较器；同系列还覆盖 Verilog-A 与一套 Razavi 基准。(coll · ★124 · 2026-07)
- [SpiceSharp/SpiceSharpParser `.agents/skills/`](https://github.com/SpiceSharp/SpiceSharpParser) - 以测试驱动的方式设计网表，用 `.MEAS` 做验证。(official · ★33 · 2026-08)
- [fireostendere/mcp_diptrace](https://github.com/fireostendere/mcp_diptrace) - DipTrace MCP 加一个信号完整性审查 Skill。(★23 · 2026-09)
- [akiselev/altium-cli `.agents/skills/`](https://github.com/akiselev/altium-cli) - 处理 SchDoc / PcbDoc / 元件库的 Rust CLI，带校验、规则审查、数据审查与 GUI 控制 Skill。(coll · ★14 · 2026-09)
- [l3wi/claude-eda](https://github.com/l3wi/claude-eda) - 面向 KiCad 的 `eda-architect`、`eda-schematics`、`eda-pcb`、`eda-drc`、`eda-research`。(coll · ★19 · 2026-01)
- [pjcau/esp32-emu-turbo `.claude/skills/`](https://github.com/pjcau/esp32-emu-turbo) - 唯一一套真正驱动 JLCPCB DFM 工具的 Skill：上传、校验、PCB 审查、PCBA 就绪度检查。(coll · ★4 · 2026-09)
- [daishuge/pcb-skill](https://github.com/daishuge/pcb-skill) - 把硬件想法带到可制造 PCB 的 agent skill，通过 MCP 驱动 EasyEDA Pro：概念、原理图、选型、布局、布线与验证门禁，直至下单前的付款页。(★132 · 2026-09)
- [biosshot/easyeda-copilot](https://github.com/biosshot/easyeda-copilot) - 面向 EasyEDA 的 AI 助手，从自然语言生成原理图并检索 LCSC 元件，含 docs、datasheets 与 spice 等 skill。(coll · ★145 · 2026-09)
- [seanrobertwright/lril-kicad-skills](https://github.com/seanrobertwright/lril-kicad-skills) - 九个 KiCad 10 agent skill，先访谈用户并写下规格，再生成原理图、PCB、符号与封装，并用 KiCad 自带的 ERC/DRC/网表/渲染工具逐一验证。(coll · ★0 · 2026-09)
- [nickkraakman/skidl-skills](https://github.com/nickkraakman/skidl-skills) - 基于 SKiDL Python 库的 KiCad PCB agentic 工作流，含 new-circuit、find-part、ERC 规则与设计评审等 skill 及九个协作 agent。(coll · ★18 · 2026-04)
- [Milind220/Ki-Stack](https://github.com/Milind220/Ki-Stack) - 面向 agent 的深度 KiCad 自动化栈，结合 kicad-python IPC、kicad-cli 与 kiutils-rs，含 orient、PCB、footprints、render、file-surgery 与 live IPC 等 skill。(coll · ★22 · 2026-05)
- [mattpainter701/kicad_automations](https://github.com/mattpainter701/kicad_automations) - Circuit Weaver：程序化生成 KiCad 原理图并做严格校验、ERC 与制造导出，含 kicad、sim、jlcpcb、digikey/mouser/lcsc 选型与 vivado 辅助等 skill。(coll · ★21 · 2026-08)
- [HubertHQH/KiCad-skills](https://github.com/HubertHQH/KiCad-skills) - 通过 KiCad IPC API 与自带 kipy 解释器读取、修改并导出 PCB 设计的 KiCad 10+ agent skill：kicad-connect、kicad-pcb、kicad-project 与 kicad-export。(coll · ★13 · 2026-04)
- [BeckhamLabsLLC/kicad-jlcpcb](https://github.com/BeckhamLabsLLC/kicad-jlcpcb) - Claude Code 插件加 MCP server，检索 JLCPCB/LCSC 元件、抓取 EasyEDA 引脚图、放置 KiCad 封装并按引脚名连线，产出可制造的 .kicad_pcb。(★24 · 2026-09)
- [Prithvi-0g/claude-kicad-skills](https://github.com/Prithvi-0g/claude-kicad-skills) - KiCad PCB 设计、分析与制造 skill，含 autoroute、BOM、SPICE、EMC、JLCPCB/PCBWay 导出与 digikey/mouser/lcsc/element14 选型。(coll · ★1 · 2026-05)
- [tipoLi5890/akcli](https://github.com/tipoLi5890/akcli) - 零依赖的 Python CLI，用于 AI 原生的 KiCad 原理图设计，从 JSON op-list 生成 .kicad_sch，含电路设计/调试、ERC/设计评审、JLCPCB 能力与选型等 skill。(coll · ★8 · 2026-08)
- [oaslananka/easyeda-mcp-pro](https://github.com/oaslananka/easyeda-mcp-pro) - 面向 EasyEDA Pro 的 MCP server，含 easyeda-professional-layout skill，覆盖 PCB 检查、BOM 选型、制造导出与 AI 辅助布局。(★46 · 2026-09)
- [Huaqiu-Electronics/skills](https://github.com/Huaqiu-Electronics/skills) - 华秋电子为华秋 EDA 提供的 agent skill，每个编辑器 API 操作对应一个小 skill，覆盖 BOM、画布编辑、对象放置、ERC、器件搜索以及设计导入/导出等领域，可用 npx skills 安装。(official · coll · ★4 · 2026-08)
- [coffeenmusic/altium-scripts-skill](https://github.com/coffeenmusic/altium-scripts-skill) - 用于编写 Altium Designer DelphiScript 自动化脚本的 Claude Code skill，基于 230+ 可用示例脚本与 PCB、原理图、DXP 接口的 API 参考。(★14 · 2026-04)
- [dnewcome/circuit-skills](https://github.com/dnewcome/circuit-skills) - 面向代码驱动电子设计的 Claude Code skill：ngspice/Falstad 电路仿真、tscircuit PCB 布局、3D 渲染与外壳适配。(coll · ★4 · 2026-07)
- [zuoliangyu/multisim-spice](https://github.com/zuoliangyu/multisim-spice) - 把一句话电路描述变成 ngspice 自检通过、可直接在 NI Multisim 打开的 SPICE 网表的 Claude Code skill。(★11 · 2026-05)
- [hyndex/Schematics-and-PCB-Skills](https://github.com/hyndex/Schematics-and-PCB-Skills) - 庞大的元件与 PCB skill 集合，涵盖数据手册提取、符号/封装、DFT、EMC，以及汽车、航空、BMS、EV 充电、柔性、HDI、大功率等专用板卡。(coll · ★1 · 2026-05)
- [Arcadia-1/analog-agents](https://github.com/Arcadia-1/analog-agents) - 联邦式模拟 IC 设计框架，其 skill 覆盖架构探索、尺寸设计、行为建模、验证、ADC 分析、跨模型审计与自演化，可在有/无 EDA 下运行。(coll · ★69 · 2026-07)
- [Arcadia-1/veriloga-skills](https://github.com/Arcadia-1/veriloga-skills) - 可复用的 Verilog-A 撰写 skill，含自包含语言指南，以及可选的 evas-sim 与 openvaf 编译/仿真配套 skill。(coll · ★34 · 2026-07)
- [Arcadia-1/analog-circuit-skills](https://github.com/Arcadia-1/analog-circuit-skills) - 面向常见模拟单元（LDO、比较器、五管 OTA、两级运放、自举开关）的 agent skill，使用 ngspice 仿真。(coll · ★13 · 2026-06)
- [hdl-tools/analog-chip-design-agents](https://github.com/hdl-tools/analog-chip-design-agents) - 面向模拟/混合信号与 RF 芯片流程的 16 插件 Claude Code marketplace：架构、电路设计、AMS 集成/验证、EM 建模、寄生参数提取与特性化。(coll · ★22 · 2026-06)
- [deanyou/virtuoso-cli](https://github.com/deanyou/virtuoso-cli) - 用 Rust 编写的桥接与 CLI，让 agent 驱动 Cadence Virtuoso，含 schematic-gen、gm-over-id 尺寸、Maestro、sim-measure、电路优化与 OCEAN 网表重生等 skill。(coll · ★33 · 2026-09)
- [simra-tech/OpenADA](https://github.com/simra-tech/OpenADA) - Open Agentic Design Automation，定义 agent–EDA 契约，含 bootstrap ASIC 工程、模拟单元特性化、评估时序/PVT/良率、跑综合与增量收敛版图等 skill。(coll · ★26 · 2026-08)
- [SPREsxm/claude-pcb-designer](https://github.com/SPREsxm/claude-pcb-designer) - 覆盖 PCB 全流程的开放 agent skill：需求、选型、原理图评审、层叠、布局/布线、信号完整性/热设计、DFM/DFA 与制造放行，含确定性计算器。(★4 · 2026-09)

### FPGA / HDL

- [Shinei-Nouzen-Arch/FPGA-Agent](https://github.com/Shinei-Nouzen-Arch/FPGA-Agent) - 最好的 Vivado / Vitis Skill 集：综合、实现、仿真、Tcl、约束、调试、分析、借助 RapidWright 做时序收敛。(coll · ★171 · 2026-09)
- [hdl-tools/digital-chip-design-agents](https://github.com/hdl-tools/digital-chip-design-agents) - 覆盖芯片全流程的 16 个插件：RTL、验证、综合、静态时序分析、物理设计、可测试性设计、FPGA、高层次综合、形式验证；姊妹项目 `analog-chip-design-agents`。(coll · ★205 · 2026-09)
- [Eriemon/verilog-generator](https://github.com/Eriemon/verilog-generator) - 可读的 Verilog-2001 生成、审查与注释、testbench 脚手架、本地或远程 Vivado。(★288 · 2026-08)
- [Mindrally/skills `fpga` / `systemverilog`](https://github.com/Mindrally/skills) - 由 Cursor rule 演化而来的 FPGA 与 SystemVerilog Skill，各约 1000 次安装。(★259 · 2026-09)
- [codejunkie99/Gateflow-Plugin](https://github.com/codejunkie99/Gateflow-Plugin) - 在开源工具链上完成 SystemVerilog 设计 → 验证（cocotb、形式化）→ 交付，带 FuseSoC 与 IP 打包。(coll · ★114 · 2026-09)
- [one-ware/OneWare](https://github.com/one-ware/OneWare) - ONE WARE Studio 内用于 Yosys / nextpnr 的 `fpga-toolchain-yosys`。(official · ★143 · 2026-09)
- [a2fpga/a2fpga_core `.claude/skills/`](https://github.com/a2fpga/a2fpga_core) - 高云 Tang Nano 20K 比特流构建与烧录，外加 BL616 MCU 烧录。(coll · ★75 · 2026-08)
- [TONGJI-EDA-LAB/RTL-CLAW](https://github.com/TONGJI-EDA-LAB/RTL-CLAW) - OpenClaw 上的学术向 Verilog 划分 / 优化（Yosys + Verible）/ 合并 Skill。(coll · ★65 · 2026-04)
- [bjwanneng/veriflow-cc](https://github.com/bjwanneng/veriflow-cc) - 架构 → RTL → iverilog / Yosys 流水线，带 cocotb 覆盖率。(★51 · 2026-08)
- [LilithSemi/claude-for-hardware](https://github.com/LilithSemi/claude-for-hardware) - 唯一一套涉及物理 bring-up 的 FPGA 合集：用树莓派模拟 JTAG 下载比特流、综合适配、面积 / 时序、裸机启动链、ROHD 的坑。(coll · ★21 · 2026-08)
- [a5c-ai/babysitter `fpga-programming`](https://github.com/a5c-ai/babysitter/tree/main/library/specializations/fpga-programming/skills) - 19 个短 Skill：Verilog / SV / VHDL、时序约束、跨时钟域、SVA、UVM、高层次综合、布局布线、综合、调试。(coll · ★1.8k · 2026-09)
- [wweiyi2004/minifpga-quartus-skill](https://github.com/wweiyi2004/minifpga-quartus-skill) - Quartus Cyclone IV 的 Codex Skill；唯一一个有实际使用量的 Quartus Skill。(★8 · 2026-06)
- [Tomer-Harari/claude-fpga-skills](https://github.com/Tomer-Harari/claude-fpga-skills) - 无头的厂商流程：Vivado 批处理、ModelSim 无头运行、cocotb testbench、跨时钟域形式验证、时序收敛、AXI-Stream 验证。(coll · ★1 · 2026-08)
- [londey/claude-skill-verilog](https://github.com/londey/claude-skill-verilog) - 一个可用的 Verilog Skill。(★18 · 2026-04)
- [QingquanYao/xilinx-skill](https://github.com/QingquanYao/xilinx-skill) - Xilinx/AMD 全工具链 skill，从自然语言生成可运行的 Vivado、Vitis HLS、Vitis Unified 与 PetaLinux Tcl 脚本，覆盖 HLS 到启动镜像的 FPGA/MPSoC 流程。(★433 · 2026-04)
- [babyworm/rtl-agent-team](https://github.com/babyworm/rtl-agent-team) - 面向自动化 RTL 设计与验证的 Claude Code 插件 harness，含 99 个 agent 与 97 个 skill，自动执行 Research→Architecture→uArch→RTL→Verify→Design-Note 的六阶段流水线。(coll · ★52 · 2026-08)
- [ShenShan123/r2g-skills](https://github.com/ShenShan123/r2g-skills) - 驱动开源 RTL-to-GDS 流程的 Claude Code skill，从自然语言规格经综合、布局布线到完整签核（DRC/LVS/RCX），使用 Yosys、OpenROAD、KLayout 与 OpenRCX。(coll · ★43 · 2026-09)
- [adeleempurpled290/FPGA-Agent-skills](https://github.com/adeleempurpled290/FPGA-Agent-skills) - 八个 AMD Vivado/Vitis skill，覆盖 HLS 综合、RTL 仿真、综合、实现、约束、时序、调试与 Tcl 脚本。(coll · ★37 · 2026-09)
- [LNC0831/oh-my-fpga](https://github.com/LNC0831/oh-my-fpga) - 开放的 FPGA skill 包，在 SynthPilot MCP server 的原子工具之上叠加有主见的工作流（时序收敛、CDC 审计、ILA 硬件调试、比特流烧录、全流程 demo）。(coll · ★21 · 2026-06)
- [oniondas/duck-rtl](https://github.com/oniondas/duck-rtl) - 面向 agent 的省 token RTL 构建-验证回路，校验模块接口、门控编译、跑 cocotb 协同仿真，并在确定性护栏下从 AST 提取并绘制控制 FSM。(★6 · 2026-07)
- [rtl-buddy/rtl_buddy](https://github.com/rtl-buddy/rtl_buddy) - 面向 Verilog/SystemVerilog 回归测试的 Python CLI，支持 Verilator/VCS，附 dispatch、形式属性验证、图提取、实现与测试等 skill。(coll · ★3 · 2026-09)
- [hjxxlogic/open-vivado](https://github.com/hjxxlogic/open-vivado) - 通过本地 JSON/TCP 桥接 Vivado Tcl 自动化 AMD Vivado FPGA 流程的 skill 包：工程搭建、RTL/XDC 编写、综合、实现、时序与比特流生成。(★12 · 2026-03)
- [Fzhiyu1/chipforge-plugin](https://github.com/Fzhiyu1/chipforge-plugin) - 面向 Claude Code 的 AI FPGA 开发插件，含 chipforge skill，提供 Verilog 仿真与知识图谱。(★4 · 2026-01)
- [baranidh/FpgaSkills](https://github.com/baranidh/FpgaSkills) - 覆盖 FPGA 开发生命周期的 skill 库：功能规格、cocotb 验证、功能覆盖率收敛、比特流与 bring-up。(coll · ★0 · 2026-07)
- [edawise/edagent-skills](https://github.com/edawise/edagent-skills) - 开源的芯片设计验证 skill，覆盖 testbench 生成、波形调试、根因分析、RAL 寄存器模型生成与回归分诊，支持 Claude Code、Codex 与 Copilot。(coll · ★0 · 2026-08)
- [11philip22/fpga-skills](https://github.com/11philip22/fpga-skills) - 面向 Xilinx Spartan-6 命令行工作流的 Codex skill：用 Docker 化的 ISE 14.7 构建 Verilog、通过 OpenFPGALoader 烧写 SPI flash，以及 LiteX/LiteScope JTAGBone 调试流。(coll · ★1 · 2026-09)
- [hslee-cmyk/chip-design-skills](https://github.com/hslee-cmyk/chip-design-skills) - 芯片设计 skill，涵盖模拟 gm/Id 设计、芯片/形式化/UVM 验证与 Lattice FPGA 开发。(coll · ★0 · 2026-07)

### 无线

- [simpleble/simpleble `simpleaible`](https://github.com/simpleble/simpleble/tree/main/simpleaible) - SimpleBLE 官方的 MCP 与 Skill：从主机侧扫描、连接、GATT 读取与订阅。(official · ★1.1k · 2026-09)
- [meshtastic/meshtastic-mcp](https://github.com/meshtastic/meshtastic-mcp) - Meshtastic 官方 MCP，内置三个 Skill：通过串口 / TCP 发现、配置、烧录与监控电台，端到端测试，模拟器。(official · coll · ★15 · 2026-09)
- [project-chip/connectedhomeip `.agents/skills/`](https://github.com/project-chip/connectedhomeip/tree/master/.agents/skills) - 14 个 Matter SDK 贡献者 Skill：ZAP cluster 生成、代码驱动的 cluster TDD、chip-tool 测试、二进制体积对比。(official · coll · ★9k · 2026-09)
- [SmartThingsCommunity/SmartThingsEdgeDrivers `.agents/skills/`](https://github.com/SmartThingsCommunity/SmartThingsEdgeDrivers/tree/main/.agents/skills) - 三星官方用于编写 Zigbee / Z-Wave / Matter Lua edge driver 的 Skill：profile、库、测试流程。(official · coll · ★347 · 2026-09)
- [zwave-js/zwave-js `.agents/skills/`](https://github.com/zwave-js/zwave-js) - `author-config-from-web` 根据产品页面生成 Z-Wave 设备配置文件。(official · ★888 · 2026-09)
- [BrownFineSecurity/iothackbot](https://github.com/BrownFineSecurity/iothackbot) - 带物理工具的 IoT 渗透测试：JTAG 探测、逻辑分析仪 / MSO 抓取、picocom 串口控制台、telnet shell、chipsec、ONVIF 与网络扫描、jadx / apktool。(coll · ★846 · 2026-06)
- [BasedHardware/omi `.cursor/skills/`](https://github.com/BasedHardware/omi) - Omi 可穿戴设备 nRF / ESP32 Zephyr 蓝牙音频固件的 `omi-firmware-patterns`。(cursor-rules · ★13.5k · 2026-09)
- [veonua/SmartThingsEdge-Xiaomi `.agents/skills/`](https://github.com/veonua/SmartThingsEdge-Xiaomi) - SmartThings Edge driver 的 Zigbee 设备入网。(★82 · 2026-09)
- [ksachdeva/zephyr-rtos-ai `zephyr-bluetooth-le`](https://github.com/ksachdeva/zephyr-rtos-ai/tree/main/skills/zephyr-bluetooth-le) - Zephyr 中的 GAP / GATT / 广播 / 配对 / NUS。(★23 · 2026-06)
- [beriberikix/zephyr-agent-skills `connectivity-ble`](https://github.com/beriberikix/zephyr-agent-skills/tree/main/skills/connectivity-ble) - Zephyr BLE，以及覆盖 MQTT / CoAP / LwM2M 的姊妹 Skill `iot-protocols`。(★64 · 2026-05)
- [wangjianjq/Skill `.agents/skills/`](https://github.com/wangjianjq/Skill) - 用 Python 与 Wireshark 做蓝牙调试，另有一个泰克示波器 Skill。(coll · ★24 · 2026-02)
- [rnd-southerniot/rak3112-rs485-node `.claude/skills/`](https://github.com/rnd-southerniot/rak3112-rs485-node) - 在 ChirpStack 中为 RAK3172 / RAK3112 做 LoRaWAN OTAA 入网、注销与入网校验。(coll · ★1 · 2026-07)
- [JasonYANG170/esp-dev-skill `esp-zigbee-sdk`](https://github.com/JasonYANG170/esp-dev-skill/tree/main/repos/esp-zigbee-sdk) - ESP Zigbee SDK 子 Skill。(★27 · 2026-08)
- [SnailSploit/Claude-Red `Skills/wireless`](https://github.com/SnailSploit/Claude-Red) - 攻击向的 BLE、LoRaWAN / sub-GHz、Zigbee / Thread / Matter 与 Z-Wave Skill；仅安全侧。(coll · ★6.1k · 2026-08)
- [mateuszsury/uZigbee](https://github.com/mateuszsury/uZigbee) - 面向 ESP32-C6 的 MicroPython Zigbee 3.0 库，含七个 skill，覆盖原生 C 桥接、Zigbee 协议、固件构建、Python API、内存/性能与 CI。(coll · ★2 · 2026-02)
- [kuohsianglu/wisblock-zephyr-skills](https://github.com/kuohsianglu/wisblock-zephyr-skills) - 面向基于 Zephyr 的 RAK WisBlock 工程的 agent skill：数据手册驱动的 devicetree overlay 生成器，以及 LoRaWAN Class A 传感器上行应用脚手架。(coll · ★0 · 2026-02)
- [rnd-southerniot/rak4630-e-ink-claude](https://github.com/rnd-southerniot/rak4630-e-ink-claude) - 面向 RAK WisBlock LoRaWAN 节点的门控 ESP-IDF 固件 skill：RAK4630/RAK3312 引脚参考、PlatformIO 构建、串口抓取、ChirpStack 接入与 LoRaWAN provisioning。(coll · ★0 · 2026-07)
- [p0fi/matter-cli](https://github.com/p0fi/matter-cli) - Matter CLI 项目，含 esp32-matter skill 与 matter-js 测试设备 skill，用于在 ESP32 上构建与测试 Matter 设备。(★2 · 2026-09)
- [amscotti/hermes-meshtastic-adapter](https://github.com/amscotti/hermes-meshtastic-adapter) - Hermes Agent 插件，连接 Meshtastic LoRa mesh，接收明文 mesh 消息并转发给 agent。(★7 · 2026-09)
- [urmzd/zigbee-skill](https://github.com/urmzd/zigbee-skill) - AI 原生的智能家居 skill，让 agent 无需云端、无需网关直接控制 Zigbee 设备。(★0 · 2026-06)

### 硬件安全

- [solokeys/solo2](https://github.com/solokeys/solo2) - Solo 2 FIDO2 安全密钥固件，附带用于给密钥本身做量产配置的 `solo2-cli` 与 `solo2-examples` Skill。(official · coll · ★714 · 2026-08)
- [dslsdzc/rev-skills](https://github.com/dslsdzc/rev-skills) - 122 个逆向工程 Skill，含面向 UART、SPI、JTAG 的 `re-hardware-io` 与 `re-javacard`。(coll · ★64 · 2026-09)
- [keycard-tech/keycard-cli](https://github.com/keycard-tech/keycard-cli) - Keycard 智能卡 CLI，带 `keycard-admin` 与 `keycard-signing` Skill。(official · coll · ★57 · 2026-09)
- [nemanjan00/claude-code-skills](https://github.com/nemanjan00/claude-code-skills) - 一套很小的个人合集，恰好收录了目前仅有的 Bus Pirate 与智能卡 Skill。(coll · ★0 · 2026-08)
- [OrbitCurve/firmware-reverse-engineering](https://github.com/OrbitCurve/firmware-reverse-engineering) - 面向 Claude Code 与 Codex 的五个固件逆向 skill：unblob 提取、ELF 静态分析、带脚本的 Ghidra 逆向、QEMU/Firmadyne 仿真与安全报告。(coll · ★190 · 2026-09)
- [darkmentorllc/bt-re-mad-skillz](https://github.com/darkmentorllc/bt-re-mad-skillz) - 用于在 HCI 层及以下逆向蓝牙控制器固件的 LLM skill，为 Claude Code 与 Codex 驱动 Ghidra。(coll · ★29 · 2026-08)
- [ByteLandTechnology/headless-ghidra](https://github.com/ByteLandTechnology/headless-ghidra) - 无头 Ghidra 逆向 skill 家族，面向可复现、带证据的工作流：intake、发现、批量反编译、函数分析与 agent CLI。(coll · ★5 · 2026-05)
- [jxw1102/flipper-claude-buddy](https://github.com/jxw1102/flipper-claude-buddy) - 面向 Flipper Zero 工作流的 Claude Code 插件，含 notify skill 与配套工具。(★49 · 2026-07)
- [Nikolaibibo/flipper-blackhat-skill](https://github.com/Nikolaibibo/flipper-blackhat-skill) - 面向运行 BlackHat OS 的 Flipper Zero WiFi 开发板的 Claude WiFi 渗透测试 skill，涵盖侦察、攻击规划与 BlackHat OS 命令。(★4 · 2025-10)
- [vezril/claude-toolkit](https://github.com/vezril/claude-toolkit) - 个人 Claude 工具集，其 skill 含 flipper-zero 与 flipper-unleashed，用于操作 Flipper Zero 与 Unleashed 固件。(coll · ★1 · 2026-09)

### 汽车

- [CSS-Electronics/can-bus-reverse-engineering-skills](https://github.com/CSS-Electronics/can-bus-reverse-engineering-skills) - 三个 Skill，用 CANsub USB / 以太网接口在真实 OBD2 口上把实时 CAN 流量逆向成 DBC 文件。(official · coll · ★172 · 2026-08)
- [ecubus/EcuBus-Pro `resources/skills/`](https://github.com/ecubus/EcuBus-Pro/tree/master/resources/skills) - EcuBus-Pro 的 TypeScript 脚本 API（UDS、CAN-TP、DoIP、LIN、总线事件），配合其自家 USB CAN / LIN 适配器。(official · ★870 · 2026-09)
- [philipkocanda/canair](https://github.com/philipkocanda/canair) - WiCAN OBD-II Wi-Fi / 蓝牙 dongle 工具箱，带信号逆向与 WiCAN 协议 Skill。(coll · ★26 · 2026-08)
- [spawahh/openpilot-claude-kit](https://github.com/spawahh/openpilot-claude-kit) - 四个面向 openpilot 的 Claude Code 插件，含只读的 comma 设备 API 与 SSH 设备操作。(coll · ★2 · 2026-08)
- [JiaxI2/Codex-Skills `ethercat-cia402`](https://github.com/JiaxI2/Codex-Skills) - EtherCAT 从站 / CiA 402 / TwinCAT NC 诊断。中文。(★1 · 2026-09)
- [danielrosehill/Claude-OBD-Diagnostics-Plugin](https://github.com/danielrosehill/Claude-OBD-Diagnostics-Plugin) - 开发中的 Claude Code 插件：从 ELM327 类适配器读取 OBD-II 数据并保存为 JSON 快照或 NDJSON 行车日志，解码故障码、诊断故障并规划保养；其采集脚本尚未在真实车辆上运行过。(coll · ★0 · 2026-08)
- [wexcomm/hp-tuners-ai-agent](https://github.com/wexcomm/hp-tuners-ai-agent) - 面向 LFX 3.6L V6 的 HP Tuners ECU 调校与车辆诊断 agent，附带 HPT 文件转换和 SAE J2534 PassThru 访问的 skill。(coll · ★8 · 2026-04)
- [thongdt89/asr_bsw](https://github.com/thongdt89/asr_bsw) - AUTOSAR Classic BSW 配置用的 Codex skill：ARXML 清点、BSW 评审、补丁建议，以及配置 Com、PduR、CanIf、CanTp 等模块。(coll · ★2 · 2026-07)
- [ptsilivis/autonomousguy](https://github.com/ptsilivis/autonomousguy) - 面向汽车嵌入式工程师的 AI skill，涵盖 AUTOSAR BSW 与 SWC（COM 协议栈、ARXML、RTE、CAN/LIN/以太网/UDS）、MISRA、ISO 26262 和 ECU 代码评审。(coll · ★32 · 2026-07)
- [Washabii14/agent-skills `skills/automotive-embedded-skills/`](https://github.com/Washabii14/agent-skills/tree/main/skills/automotive-embedded-skills) - 针对汽车 ECU 的 C/C++ 与 CAPL 实践 skill，遵循 MISRA、AUTOSAR、ISO 26262 和 ISO 21434，涵盖 CAN FD、LIN、以太网、DoIP 和 SOME/IP 通信。(★12 · 2026-02)
- [sdv-playground/SOVDd `.skills/`](https://github.com/sdv-playground/SOVDd/tree/main/.skills) - 用 Rust 实现的 ASAM SOVD 服务器，把 REST 调用转换为经 CAN/ISO-TP 或 DoIP 发送的 UDS 命令，附带 ECU 配置、软件刷写与 OTA 以及问题排查的 skill。(coll · ★0 · 2026-09)
- [TongLi0406/uds-diagnostic-test](https://github.com/TongLi0406/uds-diagnostic-test) - UDS 诊断测试 skill：解析诊断调查表，为 DID、DTC、IOControl 和 RoutineControl 生成测试脚本，经 CAN 执行并生成报告。(★3 · 2026-05)
- [canforge/dbckit](https://github.com/canforge/dbckit) - 用于解析、编辑、校验、比对和编解码 DBC（CAN 数据库）文件的 Python 库与 CLI，附带指导 agent 正确使用的 skill。(★0 · 2026-07)
- [matlab/simulink-agentic-toolkit](https://github.com/matlab/simulink-agentic-toolkit) - MathWorks 官方的 Simulink skill 目录，面向基于模型的设计，包括嵌入式代码生成与优化、A2L 定制、电机控制、Simscape 建模和模型测试。(official · coll · ★1.1k · 2026-09)

### 工业 / PLC

- [bulaofen0036-coder/TIA_Portal_Openness_MCP](https://github.com/bulaofen0036-coder/TIA_Portal_Openness_MCP) - 西门子博途 V20 / V21：通过 MCP 创建、编译并下载 STEP 7 与 WinCC 工程，内置一个 Skill。(★252 · 2026-09)
- [Czarnak/totally-integrated-claude](https://github.com/Czarnak/totally-integrated-claude) - 带路由的博途 Openness 插件（20+ 个 Skill）：PLC 操作、导入导出、网络组态、HMI、Python、MAC 模块生成。(coll · ★62 · 2026-08)
- [huahaizo/tia-portal-openness-ai](https://github.com/huahaizo/tia-portal-openness-ai) - 博途 Openness V15–V21 的 C# / PowerShell 脚手架。(★66 · 2026-05)
- [MichielVanwelsenaere/HomeAutomation.CoDeSys3 `.claude/skills/`](https://github.com/MichielVanwelsenaere/HomeAutomation.CoDeSys3) - 通过 ScriptEngine 无头运行 CODESYS：对二进制 `.project` 做编译检查、排查 PLC 异常。(coll · ★147 · 2026-09)
- [ArthurkaX/cds-text-sync](https://github.com/ArthurkaX/cds-text-sync) - CODESYS 与结构化文本的双向同步 CLI，带 IDE 守护进程与 PLC 下载，另有一个 visu-SVG Skill。(coll · ★95 · 2026-09)
- [midea-ai/SemaPLC](https://github.com/midea-ai/SemaPLC) - 美的的 Agent 化 PLC IDE，带 `plc-spec-review` Skill。(official · ★88 · 2026-09)
- [MIGO-OvO/plc-skill](https://github.com/MIGO-OvO/plc-skill) - 厂商中立的 IEC 61131-3 ST / LD / FBD / SFC，带厂商路由；ClawHub 约 1000 次安装。(★23 · 2026-05)
- [Navifra-Sally/vda5050-skill](https://github.com/Navifra-Sally/vda5050-skill) - VDA 5050 AGV 与 AMR 机队协议：规范要点、JSON schema 与消息校验器。(★0 · 2026-09)
- [eponce00/twincat-mcp](https://github.com/eponce00/twincat-mcp) - 通过 MCP 完成 TwinCAT 3 构建、部署、TcUnit 与 ADS 检视。(★29 · 2026-09)
- [TechIndustryX/twincat-agent](https://github.com/TechIndustryX/twincat-agent) - TwinCAT 结构化文本规约，外加一个 MCP 可执行程序。(coll · ★29 · 2026-06)
- [SionVerhoef/twincat-st](https://github.com/SionVerhoef/twincat-st) - TwinCAT 3 / CODESYS 结构化文本，带可执行的 `st_review.py`（阻塞循环、浮点相等判断）。(★1 · 2026-09)
- [FREEZONEX/ia2](https://github.com/FREEZONEX/ia2) - Agent 优先的 IEC 61131-3 IDE 与运行时，支持 Modbus、EtherCAT、OPC UA、CANopen 与 HMI。(★6 · 2026-09)
- [gmantoha/ctrlx-os-agent-skills](https://github.com/gmantoha/ctrlx-os-agent-skills) - 博世力士乐 ctrlX OS / CORE snap、Data Layer、PLC。(★6 · 2026-09)
- [Meisterschulen-am-Ostbahnhof-Munchen/4diac_training1 `.agents/skills/`](https://github.com/Meisterschulen-am-Ostbahnhof-Munchen/4diac_training1) - 面向 Eclipse 4diac 的 IEC 61499 功能块、适配器与系统。(★1 · 2026-09)
- [OPCFoundation/UA-.NETStandard `.agents/skills/`](https://github.com/OPCFoundation/UA-.NETStandard) - OPC 基金会 .NET 协议栈的 `opcua-v20-migration`。(official · ★2.4k · 2026-09)
- [riclolsen/json-scada `.agents/skills/`](https://github.com/riclolsen/json-scada) - 为 JSON-SCADA 增加 Modbus / DNP3 / IEC 60870 / IEC 61850 驱动的 `protocol-driver-development`。(official · ★424 · 2026-08)
- [studioxvii/modbus-skills](https://github.com/studioxvii/modbus-skills/tree/main/plugins/modbus-skills/skills) - 20 个只读的 Modbus 工程 Skill：从原厂 PDF 提取寄存器表、归一化、校验字节序、规划读取、生成 modpoll / ModScan / Node-RED 工具包、分析抓包。(coll · ★1 · 2026-09)
- [wirenboard/wb-ai-skills](https://github.com/wirenboard/wb-ai-skills) - Wiren Board PLC 厂商 Skill：通过 MQTT 与 Modbus 与控制器通信、编写 wb-rules、管理 Zigbee 与串口设备、根因分析。(official · coll · ★3 · 2026-09)
- [TuojianLYU/openplc-codex-skill](https://github.com/TuojianLYU/openplc-codex-skill) - 生成带梯形图 `.ld` 文件的 OpenPLC v4 工程。(★1 · 2026-06)
- [arkbsz/siemens-tia-skill-suite](https://github.com/arkbsz/siemens-tia-skill-suite) - 面向 Codex 等 agent 的 Siemens TIA Portal V16-V21 skill 套件：Openness 就绪检查、项目备份、PLC-as-code 工作区、SCL/LAD/FBD 读写、WinCC HMI 自动化以及 Codex TIA 客户端工作流。(coll · ★2 · 2026-09)
- [ac-rosu/skills](https://github.com/ac-rosu/skills) - 面向 TIA Portal 中 Siemens S7-1200/S7-1500 编程（SCL、LAD、FBD、STL、GRAPH、CEM）以及 WinCC Unified 脚本与自定义 Web 控件的 skill。(coll · ★0 · 2026-09)
- [rraxge/Agent_skill_tia_openness_api](https://github.com/rraxge/Agent_skill_tia_openness_api) - TIA Portal V19 Openness API skill：创建与打开项目、导入导出 PLC 块、管理变量表、编写 LAD/SCL XML 以及调试 Openness 报错。(★2 · 2026-06)
- [mianmianlingqi/tia-openness-reader](https://github.com/mianmianlingqi/tia-openness-reader) - 附带 C# CLI 的 Codex skill，通过 Openness 读取 TIA Portal V17 项目、导出 PLC 块和变量，并分析导出的 XML。(★0 · 2026-05)
- [ActionUnity/tia-v18-lad-agent](https://github.com/ActionUnity/tia-v18-lad-agent) - 通过 Openness 导出、导入和编译以 LAD 编辑 Siemens TIA Portal V18 PLC 对象的 harness skill，为 FB/FC XML、全局 DB、UDT 和变量表设有安全关卡。(★0 · 2026-07)
- [Lance0901/AI-TwinCAT-Skill](https://github.com/Lance0901/AI-TwinCAT-Skill) - 包含 34 个 cmdlet 的 PowerShell 模块及配套 skill，让 AI 工具自动化 TwinCAT 3 IDE、构建和部署 PLC 程序、通过 ADS 读写变量并运行测试。(★14 · 2026-04)
- [idomp/twincat-skills](https://github.com/idomp/twincat-skills) - 驱动 TwinCAT MCP server 的 skill 与配置文档：自动化、代码搜索、驱动器参数、.tsproj 映射和 Scope 录制。(coll · ★0 · 2026-06)
- [georgeturneruk/tckit `.claude/skills/`](https://github.com/georgeturneruk/tckit/tree/main/.claude/skills) - TwinCAT MCP server，附带构建、部署与 TcUnit 测试循环、Beckhoff 文档查询、配置和 ADR 的 skill。(coll · ★5 · 2026-08)
- [SionVerhoef/twincat-scope](https://github.com/SionVerhoef/twincat-scope) - 录制并分析 Beckhoff TwinCAT 3 Scope 测量的 skill：包络图、事件检测和 .tcscopex 配置生成。(★0 · 2026-09)
- [DiamondLightSource/fastcs-catio `.claude/skills/`](https://github.com/DiamondLightSource/fastcs-catio/tree/main/.claude/skills) - Diamond Light Source 基于 pyads 将 TwinCAT 下 EtherCAT I/O 接入 FastCS 的项目，附带 Beckhoff ESI XML、ADS 模拟器测试和控制器连接的 skill。(coll · ★1 · 2026-09)
- [chency1024dy/Codesys-Skill](https://github.com/chency1024dy/Codesys-Skill) - 通过官方 CLI 和 ScriptEngine 操作 CODESYS 3.5 与 HCPWorks3 项目的 CLI 与 skill：查看和编辑 ST、POU、GVL、任务与 I/O，构建并诊断编译错误。(★3 · 2026-09)
- [mokouliszt/iec61131-3-motioncontrol-skill](https://github.com/mokouliszt/iec61131-3-motioncontrol-skill) - 使用三菱 MELSEC iQ-R PLCopen Motion Control 功能块编写 IEC 61131-3 ST 的 skill，适用于 RD77 简易运动模块以及 CC-Link IE Field + MR-J4-GF 伺服。(★0 · 2026-05)
- [johannesPettersson80/trust-platform `.codex/skills/`](https://github.com/johannesPettersson80/trust-platform/tree/main/.codex/skills) - truST（IEC 61131-3 结构化文本工具链）仓库中的 Codex skill：IEC 合规判定、LSP 开发、HMI 契约、测试编写和发布关卡。(coll · ★220 · 2026-09)
- [php-opcua/opcua-cli `.ai/skills/opcua-cli/`](https://github.com/php-opcua/opcua-cli/tree/master/.ai/skills/opcua-cli) - OPC UA 命令行工具，附带 skill 讲解其命令：浏览、读取、写入和监视数值，探索地址空间，发现端点以及管理证书信任。(★0 · 2026-08)
- [TheThoughtagen/ignition-ide-plugins `claude-code-plugin/skills/`](https://github.com/TheThoughtagen/ignition-ide-plugins/tree/main/claude-code-plugin/skills) - 面向 Inductive Automation Ignition 的 Claude Code 插件，含 system.* 脚本 API、表达式、lint、测试和端到端测试的 skill。(coll · ★14 · 2026-09)
- [vogler75/monster-mq `.agents/skills/`](https://github.com/vogler75/monster-mq/tree/main/.agents/skills) - MQTT broker，附带 skill 用于接入 Modbus、OPC UA 等新设备连接器，以及 broker 配置、GraphQL 配置与数据和仪表板开发。(coll · ★142 · 2026-09)
- [dscsystems/scadavis-synoptic3 `skills/`](https://github.com/dscsystems/scadavis-synoptic3/tree/main/skills) - SCADAvis Synoptic Toolkit Web 组件，附带其 API 和 SVG 画面的 skill，用于实时工业看板。(official · coll · ★4 · 2026-04)

### 专业 AV 与楼宇系统

- [shorty456132/av-module-maker](https://github.com/shorty456132/av-module-maker) - 生成 Q-SYS、Extron 与 Crestron 控制模块，带 SIMPL+、SIMPL# 与 SIMPL# Pro Skill。(coll · ★9 · 2026-09)
- [Crestron/CrestronAISkills](https://github.com/Crestron/CrestronAISkills) - Crestron 官方面向 AV 控制编程的 Skill 插件与 Copilot 版本；唯一发布 Skill 的专业 AV 厂商。(official · coll · ★4 · 2026-09)
- [mvanhorn/printing-press-library `cli-skills/pp-qsys/`](https://github.com/mvanhorn/printing-press-library/tree/main/cli-skills/pp-qsys) - 驱动 qsys-pp-cli 离线索引的 Q-SYS skill，涵盖规格、配置、接线、兼容性和故障文章，可用来核对设备清单；同目录的 pp-crestron 索引 Crestron 产品、规格书和固件，pp-extron 索引 Extron 规格书与手册。(★2k · 2026-09)
- [RAKWireless/RAK-BACnet-Profiles `.agents/skills/generate-bacnet-profile/`](https://github.com/RAKWireless/RAK-BACnet-Profiles/tree/main/.agents/skills/generate-bacnet-profile) - RAKwireless 官方 skill，依据协议文档、解码器和样例报文生成或修复 RAK BACnet 设备 Profile，含上行、下行和测试夹具。(official · ★0 · 2026-09)
- [songzh96/aptishome-knx-edge-agent](https://github.com/songzh96/aptishome-knx-edge-agent) - AptisHome KNX Edge（ESP32 网关）的 MCP 与 OpenAPI 桥接，附带 Codex skill 管理 KNX 房间、设备、场景和本地自动化并控制设备。(★0 · 2026-08)
- [bbartling/diy-bacnet-router `.cursor/skills/`](https://github.com/bbartling/diy-bacnet-router/tree/master/.cursor/skills) - 嵌入式 Linux BACnet 路由器项目，附带 skill：为教学用路由器提供产品与仪表板上下文，并在本地虚拟机中调试 Buildroot 系统构建。(coll · ★0 · 2026-09)

### 实验室仪器

- [nominal-io/instro](https://github.com/nominal-io/instro) - 带类型的多厂商仪器库（电源、万用表、示波器、数采、电子负载），其 Skill 负责生成新驱动并在真实仪器上验证。(official · coll · ★704 · 2026-09)
- [ma-compbio-lab/SkillFoundry](https://github.com/ma-compbio-lab/SkillFoundry) - 科研 Agent 的 Skill 框架，其 `qcodes-parameter-sweep-starter` 是找到的唯一 QCoDeS 参数扫描 Skill。(coll · ★39 · 2026-09)
- [RRGGZZ/Zurich_Instruments_Skills](https://github.com/RRGGZZ/Zurich_Instruments_Skills) - 苏黎世仪器 MFLI 锁相放大器。(★1 · 2026-07)
- [jetperch/pyjoulescope_ui `ui-remote`](https://github.com/jetperch/pyjoulescope_ui/tree/main/.claude/skills/ui-remote) - 通过 TCP 远程控制接口驱动 Joulescope 功耗分析仪的界面。(official · ★110 · 2026-09)
- [Scaxlibur/WaveBench](https://github.com/Scaxlibur/WaveBench) - SCPI 台式仪器 Skill 集。(★63 · 2026-09)
- [Erlla/DS1202ZE-skills](https://github.com/Erlla/DS1202ZE-skills) - 通过 USBTMC 操作普源 DS1202Z-E 示波器，配 Python CLI；姊妹项目 `DM3058E-skills` 对应万用表。(★1 · 2026-07)
- [K-Dense-AI/scientific-agent-skills `opentrons-integration`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/opentrons-integration) - 面向真实 OT-2 / Flex 机器人编写 Opentrons Protocol API v2，位于一个非常大的通用科研 Skill 库中（星数是整库的）。(★45.5k · 2026-09)
- [KRATSZ/labscriptai-ot](https://github.com/KRATSZ/labscriptai-ot) - Opentrons 插件：MCP server、七个 Skill、安全策略、协议库。(coll · ★2 · 2026-07)
- [DCC-Lab/PyHardwareLibrary](https://github.com/DCC-Lab/PyHardwareLibrary) - USB / 串口实验设备库（光谱仪、位移台、激光器、数采），带一个编写驱动的 Skill。(★12 · 2026-08)
- [deepmodeling/Uni-Lab-OS](https://github.com/deepmodeling/Uni-Lab-OS) - 自动化实验室平台，带 AGENTS.md 与一个 `add-device` Cursor Skill。(cursor-rules · ★178 · 2026-09)
- [BCDA-APS/opencode-skills](https://github.com/BCDA-APS/opencode-skills) - 面向 Argonne APS 光束线 EPICS 开发的 OpenCode skill，包括 Aerotech AeroScript 运动程序、areaDetector 驱动与 IOC 以及 synApps IOC。(coll · ★2 · 2026-06)
- [curtisgalloway/public-skills `plugins/hardware-lab/`](https://github.com/curtisgalloway/public-skills/tree/main/plugins/hardware-lab) - hardware-lab 插件中的 skill：通过 SCPI 控制 Siglent SDS1000X-E 示波器、Bus Pirate、Cynthion USB 抓包与解码，以及 MCCI 3411 USB 开关。(coll · ★2 · 2026-09)
- [determlab/shal `integrations/claude-code/skills/`](https://github.com/determlab/shal/tree/main/integrations/claude-code/skills) - SHAL 把实验室软硬件变成有类型、受权限管控的 agent 工具，附带 Claude Code skill 用于编写新设备驱动、总线传输和 YAML 配置。(coll · ★2 · 2026-09)
- [pragmatest-dev/testerkit `src/testerkit/skills/`](https://github.com/pragmatest-dev/testerkit/tree/main/src/testerkit/skills) - 基于 pytest 的电子产品验证与量产硬件测试平台，附带测试工位、采集波形与传感器证据、数据和规格书相关 skill。(coll · ★1 · 2026-09)
- [pragmatest-dev/lvkit `src/lvkit/skill_templates/`](https://github.com/pragmatest-dev/lvkit/tree/main/src/lvkit/skill_templates) - 无需安装 LabVIEW 即可描述、渲染、比对和转换 VI 的 CLI，附带由 lvkit setup 安装的 agent skill，用于描述、文档化、查询、评审、解析和转换 VI。(coll · ★38 · 2026-09)
- [sendu2wfdx/rigol-dho-scpi](https://github.com/sendu2wfdx/rigol-dho-scpi) - 通过 LAN 或 USBTMC/VISA 查询和控制 RIGOL DHO800/DHO900 示波器的 Codex skill。(★0 · 2026-08)
- [fooping-tech/rigol_ds1104 `.codex/skills/rigol-ds1104z-lan/`](https://github.com/fooping-tech/rigol_ds1104/tree/main/.codex/skills/rigol-ds1104z-lan) - 通过 LAN/LXI 控制 RIGOL DS1104Z 示波器的 skill：SCPI、截图、单次捕获、波形 CSV 导出和测量记录。(★1 · 2026-05)
- [chouswei/MXO4-SigCapture `.cursor/skills/rs-scpi-scopes/`](https://github.com/chouswei/MXO4-SigCapture/tree/main/.cursor/skills/rs-scpi-scopes) - 在 MXO4 远程采集项目中编写、评审和调试 Rohde & Schwarz 示波器（MXO4/5、RTO/RTO6、RTP、RTM/RTA）SCPI 的 skill。(★0 · 2026-07)
- [zhaojiseng/debug-lab-instruments](https://github.com/zhaojiseng/debug-lab-instruments) - 附带 LAN-SCPI Python 控制脚本的 skill，用于 SIGLENT SDG 信号发生器和 RIGOL DHO/MHO 示波器：设备发现、连接测试、波形输出和测量。(★0 · 2026-07)
- [LHX369963/sdg2122-cli](https://github.com/LHX369963/sdg2122-cli) - 面向 SIGLENT SDG2122X 波形发生器的类型化 Linux USBTMC CLI 与 Codex skill，覆盖双通道输出、调制、扫频、脉冲串和任意波。(★0 · 2026-08)
- [Erlla/DM3058E-skills](https://github.com/Erlla/DM3058E-skills) - RIGOL DM3058E 数字万用表的 skill：通过 USBTMC 读取、记录和 SCPI 控制，支持 Windows 原生 USB 通信。(★1 · 2026-07)
- [zxf1023818103/cmw-wlan-test](https://github.com/zxf1023818103/cmw-wlan-test) - 基于纯 SCPI 在 Rohde & Schwarz CMW500 上自动化 WLAN 信令测试的 Claude Code skill 与 Python 脚本。(★0 · 2026-08)
- [pasrom/kiprim-psu](https://github.com/pasrom/kiprim-psu) - KIPRIM DC310S/DC605S（OWON SPE3103/SPE6053）台式电源的 USB 串口驱动、CLI 与 skill。(★0 · 2026-07)
- [metachow/instrument-software-skill](https://github.com/metachow/instrument-software-skill) - 中英双语 skill，用于开发 SMU、锁相放大器、温控器等科学仪器的 Python 控制软件。(★0 · 2026-06)
- [DavidBlackCN/econtest-bench-mcp](https://github.com/DavidBlackCN/econtest-bench-mcp) - 面向电赛低压信号题的 USB/VISA MCP server 与 skill，安全控制 SIGLENT SDS2000X Plus 示波器和 SDG6000X 信号发生器。(★1 · 2026-08)
- [HuMoran/tt-skills](https://github.com/HuMoran/tt-skills) - 个人 Claude Code skill 集，含 Keysight DSO5000 与 RIGOL DS1000Z 示波器驱动、RS-485 Modbus RTU、PTC Creo J-Link 自动化以及 EasyEDA Pro 转 KiCad。(coll · ★0 · 2026-08)
- [analogdevicesinc/scopy `tools/scopy_dev_plugin/skills/`](https://github.com/analogdevicesinc/scopy/tree/main/tools/scopy_dev_plugin/skills) - Analog Devices 为其示波器与信号分析软件 Scopy 提供的开发 skill，涵盖 IIO 控件模式、API 质量检查和插件开发。(official · coll · ★499 · 2026-09)
- [Opentrons/opentrons `.cursor/skills/`](https://github.com/Opentrons/opentrons/tree/edge/.cursor/skills) - Opentrons monorepo 中面向 Flex 与 OT-2 移液机器人软件的 Cursor skill，包括机器人 Python 项目、analyses 快照测试以及 AI 客户端/服务端开发。(official · coll · ★520 · 2026-09)
- [jsgoecke/photron-fastcam-skill](https://github.com/jsgoecke/photron-fastcam-skill) - 用 PDCLIB SDK 编程和集成 Photron FASTCAM 高速相机（Mini R5-4K、Nova、SA-Z）的 skill。(★0 · 2026-02)
- [ni/labview-fpga-hdl-tools `.github/skills/labview-fpga-hdl-tools/`](https://github.com/ni/labview-fpga-hdl-tools/tree/main/.github/skills/labview-fpga-hdl-tools) - NI 官方 skill，讲解 nihdl Python CLI，为 NI FPGA 硬件目标自动化 Vivado 工程创建、编译、目标插件生成和 LabVIEW 集成。(official · ★3 · 2026-09)

### 数字制造

- [codeofaxel/Kiln](https://github.com/codeofaxel/Kiln) - 一个覆盖 OctoPrint、Moonraker、拓竹、Prusa Link、Elegoo、Duet 与 Marlin 的 3D 打印 MCP，外加无头的 PrusaSlicer / Orca / 拓竹切片；`pip install kiln3d`，附带 SKILL.md。(★63 · 2026-09)
- [earthtojake/text-to-cad `bambu-labs` / `gcode`](https://github.com/earthtojake/text-to-cad/tree/main/skills/bambu-labs) - 拓竹打印机控制与 G-code 生成；`bambu-labs` 在 skills.sh 上约 6700 次安装。(★16.1k · 2026-09)
- [santiagomoneta/3d-printing-skills](https://github.com/santiagomoneta/3d-printing-skills) - 通过 Moonraker API 做 Klipper 配置、诊断与校准，外加 OrcaSlicer。(coll · ★4 · 2026-03)
- [George-RD/cli-anything-meerk40t](https://github.com/George-RD/cli-anything-meerk40t) - 封装真实的 MeerK40t 内核（GRBL / 睿达 / 力辉宇），由 Agent 无头驱动激光任务。(★2 · 2026-08)
- [jl-codes/laser-skills](https://github.com/jl-codes/laser-skills) - LightBurn 设计、预检与任务 Skill；只做设计，绝不真正出光。(coll · ★0 · 2026-08)
- [Lordgrimz/escpos-skill](https://github.com/Lordgrimz/escpos-skill) - 依据官方规范逐字节生成热敏小票打印机的 ESC/POS 指令流。(★0 · 2026-04)
- [johncattrall/keymap-ai](https://github.com/johncattrall/keymap-ai) - 审查并生成 ZMK / QMK 键位映射（home-row mods、层）。(★22 · 2026-08)
- [FracktalWorks/agent-3dprinter-expert](https://github.com/FracktalWorks/agent-3dprinter-expert) - Fracktal Works 官方 agent，用于调试其基于 Klipper 的 3D 打印机（Dragon、TwinDragon、Volterra），覆盖 Klipper 日志、OctoPrint 与 Moonraker API、printer.cfg、MCU 和热敏电阻故障。(official · coll · ★0 · 2026-08)
- [moggieuk/Happy-Hare `.claude/skills/`](https://github.com/moggieuk/Happy-Hare/tree/main/.claude/skills) - 面向 ERCF、Tradrack、Box Turtle 等多色换料器的 Klipper MMU 驱动，附带关于料道限位不变量、NFC/RFID 子系统和 Kconfig 菜单的 Claude Code skill。(coll · ★1.1k · 2026-09)
- [makermate/claw3d-skill](https://github.com/makermate/claw3d-skill) - 模块化的 3D 工作流 skill：用 AI 生成模型、搜索 Thingiverse、切片并发送打印。(★64 · 2026-03)
- [bbolinger/snapmaker-u1-toolkit](https://github.com/bbolinger/snapmaker-u1-toolkit) - 通过 Telegram 在手机上向 Snapmaker U1 发起打印的工具包，含无头 OrcaSlicer、Moonraker 上传、摄像头确认和人工批准开打，另附切片自动化 skill。(★20 · 2026-09)
- [estampo/estampo](https://github.com/estampo/estampo) - 可复现 3D 打印的构建系统，附带 skill：配置 estampo.toml、选择切片引擎与配置，并为 STL、STEP、3MF 或代码 CAD 输出运行打印流水线。(★16 · 2026-08)
- [CarlosZiegler/bambu-h2c-skills](https://github.com/CarlosZiegler/bambu-h2c-skills) - 面向 Bambu Lab H2C 的 skill：在 Bambu Studio 中切片并校验项目（含 AMS 与喷嘴映射）、执行已授权的打印、FDM 打印前检查、打印故障排查以及准备 Blender 模型。(coll · ★2 · 2026-09)
- [Ethan2298/bambu-printer-agent-plugin](https://github.com/Ethan2298/bambu-printer-agent-plugin) - 在 Mac 本地运行的 agent 插件，封装 bambu-printer-mcp，并附带检查和控制 Bambu Lab A1 打印机的 skill。(★0 · 2026-09)
- [phoenixjyb/openclaw-3dprint](https://github.com/phoenixjyb/openclaw-3dprint) - OpenClaw skill，实现文字到 3D 打印的流水线，把聊天消息变成 Bambu Lab 打印机上的实物。(★3 · 2026-03)
- [Flatsher/elegoo-centauri-skill](https://github.com/Flatsher/elegoo-centauri-skill) - 通过 SDCP WebSocket 协议控制和监控 Elegoo Centauri Carbon 3D 打印机的 skill：状态、温度、文件、打印控制、风扇、灯光、移轴和上传。(★0 · 2026-04)
- [danthi123/Q1Libre `.claude/skills/`](https://github.com/danthi123/Q1Libre/tree/main/.claude/skills) - Qidi Q1 Pro 的开源固件补丁，附带 Claude Code skill：通过 USB 部署、给 Klipper 打补丁、诊断打印机和发布版本。(coll · ★7 · 2026-07)
- [ttracx/qidi-q2-hermes](https://github.com/ttracx/qidi-q2-hermes) - Qidi Q2 3D 打印机的 Hermes Agent 集成，借助 Moonraker API 实现自然语言控制、监控和延时摄影。(★1 · 2026-08)
- [toprak1919/flashforge-3d-print-skill](https://github.com/toprak1919/flashforge-3d-print-skill) - FlashForge 网络打印的 Claude Code skill：打印机发现、切片、G-code 转换（M82 转 M83）、上传与流式传输。(★0 · 2026-03)
- [therynamo/3d-print-skill](https://github.com/therynamo/3d-print-skill) - Claude skill：导入模型、按固化的调整规则切片、预览，并把实际打印任务发送到打印机。(★1 · 2026-07)
- [jchadwick/autofab-skills](https://github.com/jchadwick/autofab-skills) - 从模型到打印的闭环 skill：3D 建模、打印机配置、切片，以及通过 Moonraker 上传、排队和启动 G-code。(coll · ★0 · 2026-07)
- [flux3dp/beam-studio `.agents/skills/`](https://github.com/flux3dp/beam-studio/tree/main/.agents/skills) - FLUX 官方 Beam Studio 激光软件仓库，附带 FCode 任务格式、相机标定与预览、路径预览和打印后切割的 skill。(official · coll · ★25 · 2026-09)
- [peytoncasper/modeling `skills/`](https://github.com/peytoncasper/modeling/tree/main/skills) - Fusion 360 skill：草图、实体、装配和 CAM，包括 CAM 设置以及自适应清角、轮廓、等高残留等 2D/3D 加工操作。(coll · ★1 · 2026-03)
- [KlaKalma/Ma_CNC `.claude/skills/`](https://github.com/KlaKalma/Ma_CNC/tree/main/.claude/skills) - 基于 EtherCAT 伺服和 RS-485 变频器的 LinuxCNC 机床项目，附带 LinuxCNC 配置、EtherCAT、手轮 HMI、切削参数和安全联锁的 Claude Code skill。(coll · ★2 · 2026-08)

### 智能家居

- [home-assistant/core `.claude/skills/`](https://github.com/home-assistant/core/tree/dev/.claude/skills) - 用于编写 Home Assistant 集成的 `ha-integration-knowledge`、`ha-quality-scale-verify`、`ha-review`。(official · coll · ★90.7k · 2026-09)
- [komal-SkyNET/claude-skill-homeassistant](https://github.com/komal-SkyNET/claude-skill-homeassistant/tree/main/skills/home-assistant-manager) - 通过 API 管理 Home Assistant：新版自动化 YAML（2024.10+）、仪表盘、应用变更前的校验流程。(★961 · 2026-07)
- [homeassistant-ai/skills `home-assistant-best-practices`](https://github.com/homeassistant-ai/skills/tree/main/skills/home-assistant-best-practices) - 自动化、辅助实体、脚本、仪表盘、蓝图；skills.sh 上安装量最高的硬件相关 Skill（约 7000 次）。(★750 · 2026-09)
- [tuya/tuya-openclaw-skills](https://github.com/tuya/tuya-openclaw-skills) - `tuya-smart-control` 通过 tuya.ai 密钥在 OpenClaw 中控制涂鸦设备（云端侧）。(official · ★510 · 2026-04)
- [jtenniswood/espcontrol `.agents/skills/`](https://github.com/jtenniswood/espcontrol) - `flash-displays` 负责通过 ESPHome OTA 与 USB 烧录 ESP32 屏幕板。(★1k · 2026-09)
- [bradsjm/hassio-addons](https://github.com/bradsjm/hassio-addons) - 通过加载项发布的七个 HA Skill：自动化脚本、仪表盘卡片、实体与服务、ESPHome、集成、自定义集成、AWTRIX。(coll · ★45 · 2026-07)
- [nodnarbnitram/claude-code-extensions `esphome-config-helper`](https://github.com/nodnarbnitram/claude-code-extensions) - ESPHome YAML 的生成、校验与排障。(★16 · 2026-04)
- [tonylofgren/aurora-smart-home](https://github.com/tonylofgren/aurora-smart-home) - 覆盖整个智能家居的独立 Claude skill：Home Assistant、ESPHome、Node-RED、自定义集成、仪表板以及可直接生产的硬件设计。(coll · ★104 · 2026-09)
- [SmartThingsCommunity/wwst-skills](https://github.com/SmartThingsCommunity/wwst-skills) - 面向 Works With SmartThings 开发者的 SmartThings skill：Hub 接入、云接入和直连（st-device-sdk-c）设备、应用间账号关联以及 Matter 与 Zigbee 的二维码入网。(official · coll · ★21 · 2026-07)
- [401Unauthorized/smartthings-skills](https://github.com/401Unauthorized/smartthings-skills) - 面向 SmartThings 生态的 agent skill，涵盖公开 API、CLI、Edge 驱动和 SmartApp。(coll · ★0 · 2026-02)
- [DanielWinks/Hubitat-Public `skills/`](https://github.com/DanielWinks/Hubitat-Public/tree/main/skills) - Hubitat 应用、驱动与库的合集，附带 Hubitat Groovy 开发、代码评审和包发布的 skill。(coll · ★2 · 2026-09)
- [jbaruch/hubitat-dev](https://github.com/jbaruch/hubitat-dev) - Hubitat Elevation 的 Tessl 上下文插件，附带部署与调试应用和驱动、通过 HTTP 发送并确认设备命令的 skill。(coll · ★0 · 2026-09)
- [timvdhoorn/homey-cli-skill](https://github.com/timvdhoorn/homey-cli-skill) - 通过官方 homey CLI 操作 Homey Pro 的 agent skill，完整支持高级 Flow JSON。(★2 · 2026-09)
- [KrauseFx/homey-cli](https://github.com/KrauseFx/homey-cli) - 附带 skill 的 CLI，让 agent 安全地控制 Athom Homey 设备和 Flow。(★1 · 2026-03)
- [markusleben/ha-nova](https://github.com/markusleben/ha-nova) - 通过轻量中继加 31 个 LLM skill 控制 Home Assistant，适用于 Claude Code、Codex 和 OpenCode，涵盖管理、Assist、备份等。(coll · ★21 · 2026-09)
- [nolte/claude-home-assistant](https://github.com/nolte/claude-home-assistant) - 用于 Home Assistant 开发的 Claude Code skill 与 agent：自定义集成、Lovelace 卡片、蓝图与自动化以及 ESPHome。(coll · ★1 · 2026-09)
- [beclab/hass-cli `skills/`](https://github.com/beclab/hass-cli/tree/main/skills) - Home Assistant 命令行工具，附带自动化、脚本与场景、Assist、备份等管理任务的 skill。(coll · ★1 · 2026-06)
- [ESJavadex/claude-homeassistant-plugins](https://github.com/ESJavadex/claude-homeassistant-plugins) - Home Assistant 的 Claude 插件市场，附带创建和管理 YAML 配置的 skill：自动化、脚本、模板、蓝图和 Lovelace 仪表板。(★26 · 2025-11)
- [PineappleEmperor/ha-skills](https://github.com/PineappleEmperor/ha-skills) - 用于开发 Home Assistant 自定义集成的 Claude Code 插件，含集成开发、面板设计和问题分诊 skill，并附带 skill 评测结果。(coll · ★0 · 2026-09)
- [mobilewhatelse/home-assistant-skill](https://github.com/mobilewhatelse/home-assistant-skill) - 用于 Home Assistant 自动化开发的 Claude Code skill，包含光伏控制、仪表板和 YAML 模式。(★1 · 2026-09)
- [sam2kb/openclaw-home-assistant](https://github.com/sam2kb/openclaw-home-assistant) - 安全优先的 OpenClaw skill，通过 REST 与 WebSocket API 运维、诊断和修复 Home Assistant 实例：日志、历史、注册表、自动化 trace 和服务调用。(★0 · 2026-08)
- [sofiaferro/rpi-voice-satellite-skill](https://github.com/sofiaferro/rpi-voice-satellite-skill) - 在 Raspberry Pi Zero 2 W 上搭配 ReSpeaker 2-Mic HAT、Wyoming 和 Home Assistant 搭建语音卫星的 skill。(★0 · 2026-04)
- [yaniv-golan/smalltv-ultra-skill](https://github.com/yaniv-golan/smalltv-ultra-skill) - GeekMagic SmallTV Ultra 桌面小屏的 Claude skill：控制主题、亮度和图片，并刷入 ESPHome 等替代固件。(coll · ★10 · 2026-03)
- [omarshahine/lutron-cli](https://github.com/omarshahine/lutron-cli) - 在终端控制 Lutron Caseta 照明，附带用于场景、Smart Away 和设备的 OpenClaw 与 Claude Code skill。(★0 · 2026-08)
- [McCavity/iobroker-plugin](https://github.com/McCavity/iobroker-plugin) - 与后端无关的 ioBroker skill 包，适用于 Claude Code 和 Codex：诊断设备、按模式查找状态和检查电池。(coll · ★0 · 2026-06)
- [alackmann/openhab-config-manager-skill](https://github.com/alackmann/openhab-config-manager-skill) - 管理私有仓库中 openHAB 配置的 OpenClaw skill：编辑 item、rule 和 thing，通过 SSH 部署到远程服务器并查询实时状态。(★3 · 2026-04)
- [deworn/claude-market `plugins/loxone-config/`](https://github.com/deworn/claude-market/tree/main/plugins/loxone-config) - Loxone 的 Claude 插件：解析模块与连线图以读取并安全编辑 Miniserver 的 .Loxone 配置文件，另含 Loxone 文档 skill。(coll · ★0 · 2026-07)

## MCP server 与桥接

Agent 在运行时调用的工具服务器。目前对这个领域最好的综述是 Veecle 在 2026 年 8 月发布的两篇评测（链接见"论文与文章"）；beriberikix/awesome-mcp-hardware（见"相关列表"）是本节最初的上游来源。

### MCU / 嵌入式（MCP）

- [78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) - 基于 MCP 的 ESP32 语音 AI 聊天机器人固件：设备把自身的工具暴露给大模型。配套 [xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server)（★10.6k）。(★30k · 2026-09)
- [horw/esp-mcp](https://github.com/horw/esp-mcp) - ESP-IDF 构建、烧录与自动修复构建错误。(★157 · 2025-12)
- [golioth/tinymcp](https://github.com/golioth/tinymcp) - 让大模型通过经 Golioth 云端 RPC 代理的 MCP 控制受限嵌入式设备。实验性质。(official · ★157 · stale since 2025-07)
- [jl-codes/platformio-mcp](https://github.com/jl-codes/platformio-mcp) - 在 PlatformIO 支持的 1000+ 块板子上构建、上传与监视。(★50 · 2026-09)
- [shieldyguy/stm32-mcp](https://github.com/shieldyguy/stm32-mcp) - 通过 SWD 与串口构建、烧录并与 STM32 通信。(★25 · 2026-08)
- [espressif/esp-rainmaker-mcp](https://github.com/espressif/esp-rainmaker-mcp) - 通过 RainMaker CLI 控制 ESP RainMaker 设备。(official · ★18 · stale since 2025-07)
- [hardware-mcp/arduino-mcp-server](https://github.com/hardware-mcp/arduino-mcp-server) - 封装 arduino-cli：编译、上传、串口会话。(★18 · 2026-08)
- [Oliver0804/arduino-cli-mcp](https://github.com/Oliver0804/arduino-cli-mcp) - 面向 VS Code / Claude 的 Arduino CLI：编译、上传、库管理。(★13 · 2026-05)
- [Volt23/mcp-arduino-server](https://github.com/Volt23/mcp-arduino-server) - Arduino CLI 桥：草图、板型、库与文件管理。(★10 · 2026-01)
- [SWITCHSCIENCE/mcp-micropython-bridge](https://github.com/SWITCHSCIENCE/mcp-micropython-bridge) - 通过 USB 串口桥接到 ESP32 / RP2040 上的 MicroPython REPL。日文文档。(★9 · 2026-04)
- [neusse/Codex-Circuitpython-MCP](https://github.com/neusse/Codex-Circuitpython-MCP) - CircuitPython 板卡发现、文件部署、串口读取、中断与复位。(★7 · 2026-05)
- [ctrlpi/pico-bay](https://github.com/ctrlpi/pico-bay) - 通过 USB 管理运行 MicroPython 或 CircuitPython 的树莓派 Pico 与 ESP32 板。(★5 · 2026-09)
- [Wokwi MCP 模式](https://docs.wokwi.com/wokwi-ci/mcp-support) - `wokwi-cli mcp` 把托管的 Wokwi 仿真暴露给 Agent：无需板子即可运行 Arduino / ESP32 / RP2040 固件并读取串口。(official)
- [jinw06k/esp-idf-monitor-mcp](https://github.com/jinw06k/esp-idf-monitor-mcp) - ESP-IDF idf.py mcp-server 的替换扩展，新增基于 PTY 的 monitor 工具，用于读取启动日志与交互式串口收发。(★13 · 2026-03)
- [cmd0s/esp32-ai-loop-mcp-server](https://github.com/cmd0s/esp32-ai-loop-mcp-server) - MCP server，11 个工具在真实 ESP32 板上打通 ESP-IDF 构建、烧录与串口观测闭环。(★8 · 2026-04)
- [cunjun/McuBuddy](https://github.com/cunjun/McuBuddy) - MCU 调试 MCP server，暴露调试探针、Keil MDK 工程、ELF/DWARF 符号、SVD 寄存器、UART/RTT 日志、FreeRTOS 状态与 Flash 操作。(★6 · 2026-08)
- [powerdragonfire/platformio.mcp](https://github.com/powerdragonfire/platformio.mcp) - PlatformIO MCP server（uvx platformio.mcp），用于构建、烧录、查看串口、运行测试、解码崩溃与压缩固件体积。(★3 · 2026-09)
- [Umer-Mahmood/embedded-mcp](https://github.com/Umer-Mahmood/embedded-mcp) - 面向 TI CC26xx（XDS110/dslite）与 Nordic nRF52/nRF91（nrfjprog）的 MCP server，可检测、擦除、烧录、复位并采集 UART 或 RTT 日志。(★3 · 2026-08)
- [Helistana/mcp-e2studio-server](https://github.com/Helistana/mcp-e2studio-server) - 面向 Renesas e2studio RA/RX 工程的 MCP server，覆盖编译、烧录、调试与故障诊断，返回结构化 JSON。(★0 · 2026-08)
- [ByteAsk/ByteAsk-Embedded-MCP](https://github.com/ByteAsk/ByteAsk-Embedded-MCP) - ByteAsk Embedded Docs 背后的开源 MCP server，从嵌入式参考文档返回带页码引用的原文片段（寄存器、Modbus 功能码、SCPI 命令）；检索引擎与文档语料仅在托管端点提供，不在仓库中。(★24 · 2026-06)
- [Aarav-J/zephyr-mcp-server](https://github.com/Aarav-J/zephyr-mcp-server) - MCP server（npx @aarav-j/zephyr-mcp-server），提供准确的 Zephyr RTOS Kconfig 符号、Devicetree 绑定与 API 签名。(★3 · 2026-07)
- [jaklys/Lvgl-mcp-esp32](https://github.com/jaklys/Lvgl-mcp-esp32) - MCP server，在无头模拟器中编译面向 ESP32 的 LVGL UI 片段并返回 PNG 截图作为视觉反馈。(★12 · 2026-07)

### 端侧 MCP server

直接运行在单片机或 SBC 上的 MCP server——设备本身就是工具提供方。

- [espressif/esp-iot-solution `mcp-c-sdk`](https://github.com/espressif/esp-iot-solution/tree/master/components/mcp-c-sdk) - 面向 ESP-IDF 5.4+ 的 C 实现：Streamable HTTP、SSE 与自定义传输；支持工具、资源、提示、补全与异步任务。ESP 组件注册表下载约 2.4 万次；esp-claw 就构建于其上。(official · ★2.7k · 2026-09)
- [Zephyr MCP server 库](https://docs.zephyrproject.org/latest/services/connectivity/networking/api/mcp.html) - 上游的 `subsys/net/lib/mcp`，由 NXP 贡献、2026-06 合入：首个在主线内置 MCP server 的 RTOS（HTTP，SSE 回退，仅工具，实验性）。(official)
- [emqx/esp-mcp-over-mqtt](https://github.com/emqx/esp-mcp-over-mqtt) - 按 MCP-over-MQTT 规范在 MQTT 5.0 上提供 MCP 的 ESP-IDF 组件。(official · ★8 · 2025-12)
- [servoagents/mcp-c](https://github.com/servoagents/mcp-c) - 与传输无关的 C99 内核，附 POSIX、Zephyr 与 ESP32 示例；支持 HTTP、stdio、MQTT 5 与实验性 CoAP。(★2 · 2026-09)
- [solnera/esp32-mcpserver](https://github.com/solnera/esp32-mcpserver) - 基于 AsyncTCP 的 Arduino / ESP32 HTTP JSON-RPC，带 mDNS 与工作任务式工具调用；PlatformIO 包名 `ESP32-MCPServer`，姊妹项目增加了 BLE 传输。(★11 · 2026-08)
- [AaronWander/EmbedMCP](https://github.com/AaronWander/EmbedMCP) - 在 STM32、ESP32、nRF 或树莓派上运行 MCP server 的 C 库。(★32 · 2026-02)
- [navado/ESP32MCPServer](https://github.com/navado/ESP32MCPServer) - 暴露 NMEA2000 / NMEA0183 / OBD-II 传感器的 ESP32 WebSocket MCP server。(★60 · 2026-03)
- [rzeldent/esp32-cam-ai](https://github.com/rzeldent/esp32-cam-ai) - 内置在 ESP32-CAM 固件中的 MCP server。(★28 · 2026-08)
- [ThanabordeeN/MCP-U_Arduino](https://github.com/ThanabordeeN/MCP-U_Arduino) - Arduino 库管理器中的 `MCP-U`：在 AVR / ESP / RP2040 的任意 `Stream` 上跑 JSON-RPC，暴露 GPIO、PWM、ADC 与 I2C，并由一个 npm 客户端转换为标准 MCP。(★0 · 2026-05)
- [PedroFnseca/esp32-mcp](https://github.com/PedroFnseca/esp32-mcp) - Arduino 库管理器中的 `ESP32-MCP`：无状态 MCP 2026-07-28，带主机端单元测试与 CI。(★1 · 2026-08)
- [matta-pie/micro-mcp](https://github.com/matta-pie/micro-mcp) - 已在 Pico W / Pico 2 W 上验证的 MicroPython MCP server；支持 HTTP 与 USB 上的 stdio 传输。(★1 · 2026-02)
- [solnera/esp32-ble-mcp-server](https://github.com/solnera/esp32-ble-mcp-server) - 唯一真正可用的 MCP-over-BLE GATT 传输：ESP32 服务端，外加 FastMCP / TS / Swift 的 BLE 客户端传输。(★1 · 2026-02)
- [Kongnitive/Kongnitive-ESP32-Harness](https://github.com/Kongnitive/Kongnitive-ESP32-Harness) - Kongnitive EdgeMCP：运行在 ESP32 上的 MCP server，内置 Lua 5.4 运行时，Agent 无需重新烧录即可推送脚本并读取日志。(★10 · 2026-05)
- [Ai-Thinker-Open/emMCP](https://github.com/Ai-Thinker-Open/emMCP) - 极小的 MCU C 库（RAM 62 字节），实现 Ai-Thinker UART-MCP 协议，让单片机向 AI 语音模组注册 MCP 工具。(official · ★5 · 2026-07)
- [jurgen178/esp32-mcp](https://github.com/jurgen178/esp32-mcp) - 运行在 Arduino Nano ESP32 上的 JSON-RPC 2.0 MCP server，自带小型嵌入式 C++ MCP SDK，把硬件控制暴露为工具。(★7 · 2025-12)
- [ertgtct/mcpesp](https://github.com/ertgtct/mcpesp) - 在 ESP32 上通过内置 WebServer 运行 MCP server 的 Arduino 库，支持工具注册与 schema 校验。(★4 · 2025-11)

### 串口 / 总线 / 调试（MCP）

- [Adancurusul/embedded-debugger-mcp](https://github.com/Adancurusul/embedded-debugger-mcp) - 基于 probe-rs / OpenOCD 的 24 工具调试器，支持 Cortex-M、RISC-V 与 Xtensa，内置 Claude / Codex Skill。Veecle 评测的首选。(★191 · 2026-07)
- [Adancurusul/serial-mcp-server](https://github.com/Adancurusul/serial-mcp-server) - Rust 串口 / UART MCP 与 CLI，带 JSON 宏自动化与 Agent Skill。(★91 · 2026-07)
- [Ipiano/gdb-mcp](https://github.com/Ipiano/gdb-mcp) - 直接驱动 GDB/MI，适用于嵌入式与本机目标。(★48 · 2026-03)
- [YaoIsAI/SerialRUN](https://github.com/YaoIsAI/SerialRUN) - 面向 Modbus / PLC / CAN / I2C / SPI 的 Rust 串口调试器，带 15 工具的 MCP server。(★38 · 2026-06)
- [es617/dbgprobe-mcp-server](https://github.com/es617/dbgprobe-mcp-server) - 通过 J-Link、CMSIS-DAP 与 ST-Link 做带符号（ELF / SVD）感知的片上调试。(★10 · 2026-03)
- [Leonezz/openbaud](https://github.com/Leonezz/openbaud) - 把串口设备变成带类型、可审计的 MCP 工具：解码、抓取、回放。(★6 · 2026-09)
- [magnusmalm/smolmux](https://github.com/magnusmalm/smolmux) - C11 编写的串口与 GDB-SWD 复用器，带 MCP server，让一个探针同时服务多个使用方。(★2 · 2026-08)
- [Pan-Robotics/bus-mcp](https://github.com/Pan-Robotics/bus-mcp) - 把树莓派上的 CAN / CAN-FD、RS-485 / UART、I2C、SPI 与 GPIO 暴露为 MCP 工具，默认只读。(★2 · 2026-06)
- [mcp2everything/mcp2mqtt](https://github.com/mcp2everything/mcp2mqtt) - 用于硬件控制的 MCP → MQTT 桥；被引用最多的早期作品，但已无人维护。姊妹项目 `mcp2serial` 与 `mcp2tcp` 同样停更。(★371 · stale since 2024-12)
- [signal-slot/mcp-gdb](https://github.com/signal-slot/mcp-gdb) - GDB MCP server（npx mcp-gdb），支持会话、断点、单步、内存、寄存器与 core dump。(★159 · 2026-07)
- [Klievan/jlink-mcp](https://github.com/Klievan/jlink-mcp) - 面向 SEGGER J-Link、OpenOCD、Black Magic 探针的 MCP server，可烧录、暂停、读取故障寄存器并诊断崩溃，已在 nRF52840-DK 上演示。(★30 · 2026-09)
- [cyj0920/jlink_mcp](https://github.com/cyj0920/jlink_mcp) - J-Link MCP server，支持 SWD/JTAG 连接、内存读写、Flash 编程、断点与 RTT。(★34 · 2026-04)
- [es617/serial-mcp-server](https://github.com/es617/serial-mcp-server) - 有状态的 pyserial MCP server，可列出端口、打开连接、切换 DTR/RTS，并支持协议规范与设备插件。(★20 · 2026-03)
- [KenosInc/sigrok-mcp-server](https://github.com/KenosInc/sigrok-mcp-server) - sigrok-cli 的 MCP server，扫描逻辑分析仪、采集数据并用 sigrok 解码器解码协议。(★11 · 2026-08)
- [luiox/openocd-mcp](https://github.com/luiox/openocd-mcp) - OpenOCD MCP server，复用 VS Code launch.json 完成烧录、异步 GDB/MI 调试与 SEGGER RTT 日志读取。(★10 · 2026-06)
- [konbakuyomu/pyocd-debug-mcp](https://github.com/konbakuyomu/pyocd-debug-mcp) - 基于 pyOCD 的 MCP server，为 CMSIS-DAP 探针提供 58 个工具：烧录校验、硬件断点、观察点、寄存器与 HardFault 分析。(★1 · 2026-04)
- [wegitor/logic-analyzer-ai-mcp](https://github.com/wegitor/logic-analyzer-ai-mcp) - 实验性（alpha）Saleae 逻辑分析仪 MCP server，可配置并执行采集、解析采集文件并导出数据，目前仅在旧版 Logic 1.2.40 软件上测试。(★10 · 2026-07)
- [qarnet/serial-mcp](https://github.com/qarnet/serial-mcp) - Rust 编写的串口 MCP server，持续接收捕获，支持 SLIP/COBS 分帧、AT/NMEA/Modbus ASCII 解析、DTR/RTS 与 BREAK 控制。(★9 · 2026-09)
- [okhsunrog/flashprobe-mcp](https://github.com/okhsunrog/flashprobe-mcp) - MCP server，通过 probe-rs（JTAG/SWD，含 RTT 或 semihosting）或 espflash 烧录并监控固件，支持 defmt 解码与提前退出的日志捕获。(★5 · 2026-09)
- [Rance-OwO/Serial-Agent](https://github.com/Rance-OwO/Serial-Agent) - Serial Agent：VS Code 插件加 MCP server 与 skill，让 Agent 访问串口、日志与固件工具进行嵌入式调试。(★40 · 2026-08)
- [woooooooooolf/ser2mcp](https://github.com/woooooooooolf/ser2mcp) - Rust 编写的 UART MCP server，14 个 uart_* 工具支持多串口读写、输出匹配、hex/文本模式与文件流式发送。(★7 · 2026-09)
- [felixfinal/agent-dsviewer-logic-analyzer](https://github.com/felixfinal/agent-dsviewer-logic-analyzer) - MCP server、原生 dslogic-cli 后端与 Agent skills，用于 DreamSourceLab DSLogic USB 逻辑分析仪的采集与解码。(★4 · 2026-06)
- [BeaCox/gdb-mcp](https://github.com/BeaCox/gdb-mcp) - 多会话 GDB/MI MCP server，支持本地程序、core 文件与 gdbserver 目标，返回精简的帧与回溯信息。(★9 · 2026-09)
- [paulopalaoro/cortex-mcp-bridge](https://github.com/paulopalaoro/cortex-mcp-bridge) - VS Code 插件，经 MCP 暴露 Cortex-Debug 与 PlatformIO 的实时调试状态，并可通过 OpenOCD 在无固件情况下驱动 STM32 外设。(★5 · 2026-04)
- [harrisonfaulkner/canbus-mcp](https://github.com/harrisonfaulkner/canbus-mcp) - 面向 PEAK PCAN-USB 的 CAN 总线逆向 MCP server，读取、分析并映射 ECU 报文，支持 DBC 导入导出。(★2 · 2026-05)

### 机器人（MCP）

- [robotmcp/ros-mcp-server](https://github.com/robotmcp/ros-mcp-server) - 通过 rosbridge 把 Claude / GPT 接到 ROS 与 ROS 2 机器人；客户端对应项目 [robotmcp_client](https://github.com/robotmcp/robotmcp_client)。(★1.5k · 2026-09)
- [Rerun viewer-mcp](https://rerun.io/docs/reference/viewer/mcp) - 官方 `rerun viewer-mcp` 子命令，通过 gRPC 驱动正在运行或无头的 Rerun Viewer。(official)
- [Foxglove Desktop MCP server](https://docs.foxglove.dev/docs/agents/mcp-server) - 内置于 Foxglove Desktop：查看数据、搭建布局、编写用户脚本、回放、文档检索；本地端点，需要 Pro / Enterprise / Academic 席位。(official)
- [Roboflow MCP](https://blog.roboflow.com/mcp-server/) - 托管的 `mcp.roboflow.com`：训练、Workflows、托管推理与边缘设备部署；[computer-vision-skills](https://github.com/roboflow/computer-vision-skills) 以 Claude / Codex 插件形式提供十个 Skill。(official)
- [Extelligence-ai/bagel](https://github.com/Extelligence-ai/bagel) - 用自然语言查询机器人、无人机与 IoT 遥测数据（ROS bag、MCAP、PX4 日志），带边缘侧数据精简流水线。(★397 · 2026-09)
- [rokbenko/quackd](https://github.com/rokbenko/quackd) - 一个 CLI / MCP 驱动七种机器人本体（Microduck、Open Duck、SO-101、XLeRobot、AlohaMini、ToddlerBot、rosbridge），每种本体有自己的 Skill 契约；目前只有仿真与 mock。(★208 · 2026-09)
- [omni-mcp/isaac-sim-mcp](https://github.com/omni-mcp/isaac-sim-mcp) - 用自然语言控制 NVIDIA Isaac Sim 的场景与机器人。(★191 · stale since 2025-04)
- [wise-vision/ros2_mcp](https://github.com/wise-vision/ros2_mcp) - 支持图像流与自动 QoS 匹配的 ROS 2 MCP。(★88 · 2026-08)
- [lpigeon/unitree-go2-mcp-server](https://github.com/lpigeon/unitree-go2-mcp-server) - 通过 ROS 2 控制宇树 Go2 机器狗。(★87 · 2026-06)
- [kakimochi/ros2-mcp-server](https://github.com/kakimochi/ros2-mcp-server) - 基于 topic 的 ROS 2 控制。(★83 · stale since 2025-06)
- [IliaLarchenko/robot_MCP](https://github.com/IliaLarchenko/robot_MCP) - LeRobot 生态中的 SO-ARM100 / 101 与 LeKiwi 机械臂控制。(★85 · stale since 2025-08)
- [Yutarop/ros-mcp](https://github.com/Yutarop/ros-mcp) - 把 ROS topic、service 与 action 暴露为 MCP 工具。(★36 · stale since 2025-08)
- [agentculture/reachy-mini-mcp](https://github.com/agentculture/reachy-mini-mcp) - 单工具的 Reachy Mini MCP，带序列模式，可对接真机或仿真；配套 CLI 提供 `find-reachy` Skill。(★32 · 2026-07)
- [jackccrawford/reachy-mini-mcp](https://github.com/jackccrawford/reachy-mini-mcp) - Pollen Robotics Reachy Mini 控制。(★29 · 2026-07)
- [binabik-ai/mcp-rosbags](https://github.com/binabik-ai/mcp-rosbags) - 离线 rosbag 分析。(★28 · 2025-09)
- [phospho-app/phospho-mcp-server](https://github.com/phospho-app/phospho-mcp-server) - 面向 SO-100 / 101 机械臂的 VLA 桥接。(★10 · stale since 2025-09)
- [neka-nat/mycobot-mcp](https://github.com/neka-nat/mycobot-mcp) - 大象机器人 myCobot；该厂商唯一的 MCP。(★8 · stale since 2025-05)
- [nonead/Nonead-Universal-Robots-MCP](https://github.com/nonead/Nonead-Universal-Robots-MCP) - Universal Robots 协作机器人 MCP 中间件（中 / 英 / 日文档）。(★8 · 2026-09)
- [monteslu/robot-mcp](https://github.com/monteslu/robot-mcp) - Johnny-Five MCP：Arduino 与树莓派上的舵机与硬件。(★7 · 2026-02)
- [eliasbitsch/abb-robotstudio-mcp](https://github.com/eliasbitsch/abb-robotstudio-mcp) - ABB RobotStudio SDK 插件，外加在真实控制器上使用 Robot Web Services。(★6 · 2026-05)
- [RoversX/universal-robot-mcp](https://github.com/RoversX/universal-robot-mcp) - Universal Robots 协作机器人控制。(★5 · stale since 2025-09)
- [ros-claw/unitree-sdk2-mcp](https://github.com/ros-claw/unitree-sdk2-mcp) - 不依赖 ROS，直接通过 DDS 控制宇树 G1 / Go2 / H1 / B2 / A2 / R1；ros-claw 组织下还有约 35 个同类 MCP（RealSense、Vicon、Nav2、MoveIt 2、UR、LIMO、因时灵巧手）。(★4 · 2026-04)
- [gtoff/moveit-mcp-server](https://github.com/gtoff/moveit-mcp-server) - 把 MoveIt 2 规划暴露为 MCP 工具。(★5 · 2026-03)
- [ros-claw/inspire-rh56-mcp](https://github.com/ros-claw/inspire-rh56-mcp) - 通过 CAN 控制因时 RH56 灵巧手，已在实物上复验。(★1 · 2026-07)
- [erh/viam-mcp-server](https://github.com/erh/viam-mcp-server) - 以 Viam 模块形式提供的 MCP：根据每个组件的 Go 接口逐方法生成工具，作者是 Viam 的 CEO。(★0 · 2026-04)
- [ajtudela/nav2_mcp_server](https://github.com/ajtudela/nav2_mcp_server) - 面向 ROS 2 Nav2 机器人的 MCP server：导航到位姿、跟随航点、清除代价地图并管理生命周期。(★84 · 2026-05)
- [proxi666/amazing-ros2-mcp](https://github.com/proxi666/amazing-ros2-mcp) - 原生 rclpy 的 ROS 2 MCP server，覆盖话题、服务、动作、参数、图像与 Nav2，并有速度限幅和话题黑名单。(★14 · 2026-05)
- [LCAS/ros2_mcp](https://github.com/LCAS/ros2_mcp) - LCAS 的 ROS 2 MCP server，支持话题回显、为 VLM 获取图像与接口内省。(★9 · 2025-12)
- [selfpatch/ros2_medkit_mcp](https://github.com/selfpatch/ros2_medkit_mcp) - ros2_medkit SOVD 网关的 MCP 适配器，暴露 ROS 2 诊断、操作、参数与生命周期状态。(official · ★6 · 2026-09)
- [zhou-zhichao/robotstudio-mcp](https://github.com/zhou-zhichao/robotstudio-mcp) - ABB RobotStudio 桥接（C# 插件，含 CLI、skills 与 MCP），检查工作站、上传 RAPID 代码并运行仿真。(★97 · 2026-09)
- [PixelML/reachy-mini-mcp](https://github.com/PixelML/reachy-mini-mcp) - Reachy Mini 机器人的 MCP server，支持舞蹈、情绪、头部运动、相机拍照、人脸追踪与本地 TTS。(★21 · 2026-01)
- [danmartinez78/VectorClaw](https://github.com/danmartinez78/VectorClaw) - MCP server，经 Wire-Pod 通过本地 gRPC 暴露 Anki Vector 机器人能力。(★19 · 2026-06)
- [Jizai-inc/palmimo-devkit](https://github.com/Jizai-inc/palmimo-devkit) - Palmimo 六足桌面机器人（18 个腿部舵机、舵机颈部、脸部屏幕）的 Python SDK、MCP server 与 Agent 示例。(official · ★9 · 2026-09)

### 无人机（MCP）

- [ion-g-ion/MAVLinkMCP](https://github.com/ion-g-ion/MAVLinkMCP) - 通过 MAVLink 控制 PX4 / ArduPilot 无人机。(★23 · 2026-08)
- [ysznai/dji-waypoint-mcp](https://github.com/ysznai/dji-waypoint-mcp) - 大疆航线规划；除 Tello 外唯一的大疆 MCP。(★7 · stale since 2025-07)
- [0xKoda/drone-mcp](https://github.com/0xKoda/drone-mcp) - 大疆 Tello 无人机控制。(★25 · stale since 2025-04)
- [showkeyjar/robot-mcp-server](https://github.com/showkeyjar/robot-mcp-server) - 宇树与大疆无人机的运动控制。(★12 · 2026-03)
- [hfujikawa77/ardupilot-mcp-server](https://github.com/hfujikawa77/ardupilot-mcp-server) - 通过 MAVLink TCP 控制 ArduPilot。日文。(★9 · 2026-05)
- [rmeadomavic/ardupilot-mcp](https://github.com/rmeadomavic/ardupilot-mcp) - SITL 优先、带安全门禁的 ArduPilot MAVLink MCP。(★2 · 2026-08)
- [starlordz12/inav-mcp](https://github.com/starlordz12/inav-mcp) - 通过 USB 配置、诊断与调校 iNAV 固定翼飞控。(★2 · 2026-08)
- [bvandevliet/betaflight-mcp](https://github.com/bvandevliet/betaflight-mcp) - 实时的 Betaflight CLI 配置与 PID 助手，内置调参 Skill。(★1 · 2026-08)
- [deepak61296/mavlink-mcp](https://github.com/deepak61296/mavlink-mcp) - MAVLink MCP server，可驾驶 ArduPilot 飞行器并获取相机画面，已在 ArduPilot SITL 中测试（尚未在实机上飞行），飞行工具默认关闭。(★4 · 2026-09)
- [robotto-xyz/ai-drone-toolkit](https://github.com/robotto-xyz/ai-drone-toolkit) - uv monorepo，含用于 PX4 ULog 飞行日志分析和仅限仿真的 PX4 SITL 指令（带安全检查）的 MCP server。(coll · ★3 · 2026-06)
- [Project-GrADyS/uav_mcp](https://github.com/Project-GrADyS/uav_mcp) - 基于 uav-api 的 MCP 到 HTTP 适配层，用于 ArduPilot 四旋翼或 SITL 的解锁、GPS/NED 移动与遥测。(★3 · 2026-05)
- [furkanisikay/ardupilot-mcp](https://github.com/furkanisikay/ardupilot-mcp) - MCP server，诊断 ArduPilot .bin 飞行日志（振动、参数、校准、功率裕度）并附 ArduPilot 文档链接。(★4 · 2026-07)
- [alireza787b/dronesphere](https://github.com/alireza787b/dronesphere) - DroneSphere：带 MCP 接口的 PX4 无人机群控制，支持 GPS 与 NED 坐标系下的自然语言导航与遥测。(★14 · 2025-09)

### 仿真器（MCP）

- [kvgork/gazebo-mcp](https://github.com/kvgork/gazebo-mcp) - Gazebo：生成 TurtleBot3、多机器人编队、世界生成、传感器数据。(★17 · 2026-07)
- [robotlearning123/mujoco-mcp](https://github.com/robotlearning123/mujoco-mcp) - 65 个 MuJoCo 工具：轨迹优化、接触分析、视频导出、查看器。(★9 · 2026-06)
- [Rongxuan-Zhou/mujoco-mcp-server](https://github.com/Rongxuan-Zhou/mujoco-mcp-server) - 在 Claude Code 中对 MuJoCo 做仿真、渲染、分析与构建强化学习环境。(★8 · 2026-03)
- [nullbyte91/nvidia-isaac-mcp](https://github.com/nullbyte91/nvidia-isaac-mcp) - Isaac Sim 扩展加外部 MCP，带 Isaac Lab 钩子。(★8 · 2026-02)
- [game4automation/io.realvirtual.mcp](https://github.com/game4automation/io.realvirtual.mcp) - Unity 数字孪生 MCP：驱动、传感器、PLC 信号、机器人逆解。(official · ★15 · 2026-07)
- [mergeos-bounties/gazebo-mcp](https://github.com/mergeos-bounties/gazebo-mcp) - Gazebo（gz-sim）的世界、模型、位姿与单步推进，带完整的离线 mock 以便 CI 使用。(★4 · 2026-07)
- [SchiopuAndreiViorel/coppelia-mcp](https://github.com/SchiopuAndreiViorel/coppelia-mcp) - Claude ↔ CoppeliaSim。(★4 · 2026-03)
- [lyuai/genesis-mcp](https://github.com/lyuai/genesis-mcp) - 带可视化的 Genesis World 仿真器 MCP。(★5 · stale since 2025-03)
- [punithkrishnakeepudi/webots-mcp-server](https://github.com/punithkrishnakeepudi/webots-mcp-server) - Webots 启动、监视、强化学习训练与场景操作；找到的唯一 Webots MCP。(★0 · 2026-04)
- [omnilink-tech/omnisim](https://github.com/omnilink-tech/omnisim) - OmniSim：面向编码 Agent 的 Newton 物理机器人仿真器，提供 HTTP/JSON 控制、官方 MCP server 与 ROS 2 sidecar。(★181 · 2026-09)
- [sherndon79/agent-world](https://github.com/sherndon79/agent-world) - Isaac Sim 扩展集，提供 HTTP API 与 MCP 工具，用于搭建场景、相机控制、导航与录制。(coll · ★4 · 2025-10)
- [SofianeAlla/carla-mcp](https://github.com/SofianeAlla/carla-mcp) - CARLA MCP server，55 个工具支持启动仿真器、世界控制、完整传感器配置、激光雷达点云分析与 KITTI 格式数据集导出。(★2 · 2026-05)
- [Croquembouche/CARLA_MCP](https://github.com/Croquembouche/CARLA_MCP) - 定制 CARLA UE5 仿真器的 WebUI 与 MCP server（49 个工具），支持场景控制、泊车、传感器、录制与 ROS 2 bag。(★2 · 2026-09)

### 工业 IoT（MCP）

- [anviod/edgeCore](https://github.com/anviod/edgeCore) - 部署在工业现场的边缘运行时，支持 Modbus、BACnet、OPC UA、S7 与 EtherNet/IP。(★126 · 2026-09)
- [rivie13/studio5000-AI-Assistant](https://github.com/rivie13/studio5000-AI-Assistant) - 把罗克韦尔自动化 SDK 与内部文档作为 Studio 5000 的 MCP 工具。(★35 · 2025-12)
- [Nodeblue-AI/studio5000-mcp-server](https://github.com/Nodeblue-AI/studio5000-mcp-server) - 解析罗克韦尔与 Allen-Bradley PLC 的 Studio 5000 L5X 工程导出；姊妹项目 `bridge-mcp-server` 将其与 Ignition SCADA 关联。(★20 · 2026-08)
- [ThingsPanel/thingspanel-mcp](https://github.com/ThingsPanel/thingspanel-mcp) - ThingsPanel IoT 平台的设备控制与数据分析。(★47 · 2025-11)
- [chewcw/tia-portal-openness-mcpserver](https://github.com/chewcw/tia-portal-openness-mcpserver) - 西门子博途 Openness MCP。(★37 · 2026-09)
- [kukapay/opcua-mcp](https://github.com/kukapay/opcua-mcp) - 连接 OPC UA 系统：监视、分析与控制节点。(★29 · 2025-10)
- [midhunxavier/OPCUA-MCP](https://github.com/midhunxavier/OPCUA-MCP) - OPC UA MCP server。(★25 · 2026-09)
- [kukapay/modbus-mcp](https://github.com/kukapay/modbus-mcp) - 为 Agent 规范化并语义化 Modbus 寄存器。(★25 · stale since 2025-05)
- [OPCFoundation/UA-for-AI-Prototype](https://github.com/OPCFoundation/UA-for-AI-Prototype) - OPC UA for AI 工作组：把规范切分为 RAG 片段，并托管在 reference.opcfoundation.org/mcp，计划覆盖 430+ 个配套规范。(official · ★14 · 2026-06)
- [efranceschetti/festo-codesys-mcp](https://github.com/efranceschetti/festo-codesys-mcp) - Festo / CODESYS MCP，带结构化文本编写、PLCopen XML、运动控制与故障诊断 Skill。(★1 · 2026-09)
- [lwsinclair/IoT-Edge-MCP-Server](https://github.com/lwsinclair/IoT-Edge-MCP-Server) - 统一 MQTT、Modbus 与 InfluxDB，用于 SCADA / PLC 场景。(★4 · 2025-11)
- [daedalus/mcp-snap7](https://github.com/daedalus/mcp-snap7) - 通过 python-snap7 访问西门子 S7 PLC。(★0 · 2026-04)
- [ezhuk/modbus-mcp](https://github.com/ezhuk/modbus-mcp) - Python 编写的 Modbus MCP server（`uv add modbus-mcp`），通过 Streamable HTTP 端点让智能体读取楼宇自动化与工业控制系统中 Modbus 设备的寄存器并执行控制。(★4 · 2026-09)
- [ezhuk/mqtt-mcp](https://github.com/ezhuk/mqtt-mcp) - Python 编写的 MQTT MCP server（`uv add mqtt-mcp`），让智能体订阅传感器主题并向工业、楼宇与智能家居系统中的 MQTT 设备发布控制指令。(★22 · 2026-09)
- [shriramkv/opcua-mcp](https://github.com/shriramkv/opcua-mcp) - OPC UA MCP server，把 PLC、SCADA 网关和历史库中白名单内的点位发布为智能体工具，默认只读，写入设定值需显式放行。(★20 · 2026-07)
- [mwieczorkiewicz/opcua-mcp](https://github.com/mwieczorkiewicz/opcua-mcp) - Go 编写的 OPC UA MCP server，可通过 stdio 或 HTTP 浏览、搜索、读写并订阅 PLC 与机器人实时数据，内置地址空间索引，并提供对接测试 OPC UA 服务器的 Docker Compose 演示。(★5 · 2026-08)
- [luke-harriman/Codesys-MCP](https://github.com/luke-harriman/Codesys-MCP) - MCP server，把 CODESYS V3.5 IDE 脚本 API 暴露为 41 个工具和 3 个资源，并保持 CODESYS 界面常开，智能体对 PLC 工程的修改会实时显示在 IDE 中。(★80 · 2026-05)
- [KerberosClaw/kc_modbus_mcp](https://github.com/KerberosClaw/kc_modbus_mcp) - Modbus TCP MCP server，通过 YAML 设备配置让智能体按名称读写 PLC 寄存器并自动做数据类型转换，内置模拟器可在无硬件时测试。(★2 · 2026-03)
- [alejoseb/ModbusMCP](https://github.com/alejoseb/ModbusMCP) - 提供 Modbus RTU/TCP 主站与模拟从站功能的 MCP server，支持串口发现，并可在多个并发连接上读写线圈、离散输入和寄存器。(★3 · 2026-02)
- [MountainClimberJiwen/plc-mcp](https://github.com/MountainClimberJiwen/plc-mcp) - PLC MCP server，把 Siemens TIA Portal（经 TIA Openness）与汇川 AM600/InoProShop 工程映射为虚拟文件系统，让智能体用 ls、cat、写入与 diff 查看和修改程序块。(★4 · 2026-07)
- [WagoAlex/wago-plc-mcp-server](https://github.com/WagoAlex/wago-plc-mcp-server) - MCP server，通过 WAGO WDA REST API 把助手连接到一组 WAGO PLC，提供 29 个工具、Bearer 认证、哈希链审计日志以及智能体无法绕过的写入闸门。(★3 · 2026-09)
- [fieldworks-build/fieldworks-adapters](https://github.com/fieldworks-build/fieldworks-adapters) - Rust 工作区形式的一组 MCP 协议适配器，以统一的九工具接口访问工业数据，MQTT、OPC UA 与 Modbus TCP 适配器可用，DNP3、EtherNet/IP 与 AVEVA PI 仍为桩实现。(coll · ★0 · 2026-08)
- [zhiningsun/industrial-mcp](https://github.com/zhiningsun/industrial-mcp) - MCP server，把 Modbus TCP 与 MQTT 工业设备变成智能体工具（列出、读取、调速、启停），OPC UA 仅为仿真，内置设备仿真引擎，并提供巡检与紧急停机提示词。(★3 · 2026-08)
- [rjboer/OMRON-MCP](https://github.com/rjboer/OMRON-MCP) - 面向 OMRON Sysmac Studio 工程的 Go MCP server 与 Windows 工作台，让智能体查看程序与变量、排查故障、生成结构化文本并应用经审核的修改。(★2 · 2026-08)
- [dad-io/kepware_mcp_server](https://github.com/dad-io/kepware_mcp_server) - 面向 Kepware KEPServerEX 的 MCP server，通过 Configuration API 管理通道、设备、标签、IoT Gateway、数据记录器和用户，支持 stdio、SSE 与 HTTPS。(★2 · 2026-03)
- [arhunn/s7-plc-mcp](https://github.com/arhunn/s7-plc-mcp) - MCP server，使用纯 Python 的 python-snap7 经 TCP 102 端口直连 Siemens S7-1200/1500 PLC，无需外部 DLL。(★0 · 2026-04)

### 汽车（MCP）

- [farzadnadiri/MCP-CAN](https://github.com/farzadnadiri/MCP-CAN) - 基于 SocketCAN / vcan 的 OBD-II（J1979）、UDS 与 J1939 诊断；可 pip 安装。(★17 · 2026-08)
- [hexsecs/canarchy](https://github.com/hexsecs/canarchy) - 流式优先的 CAN / J1939 工具箱（python-can、SocketCAN），内置 MCP server、TUI 与模糊测试。(★4 · 2026-09)
- [HadiCherkaoui/klartext](https://github.com/HadiCherkaoui/klartext) - 原生 Rust 实现、通过 ENET 线（HSFZ / UDS）做宝马 F 系列诊断，带 MCP server。(★5 · 2026-08)
- [chrisbray85/headless-ista](https://github.com/chrisbray85/headless-ista) - Agent 通过 MCP 驱动宝马 ISTA+，以文本形式读取故障与测试计划。(★4 · 2026-09)
- [petrpatek/obd2-mcp-server](https://github.com/petrpatek/obd2-mcp-server) - 通过蓝牙或 USB 连接 ELM327：故障码与实时 PID，带 `--mock` 模式。(★3 · 2026-05)
- [awtoau/awto-can](https://github.com/awtoau/awto-can) - SocketCAN MCP 守护进程：DBC 感知的收发、ISO-TP、抓取与回放、实时 DBC 校验。(★0 · 2026-04)
- [mikehaller/kuksa-mcp-server](https://github.com/mikehaller/kuksa-mcp-server) - 通过 Eclipse Kuksa Databroker 读写 COVESA VSS 信号；找到的唯一 VSS MCP。(★0 · 2026-06)
- [cyrusdavirusss/j2534-mcp-server](https://github.com/cyrusdavirusss/j2534-mcp-server) - J2534 PassThru 的 UDS / OBD-II；找到的唯一 J2534 MCP。仅 Windows。(★0 · 2026-09)
- [daedalus/mcp-canbus](https://github.com/daedalus/mcp-canbus) - 极简 CAN 总线 MCP。(★0 · 2026-03)
- [cobanov/teslamate-mcp](https://github.com/cobanov/teslamate-mcp) - MCP server，把 TeslaMate 的 PostgreSQL 数据库交给 AI 客户端，无需写 SQL 即可回答 Tesla 电池衰减、行程和充电费用等问题。(★140 · 2026-08)
- [ysrdevs/tesla-mcp](https://github.com/ysrdevs/tesla-mcp) - 面向 Tesla Fleet API 的 MCP server，提供 96 个工具，覆盖车辆控制、空调、充电、导航、媒体、哨兵与代客模式以及实时车辆数据。(★1 · 2026-04)
- [Zenotech-bv/teslafi-mcp](https://github.com/Zenotech-bv/teslafi-mcp) - 面向 TeslaFi API 的 MCP server，可查询 Tesla 实时状态、行程与充电历史和通勤规律，仅在显式开启时才发送车辆指令。(★2 · 2026-09)
- [keithah/tessie-mcp](https://github.com/keithah/tessie-mcp) - 自托管的 Tessie Streamable HTTP MCP server，可列出车辆、读取状态、分析行驶历史与轨迹并发送车辆指令，通过 Bearer token 保护。(★9 · 2026-08)
- [ayhammouda/obd-mcp-server](https://github.com/ayhammouda/obd-mcp-server) - 安全优先、只读的 OBD MCP server，从确定性模拟器或 ELM327 适配器为 AI 客户端提供结构化车辆诊断数据，支持扩展驱动与诊断配置。(★0 · 2026-09)
- [mbohaychuk/OBD-II-MCP-Server](https://github.com/mbohaychuk/OBD-II-MCP-Server) - FastMCP 服务器，经 ELM327 适配器把 MCP 主机连接到实车 OBD-II 接口，提供实时 PID、故障码、冻结帧、会话录制、OBDb Ford 信号集与 NHTSA 召回查询。(★0 · 2026-06)

### 楼宇自动化与能源（MCP）

- [knx-ai/knx-ets-mcp](https://github.com/knx-ai/knx-ets-mcp) - 通过 ETS 插件接入 ETS 5 / 6 的 MCP：检视与编辑工程、编程与扫描设备。仅 Windows。(★33 · 2026-08)
- [NickoScope/nickol-knx-mcp](https://github.com/NickoScope/nickol-knx-mcp) - 设计阶段的 KNX / ETS 校验与修复（DPT、Secure、Matter）。(★25 · 2026-09)
- [ezhuk/bacnet-mcp](https://github.com/ezhuk/bacnet-mcp) - BACnet 属性读写；`pip install bacnet-mcp`。(★6 · 2026-09)
- [chappo/rusty-bacnet-mcp](https://github.com/chappo/rusty-bacnet-mcp) - Rust 实现的 BACnet MCP：发现、传感器、设定值；默认只读，单一二进制。(★0 · 2026-08)
- [lubosstrejcek/victron-tcp](https://github.com/lubosstrejcek/victron-tcp) - 通过本地 Modbus TCP 与 MQTT 访问 Victron GX，32 个工具覆盖 900+ 个寄存器；姊妹项目 `victron-vrm-mcp` 对接云端。(★4 · 2026-09)
- [flowiesner/fronius-mcp](https://github.com/flowiesner/fronius-mcp) - Fronius Solar API：光伏、电池、并网馈电。(★1 · 2026-04)
- [mregen/shelly-em-mcp](https://github.com/mregen/shelly-em-mcp) - 本地读取 Shelly Pro 3EM / EM / Plus PM 的电能数据。(★1 · 2026-09)
- [mrksmts/homewizard-mcp-server](https://github.com/mrksmts/homewizard-mcp-server) - HomeWizard P1 智能电表本地 API，只读。(★1 · 2026-04)
- [gkoenig/anker-solix-mcp](https://github.com/gkoenig/anker-solix-mcp) - 安克 Solix Solarbank 与智能电表。(★1 · 2026-09)
- [bjeans/homelab-mcp](https://github.com/bjeans/homelab-mcp) - 家庭实验室工具包，其中的 UPS server 直接对硬件说 NUT 协议。(★42 · 2026-06)
- [javierojan/askacharge-mcp](https://github.com/javierojan/askacharge-mcp) - 运营一整个 OCPP 充电桩集群。(★0 · 2026-09)
- [cr2007/mcp-helvarnet](https://github.com/cr2007/mcp-helvarnet) - 通过 HelvarNet 控制 Helvar DALI 照明；找到的唯一 DALI MCP。(★0 · 2026-01)
- [SAP/e-mobility-charging-stations-simulator `skills/`](https://github.com/SAP/e-mobility-charging-stations-simulator) - SAP OCPP-J 充电桩模拟器的 EVSE 模拟 Skill；是模拟而非硬件。(official · ★225 · 2026-09)
- [Smarteon/lox-mcp](https://github.com/Smarteon/lox-mcp) - Java 编写的 MCP server，连接 Loxone Miniserver Gen 1/Gen 2，控制灯光、遮阳与场景并通过 WebSocket 读取实时状态，附带桌面配置工具。(★9 · 2026-07)
- [New-Forest-Technology-Services/Loxone-MCP](https://github.com/New-Forest-Technology-Services/Loxone-MCP) - 基于 Loxone Miniserver 本地 API 的 MCP server，80 多个工具，覆盖灯光、灯光情景、遮阳、温控等控制项。(★1 · 2026-07)
- [Yveshby27/brick-bacnet-mcp](https://github.com/Yveshby27/brick-bacnet-mcp) - 只读 BACnet/IP 网关，通过 MCP 向 LLM 智能体开放楼宇自动化点位库，并在导入时打上 Brick 与 Project Haystack 语义标签。(★1 · 2026-06)
- [marcinn2/goodwe-inverter-mcp](https://github.com/marcinn2/goodwe-inverter-mcp) - MCP server，在局域网内监控和控制 GoodWe 光伏逆变器，读取光伏、电池与电网数据，并可切换运行模式、设置馈网上限和电池放电深度。(★0 · 2026-09)
- [huber/fronius-mcp-server](https://github.com/huber/fronius-mcp-server) - TypeScript 编写的 MCP server，覆盖 Fronius Solar API v1，可读取逆变器实时数据、数据记录器与 LED 状态、智能电表和能量流。(★4 · 2025-11)
- [beldur/fronius-mcp](https://github.com/beldur/fronius-mcp) - 面向 Fronius 逆变器与智能电表的 MCP server 和 CLI，提供逆变器、能量流与电表实时数据，并可回答历史发电量与电池状态问题。(★0 · 2026-07)
- [xianman/enphase-mcp](https://github.com/xianman/enphase-mcp) - 面向 Enphase Developer API v4 的 MCP server，提供 30 个读取光伏发电、用电、电池与电网遥测的工具，电池和 EV 充电桩写操作需显式开启。(★1 · 2026-05)
- [holger1411/unofficial-solaredge-mcp](https://github.com/holger1411/unofficial-solaredge-mcp) - 非官方 MCP server，通过 SolarEdge Monitoring API 让助手以结构化方式访问 SolarEdge 光伏系统数据。(★0 · 2026-06)
- [karlattard237/V2C-Cloud-MCP](https://github.com/karlattard237/V2C-Cloud-MCP) - 面向 V2C Trydan EV 充电桩的 FastMCP 服务器，可监控充电会话并控制电流、功率模式、光伏联动、定时与锁定状态。(★0 · 2026-04)

### 智能家居（MCP）

- [home-assistant/core `mcp_server`](https://www.home-assistant.io/integrations/mcp_server/) - 内置的 MCP server 集成，通过 Streamable HTTP 暴露 Assist API。(official · ★90k · 2026-09)
- [homeassistant-ai/ha-mcp](https://github.com/homeassistant-ai/ha-mcp) - 87 个工具；功能最全的 Home Assistant MCP。(★4.8k · 2026-09)
- [tevonsb/homeassistant-mcp](https://github.com/tevonsb/homeassistant-mcp) - 支持 SSE 实时更新的 Home Assistant MCP。(★576 · 2026-01)
- [voska/hass-mcp](https://github.com/voska/hass-mcp) - 节省 token 的 Home Assistant 控制与查询。(★343 · 2026-08)
- [openHAB MCP 加载项](https://www.openhab.org/addons/integrations/mcp/) - openHAB 5.x 内置加载项：item、thing、规则、订阅；独立部署可选 [tdeckers/openhab-mcp](https://github.com/tdeckers/openhab-mcp)。(official)
- [Homey MCP](https://mcp.athom.com) - Athom 为 Homey 托管的远程 MCP，2025-11 上线；无公开仓库。(official)
- [aqara/aqara-mcp-server](https://github.com/aqara/aqara-mcp-server) - 绿米 Aqara 的远程 Streamable-HTTP MCP，24 个工具覆盖设备、场景、自动化、能耗与固件。(official · ★43 · 2026-09)
- [Yeelight/yeelight-iot-mcp](https://github.com/Yeelight/yeelight-iot-mcp) - 易来 Yeelight Pro 云端：家庭、房间、设备、分组、场景。(official · ★9 · 2026-07)
- [ecovacs-ai/ecovacs-mcp](https://github.com/ecovacs-ai/ecovacs-mcp) - 科沃斯地宝扫地机：清扫、回充、状态；需要开放平台密钥。(official · ★23 · stale since 2025-04)
- [tuya/tuya-mcp-sdk](https://github.com/tuya/tuya-mcp-sdk) - 方向正好相反：这是一套 Python / Go / C# SDK，用来把你自己的工具注册进涂鸦的 Agent 平台，而不是用来控制涂鸦设备。(official · ★67 · 2026-04)
- [Do1e/mijia-api](https://github.com/Do1e/mijia-api) - 米家云端 API、CLI 与 MCP（`uvx mijiaAPI mcp`）：扫码登录、设备属性、动作、场景。小米没有官方 MCP，这是事实标准。(★807 · 2026-08)
- [mihai-dinculescu/tapo](https://github.com/mihai-dinculescu/tapo) - Rust / Python 的 TP-Link Tapo 库，内置一等公民级 MCP server：插座、灯泡、网关、摄像头。(★803 · 2026-09)
- [sirkirby/unifi-mcp](https://github.com/sirkirby/unifi-mcp) - UniFi Network / Protect / Access MCP 套件；光 Protect server 就有 62 个工具。(★827 · 2026-09)
- [shenjingnan/xiaozhi-client](https://github.com/shenjingnan/xiaozhi-client) - 把多个标准 MCP server 聚合到一个小智接入点连接上，带 Web 配置界面。(★338 · 2026-09)
- [c1pher-cn/ha-mcp-for-xiaozhi](https://github.com/c1pher-cn/ha-mcp-for-xiaozhi) - 把 Home Assistant 作为 MCP server 暴露给小智设备的 HA 集成。(★268 · 2026-09)
- [xinnan-tech/mcp-endpoint-server](https://github.com/xinnan-tech/mcp-endpoint-server) - 小智 MCP 接入点：本地 MCP server 反向拨入的 WebSocket 注册中心，因此它们无法被宿主客户端直接拉起。(official · ★166 · 2026-06)
- [78/mcp-calculator](https://github.com/78/mcp-calculator) - 固件作者提供的小智反向连接 MCP 标准示例。(official · ★445 · 2026-02)
- [toddpan/xiaozhi-esp32-mcp](https://github.com/toddpan/xiaozhi-esp32-mcp) - 固件侧 MCP 客户端库，用于向小智注册 ESP32 工具。(★71 · 2025-10)
- [jango-blockchained/advanced-homeassistant-mcp](https://github.com/jango-blockchained/advanced-homeassistant-mcp) - 50+ 个 Home Assistant 工具，支持三种传输方式。(★56 · 2026-06)
- [alexpfau/zigbee2mqtt-mcp](https://github.com/alexpfau/zigbee2mqtt-mcp) - Zigbee2MQTT 管理：网状网络健康、OTA、配对、绑定。(★29 · 2026-09)
- [loryanstrant/ESPHome-MCP](https://github.com/loryanstrant/ESPHome-MCP) - ESPHome MCP，含 2026.6 版的 Device Builder。(★26 · 2026-08)
- [gehaiyi/xiaomi-home-mcp](https://github.com/gehaiyi/xiaomi-home-mcp) - 独立的小米云端 MCP，带型号自动映射与音箱控制。(★25 · 2026-04)
- [ykhli/mcp-light-control](https://github.com/ykhli/mcp-light-control) - 飞利浦 Hue 控制。(★22 · stale since 2025-03)
- [kingpanther13/Hubitat-local-MCP-server](https://github.com/kingpanther13/Hubitat-local-MCP-server) - 直接运行在 Hubitat 网关上的 Groovy MCP server：116 个工具，带规则引擎。(★18 · 2026-09)
- [scald/tesla-mcp](https://github.com/scald/tesla-mcp) - 通过 Fleet API 控制特斯拉车辆。(★15 · stale since 2025-03)
- [ichbinder/MCP2ZigBee2MQTT](https://github.com/ichbinder/MCP2ZigBee2MQTT) - Zigbee2MQTT 设备发现与控制。(★12 · 2025-10)
- [0x1abin/matter-controller-mcp](https://github.com/0x1abin/matter-controller-mcp) - Matter 控制器 MCP：发现、配网、控制。(★8 · stale since 2025-08)
- [MatterCoder/matter-mcp-server](https://github.com/MatterCoder/matter-mcp-server) - Matter 设备控制；控制器侧 Matter 覆盖的另一半。(★7 · stale since 2025-03)
- [TimCinel/homekit-mcp](https://github.com/TimCinel/homekit-mcp) - HomeKit（HAP）MCP；另有基于 macOS 原生 HomeKit 框架与 Homebridge 的替代方案。(★8 · 2026-03)
- [genm/switchbot-mcp](https://github.com/genm/switchbot-mcp) - SwitchBot 设备控制。(★7 · 2026-09)
- [noboru-i/nature-remo-mcp-server](https://github.com/noboru-i/nature-remo-mcp-server) - Nature Remo 红外网关。(★7 · stale since 2025-04)
- [caroliny1031/midea-mcp](https://github.com/caroliny1031/midea-mcp) - 美的空调，局域网优先、云端兜底。(★5 · 2026-08)
- [veonua/smartthings-mcp](https://github.com/veonua/smartthings-mcp) - 三星 SmartThings 的房间、设备与指令。(★5 · stale since 2025-07)
- [sandraschi/dreame-mcp](https://github.com/sandraschi/dreame-mcp) - 通过追觅云端（可选本地 miIO）控制追觅扫地机。(★4 · 2026-09)
- [cacack/mcp-server-zwave-js-ui](https://github.com/cacack/mcp-server-zwave-js-ui) - Z-Wave JS UI 的 WebSocket MCP：取值、配置、入网与退网。(★0 · 2026-08)
- [Buggy1111/shelly-mcp](https://github.com/Buggy1111/shelly-mcp) - Shelly Gen1–4 与 BLU 设备，本地优先；官方 MCP 注册表中极少数的智能家居 server 之一。(★0 · 2026-08)
- [Coolver/home-assistant-vibecode-agent](https://github.com/Coolver/home-assistant-vibecode-agent) - Home Assistant 加载项（或独立 Docker）Agent，提供 REST API 供配套 MCP server 调用，让 Claude Code、Cursor 与 VS Code 检查正在运行的 Home Assistant，并在设备上构建、部署、测试和调试自动化、脚本与仪表盘。(★629 · 2026-09)
- [robbrad/homeassistant-mcp](https://github.com/robbrad/homeassistant-mcp) - 基于 FastMCP 的 Home Assistant MCP server，提供 40 个工具控制灯光、温控、窗帘、门锁、媒体、扫地机和摄像头，支持 BM25 按需工具搜索、资源和引导提示词。(★106 · 2026-05)
- [tdeckers/openhab-mcp](https://github.com/tdeckers/openhab-mcp) - 面向真实 openHAB 实例的 MCP server，通过 REST API 列出、创建和更新 Item、Thing 与规则，并可查看 Thing 状态和固件更新。(★25 · 2026-06)
- [deswong/Openhab-MCP](https://github.com/deswong/Openhab-MCP) - Node.js 编写的 MCP server，把 openHAB v5+ REST API 暴露为 Item、Thing、规则、持久化和语义标签相关工具。(★7 · 2026-07)
- [saihgupr/esphome-mcp](https://github.com/saihgupr/esphome-mcp) - 面向 ESPHome Device Builder 的 MCP server，让智能体列出设备、编辑并校验 YAML 配置、编译固件并通过 OTA 刷写。(★16 · 2026-08)
- [loryanstrant/Zigbee2MQTT-MCP](https://github.com/loryanstrant/Zigbee2MQTT-MCP) - MCP server，通过 Zigbee2MQTT 前端 websocket API 列出、查看和控制 Zigbee 设备并管理网桥，无需直连 MQTT broker。(★4 · 2026-08)
- [solaegis/hubitat-mcp](https://github.com/solaegis/hubitat-mcp) - 面向 Hubitat Elevation 网关的 MCP server，通过 Maker API 控制设备，并可选开启受控的固件、Z-Wave 网络与备份管理工具。(★0 · 2026-08)
- [tim661811/homey-mcp](https://github.com/tim661811/homey-mcp) - 面向 Homey Pro 的 MCP server，可读取全屋状态、查询传感器与能耗历史，并根据自然语言描述创建可运行的 Flow。(★0 · 2026-09)
- [langowarny/smartthings-mcp](https://github.com/langowarny/smartthings-mcp) - 封装 Samsung SmartThings Public API 的 MCP server，覆盖设备、能力、指令、房间、场景、规则、网关与事件订阅。(★4 · 2025-12)
- [mp-consulting/homebridge-mcp-server](https://github.com/mp-consulting/homebridge-mcp-server) - 面向 Homebridge（经 homebridge-config-ui-x）的 MCP server，可控制配件、重启服务、读取并替换 config.json、查询插件及其配置 schema，并读取日志。(★5 · 2026-09)
- [adrighem/domoticz-mcp](https://github.com/adrighem/domoticz-mcp) - 面向 Domoticz 家庭自动化系统的 MCP server，可搜索和控制设备、场景、用户变量与事件脚本，并提供资源和提示词模板。(★0 · 2026-09)
- [joeynyc/Govee-MCP](https://github.com/joeynyc/Govee-MCP) - TypeScript 编写的 MCP server，通过 Govee 云端 API 用自然语言控制 Govee 智能灯，具备设备白名单、限流、指令合并和演练模式；局域网适配器只是占位实现，会回退到云端。(★9 · 2026-04)
- [Roach/airglow](https://github.com/Roach/airglow) - Philips Hue MCP server 加 Claude Code hooks，实时用 Hue 灯光颜色显示智能体状态，如思考中、工作中、成功或等待权限确认。(★10 · 2026-06)
- [tsali/lifx-mcp](https://github.com/tsali/lifx-mcp) - Python 编写的 MCP server，通过 UDP 在局域网内直接控制 LIFX 灯，支持发现、分组、颜色预设、场景与呼吸/脉冲效果，无需云端。(★0 · 2026-04)
- [Tommertom/sonos-ts-mcp](https://github.com/Tommertom/sonos-ts-mcp) - TypeScript 编写的 MCP server，通过 UPnP/SOAP 控制局域网内的 Sonos 音箱，覆盖播放、分区编组、队列、曲库浏览和闹钟。(★15 · 2025-11)
- [emrikol/ecobee-mcp](https://github.com/emrikol/ecobee-mcp) - TypeScript 编写的 MCP server，用于控制 Ecobee 温控器，基于官方 MCP TypeScript SDK 的性能优化分支构建。(★1 · 2026-08)
- [holger1411/roborock-mcp](https://github.com/holger1411/roborock-mcp) - 非官方 Roborock 扫地机 MCP server（V1 协议），可读取状态、按房间下发清扫任务并查看清扫历史和耗材损耗。(★2 · 2026-07)
- [caffeinum/irobot-mcp](https://github.com/caffeinum/irobot-mcp) - CLI 与 MCP server，经局域网直连 iRobot Roomba 自带的 MQTT broker，读取状态、启动/暂停/回充任务，并解码机器人停止原因。(★0 · 2026-09)
- [andresgarcia0313/samsung-tv-mcp](https://github.com/andresgarcia0313/samsung-tv-mcp) - 提供 18 个工具的 MCP server，在局域网内控制 Samsung Tizen 智能电视，支持 SSDP 自动发现，无需云端或 SmartThings 账号。(★0 · 2026-03)
- [tanny-pm/switchbot-mcp](https://github.com/tanny-pm/switchbot-mcp) - Rust 编写的 MCP server，通过带 HMAC-SHA256 签名的 SwitchBot API v1.1 把 SwitchBot 设备暴露为工具，可列出、查询和操作设备。(★1 · 2026-07)
- [Jacou/lg-thinq-mcp](https://github.com/Jacou/lg-thinq-mcp) - 基于 ThinQ Connect API 的 LG ThinQ 家电 MCP server，可列出设备、读取状态并向洗衣机、烘干机、洗碗机等发送控制指令，另附独立的 MQTT 监听程序，将程序完成通知推送到 webhook。(★0 · 2026-01)
- [danecodes/roku-mcp](https://github.com/danecodes/roku-mcp) - MCP server 与 CLI，让智能体在 Roku 设备上查看 SceneGraph 界面、截图、发送遥控输入、侧载开发包并运行冒烟测试。(★4 · 2026-04)

### 实验室仪器（MCP）

- [lagerdata/lager](https://github.com/lagerdata/lager) - 从笔记本或 CI 发起的硬件测试自动化，带 MCP server；支持普源、是德、吉时利。(★8 · 2026-09)
- [JanGoebel/LabVIEW-MCP-Server-Toolkit](https://github.com/JanGoebel/LabVIEW-MCP-Server-Toolkit) - 在 LabVIEW 中托管 MCP server，让 VI 变成工具。(★56 · 2026-07)
- [Zuehlke/labview-mcp](https://github.com/Zuehlke/labview-mcp) - 通过 NI gRPC 读、写并运行 LabVIEW VI；以 Claude 插件形式安装。(★29 · 2026-09)
- [erebusnz/rigol-mcp](https://github.com/erebusnz/rigol-mcp) - 通过局域网或 USB 控制普源 DS1000Z / MSO1000Z / DHO 示波器。(★29 · 2026-07)
- [lucasgerads/lecroy-mcp](https://github.com/lucasgerads/lecroy-mcp) - 通过 VXI-11 或 USB 控制力科 WaveSurfer / HDO / WaveRunner / WavePro。(★11 · 2026-04)
- [Netlist-Studio/scope-mcp](https://github.com/Netlist-Studio/scope-mcp) - 通过以太网控制是德 / 安捷伦示波器，已在 MSOX2024A 上测试。(★11 · 2026-02)
- [Anai-Guo/LabAgent](https://github.com/Anai-Guo/LabAgent) - 通过 GPIB / USB / 串口支持 26 家厂商的 68 种仪器型号，提供 MCP、Web 与 CLI。(★8 · 2026-09)
- [MagnusJohansson/siglent-sds-mcp](https://github.com/MagnusJohansson/siglent-sds-mcp) - 通过 SCPI TCP 控制鼎阳 SDS1000X-E。(★7 · 2026-02)
- [techmanual-ai/lablink-mcp](https://github.com/techmanual-ai/lablink-mcp) - 统一的实验设备 MCP，支持 VISA / SCPI、SSH、REST 与串口；已在泰克 MSO44、鼎阳 SDG 与是德电源上测试。(★5 · 2026-09)
- [Keysight/cyperf-mcp](https://github.com/Keysight/cyperf-mcp) - 是德官方用于驱动 CyPerf 流量生成 agent 的 MCP。(official · ★1 · 2026-04)
- [daqifi/daqifi-core](https://github.com/daqifi/daqifi-core) - 面向 DAQiFi Nyquist 无线数采的 .NET SDK 与 MCP server。(official · ★5 · 2026-09)
- [KenosInc/dwf-mcp-server](https://github.com/KenosInc/dwf-mcp-server) - 通过 WaveForms SDK 控制 Digilent Analog Discovery 3（示波器、任意波形发生器、逻辑分析仪、电源）。(★3 · 2026-08)
- [armchairdeity/mcp-server-scpi](https://github.com/armchairdeity/mcp-server-scpi) - 带高层工具的 SCPI / VISA MCP，后端为普源 DS1054Z。(★3 · 2026-07)
- [JacobBeningo/devsignal](https://github.com/JacobBeningo/devsignal) - 鼎阳 SDG 信号发生器的 CLI 与 MCP。(★3 · 2026-07)
- [hsoffar/saleae-logic2-mcp](https://github.com/hsoffar/saleae-logic2-mcp) - Saleae Logic 2 逻辑分析仪自动化。(★3 · 2026-03)
- [TECTOS-JP/lab-visa-mcp](https://github.com/TECTOS-JP/lab-visa-mcp) - PyVISA MCP，用 YAML 定义仪器指令集与安全范围；姊妹项目 `lab-modbus-mcp` 面向冷水机与温控器。(★0 · 2026-08)
- [yerbymatey/opentrons-mcp](https://github.com/yerbymatey/opentrons-mcp) - 通过 HTTP API 控制 Opentrons OT-2 / Flex。(★7 · stale since 2025-06)
- [nygmeta/OpenLabAI](https://github.com/nygmeta/OpenLabAI) - 面向 Opentrons OT-2、Hamilton STAR、Biomek FXP 与 Cellario 的 MCP server，带人工审批门禁。(★0 · 2026-09)
- [ghollyer/AMADEUS](https://github.com/ghollyer/AMADEUS) - Gatan / DigitalMicrograph 电子显微镜：通过 ZMQ 控制样品台、电子束、STEM 与 EDS。(★4 · 2026-07)
- [sandraschi/sdr-mcp](https://github.com/sandraschi/sdr-mcp) - RTL-SDR：频谱、瀑布图、FM 解调、GNU Radio。(★7 · 2026-09)
- [masahiro-999/oscilloscope-mcp](https://github.com/masahiro-999/oscilloscope-mcp) - MCP server，让智能体经 LAN/SCPI 操作 RIGOL DS1000Z 台式示波器，设置触发与通道、读取测量并采集真实波形，为 FPGA 开发提供反馈。(★3 · 2026-06)
- [DVSProductions/rigol-mcp](https://github.com/DVSProductions/rigol-mcp) - MCP server，经 TCP 5555 端口裸 SCPI 驱动 Rigol DS1000Z/MSO1000Z 示波器，无需 VISA，可返回屏幕截图、测量值和波形采集。(★0 · 2026-07)
- [gloveboxes/rigol-mcp](https://github.com/gloveboxes/rigol-mcp) - 基于标准的 stdio MCP server，经 LAN 控制 Rigol 示波器，以 DHO814 为主要测试机型，提供按型号过滤的指令目录和流式存储下载。(★0 · 2026-09)
- [mp911de/siglent-scpi-mcp](https://github.com/mp911de/siglent-scpi-mcp) - MCP server，经 SCPI/TCP 连接 Siglent 示波器和电源，提供带类型校验的工具并回报每次写操作所用 SCPI，内置 OpenTelemetry 可观测性。(★0 · 2026-09)
- [abhinav937/pyvisa-mcp](https://github.com/abhinav937/pyvisa-mcp) - MCP server，借助 PyVISA 让 AI 工具经 USB、GPIB、串口与以太网发现和驱动示波器等 SCPI 仪器，并跨会话记忆每台仪器的指令方言。(★0 · 2026-09)
- [colingimenez/SCPI_MCP](https://github.com/colingimenez/SCPI_MCP) - MCP server，把联网的波形发生器、万用表、示波器和电源暴露为 76 个工具（含一个裸 SCPI 透传工具），让编码智能体在台架上调查电路。(★1 · 2026-08)
- [rbxxswap/labview-mcp](https://github.com/rbxxswap/labview-mcp) - LabVIEW MCP 插件，让 Claude 运行 VI、读写前面板控件、执行测试、生成 VI 代码、构建可执行文件并读取 TDMS 数据，支持 Community Edition。(★2 · 2026-06)
- [AnterCreeper/keyscope-mcp](https://github.com/AnterCreeper/keyscope-mcp) - 纯 Python MCP 服务，经 USBTMC 通过单个紧凑 DSL 工具控制 Keysight EDUX1052G 示波器，返回波形、数据和截图。(★0 · 2026-05)
- [clarholm/NanoVNA-MCP](https://github.com/clarholm/NanoVNA-MCP) - 面向 NanoVNA-H4 矢量网络分析仪的串口 MCP server，可扫描天线并测量带宽与阻抗，附带生成 SWR 与史密斯圆图 PDF 报告的 skill。(★0 · 2026-03)
- [createskyblue/Yingjia_EMK850_low-power_analyzer_MCP](https://github.com/createskyblue/Yingjia_EMK850_low-power_analyzer_MCP) - 逆向 Yingjia EMK850+ 低功耗分析仪串口协议的驱动、CLI 与 MCP server，可自动化 µA/µW 级功耗采集和可编程电源控制。(★2 · 2026-08)

### 摄像头（MCP）

- [reolink/reolink-cli](https://github.com/reolink/reolink-cli) - 仅限局域网的 Reolink CLI，内置 MCP stdio server 与 SKILL.md：抓图、云台、RTSP。(official · ★99 · 2026-09)
- [evalstate/mcp-webcam](https://github.com/evalstate/mcp-webcam) - 把网络摄像头画面作为工具与资源提供。(★121 · 2025-10)
- [jakekeeys/frigate-mcp](https://github.com/jakekeeys/frigate-mcp) - Frigate NVR，90 个工具与 HTTP API 一一对应。(★12 · 2026-09)
- [sandraschi/tapo-mcp](https://github.com/sandraschi/tapo-mcp) - TP-Link Tapo 摄像头：云台、抓图、推流。(★2 · 2026-09)
- [ros-claw/librealsense-mcp](https://github.com/ros-claw/librealsense-mcp) - 封装 pyrealsense2 的 26 个工具：深度、点云、标定、多相机。(★1 · 2026-07)
- [oneshot2001/onvif-pp-cli](https://github.com/oneshot2001/onvif-pp-cli) - ONVIF Profile S / T / G / M 的 CLI 与 MCP，64 条命令，已在 Axis 摄像头上冒烟测试。(★0 · 2026-05)
- [brianegge/dahua-mcp](https://github.com/brianegge/dahua-mcp) - MCP server，通过 CGI HTTP API 管理多台 Dahua 与 Amcrest 网络摄像头，支持 stdio 与 HTTP 传输。(★5 · 2026-09)
- [ed-dryha/reolink-mcp](https://github.com/ed-dryha/reolink-mcp) - 局域网 Reolink 摄像头 MCP server，可获取快照、设备与 AI 检测状态、PTZ 预置位，并控制聚光灯、警笛和红外/白光 LED，无需云端或 NVR。(★2 · 2026-07)
- [oneshot2001/onvif-mcp](https://github.com/oneshot2001/onvif-mcp) - 实验性的受管控网络摄像头 MCP server（AXIS VAPIX 与 ONVIF SOAP），提供快照与 PTZ 工具以及仅支持 VAPIX 的配置漂移工具，每次调用都经过按智能体划分、失败即拒绝的策略闸门并生成签名的哈希链回执。(★1 · 2026-09)
- [DataKnifeAI/unifi-protect-mcp](https://github.com/DataKnifeAI/unifi-protect-mcp) - Go 编写的 Ubiquiti UniFi Protect MCP server，可查询摄像头、传感器、智能灯、门铃提示器、实时画面、显示终端、NVR 与安防事件，并执行 PTZ 巡航与预置位、RTSPS 流和对讲会话；项目标注为早期开发阶段。(★0 · 2026-08)
- [vijayg10/iot-onvif-mcp](https://github.com/vijayg10/iot-onvif-mcp) - 容器化的 ONVIF MCP server（HTTP/SSE），可列出摄像头配置与流地址，通过快照或 ffmpeg RTSP 回退抓图，并执行 PTZ 移动与预置位。(★1 · 2026-03)

### 无线与软件无线电（MCP）

- [es617/ble-mcp-server](https://github.com/es617/ble-mcp-server) - 基于 bleak 的跨平台 BLE：扫描、连接、GATT 读取与订阅。(★18 · 2026-03)
- [stass/blew](https://github.com/stass/blew) - macOS 上的 BLE CLI 与 MCP，支持外设模式。(★18 · 2026-05)
- [mr-tbot/mesh-api](https://github.com/mr-tbot/mesh-api) - 面向 Meshtastic 与 MeshCore 的离网 AI 路由器，带 MCP server 与 OpenClaw Skill。(★173 · 2026-07)
- [busse/flipperzero-mcp](https://github.com/busse/flipperzero-mcp) - 通过 USB 或 Wi-Fi 控制 Flipper Zero。(★32 · 2025-12)
- [Wet-wr-Labs/claupper](https://github.com/Wet-wr-Labs/claupper) - 一个 Flipper Zero `.fap` 应用，充当单手 BLE / USB 遥控器，用来批准或拒绝 Agent 的操作。(★27 · 2026-05)
- [roostercoopllc/flipper-mcp](https://github.com/roostercoopllc/flipper-mcp) - 运行在 Flipper 的 ESP32-S2 Wi-Fi 开发板上的 MCP server，通过 UART 桥接约 30 个工具（Sub-GHz、NFC、RFID、红外、BLE、GPIO）。(★17 · 2026-03)
- [jonastbrg/FlipperAgent](https://github.com/jonastbrg/FlipperAgent) - Flipper MCP 与 Agent，67 个工具，带 ESP32 Marauder 桥与 Skill。(★10 · 2026-03)
- [N-Erickson/AetherLink-SDR-MCP](https://github.com/N-Erickson/AetherLink-SDR-MCP) - RTL-SDR 与 HackRF：ADS-B、AIS、POCSAG、Meteor LRPT。(★24 · 2026-07)
- [thehappydinoa/hackrf-mcp](https://github.com/thehappydinoa/hackrf-mcp) - 封装 hackrf_tools：扫频、IQ 采集与发射。(★2 · 2026-08)
- [mplogas/pm3-mcp](https://github.com/mplogas/pm3-mcp) - Proxmark3（Iceman 固件）RFID / NFC 识别与读取。(★3 · 2026-06)
- [oliveres/chirpstack-mcp-server](https://github.com/oliveres/chirpstack-mcp-server) - 通过 gRPC 访问 ChirpStack v4 LoRaWAN，支持实时上行调试。(★0 · 2026-08)
- [swannman/openthread-mcp](https://github.com/swannman/openthread-mcp) - Arduino Nano Matter 上的 OpenThread CLI MCP 与 Prometheus 导出器；找到的唯一 Thread MCP。(★1 · 2026-03)
- [koolsb/zwavejs-mcp](https://github.com/koolsb/zwavejs-mcp) - Z-Wave JS UI 维护：修复网络、重新问询、诊断，并对门锁相关信息做脱敏。(★0 · 2026-06)
- [yoelbassin/gr-mcp](https://github.com/yoelbassin/gr-mcp) - Marconi（原 GR-MCP）：GNU Radio Agent 工具，扫描频谱并构建接收机，产出 SigMF 采集、YAML 流水线与 .grc 流图；v1.0 仅支持仿真。(★51 · 2026-08)
- [patrickrb/smartsdr-mcp](https://github.com/patrickrb/smartsdr-mcp) - FlexRadio SmartSDR 电台的 MCP server，支持频率/模式控制、CW 解码、SSB 转写与需审批的发射。(★3 · 2026-03)
- [ConsentirDev/meshtastic.mcp](https://github.com/ConsentirDev/meshtastic.mcp) - Meshtastic MCP server，经 USB 串口、TCP 或蓝牙连接，发送消息、traceroute 并读取节点遥测。(★6 · 2025-11)
- [millsymills-com/flipperzero-mcp](https://github.com/millsymills-com/flipperzero-mcp) - Flipper Zero MCP server，经 USB 或 WiFi Dev Board 使用 protobuf RPC，提供存储、应用、GPIO 与 CLI 工具，发射/写入工具默认关闭。(★5 · 2026-09)

### USB、HID 与 KVM（MCP）

- [verygoodplugins/streamdeck-mcp](https://github.com/verygoodplugins/streamdeck-mcp) - 通过配置文件操作 Elgato Stream Deck，附带一个 Skill。(★44 · 2026-08)
- [tinqiao-oss/clawtouch-mcp](https://github.com/tinqiao-oss/clawtouch-mcp) - 把树莓派 Pico 2 上真实的 USB-HID 键盘与鼠标暴露为 MCP 工具。(★10 · 2026-09)
- [Oliver0804/cynthion-mcp](https://github.com/Oliver0804/cynthion-mcp) - 驱动 Cynthion USB 测试仪：嗅探、解码与模拟 USB 通信。(★5 · 2026-05)
- [bsu-tool/bsu-tool](https://github.com/bsu-tool/bsu-tool) - "Behavioral Sleuth for USB"：在 Linux 上抓取、解码与分析 USB 协议，同时提供 CLI 与 MCP server。(★5 · 2026-08)
- [elgatosf/elgato-mcp-server](https://github.com/elgatosf/elgato-mcp-server) - Elgato 官方用于自动化其应用的 MCP。(official · ★10 · 2026-09)
- [sunasaji/mcp-serial-hid-kvm](https://github.com/sunasaji/mcp-serial-hid-kvm) - CH9329 USB-HID 加 HDMI 采集：Agent 像 KVM 一样操作一台真实电脑，并带 OCR。(★4 · 2026-04)
- [yindia/qmkmcp](https://github.com/yindia/qmkmcp) - 通过 raw HID 操作任意 QMK / VIA 键盘：灯光、键位、宏。(★0 · 2026-08)
- [Kevin-HYX/kvmctl](https://github.com/Kevin-HYX/kvmctl) - 运行在香橙派上、基于 V4L2 与 USB gadget HID 的 KVM 控制服务，提供 CLI 与 MCP。(★0 · 2026-09)
- [mantis5x5/kvm-automation](https://github.com/mantis5x5/kvm-automation) - MCP server、CLI 与 skills，通过 HDMI 采集与 USB HID 对 GLKVM、PiKVM、TinyPilot IP-KVM 进行带外自动化。(★18 · 2026-08)
- [shvartzj1/jetkvm-mcp](https://github.com/shvartzj1/jetkvm-mcp) - 面向原厂 JetKVM 设备的 MCP server：在操作系统之下截图、键入、点击、挂载启动介质与控制电源。(★7 · 2026-09)
- [kennypeh85/glkvm-mcp](https://github.com/kennypeh85/glkvm-mcp) - GL.iNet GLKVM MCP server，提供键盘、鼠标、截图与 Tesseract OCR，让 Agent 按文字点击界面元素。(★8 · 2026-06)
- [DVSProductions/comet-kvm-mcp](https://github.com/DVSProductions/comet-kvm-mcp) - GL.iNet Comet（GL-RM1）KVM 的 MCP server，封装 kvmd HTTP API 实现截图、键盘、鼠标与 ATX 电源控制。(★6 · 2026-07)
- [DustinTrap/kvm-pilot](https://github.com/DustinTrap/kvm-pilot) - 带权限门控与审计的 MCP server，通过 IP-KVM（PiKVM、GLKVM、BliKVM）、BMC（Redfish/IPMI）、Intel AMT 与 SSH 控制裸机。(★5 · 2026-08)
- [KultivatorConsulting/pikvm_mcp_server](https://github.com/KultivatorConsulting/pikvm_mcp_server) - PiKVM MCP server，提供键盘、鼠标与屏幕访问，并支持基于视觉的鼠标自动校准。(★3 · 2026-03)
- [JacobBeningo/devusb](https://github.com/JacobBeningo/devusb) - CLI 与 MCP server，通过 Yepkit YKUSH 集线器或兼容 uhubctl 的通用集线器，对工作台设备做 USB 电源开关与重启。(★5 · 2026-07)

### EDA / PCB / CAD（MCP）

- [mixelpixx/KiCAD-MCP-Server](https://github.com/mixelpixx/KiCAD-MCP-Server) - 直接从 Claude 编辑 KiCad 原理图与 PCB。(★2.3k · 2026-09)
- [Arcadia-1/virtuoso-bridge-lite](https://github.com/Arcadia-1/virtuoso-bridge-lite) - LLM Agent 与 Cadence Virtuoso 之间的桥，用于 Agent 化的模拟与混合信号设计；在商用 EDA 桥接中星数遥遥领先。(★740 · 2026-09)
- [gokeshenzhen/TraceWeave](https://github.com/gokeshenzhen/TraceWeave) - 基于证据的 RTL 仿真调试 MCP：把 VCS 与 Xcelium 日志和 VCD、FSDB 波形关联起来。(★111 · 2026-09)
- [qfliuyang/hipilot](https://github.com/qfliuyang/hipilot) - VLSI 物理设计助手，带面向 Synopsys ICC2 与 Cadence Innovus 的 MCP server。(★7 · 2026-03)
- [lamaalrajih/kicad-mcp](https://github.com/lamaalrajih/kicad-mcp) - KiCad 工程管理、DRC、BOM 与网表分析。(★522 · 2025-10)
- [salitronic/eda-agent](https://github.com/salitronic/eda-agent) - 290+ 个工具驱动正在运行的 Altium Designer 会话，可选 KiCad / 嘉立创 EDA 专业版。(★204 · 2026-09)
- [jhacksman/OpenSCAD-MCP-Server](https://github.com/jhacksman/OpenSCAD-MCP-Server) - 文本或图片 → 参数化 OpenSCAD 三维模型。(★193 · 2026-09)
- [coffeenmusic/altium-mcp](https://github.com/coffeenmusic/altium-mcp) - Altium Designer PCB 查询与操作。(★161 · 2026-09)
- [Seeed-Studio/kicad-mcp-server](https://github.com/Seeed-Studio/kicad-mcp-server) - 矽递维护的 KiCad MCP：引脚级连通性追踪与设计编辑。(official · ★130 · 2026-09)
- [mapleleavessssssss-wq/vivado-mcp](https://github.com/mapleleavessssssss-wq/vivado-mcp) - 30 个工具的 Vivado MCP，支持 GUI、Tcl 与附加模式。(★130 · 2026-08)
- [circuit-synth/kicad-sch-api](https://github.com/circuit-synth/kicad-sch-api) - KiCad 原理图 s-expression 的 Python API，带一个 [MCP 封装](https://github.com/circuit-synth/mcp-kicad-sch-api)。(★53 · 2025-12)
- [Netlist-Studio/kicad-mcp](https://github.com/Netlist-Studio/kicad-mcp) - 通过 IPC API 控制 KiCad 9。(★19 · 2026-02)
- [octoco-ltd/sheetsdata-mcp](https://github.com/octoco-ltd/sheetsdata-mcp) - 元器件数据手册：从 PDF 提取规格、引脚图与绝对最大额定值。(★12 · 2026-04)
- [WangErShao/SynthAid_quartus_mcp](https://github.com/WangErShao/SynthAid_quartus_mcp) - 22 个工具的 Intel Quartus MCP。(★3 · 2026-06)
- [neka-nat/freecad-mcp](https://github.com/neka-nat/freecad-mcp) - FreeCAD 插件加 MCP server，让 Agent 创建和编辑模型、运行 Python 脚本、检查文档并运行 FEM 分析。(★2.4k · 2026-09)
- [eyfel/mcp-server-solidworks](https://github.com/eyfel/mcp-server-solidworks) - SolidPilot：SolidWorks MCP server，在底层 CAD 工具之外提供与 CAD 无关的 Feature Graph IR 编译器（目前用于从 IR 重建零件）以及仍在完善的 DXF/DWG 图纸读取器。(★321 · 2026-09)
- [spkane/freecad-addon-robust-mcp-server](https://github.com/spkane/freecad-addon-robust-mcp-server) - FreeCAD Robust MCP server，附带 MCP Bridge 工作台插件，可通过 pip 或 Docker 安装。(★234 · 2026-09)
- [hyl64/jlcmcp](https://github.com/hyl64/jlcmcp) - 嘉立创 EDA 专业版 MCP server，把工具调用编译成官方 eda.* API 代码，经 Run API Gateway 扩展执行原理图与 PCB 自动化。(★223 · 2026-08)
- [ReshefElisha/jarvis-onshape-mcp](https://github.com/ReshefElisha/jarvis-onshape-mcp) - Claude Code 插件，驱动 Onshape（草图、拉伸、配合、FeatureScript），返回结构化重建反馈与多视图 PNG 渲染，并附视觉拆解 skill。(★170 · 2026-04)
- [hedless/onshape-mcp](https://github.com/hedless/onshape-mcp) - Onshape MCP server，48 个工具覆盖草图、特征、装配与配合、变量表、FeatureScript 以及 STEP/STL 导出。(★143 · 2026-09)
- [RobertCoop/openscad-mcp](https://github.com/RobertCoop/openscad-mcp) - OpenSCAD MCP server（uvx openscad-mcp），可渲染、测量几何、检查装配干涉与间隙、评估可打印性并导出零件。(★138 · 2026-09)
- [AuraFriday/Fusion-360-MCP-Server](https://github.com/AuraFriday/Fusion-360-MCP-Server) - Autodesk Fusion 插件，经 MCP-Link server 把 Fusion 暴露给 AI Agent，提供通用 API 桥与 Fusion 内 Python 执行。(★126 · 2026-01)
- [jdilla1277/agentcad](https://github.com/jdilla1277/agentcad) - CAD CLI 与 MCP server：Agent 编写 build123d 脚本，获得 STEP/STL 导出、PNG 渲染、几何度量、校验与差异比对。(★128 · 2026-09)
- [Averyy/pcbparts-mcp](https://github.com/Averyy/pcbparts-mcp) - 跨 JLCPCB、Mouser、DigiKey 做参数化元件搜索的 MCP server，提供 KiCad 封装、引脚、替代料与参考板设计规则。(★114 · 2026-09)
- [pzfreo/build123d-mcp](https://github.com/pzfreo/build123d-mcp) - build123d MCP server，让 Agent 逐步构建 CAD 模型、渲染预览、测量几何并导出 STEP、STL、SVG、DXF。(★88 · 2026-09)
- [embedded-society/altium-designer-mcp](https://github.com/embedded-society/altium-designer-mcp) - MCP server，读写 Altium Designer 的 .PcbLib 封装与 .SchLib 符号库，让 Agent 创建符合 IPC-7351B 的元件。(★61 · 2026-09)
- [andrewbartels1/SolidworksMCP-python](https://github.com/andrewbartels1/SolidworksMCP-python) - SolidWorks 的 Python MCP server，132 个工具覆盖建模、草图、工程图、分析、导出与宏（经 COM/VBA）。(★76 · 2026-09)
- [faust-machines/fusion360-mcp-server](https://github.com/faust-machines/fusion360-mcp-server) - MCP server 加 Fusion 360 插件，经 TCP 转发 Agent 命令并在主线程执行 Fusion API 调用。(★98 · 2026-09)
- [clanker-lover/spicebridge](https://github.com/clanker-lover/spicebridge) - SPICEBridge：ngspice MCP server，28 个工具支持 AC/瞬态/DC 仿真、Monte Carlo、电路模板与 KiCad 原理图导出。(★35 · 2026-04)
- [xuio/ltspice-mcp](https://github.com/xuio/ltspice-mcp) - macOS 上的 LTspice MCP server，运行仿真、生成原理图、渲染波形并查询 RAW 数据做验证。(★19 · 2026-05)
- [ariklapid/pyslang-mcp](https://github.com/ariklapid/pyslang-mcp) - 只读 MCP server，基于 pyslang 编译器为 Agent 提供 Verilog/SystemVerilog 上下文：诊断、实例层级与符号引用。(★21 · 2026-06)
- [najaeda/naja-scope](https://github.com/najaeda/naja-scope) - 基于 najaeda 网表引擎的 MCP server，让 Agent 追踪连接关系并遍历已展开 SystemVerilog 设计的层级。(official · ★16 · 2026-09)
- [blwfish/kicad-mcp](https://github.com/blwfish/kicad-mcp) - KiCad MCP server，17 个工具支持原理图绘制、布局、FreeRouting 自动布线、DRC 与拼板生产输出。(★17 · 2026-09)
- [cheewee2000/flamingo-pcb](https://github.com/cheewee2000/flamingo-pcb) - 以提示词为先的 PCB CAD，经 MCP（34 个工具）选取真实 LCSC 元件、用 Freerouting 自动布线、运行 DRC 并导出 JLCPCB 生产包。(★6 · 2026-09)
- [abbbe/fpga-mcp-servers](https://github.com/abbbe/fpga-mcp-servers) - 两个用于 DE10-Nano 开发的 MCP server：异步 Intel Quartus 构建与板卡管理。(coll · ★10 · 2026-01)
- [lcapossio/fpgaZeroMCP](https://github.com/lcapossio/fpgaZeroMCP) - 集成开源 FPGA 工具链的 MCP server：lint、仿真、综合、布局布线，并为 iCEBreaker、ULX3S 等 11 种板卡预设烧录比特流。(★5 · 2026-08)
- [Cai-aa/CAD-Agent-Hub](https://github.com/Cai-aa/CAD-Agent-Hub) - 面向 Windows 的 CATIA V5、SolidWorks、Siemens NX MCP server 与桥接，另含 Fusion Electronics 写入桥和 ANSYS Workbench skill。(coll · ★61 · 2026-09)

### 边缘 AI 与 SBC（MCP）

- [Zalmotek/jetson-mcp](https://github.com/Zalmotek/jetson-mcp) - 通过 SSH 监视并远程控制 Jetson。(★11 · stale since 2025-04)
- [axonixtools/PocketMCP](https://github.com/axonixtools/PocketMCP) - 把安卓手机变成暴露其传感器的 MCP server。(★17 · 2026-08)
- [edgeimpulse/ei-agentic-claude](https://github.com/edgeimpulse/ei-agentic-claude) - 官方 `@edgeimpulse/mcp-server` npm 包的源码；Studio 工作流的概念验证，不负责部署到设备。(official · ★3 · 2026-02)
- [marc-shade/coral-tpu-mcp](https://github.com/marc-shade/coral-tpu-mcp) - Google Coral Edge TPU 推理；唯一的 Coral 条目。(★1 · 2026-02)
- [dmmdea/Hailo-8L-Analysis-Pipelines](https://github.com/dmmdea/Hailo-8L-Analysis-Pipelines) - 14 个工具的 MCP，在 Hailo-8L 上跑人脸检测、OCR 与 CLIP。(★0 · 2026-08)
- [grammy-jiang/RaspberryPiOS-MCP](https://github.com/grammy-jiang/RaspberryPiOS-MCP) - 树莓派 OS：GPIO、I2C、摄像头。(★0 · 2026-03)
- [zja0011/edgesentinel-visionops](https://github.com/zja0011/edgesentinel-visionops) - EdgeSentinel：运行在 Jetson Nano 上的视觉 Agent harness，含实时检测、MCP 工具、RBAC 确认门与离线降级。(★22 · 2026-08)
- [nbhansen/retroMCP](https://github.com/nbhansen/retroMCP) - 通过 SSH 管理 Raspberry Pi 系统的 MCP server，涵盖硬件信息、手柄、温度与 RetroPie 配置。(★3 · 2025-10)

### 数字制造（MCP）

- [DMontgomery40/mcp-3D-printer-server](https://github.com/DMontgomery40/mcp-3D-printer-server) - OctoPrint、Klipper、Duet、Repetier、Prusa、拓竹与创想三维，外加 STL 操作。(★237 · 2026-07)
- [DMontgomery40/bambu-printer-mcp](https://github.com/DMontgomery40/bambu-printer-mcp) - 拓竹本地 MQTT / FTPS，外加 BambuStudio 切片与 STL 操作。(★142 · 2026-07)
- [griches/bambu-mcp](https://github.com/griches/bambu-mcp) - 仅限局域网的拓竹 MQTT / FTPS 机群管理。(★46 · 2026-03)
- [OctoEverywhere/mcp](https://github.com/OctoEverywhere/mcp) - 免费的 3D 打印 MCP：实时状态、摄像头抓图、控制。(★37 · stale since 2025-07)
- [Charleslotto/klipper-mcp](https://github.com/Charleslotto/klipper-mcp) - 通过 Moonraker 控制 Klipper，100+ 个工具，支持换头，并对危险操作设有"上膛"开关。(★24 · 2026-08)
- [bjan/pycentauri](https://github.com/bjan/pycentauri) - Elegoo Centauri Carbon（SDCP WebSocket / MQTT）的客户端、CLI 与 MCP。(★22 · 2026-07)
- [schwarztim/bambu-mcp](https://github.com/schwarztim/bambu-mcp) - 拓竹本地 MQTT + FTPS + X.509，带摄像头与 AMS，25 个工具。(★19 · 2026-09)
- [GLechevalier/OpenGalatea](https://github.com/GLechevalier/OpenGalatea) - 通过 PrusaLink 控制 Prusa：Printables 搜索、自动切片、完整任务控制。(★19 · 2026-04)
- [Noosbai/PrusaMCP](https://github.com/Noosbai/PrusaMCP) - PrusaSlicer MCP，17 个工具，带 FDM 参数推荐引擎与网格分析。(★8 · 2026-02)
- [zackpeters93/ugs-mcp](https://github.com/zackpeters93/ugs-mcp) - 通过 Universal GCode Sender Pendant REST API 控制 GRBL 数控机床，运动指令需令牌授权。(★5 · 2026-06)
- [damione1/maslow-desktop](https://github.com/damione1/maslow-desktop) - Maslow CNC（FluidNC）控制面板，带 MCP。(★3 · 2026-07)
- [bleugreen/openpnp-mcp](https://github.com/bleugreen/openpnp-mcp) - OpenPnP；找到的唯一贴片机 MCP。(★0 · 2026-03)
- [mikehatch/KlipperMCP](https://github.com/mikehatch/KlipperMCP) - MCP server，经 Moonraker 读取并编辑 Klipper printer.cfg（自动备份），评估宏与 Jinja2 模板，执行 G-code 并控制多台打印机的打印任务。(★7 · 2026-08)
- [synman/bambu-mcp](https://github.com/synman/bambu-mcp) - 自包含的 Bambu Lab 3D 打印机局域网模式 MCP server，经 MQTT 与 FTPS 提供发现、打印控制、温控、耗材/AMS、摄像头与文件管理等工具。(★4 · 2026-09)
- [Eyalm321/bambu-mcp](https://github.com/Eyalm321/bambu-mcp) - npm 发布的 MCP server（`npx bambu-mcp`），在局域网模式下经 MQTT 与 FTPS 为 Bambu Lab P2S、P1S、X1 打印机切片、上传、打印并监控。(★1 · 2026-07)
- [MrMebelMan/bambuddy-mcp](https://github.com/MrMebelMan/bambuddy-mcp) - MCP server，启动时根据 Bambuddy 打印管理实例的 OpenAPI 规范生成工具，并通过三个元工具（分类浏览、搜索、执行）开放整个 REST API，摄像头快照以图片形式返回。(★5 · 2026-02)
- [gioelemo/prusa-mcp](https://github.com/gioelemo/prusa-mcp) - 面向 Prusa Connect 的 MCP server，一次性 OAuth2 PKCE 登录后即可列出打印机、跟踪任务、浏览文件，并发送暂停、恢复和温度指令。(★2 · 2026-09)
- [nixkor/moonraker-mcp](https://github.com/nixkor/moonraker-mcp) - 设计为运行在 Moonraker 旁边树莓派上的 HTTP MCP 守护进程，提供 Klipper 打印机状态、温度、文件、打印任务控制与 G-code/宏执行。(★1 · 2026-06)
- [skribascode/elegoo-mcp-server](https://github.com/skribascode/elegoo-mcp-server) - 本地 MCP server，经 SDCP 协议控制 Elegoo 3D 打印机，支持多机管理、状态读取与打印暂停、恢复、停止和启动，已在 Centauri Carbon 上测试。(★2 · 2026-01)
- [WhitneyDesignLabs/cnc-fluidnc-mcp](https://github.com/WhitneyDesignLabs/cnc-fluidnc-mcp) - 提供 27 个工具的 MCP server，让 Claude 经 WebSocket 与 HTTP 控制 FluidNC CNC 雕刻机，查看状态、点动轴、运行 G-code、管理 SD 文件、备份配置并创建宏。(★0 · 2026-03)

### 音频、灯光与生物信号（MCP）

- [roomi-fields/osc-bridge](https://github.com/roomi-fields/osc-bridge) - 面向数百款硬件合成器的 OSC ↔ MIDI / SysEx 桥，附带配套 Skill。(★7 · 2026-08)
- [NeuroSkill-com/skill](https://github.com/NeuroSkill-com/skill) - 支持 20+ 种脑电设备（Emotiv、OpenBCI、Muse）的桌面脑机接口应用，带 Agent Skill。(official · ★101 · 2026-09)
- [enkhbold470/bci-mcp](https://github.com/enkhbold470/bci-mcp) - 通过 BrainFlow 与 LSL 获取 OpenBCI / Muse 的实时脑电状态。(★17 · 2026-09)
- [kieranklaassen/farmbot-agent-cli-mcp](https://github.com/kieranklaassen/farmbot-agent-cli-mcp) - 通过 MQTT / CeleryScript RPC 控制 FarmBot 硬件。(★3 · 2026-05)
- [tamengual/neptune-apex-mcp](https://github.com/tamengual/neptune-apex-mcp) - Neptune Apex 水族箱控制器：探头、插座、喂食、程序编辑。(★2 · 2026-03)
- [prmichaelsen/dmx-mcp](https://github.com/prmichaelsen/dmx-mcp) - 通过 OLA 与 Enttec USB 适配器控制 DMX 灯光。(★0 · 2026-03)
- [jamiew/digitakt-digitone-mcp](https://github.com/jamiew/digitakt-digitone-mcp) - 通过 MIDI 控制 Elektron Digitakt / Digitone，各 43 个工具。(★0 · 2026-07)
- [anteriovieira/osc-mcp-server](https://github.com/anteriovieira/osc-mcp-server) - MCP server，经 OSC 控制 Behringer X32 与 Midas M32 数字调音台，覆盖推子、静音、声像、四段 EQ、门限、压缩器与辅助发送。(★12 · 2025-12)
- [elisha-rudenkov/x32-mcp-server](https://github.com/elisha-rudenkov/x32-mcp-server) - X32 OSC MCP server 的扩展重写版，让 LLM 在 Behringer X32 上审查场景、追踪信号流、修复路由、调整 EQ、切换效果器并抓取电平表，已在 X32 固件 4.13 实机测试，M32 等型号预计兼容但未测试。(★3 · 2026-07)
- [wramsdell/ETC_Eos_OSC_MCP](https://github.com/wramsdell/ETC_Eos_OSC_MCP) - Python 编写的 MCP server，经 OSC 控制 ETC Eos 系列灯光控制台，用于配接、创建 Cue、效果、调色板与盲编。(★1 · 2025-12)
- [film42/wled-mcp](https://github.com/film42/wled-mcp) - Rust 编写的 MCP server，通过 mDNS 发现 WLED LED 控制器并管理其状态、预设、效果与定时，可选 OAuth。(★4 · 2026-04)
- [feamster/digitakt-midi-mcp](https://github.com/feamster/digitakt-midi-mcp) - MCP server，经 MIDI 控制 Elektron Digitakt II，可触发音轨、通过 CC/NRPN 调节参数并控制走带和 Pattern。(★8 · 2026-07)
- [Turik1/morningstar-midi-mcp](https://github.com/Turik1/morningstar-midi-mcp) - MCP server，根据自然语言经 USB 为 Morningstar MIDI 脚踏控制器编程，借助 545+ 个 OpenMIDI 设备配置并进行冲突检测。(★1 · 2026-03)
- [daredoole/evoburrow-mcp](https://github.com/daredoole/evoburrow-mcp) - 非官方 MCP server，面向 A1 Evo AcoustiX、REW 与 Audyssey 校准，可执行受保护的测量，并对 Denon/Marantz AV 功放做白名单内的局域网修改（含备份与校验）。(★4 · 2026-09)
- [amineutron/denon-mcp](https://github.com/amineutron/denon-mcp) - 面向 Denon AVR 家庭影院功放的 MCP server，经局域网 telnet 控制协议管理电源、音量、静音、输入源切换与状态，已在 AVR-X1700H 上测试。(★0 · 2026-09)

### 航天与地面站（MCP）

- [alti3/stk-mcp](https://github.com/alti3/stk-mcp) - 驱动 Ansys STK Desktop 与 Engine：场景、卫星、可见性分析。(★42 · 2026-01)
- [dsi012/mcp-server-cFS](https://github.com/dsi012/mcp-server-cFS) - 用自然语言控制 NASA core Flight System 软件总线。(★1 · 2025-10)
- [Pranav-d33/gnuradio-mcp-server](https://github.com/Pranav-d33/gnuradio-mcp-server) - 构建并运行 GNU Radio 流图。(★1 · 2026-06)
- [harris-mohamed/satnogs-mcp](https://github.com/harris-mohamed/satnogs-mcp) - SatNOGS 卫星地面站网络。(★0 · 2026-04)
- [mgrandau/telescope-mcp](https://github.com/mgrandau/telescope-mcp) - 面向 AI 操作望远镜的 MCP server 与 Web 仪表盘，可发现相机、采集图像、指向目标并管理观测会话，每个硬件组件都有仿真数字孪生。(★1 · 2026-04)

### 船舶、航空与铁路（MCP）

- [VesselSense/signalk-mcp-server](https://github.com/VesselSense/signalk-mcp-server) - 把 SignalK server 作为 MCP：船舶状态、AIS 与源自 NMEA 的数据路径。(★11 · 2025-11)
- [cyanheads/noaa-marine-mcp-server](https://github.com/cyanheads/noaa-marine-mcp-server) - NOAA 潮汐站与 NDBC 浮标的硬件数据源。(★1 · 2026-09)
- [HO44-PROJECT/MrJ-JMRI-MCP](https://github.com/HO44-PROJECT/MrJ-JMRI-MCP) - 面向 DCC 模型铁路的 JMRI：道岔、调速器、进路。(★1 · 2026-08)
- [pipeworx-io/mcp-opensky](https://github.com/pipeworx-io/mcp-opensky) - 通过 OpenSky Network 追踪 ADS-B 航空器。(★0 · 2026-09)
- [deanjbrown/geotab-mcp](https://github.com/deanjbrown/geotab-mcp) - MyGeotab 车队远程信息：设备状态、故障、行驶记录仪文件、油耗。(★0 · 2026-09)
- [dirkhh/adsb-mcp-server](https://github.com/dirkhh/adsb-mcp-server) - MCP server，开放 ADS-B 接收站的实时飞机位置、呼号与高度、接收机统计和覆盖范围数据，并支持按呼号或 hex 码搜索飞机。(★9 · 2025-11)
- [sailingnaturali/signalk-mcp](https://github.com/sailingnaturali/signalk-mcp) - MCP server，封装 SignalK 船载数据服务器，把传感器路径、当前航线、电池组以及含龙骨下余量的水深暴露为智能体工具。(★1 · 2026-08)

### 半导体与科学仪器（MCP）

- [vibeic/vibe-ic](https://github.com/vibeic/vibe-ic) - AI 原生的芯片设计插件，通过 MCP-EDA 打通从意图到验证后硅片的路径。(★26 · 2026-09)
- [Jacky1-Jiang/EPICS-MCP-Server](https://github.com/Jacky1-Jiang/EPICS-MCP-Server) - EPICS 过程变量读写——大多数加速器与大型望远镜背后的控制系统。(★4 · stale since 2025-05)
- [seikaikyo/secsgem-mcp-server](https://github.com/seikaikyo/secsgem-mcp-server) - SECS/GEM 半导体设备控制。(★1 · 2026-09)
- [BCDA-APS/bait_mcp](https://github.com/BCDA-APS/bait_mcp) - 通过 Bluesky 队列服务控制先进光子源（APS）光束线。(official · ★1 · 2026-09)
- [Oekalegon/indi-mcp](https://github.com/Oekalegon/indi-mcp) - 在树莓派上通过 INDI 控制天文摄影赤道仪与相机。(★0 · 2026-09)

### 专业 AV、门禁与标牌（MCP）

- [Z-bit-Systems-LLC/OSDP-Embedded](https://github.com/Z-bit-Systems-LLC/OSDP-Embedded) - 其中的 `osdp-mcp` 暴露一个虚拟 OSDP 外设，让 Agent 充当读卡器去测试真实的门禁控制器——物理安防领域里的硬件在环模式。(★5 · 2026-08)
- [reowens/qsys-tools](https://github.com/reowens/qsys-tools) - 通过 QRC 控制 QSC Q-SYS，提供 CLI、TypeScript 客户端与 MCP server，已在真实 Core 上测试。(★3 · 2026-07)
- [DaScheife/Sklera-Digital-Signage-MCP-Server](https://github.com/DaScheife/Sklera-Digital-Signage-MCP-Server) - Sklera 数字标牌屏幕。(★2 · 2026-06)
- [tkrisztian95/eink-mcp-server](https://github.com/tkrisztian95/eink-mcp-server) - 在微雪墨水屏上绘制仪表盘或原始像素。(★0 · 2026-04)
- [guycochran/atem-mcp-server](https://github.com/guycochran/atem-mcp-server) - MCP server，用自然语言控制 Blackmagic ATEM 视频切换台，切换与转场信号源、运行宏并启动推流和录制，支持 stdio 或 OAuth 保护的 HTTP。(★7 · 2026-09)
- [Desluca/crestron-mcp](https://github.com/Desluca/crestron-mcp) - 基于 Crestron Home REST API 的 Python MCP server，可发现房间与设备，控制遮阳、场景和温控器，读取传感器，并通过模糊匹配解析设备名；灯光可列出但没有专门的控制工具。(★4 · 2025-10)
- [SolutionAVAutomation/mcp-for-crestron-client](https://github.com/SolutionAVAutomation/mcp-for-crestron-client) - MCP for Crestron 的免费客户端部分，经 TLS 文本协议把运行 MCP for Crestron 模块的 Crestron 4-Series 处理器暴露为 MCP 工具，以 Claude Desktop .mcpb 和 npm 包发布。(★0 · 2026-08)

### 医疗与零售设备（MCP）

- [ChristianHinge/dicom-mcp](https://github.com/ChristianHinge/dicom-mcp) - 对 PACS 归档与 DICOM 影像设备执行查询、读取与 C-MOVE。(★100 · 2026-09)
- [Kovinda/mirth_connect_mcp](https://github.com/Kovinda/mirth_connect_mcp) - Mirth Connect——医院用来串接各类设备的 HL7 接口引擎。(★5 · 2026-02)
- [NyxToolsDev/dicom-hl7-mcp-server](https://github.com/NyxToolsDev/dicom-hl7-mcp-server) - 集成 DICOM 与 HL7 的互操作。(★4 · 2026-07)
- [bhandzo/mcposprint](https://github.com/bhandzo/mcposprint) - 通过 USB 向 ESC/POS 小票打印机打印。(★1 · 2026-03)
- [gian-reto/print-blocks](https://github.com/gian-reto/print-blocks) - 通过 HTTP 或 MCP 进行 ESC/POS 热敏打印。(★1 · 2026-09)

## Agent 协议与端侧运行时

在模型与设备之间，除了宿主侧 MCP server 之外还有什么：线协议、跑在单片机或 SBC 上的 Agent 循环，以及机器人 / 家居 Agent 框架。

### 协议与传输

A2A（Agent2Agent）发布十七个月后仍没有任何真正的硬件实现：官方示例和所有 A2A 目录中物理 Agent 的数量都是零，机器人领域最终选择了 MCP 加 Skill。下面列出的是实际存在的东西。

- [mqtt-ai/mcp-over-mqtt](https://github.com/mqtt-ai/mcp-over-mqtt) - MCP-over-MQTT 规范：由 broker 负责发现、负载均衡与 topic 访问控制；EMQX 提供 [TypeScript](https://github.com/emqx/mcp-typescript-sdk) 与 Python SDK 以及 broker 插件。唯一一个同时具备规范、SDK 与厂商固件的 MCP 替代传输。(★12 · 2026-01)
- [arm/device-connect](https://github.com/arm/device-connect) - Arm 的开放协议，让 Agent 通过网络发现、调用与编排设备和机器人。(official · ★95 · 2026-09)
- [device-context-protocol/dcp](https://github.com/device-context-protocol/dcp) - "Device Context Protocol"：小于 50 字节的 CBOR 帧，在 ESP32 上仅占 27.6 KB 闪存与 0.6 KB 内存，带能力范围清单、HMAC、试运行，并提供 DCP ↔ MCP 桥。(★57 · 2026-05)
- [macc-n/wot-mcp](https://github.com/macc-n/wot-mcp) - W3C 物联网（Web of Things）Thing Description → MCP：属性变成读写工具、动作变成工具、事件变成资源，支持 HTTP / CoAP / MQTT。(★9 · 2026-02)
- [w3c-cg/webagents](https://github.com/w3c-cg/webagents) - W3C"Web 上的自主 Agent"社区组：基于 WoT 与关联数据的超媒体多 Agent 系统。(★47 · 2026-08)
- [agenticros/agenticros](https://github.com/agenticros/agenticros) - 面向 OpenClaw、Claude Code、Codex 与 Gemini 的 ROS 2 插件：机器人暴露带类型的能力动词（`drive_base`、`find_object`），其清单的形状刻意设计成可兼作 ACP / A2A agent card；真正在线上跑 A2A 仍在路线图上。(★149 · 2026-09)
- [win4r/openclaw-a2a-gateway](https://github.com/win4r/openclaw-a2a-gateway) - 实现 A2A v0.3 的 OpenClaw 插件（JSON-RPC / REST / gRPC、mDNS、agent card）；纯软件，但天然适合作为 agenticros 的前端。(★555 · 2026-07)
- [strands-labs/robots](https://github.com/strands-labs/robots) - 通过 Strands Agents 用自然语言控制 70+ 种机器人；机器人以 Zenoh 对等节点组网，并通过 AWS IoT Core 桥接机队。(★159 · 2026-09)
- [agntcy/slim](https://github.com/agntcy/slim) - AGNTCY 的安全低延迟交互消息（SLIM）；配合 `slim-a2a-*` 与 A2A 自己的 SLIM-RPC 扩展，是 A2A 唯一的低延迟传输绑定。(★219 · 2026-09)
- [QUSD-ai/m5stick-nanda](https://github.com/QUSD-ai/m5stick-nanda) - M5StickC Plus 2 的 ESP32 固件，直接在设备上提供 agent card 与 JSON-RPC；但它是按关键词匹配而非按协议方法分发，而且发布当天就被弃置。收录它，是因为这是现存最接近"A2A 跑在硬件上"的东西。(★0 · 2026-01)
- [r1marcus/TinyA2A](https://github.com/r1marcus/TinyA2A) - 面向 STM32 与 ESP-IDF 的 C11 Agent 意图库，带 MQTT JSON 与 64 字节 CAN-FD 帧两种 profile。与 Linux 基金会的 A2A 同名，但线格式并不相同。(★2 · 2026-05)
- [kushalsinha/openmhp](https://github.com/kushalsinha/openmhp) - Open Model Hardware Protocol，一套类 MCP 的协议规范与 Python 参考实现，让 Agent 发现实验室仪器、机器人和工业设备，并通过租约、遥测事件流和设备侧安全检查执行长时任务。(★0 · 2026-09)

### 端侧 Agent 运行时

直接运行在单片机或 SBC 上、带工具调用能力的 Agent 循环，而非跑在宿主机上。

- [espressif/esp-claw](https://github.com/espressif/esp-claw) - ESP32-S3 / P4 / C5 上的 Agent 运行时：能力用 C 写、Skill 用 Lua 写，双向 MCP，事件路由。(official · ★2.2k · 2026-09)
- [memovai/mimiclaw](https://github.com/memovai/mimiclaw) - 无操作系统、C / ESP-IDF 实现，跑在 ESP32-S3 上：Anthropic 工具调用 ReAct 循环、Telegram、本地记忆。MCU 版 claw 家族的领头羊。(★5.8k · 2026-08)
- [sipeed/picoclaw](https://github.com/sipeed/picoclaw) - 内存占用不到 10 MB 的单个 Go 二进制，面向 LicheeRV-Nano / MaixCAM / Pi Zero，带完整的 MCP 与 Skill 循环。(official · ★30k · 2026-09)
- [zeroclaw-labs/zeroclaw](https://github.com/zeroclaw-labs/zeroclaw) - 面向树莓派级 SBC 的 Rust 重写版（3.4 MB）；[nullclaw](https://github.com/nullclaw/nullclaw)（Zig，678 KB）额外提供树莓派 GPIO 与 STM32 / Nucleo 外设工具。(★32.8k · 2026-09)
- [M64GitHub/WireClaw](https://github.com/M64GitHub/WireClaw) - 基于 Arduino / PlatformIO，跑在 ESP32-C3 / C6 / S3 上：大模型调用 `gpio_write` 与 `rule_create` 实现离线自动化；支持 Telegram、串口、NATS；带网页烧录器。(★188 · 2026-02)
- [jetpax/pycoclaw](https://github.com/jetpax/pycoclaw) - 跑在 ESP32-S3 / P4 / C6 上的 MicroPython 实现，支持递归工具调用、MCP 客户端与 GPIO / I2C / CAN 工具；Agent 核心尚未公开。(★164 · 2026-04)
- [wireless-tag-com/EmbedClaw](https://github.com/wireless-tag-com/EmbedClaw) - 启明云端的 C / ESP-IDF 实现，跑在 ESP32-S3 上，带 JSON-schema 工具注册表与 ReAct 循环，适配通义千问 / DeepSeek / 豆包 / Kimi；首个模组厂商分支。(official · ★45 · 2026-04)
- [laurenvil/Uno-QClaw](https://github.com/laurenvil/Uno-QClaw) - 跑在 Arduino UNO Q 上的 picoclaw 分支，本地运行 Qwen3.5-0.8B：能自己写代码、编译并通过 OpenOCD 烧录自己的 MCU，带摄像头与 I2C 扫描，完全离线。(★19 · 2026-06)
- [hrwtech/openclaw-esp32](https://github.com/hrwtech/openclaw-esp32) - 把 OpenClaw 的 Agent 循环移植到 ESP32 板上；OpenClaw 本身不附带任何硬件 Skill。(★10 · 2026-02)
- [espressif/esp-brookesia](https://github.com/espressif/esp-brookesia) - AIoT 人机界面框架，其 Agent 管理器为扣子、OpenAI 与小智提供 Function Calling 与 MCP 适配。(official · ★789 · 2026-09)
- [tuya/TuyaOpen](https://github.com/tuya/TuyaOpen) - 面向 T2 / T3 / T5AI 与 ESP32 的 C SDK，带端侧推理引擎；Agent 的"大脑"仍在涂鸦云端 Agent Hub。(official · ★1.8k · 2026-09)
- [XiaoMi/xiaomi-miloco](https://github.com/XiaoMi/xiaomi-miloco) - 基于 MiMo 的 OpenClaw 插件：家庭摄像头感知驱动米家设备控制；需要 4 GB 以上内存的主机，而非单片机。(official · ★3.4k · 2026-09)
- [NVIDIA-AI-IOT/jetson-ai-lab](https://github.com/NVIDIA-AI-IOT/jetson-ai-lab) - 在 Jetson 上运行 OpenClaw 的官方路径：Orin Nano 用 Ollama，AGX / Thor 用 vLLM。(official · ★207 · 2026-09)
- [HeyWillow/willow](https://github.com/HeyWillow/willow) - ESP32-S3 语音设备固件，把音频流式发送到服务器由服务器执行工具；与 esp-ai、ElatoAI 一样，端侧没有 Agent 循环。(★3.1k · 2026-09)
- [tnm/zclaw](https://github.com/tnm/zclaw) - 运行在 ESP32 上的 C 语言 AI 助手固件，整体固件预算不超过 888 KiB，支持 GPIO 控制、定时任务、持久记忆和用自然语言组合的自定义工具。(★2.2k · 2026-05)
- [nullclaw/nullclaw](https://github.com/nullclaw/nullclaw) - 用 Zig 编写的自主助手运行时，678 KB 静态二进制、约 1 MB 内存，提供串口、Arduino、Raspberry Pi GPIO 和 STM32/Nucleo 外设接口并支持 MCP。(★8.1k · 2026-07)
- [atiti/espclaw](https://github.com/atiti/espclaw) - ESP32 原生 Agent 运行时，带 LLM 工具循环、本地 GPIO/I2C/PWM/摄像头工具、可热替换的 Lua 应用、OTA，以及 Web、UART 或 Telegram 控制入口。(★8 · 2026-03)
- [xinnan-tech/xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server) - 为 xiaozhi-esp32 语音设备提供的自托管 Python/Java 后端，支持 MQTT+UDP 与 WebSocket 协议、MCP 接入点、声纹识别和知识库。(★10.6k · 2026-09)
- [huangjunsen0406/py-xiaozhi](https://github.com/huangjunsen0406/py-xiaozhi) - 面向桌面和 Raspberry Pi、RDK、Jetson Nano 等 ARM 板的 Python 版 xiaozhi 客户端，支持实时语音、视觉、MCP 工具服务、离线唤醒词和 GPIO 控制。(★3.5k · 2026-09)
- [akdeb/ElatoAI](https://github.com/akdeb/ElatoAI) - 通过安全 WebSocket 和 Deno 边缘函数为 Arduino ESP32 设备提供实时语音 AI，支持 OpenAI Realtime、Gemini Live、xAI Grok、ElevenLabs、Hume 和 Boson 管线；本地模型支持在独立的 local-ai-toys 仓库中。(★2k · 2026-09)
- [livekit/client-sdk-esp32](https://github.com/livekit/client-sdk-esp32) - LiveKit 官方 ESP32-S3/ESP32-P4 SDK，传输音频、视频和数据，让设备与云端 LiveKit Agents 交互，并支持 RPC。(official · ★150 · 2026-09)
- [second-state/echokit_server](https://github.com/second-state/echokit_server) - 为 EchoKit ESP32 设备提供的语音 Agent 服务端，可对接任意 OpenAI 兼容端点运行 ASR、LLM、TTS 管线并调用 MCP 服务器，固件在 echokit_box 仓库。(★592 · 2026-02)
- [m5stack/StackChan](https://github.com/m5stack/StackChan) - M5Stack 基于 CoreS3 的 StackChan 桌面机器人（舵机、RGB LED、摄像头、传感器）的开源固件、遥控器固件、手机 App 与服务端，其出厂固件内置 AI Agent。(official · ★1.3k · 2026-08)

### 机器人与具身 Agent 框架

- [dimensionalOS/dimos](https://github.com/dimensionalOS/dimos) - 面向物理空间的 Agent 操作系统：用自然语言指挥人形机器人、宇树四足、xArm 与 MAVLink 无人机。(★4.5k · 2026-09)
- [ros-claw/rosclaw](https://github.com/ros-claw/rosclaw) - "可信的物理执行运行时"：失效即关闭的策略、执行回执、MCP 工具发现、安全包络、ROS 2；alpha 阶段，已在 UR5e 仿真中验证。(★199 · 2026-09)
- [Grigorij-Dudnik/RoboCrew](https://github.com/Grigorij-Dudnik/RoboCrew) - `pip install robocrew`：带运动工具、VLA 策略与传感器扫描的大模型 Agent；XLeRobot 演示。(★139 · 2026-09)
- [Hugging Face LeRobot](https://github.com/huggingface/lerobot) - 端到端的机器人学习：数据集、ACT / Diffusion / VLA 策略，SO-100 / 101、Koch 与 LeKiwi 的驱动；附带面向 Agent 的 `AGENT_GUIDE.md`。(★27.6k · 2026-09)
- [isaac-sim/IsaacLab](https://github.com/isaac-sim/IsaacLab) - 基于 Isaac Sim 的统一机器人学习框架：强化学习、模仿学习、仿真到现实迁移。(★8.2k · 2026-09)
- [NVIDIA/Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T) - 面向通用人形机器人的 GR00T 基础模型，带微调与推理栈以及一份 `AGENTS.md`。(★8.1k · 2026-08)
- [openvla/openvla](https://github.com/openvla/openvla) - 用于操作任务的 7B 开源视觉-语言-动作模型；VLA 的参考实现，现已冻结。(★7k · stale since 2025-03)
- [nasa-jpl/rosa](https://github.com/nasa-jpl/rosa) - 用自然语言检视、诊断并操作 ROS 1 / 2 机器人的 LangChain Agent。(★1.6k · 2026-03)
- [FlagOpen/RoboOS](https://github.com/FlagOpen/RoboOS) - 智源研究院的"大脑–小脑"具身操作系统：RoboBrain 多模态大模型、Skill 库与多机器人共享记忆。(official · ★623 · 2025-12)
- [automatika-robotics/embodied-agents](https://github.com/automatika-robotics/embodied-agents) - ROS 2 原生框架，用于构建带 LLM / VLM 组件的交互式物理 Agent。(★68 · 2026-09)
- [RobotecAI/rai](https://github.com/RobotecAI/rai) - 面向 ROS 2 机器人的厂商无关 Agent 框架，包含多 Agent 核心、基于 URDF 和文档的本体自描述、ASR/TTS、感知、仿真连接器以及 rai_bench 评测套件。(★589 · 2026-09)
- [OpenMind/OM1](https://github.com/OpenMind/OM1) - 用于人形、四足、TurtleBot 4 及 Gazebo/Isaac Sim 的模块化 Go 多模态 Agent 运行时，通过 ROS 2、Zenoh 和 CycloneDDS 插件接入硬件。(★2.9k · 2026-09)
- [fujitatomoya/ros2ai](https://github.com/fujitatomoya/ros2ai) - ROS 2 命令行扩展，借助 OpenAI 或 Ollama 模型回答问题并执行 ros2 命令，支持 Humble 到 Rolling，其中 Jazzy、Kilted、Rolling 可通过 apt 安装。(★330 · 2026-08)
- [ROSClaw/rosclaw](https://github.com/ROSClaw/rosclaw) - ROSClaw 的工作区引导仓库，通过机器人侧 ROS 2 包、OpenClaw 插件和可选 WebRTC 信令，把 OpenClaw Agent 运行时接到 ROS 2 机器人。(★6 · 2026-03)
- [bob-ros2/bob_llm](https://github.com/bob-ros2/bob_llm) - ROS 2 节点，把任意 OpenAI 兼容 LLM 变成机器人 Agent，管理会话状态并通过可动态加载的工具调用机器人功能。(★3 · 2026-06)

### 智能家居与设备平台

- [Home Assistant LLM API](https://developers.home-assistant.io/docs/core/llm/) - 官方的 Assist LLM API：各集成注册的工具可被任意对话 Agent 调用。(official)
- [acon96/home-llm](https://github.com/acon96/home-llm) - Home Assistant 集成，外加为设备控制微调的本地模型。(★1.4k · 2026-09)
- [arm/mcp](https://github.com/arm/mcp) - Arm 官方 MCP：文档检索、迁移分析、汇编性能分析。Nordic、Microchip、Silicon Labs、TI 与 ADI 也发布过类似的纯文档型厂商 MCP。(official · ★91 · 2026-09)
- [Google Home MCP](https://developers.home.google.com/mcp/home) - Google 官方抢先体验版 Home MCP 服务器为 MCP Agent 提供五个工具，可列出家庭和设备、读取状态与历史并对 Google Home 设备执行操作，面向 Google Home Premium Advanced 订阅用户。
- [thingsboard/thingsboard-mcp](https://github.com/thingsboard/thingsboard-mcp) - ThingsBoard 官方 MCP 服务器，以 Docker 镜像发布，让 Agent 在 ThingsBoard Cloud、自托管或 Edge 实例上查询设备、管理实体和分析遥测数据。(official · ★98 · 2026-03)
- [nRF Cloud MCP server](https://docs.nrfcloud.com/docs/platform/mcp-server) - Nordic 托管的只读 nRF Cloud MCP 服务器，通过 OAuth 提供设备群元数据、遥测、健康指标、重启历史和崩溃追踪。

## 验证基础设施

用来运行硬件 Skill `evals/` 的工具。模拟器与托管虚拟板用于迭代和预检——它们都无法让一个 Skill 通过，因为通过需要真实的板子。驱动真实板子的设备农场是例外：在上面跑的结果算数。

### 模拟器与仿真器

- [wokwi/wokwi-cli](https://github.com/wokwi/wokwi-cli) - ESP32 全系列、AVR、RP2040、nRF52、部分 STM32，外加传感器与显示屏。YAML 场景可断言串口文本并设置引脚；提供 GitHub Action；开源项目可免费获得 CI 令牌。仿真核心是托管且闭源的。本仓库 `L1 (wokwi)` 预检的后端。(★66 · 2026-09)
- [renode/renode](https://github.com/renode/renode) - Cortex-M / A / R、RISC-V、Xtensa，整板与多节点网络；`.resc` 脚本、Robot Framework 测试框架、Zephyr twister 集成，确定性执行。MIT 许可。断言层已经存在——`renode-test` 以 `Wait For Line On Uart` 这类关键字驱动 Robot Framework——但还没有东西替 Agent 封装一个活的会话。本仓库 `L1 (renode)` 预检的后端。(★2.9k · 2026-09)
- [qemu/qemu](https://github.com/qemu/qemu) - ARM `mps2` 等机型、RISC-V、x86；[乐鑫的分支](https://github.com/espressif/qemu)增加了 Xtensa / ESP32。提供 QMP JSON API 与 GDB 桩。文献中被用于 FreeRTOS 的模糊测试与修补循环。(★13.7k · 2026-09)
- [Zephyr native_sim](https://docs.zephyrproject.org/latest/boards/native/native_sim/doc/index.html) - 把任意 Zephyr 应用构建成宿主机上的 Linux 可执行文件，带仿真的 I2C / SPI / GPIO 与 BabbleSim BLE；`twister -p native_sim`。Zephyr 类 Skill 最便宜的 L1 方案。(official)
- [gazebosim/gz-sim](https://github.com/gazebosim/gz-sim) - 带 ROS 2 桥与传感器的机器人世界；`gz sim -s -r world.sdf` 可无头运行。(★1.5k · 2026-09)
- [google-deepmind/mujoco](https://github.com/google-deepmind/mujoco) - 带 Python 绑定与 MJX GPU 版本的多体动力学引擎；LIBERO 与大多数 VLA 评测的底座。(★15.2k · 2026-09)
- [isaac-sim/IsaacSim](https://github.com/isaac-sim/IsaacSim) - 照片级真实感的机器人仿真；支持 `--headless` 与 Python 独立脚本；5.0 起开源，需要 RTX 显卡。适合每晚跑，而不适合每个 PR 都跑。(★4.1k · 2026-09)
- [cyberbotics/webots](https://github.com/cyberbotics/webots) - 带 ROS 2 桥的机器人仿真；`webots --batch --no-rendering`。(★4.6k · 2026-09)
- [mani-skill/ManiSkill](https://github.com/mani-skill/ManiSkill) - 基于 SAPIEN、离屏 Vulkan 渲染的 GPU 并行操作任务仿真；本身也是一个评测基准。(★3.3k · 2026-08)
- [pymodbus-dev/pymodbus](https://github.com/pymodbus-dev/pymodbus) - `pymodbus.simulator` 根据 JSON 寄存器定义提供一个 Modbus TCP / RTU 设备，并带 HTTP 控制 API。本仓库 `L1 (modbus-sim)` 预检的后端。(★2.8k · 2026-09)
- [open62541/open62541](https://github.com/open62541/open62541) - OPC UA 服务端 / 客户端；其示例服务器可以充当可用的 PLC 替身。(★3.2k · 2026-09)
- [Home Assistant 演示模式](https://www.home-assistant.io/integrations/demo/) - `hass --demo-mode` 在真实的 REST / WebSocket API 背后创建虚拟的灯、空调与传感器。本仓库 `L1 (ha-demo)` 预检的后端。(official)
- [micropython/micropython unix 移植](https://github.com/micropython/micropython/tree/master/ports/unix) - 宿主机上的 MicroPython 虚拟机；只能做逻辑层检查，没有外设。(★22.1k · 2026-09)
- [ARM-software/AVH](https://github.com/ARM-software/AVH) - Arm 虚拟硬件：Cortex-M FVP（Corstone-300 / 310 / 315），附 GitHub Actions 示例；对开源与评估用途免费。(official · ★54 · 2026-09)
- [davidmonterocrespo24/velxio](https://github.com/davidmonterocrespo24/velxio) - 开源浏览器端开发板模拟器，覆盖 AVR、RP2040/RP2350、STM32、ESP32 Xtensa/RISC-V 和 Raspberry Pi Linux 开发板，含 150 多个元件和 MCP 服务器；Docker 自托管镜像只包含 Arduino、Pico 和 ESP32 系列，CI 命令行工具单独发布为 velxio/velxio-cli。(★2.9k · 2026-09)
- [wokwi/rp2040js](https://github.com/wokwi/rp2040js) - 用 JavaScript 编写的 Raspberry Pi Pico RP2040 模拟器，可在 Node.js 或浏览器中运行 Arduino 代码和 MicroPython REPL。(★526 · 2026-09)
- [wokwi/avr8js](https://github.com/wokwi/avr8js) - 用 JavaScript 实现 AVR 8 位架构的库，可运行于浏览器和 Node.js，是 Wokwi Arduino 模拟器的核心。(★845 · 2026-08)
- [buserror/simavr](https://github.com/buserror/simavr) - 精简的 AVR 模拟器，支持 Linux 和 macOS、GDB 调试和 VCD 波形输出，可无界面运行以在 CI 中测试 Arduino 级固件。(★1.8k · 2026-09)
- [lcgamboa/picsimlab](https://github.com/lcgamboa/picsimlab) - 实时模拟 PIC、AVR、STM32 和 ESP32 开发板的仿真器，带 LED、显示屏、W5500 以太网等外设件，并集成 MPLAB X 和 avr-gdb 调试。(★667 · 2026-09)
- [verilator/verilator](https://github.com/verilator/verilator) - 高速开源 Verilog/SystemVerilog 仿真器与 lint 工具，把 RTL 编译为多线程 C++ 或 SystemC，被 AgentDV 等 Agent RTL 基准和 cocotb 测试用作仿真后端。(★3.9k · 2026-09)
- [cocotb/cocotb](https://github.com/cocotb/cocotb) - 基于 Python 协程的 RTL 验证测试框架，可用 pytest 风格测试驱动 Verilator、Icarus、GHDL 及商业仿真器。(★2.5k · 2026-09)
- [Genesis-Embodied-AI/genesis-world](https://github.com/Genesis-Embodied-AI/genesis-world) - Genesis World 机器人物理仿真平台，集成刚体、FEM、MPM、粒子求解器和机器人渲染器，通过 Python API 导入 URDF/MJCF/USD。(★30k · 2026-09)
- [newton-physics/newton](https://github.com/newton-physics/newton) - Linux Foundation 旗下面向机器人的 GPU 物理引擎，基于 NVIDIA Warp、以 MuJoCo Warp 为主后端，支持 OpenUSD 和可微分。(★5.7k · 2026-09)
- [carla-simulator/carla](https://github.com/carla-simulator/carla) - 开源自动驾驶仿真器，提供传感器套件、交通场景和 Python API，用于车辆软件闭环测试。(★14.4k · 2026-09)
- [iamaisim/ProjectAirSim](https://github.com/iamaisim/ProjectAirSim) - Project AirSim：Microsoft AirSim 的继任项目，现由 IAMAI Simulations 维护，面向无人机等自主系统，提供用于控制器与 CI 快速测试的轻量运行时，以及用于摄像头、LiDAR、雷达的 Unreal Engine 5 模式。(★864 · 2026-09)
- [ArduPilot/ardupilot](https://github.com/ArduPilot/ardupilot) - ArduPilot 多旋翼、固定翼、车辆和潜航器自驾仪源码，其 SITL 构建在 PC 上运行真实飞控代码，是无人机 MCP 服务器和 Agent 论文的常用测试对象。(★15.9k · 2026-09)
- [qilingframework/qiling](https://github.com/qilingframework/qiling) - 可插桩的二进制仿真框架，支持 ARM、MIPS、RISC-V、x86 固件与系统二进制，提供多级 hook、快照和反向调试器。(★6.1k · 2026-09)

不适合 CI，列出来免得有人再查一遍：Tinkercad Circuits（无 API）、SimulIDE（仅 GUI）、Proteus VSM（商业软件，以 GUI 为中心）、Simulavr（2023 年起停止维护）。

### 虚拟硬件与设备农场

- [veecle/chiplab](https://github.com/veecle/chiplab) - 只通过 MCP 暴露的托管虚拟 STM32 与 Nordic Cortex-M 板：上传 ELF、读取串口。专为编程 Agent 打造。(★16 · 2026-09)
- [eust-w/agentic-embedded-lab](https://github.com/eust-w/agentic-embedded-lab) - Agent 原生的嵌入式实验室，带可插拔的仿真后端与基于证据的验证；最接近"以 Renode 为后端的测试框架"的东西。(★34 · 2026-09)
- [EliasOenal/term-cli](https://github.com/EliasOenal/term-cli) - 为 Agent 提供的交互式终端，专为那些无法自动确认的提示而生：带 MFA 的 SSH、GRUB 与 U-Boot 控制台、debconf。(★102 · 2026-08)
- [jumpstarter-dev/jumpstarter](https://github.com/jumpstarter-dev/jumpstarter) - 红帽支持的硬件在环框架，面向真实或虚拟目标、本地或远程，Kubernetes 原生，并明确为"人类、自动化或 Agent"三类驱动方设计；带电源、串口与烧录驱动。最适合搭建 L2 设备农场。(★220 · 2026-09)
- [labgrid-project/labgrid](https://github.com/labgrid-project/labgrid) - Pengutronix 的板卡控制库（电源、串口、USB、网络启动），集成 pytest。(★528 · 2026-09)
- [kernelci/kernelci-core](https://github.com/kernelci/kernelci-core) - 带开放 API 的社区硬件实验室；实验室由 Collabora、BayLibre 等捐赠。(★120 · 2026-09)
- [Linaro LAVA](https://gitlab.com/lava/lava) - KernelCI 与 Linaro 实验室使用的板卡农场调度器；可自建部署。(★82 · 2026-09)
- [Zephyr twister 设备测试](https://docs.zephyrproject.org/latest/develop/test/twister.html) - `twister --device-testing --hardware-map` 在连接的板子上运行测试套件；[golioth/zephyr_twister_hil_testing](https://github.com/golioth/zephyr_twister_hil_testing) 演示了如何在 GitHub 自托管 runner 上实现。(official)
- [Wokwi CI](https://docs.wokwi.com/wokwi-ci/getting-started) - 在 GitHub Actions 中运行托管仿真；开源项目可免费获得令牌。(official)
- [OpenHiL](https://openhil.github.io/) - 开源硬件在环工具的社区中心。
- [agentic-hil/agentic-hil](https://github.com/agentic-hil/agentic-hil) - Python 包、MCP 服务器和 Agent Skill，让 Claude Code、Codex 或 OpenCode 通过 OpenOCD、pyOCD 或 STM32CubeProgrammer 在真实开发板上烧录并测试固件，支持 UART/CAN 校验、YAML 测试计划和审计日志。(★13 · 2026-09)
- [espressif/pytest-embedded](https://github.com/espressif/pytest-embedded) - Espressif 官方嵌入式测试 pytest 插件，提供串口 DUT、ESP-IDF、Arduino、NuttX、JTAG、QEMU 与 Wokwi 目标等服务。(official · ★155 · 2026-09)
- [Rahix/tbot](https://github.com/Rahix/tbot) - 面向嵌入式 Linux 的 Python 自动化与测试工具，编排串口控制台、SSH 主机和开发板电源，在 CI 中对真实硬件跑测试。(★101 · 2026-09)
- [everypinio/hardpy](https://github.com/everypinio/hardpy) - 可用 pip 安装的 Python 库，基于 pytest 搭建设备测试台，提供浏览器操作界面，结果存入 CouchDB、JSON 或 StandCloud。(★76 · 2026-06)
- [lgirdk/boardfarm](https://github.com/lgirdk/boardfarm) - 源自 Qualcomm 的 Python 测试自动化框架，用于在板卡农场中烧录并测试 OpenWrt/RDK-B 路由器和 IoT 设备。(★32 · 2026-09)

## 评测基准

只有前两个在真实单片机上发布过结果；其余要么只查编译，要么只跑仿真。

- [iot-agent/iot-skillsbench](https://github.com/iot-agent/iot-skillsbench) - 在 ATmega2560 / Arduino、ESP32-S3 / ESP-IDF 与 nRF52840 / Zephyr 上的 42 个硬件在环任务，覆盖 23 种外设、3 个难度等级；在真实板子上对比"不用 Skill、LLM 生成的 Skill、专家编写的 Skill"三种情况。其 30 个专家 Skill 是带 frontmatter 的单文件 `.md`，可轻松转换为 SKILL.md。论文：[arXiv 2603.19583](https://arxiv.org/abs/2603.19583)。(★41 · 2026-07)
- [ubicomplab/embedded-arena](https://github.com/ubicomplab/embedded-arena) - 硬件在环竞技场：Agent 修改模型与固件，测试框架负责编译、烧录，并对可部署性、电流、能耗与温度打分。前沿模型在没有硬件反馈时得分为 0%，有了反馈则三轮内即可成功。论文：[arXiv 2606.16190](https://arxiv.org/abs/2606.16190)。(★12 · 2026-07)
- [cezman/ironharness](https://github.com/cezman/ironharness) - 固件 Agent 的 pass@k 基准，可跑在 Wokwi、Renode 或真实硬件上，外面套一层沙箱化的 MCP I/O 框架。非常早期。(★2 · 2026-09)
- [EmbedBench / EmbedAgent](https://arxiv.org/abs/2506.11003) - 在 Uno / ESP32 / Pico 上覆盖 9 类元件的 126 个用例，分程序员、架构师与集成者三种角色；无公开仓库。
- [EmbedGenius](https://arxiv.org/abs/2412.09058) - 借助硬件感知检索生成嵌入式 IoT 软件。
- [面向嵌入式软件开发的 LLM Agent 闭环评测](https://www.sciencedirect.com/science/article/pii/S1383762126002559) - 五个嵌入式控制任务，在四种反馈机制下评测：一次性生成、自我验证、CI 红绿灯、预言机。
- [NVlabs/verilog-eval](https://github.com/NVlabs/verilog-eval) - Verilog 补全与"规格到 RTL"，用 iverilog 校验 pass@k。(★472 · stale since 2025-07)
- [hkust-zhiyao/RTLLM](https://github.com/hkust-zhiyao/RTLLM) - 自然语言 → RTL：语法、功能、PPA。(★228 · 2026-08)
- [HardSecBench](https://arxiv.org/abs/2601.13864) - 评估 LLM 生成的 RTL 与 C 固件的安全意识。
- [EmbodiedBench/EmbodiedBench](https://github.com/EmbodiedBench/EmbodiedBench) - 面向多模态具身 Agent 的 1128 个任务，覆盖 ALFRED、Habitat、导航与操作。(★342 · 2026-05)
- [StanfordVL/BEHAVIOR-1K](https://github.com/StanfordVL/BEHAVIOR-1K) - OmniGibson 中的 1000 项家务活动。(★1.7k · 2026-09)
- [Lifelong-Robot-Learning/LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO) - 130 个终身学习式操作任务；事实上的 VLA 评测标准。(★2.3k · stale since 2025-03)
- [stepjam/RLBench](https://github.com/stepjam/RLBench) - CoppeliaSim 中的 100 个操作任务。(★1.8k · stale since 2025-01)
- [holi-lab/SimuHome](https://github.com/holi-lab/SimuHome) - 基于 Matter、可加速时间的智能家居仿真器，含 600 个 episode，涵盖定时与隐含意图。ICLR 2026 口头报告。(★34 · 2026-04)
- [SMH-Bench](https://arxiv.org/abs/2606.01912) - 在最多 135 台设备的家庭中设置的 1100 个智能家居任务；代码尚未发布。
- [NVlabs/cvdp_benchmark](https://github.com/NVlabs/cvdp_benchmark) - NVIDIA 的 CVDP 评测框架，涵盖专家编写的 RTL 设计、验证与调试题，支持 Agent 与非 Agent 模式，基于 Docker 运行并配套 Hugging Face 数据集（论文报告 783 题，公开版本少 20 题）。(official · ★221 · 2026-06)
- [LGAI-Research/PCBWorld](https://github.com/LGAI-Research/PCBWorld) - 基于 KiCad 推挤布线器的 Gymnasium 环境，Agent 在真实 .kicad_pcb 板上布线并由 KiCad DRC 打分，附带 RL、LLM 工具调用和 FreeRouting 等基线。(★13 · 2026-09)
- [pengjas/posteda-bench](https://github.com/pengjas/posteda-bench) - PostEDA-Bench：145 个任务，评测 LLM Agent 在 KLayout 中修复版图 DRC 违例、在真实 OpenROAD 流程上优化 PPA，附 ReAct、ToT、Reflexion 等 Agent 基线。(★2 · 2026-07)
- [Luoji-zju/Agents4PLC_release](https://github.com/Luoji-zju/Agents4PLC_release) - 可验证的基准数据集，含 96 个从自然语言生成 IEC 61131-3 Structured Text 的任务，附 nuXmv/PLCverif 形式化规约和参考代码，来自 Agents4PLC 多 Agent PLC 研究。(★78 · 2026-08)
- [HPAI-BSC/TuRTLe](https://github.com/HPAI-BSC/TuRTLe) - 统一的评测框架和排行榜，在 VerilogEval、RTLLM 等基准上从语法、功能、综合和 PPA 维度给 LLM 的 RTL 生成打分。(★49 · 2026-07)
- [Phoenix-bench](https://arxiv.org/abs/2605.15226) - Phoenix-bench（arXiv 2026-05）：来自 114 个硬件仓库的 511 个经 Verilator 验证的修复实例，EDA 环境用 Docker 固定，显示编码 Agent 成绩比 SWE-bench Verified 低 37-58%。
- [PDAgent-Bench](https://arxiv.org/abs/2606.17253) - PDAgent-Bench（arXiv 2026-06）：353 道 VLSI 物理设计题目和面向 EDA 工具的闭环 Agent 工作流，评测 11 个模型，发现其在工具执行类任务上仍较弱（如 Innovus 脚本生成 42.2%）；代码尚待发布。
- [HSCO-Bench](https://arxiv.org/abs/2605.19399) - HSCO-Bench（arXiv 2026-05）：端到端软硬件协同设计基准，LLM Agent 生成含加速器的 SoC 并部署到 AMD VC707 FPGA，代码见 B07901087/hsco_bench。
- [CaP-X](https://arxiv.org/abs/2603.22435) - CaP-X（arXiv 2026-03）：CaP-Gym 环境与 CaP-Bench，评测编码 Agent 通过编写组合感知与控制原语的程序来操控机械臂，覆盖 12 个模型。

## 论文与文章

- [Skilled AI Agents for Embedded and IoT Systems Development](https://arxiv.org/abs/2603.19583) - 提出 IoT-SkillsBench；专家编写的 Skill 在硬件在环任务上达到接近满分的成功率，而裸模型失败。ACM AIAS 2026。
- [Every hardware MCP server I could find, and what each one actually does](https://veecle.ai/blog/hardware-mcp-servers-reviewed) - Veecle，2026-08。把 42 个 server 分为六档；其中只有三个能在没有本地硬件的情况下运行固件。
- [The chip vendors showed up: hardware MCP servers, six months later](https://veecle.ai/blog/hardware-mcp-servers-2026) - Veecle，2026-08。七家厂商的官方 MCP；没有一家支持仿真执行。
- [LLMs write good firmware. They can't prove it.](https://veecle.ai/blog/llms-write-good-firmware-cant-prove-it) - 主张投入验证基础设施而非打磨提示词——这正是本列表验证阶梯所依据的论点。
- [What the LLM-for-embedded benchmarks actually measure](https://veecle.ai/blog/what-llm-embedded-benchmarks-measure) - 对 EmbedBench 与 IoT-SkillsBench 评测指标的批判性解读。
- [Device Context Protocol: an agent protocol for constrained devices](https://arxiv.org/abs/2605.26159) - DCP 背后的论文：为什么 MCP 对单片机来说太重，以及一个 27 KB 的替代方案长什么样。
- [LAP: An Agent-to-Instrument Protocol for Autonomous Science](https://arxiv.org/abs/2606.03755) - 点出了 MCP 与 A2A 都没有建模的"Agent 到仪器"这条边，并提出仪器卡片、独占预约、安全围栏握手与带不确定度类型的测量结果。关于"为什么 Agent 间协议到达不了硬件"最有力的论述。
- [Robot Context Protocol](https://arxiv.org/abs/2506.11650) - 一种与中间件无关的机器人控制协议，把 A2A 放在客户端边缘的适配器里，而不是控制通路上。
- [Agentic IoT: a survey](https://arxiv.org/abs/2607.04219) - 关于 LLM Agent 与 IoT 设备、协议及边缘约束相遇的综述。
- [Securing LLM-Generated Embedded Firmware through AI Agent-Driven Validation and Patching](https://arxiv.org/abs/2509.09970) - 在 QEMU 上跑 FreeRTOS，结合模糊测试、静态分析与 Agent 修补的闭环。
- [Embedded Arena: Iterative Optimization via Hardware Feedback](https://arxiv.org/abs/2606.16190) - 硬件反馈让成功率在三轮内从 0% 翻转为成功。
- [SemaPLC: an agentic IDE for PLC programming](https://arxiv.org/abs/2608.18565) - 美的从规格到 PLC 程序的 Agent 流水线，带审查 Skill。
- [Toward a Modular Architecture for Embedded AI Agent Systems at the Edge](https://arxiv.org/abs/2606.02862) - 端侧 Agent 运行时的设计；可与 esp-claw 及 claw 家族对照阅读。
- [Coscientist](https://github.com/gomesgroup/coscientist) - 驱动 Opentrons 移液工作站与 Emerald Cloud Lab 的 GPT-4 Agent。Nature 2023。(★211 · stale since 2025-08)
- [Autonomous Chemistry and Materials Innovation Driven by Scientific Agents](https://pubs.acs.org/doi/10.1021/jacsau.6c00213) - 关于由 LLM 驱动的自动化实验室的综述。JACS Au 2026。
- [IoT-MCP: Bridging LLMs and IoT Systems Through Model Context Protocol](https://arxiv.org/abs/2510.01260) - IoT-MCP（arXiv 2025-09）：在 6 种 MCU、22 类传感器上部署边缘 MCP 服务器，并提出含 1,254 个任务的 IoT-MCP Bench，代码见 Duke-CEI-Center/IoT-MCP-Servers。
- [An LLM-Agnostic, MAVLink-Based Drone Command and Control Interface and Agentic Harness Using the Model Context Protocol](https://arxiv.org/abs/2601.15486) - DroneServer（arXiv 2026-01）：连接 MCP 与 MAVLink 的 98 工具 Agent 框架，支持 ArduPilot 和 PX4，服务端强制地理围栏和确认，经 1,000 多次 SITL 飞行和三架真实四旋翼测试。
- [Demonstration-Free Robotic Control via LLM Agents](https://arxiv.org/abs/2601.20334) - FAEA（arXiv 2026-01）：将未修改的 Claude Agent SDK 直接用作操作控制器，在可获取特权环境状态的条件下，于 LIBERO、ManiSkill3、MetaWorld 上无需示教达到 84.9-96% 成功率，代码见 robiemusketeer/faea-sim。
- [AgentRob: From Virtual Forum Agents to Hijacked Physical Robots](https://arxiv.org/abs/2602.13591) - AgentRob（arXiv 2026-02）：读取论坛帖子的 LLM Agent 通过 MCP 向 Unitree Go2/G1 机器人上的 VLM 控制器下发指令，揭示实体 Agent 被劫持的风险。
- [ROSClaw: An OpenClaw ROS 2 Framework for Agentic Robot Control and Interaction](https://arxiv.org/abs/2603.26997) - ROSClaw（arXiv 2026-03）：连接 OpenClaw 与 ROS 2 的执行层，提供能力发现、执行前安全校验和审计日志，已部署在轮式、四足和人形机器人上。
- [Say the Mission, Execute the Swarm: Agent-Enhanced LLM Reasoning in the Web-of-Drones](https://arxiv.org/abs/2605.03788) - Web-of-Drones（arXiv 2026-05）：LLM Agent 核心通过 MCP 网关操作基于 W3C WoT 的无人机 Thing 执行集群任务，在 ArduPilot 仿真中评测六个 LLM。
- [Octopus Protocol: One-Shot Hardware Discovery and Control for AI Agents via Infrastructure-as-Prompts](https://arxiv.org/abs/2605.09055) - Octopus Protocol（arXiv 2026-05）：编码 Agent 通过一条引导命令枚举主机硬件、推断能力、生成带类型的 MCP 工具与驱动代码并部署为在线端点。
- [AutoMCU: Feasibility-First MCU Neural Network Customization via LLM-based Multi-Agent Systems](https://arxiv.org/abs/2605.21560) - AutoMCU（arXiv 2026-05）：多 Agent 系统为 MCU 设计神经网络，在环利用厂商工具链反馈剔除超出 RAM 和 Flash 限制的候选架构。
- [When Agents Control Robots: A Zero Trust Policy Model for Agentic Cyber-Physical Systems](https://arxiv.org/abs/2605.25653) - ZTPM（arXiv 2026-05）：包含 25 个策略原语和物理影响分级的零信任策略模型，基于对四 Agent UR3e 机械臂控制系统的攻击分析。
- [Can AI Agents Really Complete RTL-to-GDS? Lessons from Benchmarking Tool-Interactive EDA Workflows](https://arxiv.org/abs/2607.17528) - RTL-to-GDS Agent 研究（arXiv 2026-07）：让 Claude Code 等带 EDA Skill 的 Agent 在商业工具上跑 PicoRV32 全流程，发现 Skill 有助于子任务但不能保证长流程完成。
- [AgentDV: Closed-Loop Agentic AI for Hardware Design Verification](https://arxiv.org/abs/2608.27148) - AgentDV（arXiv 2026-08）：闭环 Agent 生成 Verilator/cocotb/pyUVM 测试平台，结合可运行性过滤和覆盖率引导迭代，在 OpenTitan IP 上评测。
- [LLM-based Hardware Development with Hierarchical IRs and End-to-End Multi-Agent Workflow](https://arxiv.org/abs/2608.30659) - 分层 IR 硬件 Agent（arXiv 2026-08）：多 Agent 流程使用架构草图和操作规格两级 IR，调试循环自主选择探测信号，在 VerilogEval 上 pass@5 达 95.5%。
- [Spec2Control: Automating PLC/DCS Control-Logic Engineering from Natural Language Requirements with LLMs - A Multi-Plant Evaluation](https://arxiv.org/abs/2510.04519) - Spec2Control（arXiv 2025-10）：ABB 提出的 LLM 工作流，把控制说明转换为 IEC 61131-3 功能块图，开源于 hkoziolek/Spec2Control。
- [Vendor-Aware Industrial Agents: RAG-Enhanced LLMs for Secure On-Premise PLC Code Generation](https://arxiv.org/abs/2511.09122) - 厂商感知 PLC Agent（arXiv 2025-11）：面向 Mitsubishi Electric PLC 方言的本地部署 RAG 编码助手，在环编译生成代码并使用小型本地模型。
- [ROSBag MCP Server: Analyzing Robot Data with LLMs for Agentic Embodied AI Applications](https://arxiv.org/abs/2511.03497) - ROSBag MCP Server（arXiv 2025-11）：介绍一个 MCP 服务器，让 LLM 和 VLM 用自然语言分析、可视化和处理 ROS/ROS 2 bag 数据。
- [The Dawn of Agentic EDA: A Survey of Autonomous Digital Chip Design](https://arxiv.org/abs/2512.23189) - Agentic EDA 综述（arXiv 2025-12）：梳理从单点 AI-for-EDA 工具向由 Agent 编排 RTL-to-GDSII 全流程的转变。
- [Spec2RTL-Agent: Automated Hardware Code Generation from Complex Specifications Using LLM Agent Systems](https://arxiv.org/abs/2506.13905) - Spec2RTL-Agent（arXiv 2025-06）：多 Agent 系统直接读取完整规格文档，规划实现并通过错误溯源反思迭代可综合 C++ 代码，再经 HLS 生成 RTL，人工干预最多减少 75%。
- [Embedded Firmware Development with Claude Code](https://reversetobuild.com/devlogs/claude-code-embedded-firmware-development/) - 使用 Claude Code 开发 nRF52840 Zephyr/NCS 固件的工程实践文章：编写 devicetree overlay、用 hook 拦截臆造的 Kconfig 符号、追踪编译错误并解析 HardFault。
- [How Firmware Engineers Get the Most Out of Claude](https://hubble.com/community/guides/how-firmware-engineers-get-the-most-out-of-claude/) - Hubble Network 面向固件工程师的指南，介绍用 Claude 从寄存器表生成头文件、做嵌入式专项代码审查，以及结合 map 文件诊断链接错误。

## Agent 友好文档（llms.txt）

提供 `llms.txt` 的厂商文档——已于 2026-09-16 实时核验为纯文本，以该名称返回 HTML 页面的一律剔除。可作为 Skill 的 `references/` 使用。

- [Arduino](https://docs.arduino.cc/llms.txt) - 181 KB 的索引加 `llms-full.txt`；找到的唯一一个 MCU 厂商 llms.txt。
- [NVIDIA Jetson](https://docs.nvidia.com/jetson/llms.txt) - 另有 `docs.omniverse.nvidia.com/llms.txt`。
- [Silicon Labs](https://docs.silabs.com/llms.txt) - 36 MB 的完整转储，覆盖 EFR32、BLE、Zigbee 与 Matter。
- [瑞萨](https://www.renesas.com/llms.txt) - 公司与产品索引，6.7 KB。
- [Nordic nRF Cloud](https://docs.nrfcloud.com/llms.txt) - 50 KB；Nordic 的器件文档挡在一个人机验证页面后面，这个没有。
- [DFRobot](https://wiki.dfrobot.com/llms.txt) - 2.2 MB 的产品 Wiki、教程、手册与数据手册——找到的最大硬件类 llms.txt。
- [Radxa](https://docs.radxa.com/llms.txt) - 产品与技术文档索引。
- [Edge Impulse](https://docs.edgeimpulse.com/llms.txt) - TinyML 流水线文档。
- [Particle](https://docs.particle.io/llms.txt) - Device OS 与云平台。
- [Memfault](https://docs.memfault.com/llms.txt) - 可观测性 SDK。
- [Blues Notecard](https://dev.blues.io/llms.txt) - 蜂窝 / LoRa Notecard API。
- [balena](https://docs.balena.io/llms.txt) - 面向 Linux SBC 的机队管理。
- [Viam](https://docs.viam.com/llms.txt) - 机器人平台。
- [Foxglove](https://docs.foxglove.dev/llms.txt) - 机器人可观测性。
- [Luxonis](https://docs.luxonis.com/llms.txt) - OAK 相机。
- [LeRobot](https://huggingface.co/docs/lerobot/llms.txt) - Hugging Face 机器人学习。
- [Adafruit Learn](https://learn.adafruit.com/llms.txt) - Adafruit 开发板与模块的教程。
- [涂鸦](https://developer.tuya.com/llms.txt) - IoT 平台。
- [Flux.ai](https://docs.flux.ai/llms.txt) - 浏览器端 EDA。
- [Espressif MCP servers](https://mcp.espressif.com/) - Espressif 托管 MCP 服务器汇总页，涵盖文档检索、ESP Component Registry、RainMaker、ESP-VISION、故障排查流程和 ESP Pilot 板级配置。
- [Google Home Developer MCP](https://developers.home.google.com/mcp/developer) - Google 官方 Home Developer MCP 服务器（homedevelopers.googleapis.com/mcp），让编码 Agent 检索 Home API 文档、Matter 1.5.1 与 Thread 1.4.1 规范以及 OpenThread 文档。
- [Silicon Labs MCP server](https://docs.silabs.com/mcp/1.0.0/mcp-start/) - Silicon Labs 托管的 AskAI MCP 服务器，需要 Silicon Labs 账号登录，为 Agent 提供一个检索 Silicon Labs 文档与资源的工具。
- [OPC UA Online Reference MCP](https://opcconnect.opcfoundation.org/2026/06/updates-to-online-reference-for-humans-and-ai/) - OPC Foundation 在 reference.opcfoundation.org/mcp 提供的 MCP 端点，可按全文、NodeId、一致性单元和术语检索 OPC UA 规范，并提供 Markdown 与 JSONL 规范下载。
- [docs.modalai.com llms.txt](https://docs.modalai.com/llms.txt) - 面向 PX4 与 ArduPilot 无人机的 ModalAI VOXL/VOXL 2 机载计算机的官方 llms.txt 索引。
- [docs.auterion.com llms.txt](https://docs.auterion.com/llms.txt) - Auterion Suite 无人机机队管理与 Mission Control 的官方 llms.txt 索引。
- [docs.hello-robot.com llms.txt](https://docs.hello-robot.com/llms.txt) - Hello Robot Stretch 移动操作机器人的官方 llms.txt 索引。
- [docs.picknik.ai llms.txt](https://docs.picknik.ai/llms.txt) - MoveIt Pro 机械臂应用平台（含行为树）的官方 llms.txt 索引。
- [docs.formant.io llms.txt](https://docs.formant.io/llms.txt) - Formant 机器人群监控、干预与遥操作的官方 llms.txt 索引。
- [rerun.io llms.txt](https://rerun.io/llms.txt) - Rerun 多模态机器人与空间数据记录可视化平台的官方 llms.txt 索引。
- [docs.saleae.com llms.txt](https://docs.saleae.com/llms.txt) - Saleae Logic 2 自动化、扩展与 MSO API 的官方 llms.txt 索引。
- [docs.lagerdata.com llms.txt](https://docs.lagerdata.com/llms.txt) - Lager 嵌入式硬件测试自动化的官方 llms.txt 索引。
- [docs.flipper.net llms.txt](https://docs.flipper.net/llms.txt) - Flipper Zero 与 Flipper One 用户与开发者文档的官方 llms.txt 索引。
- [docs.tuyaopen.ai llms.txt](https://docs.tuyaopen.ai/llms.txt) - TuyaOpen（涂鸦开源 AI+IoT 设备操作系统与 SDK）的官方 llms.txt 索引。
- [docs.emqx.com llms.txt](https://docs.emqx.com/llms.txt) - EMQX MQTT Broker、边缘与工业 IoT 产品的官方 llms.txt 索引。
- [thingsboard.io llms.txt](https://thingsboard.io/llms.txt) - ThingsBoard IoT 设备管理平台的官方 llms.txt 索引。
- [docs.hubble.com llms.txt](https://hubble.com/docs/llms.txt) - Hubble Network 蓝牙直连卫星 IoT 连接与设备 SDK 的官方 llms.txt 索引。
- [docs.qualcomm.com llms.txt](https://docs.qualcomm.com/llms.txt) - Qualcomm SDK、API 与平台指南的官方 llms.txt 索引。
- [developers.soracom.io llms.txt](https://developers.soracom.io/llms.txt) - Soracom 蜂窝 IoT 连接 API 与 SDK 的官方 llms.txt 索引。
- [docs.hologram.io llms.txt](https://docs.hologram.io/llms.txt) - Hologram IoT 蜂窝 SIM 与连接服务的官方 llms.txt 索引。
- [docs.helium.com llms.txt](https://docs.helium.com/llms.txt) - Helium LoRaWAN IoT 与移动网络的官方 llms.txt 索引。
- [apps.developer.homey.app llms.txt](https://apps.developer.homey.app/llms.txt) - 在 Homey 网关上运行应用的 Homey Apps SDK 的官方 llms.txt 索引。
- [docs.aqara.com llms.txt](https://docs.aqara.com/llms.txt) - Aqara 开发者文档中心的官方 llms.txt 索引。
- [kb.shelly.cloud llms.txt](https://kb.shelly.cloud/llms.txt) - 按型号组织的 Shelly 设备知识库的官方 llms.txt 索引。
- [developer.govee.com llms.txt](https://developer.govee.com/llms.txt) - Govee 开发者平台的官方 llms.txt 索引，涵盖列出、控制和订阅 Govee 智能家居设备事件的 API。
- [apidocs.verkada.com llms.txt](https://apidocs.verkada.com/llms.txt) - Verkada 摄像头与门禁 API 的官方 llms.txt 索引。
- [docs.jitx.com llms.txt](https://docs.jitx.com/llms.txt) - JITX 代码驱动 PCB 设计的官方 llms.txt，以整份文档全文形式提供。
- [docs.quilter.ai llms.txt](https://docs.quilter.ai/llms.txt) - Quilter 自动化 PCB 布局的官方 llms.txt 索引。
- [docs.allspice.io llms.txt](https://learn.allspice.io/llms.txt) - AllSpice 硬件设计评审与版本管理的官方 llms.txt 索引。

已核查但缺失（404 或返回 HTML）：Zephyr、乐鑫、Nordic、ST、PlatformIO、KiCad、ROS 文档、Golioth、Home Assistant、ESPHome、MicroPython、CircuitPython、树莓派、矽递 Wiki、Isaac Sim / Lab、Embassy、BeagleBoard、ThingsBoard。Zephyr 改为提供 `AGENTS.md`、`CLAUDE.md` 与 `copilot-instructions.md`；nRF Connect SDK 在 HEAD 上三者皆无。

## 空白

尚不存在的东西记录在 **`GAPS.zh-CN.md`** 中，附有每条声明背后的证据、现存最接近的东西（好让声明保持可证伪），以及五个范围明确、连 eval 断言都已写好的首次贡献建议。要点如下：

**A2A 从未真正落到硬件上。** 发布十七个月后，没有任何仓库在真实物理设备上端到端实现 Linux 基金会的 A2A 规范。这份 3618 行的规范中，*robot*、*actuator*、*sensor*、*embedded* 出现次数均为零，1721 个 issue 中也没有一个在要求设备控制。这看起来是设计上的必然而非疏忽：设备是独占的、物理上不可逆的、有时限约束的，而 A2A 建模的是不透明对等方之间可重试的对话。此后所有设备侧的协议尝试——MCP-over-MQTT、Arm Device Connect、DCP——都选择依附于 MCP。

**厂商几乎没有入场。** 只有四家芯片厂商发布过宿主侧 Skill：Arm、瑞萨、德州仪器，以及在 ESP-DL 仓库中发布的乐鑫。ST 有 786 个公开仓库却一个都没有；英飞凌有 2301 个；NXP 有 221 个；树莓派有 115 个，Pico SDK 空空如也。`espressif/skills` 是一个官方仓库，README 教你去安装它，而整棵文件树只有 `README.md` 加一个 `skills/.gitkeep`——2026-04-24 当天创建后三小时内就被弃置。七家厂商发布了 MCP server，没有一家能在仿真中执行任何东西。

**Renode 缺少面向 Agent 的接口。** 模拟器本身不是瓶颈：它确定性执行、可以无头运行，而且已经在 `renode-test` 与 Robot Framework 中自带断言框架。缺的是一个能为 Agent 维持活会话的东西，好让交互式固件调试与 L1 runner 共用同一套集成，而不是各自重新拼凑一段脆弱的 shell 配方。它值得为了更快的迭代而去做——但它无法让任何 Skill 通过，所以验证真正的瓶颈是能否接触到板子，而不是模拟器。

**硬件在环仍是覆盖最少的模式**——烧录、运行、读串口、迭代——尽管它恰恰是唯一有公开证据支撑的模式：前沿模型在没有硬件反馈时部署成功率为 0%，有了反馈则在七轮内超越人类专家。它也是通往"通过"的唯一途径。

同样空白、且每一项都经过核实而非假设：树莓派 5 Linux、设备树与 U-Boot、Thread 与设备侧 Matter、非攻击用途的 NFC、作为 Agent 工具的 VLA 策略、波士顿动力 Spot，以及通用 USB 控制（USB *分析* 已有覆盖）。Wi-Fi 配网与 Lattice FPGA 工具链现在各有一个 Skill，但都还没有 MCP server。

## 相关列表

- [beriberikix/awesome-mcp-hardware](https://github.com/beriberikix/awesome-mcp-hardware) - 硬件 MCP server 的上游列表；本列表的 MCP 部分由此起步。
- [TensorBlock/awesome-mcp-servers — hardware & IoT](https://github.com/TensorBlock/awesome-mcp-servers/blob/main/docs/hardware--iot.md) - 某通用 MCP 列表中的硬件分类。
- [fouad1233/amazing-robotics-skills](https://github.com/fouad1233/amazing-robotics-skills) - 区分许可证的 NVIDIA 生态 Skill 索引，覆盖 35 个仓库中的 1039 个 Skill。
- [ros-claw](https://github.com/ros-claw) - 汇集约 35 个机器人与传感器 MCP 的组织，外加一套 Skill 目录格式（SKILL.md + skill.yaml + 行为树）。
- [heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills) - 通用 Agent Skill 目录。
- [skillmatic-ai/awesome-agent-skills](https://github.com/skillmatic-ai/awesome-agent-skills) - 通用 Agent Skill 目录。
- [skills.sh](https://skills.sh) - 带安装量统计的 Skill 注册表；上文引用的安装量即来自这里。
- [ClawHub](https://www.clawhub.ai) - OpenClaw 的 Skill 注册表；收录了一些没有 GitHub 源码的硬件 Skill（esp32、arduino、raspberry、bambu-cli、meshtastic），上文引用的相应安装量即来自这里。
- [s87343472/awesome-ai-hardware](https://github.com/s87343472/awesome-ai-hardware) - 经过审核的可复现开源项目清单，收录把 LLM 和 Agent 接入真实硬件的项目，涵盖智能家居、可穿戴、机器人、微控制器和硬件协议桥接。(★12 · 2026-09)
- [GT-RIPL/Awesome-LLM-Robotics](https://github.com/GT-RIPL/Awesome-LLM-Robotics) - 规模很大的精选清单，收录将语言与多模态模型用于机器人推理、规划、操作和 Agent 的论文与代码。(★4.5k · 2026-07)
- [zchoi/Awesome-Embodied-Robotics-and-Agent](https://github.com/zchoi/Awesome-Embodied-Robotics-and-Agent) - 基于 LLM 与 VLM 的具身机器人与 Agent 研究精选清单，含基准和规划相关工作。(★1.9k · 2026-09)
- [ai4eda/awesome-AI4EDA](https://github.com/ai4eda/awesome-AI4EDA) - AI for EDA 论文精选清单（ai4eda.github.io），涵盖 LLM 与 Agent 在芯片设计上的研究。(★217 · 2026-05)
- [labclaw/awesome-physical-ai-for-science](https://github.com/labclaw/awesome-physical-ai-for-science) - 关于自动驾驶实验室、实验室机器人以及操作科学仪器的 AI Agent 的精选清单。(★8 · 2026-03)
- [natnew/awesome-physical-ai](https://github.com/natnew/awesome-physical-ai) - 面向工程实践的具身智能资源地图，收录 229 条机器人学习、VLA 模型、仿真、安全与机器人硬件资源。(★142 · 2026-09)

## 贡献

请阅读 [CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md)。简而言之：每个条目一行、放进正确的分类，运行 `python scripts/l0_check.py readme README.md`；如果你添加的是自己维护的 Skill，请把 [`template/evals/`](template/evals/) 复制进去（或者让 `hardware-skill-creator` 和你一起搭建这个包），并在真实板子上跑过之后提交一份 [L2 实测背书](.github/ISSUE_TEMPLATE/attestation.yml)。

新增或修改条目时，请**同时修改** `README.md` 与本文件——CI 会检查两份文档的条目是否一一对应。
