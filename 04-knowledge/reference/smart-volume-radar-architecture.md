# Smart Volume Radar — Architecture Reference

> Updated: March 2026

## Overview

Node.js CLI for daily stock volume monitoring. Identifies unusual trading (RVOL), enriches with news, sends formatted reports via Telegram.

## Tech Stack

- **Runtime:** Node.js ≥20, TypeScript 5.9, ESM
- **APIs:** Yahoo Finance (chart), Finnhub (news), Twelve Data (RSI/SMA fallback), Telegram
- **Config:** Env vars + Google Sheet watchlist
- **CI:** GitHub Actions

## Project Structure

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
│   └── utils/                # technicalAnalysis, logger, errorHandler, escapeHtml, writeScanResults
├── scripts/
│   └── evaluate-setups.ts    # Weekly: download artifacts, fetch prices, report setup performance
├── results/                  # scan-YYYY-MM-DD.json (gitignored)
└── tests/
```

## Key Decisions (from PLAN-hardening + audit)

1. **Concurrency:** `p-limit` instead of sequential sleep — 3–5 tickers, 2 news calls.
2. **Config:** Google Sheet watchlist + `src/config/`; no tickers.json merge.
3. **Logging:** `logger` only; no `console.log`.
4. **Security:** `validateTicker`/`validateGoogleSheetId`; `encodeURIComponent` in URLs; `escapeHtml` for Telegram HTML.
5. **Build:** `israeliNames.json` copied to `dist/config/`; newsService caches it in memory.

## Data Flow

1. `fetchAndCacheWatchlist()` — load symbols from Google Sheet
2. `fetchAllStocks()` — Yahoo chart (primary) or Twelve Data (fallback)
3. `calculateRVOL()` — filter by MIN_RVOL, sort, TOP_N
4. `enrichWithNews()` — Finnhub headlines
5. `sendDailyReport()` — format + Telegram
6. `writeScanResults()` — save `StoredScanResult` to `results/scan-YYYY-MM-DD.json` (setupType per stock)

## Signal Results & Weekly Evaluation (March 2026)

- **Storage:** Daily scan writes `results/scan-YYYY-MM-DD.json`; CI uploads as artifact `scan-YYYY-MM-DD` (90 days retention).
- **Evaluate:** `npm run evaluate-setups` — downloads last 7 days via `gh run download`, fetches current prices, computes % change for full setup (🎯) signals.
- **Weekly workflow:** Runs Sunday 10:00 UTC; sends performance summary to Telegram.

## Config (critical)

| Var | Required | Default |
|-----|----------|---------|
| GOOGLE_SHEET_ID | ✓ | — |
| FINNHUB_API_KEY | ✓ | — |
| TELEGRAM_BOT_TOKEN | ✓ | — |
| TELEGRAM_CHAT_ID | ✓ | — |
| MIN_RVOL | | 2.0 |
| TOP_N | | 15 |
| USE_FETCHED_INDICATORS | | true |
| ENABLE_LLM_SUMMARY | | true |
| LLM_MIN_RVOL | | 2 |
| LLM_PER_STOCK | | true |
| LLM_MODEL | | (empty = provider default: gpt-4o-mini / sonar / gemini-2.0-flash) |
| LLM_SIGNALS_ONLY | | false |

Full config: `src/config/index.ts`.

## Links (vault)

- Project: `~/.gemini/antigravity/projects/smart-volume-radar`
- Coding patterns: [[04-knowledge/reference/smart-volume-radar-coding-patterns]]
- Calculations: [[04-knowledge/reference/smart-volume-radar-calculations]]
- Message guide: [[04-knowledge/reference/smart-volume-radar-message-guide]]
- Indicator sources: [[04-knowledge/reference/smart-volume-radar-indicator-sources]]
