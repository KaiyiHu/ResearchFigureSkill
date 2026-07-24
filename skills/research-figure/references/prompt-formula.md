# Scientific figure prompt formula

This is the primary prompt-engineering asset of the Skill. Use it only after a
full-paper summary, evidence ledger, figure-role decision, and FigureSpec exist.
The purpose of the formula is not to make a prompt longer. It is to compile the
right scientific story into observable drawing instructions.

## Contents

1. Prompt-first workflow
2. Formula and variables
3. Compilation procedure
4. Reference-figure extraction
5. Role adapters
6. Renderer adapters
7. Negative-prompt compiler
8. Editable-output contract
9. Prompt lint and regression rules

## 1. Prompt-first workflow

```text
paper / source package
  → detailed paper summary
  → evidence and exact-text register
  → figure-role classification
  → one visual narrative
  → FigureSpec
  → prompt formula
  → renderer-specific production prompt
  → AI/vector/plot rendering
  → optical + scientific QA
  → editable delivery
```

Do not paste an entire paper or the complete detailed summary into the drawing
prompt. Use the summary to make the role and evidence decisions, then compile
only figure-relevant content into the prompt.

## 2. Formula and variables

Use this ordered formula:

```text
P = J + R + S + N + C + E + L + V + D + X + O + Q
```

Where:

| Token | Prompt layer | Question answered |
|---|---|---|
| `J` | Job, target, canvas | What is being produced, for whom, and at what size? |
| `R` | Reference contract | Which abstract visual attributes may guide the result? |
| `S` | Scientific purpose | What single question and bounded claim does the figure answer? |
| `N` | Narrative arc | What should a reader understand in order? |
| `C` | Content inventory | Which components and exact labels must appear? |
| `E` | Edge/relation contract | What does every connector mean? |
| `L` | Layout geometry | Where are regions placed and how large are they? |
| `V` | Visual system | Which palette, typography, icon, border, and density rules apply? |
| `D` | Deterministic/editable construction | Which elements must remain live, exact, and editable? |
| `X` | Negative constraints | What plausible but wrong content or rendering must be excluded? |
| `O` | Output contract | Which source files and previews must be returned? |
| `Q` | Preflight QA | What must be checked on the real rendered artifact? |

The production template serializes `L` into two numbered sections—global
layout/region geometry and per-panel composition—so the final prompt has 13
headings while the formula has 12 semantic tokens.

The order is mandatory. Scientific purpose and inventory must precede style.
Negative constraints must be derived from the role, source boundary, renderer,
reference, and known failure modes; do not use one generic negative list for
every figure.

## 3. Compilation procedure

### 3.1 Compile `J`: job, target, and canvas

State:

- target venue or medium;
- figure number or role, if known;
- audience and language;
- physical width or column class;
- aspect ratio;
- preview pixel dimensions;
- editable-source requirement.

If the venue is named, verify current official requirements before asserting
dimensions or AI-image policies. If dimensions are unknown, label them
provisional.

Template:

```text
Create a publication-quality {{ROLE}} figure for {{VENUE_OR_MEDIUM}}.
Canvas: {{WIDTH}}, {{ASPECT_RATIO}}, approximately {{PIXELS}} for review.
The final delivery must include {{EDITABLE_FORMATS}} and a crisp preview.
```

### 3.2 Compile `R`: reference contract

Extract visual attributes into a written style contract before compiling the
prompt. Separate:

- **safe abstract attributes**: functional composition class, reading
  direction, approximate rounded region ratios, density, whitespace, border
  treatment, palette relationships, icon scale, arrow rhythm, typography
  hierarchy;
- **content that must be replaced**: all source-specific text, labels,
  symbols, data, logos, and scientific entities;
- **expression not to copy**: distinctive characters, unique icon drawings,
  exact decorative motifs, or a near-duplicate arrangement when unnecessary.

Never instruct a renderer to reproduce a reference “exactly” or to make the new
figure look as if it were made by the same living artist. Use the reference as
an abstract layout and visual-language guide.

Template:

```text
Use the supplied reference only for these abstract attributes:
{{REFERENCE_ATTRIBUTES}}.

Do not copy its scientific content, text, logos, unique icons, or distinctive
expressive details. The validated scientific inventory overrides the reference.
```

### 3.3 Compile `S`: scientific purpose

Include exactly:

- dominant role;
- reader question;
- five-second message;
- claim boundary.

Template:

```text
Figure role: {{ROLE}}
Reader question: {{QUESTION}}
Five-second message: {{MESSAGE}}
Do not imply: {{CLAIM_BOUNDARY}}
```

### 3.4 Compile `N`: narrative arc

Write a short sequence of visual propositions, not a paragraph of paper
summary. Each step must map to one or more supported claim IDs.

Good:

```text
1. Candidate-only evaluation hides corpus recovery.
2. Aggregate full-flow outcomes do not localize the failed responsibility.
3. Therefore recovery, prioritization, and inspection require separate
   diagnostic boundaries.
```

Bad:

```text
Show our innovative framework with powerful modules and superior performance.
```

The bad version contains no observable scientific inventory and invites
unsupported claims.

### 3.5 Compile `C`: components and exact text

List:

- title;
- panels/regions;
- entities with stable IDs and kinds;
- required exact text;
- optional content that may be removed first;
- exact numbers, units, and uncertainty only when supported.

Do not ask an image model to spell long final labels. For image-generation or
hybrid routes, render labels in a deterministic overlay.

### 3.6 Compile `E`: edge/relation contract

For every relation state:

```text
{{RELATION_ID}} | {{SOURCE_ID}} → {{TARGET_ID}}
type={{DATA_FLOW|CONTROL_FLOW|TEMPORAL|ASSOCIATION|CAUSAL|...}}
payload/label={{TEXT}}
claim={{CLAIM_ID_OR_NONE}}
```

Do not use “connect the modules appropriately.” It is not auditable. A visual
arrow is allowed only when its endpoint, direction, semantic type, and payload
are explicit.

### 3.7 Compile `L`: global layout and region geometry

Describe layout from coarse to fine:

1. title band;
2. main regions/panels;
3. relative area and dominance;
4. alignment and gaps;
5. internal component positions;
6. reading order;
7. arrow routes and crossing avoidance.

Use normalized percentages when a simple functional composition matters.
Round measured reference geometry rather than tracing pixels:

```text
Region A: x=3%, y=14%, width=48%, height=76%
Region B: x=53%, y=14%, width=44%, height=34%
Region C: x=53%, y=51%, width=44%, height=39%
```

Percentages are approximate layout constraints, not scientific measurements.
Do not invent them from a reference that was not inspected, and do not use
them to reproduce a distinctive arrangement as a near-copy.

### 3.8 Compile `V`: visual system

Specify observable tokens:

- background;
- semantic palette;
- typography family and hierarchy;
- border radius and dash treatment;
- line weights and arrowheads;
- icon abstraction level;
- density and whitespace;
- color-blind and grayscale redundancy.

Avoid unsupported venue stereotypes. “AAAI style” alone is not a usable visual
contract. Translate it into concrete, verifiable attributes.

### 3.9 Compile `D`: deterministic and editable construction

Choose the lowest-risk renderer:

- exact structure/text → SVG, draw.io, or native PPTX shapes;
- exact values/axes → plot code;
- conceptual illustration → image generation for illustration layers only;
- mixed evidence → hybrid composition.

Always state:

```text
Keep final text as live editable text.
Keep core shapes and arrows as vector/native objects.
Assign stable IDs to required components and relations.
Do not flatten the complete figure into a single bitmap.
```

### 3.10 Compile `X`: negative constraints

Build the negative prompt from five sources:

```text
X = X_role + X_evidence + X_reference + X_renderer + X_optical
```

- `X_role`: content that would turn motivation into method, method into
  results, and so on;
- `X_evidence`: unsupported values, modules, causality, generalization, or
  legal/clinical claims;
- `X_reference`: source-specific text, logos, unique icons, or exact copying;
- `X_renderer`: long image-generated labels, image-generated plots, flattened
  vector content, or unsupported effects;
- `X_optical`: blur, fuzzy edges, pseudo-text, glyph corruption, clipping,
  overlap, low-resolution upscaling, ghosting, or local melting.

### 3.11 Compile `O`: output contract

Require:

- editable master;
- vector or PDF paper export;
- high-resolution preview;
- font/asset manifest when non-system assets are used;
- provenance;
- audit record.

For handoff, report limitations instead of silently omitting an output.

### 3.12 Compile `Q`: preflight

The prompt must end with observable checks for:

- scientific inventory;
- relation correctness;
- exact text;
- role purity;
- final-size readability;
- font/glyph integrity;
- local blur and fuzzy shapes;
- overlap/clipping;
- editable structure;
- raster resolution and upscaling.

Use the production template at
[`../assets/final-prompt.template.md`](../assets/final-prompt.template.md).

## 4. Reference-figure extraction

When a reference is supplied, first create this compact style record:

```json
{
  "available": true,
  "source": "reference path or identifier",
  "mode": "abstract-attributes",
  "use_for": [
    "4:3 landscape aspect ratio",
    "one large left region and two stacked right regions",
    "hand-drawn visual language with an academic infographic tone",
    "dashed rounded region borders",
    "small icon scale with flat 2D treatment"
  ],
  "region_geometry": [
    {"id": "left", "x_pct": 3, "y_pct": 14, "w_pct": 48, "h_pct": 76},
    {"id": "upper-right", "x_pct": 53, "y_pct": 14, "w_pct": 44, "h_pct": 34},
    {"id": "lower-right", "x_pct": 53, "y_pct": 51, "w_pct": 44, "h_pct": 39}
  ],
  "do_not_copy": [
    "reference text",
    "scientific entities",
    "logos",
    "unique icon drawings",
    "distinctive expressive details"
  ]
}
```

Use percentages only after inspecting the actual reference. Round them to
functional bounds instead of tracing exact pixels. The example above
illustrates the extraction record; it is not a default layout. Transfer its
`region_geometry` entries into FigureSpec `layout.regions` only when the
arrangement is simple and non-distinctive; otherwise redesign it. Copy the
other fields into `visual_reference` before compilation.

## 5. Role adapters

Append exactly one dominant adapter.

### Motivation

```text
Narrative: status quo → source-grounded failure/limitation → bounded research
gap or design need.
Maximum: three primary messages.
Make the failure or gap dominant.
Do not reveal the full architecture, training loop, or result leaderboard.
Explicit clause: This is a motivation figure, not a method pipeline.
```

### Method / pipeline

```text
Narrative: typed input → no more than five visible stages → typed output.
Show exact handoffs, fixed pools, budgets, state, and feedback only when
supported.
Make the novel operation or separation principle dominant.
Do not add performance badges, unsupported feedback loops, or decorative
modules.
```

### Mechanism / algorithm

```text
Narrative: limitation → intervention → supported intermediate transformation →
bounded outcome.
Distinguish implemented operations, observed associations, and hypothesized
causal mechanisms.
Do not turn a conceptual hypothesis into an established causal chain.
```

### Experiment / comparison

```text
Narrative: tested question → exact comparison → uncertainty/negative evidence →
bounded interpretation.
Generate geometry from machine-readable data.
Do not let an image model draw axes, values, tables, error bars, or
significance marks.
```

### Dataset / taxonomy

```text
Narrative: source/population → construction or organizing dimensions → groups,
splits, overlap, exceptions, and scope.
Do not imply completeness, exclusivity, balance, or representativeness unless
supported.
```

### Graphical abstract

```text
Narrative: context → intervention → principal result → bounded implication.
Use one dominant path and very few secondary details.
Do not combine all paper figures into a miniature poster.
```

See [`role-playbooks.md`](role-playbooks.md) for complete evidence and
counter-reading rules.

## 6. Renderer adapters

### Vector code

```text
Create SVG, draw.io XML, TikZ, Graphviz, Mermaid, or native slide shapes.
Keep text live, group semantic components, use stable IDs, and preserve arrow
endpoints deterministically. Export SVG/PDF and a raster preview. Do not embed
unapproved raster assets.
```

### Plot code

```text
Bind every plotted artist to supplied data. Preserve values, signs, units,
category order, missing data, uncertainty, and test definitions. Export source
code, editable SVG/PDF, and a preview. Do not infer significance.
```

### Image generation

```text
Generate only the approved conceptual illustration layer. Prefer a text-free
or placeholder-label draft. Reserve clean space for deterministic labels,
arrows, equations, and values. A generated raster is a draft asset, not the
editable scientific master.
```

### Hybrid

```text
Generate illustrative assets separately, then assemble them with deterministic
text, arrows, plots, and geometry in SVG/PPTX/draw.io. Preserve a layer/source
manifest. Use this route when a reference asks for hand-drawn or naturalistic
visual language but scientific labels must remain exact and editable.
```

## 7. Negative-prompt compiler

Start with role-specific exclusions, then add only relevant items from this
failure library:

### Scientific hallucination

```text
No unlisted module, result, number, equation, baseline, dataset, causal link,
feedback loop, legal conclusion, clinical conclusion, or universal claim.
```

### Role leakage

```text
No full architecture in a motivation figure.
No leaderboard, result badge, or causal performance claim in a method figure.
No decorative method pipeline in a quantitative result figure.
```

### Text corruption

```text
No pseudo-text, wrong spelling, missing glyphs, substituted symbols, warped
characters, duplicated labels, rasterized final text, or microscopic labels.
```

### Blur and local degeneration

```text
No blurred, fuzzy, melted, ghosted, partially erased, or low-resolution shapes.
No soft edges caused by upscaling. No inconsistent line sharpness between
regions. No object may fade into the background unless explicitly encoded.
```

### Composition

```text
No overlap, clipping, truncated text, off-canvas objects, ambiguous arrow
junctions, unintended crossings, excessive whitespace, or dense paragraphs.
```

### Decorative drift

```text
No corporate dashboard, futuristic interface, glossy 3D icon, photorealistic
robot, AI brain, chip, watermark, logo, celebratory badge, cinematic lighting,
or texture unless explicitly inventoried.
```

## 8. Editable-output contract

Preferred deliverables:

1. SVG with live text and semantic group IDs;
2. draw.io XML for general diagram editing;
3. PPTX with native shapes for common research workflows;
4. PDF for paper insertion;
5. PNG for preview only.

One editable master is required by default; do not promise all three editable
formats unless the available tools can produce and verify them.

For hybrid work:

```text
editable/
  figure.svg or figure.pptx
assets/
  generated-illustration-01.png
  source-manifest.json
previews/
  draft-01.png
  final.png
```

## 9. Prompt lint and regression rules

A compiled prompt passes only when:

- it is the canonical deterministic `RF-COMPILE-2.0` output for the supplied
  completed summary and FigureSpec, including the matching summary SHA-256;
- sections appear in formula order;
- no unresolved `{{PLACEHOLDER}}` remains;
- every required exact string from FigureSpec appears;
- every relation includes source, target, direction, and type;
- the role adapter and renderer adapter are present;
- the negative prompt includes evidence, role, renderer, and optical risks;
- editable and preview outputs are named;
- preflight includes font/glyph, blur/fuzziness, clipping, final-size
  readability, and editability checks.

Add a regression fixture whenever a prompt change fixes a real failure. The
ClaimCrawl fixture should test:

- motivation does not become Figure 2;
- top-5,000 → fixed top-1,000 → top-100 → inspect-at-most-20 is not visually
  collapsed;
- the controller does not acquire a fabricated retrieval/reranking feedback
  edge;
- exact text remains live and local shapes remain sharp.

The Markdown prompt template is a readable design contract, not a bypass
around the compiler. When drafting fields manually, transfer the result into
the summary/FigureSpec and run `compile`; strict `lint-prompt` intentionally
rejects section-local bags of copied keywords that differ from the canonical
output.
