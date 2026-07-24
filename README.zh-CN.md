# ResearchFigureSkill

> 一个“证据锁定”的科研视觉编译器：输入论文证据，输出可审计的科研图形契约。

[English](README.md) · [市场调研](docs/MARKET_LANDSCAPE_2026.md) · [验证报告](docs/VALIDATION_REPORT.md) · [版本记录](CHANGELOG.md) · [贡献指南](CONTRIBUTING.md)

ResearchFigureSkill 的重点不是让模型更快地画出一张“漂亮科研图”，而是先回答：

1. 这张图在论文里承担什么科学职能？
2. 读者 5 秒内应该理解什么？
3. 每一个视觉命题由论文哪里支持？
4. 箭头到底表示数据流、时间、相关、因果、反馈还是包含？
5. 哪些内容不能进入图中？
6. 应该使用 SVG、数据绘图、图像生成，还是混合装配？
7. 最终图片是否真的表达了正确科学叙事？

## 核心流程

```text
论文 / brief / 数据 / 旧图
→ Source grounding
→ Claim–evidence ledger
→ Figure portfolio 与角色选择
→ FigureSpec 1.0
→ 渲染后端路由
→ 真实产物
→ 科学、结构、视觉与技术审计
→ 最小修改 delta
→ 可编辑源文件 + 预览 + provenance
```

它覆盖 motivation、method/pipeline、mechanism、experiment、ablation、comparison、taxonomy、graphical abstract，以及有明确主角色的多 panel 混合图。

## 与常见方案的区别

| 常见方案 | ResearchFigureSkill |
|---|---|
| 论文全文直接变成长 Prompt | 先做证据定位、图形决策和结构化中间表示 |
| 依赖“Nature 风格、专业、简洁”等形容词 | 科学论证为主，视觉风格只是最后一层 |
| 所有箭头一种含义 | typed edge + claim ID + 证据范围 |
| 一种模型画所有图 | vector / plot / image / hybrid 风险路由 |
| 用总体美观分抵消局部错误 | 科学硬错误一票否决 |
| 每轮整张图重新抽卡 | 稳定 ID + 局部 revision delta |
| 最后只留下 PNG | spec、prompt、可编辑源文件、audit、provenance |

## Prompt Engineering 核心资产

项目不是维护十几份互相重复的完整 Prompt，而是一个有版本的编译链：

```text
RF-GROUND-1.0
→ RF-DECIDE-1.0
→ RF-SPECIFY-1.0
→ RF-COMPILE-1.0
→ renderer adapter
→ RF-CRITIQUE-1.0
→ RF-PATCH-1.0
```

每一阶段都有：

- 明确输入；
- 结构化输出；
- 禁止行为；
- 缺失证据时的失败行为；
- 可自动测试的验收项。

完整模板见 [`prompt-system.md`](skills/research-figure/references/prompt-system.md)。

## FigureSpec

FigureSpec 是论文分析与绘图工具之间的事实源，包含：

- 目标读者、媒介、尺寸和可编辑性；
- reader question、five-second message 和 claim boundary；
- claim 状态、范围、证据和 source anchor；
- 必须出现、可选和禁止内容；
- panel、entity、typed relation、阅读顺序和视觉层级；
- renderer、数据来源、精确文字和数值要求；
- 科学与结构验收阈值。

校验器能够发现：

- supported claim 没有证据锚点；
- missing claim 被放入成品 panel；
- hypothesis 没有在图上明确标注；
- 箭头端点不存在；
- 因果箭头没有 supported causal claim；
- experiment / ablation 被错误路由到图像生成；
- 数据图没有 machine-readable data source。

## 安装

```bash
git clone <你的仓库地址> ResearchFigureSkill
cp -R ResearchFigureSkill/skills/research-figure ~/.codex/skills/research-figure
```

随后可显式调用 `$research-figure`，也可由 Codex 根据科研绘图任务自动触发。

## 使用示例

```text
用 $research-figure 分析这篇论文的 Figure 1 应该是 motivation 还是
method overview。先输出证据锚点、reader question 和 FigureSpec，不要立刻画图。
```

```text
用 $research-figure 审计这张机制图。先列出普通读者会从图中推断出的
命题，再检查箭头是否把相关性夸大成因果，并给出最小修改 delta。
```

```text
用 $research-figure 把实验数据做成论文图。数值、误差棒和坐标必须由
数据代码生成，图像模型只能用于非证据性的插画元素。
```

## 命令行工作台

```bash
SKILL_ROOT="./skills/research-figure"

python "$SKILL_ROOT/scripts/figure_workbench.py" \
  new --role method --out figure-spec.json

python "$SKILL_ROOT/scripts/figure_workbench.py" \
  validate figure-spec.json --strict

python "$SKILL_ROOT/scripts/figure_workbench.py" \
  validate-artifact --kind evidence-ledger evidence-ledger.json --strict

python "$SKILL_ROOT/scripts/figure_workbench.py" \
  compile figure-spec.json --out final-prompt.md

python "$SKILL_ROOT/scripts/figure_workbench.py" \
  audit-template figure-spec.json --out figure-audit.json

python "$SKILL_ROOT/scripts/figure_workbench.py" \
  validate-artifact --kind figure-audit figure-audit.json --spec figure-spec.json
```

该脚本只依赖 Python 3.9+ 标准库。同一个有效 FigureSpec 会稳定编译出同一个 Prompt。

## 示例与测试

- [`claimcrawl`](examples/claimcrawl/)：把混合 WHY / HOW / WHETHER 的 Figure 1 拆成 motivation 与 method 两张图；
- [`method-pipeline`](examples/method-pipeline/)：展示 typed edge，并明确阻止模型凭空补反馈回路；
- [`quantitative-result`](examples/quantitative-result/)：CSV 绑定的数据图，禁止虚构显著性或让图像模型绘制数值几何。

测试命令：

```bash
python -m unittest discover -s tests -v
python skills/research-figure/scripts/figure_workbench.py check-links --strict
```

## 科学质量门禁

一张图只有在以下条件同时满足时才能通过：

- 所有 supported claim 均可追溯；
- inferred / hypothesis 在视觉上明确标注；
- 所有 edge 的端点、方向和类型正确；
- 因果箭头有足够证据；
- 数据图使用精确、可复现的代码路径；
- 真实最终尺寸的产物已经检查；
- 不存在 fabricated value、错误标签、反向箭头或过度宣称；
- 科学忠实度和结构正确性均为 5/5；
- 在需要时交付可编辑源文件、audit 和 provenance。

默认最多进行三轮有针对性的 render–audit。若同一 major issue 连续两轮没有改善，则升级给作者或领域专家，而不是继续消耗并宣称“publication-ready”。

## 市场定位

PaperBanana/PaperVizAgent、SciFig、AutoFigure、AutoFigure-Edit 等项目已经在端到端方法图生成、参考驱动与可编辑化方面取得明显进展；现有科研 Skill 则分别擅长数据图、风格库或工程图后端。

仍然明显缺少的是：一个跨 motivation、method、mechanism、results 的 claim–evidence–epistemic 审计层。这正是本项目的差异化位置。完整竞品工作量、质量和局限对比见 [2026 市场调研](docs/MARKET_LANDSCAPE_2026.md)。

## 边界

- 不把生成图片当作实验数据。
- 不在未经授权时把未发表论文、审稿材料、患者数据或内部数据发送给外部服务。
- 不凭记忆虚构 AAAI、NeurIPS、ACL、Nature 等 venue 的固定“绘图风格”或 AI 政策；投稿前必须核验官方当前规则。
- 不整体模仿参考图受保护的独特表达，只抽取抽象布局与视觉属性。
- 最终科学解释仍需作者或领域专家确认。

项目采用 MIT License。
