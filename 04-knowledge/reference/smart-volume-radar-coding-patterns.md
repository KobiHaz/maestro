# Smart Volume Radar — Extracted Coding Patterns

> **Goal:** Document existing patterns only. No improvement suggestions.  
> **Updated:** 2026-03-02 (post refactor: O(1) sector Map, getIsraeliNames getter, split formatDailyReport/sendDailyReport)
>
> **Relationship:** Extends [[04-knowledge/standards/base-coding-standards|base-coding-standards]]. Base = universal rules; this = project-specific observations. No conflicts; Node CLI exempts base §7, §11, §14 (React, state, folder structure).

---

## 1. Naming Conventions

### Data fetching verb prefix

- **Observed pattern:** Mix of `fetch` and `load` and `get`.
  - `fetch` for remote/network: `fetchAllStocks`, `fetchWatchlistCsv`, `fetchAndCacheWatchlist`, `fetchNewsForStock`, `fetchHebrewNews`, `fetchFromYahooChart`, `fetchFromTwelveData`, `fetchIndicatorsFromTwelveData`
  - `load` for in-memory/cache: `loadWatchlist`; `get` for cached data: `getIsraeliNames`
  - `get` for synchronous access/computation: `getSectorForTicker`, `getTickers`, `getCodeSetup`, `getReportSummary`, `getPerStockAnalyses`, `getStocksForLlm`, `getAllSignalRows`, `getSetupRowsFromData`
- **Consistency score:** Mostly consistent (`fetch` = network, `load` = from cache/file, `get` = sync access)
- **Example:** `src/services/marketData.ts:266` — `fetchAllStocks`; `src/config/index.ts:203` — `loadWatchlist`

### Booleans

- **Observed pattern:** `is` / `has` / `can` / `use` / `enable`.
  - `is`: `isOpen`, `isHeaderRow`, `isFull`, `isClose`, `isVolumeWithoutPrice`, `isIsraeli`, `isFullSetup`, `isCloseSetup`, `isBullish`, `isNearSMA`, `isFullConsolidationSetup`, `isCloseConsolidationSetup`
  - `has`: `hasKey`, `hasSetup`
  - config flags: `useFetchedIndicators`, `enableLlmSummary`, `llmPerStock`, `llmSignalsOnly`, `forceScan`, `debug`
- **Consistency score:** Consistent
- **Example:** `src/types/index.ts:89` — `isOpen`; `src/config/index.ts:41` — `useFetchedIndicators`

### Constants

- **Observed pattern:** `SCREAMING_SNAKE_CASE` or `camelCase`.
  - Module-level: `TICKER_REGEX`, `GOOGLE_SHEET_ID_REGEX`, `GOOGLE_SHEETS_CSV_URL`, `TELEGRAM_MAX_LENGTH`, `OPENAI_API_URL`, `MAX_LLM_TOKENS`, `TWELVE_DATA_BASE`, `VOLUME_RVOL_LOOKBACK`, `TRADING_DAYS_PER_MONTH`, `TRADING_DAYS_52W`
  - Config keys: `camelCase` (e.g. `minRVOL`, `topN`)
- **Consistency score:** Consistent — SCREAMING_SNAKE for true constants; camelCase for config
- **Example:** `src/config/index.ts:78` — `TICKER_REGEX`; `src/services/llmSummary.ts:68` — `MAX_LLM_TOKENS`

### Components / hooks / utilities

- **Observed pattern:** No React components. Project is Node.js CLI/backend.
  - **Services:** `*Service` implied by folder; functions like `fetchAllStocks`, `enrichWithNews`
  - **Utils:** pure functions, often with verb prefixes (`calculate`, `format`, `validate`, `parse`, `escape`)
  - **Config:** `config` object export; `validateConfig`, `loadWatchlist`, `getSectorForTicker`
- **Consistency score:** Consistent
- **Example:** `src/utils/technicalAnalysis.ts` — `calculateSMA`, `calculateRSI`, `isNearSMA`; `src/utils/escapeHtml.ts` — `escapeHtml`

---

## 2. Data Patterns

### Data normalization

- **Observed pattern:** Normalization at API boundary.
  - Yahoo/Finnhub/Twelve Data responses → `StockData`, `NewsItem` in the same module that fetches
  - News: `FinnhubNewsResponse[]` → `NewsItem[]` with `publishedAt: new Date(item.datetime * 1000)`
  - RSS: raw object → `{ headline, url, source, publishedAt }`
  - Arrays normalized with `Array.isArray(items) ? items : [items]` when API may return single item
- **Consistency score:** Consistent
- **Example:** `src/services/newsService.ts:74-78` — Finnhub → NewsItem; `src/services/newsService.ts:106` — `Array.isArray(items) ? items : [items]`

### Data transformation location

- **Observed pattern:** In the service that fetches, or in a dedicated util.
  - Market data: `marketData.ts` maps API response → `StockData`
  - Technical: `technicalAnalysis.ts` does SMA, RSI, ATH from raw arrays
  - Display formatting: `telegramBot.ts` (`formatDailyReport`, `formatSetupIndicator`, `formatSingleStockBlock`)
  - **Setup criteria:** `setup.ts` — `isFullSetup`, `isCloseSetup` (RVOL ≥ minRVOL + SMA21 + ATH + base; single source of truth)
  - **Display formatters:** `formatters.ts` — `formatRVOL`, `formatPriceChange` (config-aware)
- **Consistency score:** Consistent — transform at fetch boundary, format at output
- **Example:** `src/services/marketData.ts:131-154` — raw chart data → StockData; `src/utils/technicalAnalysis.ts:9-14` — calculateSMA

### Async data handling

- **Observed pattern:** No explicit loading/error/success state objects. Async handled by:
  - Return `null` or `[]` on failure / empty
  - `try/catch` with `logger.warn`/`logger.error`, then fallback
  - `Promise.all` for parallelism; `pLimit` for concurrency
  - Caller checks emptiness (`if (stocks.length === 0) return`)
- **Consistency score:** Consistent for this CLI style
- **Example:** `src/services/marketData.ts:17` — returns `null` on failure; `src/services/newsService.ts:80-82` — catch returns `[]`

---

## 3. Complexity Patterns

### Lookup complexity

- **Observed pattern:** O(1) for sector lookup via Map; O(n) for volumeWithoutPrice.some; Set for dedup.
  - `getSectorForTicker`: `sectorMap.get(symbol.toUpperCase()) ?? 'Other'` — O(1) (Map built once after ticker load)
  - `volumeWithoutPrice.some((v) => v.ticker === s.ticker)` — O(n)
  - `seen.has(s.ticker)` in `getSetupRowsFromData` via `Set` — O(1)
- **Consistency score:** Consistent — Map for keyed lookups, Set for dedup
- **Example:** `src/config/index.ts` — sectorMap; `src/services/telegramBot.ts:375` — `new Set<string>()`

### Arrays vs objects/maps

- **Observed pattern:**
  - **Arrays** for ordered collections: tickers, stocks, signals, news
  - **Objects (`Record`)** for keyed lookups and grouping: `Record<string, RVOLResult[]>` (sectors), `Record<string, string>` (israeliNames)
  - **Map** for O(1) sector lookup: `Map<string, string>`
- **Consistency score:** Consistent — arrays for sequences, objects/Map for keyed data
- **Example:** `src/services/telegramBot.ts:185` — `const sectors: Record<string, RVOLResult[]> = {}`; `src/config/index.ts` — `sectorMap`

---

## 4. Component / Function Patterns

### Average function length

- **Observed pattern:** Broad range.
  - Short: `sleep`, `escapeHtml`, `truncate`, `isBullish`, `formatRVOL` (1–5 lines)
  - Medium: `calculateSMA`, `validateTicker`, `formatDate` (~5–15 lines)
  - Long: `fetchFromYahooChart`, `formatSingleStockBlock` (30–50 lines); `buildLlmSummaryMessage`, `sendDailyReport` orchestration
- **Consistency score:** Mostly consistent — `formatDailyReport` and `sendDailyReport` split into smaller functions
- **Example:** `src/utils/errorHandler.ts:9-11` — short; `src/services/telegramBot.ts` — formatSingleStockBlock, buildLlmSummaryMessage

### Props / parameters

- **Observed pattern:** Individual params preferred; config objects when many related options.
  - Individual: `formatSetupIndicator(stock, athThreshold, athCloseThreshold, smaTouch, ...)`
  - Object: `calculateRVOL(stocks, rvolConfig)` with `RVOLConfig`; `sendDailyReport(date, topSignals, volumeWithoutPrice, failedTickers, scope?)`
  - Config passed as object from `config` singleton
- **Consistency score:** Mostly consistent — object when 4+ related params
- **Example:** `src/services/rvolCalculator.ts:37` — `calculateRVOL(stocks, rvolConfig)`; `src/index.ts:115-119` — config object

### Side effects

- **Observed pattern:** Explicit.
  - I/O: `fetch`, `fs.readFileSync`, `sendTelegramMessage` — in service functions
  - Mutations: module-level cache (`tickerCache`, `sectorMap` via `fetchAndCacheWatchlist`; `_israeliNamesCache` via `getIsraeliNames` getter with lazy init)
  - Logging: `logger.info`, `logger.warn`, `logger.error` throughout
- **Consistency score:** Consistent — side effects in services; caches wrapped in getters
- **Example:** `src/config/index.ts:187` — `tickerCache = parseWatchlistCsv(csv)`; `src/services/newsService.ts` — `getIsraeliNames()` lazy init

---

## 5. Error Handling

### Error catching and surfacing

- **Observed pattern:**
  - `try/catch` in async fetchers; return `null` or `[]` on failure
  - `throw` for invalid config or critical failures
  - Top-level in `main()`: catch, `formatErrorForTelegram`, log, send Telegram, `process.exit(1)`
  - API errors: log and return empty/null; no rethrow unless caller needs to handle
- **Consistency score:** Consistent
- **Example:** `src/index.ts:146-158` — top-level catch; `src/services/marketData.ts:153-156` — catch, log, return null

### Error format

- **Observed pattern:** Plain `Error` with message string.
  - `formatErrorForTelegram`: `error.name + ': ' + error.message` for `Error`, else `String(error)`
  - Thrown messages: descriptive, often include hints (e.g. "Check GOOGLE_SHEET_ID...")
- **Consistency score:** Consistent
- **Example:** `src/utils/errorHandler.ts:16-21`; `src/config/index.ts:119-120`

---

## 6. State Management

### Where state lives

- **Observed pattern:** Module-level singletons and function parameters.
  - **Module cache:** `tickerCache`, `sectorMap` (config); `_israeliNamesCache` (newsService, via getter)
  - **Config:** `config` object from `config/index.ts`
  - **No global store** — data flows top-down via `main()` → services
- **Consistency score:** Consistent for CLI
- **Example:** `src/config/index.ts:108` — `let tickerCache`; `src/services/newsService.ts` — `getIsraeliNames()` getter

### Shared state

- **Observed pattern:** Passed as arguments. No shared mutable state across services except config.
  - `main()` fetches → passes to `calculateRVOL` → passes to `enrichWithNews` → passes to `sendDailyReport`
  - `config` imported where needed
- **Consistency score:** Consistent
- **Example:** `src/index.ts:105-138` — pipeline of function calls with data passing

---

## 7. File & Folder Structure

- **Observed pattern:** By type, flat within types.
  ```
  src/
    index.ts          # entry, orchestration
    config/           # config + watchlist
    services/          # marketData, news, llm, telegram, rvol
    utils/             # errorHandler, escapeHtml, logger, technicalAnalysis
    types/             # index.ts with interfaces
  scripts/             # one-off scripts
  tests/               # co-located with src by name
  docs/                # CODING_PATTERNS, REPOSITORY_ANALYSIS (→ Maestro 04-knowledge / 06-outputs)
  ```
- **Consistency score:** Consistent — config, services, utils, types
- **Example:** `src/services/`, `src/utils/`, `src/config/`

---

## 8. Concise Ruleset for Coding Standards

Use these as the baseline for new code:

### Naming

1. **Data fetching:** `fetch` for network, `load` for cache/file, `get` for sync access.
2. **Booleans:** `is` / `has` / `can` / `use` / `enable` prefixes.
3. **Constants:** `SCREAMING_SNAKE_CASE` for true constants; `camelCase` for config.
4. **Utils:** Verb prefixes: `calculate`, `format`, `validate`, `parse`, `escape`, `build`.

### Data

5. **Normalize** at API boundary in the service that fetches.
6. **Arrays:** Use when API may return single item: `Array.isArray(x) ? x : [x]`.
7. **Async:** Return `null` or `[]` on failure; log; no loading-state objects.

### Structure

8. **Lookups:** Prefer `Map` for O(1) keyed lookups, `Set` for dedup, `Record` for keyed groups; arrays for ordered data.
9. **Params:** Object when 4+ related params; otherwise individual args.
10. **Side effects:** In services only; keep utils pure.
11. **Caches:** Wrap in getter with lazy init; avoid direct module mutation exposure.

### Error handling

12. **Catch** in async fetchers; return `null`/`[]` or rethrow for critical failures.
13. **Format** for user-facing: `error.name + ': ' + error.message` (or `String(error)`).
14. **Top-level** in `main()`: catch, format, log, notify, `process.exit(1)`.

### State

15. **State:** Module-level cache where needed; pass data as arguments.
16. **Config:** Single `config` object; validate with `validateConfig()`.

### Files

17. **Layout:** `config/`, `services/`, `utils/`, `types/`; tests mirror `src` structure.
