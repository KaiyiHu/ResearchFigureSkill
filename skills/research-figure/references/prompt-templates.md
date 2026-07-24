# Fixed scientific-figure prompt templates

Use these templates after reading the allowed source and writing
`paper-summary.md`. Replace every `{{PLACEHOLDER}}`; delete optional lines that
do not apply. Keep the final prompt compact enough for a renderer to follow.

## Shared filling rules

- Use only claims, entities, numbers, and relations supported by the summary.
- Keep exact labels short. Put long explanation in the caption, not the image.
- List arrows explicitly. Never say “connect appropriately.”
- Use the user's requested language for visible text.
- If dimensions are unspecified, use a provisional 16:9 landscape canvas,
  approximately 1800 × 1000 px for review.
- If no reference image exists, write `Reference: none` and design an original
  composition.
- If a reference exists, describe only abstract reusable attributes.
- Default output is editable SVG with live text plus PNG preview.

---

## Motivation prompt

```text
Create a publication-quality scientific MOTIVATION figure.

1. JOB AND CANVAS
- Paper/topic: {{PAPER_TITLE_OR_TOPIC}}
- Audience: {{AUDIENCE}}
- Visible-text language: {{LANGUAGE}}
- Canvas: {{CANVAS_AND_ASPECT_RATIO}}
- Output: editable SVG with live text and separate vector objects, plus a crisp
  PNG preview.

2. SOURCE-BOUNDED PURPOSE
- Research problem: {{RESEARCH_PROBLEM}}
- Current practice or assumption: {{STATUS_QUO}}
- Observed limitation or blind spot: {{OBSERVED_LIMITATION}}
- Bounded research need: {{RESEARCH_NEED}}
- Five-second message: {{FIVE_SECOND_MESSAGE}}
- Do not imply: {{CLAIM_BOUNDARY}}

This is a motivation figure, not a method pipeline. Make the limitation and
research need visually dominant. Do not reveal the full architecture, training
procedure, or result leaderboard.

3. CONTENT INVENTORY
- Main title: {{SHORT_TITLE}}
- Message block 1 — status quo:
  {{STATUS_QUO_BLOCK}}
- Message block 2 — failure or blind spot:
  {{LIMITATION_BLOCK}}
- Message block 3 — bounded need:
  {{NEED_BLOCK}}
- Optional supporting evidence:
  {{OPTIONAL_EXACT_EVIDENCE_OR_NONE}}
- Exact visible labels:
  {{EXACT_LABEL_LIST}}
- Boundary/qualifier labels:
  {{BOUNDARY_LABEL_LIST}}

4. RELATIONS
Use arrows only for source-supported direction, time, or dependence.
{{EXPLICIT_RELATION_LIST_OR_NONE}}

Do not connect independent problems as sequential method stages. Use alignment,
contrast, numbering, or whitespace when an arrow would overstate meaning.

5. LAYOUT
- Reading direction: {{READING_DIRECTION}}
- Title band: {{TITLE_POSITION}}
- Main regions: {{REGION_PLAN}}
- Dominant region: {{DOMINANT_REGION}}
- Approximate region ratios or reference-derived layout: {{REGION_RATIOS_OR_NONE}}
- Keep generous whitespace and avoid connector crossings.

6. VISUAL LANGUAGE
- Reference: {{REFERENCE_OR_NONE}}
- Permitted abstract reference attributes: {{REFERENCE_ATTRIBUTES_OR_NONE}}
- Background: {{BACKGROUND}}
- Semantic palette: {{PALETTE_AND_MEANING}}
- Typography: clean sans-serif with a clear title/body/qualifier hierarchy.
- Shapes: flat 2D vector forms, consistent stroke weight, restrained corner
  radius, no decorative modules.
- Accessibility: pair every color distinction with text, shape, number, or line
  style.

7. EDITABLE CONSTRUCTION
- Keep all final text as live editable text.
- Keep shapes, borders, and connectors as separate vector objects.
- Preserve exact spelling, symbols, values, and units.
- If illustrative AI imagery is used, make that layer text-free and keep it
  separate from deterministic labels and arrows.
- Do not flatten the full figure into one bitmap.

8. NEGATIVE PROMPT
No invented claim, module, value, equation, citation, causal link, universal
claim, legal or clinical conclusion. No full method architecture, training
loop, leaderboard, result badge, pseudo-text, wrong glyph, substituted symbol,
blur, fuzzy or melted shape, ghosting, overlap, clipping, off-canvas object,
microscopic label, low-resolution upscaling, glossy 3D icon, corporate
dashboard, futuristic interface, watermark, or logo.

9. OUTPUT
Return:
- {{OUTPUT_BASENAME}}.svg — editable master with live text;
- {{OUTPUT_BASENAME}}.png — review preview at the declared canvas size.

10. PREFLIGHT
- The viewer can state the research need within five seconds.
- Every visible scientific statement is supported by the supplied summary.
- Every required label is exact and readable.
- No arrow implies a stronger relation than the source.
- No blur, fuzzy edge, overlap, or clipping is visible at 100% or 200%.
- The SVG remains editable and is not a full-canvas bitmap.
```

---

## Pipeline prompt

```text
Create a publication-quality scientific METHOD / PIPELINE figure.

1. JOB AND CANVAS
- Paper/topic: {{PAPER_TITLE_OR_TOPIC}}
- Audience: {{AUDIENCE}}
- Visible-text language: {{LANGUAGE}}
- Canvas: {{CANVAS_AND_ASPECT_RATIO}}
- Output: editable SVG with live text and separate vector objects, plus a crisp
  PNG preview.

2. SOURCE-BOUNDED PURPOSE
- Input type: {{INPUT_TYPE}}
- Output type: {{OUTPUT_TYPE}}
- Core transformation: {{CORE_TRANSFORMATION}}
- Novel or focal stage: {{FOCAL_STAGE}}
- Five-second message: {{FIVE_SECOND_MESSAGE}}
- Do not imply: {{CLAIM_BOUNDARY}}

This is a method pipeline, not a motivation or results infographic. Show what
happens next, to which object, and through which handoff. Do not add performance
badges or unsupported feedback loops.

3. STAGE INVENTORY
Use 3–7 visible stages. Each stage label should be a short noun; its operation
should be a short verb phrase.

{{STAGE_TABLE_WITH_ID_LABEL_INPUT_OPERATION_OUTPUT}}

Required exact visible labels:
{{EXACT_LABEL_LIST}}

Training-only, inference-only, fixed, or deterministic annotations:
{{SCOPE_ANNOTATIONS_OR_NONE}}

4. ARROW AND HANDOFF CONTRACT
Write one line per connector:

source ID → target ID | payload or control label | relation meaning

{{EXPLICIT_ARROW_LIST}}

Do not add an arrow without named endpoints and meaning. Do not add feedback,
iteration, branching, or fusion unless the source explicitly supports it.

5. LAYOUT
- Reading direction: {{READING_DIRECTION}}
- Title band: {{TITLE_POSITION}}
- Main topology: {{LINEAR_BRANCH_LOOP_OR_PARALLEL}}
- Stage placement: {{STAGE_PLACEMENT}}
- Optional inset or lane: {{INSET_OR_LANE_OR_NONE}}
- Approximate region ratios or reference-derived layout: {{REGION_RATIOS_OR_NONE}}
- Keep arrow routes short, unambiguous, and free of crossings.

6. VISUAL LANGUAGE
- Reference: {{REFERENCE_OR_NONE}}
- Permitted abstract reference attributes: {{REFERENCE_ATTRIBUTES_OR_NONE}}
- Background: {{BACKGROUND}}
- Semantic palette: {{PALETTE_AND_MEANING}}
- Typography: clean sans-serif with clear stage, payload, and qualifier levels.
- Shapes: consistent flat 2D vector modules; use shape or labels in addition to
  color.
- Make the focal stage dominant without shrinking other required labels.

7. EDITABLE CONSTRUCTION
- Keep final text, numbers, equations, and payload labels live and editable.
- Keep every stage and arrow as a separate vector/native object.
- Preserve exact arrow endpoints, direction, labels, and branch conditions.
- Render exact plots or quantitative geometry from data, never with an image
  model.
- If illustrative AI assets are used, keep them text-free and separate.
- Do not flatten the full figure into one bitmap.

8. NEGATIVE PROMPT
No invented stage, branch, feedback loop, value, equation, dataset, baseline,
causal link, or result claim. No unlabeled arrow, reversed endpoint, ambiguous
junction, pseudo-text, wrong glyph, substituted symbol, blur, fuzzy or melted
shape, ghosting, overlap, clipping, off-canvas object, microscopic label,
low-resolution upscaling, decorative AI brain, glossy 3D icon, corporate
dashboard, futuristic interface, watermark, or logo.

9. OUTPUT
Return:
- {{OUTPUT_BASENAME}}.svg — editable master with live text;
- {{OUTPUT_BASENAME}}.png — review preview at the declared canvas size.

10. PREFLIGHT
- A reader can follow input → stages → output without reading the paper.
- Every stage, label, and handoff exists in the supplied summary.
- Every arrow has the correct source, target, direction, and payload.
- Exact text is readable and contains no pseudo-text or missing glyphs.
- No blur, fuzzy edge, overlap, or clipping is visible at 100% or 200%.
- The SVG remains editable and is not a full-canvas bitmap.
```
