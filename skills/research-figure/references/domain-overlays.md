# Domain overlays

Load one overlay only after the universal evidence, FigureSpec, role, and renderer rules are fixed. An overlay adds domain semantics; it must not create new claims or override source evidence.

## Contents

1. AI and machine learning
2. Agents, reinforcement learning, and control
3. Life sciences and medicine
4. Chemistry and materials
5. Robotics and embodied systems
6. Theory and mathematical concepts
7. Cross-domain and multimodal figures

## 1. AI and machine learning

### Preserve

- input/output object types;
- tensor or representation dimensions when scientifically material;
- training vs inference paths;
- shared vs separate parameters;
- repeated blocks and iteration counts;
- loss-only edges vs inference-time data flow;
- retrieval, memory, tool, and environment boundaries;
- evaluation setting and baseline identity.

### Relation safeguards

- A gradient/update edge is not an inference data-flow edge.
- Attention or similarity is not automatically causal influence.
- A retrieval arrow should name query, candidate, score, or evidence payload.
- A dashed “optional” module is not the same as a hypothesized mechanism.
- A feedback loop must state what state or signal returns and when it terminates.

### Renderer

Prefer vector code for architecture and pipeline figures. Render equations and tensor shapes deterministically. Use generated icons only as non-semantic decoration or clearly inventoried assets.

### Common failures

- train/inference fusion;
- invented tensor sizes;
- decorative brain/robot icons replacing topology;
- a benchmark badge inside a method figure;
- attention heatmap used as causal explanation;
- “agent” drawn as anthropomorphic intention unsupported by the system.

## 2. Agents, reinforcement learning, and control

### Preserve

- agent, policy/controller, environment/plant, observation, state, action, reward/cost;
- online vs offline data;
- model-based vs model-free components;
- planning horizon and rollout when relevant;
- exploration vs execution;
- safety filter or constraint location;
- real-world vs simulated loop.

### Relation safeguards

Use distinct labels:

```text
environment → observation → agent
agent → action → environment
environment → reward/cost → learner
learner → parameter update → policy
```

Do not merge an optimization update with an environment transition. Do not show reward as ground-truth correctness. A safety filter does not guarantee safety unless the evidence and specification support that boundary.

### Mechanism claims

An RL ablation can show a contribution under tested settings; it rarely proves a universal behavioral mechanism. Label proposed explanations and distinguish learned policy behavior from designer intention.

## 3. Life sciences and medicine

### Preserve

- biological scale and compartment;
- cell/tissue/organ identity;
- molecular directionality;
- activation, inhibition, transport, binding, cleavage, expression, and differentiation semantics;
- intervention dose/time/route when relevant;
- experimental vs proposed pathway;
- sample, cohort, and assay scope;
- anatomical orientation and scale bars.

### Relation safeguards

- Use domain-standard activation arrows and inhibition T-bars with a legend.
- Use transport arrows only across the correct compartment boundary.
- Do not infer a pathway edge from co-expression alone.
- Distinguish direct binding, downstream association, and author-proposed mechanism.
- Preserve uncertainty and alternative pathways.

### Renderer

Use validated domain tools for exact molecular structures, sequences, phylogenies, anatomy, and quantitative plots. Image generation may create a conceptual graphical-abstract asset but must not replace microscopy, pathology, gels/blots, clinical images, or other evidence.

### Integrity

- Preserve original evidence images and processing history.
- Protect participant/patient privacy.
- Record representative-image selection.
- Do not add, remove, move, or duplicate evidence-bearing features.
- Verify icons/biological assets and licenses.

### Common failures

- causal pathway invented from correlation;
- organelle or tissue placed in the wrong compartment;
- receptor direction or activation/inhibition reversed;
- illustrative cell mistaken for an observed micrograph;
- population-level association shown as an individual treatment effect.

## 4. Chemistry and materials

### Preserve

- chemical identity, composition, stoichiometry, charge, phase, and state;
- reaction direction, catalyst, solvent, temperature, pressure, time, and atmosphere when material;
- crystal/lattice orientation and defects;
- processing history;
- length/energy/time scale;
- characterization modality;
- simulated vs measured structure.

### Relation safeguards

- A reaction arrow requires source-supported reactants/products and conditions.
- A schematic transport arrow must identify species and direction.
- Energy diagrams require quantitative or explicitly qualitative scale.
- Structural similarity does not establish reaction mechanism.
- A proposed nucleation/growth mechanism must remain visibly hypothetical when unverified.

### Renderer

Use chemistry/crystallography/materials software for exact structures, spectra, diffraction, band diagrams, and quantitative geometry. Use vector code for process schematics. Use image generation only for clearly conceptual scene assets.

### Common failures

- invented bonds, valence, lattice planes, or stoichiometry;
- decorative particle counts interpreted quantitatively;
- gradient implying concentration without a legend;
- simulated image presented as measurement;
- material phase or scale omitted.

## 5. Robotics and embodied systems

### Preserve

- coordinate frames and transformations;
- sensor modality and observation timing;
- perception, state estimation, planning, control, and actuation boundaries;
- robot/environment interaction;
- simulation vs hardware;
- centralized vs distributed computation;
- safety, latency, and communication constraints when claimed.

### Relation safeguards

- Label sensor data, estimated state, plan, command, and physical feedback separately.
- Do not connect an optimizer into deployment unless online optimization occurs.
- A world-model prediction is not an observation.
- A planned trajectory is not the executed trajectory.
- A simulator result is not physical-world validation.

### Renderer

Use vector diagrams for system topology and coordinate transforms; validated plotting for trajectories and errors; source images for hardware evidence. Generated robot scenes must be labeled illustrative.

### Common failures

- reversed sensor/action flow;
- coordinate frame omitted;
- offline training loop shown in real-time control;
- simulated success shown as field deployment;
- collision-free icon interpreted as a safety guarantee.

## 6. Theory and mathematical concepts

### Preserve

- objects, domains, assumptions, operators, definitions, and quantifiers;
- sufficient vs necessary conditions;
- theorem statement and scope;
- implication direction;
- exact notation;
- counterexamples and boundary cases.

### Relation safeguards

- Implication is not equivalence.
- Set inclusion is not equality.
- Optimization objective is not achieved optimum.
- A geometric intuition is not a proof.
- An existence result is not a constructive algorithm.

### Renderer

Render notation and geometry programmatically. Use TikZ, SVG, plotting code, or a theorem-specific tool. Do not use an image model to typeset exact equations or construct evidence-bearing geometry.

### Common failures

- arrow direction strengthens a theorem;
- “if” becomes “if and only if”;
- illustrative regions imply exact measure;
- axes or boundaries omitted;
- notation silently normalized into a different definition.

## 7. Cross-domain and multimodal figures

When a figure combines domains:

1. Keep one universal claim ledger.
2. Add a domain tag to each panel/entity.
3. Apply the corresponding overlay locally.
4. Define cross-domain relations and units explicitly.
5. Use separate renderers for exact structures, data, and illustration assets.
6. Audit terminology, scale, and epistemic status within each panel and across interfaces.

Example:

```text
microscopy image (source evidence)
  → quantified morphology (plot code)
    → model prediction (AI/ML panel)
      → proposed biological interpretation (causal-hypothesis)
```

Do not let the model prediction or proposed interpretation visually overwrite the evidence boundary.
