# ClaimCrawl synthetic design brief

This fixture is an illustrative reconstruction created for testing. It does not describe verified scientific results.

Anchors:

- `B1`: Candidate-only evaluation can hide retrieval behavior.
- `B2`: A full-flow API outcome alone does not localize whether a failure occurred during retrieval, selection, or coverage tracking.
- `B3`: The design separates three responsibilities: a crawler acquires candidates, a selector prioritizes candidates, and a coverage controller records explored scope.
- `B4`: The brief contains no benchmark values or causal performance evidence.

Safe uses:

- Motivation: distinguish three diagnostic bottlenecks without claiming universal failure.
- Method: show the three responsibilities and high-level procedural handoffs.

Unsafe uses:

- Invent benchmark gains.
- Claim that the coverage controller prevents all failures.
- Present this fixture as a real published system.
