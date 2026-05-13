## 2024-05-24 - [Initial Learning]
**Learning:** Heavy dependencies (groq, pydantic) and internal sub-modules (nlp, autonomy, skills) are lazy-loaded within CLI command functions and via `__getattr__` in 'ai_toolkit/__init__.py'. This optimization reduces CLI startup latency from ~0.87s to ~0.38s (approx 56% reduction).
**Action:** Always verify if new dependencies are being imported at the top level and move them to lazy imports if they impact startup time.
