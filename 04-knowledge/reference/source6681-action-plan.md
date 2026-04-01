---
project: source6681
type: reference
updated: 2026-03-02
---

# source6681 — תוכנית פעולה מרכזית

> **מקור יחיד.** כל המשימות והעדיפויות במקום אחד. checkout לא רלוונטי כרגע.

---

## הושלם (סיכום)

| תחום | פריטים |
|------|--------|
| **Product View** | product-utils, ProductModal, ArchiveItem, SOLD/ARCHIVED badge |
| **Performance** | Server-side filtering, URL filters, infinite scroll, content-visibility, deep link product fetch |
| **Security** | is_admin, RLS, CRON_SECRET, Admin Bearer |
| **Security (02.03)** | Security headers (X-Frame-Options, X-Content-Type-Options, Referrer-Policy), rate limiting (Upstash) |
| **Production** | .trim() ל-env vars, image domains, validate-env.mjs |
| **Condition Rank** | SA ב-DB, types, ProductModal, FilterDrawer |
| **CI/CD** | lint, build, test, smoke, verify-admin-isolation |
| **Docs** | CHANGELOG, API, eBay setup, architecture |

---

## תוכנית ביצוע — לפי עדיפות

### P2 — Production Verification

| # | משימה | פרטים |
|---|--------|--------|
| 1 | Redeploy עם הקוד הנוכחי | trim fixes + image domains + security headers |
| 2 | בדיקת WebSocket | אחרי deploy — console ללא שגיאות Realtime |
| 3 | בדיקת תמונות | product images נטענות, אין 400 על _vercel/image |
| 4 | env vars ב-Vercel | אופציונלי: העתקה מחדש ללא newlines ([vercel#14371](https://github.com/vercel/vercel/issues/14371)) |

### P2 — eBay & Admin

| # | משימה |
|---|--------|
| 1 | eBay: availability API, rate limits |

### P2 — Testing

| # | משימה |
|---|--------|
| 1 | הרחבת check-browser לכיסוי admin |

### P3 — אופציונלי

| משימה |
|--------|
| npm audit — 2 moderate נשארו (esbuild/vite, דורש Vite 7) |
| ErrorBoundary → logger |
| BRAND_PATTERNS → lib/brand-patterns.ts |
| TanStack Query — להסיר או לאמץ |
| Lucide direct imports — מדוד השפעה |
| fetchAllSoldProductIds / banner brands — אופטימיזציה לקטלוג גדול |
| connection pooling (Supabase at scale) |

---

## Rate Limiting (proxy-image)

**מימוש:** Upstash Redis. כש-`UPSTASH_REDIS_REST_URL` ו-`UPSTASH_REDIS_REST_TOKEN` לא מוגדרים — מאפשר הכל.

**הפעלה:** יצירת Redis ב-[upstash.com](https://upstash.com), הוספת ה-secrets ב-Supabase Edge Functions.

---

## Production Issues (סיכום)

**תסמינים:** WebSocket %0A, Image 400.

**שורש:** Env vars ב-Vercel עם trailing newline; חסר domain ב-vercel.json.

**תיקונים קיימים:** .trim(), image domains, validate-env.mjs. **נדרש:** deploy + verification.

---

## Reference

- Architecture: source6681-architecture
- API: source6681-api
- Vercel: source6681-vercel-setup
- eBay: source6681-ebay-setup
- Standards: source6681-standards
