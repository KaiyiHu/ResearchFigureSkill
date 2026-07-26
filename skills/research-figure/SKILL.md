---
name: research-figure
description: Create AI top-conference-grade scientific Motivation and Pipeline figures from papers or research briefs. Summarize the allowed source, fill the original user-supplied Research Figure Prompt Template without paraphrasing its fixed visual-style lock, directly generate a style-faithful primary PNG, reconstruct a faithful editable PowerPoint companion, and visually check scientific correctness, text overflow, collisions, blur, spacing, alignment, clipping, and consistent connected arrows. Use for NeurIPS-, ICML-, ICLR-, AAAI-, CVPR-, ACL-, or KDD-level paper figures; Figure 1; method, workflow, or architecture diagrams; editable PPT/PPTX scientific illustrations; research figure prompts; 论文配图; 科研绘图; 动机图; 方法图; or 流程图. Before work, establish the requested figure type, whether the paper already has that figure, and whether to replace it completely, use it as a reference and improve it, or preserve and repair it.
---

# Research Figure Compiler

Public workflow version: **1.0**.

Use the shortest safe workflow:

```text
allowed paper content
  → resolve whether existing figures may be inspected
  → one useful paper summary
  → complete Motivation and/or Pipeline master prompt
  → primary style-faithful PNG
  → faithful editable PPTX companion
  → visual-first critical check of both
```

Do not create an evidence ledger, role-analysis file, FigureSpec, provenance
bundle, audit JSON, or multi-round review package unless requested.

Resolve `SKILL_ROOT` as the directory containing this file.

## 1. Establish the user brief

Target the communication quality expected of leading AI-conference figures:
one five-second message, source-bounded claims, reviewer-readable text, precise
arrows, breathing room, disciplined alignment, accessible color, and an
editable master. This is a quality target, not automatic venue compliance.

Ask for the following missing decisions in one concise question:

```text
Figure type: Motivation, Pipeline, or both?
Existing corresponding figure: yes, no, or unknown?
If yes: completely replace it, use it as a reference and improve it, or
preserve it and repair selected parts?
```

Do not repeat decisions the user has already supplied.

## 2. Select the requested output

- `motivation`: status quo → observed limitation → bounded research need.
- `pipeline`: typed input → normally 3–5 verb-led stages → typed output.
- Generate both only when the user asks for both.
- Ask before continuing when the type is missing.

Do not classify one type as the winner and suppress the other.

## 3. Resolve existing figures before inspecting them

Respect exclusions first. Never inspect an excluded figure, caption, page, or
supplement.

When the allowed source appears to contain a corresponding figure and the user
has not chosen how to treat it, ask:

```text
The paper appears to contain an existing Motivation/Pipeline figure. Should I
(1) regenerate independently and ignore it, (2) use only its visual/layout
language as a reference, or (3) preserve and repair it?
```

For complete replacement, enforce strict isolation:

- do not open, render, OCR, summarize, or use the old figure or caption;
- do not reuse its topology, palette, wording, icons, or placement;
- if it is already visible in the conversation, explicitly ignore it;
- start image generation without image inputs or recent-image carryover;
- write `Reference: none — complete replacement` in the prompt.

For reference-led improvement, use the old figure only as permitted visual
structure, never as scientific evidence. For repair, preserve verified
elements and change only requested or failed parts.

## 4. Summarize the allowed source once

Create `paper-summary.md`, normally 500–900 words or equivalent:

1. research problem and importance;
2. current approach and concrete gap;
3. bounded thesis and contributions;
4. method input, 3–7 source-supported stages, handoffs, and output;
5. strongest exact results useful for understanding the paper;
6. limitations and interpretations the figure must not imply;
7. exact terms, numbers, and labels likely to appear;
8. inspected scope, exclusions, and missing material.

Use page or section anchors where practical. Preserve units, qualifiers,
uncertainty, and direction. Do not invent missing modules, values, or links.

## 5. Fill the production prompt

Read [`references/prompt-templates.md`](references/prompt-templates.md) every
time. Treat its **Original Research Figure Prompt Template** as the Skill's
immutable core asset. Copy the fixed reference lock, scientific-topic
scaffold, reference-aligned layout wording, and base Negative Prompt without
paraphrasing, shortening, modernizing, or reorganizing them. Replace only the
declared placeholders and delete inapplicable placeholder lines. Fill only the
requested Motivation or Pipeline card, copy exact labels from the summary, and
list every connector internally as:

```text
source ID → target ID | payload/control label | relation meaning
```

Save `motivation-prompt.md`, `pipeline-prompt.md`, or both. Do not paste the
entire paper into the drawing prompt. The renderer-facing prompt must end after
the original-style `Negative Prompt`. Never append PowerPoint, editability,
overflow, QA, reviewer, or implementation instructions to it; those are
post-generation workflow rules in this file.

Before writing the renderer-facing prompt, derive these fields internally from
the summary and then insert them into the master formula:

1. scientific role and the single question the figure answers;
2. five-second message and information priority;
3. source-bounded scientific narrative;
4. necessary visual elements and exact visible labels;
5. forbidden content and claim boundaries;
6. reference visual grammar, when permitted;
7. global composition and region-by-region content;
8. explicit arrow semantics;
9. the unchanged base Negative Prompt plus source-specific forbidden content.

Do not save this derivation as another file. Its purpose is to make the final
prompt complete, paper-specific, and visually executable.

### Compress content before layout

Every filled prompt must:

- reserve a clean 4–6% outer safe area;
- choose the composition only after reducing the visible-text inventory;
- keep the main title to about 8 English words or 16 Chinese characters;
- use no optional subtitle unless it is essential to the five-second message;
- default to 3–5 pipeline stages; use 6–7 only when each stage needs no more
  than a short title and one short label;
- keep stage/scene titles to about four words and explanatory labels to about
  seven words;
- keep connector labels to one to three words;
- show zero equations and callouts by default; allow at most one of each only
  when essential to the five-second message; move derivations,
  qualifiers, caveats, repeated explanations, and implementation details to
  the paper caption instead of a bottom strip;
- use at least 36 pt for the slide title, 26 pt for stage/scene titles, 20 pt
  for body labels, and 18 pt for connector labels;
- reject all figure footnotes and any non-axis text below 18 pt;
- keep one-line titles on one line;
- shorten wording first, then remove nonessential copy, then wrap at semantic
  boundaries, then change the composition; never solve overflow by shrinking;
- reserve text boxes before placing icons, connectors, or decoration;
- keep text, equations, arrowheads, and icons fully inside their usable area;
- keep connector labels in open whitespace, never across a border;
- keep unrelated geometry at least 0.5 body-line height from text;
- use brackets/braces only for declared grouping targets and junctions only
  for source-supported convergence.

### Preserve the original visual system

Do not let overflow safeguards redefine the style. The original prompt's
visual language remains primary:

- white background;
- hand-drawn academic infographic style;
- large black hand-lettered title with slightly irregular strokes;
- rounded dashed semantic regions in restrained orange, blue, and green;
- simple consistent 2D scientific icons;
- compact but readable information density;
- clear hand-drawn arrows;
- no gradients, shadows, glossy 3D, corporate UI, or Nature-style polished
  vector redesign.

Use the permitted reference's topology, proportions, region borders, gaps,
icon scale, arrow rhythm, density, and typography hierarchy. Do not replace
rounded dashed regions with an open canvas merely because a generic layout
rule prefers it. Without a reference, choose two or three broad regions in this
same original visual system and state their exact proportions and alignments in
the prompt.

Do not add a bottom formula ribbon, disclaimer bar, or repeated summary
callouts unless the science requires it. Do not target a fixed
canvas-occupancy percentage, but do specify the region proportions required by
the original prompt formula.

Treat the main title as a protected lane. Keep panels, arcs, connectors,
borders, icons, and texture outside it. Start body content below the title
lane plus at least 0.5 body-line height. Do not hide a collision with a mask,
crop, or z-order trick.

### Arrow system contract

Declare an `ARROW_STYLE_TOKENS` table before assembly. Use no more than three
semantic families:

```text
FLOW_PRIMARY   | color | 2–3 px | solid  | arrow/stealth med | round | round
FLOW_SECONDARY | color | 2–3 px | solid  | arrow/stealth med | round | round
SUPERVISION    | color | 2–3 px | dashed | arrow/stealth med | round | round
```

Omit unused families. A token fixes stroke color, width, dash, opacity,
arrowhead type/width/length, line cap, line join, and semantic role. The same
meaning must use the same token everywhere.

For every arrow:

- use one native connected object for the shaft and head;
- never assemble a separate triangle and line;
- make head fill/stroke match the shaft;
- attach endpoints to named shape ports, not approximate floating coordinates;
- keep the head tangent to the final shaft segment with no gap, double outline,
  overshoot, or shaft visible through the head;
- create connectors before nodes so lines remain behind nodes and labels;
- route around all text boxes and keep labels beside the route in reserved
  whitespace;
- use dash/color to distinguish semantics, not arbitrary head shapes;
- render and visually inspect every bend, endpoint, crossing, and merge.

## 6. Generate the primary PNG and editable companion

Use the Presentations Skill for every PPTX workflow and follow its local
instructions. Use `@oai/artifact-tool` from a JavaScript ES module; do not use
`python-pptx`.

Default deliverables are:

```text
motivation.pptx + motivation.png
pipeline.pptx + pipeline.png
```

Use one slide per figure. Keep all final titles, labels, numbers, equations,
panels, arrows, leaders, brackets, braces, and junctions as
native editable PowerPoint objects. A stylistic illustration layer may remain raster only when
disclosed; never call a flattened bitmap fully editable.

Use **aesthetic-first image generation by default**, including when no
reference exists. Send the complete filled original prompt—not a shortened
summary and not a rewritten meta-prompt—to the built-in image-generation tool.
Do not append the downstream PowerPoint or QA instructions. Generate the
primary PNG as a complete scientific figure with the declared title, labels,
arrows, icons, panel topology, and visual language. This restores the original
prompt-driven workflow in which one coherent image model controls the whole
design system.
In reference-led improvement or repair mode, include only the user-permitted
reference image with the complete prompt so its observable visual grammar can
control the result. In complete-replacement mode, include no reference image
and no recent-image carryover.

Inspect the primary PNG before PowerPoint reconstruction. Reject or revise it
if it looks generic, childish, corporate, diagram-template-like, visually
unbalanced, misspelled, structurally wrong, blurred, or overcrowded. Check every
visible word, number, symbol, equation, arrow, and endpoint character by
character. Never accept pseudo-text merely because the composition is good.

After the primary PNG passes, create the PPTX as a faithful editable companion
using the approved PNG as the visual reference. Reproduce its composition,
scale relationships, border language, icon placement, arrow rhythm, palette,
and typography hierarchy rather than redesigning it. Keep exact text, numbers,
equations, arrows, brackets, and junctions editable. A raster illustration
layer may remain and must be disclosed.

Use native-first assembly only when the user explicitly prioritizes fully
editable deterministic geometry, or when exact plots/equations dominate.
Native-first must still be designed from an approved visual concept and must
not fall back to default ovals, cards, SmartArt, or clip art.

When no reference exists, use a publication-grade hand-drawn academic
infographic by default: white paper, refined slightly organic black linework,
large black hand-lettered headings, clean readable body labels, concrete
scientific 2D icons, restrained orange/blue/green accents, rounded dashed
semantic regions, clear hand-drawn arrows, and compact but readable information
density. Do not substitute Comic Sans, default PowerPoint shapes, corporate
SmartArt, polished Nature-style vector art, or a futuristic AI interface.

Create connectors before entity nodes with `slide.shapes.connect(...)`. Prefer
side anchors or explicit connection sites. Use the token's built-in `head`,
`line`, `cap`, and `join` properties so the arrowhead and shaft remain one
consistent PowerPoint connector.

SVG is not a default deliverable and is not the default QA surface. Create it
only when the user explicitly requests SVG.

## 7. Run visual-first QA

The approved primary PNG is the aesthetic reference. The rendered PPTX preview
is the editability/fidelity reference. Passing metadata or code checks never
overrides a visible defect in either.

For each PPTX:

1. run the Presentations Skill's `slides_test.py`;
2. render every final slide with `render_slides.py`;
3. inspect both the primary PNG and PPTX-rendered preview at original
   resolution with an image-viewing tool;
4. compare their global topology, scale, typography hierarchy, icon language,
   border treatment, palette behavior, and arrow rhythm;
5. inspect the title, each text-heavy panel, every gutter/connector route, and
   all four outer edge bands at a close view;
6. fix every unintended overflow, wrap, overlap, broken connector, crop, or
   unacceptable style drift;
7. rerender and reinspect after any fix.

Do not approve a figure unless all six gates pass:

1. **Science** — no invented or stronger-than-source claim, number, or module.
2. **Structure** — entities, order, endpoints, direction, branches, brackets,
   and junctions are correct.
3. **Text** — exact glyphs and numbers; no pseudo-text, unexpected wrap,
   clipping, border contact, or collision.
4. **Aesthetics** — looks like a publication figure, not PowerPoint SmartArt,
   a classroom worksheet, generic clip art, a corporate process diagram, or a
   collection of oversized pastel shapes. Typography, illustration, palette,
   and stroke character form one deliberate visual system.
5. **Optics/layout** — no blur, melted shape, overlap, off-canvas content,
   edge crowding, tiny auxiliary copy, information overload, repeated narrow
   cards, dense bottom strips, inconsistent gap, or misalignment.
6. **Arrows/editability** — consistent token use; no floating endpoint,
   shaft/head gap, mismatched head, broken bend, connector through text, or
   flattened final text/structure.

Programmatic warnings are a lower bound, not a waiver. A visible defect fails
even when `slides_test.py` is clean. Conversely, inspect a reported overlap
before deciding whether it is intentional.

Treat semantic overflow as a failure even when every text box is technically
inside the slide. Fail when a reader must zoom to read ordinary labels, when
the main route competes with caveats or formulas, or when the composition uses
small type to preserve a preselected grid. Remove content or change the
composition rather than making the text fit.

If a gate fails, make one targeted repair and inspect again. Stop at the first
passing result. Use at most two repair rounds unless the user requests more.

For explicitly requested SVG only, `scripts/quick_qa.py` remains an optional
legacy structural check. It does not replace PPT/PNG visual inspection.

## 8. Keep delivery small

For one requested type, keep only:

```text
paper-summary.md
motivation-prompt.md or pipeline-prompt.md
motivation.pptx or pipeline.pptx
motivation.png or pipeline.png
```

Reuse one summary for both figures. Report QA in the final response instead of
creating a QA file. Remove temporary source modules, renders, crops, layout
JSON, and montages after approval.

## Boundaries

- Do not expose private or unpublished material to an external provider
  without authorization.
- Keep exact values, equations, axes, and high-risk labels deterministic.
- Do not claim venue compliance without checking current official rules.
- Do not closely copy a reference figure or imitate a living artist.
- Do not replace expert scientific, statistical, clinical, or legal review.
