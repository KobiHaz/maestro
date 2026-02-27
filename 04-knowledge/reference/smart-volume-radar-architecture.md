# Smart Volume Radar — Architecture Reference

> Updated: February 2026

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
│   └── utils/                # technicalAnalysis, logger, errorHandler
└── tests/
```

## Key Decisions (from PLAN-hardening)

1. **Concurrency:** `p-limit` instead of sequential sleep — 3–5 tickers, 2 news calls.
2. **Config:** Google Sheet watchlist + `src/config/`; no tickers.json merge.
3. **Logging:** `logger` only; no `console.log`.

## Data Flow

1. `fetchAndCacheWatchlist()` — load symbols from Google Sheet
2. `fetchAllStocks()` — Yahoo chart (primary) or Twelve Data (fallback)
3. `calculateRVOL()` — filter by MIN_RVOL, sort, TOP_N
4. `enrichWithNews()` — Finnhub headlines
5. `sendDailyReport()` — format + Telegram

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

Full config: `src/config/index.ts`.

## Links (vault)

- Project: `~/.gemini/antigravity/projects/smart-volume-radar`
- Calculations: [[04-knowledge/reference/smart-volume-radar-calculations]]
- Message guide: [[04-knowledge/reference/smart-volume-radar-message-guide]]
- Indicator sources: [[04-knowledge/reference/smart-volume-radar-indicator-sources]]
