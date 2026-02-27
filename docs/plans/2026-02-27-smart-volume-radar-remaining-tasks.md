# Smart Volume Radar — Pending Tasks

> Consolidated plan from code-quality-hardening. Source: docs/plans/2025-02-23-code-quality-hardening.md

**Date:** 27 February 2026

---

## Lint & Code Quality (from Task 3)

| # | Task | File |
|---|------|------|
| 1 | Resolve `no-explicit-any` warnings | marketData.ts, newsService.ts, telegramBot.ts |
| 2 | Add explicit return types to telegramBot helpers | telegramBot.ts (formatMessageDataHeader, etc.) |
| 3 | Fix unused variable (if any remain) | llmSummary.ts, newsService.ts, telegramBot.ts |

**Verification:** `npm run build && npm test && npm run lint` → 0 errors

---

## Deferred (Future Plan)

| # | Task | Notes |
|---|------|------|
| 1 | Add typed interfaces for Yahoo Chart, Twelve Data, Telegram API responses | Remove `as any` casts; separate plan with API response parsing tests |
| 2 | Add explicit return types to all telegramBot helper functions | LOW priority |

---

## Priority order

1. **Lint (1–3):** If warnings are bothersome — fix
2. **Deferred:** Separate plan when there's time
