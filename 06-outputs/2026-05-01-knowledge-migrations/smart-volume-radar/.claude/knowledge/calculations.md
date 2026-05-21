# smart-volume-radar — Calculation Reference

Exact formulas used in `src/utils/technicalAnalysis.ts` and `src/services/marketData.ts`.

## Data Source (Yahoo Chart)

URL: `https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=5y`
Arrays: `volumes[]`, `closes[]` — chronological, newest last (index 0 = oldest).

---

## RVOL (Relative Volume)

```
currentVolume    = volumes[volumes.length - 1]
historicalVols   = volumes.slice(0, -1)          // exclude today
lookback63       = historicalVols.slice(-63)       // 63-day window (~3 months)
avgVolume        = sum(lookback63) / lookback63.length
RVOL             = currentVolume / avgVolume
```

- 63-day SMA baseline (industry standard; avoids liquidity-tier distortion from 5y)
- If < 63 historical days: use all available
- Config: `VOLUME_RVOL_LOOKBACK = 63`

## Price Change (%)

```
priceChange = ((closes[-1] - closes[-2]) / closes[-2]) * 100
```

## SMA (Simple Moving Average)

```
SMA(prices, N) = sum(prices[length-N : length]) / N
// returns undefined if length < N
```

Used for SMA21, SMA50, SMA200.

## RSI — 14-period, Wilder's Smoothing

```
// Seed: simple average of first 14 periods
sumGain, sumLoss = 0
for i = 1 to 14:
  diff = prices[i] - prices[i-1]
  sumGain += max(diff, 0)
  sumLoss += max(-diff, 0)
avgGain = sumGain / 14
avgLoss = sumLoss / 14

// Wilder's: ((prev * 13) + current) / 14
for i = 15 to length-1:
  diff = prices[i] - prices[i-1]
  avgGain = (avgGain * 13 + max(diff, 0)) / 14
  avgLoss = (avgLoss * 13 + max(-diff, 0)) / 14

if avgLoss == 0: return 100
RS = avgGain / avgLoss
RSI = 100 - (100 / (1 + RS))
```

Matches TradingView. Wilder's (not Cutler's simple average).

## 52-Week High (PeriodHigh_52w)

```
lookback = closes.slice(-252)          // 252 trading days ≈ 1 year
PeriodHigh_52w = max(lookback)
// Variable name in code: `ath` (legacy)
```

## pctFromAth

```
pctFromAth = ((lastClose - PeriodHigh_52w) / PeriodHigh_52w) * 100
// Negative when below 52w high
```

## monthsInConsolidation

```
threshold = PeriodHigh_52w * 0.98
// Most recent bar within 2% of 52w high
periodHighIndex = last index i where lookback[i] >= threshold
tradingDaysSinceHigh = lookback.length - 1 - periodHighIndex
monthsInConsolidation = tradingDaysSinceHigh / 21   // 21 trading days/month
// If no bar found: periodHighIndex = -1 → full lookback
```

---

## Setup Threshold Config

| Variable | Default | Used in |
|----------|---------|---------|
| `ATH_THRESHOLD_PCT` | 20 | nearAth |
| `ATH_CLOSE_THRESHOLD_PCT` | 25 | nearAthClose |
| `SMA21_TOUCH_THRESHOLD_PCT` | 3 | nearSMA21 |
| `SMA21_CLOSE_THRESHOLD_PCT` | 5 | nearSMA21Close |
| `CONSOLIDATION_MIN_MONTHS` | 6 | inConsolidationWindow |
| `CONSOLIDATION_MAX_MONTHS` | 36 | inConsolidationWindow |
| `CONSOLIDATION_CLOSE_MIN_MONTHS` | 4 | inConsolidationClose |

## Derived Booleans

```
nearAth              = |pctFromAth| ≤ ATH_THRESHOLD_PCT
nearAthClose         = (NOT nearAth) AND |pctFromAth| ≤ ATH_CLOSE_THRESHOLD_PCT
inConsolidationWindow = months ≥ MIN AND months ≤ MAX
inConsolidationClose  = (NOT window) AND months ≥ CLOSE_MIN AND months < MIN
nearSMA21            = |lastPrice - sma21| / sma21 * 100 ≤ SMA21_TOUCH_THRESHOLD_PCT
nearSMA21Close       = (NOT nearSMA21) AND pctDiff ≤ SMA21_CLOSE_THRESHOLD_PCT
```
