# Figure audit and revision protocol

Audit the rendered artifact, not the elegance of its prompt. Use a conjunctive gate: a serious failure in one required dimension cannot be compensated by high aesthetics elsewhere.

## Contents

1. Audit inputs
2. Inventory diff
3. Rubric
4. Critical failures
5. Role-specific adversarial checks
6. Cross-cutting failure modes
7. Revision deltas
8. Stopping conditions
9. Audit output

## 1. Audit inputs

Require as many of these as the mode supports:

- source map or relevant source excerpts;
- validated FigureSpec;
- compiled prompt or source code;
- actual final-size artifact;
- source data for quantitative panels;
- previous artifact and audit for revisions;
- target venue/export contract.

If the artifact cannot be opened or inspected, return `blocked`; do not infer quality from generation logs.

For complex or high-stakes figures, run four focused passes, preferably with fresh context:

1. **Scientific critic** — reader inferences, evidence scope, causal calibration.
2. **Graph critic** — node/component/edge/text inventory diff.
3. **Visual critic** — hierarchy, density, reading order, final-size legibility.
4. **Technical critic** — numeric binding, OCR/exact text, export, accessibility, editability, and provenance.

Merge findings by stable IDs. Do not let the renderer be the only critic of its own output, and do not collapse the four passes into a single average score.

## 2. Inventory diff

Extract from the artifact:

```yaml
panels:
components:
required_text:
relations:
numeric_marks:
legend_semantics:
generated_or_external_assets:
```

Compare to FigureSpec:

- missing required item;
- extra scientific-looking item;
- duplicated item;
- corrupted label;
- wrong panel;
- wrong relation endpoint/direction/type;
- changed number/unit/order/uncertainty;
- style token that changes scientific interpretation.

Use stable IDs or exact visible locations. “The layout feels off” is not actionable.

## 3. Rubric

Score each dimension independently from 1 to 5.

### Scientific fidelity

- **5** — every visible claim and qualifier matches grounded source scope.
- **4** — no false claim; one minor qualifier could be clearer.
- **3** — ambiguous implication or unsupported but non-central detail.
- **2** — central overclaim, omitted boundary, or unverifiable evidence.
- **1** — fabricated or materially false scientific content.

### Structural correctness

Evaluate components, arrows, text, panel membership, and numeric geometry together.

- **5** — complete and exact inventory; every relation is correct.
- **4** — non-semantic alignment issue only.
- **3** — one recoverable relation/text ambiguity.
- **2** — missing/reversed relation or corrupted required component.
- **1** — structure communicates a different method or result.

### Role purity

- **5** — reader question and figure role are immediate and focused.
- **4** — one removable role-adjacent detail.
- **3** — secondary role competes with the main message.
- **2** — WHY/HOW/WHETHER are conflated.
- **1** — no identifiable scientific job.

### Message clarity

- **5** — five-second message is visible at thumbnail scale.
- **4** — message emerges quickly with one minor distraction.
- **3** — correct but requires reading most labels.
- **2** — hierarchy suggests the wrong takeaway.
- **1** — main message is absent or contradicted.

### Readability

Check final physical size, not enlarged view.

- **5** — all required text, symbols, and paths are legible.
- **4** — minor supporting annotation strain.
- **3** — several labels require zoom.
- **2** — required labels or paths are difficult to read.
- **1** — semantic content is unreadable.

### Accessibility

- **5** — color-independent distinctions, contrast, line/shape redundancy, meaningful reading order.
- **4** — one minor non-critical accessibility issue.
- **3** — some categories rely mainly on color.
- **2** — central distinction fails grayscale or common color-vision conditions.
- **1** — inaccessible encoding changes the scientific reading.

### Editability and reproducibility

- **5** — editable source, deterministic text/data, provenance, and rerun path exist.
- **4** — one non-critical asset is flattened.
- **3** — editable handoff exists but provenance or source data is incomplete.
- **2** — only raster output or non-reproducible manual edits.
- **1** — artifact cannot be safely corrected or regenerated.

## 4. Critical failures

Any one blocks acceptance:

1. fabricated, altered, or unsupported central content;
2. missing required component or label;
3. reversed/wrong arrow or relation semantics;
4. causal visual stronger than evidence;
5. wrong number, sign, unit, category, axis, scale, or uncertainty;
6. required text unreadable or corrupted;
7. visual hierarchy communicates a materially stronger/different claim;
8. confidential/private material exposed without authorization;
9. prohibited or undisclosed asset usage for the target venue;
10. final artifact cannot be inspected.

Do not downgrade a critical failure because it is easy to repair.

## 5. Role-specific adversarial checks

### Motivation

- Does the visual criticize prior work more broadly than evidence permits?
- Are independent failures falsely connected as stages?
- Has the proposed full method displaced the problem?

### Method

- Do arrows carry the correct object/control signal?
- Are training and inference paths confused?
- Does a decorative icon resemble an unimplemented module?

### Mechanism

- Is the intermediate variable observable, defined, or clearly hypothesized?
- Does the artifact convert association into causality?
- Is outcome improvement shown without a supported link?

### Experiment

- Do plot marks reproduce machine-readable values?
- Are axes, baselines, error definitions, and sample scope honest?
- Are negative or tied results hidden?

### Ablation

- Is exactly one controlled factor changed per contrast?
- Are interactions treated honestly?
- Does “importance” exceed the tested setting?

### Comparison/taxonomy

- Are criteria applied consistently?
- Is “not reported” distinguished from “absent”?
- Does geometry imply unsupported similarity or completeness?

### Graphical abstract

- Is the result exact and bounded?
- Has simplification invented a mechanism?
- Are decorative metaphors distinguishable from evidence?

## 6. Cross-cutting failure modes

| Failure | Owner layer | Required response |
|---|---|---|
| Motivation rendered as a pipeline | figure intent | split roles or change topology |
| WHY, HOW, and WHETHER compete | figure portfolio | split figures/panels |
| Association shown as causality | semantic spec | downgrade edge and label status |
| Author interpretation shown as mechanism | evidence ledger | correct epistemic status |
| Train and inference flows are mixed | semantic spec | separate scope/lanes |
| Size/area implies an invented magnitude | layout spec | equalize or bind a real scale |
| Module, number, acronym, or equation is auto-completed | source/spec | remove; mark missing |
| Main message disappears under full-paper detail | figure intent | remove secondary content |
| Axis, dual scale, smoothing, or uncertainty misleads | plot/data spec | repair code and disclose |
| Ablation implies independent contribution | claim boundary | narrow interpretation |
| Qualitative examples are cherry-picked | evidence/data | disclose selection; add failures |
| Image model corrupts text or arrows | renderer | use deterministic overlay/vector |
| Reference style transfers scientific content | source/style boundary | remove copied semantics |
| A global score hides a blocker | audit policy | apply conjunctive gate |
| Renderer and critic repeat the same assumption | audit context | inspect artifact as reader first |
| Critique accumulation bloats the prompt | revision layer | issue minimal deltas only |
| Later iteration regresses a correct figure | revision control | restore best-so-far |
| Only PNG is delivered | output contract | add editable source and provenance |
| Fixed DPI/palette is called venue compliance | venue check | verify official current rules |
| Caption or alt text merely repeats labels | delivery | describe takeaway and relations |

## 7. Revision deltas

Write each delta as:

```yaml
target: relation:R3
observed_failure: Arrow points verifier → retriever, but the spec requires retriever → verifier for candidate evidence.
minimal_change: Reverse R3 and retain label "candidates".
preserve:
  - positions of verifier and retriever
  - all other relations
  - typography and palette
rationale: FigureSpec panel B, relation R3; source anchor §3.2.
verification: Arrowhead terminates at verifier and label remains exact.
```

Prioritize:

1. truth/structure;
2. role/message;
3. readability/accessibility;
4. style polish.

Prefer local editable patches. Regenerate only when the composition itself is invalid or local editability is unavailable.

After each accepted audit state, save it as `best-so-far` with its spec, artifact, scores, and unresolved issues. Compare the next artifact against that state. Roll back when a revision:

- introduces a new critical failure;
- lowers scientific fidelity or structural correctness;
- corrupts a previously exact label/value/relation;
- fixes style by weakening the scientific message.

## 8. Stopping conditions

Default maximum: **three render–audit rounds**.

Stop successfully when:

- no critical failure exists;
- scientific fidelity and structural correctness score 5;
- every other required dimension meets FigureSpec threshold;
- final-size inspection passes;
- no new critical issue appears in the last two audited states.

Escalate when:

- the same major issue does not improve in two consecutive rounds;
- repair requires missing scientific evidence;
- the renderer repeatedly corrupts exact text/relations;
- improvement requires a materially different figure decision;
- privacy, policy, licensing, or author choice blocks safe completion.

Do not spend the iteration budget on minor polish while a major issue remains.
Reaching the round limit means “needs escalation,” not “publication-ready.”

## 9. Audit output

Use the JSON shape generated by:

```bash
python "${SKILL_ROOT}/scripts/figure_workbench.py" audit-template figure-spec.json --out figure-audit.json
```

Return:

- verdict: `pass`, `revise`, or `blocked`;
- per-dimension scores;
- observable critical/major/minor findings;
- source/spec-linked revision deltas;
- unresolved evidence;
- comparison to the prior audited state.

Never return only a global aesthetic score.
