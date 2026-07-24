# Contributing

Contributions should improve scientific correctness, auditability, or reproducibility—not merely add more style adjectives.

## Before opening a pull request

1. Keep the installable Skill under `skills/research-figure/`.
2. Keep `SKILL.md` under 500 lines and move detailed material to a directly linked reference.
3. Do not add a README, changelog, or installation guide inside the Skill package.
4. Give every prompt change a prompt ID/version and a regression fixture.
5. Use synthetic, open-licensed, or sufficiently short attributed source material.
6. Do not commit API keys, unpublished papers, participant data, reviewer material, or provider logs containing private content.
7. Preserve backward compatibility for FigureSpec 1.0 or provide a migration.

## Required checks

```bash
python3 -m unittest discover -s tests -v
python3 skills/research-figure/scripts/figure_workbench.py check-links --strict
```

For a new example, include:

- source scope and license/provenance;
- valid FigureSpec;
- deterministic compiled prompt;
- audit template or completed audit;
- a test that captures the intended scientific guardrail.

For a bug fix, add the smallest fixture that fails before the change and passes after it.

## Prompt contribution rubric

A prompt instruction belongs in the project only when:

- its input and output are explicit;
- its effect can be observed or tested;
- it does not duplicate another stage;
- it fails safely when evidence is missing;
- it does not silently depend on one provider's undocumented behavior;
- it preserves exact text, values, and relation semantics.

Keep role adapters separate from renderer adapters. Fix upstream evidence or semantic errors in FigureSpec rather than adding downstream negative prose.

## Scientific review

Pull requests that change relation semantics, evidence status, quantitative rules, image-integrity behavior, or venue guidance require a focused scientific-integrity review. A high aesthetic score is not evidence that the change is correct.
