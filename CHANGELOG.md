# Changelog

## 1.0 — 2026-07-26

This is the only active public release line of **Research Figure Compiler**.

### Cross-agent usage notice

- Document use from Codex, Claude Code, and other capable agentic coding
  environments, while making tool-dependent output differences explicit.
- Recommend the latest capable GPT model with strong image generation and
  visual reasoning when model choice is available.
- Clarify the prompt-first paper-understanding value proposition, the strict
  separation of Motivation and Pipeline, the current
  input → core processing → output bias, and the information users should
  provide up front to save tokens.
- Explain why SVG is not a default output and position PPTX as an editable
  companion template rather than a pixel-identical reproduction of the PNG.

### Original user prompt restored verbatim as the core

- Preserve the user-supplied reference-lock paragraph, scientific-topic
  scaffold, reference-aligned global-layout language, exact source example,
  and base Negative Prompt.
- Permit placeholder filling only; forbid paraphrasing, shortening,
  modernizing, or reorganizing the fixed wording.
- End the renderer-facing prompt after `Negative Prompt`. Keep PowerPoint,
  editability, overflow, QA, reviewer, and implementation instructions outside
  the image-generation prompt.
- Require the complete filled prompt to generate the primary PNG directly;
  layout and overflow rules are guardrails, not substitutes for the prompt.
- Reconstruct a faithful editable one-slide PPTX companion only after the
  primary PNG passes character-by-character and visual review.
- Keep SVG optional only when explicitly requested.
- Use `@oai/artifact-tool` through the Presentations workflow; do not use
  `python-pptx`.
- Keep final text, values, equations, panels, arrows, brackets, braces, and
  junctions as native editable PowerPoint objects.
- Disclose any remaining raster illustration layer.

### Text overflow and layout

- Reserve a 4–6% outer safe area without imposing a canvas-occupancy target.
- Preserve reference-defined region topology and exact proportions; do not
  force a generic open-canvas redesign.
- Use minimum default sizes of 36 pt for the slide title, 26 pt for stage
  titles, 20 pt for body labels, and 18 pt for connector labels.
- Reject figure footnotes and ordinary non-axis text below 18 pt.
- Default to 3–5 stages, one short label per stage, at most one equation, and
  at most one callout only when indispensable; both are omitted by default.
- Resolve long copy by shortening, deleting nonessential content, moving
  detail to the caption, and changing the composition before wrapping.
- Remove bottom formula ribbons, disclaimer bars, legend bands, and repeated
  callouts unless essential.
- Reject clipping, masking, cropping, or z-order as overflow fixes.
- Treat the final rendered PNG as the visual source of truth even when
  programmatic checks pass.
- Treat information overload and zoom-dependent small copy as overflow even
  when text boxes technically remain inside the slide.

### Aesthetic generation

- Make image-first generation the default visual route, including when no
  reference is supplied.
- Generate the complete publication-grade figure—including the declared title,
  labels, icons, arrows, border language, and panel topology—from the full
  master prompt.
- Make the approved primary PNG the aesthetic reference and require the
  editable PPTX companion to preserve its visual system rather than redesign
  it.
- Check every visible word, number, symbol, equation, arrow, and endpoint in
  the primary PNG; reject pseudo-text even when the composition is attractive.
- Reject giant translucent ellipses, pastel blobs, default PowerPoint shapes,
  SmartArt, clip art, Comic Sans/marker body copy, classroom worksheets, and
  generic corporate process graphics.
- Add an explicit aesthetics gate alongside science, structure, text, layout,
  arrows, and editability.

### Unified arrow construction

- Require at most three declared semantic arrow-token families.
- Fix each token's color, opacity, width, dash, head type/size, cap, join, and
  meaning.
- Build the shaft and arrowhead as one native PowerPoint connector.
- Attach endpoints to named shape ports and create connectors before nodes.
- Reject gaps, double outlines, shaft-through-head artifacts, overshoot,
  floating endpoints, arbitrary head changes, and connectors through text.

### Fast QA

- Run the PowerPoint overflow check and render every final slide.
- Visually inspect the final PNG at full size plus close views of titles,
  text-heavy regions, connector routes, gutters, and all four edge bands.
- Gate on science, structure, text, optics/layout, and arrows/editability.
- Stop at the first passing result, with at most two targeted repair rounds by
  default.

### Source and reference handling

- Ask whether the user wants Motivation, Pipeline, or both.
- Ask whether a corresponding paper figure exists and whether to replace,
  reference, or repair it.
- Complete replacement strictly isolates the old figure and caption.
- Reference-led work may reuse permitted visual grammar but never treats the
  reference as scientific evidence.

### Compact delivery

```text
paper-summary.md
motivation-prompt.md
motivation.pptx
motivation.png
pipeline-prompt.md
pipeline.pptx
pipeline.png
```

The active public version name remains `1.0`.
