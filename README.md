# ResearchFigureSkill

> Summarize the paper, fill a strong prompt template, generate an editable
> motivation and/or pipeline figure, then run one fast critical check.

[中文说明](README.zh-CN.md) · [Changelog](CHANGELOG.md) ·
[Contributing](CONTRIBUTING.md)

The user-facing name is again **Research Figure Compiler**, matching the first
release. The default workflow is deliberately small:

```mermaid
flowchart LR
    A["Allowed paper content"] --> B["One paper summary"]
    B --> C{"Requested output"}
    C --> D["Motivation prompt"]
    C --> E["Pipeline prompt"]
    D --> F["Style-faithful PNG"]
    E --> G["Style-faithful PNG"]
    F --> H["Editable companion"]
    G --> H
    H --> I["Fast critical QA"]
```

## Two fixed figure types

- **Motivation** — status quo → observed limitation → bounded research need.
- **Pipeline** — typed input → 3–7 named stages → typed output.

The Skill no longer spends time deciding which role “wins”:

- ask for `motivation` and it creates only motivation;
- ask for `pipeline` and it creates only pipeline;
- ask for both, or do not specify, and it creates both.

## Prompt templates are the core asset

[`prompt-templates.md`](skills/research-figure/references/prompt-templates.md)
contains the two production templates. Each template includes:

- the scientific purpose and five-second message;
- exact visible labels and explicit arrow contracts;
- layout and visual-language instructions;
- editable construction requirements;
- a role-specific negative prompt;
- a short preflight checklist.

The agent first writes one useful summary, then fills the selected template.
There is no default evidence-ledger, FigureSpec, role-analysis, provenance, or
audit-JSON stage.

## Reference fidelity and rendering order

When the user supplies a desired example, the Skill treats it as the **primary
visual and compositional reference**. It preserves the requested panel
topology, dashed-border treatment, handwriting character, icon language,
arrow rhythm, palette behavior, and information density while replacing all
source-specific scientific content.

Reference-led work is image-first by default: the filled prompt and reference
are sent directly to the image generator for the style-faithful PNG. If
editability is requested, an SVG companion is then reconstructed with live
corrected labels, borders, and arrows. The Skill discloses any raster
illustration instead of falsely describing a hybrid file as fully vector.

Without a reference, the default is a hand-drawn academic infographic—not a
SaaS dashboard or equal-card corporate diagram.

## Minimal default outputs

For one figure type:

```text
paper-summary.md
motivation-prompt.md  or  pipeline-prompt.md
motivation.svg        or  pipeline.svg
motivation.png        or  pipeline.png
```

When both are requested, the same summary is reused. QA is reported in the
response instead of creating another file.

## Fast QA

The generated artifact is inspected once at 100% and once at 200% for:

1. unsupported or invented scientific content;
2. missing components or wrong arrow direction;
3. misspelled, corrupted, or unreadable text;
4. blur, fuzzy/melted shapes, overlap, and clipping;
5. live text and separate editable vector objects.

When a reference is supplied, QA also rejects a render that drifts into a
different style family.

If a critical gate fails, the agent makes one targeted repair and stops at the
first passing result. The default maximum is two renders.

The optional structural helper is:

```bash
python3 skills/research-figure/scripts/quick_qa.py \
  motivation.svg motivation.png \
  --required-text "Exact label"
```

It checks SVG/XML validity, live text, duplicate IDs, blur filters,
full-canvas raster flattening, required strings, vector geometry, and PNG
dimensions. Visual and scientific inspection still matters.

Use `--allow-hybrid` only for a disclosed image-first SVG companion whose
illustration remains raster but whose corrected labels and structural overlays
are genuinely editable.

## Install and update

Install with a recent GitHub CLI:

```bash
gh skill install KaiyiHu/ResearchFigureSkill research-figure \
  --agent codex --scope user
```

Update a tracked installation:

```bash
gh skill update research-figure --dir ~/.codex/skills
```

Manual fallback:

```bash
git clone https://github.com/KaiyiHu/ResearchFigureSkill.git
cp -R ResearchFigureSkill/skills/research-figure ~/.codex/skills/research-figure
```

Manual copies do not carry tracked-update metadata. Reload Codex after install
or update if the old Skill instructions remain cached.

## Usage

Create both figures:

```text
Use $research-figure to summarize this paper, fill the motivation and pipeline
prompt templates, generate both editable figures, and stop after the first
passing critical check.
```

Create only motivation:

```text
Use $research-figure to generate an editable motivation figure for this paper.
Do not inspect the two excluded placeholder captions.
```

Create only pipeline:

```text
Use $research-figure to summarize the paper and generate only the editable
pipeline figure.
```

## Safety boundaries

- Explicitly excluded source regions are never read or used.
- Exact values, equations, axes, and final labels are deterministic.
- Private or unpublished material is not sent to an external provider without
  authorization.
- Reference figures control the requested visual grammar, but never supply
  scientific evidence; their text, values, logos, and source-specific symbols
  are replaced.
- The Skill does not replace scientific, statistical, clinical, or legal
  review.

## License

[MIT](LICENSE)
