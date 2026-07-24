# Scientific integrity, provenance, and venue checks

Use this reference for submission-oriented work, quantitative figures, image panels, generated assets, reference-based styling, or unpublished material.

## Contents

1. Evidence integrity
2. Quantitative integrity
3. Image integrity
4. Generated-asset provenance
5. Privacy and unpublished work
6. Reference-figure use
7. Venue verification
8. Handoff manifest

## 1. Evidence integrity

- Keep claim strength at or below source evidence.
- Preserve uncertainty, exceptions, negative results, and tested scope.
- Distinguish observation, association, intervention, mechanism, and hypothesis.
- Do not use icons, arrows, size, color, or proximity to smuggle in an unsupported claim.
- Keep a source anchor for every central visual claim.
- Require author/domain-expert approval for scientific interpretation before submission.

When the source conflicts with itself, visualize the conflict only if it is the intended message; otherwise stop and request resolution.

## 2. Quantitative integrity

Generate quantitative geometry only from machine-readable data or a verified transcription.

Record:

- source file and immutable identifier/checksum when practical;
- filters and exclusions;
- transformations and normalization;
- category ordering;
- units;
- missing-value behavior;
- sample size;
- uncertainty/error-bar definition;
- statistical test and correction;
- random seed for stochastic layouts;
- plotting code and library versions when reproducibility matters.

Do not:

- infer bar heights from prose;
- redraw a plot with a text-to-image model;
- change axis limits solely to strengthen the claim;
- smooth, aggregate, or normalize without disclosure;
- add significance annotations not present in the analysis.

## 3. Image integrity

For microscopy, medical, remote-sensing, gel/blot, or other evidentiary images:

- preserve original files and metadata;
- document crop, rotation, contrast, denoising, stitching, and pseudocolor;
- apply global adjustments consistently unless local processing is scientifically justified and disclosed;
- retain scale bars and calibration;
- do not remove, add, move, or duplicate evidence-bearing content;
- distinguish representative images from quantitative summaries;
- keep panel provenance and sample IDs.

Do not use generative fill or generated substitutes in evidence-bearing panels.

## 4. Generated-asset provenance

For each generated or externally sourced asset, record:

```json
{
  "asset_id": "asset-icon-01",
  "role": "decorative conceptual illustration",
  "provider": "name or local model",
  "model": "model/version when available",
  "prompt_id": "RF-COMPILE-1.0",
  "prompt_file": "compiled-prompt.md",
  "source_references": [],
  "license_or_terms_checked": true,
  "scientific_evidence": false,
  "edits": ["background removed", "labels added deterministically"]
}
```

Generated assets must not masquerade as observed data. Label simulations, illustrative examples, and hypotheses where a reader could confuse them with evidence.

## 5. Privacy and unpublished work

Before using an external provider, determine whether the input contains:

- unpublished paper text;
- reviewer material;
- patient or participant information;
- proprietary code/data;
- export-controlled or confidential material;
- credentials, internal paths, or metadata.

Default to local analysis and prompt preparation. Send material externally only when the user has authorized that service and the data handling is appropriate.

Do not put secrets in prompts, logs, provenance manifests, examples, or screenshots.

## 6. Reference-figure use

Use a reference to extract abstract attributes:

- panel topology;
- density;
- color roles;
- line weight;
- typography hierarchy;
- amount of whitespace;
- icon abstraction level.

Do not copy:

- distinctive composition and expression wholesale;
- protected icons or illustrations without license;
- another paper's data or scientific content;
- watermarks, journal branding, or author identifiers.

When the user requests “same style,” translate it into a neutral style specification and retain necessary attribution/license information.

## 7. Venue verification

Publisher and conference rules change. When a venue or journal is named:

1. Search the current official author instructions and policy pages.
2. Record the access date and exact page URL.
3. Verify:
   - column/page dimensions and file formats;
   - font and line legibility expectations;
   - resolution and color-space requirements;
   - accessibility guidance;
   - image manipulation policy;
   - generative-AI image/text policy and disclosure;
   - copyright/license and third-party asset rules;
   - supplementary/source-data requirements.
4. Separate official requirements from house-style preference.
5. If rules are silent or ambiguous, say so and request author/editorial judgment.

Do not create fictional “AAAI style,” “NeurIPS style,” “ACL style,” or “Nature style” rules. These venues have official formatting/policy constraints and observable publication conventions, not a single mandatory illustration aesthetic.

## 8. Handoff manifest

Use a compact `provenance.json`:

```json
{
  "figure_id": "fig-1",
  "figure_spec": "figure-spec.json",
  "source_scope": ["§3", "Table 2", "results.csv"],
  "render_route": "hybrid",
  "editable_source": "figure.svg",
  "preview": "figure.png",
  "data_sources": ["results.csv"],
  "generated_assets": [],
  "audit": "figure-audit.json",
  "venue_policy_checks": [
    {
      "url": "official URL",
      "accessed": "YYYY-MM-DD",
      "requirement": "verified statement"
    }
  ],
  "author_approval": "pending"
}
```

Keep the manifest useful but free of confidential content.
