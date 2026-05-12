## 2025-05-15 - [Import Overhead in CLI]
**Learning:** The AI Toolkit CLI eagerly loads all submodules and their dependencies (like `groq`, `tensorflow` if present, etc.) even for simple help commands or unrelated tasks. This increases startup latency.
**Action:** Implement lazy loading using `__getattr__` in `__init__.py` and move imports inside CLI command functions.
