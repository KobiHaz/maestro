# Smart Volume Radar — Repository Analysis

> Generated: 2026-03-01. Systematic analysis of codebase structure, patterns, dependencies, and technical debt.  
> **Note:** Some items resolved in later refactors (e.g. dead code removed, israeliNames copied to dist, send-legend→logger). See CHANGELOG.

---

## 1. Structure Map

### Directory Layout

```
smart-volume-radar/
├── src/
│   ├── index.ts                 # Main entry, orchestration
│   ├── config/
│   │   ├── index.ts             # Config loader, watchlist (Google Sheets), validateConfig
│   │   └── israeliNames.json    # Ticker → Hebrew name mapping for TASE stocks
│   ├── services/
│   │   ├── marketData.ts        # Yahoo Chart API + Twelve Data fallback
│   │   ├── rvolCalculator.ts    # RVOL filter, sort, consolidation setup
│   │   ├── newsService.ts       # Finnhub + Google News RSS (TASE)
│   │   ├── telegramBot.ts       # Format and send via Telegram
│   │   └── llmSummary.ts        # Optional LLM commentary (OpenAI/Perplexity/Gemini)
│   ├── types/
│   │   └── index.ts             # StockData, RVOLResult, NewsItem, etc.
│   └── utils/
│       ├── logger.ts            # Timestamped logging (uses console internally)
│       ├── errorHandler.ts     # sleep, formatErrorForTelegram
│       ├── escapeHtml.ts        # XSS prevention for Telegram HTML
│       └── technicalAnalysis.ts # SMA, RSI, 52w high, consolidation
├── tests/
│   ├── rvolCalculator.test.ts
│   ├── telegramFormatter.test.ts
│   ├── watchlist.test.ts
│   ├── marketData.test.ts
│   ├── technicalAnalysis.test.ts
│   └── errorHandler.test.ts
├── scripts/
│   └── send-legend.ts           # One-time: send legend to Telegram
└── .github/workflows/
    ├── ci.yml
    └── daily-scan.yml           # Scheduled Mon–Fri 21:30 UTC
```

### Entry Points

| Entry | Purpose | Invocation |
|-------|---------|------------|
| `src/index.ts` | Main CLI orchestration | `npm run start` (tsx) or `node dist/index.js` |
| `scripts/send-legend.ts` | Send legend to Telegram | `npx tsx scripts/send-legend.ts` |

---

## 2. Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 1. fetchAndCacheWatchlist()                                                     │
│    Google Sheet CSV → parseWatchlistCsv → tickerCache + sectorMap                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        ↓
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 2. fetchAllStocks(tickers)                                                       │
│    pLimit(3) → Yahoo Chart API (primary) → Twelve Data (fallback) per ticker     │
│    → StockData[] (volume, RVOL, RSI, SMA, 52w high, consolidation)               │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        ↓
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 3. calculateRVOL(stocks, config)                                                 │
│    Filter RVOL ≥ minRVOL → sort by RVOL + consolidation boost → topN            │
│    → topSignals, volumeWithoutPrice                                              │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        ↓
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 4. enrichWithNews(topSignals)                                                    │
│    pLimit(2) → Finnhub (US) / Google News RSS (TASE .TA)                         │
│    → RVOLResult[] with news[]                                                    │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        ↓
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 5. sendDailyReport()                                                             │
│    buildLlmSummaryMessage() → optional LLM first message                          │
│    formatDailyReport() → chunkMessage() → sendTelegramMessage() per chunk         │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Key decisions:**

- Yahoo Chart API is primary; Twelve Data used when Yahoo returns no data or for RSI/SMA when key set.
- Watchlist is fetched once per run; sectorMap built for O(1) sector lookup.
- LLM summary is optional; sent as first message when enabled and API key present.

---

## 3. Architectural Patterns and Design Choices

### Service Layer

- **Services** are stateless modules; config is centralized in `config/index.ts`.
- No dependency injection; services import config directly.
- Async operations use `p-limit` for concurrency (3 market fetches, 2 news fetches, 3 LLM calls).

### Config & Env

- Configuration via `process.env`; `config` object centralizes all vars.
- `validateConfig()` throws on missing required vars (Finnhub, Telegram, Google Sheet).
- Optional: Twelve Data, LLM providers (OpenAI, Perplexity, Gemini).

### Data Contracts

- `StockData` and `RVOLResult` drive the pipeline.
- Types well-defined; API responses use typed interfaces where practical.

### Error Handling

- `formatErrorForTelegram()` for user-facing error messages.
- Fatal errors attempt Telegram notification before `process.exit(1)`.
- Individual ticker/news failures are logged and skipped; scan continues.

---

## 4. Dependency Tree and Coupling

### package.json Dependencies

| Package | Used | Purpose |
|---------|------|---------|
| `dotenv` | ✓ | Load .env |
| `fast-xml-parser` | ✓ | Parse Google News RSS XML |
| `p-limit` | ✓ | Concurrency control (marketData, newsService, llmSummary) |

### External APIs

| API | Role | Coupling |
|-----|------|----------|
| Yahoo Chart | Primary market data (5y chart, volume, close) | Direct HTTP; no SDK |
| Twelve Data | Fallback quote + RSI/SMA when API key set | Direct HTTP |
| Finnhub | Company news for US stocks | Direct HTTP |
| Google News RSS | Hebrew news for TASE (.TA) tickers | Direct HTTP + fast-xml-parser |
| Telegram Bot API | Send report | Direct HTTP |

---

## 5. Technical Debt (as of 2026-03-01)

### Resolved

- ~~yahoo-finance2, rss-parser~~ — removed
- ~~withRetry, safeJsonParse~~ — removed from errorHandler
- ~~ScanResults~~ — removed
- ~~israeliNames.json copy to dist~~ — build step added
- ~~send-legend console.log~~ — uses logger

### Remaining

| Item | Severity |
|------|----------|
| Coverage ~59% (target 70%) | Low |
| newsService tests (ESM/__dirname with Jest) | Low |

---

## 6. Consistency with Best Practices (Node CLI)

### Aligned

| Practice | Status |
|---------|--------|
| ESM modules | ✓ `"type": "module"` |
| TypeScript strict | ✓ |
| Centralized config | ✓ |
| Structured logging | ✓ |
| Env for secrets | ✓ |
| Concurrency control | ✓ p-limit |
| Error handling | ✓ try/catch, formatErrorForTelegram |
| Tests | ✓ Jest, multiple suites |
| CI | ✓ GitHub Actions |

---

## Links

- [[04-knowledge/reference/smart-volume-radar-architecture|Architecture]]
- [[04-knowledge/reference/smart-volume-radar-coding-patterns|Coding Patterns]]
- [[04-knowledge/standards/smart-volume-radar-standards|Standards]]
