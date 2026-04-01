# שינויים נדרשים — התאמת הפרויקטים ל-base-coding-standards

> **תאריך:** 2 מרץ 2026  
> **מטרה:** רשימת שינויים בקוד כדי שכל פרויקט יעמוד ב-base-coding-standards. אין דריסות — משנים את הקוד.

---

## source6681

**פרויקט:** Vintage handbag archive/dropship. Path: ראה 02-projects/source6681.

### Naming (Base §2)

| נוכחי | נדרש | הערות |
|-------|------|--------|
| `use-wishlist.ts` | `useWishlist.ts` | Hooks: `use`+PascalCase |
| `use-toast.ts` | `useToast.ts` | |
| `use-mobile.ts` | `useMobile.ts` | |
| `format-price.ts` | `formatPrice.ts` | Utilities: camelCase |
| `proxy-image.ts` | `proxyImage.ts` | |
| `product-utils.ts` | `productUtils.ts` | |
| `ga-loader.ts` | `gaLoader.ts` | |

**פעולות:**
1. שנה שמות קבצי hooks ל־`use`+PascalCase
2. שנה שמות קבצי lib ל־camelCase
3. עדכן את כל ה-imports בפרויקט

---

## hadaryaCRM

**פרויקט:** Demo CRM. Path: ראה 02-projects/hadaryaCRM.

### בדיקה נדרשת

- [ ] Folders: kebab-case — Base לא מגדיר. אם יש `entity-page`, `ad-agency` — OK כתוספת.
- [ ] Components, Hooks, Lib — לוודא תואמים ל-base (PascalCase, use+PascalCase, camelCase)
- [ ] אין `any`, exhaustive switch, imports למעלה — audit קצר

---

## cms

**פרויקט:** CMS multi-vertical. Path: ראה 02-projects/cms.

### בדיקה נדרשת

- [ ] Data loading: normalize ב-loaders בלבד (Base §4)
- [ ] Lookups: Map ל-O(1), לא `.find()` בלולאות (Base §5)
- [ ] Naming: Components, Hooks, Services — לפי base

---

## smart-volume-radar

**פרויקט:** Node CLI — stock volume monitoring. Path: ~/.gemini/antigravity/projects/smart-volume-radar.

### בדיקה נדרשת

- [ ] TypeScript §3: No `any`, exhaustive switch, imports למעלה
- [ ] Error Handling §10: try/catch, לא catch ריק
- [ ] Logging: `logger` בלבד (כבר בסטנדרט הפרויקט)

---

## proposal-generator

**פרויקט:** Proposal/Quote generator. Path: ראה 02-projects/proposal-generator.

### בדיקה נדרשת

- [ ] Context: useMemo ל-value — כבר מוגדר (מוצדק per base)
- [ ] TypeScript §3: No `any`, exhaustive switch
- [ ] Naming: Components, Hooks, Lib — לפי base

---

## סיכום לפי עדיפות

| פרויקט | שינויים עיקריים | effort |
|--------|-----------------|--------|
| **source6681** | שינוי שמות hooks + lib (7+ קבצים) | בינוני |
| hadaryaCRM | Audit | נמוך |
| cms | Audit | נמוך |
| smart-volume-radar | Audit | נמוך |
| proposal-generator | Audit | נמוך |

**המלצה:** להתחיל ב-source6681 — שם יש פער ידוע (kebab-case). שאר הפרויקטים — audit כדי לאמת עמידה.
