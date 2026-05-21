# smart-volume-radar — Coding Standards

Node.js CLI project. No React. Extends base-coding-standards (Maestro vault).
Exemptions from base: §7 (React), §11 (state management), §14 (folder structure).

## Naming

| Pattern | Prefix | Examples |
|---------|--------|---------|
| Network calls | `fetch` | `fetchAllStocks`, `fetchAndCacheWatchlist`, `fetchFromYahooChart` |
| In-memory/cache | `load` | `loadWatchlist` |
| Sync access/compute | `get` | `getSectorForTicker`, `getIsraeliNames`, `getReportSummary` |
| Calculations | `calculate` | `calculateSMA`, `calculateRSI`, `calculateRVOL` |
| Formatters | `format` | `formatRVOL`, `formatDailyReport`, `formatSingleStockBlock` |
| Validators | `validate` | `validateTicker`, `validateGoogleSheetId`, `validateConfig` |
| Booleans | `is`/`has`/`can`/`use`/`enable` | `isFullSetup`, `useFetchedIndicators`, `enableLlmSummary` |
| Constants | `SCREAMING_SNAKE_CASE` | `TICKER_REGEX`, `TELEGRAM_MAX_LENGTH`, `VOLUME_RVOL_LOOKBACK` |
| Config keys | `camelCase` | `minRVOL`, `topN`, `llmPerStock` |

## Data Patterns

- **Normalize at API boundary** — Yahoo/Finnhub/Twelve Data → typed interfaces in the fetching service
- **Return `null` or `[]` on failure** — log with logger.warn/error, no swallowing
- **`Array.isArray(x) ? x : [x]`** — when API may return single item instead of array
- **Map for O(1) lookups** — `sectorMap: Map<string, string>` built once after watchlist load
- **Set for dedup** — `new Set<string>()` for seen tickers
- **Record for grouping** — `Record<string, RVOLResult[]>` for sector groupings

## Concurrency

```ts
const limit = pLimit(3);
await Promise.all(tickers.map(t => limit(() => fetchStock(t))));
```

Never use `sleep()` for spacing — use `pLimit`.

## Logging

```ts
import { logger } from '../utils/logger.js';
logger.info('message', { context });   // ✅
logger.warn('degraded', { ticker });   // ✅
logger.error('failed', err);           // ✅
console.log('...');                    // ❌ never
```

## Error Handling

```ts
// Services: return null/[] on failure, log
async function fetchFoo(): Promise<Foo | null> {
  try { ... }
  catch (err) { logger.warn('fetchFoo failed', err); return null; }
}

// main(): catch all, notify Telegram, exit
catch (err) {
  logger.error('Fatal', err);
  await sendTelegramMessage(formatErrorForTelegram(err));
  process.exit(1);
}
```

## Telegram HTML Escaping

Always use `escapeHtml()` from `src/utils/escapeHtml.ts` for user-facing strings in Telegram messages. Never build HTML strings without it.

## Security

- `validateTicker(ticker)` — regex guard before using in URLs
- `validateGoogleSheetId(id)` — guard for Sheet ID
- `encodeURIComponent(ticker)` — in all API URL construction
- Never expose API keys in logs

## What NOT to Do

- ❌ `console.log` — use logger
- ❌ `sleep()` for concurrency control — use p-limit
- ❌ Inline setup criteria — always use `isFullSetup`/`isCloseSetup` from `setup.ts`
- ❌ Skip `validateTicker` before URL construction
- ❌ Skip `escapeHtml` in Telegram message building
- ❌ Commit results/ folder (gitignored)
