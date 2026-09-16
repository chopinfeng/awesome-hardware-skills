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

提交 PR 前请运行 `python scripts/l0_check.py readme README.md`；如果改动了 `GAPS.md`，再运行 `python scripts/l0_check.py links GAPS.md`。CI 会执行同样的检查，并每周扫描一次失效链接。

本列表同时有简体中文版 [README.zh-CN.md](README.zh-CN.md)，CI 会检查两份文件是否以相同顺序收录了相同的条目。如果你能读中文，请在对应位置加上翻译后的那一行；如果不能，只改 `README.md` 即可——此时 `translation-sync` 这个 job 会失败，这是预期行为，维护者会补上译文。`GAPS.md` 与本文件同理，它们的译文分别是 [GAPS.zh-CN.md](GAPS.zh-CN.md) 和本文件。

收录的基本门槛：

- 有真实的 README，并且用户今天就能安装或运行。不收"即将推出"的东西。
- 没有被弃置：过去 12 个月内至少有一次推送，除非它是某个硬件类别下唯一的选择。
- 对 Skill（SKILL.md 形式）而言：description 必须具体到能够稳定触发——一句光秃秃的"帮你搞定 ESP32"不合格。

## 验证徽章

**Skills** 各分类中的条目会带一个徽章，表示其 `evals/` 包被验证到了哪一级：

| 徽章 | 含义 |
|---|---|
| `L0` | 静态检查通过：frontmatter、description 长度、不含密钥、链接可达、evals 包结构正确。 |
| `L1 (wokwi)` | 所有任务都在指定模拟器中通过，由本仓库 CI 运行。即将推出。 |
| `L2 ×3` | 三位互不相关的人在真实硬件上跑完了这些任务，并提交了附带会话记录的背书。 |
| `ΔPass +42%` | 同一批任务、同一模型下，装了 Skill 与不装 Skill 的通过率之差。即将推出。 |
| `stale` | 90 天内没有重跑 L1，或上游 12 个月没有推送。 |

没有 `evals/` 包的 Skill 仍然可以被收录，只是不显示徽章。要添加一个，把 [`template/evals/`](template/evals/) 复制到 Skill 中，填写 `manifest.yaml`，并至少写一个断言强于 `compile_only` 的任务。运行 `python scripts/l0_check.py skill path/to/skill` 即可知道这个包的结构是否正确。

### 如何写好任务

- prompt 是 Agent 能看到的**唯一**信息。如果一个人需要提示才能完成，说明任务描述不充分。
- 断言要针对脚本可观测的物理副作用：串口输出、GPIO 跳变、总线抓包、ROS topic、HTTP 探测。绝不能是"代码看起来对"。
- 需要真实硬件的断言（BLE 嗅探器、实体传感器）请标记 `l1_skippable: true`，这样 L1 仍能跑其余部分。
- 三个任务——简单 / 中等 / 困难——是最合适的数量。一个任务说明不了泛化能力；十个任务做 A/B 对比又太贵。

### 提交 L2 实测背书

用 **L2 hardware attestation** 模板开一个 issue。只有附带未经编辑的完整会话记录链接的背书才会被接受；之后由维护者将其追加到该 Skill 的 `manifest.yaml` 中 `verified.L2` 之下。

### A/B 对照

即将推出。runner 就绪后，`ΔPass` 将这样得出：每个任务对同一模型跑两次，一次装上 Skill，一次移除 Skill、只把 SKILL.md 的 `description` 换成一句泛泛的描述。如果一个 Skill 没能让通过率或首次编译成功率提升至少 15 个百分点，就会被标记为 `low-gain`——它很可能只是在复述模型已经知道的东西，维护者会追问它到底打算承载哪些非显而易见的知识。

## 添加新的模拟器或断言类型

模拟器 id 与断言类型都枚举在 `scripts/l0_check.py` 中。如需新增，请提交一个 PR 扩展这些集合，并在 `README.md` 的 **Verification infrastructure** 一节下补充一小段，说明 runner 如何驱动它。
