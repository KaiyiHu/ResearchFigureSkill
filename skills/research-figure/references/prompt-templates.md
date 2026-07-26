# Original Research Figure Prompt Template

This file is the core asset of Research Figure Compiler. The wording below is
derived directly from the user-supplied original AAAI prompt. Preserve its
order, tone, style lock, and negative prompt.

## Non-negotiable rule

Fill placeholders and delete inapplicable placeholder lines. Do **not**:

- paraphrase, summarize, modernize, or reorganize the fixed prose;
- replace the style lock with generic phrases such as "clean infographic";
- insert PowerPoint, editability, QA, overflow, reviewer, or implementation
  instructions into the renderer-facing prompt;
- replace hand-drawn academic infographic styling with corporate geometry,
  Nature-style vector art, SmartArt, pastel cards, or a generic open canvas;
- shorten the reference-alignment paragraph or the base Negative Prompt.

The image-generation prompt ends after `Negative Prompt`. PowerPoint
reconstruction and visual QA happen afterward under `SKILL.md`.

## Original formula

```text
PRIMARY visual and compositional reference
→ publication target, aspect ratio, and resolution
→ fixed visual-language lock
→ SCIENTIFIC TOPIC
→ exact main title and conceptual components
→ complete scientific narrative
→ REFERENCE-ALIGNED GLOBAL LAYOUT
→ exact title treatment, region topology, proportions, alignment, and gaps
→ Negative Prompt
```

## Fixed reference-lock block

For reference-led improvement or repair, copy the following block into the
final prompt and replace only the brace-delimited variables:

```text
Use the supplied reference figure as the PRIMARY visual and compositional
reference. Create a publication-quality Figure 1 for {{VENUE_AND_DOMAIN}},
in a {{ASPECT_RATIO}} landscape format, approximately
{{PIXEL_WIDTH}} × {{PIXEL_HEIGHT}} pixels.

The new figure should closely preserve the reference image's distinctive
visual language, layout proportions, information density, hand-drawn academic
infographic style, icon scale, arrow rhythm, border treatment, and typography
hierarchy. Do not redesign it as a modern corporate diagram, a polished
Nature-style vector illustration, or a futuristic AI interface. The result
should immediately look like another figure produced by the same visual design
system as the supplied reference, while presenting completely new
{{SCIENTIFIC_DOMAIN}} content.
```

Do not weaken "PRIMARY," "closely preserve," or "immediately look like another
figure produced by the same visual design system."

For complete replacement, do not inspect or send the old paper figure. Use:

```text
Reference: none — complete replacement. Do not inspect or use the old figure
or caption and do not include it as an image input or recent-image carryover.
Create a publication-quality Figure 1 for {{VENUE_AND_DOMAIN}}, in a
{{ASPECT_RATIO}} landscape format, approximately
{{PIXEL_WIDTH}} × {{PIXEL_HEIGHT}} pixels.

Use this PRIMARY visual design system: white background, hand-drawn academic
infographic style, large black hand-lettered title with slightly irregular
strokes, simple consistent 2D scientific icons, rounded dashed semantic
borders when grouping is needed, compact but readable information density,
restrained orange/blue/green accents, and clear hand-drawn arrows. Do not
redesign it as a modern corporate diagram, a polished Nature-style vector
illustration, or a futuristic AI interface.
```

For a paper with no corresponding figure and no separate reference, use the
same complete-replacement block without mentioning an old figure.

## Renderer-facing master template

Copy one reference block above, then continue with this exact scaffold:

```text
SCIENTIFIC TOPIC

The figure presents {{ONE_SENTENCE_SCIENTIFIC_TOPIC}}.

Main centered title:
"{{EXACT_SHORT_TITLE}}"

The framework contains {{COMPONENT_COUNT}} conceptual components:
{{COMPONENT_1}}
{{COMPONENT_2}}
{{COMPONENT_3}}
{{ADDITIONAL_COMPONENTS_OR_DELETE}}

The overall scientific narrative is:
{{COMPLETE_SOURCE_BOUNDED_NARRATIVE}}

REFERENCE-ALIGNED GLOBAL LAYOUT

Maintain almost exactly the same high-level composition as the supplied
reference.

Place the main title {{TITLE_POSITION}}, occupying approximately
{{TITLE_HEIGHT_PERCENT}} of the canvas height. Use large black hand-lettered
text with slightly irregular strokes. {{TITLE_DECORATION_DESCRIPTION_OR_DELETE}}

Below the title, divide the canvas into
{{REGION_COUNT_AND_BACKGROUND_DESCRIPTION}}:

{{REGION_A_EXACT_POSITION_BORDER_COLOR_PROPORTION_AND_CONTENT}}

{{REGION_B_EXACT_POSITION_BORDER_COLOR_PROPORTION_AND_CONTENT}}

{{REGION_C_EXACT_POSITION_BORDER_COLOR_PROPORTION_AND_CONTENT_OR_DELETE}}

{{ADDITIONAL_REGION_DESCRIPTION_OR_DELETE}}

{{EXACT_ALIGNMENT_GAP_AND_SPAN_RELATIONSHIPS}}

Negative Prompt: Sleek corporate infographic, Nature-style polished vector
art, futuristic interface, dark background, navy background, gradient-filled
panels, glossy 3D icons, isometric illustration, photorealistic robot,
cyberpunk UI, rigid symmetrical grid, ultra-clean geometric sans-serif
typography, formal academic serif font, thin gray boxes, solid colored panel
backgrounds, excessive equations, dense algorithm pseudocode, benchmark
plots, result tables, microscopic labels, long paragraphs, complex neural
networks, detailed environment screenshots, realistic shadows, cinematic
lighting, metallic texture, high-tech dashboard, finance imagery, stock
charts, currency symbols, Alpha Search, Alpha Zoo, investment simulation,
exact copying of the original text, Chinese screenshot header, source footer,
institutional logo, AAAI logo{{ADDITIONAL_SOURCE_SPECIFIC_NEGATIVES}}.
```

### When no external reference is supplied

Replace only these two reference-dependent lines:

```text
Maintain almost exactly the same high-level composition as the supplied
reference.
```

with:

```text
Maintain the high-level composition declared below and keep the PRIMARY visual
design system unchanged.
```

Do not change the rest of the scaffold.

## Fill card: Motivation

Use the master template unchanged. Fill it as follows:

```text
Purpose:
Explain WHY the problem exists and why a new approach is needed.

Conceptual components:
2–4 source-supported scenes, normally:
current situation
observed limitation or failure
bounded research need

Narrative:
Write 2–4 complete sentences connecting the status quo, concrete limitation,
source-supported evidence when available, and bounded need. Do not describe
the proposed architecture or turn the image into a benchmark dashboard.

Layout:
Use the permitted reference's topology and proportions. Without a reference,
use three broad hand-drawn academic infographic regions with rounded dashed
semantic borders, or one large problem region paired with two smaller evidence
and need regions. State the exact percentage, border color, position, gap, and
alignment of every region in the master template.

Exact visible labels:
One short main title, one short heading per region, and only indispensable
object labels.
```

## Fill card: Pipeline

Use the master template unchanged. Fill it as follows:

```text
Purpose:
Explain HOW the proposed method transforms an input into an output.

Conceptual components:
3–5 source-supported high-level stages by default, plus typed input and output
when they are not already components.

Narrative:
Write 2–4 complete sentences naming the input, ordered transformations,
handoffs, and output. State training-only, inference-only, fixed, or
deterministic scope only when necessary. Do not add unsupported branches,
loops, modules, or benchmark claims.

Layout:
Use the permitted reference's topology and proportions. Without a reference,
use a hand-drawn academic infographic composition with rounded dashed semantic
regions, simple 2D scientific icons, and clearly directed arrows. State the
exact percentage, border color, position, gap, span, and alignment of every
region in the master template.

Exact visible labels:
One short main title, one short heading per component, one short object label
when indispensable, and one-to-three-word arrow labels only when necessary.
```

## Exact source example

The following source text is retained as a regression reference. Do not send
its paper-specific content to the renderer for another paper:

```text
Use the supplied reference figure as the PRIMARY visual and compositional
reference. Create a publication-quality Figure 1 for an AAAI reinforcement
learning paper, in a 4:3 landscape format, approximately 2400 × 1800 pixels.

The new figure should closely preserve the reference image's distinctive
visual language, layout proportions, information density, hand-drawn academic
infographic style, icon scale, arrow rhythm, border treatment, and typography
hierarchy. Do not redesign it as a modern corporate diagram, a polished
Nature-style vector illustration, or a futuristic AI interface. The result
should immediately look like another figure produced by the same visual design
system as the supplied reference, while presenting completely new
reinforcement learning content.

SCIENTIFIC TOPIC

The figure presents an LLM-guided Monte Carlo Tree Search framework for
automatically discovering reusable hierarchical reinforcement learning
skills.

Main centered title:
"Hierarchical Skill Mining Pipeline"

The framework contains four conceptual components:
Skill Search
Agent Tools
Skill Zoo
Policy Building

The overall scientific narrative is:
MCTS explores candidate skill structures; an LLM proposes promising skills and
intrinsic rewards; an evaluator filters ineffective candidates; reusable
skills are stored in a Skill Zoo; selected skills are composed into a
hierarchical reinforcement learning policy and evaluated in simulation.

REFERENCE-ALIGNED GLOBAL LAYOUT

Maintain almost exactly the same high-level composition as the supplied
reference.

Place the main title near the top center, occupying approximately 8–10% of the
canvas height. Use large black hand-lettered text with slightly irregular
strokes. Behind and around the title, add a sparse decorative field of tiny
gray and pale-blue dots, similar to a lightly printed halftone cloud. The dots
should be subtle and should not interfere with readability.

Below the title, divide the canvas into three white-background rounded
rectangular regions:

A. One large orange dashed rounded rectangle on the left, occupying
approximately 49–51% of the total canvas width and about 76% of the canvas
height.

B. One blue dashed rounded rectangle in the upper-right area, occupying
approximately 47% of the canvas width and about 34% of the canvas height.

C. One green dashed rounded rectangle in the lower-right area, occupying
approximately 47% of the canvas width and about 39% of the canvas height.

The blue and green right-side rectangles should nearly touch vertically, with
only a small white gap between them. Their left edges should align. The orange
left rectangle should span the combined height of both right-side rectangles.

Negative Prompt: Sleek corporate infographic, Nature-style polished vector
art, futuristic interface, dark background, navy background, gradient-filled
panels, glossy 3D icons, isometric illustration, photorealistic robot,
cyberpunk UI, rigid symmetrical grid, ultra-clean geometric sans-serif
typography, formal academic serif font, thin gray boxes, solid colored panel
backgrounds, excessive equations, dense algorithm pseudocode, benchmark
plots, result tables, microscopic labels, long paragraphs, complex neural
networks, detailed environment screenshots, realistic shadows, cinematic
lighting, metallic texture, high-tech dashboard, finance imagery, stock
charts, currency symbols, Alpha Search, Alpha Zoo, investment simulation,
exact copying of the original text, Chinese screenshot header, source footer,
institutional logo, AAAI logo.
```
