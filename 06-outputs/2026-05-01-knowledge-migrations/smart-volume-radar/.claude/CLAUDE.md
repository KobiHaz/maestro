# smart-volume-radar — Project Context

Automated stock volume monitoring with RVOL analysis, news enrichment, and Telegram delivery.

**Stack:** Node.js ≥20, TypeScript 5.9, ESM, tsx
**APIs:** Yahoo Finance (yahoo-finance2), Finnhub, Twelve Data (fallback), Telegram Bot
**Testing:** Jest + ts-jest
**CI/CD:** GitHub Actions (daily scan + weekly evaluate)

---

## Quick Start

```sh
npm install
npm run start        # run daily scan
npm run evaluate-setups  # weekly performance evaluation
npm run test         # Jest test suite
```

---

## Folder Map

```
src/
  index.ts          → Main entry, orchestration pipeline
  config/           → Env vars, watchlist (Google Sheet), validateConfig, sector map
  services/
    marketData.ts   → Yahoo Finance (primary) + Twelve Data (fallback); p-limit concurrency
    rvolCalculator.ts → RVOL filter + sort
    newsService.ts  → Finnhub + Israeli names; p-limit
    telegramBot.ts  → Format + send report
    llmSummary.ts   → Optional AI summary (OpenAI/Perplexity/Gemini)
  types/            → Shared interfaces (StockData, NewsItem, RVOLResult…)
  utils/
    technicalAnalysis.ts → calculateSMA, calculateRSI, isNearSMA
    setup.ts        → isFullSetup, isCloseSetup (single source of truth)
    formatters.ts   → formatRVOL, formatPriceChange
    logger.ts       → Structured logging (no console.log)
    errorHandler.ts → formatErrorForTelegram
    escapeHtml.ts   → Safe Telegram HTML
    writeScanResults.ts → Persist results/scan-YYYY-MM-DD.json
scripts/
  evaluate-setups.ts → Download CI artifacts, fetch prices, report setup performance
results/              → scan-YYYY-MM-DD.json (gitignored)
tests/
```

---

## Data Pipeline

```
1. fetchAndCacheWatchlist()  → Google Sheet CSV → ticker list + sector map
2. fetchAllStocks()          → Yahoo chart API (primary) or Twelve Data (fallback)
3. calculateRVOL()           → Filter MIN_RVOL, sort by RVOL, take TOP_N
4. enrichWithNews()          → Finnhub headlines per stock
5. sendDailyReport()         → Format + Telegram
6. writeScanResults()        → Save StoredScanResult to results/scan-YYYY-MM-DD.json
```

---

## Setup Signals

**Full Setup 🎯:**
```
RVOL ≥ MIN_RVOL  AND  nearSMA21  AND  nearAth  AND  inConsolidationWindow
```

**Close Setup 👀:**
```
RVOL ≥ MIN_RVOL  AND  (nearSMA21 OR nearSMA21Close)  AND  (nearAth OR nearAthClose)  AND  (inConsolidationWindow OR inConsolidationClose)
```

Source: `src/utils/setup.ts` — `isFullSetup`, `isCloseSetup`

---

## Required Config (env vars)

| Var | Required | Default |
|-----|----------|---------|
| `GOOGLE_SHEET_ID` | ✓ | — |
| `FINNHUB_API_KEY` | ✓ | — |
| `TELEGRAM_BOT_TOKEN` | ✓ | — |
| `TELEGRAM_CHAT_ID` | ✓ | — |
| `MIN_RVOL` | | 2.0 |
| `TOP_N` | | 15 |
| `ENABLE_LLM_SUMMARY` | | true |
| `LLM_MIN_RVOL` | | 2 |
| `LLM_PER_STOCK` | | true |
| `LLM_SIGNALS_ONLY` | | false |

Full config: `src/config/index.ts`

---

## CI/CD

- **Daily scan:** GitHub Actions, runs on schedule → uploads `scan-YYYY-MM-DD` artifact (90d retention)
- **Weekly evaluate:** Sunday 10:00 UTC → downloads last 7 artifacts, reports % change for 🎯 signals
- **On push:** lint + build + test

---

## Core Rules

1. **No `console.log`** — use `logger` only
2. **Concurrency via `p-limit`** — 3–5 tickers, 2 news calls (no sequential sleep)
3. **Normalize at API boundary** — Yahoo/Finnhub responses → typed interfaces in the same service
4. **Return `null`/`[]` on failure** — log with logger.warn/error; never swallow silently
5. **Top-level catch in `main()`** — format, log, Telegram notify, `process.exit(1)`
6. **Config validation** — `validateConfig()` runs at startup; throws on missing required vars
7. **`setup.ts` is the single source of truth** — never inline setup criteria elsewhere

---

## Reference

- [Architecture & data flow](.claude/knowledge/architecture.md)
- [Calculations (exact formulas)](.claude/knowledge/calculations.md)
- [Coding patterns & conventions](.claude/knowledge/standards.md)
