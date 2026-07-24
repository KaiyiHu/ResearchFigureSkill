# Source-to-figure analysis protocol

Use this protocol when the input is a paper, proposal, long method description, result bundle, or an underspecified request such as “make Figure 1.” Produce compact artifacts rather than a narrated chain of thought.

## Contents

1. Intake ladder
2. Source map
3. Argument model
4. Figure portfolio
5. Claim–evidence ledger
6. Role-purity checks
7. Missing-information behavior
8. Output templates

## 1. Intake ladder

Read only as much as the decision requires, but never claim to understand unread material.

### Minimum useful input

- User's desired figure role or manuscript location
- One paragraph of source-grounded content
- Intended medium or output type

### Better input

- Abstract and contribution statement
- Relevant method or result sections
- Caption draft
- Existing figures and cross-references
- Raw data for quantitative panels
- Target venue and final size

### Full-paper intake order

1. Title, abstract, and explicit contribution list
2. Existing figure captions and in-text figure references
3. Introduction paragraphs that state the gap
4. Method overview and only the subsections needed for the planned figure
5. Main results, ablations, and limitations
6. Appendix details only when required for correctness

Do not use section order as the visual narrative by default. Manuscripts document research; figures compress an argument for a specific reading task.

## 2. Source map

Create a compact source map before planning panels.

```markdown
| Anchor | Source content | Candidate use | Status |
|---|---|---|---|
| A1: Abstract, sent. 3 | Claimed problem | motivation | direct |
| M2: §3.2, para. 1 | Operation and inputs | method | direct |
| R1: Table 2, row 4 | Effect with uncertainty | experiment | direct |
| L1: §6, para. 2 | Known boundary | annotation/caption | direct |
```

Use stable anchors available in the material:

- page + paragraph or line;
- section + paragraph;
- equation, algorithm, table, or figure identifier;
- filename + row/column for data;
- timestamp or frame for video;
- explicit user statement when no document exists.

If exact anchors are impossible, use a descriptive locator and mark its precision:

```text
source_anchor: "method overview paragraph supplied by user (coarse)"
```

## 3. Argument model

Extract five fields:

```yaml
problem: What condition prevents the desired outcome?
gap: What specifically remains unresolved?
intervention: What does this work introduce or change?
mechanism: Through what supported intermediate relation could it help?
evidence: What observation tests the claim, including uncertainty and boundary?
```

Then write:

- **Paper thesis** — the narrowest sentence that still captures the contribution.
- **Figure question** — the one question this figure answers.
- **Five-second message** — the sentence the visual hierarchy must make obvious.
- **Claim boundary** — what the figure must not imply.
- **Reader action** — compare, follow, diagnose, remember, or inspect.

Avoid generic messages such as “our framework is effective.” Prefer a contrast or transformation that can be encoded:

```text
Weak: Our method improves retrieval.
Better: Coverage feedback prevents the selector from repeatedly exploring already-saturated sources.
```

The better form is still only `supported` when the paper provides evidence for that mechanism.

## 4. Figure portfolio

Plan the manuscript-level portfolio before overloading one figure.

### Candidate portfolio card

```yaml
figure_id: fig-1
role: motivation
reader_question: Why do full-flow evaluations hide three distinct failure modes?
takeaway: Aggregate success cannot locate retrieval, selection, and coverage failures.
unique_evidence: [C1, C2]
manuscript_job: establish necessity
overlap_with: []
```

### Portfolio selection rules

1. Give each figure one dominant manuscript job.
2. Separate **WHY**, **HOW**, and **WHETHER** unless a multi-panel composition has an explicit reason to combine them.
3. Do not make Figure 1 a miniature of the entire paper.
4. Prefer fewer figures with distinct reader questions over many decorative variants.
5. Use a graphical abstract for broad orientation, not as a replacement for a precise method or result figure.
6. Preserve a logical reading sequence across figures:

```text
necessity → approach → mechanism → evidence → boundary
```

This sequence is a portfolio heuristic, not a required panel flow.

### Redundancy test

For every pair of figures, ask:

- Do they have different reader questions?
- Do they use different indispensable evidence?
- Would removing either one weaken a different manuscript claim?

If all three answers are no, merge or delete one.

## 5. Claim–evidence ledger

Record every visual claim, including claims implied by position, size, arrow direction, color, and icons.

```json
{
  "id": "C1",
  "text": "The coverage controller reduces repeated exploration.",
  "status": "supported",
  "scope": "associational",
  "source_anchor": "§4.3 and Table 5",
  "evidence": "Removing the controller increases duplicate visits under the reported setup.",
  "visual_implication": "Show lower repetition, not universal prevention."
}
```

### Status vocabulary

- `supported`: explicit source support exists.
- `inferred`: synthesis is plausible but not stated or directly tested.
- `hypothesis`: proposed causal or explanatory idea.
- `missing`: the figure needs support that is unavailable.

### Scope vocabulary

- `descriptive`: states what exists or was observed.
- `associational`: relates variables without intervention-based causality.
- `causal`: supported intervention-to-outcome claim.
- `procedural`: describes an implemented operation or data flow.
- `normative`: states a design principle or recommendation.

### Visual-strength matching

| Evidence | Safe visual | Unsafe escalation |
|---|---|---|
| One reported association | aligned nodes, dotted association | solid causal arrow |
| Component ablation | component → observed delta | universal mechanism claim |
| Algorithm definition | deterministic process arrow | empirical superiority |
| Hypothesis | dashed arrow + “hypothesized” | unqualified solid arrow |
| Missing evidence | visible gap note | invented example or number |

## 6. Role-purity checks

### Motivation

Remove implementation modules, training stages, and result dashboards unless a small observation is necessary to prove the gap.

### Method

Remove benchmark rankings, celebratory badges, and unrelated prior-work criticism. Show transformations and interfaces.

### Mechanism

Remove module inventories that do not explain why an outcome changes. Make the intermediate variable explicit.

### Experiment

Remove decorative architecture and unsupported explanations. Show comparison, magnitude, uncertainty, and boundary.

### Ablation

Remove uncontrolled comparisons and causal language that the ablation cannot isolate.

### Graphical abstract

Remove low-level operations and secondary results. Preserve only the end-to-end paper story.

## 7. Missing-information behavior

Do not ask a broad questionnaire. Continue with safe assumptions when they do not affect scientific meaning. Ask only when a missing choice changes the claim, evidence, privacy, or deliverable materially.

### Continue safely

- Use `venue: unspecified`.
- Recommend a renderer without invoking an external service.
- Use a neutral, accessible palette.
- Create a partial spec with `missing` claims.
- Mark width or aspect ratio as provisional.

### Block rendering

- A required numeric value has no source.
- A causal relation lacks evidence and cannot be downgraded.
- The figure would expose private material to an external provider without authorization.
- The target requires exact equations or labels but only a raster image route is available.
- The user asks to mimic a protected reference's distinctive expression rather than abstract attributes.

## 8. Output templates

### Analysis decision

```markdown
Figure role:
Reader question:
Five-second message:
Claim boundary:
Unique evidence:
Recommended renderer:
Missing/blocking evidence:
```

### Portfolio decision

```markdown
| Figure | Role | Reader question | Unique evidence | Keep/split/merge |
|---|---|---|---|---|
```

### Source-grounding note

```markdown
Verified:
- C1 ← source anchor

Inferred:
- C2 ← why inference is useful

Missing:
- C3 ← exact material needed
```

Do not expose hidden reasoning. Return the source map, decisions, and evidence links needed for verification.
