# smart-volume-radar — Architecture

## Runtime & Module System

Node.js ≥20, TypeScript 5.9, ESM (import/export), tsx for execution.
No React — pure CLI/backend.

## Service Responsibilities

| Service | Responsibility |
|---------|---------------|
| `marketData.ts` | Yahoo Finance chart API (primary); Twelve Data API (fallback); concurrency via p-limit |
| `rvolCalculator.ts` | Filter by MIN_RVOL, sort descending, slice TOP_N |
| `newsService.ts` | Finnhub headlines; Israeli names cache (`israeliNames.json`); deduplicate |
| `telegramBot.ts` | Format daily report (sectors, signals, summary); send via Telegram Bot API |
| `llmSummary.ts` | Optional AI summary — OpenAI (gpt-4o-mini), Perplexity (sonar), or Gemini |

## Config / Watchlist

- `src/config/index.ts` — reads env vars, exports typed `config` object
- `validateConfig()` — throws on missing required vars, called at startup
- `loadWatchlist()` — fetches Google Sheet CSV → ticker + sector data
- `getSectorForTicker()` — O(1) Map lookup built after watchlist load
- `getIsraeliNames()` — lazy-init getter caching `israeliNames.json` in memory

## Key Types

```ts
StockData      // Raw market data per ticker (price, volume, indicators)
RVOLResult     // StockData + rvol, priceChange, setup flags
NewsItem       // { headline, url, source, publishedAt }
StoredScanResult // Persisted per-scan result for evaluate-setups
```

## Concurrency

```ts
import pLimit from 'p-limit';
const marketLimit = pLimit(3);  // 3–5 tickers in parallel
const newsLimit = pLimit(2);    // 2 news requests in parallel
```

Never use `sleep()` for rate limiting — use p-limit.

## Error Handling Pattern

```ts
// In services: return null/[] on failure
async function fetchStock(ticker: string): Promise<StockData | null> {
  try {
    // ...
  } catch (err) {
    logger.warn('fetchStock failed', { ticker, err });
    return null;
  }
}

// In main(): catch, notify, exit
try {
  await main();
} catch (err) {
  logger.error('Fatal error', err);
  await sendTelegramMessage(formatErrorForTelegram(err));
  process.exit(1);
}
```

## Signal Storage & Weekly Evaluation

- Daily scan writes `results/scan-YYYY-MM-DD.json` (gitignored locally)
- CI uploads as artifact `scan-YYYY-MM-DD` with 90-day retention
- `npm run evaluate-setups` → `scripts/evaluate-setups.ts`:
  1. `gh run download` — last 7 days of artifacts
  2. Fetch current prices via Yahoo
  3. Compute % change for 🎯 (Full Setup) signals
  4. Send performance summary to Telegram

## Twelve Data Fallback

When Yahoo Finance fails for a ticker, Twelve Data provides:
- volume, avgVolume → RVOL
- priceChange, lastPrice, RSI, SMA21
- ath (52w high via `fifty_two_week.high`)
- Note: `monthsInConsolidation` not available from Twelve Data
