[COMPILED_FROM: RF-COMPILE-1.0 | FIGURESPEC: 1.0 | FIGURE: claimcrawl-fig-2]

SCIENTIFIC OBJECTIVE
Role: method
Reader question: How are acquisition, prioritization, and coverage tracking separated?
Five-second message: Three responsibilities turn candidate acquisition into coverage-aware prioritization.
Claim boundary: Do not imply verified performance gains, exact interfaces, or guaranteed coverage.

TRUTH AND PROVENANCE CONTRACT
- Render only the supplied scientific inventory.
- Do not invent or strengthen claims, values, equations, labels, or relations.
- Preserve epistemic qualifiers and source-bounded scope.
- If an instruction cannot be rendered faithfully, omit decoration and report the unresolved item; never substitute plausible content.
- Source scope: source.md anchor B3
- Known source limitations: Exact interfaces and algorithm internals are intentionally omitted.

CLAIM INVENTORY
- C1 [supported/procedural] The design separates crawler, selector, and coverage-controller responsibilities. | source: source.md B3 | evidence: The brief explicitly assigns acquisition, prioritization, and scope tracking to three named responsibilities.

COMPONENT AND REQUIRED-TEXT INVENTORY
Must show:
- crawler acquires candidates
- selector prioritizes candidates
- coverage controller records explored scope

Semantic entities:
- Panel A: crawler | kind: process | exact label: Crawler
- Panel A: selector | kind: process | exact label: Selector
- Panel A: coverage | kind: state | exact label: Coverage controller
- Panel A: output | kind: output | exact label: Selected candidates

Required exact text:
- Crawler
- Selector
- Coverage controller
- Candidates
- Coverage state

Optional; remove before compressing required content:
- a grouped boundary for the three responsibilities

RELATION INVENTORY
- Panel A: crawler → selector | type: data-flow | label: Candidates | claim: C1
- Panel A: selector → coverage | type: data-flow | label: Explored scope | claim: C1
- Panel A: coverage → selector | type: feedback | label: Coverage state | claim: C1
- Panel A: selector → output | type: data-flow | label: Priority | claim: C1

PANEL AND LAYOUT PLAN
- Panel A — Separated responsibilities | question: How does each responsibility contribute to the high-level procedure? | claims: C1 | dominance: 1 | form: three-component flow with state feedback
- Topology: left-to-right with bounded feedback
- Reading order: A
- Hierarchy: three responsibilities > candidate flow > coverage feedback
- Panel grid: A
- Whitespace: generous
- Maximum label words: 5

ROLE-SPECIFIC DIRECTIVE
Treat the diagram as a typed transformation, not a box inventory. For every arrow preserve source, target, direction, semantic type, and payload label. Make the novel operation dominant.

RENDERER-SPECIFIC DIRECTIVE
Mode: vector-code
Generate editable vector geometry or native diagram objects. Keep text as text nodes. Preserve stable IDs, endpoints, arrowheads, grouping, and alignment deterministically. Return editable source plus SVG/PDF preview.

STYLE BOUNDS
- Background: white
- Palette: #334155, #2563EB, #D97706, #0F766E
- Color semantics: #334155=context and labels; #2563EB=candidate acquisition; #D97706=prioritization; #0F766E=coverage state
- Font: sans-serif
- Line style: clean technical vector
- Avoid: unlabeled arrows, decorative gradients, pseudo-code, tiny text
- Do not rely on color alone for any scientific distinction.

FORBIDDEN CONTENT
- benchmark values
- guaranteed correctness
- unverified internal algorithms
- training stages
- external modules absent from the brief
- No decorative entity may resemble an additional scientific component.
- No unlabeled arrow, pseudo-equation, fake number, fake citation, watermark, venue logo, or celebratory badge.

OUTPUT CONTRACT
- Medium/venue: paper / unspecified
- Audience/language: AI researchers / en
- Final size: double-column
- Preferred/fallback format: svg / pdf
- Editable required: true
- Deterministic text/numbers: true / false
- Data source: none
- External provider allowed: false

PREFLIGHT CHECKLIST
[ ] Every required component appears exactly once unless repetition is specified.
[ ] Every relation has correct endpoints, direction, type, and label.
[ ] Every required label is exact and legible at final size.
[ ] No extra scientific entity, value, or claim appears.
[ ] Visual hierarchy makes the five-second message dominant.
[ ] The claim boundary cannot be misread from arrows, scale, or color.
