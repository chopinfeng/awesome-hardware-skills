# 尚存的空白

*[English](GAPS.md) · 简体中文*

> 本文档译自 [GAPS.md](GAPS.md)。如两者有出入，以英文版为准。

这份文件是列表的另一半。README 记录已经存在的东西；这里记录尚不存在的东西——附上足够的证据，让你可以亲自核查而不必盲信，也附上足够的细节，让你可以直接开工。

下面每条空白都包含四项内容：

- **状态** —— `EMPTY`（什么都没找到）、`PLACEHOLDER`（官方仓库已建但没有内容）、`DEMO-ONLY`（有产物但都没在真实硬件上跑通）或 `PARTIAL`（覆盖了一部分，其余没有）。
- **核查方式** —— 精确到组织、搜索式与文件，方便你复跑。以下所有核查均在 2026-09-16 进行。
- **为什么重要** —— 为什么值得有人为它花一个周末。
- **现存最接近的东西** —— 刻意点名，好让每条声明都可被证伪。如果你能找到更好的，那说明这条声明是错的，欢迎提交 [pull request](CONTRIBUTING.zh-CN.md) 修正。

某个方向是空白，并不能证明它就应该被填补。有些之所以空着，是因为这个想法本身不好；遇到这种情况，文中会直说。

## 为什么这个方向值得投入

有三件事同时成立，合在一起构成了投入的理由。

**前沿模型在硬件上的失败方式，是它们在软件上不会出现的。** [Embedded Arena](https://arxiv.org/abs/2606.16190) 搭建了一个硬件在环竞技场：Agent 修改模型与固件，测试框架负责编译、烧录，并在真实单片机上给结果打分。它的结论毫不含糊："包括 Claude Opus 4.7 与 Gemini 3.1 Pro 在内的前沿模型，在没有硬件反馈时彻底失败（部署成功率 0%）。"不是变差——是零。给同样的模型加上迭代式的硬件反馈，它们能"在三轮迭代内首次部署成功，并在七轮内超越人类专家的结果"。

**专家编写的 Skill 能补上这个差距。** [IoT-SkillsBench](https://arxiv.org/abs/2603.19583) 在 42 个任务、3 个平台、23 种外设上做了 378 次真机验证实验，对比了不用 Skill、LLM 生成的 Skill 与人类专家编写的 Skill。结论是："简洁的人类专家 Skill 配合结构化的专家知识，能在各平台上实现接近满分的成功率。"补上这道差距的知识，恰恰是那种藏在勘误表和资深工程师脑子里的东西——哪个引脚同时是启动配置引脚、哪个外设会悄悄截断数据、哪个 SDK 符号必须写进 `sdkconfig.defaults` 而不是只在 menuconfig 里改。

**掌握这些知识的人还没有入场。** 在为本列表调研的所有芯片厂商中，只有三家发布过宿主侧 Agent Skill：Arm、瑞萨与德州仪器。ST 有 786 个公开仓库，一个 Skill 都没有。英飞凌有 2301 个。NXP 有 221 个。树莓派有 115 个，Pico SDK 空空如也。与此同时，面向这些芯片的社区 Skill 每周被安装数千次。

所以：能力差距已被量化，修复方法已经明确，需求已经得到证明，而供给恰恰缺在真正掌握一手资料的地方。这是一个难得清晰的动手理由。

第四件事，则是本仓库之所以要有一套[验证阶梯](README.zh-CN.md#条目如何验证)的原因。Veecle 在 [LLMs write good firmware. They can't prove it.](https://veecle.ai/blog/llms-write-good-firmware-cant-prove-it) 一文里说得最好：瓶颈不在生成，而在证明。一个没人能验证的 Skill 只是一个声称，而不是一个工具。而且证明必须来自芯片本身：本列表只有在一个 Skill 的任务于真实板子上运行过之后，才认为它通过。

## A2A 在硬件侧

**状态：EMPTY。** 发布十七个月后，没有任何仓库在真实物理设备上端到端实现 Linux 基金会的 [A2A](https://github.com/a2aproject/A2A) 规范。

**核查方式。** `a2aproject` 组织共有 19 个仓库——六个 SDK、规范、CLI、inspector、TCK、ITK、gateway 与两个扩展——没有一个与硬件相关。其示例集包含 32 个 Python Agent，外加 3 个 JS、5 个 Java、3 个 Go 与 3 个 .NET；没有一个接触过设备。规范共 3618 行，*robot*、*hardware*、*actuator*、*IoT*、*sensor*、*drone*、*embedded* 的出现次数均为零；"device"唯一的一次匹配是 `DeviceCodeOAuthFlow`，那是 OAuth。在全部状态共 1721 个 issue 中，没有一个在要求设备控制。确实存在的四个与硬件沾边的 issue——#2078 与 #2088 关于基于硬件的远程证明，#2167 关于以硬件为锚的信任分级，#2076 关于边缘-云端能力契约——方向恰好相反：是硬件为 Agent 提供安全保障，而不是 Agent 驱动硬件。两个公开的 A2A 目录共收录 316 个 Agent，物理 Agent 为零；而 KoPass 统计的公开 A2A 仓库总数为 1610 个。topic 交叉搜索同样一片空白：`a2a-protocol` 加 `robot`、`robotics`、`iot`、`ros` 的结果都是零。

**现存最接近的东西。** [QUSD-ai/m5stick-nanda](https://github.com/QUSD-ai/m5stick-nanda)——M5StickC Plus 2 的 ESP32 固件，直接在设备上提供 `/.well-known/agent.json` 与一个 JSON-RPC `/rpc` 端点。这是现存最接近的产物，但仍然差得远：处理函数靠 `indexOf("sensor")` 和 `indexOf("beep")` 做关键词匹配，而不是读取 JSON-RPC 的 `method`；没有 `tasks/get`，没有任务生命周期，没有流式传输；代码树里的一个 `nanda_server.cpp.bak` 还表明，设备端 server 已被撤下，改为宿主机侧的代理。它在创建当天就被弃置了。

**为什么是空的——以及为什么这可能是对的。** 这是最有可能长期空着的一条，原因是结构性的。[LAP](https://arxiv.org/abs/2606.03755)（Zhu 等，2026 年 6 月）精确地指出了这一点：现有的互操作协议"厘清了 Agent 生态三条边中的两条……但都没有建模 Agent 到仪器这条边——在这条边上，操作是有状态的、安全攸关的、独占的、有物理实体的，并且产出带有单位、校准与不确定度的测量结果"。A2A 建模的是不透明对等方之间可重试的多轮对话。设备则完全不是这样：它是独占的、物理上不可逆的、有时限约束的。急停不是一个可以重试的任务。规范里没有 QoS、没有截止时间、没有联锁，服务发现走的是 HTTPS well-known 路径，而不是任何能在局域网里工作的机制。

市场的选择与此一致。MCP-over-MQTT 创建于 2025-04-16，距 A2A 发布仅一周；此后所有设备侧的协议尝试都依附于 MCP——[wot-mcp](https://github.com/macc-n/wot-mcp)、[arm/device-connect](https://github.com/arm/device-connect)、[DCP](https://github.com/device-context-protocol/dcp)——没有一个依附于 A2A。[Robot Context Protocol](https://arxiv.org/abs/2506.11650) 走得更远，把 A2A 放进客户端边缘的适配器里，让它去和"那个跟机器人说话的东西"对话。

**填补它会是什么样子。** 不是 fork，而是一个扩展，放在 Secure Passport 与 x402 已经在用的那个位置上，声明规范所缺的三样东西：带 TTL 的 `reservation`，防止两个 Agent 同时驱动底盘；一个 `safety` 块，携带声明的物理限值，以及任何运动任务都必须附带的联锁令牌；以及每条消息的 `deadline_ms`，执行方可以直接拒绝而非排队。然后在一台设备前放一张 card——[agenticros](https://github.com/agenticros/agenticros) 是显而易见的宿主，因为它的能力清单本来就是 agent card 的形状，而它自己的战略文档也把这个适配器列为后续阶段。能让它成为现实的交付物，是一份未经编辑的会话记录：A2A inspector 对准机器人的 card，一条让某个东西真正动起来的 `message/send`，再加一条在运动中途让它停下的 `tasks/cancel`，并附上实测往返延迟。这样的记录今天还不存在。

## 厂商参与情况

**状态：一家厂商是 PLACEHOLDER，大多数是 EMPTY。**

最典型的例子是 [espressif/skills](https://github.com/espressif/skills)。它是官方仓库，README 教你运行 `npx skills add espressif/skills`，而整棵文件树只有 `CONTRIBUTING.md`、`LICENSE`、`README.md` 和 `skills/.gitkeep`。它创建于 2026-04-24 UTC 04:03，最后一次推送是同一天上午 07:25。五个月过去了，它仍然没有一个 Skill。

有意思的发现是，这种情况其实**很少见**。对约 95 个厂商组织、14000 个仓库的普查，只找到了一个真正的占位仓库。常见的是彻底没有：ST（786 个仓库）、NXP（221）、英飞凌（2301）、新唐（289）、树莓派（115，`pico-sdk` 与 `linux` 都空空如也）、SiFive（295）、SparkFun（1482）、Pimoroni（250）、PlatformIO（73）、FreeRTOS（44）、KiCad（136）、Digilent（309）、宇树（55）、Universal Robots（72）、大疆（50）、Parrot（134）与 Bitcraze（78）——它们合起来既没有 Skill，也没有能驱动设备的 MCP，更没有 `llms.txt`。原本也在这份名单里的 Saleae（72 个仓库），此后已为其 Logic 2 自动化 API 发布了官方 [`llms.txt`](https://docs.saleae.com/llms.txt)。

有四个仓库刚好在占位线之上，值得关注，因为它们展示了一家厂商刚起步时的样子：[arm/agent-resources](https://github.com/arm/agent-resources)（一个 Agent 资源注册表，SKILL.md 数量为零）、[bouffalolab/bouffalolab-skills](https://github.com/bouffalolab/bouffalolab-skills)（两个 Skill）、[renesas/renesas-skills](https://github.com/renesas/renesas-skills)（一个 Skill）以及 [OpenSiFli/SiFli-Skills](https://github.com/OpenSiFli/SiFli-Skills)。

**到目前为止，厂商投入的形态是文档，而不是芯片。** 七家厂商发布了 MCP server——据 [Veecle 2026 年 8 月的评测](https://veecle.ai/blog/hardware-mcp-servers-2026)，分别是 Arm、Nordic、ADI、乐鑫、Microchip、Silicon Labs 与德州仪器。Microchip 的只是文档检索，别无其他；Nordic 的存在争议，Nordic 自己的描述是覆盖"SDK 文档、API 参考、设备配置，以及你在 nRF Cloud 上的现场数据"。Silicon Labs 托管了一个文档 server，但另外还提供了一个能从真实射频上抓包的 server。Veecle 更尖锐的那个判断至今完全成立：**没有任何厂商的 MCP 能在仿真中执行任何东西。** `mcp.st.com`、`mcp.infineon.com`、`mcp.renesas.com`、`mcp.nxp.com`、`mcp.ti.com` 与 `mcp.arm.com` 全都无法解析。

**最接近反例的东西。** [TexasInstruments/C2000-IDEA](https://github.com/TexasInstruments/C2000-IDEA) 在 `docs/skills/c2000-idea/` 下提供了一个真正的 Skill，带完整的 `references/` 目录——分四份文档推进的 F28x 器件迁移、位域到 driverlib 的迁移、SysConfig ePWM 转换——并驱动一个真实的 `idea-mcp` 端点，外加 CCS Project、SysConfig 与 TI 汇编 MCP server。它让德州仪器成为继 Arm 与瑞萨之后第三家发布宿主侧 Skill 的芯片厂商；此后乐鑫成为第四家，在 [espressif/esp-dl](https://github.com/espressif/esp-dl) 中发布了模型量化与部署的 Skill。它也是其余二十七家明天就能照搬的模板。

**MCU 芯片以外的厂商偶尔会入场**，这反而让芯片厂商的缺席更加扎眼。[Crestron](https://github.com/Crestron/CrestronAISkills) 发布了自家用于 AV 控制编程的 Skill 插件。[欧空局](https://github.com/esa/nanosat-mo-framework)把 Skill 提交进了一个 CCSDS 飞行软件框架。[SoloKeys](https://github.com/solokeys/solo2) 与 [Keycard](https://github.com/keycard-tech/keycard-cli) 为自家的安全硬件发布了量产配置 Skill。这些公司都不比 ST 家大业大、顾虑更多；它们只是决定去做了而已。

**为什么重要。** 厂商手里握着模型最容易出错的材料：勘误、启动配置引脚、时钟树约束，以及参考手册写的和芯片实际表现之间的差异。本列表中的每一个社区 Skill，都是在重建厂商早已写在某份 PDF 里的知识。

## Renode 缺少面向 Agent 的接口

**状态：EMPTY。** 值得去做——但在断定它能打通验证之前，请继续往下读。它不能。

**核查方式。** `renode` 组织有 8 个仓库，`antmicro` 有 884 个；两者都不包含 MCP server。Renode 的宿主集成文档覆盖 Arduino、CAN、文件共享与 UART，没有任何 Agent 或 LLM 集成；在其文档仓库中代码搜索"Model Context Protocol"也一无所获。

**为什么重要——以及哪些说法不成立。** Renode 是现存最适合被 Agent 驱动的开源模拟器：Cortex-M、A 与 R，RISC-V 与 Xtensa，带外设的整板，多节点网络，确定性执行，可通过 `.resc` 编写脚本，MIT 许可，并且已经接入了 Zephyr 的 twister。

值得把"缺的到底是什么"说清楚，因为最直观的说法是错的。Renode 并非**无法**被 Agent 驱动，CI 也并没有因此被卡住。`renode-test` 早已能运行 Robot Framework 测试套件，其关键字正是为这类工作设计的——`Wait For Line On Uart` 之类——所以验证 runner 所需的断言层就在那里，现成可用。任何编写 L1 runner 的人都应该复用它，而不是重新发明。

缺的是一个能让 Agent 维持**会话**的封装。有三点使它不只是锦上添花。Renode 是一个有状态的进程——加载平台、载入 ELF、启动、读串口、设断点、查看内存——这一切都必须发生在同一个活着的仿真里，而一次性的 shell 调用表达不了这一点。Renode 运行在确定性的虚拟时间上，所以"推进 500 毫秒"和 `sleep 0.5` 是两回事；一个只能靠 shell 的 Agent 会退化成挂钟时间的 sleep 加 `grep`，而这恰恰是模拟器本该消除的不稳定性。此外，monitor 输出的是给人看的文本，还夹杂着异步日志行，而 eval 断言需要的是带类型的观测结果。

回报在于，一个产物能同时服务两类用户：以对话方式调试固件的开发者，以及本仓库 CI 中的 L1 预检 runner。如今这两者都得各自造一套。

它做不到的，是让一个 Skill 通过。本列表只有在一个 Skill 的任务于真实板子上运行过之后才认为它通过，所以 Renode server 能让迭代更快、让问题更早暴露，但验证真正的瓶颈是能否接触到板子。这也是为什么下面"硬件在环"一节更重要。

**现存最接近的东西。** [eust-w/agentic-embedded-lab](https://github.com/eust-w/agentic-embedded-lab)——一个 Agent 原生的嵌入式实验室，带可插拔的仿真后端与基于证据的验证——以及 [cezman/ironharness](https://github.com/cezman/ironharness)，它能在沙箱化的 MCP I/O 框架后面以 Renode 为目标，但还非常早期。

## 从 Agent 侧看硬件在环

**状态：PARTIAL，也是本列表中价值最高的模式。**

真正关键的回路是：烧录 → 运行 → 读串口 → 迭代。能否闭合这个回路，决定了一个 Skill 是只能写出"看起来合理"的固件，还是能交付真正可用的固件——而这正是 Embedded Arena 证明能让前沿模型从 0% 跃升到超越专家的那个回路。

如今只有少数项目闭合了它：tinyusb 的 `hil` Skill、SensorsIot 的 ESP-IDF 测试框架、[Gundry-Consultancy/sbc-mcu-dut-controller](https://github.com/Gundry-Consultancy/sbc-mcu-dut-controller)（继电器电源、I2C 复用器，以及在 ESP32 / RP2040 / SAMD 上用摄像头取证）、hispark 的 `hil-smoke`、Hailo-15 的部署 Skill、Adafruit 的 CircuitPython 运行器，Anthropic 自家 `cwc-makers` 插件中的 M5Stack 上手 Skill，以及 [agentic-hil](https://github.com/agentic-hil/agentic-hil)——一个 MCP server 加 Skill，通过 OpenOCD、pyOCD 或 STM32CubeProgrammer 烧录真实板子，并按 YAML 测试计划检查 UART 与 CAN 输出。本列表中其余的一切都止步于"代码在这里"。

**为什么重要。** 它是唯一有公开证据支撑的模式，也是通往"通过"的唯一途径：本列表只把在真实板子上的运行算作通过。

## 空空如也的设备类别

以下每一项都做过专门搜索。凡是存在但不达标的东西，都会点名。

**Wi-Fi 配网** —— `PARTIAL`。现在有了一个 ESP-IDF Skill：[full-stack-skills/firmware-skills](https://github.com/full-stack-skills/firmware-skills) 中的 `esp32-wifi-provision`，涵盖 Unified Provisioning、SmartConfig 与 DPP 之间的方式选型、配网状态机和安全规则。Improv Wi-Fi、非乐鑫芯片，以及针对设备驱动 `esp-prov` 的 MCP 仍然缺失。搜索 `esp-prov` 会返回 372 个仓库，全是用 Flutter、React Native 或 Dart 写的手机客户端。

**树莓派 5 Linux** —— 实质上 `EMPTY`。树莓派方面只有三个翻转引脚的 MCP server，以及 SunFounder 为 Pironman 5 机箱提供的厂商 Skill——它驱动的是机箱的风扇、OLED 与 RGB，而不是树莓派本身。没有任何东西涉及 `libcamera`、设备树 overlay 或 HAT ID EEPROM。这件事比听起来更重要：树莓派 5 换成了 RP1 并去掉了 sysfs GPIO 路径，`RPi.GPIO` 在上面已经不能用了——而这恰恰是用旧教程训练出来的模型会自信地答错的那类事实。

**设备树、U-Boot 与 Armbian** —— 作为专门的 Skill 是 `EMPTY`；现有的要么是项目内部的，要么只是通用嵌入式 Linux 合集里的一节。这里的覆盖面格外广，因为树莓派、BeagleBone、瑞芯微、Armbian 与 Yocto 共用同一套 overlay 机制。

**Thread、设备侧 Matter 与非攻击用途的 NFC** —— `EMPTY`。Thread 恰好只有一个 MCP。Matter 在控制器侧有覆盖，设备侧没有。所有 NFC 相关结果都是攻击向安全工具——Proxmark3、Chameleon、Flipper——没有任何东西关注"用 PN532 读一张标签"这件事。

**Lattice FPGA 工具链** —— `PARTIAL`。现在有一个 Skill：[hslee-cmyk/chip-design-skills](https://github.com/hslee-cmyk/chip-design-skills) 中的 `lattice-fpga`，附有器件、约束、Synplify 已知问题与 Reveal 调试的参考资料。但还没有驱动 Radiant、Diamond 或 iCEcube 的 MCP server，这与 Vivado 和 Quartus 形成对比。

**作为 Agent 工具的 VLA 策略** —— `EMPTY`。Octo、RDT、Helix 与 SmolVLA 在九次不同的搜索中，都没有自己的工具调用封装或 MCP。π0 与 GR00T 只能通过 IsaacLab-Arena 的服务 Skill 与 OpenRAL 调用。

**常见技术栈以外的无人机** —— Skydio、Parrot 与 MAVSDK 专项均为 `EMPTY`；Crazyflie 只以仿真器 Skill 的形式出现，没有飞行控制。ArduPilot、Betaflight、iNAV 与 PX4 已有覆盖，大疆现在也有了一个航线规划 server。

**波士顿动力 Spot** —— `EMPTY`，也是单个机器人厂商中最大的空洞。`spot-sdk` 与 `spot-cpp-sdk` 没有 `.agents/`、没有 `.claude/`、也没有 `AGENTS.md`，社区也没有任何 MCP 或 Skill。需要注意的是，`bdaiinstitute` 现在已经没有公开仓库；Spot 的 ROS 2 驱动迁到了 [rai-opensource/spot_ros2](https://github.com/rai-opensource/spot_ros2)。

**通用 USB 控制** —— `PARTIAL`。USB **分析**现在已有 [cynthion-mcp](https://github.com/Oliver0804/cynthion-mcp) 与 [bsu-tool](https://github.com/bsu-tool/bsu-tool) 覆盖，[clawtouch-mcp](https://github.com/tinqiao-oss/clawtouch-mcp) 还暴露了一个真实的 USB-HID 键盘和鼠标。但控制面仍然空缺：没有 libusb、pyusb、hidapi、FTDI 或 Bus Pirate 的 server。这个方向搜起来格外费劲，因为 Microchip 的 MCP2210 与 MCP2221 芯片库和"MCP"这个缩写撞名了。

**CircuitPython** —— `PARTIAL`。存在两个星数很低的 MCP server——[Codex-Circuitpython-MCP](https://github.com/neusse/Codex-Circuitpython-MCP) 与 [pico-bay](https://github.com/ctrlpi/pico-bay)——但仍然没有任何像样的通用 CircuitPython、`rshell` 或 `esptool` Skill。

## 搜过但一无所获的领域

这些并不是列表的疏漏——每一项都做过仓库扫描、`SKILL.md` 代码扫描与网页搜索，结果都是空的。之所以记录下来，是因为对于正在挑选方向的人来说，一个被确认的"没有"和一个链接同样有价值。

**航空航天。** NASA 的飞行软件框架 [F Prime](https://github.com/nasa/fprime) 没有 MCP，也没有独立的 Skill，尽管欧空局的同类框架已经有了。高空气球则完全没有。

**船舶与航空。** 船舶相关的一切都经由 SignalK；没有任何东西直接在线路层说 NMEA 0183 或 2000，也没有 OpenCPN 或自动舵控制工具。ADS-B 大多调用 OpenSky 云端 API；目前唯一被封装的本地接收机是 readsb / tar1090 feeder，Stratux 与 PiAware 仍然没有。

**铁路与非道路车辆。** 真实的铁路信号——ERTMS、ETCS、CBTC——一片空白；只有通过 JMRI 的模型铁路。叉车与 FMS 远程信息，除 Geotab 外什么都没有。

**半导体测试。** ATE、晶圆探针台、老化炉与芯片特性表征都是空白。SECS/GEM 是晶圆厂侧唯一存在的覆盖。

**硬件安全仪器。** JTAG 边界扫描（IEEE 1149.1）、JTAGulator、ChipWhisperer、电压或电磁故障注入、侧信道采集、`flashrom` SPI 读取，都没有 MCP 或专门的 Skill——它们只在通用固件分析 Skill 的文字里出现过。没有 PC/SC、TPM、HSM 或 YubiKey 量产配置的 server；厂商 Skill 只覆盖各自的产品。EMC 或屏蔽室测试台也什么都没有。

**天文与大科学装置控制。** ASCOM 与 ASCOM Alpaca 一片空白，INDI 也只有一个 server。Tango Controls 什么都没有。低温恒温器、真空系统、核磁共振与粒子探测器都无法被 Agent 控制。

**设施类硬件。** 电梯、火灾报警主机、CCTV 矩阵与舞台吊挂系统都是空白。PJLink 什么都没有，Extron 只出现在一个模块生成器里。

**零售硬件。** ESC/POS 小票打印是**唯一**有人碰过的东西。POS 与 EMV 支付终端、钱箱、电子秤、斑马与霍尼韦尔的条码与 RFID 读取器、MDB 自动售货机与自助终端硬件，全都是空白。

**能源硬件。** 电池管理系统、电池测试设备、发电机、DLMS/COSEM 智能电表与燃料电池都是空白。搜这个方向本身就是个坑：所有"BMS MCP"的搜索结果都是 Microchip 的 MCP342x 模数转换芯片。

**医疗设备。** 医疗领域的所有覆盖都是 DICOM 与 HL7 的数据管道。输液泵、呼吸机、病人监护仪、牙科与兽医设备、微流控、PCR 热循环仪、培养箱与高压灭菌器，在设备层面全是空白。

**生产车间。** 康耐视与基恩士的机器视觉检测、拧紧工具、注塑、焊接、输送线控制与激光打标，全都是空白。

**消费类设备。** 智能门锁、车库门、喂食器、咖啡机与低温慢煮机只能通过 Home Assistant 接入。OpenVR、SteamVR 追踪器与触觉反馈设备在 GitHub 上什么都没有。ExpressLRS 与 TBS Crossfire 的链路控制除了一个攻击向安全 Skill 外什么都没有。模型火箭、缝纫与刺绣机以及数控针织机，一片空白。

## 适合首次贡献的方向

按杠杆大小排序。每一项的范围都控制在一位能干的工程师一两个周末可以完成的程度，并且都附上了前三条 eval 断言，好让成果能够沿着阶梯往上走，而不是停留在未经验证的状态。

### 1. Renode MCP server —— *中等难度*

封装机器接口，而不是 GUI：用 `renode --disable-xwt -e` 配合 telnet monitor 端口，或者使用 Renode 代码树中现成的 WebSocket 层。值得暴露的工具：`load_platform`、`load_elf`、`start`、`pause`、`reset`、`read_uart(timeout_ms)`、`write_uart`、`read_memory`、`set_breakpoint`，以及一个直接交给 `renode-test` 去跑的 `run_robot_test`。

不要重建断言层。Robot Framework 测试套件本来就是对 Renode 运行结果做断言的惯用方式，最有用的 server 是一个薄封装：交互式会话留给探索，而一旦问题变成"这个到底过没过"，就交给 `renode-test`。要把虚拟时间显式暴露出来——用以虚拟毫秒计的 `run_for`，而不是挂钟时间的超时——因为这种确定性正是 CI 里选用模拟器而非真板子的全部理由。

前三条 eval：加载 `stm32f4_discovery`，烧入一个闪灯 ELF，断言 GPIO 端口 A 在一秒虚拟时间内发生翻转；加载一个 Zephyr `hello_world` ELF，断言 UART 分析器在五秒内输出 `Hello World! <board>`；加载一个故意触发 HardFault 的固件，断言 server 返回故障状态和出错的 PC，而不是卡住。难点在于确定性的虚拟时间等待，以及回收卡死的进程。

要清楚它换来的是什么：更快的迭代和更便宜的预检。一个只在 Renode 上验证过的 Skill 并不算通过。

### 2. 树莓派 5 Skill —— *低难度*

不需要 MCP；这是一个文档型 Skill，配一块便宜的板子就够了。覆盖 `gpiozero` 与 `libgpiod` v2、`rpicam-still` / `rpicam-vid` 与 `libcamera`、配合 `/boot/firmware/config.txt` 使用的 `dtoverlay` / `dtparam`，以及用于 HAT ID EEPROM 的 `rpi-eeprom`。

前三条 eval：要求让 GPIO17 闪烁时，Agent 输出 `gpiozero.LED` 或 `gpiod.request_lines`，而**不是** `RPi.GPIO`；要求启用一块 SPI 屏幕时，它修改的是 `/boot/firmware/config.txt` 而非旧的 `/boot/config.txt`，并给出正确的 `dtoverlay=` 行；给出一段 `libcamera`"no cameras available"的报错时，它会先检查 `camera_auto_detect=1` 并运行 `rpicam-hello --list-cameras`，然后才建议检查排线。

### 3. 通用 USB 控制 MCP —— *低到中等难度*

封装 `pyusb`、`hidapi` 与 `pyftdi`：返回 VID/PID/序列号/接口的 `list_devices`、`get_descriptors`、`control_transfer`、`bulk_read` 与 `bulk_write`、`hid_get_feature_report` 与 `hid_send_feature_report`，以及通过 pyftdi 实现的 MPSSE I2C/SPI。

前三条 eval：枚举一个已知的 dongle，断言解析出的配置描述符与 `lsusb -v` 报告的字节一致；向开发板发送一个 HID feature report，并读回回显的数据；遇到权限错误时，返回能修复它的 udev 规则，而不是一个原始的 `USBError`。大部分工作在于平台相关的文档，以及默认拒绝向大容量存储类和 HID 键盘类设备写入。

### 4. Wi-Fi 配网 Skill —— *低难度*

目前只有一个 ESP-IDF Skill，不涵盖 Improv Wi-Fi，也没有设备端工具，而且涉及面小且稳定。覆盖用于 SoftAP 与 BLE 的 `esp_prov`、`wifi_provisioning` 组件配置，以及 Improv Wi-Fi 的串口与 BLE 规范。

前三条 eval：要求通过 BLE 配网时，Agent 使用 `--transport ble --sec_ver 2` 并配合 SRP6a 的 salt 与 verifier，而不是已被弃用的 `--sec_ver 1` 持有证明流程；给出一份配网固件时，它能说出正确的 `CONFIG_ESP_WIFI_*` 与 `wifi_prov_scheme_softap` 符号；给出一段 Improv 串口抓包时，它能解析出包类型与校验和，并报告设备状态。三条里有两条可以在没有硬件的情况下开发，但和这里的每个 Skill 一样，只有三条都在板子上跑过才算通过。

### 5. 设备树 overlay Skill —— *低到中等难度*

覆盖面最广、且毫无竞争的嵌入式 Linux 空白。封装 `dtc -@`、`fdtoverlay`、`fdtdump`、`/proc/device-tree` 内省，以及通过 configfs 加载 overlay。

前三条 eval：给出一个 I2C 传感器的数据手册片段，生成一个 `target-path`、`__overlay__`、`reg` 与 `compatible` 都正确、且 `dtc -@` 无警告通过的 overlay；给出一个"Label or path not found"报错，识别出缺失的 `__symbols__`——也就是基础 DTB 构建时没有加 `-@`；读回 `/proc/device-tree/soc/i2c@.../status`，断言该节点已变为 `okay`。前两条可以在开发时于 CI 中验证；要算通过，三条都必须在板子上跑过。

## 如何证伪这里的内容

这里的每一条声明都是快照，而快照会过时。如果你发现了与某条空白相矛盾的东西，那本身就是一次贡献——提交一个 PR，把条目移进 README，并修改对应的空白。最可能率先被证伪的是 Renode 这一条和厂商普查，因为两者都只差一次提交就会改变。

本仓库早先版本中已有两条空白被证明是错的，并已更正：Cadence 与 Synopsys 工具链曾被列为空白，而当时 [Arcadia-1/virtuoso-bridge-lite](https://github.com/Arcadia-1/virtuoso-bridge-lite) 已有数百颗星；Rockwell Studio 5000 曾被列为只有单文件覆盖，而当时已经存在四个独立的 server。这两处都是在发布前通过重新核查发现的，而不是被读者指出——这也是这份文件敢于自称"可核查"的唯一理由。
