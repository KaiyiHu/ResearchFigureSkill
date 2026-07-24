[COMPILED_FROM: RF-COMPILE-1.0 | FIGURESPEC: 1.0 | FIGURE: synthetic-benchmark]

SCIENTIFIC OBJECTIVE
Role: experiment
Reader question: How do the two methods compare across three synthetic settings?
Five-second message: The proposed method is higher in all three synthetic settings, with a small difference in S3.
Claim boundary: Do not imply statistical significance, causality, or performance beyond S1–S3.

TRUTH AND PROVENANCE CONTRACT
- Render only the supplied scientific inventory.
- Do not invent or strengthen claims, values, equations, labels, or relations.
- Preserve epistemic qualifiers and source-bounded scope.
- If an instruction cannot be rendered faithfully, omit decoration and report the unresolved item; never substitute plausible content.
- Source scope: results.csv, source.md anchors Q1–Q5
- Known source limitations: Synthetic values; no significance test was performed.

CLAIM INVENTORY
- C1 [supported/descriptive] The proposed mean is higher than the baseline mean in S1, S2, and S3. | source: results.csv rows S1–S3 | evidence: The proposed means 74.8, 72.1, and 75.4 exceed baseline means 71.2, 68.5, and 75.0.
- C2 [supported/descriptive] The S3 mean difference is smaller than the S1 and S2 mean differences. | source: results.csv rows S1–S3 | evidence: Mean differences are 3.6, 3.6, and 0.4 percentage points.

COMPONENT AND REQUIRED-TEXT INVENTORY
Must show:
- baseline and proposed means for S1–S3
- one-standard-deviation error bars
- percentage unit
- higher-is-better direction
- three synthetic runs

Semantic entities:
- Panel A: baseline-series | kind: baseline | exact label: Baseline
- Panel A: proposed-series | kind: proposed | exact label: Proposed

Required exact text:
- Baseline
- Proposed
- Score (%)
- Mean ± 1 SD
- n = 3 runs

Optional; remove before compressing required content:
- direct mean labels

RELATION INVENTORY
- Panel A: baseline-series → proposed-series | type: comparison | label: shared setting scale | claim: C1

PANEL AND LAYOUT PLAN
- Panel A — Synthetic benchmark | question: What are the mean and variability for each method and setting? | claims: C1, C2 | dominance: 1 | form: grouped point-range plot
- Topology: single-panel grouped comparison
- Reading order: A
- Hierarchy: method comparison > uncertainty > exact values
- Panel grid: A
- Whitespace: generous
- Maximum label words: 5

ROLE-SPECIFIC DIRECTIVE
Render values and geometry deterministically from supplied data. Make the primary comparison obvious, show uncertainty and scope, and retain negative or tied evidence.

RENDERER-SPECIFIC DIRECTIVE
Mode: plot-code
Generate geometry from the supplied machine-readable data. Preserve values, units, signs, category order, uncertainty, and missing values. Do not infer significance. Return plotting source, editable SVG/PDF, and a preview.

STYLE BOUNDS
- Background: white
- Palette: #334155, #2563EB
- Color semantics: #334155=baseline; #2563EB=proposed
- Font: sans-serif
- Line style: clean publication plot
- Avoid: 3D bars, gradient fills, color-only distinction, tiny text
- Do not rely on color alone for any scientific distinction.

FORBIDDEN CONTENT
- significance stars or p-values
- settings beyond S1–S3
- image-generated numeric geometry
- causal explanation
- truncated scale without disclosure
- No decorative entity may resemble an additional scientific component.
- No unlabeled arrow, pseudo-equation, fake number, fake citation, watermark, venue logo, or celebratory badge.

OUTPUT CONTRACT
- Medium/venue: paper / unspecified
- Audience/language: machine-learning researchers / en
- Final size: single-column
- Preferred/fallback format: svg / pdf
- Editable required: true
- Deterministic text/numbers: true / true
- Data source: results.csv
- External provider allowed: false

PREFLIGHT CHECKLIST
[ ] Every required component appears exactly once unless repetition is specified.
[ ] Every relation has correct endpoints, direction, type, and label.
[ ] Every required label is exact and legible at final size.
[ ] No extra scientific entity, value, or claim appears.
[ ] Visual hierarchy makes the five-second message dominant.
[ ] The claim boundary cannot be misread from arrows, scale, or color.
