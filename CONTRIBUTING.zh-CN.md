# 贡献指南

*[English](CONTRIBUTING.md) · 简体中文*

> 本文档译自 [CONTRIBUTING.md](CONTRIBUTING.md)。如两者有出入，以英文版为准。

## 从哪里开始

如果你想动手做东西，而不只是整理清单，[GAPS.zh-CN.md](GAPS.zh-CN.md) 列出了目前缺失的方向，附有证据和五个范围明确的首次贡献建议。补上其中一项并把它收录进来，是你能提交的最有价值的 PR。

如果你发现了与某条"空白"相矛盾的东西，同样欢迎：在同一个 PR 里把它移进 README，并修改对应的空白条目。

## 向列表添加条目

每个条目一行，放进正确的分类。同一分类内按维护者判断的有用程度排序，而非星数——一个恰好包含一个小 Skill 的 1.5 万星 monorepo，不应该排在一个专注的 50 星 Skill 前面。格式：

```
- [名称](https://github.com/owner/repo) - 一句话描述，英文版须首字母大写、以句号结尾。(标签 · ★星数 · YYYY-MM)
```

末尾括号中的标签：`official`（仓库位于厂商自己的组织下）、`coll`（多个 Skill 的合集）、`cursor-rules`、`placeholder`、`stale since YYYY-MM`。星数以千计时用 `k` 表示。

提交 PR 前请运行 `python scripts/l0_check.py readme README.md`；如果改动了 `GAPS.md`，再运行 `python scripts/l0_check.py links GAPS.md`。CI 会执行同样的检查，并每周扫描一次失效链接。维护者用 `python scripts/refresh_meta.py`（需要已登录的 `gh`）刷新星数和最近推送时间：它会把 12 个月没有推送的条目标为 `stale since YYYY-MM`、跟随仓库改名，并报告已消失的仓库；之后运行 `python scripts/gen_catalog.py` 重建 `CATALOG.md` 中的表格。

本列表同时有简体中文版 [README.zh-CN.md](README.zh-CN.md)，CI 会检查两份文件是否以相同顺序收录了相同的条目。如果你能读中文，请在对应位置加上翻译后的那一行；如果不能，只改 `README.md` 即可——此时 `translation-sync` 这个 job 会失败，这是预期行为，维护者会补上译文。`GAPS.md` 与本文件同理，它们的译文分别是 [GAPS.zh-CN.md](GAPS.zh-CN.md) 和本文件。

收录的基本门槛：

- 有真实的 README，并且用户今天就能安装或运行。不收"即将推出"的东西。
- 没有被弃置：过去 12 个月内至少有一次推送，除非它是某个硬件类别下唯一的选择。
- 对 Skill（SKILL.md 形式）而言：description 必须具体到能够稳定触发——一句光秃秃的"帮你搞定 ESP32"不合格。

## 添加 evals 包

**Skills** 各分类中的条目可以带验证徽章——`L0`、`L1`、`L2 ×N`、`ΔPass`——方法是在 Skill 内部提供一个 `evals/` 包。只有 `L2`——在真实板子上运行——才表示这个 Skill 已通过；`L0` 和 `L1` 都只是预检。完整测试方案见 **[EVALS.zh-CN.md](EVALS.zh-CN.md)**：阶段 0 到 3 的步骤、每种断言在真实板子上怎么测、运行记录格式、审核标准，以及包格式参考。

简短版本：

1. 把 [`template/evals/`](template/evals/) 复制到你的 Skill 中，填写 `manifest.yaml`——或者安装 [hardware-skill-creator](skills/hardware-skill-creator/)：这是一个 Agent Skill，会生成包的脚手架、检查它，并带着你和你的 agent 走完下面每一步。
2. 写大约三个任务——简单、中等、困难——其断言观测物理副作用，并且至少有一条强于 `compile_only`。
3. 运行 `python scripts/l0_check.py skill path/to/skill`，直到通过。
4. **阶段 0——验证 eval。** 为每个任务在 `evals/fixtures/<task-id>/` 下添加 `reference/`、`broken/` 与 `spoof/` 三份方案，并在板子上证明：参考方案通过、空工程上每条断言都失败、错误方案与伪造固件都被抓住、被要求作弊的 Agent 也被抓住。确认 Skill 中不含任何任务的答案。把结果记为 manifest 中的 `eval_validated`。再添加 `evals/trigger_queries.json` 用于触发预检，这一步不需要板子。
5. **阶段 1–2——通过判定运行。** 在两次通过的测试台自检之间，让每个任务在真实板子上运行——或者请有这块板子的人来跑——每次运行前都安装**不带** `evals/` 的 Skill、把主机恢复到基线、并完全复位板子，审查每一次通过的运行有没有伪造工作，然后附上全部运行记录，提交一个 **L2 hardware attestation** issue。一个任务在最多三次运行中有两次通过即算通过；在每个任务都通过之前，这个 Skill 都不算通过。

没有 `evals/` 包的 Skill 仍然可以被收录，只是不显示徽章。

## 提交测试结果

结果以两部分提交：保存在 git 中的证据，加上一份可供维护者审核的声明。

1. **阶段 0**，由 Skill 作者提交：把 fixtures 和阶段 0 日志提交到 Skill 的仓库，并把该提交的永久链接填进 `eval_validated.evidence`。
2. **板上运行**，任何人都可以提交：把每次运行的记录、日志、抓包文件和对话记录连同 `SHA256SUMS` 文件提交到你能控制的仓库，然后开一个 **L2 hardware attestation** issue，附上提交的永久链接和 `SHA256SUMS` 的摘要。公开前把对话记录中的机密替换为 `[REDACTED]`，不要做其他改动。
3. **徽章**，由维护者更新：接受背书后，维护者会发 Pull Request 更新两个 README 中该条目的徽章。请不要在你自己的 Pull Request 里修改徽章。

逐步的命令（包括发 Pull Request 用的 `gh` 命令）见 [hardware-skill-creator 的 README](skills/hardware-skill-creator/README.zh-CN.md#提交结果)。

## 添加新的模拟器或断言类型

见 [EVALS.zh-CN.md](EVALS.zh-CN.md) 的最后一节。
