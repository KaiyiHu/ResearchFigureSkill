# Changelog

All notable changes to this project are documented in this file.

The project follows semantic versioning for the public Skill contract, prompt
protocols, and FigureSpec schema.

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
