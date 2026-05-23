# Bolt Performance Journal

## 2026-05-23 - [CLI Startup Optimization via Lazy Loading]
**Learning:** Top-level imports of heavy dependencies (groq, subprocess) and internal submodules were causing a significant delay (~0.38s) in CLI startup, even for simple commands like --help.
**Action:** Move heavy imports to local function scope and implement PEP 562 __getattr__ for lazy loading in the package's __init__.py to ensure "pay-for-what-you-use" import behavior.
