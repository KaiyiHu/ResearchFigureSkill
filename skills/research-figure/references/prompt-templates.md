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
- If no reference image exists, write `Reference: none — use the default
  hand-drawn academic infographic style`.
- If a reference exists, call it the **PRIMARY visual and compositional
  reference** and enumerate the panel topology, border treatment, lettering,
  icon language, arrow rhythm, density, and palette behavior that must be
  preserved.
- Never let a generic house style override the declared reference style.
- Replace the reference's scientific content, text, numbers, logos, and
  source-specific symbols; a reference is not evidence.
- With a visual reference, default to image-first rendering for the
  style-faithful PNG, followed by an editable SVG companion when requested.
- Without a reference, default to a hand-drawn academic infographic rather
  than a corporate card dashboard.

---

## Motivation prompt

```text
Create a publication-quality scientific MOTIVATION figure.

1. JOB AND CANVAS
- Paper/topic: {{PAPER_TITLE_OR_TOPIC}}
- Audience: {{AUDIENCE}}
- Visible-text language: {{LANGUAGE}}
- Canvas: {{CANVAS_AND_ASPECT_RATIO}}
- Rendering order: {{IMAGE_FIRST_OR_VECTOR_FIRST_AND_WHY}}
- Output: a style-faithful PNG plus an editable SVG companion with live text,
  separate arrows, borders, and labels. If any illustration remains raster,
  disclose it instead of calling the whole SVG fully editable.

2. REFERENCE-LOCKED VISUAL CONTRACT
- Reference: {{PRIMARY_REFERENCE_OR_NONE}}
- Reference role: PRIMARY visual and compositional reference; not scientific
  evidence.
- Mandatory visual attributes:
  {{REFERENCE_LOCKED_ATTRIBUTES_OR_DEFAULT_HANDDRAWN_PROFILE}}
- Content that must be replaced:
  {{REFERENCE_CONTENT_TO_REPLACE}}
- Explicit instruction: preserve the declared visual design system. Do not
  redesign it into a modern corporate diagram, SaaS dashboard, polished
  geometric vector plate, or generic card grid.

If no reference exists, use this default profile: white paper-like background;
slightly irregular black ink linework; colored dashed rounded panel borders;
large colored handwritten-looking section titles; readable black handwritten
body labels; concrete scientific doodle icons; sparse pastel highlights;
curved arrows, brackets, callouts, and dense but legible scientific content.

3. SOURCE-BOUNDED PURPOSE
- Research problem: {{RESEARCH_PROBLEM}}
- Current practice or assumption: {{STATUS_QUO}}
- Observed limitation or blind spot: {{OBSERVED_LIMITATION}}
- Bounded research need: {{RESEARCH_NEED}}
- Five-second message: {{FIVE_SECOND_MESSAGE}}
- Do not imply: {{CLAIM_BOUNDARY}}

This is a motivation figure, not a method pipeline. Make the limitation and
research need visually dominant. Do not reveal the full architecture or
training procedure. Use only the small amount of quantitative evidence needed
to make the motivation concrete.

4. CONTENT INVENTORY
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

5. RELATIONS
Use arrows only for source-supported direction, time, or dependence.
{{EXPLICIT_RELATION_LIST_OR_NONE}}

Do not connect independent problems as sequential method stages. Use alignment,
contrast, numbering, or whitespace when an arrow would overstate meaning.

6. LAYOUT
- Reading direction: {{READING_DIRECTION}}
- Title placement: {{TITLE_POSITION_OR_PANEL_TITLES_ONLY}}
- Main regions: {{REGION_PLAN}}
- Dominant region: {{DOMINANT_REGION}}
- Approximate region ratios or reference-derived layout: {{REGION_RATIOS_OR_NONE}}
- Match the reference's information density and asymmetry. Prefer a few large
  dashed narrative regions over equal-width cards. Avoid connector crossings.

7. VISUAL LANGUAGE
- Background: white or warm white paper, not a gray application canvas.
- Semantic palette: {{PALETTE_AND_MEANING}}. Keep main text and object outlines
  black; use color mainly for section titles, dashed borders, arrows, selected
  evidence, and small emphasis areas.
- Typography: handwritten-looking academic lettering. Section titles are large
  and colored; body labels are black, readable, mildly irregular, and compact.
  For editable SVG use an available handwriting family such as Chalkboard,
  Comic Sans MS, Marker Felt, or a metrically similar fallback. Do not default
  to Inter/Arial/Helvetica corporate typography.
- Shapes: thin black hand-drawn outlines with slightly irregular strokes.
  Prefer concrete scientific cartoons—documents, corpus/database, search,
  ranked lists, targets, checklists, evidence cells—over abstract UI symbols.
- Panels: mostly white interiors with colored dashed rounded boundaries. Use
  pastel fill only for selected documents, evidence cells, targets, and small
  callouts.
- Density: scientific illustrations and annotations should occupy roughly
  75–85% of the useful canvas, while remaining legible.
- Accessibility: pair every color distinction with text, shape, number, or line
  style.

8. EDITABLE CONSTRUCTION
- Keep all final text as live editable text.
- Keep shapes, borders, and connectors as separate vector objects.
- Preserve exact spelling, symbols, values, and units.
- In image-first mode, approve the style-faithful PNG before reconstructing or
  correcting the editable companion.
- Keep high-risk numbers, quantitative bars, and final corrected labels
  deterministic.
- Do not flatten the full figure into one bitmap.

9. NEGATIVE PROMPT
No invented claim, module, value, equation, citation, causal link, universal
claim, legal or clinical conclusion. No full method architecture, training
loop, leaderboard, result badge, pseudo-text, wrong glyph, substituted symbol,
blur, fuzzy or melted shape, ghosting, overlap, clipping, off-canvas object,
microscopic label, low-resolution upscaling, or logo.

Do not redesign this as a corporate presentation, SaaS dashboard, modern
product interface, Nature-style polished geometric vector plate, or generic
flowchart. No global eyebrow label, oversized corporate title band, dark navy
insight card, equal-width stage cards, input rail, output rail, measurement
band, filled header bars, UI pills, chips, badges, soft-gray app background,
blue-violet-teal product-brand palette, excessive rounded rectangles, large
empty margins, glossy 3D icon, futuristic interface, or clean corporate
sans-serif typography.

10. OUTPUT
Return:
- {{OUTPUT_BASENAME}}.png — primary style-faithful image at the declared size;
- {{OUTPUT_BASENAME}}.svg — editable companion with live corrected text,
  separate arrows, borders, and labels.

11. PREFLIGHT
- The viewer can state the research need within five seconds.
- Every visible scientific statement is supported by the supplied summary.
- Every required label is exact and readable.
- No arrow implies a stronger relation than the source.
- No blur, fuzzy edge, overlap, or clipping is visible at 100% or 200%.
- Compare against the reference: panel topology, dashed-border treatment,
  handwriting character, icon language, arrow rhythm, palette behavior, and
  information density must remain in the same requested style family.
- The editable companion is honest about which layers are editable and is not
  falsely described as fully vector when it contains raster illustration.
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
- Rendering order: {{IMAGE_FIRST_OR_VECTOR_FIRST_AND_WHY}}
- Output: a style-faithful PNG plus an editable SVG companion with live text,
  separate stages, arrows, borders, and labels. If any illustration remains
  raster, disclose it.

2. REFERENCE-LOCKED VISUAL CONTRACT
- Reference: {{PRIMARY_REFERENCE_OR_NONE}}
- Reference role: PRIMARY visual and compositional reference; not scientific
  evidence.
- Mandatory visual attributes:
  {{REFERENCE_LOCKED_ATTRIBUTES_OR_DEFAULT_HANDDRAWN_PROFILE}}
- Content that must be replaced:
  {{REFERENCE_CONTENT_TO_REPLACE}}
- Explicit instruction: preserve the declared visual design system. Do not
  redesign it into a modern corporate diagram, SaaS dashboard, polished
  geometric vector plate, or generic card grid.

If no reference exists, use this default profile: white paper-like background;
slightly irregular black ink linework; colored dashed rounded panel borders;
large colored handwritten-looking section titles; readable black handwritten
body labels; concrete scientific doodle icons; sparse pastel highlights;
curved arrows, brackets, callouts, and dense but legible scientific content.

3. SOURCE-BOUNDED PURPOSE
- Input type: {{INPUT_TYPE}}
- Output type: {{OUTPUT_TYPE}}
- Core transformation: {{CORE_TRANSFORMATION}}
- Novel or focal stage: {{FOCAL_STAGE}}
- Five-second message: {{FIVE_SECOND_MESSAGE}}
- Do not imply: {{CLAIM_BOUNDARY}}

This is a method pipeline, not a motivation or results infographic. Show what
happens next, to which object, and through which handoff. Do not add performance
badges or unsupported feedback loops.

4. STAGE INVENTORY
Use 3–7 visible stages. Each stage label should be a short noun; its operation
should be a short verb phrase.

{{STAGE_TABLE_WITH_ID_LABEL_INPUT_OPERATION_OUTPUT}}

Required exact visible labels:
{{EXACT_LABEL_LIST}}

Training-only, inference-only, fixed, or deterministic annotations:
{{SCOPE_ANNOTATIONS_OR_NONE}}

5. ARROW AND HANDOFF CONTRACT
Write one line per connector:

source ID → target ID | payload or control label | relation meaning

{{EXPLICIT_ARROW_LIST}}

Do not add an arrow without named endpoints and meaning. Do not add feedback,
iteration, branching, or fusion unless the source explicitly supports it.

6. LAYOUT
- Reading direction: {{READING_DIRECTION}}
- Title placement: {{TITLE_POSITION_OR_PANEL_TITLES_ONLY}}
- Main topology: {{LINEAR_BRANCH_LOOP_OR_PARALLEL}}
- Stage placement: {{STAGE_PLACEMENT}}
- Optional inset or lane: {{INSET_OR_LANE_OR_NONE}}
- Approximate region ratios or reference-derived layout: {{REGION_RATIOS_OR_NONE}}
- Match the reference's information density and asymmetric panel topology.
  Prefer concrete object-to-object storytelling inside a few large dashed
  regions over equal stage cards or UI rails. Keep arrow routes unambiguous.

7. VISUAL LANGUAGE
- Background: white or warm white paper, not a gray application canvas.
- Semantic palette: {{PALETTE_AND_MEANING}}. Keep main text and object outlines
  black; use orange-red, deep blue, and dark green as stage accents unless the
  reference establishes another palette.
- Typography: handwritten-looking academic lettering. Section titles are large
  and colored; body labels are black, readable, mildly irregular, and compact.
  For editable SVG use an available handwriting family such as Chalkboard,
  Comic Sans MS, Marker Felt, or a metrically similar fallback. Do not default
  to Inter/Arial/Helvetica corporate typography.
- Shapes: thin black hand-drawn outlines. Prefer concrete scientific cartoons:
  query documents, database cylinders, patent stacks, retrieval models, ranked
  document queues, targets, checklists, and coverage cells.
- Arrows: gray hand-drawn arrows for data flow, colored arrows for actions, and
  dashed curved arrows for training-only supervision.
- Panels: mostly white interiors with colored dashed rounded boundaries; no
  filled header bars or uniform cards.
- Density: scientific illustrations and annotations should occupy roughly
  75–85% of the useful canvas while remaining legible.
- Make the focal stage visually dominant through illustration and region area,
  not through a dark UI card.

8. EDITABLE CONSTRUCTION
- Keep final text, numbers, equations, and payload labels live and editable.
- Keep every stage and arrow as a separate vector/native object.
- Preserve exact arrow endpoints, direction, labels, and branch conditions.
- Render exact plots or quantitative geometry from data, never with an image
  model.
- In image-first mode, approve the style-faithful PNG before reconstructing or
  correcting the editable companion.
- Keep high-risk numbers, quantitative geometry, and final corrected labels
  deterministic.
- Do not flatten the full figure into one bitmap.

9. NEGATIVE PROMPT
No invented stage, branch, feedback loop, value, equation, dataset, baseline,
causal link, or result claim. No unlabeled arrow, reversed endpoint, ambiguous
junction, pseudo-text, wrong glyph, substituted symbol, blur, fuzzy or melted
shape, ghosting, overlap, clipping, off-canvas object, microscopic label,
low-resolution upscaling, decorative generic AI brain, watermark, or logo.

Do not redesign this as a corporate presentation, SaaS dashboard, modern
product interface, Nature-style polished geometric vector plate, or generic
flowchart. No global eyebrow label, oversized corporate title band, dark navy
insight card, equal-width stage cards, compact input rail, output rail, bottom
measurement band, deterministic-handoff UI pill, filled header bars, chips,
badges, soft-gray app background, blue-violet-teal product-brand palette,
excessive rounded rectangles, large empty margins, glossy 3D icons, futuristic
interface, or clean corporate sans-serif typography.

10. OUTPUT
Return:
- {{OUTPUT_BASENAME}}.png — primary style-faithful image at the declared size;
- {{OUTPUT_BASENAME}}.svg — editable companion with live corrected text and
  separate stages, arrows, borders, and labels.

11. PREFLIGHT
- A reader can follow input → stages → output without reading the paper.
- Every stage, label, and handoff exists in the supplied summary.
- Every arrow has the correct source, target, direction, and payload.
- Exact text is readable and contains no pseudo-text or missing glyphs.
- No blur, fuzzy edge, overlap, or clipping is visible at 100% or 200%.
- Compare against the reference: panel topology, dashed-border treatment,
  handwriting character, icon language, arrow rhythm, palette behavior, and
  information density must remain in the same requested style family.
- The editable companion is honest about which layers are editable and is not
  falsely described as fully vector when it contains raster illustration.
```
