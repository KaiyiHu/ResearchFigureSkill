[COMPILED_FROM: RF-COMPILE-2.0 | FIGURESPEC: 2.0 | FIGURE: verification-pipeline | SUMMARY_SHA256: c59c869e2ac868a989f3e68b0889b12ead9dec7f94c93150c1d803ddc11ef434]

# 1. JOB, TARGET, AND CANVAS

Create a publication-quality scientific figure for unspecified.

- Figure ID and role: verification-pipeline / method
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

- Source topic: Synthetic verification pipeline
- Figure role: method
- Reader question: How does a query become verified evidence?
- Five-second message: Encoding, retrieval, and verification form a typed one-way pipeline.
- Claim boundary: Do not add a feedback loop or claim that verification guarantees correctness.
- Source scope: source.md anchors M1–M5
- Known source limitations: No retrieval retry loop or performance evidence is specified.

Render only the supplied scientific inventory. Preserve epistemic qualifiers
and source-bounded scope. Never fill missing evidence with plausible content.

# 4. SCIENTIFIC NARRATIVE

Communicate the following evidence-bounded propositions in order:
- 1. C1 [supported]: A query is encoded, used for retrieval, and checked by a verifier.
- 2. C2 [supported]: Failed candidates are logged for inspection.

Role-specific narrative directive:
Treat the diagram as a typed transformation, not a box inventory. For every arrow preserve source, target, direction, semantic type, and payload label. Make the novel operation dominant.

Claim inventory with provenance:
- C1 [supported/procedural] A query is encoded, used for retrieval, and checked by a verifier. | source: source.md M1–M3 | evidence: The fixture defines the three operations and their outputs.
- C2 [supported/procedural] Failed candidates are logged for inspection. | source: source.md M4 | evidence: The fixture explicitly defines a failure log but no retry.

# 5. CONTENT AND EXACT-TEXT INVENTORY

- Main title: not specified; do not invent one

Must show:
- text query input
- query encoder
- retriever
- verifier
- verified evidence output
- failed-candidate log

Semantic entities with stable IDs:
- Panel A: query | kind: input | exact label: Text query
- Panel A: encoder | kind: process | exact label: Query encoder
- Panel A: retriever | kind: process | exact label: Retriever
- Panel A: verifier | kind: process | exact label: Verifier
- Panel A: evidence | kind: output | exact label: Verified evidence
- Panel A: failure-log | kind: output | exact label: Failure log

Required exact text:
- Text query
- Query encoder
- Retriever
- Verifier
- Verified evidence
- Failure log

Optional; remove before compressing required content:
- module grouping

# 6. RELATION AND ARROW CONTRACT

- Panel A: R1 | query → encoder | type: data-flow | payload/label: text | claim: C1
- Panel A: R2 | encoder → retriever | type: data-flow | payload/label: embedding | claim: C1
- Panel A: R3 | retriever → verifier | type: data-flow | payload/label: candidate passages | claim: C1
- Panel A: R4 | verifier → evidence | type: control-flow | payload/label: supported | claim: C1
- Panel A: R5 | verifier → failure-log | type: control-flow | payload/label: unsupported | claim: C2

Every connector must preserve its listed source, target, direction, type, and
payload. Never add an unlabeled or scientifically ambiguous arrow.

# 7. GLOBAL LAYOUT AND REGION GEOMETRY

- Topology: left-to-right with terminal branch
- Reading order: A
- Hierarchy: verified evidence path > three operations > failure log
- Panel grid: A
- Whitespace: generous
- Maximum label words: 5

Normalized regions:
- No normalized region geometry specified; do not infer percentages from an uninspected reference.

# 8. PER-PANEL COMPOSITION

- Panel A — Verification pipeline | question: What happens to the query at each stage? | claims: C1, C2 | dominance: 1 | form: linear typed pipeline with one terminal branch

# 9. VISUAL LANGUAGE

- Background: white
- Palette: #334155, #2563EB, #D97706, #0F766E
- Color semantics: #334155=input and context; #2563EB=processing; #D97706=failed candidate path; #0F766E=verified output
- Typography: sans-serif; preserve exact glyphs and a clear title/label hierarchy.
- Borders and lines: clean technical vector
- Density and whitespace: generous
- Accessibility: pair color with shape, text, or line style; never rely on color alone.

# 10. EDITABLE CONSTRUCTION CONTRACT

- Renderer mode: vector-code
- Generate editable vector geometry or native diagram objects. Keep final labels as live text nodes, not outlined glyphs or a raster layer. Preserve stable IDs, endpoints, arrowheads, grouping, and alignment deterministically. Return editable source plus SVG/PDF and a crisp raster preview.
- Keep final labels as live editable text.
- Keep core shapes and arrows as vector or native objects with stable IDs.
- Do not flatten the complete figure into one bitmap.
- Deterministic text/numbers: true / false
- Data source: none
- External provider allowed: false
- If AI image generation is used, generate only the approved illustration layer; add exact text, arrows, equations, plots, and values deterministically.

# 11. NEGATIVE PROMPT

Do not include:
- retrieval retry loop
- performance values
- guaranteed correctness
- additional ranking module
- curved retry arrow
- decorative gradients
- color-only branches
- tiny text
- Anything that violates this claim boundary: Do not add a feedback loop or claim that verification guarantees correctness.
- Content that changes the dominant method role into another figure role
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
