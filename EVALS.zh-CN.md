# 硬件 Skill 的评测方法

*[English](EVALS.md) · 简体中文*

> 本文档译自 [EVALS.md](EVALS.md)。如两者有出入，以英文版为准。

这份文档讲的是 [README](README.zh-CN.md) 中那些徽章背后的方法：一个硬件 Skill 如何证明自己能用、一个 eval 包里包含什么、每一级验证具体检查什么——以及同样重要的：哪些部分今天已经存在，哪些还在建设中。

至于为什么要费这个劲，[GAPS.zh-CN.md](GAPS.zh-CN.md) 里有完整论证。简短版本是：前沿模型在没有硬件反馈时，在真实单片机上的部署成功率为 0%；专家编写的 Skill 能把成功率推到接近 100%；而光靠阅读，没人分得清一个好的硬件 Skill 和一个看起来像样的硬件 Skill。评测就是用来分清这一点的。

## 今天已经有什么

请先读这张表。其余每一节描述的都是完整设计，很容易把计划中的部分误当成已经能用的部分。

| 组成部分 | 状态 | 位置 |
|---|---|---|
| Eval 包格式 | 已定义 | `template/evals/` 与本文档 |
| `L0` 静态检查 | **可用**，已接入 CI | `scripts/l0_check.py skill <path>` |
| `L1` 模拟器预检 runner | 尚未构建——且永远不算通过 | 设计见下文 |
| `L2` 真机实测背书 | **可用**，人工流程——**唯一算作通过的一级** | Issue 模板 `.github/ISSUE_TEMPLATE/attestation.yml`；由维护者记录被接受的背书 |
| `ΔPass` A/B runner | 尚未构建 | 设计见下文 |
| `stale` 标记 | 尚未构建 | 由维护者根据背书日期标记 |

第一个以此格式提供 eval 包的第三方 Skill 是 [fxp/m5stack-embedded-dev-skill](https://github.com/fxp/m5stack-embedded-dev-skill)，文末会以它作为实例。

## 原则

**只有真实的板子能让一个 Skill 通过。** 静态检查和模拟器能低成本地尽早发现问题，两者都值得有，但都不算通过。模拟器只建模那些容易建模的部分；而硬件中真正要命的故障，恰恰藏在它们跳过的地方——电源管理芯片、射频、闪存时序、USB 供电不足时的掉电复位。只有当有人在真实芯片上跑完了任务、且每一条断言都成立时，一个 Skill 才算通过。本仓库中任何其他情况都不叫"通过"。

**对物理现象断言，而不是对文字断言。** 一个任务通过，是因为脚本观测到了现实世界中的副作用：UART 上的一行输出、GPIO 上的一次跳变、总线上的一个数据包、ROS topic 上的一条消息、HTTP 端点的一次响应。绝不是因为某个模型或某个人判断"代码看起来对"。硬件在这方面格外合适，因为固件做的几乎每件事都能从芯片外部观测到。

**prompt 就是任务的全部。** Agent 只能看到 prompt，别的什么都看不到。如果一位称职的工程师需要额外提示才能完成，那么这条提示就应该写进 prompt，否则就是任务描述不充分。

**每一条断言都必须有可能失败。** 在被检查的对象根本不存在时仍然通过的断言，比没有断言更糟，因为它制造了不该有的信心。这是真实 eval 包中最常见的缺陷，下文专门有一节讲它。

**说清楚哪些级别你还没达到。** 一个声明 `simulator: none` 并解释原因的包，比一个声称用了某个模拟器但实际上从未跑过的包更有用。坦诚的空缺没问题；名不副实的徽章不行。

**衡量的是 Skill，而不是模型。** 一个所有模型不装 Skill 就能通过的任务，对这个 Skill 说明不了任何问题。`ΔPass` 就是为了抓出这种情况。

## Eval 包

eval 包是 Skill 内部一个名为 `evals/` 的目录，与 `SKILL.md` 并列：

```
my-skill/
├── SKILL.md
├── references/
└── evals/
    ├── manifest.yaml
    ├── tasks/
    │   ├── 01-easy-thing.yaml
    │   ├── 02-medium-thing.yaml
    │   └── 03-hard-thing.yaml
    └── fixtures/            # 可选
```

从复制 [`template/evals/`](template/evals/) 开始。

### manifest.yaml

| 字段 | 必填 | 含义 |
|---|---|---|
| `skill` | 是 | 必须与该 Skill 的 SKILL.md frontmatter 中的 `name` 相同。 |
| `version` | 否 | eval 包的版本，而不是 Skill 的版本。 |
| `target.board` | 是 | 精确的板型标识——`esp32-c3-devkitm-1`，或 `esp32:esp32:m5stack_core2` 这样的 arduino-cli FQBN——绝不能是"ESP32"这种系列名。 |
| `target.framework` | 是 | `esp-idf`、`arduino`、`zephyr`、`ros2` 等。 |
| `target.framework_version` | 是 | 编写与测试这些任务时所用的版本。硬件 SDK 的小版本之间就可能不兼容，这个字段是结果可复现的前提。 |
| `target.toolchain` | 否 | 预期 Agent 调用的工具：`idf.py`、`arduino-cli`、`west`。 |
| `simulator` | 是 | L1 预检将在哪里运行；与这个 Skill 能否通过无关。取值为 `wokwi`、`renode`、`qemu`、`native_sim`、`gazebo`、`isaac`、`mujoco`、`webots`、`ha-demo`、`modbus-sim`、`opcua-sim` 或 `none` 之一。 |
| `assertions_supported` | 是 | 本包中任一任务用到的所有断言类型。 |
| `verified.L0` | 否 | `l0_check.py` 通过后填写 `{date, run}`。 |
| `verified.L1` | 保留 | 由 L1 runner 写入。保持 `null`。 |
| `verified.L2` | 否 | 被接受的背书列表，由维护者添加。 |
| `ab.*` | 保留 | 由 A/B runner 写入。保持 `null`。 |

当没有任何公开模拟器能建模任务所依赖的硬件时，请使用 `simulator: none`，并在注释中说明原因。M5Stack 的包是个好榜样：Core2 的电源管理芯片没有被任何公开的 Wokwi 或 Renode 板型建模，所以它声明了 `none`，而不是声称一个会悄悄跳过关键部分的模拟器。声明 `none` 没有任何代价：所有 Skill 都以同样的方式通过——在板子上。

### 任务文件

`tasks/` 中每个任务一个 YAML 文件。文件名去掉 `.yaml` 后必须等于任务的 `id`。

| 字段 | 必填 | 含义 |
|---|---|---|
| `id` | 是 | 等于文件名主干。加上数字前缀，让任务按难度排序。 |
| `level` | 是 | `easy`、`medium` 或 `hard`。 |
| `timeout_s` | 否 | Agent 整次尝试的挂钟时间预算。 |
| `prompt` | 是 | 告诉 Agent 的全部内容。不能为空。 |
| `build.cmd` | 否 | Agent 宣布完成后 runner 执行的命令，例如 `idf.py build`。 |
| `build.cwd` | 否 | 相对于 Agent 的工作目录。 |
| `assertions` | 是 | 断言列表。**全部**通过，任务才算通过。 |
| `fixtures` | 否 | 已知正确的参考输出，例如预期的串口日志。 |

目标是三个任务——简单、中等、困难各一个。一个任务说明不了 Skill 能否泛化；十个任务在每次 A/B 对照都要跑两遍，成本太高。

## 断言类型

每条断言都有一个 `type`。任何断言都可以设置 `l1_skippable: true`，表示它需要模拟器提供不了的真实硬件——BLE 嗅探器、实体按键、读取真实环境的传感器。L1 预检会跳过它；但在真实板子上它仍然必须成立，任何一条断言没被检查的任务都不算通过。

合法类型的集合枚举在 `scripts/l0_check.py` 中。其中五种已经由真实的 eval 包确立了字段格式。另外三种是保留的：类型名会被接受，但字段尚未定义，由第一个需要它的包通过向本文档提交 PR 来定义。

| 类型 | 观测对象 | 字段 |
|---|---|---|
| `compile_only` | `build.cmd` 以 0 退出 | 无 |
| `serial_match` | UART 输出 | `baud`、`pattern`（正则表达式，逐行匹配）、`min_matches`、`within_s` |
| `gpio_state` | 引脚电平随时间的变化 | `pin`、`expect`（如 `toggles`）、`min_edges`、`within_s` |
| `bus_capture` | 总线上的通信 | `bus`（如 `ble`）、`expect`（与总线相关的映射，如 `adv_name`、`service_uuid`、`char_uuid`、`notify_count_min`、`within_s`） |
| `exit_code` | 任意脚本的结果 | `cmd`（shell 命令）、`expect`（退出码） |
| `network_probe` | 设备的网络端点 | 保留 |
| `ros_topic` | ROS topic 上的消息 | 保留 |
| `file_exists` | 磁盘上的产物 | 保留 |

单独一个 `compile_only` 对硬件几乎证明不了什么，所以 L0 要求每个包至少包含一条比它更强的断言。

`exit_code` 是一个逃生口，用于检查生成代码中那些任何运行时观测都抓不到的静态性质。M5Stack 的包用它来检查 Agent **没有**再次调用 `Wire.begin()`：在那块板子上，即使违反了这条规则，I2C 扫描照样能成功，所以只有检查源码才能发现这个错误。请谨慎使用——只要有可能，运行时断言几乎总是更强。

## 空转断言

当一条断言因为它要检查的东西根本不存在而通过时，它就是空转的。这是最值得排查的缺陷，因为在一次全绿的运行中你完全看不出来。

这种模式最常出现在搜索源码的 `exit_code` 检查中。设想一条检查：它通过匹配 `void IRAM_ATTR <name>(...)` 找到中断处理函数，如果函数体里有 `Serial.` 或 `delay(` 就判失败。如果 Agent 写的处理函数没有 `IRAM_ATTR`，模式什么也匹配不到——而一个按"找到了且有问题才失败"来写的脚本会以 0 退出。即使这个处理函数确实调用了 `Serial.println` 和 `delay` 也一样，而这恰恰是这条检查存在的意义所要抓的违规：Agent 犯了这个错，只是少写了一个属性，断言就变绿了。修复方法是，在找不到要检查的对象时判为失败：

```python
m = re.search(r'void\s+IRAM_ATTR\s+\w+\s*\([^)]*\)\s*\{(.*?)\n\}', src, re.S)
if not m:
    sys.exit(1)                     # 没找到中断函数：任务没完成，不能判通过
sys.exit(1 if re.search(r'Serial\.|delay\(', m.group(1)) else 0)
```

用三个小草图来跑——一个没有 `IRAM_ATTR` 的阻塞式处理函数、一个调用了 `Serial` 的 `IRAM_ATTR` 处理函数、一个只置标志位的正确处理函数——原来的检查分别以 0、1、0 退出：它放过了第一个错误的草图。加上防护后则分别以 1、1、0 退出。

有两个快速测试，能在提交之前抓出几乎所有空转断言。先对一个空工程跑每条断言，此时每一条都应该失败。再对一个故意写错的方案跑，此时针对这个错误的那条断言应该失败，其余不应失败。由于同一任务内的断言是"与"的关系，空转的断言有时会被相邻的断言兜住——比如缺少 `.ino` 文件同样会让 `compile_only` 失败——但不要依赖这一点：每条断言都应该能独立成立。

## 第 0 级——静态检查

**可用。** 提交 PR 前请在本地运行：

```
python scripts/l0_check.py skill path/to/my-skill
```

它检查以下内容，并且只检查这些：

- `SKILL.md` 存在，且带有 `name` 与 `description` 均非空的 YAML frontmatter。
- `description` 至少 80 个字符——更短的描述很少能稳定触发。
- `SKILL.md` 中没有形似 API 密钥或访问令牌的内容。
- `evals/manifest.yaml` 存在，其 `skill` 等于 frontmatter 中的 `name`，`simulator` 是已知 id，`assertions_supported` 中每一项都是已知类型，并且 `target.board`、`target.framework` 与 `target.framework_version` 均已设置。
- `evals/tasks/` 中至少有一个任务；每个任务的 `id` 等于文件名主干，`level` 合法，`prompt` 非空。
- 每条断言的 `type` 都是已知类型，且已在 `assertions_supported` 中声明。
- 整个包中至少有一条断言强于 `compile_only`。

它**不**检查断言内部的字段、`build` 块、正则是否合法，也不检查一条断言是否有可能失败。L0 表示这个包结构正确，而不表示它是好的。

## 第 1 级——模拟器预检

**尚未构建。** 本节是 runner 将要遵循的设计。

L1 是预检，不是通过。它的作用是在有人烧录板子之前，低成本地拦下问题——一个连在 Wokwi 里都过不了的任务，不值得背书者花一个下午。处于 L1 的包仍然不算通过。

对每个任务，runner 在装有该 Skill 的干净工作目录中把 prompt 交给 Agent，等待 Agent 完成或达到 `timeout_s`，运行 `build.cmd`，把产物加载进声明的模拟器，然后评估所有未标记 `l1_skippable` 的断言。当所有任务的这些断言都在某个指定模型上通过时，这个包就达到 L1，记录为 `{date, simulator, tasks_passed, model}`。

有三个决定已经确定：

- **复用模拟器自带的断言层。** Renode 自带 `renode-test`，其 Robot Framework 关键字中有 `Wait For Line On Uart` 这类关键字；Wokwi 的场景文件原生支持对串口文本做断言。runner 应当把 `serial_match` 翻译成这些机制，而不是在抓取来的控制台输出上重新实现一遍匹配。
- **在模拟器里计时，而不是用挂钟计时。** `within_s` 指的是仿真时间的秒数。模拟器的确定性虚拟时间，正是 CI 里选它而不选真板子的全部理由；一个靠 sleep 加 grep 的 runner 会把这点丢掉，变得不稳定。
- **记录哪些断言被跳过了。** L1 徽章必须显示有多少断言被计入，这样一个关键检查全都标了 `l1_skippable` 的包，就不会看起来和一个检查全部实际运行过的包一样强。

哪个模拟器能支持哪些断言，汇总在 README 的验证基础设施一节。Renode 缺少面向 Agent 的会话接口，这是 [GAPS.zh-CN.md](GAPS.zh-CN.md) 中排在第一位的问题。

## 第 2 级——真实硬件（通过）

**可用，人工流程。** 这是唯一算作通过的一级。任何拥有目标板子的人都可以提交背书。

1. 安装该 Skill，严格按照 `evals/tasks/` 中写的内容运行每个任务，只给 Agent prompt，别的什么都不给，并且在真实板子上运行。模拟器不算，Wokwi、Chiplab 这类托管虚拟板也不算。远程烧录真实板子的设备农场——比如驱动物理目标的 Jumpstarter 或 labgrid——算。
2. 评估每一条断言，包括标记了 `l1_skippable` 的。全部成立，任务才算通过。
3. 把完整、未经编辑的 Agent 会话记录保存到公开位置，并附上硬件证据：烧录工具识别到芯片并写入镜像的输出——esptool 的 `Chip is …` 那一行、`arduino-cli upload` 的端口、probe-rs 的目标——以及从板子上读回的串口日志。
4. 用 **L2 hardware attestation** 模板开一个 issue。模板会要求填写：Skill、精确的板型与版本、框架版本、Agent 模型与运行环境、每个任务一行 `pass` 或 `fail`、硬件证据与会话记录链接，并要求确认是在真实板子上运行的、没有给过额外提示、会话记录未经编辑。

缺少会话记录或硬件证据的背书不会被接受。背书被接受后，由维护者将其追加到该包的 `verified.L2` 中。只要有一份被接受的背书显示所有任务都通过，这个包就算通过。README 会为 N 份独立背书显示 `L2 ×N`——"独立"指不同的人、不同的板子——用来衡量这个结果的可复现程度。

## ΔPass——这个 Skill 是否真的携带了知识？

**尚未构建。** 本节是 A/B runner 将要遵循的设计。

每个任务在同一模型、同一运行环境、同一块真实板子上跑两次：一次装上 Skill；另一次移除 Skill，并把它的 `description` 替换为一句泛泛的占位描述，这样两组之间唯一的差别就是 Skill 所携带的知识。在模拟器上测得的比率不算数，理由与模拟器上的通过不算数相同。runner 为每一组记录两个比率——任务通过率，以及首次编译成功率，即第一次构建无需 Agent 修复任何东西就成功的尝试所占的比例。

`ΔPass` 是装了 Skill 的通过率减去不装 Skill 的通过率。如果一个 Skill 在两个比率上都没能带来至少 15 个百分点的提升，就会被标记为 `low-gain`。这不是拒绝，而是一个问题：它很可能只是在复述模型已经知道的东西，维护者会追问它到底打算承载哪条非显而易见的事实。

之所以单独跟踪首次编译成功率，是因为这正是硬件 Skill 体现价值的地方。寄存器名写错、漏了某个 `sdkconfig` 符号、FQBN 用错——模型通常在两三次构建失败后就能自己改过来，所以只看通过率，可能会埋没一个实实在在省下了迭代次数的 Skill。

## 实例

[fxp/m5stack-embedded-dev-skill](https://github.com/fxp/m5stack-embedded-dev-skill) 面向使用 Arduino 与 M5Unified 的 M5Stack Core2。它的 eval 包用三个任务展示了这套方法的大部分内容：

- **`01-hello-serial-tick`**（简单）——每秒打印一次 `tick`。`compile_only` 加一条 `serial_match`，要求六秒内有四行匹配 `^tick$`。最简单的诚实任务。
- **`02-i2c-scan-no-redundant-wire-begin`**（中等）——扫描内部 I2C 总线，但不能再次调用 `Wire.begin()`。一条针对地址 `0x34` 上电源管理芯片的 `serial_match`，加一条 `exit_code` 源码检查。它承载了这个 Skill 真正要教的东西，也是一个适合用 `exit_code` 的好例子：在这个板子版本上，即使违反了规则，扫描照样成功，所以任何运行时观测都抓不到这个错误。
- **`03-isr-safe-button-notify`**（困难）——在不使用阻塞调用的前提下，从 GPIO 中断通知主循环。`serial_match` 需要真实地按下按键，所以正确地标记了 `l1_skippable`。其 `exit_code` 检查正是"空转断言"一节中的那个例子：按目前发布的写法，只要处理函数没有 `IRAM_ATTR`，一个带阻塞调用的处理函数也能通过。这件事比看上去更重要，因为在 L1 预检中串口断言会被跳过，这时它就是唯一在检查处理函数的断言。加上 `if not m: sys.exit(1)` 这道防护即可修复。

它的 manifest 声明了 `simulator: none`，并解释了没有公开模拟器能建模 Core2 的 PMIC。这对它没有任何代价：它通往"通过"的路径和其他所有包一样——由拥有 Core2 的人在板子上跑完这三个任务。在此之前，它处于 L0，尚未通过。

## 扩展这套方法

要新增一个模拟器 id 或一种断言类型，请提交一个 PR，并做到以下几点：

1. 把它加进 `scripts/l0_check.py` 中的 `SIMULATORS` 或 `ASSERTION_TYPES`。
2. 如果是断言类型，在上面的断言表中加一行定义它的字段，并说明是什么让它有可能失败。
3. 如果是模拟器，把它加进 README 的验证基础设施一节，说明 runner 如何以无头方式驱动它，以及它能支持哪些断言类型。
4. 同步更新 `EVALS.zh-CN.md` 中的译文，或者让 `translation-sync` job 保持失败，由维护者修复。
