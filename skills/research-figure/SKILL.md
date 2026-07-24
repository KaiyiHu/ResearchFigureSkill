---
name: research-figure
description: Read papers or research briefs in full, produce an evidence-anchored detailed summary, classify the intended figure role, compile a reference-aware scientific drawing prompt from a reusable prompt formula, generate editable SVG/PPTX/draw.io or exact plots, and audit the real artifact for scientific errors, wrong arrows, garbled fonts, blur, fuzzy shapes, clipping, and low resolution. Use for Figure 1, motivation figures, method/pipeline diagrams, mechanism figures, dataset/taxonomy figures, experiment or ablation plots, graphical abstracts, reference-guided redesign, figure prompts, editable scientific illustration, paper-to-figure workflows, figure critique/repair, 论文配图, 科研绘图, 提示词模板, 方法图, 机制图, 实验图, 消融图, 图形摘要, or 图片清晰度检查.
---

# Research Figure Prompt Compiler

Turn paper understanding into a precise drawing prompt, then turn the prompt
into an editable, audited scientific figure.

The default sequence is:

```text
full source inspection
  → detailed paper summary
  → evidence and exact-text register
  → figure-role classification
  → visual narrative and FigureSpec
  → prompt-formula compilation
  → AI/vector/plot rendering
  → scientific + optical QA
  → editable delivery
```

Do not start by drawing. Do not hide the prompt behind internal planning. For a
paper-to-figure request, deliver the detailed summary and compiled production
prompt as first-class artifacts.

Resolve `SKILL_ROOT` as the directory containing this `SKILL.md`. Run bundled
scripts from that path, not from the user's current directory.

## Non-negotiable rules

1. Read the allowed source scope before deciding the figure. Respect explicit
   exclusions such as captions, supplementary material, or existing figures.
2. Do not invent methods, components, values, equations, labels, citations,
   causal links, feedback loops, or legal/clinical conclusions.
3. Give one figure one dominant reader question. Separate **WHY**, **HOW**, and
   **WHETHER** when combining them would blur the argument.
4. Compile exact components, text, relations, layout, style, negative
   constraints, outputs, and QA into the production prompt.
5. Never ask an image model to carry evidence-bearing values, axes, equations,
   tables, or long final labels. Render them deterministically.
6. Prefer an editable master: SVG, native PPTX shapes, draw.io XML, plot source,
   or a hybrid composition with live text.
7. Inspect the actual rendered artifact. Wrong glyphs, pseudo-text, blur,
   fuzzy/melted shapes, clipping, overlap, low-resolution upscaling, or
   unreadable final-size text block acceptance.
8. Verify current venue requirements from official sources when they matter;
   do not treat “AAAI style” or “Nature style” as a fixed factual standard.

## Choose the operating mode

- **Plan** — summarize the source, classify the figure, and return FigureSpec.
- **Prompt** — run through prompt compilation and return `final-prompt.md`.
- **Build** — compile, render, inspect, revise, and deliver editable outputs.
- **Critique** — reconstruct the minimum expected contract and audit an
  existing artifact.
- **Repair** — preserve verified content and apply only evidence-linked deltas.

Infer the mode from the request. If the user asks to “make a figure,” use
Build. If the user asks mainly for a prompt, stop after Prompt unless rendering
is also requested.

## Run the workflow

### Stage 0 — Establish the delivery contract

Record:

- source files and allowed/excluded scope;
- requested figure number or purpose;
- audience, language, venue, medium, and provisional dimensions;
- reference figures and how they may be used;
- editable formats and preview formats;
- privacy/external-provider permission.

When the role is unspecified, infer it from the paper and explain the decision.
Ask only when two evidence-supported roles remain equally plausible and would
produce materially different figures.

### Stage 1 — Inspect and summarize the full source

For a paper, inspect all available relevant sections: abstract, introduction,
related work, method overview and details, experiments, ablations/analysis,
limitations, conclusion, and relevant appendix/supplement. Use the appropriate
document/PDF tools and inspect page geometry when captions or figures affect
scope.

Create `paper-summary.md` from
[`assets/paper-summary.template.md`](assets/paper-summary.template.md). It must
include:

- problem, difficulty, existing approaches, and gap;
- key observations, bounded thesis, and contributions;
- method inputs, operations, states, outputs, and absent paths;
- datasets, baselines, metrics, uncertainty, and experimental boundaries;
- exact main, ablation, negative, and qualitative findings;
- limitations, proxies, ethics/legal boundaries, and missing evidence;
- terminology/exact-text register and section-coverage table;
- candidate figure roles and unique evidence.

This is a detailed evidence-anchored summary, not a generic abstract rewrite.
Read [`references/analysis-protocol.md`](references/analysis-protocol.md) for
source mapping, claim status, and portfolio planning.

For substantial work, also create and validate `evidence-ledger.json`:

```bash
python3 "${SKILL_ROOT}/scripts/figure_workbench.py" validate-artifact \
  --kind evidence-ledger evidence-ledger.json --strict
```

### Stage 2 — Classify the figure role

Classify by reader question, not figure number:

| Role | Reader question | Default story |
|---|---|---|
| `motivation` | Why is this work needed? | status quo → observed failure → bounded need |
| `method` | How does it work? | typed input → operations/handoffs → output |
| `mechanism` | Why should a component change an outcome? | limitation → intervention → intermediate change → outcome |
| `experiment` | Does evidence support the claim? | comparison → uncertainty/negative evidence → boundary |
| `ablation` | Which controlled choice matters? | controlled change → exact delta → bounded interpretation |
| `comparison` | How do alternatives differ? | shared criteria → trade-offs → implication |
| `taxonomy` | How is the space or dataset organized? | dimensions/construction → groups → overlap/exceptions |
| `graphical-abstract` | What compact story should readers retain? | context → intervention → principal result → implication |

Figure 1 is often motivation, but never assume that from numbering alone.
Prevent the common failure “Figure 1 becomes Figure 2”: a motivation figure
must not reveal the complete method architecture. Read
[`references/role-playbooks.md`](references/role-playbooks.md).

Save a concise `figure-role-analysis.md` with:

- selected role and confidence;
- reader question and five-second message;
- claim boundary;
- unique evidence;
- content to include and explicitly exclude;
- renderer recommendation.

### Stage 3 — Build the visual argument

Create a claim–evidence map, then a FigureSpec. Every panel must contribute a
unique supported claim. Every relation must name source, target, direction,
semantic type, payload label, and claim ID when it carries a claim.

```bash
python3 "${SKILL_ROOT}/scripts/figure_workbench.py" new \
  --role method --out figure-spec.json
python3 "${SKILL_ROOT}/scripts/figure_workbench.py" validate \
  figure-spec.json --strict
```

Use [`references/figure-spec.md`](references/figure-spec.md) and
[`references/visual-grammar.md`](references/visual-grammar.md). Keep scientific
relations separate from spatial reading order.

When a reference figure is supplied, inspect it and record only abstract
attributes: aspect ratio, region proportions, alignment, whitespace, density,
border treatment, palette relationships, icon scale, arrow rhythm, and
typography hierarchy. Do not copy its text, data, logos, unique icons, or
distinctive expression.

### Stage 4 — Compile the core production prompt

Read [`references/prompt-formula.md`](references/prompt-formula.md) every time a
new production prompt is created. Compile in this fixed order:

```text
P = Job/Canvas
  + Reference contract
  + Scientific purpose
  + Narrative
  + Components/exact text
  + Relations
  + Layout geometry
  + Visual system
  + Deterministic/editable construction
  + Negative constraints
  + Outputs
  + Preflight QA
```

Use the deterministic compiler when possible:

```bash
python3 "${SKILL_ROOT}/scripts/figure_workbench.py" compile \
  figure-spec.json --summary paper-summary.md --out final-prompt.md
python3 "${SKILL_ROOT}/scripts/figure_workbench.py" lint-prompt \
  final-prompt.md --spec figure-spec.json --summary paper-summary.md --strict
```

The final prompt must be explicit enough to reproduce the scientific
inventory, high-level composition, region ratios when known, exact text,
relation semantics, negative prompt, editable output, and QA checks. Style is a
bounded layer after scientific content.

See [`references/prompt-system.md`](references/prompt-system.md) for the
versioned stage prompts that produce the summary, decision, specification,
compiled prompt, critique, and patch.

### Stage 5 — Route and render

Choose the lowest-risk route:

- `vector-code` for label/arrow-heavy diagrams and editable structure;
- `plot-code` for exact values, axes, uncertainty, and statistics;
- `image-generation` for approved conceptual illustration layers only;
- `hybrid` for generated illustration plus deterministic text/arrows/plots.

For reference-driven hand-drawn or illustrative styles, default to hybrid:
generate a text-free illustration layer, then compose exact live labels,
arrows, and scientific geometry in SVG/PPTX/draw.io. Do not accept generated
pseudo-text as final typography.

### Stage 6 — Inspect scientific and optical quality

Open the real artifact, not only the prompt. Audit at final size, 100%, and
200% zoom. Use [`references/review-protocol.md`](references/review-protocol.md).

Check:

- claim, component, number, equation, and relation correctness;
- role purity and five-second message;
- exact spelling, symbols, font substitution, missing glyphs, pseudo-text, and
  accidental text rasterization;
- clipped, overlapping, duplicated, off-canvas, or microscopic labels;
- blurred, fuzzy, melted, ghosted, partially erased, or visibly upscaled
  shapes and inconsistent local sharpness;
- final-size readability, color/shape redundancy, and contrast;
- editable layers, semantic groups, stable IDs, and provenance.

For SVG, run the bundled structural inspector. For every format, generate and
complete an audit:

```bash
python3 "${SKILL_ROOT}/scripts/figure_workbench.py" inspect-svg \
  editable/figure.svg --spec figure-spec.json --strict
python3 "${SKILL_ROOT}/scripts/figure_workbench.py" audit-template \
  figure-spec.json --out figure-audit.json
python3 "${SKILL_ROOT}/scripts/figure_workbench.py" validate-artifact \
  --kind figure-audit figure-audit.json --spec figure-spec.json --strict
```

`inspect-svg` is a structural precheck, not a visual verdict. Render the SVG
and inspect the pixels as required above. For PPTX, draw.io, or PDF masters,
open the source and export with a format-native application or document tool,
verify live text/groups there, and record that real-file inspection in the
audit. The workbench does not claim automatic structural inspection for those
non-SVG formats.

One scientific or optical critical failure blocks acceptance.

### Stage 7 — Repair by delta

Express each change as:

```text
target → observed failure → minimal change → preserve → verification
```

Prefer local edits to the editable master. Do not regenerate the entire figure
to fix one label or arrow. Default to three render–audit rounds, preserve the
best valid state, and stop only when the required thresholds pass and no new
critical issue appears in two consecutive audited states.

## Default artifact layout

```text
output/<paper>/<figure>/
├── paper-summary.md
├── figure-role-analysis.md
├── evidence-ledger.json
├── figure-spec.json
├── final-prompt.md
├── editable/
│   └── figure.svg | figure.pptx | figure.drawio
├── previews/
│   ├── draft-01.png
│   └── final.png
├── figure-audit.json
└── provenance.json
```

Return paths to the summary, role decision, compiled prompt, editable master,
preview, audit, and unresolved evidence. Do not claim an output exists unless
it was created and inspected.

## Load references selectively

- Full-paper analysis: [`analysis-protocol.md`](references/analysis-protocol.md)
- Prompt formula and templates:
  [`prompt-formula.md`](references/prompt-formula.md)
- Versioned stage prompts: [`prompt-system.md`](references/prompt-system.md)
- FigureSpec: [`figure-spec.md`](references/figure-spec.md)
- Role purity: [`role-playbooks.md`](references/role-playbooks.md)
- Layout, arrows, accessibility:
  [`visual-grammar.md`](references/visual-grammar.md)
- Domain notation: [`domain-overlays.md`](references/domain-overlays.md)
- Real-artifact QA: [`review-protocol.md`](references/review-protocol.md)
- Venue, provenance, and AI-use boundaries:
  [`integrity-and-venues.md`](references/integrity-and-venues.md)
- End-to-end synthetic regression:
  [`worked-example.md`](references/worked-example.md)

## Boundaries

- Generated imagery is never experimental evidence.
- Do not expose unpublished/private material to external services without
  authorization.
- Do not imitate a living artist or duplicate a reference figure's protected
  expression; extract abstract visual attributes.
- Domain experts and authors retain responsibility for scientific
  interpretation and final approval.
