# Contributing

Current public version: **1.0**.

Contributions should improve scientific correctness, auditability, or reproducibility—not merely add more style adjectives.

## Before opening a pull request

1. Keep the installable Skill under `skills/research-figure/`.
2. Keep `SKILL.md` under 500 lines and move detailed material to a directly linked reference.
3. Do not add a README, changelog, or installation guide inside the Skill package.
4. Keep the fixed Motivation and Pipeline templates concise and fully filled.
5. Use synthetic, open-licensed, or sufficiently short attributed source material.
6. Do not commit API keys, unpublished papers, participant data, reviewer material, or provider logs containing private content.
7. Preserve the compact first-version PPTX + PNG delivery filenames.

## Required checks

```bash
python3 -m unittest discover -s tests -v
python3 skills/research-figure/scripts/quick_qa.py --help
```

For a bug fix, add the smallest fixture that fails before the change and passes after it.
The SVG helper is a legacy optional check; PowerPoint output must be rendered
and inspected visually with the current Presentations workflow.

## Prompt contribution rubric

A prompt instruction belongs in the project only when:

- its input and output are explicit;
- its effect can be observed or tested;
- it does not duplicate another stage;
- it fails safely when evidence is missing;
- it does not silently depend on one provider's undocumented behavior;
- it preserves exact text, values, and relation semantics.

Fix unsupported scientific content in the paper summary or filled template
rather than hiding it with downstream negative prose.

## Scientific review

Pull requests that change relation semantics, quantitative rules, image
integrity, safe-area behavior, or existing-figure handling require a focused
scientific-integrity review. A high aesthetic score is not evidence that the
change is correct.
