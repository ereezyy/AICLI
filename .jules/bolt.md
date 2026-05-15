## 2025-05-15 - Lazy-loading imports for CLI performance
**Learning:** Eagerly importing heavy dependencies like `groq` and `pydantic` in a CLI entry point significantly increases startup latency (from ~0.38s to ~0.89s). Implementing lazy-loading via `__getattr__` in the package's `__init__.py` and moving imports inside function scopes effectively mitigates this.
**Action:** Use `__getattr__` for lazy-loading in all future Python CLI projects to keep the "time-to-help" low.
