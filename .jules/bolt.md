## 2025-05-15 - [CLI Startup Latency]
**Learning:** Top-level imports of heavy libraries like `groq` and `pydantic` (via submodules) add ~0.6s of overhead to every CLI command, even `--help`.
**Action:** Use lazy loading within Click command functions to only import what's needed for the specific command being executed.
