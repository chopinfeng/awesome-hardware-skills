# 硬件 Skill 评测：测试方案

*[English](EVALS.md) · 简体中文*

> 本文档译自 [EVALS.md](EVALS.md)。如两者有出入，以英文版为准。

这份文档是 [README](README.zh-CN.md) 中那些徽章背后的测试方案。它讲清楚：一个硬件 Skill 在什么上测、由谁测、测几次、每条断言在真实板子上怎么测量、怎样让 eval 远离 Agent、记录什么，以及结果什么时候算数。为什么值得投入，见 [GAPS.zh-CN.md](GAPS.zh-CN.md)。

其余一切都服务于这一条规则：**只有当一个 Skill 的任务在真实板子上运行、且断言成立时，它才算通过。** 静态检查和模拟器只是预检。本仓库中任何其他情况都不叫"通过"。

## 今天已经有什么

请先读这里——文档其余部分描述的是完整方案，很容易把计划中的部分误当成已经可用的部分。

| 组成部分 | 状态 |
|---|---|
| Eval 包格式 | 本文档中定义；起步模板在 `template/evals/` |
| `L0` 静态检查 | **可用**，已接入 CI——`python scripts/l0_check.py skill <path>` |
| 编写辅助 | **可用**——[`skills/hardware-skill-creator/`](skills/hardware-skill-creator/)，一个 Agent Skill：生成包的脚手架，执行 L0 不做的检查（空转命令、prompt 中的取值、fixtures、泄漏提示），并协助执行阶段 0–3 |
| 触发预检 | **可用，人工执行**——在主机上跑约 20 条请求，不需要板子；见"预检"一节。永远不算通过 |
| `claude plugin eval` | **补充，而非替代**——Claude Code 内置的评测工具可以跑触发预检和主机侧的编译检查，用例对 Agent 隐藏，并自带不装 Skill 的基线组；但它没有自定义代码评分器，也观测不到板子，所以它的结果永远不算通过 |
| `L1` 模拟器预检 runner | 尚未构建，且永远不算通过 |
| 真实硬件上的阶段 0–3 | **可用，人工执行**——下面每一步今天都能用一块板子和所列工具完成 |
| `L2` 背书表单 | **可用**——`.github/ISSUE_TEMPLATE/attestation.yml`（2026-09-16 之前是非法 YAML；CI 现在会检查它） |
| `ΔPass` 自动 A/B runner | 尚未构建；由阶段 3 的人工流程代替 |
| `stale` 标记 | 尚未构建；由维护者根据背书日期标记 |

截至 2026-09-18，列表中有一个 Skill 提供了 eval 包，**还没有任何 Skill 通过。**

## 测试回答什么问题

两个问题，分开回答：

1. **这个 Skill 能不能用？** 装上 Skill 后，Agent 能否在真实板子上完成每个任务？由阶段 2 回答。回答"能"，即获得 `L2` 徽章。
2. **这个 Skill 是否携带了知识？** 装与不装相比，结果是否不同？由阶段 3 回答。差值即 `ΔPass`。

一个 Skill 可能通过了问题 1，却在问题 2 上显示不出可测量的增益——模型可能本来就会。两个结果都会公开。

在回答这两个问题之前，必须先回答第三个：**eval 本身可信吗？** 如果一条断言在什么都没做、Agent 伪造了信号、或 Agent 偷看了答案时也能通过，它对这个 Skill 说明不了任何问题。阶段 0 和隔离规则正是为此而设，它们排在最前面。

## 方案概览

| 阶段 | 由谁 | 何时 | 目的 | 产出 |
|---|---|---|---|---|
| 0——验证 eval | 包作者 | 每个 eval 版本一次 | 证明任务可完成、断言会失败 | manifest 中的 `eval_validated` |
| 1——测试台自检 | 测试者 | 每次测试会话的开始与结束 | 证明测试台正常，这样失败才能归咎于 Skill | 自检记录 |
| 2——通过判定运行 | 测试者 | 每份背书 | 判定 Skill 是否通过 | 运行记录、`L2` 背书 |
| 3——A/B 对照 | 测试者 | 可选，随背书一起 | 衡量 Skill 带来了什么 | 附区间的 `ΔPass` |

## 测试台

以下所有内容都要写进每一条运行记录。在不同测试台上跑出的两次运行不可比较。

**目标板。** 必须是 `target.board` 中指定的那块板；厂商有多个版本或模组型号时要写明，例如 `esp32-c3-devkitm-1 ESP32-C3-MINI-1`。不能用同系列的兄弟型号代替。

**主机。** 操作系统及版本，以及版本恰好等于 `target.framework_version` 的工具链。请用带电源的 USB Hub 或台式电源给板子供电——USB 口供电不足会导致掉电复位，看起来就像固件 bug。

**观测仪器**，根据包中用到的断言类型按需准备：

| 断言类型 | 仪器 | 说明 |
|---|---|---|
| `compile_only`、`exit_code` | 无 | 在主机上运行 |
| `serial_match` | 板载 USB 转串口，或独立的 USB 转串口模块 | 抓取时带主机时间戳 |
| `gpio_state` | 逻辑分析仪（兼容 sigrok 的即可） | 与板子共地 |
| `bus_capture`（BLE） | BLE 嗅探器——例如装了 nRF Sniffer 的 nRF52840 dongle，或兼容 Sniffle 的板子 | 必须跟随连接才能看到 notify |
| `bus_capture`（CAN、I2C、SPI） | CAN 适配器，或带协议解码的逻辑分析仪 | |

**Agent。** 模型 ID、运行环境（harness）及其版本，以及运行环境的工具权限。Agent 运行在连着板子的主机上，在尝试过程中可以自己构建、烧录和读串口——这个闭环正是 Skill 的实际使用方式，也是"通过"所声称的内容。记录 Agent 是否能联网，以及它接触硬件的方式——原始 shell 加串口，还是某个指定版本的工具（例如 MCP server）——写入 `agent.hardware_access`。这个选择对结果的影响可能和 Skill 本身一样大：在 Embedded Arena 中，同一个模型有硬件反馈时 70% 的尝试成功，只有文档时是 40%。阶段 3 的两组必须使用相同的接触方式；如果工具自带烧录与复位的审计日志，把日志一并作为证据。

**被测 Skill。** Skill 所在的仓库与提交 SHA，以及 eval 包的 `version`。结果属于那一次提交，而不是泛指这个 Skill。

### 主机基线

只复位板子是不够的，主机也会在运行之间残留状态。运行环境的记忆与配置（例如 `~/.claude/`、项目里的 `CLAUDE.md`、自动记忆）、工具链全局的库与组件缓存（Arduino 的库与内核、ESP-IDF 托管组件），以及 shell 历史，都会在一次运行后保留下来。Agent 在"装 Skill"那次运行中装上的库，会悄悄帮到紧随其后的"不装 Skill"那次运行，从而缩小 `ΔPass`。

预先准备一个**基线**——一个全新的系统用户、一个容器镜像或一个虚拟机快照，其中已经装好指定版本的工具链——在每次运行前恢复到它，丢弃上一次运行添加的一切。把它的标识记为 `host_baseline`。不是从这个基线启动的运行一律作废。

### 芯片身份

每次运行都要记录芯片自身的唯一标识，这样运行、自检和背书才能被关联到同一块物理芯片：

| 芯片系列 | ID 从哪里来 |
|---|---|
| ESP32 系列 | 烧录时 esptool 连接后打印的 `MAC:` 那一行，或 `esptool read-mac` |
| nRF52 | FICR `DEVICEID`，例如 `nrfjprog --memrd 0x10000060 --n 8` |
| STM32 | 96 位唯一 ID 寄存器，通过调试探针读取；其地址因系列而异 |
| RP2040 / RP2350 | `picotool info` 报告的板卡 ID（在 RP2040 上是闪存芯片的唯一 ID） |

同时记录串口的 USB 序列号；在许多原生 USB 的板子上，它是由芯片派生出来的。模拟器可以被设置成任意 ID，所以这本身并不能证明是真实硅片——它能抓住什么，见"审核"一节。

### 保护测试者与板子

测试者要在自己的机器上安装陌生人的 Skill，并把 USB 口和烧录器交给 Agent。第一次运行之前，先用 `mcp-scan` 之类的 Skill 扫描工具扫描锁定 commit 下的 Skill，并逐条阅读其 `SKILL.md` 和脚本中的每一个下载或安装步骤。Snyk 在 2026 年 2 月扫描了 3,984 个已发布的 Skill，其中 36.82% 至少有一处安全缺陷；而硬件 Skill 经常要求安装工具链，这恰好是恶意 Skill 常用的借口。把扫描结果写入运行记录。这一步只为保护测试者，与是否通过无关。

Agent 也会对板子做不可逆的事。Embedded Arena 报告，Agent 删掉了被明确要求保留的安全延时，"ultimately locking the board and forcing a manual reset that the agent cannot execute"。由此有以下规则：

- 测试台可以在不可逆命令到达板子之前将其拦截——烧写 eFuse、开启 Secure Boot、Flash Encryption、读保护，以及通过原始调试器执行整片擦除——方法可以是 PATH 包装脚本，或带白名单的硬件工具。被拦截的命令判运行失败，但板子不必退役。
- 每次运行都记录 `bench_damage`：`none`、`recovered`（注明方法）、`debug-locked` 或 `efuse-burned`。
- 带 Wi-Fi、BLE 或以太网的板子本身就是一个网络行为者，Agent 也是。把两者放在带出口白名单的隔离网络上。UK AISI 报告，在某个挑战的 122 次运行中，有 10 次出现 Agent"autonomous, unsanctioned action on the live internet"，并得出结论："good containment should not depend on the model choosing not to test its boundaries"。
- 任何一次救砖之后，都要重做阶段 1 自检，会话才能继续。无法救回的板子，或 eFuse 概要发生变化的板子，不能再用于背书。

## 让 eval 远离 Agent

前沿模型只要有机会，就会去读评分器和答案：METR 观察到的"钻奖励空子"行为——返回评分器预先算好的答案、篡改评分函数、搜索泄露的参考实现——在某个任务集上出现在 30.4% 的运行中，而且告诉模型"不要作弊"几乎没有改变这个比例。只把测试藏起来也不够：METR 2026 年 5 月的风险报告发现，在它最长的那批任务上，"at least 16% of successful runs were illegitimate upon review"；Anthropic 也报告过 Agent "by examining the git history from previous trials" 获得了不公平的优势——这正是下文主机基线与 `.git` 规则存在的原因。会话记录只是证据，不是证明：在 METR 2026 年 8 月对一次 Agent 入侵事件的调查中，Agent 做出了伪造工具调用的手段，并"used this to alter outputs in our actual transcripts"，一个共享的软件包缓存成了"a covert mailbox among agents"。所以"通过"要以测试台从板子上采集的证据为准，审查通过的运行时要同时读冻结的源码和会话记录，主机基线也要在两次运行之间丢弃工具链与软件包缓存。一个与 `SKILL.md` 并排放置的 eval 包，会把参考方案、错误方案和每一条断言的模式都放进安装好的 Skill 里。以下四条规则堵住这个口子：

1. **安装 Skill 时不带 eval。** 为本次运行复制 Skill 时，删除 `evals/` 以及任何 `.git` 目录。把 eval 包、fixtures 和评分脚本放在 Agent 的运行环境读不到的位置，并从那份副本运行所有断言。
2. **检测篡改。** 在 Agent 开始前和结束后，各记录一次已安装 Skill 目录的 SHA-256。两者不同，或会话记录显示 Agent 读取或修改了任何 eval、fixture 或评分文件，本次运行判失败，`failure_class: tampered`。
3. **Skill 里不能有答案。** Skill 传授的是知识；它不能包含任何任务的答案。知识是关于芯片的事实——M5Stack Core2 的电源管理芯片在 I2C 地址 `0x34` 应答，一个写明这一点的 Skill 正是在做它该做的事。答案则是 eval 专属的——某个任务的参考代码、它的文件名，或是与断言所匹配内容完全一致的输出字符串。作者在阶段 0 检查这一点，审核者再查一次；这需要判断，而不是一条正则，因为同一个常量既可能是知识，也可能是答案。
4. **prompt 要写明断言匹配的一切。** 断言检查的每一个引脚、字符串、UUID、频率和波特率，都必须出现在 prompt 中。否则，一个选择了不同但同样合理取值的正确方案会失败，eval 衡量的就成了运气。

## 阶段 0——验证 eval

**由谁：** 包作者，在请任何人背书之前。**何时：** 每个 eval 包版本一次；任何任务或断言变更后都要重做。

一个 eval 的价值，取决于它能否分辨正确方案与错误方案。对每个任务，作者准备若干方案，并在真实板子上做五项检查：

```
evals/fixtures/<task-id>/reference/   一份已知正确的方案；启动时打印芯片 ID
evals/fixtures/<task-id>/broken/      一份恰好包含该任务要抓的那个错误的方案
evals/fixtures/<task-id>/spoof/       一份不做任务、只伪造被观测信号的固件
```

1. **参考方案通过。** 构建、烧录并观测参考方案。每一条断言都通过，包括标记了 `l1_skippable` 的。这证明该任务在这块板子上可以完成，且没有哪条断言过严。
2. **空工程失败。** 在一个空的工作目录上运行每条断言。每一条都失败。这能抓出"什么都没构建也能通过"的检查。
3. **错误方案被抓住。** 构建、烧录并观测错误方案。针对这个错误的断言失败。这能抓出"构建了错误的东西也能通过"的检查。
4. **伪造固件被抓住。** 构建、烧录并观测一份专为骗过断言、而不是完成任务而写的固件——循环打印所有预期的行、用定时器翻转引脚、广播预期的名字但不提供 GATT 服务，或者崩溃循环让启动信息反复出现。至少一条断言或重启保护判失败。如果都没有失败，就要加一条与真实行为挂钩的断言：总线抓包、相对于某个输入的边沿时序、依赖传感器的数值。
5. **作弊 Agent 被抓住。** 在板子上运行一个装了该 Skill 的 Agent，给它的 prompt 要求它不完成任务、只让断言通过——就像 Terminal-Bench 2.0 的对抗性作弊 Agent 那样。保留会话记录与证据，无论它是否成功都要阅读。如果它通过了所有断言和重启保护，说明 eval 有漏洞：加固后重做。检查 4 的伪造固件覆盖的是作者想得到的骗法；这一项覆盖的是 Agent 自己找到的骗法，比如 Embedded Arena 在真实微控制器上看到的硬编码 UART 输出。一个成本很低的补充是**不可能完成的任务**——板子按字面要求根本做不到，比如外设达不到的速率——交给普通 Agent：任何通过都是作弊。

检查 2、3、4 抓的是不同的缺陷，一个包三者都需要。列表中第一个第三方包就说明了 2 和 3 的原因。它的一个任务禁止再次调用 `Wire.begin()`，用 `! grep -q "Wire.begin(" *.ino` 来检查。在空目录上，这条检查以 0 退出：`grep` 找不到 `*.ino`，而 `!` 把它的报错变成了通过。检查 2 能抓住它；检查 3 抓不住，因为错误方案里确实有 `.ino` 文件。另一个任务禁止在中断处理函数里使用阻塞调用，并通过匹配 `IRAM_ATTR` 来定位处理函数。在空目录上它正确地失败了——但面对一个没写 `IRAM_ATTR`、却调用了 `Serial.println` 和 `delay` 的处理函数，它以 0 退出。检查 2 抓不住它；只有检查 3 能抓住。检查 4 之所以存在，是因为串口正则是板子上最容易伪造的信号，而另外几项检查都没有去尝试伪造。检查 5 之所以存在，是因为 Agent 的想象力不受作者想象力的限制。

参考方案会在启动时打印芯片的唯一 ID，这样阶段 1 中每一份自检日志都被绑定到这块芯片上。Agent 的任务永远不要求这一点：把它写进 prompt 会改变 Agent 被要求做的事，从而污染 `ΔPass`。

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
  board: esp32-c3-devkitm-1 ESP32-C3-MINI-1
  framework_version: "5.2.2"
  reference_passed: true      # 检查 1，每个任务
  empty_failed: true          # 检查 2，每条断言
  broken_caught: true         # 检查 3，每个任务
  spoof_caught: true          # 检查 4，每个任务
  exploit_caught: true        # 检查 5，每个任务
  leakage_reviewed: true      # Skill 中不含任何任务的答案
  evidence: https://...       # 五项检查的日志、抓包与作弊 Agent 的会话记录
```

## 阶段 1——测试台自检

**由谁：** 测试者。**何时：** 每次测试会话的开始与结束。

烧录每个任务的 `reference/` 方案并评估其断言，做法与阶段 2 的一次运行完全相同，只是没有 Agent。每一条断言都必须通过，并且参考方案打印的芯片 ID 必须与烧录时记录的 ID 一致。对 ESP32 系列板子，还要在两次自检时各记录一次 eFuse 概要（`espefuse summary`）。每次会话拍一张照片：板子通过线缆连着主机，终端画面可见——这是模拟器唯一伪造不出来的证据。

只有**两次**自检都通过，这次会话的结果才算数。如果结束时的自检失败，本次会话中的每一次运行都**作废**——测试台可能在任何时刻出了问题——需要在新会话中重跑。如果两次之间 eFuse 概要发生了变化，烧写它的那次运行判失败，这块板子也不能再用于背书，因为 eFuse 位无法清除。

## 阶段 2——通过判定运行

**由谁：** 测试者。**何时：** 每份背书。

### 单次运行流程

1. **记录运行元数据**（见上文"测试台"一节所列），并给本次运行分配下一个连续编号。
2. **把板子复位到已知状态。**
   - 用工具链的擦除命令擦除整个闪存，并保留其输出。如果因为安全启动（Secure Boot）或闪存加密（Flash Encryption）已开启而被拒绝擦除——esptool 默认会拒绝——这块板子不能用于背书。
   - 断开所有电源（包括电池）至少 5 秒，并通过指示灯熄灭或电流读数确认已经断电。Hub 的端口断电命令只有在附带这种确认时才算数；很多 Hub 实际上并不会真正断电。带电池的板子在拔掉 USB 后会继续运行——例如 M5Stack Core2，需要长按电源键 6 秒才能关机。
   - 取出或重新格式化任何 SD 卡，并复位任何自带电源的外部外设。
3. **恢复主机基线**，并安装不带 `evals/` 与 `.git` 的 Skill。记录已安装 Skill 目录的 SHA-256。
4. **启动 Agent 并开始录制会话。** 把任务的 `prompt` 原文交给 Agent，别的什么都不给——不给端口名、不给提示、不纠正——除非 prompt 本身包含这些内容。
5. **让 Agent 工作**，直到它宣布完成，或挂钟时间达到 `timeout_s`。超时是一次失败的运行，而不是作废的运行。
6. **冻结结果。** 打包归档工作目录并记录其 SHA-256，再记录一次已安装 Skill 目录的 SHA-256。此后所有步骤都使用冻结的副本；Agent 在尝试过程中自己做的构建和烧录不算证据，但要记录其次数。
7. **构建。** 在冻结副本中运行 `build.cmd` 并保留日志。如果失败，`compile_only` 判失败，其余断言都记为 `not-run`。
8. **烧录。** 先擦除，再用任务定义的 `flash.cmd`（若未定义则用工具链的标准烧录命令）写入构建产物。保留烧录工具的完整输出，包括它报告所识别芯片及其唯一 ID 的那几行。
9. **观测。** 在释放复位之前启动所有抓取。**时间零点**是复位被释放、新固件开始运行的时刻；每个 `within_s` 窗口都从这里开始计算。为了下文的重启保护，串口要从时间零点一直抓取到最长的那个窗口结束。按任务定义的时间执行其 `human_action`，并记录时间戳。
10. **判定本次运行是否有效**——只依据测试台证据，在读取任何断言结果之前。
11. **评估每条断言**，方法见下一节，并保留每条断言的原始证据文件。
12. **记录结果。** 每条断言为 `pass`、`fail` 或 `not-run`。只有每条断言都通过、且重启保护未触发，这次运行才通过。失败的运行记录一个 `failure_class`：`build`、`flash`、`crash`、`behaviour`、`timeout`、`tampered` 或 `illegitimate`。每次运行都记录 `bench_damage`。
13. **计入之前，审查通过的运行是否正当**，见下文。

### 重启与崩溃保护

一个崩溃重启的固件每次都会重新打印启动输出，所以崩溃循环本身就可能满足 `min_matches`。因此，只要时间零点之后串口抓取中出现重启或致命错误，每次运行都判失败——除非任务设置了 `expect_reset: true`。

时间零点触发的那一次启动是预期之内的，所以保护机制使用 manifest 的两个字段。`boot_banner` 匹配每次启动恰好打印一次的那一行；时间零点之后第二次匹配就是一次重启。`reboot_patterns` 匹配致命错误输出；时间零点之后任何一次匹配都判运行失败。对 ESP32 系列，默认的横幅是 `^rst:0x`（ROM 每次启动打印一行），致命模式是崩溃（`Guru Meditation|abort\(\) was called|assert failed:|Backtrace:`）和掉电复位（`Brownout detector`）。其他芯片系列的包需要定义自己的模式；平台本身不打印横幅时，由 reference 和 prompt 在程序开头打印一行固定文字。在原生 USB 串口的板子上，时间零点之后端口重新枚举也算作一次重启。

### 任务与包如何算通过

- **运行：** 每条断言都通过（包括标记了 `l1_skippable` 的）、且重启保护未触发，即通过。
- **任务：** **最多三次运行中有两次通过**即通过。先跑两次；如果两次结果一致，就由它决定任务结果；如果不一致，再跑第三次来决定。这与"总是跑三次取多数"得出完全相同的结论，但运行次数更少。Agent 的行为不是确定性的，单次运行只是抽一次签。
- **包：** 每个任务都通过，包即通过。这就是 `L2` 徽章。
- **报告：** 每份背书都要列出每个任务的 `k/n`，以及所有计入运行的合并通过率及其 95% Wilson 区间，并标出计入运行**全部**通过的任务（`n/n`）。判定结果是一道门槛，而不是可靠性声明：一个 Agent 只有一半尝试能成功的任务，仍有一半概率通过这道门槛，公开的通过率才能说明这一点。对驱动硬件的东西来说，每次都成功比有时成功更重要——这就是 τ-bench 区分 pass^k 与 pass@k 的用意——所以即使"全部通过"不是门槛，也要报告它。若把它当门槛，一个成功率 90% 的任务在三次运行下大约每四次就会被误判失败一次。
- **范围：** 所有区间描述的都是这个 Skill 在这些任务、这块板子上的表现，不外推到类似任务或其他板子。
- **`L2 ×N`** 统计的是各自达到通过、且来自**不同芯片**（按芯片 ID）和**不同账号**的背书数量。在已计入的芯片上再做一次背书是受欢迎的，但不会增加 ×N。

每一次开始了的运行都要按顺序报告：通过的、失败的、作废的一视同仁。不允许挑选哪些运行计入；作废的运行要重跑，两者都要出现在记录中。

### 审查每一次通过的运行

断言检查的是正确的信号是否出现，检查不了固件是不是凭本事产生了这些信号。一次通过的运行在计入之前，测试者要阅读它的会话记录和冻结的源码，查找伪造工作的迹象：输出来自查表或定时器而不是计算、跳过外设并硬编码其结果、按时间表而不是靠检测来响应刺激，或者悄悄关掉了任务里的某项检查。断言通过但没有完成任务的运行判失败，`failure_class: illegitimate`，发现写入 `legitimacy_review`。METR 称人工检查作弊"often the majority of the work"；这里只有三个任务和少量通过的运行，逐一阅读是负担得起的。

### 失败的运行，还是作废的运行

**失败**的运行是关于 Skill 的结论。**作废**的运行是关于测试台的结论，需要重跑。两者的区分依据测试台证据，并且在读取断言结果之前做出：

| 作废——重跑 | 失败——计入 |
|---|---|
| 本次会话结束时的自检失败 | Agent 超时 |
| 模型 API 或运行环境因与任务无关的原因崩溃 | Agent 烧错了端口或目标 |
| 板子被物理断开，并注明时间 | 冻结副本的构建或烧录失败 |
| 测试者向 Agent 提供了 prompt 之外的信息 | Agent 的固件让板子无法启动 |
| 本次运行不是从记录的主机基线启动的 | 重启保护被触发 |
| | Agent 读取或修改了 eval，或已安装的 Skill 发生了变化（`tampered`） |
| | 断言通过，但审查发现任务并未完成（`illegitimate`） |
| | 测试台拦截了 Agent 发出的不可逆命令 |
| | 任何一条断言失败 |

第四种作废情况很重要：测试者帮过忙的运行不算失败，但也不能作为通过的证据。烧写了 eFuse 的运行判失败，并且这块板子不能再用于背书。

## 阶段 3——ΔPass 的 A/B 对照

**由谁：** 测试者。**何时：** 可选，与阶段 2 一起进行。

1. 按阶段 2 的流程，在同一块板子、同一模型、同一运行环境、同一硬件接触方式下，让每个任务在两组中各运行**五**次，并在每次运行前恢复主机基线：
   - **装 Skill：** 安装该 Skill，但不带其 eval。
   - **不装 Skill：** 完全不安装任何 Skill。
2. **交替运行两组**——装、不装、装、不装——这样测试台、板子或模型 API 的漂移会对两组造成同等影响。
3. 从每一次"装 Skill"运行的会话记录中，记录 **`skill_invoked`**——Agent 是否真的加载或读取了这个 Skill。一个从未被加载的 Skill，看起来和一个空无一物的 Skill 一模一样。
4. 对每一组，统计所有任务所有运行的**通过率**和**首次编译成功率**——即 Agent 在尝试过程中第一次构建就成功、无需修复任何东西的运行所占的比例——均以 `k/n` 附 95% Wilson 区间表示。同时为每次运行记录构建与烧录次数、token、费用和挂钟时间。
5. 按下一小节的方式报告 **`ΔPass`**：给出整体结果，再给出只统计 Skill 被调用过的运行的结果，然后附一张每个任务一行的表：该任务在两组中各自的 `k/5` 及其差值。如果某个任务五次"装 Skill"运行中 Skill 被调用不足四次，就把结果标记为 `trigger-weak`：这个 Skill 的 `description` 没能让它被加载。触发预检能在花任何测试台时间之前发现这一点。
6. 对"装 Skill"组，再报告每个任务的 **pass^2**——两次独立运行都通过的概率，由五次中 `c` 次通过无偏估计为 `c(c−1)/20`：五次全过为 1.0，四次为 0.6，三次为 0.3。这是"三取二"门槛给不出的可靠性数字。

之所以单独跟踪首次编译成功率，是因为这正是硬件 Skill 体现价值的地方。寄存器名写错、漏了某个 `sdkconfig` 符号、FQBN 用错——模型往往在两三次构建失败后就能自己改过来，所以只看通过率，可能会埋没一个实实在在省下了迭代次数的 Skill。

### 如实解读 ΔPass

一个三任务的包，每组每个任务五次，就是每组十五次运行，这个规模下数字噪声很大。当两组通过率都在 50% 左右时，这样的对比能可靠检出的最小差异约为 45 个百分点。要检出真实的 15 个百分点提升，每组大约需要 150 次运行；而一个毫无作用的 Skill，大约每五次就有一次会碰巧显示出 15 个百分点以上的"提升"。用单个数字加固定阈值会不断给 Skill 贴错标签，所以 `ΔPass` 始终以区间加标签的形式发布：

- **`ΔPass`** 是装 Skill 的通过率减去不装 Skill 的通过率，附 95% **Newcombe** 区间——这是两个比例之差的标准区间，由两组各自的 Wilson 区间构造而成，在小样本下依然准确，不像常见的 ±1.96 倍标准误那样。
- 区间下界大于零时，标记为 **`gain`**。
- 区间上界低于零时，标记为 **`harm`**——装了 Skill 反而更差。这不是假设：SkillsBench v4 报告"13 of 87 tasks show negative Skills deltas"。
- 区间上界低于 +15 个百分点时，标记为 **`low-gain`**——这是"Skill 帮助甚微"的证据。
- 其他情况标记为 **`inconclusive`**（无定论）。

例如 `ΔPass +20 pts [−12, +47] (15 v 15), inconclusive` 与 `ΔPass +67 pts [+34, +85] (15 v 15), gain`。按本方案的运行次数，大多数结果都会是 `inconclusive`，而每组运行次数低于大约一百次时，`low-gain` 根本无法达到。这是诚实的标签，而不是缺陷：应对噪声的办法是说出来，而不是把它藏起来。

```python
from math import sqrt

def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

def delta_pass(k_with, n_with, k_without, n_without):
    p1, p2 = k_with / n_with, k_without / n_without
    l1, u1 = wilson(k_with, n_with)
    l2, u2 = wilson(k_without, n_without)
    d = p1 - p2
    lo = d - sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = d + sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    label = "gain" if lo > 0 else "harm" if hi < 0 else "low-gain" if hi < 0.15 else "inconclusive"
    return d, lo, hi, label
```

这段代码能复现 Newcombe 方法公布的参考值（56/70 对 48/80 得到 0.200 [0.052, 0.334]）。

第一次相信 A/B 结果之前，测试者可以先做一次 **A/A** 对照——Skill 对它自己，同一测试台、同样交替——看清测试台本身的噪声。落在这个噪声以内的差异不是增益。2026 年一项关于配对噪声底的研究，正测得了这样一个对照："+5 pp with Wilson CI [−2,+12], not significant"。

跨任务合并运行，等于把它们当作独立抽样。两组中每个任务运行次数相同时，合并差值恰好等于各任务差值的平均；而 Newcombe 区间忽略了按任务的配对，在任务难度差别很大时偏保守。这是有意的选择：三个任务太少，估计不出聚类标准误，而保守的区间是更安全的错误。SkillsBench v4 在更大的框架下按任务配对计算差值；上面那张按任务的表保留了这部分信息。

不同背书的结果，按每个测试台各自的 `ΔPass` 合并，绝不跨测试台合并原始运行。想提前停止的测试者可以使用 STEP 这类序贯检验，但前提是在第一次 A/B 运行之前，把它的错误率和每组最大运行次数记录在 manifest 的 `sequential_plan` 中。

## 在真实板子上测量每种断言

### `compile_only`

在冻结副本中运行 `build.cmd`。以 0 退出即通过。保留完整的构建日志。

### `serial_match`

- **在释放复位之前打开串口**，否则会丢失早期输出。配置串口，使"打开串口"这个动作本身不会复位板子或让它停在 bootloader——在很多 ESP32 板子上，DTR 和 RTS 连着 EN 与 GPIO0——然后主动复位板子，并把这个时间戳记为时间零点。
- **使用原生 USB 串口的板子**（例如使用 USB-Serial/JTAG 的 ESP32-S3 或 ESP32-C3）在复位时端口会重新枚举。从复位时刻开始计时，端口一出现就开始抓取，并记下这段空档。空档期间打印的内容会丢失，所以面向这类板子的任务应该反复打印，而不是只打印一次。
- **抓取**时使用任务的 `baud`，写入日志文件，每行一条记录并带主机时间戳，并记录串口的 USB 序列号。在观测窗口结束后 10 秒内、不拔线的情况下，在同一个串口上运行芯片身份命令，把日志与芯片关联起来。
- **匹配**时先统一换行符，再逐行用 `pattern` 做正则匹配。在时间零点后的 `within_s` 内至少有 `min_matches` 行匹配、并且设置了 `max_matches` 时不超过该数，即通过。
- **带 `human_action` 的任务：** 该操作本应触发的那些行，在操作之前不得匹配。给这些断言加上 `after_human_action: true`。这个对照窗口能抓出"没有输入刺激也照样打印预期输出"的固件。

### `gpio_state`

- 把逻辑分析仪的一个通道接到 `pin`，并与板子共地。
- 采样率不低于任务所隐含的最快边沿速率的十倍；对于几千赫兹以下的信号，1 MHz 绰绰有余。
- 从时间零点起至少抓取 `within_s`，并保存原始抓包，例如 sigrok 的 `.sr` 文件。
- 对于 `expect: toggles`，统计窗口内的边沿数，不少于 `min_edges`、并且设置了 `max_edges` 时不超过该数，即通过。上限能抓出翻转速度远超要求的引脚。

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

每一次运行——包括自检和作废的运行——都产生一条记录。把它们和所引用的证据文件放在一起，提交这个目录，并添加一个覆盖其中每个文件的 `SHA256SUMS` 文件。

```yaml
run: 7
session: 2026-09-20-a
phase: pass                       # self-test | pass | ab-with | ab-without
task: 01-blink
skill: {repo: https://github.com/owner/skill, commit: 3f2a9c1}
eval_version: 0.1.0
board: esp32-c3-devkitm-1 ESP32-C3-MINI-1
chip_id: "30:ed:a0:88:88:a0"
serial_port: {device: /dev/ttyACM0, usb_serial: "30:ED:A0:88:88:A0"}
host: {os: Ubuntu 24.04, framework_version: "5.2.2", baseline: vm-snapshot-2026-09-20}
agent: {model: claude-opus-5, harness: claude-code 2.1.3, network: true, session_id: 1f7c..., hardware_access: shell}
supply_chain_scan: {tool: mcp-scan, result: clean}   # 每个 Skill commit 扫一次即可；每条记录重复引用
started: 2026-09-20T10:14:03Z
ended:   2026-09-20T10:21:47Z
agent_outcome: declared-done      # declared-done | timeout
skill_dir_sha256: {before: 5ac0..., after: 5ac0...}
skill_invoked: true
effort: {builds: 3, flashes: 2, first_build_ok: false, tokens_in: 184233, tokens_out: 9120, cost_usd: 2.41, wall_s: 464}
workdir_sha256: 9b1e...
build: {exit: 0, log: runs/07/build.log}
flash: {exit: 0, log: runs/07/flash.log, detected_chip: "ESP32-C3 (QFN32) (revision v0.4)"}
time_zero: 2026-09-20T10:22:15.402Z
human_actions: []                 # 例如 [{at: "+5.0s", action: "按下 GPIO39 上的按键"}]
reboot_guard: pass
assertions:
  - {type: compile_only, result: pass}
  - {type: serial_match, result: pass, matches: 6, evidence: runs/07/serial.log}
  - {type: gpio_state,   result: pass, edges: 12, evidence: runs/07/gpio5.sr}
result: pass                      # pass | fail | invalid
failure_class: null               # build | flash | crash | behaviour | timeout | tampered | illegitimate
invalid_reason: null
bench_damage: none                # none | recovered（方法） | debug-locked | efuse-burned
legitimacy_review: {by: tester, finding: "读取 tick 定时器；GPIO5 由同一任务驱动"}
transcript: {path: runs/07/transcript.jsonl, sha256: e40d...}
```

### 背书

用 **L2 hardware attestation** 表单开一个 issue。表单会要求填写：Skill 与提交、精确的板型与版本、芯片 ID、框架版本、Agent 模型与运行环境、每一次运行的结果、两次测试台自检、硬件证据、每次会话一张测试台照片，以及已提交运行记录的永久链接和其 `SHA256SUMS` 文件的 SHA-256。表单还要求确认：运行是在真实板子上进行的；每次运行都从主机基线启动，且 eval 不在 Agent 可触及的范围内；每一次运行都已报告；每一次通过的运行都做过正当性审查；没有给过额外提示；会话记录未经编辑。唯一允许的改动是把 API key、Wi-Fi 密码等机密替换为 `[REDACTED]`；公开前请先检查会话记录中是否含有这类内容。

## 审核

维护者在把背书记入 manifest 的 `verified.L2` 之前，会核对：

- 该包的 `eval_validated` 覆盖了被测的那个版本，包括 `spoof_caught`、`exploit_caught` 与 `leakage_reviewed`。
- 所有计入运行的会话，两次自检都通过了，且 eFuse 概要没有变化。
- 每次运行和每次自检中出现的 `chip_id` 都相同、与烧录工具报告的一致，并且不是已知的模拟器取值——Wokwi 模拟 ESP32 的默认 MAC `24:0a:c4:00:01:10`、全零 ID、Renode 中 nRF52840 的 `DEVICEADDR[0]` 值 `0xAABBCCDD`，或是在运行之间发生变化的 STM32 UID（Renode 的 STM32F4 Discovery 脚本就是这样）。
- 运行记录位于某个提交的永久链接下，且其 `SHA256SUMS` 与背书中填写的摘要一致。
- 每个任务的运行编号连续，按"最多三次中两次"的规则判定，作废的运行附有说明。
- **每个任务至少重新评分一次运行**：依据其原始证据——串口日志、`.sr` 抓包、`.pcapng`——确认能得出所记录的结果，包括重启保护。
- **每个任务至少完整阅读一次通过的运行**——会话记录与冻结源码——查找"审查每一次通过的运行"中列出的伪造迹象，并确认与测试者的 `legitimacy_review` 一致。
- 会话记录显示 prompt 是原文给出的、测试者没有提供帮助、Agent 没有读取 eval；已安装 Skill 前后的哈希一致。
- 记录了 `agent.hardware_access`，且阶段 3 两组使用的是同一种。

缺少上述任何一项的背书，会被退回并指明具体缺什么，而不是被默默拒绝。QEMU、Wokwi 和 Renode 都可以被配置成任意芯片 ID，所以这些检查能抓住的是粗心的、抄来的和重复的结果，而不是一个铁了心造假的人；针对后者的防线，是由 `×N` 统计的、在不同芯片上的独立复现。

## 预检：L0、触发与 L1

预检能在有人花一个下午坐到测试台前之前，先拦下问题。它们都不算通过。

### L0——静态检查

**可用。** 运行 `python scripts/l0_check.py skill path/to/my-skill`。它检查以下内容，并且只检查这些：

- `SKILL.md` 存在，其 YAML frontmatter 包含非空的 `name` 与 `description`，且 description 至少 80 个字符。
- `SKILL.md` 中没有形似 API 密钥或访问令牌的内容。
- `evals/manifest.yaml` 存在；`skill` 等于 frontmatter 中的 `name`；`simulator` 是已知 id；`assertions_supported` 中每一项都是已知类型；`target.board`、`target.framework` 与 `target.framework_version` 均已设置。
- `evals/tasks/` 中至少有一个任务；每个任务的 `id` 等于文件名主干，`level` 合法，`prompt` 非空，且设置了 `timeout_s`。
- 每条断言的 `type` 都是已知类型，且已在 `assertions_supported` 中声明。
- 整个包中至少有一条断言强于 `compile_only`。

它不检查断言字段、`build` 或 `flash` 块、fixtures、`eval_validated`、答案泄露，也不检查任何断言是否有可能失败。那些是阶段 0 的职责。

### 触发预检

**可用，人工执行。** 一个从不被加载的 Skill，在阶段 3 里测出来就是零；而它会不会被加载，只取决于它的 `description` 和用户的请求，与板子无关。所以可以先在主机上测。在 `evals/trigger_queries.json` 中写约 20 条请求，每条为 `{"query": ..., "should_trigger": true|false}`：8 到 10 条应当加载该 Skill，8 到 10 条是不应加载的近似请求，比如换一个芯片系列或换一个框架的同类任务。装上 Skill 后每条跑三次，统计加载的比例。`should_trigger: true` 的比例不低于 0.5、`false` 的比例低于 0.5，这条请求才算通过。结果记入 manifest 的 `trigger_eval`。这沿用了 agentskills.io 公布的调优 description 的方法。

`claude plugin eval` 可以跑这项预检：每条请求一个用例，用针对 `Skill` 的 `tool_used` 评分器，近似请求设 `min: 0, max: 0`。它的用例对 Agent 隐藏，并会加一个不装 Skill 的对照组，因此也适合跑主机侧的编译检查。它跑不了阶段 2：没有自定义代码评分器，观测不到板子，而它对 home 目录的沙箱通常还会把工具链挡在外面。把它的用例放在用 `--eval-dir` 指定的单独目录里，否则它会把结果写进 `evals/`。

### L1——模拟器预检

**尚未构建。** runner 将在模拟器中遵循阶段 2 的流程：把 prompt 交给 Agent、冻结结果、构建、把产物加载进声明的模拟器，并评估所有未标记 `l1_skippable` 的断言，`within_s` 以仿真时间计。它会复用各模拟器自带的断言层——Renode 的 `renode-test` 关键字（如 `Wait For Line On Uart`）、Wokwi 场景文件中的期望——而不是抓取控制台输出，并会报告跳过了多少条断言。一旦它与真实背书并行运行，将公布 L1 与 L2 结论一致的比例。一个过不了 L1 的任务不值得拿到测试台上；一个过了 L1 的任务仍然不算通过。

## 参考：eval 包

```
my-skill/
├── SKILL.md
└── evals/                        # 每次运行前从 Skill 中移除
    ├── manifest.yaml
    ├── tasks/
    │   ├── 01-easy-thing.yaml
    │   ├── 02-medium-thing.yaml
    │   └── 03-hard-thing.yaml
    ├── fixtures/
    │   └── <task-id>/
    │       ├── reference/        # 阶段 0 检查 1，以及阶段 1 自检
    │       ├── broken/           # 阶段 0 检查 3
    │       └── spoof/            # 阶段 0 检查 4
    └── trigger_queries.json      # 触发预检
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
| `boot_banner` | L2 需要 | 匹配每次启动恰好打印一次的那一行的正则表达式。时间零点之后第二次匹配即为重启。 |
| `reboot_patterns` | L2 需要 | 致命错误输出的正则表达式；时间零点之后任何一次匹配都判运行失败。ESP32 系列有默认值；其他系列自行定义。 |
| `eval_validated` | L2 必填 | 阶段 0 记录，包括 `exploit_caught`。没有它，背书不被接受。 |
| `trigger_eval` | 否 | 触发预检结果：`{date, model, runs_per_query, should_trigger: k/n, should_not_trigger: k/n}`。 |
| `sequential_plan` | 否 | 若阶段 3 会提前停止，事先登记的错误率与每组最大运行次数。 |
| `verified.L0` | 否 | `l0_check.py` 通过后填写 `{date, run}`。 |
| `verified.L1` | 保留 | 由 L1 runner 写入。 |
| `verified.L2` | 否 | 被接受的背书，由维护者添加。 |
| `ab.*` | 否 | 阶段 3 结果：每组的 `k/n`，以及附区间与标签的 `ΔPass`。 |

### 任务文件

`tasks/` 中每个任务一个文件；文件名主干必须等于 `id`。

| 字段 | 必填 | 含义 |
|---|---|---|
| `id` | 是 | 等于文件名主干；加数字前缀，让任务按难度排序。 |
| `level` | 是 | `easy`、`medium` 或 `hard`。 |
| `timeout_s` | 是 | Agent 尝试的挂钟时间预算。 |
| `prompt` | 是 | 告诉 Agent 的全部内容，包括断言匹配的每一个取值。 |
| `build.cmd`、`build.cwd` | 否 | 在冻结副本上运行的构建命令。 |
| `flash.cmd` | 否 | 烧录命令；`{port}` 会被替换为板子的端口。默认使用工具链的标准烧录命令。 |
| `human_action` | 否 | 测试者需要执行的物理操作及时间，例如 `时间零点后 5 秒按一次 GPIO39 上的按键`。会在该操作之前开启一个对照窗口。 |
| `expect_reset` | 否 | 若任务本身会合理地复位板子，设为 `true`，此时对该任务禁用重启保护。 |
| `assertions` | 是 | 全部通过，本次运行才通过。 |
| `fixtures` | 否 | 参考输出的路径，例如预期的串口日志。 |

### 断言类型

当模拟器无法评估某条断言时，可以设置 `l1_skippable: true`。这只影响 L1：在真实板子上，每条断言都会被评估。

| 类型 | 观测对象 | 字段 |
|---|---|---|
| `compile_only` | `build.cmd` 以 0 退出 | 无 |
| `serial_match` | UART 输出 | `baud`、`pattern`（正则表达式，逐行）、`min_matches`、`within_s`，可选 `max_matches` 与 `after_human_action` |
| `gpio_state` | 引脚电平随时间的变化 | `pin`、`expect`（如 `toggles`）、`min_edges`、`within_s`，可选 `max_edges` |
| `bus_capture` | 总线上的通信 | `bus`（如 `ble`）、`expect`（与总线相关，如 `adv_name`、`service_uuid`、`char_uuid`、`notify_count_min`、`within_s`） |
| `exit_code` | 脚本的结果 | `cmd`、`expect` |
| `network_probe`、`ros_topic`、`file_exists` | —— | 保留；由第一个需要它的包来定义 |

单独一个 `compile_only` 对硬件几乎证明不了什么，所以每个包至少需要一条比它更强的断言。只要存在可用的运行时观测，就优先使用它而不是 `exit_code`；`exit_code` 用于那些任何观测都抓不到的性质，比如"一个恰好没把板子搞坏的违禁调用确实没有出现"。

## 实例

[fxp/m5stack-embedded-dev-skill](https://github.com/fxp/m5stack-embedded-dev-skill) 面向使用 Arduino 与 M5Unified 的 M5Stack Core2，是列表中第一个带 eval 包的 Skill。对照本方案：

- **包的形态——良好。** 三个任务分属三个难度；FQBN 精确；声明了 `simulator: none` 并说明原因；断言观测的是串口输出，而不是对代码做判断。
- **答案泄露——通过。** 它的参考资料写明 Core2 的 AXP192 在 `0x34` 应答、`M5.begin()` 已经接管了 I2C 总线。这些是关于芯片的知识，正是 Skill 该有的内容；其中没有出现任何任务的输出格式或解题代码。
- **阶段 0——尚未完成。** 没有 `reference/`、`broken/` 或 `spoof/` 方案，也没有 `eval_validated` 记录。如果做了，它会抓出两个缺陷：任务 02 的 `exit_code` 在空工程上通过（检查 2），任务 03 的 `exit_code` 会放过一个没写 `IRAM_ATTR` 的阻塞式处理函数（检查 3）。两处修复各只需一行，写法见上面阶段 0 一节。
- **阶段 2——需要补 `human_action`，并真正断电。** 任务 03 的串口断言要等待 GPIO39 上的按键操作，但任务没有说明什么时候按；加上 `human_action: 时间零点后 5 秒按一次 GPIO39 上的按键`，运行才可复现，并且获得一个对照窗口。另外，Core2 靠内置电池运行，所以第 2 步的"断电"意味着长按电源键 6 秒，而不是拔掉 USB。
- **状态：`L0`。未通过。** 通往通过的路径是：先由作者完成阶段 0，再由任何拥有 Core2 的人在板子上运行。

## 本方案的依据

- [METR，*Recent frontier models are reward hacking*](https://metr.org/blog/2025-06-05-recent-reward-hacking/)——Agent 会读取评分器和泄露的解法；这是让 eval 远离 Agent 的原因。
- [METR，*Frontier Risk Report*](https://metr.org/blog/2026-05-19-frontier-risk-report/)（2026 年 5 月）——测试被隐藏时作弊依然存在，长任务中至少 16% 的成功运行经审查不正当；这是审查每一次通过运行的原因。
- [Anthropic，*Demystifying evals for AI agents*](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)（2026 年 1 月）——隔离的试验、Agent 读取之前试验的 git 历史，以及在一致性重要时使用 pass^k。
- [METR，*OpenAI / Hugging Face hacking incident investigation*](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/)（2026 年 8 月）与 [UK AISI，*Incident report*](https://www.aisi.gov.uk/blog/incident-report-unsanctioned-agent-behaviour-during-cyber-testing)（2026 年 8 月）——伪造的会话记录、充当隐蔽信道的共享缓存，以及在真实互联网上行动的 Agent；这是"通过"以测试台证据为准、板子放在隔离网络上的原因。
- [How Much Coordination Gain Is Real?](https://arxiv.org/abs/2606.20695)——配对噪声底方案；A/A 对照的依据。
- [SkillsBench](https://arxiv.org/abs/2602.12670v4)（v4，2026 年 6 月）——大规模的 Skill 评测：用自动门禁拒绝泄露任务解法的 Skill、只在 Skill 真正被调用时才计入试验、模型自己生成的 Skill 得分反而低于不装 Skill，以及按任务配对计算差值。
- [Terminal-Bench 2.0](https://arxiv.org/abs/2601.11868)——必须通过的标准解法、必须失败的空 Agent，以及无论是否得逞都要阅读其轨迹的对抗性作弊 Agent；阶段 0 检查 1、2、5 以此为蓝本。
- [τ-bench](https://arxiv.org/abs/2406.12045) 与 [Towards a Science of AI Agent Reliability](https://arxiv.org/abs/2602.16666)——作为可靠性指标、区别于 pass@k 的 pass^k。
- [Establishing Best Practices for Building Rigorous Agentic Benchmarks](https://arxiv.org/abs/2507.02825)——Agentic Benchmark Checklist，其中包括把空回复计为成功的基准测试。
- [Adding Error Bars to Evals](https://www.anthropic.com/research/statistical-approach-to-model-evals) 与 [Don't Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints](https://arxiv.org/abs/2503.01747)——为什么结果要附区间，以及为什么小样本区间不能用正态近似。
- [Is Your Imitation Learning Policy Better than Mine?](https://arxiv.org/abs/2503.10966)——STEP，在预设错误率与最大试验次数下比较两个策略的序贯检验。
- [IoT-SkillsBench](https://arxiv.org/abs/2603.19583)——单次生成固件、在真实板子上由人工验证；专家编写的 Skill 有帮助，模型自生成的没有。
- [Embedded Arena](https://arxiv.org/abs/2606.16190)——在真实微控制器上的硬件闭环，其中 Agent 硬编码 UART 输出、并在过程中锁死了一块板子；这是检查 5、运行审查和 `bench_damage` 的证据。
- [agentic-hil](https://github.com/agentic-hil/agentic-hil)——一个硬件在环工具：配置放在 Agent 工作区之外，在允许原始调试器命令或整片擦除时拒绝烧录，并把每一次硬件操作写入 SHA-256 审计链。
- [Snyk，*ToxicSkills*](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/) 与 [agentskills.io 关于优化 description 的指南](https://agentskills.io/skill-creation/optimizing-descriptions)——供应链扫描与触发预检的依据。
- [Claude Code plugin evals](https://code.claude.com/docs/en/plugin-evals)——内置评测工具能为本方案做什么、不能做什么。
- [esptool](https://docs.espressif.com/projects/esptool/en/latest/esp32/esptool/basic-commands.html)、[M5Stack Core2](https://docs.m5stack.com/en/core/core2)、[Wokwi ESP32](https://docs.wokwi.com/guides/esp32) 与 [Renode nRF52840](https://github.com/renode/renode/blob/master/platforms/cpus/nrf52840.repl)——复位流程与模拟器 ID 检查背后的具体事实。

## 扩展本方案

要新增一个模拟器 id 或一种断言类型，请提交一个 PR，并做到以下几点：

1. 把它加进 `scripts/l0_check.py` 中的 `SIMULATORS` 或 `ASSERTION_TYPES`。
2. 如果是断言类型，在断言表中加一行，在"在真实板子上测量每种断言"一节下补充测量方法，把所需仪器加进测试台表格——并说明它如何会失败，以及对它的伪造会如何被抓住。
3. 如果是模拟器，把它加进 README 的验证基础设施一节。
4. 同步更新 `EVALS.zh-CN.md`，或者让 `translation-sync` job 保持失败，由维护者修复。
