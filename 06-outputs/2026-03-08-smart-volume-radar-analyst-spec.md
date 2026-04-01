# Smart Volume Radar — מפרט תנאים חישוביים לאנליסט

**גרסה:** 1.0  
**תאריך:** 2026-03-08  
**מסמך:** מפרט מלא של הנוסחאות והתנאים להכנסת מניות לדוחות היומי והשבועי

---

## 1. סקירה

Smart Volume Radar סורק מניות מ־Watchlist (Google Sheets), מזהה אותות נפח גבוה (RVOL), ומחשיב אינדיקטורים טכניים (SMA21, 52w high, בסיס איחוד). המסמך מגדיר במדויק:

- נוסחאות חישוב לכל אינדיקטור
- תבניות Setup (Full / Close)
- תנאי כניסה לדוח היומי ולדוח השבועי

---

## 2. נתוני מקור

| מקור | פרטי גישה |
|------|-----------|
| **Yahoo Finance Chart** | `query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=5y` |
| מערכים | `volumes[]`, `closes[]` — כרונולוגי, החדש ביותר באחרון |
| Fallback | Twelve Data (שאות, RSI, SMA21, 52w high) |

---

## 3. חישובים בסיסיים

### 3.1 RVOL (Relative Volume)

```
currentVolume  = volumes[last]
lookback       = volumes[last-64 : last-1]   // 63 ימים לפני היום
avgVolume      = sum(lookback) / 63
RVOL           = currentVolume / avgVolume
```

- **63 ימים** — ממוצע נע ~3 חודשים (סטנדרט תעשייתי)
- היום עצמו לא נכלל בממוצע
- יחידות: כפולה (למשל 2.5x = 2.5× נפח ממוצע)

### 3.2 שינוי מחיר (%)

```
priceChange = ((close[last] - close[last-1]) / close[last-1]) × 100
```

- שינוי אחוז יום־לפני־יום

### 3.3 SMA21 (ממוצע נע 21 ימים)

```
SMA21 = (close[-21] + close[-20] + ... + close[-1]) / 21
```

### 3.4 52-Week High (שיא 52 שבועות)

```
lookback   = closes[last 252 days]
PeriodHigh = max(lookback)
```

- **252** ≈ ימי מסחר בשנה

### 3.5 pctFromAth (% מהשיא)

```
pctFromAth = ((lastClose - PeriodHigh) / PeriodHigh) × 100
```

- שלילי כשהמחיר מתחת לשיא

### 3.6 monthsInConsolidation (חודשים באיחוד)

```
periodHighThreshold   = PeriodHigh × 0.98
periodHighIndex       = האינדקס האחרון שבו close >= periodHighThreshold (ב־252 ימים)
tradingDaysSinceHigh  = 251 - periodHighIndex
monthsInConsolidation = tradingDaysSinceHigh / 21
```

- **21** = ימי מסחר לחודש
- "נגיעה" בשיא = מחיר בתוך 2% מהשיא

---

## 4. אינדיקטורים למבנה Setup

### 4.1 nearSMA21 (קרבה ל־SMA21)

```
pctDiff    = |lastPrice - SMA21| / SMA21 × 100
nearSMA21  = (pctDiff ≤ 3%)
```

| סטטוס | טווח | ערך ברירת מחדל |
|-------|------|----------------|
| ✓ Full | ≤3% | `SMA21_TOUCH_THRESHOLD_PCT` |
| ~ Close | 3%–5% | `SMA21_CLOSE_THRESHOLD_PCT` |

### 4.2 nearAth (קרבה ל־52w High)

```
absPct   = |pctFromAth|
nearAth  = (absPct ≤ 20%)
```

| סטטוס | טווח | ערך ברירת מחדל |
|-------|------|----------------|
| ✓ Full | ≤20% | `ATH_THRESHOLD_PCT` |
| ~ Close | 20%–25% | `ATH_CLOSE_THRESHOLD_PCT` |

### 4.3 inConsolidationWindow (חלון איחוד)

```
inConsolidationWindow = (monthsInConsolidation ≥ 6) AND (monthsInConsolidation ≤ 36)
```

| סטטוס | טווח (חודשים) | ערך ברירת מחדל |
|-------|----------------|----------------|
| ✓ Full | 6–36 | `CONSOLIDATION_MIN_MONTHS`, `CONSOLIDATION_MAX_MONTHS` |
| ~ Close | 4–6 | `CONSOLIDATION_CLOSE_MIN_MONTHS` |

---

## 5. תבניות Setup

### 5.1 Full Setup (🎯)

מניה מקבלת **Full Setup** כאשר **כל** התנאים מתקיימים:

| # | תנאי | נוסחה/ערך |
|---|------|-----------|
| 1 | RVOL | RVOL ≥ 2.0 |
| 2 | SMA21 | pctDiff ≤ 3% |
| 3 | 52w High | \|pctFromAth\| ≤ 20% |
| 4 | Base | 6 ≤ monthsInConsolidation ≤ 36 |

```
Full Setup = (RVOL ≥ minRVOL) AND nearSMA21 AND nearAth AND inConsolidationWindow
```

### 5.2 Close Setup (👀)

מניה מקבלת **Close Setup** כאשר RVOL ≥ 2 **ו**לפחות תנאי "קרוב" אחד מכל זוג:

| אינדיקטור | Full (✓) | Close (~) |
|-----------|----------|-----------|
| SMA21 | ≤3% | 3%–5% |
| 52w High | ≤20% | 20%–25% |
| Base | 6–36 חודשים | 4–6 חודשים |

```
Close Setup = (RVOL ≥ minRVOL) AND (smaOk) AND (athOk) AND (baseOk)
  where smaOk  = nearSMA21 OR nearSMA21Close
        athOk  = nearAth OR nearAthClose
        baseOk = inConsolidationWindow OR inConsolidationClose
```

---

## 6. דוח יומי — תנאי כניסה

### 6.1 סיגנלים ראשיים (Top Signals)

| תנאי | ערך | הערה |
|------|-----|------|
| RVOL | ≥ 2.0 | `MIN_RVOL` |
| \|priceChange %\| | ≥ 2% | `PRICE_CHANGE_THRESHOLD` |
| מיון | לפי RVOL יורד | — |
| הגבלה | 15 מניות | `TOP_N` |

מניות שמופיעות בדוח הראשי: RVOL גבוה **ו**שינוי מחיר משמעותי.

### 6.2 Silent Activity (נפח בלי מחיר)

| תנאי | ערך | הערה |
|------|-----|------|
| RVOL | ≥ 2.0 | כמו Top Signals |
| \|priceChange %\| | < 2% | נפח גבוה בלי תזוזה חזקה במחיר |
| הגבלה | 5 מניות | לפי RVOL יורד |

מניות עם נפח גבוה אך שינוי מחיר קטן — אפשרות לצבירה שקטה.

### 6.3 סימון בדוח

- **🎯** — Full Setup (מתקיימים כל 4 התנאים)
- **👀** — Close Setup (קרוב לתנאים)
- ללא סימון — אותות רגילים (RVOL גבוה, בלי Setup מלא)

### 6.4 סיכום ערכי ברירת מחדל

| משתנה | ערך | שימוש |
|-------|-----|-------|
| MIN_RVOL | 2.0 | סינון אותות + Setup |
| TOP_N | 15 | מספר סיגנלים ראשיים |
| PRICE_CHANGE_THRESHOLD | 2 | הפרדת Top / Silent |
| SMA21_TOUCH_THRESHOLD_PCT | 3 | nearSMA21 |
| SMA21_CLOSE_THRESHOLD_PCT | 5 | nearSMA21Close |
| ATH_THRESHOLD_PCT | 20 | nearAth |
| ATH_CLOSE_THRESHOLD_PCT | 25 | nearAthClose |
| CONSOLIDATION_MIN_MONTHS | 6 | חלון איחוד |
| CONSOLIDATION_MAX_MONTHS | 36 | חלון איחוד |
| CONSOLIDATION_CLOSE_MIN_MONTHS | 4 | חלון "קרוב" |

---

## 7. דוח שבועי — תנאי כניסה

### 7.1 מניות בדוח

| תנאי | משמעות |
|------|---------|
| setupType | **full בלבד** (🎯) |
| חלון זמן | 7 הימים האחרונים |
| מקור | קבצי תוצאות סקאן יומי (`scan-YYYY-MM-DD.json`) |

### 7.2 חישוב ביצועים

```
Δ% = (priceNow - priceThen) / priceThen × 100
```

- **priceThen** — מחיר ביום שזוהה כ־Full Setup
- **priceNow** — מחיר נוכחי (במועד הדוח השבועי)
- **ימים** — מספר ימי מסחר מאז האות

### 7.3 ממוצע

```
avgChange = sum(Δ% for all rows) / count(rows with valid Δ%)
```

---

## 8. תרשים זרימה — דוח יומי

```
Watchlist (Google Sheets)
        ↓
[Fetch market data — Yahoo / Twelve Data]
        ↓
[Calculate: RVOL, priceChange, SMA21, pctFromAth, monthsInConsolidation]
        ↓
[Apply: nearSMA21, nearAth, inConsolidationWindow (+ Close variants)]
        ↓
[Filter: RVOL ≥ 2]
        ↓
[Sort by RVOL; Full Setup preferred in ties]
        ↓
topSignals     = first 15 where |priceChange| ≥ 2%
volumeWOP      = up to 5 where |priceChange| < 2%
        ↓
[Tag: 🎯 Full | 👀 Close | —]
        ↓
Daily Report
```

---

## 9. תרשים זרימה — דוח שבועי

```
7–10 successful daily-scan runs
        ↓
Load scan-YYYY-MM-DD.json (last 7 days)
        ↓
Extract signals where setupType === 'full'
        ↓
Fetch current prices for those tickers
        ↓
Calculate Δ% per signal
        ↓
Weekly Report (table + avgChange)
```

---

## 10. צור קשר / שאלות

לבהרות לגבי המפרט — פנה למנהל הפרויקט.

*מסמך זה משקף את הלוגיקה בקוד (`src/`) נכון לתאריך המסמך.*
