# Smart Volume Radar — דוח ביקורת מקיף

> **תאריך:** 1 מרץ 2026  
> **מקור:** הפעלת כל סוכני Maestro הרלוונטיים לפרויקט  
> **פרויקט:** smart-volume-radar — Node.js CLI לניטור נפחי מסחר ו-Telegram

---

## תמצית מנהלים

מערכת מוכנה לייצור עם ארכיטקטורה ברורה ומתועדת. נמצאו שיפורים קריטיים באבטחה (תלויות פגיעות, ולידציית קלט), בבדיקות (כיסוי 48%), וב-CI/CD. רוב המלצות הבינוניות והנמוכות ניתנות ליישום במהירות יחסית.

| היבט | ציון | מצב |
|------|------|-----|
| ארכיטקטורה | טוב | Data flow ברור, p-limit, config מרכזי |
| אבטחה | דורש תשומת לב | 3 פגיעויות, הזרקת URL, XSS ב-Telegram |
| בדיקות | בינוני | 48% כיסוי, 5 מודולים ללא בדיקות |
| ביצועים | טוב | Twelve Data burst, israeliNames קורא שוב ושוב |
| DevOps | דורש שיפור | אין CI על PR, אין build, אין timeout |
| דוקומנטציה | טוב | README, reference בכספת, תיעוד עדכני |

---

## 1. ארכיטקטורה ומבנה (Explorer Agent)

### 1.1 מבנה הקוד

```
smart-volume-radar/
├── src/
│   ├── index.ts              # אורקסטרציה ראשית
│   ├── config/               # Env, Google Sheet watchlist
│   ├── services/             # marketData, rvolCalculator, newsService, telegramBot, llmSummary
│   ├── types/
│   └── utils/                # technicalAnalysis, logger, errorHandler
├── tests/                    # 3 קבצי בדיקה, 32 טסטים
├── scripts/send-legend.ts
└── .github/workflows/daily-scan.yml
```

### 1.2 Data Flow

```
1. fetchAndCacheWatchlist() → Google Sheet CSV
2. fetchAllStocks() → Yahoo Chart / Twelve Data (p-limit 3)
3. calculateRVOL() → סינון, מיון, topN
4. enrichWithNews() → Finnhub / Google News RSS (p-limit 2)
5. sendDailyReport() → LLM (אופציונלי) + Telegram
```

### 1.3 Dependencies — תלויות מתות

| Package | סטטוס |
|---------|-------|
| `yahoo-finance2` | ❌ לא בשימוש — marketData משתמש ב-fetch ישיר |
| `rss-parser` | ❌ לא בשימוש — newsService משתמש ב-fast-xml-parser |

**המלצה:** `npm uninstall yahoo-finance2 rss-parser`

### 1.4 Technical Debt

- **קוד מת:** `withRetry`, `safeJsonParse`, `ScanResults`, config: `batchSize`, `batchDelayMs`, `maxRetries`, `retryDelayMs`
- **חריגה מסטנדרטים:** `scripts/send-legend.ts` משתמש ב-`console.log` במקום `logger`
- **באג פוטנציאלי:** `israeliNames.json` לא מועתק ל-`dist/` — הרצה מ-`node dist/index.js` תכשל ב-Hebrew news

---

## 2. אבטחה (Security Auditor)

### 2.1 Executive Summary

| חומרה | כמות |
|-------|------|
| Critical | 1 |
| High | 3 |
| Medium | 4 |
| Low | 3 |

### 2.2 תלויות פגיעות (npm audit)

| Package | חומרה | Advisory |
|---------|-------|----------|
| **fast-xml-parser** ≤5.3.7 | **Critical** | XXE, entity expansion DoS, regex injection |
| **minimatch** | High | ReDoS |
| **ajv** | Moderate | ReDoS עם $data |

**פעולה:** `npm audit fix` + עדכון ל-fast-xml-parser גרסה מתוקנת

### 2.3 Input Validation

| Location | בעיה |
|----------|------|
| Ticker symbols | הזרקת URL — אין allowlist או encoding |
| `newsService.ts:47` | `symbol=${ticker}` — query injection |
| `marketData.ts:17-18` | `chart/${ticker}` — path traversal אם ticker מכיל `../` |
| Google Sheet ID | אין ולידציה לפורמט |
| Sector / headline / URL | הזרקה ל-Telegram HTML ללא escape → XSS |

**המלצות:**
- Regex ל-ticker: `^[A-Z0-9]{1,5}(\.[A-Z]{2})?$`
- `encodeURIComponent()` לכל ticker ו-sheetId ב-URLs
- פונקציית `escapeHtml()` לפני הכנסה להודעות Telegram

### 2.4 רגישות ב-Logging

- Stack traces מלאים ב-`logger.error()`
- 200 תווים מתגובת API ב-llmSummary
- `JSON.stringify(error)` מלא ב-telegramBot ב-API error

### 2.5 OWASP Mapping

| OWASP | רלוונטי |
|-------|----------|
| A03 Injection | ✓ Ticker, sheet ID, sector, headline |
| A06 Vulnerable Components | ✓ 3 פגיעויות |
| A09 Logging | ✓ דליפת מידע |

---

## 3. בדיקות (Test Engineer)

### 3.1 כיסוי נוכחי

| Metric | ערך |
|--------|-----|
| Statements | 48.26% |
| Branches | 37.73% |
| Functions | 50% |
| Lines | 49.4% |
| Test suites | 3 |
| Tests | 32 |

### 3.2 מודולים ללא כיסוי

| Module | פונקציות |
|--------|-----------|
| `marketData.ts` | fetchAllStocks, Yahoo/12Data fallback |
| `newsService.ts` | enrichWithNews, fetchHebrewNews |
| `llmSummary.ts` | getReportSummary, providers |
| `technicalAnalysis.ts` | calculateSMA, calculateRSI, calculate52wHigh |
| `errorHandler.ts` | withRetry, safeJsonParse, formatErrorForTelegram |

### 3.3 המלצות — לפי עדיפות

**Priority 1:**
1. `tests/technicalAnalysis.test.ts` — פונקציות טהורות
2. `tests/errorHandler.test.ts` — טיפול בשגיאות
3. בדיקות ל-`validateConfig()`
4. בדיקות ל-tie-breaker ב-rvolCalculator

**Priority 2:**
- `marketData.test.ts` עם mock ל-fetch
- `newsService.test.ts` עם mock ל-fetch

**Priority 3:** `llmSummary.test.ts`

**כללי:** Mock ל-logger, coverage thresholds ב-Jest (למשל 70%).

---

## 4. ביצועים (Performance Optimizer)

### 4.1 Concurrency (p-limit)

| Service | Limit |
|---------|-------|
| marketData | 3 |
| newsService | 2 |
| llmSummary | 3 |

### 4.2 Bottlenecks

| Bottleneck | חומרה |
|-----------|--------|
| Twelve Data burst — 6–9 קריאות במקביל | High |
| `israeliNames.json` — קריאה בכל Hebrew stock | Medium |
| News delay בתוך task | Medium |
| batchSize / batchDelayMs לא בשימוש | Low |

### 4.3 המלצות

1. **קריטי:** cache ל-`israeliNames.json` בזיכרון
2. **קריטי:** throttling ל Twelve Data (למשל p-limit(1) או 2)
3. **בינוני:** העברת news delay מחוץ ל-task
4. **בינוני:** שימוש או הסרה של batchSize / batchDelayMs

---

## 5. DevOps (DevOps Engineer)

### 5.1 GitHub Actions — daily-scan.yml

**יתרונות:**
- Cron ברור: 21:30 UTC, Mon–Fri
- `workflow_dispatch` לריצה ידנית
- `npm ci`, cache, secrets

**חסרים:**

| חסר | השפעה |
|-----|--------|
| אין build | TypeScript לא נבדק בקומפילציה |
| אין test | בדיקות לא רצות ב-CI |
| אין PR CI | lint/build/test לא על push/PR |
| אין concurrency | ריצות מקבילות אפשריות |
| אין timeout | ברירת מחדל ~6 שעות |
| אין התראה ב-Telegram | כישלון לא מדווח למשתמש |

### 5.2 המלצות

| עדיפות | פעולה |
|--------|-------|
| High | CI workflow: lint → build → test על push/PR |
| High | הוספת `.env.example` |
| Medium | התראת כישלון ב-Telegram |
| Medium | `concurrency: group: daily-scan` + `timeout-minutes: 30` |

---

## 6. תיעוד (Documentation Writer)

**מצב נוכחי:**
- README מפורט עם Quick Start, Configuration, Sample Output
- Reference בכספת: architecture, calculations, message-guide, indicator-sources
- Standards: smart-volume-radar-standards.md
- `.env.example` חסר (מוזכר ב-README)

---

## 7. סיכום סוכנים שהשתתפו

| Agent | היבט | פלט |
|-------|------|-----|
| **explorer-agent** | מבנה, ארכיטקטורה, technical debt | REPOSITORY_ANALYSIS.md |
| **security-sentinel** | אבטחה, OWASP, תלויות | דוח אבטחה מקיף |
| **test-engineer** | כיסוי, gaps, המלצות | דוח בדיקות |
| **performance-oracle** | concurrency, bottlenecks | דוח ביצועים |
| **devops-engineer** | CI/CD, secrets, failure handling | דוח DevOps |
| **cto** | ארכיטקטורה, החלטות | אופקי (מהפרויקט brief) |
| **documentation-writer** | עקרונות | הערכת תיעוד נוכחי |

---

## 8. Roadmap לפעולה — לפי עדיפות

### קריטי (מיד)

1. `npm audit fix` + עדכון fast-xml-parser
2. הסרת תלויות מתות: yahoo-finance2, rss-parser
3. ולידציית ticker + encodeURIComponent ב-URLs
4. escapeHtml לפני הכנסת sector/headline/URL ל-Telegram

### גבוה (שבוע)

5. CI workflow: lint, build, test על PR
6. `.env.example`
7. החלפת console.log ב-send-legend ל-logger
8. העתקת israeliNames.json ל-dist או תיעוד tsx-only
9. cache ל-israeliNames.json
10. Twelve Data throttling

### בינוני (חודש)

11. בדיקות: technicalAnalysis, errorHandler, marketData
12. התראת כישלון ב-Telegram ב-CI
13. concurrency + timeout ב-daily-scan
14. ניקוי קוד מת (withRetry, safeJsonParse, ScanResults)

### נמוך

15. coverage threshold 70%
16. העברת TWELVE_DATA_API_KEY, FORCE_SCAN, DEBUG ל-config
17. טייפים ל-API responses במקום `as any`

---

## 9. קישורים

- **פרויקט:** `~/.gemini/antigravity/projects/smart-volume-radar`
- **כספת:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Maestro`
- **Reference:** `04-knowledge/reference/smart-volume-radar-*`
- **Standards:** `04-knowledge/standards/smart-volume-radar-standards.md`
- **דוח Explorer:** `smart-volume-radar/docs/REPOSITORY_ANALYSIS.md`
