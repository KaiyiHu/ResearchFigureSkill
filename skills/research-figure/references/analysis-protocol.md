# Full-source analysis protocol

Use this protocol for papers, proposals, long methods, result bundles, or
underspecified requests such as “make Figure 1.” Produce evidence-linked
artifacts, not hidden chain-of-thought.

## Contents

1. Intake and scope
2. Full-paper coverage
3. Detailed summary contract
4. Source map
5. Argument model
6. Figure portfolio and role
7. Claim–evidence ledger
8. Missing-information behavior
9. Output contracts

## 1. Intake and scope

Record before reading:

- user objective and requested figure;
- source files;
- allowed and explicitly excluded regions;
- whether existing figures or captions may be inspected;
- target medium, venue, language, size, and editability;
- reference figures and permitted uses;
- privacy/external-provider restrictions.

Treat explicit exclusions as hard source boundaries. If the user says not to
read a caption or placeholder figure, mask or skip it before inspection and
record the exclusion in the source map.

Do not use a reference figure as scientific evidence. It can inform only
permitted abstract visual attributes.

## 2. Full-paper coverage

For a paper-to-figure task, inspect all available relevant sections unless the
user restricts scope:

1. title, abstract, and contribution list;
2. introduction and related work;
3. method overview and method details;
4. experiments, datasets, baselines, metrics, and statistics;
5. ablations, sensitivity, qualitative analysis, and negative evidence;
6. limitations, ethics, conclusion, and relevant appendix/supplement;
7. in-text references to the requested figure;
8. captions/existing figures only when allowed.

Do not confuse “read everything relevant” with “put everything in the figure.”
The detailed summary preserves paper context; the final prompt receives only
figure-relevant claims.

Maintain a section-coverage table:

```markdown
| Section/region | Inspected | Key extraction | Figure relevance | Exclusion |
|---|---|---|---|---|
| Abstract | yes | problem and thesis | high | |
| Appendix B | no | | unknown | unavailable |
```

Never claim complete-paper understanding when material was unavailable or
excluded.

## 3. Detailed summary contract

Create `paper-summary.md` from
[`../assets/paper-summary.template.md`](../assets/paper-summary.template.md).
The summary must cover:

### Research problem

- task, input, output, constraints, importance;
- what makes the problem technically difficult;
- existing paradigms and source-grounded limitations.

### Thesis and contributions

- central observations and their status (`supported`, `inferred`,
  `hypothesis`);
- narrow paper thesis;
- each contribution, evidence type, and likely visual role;
- strongest interpretation the source does not support.

### Method

- input–process–output;
- components and responsibilities;
- intermediate states and handoffs;
- training-only, inference-only, fixed, and deterministic operations;
- supported feedback/control paths and explicitly absent paths.

### Experimental design and evidence

- datasets/corpora, splits, sample sizes, baselines, metrics;
- what each metric measures and does not measure;
- exact results with units, uncertainty, and statistical tests;
- ablations, sensitivity, qualitative/manual evidence;
- negative, tied, contradictory, and unreported evidence.

### Boundaries

- dataset, proxy, measurement, generalization, and statistical limitations;
- legal, clinical, ethical, privacy, and external-provider limits;
- terms, symbols, and exact strings that must remain unchanged.

### Figure portfolio signals

- possible figures;
- reader question and unique evidence for each;
- content that belongs in another figure;
- likely renderer and editable format.

The executive summary may be concise, but the remaining sections must be
specific enough for a reviewer to trace every proposed visual claim.

## 4. Source map

Create a compact source map before planning panels.

```markdown
| Anchor | Source content | Candidate use | Precision |
|---|---|---|---|
| A1: p.1 abstract, sent. 3 | bounded thesis | motivation | exact |
| M2: §3.2 para. 1 | operation and handoff | method | exact |
| R1: Table 2 row 4 | effect with uncertainty | experiment | exact |
| L1: §6 para. 2 | known limitation | boundary | exact |
```

Use stable anchors:

- page + paragraph or line;
- section + paragraph;
- equation, algorithm, table, or figure identifier;
- filename + row/column for data;
- timestamp/frame for video;
- explicit user statement when no document exists.

If exact anchors are impossible, mark precision as coarse:

```text
source_anchor: "method overview supplied by user (coarse)"
```

## 5. Argument model

Extract:

```yaml
problem: What condition prevents the desired outcome?
gap: What remains unresolved?
intervention: What does the work introduce or change?
mechanism: Through what supported intermediate relation could it help?
evidence: What observation tests the claim, including uncertainty and boundary?
```

Then write:

- **Paper thesis** — narrowest sentence retaining the contribution.
- **Figure question** — one reader question.
- **Five-second message** — one bounded visual takeaway.
- **Claim boundary** — strongest interpretation the figure must prevent.
- **Reader action** — compare, follow, diagnose, remember, or inspect.

Avoid “our framework is effective.” Prefer an observable contrast or
transformation, but keep it `supported` only when the source supports it.

## 6. Figure portfolio and role

Create a role decision:

```markdown
Selected role:
Confidence:
Reader question:
Five-second message:
Claim boundary:
Unique evidence:
Include:
Exclude:
Recommended renderer:
```

Classify by question:

- motivation: why needed;
- method: how it transforms input to output;
- mechanism: why an intervention should change an outcome;
- experiment: whether evidence supports a claim;
- ablation: which controlled choice matters;
- comparison: how alternatives differ on shared criteria;
- taxonomy/dataset: how a space or dataset is constructed and organized;
- graphical abstract: what compact paper story should be retained.

Figure number is a clue, not evidence. Figure 1 is not automatically
motivation; Figure 2 is not automatically method.

### Portfolio rules

1. Give each figure one dominant manuscript job.
2. Separate **WHY**, **HOW**, and **WHETHER** unless a deliberate multi-panel
   composition has one figure-level message.
3. Do not make Figure 1 a miniature of the entire paper.
4. Keep model architecture out of motivation unless a minimal contrast is
   required to establish the gap.
5. Keep leaderboard numbers out of method unless they label a supported
   operating budget rather than a result.
6. Preserve the manuscript sequence when useful:

```text
necessity → approach → mechanism → evidence → boundary
```

### Redundancy test

For each pair of planned figures ask:

- different reader questions?
- different indispensable evidence?
- would removing either weaken a different paper claim?

If all are no, merge or delete one.

## 7. Claim–evidence ledger

Record every claim implied by text, size, position, color, icon, or relation.

```json
{
  "id": "C1",
  "text": "The controller maps a fixed ranking to an inspection depth.",
  "status": "supported",
  "scope": "procedural",
  "source_anchor": "§3.4, para. 2",
  "evidence": "The method definition states that it neither retrieves nor reranks.",
  "visual_implication": "One-way fixed-ranking input; no feedback edge.",
  "must_not_imply": "The controller improves retrieval."
}
```

### Status

- `supported`: explicit source support;
- `inferred`: useful synthesis not directly stated/tested;
- `hypothesis`: proposed causal or explanatory idea;
- `missing`: required evidence unavailable.

### Scope

- `descriptive`;
- `associational`;
- `causal`;
- `procedural`;
- `normative`.

### Visual-strength matching

| Evidence | Safe visual | Unsafe escalation |
|---|---|---|
| Reported association | alignment or dotted association | solid causal arrow |
| Component ablation | component → observed delta | universal mechanism |
| Algorithm definition | process/data-flow arrow | empirical superiority |
| Hypothesis | dashed + visible “hypothesized” | unqualified solid arrow |
| Missing evidence | visible gap or exclusion | invented example/value |

## 8. Missing-information behavior

Continue with safe, visible assumptions when they do not alter scientific
meaning:

- `venue: unspecified`;
- provisional size/aspect ratio;
- neutral accessible palette;
- partial spec with `missing` claims;
- renderer recommendation without calling an external service.

Block or ask when:

- a required value/equation has no source;
- a causal relation cannot be supported or safely downgraded;
- private material would be sent externally without permission;
- exact labels are required but only a raster-only path is available;
- the user requests wholesale imitation of protected expression;
- two equally supported roles would produce materially different figures.

## 9. Output contracts

Default paper-to-figure analysis outputs:

```text
paper-summary.md
figure-role-analysis.md
evidence-ledger.json
figure-spec.json
final-prompt.md
```

For Build, also return editable source, preview, audit, and provenance.

Do not expose hidden reasoning. Return source maps, summaries, decisions,
prompts, and evidence links required for verification.
