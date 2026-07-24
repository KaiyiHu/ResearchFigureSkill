[COMPILED_FROM: RF-COMPILE-1.0 | FIGURESPEC: 1.0 | FIGURE: verification-pipeline]

SCIENTIFIC OBJECTIVE
Role: method
Reader question: How does a query become verified evidence?
Five-second message: Encoding, retrieval, and verification form a typed one-way pipeline.
Claim boundary: Do not add a feedback loop or claim that verification guarantees correctness.

TRUTH AND PROVENANCE CONTRACT
- Render only the supplied scientific inventory.
- Do not invent or strengthen claims, values, equations, labels, or relations.
- Preserve epistemic qualifiers and source-bounded scope.
- If an instruction cannot be rendered faithfully, omit decoration and report the unresolved item; never substitute plausible content.
- Source scope: source.md anchors M1–M5
- Known source limitations: No retrieval retry loop or performance evidence is specified.

CLAIM INVENTORY
- C1 [supported/procedural] A query is encoded, used for retrieval, and checked by a verifier. | source: source.md M1–M3 | evidence: The fixture defines the three operations and their outputs.
- C2 [supported/procedural] Failed candidates are logged for inspection. | source: source.md M4 | evidence: The fixture explicitly defines a failure log but no retry.

COMPONENT AND REQUIRED-TEXT INVENTORY
Must show:
- text query input
- query encoder
- retriever
- verifier
- verified evidence output
- failed-candidate log

Semantic entities:
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

RELATION INVENTORY
- Panel A: query → encoder | type: data-flow | label: text | claim: C1
- Panel A: encoder → retriever | type: data-flow | label: embedding | claim: C1
- Panel A: retriever → verifier | type: data-flow | label: candidate passages | claim: C1
- Panel A: verifier → evidence | type: control-flow | label: supported | claim: C1
- Panel A: verifier → failure-log | type: control-flow | label: unsupported | claim: C2

PANEL AND LAYOUT PLAN
- Panel A — Verification pipeline | question: What happens to the query at each stage? | claims: C1, C2 | dominance: 1 | form: linear typed pipeline with one terminal branch
- Topology: left-to-right with terminal branch
- Reading order: A
- Hierarchy: verified evidence path > three operations > failure log
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
- Color semantics: #334155=input and context; #2563EB=processing; #D97706=failed candidate path; #0F766E=verified output
- Font: sans-serif
- Line style: clean technical vector
- Avoid: curved retry arrow, decorative gradients, color-only branches, tiny text
- Do not rely on color alone for any scientific distinction.

FORBIDDEN CONTENT
- retrieval retry loop
- performance values
- guaranteed correctness
- additional ranking module
- No decorative entity may resemble an additional scientific component.
- No unlabeled arrow, pseudo-equation, fake number, fake citation, watermark, venue logo, or celebratory badge.

OUTPUT CONTRACT
- Medium/venue: paper / unspecified
- Audience/language: machine-learning researchers / en
- Final size: single-column
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
