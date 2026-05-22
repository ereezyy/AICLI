## 2025-05-15 - Deferred Imports for CLI Startup Optimization
**Learning:** Eagerly importing heavy third-party libraries (like 'groq' or 'fastapi') and internal submodules at the top level of a CLI entry point significantly inflates startup latency (~0.88s).
**Action:** Use PEP 562 (__getattr__) for lazy loading in the package root and move heavy imports into CLI command functions to defer execution cost until necessary. This reduced startup time to ~0.12s.
