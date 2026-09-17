# hardware-skill-creator

*[English](README.md) · 简体中文*

一个 Agent Skill，帮助硬件开发者为某块板子、某个 SDK 或某台仪器编写自己的 Skill，并配上一个在真实板子上证明其有效的 eval 包。它对硬件做的事，相当于 Claude 的 [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) 对通用 Skill 做的事，遵循的是 [EVALS.zh-CN.md](../../EVALS.zh-CN.md) 中的测试方案。

它坚持的规则是：**只有任务在真实板子上运行、并且每条断言都成立，Skill 才算通过。**

## 安装

**Claude Code，以插件方式安装。** 本仓库就是一个插件市场。在 Claude Code 中输入：

```
/plugin marketplace add chopinfeng/awesome-hardware-skills
/plugin install hardware-skill-creator@awesome-hardware-skills
```

在终端里做同样的事：

```bash
claude plugin marketplace add chopinfeng/awesome-hardware-skills
claude plugin install hardware-skill-creator@awesome-hardware-skills
```

以后更新：先运行 `claude plugin marketplace update awesome-hardware-skills`，再运行 `claude plugin update hardware-skill-creator@awesome-hardware-skills`。

**任何读取 SKILL.md 目录的 agent**，直接复制目录即可：

```bash
git clone https://github.com/chopinfeng/awesome-hardware-skills
rsync -a --exclude evals awesome-hardware-skills/skills/hardware-skill-creator ~/.claude/skills/
```

把目标路径换成你的 agent 的 skills 目录。`evals/` 是这个 Skill 自己的测试，日常使用不需要。

**依赖。** 脚本需要 Python 3.9+ 和 `pyyaml`，串口抓取需要 `pyserial`，另外 `PATH` 上要有你板子的工具链（ESP-IDF、arduino-cli、west 等）。

## 使用

用你自己的话提需求就行。Skill 会判断你处在哪个阶段，从那里接着往下走。

| 你手上有 | 可以这样说 |
|---|---|
| 经验，还没有 Skill | "把我关于 M5Stack Core2 电源芯片的笔记做成一个带 eval 的 Skill。" |
| 一个没有 eval 的 Skill | "给 `./my-esp32-skill` 加一个针对 ESP32-S3-DevKitC-1 的 eval 包。" |
| 一个 eval 包 | "检查 `./my-skill/evals` 里的断言是否真的会失败。" |
| 桌上有块板子 | "在 /dev/ttyUSB0 上的板子上跑任务 02 的阶段 0。" |
| 测试已经跑完 | "根据这些运行记录算出任务判定和 ΔPass。" |

一次典型的会话：

1. **确定目标。** 你给出准确的板子、框架版本、测量仪器，以及模型在这块板子上常犯的错误。
2. **编写 Skill。** agent 起草 SKILL.md 和 `references/`，写的是关于器件的事实，不写任务答案。
3. **设计任务。** 它围绕这些错误提出三个任务，断言都是板子能呈现的现象。由你确认。
4. **生成包。** 它生成 `evals/` 脚手架，并为每个任务编写 reference、broken 和 spoof 固件。
5. **静态检查。** L0，加上 L0 做不到的检查，比如在空工程上也会通过的断言。
6. **在板子上做阶段 0。** 它先问清哪个端口是测试板，再逐个烧录 fixture，和你一起评估断言。逻辑分析仪、抓包器和按键操作由你动手。
7. **改进与测试。** 开发性运行暴露 Skill 的薄弱处；阶段 1–3 的测试台运行给出结论。

不经过 agent，也可以直接使用脚本：

```bash
S=skills/hardware-skill-creator/scripts
python $S/init_skill.py my-skill --board esp32-c3-devkitm-1 --framework esp-idf --framework-version 5.2 \
    --family esp32 --toolchain idf.py --task-ids toggle,boot-button,isr-count --out .
python $S/check_package.py my-skill --run-empty
python $S/bench.py capture --port /dev/ttyUSB0 --seconds 15 --out run.log --reset rts
python $S/bench.py serial run.log my-skill/evals/tasks/01-toggle.yaml --manifest my-skill/evals/manifest.yaml
python $S/stats.py delta 12 15 6 15
```

## 提交结果

提交分三类，去的地方不同。证据始终保存在某个 git 提交里，任何人以后都能按哈希核对。

| 提交什么 | 谁提交 | 提交到哪里 |
|---|---|---|
| 带 eval 包的 Skill | Skill 作者 | 向本列表发 Pull Request，添加条目 |
| 阶段 0 验证 | Skill 作者 | Skill 自己仓库里的一个提交 |
| 在板子上的测试运行（L2） | 任何拥有这块板子的人 | 记录放进一个 git 仓库，再到本仓库开背书 issue |

### 1. 收录你的 Skill（Pull Request）

```bash
gh repo fork chopinfeng/awesome-hardware-skills --clone
cd awesome-hardware-skills
git checkout -b add-my-skill
# 按 CONTRIBUTING.zh-CN.md 给出的格式，在 README.md 的对应分类里加一行。
# 如果你读中文，在 README.zh-CN.md 的相同位置加上翻译后的那一行。
python scripts/l0_check.py readme README.md
python scripts/l0_check.py skill /path/to/my-skill
git commit -am "Add my-skill"
git push -u origin add-my-skill
gh pr create --repo chopinfeng/awesome-hardware-skills --title "Add my-skill" \
    --body "Skill with an evals/ package. L0 passes locally. Phase 0: not yet done / done at <permalink>."
```

新收录的 Skill 状态是 `L0`。在背书被接受之前，它都不算通过。

### 2. 记录阶段 0（Skill 仓库里的提交）

把 fixtures 和阶段 0 的证据（串口日志、抓包文件、烧录工具输出）提交到你 Skill 的仓库，例如放在 `evals/phase0/<eval-version>/` 下。把这个提交的永久链接填进 `eval_validated.evidence`，再提交一次。永久链接里是提交的 SHA，不是分支名：

```
https://github.com/<you>/<skill-repo>/tree/<commit-sha>/evals/phase0/0.1.0
```

如果 Skill 已经被收录，就在这里发一个 Pull Request，在条目描述中注明已完成阶段 0。

### 3. 提交在板子上的测试运行（先存记录，再开背书 issue）

1. **把记录存进你能控制的仓库。** Fork 这个 Skill 的仓库，或者用你自己的任意仓库。一次会话的文件放在同一个目录里：每次运行一份运行记录（模板见 `assets/run-record.yaml`），以及编译和烧录日志、串口日志、`.sr` 和 `.pcapng` 抓包文件、测试台照片和 agent 对话记录。

   ```
   evals/runs/2026-09-20-esp32-c3-devkitm-1-<your-github-name>/
   ├── runs/01/record.yaml  build.log  flash.log  serial.log  gpio5.sr  transcript.jsonl
   ├── runs/02/...
   ├── self-test-start/ and self-test-end/
   └── bench.jpg
   ```

2. **公开前检查对话记录。** 里面可能有 API key、token、Wi-Fi 密码、用户目录路径等隐私数据。把机密替换成 `[REDACTED]`，并在 issue 里说明；除此之外的任何改动都会让对话记录失去证据效力。

3. **计算哈希、提交并推送。**

   ```bash
   cd evals/runs/2026-09-20-esp32-c3-devkitm-1-<you>
   find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 shasum -a 256 > SHA256SUMS
   shasum -a 256 SHA256SUMS            # 这个摘要填进 issue
   git add . && git commit -m "L2 runs: esp32-c3-devkitm-1, 2026-09-20" && git push
   git rev-parse HEAD                  # 这个 SHA 用于永久链接
   ```

4. **开背书 issue**：<https://github.com/chopinfeng/awesome-hardware-skills/issues/new?template=attestation.yml>。表单会要求填写：被测 Skill 与提交、板子、芯片 ID、版本、按顺序列出的每次运行及结果、自检、硬件证据、照片、记录的永久链接和 `SHA256SUMS` 摘要。表单要的数字可以用本 Skill 的 `stats.py task` 和 `stats.py wilson` 算出来。

5. **可选：向 Skill 的仓库发一个 Pull Request**，把你的记录目录加进去，让作者也保留一份。

之后的流程：维护者按 EVALS.zh-CN.md 中的清单审核 issue，用你的原始文件为每个任务至少重新评分一次运行，缺什么会提出来。被接受后，维护者会在本仓库发 Pull Request 更新条目徽章（例如 `L2 ×1`；如果你做了阶段 3，还有 `ΔPass`），并请 Skill 作者把这次背书追加到 manifest 的 `verified.L2`。测试者不需要自己修改徽章。

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/init_skill.py` | 为 `esp32`、`nrf52`、`stm32`、`rp2040` 或 `other` 生成 Skill 和 eval 包的脚手架 |
| `scripts/check_package.py` | 执行 L0 不做的检查：残留 TODO、prompt 中的取值、fixtures、空转或无法运行的命令、泄漏提示 |
| `scripts/l0_check.py` | 本仓库 L0 检查器的副本；CI 保证两者一致 |
| `scripts/bench.py` | 不带 `evals/` 安装、计算哈希、冻结工作目录、抓取串口、评估串口断言与重启保护 |
| `scripts/stats.py` | 三取二任务判定、Wilson 区间、带 Newcombe 区间的 ΔPass |

仓库根目录的 `scripts/test_skill_creator.py` 在 CI 中测试这些脚本。

## 状态

这个 Skill 在 `evals/` 里有自己的 eval 包：在 ESP32-C3-DevKitM-1 上的三个任务，agent 必须产出一个包，并且包里的 reference 固件要在板子上真正工作。它的阶段 0 还没有做。当前状态是 `L0`，尚未通过。
