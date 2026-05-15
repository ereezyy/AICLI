## 2026-05-15 - Lazy Loading with Module-level Functions
**Learning:** Implementing PEP 562 `__getattr__` for lazy loading sub-modules works for external access, but internal convenience functions in the same module will raise `NameError` if they try to access the lazy-loaded attributes directly without using `getattr(sys.modules[__name__], ...)`.
**Action:** Always use `getattr(sys.modules[__name__], name)` within module-level functions when referring to attributes intended to be lazy-loaded via `__getattr__`.
