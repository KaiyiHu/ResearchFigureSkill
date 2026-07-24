[COMPILED_FROM: RF-COMPILE-2.0 | FIGURESPEC: 2.0 | FIGURE: claimcrawl-fig-1 | SUMMARY_SHA256: 050260ea9be9fc67691965b94df0144192cc0883aabdcd26d76534b08edbd07d]

# 1. JOB, TARGET, AND CANVAS

Create a publication-quality scientific figure for unspecified.

- Figure ID and role: claimcrawl-fig-1 / motivation
- Medium: paper
- Audience and language: AI researchers / en
- Final canvas or column class: double-column
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

- Source topic: ClaimCrawl synthetic design brief
- Figure role: motivation
- Reader question: Why can aggregate full-flow evaluation fail to localize a problem?
- Five-second message: Retrieval, selection, and coverage are distinct diagnostic bottlenecks.
- Claim boundary: Do not imply that every API or evaluation exhibits all three failures.
- Source scope: source.md anchors B1–B4
- Known source limitations: Illustrative fixture; no empirical values or universal claims are available.

Render only the supplied scientific inventory. Preserve epistemic qualifiers
and source-bounded scope. Never fill missing evidence with plausible content.

# 4. SCIENTIFIC NARRATIVE

Communicate the following evidence-bounded propositions in order:
- 1. C1 [supported]: Candidate-only evaluation can hide retrieval behavior.
- 2. C2 [supported]: An aggregate full-flow outcome does not by itself localize retrieval, selection, or coverage-tracking failure.

Role-specific narrative directive:
Make the gap visually dominant. Encode status quo, observed failure, and bounded research need as distinct regions. Do not turn independent problems into method stages or reveal the full proposed architecture.

Claim inventory with provenance:
- C1 [supported/descriptive] Candidate-only evaluation can hide retrieval behavior. | source: source.md B1 | evidence: The design brief states that candidate-only evaluation can hide retrieval behavior.
- C2 [supported/descriptive] An aggregate full-flow outcome does not by itself localize retrieval, selection, or coverage-tracking failure. | source: source.md B2 | evidence: The brief names three possible failure loci that a single outcome cannot distinguish.

# 5. CONTENT AND EXACT-TEXT INVENTORY

- Main title: not specified; do not invent one

Must show:
- retrieval visibility bottleneck
- selection behavior bottleneck
- coverage-state bottleneck
- aggregate outcome hides location

Semantic entities with stable IDs:
- Panel A: hidden-retrieval | kind: evidence | exact label: Retrieval visibility
- Panel B: selection | kind: evidence | exact label: Selection behavior
- Panel B: aggregate | kind: annotation | exact label: Failure not localized
- Panel C: coverage | kind: evidence | exact label: Coverage state

Required exact text:
- Retrieval visibility
- Selection behavior
- Coverage state
- Failure not localized

Optional; remove before compressing required content:
- a neutral aggregate outcome icon

# 6. RELATION AND ARROW CONTRACT

- Panel B: R1 | selection → aggregate | type: association | payload/label: possible locus | claim: C2

Every connector must preserve its listed source, target, direction, type, and
payload. Never add an unlabeled or scientifically ambiguous arrow.

# 7. GLOBAL LAYOUT AND REGION GEOMETRY

- Topology: parallel diagnostic triptych
- Reading order: A, B, C
- Hierarchy: three distinct bottlenecks > failure not localized > bounded explanatory labels
- Panel grid: A:B:C
- Whitespace: generous
- Maximum label words: 5

Normalized regions:
- No normalized region geometry specified; do not infer percentages from an uninspected reference.

# 8. PER-PANEL COMPOSITION

- Panel A — Retrieval visibility | question: What retrieval behavior can candidate-only evaluation hide? | claims: C1 | dominance: 2 | form: independent diagnostic region
- Panel B — Selection behavior | question: Can the aggregate outcome identify a selection failure? | claims: C2 | dominance: 1 | form: independent diagnostic region
- Panel C — Coverage state | question: Can the aggregate outcome identify a coverage-state failure? | claims: C2 | dominance: 2 | form: independent diagnostic region

# 9. VISUAL LANGUAGE

- Background: white
- Palette: #334155, #2563EB, #D97706, #0F766E
- Color semantics: #334155=context and labels; #2563EB=retrieval; #D97706=selection warning; #0F766E=coverage
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
- a sequential workflow between the three bottlenecks
- method architecture or training stages
- benchmark values
- universal failure claims
- causal performance claims
- workflow arrows between panels
- decorative gradients
- color-only distinctions
- tiny text
- Anything that violates this claim boundary: Do not imply that every API or evaluation exhibits all three failures.
- Content that changes the dominant motivation role into another figure role
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
