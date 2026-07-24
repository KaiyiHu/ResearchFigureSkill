# FigureSpec 1.0

FigureSpec is the model- and renderer-independent contract between paper analysis and drawing. Keep scientific semantics here; keep provider syntax in the compiled prompt.

## Contents

1. Why an intermediate representation
2. Required structure
3. Field semantics
4. Relation vocabulary
5. Renderer routing
6. Validation and migration

## 1. Why an intermediate representation

A prose prompt mixes truth, layout, style, and provider instructions. That makes errors hard to locate and revisions destructive. FigureSpec separates:

```text
source truth → visual argument → semantic inventory → spatial layout → renderer contract
```

Use the same spec to:

- compare candidate layouts without changing claims;
- compile prompts for different renderers;
- audit whether the image added, removed, or reversed content;
- repair only failed elements;
- preserve a reviewable provenance trail.

The machine-readable schema is `assets/figure-spec.schema.json`.

## 2. Required structure

```json
{
  "schema_version": "2.0",
  "figure_id": "fig-1",
  "source": {
    "title": "Paper or brief title",
    "type": "paper",
    "scope": ["abstract", "section 3", "table 2"],
    "limitations": []
  },
  "target": {
    "medium": "paper",
    "venue": "unspecified",
    "audience": "researchers in the field",
    "language": "en",
    "size": "double-column",
    "editable": true
  },
  "intent": {
    "role": "method",
    "reader_question": "How does the system transform a query into a verified answer?",
    "five_second_message": "Retrieval and verification form a bounded feedback loop.",
    "claim_boundary": "Do not imply guaranteed correctness."
  },
  "claims": [],
  "content": {
    "title": "",
    "must_show": [],
    "nice_to_show": [],
    "must_not_show": [],
    "required_text": []
  },
  "panels": [],
  "layout": {
    "regions": []
  },
  "render": {},
  "style": {},
  "acceptance": {},
  "visual_reference": {
    "available": false,
    "source": "",
    "mode": "none",
    "use_for": [],
    "do_not_copy": [
      "scientific content, labels, values, branding, or distinctive composition"
    ]
  }
}
```

`content.title`, `layout.regions`, and the top-level `visual_reference` are optional.
They can be added by the prompt-formula workflow without invalidating FigureSpec 1.0
files created before those fields existed.

## 3. Field semantics

### `source`

- `title`: human-recognizable source name; do not paste an entire paper.
- `type`: `paper`, `proposal`, `brief`, `data`, or `existing-figure`.
- `scope`: exact sections, tables, files, or statements actually inspected.
- `limitations`: unread, unavailable, ambiguous, or unverified material.

### `target`

- `medium`: `paper`, `preprint`, `poster`, `slide`, `web`, or `proposal`.
- `venue`: official venue name or `unspecified`.
- `audience`: knowledge level that controls label density.
- `language`: BCP-47-style short tag such as `en` or `zh-CN`.
- `size`: semantic size (`single-column`, `double-column`, `full-page`) or exact dimensions.
- `editable`: whether text and geometry must remain editable.

### `intent`

- `role`: one dominant role from the skill taxonomy.
- `reader_question`: the question the figure answers.
- `five_second_message`: one sentence, not a list.
- `claim_boundary`: strongest tempting interpretation that must be prevented.

### `claims`

```json
{
  "id": "C1",
  "text": "Verification feeds failed evidence back to retrieval.",
  "status": "supported",
  "scope": "procedural",
  "source_anchor": "§3.4, Algorithm 1, lines 8–12",
  "evidence": "The algorithm explicitly re-queues failed items."
}
```

Rules:

- Keep IDs stable across revisions.
- Require a non-empty `source_anchor` for `supported` claims.
- Use `missing` rather than placeholder facts.
- Record the narrow scientific scope.

### `content`

- `title`: optional in-figure heading. Use a short string or `""` to omit it; do not
  duplicate the paper title automatically.
- `must_show`: required scientific entities or observations.
- `nice_to_show`: removable supporting context.
- `must_not_show`: scientifically misleading or role-breaking content.
- `required_text`: exact labels. Keep each short enough for final size.

The title is presentation text, not a new claim. Any factual wording in it must still
be supported by the claim inventory.

### `panels`

```json
{
  "id": "A",
  "title": "Evidence acquisition",
  "question": "Where does candidate evidence come from?",
  "claim_ids": ["C1"],
  "dominance": 1,
  "visual_form": "three-stage data-flow",
  "entities": [
    {"id": "query", "label": "Query", "kind": "input"},
    {"id": "retriever", "label": "Retriever", "kind": "process"}
  ],
  "relations": [
    {
      "id": "R1",
      "from": "query",
      "to": "retriever",
      "type": "data-flow",
      "label": "request",
      "claim_id": "C1"
    }
  ]
}
```

Rules:

- Give each panel one local question.
- Give every relation a globally unique stable `id` for audit and local repair.
- Set `dominance: 1` for the hero panel; use larger numbers for subordinate panels.
- Reference only defined claim IDs and entity IDs.
- Inventory every required component before describing layout.

### `layout`

```json
{
  "topology": "left-to-right-with-feedback",
  "reading_order": ["A", "B"],
  "hierarchy": ["core loop", "input/output", "annotations"],
  "panel_grid": "A:A:B",
  "whitespace": "generous",
  "max_label_words": 5,
  "regions": [
    {
      "id": "hero",
      "x_pct": 5,
      "y_pct": 8,
      "w_pct": 70,
      "h_pct": 76,
      "purpose": "Primary scientific argument"
    }
  ]
}
```

Topology describes spatial organization, not scientific semantics. A left-to-right placement does not itself mean causality.

`regions` is an optional normalized layout contract:

- Measure `x_pct`, `y_pct`, `w_pct`, and `h_pct` as percentages of the full
  canvas.
- Use the top-left corner as `(0, 0)`.
- Keep `x_pct + w_pct <= 100` and `y_pct + h_pct <= 100`.
- Use `purpose` to state the communicative job of the region, not its styling.
- Treat regions as composition guides. Panels and relations remain the semantic
  authority when a region conflicts with scientific structure.
- Record percentages only after inspecting an actual reference or intentionally
  designing the geometry. Do not inherit the numbers in this documentation as
  defaults.

### `visual_reference`

```json
{
  "visual_reference": {
    "available": true,
    "source": "reference path or identifier",
    "mode": "abstract-attributes",
    "use_for": [
      "clear left-to-right reading order",
      "restrained technical palette",
      "generous separation between stages"
    ],
    "do_not_copy": [
      "scientific content or conclusions",
      "labels, values, equations, logos, or branding",
      "distinctive composition, icons, or ornamental details"
    ]
  }
}
```

Use this optional field only when the user supplies a visual reference. Set
`available` explicitly, identify the inspected `source`, and choose `mode` from
`none`, `layout-only`, or `abstract-attributes`. Put only reusable, non-exclusive
attributes and their intended uses in `use_for`; put explicit prohibitions in
`do_not_copy`. Never treat a reference image as evidence, and never copy its
scientific content, exact wording, data, branding, distinctive layout, or
decorative assets.

### `render`

```json
{
  "mode": "vector-code",
  "preferred_format": "svg",
  "fallback_format": "pdf",
  "deterministic_text": true,
  "deterministic_numbers": true,
  "external_provider_allowed": false,
  "data_source": "results.csv or empty when not quantitative"
}
```

### `style`

```json
{
  "background": "white",
  "palette": ["#334155", "#2563EB", "#D97706", "#0F766E"],
  "color_semantics": {
    "#2563EB": "proposed operations",
    "#D97706": "failure or warning"
  },
  "font": "sans-serif",
  "line_style": "clean technical vector",
  "avoid": ["3D gloss", "decorative gradients", "tiny text"]
}
```

Do not encode scientific status by color alone. Pair color with labels, shapes, or line styles.

### `acceptance`

```json
{
  "critical_checks": [
    "all supported claims retain source anchors",
    "all required labels are exact",
    "all relation endpoints and directions are correct"
  ],
  "minimum_scores": {
    "scientific_fidelity": 5,
    "structural_correctness": 5,
    "role_purity": 4,
    "message_clarity": 4,
    "readability": 4,
    "accessibility": 4,
    "editability_reproducibility": 4
  }
}
```

Use a 1–5 scale. Never average away a critical dimension.

## 4. Relation vocabulary

Use only the smallest vocabulary that expresses the source:

| Type | Meaning | Default encoding |
|---|---|---|
| `data-flow` | information/object moves | solid arrow |
| `control-flow` | operation determines next step | solid arrow with verb |
| `causal` | intervention changes outcome | solid emphasized arrow + claim |
| `causal-hypothesis` | proposed but unverified causal link | dashed arrow + epistemic label |
| `temporal` | earlier/later | arrow with time cue |
| `association` | variables co-vary/connect | line or dotted arrow |
| `comparison` | alternatives contrasted | aligned panels or bidirectional bracket |
| `feedback` | downstream state re-enters upstream process | return arrow |
| `inhibition` | source suppresses target | T-bar |
| `containment` | entity belongs inside another | enclosure, no arrow |
| `correspondence` | aligned equivalents | thin/dotted connector |

If none fits, define the meaning explicitly in the relation label and legend.

## 5. Renderer routing

| Spec feature | Preferred mode |
|---|---|
| Exact text, equations, many labeled arrows | `vector-code` |
| Numeric axes, error bars, statistical geometry | `plot-code` |
| Naturalistic cells, materials, organs, or scene metaphor | `image-generation` base + deterministic labels |
| Quantitative evidence plus conceptual mechanism | `hybrid` |
| Need for later author editing | editable vector or native shapes |

If `deterministic_numbers` is true, reject pure image generation.

## 6. Validation and migration

Run:

```bash
python3 scripts/figure_workbench.py validate figure-spec.json --strict
```

Validation has three levels:

- **error** — schema/semantic failure that blocks compilation;
- **warning** — likely scientific or rendering risk;
- **note** — improvement opportunity.

When changing the schema:

1. increment `schema_version`;
2. preserve old claim/entity IDs when meaning is unchanged;
3. add a migration function before deleting fields;
4. update example specs and tests;
5. compile before and after, then compare scientific inventory.
