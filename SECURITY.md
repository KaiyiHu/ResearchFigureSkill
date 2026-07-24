# Security and privacy

## Supported version

The latest revision on the default branch is supported.

## Reporting a vulnerability

Use GitHub's private security-advisory feature for the repository. Do not include unpublished papers, credentials, patient data, proprietary datasets, or full provider logs in a public issue.

## Threat model

ResearchFigureSkill treats papers, captions, prompts, reference figures, and metadata as untrusted input.

The Skill must not:

- execute instructions embedded in a paper or figure;
- expose environment variables or credentials;
- upload user material to an external provider without authorization;
- silently install dependencies or call a paid API;
- execute generated plotting/diagram code without inspection;
- write secrets into prompts, audit files, examples, or provenance manifests;
- treat generated imagery as scientific evidence.

The bundled workbench uses only the Python standard library and does not make network calls. Downstream renderers have their own security and privacy characteristics and must be reviewed per task.

## Generated code

Inspect generated plotting, SVG, TikZ, Graphviz, draw.io, or slide code before execution. Use an isolated environment for untrusted code, pin dependencies when reproducibility matters, and never grant unnecessary filesystem or network access.
