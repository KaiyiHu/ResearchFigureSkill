---
name: research-figure
description: Transform papers, proposals, experiment results, figure briefs, or existing figures into scientifically grounded visual arguments, auditable FigureSpec JSON, renderer-specific prompts, and revision instructions. Use when deciding what a research figure should communicate; planning motivation, method, pipeline, mechanism, result, ablation, taxonomy, comparison, or graphical-abstract figures; generating or critiquing scientific diagrams; preventing unsupported claims, misleading arrows, or invented values; choosing between editable vector code, exact data plots, image generation, and hybrid composition; or auditing publication readiness. Trigger on requests such as research figure, paper figure, Figure 1, methodology diagram, scientific schematic, graphical abstract, figure prompt, figure critique, 论文配图, 科研绘图, 方法图, 机制图, 实验图, 消融图, or 图形摘要.
---

# Research Figure Compiler

Treat every figure as a **visual argument with a truth contract**. Compile source-grounded claims into an explicit intermediate representation before choosing a renderer. Optimize beauty only after scientific fidelity, role purity, and structural correctness pass.

## Non-negotiable rules

1. Do not draw or write a final image prompt before defining the figure's reader question, five-second message, claim boundary, and evidence anchors.
2. Do not invent methods, results, numbers, equations, labels, baselines, citations, or causal relations.
3. Use a causal arrow only when the source supports causality. Use data-flow, temporal, associative, comparison, containment, or feedback semantics otherwise.
4. Never use an image generator to render exact values, axes, tables, equations, or benchmark geometry. Route quantitative panels to deterministic plotting code.
5. Keep generated text short. Prefer programmatic text overlays or editable vector text when label fidelity matters.
6. Preserve uncertainty and negative evidence. Mark unsupported but useful content as `hypothesis`, `inferred`, or `missing`; never silently promote it to `supported`.
7. Treat a critical failure as conjunctive: one reversed arrow, fabricated value, unsupported claim, or unreadable required label blocks acceptance even if the figure is attractive.
8. Verify current venue and publisher requirements from official sources when a submission target is named; do not rely on remembered policies.

## Choose the operating mode

- **Plan** — Decide the figure portfolio, role, argument, panels, and renderer. Return a FigureSpec; do not render.
- **Prompt** — Compile a validated FigureSpec into a renderer-specific prompt.
- **Build** — Plan, compile, render with available tools, inspect the real artifact, and revise.
- **Critique** — Audit an existing figure against its source and return evidence-linked revision deltas.
- **Repair** — Preserve correct content, change only failed elements, then re-audit.

Infer the mode from the request. If the user asks for a figure without enough source material, produce the most useful partial FigureSpec and label the missing evidence instead of fabricating or stopping prematurely.

Route gates by mode:

| Mode | Gates |
|---|---|
| `Plan` | Run Gates 0–4, return the spec, and stop before compilation/rendering. |
| `Prompt` | Run Gates 0–6, return the spec and prompt, and stop before rendering. |
| `Build` | Run Gates 0–8. |
| `Critique` | Reconstruct the minimum source-grounded FigureSpec, then run Gate 7. |
| `Repair` | Start from the last valid spec/artifact, then run Gates 7–8. |

Resolve `SKILL_ROOT` as the directory containing this `SKILL.md`. Invoke bundled scripts with their resolved path; never assume the user's current directory is the Skill directory.

## Run the gated workflow

### Gate 0 — Establish the delivery contract

Record the intended medium, audience, language, target venue if known, width/aspect ratio, editability requirement, and desired outputs. Separate:

- scientific target: what the reader must learn;
- artifact target: spec, prompt, SVG, plot, slide, raster draft, or critique;
- evidence target: source anchors, raw data, statistics, and disclosure needs.

When exact dimensions or policies matter, verify them before rendering.

### Gate 1 — Ground the source

Inspect the paper, relevant sections, caption draft, experiment data, and existing figures. Build a source map before summarizing. Read [analysis-protocol.md](references/analysis-protocol.md) for full-paper intake, figure-portfolio planning, or ambiguous source material.

Classify every planned statement:

- `supported` — directly backed by a source anchor;
- `inferred` — reasonable synthesis not stated directly;
- `hypothesis` — proposed explanation or design expectation;
- `missing` — required evidence is unavailable.

Do not proceed to rendering when a required claim is `missing`.
Allow `inferred` or `hypothesis` content in a final artifact only when the figure itself visibly labels that status and the explanatory content is intentional. Otherwise keep it in planning/audit artifacts and render only supported claims.

For substantial work, save the `RF-GROUND-1.0` output and validate it:

```bash
python "${SKILL_ROOT}/scripts/figure_workbench.py" validate-artifact \
  --kind evidence-ledger evidence-ledger.json --strict
```

### Gate 2 — Select one dominant figure role

Choose the dominant reader question, not merely the paper section:

| Role | Reader question | Default logic |
|---|---|---|
| `motivation` | Why is a new solution needed? | status quo → observed failure → bounded gap |
| `method` | How does the proposed system transform input to output? | input → operations → output |
| `mechanism` | Why should a component change an outcome? | limitation → intervention → intermediate change → outcome |
| `experiment` | Does the evidence support the main claim? | comparison → effect/uncertainty → boundary |
| `ablation` | Which component or choice matters? | controlled removal/change → delta → interpretation |
| `comparison` | How do alternatives differ on meaningful dimensions? | common criteria → contrasts → implication |
| `taxonomy` | How is a space organized? | dimensions → groups → boundaries/exceptions |
| `graphical-abstract` | What is the paper's compact end-to-end story? | context → intervention → principal result → bounded implication |

Use `mixed` only for a deliberate multi-panel figure whose panels have distinct roles. Never hide role confusion under `mixed`. Read [role-playbooks.md](references/role-playbooks.md) for role-specific content, forbidden content, and prompt clauses.

### Gate 3 — Build the claim–evidence map

Write one sentence for the five-second message. Map each claim to a source anchor and each panel to a unique claim. Remove panels that duplicate another panel or serve only decoration.

Apply these tests:

- **necessity** — removing the panel weakens the argument;
- **uniqueness** — no other panel answers the same question;
- **traceability** — a reviewer can locate the supporting source;
- **scope** — the visual strength does not exceed the evidence;
- **counter-reading** — a skeptical reader cannot reasonably infer a stronger claim from the encoding.

### Gate 4 — Author FigureSpec

Use [figure-spec.md](references/figure-spec.md) and the schema at `assets/figure-spec.schema.json`. Prefer a saved `figure-spec.json` for non-trivial work. Create and validate it with:

```bash
python "${SKILL_ROOT}/scripts/figure_workbench.py" new --role method --out figure-spec.json
python "${SKILL_ROOT}/scripts/figure_workbench.py" validate figure-spec.json --strict
```

Define an inventory of components, required text, panels, and relations. Assign every relation a semantic type and, when it carries a scientific claim, a claim ID. Keep spatial layout separate from semantic relations.

### Gate 5 — Route the renderer

Choose the lowest-risk route that satisfies the artifact contract:

- `vector-code` — architecture, pipeline, taxonomy, comparison, or label-heavy diagrams needing editability; use SVG, draw.io, TikZ, Graphviz, Mermaid, or native slide shapes.
- `plot-code` — exact quantitative results; use the user's chosen plotting stack and source data.
- `image-generation` — conceptual illustration, natural objects, textures, or graphical-abstract base art where exact geometry and text are not evidence.
- `hybrid` — deterministic plots/text/geometry plus generated illustration assets, assembled in an editable composition.

For mixed figures, render quantitative panels first and treat them as immutable evidence assets. Read [visual-grammar.md](references/visual-grammar.md) for relation semantics, topology selection, hierarchy, accessibility, and route-specific constraints.

### Gate 6 — Compile the prompt

Read [prompt-system.md](references/prompt-system.md) and use only the stages needed for the task. Compile a validated spec with:

```bash
python "${SKILL_ROOT}/scripts/figure_workbench.py" compile figure-spec.json --out final-prompt.md
```

Keep the prompt contract ordered as:

1. scientific objective;
2. truth and provenance constraints;
3. component/text/relation inventory;
4. panel and layout plan;
5. renderer-specific execution instructions;
6. explicit negative constraints;
7. output requirements;
8. preflight checklist.

Do not replace source-grounded content with style prose. Style must remain a bounded final layer.

### Gate 7 — Inspect and critique the real artifact

Never accept from prompt text alone. Render or open the actual artifact and audit it using [review-protocol.md](references/review-protocol.md). Generate a blank audit record when useful:

```bash
python "${SKILL_ROOT}/scripts/figure_workbench.py" audit-template figure-spec.json --out figure-audit.json
python "${SKILL_ROOT}/scripts/figure_workbench.py" validate-artifact \
  --kind figure-audit figure-audit.json --spec figure-spec.json
```

Check at minimum:

- required components are present and extras are absent;
- every arrow has the correct endpoints, direction, type, and label;
- required text is exact and legible at final size;
- data geometry matches source values and uncertainty;
- visual hierarchy matches claim priority;
- the dominant role remains clear within five seconds;
- colors, shapes, and line styles remain distinguishable without color alone;
- editable/reproducible outputs and disclosure notes exist when required.

### Gate 8 — Revise by delta and stop deliberately

Preserve verified elements. Express each revision as:

```text
target → observed failure → minimal change → preserve → verification
```

Re-render and re-audit affected dimensions. Stop only when all critical gates pass, every required rubric dimension meets threshold, and two consecutive rounds produce no new critical issue. Escalate unresolved evidence gaps to the user rather than polishing around them.

Default to at most three render–audit rounds. Preserve the best scientifically valid artifact after every round and roll back any regression. Escalate when the same major issue fails to improve twice; do not spend additional rounds on style while a scientific or structural issue remains.

## Return useful artifacts

For plan or prompt work, return:

1. concise figure decision and rationale;
2. FigureSpec path or inline spec;
3. compiled prompt or prompt path;
4. unresolved evidence and risks;
5. recommended renderer and editable output;
6. audit result or next verification step.

For build or repair work, also return the rendered artifact, source/editable file, provenance notes, and the completed audit.

## Load references selectively

- Read [analysis-protocol.md](references/analysis-protocol.md) for paper ingestion, source maps, claim extraction, and figure-portfolio decisions.
- Read [figure-spec.md](references/figure-spec.md) whenever creating or editing FigureSpec.
- Read [role-playbooks.md](references/role-playbooks.md) for role-specific scientific stories and negative constraints.
- Read [prompt-system.md](references/prompt-system.md) for exact stage prompts and renderer prompt contracts.
- Read [visual-grammar.md](references/visual-grammar.md) for layout, arrows, panels, typography, color, accessibility, and renderer routing.
- Read [domain-overlays.md](references/domain-overlays.md) when domain notation or integrity rules for AI/ML, agents/control, life sciences, chemistry/materials, robotics, or theory materially affect the figure.
- Read [review-protocol.md](references/review-protocol.md) for scoring, critical failures, revision deltas, and stopping criteria.
- Read [integrity-and-venues.md](references/integrity-and-venues.md) before submission-oriented delivery, quantitative/image panels, or AI-generated assets.
- Read [worked-example.md](references/worked-example.md) only when a concrete bad-to-better walkthrough would help.

## Boundaries

- Do not replace domain experts, statistical review, or author approval.
- Do not infer a publisher's current AI-image policy from venue prestige or prior-year rules.
- Do not imitate a living artist or copy a reference figure's distinctive expression. Extract abstract layout/style attributes and preserve attribution where required.
- Do not expose private paper text, reviewer material, or unpublished data to external services without user authorization.
