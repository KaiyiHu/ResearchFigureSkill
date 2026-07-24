# Changelog

All notable changes to this project are documented in this file.

The project follows semantic versioning for the public Skill contract, prompt
protocols, and FigureSpec schema.

## 2.1.0 — 2026-07-25

### Changed

- Restored the first-release user-facing name, **Research Figure Compiler**.
- Replaced the default multi-artifact compiler path with a short workflow:
  paper summary → Motivation and/or Pipeline template → editable figure →
  one fast critical check.
- Removed automatic figure-role selection. Unspecified requests now generate
  both fixed figure types; explicit requests generate only the named type.
- Reduced default delivery to one summary, one prompt per selected type, one
  editable SVG per selected type, and matching PNG previews.
- Limited normal rendering to the first passing result, with at most one
  targeted repair by default.

### Added

- Dedicated Motivation and Pipeline production templates in
  `references/prompt-templates.md`.
- Lightweight `scripts/quick_qa.py` for live-text, vector-structure, blur
  filter, duplicate-ID, flattening, required-text, and PNG-size checks.

### Compatibility

- The v2.0 FigureSpec schemas, workbench, and detailed audit references remain
  available for users who explicitly request the legacy auditable workflow,
  but the simplified Skill does not load or invoke them by default.

## 2.0.0 — 2026-07-25

### Added

- Full-paper-first `RF-SUMMARIZE-2.0` stage and a detailed summary template
  covering claims, methods, experiments, exact results, limitations, terminology,
  section coverage, figure-portfolio signals, and unresolved questions.
- The explicit production-prompt formula
  `P = J + R + S + N + C + E + L + V + D + X + O + Q`, with contracts for
  reference use, scientific narrative, exact content, typed relations, normalized
  layout, editable construction, negative constraints, outputs, and QA.
- A renderer-ready final-prompt template plus deterministic `lint-prompt`
  checks for canonical summary/spec binding, section order, unresolved
  placeholders, exact text, relations, negatives, editability, and output
  requirements.
- Deterministic SVG inspection for live text, exact-label coverage, blur
  filters, hidden/off-canvas text, raster native dimensions and upscaling,
  stable entity/relation IDs, duplicate IDs, and glyph hazards.
- Reference-figure and normalized-region fields that preserve permitted
  abstract layout attributes without treating a reference as evidence or
  copying its protected expression.
- Technical audit records for final-size, 100%, and 200% inspection, editable
  source verification, artifact/source paths and SHA-256 hashes, inventory
  comparison, file-signature/container sanity checks, and localized defect
  reporting.

### Changed

- Reframed the primary workflow as detailed full-paper summary → evidence
  constraints → figure-role decision → FigureSpec → prompt compilation →
  renderer routing → artifact audit → editable delivery.
- Upgraded prompt compilation and artifact critique to `RF-COMPILE-2.0` and
  `RF-CRITIQUE-2.0`.
- Made a completed detailed summary a compiler input and embedded its SHA-256
  in every compiled prompt; thin, duplicated, out-of-order, or anchor-missing
  summaries are rejected.
- Strengthened renderer adapters: quantitative evidence stays in plot code;
  exact labels and relations stay in vector layers; image-generation routes
  prefer text-free base art with deterministic overlays.
- Made pseudo-text, wrong fonts or glyphs, local blur, fuzzy or melted shapes,
  ghosting, clipping, overlap, rasterized required text, low-resolution assets,
  and upscaling artifacts blocking failures.
- Updated the ClaimCrawl regression fixture to keep inferred controller
  behavior out of the final method diagram.

### Compatibility

- FigureSpec moves to schema version 2.0. Version 1.0 specifications must add a
  stable `id` to every relation and adopt the stricter summary, reference,
  prompt, and artifact-audit contracts before recompilation.
- Existing tracked installations can update with
  `gh skill update research-figure --dir ~/.codex/skills`.

## 1.0.1 — 2026-07-24

### Changed

- Replaced placeholder installation examples with the public repository URL.
- Added GitHub CLI installation and tracked-update commands in English and
  Chinese documentation.

## 1.0.0 — 2026-07-24

### Added

- Evidence-locked eight-gate workflow for planning, prompting, building,
  critiquing, and repairing research figures.
- Versioned prompt chain from source grounding through renderer compilation,
  artifact critique, minimal patching, captioning, alt text, and disclosure.
- FigureSpec 1.0, evidence-ledger, and figure-audit JSON schemas.
- Typed relation semantics with explicit causal and causal-hypothesis guards.
- Renderer risk routing across vector code, deterministic plot code, image
  generation, and hybrid composition.
- Role playbooks for motivation, method, mechanism, experiment, ablation,
  comparison, taxonomy, graphical abstract, and deliberate mixed figures.
- Domain overlays for AI/ML, agent/control systems, life sciences,
  chemistry/materials, robotics, and theory.
- Standard-library CLI for scaffolding, semantic validation, deterministic
  prompt compilation, audit-template generation, and repository checks.
- Three worked example families and 24 automated regression tests.
- Market landscape, scientific-integrity rules, contribution guidance,
  security guidance, and GitHub Actions CI.

### Quality gates

- Scientific or structural hard failures cannot be averaged away by aesthetics.
- Quantitative figures cannot use pure image generation for evidence geometry.
- Supported claims require anchors; missing claims cannot enter final panels.
- Hypotheses and inferences require visible epistemic labels.
- A passing audit requires complete scores, no blocking reader inference, and
  the configured thresholds.
