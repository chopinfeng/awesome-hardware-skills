# Awesome Hardware Skills [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

*[English](README.md) · 简体中文*

> 让 AI 编程 Agent（Claude Code、Codex、Cursor、OpenClaw 等）构建、烧录、调试和控制物理硬件的 Skill、MCP server、端侧 Agent 运行时、模拟器、评测基准与 CI 基础设施——并配一套验证阶梯，让你能分辨哪些是真的能在板子上跑起来的。

大多数"awesome MCP"列表只告诉你某个硬件 server **存在**。这份列表还追踪有没有人证明过它能用：每个 Skill 条目都可以带上三级阶梯的徽章——静态检查、模拟器预检、在真实板子上运行——而且**只有在真实板子上运行才算通过**。阶梯的含义见下面第一节。

配套文件 [GAPS.zh-CN.md](GAPS.zh-CN.md) 追踪的是**尚不存在**的东西——每条空白都附上核查证据、现存最接近的东西（好让这条声明可被证伪），以及带有 eval 断言的、范围明确的首次贡献建议。

快照时间：2026-09-16。星数、最近推送时间以及 skills.sh / ClawHub 的安装量均取自当天。`stale` 表示 12 个月以上没有推送；`official` 表示仓库位于硬件或 SDK 厂商自己的 GitHub 组织下。

> 本文档译自 [README.md](README.md)。如两者有出入，以英文版为准。

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

**`ΔPass +42%`** —— 同一模型下、在真实板子上、每组每个任务交替运行五次测得的，装了 Skill 与不装 Skill 的任务通过率之差，发布时附 95% 置信区间和 `gain`、`low-gain` 或 `inconclusive` 标签，以免把噪声当成证据。它用来说明这个 Skill 确实携带了模型原本不具备的知识。即将推出。

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

厂商官方 Skill 就地标注 `official`。截至本次快照，它们来自 NVIDIA、乐鑫（仅端侧）、Adafruit、矽递、M5Stack、Arm、瑞萨、德州仪器、博流、安信可、思澈、合宙、LilyGO、RT-Thread、小米 Vela、涂鸦、嘉立创 EDA、Hailo、地平线、D-Robotics、Luxonis、Intel、Google、Meta、Pollen、智元、Wandelbots、Viam、PX4、Matter SDK、Home Assistant、SmartThings、Z-Wave JS、Meshtastic、SimpleBLE、Reolink、Elgato、CSS Electronics、EcuBus、Nominal、Joulescope、DAQiFi、高通、Ångström、openEuler、Anthropic 与 Nebius——而 MCU 芯片厂商中，除瑞萨、Arm 和德州仪器外别无他家。

### MCU / 嵌入式

- [Jeffallan/claude-skills `embedded-systems`](https://github.com/Jeffallan/claude-skills/tree/main/skills/embedded-systems) - STM32 / ESP32 / FreeRTOS / 裸机工作流：外设、中断服务程序、DMA、功耗；安装量最高的通用嵌入式 Skill（skills.sh 上约 6000 次）。(★11.5k · 2026-08)
- [hathach/tinyusb `.claude/skills/`](https://github.com/hathach/tinyusb/tree/master/.claude/skills) - `hil` 驱动 TinyUSB 的硬件在环测试台；`target-debug`、`rtt`、`etm-trace`、`usb-sniffer`、`usbmon` 解读目标板上的 USB 协议栈行为。Agent Skill 接真实 HIL 测试台的最佳范例。(coll · ★7.1k · 2026-09)
- [FastLED/FastLED `.claude/skills/`](https://github.com/FastLED/FastLED/tree/master/.claude/skills) - 项目内部但货真价实：ESP-IDF v5 RMT5 驱动专家、ESP32 日志分诊与测试计划 Skill、Xtensa 与 RISC-V 汇编代码审查、时序分析。(coll · ★7.5k · 2026-09)
- [LeoKemp223/embed-ai-tool](https://github.com/LeoKemp223/embed-ai-tool) - 约 25 个自带脚本的 Skill，覆盖整条 MCU 工具链：用 Keil / IAR / CMake / ESP-IDF / PlatformIO 构建，用 OpenOCD / J-Link / idf.py 烧录，用 GDB 调试，另有 CAN、Modbus、VISA 与 RTOS 调试。中文。(coll · ★919 · 2026-08)
- [zhinkgit/embeddedskills](https://github.com/zhinkgit/embeddedskills) - 跨 OpenOCD、J-Link、probe-rs、Keil 与 EIDE 的探针识别、烧录、GDB server、telnet 调试、半主机与 ITM 抓取。中文。(coll · ★664 · 2026-09)
- [DunCanYounG-1/auto-embedded](https://github.com/DunCanYounG-1/auto-embedded) - STM32 / ESP32 / GD32 / MSPM0 开发框架，含 24 个工具 Skill，可注入七种 Agent 平台。中文。(coll · ★243 · 2026-09)
- [Mindrally/skills `embedded-stm32`](https://github.com/Mindrally/skills/tree/main/embedded-stm32) - 由 Cursor rules 演化而来的 STM32 HAL Skill：CubeMX、DMA、SWD 约定。(★259 · 2026-09)
- [mohitmishra786/low-level-dev-skills](https://github.com/mohitmishra786/low-level-dev-skills) - 带数据手册阅读指引的裸机基本功：STM32 裸机、GPIO、UART、I2C/SPI 总线驱动、DMA、Bootloader、OpenOCD/JTAG、嵌入式 Rust、QEMU 仿真、FreeRTOS、Zephyr。(coll · ★210 · 2026-06)
- [SensorsIot/Embedded-AI-Harness `esp-idf-handling`](https://github.com/SensorsIot/Embedded-AI-Harness/tree/main/.claude/skills/esp-idf-handling) - 闭环 ESP-IDF：构建、通过本地 USB 或 RFC2217 远程测试台烧录、监视、OTA、崩溃恢复。少数真正闭合"烧录 → 观测 → 迭代"回路的 Skill 之一。(★175 · 2026-08)
- [Gundry-Consultancy/sbc-mcu-dut-controller `.agent/skills/`](https://github.com/Gundry-Consultancy/sbc-mcu-dut-controller/tree/main/.agent/skills) - 把一套真实 HIL 测试台做成 Skill：`hil-job-api`、`hil-author-test`、`hil-firmware-compare`、`hil-bisect`、`hil-camera-proof`，覆盖 ESP32 / RP2040 / SAMD 烧录、继电器电源与 I2C 复用器。(coll · ★0 · 2026-07)
- [magnus919/agent-skills `esp32-development`](https://github.com/magnus919/agent-skills/tree/main/esp32-development) - 识别 ESP32 板型，在 ESP-IDF、Arduino、MicroPython、CircuitPython、ESPHome、Zephyr、Rust 与 NuttX 之间做选择，接线、烧录、救砖。(★82 · 2026-09)
- [CY-CHENYUE/esp-idf-cy](https://github.com/CY-CHENYUE/esp-idf-cy) - 用国内镜像安装 ESP-IDF，然后构建 → 烧录 → 监视，并带设备命名。(★40 · 2026-07)
- [kukucaiCndy/embedded_ai_skills](https://github.com/kukucaiCndy/embedded_ai_skills) - ESP32（IDF 与 Arduino）、STM32 与 Nordic NCS 的"环境搭建 / 工程初始化 / 调试"三件套，另含 ZMK 键盘与嘉立创 EDA 绘图 Skill。(coll · ★54 · 2026-07)
- [ezrover/ESP32-AI-Agent-Skill](https://github.com/ezrover/ESP32-AI-Agent-Skill/tree/main/skills/esp32) - 选型（S3 / C3 / C6）、PSRAM 与 MMU 注意事项、GPIO12 启动引脚陷阱、ESP-IDF 与 PlatformIO 配置、LVGL 与微雪屏幕资料。(★37 · 2026-08)
- [easyzoom/aix-skills](https://github.com/easyzoom/aix-skills) - 偏集成的 MCU Skill：ESP-IDF、STM32 HAL/LL、FreeRTOS 内核调试、FreeRTOS+TCP、OpenOCD / J-Link / ST-Link。(coll · ★32 · 2026-07)
- [JasonYANG170/esp-dev-skill](https://github.com/JasonYANG170/esp-dev-skill) - 乐鑫每个仓库一个子 Skill：esp-idf、arduino-esp32、esp-adf、esp-dl、esp-zigbee-sdk、esp-at、esp-brookesia、esp-claw、connectedhomeip。(coll · ★27 · 2026-08)
- [ylongw/embedded-review](https://github.com/ylongw/embedded-review) - 针对中断、RTOS 与内存问题的双模型固件审查；ClawHub 约 1800 次安装。(★48 · 2026-03)
- [EricSun787/stm32-development-workflow](https://github.com/EricSun787/stm32-development-workflow) - STM32CubeCLT 命令行流程：工具链、HAL、构建、ST-Link 烧录、常见报错修复。中文。(★24 · 2026-02)
- [wedsamuel1230/arduino-skills](https://github.com/wedsamuel1230/arduino-skills) - 30 个 Arduino 与创客 Skill：代码生成、arduino-cli、串口监视、引脚分配、I2C 上电诊断、接线安全检查、功耗预算、BOM、OTA 守卫。(coll · ★21 · 2026-08)
- [claudius-ars/embedded-agent-skills `gpio-config`](https://github.com/claudius-ars/embedded-agent-skills/tree/main/embedded-agent-skills/gpio-config) - 树莓派（设备树 overlay、config.txt）与 ESP32（sdkconfig）的 GPIO / I2C / SPI / UART / PWM 引脚分配与冲突检查。(★19 · 2026-02)
- [alexex1993/mcu-skills](https://github.com/alexex1993/mcu-skills) - 一板一 Skill（共 19 个）：RP2040 Pico、RP2350、ESP32-WROOM 30/36/38 脚、ESP32-S3-CAM、ESP32-C6、ESP32-P4、nRF52840 ProMicro、STM32F411 BlackPill、STM32H750、ATmega328P Nano、ESP8266——引脚图、外设、供电。(coll · ★17 · 2026-09)
- [Loclove/Electronics-Design-Competition-Skill-2](https://github.com/Loclove/Electronics-Design-Competition-Skill-2) - 全国大学生电子设计竞赛（电赛）单片机 Skill，含 agents 与参考资料。(★14 · 2026-07)
- [o2scale/electronics-agent-kit](https://github.com/o2scale/electronics-agent-kit/tree/main/.agent/skills) - 面向 Arduino、ESP-IDF 与 STM32 的 PlatformIO 工程 / 配置 / 调试，外加 kicad-cli 与 KiCad 文件格式 Skill。(coll · ★12 · 2026-02)
- [grumat/glossy-msp430 `.claude/skills/`](https://github.com/grumat/glossy-msp430/tree/master/.claude/skills) - 解码 MSP430 JTAG 逻辑分析仪抓包并跑单元测试；目前找到的唯一 TI MSP430 Skill。(coll · ★15 · 2026-07)
- [varo6/reTerminal-sticky-skill](https://github.com/varo6/reTerminal-sticky-skill/tree/main/skills/sticky-device) - 矽递 reTerminal Sticky（ESP32-S3 墨水屏）：引脚映射、ESP-IDF 写法、电子纸刷新规则。(★7 · 2026-08)
- [BlueAndi/Pixelix `.github/skills/`](https://github.com/BlueAndi/Pixelix/tree/master/.github/skills) - 面向 ESP32 固件的 MISRA 风格嵌入式 C++14 规约，以 GitHub Copilot skill 形式提供。(copilot · ★442 · 2026-09)
- [fxp/m5stack-embedded-dev-skill](https://github.com/fxp/m5stack-embedded-dev-skill) - 以 Arduino + M5Unified 为先的 M5Stack/ESP32 Skill：板型到 FQBN 的对照表、按芯片代际区分的 GPIO 安全规则、I2C 与 PMIC 的坑、FreeRTOS 与中断规则、崩溃分诊；自带 `serial_match` / `exit_code` 断言的 evals 包，已在本地通过 L0。新项目、尚无星标——收录它是因为 evals 包的形态，而非过往记录。(★0 · 2026-09)
- [PatrickJS/awesome-cursorrules `embedded-stm32-hal`](https://github.com/PatrickJS/awesome-cursorrules/blob/main/rules/embedded-stm32-hal.mdc) - 是 Cursor rule 而非 Skill：STM32 HAL 上的嵌入式 C/C++、中断、DMA 与内存约束规范。(cursor-rules · ★40.8k · 2026-05)

### RTOS

- [beriberikix/zephyr-agent-skills](https://github.com/beriberikix/zephyr-agent-skills) - 最完整的 Zephyr 目录（21 个 Skill）：基础、板级 bring-up（HWMv2）、设备树、构建系统、内核、BLE / IP / USB / CAN 连接、IoT 协议、多核、`native_sim`、功耗、安全更新、存储、测试；一个按关键词 / Kconfig / compatible 打分的路由器负责挑选。(coll · ★64 · 2026-05)
- [ksachdeva/zephyr-rtos-ai](https://github.com/ksachdeva/zephyr-rtos-ai/tree/main/skills) - 25 个按子系统划分的 Zephyr API Skill：BLE（GAP 角色、GATT、配对、NUS）、设备树、Kconfig、GPIO、I2C、SPI、UART、中断、线程、同步、电源管理、settings、存储、socket、Wi-Fi、状态机框架、shell、测试、内存。(coll · ★23 · 2026-06)
- [a5c-ai/babysitter `embedded-systems`](https://github.com/a5c-ai/babysitter/tree/main/library/specializations/embedded-systems/skills) - 29 个短 Skill：Zephyr、FreeRTOS、Nordic nRF、STM32 HAL、Cortex-M、JTAG/SWD、链接脚本、CAN、USB 协议栈、OTA、电机控制、MISRA、Unity/Ceedling。广度优先，深度不足。(coll · ★1.8k · 2026-09)
- [RT-Thread/rtthread-skills](https://github.com/RT-Thread/rtthread-skills) - RT-Thread 官方 Skill：创建 BSP、创建软件包、env 配置、代码审查、精简、Git 工作流。(official · coll · ★3 · 2026-07)
- [open-vela/.claude](https://github.com/open-vela/.claude) - 小米 Vela（NuttX）设备开发：驱动开发、构建、Kconfig 调整、内存转储、代码体积、驱动审查、PCM 音频（共 15 个 Skill）。(official · coll · ★5 · 2026-09)
- [chshzh/charlie-skills](https://github.com/chshzh/charlie-skills) - 27 个 Nordic nRF Connect SDK Skill，覆盖 PRD → 规格 → 编码 → 测试全流程、NCS 3.x 迁移、nRF70 Wi-Fi 吞吐与固件统计、Memfault。(coll · ★0 · 2026-08)
- [gevico/rt-claw `.agents/skills/`](https://github.com/gevico/rt-claw) - 移植与诊断基于 RT-Thread 的端侧 Agent 运行时：平台移植、OSAL 审查、诊断。(coll · ★11 · 2026-06)
- [eduardojvieira/ZPLC `stm32-freertos-developer`](https://github.com/eduardojvieira/ZPLC) - 软 PLC 项目中的 STM32 + FreeRTOS 开发 Skill；唯一一个有实质深度的 FreeRTOS 专项 Skill。(★6 · 2026-09)
- [goliothlabs/golioth-firmware-skill](https://github.com/goliothlabs/golioth-firmware-skill/tree/main/skills/golioth-firmware) - Zephyr、ESP-IDF、NCS 与 ModusToolbox 上的 Golioth SDK：全新接入与存量改造、OTA、六项云服务。(★1 · 2026-03)
- [toppers/asp3_pico_sdk `.claude/skills/`](https://github.com/toppers/asp3_pico_sdk) - RP2350（Cortex-M33 与 Hazard3 RISC-V）上的 TOPPERS/ASP3 RTOS，配 OpenOCD 与 GDB；同系列另有 NXP MCUXpresso 与瑞萨 FSP 移植。日文。(official · ★0 · 2026-09)

### MicroPython / CircuitPython

- [FreakStudioCN/MicroPython_Skills](https://github.com/FreakStudioCN/MicroPython_Skills) - 最大的 MicroPython 合集（60+）：mpremote 操作、固件烧录、部署、按规格生成驱动、选型、接线、仿真。中文。(coll · ★5 · 2026-09)
- [andrewleech/claude-mpy-marketplace](https://github.com/andrewleech/claude-mpy-marketplace) - mpremote 设备交互、文件传输与实时会话 Skill，外加 MicroPython 贡献者 Skill，作者是 MicroPython 核心维护者。(coll · ★2 · 2026-09)
- [m5stack/uiflow-micropython `tools/knowledge-base/`](https://github.com/m5stack/uiflow-micropython/tree/master/tools/knowledge-base) - 面向 UIFlow2 MicroPython 的 `uiflow2-coder` 与 `uiflow2-ui-designer`，内置官方文档。(official · coll · ★208 · 2026-09)
- [adafruit/LLM-Recipes](https://github.com/adafruit/LLM-Recipes/tree/main/circuitpython) - 在已连接的 CircuitPython 板上运行代码、编写并执行硬件测试，并通过对比 Arduino 与 CircuitPython 的总线波形来验证 I2C 驱动。(official · coll · ★3 · 2026-06)
- [adafruit/Adafruit_Learning_System_Guides `embodiment-kit`](https://github.com/adafruit/Adafruit_Learning_System_Guides/tree/main/Embodiment_Kit/agent_skill/embodiment-kit) - 通过 Adafruit IO 驱动 CircuitPython "embodiment kit"（显示屏、NeoPixel、传感器），并带前后传感器读数作为证据。(official · ★1.1k · 2026-09)
- [rockets-cn/unihiker-k10-skills](https://github.com/rockets-cn/unihiker-k10-skills) - DFRobot 行空板 K10 的烧录与 API，覆盖 MicroPython、Arduino 与 PlatformIO，另含 OTA 与编译服务；各约 2000 次 ClawHub 安装。(coll · ★6 · 2026-08)
- [MakerClassCZ/picogame `skills/`](https://github.com/MakerClassCZ/picogame/tree/main/skills) - CircuitPython Pico 板级 bring-up：settings.toml、GPIO、显示。(★25 · 2026-09)
- [Cerwor/jlc-k230-lushan-pi](https://github.com/Cerwor/jlc-k230-lushan-pi) - 嘉立创庐山派 K230 CanMV MicroPython：摄像头、LCD、YOLO、mpremote 部署。(★4 · 2026-09)

### 嵌入式 Rust

- [actionbook/rust-skills `domain-embedded`](https://github.com/actionbook/rust-skills/tree/main/skills/domain-embedded) - `no_std`、Embassy 与 RTIC 约束，并自动注入 `.cargo/config.toml`；约 2400 次安装，是安装量最高的嵌入式 Rust Skill。另有姊妹 Skill `domain-iot`。(★1.5k · 2026-08)
- [OutlineDriven/odin-claude-plugin `odin-native`](https://github.com/OutlineDriven/odin-claude-plugin/tree/main/plugins/odin-native/skills) - 基于 cortex-m-rt / probe-rs / defmt / RTIC 的固件开发，外加 OpenOCD JTAG、FreeRTOS 与 QEMU 跑内核的 Skill。(coll · ★36 · 2026-09)
- [ch32-rs/ch32-rs `.claude/skills/`](https://github.com/ch32-rs/ch32-rs) - 把厂商 SVD 转成沁恒 RISC-V 芯片的 PAC crate。(★170 · 2026-05)
- [hispark-rs/hisi-riscv-rs `.agents/skills/`](https://github.com/hispark-rs/hisi-riscv-rs) - `hil-smoke` 与 `hil-regression`：烧录真实海思 ws63 板、读串口、断言特征字符串。(coll · ★3 · 2026-09)
- [bitscrafts/EFR32MG2X-RS](https://github.com/bitscrafts/EFR32MG2X-RS) - Silicon Labs EFR32MG24 的 Rust HAL 专家 Skill。(★6 · 2026-06)
- [Microbiosis/esp-rust-skills](https://github.com/Microbiosis/esp-rust-skills) - esp-hal 外设、Wi-Fi / BLE / ESP-NOW、工具链。中文。(coll · ★1 · 2026-06)

### 厂商 SDK

- [Open-CMSIS-Pack/CMSIS-Developer-Assistant](https://github.com/Open-CMSIS-Pack/CMSIS-Developer-Assistant) - Arm 的 CMSIS Skill 外加一个 MCP：bring-up、实时调试、pack 与工程创建、Cortex-M 板级层。(official · coll · ★2 · 2026-09)
- [TexasInstruments/C2000-IDEA `docs/skills/c2000-idea`](https://github.com/TexasInstruments/C2000-IDEA/tree/main/docs/skills/c2000-idea) - F28x 器件迁移分四份参考文档推进、位域到 driverlib 的转换、SysConfig ePWM 迁移；驱动本地 `idea-mcp` 端点以及 CCS Project、SysConfig 与 TI 汇编 MCP server。第三家发布宿主侧 Skill 的芯片厂商。(official · ★20 · 2026-09)
- [renesas/renesas-skills](https://github.com/renesas/renesas-skills) - `configure-renesas-debug` 为 J-Link / E2 / E2Lite / IECUBE 生成 VS Code launch.json；除 Arm 外唯一的芯片厂商 Skill 仓库。(official · ★5 · 2026-07)
- [bouffalolab/bouffalo_sdk `.agents/skills/`](https://github.com/bouffalolab/bouffalo_sdk/tree/master/.agents/skills) - 博流 SDK 开发指南，覆盖 BL602 / BL616 / BL808，另有变更日志与测试手册 Skill。(official · coll · ★498 · 2026-09)
- [bouffalolab/bouffalolab-skills](https://github.com/bouffalolab/bouffalolab-skills) - 博流的第二个 Skill 仓库：BL616 低功耗 IO 指南与 Wi-Fi 低功耗采集。(official · ★0 · 2026-09)
- [Ai-Thinker-Open/skills](https://github.com/Ai-Thinker-Open/skills) - 安信可模组 Skill（14 个）：Ai-M62/M61（BL616）、Ai-WB2（BL602）、Ra-01SC LoRa、coredump、OTA 生成、选型；配套还有 FlashKey MCP 烧录调试设备。(official · coll · ★8 · 2026-09)
- [Ai-Thinker-Open/FlashKey-skills](https://github.com/Ai-Thinker-Open/FlashKey-skills) - FlashKey 烧录调试设备的 Skill，搭配 `emMCP` 这个 UART 转 MCP 的协议生成库。(official · ★0 · 2026-08)
- [OpenSiFli/SiFli-SDK `skills/`](https://github.com/OpenSiFli/SiFli-SDK/tree/main/skills) - 思澈 SF32 蓝牙 SoC：Windows 构建、代码审查、崩溃转储分诊、USB 寄存器转储分析。(official · coll · ★182 · 2026-09)
- [OpenSiFli/SiFli-Skills](https://github.com/OpenSiFli/SiFli-Skills) - 思澈独立的 Skill 仓库，与 SDK 内那套分开维护。(official · ★1 · 2026-09)
- [openLuat/LuatOS `skill-packs/`](https://github.com/openLuat/LuatOS/tree/master/skill-packs) - 合宙 LuatOS Lua 固件（Air780 / Air101）：覆盖 72 个核心库的开发、文档与示例规格 Skill。(official · coll · ★589 · 2026-09)
- [Xinyuan-LilyGO/lilygo-skills](https://github.com/Xinyuan-LilyGO/lilygo-skills) - LilyGO T-Display / T-Watch / T-Beam 的引脚图与 Arduino / IDF / SF32 构建，前面挂一个路由 Skill。(official · ★6 · 2026-07)
- [tuya/TuyaOpen-dev-skills](https://github.com/tuya/TuyaOpen-dev-skills) - TuyaOpen 固件闭环：环境搭建、工程配置、构建、调试助手、开发循环、设备授权、新增板型、CLI 调试、崩溃解析。(official · coll · ★16 · 2026-07)
- [espressif/esp-claw-skills-lab](https://github.com/espressif/esp-claw-skills-lab) - 乐鑫第一个真正的 Skill 仓库，但是端侧的：43 个 SKILL.md 加 Lua 脚本，由 esp-claw 运行时在 ESP32 上执行（JSON frontmatter，并非 agentskills.io 格式）。(official · coll · ★32 · 2026-09)
- [espressif/skills](https://github.com/espressif/skills) - 乐鑫的宿主侧 Skill 仓库，2026-04 创建，README 里写着可用 `npx skills add espressif/skills` 安装——至今没有任何 SKILL.md。(official · placeholder · ★2 · 2026-04)
- [arm/agent-resources](https://github.com/arm/agent-resources) - Arm 的 Agent 资源注册表——schema、校验器和四个注册表 YAML，但还没有 SKILL.md。第二个厂商占位仓库。(official · ★0 · 2026-09)
- [0xchaihu/nxp-mcu-build-verify](https://github.com/0xchaihu/nxp-mcu-build-verify) - 用命令行构建 IAR、Keil、MCUXpresso IDE 与 VS Code MCUX 工程。(★28 · 2026-04)
- [JasonYANG170/ch57x-dev-skill](https://github.com/JasonYANG170/ch57x-dev-skill) - 沁恒 CH57x 蓝牙固件。(★12 · 2026-06)
- [ClarkJ-Infineon/mtb-workspace-template `.github/skills/`](https://github.com/ClarkJ-Infineon/mtb-workspace-template/tree/main/.github/skills) - 英飞凌工程师个人仓库里的 19 个 ModusToolbox Copilot Skill：BLE 配置、Wi-Fi MQTT、OpenOCD 调试、双核、PSoC 6 到 Edge 的迁移、雷达 DSP。(copilot · coll · ★0 · 2026-05)
- [ailyProject/aily-blockly `public/skills/`](https://github.com/ailyProject/aily-blockly) - aily Arduino AI IDE 的 Blockly 最佳实践与库迁移 Skill。(coll · ★3.8k · 2026-09)

### SBC / Linux

- [NVIDIA-AI-IOT/jetson-device-skills](https://github.com/NVIDIA-AI-IOT/jetson-device-skills) - `jetson-diagnostic`、`jetson-memory-audit`、`jetson-llm-serve`、`jetson-video-*` 等的权威来源，会镜像进 NVIDIA/skills；skills.sh 上安装量最高的硬件 Skill。(official · coll · ★135 · 2026-08)
- [NVIDIA-AI-IOT/jetson-bsp-skills](https://github.com/NVIDIA-AI-IOT/jetson-bsp-skills) - `jetson-customize-*` 系列 BSP Skill 的权威来源：pinmux、PCIe、USB、时钟、风扇、载板衍生、镜像校验与烧录。(official · coll · ★59 · 2026-06)
- [D-Robotics/moss `jetson-knowledge`](https://github.com/D-Robotics/moss) - Orin / Xavier 规格、JetPack / L4T、Super Mode、TensorRT engine 构建，同仓库还有 D-Robotics RDK 的 Skill。(coll · ★142 · 2026-08)
- [Seeed-Projects/Seeed-Jetson-DevelopTool](https://github.com/Seeed-Projects/Seeed-Jetson-DevelopTool/tree/main/skills/openclaw) - 矽递 reComputer / Jetson 支持 Skill：JetPack 概览、Docker 配置、AI 工具、L4T 版本差异、Jetson 上跑 YOLO、FAQ。(coll · ★55 · 2026-09)
- [sammcj/agentic-coding `raspberry-pi-pico2`](https://github.com/sammcj/agentic-coding/tree/main/Skills/raspberry-pi) - RP2350 配 Debug Probe：pico-sdk CMake、ARM 与 RISC-V、picotool、OpenOCD / GDB / RTT 资料。(★161 · 2026-09)
- [irfanmuhammedharis/raspberry-pi-skills-suite](https://github.com/irfanmuhammedharis/raspberry-pi-skills-suite) - 唯一一套覆盖面较广的树莓派合集：Pico MicroPython 与 C SDK、GPIO 传感器与执行器、Linux 配置、调试、边缘 AI 视觉、网络、机器人、供电。偏薄（每个约 3 KB）。(coll · ★0 · 2026-03)
- [TheYoctoJester/dutler](https://github.com/TheYoctoJester/dutler) - 把 Pico 当作板卡农场的 USB 串口控制台桥与电源继电器，配 `run-dutler` Skill。(★21 · 2026-07)
- [qualcomm-linux/qcom-linux-skills](https://github.com/qualcomm-linux/qcom-linux-skills) - 高通 Linux / meta-qcom / Dragonwing 板卡：Yocto 镜像构建、预编译下载、LAVA CI 报告、PR 前检查、Debian 镜像构建。(official · coll · ★6 · 2026-09)
- [prashantdivate/awesome-yocto-ai-agent-skills](https://github.com/prashantdivate/awesome-yocto-ai-agent-skills) - 覆盖最广的 Yocto 合集（12 个）：BSP bring-up、构建调试、kas CI 构建、部署与烧录、镜像分析、内核 BSP、recipe 维护、安全 / OTA / SBOM。(coll · ★4 · 2026-07)
- [Higangssh/yocto-agent-skills](https://github.com/Higangssh/yocto-agent-skills) - 以官方文档为准、经 CI 验证的 Yocto Skill：文档路由、BSP 内核、镜像 rootfs、layer 与 recipe 审查、安全 SBOM。(coll · ★9 · 2026-08)
- [Angstrom-distribution/meta-angstrom `skills/`](https://github.com/Angstrom-distribution/meta-angstrom) - `boot-validate` 在全部十二台 oe-core QEMU 机型加上 BeagleBone QEMU 上启动镜像，并断言 systemd 与网络正常。(official · ★51 · 2026-09)
- [processmission/oh-my-qemu](https://github.com/processmission/oh-my-qemu) - 在 QEMU 中建模板卡与外设：U-Boot 构建、Linux 启动、板级与外设建模（17 个 Skill）。(coll · ★57 · 2026-07)
- [angelwzr/linux-phone-porting](https://github.com/angelwzr/linux-phone-porting) - 在安卓手机上做主线 Linux bring-up：设备树、bootloader。(★48 · 2026-09)
- [LittleNewton/openwrt-compile-skills](https://github.com/LittleNewton/openwrt-compile-skills) - OpenWrt 构建执行器、feed 与软件包同步、切换 target 时的清理规范。(coll · ★8 · 2026-05)
- [100askTeam/aibsp-imx6ull-pro_linux5.4.47 `.trae/skills/`](https://github.com/100askTeam/aibsp-imx6ull-pro_linux5.4.47) - 百问网 i.MX6ULL 的 Buildroot / eMMC / LVGL9 / uuu 串口自动烧录 Skill，TRAE 格式。(official · coll · ★12 · 2026-05)
- [realsenseai/realsense_mipi_platform_driver `.claude/skills/`](https://github.com/realsenseai/realsense_mipi_platform_driver) - 在 Jetson 上构建、部署并验证 RealSense MIPI 内核驱动。(official · coll · ★51 · 2026-09)
- [openharmonyinsight/openharmony-skills](https://github.com/openharmonyinsight/openharmony-skills) - OpenHarmony 源码构建、CI、C++、下载、单元测试、安全审查。(coll · ★34 · 2026-09)
- [anthropics/claude-plugins-official `cwc-makers`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/cwc-makers) - `m5-onboard` 通过 USB 识别 M5Stack Cardputer / Core / CoreS3，烧录 UIFlow 2.0 与一套 MicroPython 包；`cardputer-buddy` 通过串口迭代应用并提供一次性 REPL。(official · coll · ★36k · 2026-09)

### 机器人

- [NVIDIA/skills](https://github.com/nvidia/skills) - 从 NVIDIA 各产品仓库镜像而来的 350+ 个 Skill；硬件相关的集群是 `jetson-*`（BSP 定制、pinmux、烧录、内存审计、端侧 LLM 服务）、`hsb-*`（Holoscan Sensor Bridge FPGA 烧录）、`i4h-*`（Isaac for Healthcare 机器人数据采集与强化学习）以及 `physical-ai-*`。(official · coll · ★3.3k · 2026-09)
- [isaac-sim/IsaacSim `.claude/skills/`](https://github.com/isaac-sim/IsaacSim/tree/main/.claude/skills) - Isaac Sim 的 43 个 Skill：无头部署、ROS 2 桥、URDF/MJCF 转 USD、机械臂 IK、导航原语、占据栅格图、数据采集。(official · coll · ★4.1k · 2026-09)
- [isaac-sim/IsaacLab-Arena `skills/`](https://github.com/isaac-sim/IsaacLab-Arena/tree/main/skills) - 搭建 arena、跑实验，并为闭环评测拉起 π0（`serve-openpi-policy`）或 GR00T（`serve-gr00t-policy`）策略服务。(official · coll · ★565 · 2026-09)
- [google-deepmind/mujoco `doc/skills/`](https://github.com/google-deepmind/mujoco/tree/main/doc/skills) - 六个官方 MuJoCo Skill：python、渲染、加速（MJX / Warp）、spec 编辑、GUI、Studio。(official · coll · ★15.1k · 2026-09)
- [AgibotTech/genie_sim `skills/`](https://github.com/AgibotTech/genie_sim/tree/main/source/geniesim_ros/skills) - 智元的八个 Skill：构建工作区、启动场景、MoveIt 全身控制、从 URDF 添加机器人、遥操作桥、录制 episode、物理调试。(official · coll · ★1.4k · 2026-09)
- [pollen-robotics/reachy_mini `skills/`](https://github.com/pollen-robotics/reachy_mini/tree/main/skills) - AGENTS.md 中引用的 13 个官方 Reachy Mini Skill：创建应用、安全力矩、控制循环、符号化运动、REST API、AI 集成。纯 `.md`，无 frontmatter。(official · coll · ★1.5k · 2026-09)
- [NVIDIA-AI-IOT/reachy-mini-jetson-assistant](https://github.com/NVIDIA-AI-IOT/reachy-mini-jetson-assistant) - 在 Orin Nano 上为 Reachy Mini Lite 做本地语音 + 视觉助手，配 `reachy-jetson-deploy` Skill。(official · ★33 · 2026-09)
- [wandelbotsgmbh/wandelbots-nova `nova-api-v2`](https://github.com/wandelbotsgmbh/wandelbots-nova/tree/main/.agents/skills/nova-api-v2) - Wandelbots NOVA 面向 UR / KUKA / FANUC / ABB / 安川的机型无关运动规划：轨迹规划、限位、模型。(official · ★46 · 2026-09)
- [viam-devrel/agent-skills](https://github.com/viam-devrel/agent-skills) - 九个 Viam Skill：机器配置、模块与机队、本地 viam-server、Python / Go / C++ / TS SDK、机器学习、运动与视觉。(official · coll · ★2 · 2026-08)
- [openvinotoolkit/physicalai](https://github.com/openvinotoolkit/physicalai/tree/main/skills) - Intel 在机器人上运行 VLA 策略的运行时：接入新机型、接入相机后端、配置推理流水线。(official · coll · ★27 · 2026-09)
- [OpenRAL/openral](https://github.com/OpenRAL/openral) - "Robot Agentic Layer"：LLM 发出带类型的工具调用，在默认拒绝的 C++ 安全内核之后派发 rSkill（SmolVLA、π0.5、GR00T、OpenVLA-OFT、MoveIt / Nav2 动作）；含 50 个 rSkill 的 SKILL.md，例如 `rskill-smolvla-so101`。(coll · ★44 · 2026-09)
- [harunkurtdev/ros2-claude-code-template](https://github.com/harunkurtdev/ros2-claude-code-template) - 29 个 ROS 2 Skill，其中八个是 Nav2 相关：代价地图、规划器、控制器、行为树、插件开发。(coll · ★214 · 2026-06)
- [arpitg1304/robotics-agent-skills](https://github.com/arpitg1304/robotics-agent-skills) - 生产级 ROS 1/2 实践：QoS、生命周期节点、colcon、DDS、机器人 bring-up、感知、测试、安全、Docker 开发、Web 集成。(coll · ★358 · 2026-08)
- [dbwls99706/ros2-engineering-skills](https://github.com/dbwls99706/ros2-engineering-skills) - 单个渐进式披露的 Skill：rclcpp / rclpy、QoS / DDS、tf2 / URDF、ros2_control、Nav2、MoveIt 2、实时性、硬件安全。(★175 · 2026-09)
- [adityakamath/ros2-skill](https://github.com/adityakamath/ros2-skill) - 面向运行时控制而非代码生成：通过内置 rclpy 脚本在真实机器人上操作 topic、service、action、参数、生命周期、ros2_control 与 Nav2。(★18 · 2026-07)
- [j3soon/ros2-essentials `.agents/skills/`](https://github.com/j3soon/ros2-essentials) - 面向 AMR 的 TurtleBot3 与 Gazebo 工作区测试 Skill。(coll · ★47 · 2026-07)
- [zh-plus/unitree-g1-dev-copilot](https://github.com/zh-plus/unitree-g1-dev-copilot) - 有文档依据的宇树 G1 Skill：SDK2、DDS、ROS 2、高层与底层运动、D435i 头部相机；自带 `evals/`。(★6 · 2026-07)
- [earthtojake/text-to-cad `urdf` / `srdf` / `sdf`](https://github.com/earthtojake/text-to-cad/tree/main/skills/urdf) - CAD/CAM Skill 库中的机器人描述格式，该库还覆盖 G-code 与拓竹打印机。(coll · ★15.8k · 2026-09)
- [rerun-io/rerun `rerun-lerobot`](https://github.com/rerun-io/rerun/tree/main/skills/rerun-lerobot) - 在 Rerun 中可视化 LeRobot 数据集；同系列还有 `rerun-urdf` 与 `rerun-mcap`。(official · ★11.4k · 2026-09)
- [Flaminis/Dalaran](https://github.com/Flaminis/Dalaran) - Rerun 的替代品，机器人可视化与数据基础设施，带 `dalaran-lerobot` 与 `dalaran-mcap` Skill。(coll · ★777 · 2026-08)
- [nebius/nebius-physical-ai](https://github.com/nebius/nebius-physical-ai) - 38 个与云绑定的 Skill：LeRobot、GR00T、Isaac Lab、Genesis、mjlab、cuRobo、Foxglove、RoboCasa、动作重定向。(official · coll · ★29 · 2026-09)
- [aws-samples/sample-embodied-ai-platform `training/gr00t`](https://github.com/aws-samples/sample-embodied-ai-platform) - 用遥操作数据微调 GR00T 并部署到 SO-101 机械臂。(official · ★15 · 2026-09)
- [NVlabs/RoboLab](https://github.com/NVlabs/RoboLab) - 面向策略评测的场景生成与任务生成 Skill；姊妹项目 [GraspGenX](https://github.com/NVlabs/GraspGenX) 提供抓取生成 Skill。(official · coll · ★501 · 2026-09)
- [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) - 大型通用科研 Skill 库中的 `openpi`、`openvla-oft`、`cosmos-policy` 与 `tensorrt-llm`。(coll · ★12.7k · 2026-06)
- [ForgeCAD/forgecad-public-kit `forgecad-verify-mujoco`](https://github.com/ForgeCAD/forgecad-public-kit) - 在 MuJoCo 中验证由 CAD 生成的机器人。(★934 · 2026-06)
- [wimblerobotics/ros2-copilot-skills](https://github.com/wimblerobotics/ros2-copilot-skills) - 面向 Copilot 的 158 个 Nav2 / 行为树 / SLAM / Teensy-PlatformIO Skill；质量参差。(coll · ★18 · 2026-04)
- [robium-ai/robium](https://github.com/robium-ai/robium) - ROS 2 / Nav2 / Gazebo / MuJoCo / Isaac / LeRobot 插件，带版本化的 SKILL.md 归档。(coll · ★13 · 2026-09)
- [PatrickJS/awesome-cursorrules `ros-ros2`](https://github.com/PatrickJS/awesome-cursorrules/blob/main/rules/ros-ros2.mdc) - 面向 ROS / ROS 2 包、节点、launch 文件、消息与 URDF/xacro 的 Cursor rule。(cursor-rules · ★40.8k · 2026-05)

### 无人机

- [PX4/PX4-Autopilot `build-px4`](https://github.com/PX4/PX4-Autopilot/tree/main/.agents/skills/build-px4) - 在 px4-dev 容器内构建 PX4 板级固件，支持 worktree；不负责烧录。(official · ★12.6k · 2026-09)
- [fossuav/aap](https://github.com/fossuav/aap) - "ArduPilot AI Playbooks"：面向 Claude、Codex 与 Gemini 的构建、SITL 与 Lua 脚本 Skill。(coll · ★19 · 2026-09)
- [pelageech/ardupilot-agent-toolkit](https://github.com/pelageech/ardupilot-agent-toolkit) - 七个 ArduPilot Skill：直接控制、SITL、Gazebo Harmonic、pymavlink、Pixhawk 6C、任务规划、飞行诊断。(coll · ★0 · 2026-09)
- [raylanlin/smarttune-cli](https://github.com/raylanlin/smarttune-cli) - 面向 ArduPilot、Betaflight 与 PX4 的飞行日志调参顾问，同时提供 Skill 与 MCP。(★29 · 2026-09)
- [SebGalina/betaflight-claude-skill](https://github.com/SebGalina/betaflight-claude-skill) - Betaflight 配置、PID 调参、黑匣子分析、排障；作者的 `betaflight-mcp` 通过 USB 走 MSP 协议。(★29 · 2026-09)
- [sensei-hacker/inav-claude](https://github.com/sensei-hacker/inav-claude) - iNAV 飞控开发流程，含一个硬件在环链路测试 Skill。(coll · ★4 · 2026-09)
- [MIUAV/vibe-coding-ros2](https://github.com/MIUAV/vibe-coding-ros2) - PX4 + ROS 2 Humble 无人机开发：MAVLink、offboard 模式、固件构建、模块开发、机架、传感器配置、多旋翼调参、视觉导航、RKNN。中文。(coll · ★26 · 2026-05)
- [castacks/AirStack](https://github.com/castacks/AirStack) - CMU AirLab 的"Agent 原生" ROS 2 空中自主栈，带 `.agents/skills`。(★91 · 2026-09)

### 航空航天

- [esa/nanosat-mo-framework](https://github.com/esa/nanosat-mo-framework) - 欧空局的 CCSDS 任务运行飞行软件框架，带一个用于编写服务定义的 `mo-xml` Skill。目前找到的唯一由航天机构官方发布的 Agent Skill。(official · ★123 · 2026-09)
- [devideamax/aerospace-team](https://github.com/devideamax/aerospace-team) - 十二个卫星任务 Skill：制导导航控制、电源系统、卫星通信、地面系统与发射运行。(coll · ★21 · 2026-02)

### 边缘 AI / NPU

- [hailo-ai/hailo-apps `.claude/skills/`](https://github.com/hailo-ai/hailo-apps/tree/main/.claude/skills) - 十二个 Hailo Skill：相机、构建流水线 / LLM / VLM / 语音 / Agent 应用、模型管理、监控、校验。(official · coll · ★500 · 2026-04)
- [hailo-ai/hailo_model_zoo `.claude/skills/`](https://github.com/hailo-ai/hailo_model_zoo/tree/master/.claude/skills) - 面向 Dataflow Compiler 工具链的 `hailo-parse`、`hailo-optimize`、`hailo-compile`。(official · coll · ★708 · 2026-09)
- [hailo-ai/hailo15-agentic-coding](https://github.com/hailo-ai/hailo15-agentic-coding) - Hailo-15 视觉处理器的十二个 Skill 与 agent：连接、板卡状态、换模型、交叉编译、部署到板子——闭合了"烧录 → 运行"回路。(official · coll · ★0 · 2026-06)
- [HorizonRobotics/OE-Skills](https://github.com/HorizonRobotics/OE-Skills) - 地平线 HBDK 编译、HMCT 量化、UCP 板上推理与 LLM 压缩的 37 个 Skill。(official · coll · ★19 · 2026-07)
- [D-Robotics/rdk-device-skills](https://github.com/D-Robotics/rdk-device-skills) - 26 个端侧 RDK Skill（诊断、内存审计、相机、BPU 模型部署与跑分、GPIO、TROS）；同系列还有 `oe-skills-x5`、`bsp-skills` 与 `rdk-docs-mcp`。(official · coll · ★2 · 2026-09)
- [luxonis/skills](https://github.com/luxonis/skills) - OAK 相机路由 Skill 加七个专项（应用、设备配置、检查、模型、录制、排障、工作区），配 MCP 配置与 `oakctl`。(official · coll · ★16 · 2026-09)
- [PyTorch ExecuTorch `.claude/skills/`](https://github.com/pytorch/executorch/tree/main/.claude/skills) - 九个 ExecuTorch Skill：导出、构建、Cortex-M、Zephyr、高通、性能分析、二进制体积、知识库。(official · coll · ★5k · 2026-09)
- [google-ai-edge/litert-samples `skills/`](https://github.com/google-ai-edge/litert-samples/tree/main/skills) - 六个 LiteRT Skill：转换流程、保精度量化、GPU 干净转换、端侧验证。(official · coll · ★431 · 2026-09)
- [Dengdxx/PaddleYOLO-RKNN `rknn-flow`](https://github.com/Dengdxx/PaddleYOLO-RKNN) - 瑞芯微 RKNN 模型转换流程。中文。(★8 · 2026-08)
- [gregm123456/raspberry_pi_hailo_ai_services](https://github.com/gregm123456/raspberry_pi_hailo_ai_services) - 树莓派 5 + Hailo AI HAT 服务，带一个 Copilot Skill。(copilot · ★11 · 2026-09)

### EDA / PCB

- [aklofas/kicad-happy](https://github.com/aklofas/kicad-happy) - 分析 KiCad 工程与 PDF 原理图、DRC / ERC / DFM、EMC 预兼容、SPICE、在 DigiKey / Mouser / 立创 / element14 上选料、JLCPCB 与 PCBWay 制板准备。(coll · ★1.2k · 2026-09)
- [autodesk-platform-services/skills](https://github.com/autodesk-platform-services/skills) - Autodesk 官方面向 AutoCAD ARX 与 Autodesk Platform Services API 的 Skill；属 CAD 而非硬件，也是找到的最大厂商 Skill 仓库。(official · ★46 · 2026-08)
- [easyeda/easyeda-api-skill](https://github.com/easyeda/easyeda-api-skill) - 嘉立创 EDA 专业版：120+ 个 API 类，外加一座通往运行中客户端的 WebSocket 桥。(official · ★708 · 2026-09)
- [zhoushoujianwork/easyeda-agent](https://github.com/zhoushoujianwork/easyeda-agent) - 通过本地 CLI / 守护进程驱动嘉立创 EDA 专业版：原理图、网表检查、PCB 布局布线、DRC、制造文件导出；同时提供 CLI + Skill + MCP。(★438 · 2026-09)
- [diodeinc/pcb](https://github.com/diodeinc/pcb/tree/main/skills) - Zener 代码转 PCB 语言，外加 `datasheet-reader`、`librarian`、元件库检索与 SPICE 仿真 Skill。(coll · ★448 · 2026-09)
- [atopile/atopile `.claude/skills/`](https://github.com/atopile/atopile/tree/main/.claude/skills) - 用代码定义 PCB 设计；`ato` 与 `ato-language` 面向用户，其余是编译器 / 求解器 / 库的贡献者 Skill。(coll · ★3.9k · 2026-06)
- [American-Embedded/kistack](https://github.com/American-Embedded/kistack) - 人工编写的 KiCad Skill 栈：原理图、符号、封装、PCB 布局、Gerber、拼板、BOM、导出、产品渲染。(coll · ★383 · 2026-09)
- [drandyhaas/KiCadRoutingTools](https://github.com/drandyhaas/KiCadRoutingTools) - `plan-pcb-routing` 从 `.kicad_pcb` 生成扇出与差分对布线方案。(★428 · 2026-09)
- [Seeed-Studio/ai-skills](https://github.com/Seeed-Studio/ai-skills) - `schematic-analyzer` 追踪 KiCad 与 OrCAD/Allegro 原理图；`ee-datasheet-master` 从 PDF 中提取引脚图、I2C 地址与寄存器映射；另有 SG200x/CV181x 多媒体与 ONNX 转 cvimodel 的 Skill。(official · coll · ★25 · 2026-09)
- [Tansuo2021/ADtoKeil](https://github.com/Tansuo2021/ADtoKeil) - 把 Altium 原理图当作依据读取，为其描述的板子生成 Keil 固件，再通过串口验证。仅 Windows。(coll · ★172 · 2026-06)
- [oaslananka/kicad-mcp-pro](https://github.com/oaslananka/kicad-mcp-pro/tree/main/skills) - 架在 KiCad MCP 之上的 `pcb-design` 与 `kicad-design-review`：布局、布线、叠层、质量门禁。(coll · ★91 · 2026-09)
- [Zane456/PCB-Agent-Teams](https://github.com/Zane456/PCB-Agent-Teams) - 从拓扑到 Gerber 的多 Agent KiCad 流水线，带高压 / 低压 / 隔离分区。(coll · ★66 · 2026-07)
- [Cognitohazard/ltspice-mcp](https://github.com/Cognitohazard/ltspice-mcp) - LTspice 与 ngspice 的 MCP，配 `ltspice`、`ngspice`、`spice-bench-craft` 与 `spice-experiments` Skill。(coll · ★43 · 2026-09)
- [Arcadia-1/gmoverid-skill](https://github.com/Arcadia-1/gmoverid-skill) - 基于 ngspice 与 SKY130 / PTM 模型的模拟 IC 设计：gm/ID、晶体管模型、LDO / 运放 / 比较器；同系列还覆盖 Verilog-A 与一套 Razavi 基准。(coll · ★122 · 2026-07)
- [SpiceSharp/SpiceSharpParser `.agents/skills/`](https://github.com/SpiceSharp/SpiceSharpParser) - 以测试驱动的方式设计网表，用 `.MEAS` 做验证。(official · ★33 · 2026-08)
- [fireostendere/mcp_diptrace](https://github.com/fireostendere/mcp_diptrace) - DipTrace MCP 加一个信号完整性审查 Skill。(★22 · 2026-09)
- [akiselev/altium-cli `.agents/skills/`](https://github.com/akiselev/altium-cli) - 处理 SchDoc / PcbDoc / 元件库的 Rust CLI，带校验、规则审查、数据审查与 GUI 控制 Skill。(coll · ★14 · 2026-08)
- [l3wi/claude-eda](https://github.com/l3wi/claude-eda) - 面向 KiCad 的 `eda-architect`、`eda-schematics`、`eda-pcb`、`eda-drc`、`eda-research`。(coll · ★15 · 2026-01)
- [pjcau/esp32-emu-turbo `.claude/skills/`](https://github.com/pjcau/esp32-emu-turbo) - 唯一一套真正驱动 JLCPCB DFM 工具的 Skill：上传、校验、PCB 审查、PCBA 就绪度检查。(coll · ★4 · 2026-09)

### FPGA / HDL

- [Shinei-Nouzen-Arch/FPGA-Agent](https://github.com/Shinei-Nouzen-Arch/FPGA-Agent) - 最好的 Vivado / Vitis Skill 集：综合、实现、仿真、Tcl、约束、调试、分析、借助 RapidWright 做时序收敛。(coll · ★170 · 2026-09)
- [hdl-tools/digital-chip-design-agents](https://github.com/hdl-tools/digital-chip-design-agents) - 覆盖芯片全流程的 16 个插件：RTL、验证、综合、静态时序分析、物理设计、可测试性设计、FPGA、高层次综合、形式验证；姊妹项目 `analog-chip-design-agents`。(coll · ★203 · 2026-09)
- [Eriemon/verilog-generator](https://github.com/Eriemon/verilog-generator) - 可读的 Verilog-2001 生成、审查与注释、testbench 脚手架、本地或远程 Vivado。(★282 · 2026-08)
- [Mindrally/skills `fpga` / `systemverilog`](https://github.com/Mindrally/skills) - 由 Cursor rule 演化而来的 FPGA 与 SystemVerilog Skill，各约 1000 次安装。(★259 · 2026-09)
- [codejunkie99/Gateflow-Plugin](https://github.com/codejunkie99/Gateflow-Plugin) - 在开源工具链上完成 SystemVerilog 设计 → 验证（cocotb、形式化）→ 交付，带 FuseSoC 与 IP 打包。(coll · ★113 · 2026-05)
- [one-ware/OneWare](https://github.com/one-ware/OneWare) - ONE WARE Studio 内用于 Yosys / nextpnr 的 `fpga-toolchain-yosys`。(official · ★143 · 2026-09)
- [a2fpga/a2fpga_core `.claude/skills/`](https://github.com/a2fpga/a2fpga_core) - 高云 Tang Nano 20K 比特流构建与烧录，外加 BL616 MCU 烧录。(coll · ★75 · 2026-08)
- [TONGJI-EDA-LAB/RTL-CLAW](https://github.com/TONGJI-EDA-LAB/RTL-CLAW) - OpenClaw 上的学术向 Verilog 划分 / 优化（Yosys + Verible）/ 合并 Skill。(coll · ★64 · 2026-04)
- [bjwanneng/veriflow-cc](https://github.com/bjwanneng/veriflow-cc) - 架构 → RTL → iverilog / Yosys 流水线，带 cocotb 覆盖率。(★51 · 2026-08)
- [LilithSemi/claude-for-hardware](https://github.com/LilithSemi/claude-for-hardware) - 唯一一套涉及物理 bring-up 的 FPGA 合集：用树莓派模拟 JTAG 下载比特流、综合适配、面积 / 时序、裸机启动链、ROHD 的坑。(coll · ★21 · 2026-08)
- [a5c-ai/babysitter `fpga-programming`](https://github.com/a5c-ai/babysitter/tree/main/library/specializations/fpga-programming/skills) - 19 个短 Skill：Verilog / SV / VHDL、时序约束、跨时钟域、SVA、UVM、高层次综合、布局布线、综合、调试。(coll · ★1.8k · 2026-09)
- [wweiyi2004/minifpga-quartus-skill](https://github.com/wweiyi2004/minifpga-quartus-skill) - Quartus Cyclone IV 的 Codex Skill；唯一一个有实际使用量的 Quartus Skill。(★8 · 2026-06)
- [Tomer-Harari/claude-fpga-skills](https://github.com/Tomer-Harari/claude-fpga-skills) - 无头的厂商流程：Vivado 批处理、ModelSim 无头运行、cocotb testbench、跨时钟域形式验证、时序收敛、AXI-Stream 验证。(coll · ★1 · 2026-08)
- [londey/claude-skill-verilog](https://github.com/londey/claude-skill-verilog) - 一个可用的 Verilog Skill。(★18 · 2026-04)

### 无线

- [simpleble/simpleble `simpleaible`](https://github.com/simpleble/simpleble/tree/main/simpleaible) - SimpleBLE 官方的 MCP 与 Skill：从主机侧扫描、连接、GATT 读取与订阅。(official · ★1.1k · 2026-09)
- [meshtastic/meshtastic-mcp](https://github.com/meshtastic/meshtastic-mcp) - Meshtastic 官方 MCP，内置三个 Skill：通过串口 / TCP 发现、配置、烧录与监控电台，端到端测试，模拟器。(official · coll · ★15 · 2026-09)
- [project-chip/connectedhomeip `.agents/skills/`](https://github.com/project-chip/connectedhomeip/tree/master/.agents/skills) - 14 个 Matter SDK 贡献者 Skill：ZAP cluster 生成、代码驱动的 cluster TDD、chip-tool 测试、二进制体积对比。(official · coll · ★8.9k · 2026-09)
- [SmartThingsCommunity/SmartThingsEdgeDrivers `.agents/skills/`](https://github.com/SmartThingsCommunity/SmartThingsEdgeDrivers/tree/main/.agents/skills) - 三星官方用于编写 Zigbee / Z-Wave / Matter Lua edge driver 的 Skill：profile、库、测试流程。(official · coll · ★346 · 2026-09)
- [zwave-js/zwave-js `.agents/skills/`](https://github.com/zwave-js/zwave-js) - `author-config-from-web` 根据产品页面生成 Z-Wave 设备配置文件。(official · ★887 · 2026-09)
- [BrownFineSecurity/iothackbot](https://github.com/BrownFineSecurity/iothackbot) - 带物理工具的 IoT 渗透测试：JTAG 探测、逻辑分析仪 / MSO 抓取、picocom 串口控制台、telnet shell、chipsec、ONVIF 与网络扫描、jadx / apktool。(coll · ★841 · 2026-06)
- [BasedHardware/omi `.cursor/skills/`](https://github.com/BasedHardware/omi) - Omi 可穿戴设备 nRF / ESP32 Zephyr 蓝牙音频固件的 `omi-firmware-patterns`。(cursor-rules · ★7.6k · 2026-09)
- [veonua/SmartThingsEdge-Xiaomi `.agents/skills/`](https://github.com/veonua/SmartThingsEdge-Xiaomi) - SmartThings Edge driver 的 Zigbee 设备入网。(★82 · 2026-09)
- [ksachdeva/zephyr-rtos-ai `zephyr-bluetooth-le`](https://github.com/ksachdeva/zephyr-rtos-ai/tree/main/skills/zephyr-bluetooth-le) - Zephyr 中的 GAP / GATT / 广播 / 配对 / NUS。(★23 · 2026-06)
- [beriberikix/zephyr-agent-skills `connectivity-ble`](https://github.com/beriberikix/zephyr-agent-skills/tree/main/skills/connectivity-ble) - Zephyr BLE，以及覆盖 MQTT / CoAP / LwM2M 的姊妹 Skill `iot-protocols`。(★64 · 2026-05)
- [wangjianjq/Skill `.agents/skills/`](https://github.com/wangjianjq/Skill) - 用 Python 与 Wireshark 做蓝牙调试，另有一个泰克示波器 Skill。(coll · ★24 · 2026-02)
- [rnd-southerniot/rak3112-rs485-node `.claude/skills/`](https://github.com/rnd-southerniot/rak3112-rs485-node) - 在 ChirpStack 中为 RAK3172 / RAK3112 做 LoRaWAN OTAA 入网、注销与入网校验。(coll · ★1 · 2026-07)
- [JasonYANG170/esp-dev-skill `esp-zigbee-sdk`](https://github.com/JasonYANG170/esp-dev-skill/tree/main/repos/esp-zigbee-sdk) - ESP Zigbee SDK 子 Skill。(★27 · 2026-08)
- [SnailSploit/Claude-Red `Skills/wireless`](https://github.com/SnailSploit/Claude-Red) - 攻击向的 BLE、LoRaWAN / sub-GHz、Zigbee / Thread / Matter 与 Z-Wave Skill；仅安全侧。(coll · ★5.1k · 2026-08)

### 硬件安全

- [solokeys/solo2](https://github.com/solokeys/solo2) - Solo 2 FIDO2 安全密钥固件，附带用于给密钥本身做量产配置的 `solo2-cli` 与 `solo2-examples` Skill。(official · coll · ★713 · 2026-08)
- [dslsdzc/rev-skills](https://github.com/dslsdzc/rev-skills) - 122 个逆向工程 Skill，含面向 UART、SPI、JTAG 的 `re-hardware-io` 与 `re-javacard`。(coll · ★58 · 2026-09)
- [keycard-tech/keycard-cli](https://github.com/keycard-tech/keycard-cli) - Keycard 智能卡 CLI，带 `keycard-admin` 与 `keycard-signing` Skill。(official · coll · ★57 · 2026-09)
- [nemanjan00/claude-code-skills](https://github.com/nemanjan00/claude-code-skills) - 一套很小的个人合集，恰好收录了目前仅有的 Bus Pirate 与智能卡 Skill。(coll · ★0 · 2026-08)

### 汽车

- [CSS-Electronics/can-bus-reverse-engineering-skills](https://github.com/CSS-Electronics/can-bus-reverse-engineering-skills) - 三个 Skill，用 CANsub USB / 以太网接口在真实 OBD2 口上把实时 CAN 流量逆向成 DBC 文件。(official · coll · ★168 · 2026-08)
- [ecubus/EcuBus-Pro `resources/skills/`](https://github.com/ecubus/EcuBus-Pro/tree/master/resources/skills) - EcuBus-Pro 的 TypeScript 脚本 API（UDS、CAN-TP、DoIP、LIN、总线事件），配合其自家 USB CAN / LIN 适配器。(official · ★871 · 2026-09)
- [philipkocanda/canair](https://github.com/philipkocanda/canair) - WiCAN OBD-II Wi-Fi / 蓝牙 dongle 工具箱，带信号逆向与 WiCAN 协议 Skill。(coll · ★25 · 2026-08)
- [spawahh/openpilot-claude-kit](https://github.com/spawahh/openpilot-claude-kit) - 四个面向 openpilot 的 Claude Code 插件，含只读的 comma 设备 API 与 SSH 设备操作。(coll · ★1 · 2026-08)
- [JiaxI2/Codex-Skills `ethercat-cia402`](https://github.com/JiaxI2/Codex-Skills) - EtherCAT 从站 / CiA 402 / TwinCAT NC 诊断。中文。(★1 · 2026-09)

### 工业 / PLC

- [bulaofen0036-coder/TIA_Portal_Openness_MCP](https://github.com/bulaofen0036-coder/TIA_Portal_Openness_MCP) - 西门子博途 V20 / V21：通过 MCP 创建、编译并下载 STEP 7 与 WinCC 工程，内置一个 Skill。(★241 · 2026-09)
- [Czarnak/totally-integrated-claude](https://github.com/Czarnak/totally-integrated-claude) - 带路由的博途 Openness 插件（20+ 个 Skill）：PLC 操作、导入导出、网络组态、HMI、Python、MAC 模块生成。(coll · ★61 · 2026-08)
- [huahaizo/tia-portal-openness-ai](https://github.com/huahaizo/tia-portal-openness-ai) - 博途 Openness V15–V21 的 C# / PowerShell 脚手架。(★65 · 2026-05)
- [MichielVanwelsenaere/HomeAutomation.CoDeSys3 `.claude/skills/`](https://github.com/MichielVanwelsenaere/HomeAutomation.CoDeSys3) - 通过 ScriptEngine 无头运行 CODESYS：对二进制 `.project` 做编译检查、排查 PLC 异常。(coll · ★147 · 2026-09)
- [ArthurkaX/cds-text-sync](https://github.com/ArthurkaX/cds-text-sync) - CODESYS 与结构化文本的双向同步 CLI，带 IDE 守护进程与 PLC 下载，另有一个 visu-SVG Skill。(coll · ★95 · 2026-09)
- [midea-ai/SemaPLC](https://github.com/midea-ai/SemaPLC) - 美的的 Agent 化 PLC IDE，带 `plc-spec-review` Skill。(official · ★83 · 2026-09)
- [MIGO-OvO/plc-skill](https://github.com/MIGO-OvO/plc-skill) - 厂商中立的 IEC 61131-3 ST / LD / FBD / SFC，带厂商路由；ClawHub 约 1000 次安装。(★23 · 2026-05)
- [Navifra-Sally/vda5050-skill](https://github.com/Navifra-Sally/vda5050-skill) - VDA 5050 AGV 与 AMR 机队协议：规范要点、JSON schema 与消息校验器。(★0 · 2026-09)
- [eponce00/twincat-mcp](https://github.com/eponce00/twincat-mcp) - 通过 MCP 完成 TwinCAT 3 构建、部署、TcUnit 与 ADS 检视。(★29 · 2026-09)
- [TechIndustryX/twincat-agent](https://github.com/TechIndustryX/twincat-agent) - TwinCAT 结构化文本规约，外加一个 MCP 可执行程序。(coll · ★28 · 2026-06)
- [SionVerhoef/twincat-st](https://github.com/SionVerhoef/twincat-st) - TwinCAT 3 / CODESYS 结构化文本，带可执行的 `st_review.py`（阻塞循环、浮点相等判断）。(★1 · 2026-09)
- [FREEZONEX/ia2](https://github.com/FREEZONEX/ia2) - Agent 优先的 IEC 61131-3 IDE 与运行时，支持 Modbus、EtherCAT、OPC UA、CANopen 与 HMI。(★4 · 2026-09)
- [gmantoha/ctrlx-os-agent-skills](https://github.com/gmantoha/ctrlx-os-agent-skills) - 博世力士乐 ctrlX OS / CORE snap、Data Layer、PLC。(★6 · 2026-09)
- [Meisterschulen-am-Ostbahnhof-Munchen/4diac_training1 `.agents/skills/`](https://github.com/Meisterschulen-am-Ostbahnhof-Munchen/4diac_training1) - 面向 Eclipse 4diac 的 IEC 61499 功能块、适配器与系统。(★1 · 2026-09)
- [OPCFoundation/UA-.NETStandard `.agents/skills/`](https://github.com/OPCFoundation/UA-.NETStandard) - OPC 基金会 .NET 协议栈的 `opcua-v20-migration`。(official · ★2.4k · 2026-09)
- [riclolsen/json-scada `.agents/skills/`](https://github.com/riclolsen/json-scada) - 为 JSON-SCADA 增加 Modbus / DNP3 / IEC 60870 / IEC 61850 驱动的 `protocol-driver-development`。(official · ★423 · 2026-08)
- [studioxvii/modbus-skills](https://github.com/studioxvii/modbus-skills/tree/main/plugins/modbus-skills/skills) - 20 个只读的 Modbus 工程 Skill：从原厂 PDF 提取寄存器表、归一化、校验字节序、规划读取、生成 modpoll / ModScan / Node-RED 工具包、分析抓包。(coll · ★1 · 2026-09)
- [wirenboard/wb-ai-skills](https://github.com/wirenboard/wb-ai-skills) - Wiren Board PLC 厂商 Skill：通过 MQTT 与 Modbus 与控制器通信、编写 wb-rules、管理 Zigbee 与串口设备、根因分析。(official · coll · ★3 · 2026-09)
- [TuojianLYU/openplc-codex-skill](https://github.com/TuojianLYU/openplc-codex-skill) - 生成带梯形图 `.ld` 文件的 OpenPLC v4 工程。(★1 · 2026-06)

### 专业 AV 与楼宇系统

- [shorty456132/av-module-maker](https://github.com/shorty456132/av-module-maker) - 生成 Q-SYS、Extron 与 Crestron 控制模块，带 SIMPL+、SIMPL# 与 SIMPL# Pro Skill。(coll · ★9 · 2026-09)
- [Crestron/CrestronAISkills](https://github.com/Crestron/CrestronAISkills) - Crestron 官方面向 AV 控制编程的 Skill 插件与 Copilot 版本；唯一发布 Skill 的专业 AV 厂商。(official · coll · ★4 · 2026-09)

### 实验室仪器

- [nominal-io/instro](https://github.com/nominal-io/instro) - 带类型的多厂商仪器库（电源、万用表、示波器、数采、电子负载），其 Skill 负责生成新驱动并在真实仪器上验证。(official · coll · ★704 · 2026-09)
- [ma-compbio-lab/SkillFoundry](https://github.com/ma-compbio-lab/SkillFoundry) - 科研 Agent 的 Skill 框架，其 `qcodes-parameter-sweep-starter` 是找到的唯一 QCoDeS 参数扫描 Skill。(coll · ★39 · 2026-09)
- [RRGGZZ/Zurich_Instruments_Skills](https://github.com/RRGGZZ/Zurich_Instruments_Skills) - 苏黎世仪器 MFLI 锁相放大器。(★1 · 2026-07)
- [jetperch/pyjoulescope_ui `ui-remote`](https://github.com/jetperch/pyjoulescope_ui/tree/main/.claude/skills/ui-remote) - 通过 TCP 远程控制接口驱动 Joulescope 功耗分析仪的界面。(official · ★109 · 2026-08)
- [Scaxlibur/WaveBench](https://github.com/Scaxlibur/WaveBench) - SCPI 台式仪器 Skill 集。(★62 · 2026-08)
- [Erlla/DS1202ZE-skills](https://github.com/Erlla/DS1202ZE-skills) - 通过 USBTMC 操作普源 DS1202Z-E 示波器，配 Python CLI；姊妹项目 `DM3058E-skills` 对应万用表。(★1 · 2026-07)
- [K-Dense-AI/scientific-agent-skills `opentrons-integration`](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/opentrons-integration) - 面向真实 OT-2 / Flex 机器人编写 Opentrons Protocol API v2，位于一个非常大的通用科研 Skill 库中（星数是整库的）。(★45k · 2026-09)
- [KRATSZ/labscriptai-ot](https://github.com/KRATSZ/labscriptai-ot) - Opentrons 插件：MCP server、七个 Skill、安全策略、协议库。(coll · ★2 · 2026-07)
- [DCC-Lab/PyHardwareLibrary](https://github.com/DCC-Lab/PyHardwareLibrary) - USB / 串口实验设备库（光谱仪、位移台、激光器、数采），带一个编写驱动的 Skill。(★12 · 2026-08)
- [deepmodeling/Uni-Lab-OS](https://github.com/deepmodeling/Uni-Lab-OS) - 自动化实验室平台，带 AGENTS.md 与一个 `add-device` Cursor Skill。(cursor-rules · ★177 · 2026-09)

### 数字制造

- [codeofaxel/Kiln](https://github.com/codeofaxel/Kiln) - 一个覆盖 OctoPrint、Moonraker、拓竹、Prusa Link、Elegoo、Duet 与 Marlin 的 3D 打印 MCP，外加无头的 PrusaSlicer / Orca / 拓竹切片；`pip install kiln3d`，附带 SKILL.md。(★57 · 2026-09)
- [earthtojake/text-to-cad `bambu-labs` / `gcode`](https://github.com/earthtojake/text-to-cad/tree/main/skills/bambu-labs) - 拓竹打印机控制与 G-code 生成；`bambu-labs` 在 skills.sh 上约 6700 次安装。(★15.8k · 2026-09)
- [santiagomoneta/3d-printing-skills](https://github.com/santiagomoneta/3d-printing-skills) - 通过 Moonraker API 做 Klipper 配置、诊断与校准，外加 OrcaSlicer。(coll · ★4 · 2026-03)
- [George-RD/cli-anything-meerk40t](https://github.com/George-RD/cli-anything-meerk40t) - 封装真实的 MeerK40t 内核（GRBL / 睿达 / 力辉宇），由 Agent 无头驱动激光任务。(★2 · 2026-08)
- [jl-codes/laser-skills](https://github.com/jl-codes/laser-skills) - LightBurn 设计、预检与任务 Skill；只做设计，绝不真正出光。(coll · ★0 · 2026-08)
- [Lordgrimz/escpos-skill](https://github.com/Lordgrimz/escpos-skill) - 依据官方规范逐字节生成热敏小票打印机的 ESC/POS 指令流。(★0 · 2026-04)
- [johncattrall/keymap-ai](https://github.com/johncattrall/keymap-ai) - 审查并生成 ZMK / QMK 键位映射（home-row mods、层）。(★22 · 2026-08)

### 智能家居

- [home-assistant/core `.claude/skills/`](https://github.com/home-assistant/core/tree/dev/.claude/skills) - 用于编写 Home Assistant 集成的 `ha-integration-knowledge`、`ha-quality-scale-verify`、`ha-review`。(official · coll · ★90k · 2026-09)
- [komal-SkyNET/claude-skill-homeassistant](https://github.com/komal-SkyNET/claude-skill-homeassistant/tree/main/skills/home-assistant-manager) - 通过 API 管理 Home Assistant：新版自动化 YAML（2024.10+）、仪表盘、应用变更前的校验流程。(★957 · 2026-07)
- [homeassistant-ai/skills `home-assistant-best-practices`](https://github.com/homeassistant-ai/skills/tree/main/skills/home-assistant-best-practices) - 自动化、辅助实体、脚本、仪表盘、蓝图；skills.sh 上安装量最高的硬件相关 Skill（约 7000 次）。(★746 · 2026-09)
- [tuya/tuya-openclaw-skills](https://github.com/tuya/tuya-openclaw-skills) - `tuya-smart-control` 通过 tuya.ai 密钥在 OpenClaw 中控制涂鸦设备（云端侧）。(official · ★510 · 2026-04)
- [jtenniswood/espcontrol `.agents/skills/`](https://github.com/jtenniswood/espcontrol) - `flash-displays` 负责通过 ESPHome OTA 与 USB 烧录 ESP32 屏幕板。(★1k · 2026-09)
- [bradsjm/hassio-addons](https://github.com/bradsjm/hassio-addons) - 通过加载项发布的七个 HA Skill：自动化脚本、仪表盘卡片、实体与服务、ESPHome、集成、自定义集成、AWTRIX。(coll · ★45 · 2026-07)
- [nodnarbnitram/claude-code-extensions `esphome-config-helper`](https://github.com/nodnarbnitram/claude-code-extensions) - ESPHome YAML 的生成、校验与排障。(★16 · 2026-04)

## MCP server 与桥接

Agent 在运行时调用的工具服务器。目前对这个领域最好的综述是 Veecle 在 2026 年 8 月发布的两篇评测（链接见"论文与文章"）；beriberikix/awesome-mcp-hardware（见"相关列表"）是本节最初的上游来源。

### MCU / 嵌入式（MCP）

- [78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) - 基于 MCP 的 ESP32 语音 AI 聊天机器人固件：设备把自身的工具暴露给大模型。配套 [xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server)（★10.6k）。(★29.9k · 2026-09)
- [horw/esp-mcp](https://github.com/horw/esp-mcp) - ESP-IDF 构建、烧录与自动修复构建错误。(★157 · 2025-12)
- [golioth/tinymcp](https://github.com/golioth/tinymcp) - 让大模型通过经 Golioth 云端 RPC 代理的 MCP 控制受限嵌入式设备。实验性质。(official · ★157 · 2025-07)
- [jl-codes/platformio-mcp](https://github.com/jl-codes/platformio-mcp) - 在 PlatformIO 支持的 1000+ 块板子上构建、上传与监视。(★51 · 2026-09)
- [shieldyguy/stm32-mcp](https://github.com/shieldyguy/stm32-mcp) - 通过 SWD 与串口构建、烧录并与 STM32 通信。(★25 · 2026-08)
- [espressif/esp-rainmaker-mcp](https://github.com/espressif/esp-rainmaker-mcp) - 通过 RainMaker CLI 控制 ESP RainMaker 设备。(official · ★18 · 2025-07)
- [hardware-mcp/arduino-mcp-server](https://github.com/hardware-mcp/arduino-mcp-server) - 封装 arduino-cli：编译、上传、串口会话。(★17 · 2026-08)
- [Oliver0804/arduino-cli-mcp](https://github.com/Oliver0804/arduino-cli-mcp) - 面向 VS Code / Claude 的 Arduino CLI：编译、上传、库管理。(★13 · 2026-05)
- [Volt23/mcp-arduino-server](https://github.com/Volt23/mcp-arduino-server) - Arduino CLI 桥：草图、板型、库与文件管理。(★10 · 2026-01)
- [SWITCHSCIENCE/mcp-micropython-bridge](https://github.com/SWITCHSCIENCE/mcp-micropython-bridge) - 通过 USB 串口桥接到 ESP32 / RP2040 上的 MicroPython REPL。日文文档。(★9 · 2026-04)
- [neusse/Codex-Circuitpython-MCP](https://github.com/neusse/Codex-Circuitpython-MCP) - CircuitPython 板卡发现、文件部署、串口读取、中断与复位。(★7 · 2026-05)
- [ctrlpi/pico-bay](https://github.com/ctrlpi/pico-bay) - 通过 USB 管理运行 MicroPython 或 CircuitPython 的树莓派 Pico 与 ESP32 板。(★5 · 2026-09)
- [Wokwi MCP 模式](https://docs.wokwi.com/wokwi-ci/mcp-support) - `wokwi-cli mcp` 把托管的 Wokwi 仿真暴露给 Agent：无需板子即可运行 Arduino / ESP32 / RP2040 固件并读取串口。(official)

### 端侧 MCP server

直接运行在单片机或 SBC 上的 MCP server——设备本身就是工具提供方。

- [espressif/esp-iot-solution `mcp-c-sdk`](https://github.com/espressif/esp-iot-solution/tree/master/components/mcp-c-sdk) - 面向 ESP-IDF 5.4+ 的 C 实现：Streamable HTTP、SSE 与自定义传输；支持工具、资源、提示、补全与异步任务。ESP 组件注册表下载约 2.4 万次；esp-claw 就构建于其上。(official · ★2.7k · 2026-07)
- [Zephyr MCP server 库](https://docs.zephyrproject.org/latest/services/connectivity/networking/api/mcp.html) - 上游的 `subsys/net/lib/mcp`，由 NXP 贡献、2026-06 合入：首个在主线内置 MCP server 的 RTOS（HTTP，SSE 回退，仅工具，实验性）。(official)
- [emqx/esp-mcp-over-mqtt](https://github.com/emqx/esp-mcp-over-mqtt) - 按 MCP-over-MQTT 规范在 MQTT 5.0 上提供 MCP 的 ESP-IDF 组件。(official · ★8 · 2025-12)
- [servoagents/mcp-c](https://github.com/servoagents/mcp-c) - 与传输无关的 C99 内核，附 POSIX、Zephyr 与 ESP32 示例；支持 HTTP、stdio、MQTT 5 与实验性 CoAP。(★2 · 2026-09)
- [solnera/esp32-mcpserver](https://github.com/solnera/esp32-mcpserver) - 基于 AsyncTCP 的 Arduino / ESP32 HTTP JSON-RPC，带 mDNS 与工作任务式工具调用；PlatformIO 包名 `ESP32-MCPServer`，姊妹项目增加了 BLE 传输。(★11 · 2026-08)
- [AaronWander/EmbedMCP](https://github.com/AaronWander/EmbedMCP) - 在 STM32、ESP32、nRF 或树莓派上运行 MCP server 的 C 库。(★31 · 2026-02)
- [navado/ESP32MCPServer](https://github.com/navado/ESP32MCPServer) - 暴露 NMEA2000 / NMEA0183 / OBD-II 传感器的 ESP32 WebSocket MCP server。(★60 · 2026-03)
- [rzeldent/esp32-cam-ai](https://github.com/rzeldent/esp32-cam-ai) - 内置在 ESP32-CAM 固件中的 MCP server。(★28 · 2026-08)
- [ThanabordeeN/MCP-U_Arduino](https://github.com/ThanabordeeN/MCP-U_Arduino) - Arduino 库管理器中的 `MCP-U`：在 AVR / ESP / RP2040 的任意 `Stream` 上跑 JSON-RPC，暴露 GPIO、PWM、ADC 与 I2C，并由一个 npm 客户端转换为标准 MCP。(★4 · 2026-05)
- [PedroFnseca/esp32-mcp](https://github.com/PedroFnseca/esp32-mcp) - Arduino 库管理器中的 `ESP32-MCP`：无状态 MCP 2026-07-28，带主机端单元测试与 CI。(★1 · 2026-08)
- [matta-pie/micro-mcp](https://github.com/matta-pie/micro-mcp) - 已在 Pico W / Pico 2 W 上验证的 MicroPython MCP server；支持 HTTP 与 USB 上的 stdio 传输。(★1 · 2026-02)
- [solnera/esp32-ble-mcp-server](https://github.com/solnera/esp32-ble-mcp-server) - 唯一真正可用的 MCP-over-BLE GATT 传输：ESP32 服务端，外加 FastMCP / TS / Swift 的 BLE 客户端传输。(★1 · 2026-02)

### 串口 / 总线 / 调试（MCP）

- [Adancurusul/embedded-debugger-mcp](https://github.com/Adancurusul/embedded-debugger-mcp) - 基于 probe-rs / OpenOCD 的 24 工具调试器，支持 Cortex-M、RISC-V 与 Xtensa，内置 Claude / Codex Skill。Veecle 评测的首选。(★187 · 2026-07)
- [Adancurusul/serial-mcp-server](https://github.com/Adancurusul/serial-mcp-server) - Rust 串口 / UART MCP 与 CLI，带 JSON 宏自动化与 Agent Skill。(★91 · 2026-07)
- [Ipiano/gdb-mcp](https://github.com/Ipiano/gdb-mcp) - 直接驱动 GDB/MI，适用于嵌入式与本机目标。(★48 · 2026-03)
- [YaoIsAI/SerialRUN](https://github.com/YaoIsAI/SerialRUN) - 面向 Modbus / PLC / CAN / I2C / SPI 的 Rust 串口调试器，带 15 工具的 MCP server。(★38 · 2026-06)
- [es617/dbgprobe-mcp-server](https://github.com/es617/dbgprobe-mcp-server) - 通过 J-Link、CMSIS-DAP 与 ST-Link 做带符号（ELF / SVD）感知的片上调试。(★10 · 2026-03)
- [Leonezz/openbaud](https://github.com/Leonezz/openbaud) - 把串口设备变成带类型、可审计的 MCP 工具：解码、抓取、回放。(★6 · 2026-09)
- [magnusmalm/smolmux](https://github.com/magnusmalm/smolmux) - C11 编写的串口与 GDB-SWD 复用器，带 MCP server，让一个探针同时服务多个使用方。(★2 · 2026-08)
- [Pan-Robotics/bus-mcp](https://github.com/Pan-Robotics/bus-mcp) - 把树莓派上的 CAN / CAN-FD、RS-485 / UART、I2C、SPI 与 GPIO 暴露为 MCP 工具，默认只读。(★2 · 2026-06)
- [mcp2everything/mcp2mqtt](https://github.com/mcp2everything/mcp2mqtt) - 用于硬件控制的 MCP → MQTT 桥；被引用最多的早期作品，但已无人维护。姊妹项目 `mcp2serial` 与 `mcp2tcp` 同样停更。(★371 · stale since 2024-12)

### 机器人（MCP）

- [robotmcp/ros-mcp-server](https://github.com/robotmcp/ros-mcp-server) - 通过 rosbridge 把 Claude / GPT 接到 ROS 与 ROS 2 机器人；客户端对应项目 [robotmcp_client](https://github.com/robotmcp/robotmcp_client)。(★1.5k · 2026-09)
- [Rerun viewer-mcp](https://rerun.io/docs/reference/viewer/mcp) - 官方 `rerun viewer-mcp` 子命令，通过 gRPC 驱动正在运行或无头的 Rerun Viewer。(official)
- [Foxglove Desktop MCP server](https://docs.foxglove.dev/docs/agents/mcp-server) - 内置于 Foxglove Desktop：查看数据、搭建布局、编写用户脚本、回放、文档检索；本地端点，需要 Pro / Enterprise / Academic 席位。(official)
- [Roboflow MCP](https://blog.roboflow.com/mcp-server/) - 托管的 `mcp.roboflow.com`：训练、Workflows、托管推理与边缘设备部署；[computer-vision-skills](https://github.com/roboflow/computer-vision-skills) 以 Claude / Codex 插件形式提供十个 Skill。(official)
- [Extelligence-ai/bagel](https://github.com/Extelligence-ai/bagel) - 用自然语言查询机器人、无人机与 IoT 遥测数据（ROS bag、MCAP、PX4 日志），带边缘侧数据精简流水线。(★396 · 2026-09)
- [rokbenko/quackd](https://github.com/rokbenko/quackd) - 一个 CLI / MCP 驱动七种机器人本体（Microduck、Open Duck、SO-101、XLeRobot、AlohaMini、ToddlerBot、rosbridge），每种本体有自己的 Skill 契约；目前只有仿真与 mock。(★200 · 2026-09)
- [omni-mcp/isaac-sim-mcp](https://github.com/omni-mcp/isaac-sim-mcp) - 用自然语言控制 NVIDIA Isaac Sim 的场景与机器人。(★190 · 2025-04)
- [wise-vision/ros2_mcp](https://github.com/wise-vision/ros2_mcp) - 支持图像流与自动 QoS 匹配的 ROS 2 MCP。(★88 · 2026-08)
- [lpigeon/unitree-go2-mcp-server](https://github.com/lpigeon/unitree-go2-mcp-server) - 通过 ROS 2 控制宇树 Go2 机器狗。(★87 · 2026-06)
- [kakimochi/ros2-mcp-server](https://github.com/kakimochi/ros2-mcp-server) - 基于 topic 的 ROS 2 控制。(★83 · 2025-06)
- [IliaLarchenko/robot_MCP](https://github.com/IliaLarchenko/robot_MCP) - LeRobot 生态中的 SO-ARM100 / 101 与 LeKiwi 机械臂控制。(★83 · 2025-08)
- [Yutarop/ros-mcp](https://github.com/Yutarop/ros-mcp) - 把 ROS topic、service 与 action 暴露为 MCP 工具。(★36 · 2025-08)
- [agentculture/reachy-mini-mcp](https://github.com/agentculture/reachy-mini-mcp) - 单工具的 Reachy Mini MCP，带序列模式，可对接真机或仿真；配套 CLI 提供 `find-reachy` Skill。(★32 · 2026-07)
- [jackccrawford/reachy-mini-mcp](https://github.com/jackccrawford/reachy-mini-mcp) - Pollen Robotics Reachy Mini 控制。(★29 · 2026-07)
- [binabik-ai/mcp-rosbags](https://github.com/binabik-ai/mcp-rosbags) - 离线 rosbag 分析。(★28 · 2025-09)
- [phospho-app/phospho-mcp-server](https://github.com/phospho-app/phospho-mcp-server) - 面向 SO-100 / 101 机械臂的 VLA 桥接。(★10 · 2025-09)
- [neka-nat/mycobot-mcp](https://github.com/neka-nat/mycobot-mcp) - 大象机器人 myCobot；该厂商唯一的 MCP。(★8 · 2025-05)
- [nonead/Nonead-Universal-Robots-MCP](https://github.com/nonead/Nonead-Universal-Robots-MCP) - Universal Robots 协作机器人 MCP 中间件（中 / 英 / 日文档）。(★7 · 2026-09)
- [monteslu/robot-mcp](https://github.com/monteslu/robot-mcp) - Johnny-Five MCP：Arduino 与树莓派上的舵机与硬件。(★7 · 2026-02)
- [eliasbitsch/abb-robotstudio-mcp](https://github.com/eliasbitsch/abb-robotstudio-mcp) - ABB RobotStudio SDK 插件，外加在真实控制器上使用 Robot Web Services。(★6 · 2026-05)
- [RoversX/universal-robot-mcp](https://github.com/RoversX/universal-robot-mcp) - Universal Robots 协作机器人控制。(★5 · 2025-09)
- [ros-claw/unitree-sdk2-mcp](https://github.com/ros-claw/unitree-sdk2-mcp) - 不依赖 ROS，直接通过 DDS 控制宇树 G1 / Go2 / H1 / B2 / A2 / R1；ros-claw 组织下还有约 35 个同类 MCP（RealSense、Vicon、Nav2、MoveIt 2、UR、LIMO、因时灵巧手）。(★4 · 2026-04)
- [gtoff/moveit-mcp-server](https://github.com/gtoff/moveit-mcp-server) - 把 MoveIt 2 规划暴露为 MCP 工具。(★4 · 2026-03)
- [ros-claw/inspire-rh56-mcp](https://github.com/ros-claw/inspire-rh56-mcp) - 通过 CAN 控制因时 RH56 灵巧手，已在实物上复验。(★1 · 2026-07)
- [erh/viam-mcp-server](https://github.com/erh/viam-mcp-server) - 以 Viam 模块形式提供的 MCP：根据每个组件的 Go 接口逐方法生成工具，作者是 Viam 的 CEO。(★0 · 2026-04)

### 无人机（MCP）

- [ion-g-ion/MAVLinkMCP](https://github.com/ion-g-ion/MAVLinkMCP) - 通过 MAVLink 控制 PX4 / ArduPilot 无人机。(★23 · 2026-08)
- [ysznai/dji-waypoint-mcp](https://github.com/ysznai/dji-waypoint-mcp) - 大疆航线规划；除 Tello 外唯一的大疆 MCP。(★7 · 2025-07)
- [0xKoda/drone-mcp](https://github.com/0xKoda/drone-mcp) - 大疆 Tello 无人机控制。(★25 · 2025-04)
- [showkeyjar/robot-mcp-server](https://github.com/showkeyjar/robot-mcp-server) - 宇树与大疆无人机的运动控制。(★12 · 2026-03)
- [hfujikawa77/ardupilot-mcp-server](https://github.com/hfujikawa77/ardupilot-mcp-server) - 通过 MAVLink TCP 控制 ArduPilot。日文。(★9 · 2026-05)
- [rmeadomavic/ardupilot-mcp](https://github.com/rmeadomavic/ardupilot-mcp) - SITL 优先、带安全门禁的 ArduPilot MAVLink MCP。(★2 · 2026-08)
- [starlordz12/inav-mcp](https://github.com/starlordz12/inav-mcp) - 通过 USB 配置、诊断与调校 iNAV 固定翼飞控。(★2 · 2026-08)
- [bvandevliet/betaflight-mcp](https://github.com/bvandevliet/betaflight-mcp) - 实时的 Betaflight CLI 配置与 PID 助手，内置调参 Skill。(★1 · 2026-08)

### 仿真器（MCP）

- [kvgork/gazebo-mcp](https://github.com/kvgork/gazebo-mcp) - Gazebo：生成 TurtleBot3、多机器人编队、世界生成、传感器数据。(★17 · 2026-07)
- [robotlearning123/mujoco-mcp](https://github.com/robotlearning123/mujoco-mcp) - 65 个 MuJoCo 工具：轨迹优化、接触分析、视频导出、查看器。(★9 · 2026-06)
- [Rongxuan-Zhou/mujoco-mcp-server](https://github.com/Rongxuan-Zhou/mujoco-mcp-server) - 在 Claude Code 中对 MuJoCo 做仿真、渲染、分析与构建强化学习环境。(★8 · 2026-03)
- [nullbyte91/nvidia-isaac-mcp](https://github.com/nullbyte91/nvidia-isaac-mcp) - Isaac Sim 扩展加外部 MCP，带 Isaac Lab 钩子。(★8 · 2026-02)
- [game4automation/io.realvirtual.mcp](https://github.com/game4automation/io.realvirtual.mcp) - Unity 数字孪生 MCP：驱动、传感器、PLC 信号、机器人逆解。(official · ★15 · 2026-07)
- [mergeos-bounties/gazebo-mcp](https://github.com/mergeos-bounties/gazebo-mcp) - Gazebo（gz-sim）的世界、模型、位姿与单步推进，带完整的离线 mock 以便 CI 使用。(★4 · 2026-07)
- [SchiopuAndreiViorel/coppelia-mcp](https://github.com/SchiopuAndreiViorel/coppelia-mcp) - Claude ↔ CoppeliaSim。(★4 · 2026-03)
- [lyuai/genesis-mcp](https://github.com/lyuai/genesis-mcp) - 带可视化的 Genesis World 仿真器 MCP。(★5 · 2025-03)
- [punithkrishnakeepudi/webots-mcp-server](https://github.com/punithkrishnakeepudi/webots-mcp-server) - Webots 启动、监视、强化学习训练与场景操作；找到的唯一 Webots MCP。(★0 · 2026-04)

### 工业 IoT（MCP）

- [anviod/edgeCore](https://github.com/anviod/edgeCore) - 部署在工业现场的边缘运行时，支持 Modbus、BACnet、OPC UA、S7 与 EtherNet/IP。(★126 · 2026-09)
- [rivie13/studio5000-AI-Assistant](https://github.com/rivie13/studio5000-AI-Assistant) - 把罗克韦尔自动化 SDK 与内部文档作为 Studio 5000 的 MCP 工具。(★35 · 2025-12)
- [Nodeblue-AI/studio5000-mcp-server](https://github.com/Nodeblue-AI/studio5000-mcp-server) - 解析罗克韦尔与 Allen-Bradley PLC 的 Studio 5000 L5X 工程导出；姊妹项目 `bridge-mcp-server` 将其与 Ignition SCADA 关联。(★19 · 2026-08)
- [ThingsPanel/thingspanel-mcp](https://github.com/ThingsPanel/thingspanel-mcp) - ThingsPanel IoT 平台的设备控制与数据分析。(★47 · 2025-11)
- [chewcw/tia-portal-openness-mcpserver](https://github.com/chewcw/tia-portal-openness-mcpserver) - 西门子博途 Openness MCP。(★37 · 2026-05)
- [kukapay/opcua-mcp](https://github.com/kukapay/opcua-mcp) - 连接 OPC UA 系统：监视、分析与控制节点。(★28 · 2025-10)
- [midhunxavier/OPCUA-MCP](https://github.com/midhunxavier/OPCUA-MCP) - OPC UA MCP server。(★25 · 2026-09)
- [kukapay/modbus-mcp](https://github.com/kukapay/modbus-mcp) - 为 Agent 规范化并语义化 Modbus 寄存器。(★24 · 2025-05)
- [OPCFoundation/UA-for-AI-Prototype](https://github.com/OPCFoundation/UA-for-AI-Prototype) - OPC UA for AI 工作组：把规范切分为 RAG 片段，并托管在 reference.opcfoundation.org/mcp，计划覆盖 430+ 个配套规范。(official · ★14 · 2026-06)
- [efranceschetti/festo-codesys-mcp](https://github.com/efranceschetti/festo-codesys-mcp) - Festo / CODESYS MCP，带结构化文本编写、PLCopen XML、运动控制与故障诊断 Skill。(★1 · 2026-09)
- [lwsinclair/IoT-Edge-MCP-Server](https://github.com/lwsinclair/IoT-Edge-MCP-Server) - 统一 MQTT、Modbus 与 InfluxDB，用于 SCADA / PLC 场景。(★3 · 2025-11)
- [daedalus/mcp-snap7](https://github.com/daedalus/mcp-snap7) - 通过 python-snap7 访问西门子 S7 PLC。(★0 · 2026-04)

### 汽车（MCP）

- [farzadnadiri/MCP-CAN](https://github.com/farzadnadiri/MCP-CAN) - 基于 SocketCAN / vcan 的 OBD-II（J1979）、UDS 与 J1939 诊断；可 pip 安装。(★16 · 2026-08)
- [hexsecs/canarchy](https://github.com/hexsecs/canarchy) - 流式优先的 CAN / J1939 工具箱（python-can、SocketCAN），内置 MCP server、TUI 与模糊测试。(★4 · 2026-09)
- [HadiCherkaoui/klartext](https://github.com/HadiCherkaoui/klartext) - 原生 Rust 实现、通过 ENET 线（HSFZ / UDS）做宝马 F 系列诊断，带 MCP server。(★5 · 2026-08)
- [chrisbray85/headless-ista](https://github.com/chrisbray85/headless-ista) - Agent 通过 MCP 驱动宝马 ISTA+，以文本形式读取故障与测试计划。(★4 · 2026-09)
- [petrpatek/obd2-mcp-server](https://github.com/petrpatek/obd2-mcp-server) - 通过蓝牙或 USB 连接 ELM327：故障码与实时 PID，带 `--mock` 模式。(★3 · 2026-05)
- [awtoau/awto-can](https://github.com/awtoau/awto-can) - SocketCAN MCP 守护进程：DBC 感知的收发、ISO-TP、抓取与回放、实时 DBC 校验。(★0 · 2026-04)
- [mikehaller/kuksa-mcp-server](https://github.com/mikehaller/kuksa-mcp-server) - 通过 Eclipse Kuksa Databroker 读写 COVESA VSS 信号；找到的唯一 VSS MCP。(★0 · 2026-06)
- [cyrusdavirusss/j2534-mcp-server](https://github.com/cyrusdavirusss/j2534-mcp-server) - J2534 PassThru 的 UDS / OBD-II；找到的唯一 J2534 MCP。仅 Windows。(★0 · 2026-09)
- [daedalus/mcp-canbus](https://github.com/daedalus/mcp-canbus) - 极简 CAN 总线 MCP。(★0 · 2026-03)

### 楼宇自动化与能源（MCP）

- [knx-ai/knx-ets-mcp](https://github.com/knx-ai/knx-ets-mcp) - 通过 ETS 插件接入 ETS 5 / 6 的 MCP：检视与编辑工程、编程与扫描设备。仅 Windows。(★31 · 2026-08)
- [NickoScope/nickol-knx-mcp](https://github.com/NickoScope/nickol-knx-mcp) - 设计阶段的 KNX / ETS 校验与修复（DPT、Secure、Matter）。(★24 · 2026-09)
- [ezhuk/bacnet-mcp](https://github.com/ezhuk/bacnet-mcp) - BACnet 属性读写；`pip install bacnet-mcp`。(★5 · 2026-09)
- [chappo/rusty-bacnet-mcp](https://github.com/chappo/rusty-bacnet-mcp) - Rust 实现的 BACnet MCP：发现、传感器、设定值；默认只读，单一二进制。(★0 · 2026-08)
- [lubosstrejcek/victron-tcp](https://github.com/lubosstrejcek/victron-tcp) - 通过本地 Modbus TCP 与 MQTT 访问 Victron GX，32 个工具覆盖 900+ 个寄存器；姊妹项目 `victron-vrm-mcp` 对接云端。(★3 · 2026-09)
- [flowiesner/fronius-mcp](https://github.com/flowiesner/fronius-mcp) - Fronius Solar API：光伏、电池、并网馈电。(★1 · 2026-04)
- [mregen/shelly-em-mcp](https://github.com/mregen/shelly-em-mcp) - 本地读取 Shelly Pro 3EM / EM / Plus PM 的电能数据。(★1 · 2026-09)
- [mrksmts/homewizard-mcp-server](https://github.com/mrksmts/homewizard-mcp-server) - HomeWizard P1 智能电表本地 API，只读。(★1 · 2026-04)
- [gkoenig/anker-solix-mcp](https://github.com/gkoenig/anker-solix-mcp) - 安克 Solix Solarbank 与智能电表。(★1 · 2026-09)
- [bjeans/homelab-mcp](https://github.com/bjeans/homelab-mcp) - 家庭实验室工具包，其中的 UPS server 直接对硬件说 NUT 协议。(★43 · 2026-06)
- [javierojan/askacharge-mcp](https://github.com/javierojan/askacharge-mcp) - 运营一整个 OCPP 充电桩集群。(★0 · 2026-09)
- [cr2007/mcp-helvarnet](https://github.com/cr2007/mcp-helvarnet) - 通过 HelvarNet 控制 Helvar DALI 照明；找到的唯一 DALI MCP。(★0 · 2026-01)
- [SAP/e-mobility-charging-stations-simulator `skills/`](https://github.com/SAP/e-mobility-charging-stations-simulator) - SAP OCPP-J 充电桩模拟器的 EVSE 模拟 Skill；是模拟而非硬件。(official · ★225 · 2026-09)

### 智能家居（MCP）

- [home-assistant/core `mcp_server`](https://www.home-assistant.io/integrations/mcp_server/) - 内置的 MCP server 集成，通过 Streamable HTTP 暴露 Assist API。(official · ★90k · 2026-09)
- [homeassistant-ai/ha-mcp](https://github.com/homeassistant-ai/ha-mcp) - 87 个工具；功能最全的 Home Assistant MCP。(★4.7k · 2026-09)
- [tevonsb/homeassistant-mcp](https://github.com/tevonsb/homeassistant-mcp) - 支持 SSE 实时更新的 Home Assistant MCP。(★576 · 2026-01)
- [voska/hass-mcp](https://github.com/voska/hass-mcp) - 节省 token 的 Home Assistant 控制与查询。(★340 · 2026-08)
- [openHAB MCP 加载项](https://www.openhab.org/addons/integrations/mcp/) - openHAB 5.x 内置加载项：item、thing、规则、订阅；独立部署可选 [tdeckers/openhab-mcp](https://github.com/tdeckers/openhab-mcp)。(official)
- [Homey MCP](https://mcp.athom.com) - Athom 为 Homey 托管的远程 MCP，2025-11 上线；无公开仓库。(official)
- [aqara/aqara-mcp-server](https://github.com/aqara/aqara-mcp-server) - 绿米 Aqara 的远程 Streamable-HTTP MCP，24 个工具覆盖设备、场景、自动化、能耗与固件。(official · ★42 · 2026-06)
- [Yeelight/yeelight-iot-mcp](https://github.com/Yeelight/yeelight-iot-mcp) - 易来 Yeelight Pro 云端：家庭、房间、设备、分组、场景。(official · ★9 · 2026-07)
- [ecovacs-ai/ecovacs-mcp](https://github.com/ecovacs-ai/ecovacs-mcp) - 科沃斯地宝扫地机：清扫、回充、状态；需要开放平台密钥。(official · ★23 · 2025-04)
- [tuya/tuya-mcp-sdk](https://github.com/tuya/tuya-mcp-sdk) - 方向正好相反：这是一套 Python / Go / C# SDK，用来把你自己的工具注册进涂鸦的 Agent 平台，而不是用来控制涂鸦设备。(official · ★67 · 2026-04)
- [Do1e/mijia-api](https://github.com/Do1e/mijia-api) - 米家云端 API、CLI 与 MCP（`uvx mijiaAPI mcp`）：扫码登录、设备属性、动作、场景。小米没有官方 MCP，这是事实标准。(★799 · 2026-08)
- [mihai-dinculescu/tapo](https://github.com/mihai-dinculescu/tapo) - Rust / Python 的 TP-Link Tapo 库，内置一等公民级 MCP server：插座、灯泡、网关、摄像头。(★802 · 2026-09)
- [sirkirby/unifi-mcp](https://github.com/sirkirby/unifi-mcp) - UniFi Network / Protect / Access MCP 套件；光 Protect server 就有 62 个工具。(★820 · 2026-09)
- [shenjingnan/xiaozhi-client](https://github.com/shenjingnan/xiaozhi-client) - 把多个标准 MCP server 聚合到一个小智接入点连接上，带 Web 配置界面。(★338 · 2026-09)
- [c1pher-cn/ha-mcp-for-xiaozhi](https://github.com/c1pher-cn/ha-mcp-for-xiaozhi) - 把 Home Assistant 作为 MCP server 暴露给小智设备的 HA 集成。(★268 · 2026-09)
- [xinnan-tech/mcp-endpoint-server](https://github.com/xinnan-tech/mcp-endpoint-server) - 小智 MCP 接入点：本地 MCP server 反向拨入的 WebSocket 注册中心，因此它们无法被宿主客户端直接拉起。(official · ★166 · 2026-06)
- [78/mcp-calculator](https://github.com/78/mcp-calculator) - 固件作者提供的小智反向连接 MCP 标准示例。(official · ★444 · 2026-02)
- [toddpan/xiaozhi-esp32-mcp](https://github.com/toddpan/xiaozhi-esp32-mcp) - 固件侧 MCP 客户端库，用于向小智注册 ESP32 工具。(★71 · 2025-10)
- [jango-blockchained/advanced-homeassistant-mcp](https://github.com/jango-blockchained/advanced-homeassistant-mcp) - 50+ 个 Home Assistant 工具，支持三种传输方式。(★56 · 2026-06)
- [alexpfau/zigbee2mqtt-mcp](https://github.com/alexpfau/zigbee2mqtt-mcp) - Zigbee2MQTT 管理：网状网络健康、OTA、配对、绑定。(★29 · 2026-09)
- [loryanstrant/ESPHome-MCP](https://github.com/loryanstrant/ESPHome-MCP) - ESPHome MCP，含 2026.6 版的 Device Builder。(★26 · 2026-08)
- [gehaiyi/xiaomi-home-mcp](https://github.com/gehaiyi/xiaomi-home-mcp) - 独立的小米云端 MCP，带型号自动映射与音箱控制。(★24 · 2026-04)
- [ykhli/mcp-light-control](https://github.com/ykhli/mcp-light-control) - 飞利浦 Hue 控制。(★22 · 2025-03)
- [kingpanther13/Hubitat-local-MCP-server](https://github.com/kingpanther13/Hubitat-local-MCP-server) - 直接运行在 Hubitat 网关上的 Groovy MCP server：116 个工具，带规则引擎。(★18 · 2026-09)
- [scald/tesla-mcp](https://github.com/scald/tesla-mcp) - 通过 Fleet API 控制特斯拉车辆。(★15 · 2025-03)
- [ichbinder/MCP2ZigBee2MQTT](https://github.com/ichbinder/MCP2ZigBee2MQTT) - Zigbee2MQTT 设备发现与控制。(★12 · 2025-10)
- [0x1abin/matter-controller-mcp](https://github.com/0x1abin/matter-controller-mcp) - Matter 控制器 MCP：发现、配网、控制。(★8 · 2025-08)
- [MatterCoder/matter-mcp-server](https://github.com/MatterCoder/matter-mcp-server) - Matter 设备控制；控制器侧 Matter 覆盖的另一半。(★7 · 2025-03)
- [TimCinel/homekit-mcp](https://github.com/TimCinel/homekit-mcp) - HomeKit（HAP）MCP；另有基于 macOS 原生 HomeKit 框架与 Homebridge 的替代方案。(★8 · 2026-03)
- [genm/switchbot-mcp](https://github.com/genm/switchbot-mcp) - SwitchBot 设备控制。(★7 · 2026-09)
- [noboru-i/nature-remo-mcp-server](https://github.com/noboru-i/nature-remo-mcp-server) - Nature Remo 红外网关。(★7 · 2025-04)
- [caroliny1031/midea-mcp](https://github.com/caroliny1031/midea-mcp) - 美的空调，局域网优先、云端兜底。(★5 · 2026-08)
- [veonua/smartthings-mcp](https://github.com/veonua/smartthings-mcp) - 三星 SmartThings 的房间、设备与指令。(★5 · 2025-07)
- [sandraschi/dreame-mcp](https://github.com/sandraschi/dreame-mcp) - 通过追觅云端（可选本地 miIO）控制追觅扫地机。(★4 · 2026-09)
- [cacack/mcp-server-zwave-js-ui](https://github.com/cacack/mcp-server-zwave-js-ui) - Z-Wave JS UI 的 WebSocket MCP：取值、配置、入网与退网。(★0 · 2026-08)
- [Buggy1111/shelly-mcp](https://github.com/Buggy1111/shelly-mcp) - Shelly Gen1–4 与 BLU 设备，本地优先；官方 MCP 注册表中极少数的智能家居 server 之一。(★0 · 2026-08)

### 实验室仪器（MCP）

- [lagerdata/lager](https://github.com/lagerdata/lager) - 从笔记本或 CI 发起的硬件测试自动化，带 MCP server；支持普源、是德、吉时利。(★7 · 2026-09)
- [JanGoebel/LabVIEW-MCP-Server-Toolkit](https://github.com/JanGoebel/LabVIEW-MCP-Server-Toolkit) - 在 LabVIEW 中托管 MCP server，让 VI 变成工具。(★55 · 2026-07)
- [Zuehlke/labview-mcp](https://github.com/Zuehlke/labview-mcp) - 通过 NI gRPC 读、写并运行 LabVIEW VI；以 Claude 插件形式安装。(★29 · 2026-09)
- [erebusnz/rigol-mcp](https://github.com/erebusnz/rigol-mcp) - 通过局域网或 USB 控制普源 DS1000Z / MSO1000Z / DHO 示波器。(★28 · 2026-07)
- [lucasgerads/lecroy-mcp](https://github.com/lucasgerads/lecroy-mcp) - 通过 VXI-11 或 USB 控制力科 WaveSurfer / HDO / WaveRunner / WavePro。(★11 · 2026-04)
- [Netlist-Studio/scope-mcp](https://github.com/Netlist-Studio/scope-mcp) - 通过以太网控制是德 / 安捷伦示波器，已在 MSOX2024A 上测试。(★11 · 2026-02)
- [Anai-Guo/LabAgent](https://github.com/Anai-Guo/LabAgent) - 通过 GPIB / USB / 串口支持 26 家厂商的 68 种仪器型号，提供 MCP、Web 与 CLI。(★8 · 2026-09)
- [MagnusJohansson/siglent-sds-mcp](https://github.com/MagnusJohansson/siglent-sds-mcp) - 通过 SCPI TCP 控制鼎阳 SDS1000X-E。(★7 · 2026-02)
- [techmanual-ai/lablink-mcp](https://github.com/techmanual-ai/lablink-mcp) - 统一的实验设备 MCP，支持 VISA / SCPI、SSH、REST 与串口；已在泰克 MSO44、鼎阳 SDG 与是德电源上测试。(★5 · 2026-06)
- [Keysight/cyperf-mcp](https://github.com/Keysight/cyperf-mcp) - 是德官方用于驱动 CyPerf 流量生成 agent 的 MCP。(official · ★1 · 2026-04)
- [daqifi/daqifi-core](https://github.com/daqifi/daqifi-core) - 面向 DAQiFi Nyquist 无线数采的 .NET SDK 与 MCP server。(official · ★5 · 2026-09)
- [KenosInc/dwf-mcp-server](https://github.com/KenosInc/dwf-mcp-server) - 通过 WaveForms SDK 控制 Digilent Analog Discovery 3（示波器、任意波形发生器、逻辑分析仪、电源）。(★3 · 2026-08)
- [armchairdeity/mcp-server-scpi](https://github.com/armchairdeity/mcp-server-scpi) - 带高层工具的 SCPI / VISA MCP，后端为普源 DS1054Z。(★3 · 2026-07)
- [JacobBeningo/devsignal](https://github.com/JacobBeningo/devsignal) - 鼎阳 SDG 信号发生器的 CLI 与 MCP。(★3 · 2026-07)
- [hsoffar/saleae-logic2-mcp](https://github.com/hsoffar/saleae-logic2-mcp) - Saleae Logic 2 逻辑分析仪自动化。(★3 · 2026-03)
- [TECTOS-JP/lab-visa-mcp](https://github.com/TECTOS-JP/lab-visa-mcp) - PyVISA MCP，用 YAML 定义仪器指令集与安全范围；姊妹项目 `lab-modbus-mcp` 面向冷水机与温控器。(★0 · 2026-08)
- [yerbymatey/opentrons-mcp](https://github.com/yerbymatey/opentrons-mcp) - 通过 HTTP API 控制 Opentrons OT-2 / Flex。(★7 · 2025-06)
- [nygmeta/OpenLabAI](https://github.com/nygmeta/OpenLabAI) - 面向 Opentrons OT-2、Hamilton STAR、Biomek FXP 与 Cellario 的 MCP server，带人工审批门禁。(★0 · 2026-09)
- [ghollyer/AMADEUS](https://github.com/ghollyer/AMADEUS) - Gatan / DigitalMicrograph 电子显微镜：通过 ZMQ 控制样品台、电子束、STEM 与 EDS。(★4 · 2026-07)
- [sandraschi/sdr-mcp](https://github.com/sandraschi/sdr-mcp) - RTL-SDR：频谱、瀑布图、FM 解调、GNU Radio。(★7 · 2026-09)

### 摄像头（MCP）

- [reolink/reolink-cli](https://github.com/reolink/reolink-cli) - 仅限局域网的 Reolink CLI，内置 MCP stdio server 与 SKILL.md：抓图、云台、RTSP。(official · ★97 · 2026-09)
- [evalstate/mcp-webcam](https://github.com/evalstate/mcp-webcam) - 把网络摄像头画面作为工具与资源提供。(★121 · 2025-10)
- [jakekeeys/frigate-mcp](https://github.com/jakekeeys/frigate-mcp) - Frigate NVR，90 个工具与 HTTP API 一一对应。(★11 · 2026-09)
- [sandraschi/tapo-mcp](https://github.com/sandraschi/tapo-mcp) - TP-Link Tapo 摄像头：云台、抓图、推流。(★2 · 2026-09)
- [ros-claw/librealsense-mcp](https://github.com/ros-claw/librealsense-mcp) - 封装 pyrealsense2 的 26 个工具：深度、点云、标定、多相机。(★1 · 2026-07)
- [oneshot2001/onvif-pp-cli](https://github.com/oneshot2001/onvif-pp-cli) - ONVIF Profile S / T / G / M 的 CLI 与 MCP，64 条命令，已在 Axis 摄像头上冒烟测试。(★0 · 2026-05)

### 无线与软件无线电（MCP）

- [es617/ble-mcp-server](https://github.com/es617/ble-mcp-server) - 基于 bleak 的跨平台 BLE：扫描、连接、GATT 读取与订阅。(★17 · 2026-03)
- [stass/blew](https://github.com/stass/blew) - macOS 上的 BLE CLI 与 MCP，支持外设模式。(★16 · 2026-05)
- [mr-tbot/mesh-api](https://github.com/mr-tbot/mesh-api) - 面向 Meshtastic 与 MeshCore 的离网 AI 路由器，带 MCP server 与 OpenClaw Skill。(★173 · 2026-07)
- [busse/flipperzero-mcp](https://github.com/busse/flipperzero-mcp) - 通过 USB 或 Wi-Fi 控制 Flipper Zero。(★32 · 2025-12)
- [Wet-wr-Labs/claupper](https://github.com/Wet-wr-Labs/claupper) - 一个 Flipper Zero `.fap` 应用，充当单手 BLE / USB 遥控器，用来批准或拒绝 Agent 的操作。(★27 · 2026-05)
- [roostercoopllc/flipper-mcp](https://github.com/roostercoopllc/flipper-mcp) - 运行在 Flipper 的 ESP32-S2 Wi-Fi 开发板上的 MCP server，通过 UART 桥接约 30 个工具（Sub-GHz、NFC、RFID、红外、BLE、GPIO）。(★17 · 2026-03)
- [jonastbrg/FlipperAgent](https://github.com/jonastbrg/FlipperAgent) - Flipper MCP 与 Agent，67 个工具，带 ESP32 Marauder 桥与 Skill。(★10 · 2026-03)
- [N-Erickson/AetherLink-SDR-MCP](https://github.com/N-Erickson/AetherLink-SDR-MCP) - RTL-SDR 与 HackRF：ADS-B、AIS、POCSAG、Meteor LRPT。(★23 · 2026-07)
- [thehappydinoa/hackrf-mcp](https://github.com/thehappydinoa/hackrf-mcp) - 封装 hackrf_tools：扫频、IQ 采集与发射。(★2 · 2026-08)
- [mplogas/pm3-mcp](https://github.com/mplogas/pm3-mcp) - Proxmark3（Iceman 固件）RFID / NFC 识别与读取。(★3 · 2026-06)
- [oliveres/chirpstack-mcp-server](https://github.com/oliveres/chirpstack-mcp-server) - 通过 gRPC 访问 ChirpStack v4 LoRaWAN，支持实时上行调试。(★0 · 2026-08)
- [swannman/openthread-mcp](https://github.com/swannman/openthread-mcp) - Arduino Nano Matter 上的 OpenThread CLI MCP 与 Prometheus 导出器；找到的唯一 Thread MCP。(★1 · 2026-03)
- [koolsb/zwavejs-mcp](https://github.com/koolsb/zwavejs-mcp) - Z-Wave JS UI 维护：修复网络、重新问询、诊断，并对门锁相关信息做脱敏。(★0 · 2026-06)

### USB、HID 与 KVM（MCP）

- [verygoodplugins/streamdeck-mcp](https://github.com/verygoodplugins/streamdeck-mcp) - 通过配置文件操作 Elgato Stream Deck，附带一个 Skill。(★43 · 2026-08)
- [tinqiao-oss/clawtouch-mcp](https://github.com/tinqiao-oss/clawtouch-mcp) - 把树莓派 Pico 2 上真实的 USB-HID 键盘与鼠标暴露为 MCP 工具。(★10 · 2026-09)
- [Oliver0804/cynthion-mcp](https://github.com/Oliver0804/cynthion-mcp) - 驱动 Cynthion USB 测试仪：嗅探、解码与模拟 USB 通信。(★5 · 2026-05)
- [bsu-tool/bsu-tool](https://github.com/bsu-tool/bsu-tool) - "Behavioral Sleuth for USB"：在 Linux 上抓取、解码与分析 USB 协议，同时提供 CLI 与 MCP server。(★5 · 2026-08)
- [elgatosf/elgato-mcp-server](https://github.com/elgatosf/elgato-mcp-server) - Elgato 官方用于自动化其应用的 MCP。(official · ★10 · 2026-09)
- [sunasaji/mcp-serial-hid-kvm](https://github.com/sunasaji/mcp-serial-hid-kvm) - CH9329 USB-HID 加 HDMI 采集：Agent 像 KVM 一样操作一台真实电脑，并带 OCR。(★3 · 2026-04)
- [yindia/qmkmcp](https://github.com/yindia/qmkmcp) - 通过 raw HID 操作任意 QMK / VIA 键盘：灯光、键位、宏。(★0 · 2026-08)
- [Kevin-HYX/kvmctl](https://github.com/Kevin-HYX/kvmctl) - 运行在香橙派上、基于 V4L2 与 USB gadget HID 的 KVM 控制服务，提供 CLI 与 MCP。(★0 · 2026-09)

### EDA / PCB / CAD（MCP）

- [mixelpixx/KiCAD-MCP-Server](https://github.com/mixelpixx/KiCAD-MCP-Server) - 直接从 Claude 编辑 KiCad 原理图与 PCB。(★2.2k · 2026-09)
- [Arcadia-1/virtuoso-bridge-lite](https://github.com/Arcadia-1/virtuoso-bridge-lite) - LLM Agent 与 Cadence Virtuoso 之间的桥，用于 Agent 化的模拟与混合信号设计；在商用 EDA 桥接中星数遥遥领先。(★728 · 2026-09)
- [gokeshenzhen/TraceWeave](https://github.com/gokeshenzhen/TraceWeave) - 基于证据的 RTL 仿真调试 MCP：把 VCS 与 Xcelium 日志和 VCD、FSDB 波形关联起来。(★107 · 2026-09)
- [qfliuyang/hipilot](https://github.com/qfliuyang/hipilot) - VLSI 物理设计助手，带面向 Synopsys ICC2 与 Cadence Innovus 的 MCP server。(★7 · 2026-03)
- [lamaalrajih/kicad-mcp](https://github.com/lamaalrajih/kicad-mcp) - KiCad 工程管理、DRC、BOM 与网表分析。(★521 · 2025-10)
- [salitronic/eda-agent](https://github.com/salitronic/eda-agent) - 290+ 个工具驱动正在运行的 Altium Designer 会话，可选 KiCad / 嘉立创 EDA 专业版。(★199 · 2026-09)
- [jhacksman/OpenSCAD-MCP-Server](https://github.com/jhacksman/OpenSCAD-MCP-Server) - 文本或图片 → 参数化 OpenSCAD 三维模型。(★190 · 2026-09)
- [coffeenmusic/altium-mcp](https://github.com/coffeenmusic/altium-mcp) - Altium Designer PCB 查询与操作。(★158 · 2026-09)
- [Seeed-Studio/kicad-mcp-server](https://github.com/Seeed-Studio/kicad-mcp-server) - 矽递维护的 KiCad MCP：引脚级连通性追踪与设计编辑。(official · ★129 · 2026-09)
- [mapleleavessssssss-wq/vivado-mcp](https://github.com/mapleleavessssssss-wq/vivado-mcp) - 30 个工具的 Vivado MCP，支持 GUI、Tcl 与附加模式。(★127 · 2026-08)
- [circuit-synth/kicad-sch-api](https://github.com/circuit-synth/kicad-sch-api) - KiCad 原理图 s-expression 的 Python API，带一个 [MCP 封装](https://github.com/circuit-synth/mcp-kicad-sch-api)。(★52 · 2025-12)
- [Netlist-Studio/kicad-mcp](https://github.com/Netlist-Studio/kicad-mcp) - 通过 IPC API 控制 KiCad 9。(★18 · 2026-02)
- [octoco-ltd/sheetsdata-mcp](https://github.com/octoco-ltd/sheetsdata-mcp) - 元器件数据手册：从 PDF 提取规格、引脚图与绝对最大额定值。(★11 · 2026-04)
- [WangErShao/SynthAid_quartus_mcp](https://github.com/WangErShao/SynthAid_quartus_mcp) - 22 个工具的 Intel Quartus MCP。(★3 · 2026-06)

### 边缘 AI 与 SBC（MCP）

- [Zalmotek/jetson-mcp](https://github.com/Zalmotek/jetson-mcp) - 通过 SSH 监视并远程控制 Jetson。(★11 · 2025-04)
- [axonixtools/PocketMCP](https://github.com/axonixtools/PocketMCP) - 把安卓手机变成暴露其传感器的 MCP server。(★17 · 2026-08)
- [edgeimpulse/ei-agentic-claude](https://github.com/edgeimpulse/ei-agentic-claude) - 官方 `@edgeimpulse/mcp-server` npm 包的源码；Studio 工作流的概念验证，不负责部署到设备。(official · ★3 · 2026-02)
- [marc-shade/coral-tpu-mcp](https://github.com/marc-shade/coral-tpu-mcp) - Google Coral Edge TPU 推理；唯一的 Coral 条目。(★1 · 2026-02)
- [dmmdea/Hailo-8L-Analysis-Pipelines](https://github.com/dmmdea/Hailo-8L-Analysis-Pipelines) - 14 个工具的 MCP，在 Hailo-8L 上跑人脸检测、OCR 与 CLIP。(★0 · 2026-08)
- [grammy-jiang/RaspberryPiOS-MCP](https://github.com/grammy-jiang/RaspberryPiOS-MCP) - 树莓派 OS：GPIO、I2C、摄像头。(★0 · 2026-03)

### 数字制造（MCP）

- [DMontgomery40/mcp-3D-printer-server](https://github.com/DMontgomery40/mcp-3D-printer-server) - OctoPrint、Klipper、Duet、Repetier、Prusa、拓竹与创想三维，外加 STL 操作。(★236 · 2026-07)
- [DMontgomery40/bambu-printer-mcp](https://github.com/DMontgomery40/bambu-printer-mcp) - 拓竹本地 MQTT / FTPS，外加 BambuStudio 切片与 STL 操作。(★140 · 2026-07)
- [griches/bambu-mcp](https://github.com/griches/bambu-mcp) - 仅限局域网的拓竹 MQTT / FTPS 机群管理。(★45 · 2026-03)
- [OctoEverywhere/mcp](https://github.com/OctoEverywhere/mcp) - 免费的 3D 打印 MCP：实时状态、摄像头抓图、控制。(★36 · 2025-07)
- [Charleslotto/klipper-mcp](https://github.com/Charleslotto/klipper-mcp) - 通过 Moonraker 控制 Klipper，100+ 个工具，支持换头，并对危险操作设有"上膛"开关。(★23 · 2026-08)
- [bjan/pycentauri](https://github.com/bjan/pycentauri) - Elegoo Centauri Carbon（SDCP WebSocket / MQTT）的客户端、CLI 与 MCP。(★22 · 2026-07)
- [schwarztim/bambu-mcp](https://github.com/schwarztim/bambu-mcp) - 拓竹本地 MQTT + FTPS + X.509，带摄像头与 AMS，25 个工具。(★19 · 2026-09)
- [GLechevalier/OpenGalatea](https://github.com/GLechevalier/OpenGalatea) - 通过 PrusaLink 控制 Prusa：Printables 搜索、自动切片、完整任务控制。(★19 · 2026-04)
- [Noosbai/PrusaMCP](https://github.com/Noosbai/PrusaMCP) - PrusaSlicer MCP，17 个工具，带 FDM 参数推荐引擎与网格分析。(★8 · 2026-02)
- [zackpeters93/ugs-mcp](https://github.com/zackpeters93/ugs-mcp) - 通过 Universal GCode Sender Pendant REST API 控制 GRBL 数控机床，运动指令需令牌授权。(★5 · 2026-06)
- [damione1/maslow-desktop](https://github.com/damione1/maslow-desktop) - Maslow CNC（FluidNC）控制面板，带 MCP。(★3 · 2026-07)
- [bleugreen/openpnp-mcp](https://github.com/bleugreen/openpnp-mcp) - OpenPnP；找到的唯一贴片机 MCP。(★0 · 2026-03)

### 音频、灯光与生物信号（MCP）

- [roomi-fields/osc-bridge](https://github.com/roomi-fields/osc-bridge) - 面向数百款硬件合成器的 OSC ↔ MIDI / SysEx 桥，附带配套 Skill。(★7 · 2026-08)
- [NeuroSkill-com/skill](https://github.com/NeuroSkill-com/skill) - 支持 20+ 种脑电设备（Emotiv、OpenBCI、Muse）的桌面脑机接口应用，带 Agent Skill。(official · ★103 · 2026-09)
- [enkhbold470/bci-mcp](https://github.com/enkhbold470/bci-mcp) - 通过 BrainFlow 与 LSL 获取 OpenBCI / Muse 的实时脑电状态。(★17 · 2026-09)
- [kieranklaassen/farmbot-agent-cli-mcp](https://github.com/kieranklaassen/farmbot-agent-cli-mcp) - 通过 MQTT / CeleryScript RPC 控制 FarmBot 硬件。(★3 · 2026-05)
- [tamengual/neptune-apex-mcp](https://github.com/tamengual/neptune-apex-mcp) - Neptune Apex 水族箱控制器：探头、插座、喂食、程序编辑。(★2 · 2026-03)
- [prmichaelsen/dmx-mcp](https://github.com/prmichaelsen/dmx-mcp) - 通过 OLA 与 Enttec USB 适配器控制 DMX 灯光。(★0 · 2026-03)
- [jamiew/digitakt-digitone-mcp](https://github.com/jamiew/digitakt-digitone-mcp) - 通过 MIDI 控制 Elektron Digitakt / Digitone，各 43 个工具。(★0 · 2026-07)

### 航天与地面站（MCP）

- [alti3/stk-mcp](https://github.com/alti3/stk-mcp) - 驱动 Ansys STK Desktop 与 Engine：场景、卫星、可见性分析。(★42 · 2026-01)
- [dsi012/mcp-server-cFS](https://github.com/dsi012/mcp-server-cFS) - 用自然语言控制 NASA core Flight System 软件总线。(★1 · 2025-10)
- [Pranav-d33/gnuradio-mcp-server](https://github.com/Pranav-d33/gnuradio-mcp-server) - 构建并运行 GNU Radio 流图。(★1 · 2026-06)
- [harris-mohamed/satnogs-mcp](https://github.com/harris-mohamed/satnogs-mcp) - SatNOGS 卫星地面站网络。(★0 · 2026-04)

### 船舶、航空与铁路（MCP）

- [VesselSense/signalk-mcp-server](https://github.com/VesselSense/signalk-mcp-server) - 把 SignalK server 作为 MCP：船舶状态、AIS 与源自 NMEA 的数据路径。(★11 · 2025-11)
- [cyanheads/noaa-marine-mcp-server](https://github.com/cyanheads/noaa-marine-mcp-server) - NOAA 潮汐站与 NDBC 浮标的硬件数据源。(★1 · 2026-08)
- [HO44-PROJECT/MrJ-JMRI-MCP](https://github.com/HO44-PROJECT/MrJ-JMRI-MCP) - 面向 DCC 模型铁路的 JMRI：道岔、调速器、进路。(★1 · 2026-08)
- [pipeworx-io/mcp-opensky](https://github.com/pipeworx-io/mcp-opensky) - 通过 OpenSky Network 追踪 ADS-B 航空器。(★0 · 2026-09)
- [deanjbrown/geotab-mcp](https://github.com/deanjbrown/geotab-mcp) - MyGeotab 车队远程信息：设备状态、故障、行驶记录仪文件、油耗。(★0 · 2026-09)

### 半导体与科学仪器（MCP）

- [vibeic/vibe-ic](https://github.com/vibeic/vibe-ic) - AI 原生的芯片设计插件，通过 MCP-EDA 打通从意图到验证后硅片的路径。(★25 · 2026-09)
- [Jacky1-Jiang/EPICS-MCP-Server](https://github.com/Jacky1-Jiang/EPICS-MCP-Server) - EPICS 过程变量读写——大多数加速器与大型望远镜背后的控制系统。(★4 · stale since 2025-05)
- [seikaikyo/secsgem-mcp-server](https://github.com/seikaikyo/secsgem-mcp-server) - SECS/GEM 半导体设备控制。(★1 · 2026-09)
- [BCDA-APS/bait_mcp](https://github.com/BCDA-APS/bait_mcp) - 通过 Bluesky 队列服务控制先进光子源（APS）光束线。(official · ★1 · 2026-09)
- [Oekalegon/indi-mcp](https://github.com/Oekalegon/indi-mcp) - 在树莓派上通过 INDI 控制天文摄影赤道仪与相机。(★0 · 2026-09)

### 专业 AV、门禁与标牌（MCP）

- [Z-bit-Systems-LLC/OSDP-Embedded](https://github.com/Z-bit-Systems-LLC/OSDP-Embedded) - 其中的 `osdp-mcp` 暴露一个虚拟 OSDP 外设，让 Agent 充当读卡器去测试真实的门禁控制器——物理安防领域里的硬件在环模式。(★5 · 2026-08)
- [reowens/qsys-tools](https://github.com/reowens/qsys-tools) - 通过 QRC 控制 QSC Q-SYS，提供 CLI、TypeScript 客户端与 MCP server，已在真实 Core 上测试。(★3 · 2026-07)
- [DaScheife/Sklera-Digital-Signage-MCP-Server](https://github.com/DaScheife/Sklera-Digital-Signage-MCP-Server) - Sklera 数字标牌屏幕。(★2 · 2026-06)
- [tkrisztian95/eink-mcp-server](https://github.com/tkrisztian95/eink-mcp-server) - 在微雪墨水屏上绘制仪表盘或原始像素。(★0 · 2026-04)

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
- [arm/device-connect](https://github.com/arm/device-connect) - Arm 的开放协议，让 Agent 通过网络发现、调用与编排设备和机器人。(official · ★94 · 2026-08)
- [device-context-protocol/dcp](https://github.com/device-context-protocol/dcp) - "Device Context Protocol"：小于 50 字节的 CBOR 帧，在 ESP32 上仅占 27.6 KB 闪存与 0.6 KB 内存，带能力范围清单、HMAC、试运行，并提供 DCP ↔ MCP 桥。(★57 · 2026-05)
- [macc-n/wot-mcp](https://github.com/macc-n/wot-mcp) - W3C 物联网（Web of Things）Thing Description → MCP：属性变成读写工具、动作变成工具、事件变成资源，支持 HTTP / CoAP / MQTT。(★9 · 2026-02)
- [w3c-cg/webagents](https://github.com/w3c-cg/webagents) - W3C"Web 上的自主 Agent"社区组：基于 WoT 与关联数据的超媒体多 Agent 系统。(★47 · 2026-08)
- [agenticros/agenticros](https://github.com/agenticros/agenticros) - 面向 OpenClaw、Claude Code、Codex 与 Gemini 的 ROS 2 插件：机器人暴露带类型的能力动词（`drive_base`、`find_object`），其清单的形状刻意设计成可兼作 ACP / A2A agent card；真正在线上跑 A2A 仍在路线图上。(★148 · 2026-09)
- [win4r/openclaw-a2a-gateway](https://github.com/win4r/openclaw-a2a-gateway) - 实现 A2A v0.3 的 OpenClaw 插件（JSON-RPC / REST / gRPC、mDNS、agent card）；纯软件，但天然适合作为 agenticros 的前端。(★555 · 2026-07)
- [strands-labs/robots](https://github.com/strands-labs/robots) - 通过 Strands Agents 用自然语言控制 70+ 种机器人；机器人以 Zenoh 对等节点组网，并通过 AWS IoT Core 桥接机队。(★157 · 2026-09)
- [agntcy/slim](https://github.com/agntcy/slim) - AGNTCY 的安全低延迟交互消息（SLIM）；配合 `slim-a2a-*` 与 A2A 自己的 SLIM-RPC 扩展，是 A2A 唯一的低延迟传输绑定。(★218 · 2026-09)
- [QUSD-ai/m5stick-nanda](https://github.com/QUSD-ai/m5stick-nanda) - M5StickC Plus 2 的 ESP32 固件，直接在设备上提供 agent card 与 JSON-RPC；但它是按关键词匹配而非按协议方法分发，而且发布当天就被弃置。收录它，是因为这是现存最接近"A2A 跑在硬件上"的东西。(★0 · 2026-01)
- [r1marcus/TinyA2A](https://github.com/r1marcus/TinyA2A) - 面向 STM32 与 ESP-IDF 的 C11 Agent 意图库，带 MQTT JSON 与 64 字节 CAN-FD 帧两种 profile。与 Linux 基金会的 A2A 同名，但线格式并不相同。(★2 · 2026-05)

### 端侧 Agent 运行时

直接运行在单片机或 SBC 上、带工具调用能力的 Agent 循环，而非跑在宿主机上。

- [espressif/esp-claw](https://github.com/espressif/esp-claw) - ESP32-S3 / P4 / C5 上的 Agent 运行时：能力用 C 写、Skill 用 Lua 写，双向 MCP，事件路由。(official · ★2.1k · 2026-09)
- [memovai/mimiclaw](https://github.com/memovai/mimiclaw) - 无操作系统、C / ESP-IDF 实现，跑在 ESP32-S3 上：Anthropic 工具调用 ReAct 循环、Telegram、本地记忆。MCU 版 claw 家族的领头羊。(★5.7k · 2026-08)
- [sipeed/picoclaw](https://github.com/sipeed/picoclaw) - 内存占用不到 10 MB 的单个 Go 二进制，面向 LicheeRV-Nano / MaixCAM / Pi Zero，带完整的 MCP 与 Skill 循环。(official · ★30k · 2026-09)
- [zeroclaw-labs/zeroclaw](https://github.com/zeroclaw-labs/zeroclaw) - 面向树莓派级 SBC 的 Rust 重写版（3.4 MB）；[nullclaw](https://github.com/nullclaw/nullclaw)（Zig，678 KB）额外提供树莓派 GPIO 与 STM32 / Nucleo 外设工具。(★32.8k · 2026-09)
- [M64GitHub/WireClaw](https://github.com/M64GitHub/WireClaw) - 基于 Arduino / PlatformIO，跑在 ESP32-C3 / C6 / S3 上：大模型调用 `gpio_write` 与 `rule_create` 实现离线自动化；支持 Telegram、串口、NATS；带网页烧录器。(★188 · 2026-02)
- [jetpax/pycoclaw](https://github.com/jetpax/pycoclaw) - 跑在 ESP32-S3 / P4 / C6 上的 MicroPython 实现，支持递归工具调用、MCP 客户端与 GPIO / I2C / CAN 工具；Agent 核心尚未公开。(★164 · 2026-04)
- [wireless-tag-com/EmbedClaw](https://github.com/wireless-tag-com/EmbedClaw) - 启明云端的 C / ESP-IDF 实现，跑在 ESP32-S3 上，带 JSON-schema 工具注册表与 ReAct 循环，适配通义千问 / DeepSeek / 豆包 / Kimi；首个模组厂商分支。(official · ★45 · 2026-04)
- [laurenvil/Uno-QClaw](https://github.com/laurenvil/Uno-QClaw) - 跑在 Arduino UNO Q 上的 picoclaw 分支，本地运行 Qwen3.5-0.8B：能自己写代码、编译并通过 OpenOCD 烧录自己的 MCU，带摄像头与 I2C 扫描，完全离线。(★19 · 2026-06)
- [hrwtech/openclaw-esp32](https://github.com/hrwtech/openclaw-esp32) - 把 OpenClaw 的 Agent 循环移植到 ESP32 板上；OpenClaw 本身不附带任何硬件 Skill。(★10 · 2026-02)
- [espressif/esp-brookesia](https://github.com/espressif/esp-brookesia) - AIoT 人机界面框架，其 Agent 管理器为扣子、OpenAI 与小智提供 Function Calling 与 MCP 适配。(official · ★788 · 2026-09)
- [tuya/TuyaOpen](https://github.com/tuya/TuyaOpen) - 面向 T2 / T3 / T5AI 与 ESP32 的 C SDK，带端侧推理引擎；Agent 的"大脑"仍在涂鸦云端 Agent Hub。(official · ★1.8k · 2026-09)
- [XiaoMi/xiaomi-miloco](https://github.com/XiaoMi/xiaomi-miloco) - 基于 MiMo 的 OpenClaw 插件：家庭摄像头感知驱动米家设备控制；需要 4 GB 以上内存的主机，而非单片机。(official · ★3.3k · 2026-09)
- [NVIDIA-AI-IOT/jetson-ai-lab](https://github.com/NVIDIA-AI-IOT/jetson-ai-lab) - 在 Jetson 上运行 OpenClaw 的官方路径：Orin Nano 用 Ollama，AGX / Thor 用 vLLM。(official · ★207 · 2026-09)
- [HeyWillow/willow](https://github.com/HeyWillow/willow) - ESP32-S3 语音设备固件，把音频流式发送到服务器由服务器执行工具；与 esp-ai、ElatoAI 一样，端侧没有 Agent 循环。(★3.1k · 2026-09)

### 机器人与具身 Agent 框架

- [dimensionalOS/dimos](https://github.com/dimensionalOS/dimos) - 面向物理空间的 Agent 操作系统：用自然语言指挥人形机器人、宇树四足、xArm 与 MAVLink 无人机。(★4.5k · 2026-09)
- [ros-claw/rosclaw](https://github.com/ros-claw/rosclaw) - "可信的物理执行运行时"：失效即关闭的策略、执行回执、MCP 工具发现、安全包络、ROS 2；alpha 阶段，已在 UR5e 仿真中验证。(★197 · 2026-09)
- [Grigorij-Dudnik/RoboCrew](https://github.com/Grigorij-Dudnik/RoboCrew) - `pip install robocrew`：带运动工具、VLA 策略与传感器扫描的大模型 Agent；XLeRobot 演示。(★139 · 2026-08)
- [Hugging Face LeRobot](https://github.com/huggingface/lerobot) - 端到端的机器人学习：数据集、ACT / Diffusion / VLA 策略，SO-100 / 101、Koch 与 LeKiwi 的驱动；附带面向 Agent 的 `AGENT_GUIDE.md`。(★27.5k · 2026-09)
- [isaac-sim/IsaacLab](https://github.com/isaac-sim/IsaacLab) - 基于 Isaac Sim 的统一机器人学习框架：强化学习、模仿学习、仿真到现实迁移。(★8.1k · 2026-09)
- [NVIDIA/Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T) - 面向通用人形机器人的 GR00T 基础模型，带微调与推理栈以及一份 `AGENTS.md`。(★8.1k · 2026-08)
- [openvla/openvla](https://github.com/openvla/openvla) - 用于操作任务的 7B 开源视觉-语言-动作模型；VLA 的参考实现，现已冻结。(★7k · 2025-03)
- [nasa-jpl/rosa](https://github.com/nasa-jpl/rosa) - 用自然语言检视、诊断并操作 ROS 1 / 2 机器人的 LangChain Agent。(★1.6k · 2026-03)
- [FlagOpen/RoboOS](https://github.com/FlagOpen/RoboOS) - 智源研究院的"大脑–小脑"具身操作系统：RoboBrain 多模态大模型、Skill 库与多机器人共享记忆。(official · ★622 · 2025-12)
- [automatika-robotics/embodied-agents](https://github.com/automatika-robotics/embodied-agents) - ROS 2 原生框架，用于构建带 LLM / VLM 组件的交互式物理 Agent。(★67 · 2026-09)

### 智能家居与设备平台

- [Home Assistant LLM API](https://developers.home-assistant.io/docs/core/llm/) - 官方的 Assist LLM API：各集成注册的工具可被任意对话 Agent 调用。(official)
- [acon96/home-llm](https://github.com/acon96/home-llm) - Home Assistant 集成，外加为设备控制微调的本地模型。(★1.4k · 2026-09)
- [arm/mcp](https://github.com/arm/mcp) - Arm 官方 MCP：文档检索、迁移分析、汇编性能分析。Nordic、Microchip、Silicon Labs、TI 与 ADI 也发布过类似的纯文档型厂商 MCP。(official · ★91 · 2026-09)

## 验证基础设施

用来运行硬件 Skill `evals/` 的工具。模拟器与托管虚拟板用于迭代和预检——它们都无法让一个 Skill 通过，因为通过需要真实的板子。驱动真实板子的设备农场是例外：在上面跑的结果算数。

### 模拟器与仿真器

- [wokwi/wokwi-cli](https://github.com/wokwi/wokwi-cli) - ESP32 全系列、AVR、RP2040、nRF52、部分 STM32，外加传感器与显示屏。YAML 场景可断言串口文本并设置引脚；提供 GitHub Action；开源项目可免费获得 CI 令牌。仿真核心是托管且闭源的。本仓库 `L1 (wokwi)` 预检的后端。(★66 · 2026-06)
- [renode/renode](https://github.com/renode/renode) - Cortex-M / A / R、RISC-V、Xtensa，整板与多节点网络；`.resc` 脚本、Robot Framework 测试框架、Zephyr twister 集成，确定性执行。MIT 许可。断言层已经存在——`renode-test` 以 `Wait For Line On Uart` 这类关键字驱动 Robot Framework——但还没有东西替 Agent 封装一个活的会话。本仓库 `L1 (renode)` 预检的后端。(★2.9k · 2026-09)
- [qemu/qemu](https://github.com/qemu/qemu) - ARM `mps2` 等机型、RISC-V、x86；[乐鑫的分支](https://github.com/espressif/qemu)增加了 Xtensa / ESP32。提供 QMP JSON API 与 GDB 桩。文献中被用于 FreeRTOS 的模糊测试与修补循环。(★13.7k · 2026-09)
- [Zephyr native_sim](https://docs.zephyrproject.org/latest/boards/native/native_sim/doc/index.html) - 把任意 Zephyr 应用构建成宿主机上的 Linux 可执行文件，带仿真的 I2C / SPI / GPIO 与 BabbleSim BLE；`twister -p native_sim`。Zephyr 类 Skill 最便宜的 L1 方案。(official)
- [gazebosim/gz-sim](https://github.com/gazebosim/gz-sim) - 带 ROS 2 桥与传感器的机器人世界；`gz sim -s -r world.sdf` 可无头运行。(★1.5k · 2026-09)
- [google-deepmind/mujoco](https://github.com/google-deepmind/mujoco) - 带 Python 绑定与 MJX GPU 版本的多体动力学引擎；LIBERO 与大多数 VLA 评测的底座。(★15.1k · 2026-09)
- [isaac-sim/IsaacSim](https://github.com/isaac-sim/IsaacSim) - 照片级真实感的机器人仿真；支持 `--headless` 与 Python 独立脚本；5.0 起开源，需要 RTX 显卡。适合每晚跑，而不适合每个 PR 都跑。(★4.1k · 2026-09)
- [cyberbotics/webots](https://github.com/cyberbotics/webots) - 带 ROS 2 桥的机器人仿真；`webots --batch --no-rendering`。(★4.6k · 2026-09)
- [mani-skill/ManiSkill](https://github.com/mani-skill/ManiSkill) - 基于 SAPIEN、离屏 Vulkan 渲染的 GPU 并行操作任务仿真；本身也是一个评测基准。(★3.3k · 2026-08)
- [pymodbus-dev/pymodbus](https://github.com/pymodbus-dev/pymodbus) - `pymodbus.simulator` 根据 JSON 寄存器定义提供一个 Modbus TCP / RTU 设备，并带 HTTP 控制 API。本仓库 `L1 (modbus-sim)` 预检的后端。(★2.8k · 2026-09)
- [open62541/open62541](https://github.com/open62541/open62541) - OPC UA 服务端 / 客户端；其示例服务器可以充当可用的 PLC 替身。(★3.2k · 2026-09)
- [Home Assistant 演示模式](https://www.home-assistant.io/integrations/demo/) - `hass --demo-mode` 在真实的 REST / WebSocket API 背后创建虚拟的灯、空调与传感器。本仓库 `L1 (ha-demo)` 预检的后端。(official)
- [micropython/micropython unix 移植](https://github.com/micropython/micropython/tree/master/ports/unix) - 宿主机上的 MicroPython 虚拟机；只能做逻辑层检查，没有外设。(★22k · 2026-09)
- [ARM-software/AVH](https://github.com/ARM-software/AVH) - Arm 虚拟硬件：Cortex-M FVP（Corstone-300 / 310 / 315），附 GitHub Actions 示例；对开源与评估用途免费。(official · ★54 · 2026-09)

不适合 CI，列出来免得有人再查一遍：Tinkercad Circuits（无 API）、SimulIDE（仅 GUI）、Proteus VSM（商业软件，以 GUI 为中心）、Simulavr（2023 年起停止维护）。

### 虚拟硬件与设备农场

- [veecle/chiplab](https://github.com/veecle/chiplab) - 只通过 MCP 暴露的托管虚拟 STM32 与 Nordic Cortex-M 板：上传 ELF、读取串口。专为编程 Agent 打造。(★16 · 2026-08)
- [eust-w/agentic-embedded-lab](https://github.com/eust-w/agentic-embedded-lab) - Agent 原生的嵌入式实验室，带可插拔的仿真后端与基于证据的验证；最接近"以 Renode 为后端的测试框架"的东西。(★33 · 2026-09)
- [EliasOenal/term-cli](https://github.com/EliasOenal/term-cli) - 为 Agent 提供的交互式终端，专为那些无法自动确认的提示而生：带 MFA 的 SSH、GRUB 与 U-Boot 控制台、debconf。(★101 · 2026-08)
- [jumpstarter-dev/jumpstarter](https://github.com/jumpstarter-dev/jumpstarter) - 红帽支持的硬件在环框架，面向真实或虚拟目标、本地或远程，Kubernetes 原生，并明确为"人类、自动化或 Agent"三类驱动方设计；带电源、串口与烧录驱动。最适合搭建 L2 设备农场。(★219 · 2026-09)
- [labgrid-project/labgrid](https://github.com/labgrid-project/labgrid) - Pengutronix 的板卡控制库（电源、串口、USB、网络启动），集成 pytest。(★527 · 2026-09)
- [kernelci/kernelci-core](https://github.com/kernelci/kernelci-core) - 带开放 API 的社区硬件实验室；实验室由 Collabora、BayLibre 等捐赠。(★120 · 2026-09)
- [Linaro LAVA](https://gitlab.com/lava/lava) - KernelCI 与 Linaro 实验室使用的板卡农场调度器；可自建部署。(★82 · 2026-09)
- [Zephyr twister 设备测试](https://docs.zephyrproject.org/latest/develop/test/twister.html) - `twister --device-testing --hardware-map` 在连接的板子上运行测试套件；[golioth/zephyr_twister_hil_testing](https://github.com/golioth/zephyr_twister_hil_testing) 演示了如何在 GitHub 自托管 runner 上实现。(official)
- [Wokwi CI](https://docs.wokwi.com/wokwi-ci/getting-started) - 在 GitHub Actions 中运行托管仿真；开源项目可免费获得令牌。(official)
- [OpenHiL](https://openhil.github.io/) - 开源硬件在环工具的社区中心。

## 评测基准

只有前两个在真实单片机上发布过结果；其余要么只查编译，要么只跑仿真。

- [iot-agent/iot-skillsbench](https://github.com/iot-agent/iot-skillsbench) - 在 ATmega2560 / Arduino、ESP32-S3 / ESP-IDF 与 nRF52840 / Zephyr 上的 42 个硬件在环任务，覆盖 23 种外设、3 个难度等级；在真实板子上对比"不用 Skill、LLM 生成的 Skill、专家编写的 Skill"三种情况。其 30 个专家 Skill 是带 frontmatter 的单文件 `.md`，可轻松转换为 SKILL.md。论文：[arXiv 2603.19583](https://arxiv.org/abs/2603.19583)。(★41 · 2026-07)
- [ubicomplab/embedded-arena](https://github.com/ubicomplab/embedded-arena) - 硬件在环竞技场：Agent 修改模型与固件，测试框架负责编译、烧录，并对可部署性、电流、能耗与温度打分。前沿模型在没有硬件反馈时得分为 0%，有了反馈则三轮内即可成功。论文：[arXiv 2606.16190](https://arxiv.org/abs/2606.16190)。(★11 · 2026-07)
- [cezman/ironharness](https://github.com/cezman/ironharness) - 固件 Agent 的 pass@k 基准，可跑在 Wokwi、Renode 或真实硬件上，外面套一层沙箱化的 MCP I/O 框架。非常早期。(★2 · 2026-09)
- [EmbedBench / EmbedAgent](https://arxiv.org/abs/2506.11003) - 在 Uno / ESP32 / Pico 上覆盖 9 类元件的 126 个用例，分程序员、架构师与集成者三种角色；无公开仓库。
- [EmbedGenius](https://arxiv.org/abs/2412.09058) - 借助硬件感知检索生成嵌入式 IoT 软件。
- [面向嵌入式软件开发的 LLM Agent 闭环评测](https://www.sciencedirect.com/science/article/pii/S1383762126002559) - 五个嵌入式控制任务，在四种反馈机制下评测：一次性生成、自我验证、CI 红绿灯、预言机。
- [NVlabs/verilog-eval](https://github.com/NVlabs/verilog-eval) - Verilog 补全与"规格到 RTL"，用 iverilog 校验 pass@k。(★469 · 2025-07)
- [hkust-zhiyao/RTLLM](https://github.com/hkust-zhiyao/RTLLM) - 自然语言 → RTL：语法、功能、PPA。(★227 · 2026-08)
- [HardSecBench](https://arxiv.org/abs/2601.13864) - 评估 LLM 生成的 RTL 与 C 固件的安全意识。
- [EmbodiedBench/EmbodiedBench](https://github.com/EmbodiedBench/EmbodiedBench) - 面向多模态具身 Agent 的 1128 个任务，覆盖 ALFRED、Habitat、导航与操作。(★341 · 2026-05)
- [StanfordVL/BEHAVIOR-1K](https://github.com/StanfordVL/BEHAVIOR-1K) - OmniGibson 中的 1000 项家务活动。(★1.7k · 2026-09)
- [Lifelong-Robot-Learning/LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO) - 130 个终身学习式操作任务；事实上的 VLA 评测标准。(★2.3k · 2025-03)
- [stepjam/RLBench](https://github.com/stepjam/RLBench) - CoppeliaSim 中的 100 个操作任务。(★1.8k · 2025-01)
- [holi-lab/SimuHome](https://github.com/holi-lab/SimuHome) - 基于 Matter、可加速时间的智能家居仿真器，含 600 个 episode，涵盖定时与隐含意图。ICLR 2026 口头报告。(★34 · 2026-04)
- [SMH-Bench](https://arxiv.org/abs/2606.01912) - 在最多 135 台设备的家庭中设置的 1100 个智能家居任务；代码尚未发布。

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
- [Coscientist](https://github.com/gomesgroup/coscientist) - 驱动 Opentrons 移液工作站与 Emerald Cloud Lab 的 GPT-4 Agent。Nature 2023。(★211 · 2025-08)
- [Autonomous Chemistry and Materials Innovation Driven by Scientific Agents](https://pubs.acs.org/doi/10.1021/jacsau.6c00213) - 关于由 LLM 驱动的自动化实验室的综述。JACS Au 2026。

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

已核查但缺失（404 或返回 HTML）：Zephyr、乐鑫、Nordic、ST、PlatformIO、KiCad、ROS 文档、Golioth、Home Assistant、ESPHome、MicroPython、CircuitPython、树莓派、矽递 Wiki、Isaac Sim / Lab、Embassy、BeagleBoard、ThingsBoard。Zephyr 改为提供 `AGENTS.md`、`CLAUDE.md` 与 `copilot-instructions.md`；nRF Connect SDK 在 HEAD 上三者皆无。

## 空白

尚不存在的东西记录在 **`GAPS.zh-CN.md`** 中，附有每条声明背后的证据、现存最接近的东西（好让声明保持可证伪），以及五个范围明确、连 eval 断言都已写好的首次贡献建议。要点如下：

**A2A 从未真正落到硬件上。** 发布十七个月后，没有任何仓库在真实物理设备上端到端实现 Linux 基金会的 A2A 规范。这份 3618 行的规范中，*robot*、*actuator*、*sensor*、*embedded* 出现次数均为零，1721 个 issue 中也没有一个在要求设备控制。这看起来是设计上的必然而非疏忽：设备是独占的、物理上不可逆的、有时限约束的，而 A2A 建模的是不透明对等方之间可重试的对话。此后所有设备侧的协议尝试——MCP-over-MQTT、Arm Device Connect、DCP——都选择依附于 MCP。

**厂商几乎没有入场。** 只有三家芯片厂商发布过宿主侧 Skill：Arm、瑞萨与德州仪器。ST 有 786 个公开仓库却一个都没有；英飞凌有 2301 个；NXP 有 221 个；树莓派有 115 个，Pico SDK 空空如也。`espressif/skills` 是一个官方仓库，README 教你去安装它，而整棵文件树只有 `README.md` 加一个 `skills/.gitkeep`——2026-04-24 当天创建后三小时内就被弃置。七家厂商发布了 MCP server，没有一家能在仿真中执行任何东西。

**Renode 缺少面向 Agent 的接口。** 模拟器本身不是瓶颈：它确定性执行、可以无头运行，而且已经在 `renode-test` 与 Robot Framework 中自带断言框架。缺的是一个能为 Agent 维持活会话的东西，好让交互式固件调试与 L1 runner 共用同一套集成，而不是各自重新拼凑一段脆弱的 shell 配方。它值得为了更快的迭代而去做——但它无法让任何 Skill 通过，所以验证真正的瓶颈是能否接触到板子，而不是模拟器。

**硬件在环仍是覆盖最少的模式**——烧录、运行、读串口、迭代——尽管它恰恰是唯一有公开证据支撑的模式：前沿模型在没有硬件反馈时部署成功率为 0%，有了反馈则在七轮内超越人类专家。它也是通往"通过"的唯一途径。

同样空白、且每一项都经过核实而非假设：Wi-Fi 配网、树莓派 5 Linux、设备树与 U-Boot、Thread 与设备侧 Matter、非攻击用途的 NFC、Lattice FPGA 工具链、作为 Agent 工具的 VLA 策略、波士顿动力 Spot，以及通用 USB 控制（USB *分析* 已有覆盖）。

## 相关列表

- [beriberikix/awesome-mcp-hardware](https://github.com/beriberikix/awesome-mcp-hardware) - 硬件 MCP server 的上游列表；本列表的 MCP 部分由此起步。
- [TensorBlock/awesome-mcp-servers — hardware & IoT](https://github.com/TensorBlock/awesome-mcp-servers/blob/main/docs/hardware--iot.md) - 某通用 MCP 列表中的硬件分类。
- [fouad1233/amazing-robotics-skills](https://github.com/fouad1233/amazing-robotics-skills) - 区分许可证的 NVIDIA 生态 Skill 索引，覆盖 35 个仓库中的 1039 个 Skill。
- [ros-claw](https://github.com/ros-claw) - 汇集约 35 个机器人与传感器 MCP 的组织，外加一套 Skill 目录格式（SKILL.md + skill.yaml + 行为树）。
- [heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills) - 通用 Agent Skill 目录。
- [skillmatic-ai/awesome-agent-skills](https://github.com/skillmatic-ai/awesome-agent-skills) - 通用 Agent Skill 目录。
- [skills.sh](https://skills.sh) - 带安装量统计的 Skill 注册表；上文引用的安装量即来自这里。
- [ClawHub](https://www.clawhub.ai) - OpenClaw 的 Skill 注册表；收录了一些没有 GitHub 源码的硬件 Skill（esp32、arduino、raspberry、bambu-cli、meshtastic），上文引用的相应安装量即来自这里。

## 贡献

请阅读 [CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md)。简而言之：每个条目一行、放进正确的分类，运行 `python scripts/l0_check.py readme README.md`；如果你添加的是自己维护的 Skill，请把 [`template/evals/`](template/evals/) 复制进去（或者让 `hardware-skill-creator` 和你一起搭建这个包），并在真实板子上跑过之后提交一份 [L2 实测背书](.github/ISSUE_TEMPLATE/attestation.yml)。

新增或修改条目时，请**同时修改** `README.md` 与本文件——CI 会检查两份文档的条目是否一一对应。
