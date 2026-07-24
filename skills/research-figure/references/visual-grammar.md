# Scientific visual grammar

Use this reference after the scientific role and claim–evidence map are stable. Visual grammar turns semantics into layout without changing truth.

## Contents

1. Separate semantics from geometry
2. Relation encodings
3. Topology selection
4. Panel composition
5. Hierarchy and density
6. Text and notation
7. Color and accessibility
8. Renderer selection
9. Output and editability

## 1. Separate semantics from geometry

Maintain two graphs:

- **semantic graph** — entities and scientifically meaningful relations;
- **layout graph** — positions, alignment, grouping, and reading order.

Never derive relation semantics from position alone. Items placed left and right may be a comparison, temporal sequence, input/output flow, or before/after contrast. Encode the intended meaning explicitly.

Use stable IDs from FigureSpec for components, labels, and edges. This enables inventory diff and local repair.

## 2. Relation encodings

| Meaning | Preferred encoding | Required safeguard |
|---|---|---|
| Data flow | solid arrow | name payload when ambiguous |
| Control flow | solid arrow + verb | distinguish from data |
| Causal effect | emphasized arrow | link supported causal claim |
| Hypothesized effect | dashed arrow + “hypothesized” | never style like proven cause |
| Association | line/dotted connector | avoid causal arrowhead |
| Time | arrow + timestamps/stages | preserve direction |
| Feedback | return path | show what returns |
| Inhibition | T-bar | define in legend |
| Containment | enclosure | do not add arrow |
| Comparison | alignment/bracket | use common scale |
| Correspondence | thin/dotted mapping | avoid implying transfer |

Every arrow must have:

```text
source → target | direction | semantic type | optional payload/verb | claim ID
```

Avoid arrows used only to guide the eye. Use numbered reading order, alignment, or whitespace instead.

## 3. Topology selection

Choose topology from relation structure, not trend.

### Linear

Use for one dominant transformation with few branches. Limit the main path to roughly 3–7 high-level stages; collapse internal details into groups or an inset.

### Branched

Use when one input produces alternatives or when separate evidence paths converge. Label the branch condition and distinguish split from duplication.

### Parallel streams

Use for modalities, views, agents, or alternatives that operate concurrently. Align comparable stages and show the precise fusion or coordination point.

### Loop

Use only when output/state genuinely re-enters an upstream operation. Label the feedback payload and termination condition when known.

### Hub-and-spoke

Use when a central entity communicates symmetrically with peers. Avoid when relations have a strong temporal order.

### Hierarchy/tree

Use for exclusive or nearly exclusive containment/classification. Use a matrix/network when categories overlap.

### Matrix/grid

Use for comparisons across shared dimensions or multi-factor ablations. Maintain identical row/column semantics.

### Layered stack

Use for scales, representations, or abstraction levels. Do not use pseudo-3D depth if it implies hidden ordering.

### Spatial or biological scene

Use naturalistic spatial placement only when physical location is scientifically meaningful. Combine with deterministic callouts and labels.

## 4. Panel composition

Give each panel:

- one local reader question;
- one claim set;
- one visual form;
- a stable panel label;
- a reason it must share the canvas.

Use a hero panel when one part carries the primary scientific insight. Make subordinate panels smaller only if their text and evidence remain readable.

### Reading order

Prefer the culture/language-appropriate default unless the science requires another path. Make deviations explicit through panel labels and alignment.

### Insets

Use an inset only to:

- reveal a novel internal operation;
- magnify a dense local region;
- show a source-grounded example.

Connect it to one parent region. Do not use floating insets as miscellaneous storage.

### Cross-panel consistency

Keep the same entity:

- same label;
- same core shape;
- same color meaning;
- same line semantics;
- same direction convention.

If an entity changes state, label the change rather than silently recoloring it.

## 5. Hierarchy and density

Order visual dominance:

```text
five-second message
  > novel relation or principal evidence
    > supporting components
      > annotations and qualifiers
        > decoration
```

Delete decoration before shrinking required text.

Use these density tests:

- **squint test** — the main regions and flow remain visible;
- **thumbnail test** — the role and five-second message survive;
- **print test** — labels and line styles work at final dimensions;
- **grayscale test** — scientific groups remain distinguishable;
- **removal test** — removing an element either weakens a claim or improves clarity.

Do not assign equal visual weight to every module merely because each has a subsection.

## 6. Text and notation

Prefer:

- short noun labels for entities;
- verb labels for operations;
- payload labels for arrows;
- one terminology variant throughout;
- deterministic text nodes or overlays.

Avoid:

- paragraphs inside the figure;
- tiny captions doing the work of the main visual;
- generated pseudo-code or pseudo-equations;
- unexplained abbreviations;
- line breaks that change technical meaning.

When equations matter, render them programmatically and retain editable source. Do not ask an image model to typeset them.

Set a final-size text floor based on the venue and output medium after checking official guidance. Inspect at physical size, not only at 200% zoom.

## 7. Color and accessibility

Assign color by semantics:

```text
neutral family  → context or baseline
primary family  → proposed operation
accent family   → focal change or warning
```

Use no more accent colors than the argument needs. Do not encode success/failure with green/red alone. Pair color with:

- shape;
- label;
- line style;
- icon;
- position that does not itself mislead.

Keep contrast sufficient for the final background and print route. Test grayscale and common color-vision deficiencies when tools are available.

Do not use gradients to imply magnitude unless the scale is defined and reproducible.

## 8. Renderer selection

### Prefer vector code when

- arrows, labels, and exact geometry carry scientific meaning;
- authors must edit objects;
- the figure is a pipeline, taxonomy, architecture, or comparison;
- consistent style across many figures matters.

### Prefer plot code when

- any position, length, area, angle, color scale, or mark encodes a value;
- uncertainty, statistical tests, or axes are present;
- reproduction from data is expected.

### Prefer image generation when

- the requested asset is conceptual or naturalistic;
- small geometric deviations do not change the claim;
- exact text and numbers can be added later;
- a human/agent will inspect and composite the result.

### Prefer hybrid when

- a conceptual scene must coexist with exact plots, labels, or equations;
- generated icons can be isolated from deterministic semantics;
- editability and auditability are required.

Fail closed if the only available renderer cannot preserve the scientific inventory.

## 9. Output and editability

Recommended handoff bundle:

```text
evidence-ledger.json
figure-spec.json
compiled-prompt.md
figure-source.svg / .drawio / .tex / plotting script
figure-preview.png
figure-audit.json
source-data reference
provenance.json
```

Prefer SVG/PDF with live text for diagrams and plots. Use raster only for preview or inherently raster evidence. When raster is required, export at the actual final dimensions and verified resolution; do not claim “4K” as a substitute for readable content.

For generated assets, preserve:

- provider/model/version when available;
- prompt ID and compiled prompt;
- source/reference asset licenses;
- edit history or revision deltas;
- disclosure required by the current venue.
