# Figure-role playbooks

Choose one dominant role. Use these playbooks to populate FigureSpec and add role-specific clauses to the compiled prompt. A playbook constrains scientific content; it is not a visual style preset.

## Contents

1. Motivation
2. Method / pipeline
3. Mechanism
4. Experiment
5. Ablation
6. Comparison
7. Taxonomy
8. Graphical abstract
9. Mixed multi-panel figures

## 1. Motivation

**Reader question:** Why is a new solution needed?

**Argument grammar**

```text
current practice or assumption
        ↓ challenged by evidence
observable failure / blind spot
        ↓ bounded interpretation
specific unresolved gap
        ↓
design requirement, not the full method
```

The regions may be parallel rather than sequential. Do not connect independent problems as a pipeline.

**Must show**

- the relevant status quo;
- a concrete failure, contradiction, or missing factor;
- the exact boundary of the gap;
- evidence status (`observed`, `reported`, `illustrative`, or `hypothesized`).

**May show**

- one small empirical example;
- a contrast between expected and observed behavior;
- a concise design principle.

**Must not show**

- full architecture or training stages;
- benchmark victory claims;
- generic “complexity” icons without a failure mechanism;
- universal failure when evidence covers only a reported setting.

**Prompt clause**

```text
Make the gap visually dominant. Encode status quo, observed failure, and bounded
research need as distinct regions. Do not turn them into method stages. Do not
reveal the full proposed architecture. Label illustrative examples explicitly.
```

**Diagnostic test:** After five seconds, can a reader state the unresolved problem without knowing the proposed module names?

## 2. Method / pipeline

**Reader question:** How does the proposed system transform its inputs into outputs?

**Argument grammar**

```text
typed input → operation → intermediate representation → operation → typed output
                      ↘ control/feedback only where implemented
```

**Must show**

- input and output types;
- high-level operations with verb-like labels;
- interfaces or exchanged representations;
- branches, loops, or parallel paths that materially affect behavior.

**May show**

- a compact training/inference distinction;
- module grouping;
- one zoom-in inset for the central novelty.

**Must not show**

- unrelated motivation or leaderboard results;
- boxes that merely repeat paper subsection titles;
- arrows without defined payload or control meaning;
- every implementation detail at equal prominence.

**Prompt clause**

```text
Treat the diagram as a typed transformation, not a box inventory. For every
arrow specify source, target, direction, semantic type, and payload label. Make
the novel operation dominant while keeping inputs, outputs, and interfaces
unambiguous.
```

**Diagnostic test:** Can a reader answer “what happens next, to what object, and why?” at every transition?

## 3. Mechanism

**Reader question:** Why should an intervention or component change an outcome?

**Argument grammar**

```text
initial condition / limitation
        ↓ intervention
measured or defined intermediate change
        ↓ supported link
bounded outcome
```

Distinguish an implemented mechanism from an explanatory hypothesis.

**Must show**

- initial state;
- intervention;
- intermediate variable or representation;
- outcome and evidence scope;
- certainty of each link.

**May show**

- a counterfactual baseline;
- competing explanation;
- feedback dynamics.

**Must not show**

- a module list without intermediate effects;
- causal arrows justified only by correlation;
- a performance gain as the mechanism itself;
- anthropomorphic icons that imply agency not in the method.

**Prompt clause**

```text
Expose the intermediate transformation that connects intervention to outcome.
Use solid causal encoding only for source-supported causal links; use dashed and
explicitly labeled hypothesis encoding otherwise. Do not substitute a module
inventory for an explanation.
```

**Diagnostic test:** Can each arrow be completed as “this matters because …” using source-backed language?

## 4. Experiment

**Reader question:** Does the evidence support the main empirical claim?

**Argument grammar**

```text
predeclared comparison
        ↓
effect magnitude + uncertainty + sample/setting
        ↓
bounded conclusion and exceptions
```

**Must show**

- metric direction and units;
- compared conditions or methods;
- values from a machine-readable source;
- uncertainty/error definition when applicable;
- sample size or evaluation scope where needed;
- negative, tied, or non-significant evidence relevant to the claim.

**May show**

- direct labels for main deltas;
- one robustness or boundary panel;
- practical significance in addition to statistical significance.

**Must not show**

- image-generated axes, bars, points, or numbers;
- truncated axes that exaggerate effect without a clear break;
- significance stars without test definition;
- cherry-picked conditions presented as universal performance.

**Prompt clause**

```text
Render all values and geometry deterministically from the supplied data. Make
the primary comparison obvious, show uncertainty and evaluation scope, and
retain exceptions. Do not add unreported significance, smoothing, or values.
```

**Diagnostic test:** Can a reviewer reconstruct the main comparison and identify the evidence boundary from the figure and caption?

## 5. Ablation

**Reader question:** Which component, objective, or design choice contributes under controlled comparison?

**Argument grammar**

```text
full system
  versus one controlled removal/change
        ↓
observed delta with uncertainty
        ↓
narrow interpretation
```

**Must show**

- full configuration;
- exactly what changed;
- controlled conditions;
- metric delta and uncertainty;
- interaction caveat when components are non-additive.

**May show**

- ordered contribution view;
- interaction matrix;
- sensitivity curve for a hyperparameter.

**Must not show**

- “importance” or causal necessity beyond the design and setting tested;
- multiple simultaneous changes labeled as one-component ablation;
- bar order or color that hides a negative result;
- additive interpretation when interactions were not tested.

**Prompt clause**

```text
Center the controlled contrast. Label the removed or changed factor precisely,
show the full system as reference, and phrase interpretation at the tested
scope. Do not imply independent additive contribution unless interactions were
measured.
```

**Diagnostic test:** Is the counterfactual well defined, and is the conclusion no stronger than that counterfactual?

## 6. Comparison

**Reader question:** How do alternatives differ on meaningful, consistently applied dimensions?

**Argument grammar**

```text
common evaluation dimensions
        ↓ applied consistently
alternative A ↔ alternative B ↔ proposed approach
        ↓
trade-off or decision implication
```

**Must show**

- shared criteria;
- comparable granularity;
- source support for every check, cross, rank, or claim;
- trade-offs rather than a predetermined winner.

**May show**

- a small-multiple layout;
- decision matrix;
- Pareto view when quantitative.

**Must not show**

- unequal criteria or selectively missing cells;
- decorative checkmarks as evidence;
- red/green alone for failure/success;
- “ours” highlighted so strongly that comparison becomes unreadable.

**Prompt clause**

```text
Apply identical criteria and visual scale to every alternative. Encode unknown
or not-reported separately from absent. Show trade-offs and preserve source
anchors for every categorical judgment.
```

**Diagnostic test:** Would the visual remain fair if method names were hidden?

## 7. Taxonomy

**Reader question:** How is a research or design space organized?

**Argument grammar**

```text
explicit classification dimensions
        ↓
groups and subgroups
        ↓
boundaries, overlap, and exceptions
```

**Must show**

- classification principle;
- non-overlapping vs overlapping status;
- representative members with sources;
- incomplete coverage or ambiguous cases.

**May show**

- tree, matrix, map, or faceted grid;
- cross-cutting dimension;
- timeline if evolution is part of the taxonomy.

**Must not show**

- a tree when categories overlap materially;
- arbitrary visual proximity interpreted as similarity;
- exhaustive framing for a selective survey;
- unsourced category assignments.

**Prompt clause**

```text
State the classification dimensions and whether membership is exclusive.
Choose a topology that preserves overlap and exceptions. Do not imply complete
coverage unless the source establishes it.
```

**Diagnostic test:** Can a reader explain why each item belongs where it appears?

## 8. Graphical abstract

**Reader question:** What compact end-to-end story should a broad reader remember?

**Argument grammar**

```text
context/problem → intervention → principal supported result → bounded implication
```

**Must show**

- one context;
- one intervention;
- one principal result;
- one restrained implication.

**May show**

- a naturalistic or domain-specific visual metaphor;
- a before/after contrast;
- minimal numerical highlight when exact and sourced.

**Must not show**

- all contributions, experiments, or method internals;
- visual claims stronger than the abstract/conclusion;
- image-generated required text or quantitative geometry;
- journal logos or deceptive visual authority.

**Prompt clause**

```text
Compress the paper into four beats: context, intervention, principal result,
and bounded implication. Use minimal labels and one dominant reading path.
Retain scientific qualifiers even when simplifying.
```

**Diagnostic test:** Can a broad research reader retell the correct paper story without learning a false mechanism?

## 9. Mixed multi-panel figures

Use a mixed role only when the medium or manuscript logic justifies co-location.

Require:

1. one dominant figure-level message;
2. a distinct local question per panel;
3. explicit panel role labels in FigureSpec;
4. no duplicated evidence;
5. a reading order that explains why roles share a canvas;
6. separate renderer routes when conceptual and quantitative panels coexist.

Safe example:

```text
A: supported mechanism schematic
B: intervention measurement
C: outcome with uncertainty
```

Unsafe example:

```text
A: generic motivation
B: full pipeline
C: leaderboard
D: future work
```

Split the unsafe example into a portfolio.
