# Project Audit Report — Smart Volume Radar

**Date:** 2026-03-01  
**Project:** smart-volume-radar  
**Type:** BACKEND (Node.js CLI)

---

## Sources Used

| Source | Path |
|--------|------|
| Project brief | `02-projects/smart-volume-radar/project.smart-volume-radar.md` |
| Architecture | `04-knowledge/reference/smart-volume-radar-architecture.md` |
| Standards | `04-knowledge/standards/smart-volume-radar-standards.md` |
| Reference docs | `04-knowledge/reference/smart-volume-radar-*.md` (calculations, message guide, indicator sources) |
| Plans | `docs/plans/2026-03-01-smart-volume-radar-remaining-tasks.md` |
| Agents | explorer (discovery), security-sentinel |
| Scripts | `npm audit`, `npm run lint`, `npm test -- --coverage` |

---

## Executive Summary

Smart Volume Radar is a well-structured Node.js CLI for daily stock volume monitoring. Architecture is clear, security basics are in place, and tests cover core logic. Main gaps: **test coverage** for telegram/news/LLM services, **CI enhancements** (npm audit, coverage reporting), and **minor security hardening** (LLM output escaping, numeric config validation).

| Category | Status | Notes |
|----------|--------|-------|
| Architecture | ✅ Solid | Clear layering, single entry point, good reference docs |
| Dependencies | ✅ Safe | 3 production deps, 0 npm audit vulnerabilities |
| Security | ⚠️ Good | Validation and escaping in place; LLM output unescaped |
| Error handling | ✅ Acceptable | Centralized; failure notification via Telegram |
| Concurrency | ✅ Good | p-limit with documented limits (3–5 tickers, 2 news) |
| Test coverage | ⚠️ Partial | ~59% statements; telegramBot, newsService, llmSummary untested |
| CI/CD | ⚠️ Functional | Lint/build/test; no npm audit or coverage reporting |
| Code quality | ✅ Good | Strict TS, ESLint, Prettier |

---

## 1. Architecture (Explorer)

### Structure

```
smart-volume-radar/
├── src/
│   ├── index.ts              # Main entry, orchestration
│   ├── config/               # Env, watchlist, validateConfig
│   ├── services/
│   │   ├── marketData.ts     # Yahoo + Twelve Data; p-limit concurrency
│   │   ├── rvolCalculator.ts
│   │   ├── newsService.ts    # Finnhub; p-limit
│   │   ├── telegramBot.ts   # Format + send
│   │   └── llmSummary.ts    # Optional AI summary
│   ├── types/
│   └── utils/                # technicalAnalysis, logger, errorHandler, escapeHtml
├── tests/
└── scripts/                  # send-legend
```

### Data Flow

1. `fetchAndCacheWatchlist()` — Google Sheet symbols
2. `fetchAllStocks()` — Yahoo (primary) or Twelve Data (fallback)
3. `calculateRVOL()` — filter by MIN_RVOL, sort, TOP_N
4. `enrichWithNews()` — Finnhub headlines
5. `sendDailyReport()` — format + Telegram

### Cross-module Dependencies

- `marketData` → `technicalAnalysis`, `config`
- `newsService` → `config`, `errorHandler`, `fast-xml-parser`
- `telegramBot` → `llmSummary`, `escapeHtml`, `config`
- `llmSummary` → `config`, `p-limit`
- `rvolCalculator` → `types` only

---

## 2. Security (security-sentinel)

### Strengths

| Area | Status |
|------|--------|
| Secrets | Loaded via dotenv; only presence logged (`key=✓ set`) |
| GitHub Actions | Uses `secrets.*`; no values in workflow text |
| Ticker validation | `validateTicker()` — regex, length ≤12 |
| Google Sheet ID | `validateGoogleSheetId()` — regex, 20–60 chars |
| URL construction | `encodeURIComponent` for tickers, sheet ID |
| Telegram HTML | `escapeHtml` for tickers, sector, headlines, sources |
| Supply chain | `npm audit`: 0 vulnerabilities |

### Findings & Recommendations

| # | Severity | Finding | Recommendation |
|---|----------|---------|-----------------|
| 1 | P1 — Medium | LLM output (`a.analysis`, batch summary) inserted into Telegram HTML without escaping | Apply `escapeHtml()` to LLM output before insertion |
| 2 | P2 — Low | Numeric env vars (`MIN_RVOL`, `TOP_N`, etc.) use `parseFloat`/`parseInt` without NaN checks | Add `Number.isFinite` or fallbacks like `llmMinRvol` |
| 3 | P2 — Low | `formatErrorForTelegram` could leak URLs/tokens if error.message contains them | Sanitize before sending (strip URLs, redact token-like substrings) |
| 4 | P3 | API keys in query strings (Finnhub, Twelve Data); third-party HTTP clients might log full URLs | Prefer Authorization header where supported; ensure no URL logging |
| 5 | P3 | `escapeHtml` does not escape `'`; low risk for current usage | Optionally add `'` → `&#39;` for future single-quoted attributes |

---

## 3. Test Coverage

### Current State (56 tests, 6 suites)

| Source | Coverage (Stmt/Branch/Func/Lines) | Test File |
|--------|-----------------------------------|-----------|
| `config/index.ts` | 85 / 75 / 93 / 89 | `watchlist.test.ts` |
| `marketData.ts` | 64 / 35 / 82 / 65 | `marketData.test.ts` |
| `rvolCalculator.ts` | 89 / 53 / 100 / 88 | `rvolCalculator.test.ts` |
| `technicalAnalysis.ts` | 100 / 89 / 100 / 100 | `technicalAnalysis.test.ts` |
| `errorHandler.ts` | 100 / 100 / 100 / 100 | `errorHandler.test.ts` |
| `escapeHtml.ts` | 100 / 100 / 100 / 100 | — (used by other tests) |
| `telegramBot.ts` | 34 / 22 / 26 / 35 | **No tests** |
| `newsService.ts` | — | **No tests** |
| `llmSummary.ts` | — | **No tests** |

**Jest thresholds:** Statements 55%, Branches 35%, Functions 55%, Lines 55% ✅ (current: 59 / 41 / 62 / 60)

### Test Gaps (Prioritized)

1. **telegramBot** — Message formatting, chunking (4096 chars), Telegram API flow — **high risk**
2. **newsService** — Finnhub, RSS parsing, enrichment — **medium**
3. **llmSummary** — Provider selection, prompts — **medium**
4. **rvolCalculator** — Already well covered; minor uncovered branches
5. **escapeHtml** — Simple; covered implicitly; explicit unit test would lock behavior

---

## 4. CI/CD (DevOps)

### Workflows

| Workflow | Triggers | Steps |
|----------|----------|-------|
| `ci.yml` | Push/PR to `main`, `develop` | Checkout → `npm ci` → lint → build → test |
| `daily-scan.yml` | Cron 21:30 UTC Mon–Fri, `workflow_dispatch` | Checkout → `npm ci` → `npm run start` |

### Findings

| # | Severity | Finding |
|---|----------|---------|
| 1 | P1 | **daily-scan** does not pass `TWELVE_DATA_API_KEY` — Twelve Data fallback and fetched indicators (RSI, SMA21) will not work in production |
| 2 | P2 | No `npm audit` in CI — add step to fail on high/critical vulnerabilities |
| 3 | P2 | No coverage reporting (e.g. Codecov) — coverage computed but not published |
| 4 | P3 | **daily-scan** does not set LLM keys — `ENABLE_LLM_SUMMARY` may be off; OK if intentional |
| 5 | P3 | No explicit test run before `daily-scan` — relies on `main` being healthy (CI gates pushes) |

---

## 5. Code Quality

### Linting & TypeScript

- **ESLint:** Flat config; TypeScript recommended rules; 0 warnings
- **TypeScript:** `strict: true`, target ES2022, module node16
- **Prettier:** `npm run format` for `src/**/*.ts`

### Technical Debt

1. **Config validation:** `validateConfig` errors are caught and execution continues; only logged
2. **CJS Jest:** `jest.config.cjs` is CommonJS; rest of project is ESM
3. **LLM provider branch:** `llmProvider` branching in `llmSummary.ts` is ad-hoc; could use explicit union/switch
4. **Unused `__dirname`:** `index.ts` defines it but does not use it
5. **Error typing:** `(error as Error).message` used in places; could use type guard

---

## 6. Recommendations (Prioritized)

### P0 — Critical

None identified. Project is production-ready.

### P1 — High

1. **Escape LLM output** — Apply `escapeHtml()` to `a.analysis` and batch LLM summary before inserting into Telegram HTML
2. **daily-scan env** — Add `TWELVE_DATA_API_KEY` to `daily-scan.yml` env if Twelve Data indicators are desired in production

### P2 — Medium

3. **Numeric env validation** — Add NaN checks or fallbacks for `MIN_RVOL`, `TOP_N`, `PRICE_CHANGE_THRESHOLD`, etc.
4. **CI: npm audit** — Add `npm audit --audit-level=high` step to `ci.yml`; fail on high/critical
5. **Error sanitization** — Sanitize `formatErrorForTelegram` output (strip URLs / redact tokens) before Telegram send
6. **Test coverage** — Add unit tests for `telegramBot` (formatting, chunking); consider mocking Telegram API

### P3 — Low

7. **Coverage reporting** — Publish coverage to Codecov or similar (optional)
8. **escapeHtml** — Add `'` → `&#39;` for defense in depth
9. **Remove unused `__dirname`** in `index.ts`
10. **newsService / llmSummary tests** — Add when time permits (ESM/Jest setup issues noted in plans)

---

## 7. Knowledge Gaps

- [x] Architecture doc exists and is up to date
- [x] Standards doc exists
- [x] Calculations, message guide, indicator sources documented
- [ ] Consider: `04-knowledge/reference/smart-volume-radar-deployment.md` for env vars and CI secrets checklist

---

## 8. Next Steps

1. Implement P1 items (LLM escaping, Twelve Data key in daily-scan) in next sprint
2. Add `npm audit` to CI
3. Plan `telegramBot` test suite (format + chunk logic)
4. Update `docs/plans/2026-03-01-smart-volume-radar-remaining-tasks.md` with audit findings; mark completed items

---

## Appendix: Commands Run

```bash
npm audit          # 0 vulnerabilities
npm run lint       # Pass
npm test -- --coverage  # 56 tests, 59% statements, 41% branches, 62% functions, 60% lines
```

---

*Audit conducted per `03-agents/workflows/project-deep-audit.md`*
