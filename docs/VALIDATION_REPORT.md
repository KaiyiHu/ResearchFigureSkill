# Validation report

> Snapshot: 2026-07-24. This report evaluates the repository at version 1.0.0.
> It is a software and workflow validation report, not evidence that every
> future figure will be scientifically correct without author review.

## What was evaluated

The checks cover four layers:

1. **Package integrity** — Skill metadata, reference links, schemas, examples,
   and bundled resources resolve correctly.
2. **Contract behavior** — invalid evidence, relations, renderer choices, and
   audit verdicts fail in predictable ways.
3. **Determinism** — a valid FigureSpec compiles to the same prompt and exact
   numeric/text requirements survive compilation.
4. **Fresh-context usability** — independent agents used only the installed
   Skill and synthetic source material to complete representative tasks.

## Automated regression suite

Command:

```bash
python -m unittest discover -s tests -v
```

Result: **24/24 tests passed**.

| Test family | Guardrail exercised |
|---|---|
| Schema and template | Valid JSON, unknown-field rejection |
| Evidence status | Anchors for supported claims; missing claims blocked |
| Epistemic status | Inferred/hypothesis content needs a visible label |
| Relation semantics | Known endpoints; causal and causal-hypothesis rules |
| Renderer routing | Quantitative and exact-text work rejected from pure image generation |
| Compilation | Invalid/provisional specs blocked; deterministic output; Unicode and exact values preserved |
| Audit | Expected inventory mapping; incomplete passing verdict rejected |
| Repository | Skill resources and repository-relative Markdown links resolve |

Repository checks:

```bash
python skills/research-figure/scripts/figure_workbench.py check-links --strict
python /path/to/skill-creator/scripts/quick_validate.py skills/research-figure
```

Result: **0 errors, 0 warnings; Skill package valid**.

## Independent forward tests

Each test began in a fresh context without access to the project-development
discussion. The evaluator received the installable Skill plus a small synthetic
source package and was asked to produce or audit artifacts.

### Mechanism figure

Input contained:

- one directly implemented threshold filter;
- one merely hypothesized downstream mechanism;
- one observed proxy outcome;
- an explicit source limitation.

Expected behavior:

- keep the implemented operation supported;
- encode the proposed mechanism as `causal-hypothesis`, not established cause;
- visibly label its epistemic status;
- preserve the source limitation.

Result: the evidence ledger, FigureSpec, and compiled prompt all passed strict
validation and preserved the boundary between observation and hypothesis.

### Quantitative result figure

Input contained exact means, standard deviations, one negative value, and no
significance test.

Expected behavior:

- select `plot-code`;
- preserve every value and `mean ± 1 SD`;
- keep the negative value;
- prohibit invented significance.

Result: the FigureSpec passed strict validation and the compiled prompt retained
all numeric and statistical constraints.

### Existing-figure critique

The synthetic artifact deliberately contained:

- a reversed arrow;
- one extra unsupported component;
- a fabricated percentage;
- missing payload labels.

Expected behavior:

- reconstruct the minimum expected inventory;
- report reader inferences before inventory diffs;
- return `revise`;
- propose minimal deltas that preserve valid content.

Result: the FigureSpec and completed audit passed strict validation while
correctly blocking acceptance and identifying all planted failures.

## Known limits

- The workbench validates semantic contracts; it does not prove a source claim
  is true or substitute for domain review.
- Visual inspection still requires opening the actual rendered artifact at its
  final size.
- Venue and publisher policies must be rechecked from current official sources.
- Downstream renderers may introduce provider-specific errors after compilation.
- Broader benchmark comparison will require a public, licensed paper-to-figure
  corpus with blinded human ratings.

## Reproducing the shipped checks

```bash
python -m unittest discover -s tests -v
python skills/research-figure/scripts/figure_workbench.py check-links --strict

while IFS= read -r -d '' spec; do
  python skills/research-figure/scripts/figure_workbench.py \
    validate "$spec" --strict
done < <(find examples -name '*spec.json' -print0)
```
