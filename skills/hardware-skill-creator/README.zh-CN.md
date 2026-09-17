# hardware-skill-creator

*[English](README.md) · 简体中文*

一个 Agent Skill，帮助硬件开发者为某块板子、某个 SDK 或某台仪器编写自己的 Skill，并配上一个在真实板子上证明其有效的 eval 包。它对硬件做的事，相当于 Claude 的 [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) 对通用 Skill 做的事，遵循的是 [EVALS.zh-CN.md](../../EVALS.zh-CN.md) 中的测试方案。

它坚持的规则是：**只有任务在真实板子上运行、并且每条断言都成立，Skill 才算通过。**

## 它会和你一起做什么

1. 确认准确的板子型号、版本、框架版本、手头的测量仪器，以及模型在这块板子上常犯的错误。
2. 围绕模型会搞错的事实起草 SKILL.md，同时不把任务答案写进去。
3. 设计三个任务（简单、中等、困难），每个任务围绕一个错误，断言都是板子能呈现出来的现象。
4. 生成包的脚手架，编写 reference、broken 和 spoof 三份 fixture。
5. 运行静态检查，包括 L0 看不到的缺陷。
6. 和你一起在板子上完成阶段 0：reference 通过，空工程失败，broken 和 spoof 被抓住。
7. 用开发性运行改进 Skill，然后指导测试台运行、L2 背书和 ΔPass 统计。

## 安装

把这个 Skill 去掉它自己的 `evals/` 后，复制到你的 agent 的 skills 目录。以 Claude Code 为例：

```bash
rsync -a --exclude evals skills/hardware-skill-creator ~/.claude/skills/
```

然后用你自己的话提出需求，例如"把我关于 Core2 电源芯片的笔记做成一个带 eval 的 Skill"。脚本需要 Python 3.9+ 和 `pyyaml`，串口抓取还需要 `pyserial`。

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/init_skill.py` | 为 `esp32`、`nrf52`、`stm32`、`rp2040` 或 `other` 生成 Skill 和 eval 包的脚手架 |
| `scripts/check_package.py` | 执行 L0 不做的检查：残留 TODO、prompt 中的取值、fixtures、空转命令、泄漏提示 |
| `scripts/l0_check.py` | 本仓库 L0 检查器的副本；CI 保证两者一致 |
| `scripts/bench.py` | 不带 `evals/` 安装、计算哈希、冻结工作目录、抓取串口、评估串口断言与重启保护 |
| `scripts/stats.py` | 三取二任务判定、Wilson 区间、带 Newcombe 区间的 ΔPass |

仓库根目录的 `scripts/test_skill_creator.py` 在 CI 中测试这些脚本。

## 状态

这个 Skill 在 `evals/` 里有自己的 eval 包：在 ESP32-C3-DevKitM-1 上的三个任务，agent 必须产出一个包，并且包里的 reference 固件要在板子上真正工作。它的阶段 0 还没有做。当前状态是 `L0`，尚未通过。
