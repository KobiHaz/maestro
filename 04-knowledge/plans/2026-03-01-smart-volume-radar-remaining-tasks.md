# Smart Volume Radar — משימות פתוחות

> **מקור יחיד.** כל המשימות הפתוחות לפרויקט ממוקמות כאן.  
> **תאריך עדכון:** 2 מרץ 2026  
> **מקורות:** דוח ביקורת 2026-03-01, code-quality-hardening

---

## הושלם

- **מרץ 2026:** Code quality refactor — O(1) sector lookup (Map), cache getters (getIsraeliNames lazy init), split formatDailyReport/sendDailyReport ל־פונקציות קטנות
- npm audit fix, הסרת yahoo-finance2/rss-parser
- validateTicker, validateGoogleSheetId, encodeURIComponent
- escapeHtml, .env.example, CI workflow
- send-legend→logger, israeliNames cache+copy ל-dist
- concurrency + timeout ב-daily-scan
- **מרץ 2026:** התראת כישלון ב-Telegram, Twelve Data throttling, ניקוי קוד מת, בדיקות technicalAnalysis/errorHandler/marketData, coverage threshold 55%
- **מרץ 2026:** env ל-config (twelveDataApiKey, forceScan, debug), טייפים ל-API responses (marketData, newsService), לינט נקי (0 warnings)
- **מרץ 2026:** LLM fix — LLM_MODEL, gemini-2.0-flash default, escapeHtml ל-output, LLM_SIGNALS_ONLY, NaN guards, npm audit ב-CI, daily-scan env (GEMINI, TWELVE_DATA)

---

## פתוח (נדחה)

| # | משימה | הערות |
|---|--------|-------|
| 1 | העלאת coverage ל-70% | newsService tests נתקלו ב-ESM/__dirname עם Jest; כיסוי נוכחי ~59%

---

## משימות ידניות (Manual Tasks)

פעולות ידניות שהמשתמש צריך לבצע.

### הגדרת LLM (מקומי)

- [ ] העתק `.env.example` ל-`.env`
- [ ] הוסף `GEMINI_API_KEY` (או `OPENAI_API_KEY` / `PERPLEXITY_API_KEY`)
- [ ] הרץ מקומית עם `ENABLE_LLM_SUMMARY=true` ובדוק שניתוח LLM מופיע ב-Telegram

### הגדרת daily-scan (GitHub Actions)

- [ ] הוסף `GEMINI_API_KEY` כ-Secret ב-GitHub (Settings → Secrets and variables → Actions)
- [ ] (אופציונלי) הוסף `TWELVE_DATA_API_KEY` ל-Secrets — ל-RSI/SMA מ-Twelve Data

### אימות לאחר השינויים

- [ ] הרץ `npm run start` מקומית — וודא דוח נשלח ל-Telegram עם ניתוח LLM
- [ ] (אופציונלי) בדוק `LLM_SIGNALS_ONLY=true` — וודא שרק topSignals נשלחים ל-LLM

---

## קישורים

- **פרויקט:** `~/.gemini/antigravity/projects/smart-volume-radar`
- **דוח ביקורת:** [[../06-outputs/2026-03-01-smart-volume-radar-audit-report]]
- **Standards:** [[04-knowledge/standards/smart-volume-radar-standards]]
- **Architecture:** [[04-knowledge/reference/smart-volume-radar-architecture]]
