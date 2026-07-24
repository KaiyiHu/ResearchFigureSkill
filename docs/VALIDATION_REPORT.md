# Validation report

> Snapshot: 2026-07-25. This report evaluates repository version 2.0.0. It
> validates the workflow and deterministic contracts; it does not replace
> author or domain-expert review of a future scientific figure.

## What was evaluated

The release is checked at six layers:

1. **Package integrity** — Skill metadata, links, schemas, templates, examples,
   and bundled scripts resolve.
2. **Full-source workflow** — the Skill requires a detailed, evidence-anchored
   summary and section-coverage record before figure-role selection.
3. **Prompt compilation** — FigureSpec compiles deterministically in the fixed
   `J + R + S + N + C + E + L + V + D + X + O + Q` order.
4. **Prompt coverage** — unresolved placeholders, missing exact text, missing
   typed relations, missing negative constraints, and missing editable-output
   requirements are rejected.
5. **Artifact QA** — audit records require final-size, 100%, and 200%
   inspection and explicitly record font/glyph, blur, clipping, overlap,
   rasterization, and resolution defects.
6. **Regression usability** — synthetic fixtures preserve evidence boundaries,
   route renderers by risk, and exclude unsupported interfaces and feedback.

## Automated regression suite

Command:

```bash
python3 -m unittest discover -s tests -v
```

Result: **42/42 tests passed**.

| Test family | Guardrail exercised |
|---|---|
| Schema and templates | Valid JSON, unknown-field rejection, full-summary structure, section depth and diversity |
| Evidence status | Anchors for supported claims; missing claims blocked |
| Epistemic status | Inference/hypothesis content requires a visible label |
| Relation semantics | Known endpoints; causal and causal-hypothesis rules |
| Reference contract | Allowlisted abstract attributes; unsafe replication language blocked; explicit copy boundary; valid normalized regions |
| Renderer routing | Quantitative/exact-text work rejected from pure image generation |
| Prompt compilation | Determinism, fixed section order, Unicode, exact values, optical negatives |
| Prompt lint | Canonical summary/spec binding, placeholders, exact text, relations, negatives, references, and editability |
| Audit-record validation | Passing verdict requires a matching file signature/hash, recorded optical inspections, exact inventory, and empty defect registers |
| SVG inspection | Visible exact text, transforms, blur filters, raster native dimensions, semantic IDs/geometry, glyph hazards |
| Repository | Skill resources and repository-relative Markdown links resolve |

Additional package and fixture checks:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py \
  skills/research-figure

python3 skills/research-figure/scripts/figure_workbench.py \
  check-links --strict

python3 skills/research-figure/scripts/figure_workbench.py \
  validate examples/claimcrawl/motivation-spec.json --strict

python3 skills/research-figure/scripts/figure_workbench.py \
  lint-prompt examples/claimcrawl/motivation-spec-prompt.md \
  --spec examples/claimcrawl/motivation-spec.json \
  --summary examples/claimcrawl/paper-summary.md --strict
```

Result: package valid; **0 errors and 0 warnings** across link, FigureSpec, and
compiled-prompt checks.

## End-to-end forward test

A fresh synthetic source was processed through detailed summary, evidence
ledger, role decision, FigureSpec 2.0, canonical prompt compilation, editable
SVG construction, PNG export, 100%/200% review, completed audit, and
provenance hashing. Final strict validation returned zero errors and warnings
for the ledger, spec, prompt, SVG, and completed audit; all recorded file
hashes matched. This forward test was kept outside the repository so it does
not become a hand-tuned regression fixture.

## Regression cases

### Detailed summary and Figure 1 role split

The ClaimCrawl fixture contains motivation evidence, a separate high-level
method description, and no empirical results. The checked-in
`paper-summary.md` records the problem, method boundary, absent experiments,
limitations, terminology, section coverage, and figure portfolio.

Expected and observed behavior:

- Figure 1 is classified as motivation, not a method pipeline.
- The method figure is kept separate.
- No result panel, benchmark value, significance claim, or universal guarantee
  is generated.
- A controller-to-selector feedback path is excluded because the source does
  not state it.

### Quantitative result routing

The quantitative fixture contains exact means, standard deviations, and no
significance test.

Expected and observed behavior:

- renderer mode is `plot-code`;
- exact values and `Mean ± 1 SD` survive compilation;
- image-generated numeric geometry is forbidden;
- significance marks and causal explanations are forbidden.

### Reference-driven prompt compilation

The regression suite injects a supplied-reference contract and normalized
region geometry into a valid FigureSpec.

Expected and observed behavior:

- permitted abstract attributes enter the prompt;
- reference-specific labels and distinctive icons remain prohibited;
- region percentages survive compilation exactly;
- a missing source, empty copy boundary, or zero-size region is rejected.

### Optical and editable artifact gates

A passing audit is rejected until the real artifact, final size, 100%, 200%,
editable source, and live text are all marked inspected. Any retained
font/glyph error, blurred or soft region, overlap/clipping issue, or
rasterization/resolution issue blocks a `pass` verdict.

The deterministic SVG regression checks that:

- exact required labels must exist as live `<text>` nodes;
- hidden or off-canvas text cannot satisfy exact-label coverage;
- editable entities and relations retain their FigureSpec IDs;
- declared fonts and positive font sizes are structurally inspectable;
- blur/filter effects are surfaced;
- duplicate IDs and replacement/tofu glyph hazards are surfaced;
- embedded raster native dimensions are read when possible and placed
  upscaling is rejected.

These structural checks complement rather than replace visual inspection of
the rendered artifact.

## Known limits

- The workbench checks evidence and visual contracts; it cannot prove a source
  claim is scientifically true.
- Static SVG inspection cannot detect every perceptual defect, font
  substitution at a downstream publisher, or misleading visual emphasis.
- PPTX, draw.io, and PDF masters do not have bundled static inspectors; they
  require format-native source/export inspection recorded in the audit.
- Final physical effective PPI and local image-generation defects still require the
  recorded final-size/100%/200% artifact inspection.
- Venue and publisher policies must be rechecked from current official
  sources.
- Downstream renderers can introduce new errors after a prompt passes lint.
- General benchmark claims require a public, licensed paper-to-figure corpus
  and blinded human ratings.

## Reproduce the shipped checks

```bash
python3 -m unittest discover -s tests -v
python3 skills/research-figure/scripts/figure_workbench.py check-links --strict
python3 /path/to/skill-creator/scripts/quick_validate.py skills/research-figure

while IFS= read -r -d '' spec; do
  python3 skills/research-figure/scripts/figure_workbench.py \
    validate "$spec" --strict
done < <(find examples -name '*spec.json' -print0)
```
