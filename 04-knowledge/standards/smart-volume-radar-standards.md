# Smart Volume Radar — Cursor Rules & Standards

> Repo: smart-volume-radar. Read this when working on the project.

## Tech Stack

- Node.js, TypeScript 5.9, ESM, Node ≥20
- tsx for execution
- Jest, ESLint, Prettier
- APIs: Yahoo Finance (chart), Finnhub, Twelve Data (optional), Telegram Bot
- GitHub Actions for CI/CD

## Quick Reference — Entity & Conventions

| Domain | Pattern |
|--------|---------|
| **Config** | Central `config` object from env; `fetchAndCacheWatchlist()` before scan |
| **Watchlist** | Google Sheet CSV; Column A=symbol, B=sector |
| **Data flow** | Yahoo primary → Twelve Data fallback; p-limit for concurrency (3–5 tickers) |
| **Logging** | `logger` only; never `console.log` |
| **Imports** | Top of file only; no inline imports |

## Naming

| Type | Pattern | Example |
|------|---------|---------|
| Files | camelCase | `marketData.ts`, `rvolCalculator.ts` |
| Functions | camelCase | `fetchAllStocks`, `calculateRVOL` |
| Types | PascalCase | `StockData`, `RVOLResult`, `TickerConfig` |
| Plan files | `YYYY-MM-DD-kebab.md` | `2026-02-27-smart-volume-radar-remaining-tasks.md` |

## Plan Lifecycle

1. **On task completion** — Update docs in Obsidian (`04-knowledge/reference/smart-volume-radar-*.md`)
2. **Completed plans** — Delete from `docs/plans/` (or move to archive)
3. **Pending tasks** — Single file in `docs/plans/YYYY-MM-DD-smart-volume-radar-remaining-tasks.md` in vault
4. **Before deleting Plan** — Ensure all relevant decisions have been moved to Reference

## Review Checklist (Node CLI)

- **Logging** — No `console.log`, uses `logger` with context
- **Error Handling** — Try-catch for async, centralized handlers, helpful messages
- **TypeScript** — No `any` types, proper interfaces, no `@ts-ignore`
- **Production Readiness** — No debug statements, no TODOs, no hardcoded secrets
- **Architecture** — Follows existing patterns, code in correct directory

## Reference (vault)

- Architecture: [[04-knowledge/reference/smart-volume-radar-architecture]]
- Calculations: [[04-knowledge/reference/smart-volume-radar-calculations]]
- Message guide: [[04-knowledge/reference/smart-volume-radar-message-guide]]
- Indicator sources: [[04-knowledge/reference/smart-volume-radar-indicator-sources]]
- Remaining tasks: [[docs/plans/2026-02-27-smart-volume-radar-remaining-tasks]]
