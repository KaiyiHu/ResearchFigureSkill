[COMPILED_FROM: RF-COMPILE-2.0 | FIGURESPEC: 2.0 | FIGURE: claimcrawl-fig-2 | SUMMARY_SHA256: 050260ea9be9fc67691965b94df0144192cc0883aabdcd26d76534b08edbd07d]

# 1. JOB, TARGET, AND CANVAS

Create a publication-quality scientific figure for unspecified.

- Figure ID and role: claimcrawl-fig-2 / method
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
- Figure role: method
- Reader question: How are acquisition, prioritization, and coverage tracking separated?
- Five-second message: Candidate acquisition, candidate prioritization, and explored-scope recording are separate responsibilities.
- Claim boundary: Do not imply verified performance gains, exact interfaces, a coverage-feedback loop, or guaranteed coverage.
- Source scope: source.md anchor B3
- Known source limitations: Exact interfaces, execution order, algorithm internals, inputs, and outputs are intentionally omitted.

Render only the supplied scientific inventory. Preserve epistemic qualifiers
and source-bounded scope. Never fill missing evidence with plausible content.

# 4. SCIENTIFIC NARRATIVE

Communicate the following evidence-bounded propositions in order:
- 1. C1 [supported]: The crawler acquires candidates and the selector prioritizes candidates.
- 2. C2 [supported]: The coverage controller records explored scope.

Role-specific narrative directive:
Treat the diagram as a typed transformation, not a box inventory. For every arrow preserve source, target, direction, semantic type, and payload label. Make the novel operation dominant.

Claim inventory with provenance:
- C1 [supported/procedural] The crawler acquires candidates and the selector prioritizes candidates. | source: source.md B3 | evidence: The brief explicitly assigns candidate acquisition to the crawler and candidate prioritization to the selector.
- C2 [supported/procedural] The coverage controller records explored scope. | source: source.md B3 | evidence: The brief explicitly assigns explored-scope recording to the coverage controller.

# 5. CONTENT AND EXACT-TEXT INVENTORY

- Main title: not specified; do not invent one

Must show:
- crawler acquires candidates
- selector prioritizes candidates
- coverage controller records explored scope

Semantic entities with stable IDs:
- Panel A: crawler | kind: process | exact label: Crawler
- Panel A: selector | kind: process | exact label: Selector
- Panel A: coverage | kind: process | exact label: Coverage controller

Required exact text:
- Crawler
- Acquires candidates
- Selector
- Prioritizes candidates
- Coverage controller
- Candidates
- Records explored scope

Optional; remove before compressing required content:
- a grouped boundary for the three responsibilities

# 6. RELATION AND ARROW CONTRACT

- Panel A: R1 | crawler → selector | type: data-flow | payload/label: Candidates | claim: C1

Every connector must preserve its listed source, target, direction, type, and
payload. Never add an unlabeled or scientifically ambiguous arrow.

# 7. GLOBAL LAYOUT AND REGION GEOMETRY

- Topology: responsibility map with a bounded left-to-right candidate handoff and no feedback
- Reading order: A
- Hierarchy: three responsibilities > candidate flow > independent explored-scope recording
- Panel grid: A
- Whitespace: generous
- Maximum label words: 5

Normalized regions:
- No normalized region geometry specified; do not infer percentages from an uninspected reference.

# 8. PER-PANEL COMPOSITION

- Panel A — Separated responsibilities | question: How does each responsibility contribute to the high-level procedure? | claims: C1, C2 | dominance: 1 | form: three responsibility cards with one bounded candidate handoff and no feedback

# 9. VISUAL LANGUAGE

- Background: white
- Palette: #334155, #2563EB, #D97706, #0F766E
- Color semantics: #334155=context and labels; #2563EB=candidate acquisition; #D97706=prioritization; #0F766E=coverage state
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
- benchmark values
- guaranteed correctness
- unverified internal algorithms
- coverage feedback or control loops
- exact interfaces beyond the high-level candidate handoff
- training stages
- external modules absent from the brief
- unlabeled arrows
- decorative gradients
- pseudo-code
- tiny text
- Anything that violates this claim boundary: Do not imply verified performance gains, exact interfaces, a coverage-feedback loop, or guaranteed coverage.
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
