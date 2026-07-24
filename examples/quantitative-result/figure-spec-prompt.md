[COMPILED_FROM: RF-COMPILE-2.0 | FIGURESPEC: 2.0 | FIGURE: synthetic-benchmark | SUMMARY_SHA256: 4364960e3ddcd9555ea67b232b26fee5fcfac5c960c7266b0e4939cb879c90df]

# 1. JOB, TARGET, AND CANVAS

Create a publication-quality scientific figure for unspecified.

- Figure ID and role: synthetic-benchmark / experiment
- Medium: paper
- Audience and language: machine-learning researchers / en
- Final canvas or column class: single-column
- Editable source required: true

# 2. REFERENCE-FIGURE CONTRACT

- Reference available: false
- Source: none supplied
- Use mode: none
- Use only these abstract attributes:
- None specified
- Do not copy:
- None specified
- Replace all reference-specific scientific content. The validated inventory below overrides the reference whenever they conflict.

# 3. SCIENTIFIC TOPIC AND PURPOSE

- Source topic: Synthetic benchmark fixture
- Figure role: experiment
- Reader question: How do the two methods compare across three synthetic settings?
- Five-second message: The proposed method is higher in all three synthetic settings, with a small difference in S3.
- Claim boundary: Do not imply statistical significance, causality, or performance beyond S1–S3.
- Source scope: results.csv, source.md anchors Q1–Q5
- Known source limitations: Synthetic values; no significance test was performed.

Render only the supplied scientific inventory. Preserve epistemic qualifiers
and source-bounded scope. Never fill missing evidence with plausible content.

# 4. SCIENTIFIC NARRATIVE

Communicate the following evidence-bounded propositions in order:
- 1. C1 [supported]: The proposed mean is higher than the baseline mean in S1, S2, and S3.
- 2. C2 [supported]: The S3 mean difference is smaller than the S1 and S2 mean differences.

Role-specific narrative directive:
Render values and geometry deterministically from supplied data. Make the primary comparison obvious, show uncertainty and scope, and retain negative or tied evidence.

Claim inventory with provenance:
- C1 [supported/descriptive] The proposed mean is higher than the baseline mean in S1, S2, and S3. | source: results.csv rows S1–S3 | evidence: The proposed means 74.8, 72.1, and 75.4 exceed baseline means 71.2, 68.5, and 75.0.
- C2 [supported/descriptive] The S3 mean difference is smaller than the S1 and S2 mean differences. | source: results.csv rows S1–S3 | evidence: Mean differences are 3.6, 3.6, and 0.4 percentage points.

# 5. CONTENT AND EXACT-TEXT INVENTORY

- Main title: not specified; do not invent one

Must show:
- baseline and proposed means for S1–S3
- one-standard-deviation error bars
- percentage unit
- higher-is-better direction
- three synthetic runs

Semantic entities with stable IDs:
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

# 6. RELATION AND ARROW CONTRACT

- Panel A: R1 | baseline-series → proposed-series | type: comparison | payload/label: shared setting scale | claim: C1

Every connector must preserve its listed source, target, direction, type, and
payload. Never add an unlabeled or scientifically ambiguous arrow.

# 7. GLOBAL LAYOUT AND REGION GEOMETRY

- Topology: single-panel grouped comparison
- Reading order: A
- Hierarchy: method comparison > uncertainty > exact values
- Panel grid: A
- Whitespace: generous
- Maximum label words: 5

Normalized regions:
- No normalized region geometry specified; do not infer percentages from an uninspected reference.

# 8. PER-PANEL COMPOSITION

- Panel A — Synthetic benchmark | question: What are the mean and variability for each method and setting? | claims: C1, C2 | dominance: 1 | form: grouped point-range plot

# 9. VISUAL LANGUAGE

- Background: white
- Palette: #334155, #2563EB
- Color semantics: #334155=baseline; #2563EB=proposed
- Typography: sans-serif; preserve exact glyphs and a clear title/label hierarchy.
- Borders and lines: clean publication plot
- Density and whitespace: generous
- Accessibility: pair color with shape, text, or line style; never rely on color alone.

# 10. EDITABLE CONSTRUCTION CONTRACT

- Renderer mode: plot-code
- Generate geometry from the supplied machine-readable data. Preserve values, units, signs, category order, uncertainty, and missing values. Do not infer significance. Keep labels as live text where the export format permits it. Return plotting source, editable SVG/PDF, and a crisp preview.
- Keep final labels as live editable text.
- Keep core shapes and arrows as vector or native objects with stable IDs.
- Do not flatten the complete figure into one bitmap.
- Deterministic text/numbers: true / true
- Data source: results.csv
- External provider allowed: false
- If AI image generation is used, generate only the approved illustration layer; add exact text, arrows, equations, plots, and values deterministically.

# 11. NEGATIVE PROMPT

Do not include:
- significance stars or p-values
- settings beyond S1–S3
- image-generated numeric geometry
- causal explanation
- truncated scale without disclosure
- 3D bars
- gradient fills
- color-only distinction
- tiny text
- Anything that violates this claim boundary: Do not imply statistical significance, causality, or performance beyond S1–S3.
- Content that changes the dominant experiment role into another figure role
- invented components, values, equations, citations, claims, or causal links
- unlabeled or scientifically ambiguous arrows
- decorative entities that resemble additional scientific components
- fake numbers, pseudo-equations, watermarks, venue logos, or celebratory badges
- wrong, pseudo-, warped, duplicated, or misspelled text
- font substitution, missing glyphs, or corrupted symbols
- rasterized final labels or unreadable microtext
- blurred, fuzzy, melted, ghosted, or partially erased shapes
- soft edges caused by low-resolution upscaling
- overlapping, clipped, truncated, duplicated, or off-canvas labels

# 12. OUTPUT CONTRACT

Return:
- editable master: svg
- paper/vector fallback: pdf
- crisp high-resolution preview at the requested final aspect and size
- font and external-asset manifest when non-system assets are used
- provenance record and completed RF-CRITIQUE-2.0 audit

Report every instruction that could not be rendered faithfully. Do not silently
drop required content or replace missing evidence with plausible content.

# 13. PREFLIGHT BEFORE DELIVERY

- [ ] One dominant reader question is answered and the five-second message is visually dominant.
- [ ] Every required component appears exactly once unless repetition is specified.
- [ ] Every forbidden component is absent.
- [ ] Every arrow has the correct endpoints, direction, semantic type, and payload.
- [ ] Every required label matches the exact-text register and is readable at final size.
- [ ] No text is pseudo-text, misspelled, warped, substituted, clipped, or unintentionally rasterized.
- [ ] No local shape is blurred, fuzzy, melted, ghosted, partially erased, or visibly upscaled.
- [ ] The real export is inspected at final publication size, 100%, and 200% zoom.
- [ ] No label or object overlaps, clips, truncates, or falls off canvas.
- [ ] The editable master retains live text, semantic groups, stable IDs, and editable relations.
- [ ] The claim boundary cannot be misread from arrows, scale, color, or visual emphasis.
