---
name: research-figure
description: Summarize a paper or research brief, fill one or both fixed scientific-figure prompt templates (motivation and pipeline), generate an editable figure with a preview, and run a fast critical check for scientific errors, wrong arrows, text corruption, blur, overlap, and clipping. Use for paper-to-figure work, Figure 1 motivation figures, method or workflow diagrams, editable scientific illustrations, research figure prompts, 论文配图, 科研绘图, 动机图, 方法图, 流程图, or when the user asks for motivation, pipeline, or both.
---

# Research Figure Compiler

Use the shortest safe workflow:

```text
allowed paper content
  → one useful paper summary
  → motivation and/or pipeline prompt template
  → editable figure + preview
  → one fast critical check
```

Do not create an evidence ledger, role-analysis file, FigureSpec, provenance
bundle, audit JSON, or multi-round review package unless the user explicitly
asks for one.

Resolve `SKILL_ROOT` as the directory containing this file.

## 1. Select outputs without role classification

This Skill has two fixed figure types:

- `motivation`: why the problem matters and why the research is needed;
- `pipeline`: how the proposed method transforms input into output.

Follow the user's command:

- If the user requests `motivation`, Figure 1, problem/gap, or 动机图, generate
  only `motivation`.
- If the user requests `pipeline`, method, workflow, architecture, 方法图, or
  流程图, generate only `pipeline`.
- If the user requests both, a complete figure set, or does not specify a
  type, generate both.

Do not infer one “winning role” and suppress the other. Do not ask which type
to make when producing both is safe.

## 2. Read and summarize the allowed source

Read the full allowed paper or brief once. Respect every user exclusion before
text extraction or visual inspection. Never use excluded captions, figures,
pages, or supplements as evidence.

Create one `paper-summary.md`, normally 500–900 words or equivalent, containing:

1. research problem and importance;
2. current approach and concrete gap;
3. bounded thesis and contributions;
4. method input, 3–7 main stages, handoffs, and output;
5. strongest exact results that help understand the paper;
6. limitations and interpretations the figure must not imply;
7. exact terminology, numbers, and labels likely to appear in a figure;
8. inspected scope, exclusions, and missing material.

Use page/section anchors where practical, but do not create a separate evidence
ledger. Preserve units, signs, qualifiers, and uncertainty. Do not invent
missing modules, values, relations, or causal claims.

## 3. Fill the fixed prompt template

Read [`references/prompt-templates.md`](references/prompt-templates.md) every
time. Fill only the template or templates selected in step 1.

For each prompt:

- replace every `{{PLACEHOLDER}}`;
- copy exact scientific labels from the summary;
- keep one clear five-second message;
- list every visible entity and every arrow as
  `source → target | label/payload`;
- state what must not be shown;
- request live editable text and vector/native shapes;
- include the short negative prompt and critical QA checklist.

Save `motivation-prompt.md`, `pipeline-prompt.md`, or both. Do not paste the
entire paper into a drawing prompt.

### Reference-led style contract

When the user supplies one or more desired examples, treat each one as a
**primary style and composition reference**, not as optional inspiration and
not as scientific evidence.

Before rendering, translate the examples into observable instructions for:

- panel topology and approximate region ratios;
- border style, stroke character, and corner treatment;
- title lettering, body lettering, and typography hierarchy;
- icon family, arrow rhythm, information density, and whitespace;
- semantic accent colors and where fills are or are not used.

The filled prompt must say explicitly that the renderer must preserve this
visual language and must not redesign it into a generic house style. Replace
all reference-specific scientific content, text, numbers, logos, and unique
icons with the validated inventory from the current paper.

If no visual reference is supplied, default to a **hand-drawn academic
infographic**: white paper background, slightly irregular black linework,
colored dashed rounded panel borders, handwritten-looking headings, simple
scientific doodle icons, sparse pale highlights, and compact but readable
information density. Do not default to a modern corporate card grid.

### Motivation boundary

Use:

```text
status quo → observed limitation or blind spot → bounded research need
```

Show at most three primary messages. Do not reveal the full architecture,
training procedure, or result leaderboard.

### Pipeline boundary

Use:

```text
typed input → 3–7 verb-led stages → typed output
```

Name every handoff. Show branches or feedback only when the source explicitly
supports them. Do not add benchmark victory badges or decorative modules.

## 4. Generate the figure

Use the filled prompt as the renderer input. Do not silently reinterpret it
into a different visual system.

### 4.1 Choose the rendering order

Use **image-first** rendering when any of these is true:

- the user supplied a visual reference;
- the user asks for GPT/image-model generation;
- matching a hand-drawn or illustrative visual language is more important
  than perfect vector purity.

In image-first mode, pass the filled prompt and the supplied reference image(s)
directly to the image generator. The first artifact is the style-faithful PNG.
Do not replace this step with a manually designed corporate SVG.

Use **vector-first** rendering only when the user explicitly prioritizes a
fully editable deterministic master, or when exact plots/equations dominate.
Vector-first output must still implement the declared style contract; editable
does not mean clean sans-serif cards.

When both style fidelity and editability are requested:

1. generate and approve the style-faithful image first;
2. create an editable SVG companion that preserves the same panel topology,
   dashed borders, hand-drawn line character, lettering hierarchy, icons, and
   accent palette;
3. keep exact scientific labels, values, and arrows live and correct;
4. disclose if any illustrative layer remains raster rather than claiming the
   whole figure is fully editable.

Default deliverables remain:

```text
motivation.svg + motivation.png
pipeline.svg + pipeline.png
```

Use another editable format only when the user asks. Exact quantitative plots,
axes, equations, and sensitive numbers remain deterministic. Short diagram
labels may be generated in the image-first style pass, but must be checked
character by character and corrected in the editable companion when needed.

When a reference image is supplied, preserve its observable visual grammar
closely enough that the result belongs to the requested style family. Do not
copy its scientific content, text, values, logos, or source-specific symbols.

## 5. Run one fast critical check

Inspect the actual preview at 100% and one 200% view. Check only these gates:

1. **Science** — no invented or stronger-than-source claim, value, component,
   or legal/clinical conclusion.
2. **Structure** — required entities are present; stage order and every arrow
   endpoint/direction are correct.
3. **Text** — exact spelling, symbols, and numbers; no pseudo-text, missing
   glyphs, or unreadable labels.
4. **Optics** — no blur, fuzzy/melted shapes, overlap, clipping, off-canvas
   content, or obvious low-resolution enlargement.
5. **Editability** — the master retains live text and separate vector/native
   objects rather than one flattened bitmap.

When a reference was supplied, the optics gate also fails if panel topology,
border treatment, lettering character, icon language, or information density
has drifted into a visibly different style family.

For SVG, optionally run the lightweight check:

```bash
python3 "${SKILL_ROOT}/scripts/quick_qa.py" figure.svg figure.png
```

For an honestly disclosed image-first hybrid whose illustration layer remains
raster, use `--allow-hybrid`. Never use this flag to describe a flattened image
as fully editable.

If any gate fails, make one targeted repair and inspect again. Stop at the
first passing result. Use at most two render attempts unless the user asks for
more iteration.

## 6. Keep delivery small

Default files:

```text
paper-summary.md
motivation-prompt.md        # only when selected
motivation.svg
motivation.png
pipeline-prompt.md          # only when selected
pipeline.svg
pipeline.png
```

Report the five QA gates in the final response; do not create a QA file.
Temporary renders belong in an OS temporary directory and should be removed
after the final files pass.

## Legacy auditable mode — explicit request only

Do not load these resources in the normal workflow. If the user explicitly
asks for the former evidence-ledger/FigureSpec/audit pipeline, use the legacy
[`analysis protocol`](references/analysis-protocol.md),
[`FigureSpec contract`](references/figure-spec.md),
[`prompt system`](references/prompt-system.md),
[`visual grammar`](references/visual-grammar.md),
[`review protocol`](references/review-protocol.md),
[`domain overlays`](references/domain-overlays.md),
[`integrity and venue rules`](references/integrity-and-venues.md), and
[`worked example`](references/worked-example.md) with the bundled
`scripts/figure_workbench.py`.

## Boundaries

- Do not expose private or unpublished material to an external provider
  without authorization.
- Do not use image-generated axes, benchmark values, equations, or final
  high-risk scientific labels without deterministic verification.
- Do not claim venue compliance unless current official requirements were
  checked.
- Do not imitate a living artist or closely copy a reference figure.
- Do not replace expert scientific, statistical, clinical, or legal review.
