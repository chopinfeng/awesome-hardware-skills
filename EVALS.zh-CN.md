# 硬件 Skill 评测：测试方案

*[English](EVALS.md) · 简体中文*

> 本文档译自 [EVALS.md](EVALS.md)。如两者有出入，以英文版为准。

这份文档是 [README](README.zh-CN.md) 中那些徽章背后的测试方案。它讲清楚：一个硬件 Skill 在什么上测、由谁测、测几次、每条断言在真实板子上怎么测量、记录什么，以及结果什么时候算数。为什么值得投入，见 [GAPS.zh-CN.md](GAPS.zh-CN.md)。

其余一切都服务于这一条规则：**只有当一个 Skill 的任务在真实板子上运行、且断言成立时，它才算通过。** 静态检查和模拟器只是预检。本仓库中任何其他情况都不叫"通过"。

## 今天已经有什么

请先读这里——文档其余部分描述的是完整方案，很容易把计划中的部分误当成已经可用的部分。

| 组成部分 | 状态 |
|---|---|
| Eval 包格式 | 本文档中定义；起步模板在 `template/evals/` |
| `L0` 静态检查 | **可用**，已接入 CI——`python scripts/l0_check.py skill <path>` |
| `L1` 模拟器预检 runner | 尚未构建，且永远不算通过 |
| 真实硬件上的阶段 0–3 | **可用，人工执行**——下面每一步今天都能用一块板子和所列工具完成 |
| `L2` 背书表单 | **可用**——`.github/ISSUE_TEMPLATE/attestation.yml`（2026-09-16 之前是非法 YAML；CI 现在会检查它） |
| `ΔPass` 自动 A/B runner | 尚未构建；由阶段 3 的人工流程代替 |
| `stale` 标记 | 尚未构建；由维护者根据背书日期标记 |

截至 2026-09-16，列表中有一个 Skill 提供了 eval 包，**还没有任何 Skill 通过。**

## 测试回答什么问题

两个问题，分开回答：

1. **这个 Skill 能不能用？** 装上 Skill 后，Agent 能否在真实板子上完成每个任务？由阶段 2 回答。回答"能"，即获得 `L2` 徽章。
2. **这个 Skill 是否携带了知识？** 装与不装相比，结果是否不同？由阶段 3 回答。差值即 `ΔPass`。

一个 Skill 可能通过了问题 1，却在问题 2 上毫无增益——模型可能本来就会。两个结果都会公开。

在回答这两个问题之前，必须先回答第三个：**eval 本身可信吗？** 一条什么都没做也能通过的断言，对这个 Skill 说明不了任何问题。这就是阶段 0，它排在最前面。

## 方案概览

| 阶段 | 由谁 | 何时 | 目的 | 产出 |
|---|---|---|---|---|
| 0——验证 eval | 包作者 | 每个 eval 版本一次 | 证明任务可完成、断言会失败 | manifest 中的 `eval_validated` |
| 1——测试台自检 | 测试者 | 每次测试会话的开始与结束 | 证明测试台正常，这样失败才能归咎于 Skill | 自检记录 |
| 2——通过判定运行 | 测试者 | 每份背书 | 判定 Skill 是否通过 | 运行记录、`L2` 背书 |
| 3——A/B 对照 | 测试者 | 可选，随背书一起 | 衡量 Skill 带来了什么 | 附样本量的 `ΔPass` |

## 测试台

以下所有内容都要写进每一条运行记录。在不同测试台上跑出的两次运行不可比较。

**目标板。** 必须是 `target.board` 中指定的那块板，包括版本，例如 `esp32-c3-devkitm-1 rev 1.1`。不能用同系列的兄弟型号代替。

**主机。** 操作系统及版本，以及版本恰好等于 `target.framework_version` 的工具链。请用带电源的 USB Hub 或台式电源给板子供电——USB 口供电不足会导致掉电复位，看起来就像固件 bug。

**观测仪器**，根据包中用到的断言类型按需准备：

| 断言类型 | 仪器 | 说明 |
|---|---|---|
| `compile_only`、`exit_code` | 无 | 在主机上运行 |
| `serial_match` | 板载 USB 转串口，或独立的 USB 转串口模块 | 抓取时带主机时间戳 |
| `gpio_state` | 逻辑分析仪（兼容 sigrok 的即可） | 与板子共地 |
| `bus_capture`（BLE） | BLE 嗅探器——例如装了 nRF Sniffer 的 nRF52840 dongle，或兼容 Sniffle 的板子 | 必须跟随连接才能看到 notify |
| `bus_capture`（CAN、I2C、SPI） | CAN 适配器，或带协议解码的逻辑分析仪 | |

**Agent。** 模型 ID、运行环境（harness）及其版本，以及运行环境的工具权限。Agent 运行在连着板子的主机上，在尝试过程中可以自己构建、烧录和读串口——这个闭环正是 Skill 的实际使用方式，也是"通过"所声称的内容。记录 Agent 是否能联网。

**被测 Skill。** Skill 所在的仓库与提交 SHA，以及 eval 包的 `version`。结果属于那一次提交，而不是泛指这个 Skill。

## 阶段 0——验证 eval

**由谁：** 包作者，在请任何人背书之前。**何时：** 每个 eval 包版本一次；任何任务或断言变更后都要重做。

一个 eval 的价值，取决于它能否分辨正确方案与错误方案。对每个任务，作者准备两份方案，并在真实板子上做三项检查：

```
evals/fixtures/<task-id>/reference/   一份已知正确的方案
evals/fixtures/<task-id>/broken/      一份恰好包含该任务要抓的那个错误的方案
```

1. **参考方案通过。** 构建、烧录并观测参考方案。每一条断言都通过，包括标记了 `l1_skippable` 的。这证明该任务在这块板子上可以完成，且没有哪条断言过严。
2. **空工程失败。** 在一个空的工作目录上运行每条断言。每一条都失败。这能抓出"什么都没构建也能通过"的检查。
3. **错误方案被抓住。** 构建、烧录并观测错误方案。针对这个错误的断言失败；其余断言的表现与该错误所预期的一致。这能抓出"构建了错误的东西也能通过"的检查。

检查 2 和检查 3 抓的是不同的缺陷，一个包两者都需要。列表中第一个第三方包就说明了原因。它的一个任务禁止再次调用 `Wire.begin()`，用 `! grep -q "Wire.begin(" *.ino` 来检查。在空目录上，这条检查以 0 退出：`grep` 找不到 `*.ino`，而 `!` 把它的报错变成了通过。检查 2 能抓住它；检查 3 抓不住，因为错误方案里确实有 `.ino` 文件。另一个任务禁止在中断处理函数里使用阻塞调用，并通过匹配 `IRAM_ATTR` 来定位处理函数。在空目录上它正确地失败了——但面对一个没写 `IRAM_ATTR`、却调用了 `Serial.println` 和 `delay` 的处理函数，它以 0 退出。检查 2 抓不住它；只有检查 3 能抓住。

### 编写有可能失败的断言

当一条断言因为它要检查的东西根本不存在而通过时，它就是**空转**的。在一次全绿的运行里完全看不出来，这正是阶段 0 存在的原因。修复方法永远一样：找不到要检查的对象时，判为失败。

```python
# 空转：不存在 IRAM_ATTR 处理函数时也会通过
m = re.search(r'void\s+IRAM_ATTR\s+\w+\s*\([^)]*\)\s*\{(.*?)\n\}', src, re.S)
sys.exit(1 if m and re.search(r'Serial\.|delay\(', m.group(1)) else 0)

# 可靠：不存在即失败
if not m:
    sys.exit(1)
sys.exit(1 if re.search(r'Serial\.|delay\(', m.group(1)) else 0)
```

```sh
# 空转：在空目录里也会通过
! grep -q "Wire.begin(" *.ino

# 可靠：先要求文件存在，再检查其中不该出现的内容
ls *.ino >/dev/null 2>&1 && ! grep -q "Wire.begin(" *.ino
```

### 记录阶段 0

把结果记录在 manifest 中。只有当前版本已经验证过的包，才会接受背书。

```yaml
eval_validated:
  date: 2026-09-20
  board: esp32-c3-devkitm-1 rev 1.1
  framework_version: "5.2.2"
  reference_passed: true      # 检查 1，每个任务
  empty_failed: true          # 检查 2，每条断言
  broken_caught: true         # 检查 3，每个带 broken/ 方案的任务
  evidence: https://...       # 三项检查的日志与抓包
```

## 阶段 1——测试台自检

**由谁：** 测试者。**何时：** 每次测试会话的开始与结束。

烧录每个任务的 `reference/` 方案并评估其断言，做法与阶段 2 的一次运行完全相同，只是没有 Agent。每一条断言都必须通过。这证明串口抓取、逻辑分析仪、嗅探器、供电和工具链都正常。

只有**两次**自检都通过，这次会话的结果才算数。如果结束时的自检失败，本次会话中的每一次运行都**作废**——测试台可能在任何时刻出了问题——需要在新会话中重跑。这就是用证据、而不是凭主观判断，把"测试台坏了"和"Skill 失败了"区分开的方法。

## 阶段 2——通过判定运行

**由谁：** 测试者。**何时：** 每份背书。

### 单次运行流程

1. **记录运行元数据**（见上文"测试台"一节所列），并给本次运行分配下一个连续编号。
2. **把板子复位到已知状态。** 用工具链的擦除命令擦除闪存，然后断电重启。
3. **准备干净的工作目录**，只装好 Skill，不留任何上一次运行的东西。
4. **启动 Agent 并开始录制会话。** 把任务的 `prompt` 原文交给 Agent，别的什么都不给——不给端口名、不给提示、不纠正——除非 prompt 本身包含这些内容。
5. **让 Agent 工作**，直到它宣布完成，或挂钟时间达到 `timeout_s`。超时是一次失败的运行，而不是作废的运行。
6. **冻结结果。** 打包归档工作目录并记录其 SHA-256。此后所有步骤都使用冻结的副本；Agent 在尝试过程中自己做的构建和烧录不算证据。
7. **构建。** 在冻结副本中运行 `build.cmd` 并保留日志。如果失败，`compile_only` 判失败，其余断言都记为 `not-run`。
8. **烧录。** 先擦除，再用任务定义的 `flash.cmd`（若未定义则用工具链的标准烧录命令）写入构建产物。保留烧录工具的完整输出，包括它报告所识别芯片的那一行。
9. **观测。** 在释放复位之前启动所有抓取。**时间零点**是复位被释放、新固件开始运行的时刻；每个 `within_s` 窗口都从这里开始计算。按任务定义的时间执行其 `human_action`，并记录时间戳。
10. **评估每条断言**，方法见下一节，并保留每条断言的原始证据文件。
11. **记录结果。** 每条断言为 `pass`、`fail` 或 `not-run`。只有每条断言都通过，这次运行才通过。

### 任务与包如何算通过

- **运行：** 每条断言都通过（包括标记了 `l1_skippable` 的）即通过。
- **任务：** 运行**三**次，每次都从第 2 步开始。三次中**至少两次**通过，任务即通过。Agent 的行为不是确定性的，单次运行可能侥幸通过，也可能运气不好而失败；三次里过两次，是"不止抽一次签"的最小样本。
- **包：** 每个任务都通过，包即通过。这就是 `L2` 徽章。`L2 ×N` 统计的是各自达到通过的独立背书数量——不同的人、不同的板子。

每一次运行都要按顺序报告：通过的、失败的、作废的一视同仁。不允许在多于三次的运行里挑出最好的三次；作废的运行要重跑，两者都要出现在记录中。

### 失败的运行，还是作废的运行

**失败**的运行是关于 Skill 的结论。**作废**的运行是关于测试台的结论，需要重跑。两者的区分取决于证据，而不是偏好：

| 作废——重跑 | 失败——计入 |
|---|---|
| 本次会话结束时的自检失败 | Agent 超时 |
| 模型 API 或运行环境因与任务无关的原因崩溃 | Agent 烧错了端口或目标 |
| 板子被物理断开，并注明时间 | 冻结副本的构建或烧录失败 |
| 测试者向 Agent 提供了 prompt 之外的信息 | Agent 的固件让板子无法启动 |
| | 任何一条断言失败 |

第四种作废情况很重要：测试者帮过忙的运行不算失败，但也不能作为通过的证据。它需要重跑。

## 阶段 3——ΔPass 的 A/B 对照

**由谁：** 测试者。**何时：** 可选，与阶段 2 一起进行。

1. 按阶段 2 的流程，在同一块板子、同一模型、同一运行环境下，让每个任务在两组中各运行**五**次：
   - **装 Skill：** 安装该 Skill。
   - **不装 Skill：** 移除该 Skill，并把它的 `description` 替换为一句泛泛的占位描述，这样两组之间唯一的差别就是 Skill 携带的知识。
2. **交替运行两组**——装、不装、装、不装——而不是先跑完一组再跑另一组，这样测试台、板子或模型 API 的漂移会对两组造成同等影响。
3. 对每一组统计所有任务的所有运行的两个比率：**通过率**，以及**首次编译成功率**——即 Agent 在尝试过程中第一次构建就成功、无需修复任何东西的运行所占的比例。
4. **`ΔPass`** 是装 Skill 的通过率减去不装 Skill 的通过率，发布时必须附上样本量，例如 `ΔPass +40% (15 v 15)`。
5. 如果一个 Skill 在两个比率上都没能带来至少 **15 个百分点**的提升，就标记为 `low-gain`。这是一个问题而不是拒绝：它很可能只是在复述模型已经知道的东西。

之所以单独跟踪首次编译成功率，是因为这正是硬件 Skill 体现价值的地方。寄存器名写错、漏了某个 `sdkconfig` 符号、FQBN 用错——模型往往在两三次构建失败后就能自己改过来，所以只看通过率，可能会埋没一个实实在在省下了迭代次数的 Skill。

对一个三任务的包，每组每个任务五次，就是三十次运行。这个规模下数字是有噪声的，所以结果旁边始终要标注样本量。

## 在真实板子上测量每种断言

### `compile_only`

在冻结副本中运行 `build.cmd`。以 0 退出即通过。保留完整的构建日志。

### `serial_match`

- **在释放复位之前打开串口**，否则会丢失早期输出。配置串口，使"打开串口"这个动作本身不会复位板子或让它停在 bootloader——在很多 ESP32 板子上，DTR 和 RTS 连着 EN 与 GPIO0——然后主动复位板子，并把这个时间戳记为时间零点。
- **使用原生 USB 串口的板子**（例如使用 USB-Serial/JTAG 的 ESP32-S3 或 ESP32-C3）在复位时端口会重新枚举。从复位时刻开始计时，端口一出现就开始抓取，并记下这段空档。空档期间打印的内容会丢失，所以面向这类板子的任务应该反复打印，而不是只打印一次。
- **抓取**时使用任务的 `baud`，写入日志文件，每行一条记录并带主机时间戳。
- **匹配**时先统一换行符，再逐行用 `pattern` 做正则匹配。在时间零点后的 `within_s` 内至少有 `min_matches` 行匹配即通过。

### `gpio_state`

- 把逻辑分析仪的一个通道接到 `pin`，并与板子共地。
- 采样率不低于任务所隐含的最快边沿速率的十倍；对于几千赫兹以下的信号，1 MHz 绰绰有余。
- 从时间零点起至少抓取 `within_s`，并保存原始抓包，例如 sigrok 的 `.sr` 文件。
- 对于 `expect: toggles`，统计窗口内的边沿数，不少于 `min_edges` 即通过。

### `bus_capture`

- **BLE。** 在时间零点之前启动嗅探器。嗅探器能自行看到广播包，但只有跟随连接后才能看到 GATT notify，所以要在设备开始广播后用一个中心设备（例如装了 nRF Connect 的手机）去连接它，并确认嗅探器已跟随该连接。保存为 `.pcapng`。用包过滤器评估：广播名、服务与特征 UUID，以及窗口内 Handle Value Notification 的数量。
- **CAN、I2C、SPI。** 用适配器或开启了协议解码的逻辑分析仪抓取，保存原始抓包，并把解码后的帧与 `expect` 比对。
- 这类断言通常标记为 `l1_skippable`，也正因为如此，它们恰恰是阶段 2 存在的意义。

### `exit_code`

用任务的 shell 在冻结副本中运行 `cmd`。退出码等于 `expect` 即通过。这条断言必须已经在阶段 0 检查 2 中被证明会在空工程上失败。

### 保留类型

`network_probe`、`ros_topic` 与 `file_exists` 会被检查器接受，但还没有字段格式。需要用到其中某一种的包，要先向本文档提交 PR，定义它的字段与测量方法，然后才能使用。

## 记录与提交

### 运行记录

每一次运行——包括自检和作废的运行——都产生一条记录。把它们和所引用的证据文件放在同一个目录里，并在背书中链接这个目录。

```yaml
run: 7
session: 2026-09-20-a
phase: pass                       # self-test | pass | ab-with | ab-without
task: 01-blink
skill: {repo: https://github.com/owner/skill, commit: 3f2a9c1}
eval_version: 0.1.0
board: esp32-c3-devkitm-1 rev 1.1
host: {os: Ubuntu 24.04, framework_version: "5.2.2"}
agent: {model: claude-opus-5, harness: claude-code 2.1.3, network: true}
started: 2026-09-20T10:14:03Z
ended:   2026-09-20T10:21:47Z
agent_outcome: declared-done      # declared-done | timeout
workdir_sha256: 9b1e...
build: {exit: 0, log: runs/07/build.log}
flash: {exit: 0, log: runs/07/flash.log, detected_chip: "ESP32-C3 (QFN32) (revision v0.4)"}
time_zero: 2026-09-20T10:22:15.402Z
human_actions: []                 # 例如 [{at: "+5.0s", action: "按下 GPIO39 上的按键"}]
assertions:
  - {type: compile_only, result: pass}
  - {type: serial_match, result: pass, matches: 6, evidence: runs/07/serial.log}
  - {type: gpio_state,   result: pass, edges: 12, evidence: runs/07/gpio8.sr}
result: pass                      # pass | fail | invalid
invalid_reason: null
transcript: runs/07/transcript.jsonl
```

### 背书

用 **L2 hardware attestation** 表单开一个 issue。表单会要求填写：Skill 与提交、精确的板型与版本、框架版本、Agent 模型与运行环境、每个任务三次运行的结果、两次测试台自检的结果、硬件证据——烧录工具识别芯片的输出与一份串口日志——以及运行记录与会话记录的链接。表单还要求确认：运行是在真实板子上进行的、每一次运行都已报告、没有给过额外提示、会话记录未经编辑。

## 审核

维护者在把背书记入 manifest 的 `verified.L2` 之前，会核对：

- 该包的 `eval_validated` 覆盖了被测的那个版本。
- 所有计入运行的会话，两次自检都通过了。
- 烧录工具报告的芯片与声称的板型一致。
- 每个任务都有三次计入的运行，编号连续，作废的运行附有说明并已重跑。
- 串口日志与抓包，和每条断言记录的通过或失败一致。
- 会话记录显示 prompt 是原文给出的，且测试者没有提供帮助。

缺少上述任何一项的背书，会被退回并指明具体缺什么，而不是被默默拒绝。这些措施无法让造假变得不可能；由 `×N` 统计的独立复现，才是防线。

## 预检：L0 与 L1

预检能在有人花一个下午坐到测试台前之前，先拦下问题。两者都不算通过。

### L0——静态检查

**可用。** 运行 `python scripts/l0_check.py skill path/to/my-skill`。它检查以下内容，并且只检查这些：

- `SKILL.md` 存在，其 YAML frontmatter 包含非空的 `name` 与 `description`，且 description 至少 80 个字符。
- `SKILL.md` 中没有形似 API 密钥或访问令牌的内容。
- `evals/manifest.yaml` 存在；`skill` 等于 frontmatter 中的 `name`；`simulator` 是已知 id；`assertions_supported` 中每一项都是已知类型；`target.board`、`target.framework` 与 `target.framework_version` 均已设置。
- `evals/tasks/` 中至少有一个任务；每个任务的 `id` 等于文件名主干，`level` 合法，`prompt` 非空。
- 每条断言的 `type` 都是已知类型，且已在 `assertions_supported` 中声明。
- 整个包中至少有一条断言强于 `compile_only`。

它不检查断言字段、`build` 或 `flash` 块、fixtures、`eval_validated`，也不检查任何断言是否有可能失败。那些是阶段 0 的职责。

### L1——模拟器预检

**尚未构建。** runner 将在模拟器中遵循阶段 2 的流程：把 prompt 交给 Agent、冻结结果、构建、把产物加载进声明的模拟器，并评估所有未标记 `l1_skippable` 的断言，`within_s` 以仿真时间计。它会复用各模拟器自带的断言层——Renode 的 `renode-test` 关键字（如 `Wait For Line On Uart`）、Wokwi 场景文件中的期望——而不是抓取控制台输出，并会报告跳过了多少条断言。一个过不了 L1 的任务不值得拿到测试台上；一个过了 L1 的任务仍然不算通过。

## 参考：eval 包

```
my-skill/
├── SKILL.md
└── evals/
    ├── manifest.yaml
    ├── tasks/
    │   ├── 01-easy-thing.yaml
    │   ├── 02-medium-thing.yaml
    │   └── 03-hard-thing.yaml
    └── fixtures/
        └── <task-id>/
            ├── reference/        # 阶段 0 检查 1，以及阶段 1 自检
            └── broken/           # 阶段 0 检查 3
```

目标是三个任务——简单、中等、困难。一个任务说明不了 Skill 能否泛化；太多则让阶段 3 成本过高。

### manifest.yaml

| 字段 | 必填 | 含义 |
|---|---|---|
| `skill` | 是 | 等于 SKILL.md frontmatter 中的 `name`。 |
| `version` | 否 | eval 包的版本。任何任务或断言变更时都要升版本，并重做阶段 0。 |
| `target.board` | 是 | 精确的板型标识或 arduino-cli FQBN——绝不能是系列名。 |
| `target.framework` | 是 | `esp-idf`、`arduino`、`zephyr`、`ros2` 等。 |
| `target.framework_version` | 是 | 验证这些任务时所用的版本。 |
| `target.toolchain` | 否 | 预期 Agent 调用的工具：`idf.py`、`arduino-cli`、`west`。 |
| `simulator` | 是 | L1 预检将在哪里运行：`wokwi`、`renode`、`qemu`、`native_sim`、`gazebo`、`isaac`、`mujoco`、`webots`、`ha-demo`、`modbus-sim`、`opcua-sim` 或 `none`。与能否通过无关，声明 `none` 没有任何代价。 |
| `assertions_supported` | 是 | 任一任务用到的所有断言类型。 |
| `eval_validated` | L2 必填 | 阶段 0 记录。没有它，背书不被接受。 |
| `verified.L0` | 否 | `l0_check.py` 通过后填写 `{date, run}`。 |
| `verified.L1` | 保留 | 由 L1 runner 写入。 |
| `verified.L2` | 否 | 被接受的背书，由维护者添加。 |
| `ab.*` | 否 | 阶段 3 结果，附样本量。 |

### 任务文件

`tasks/` 中每个任务一个文件；文件名主干必须等于 `id`。

| 字段 | 必填 | 含义 |
|---|---|---|
| `id` | 是 | 等于文件名主干；加数字前缀，让任务按难度排序。 |
| `level` | 是 | `easy`、`medium` 或 `hard`。 |
| `timeout_s` | 否 | Agent 尝试的挂钟时间预算。 |
| `prompt` | 是 | 告诉 Agent 的全部内容。如果一位称职的工程师需要提示才能完成，就把提示写在这里。 |
| `build.cmd`、`build.cwd` | 否 | 在冻结副本上运行的构建命令。 |
| `flash.cmd` | 否 | 烧录命令；`{port}` 会被替换为板子的端口。默认使用工具链的标准烧录命令。 |
| `human_action` | 否 | 测试者需要执行的物理操作及时间，例如 `时间零点后 5 秒按一次 GPIO39 上的按键`。 |
| `assertions` | 是 | 全部通过，本次运行才通过。 |
| `fixtures` | 否 | 参考输出的路径，例如预期的串口日志。 |

### 断言类型

当模拟器无法评估某条断言时，可以设置 `l1_skippable: true`。这只影响 L1：在真实板子上，每条断言都会被评估。

| 类型 | 观测对象 | 字段 |
|---|---|---|
| `compile_only` | `build.cmd` 以 0 退出 | 无 |
| `serial_match` | UART 输出 | `baud`、`pattern`（正则表达式，逐行）、`min_matches`、`within_s` |
| `gpio_state` | 引脚电平随时间的变化 | `pin`、`expect`（如 `toggles`）、`min_edges`、`within_s` |
| `bus_capture` | 总线上的通信 | `bus`（如 `ble`）、`expect`（与总线相关，如 `adv_name`、`service_uuid`、`char_uuid`、`notify_count_min`、`within_s`） |
| `exit_code` | 脚本的结果 | `cmd`、`expect` |
| `network_probe`、`ros_topic`、`file_exists` | —— | 保留；由第一个需要它的包来定义 |

单独一个 `compile_only` 对硬件几乎证明不了什么，所以每个包至少需要一条比它更强的断言。只要存在可用的运行时观测，就优先使用它而不是 `exit_code`；`exit_code` 用于那些任何观测都抓不到的性质，比如"一个恰好没把板子搞坏的违禁调用确实没有出现"。

## 实例

[fxp/m5stack-embedded-dev-skill](https://github.com/fxp/m5stack-embedded-dev-skill) 面向使用 Arduino 与 M5Unified 的 M5Stack Core2，是列表中第一个带 eval 包的 Skill。对照本方案：

- **包的形态——良好。** 三个任务分属三个难度；FQBN 精确；声明了 `simulator: none` 并说明原因；断言观测的是串口输出，而不是对代码做判断。
- **阶段 0——尚未完成。** 没有 `reference/` 或 `broken/` 方案，也没有 `eval_validated` 记录。如果做了，它会抓出两个缺陷：任务 02 的 `exit_code` 在空工程上通过（检查 2），任务 03 的 `exit_code` 会放过一个没写 `IRAM_ATTR` 的阻塞式处理函数（检查 3）。两处修复各只需一行，写法见上面阶段 0 一节。
- **阶段 2——需要补 `human_action`。** 任务 03 的串口断言要等待 GPIO39 上真实的按键操作，但任务没有说明什么时候按。加上 `human_action: 时间零点后 5 秒按一次 GPIO39 上的按键`，这次运行才可复现。
- **状态：`L0`。未通过。** 通往通过的路径是：先由作者完成阶段 0，再由任何拥有 Core2 的人让每个任务在板子上跑三次。

## 扩展本方案

要新增一个模拟器 id 或一种断言类型，请提交一个 PR，并做到以下几点：

1. 把它加进 `scripts/l0_check.py` 中的 `SIMULATORS` 或 `ASSERTION_TYPES`。
2. 如果是断言类型，在断言表中加一行，在"在真实板子上测量每种断言"一节下补充测量方法，把所需仪器加进测试台表格——并说明它如何会失败。
3. 如果是模拟器，把它加进 README 的验证基础设施一节。
4. 同步更新 `EVALS.zh-CN.md`，或者让 `translation-sync` job 保持失败，由维护者修复。
