# Smart Volume Radar — Cursor Rules & Standards

> **Extends:** [[04-knowledge/standards/base-coding-standards|base-coding-standards]]. Load both.
> Repo: smart-volume-radar. Read this when working on the project.

**Node CLI:** Base §7, §11, §14 (React) לא חלים (per base). שאר הסעיפים חלים.

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

*Imports — see base section 3.*

## Naming (תוספות ל-base — Node CLI)

| Type | Pattern | Example |
|------|---------|---------|
| Files | camelCase | `marketData.ts`, `rvolCalculator.ts` |
| Types | PascalCase | `StockData`, `RVOLResult`, `TickerConfig` |

*Plan files — [[04-knowledge/standards/maestro-project-doc-lifecycle#4. תבנית שם תוכנית|maestro §4]].*

## Plan Lifecycle

[[04-knowledge/standards/maestro-project-doc-lifecycle]]

## Review Checklist (Node CLI)

- **Security** — Ticker/sheet ID validated; `encodeURIComponent` in URLs; `escapeHtml` for user/API content in HTML
- **Logging** — No `console.log`, uses `logger` with context
- **Production Readiness** — No debug statements, no TODOs, no hardcoded secrets
- **Architecture** — Follows existing patterns, code in correct directory

*TypeScript, Error Handling — see base sections 3, 10.*

## Reference (vault)

- Architecture: [[04-knowledge/reference/smart-volume-radar-architecture]]
- Coding patterns: [[04-knowledge/reference/smart-volume-radar-coding-patterns]]
- Calculations: [[04-knowledge/reference/smart-volume-radar-calculations]]
- Message guide: [[04-knowledge/reference/smart-volume-radar-message-guide]]
- Indicator sources: [[04-knowledge/reference/smart-volume-radar-indicator-sources]]
- Remaining tasks: [[docs/plans/2026-03-01-smart-volume-radar-remaining-tasks]]
