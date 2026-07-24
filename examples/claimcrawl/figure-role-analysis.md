# Figure role analysis

## Decision

- Requested figure: Figure 1
- Selected role: `motivation`
- Confidence: high
- Reader question: Why can candidate-only or aggregate full-flow evaluation
  fail to localize a problem?
- Five-second message: Retrieval, selection, and coverage tracking are
  distinct diagnostic loci that an aggregate outcome may not distinguish.
- Claim boundary: Do not imply that every evaluation exhibits all three
  failures, that the loci form a causal or temporal pipeline, or that the
  proposed responsibility split improves performance.

## Evidence and role fit

- Unique evidence: `source.md B1` supports the bounded retrieval-visibility
  limitation; `source.md B2` supports three distinct possible failure loci.
- Why motivation: these anchors answer why better diagnostic separation is
  needed without requiring implementation details.
- Why not method for Figure 1: `source.md B3` supports a separate
  responsibility map, but showing the complete crawler–selector–coverage
  structure would change the reader question from **WHY** to **HOW**.
- Why not experiment: `source.md B4` supplies no values, comparisons,
  uncertainty, or causal performance evidence.
- Why not mixed: the motivation and method roles have different indispensable
  evidence and should remain separate.

## Figure 1 content contract

Include:

- three parallel, non-sequential diagnostic regions: retrieval visibility,
  selection behavior, and coverage state;
- one aggregate-outcome region that visibly communicates “not localized”;
- a visible illustrative/bounded scope cue;
- source bindings to `B1` and `B2`.

Explicitly exclude:

- the full crawler–selector–coverage-controller architecture;
- workflow, causal, temporal, or feedback arrows between the three loci;
- benchmark values, performance gains, rankings, significance, or guarantees;
- exact interfaces or algorithms;
- content from the excluded figures or their accompanying text.

## Renderer recommendation

- Route: `vector-code`
- Editable master: SVG
- Fallback: PDF
- Layout: parallel diagnostic triptych with a shared aggregate-outcome cue
- Reason: the figure is label- and relation-sensitive, contains no naturalistic
  imagery or quantitative geometry, and must keep all text and grouping
  editable.

## Portfolio consequence

Reserve a separate method figure for `source.md B3`. That figure may show the
three responsibilities and a bounded candidate handoff, but must not invent a
coverage-feedback edge or any exact interface.
