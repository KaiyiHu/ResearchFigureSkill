# Worked example: split an overloaded Figure 1

This is an illustrative reconstruction from the design brief supplied with this skill. It is not a verified account of a published system and must not be reused as scientific evidence.

## Contents

1. Source brief
2. Bad first decision
3. Critique
4. Better portfolio
5. Example FigureSpecs
6. Compiled-prompt excerpts
7. Acceptance lessons

## 1. Source brief

Synthetic project name: **ClaimCrawl**

Permitted statements:

- Candidate-only evaluation can hide retrieval behavior.
- Full-flow APIs can fail in ways that are difficult to localize.
- The design brief distinguishes crawler, selector, and coverage-controller responsibilities.

Unknown or unverified:

- exact algorithm;
- benchmark values;
- causal performance effects;
- legal validity;
- universal behavior across APIs or domains.

## 2. Bad first decision

One Figure 1 attempts to show:

- three motivation problems;
- full crawler → selector → controller pipeline;
- benchmark improvement;
- a causal claim that coverage control prevents all failures;
- future deployment.

Why it fails:

- no dominant reader question;
- WHY, HOW, and WHETHER compete;
- benchmark values are unavailable;
- a design description is promoted to a causal guarantee;
- method modules occupy the motivation region;
- the figure cannot be audited against exact source anchors.

## 3. Critique

```json
{
  "verdict": "blocked",
  "critical_failures": [
    "Unverified benchmark values are shown.",
    "A universal causal prevention claim exceeds the source.",
    "The figure has no single dominant role."
  ],
  "major_issues": [
    "Motivation and method content compete at equal hierarchy.",
    "Independent bottlenecks are connected as a sequential workflow."
  ],
  "revision_deltas": [
    {
      "target": "figure-level composition",
      "observed_failure": "WHY, HOW, and WHETHER share one undifferentiated canvas.",
      "minimal_change": "Split into a motivation figure and a method figure; postpone the result figure until data are available.",
      "preserve": ["three bounded problem statements", "three named method responsibilities"],
      "verification": "Each new figure has one reader question and no unsupported result."
    }
  ]
}
```

## 4. Better portfolio

| Figure | Role | Reader question | Message | Status |
|---|---|---|---|---|
| Fig. 1 | motivation | Why are aggregate evaluations insufficient for diagnosing full-flow behavior? | Three failure loci must be separated rather than collapsed into one outcome. | safe as an illustrative design brief |
| Fig. 2 | method | How are crawling, selection, and coverage responsibilities organized? | The system separates acquisition, prioritization, and coverage state. | safe as a high-level procedural view |
| Fig. 3 | experiment | Does the separation improve reported outcomes? | Unknown until machine-readable results and uncertainty are supplied. | blocked |

The motivation figure uses three parallel regions, not arrows that imply time or data flow.

The method figure uses arrows only for interfaces supported by the implementation brief. If exact payloads are unknown, they remain `missing` and block final rendering of those edges.

## 5. Example FigureSpecs

The repository examples contain full machine-readable artifacts. Key intent for Fig. 1:

```json
{
  "role": "motivation",
  "reader_question": "Why can aggregate evaluation fail to localize full-flow problems?",
  "five_second_message": "Retrieval, selection, and coverage failures are distinct diagnostic bottlenecks.",
  "claim_boundary": "Do not imply that every API or evaluation has all three failures."
}
```

Key intent for Fig. 2:

```json
{
  "role": "method",
  "reader_question": "How are evidence acquisition, prioritization, and coverage state separated?",
  "five_second_message": "Three responsibilities exchange explicit artifacts without collapsing into one opaque stage.",
  "claim_boundary": "Do not imply verified performance improvement."
}
```

## 6. Compiled-prompt excerpts

### Motivation adapter

```text
Make the diagnostic gap dominant. Use three aligned but independent regions:
retrieval visibility, selection behavior, and coverage state. Do not connect
the regions as a workflow. Label the content as a conceptual diagnostic model.
Do not show architecture, performance numbers, or universal failure.
```

### Method adapter

```text
Treat the diagram as a typed transformation. Show crawler, selector, and
coverage controller as distinct responsibilities. Include only source-supported
interfaces. Do not add benchmark badges, claims of guaranteed correctness, or
implementation details absent from the source.
```

## 7. Acceptance lessons

1. Splitting a figure is often the highest-value prompt refinement.
2. Parallel placement can communicate distinct problems without inventing sequence.
3. Module names do not prove a mechanism.
4. A result panel must wait for exact data; an attractive placeholder is still fabrication.
5. The prompt should preserve claim boundaries explicitly, because negative constraints are part of the scientific argument.
6. A reproducible case study includes source scope, spec, prompt, audit, and revision delta—not only before/after images.
