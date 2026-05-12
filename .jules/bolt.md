## 2025-05-15 - Lazy Loading for CLI Performance
**Learning:** Heavy dependencies like 'groq', 'pydantic', and large internal submodules (nlp, autonomy, skills) significantly impact CLI startup latency. Moving these to function-level imports (lazy loading) can reduce startup time by over 50%. Using PEP 562 (__getattr__) in package __init__.py allows for transparent lazy loading of sub-packages.
**Action:** Always prefer lazy loading for non-essential dependencies in CLI entry points.
