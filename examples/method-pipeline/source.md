# Synthetic verification pipeline

This fixture is fictional and used only for regression testing.

- `M1`: A query encoder converts a text query into an embedding.
- `M2`: A retriever uses the embedding to return candidate passages.
- `M3`: A verifier scores candidate support and emits verified evidence.
- `M4`: Failed candidates are logged for inspection; the fixture does not state that they trigger another retrieval cycle.
- `M5`: No benchmark result or causal performance evidence is provided.
