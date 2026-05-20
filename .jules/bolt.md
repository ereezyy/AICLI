# ⚡ Bolt's Performance Journal

## 2026-05-20 - Initializing Bolt
**Learning:** Found that CLI startup is delayed by ~0.4s due to top-level 'groq' import and other heavy dependencies.
**Action:** Defer heavy imports to command functions and implement lazy loading in the core package.
