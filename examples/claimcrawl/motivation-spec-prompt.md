[COMPILED_FROM: RF-COMPILE-1.0 | FIGURESPEC: 1.0 | FIGURE: claimcrawl-fig-1]

SCIENTIFIC OBJECTIVE
Role: motivation
Reader question: Why can aggregate full-flow evaluation fail to localize a problem?
Five-second message: Retrieval, selection, and coverage are distinct diagnostic bottlenecks.
Claim boundary: Do not imply that every API or evaluation exhibits all three failures.

TRUTH AND PROVENANCE CONTRACT
- Render only the supplied scientific inventory.
- Do not invent or strengthen claims, values, equations, labels, or relations.
- Preserve epistemic qualifiers and source-bounded scope.
- If an instruction cannot be rendered faithfully, omit decoration and report the unresolved item; never substitute plausible content.
- Source scope: source.md anchors B1–B4
- Known source limitations: Illustrative fixture; no empirical values or universal claims are available.

CLAIM INVENTORY
- C1 [supported/descriptive] Candidate-only evaluation can hide retrieval behavior. | source: source.md B1 | evidence: The design brief states that candidate-only evaluation can hide retrieval behavior.
- C2 [supported/descriptive] An aggregate full-flow outcome does not by itself localize retrieval, selection, or coverage-tracking failure. | source: source.md B2 | evidence: The brief names three possible failure loci that a single outcome cannot distinguish.

COMPONENT AND REQUIRED-TEXT INVENTORY
Must show:
- retrieval visibility bottleneck
- selection behavior bottleneck
- coverage-state bottleneck
- aggregate outcome hides location

Semantic entities:
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

RELATION INVENTORY
- Panel B: selection → aggregate | type: association | label: possible locus | claim: C2

PANEL AND LAYOUT PLAN
- Panel A — Retrieval visibility | question: What retrieval behavior can candidate-only evaluation hide? | claims: C1 | dominance: 2 | form: independent diagnostic region
- Panel B — Selection behavior | question: Can the aggregate outcome identify a selection failure? | claims: C2 | dominance: 1 | form: independent diagnostic region
- Panel C — Coverage state | question: Can the aggregate outcome identify a coverage-state failure? | claims: C2 | dominance: 2 | form: independent diagnostic region
- Topology: parallel diagnostic triptych
- Reading order: A, B, C
- Hierarchy: three distinct bottlenecks > failure not localized > bounded explanatory labels
- Panel grid: A:B:C
- Whitespace: generous
- Maximum label words: 5

ROLE-SPECIFIC DIRECTIVE
Make the gap visually dominant. Encode status quo, observed failure, and bounded research need as distinct regions. Do not turn independent problems into method stages or reveal the full proposed architecture.

RENDERER-SPECIFIC DIRECTIVE
Mode: vector-code
Generate editable vector geometry or native diagram objects. Keep text as text nodes. Preserve stable IDs, endpoints, arrowheads, grouping, and alignment deterministically. Return editable source plus SVG/PDF preview.

STYLE BOUNDS
- Background: white
- Palette: #334155, #2563EB, #D97706, #0F766E
- Color semantics: #334155=context and labels; #2563EB=retrieval; #D97706=selection warning; #0F766E=coverage
- Font: sans-serif
- Line style: clean technical vector
- Avoid: workflow arrows between panels, decorative gradients, color-only distinctions, tiny text
- Do not rely on color alone for any scientific distinction.

FORBIDDEN CONTENT
- a sequential workflow between the three bottlenecks
- method architecture or training stages
- benchmark values
- universal failure claims
- causal performance claims
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
