# 2025–2026 科研绘图市场与竞品调研

> 调研快照：2026-07-24。GitHub star、fork、仓库体积和活跃时间会变化；它们只能说明关注度与工程规模，不能代替科学质量评价。

## 目录

1. 执行结论
2. 用户任务与真实痛点
3. 市场分层
4. 开源项目工作量与质量
5. Skill 型竞品
6. 商业工具
7. 从研究前沿提炼的方法
8. 未被充分解决的市场空位
9. 对 ResearchFigureSkill 的设计影响
10. 建议公开评测指标
11. 一手来源

## 1. 执行结论

科研绘图已经从“一次性文本生成图片”快速进入：

```text
内容解析
→ 结构规划
→ 多后端渲染
→ 可编辑输出
→ 多轮评价与局部修改
```

当前竞争最激烈的是“输入论文/方法描述，自动生成漂亮的 method figure”；真正没有被稳定解决的是：

> 从论文证据和 claim 出发，先建立可机器校验的视觉论证契约，再按风险路由到 plot、SVG/draw.io/PPT、image generation 或 hybrid，最终交付可编辑、可审计、可复现的图形资产。

因此，ResearchFigureSkill 不应主打“更多科研绘图 Prompt”，而应主打：

- claim–evidence traceability；
- epistemic calibration；
- typed relation / typed arrow；
- FigureSpec 中间表示；
- 数据图与概念图强制分流；
- 对真实产物而不是 Prompt 的审计；
- 科学硬错误一票否决；
- 可编辑局部修复与 provenance。

## 2. 用户任务与真实痛点

### 2.1 不知道该画什么

用户往往拥有论文、实验和方法，但缺少把论证压缩成视觉语言的能力。最先需要解决的不是画布，而是：

- 哪个 claim 最值得成为一张图；
- Figure 1 应该回答 WHY、HOW 还是 WHETHER；
- 哪些 panel 有独立证据价值；
- 哪些细节必须删除；
- 是否应该拆成两张图。

### 2.2 图很好看，但科学结构错了

端到端系统的常见风险包括：

- 漏组件；
- 箭头接错或反向；
- 相关性被升级成因果；
- hypothesis 被画成 established mechanism；
- 视觉大小暗示不存在的量级；
- 自动补全论文中没有的模块。

PaperBanana 社区在结构错误检查上报告过 critic 假收敛与额外检查成本明显上升的问题，说明“整体看起来不错”不是可靠门禁：[issue #35](https://github.com/dwzhu-pku/PaperBanana/issues/35)。

### 2.3 数值图与概念图被错误地统一处理

数值、误差棒、坐标轴、缺失值、统计显著性和样本量必须由可验证数据与代码生成。图像模型可用于插图或概念基底，但不能绘制证据性几何。PlotGen 将反馈拆为 Numeric、Lexical、Visual，也反映了这三类错误不能被一个总评覆盖：[PlotGen](https://arxiv.org/abs/2502.00988)。

### 2.4 无法局部编辑

真实论文修改通常是：

- 改一个箭头；
- 修一个标签；
- 调一个 panel；
- 替换一列数据；
- 增加限定词；
- 修复审稿人指出的 overclaim。

如果每次都重新生成整张图，正确部分也会回归。用户对 Draw.io 式局部编辑的需求在 PaperBanana 社区中也被明确提出：[issue #20](https://github.com/dwzhu-pku/PaperBanana/issues/20)。

### 2.5 不可复现与不可审计

常见交付只有最终 PNG，缺少：

- 输入证据范围；
- Prompt 版本；
- 模型/provider；
- 随机种子；
- 可编辑源文件；
- 数据绑定；
- 修改历史；
- 审计记录。

这使作者、合作者和审稿人都无法快速确认图的来源和修改影响。

### 2.6 隐私、版权和投稿政策

未发表论文、审稿材料、患者数据和内部实验数据不应被 Skill 静默上传。参考图风格也不能被当成科学内容来源。商业工具和出版方对生成式 AI 图片的政策并不统一，而且变化很快；必须在投稿时核验官方当前规则。BioRender 的官方 AI 页面本身也提醒用户在正式使用前检查期刊政策：[BioRender AI](https://www.biorender.com/ai-tools)。

## 3. 市场分层

### A. 端到端科研图形生成代理

代表：PaperBanana/PaperVizAgent、SciFig、AutoFigure、LiveFigure、Crafter。

优势：

- 自动化程度高；
- 有多代理规划与反馈；
- 精选案例视觉质量强；
- 可直接连接现代 VLM/image model。

限制：

- 主要围绕 AI/ML method figure；
- 结构检查可能假收敛；
- provider 依赖、成本和延迟明显；
- source evidence 与 visual claim 的逐条映射仍弱。

### B. 可编辑化与逆向重建

代表：AutoFigure-Edit、Edit-Banana。

优势：

- SVG、draw.io/XML 或编辑器；
- 能修旧图和 raster；
- 降低局部修改成本。

限制：

- “对象可编辑”不等于“对象有科学语义”；
- 上游错误可能被矢量化后固化；
- 分割、OCR、公式识别和 GPU 基础设施较重。

### C. 精确数据图与代码生成

代表：K-Dense scientific-visualization、LIDA、PlotGen、ChartMimic。

优势：

- 数据与代码绑定；
- 适合数值、误差、轴和统计；
- 可复现与出版导出较强。

限制：

- 不负责 paper → figure intent；
- 对 motivation、mechanism、method architecture 的视觉叙事覆盖较弱。

### D. Prompt / Skill 资产库

代表：Engineering Figure Agent、K-Dense scientific-schematics、GPT-Image2-Skill、Paper Visualizer、nature-figure。

优势：

- 安装轻；
- 模型无关或多 provider；
- 渐进披露；
- 对某一类任务有明确操作规则。

限制：

- 有的偏 renderer，有的偏 style gallery，有的偏 data plot；
- 跨图型 claim–evidence–epistemic audit 普遍不完整。

### E. 商业科研绘图平台

代表：BioRender、FigCanvas、FigureLabs、Mind the Graph、Napkin AI。

优势：

- 素材库、编辑器、协作和导出体验；
- 用户愿意为省时与易编辑付费。

限制：

- SaaS 隐私与 credits；
- 方法、benchmark 与 provenance 不完全开放；
- 生成后矢量化不一定保留科学语义。

## 4. 开源项目工作量与质量

下表 star/fork/仓库体积来自 GitHub API 快照；仓库体积含图片、数据和模型资产，不等于代码量。

| 项目 | 2026-07-24 快照 | 工作量信号 | 质量亮点 | 主要缺口 |
|---|---:|---|---|---|
| [PaperBanana](https://github.com/dwzhu-pku/PaperBanana) | 6,836★ / 514 forks / 14.7 MB | 完整多代理 Python 工程、demo、benchmark 接口 | Retriever→Planner→Stylist→Visualizer→Critic；292 个 NeurIPS 2025 方法图案例。[论文](https://arxiv.org/abs/2601.23265) | 偏 method figure；结构 critic 仍可能漏错；统计图与跨领域仍在演进 |
| [AutoFigure](https://github.com/ResearAI/AutoFigure) | 1,771★ / 132 / 82.3 MB | 前后端、生成/评价循环、编辑器 | 文本/PDF 到 SVG 或 mxGraph XML，可编辑性强 | 系统较重；上游错误可能被后续编辑格式固化 |
| [AutoFigure-Edit](https://github.com/ResearAI/AutoFigure-Edit) | 4,022★ / 262 / 115.6 MB | Python 服务、SAM/OCR/矢量化、Web 编辑器 | 长文本、参考风格、可编辑 SVG。[ACL Demo 论文](https://aclanthology.org/2026.acl-demo.6/) | provider 和多阶段依赖复杂；语义 traceability 不是主要目标 |
| [Paper2Any](https://github.com/OpenDCAI/Paper2Any) | 2,728★ / 189 / 430.6 MB | 平台级前后端与部署，覆盖多种 paper-to-* | PDF/截图/文本到图、路线图、幻灯片 | 安装与 GPU/服务成本高；开源版与在线产品边界需辨别 |
| [Edit-Banana](https://github.com/BIT-DataLab/Edit-Banana) | 5,438★ / 360 / 85.9 MB | SAM、VLM、OCR、公式识别、draw.io 重建 | raster/PDF 到可编辑结构，旧图修复强 | 主要是后处理/重建，不负责从 claim 规划新图 |
| [LiveFigure](https://github.com/tsinghua-fib-lab/LiveFigure) | 11★ / 0 / 6.8 MB | 论文原型，仓库历史很短 | 参考研究 + 程序化 PPT + actor–critic，可编辑 PPTX。[论文](https://arxiv.org/abs/2605.23527) | 当前代码成熟度较低；主要在 AI 会议方法图上验证 |
| [Crafter](https://github.com/HaozheZhao/Crafter) | 146★ / 10 / 22.6 MB | 论文原型、编辑器与多输入条件 | 支持文本、mask、关键元素、草图和 SVG 编辑。[论文](https://arxiv.org/abs/2605.30611) | API/SAM3/CUDA 依赖；当前提交历史较短 |
| [K-Dense Skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 31,638★ / 3,154 / 38.5 MB | 大型科研 Skill 集合，有脚本、references 和测试 | scientific-visualization 对数据真实、缺失值、不确定性、可访问性和导出很强 | plot 强、paper→visual argument 弱 |
| [GPT-Image2-Skill](https://github.com/wuyoscar/GPT-Image2-Skill) | 3,930★ / 333 / 458.2 MB | 大型图片 Prompt gallery 和路由索引 | 渐进披露与类别检索值得借鉴 | 研究图仍是视觉 gallery；缺数据 grounding 与科学审计 |
| [LIDA](https://github.com/microsoft/lida) | 3,270★ / 381 / 509.9 MB | 成熟的数据可视化代理架构 | 摘要、目标、代码、编辑、解释、评价和修复 | 最后活跃于 2024；非投稿科研图专用 |
| [ChartMimic](https://github.com/ChartMimic/ChartMimic) | 132★ / 3 / 18.1 MB | 4,800 真实论文图—指令—代码基准 | chart-to-code regression 思路很强 | 不是完整的 paper intent 或概念图生成系统 |
| [SciSketch](https://github.com/yale-nlp/SciSketch) | 7★ / 1 / 1.3 MB | 公开代码较小，图形代码 + 图标替换工作流 | layout plan、自 refinement、code verification。[EMNLP Demo](https://aclanthology.org/2025.emnlp-demos.28/) | 当前仓库只有少量提交；覆盖范围和工程成熟度有限 |

### 解读

- star 高不代表科学可靠，尤其是刚发布、传播性强的图像项目。
- 仓库大不代表分析更深，可能主要由模型、样例或图片资产构成。
- 论文原型可能方法先进但工程历史短。
- Skill 项目通常体积小，但 Prompt 质量、失败行为和测试更关键。

## 5. Skill 型竞品

### Engineering Figure Agent

[仓库](https://github.com/heyu-233/engineering-figure-agent)

审计快照显示其具备完整 `SKILL.md`、多份 reference、十余个脚本、schema 与测试；主要价值是：

- image / plot / mixed 路由；
- 明确禁止图片模型绘制精确数值；
- provider 适配；
- 工程图与中文标签支持；
- 可编辑交接。

不足：

- 自己明确要求“figure goal 已经清楚”后再使用；
- paper → claim → figure intent 不属于核心范围；
- 缺少 claim–evidence ledger 与 typed epistemic audit。

这意味着它很适合作为 ResearchFigureSkill 的下游 renderer，而不是直接替代。

### K-Dense scientific-schematics

[Skill](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/scientific-skills/scientific-schematics)

优势：

- 有生成脚本和 VLM 评分；
- 按 journal / conference / poster 设置不同阈值；
- 提供迭代与 API 工作流。

不足：

- 自然语言仍较直接地驱动图片；
- 单一总分可能掩盖 unsupported claim 或错误箭头；
- 证据锚点与 renderer-independent spec 不完整。

### K-Dense scientific-visualization

[仓库](https://github.com/K-Dense-AI/scientific-agent-skills)

这是数据图质量的高标准对照：

- 真实编码；
- 缺失/排除值；
- 误差与单位；
- 色盲与出版尺寸；
- 矢量导出；
- provenance / manifest；
- 测试。

它说明 ResearchFigureSkill 不应重写一个庞大 plotting library，而应把量化 panel 安全路由到这样的下游能力。

### Paper Visualizer

[仓库](https://github.com/WilsonWukz/MySkills/tree/main/skills/visual-architect)

优势：

- 用 layout pattern 先组织结构；
- 输出 zone、connections、text rules；
- 简洁、易安装。

不足：

- 核心是单个 `SKILL.md`；
- source grounding、数值路由与科学审计较弱；
- 主要产出图像模型 schema；
- 不区分不同 evidence status。

### nature-figure

[仓库](https://github.com/Yuan1z0825/nature-skills)

优势：

- claim-first 的出版图工作流；
- Python/R 数据图、SVG/PDF/TIFF、统计与图注；
- references 与 progressive disclosure 较成熟。

不足：

- 主要面向 plot 和多 panel publication figures；
- 图像模型驱动的 method/mechanism illustration 不是主路径；
- 后端选择约束较强。

## 6. 商业工具

| 工具 | 主要优势 | 给开源 Skill 留下的空间 |
|---|---|---|
| [BioRender](https://www.biorender.com/) | 大型生命科学素材库、模板、协作、行业信任 | 授权与付费；AI 输出和出版政策需核验；开放 provenance 与跨 provider 能力有限 |
| [FigCanvas](https://figcanvas.com/) | 多 panel 无限画布、科研插画与数据图统一编辑、SVG/PDF/高分辨率导出 | 公开 benchmark、内部语义图和本地审计有限 |
| [FigureLabs](https://figurelabs.ai/) | 文本/PDF/图片/参考图、局部重绘和 PPTX/SVG | SaaS 隐私、credits、方法透明度和长期可用性 |
| [Mind the Graph](https://mindthegraph.com/) | 大量科学插图、模板和生命科学工作流 | 自动 claim 推理与开放可审计链较弱 |
| [Napkin AI](https://www.napkin.ai/) | 文本到可编辑视觉、多格式导出、协作体验 | 面向通用商业叙事，不负责科学证据与数值保证 |

商业工具证明用户愿意为素材、易编辑和快速交付付费；开源 Skill 的机会是透明、可审计、本地优先、跨 provider 和可组合。

## 7. 从研究前沿提炼的方法

### PaperBanana / PaperVizAgent

[论文](https://arxiv.org/abs/2601.23265) · [代码](https://github.com/google-research/papervizagent)

值得借鉴：

- reference retrieval；
- Planner、Stylist、Visualizer、Critic 分工；
- 多候选与迭代。

不应直接照搬：

- style 与 content 不能覆盖 source truth；
- critic 需要结构化 hard gate，而不是只看整体视觉。

### SciFig

[论文](https://arxiv.org/abs/2601.04390) · [项目页](https://shramanpramanick.github.io/SciFig/)

值得借鉴：

- hierarchical layout；
- component 与 layout 分离；
- rubric-based evaluation；
- 可编辑输出。

关键启示：

> 在语义与层级结构没有锁定时，多轮反馈不保证单调改善。必须保存 best-so-far，并把 revision 限制在正确层级。

### FigAgent

[论文](https://arxiv.org/abs/2603.29590) · [项目页](https://zhuolingli.github.io/FigAgent-page-project/)

值得借鉴：

- Parser / Planner / Drawer / Evaluator / Refiner；
- Explore-and-Select；
- 可演化绘图工具库。

ResearchFigureSkill 将 Explore-and-Select 限制在 layout/render 层，避免候选生成改变科学语义。

### AutoFigure-Edit

[论文](https://aclanthology.org/2026.acl-demo.6/) · [代码](https://github.com/ResearAI/AutoFigure-Edit)

值得借鉴：

- 长文本输入；
- 参考风格；
- 可编辑 SVG；
- 嵌入式编辑器。

关键启示：

- raster text 不可靠；
- Prompt style 控制有歧义；
- “可编辑”需要和科学语义 ID 结合才更适合审计。

### SciForma

[论文](https://arxiv.org/abs/2607.18091) · [计划开放代码](https://github.com/microsoft/SciForma)

这是调研时最新的重要信号。SciForma 将结构忠实拆成 Component、Arrow、Text 三个轴，并指出结构正确是 conjunctive 的：一个反向箭头或错误标签足以让整图失效。

ResearchFigureSkill 的 hard gate 与其结论一致，但进一步加入：

- claim–source；
- epistemic status；
- role purity；
- numeric/data route；
- privacy/provenance。

### SciSketch

[论文](https://aclanthology.org/2025.emnlp-demos.28/) · [代码](https://github.com/yale-nlp/SciSketch)

值得借鉴：

- 图形代码路径与图片路径分离；
- layout refinement；
- code verification；
- 图标/经验图片替换。

## 8. 未被充分解决的市场空位

| 能力 | 端到端生成项目 | 数据图 Skill | Prompt gallery | ResearchFigureSkill 目标 |
|---|---:|---:|---:|---:|
| method figure 视觉生成 | 强 | 弱 | 中 | 下游兼容 |
| 精确数据图 | 中/在演进 | 强 | 弱 | 强制路由 |
| motivation role | 弱–中 | 弱 | 中 | 强 |
| mechanism epistemic audit | 弱 | 弱 | 弱 | 强 |
| claim–source anchor | 弱 | 数据级较强 | 弱 | 强 |
| typed edge | 中 | 不适用 | 弱 | 强 |
| 科学硬错误一票否决 | 不稳定 | 中–强 | 弱 | 强 |
| renderer-independent IR | 部分 | 部分 | 弱 | 强 |
| 可编辑局部修复 | 中–强 | 强 | 弱 | 通过稳定 ID |
| privacy/provenance | 不统一 | 中 | 弱 | 核心规则 |

最有机会形成壁垒的组合不是某一条 Prompt，而是：

```text
Evidence Ledger
+ Figure Portfolio
+ FigureSpec
+ typed relation semantics
+ renderer risk router
+ artifact inventory diff
+ minimal patch and regression guard
```

## 9. 对 ResearchFigureSkill 的设计影响

### 已采纳

1. Prompt 采用版本化六阶段编译，而不是多份重复大模板。
2. FigureSpec 成为唯一中间事实源。
3. supported / inferred / hypothesis / missing 显式区分。
4. causal edge 必须引用 supported causal claim。
5. experiment / ablation 禁止 pure image generation。
6. exact text、数字和公式走确定性路径。
7. 审计实际产物并做 component / relation / text / numeric inventory diff。
8. critical failure 不能被美观分平均。
9. 默认三轮 targeted revision；同一 major issue 两轮无改善即升级。
10. 投稿规则只从官方当前页面核验，不虚构固定 venue 审美。

### 明确不做

- 不内置一个重型端到端图像模型平台；
- 不重新实现完整 plotting ecosystem；
- 不承诺任何 provider 的“最漂亮输出”；
- 不把生成图当作实验结果；
- 不靠更长 Prompt 修复上游证据错误；
- 不自动上传未发表材料；
- 不收集没有测试价值的 style adjective gallery。

## 10. 建议公开评测指标

项目未来应报告：

- claim traceability precision / recall；
- required component recall 与 extra component rate；
- edge endpoint / direction / type accuracy；
- causal calibration error；
- exact-label match；
- numeric/data consistency；
- editable-object coverage；
- final-size readability；
- grayscale / color-vision accessibility；
- human revision count 与 time-to-accept；
- per-provider cost、latency 与 variance；
- reproducible artifact bundle completeness；
- venue export check pass rate；
- regression rate across revision rounds。

比“总体美学分”更有说服力的项目叙事是：

> 对同一份论文或数据，本 Skill 能减少遗漏组件、错误关系、过度宣称和人工修改次数，并交付完整的 spec、editable source、audit 与 provenance。

## 11. 一手来源

### 论文与项目

- [PaperBanana / PaperVizAgent](https://arxiv.org/abs/2601.23265)
- [PaperBanana GitHub](https://github.com/dwzhu-pku/PaperBanana)
- [SciFig](https://arxiv.org/abs/2601.04390)
- [SciFig project](https://shramanpramanick.github.io/SciFig/)
- [FigAgent](https://arxiv.org/abs/2603.29590)
- [AutoFigure](https://github.com/ResearAI/AutoFigure)
- [AutoFigure-Edit](https://aclanthology.org/2026.acl-demo.6/)
- [AutoFigure-Edit GitHub](https://github.com/ResearAI/AutoFigure-Edit)
- [SciSketch](https://aclanthology.org/2025.emnlp-demos.28/)
- [SciSketch GitHub](https://github.com/yale-nlp/SciSketch)
- [SciForma](https://arxiv.org/abs/2607.18091)
- [LiveFigure](https://arxiv.org/abs/2605.23527)
- [Crafter](https://arxiv.org/abs/2605.30611)
- [PlotGen](https://arxiv.org/abs/2502.00988)
- [ChartMimic](https://github.com/ChartMimic/ChartMimic)
- [LIDA](https://github.com/microsoft/lida)

### Skills 与工具

- [Engineering Figure Agent](https://github.com/heyu-233/engineering-figure-agent)
- [K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)
- [GPT-Image2-Skill](https://github.com/wuyoscar/GPT-Image2-Skill)
- [Paper Visualizer / MySkills](https://github.com/WilsonWukz/MySkills)
- [nature-skills](https://github.com/Yuan1z0825/nature-skills)

### 商业产品官方页面

- [BioRender](https://www.biorender.com/)
- [BioRender AI tools](https://www.biorender.com/ai-tools)
- [FigCanvas](https://figcanvas.com/)
- [FigureLabs](https://figurelabs.ai/)
- [Mind the Graph](https://mindthegraph.com/)
- [Napkin AI](https://www.napkin.ai/)
