# ניתוח כפילויות — Standards & Reference

> **תאריך:** 2026-03-08  
> **בוצע:** 2026-03-08 — Plan Lifecycle + Plan file naming אוחדו ב־maestro-project-doc-lifecycle

---

## 1. Standards — כפילות עם base-coding-standards

### 1.1 מה יש ב-base (משותף)

- Naming (כללי): get*/fetch*/load*, Booleans, Constants, React
- TypeScript: no any, imports at top, exhaustive switch
- Security: validate inputs, no secrets in client, auth on server
- Error handling §10: central logging service (לא מפרט logger vs console)
- Plan files: לא מוזכר ב-base

### 1.2 כפילות שמצאתי בפרויקטים

| פרויקט | כפילות | המלצה |
|--------|--------|--------|
| **כולם** | **Plan Lifecycle** — 5 פעמים כמעט identical | להחליף ב־"פירוט: [[maestro-project-doc-lifecycle]]" |
| smart-volume | "Imports — see base section 3" | ✓ טוב — לא כפיל |
| smart-volume | "TypeScript, Error Handling — see base" | ✓ טוב |
| smart-volume | Review Checklist: "No console.log" | OK — base לא מפרט; זה project-specific |
| cms | "Data loading, lookups — see base 4, 5" | ✓ טוב |
| proposal | "TypeScript, exhaustive switch — base §3" | ✓ טוב |
| **כולם** | **Plan files naming** — YYYY-MM-DD-kebab (חוזר 5 פעמים) | להעביר ל־maestro-project-doc-lifecycle או base |
| hadaryaCRM | "Don't delete plans yourself — suggest" | שונה מ-maestro — hadaryaCRM מחמיר יותר. להשאיר. |

### 1.3 סיכום Standards

**כפילות מובהקת:** Plan Lifecycle ב־5 קבצים. כבר קיים ב־maestro-project-doc-lifecycle — למחוק מהפרויקטים.

**חיסכון:** ~15–20 שורות × 5 = ~75 שורות. + Plan file naming pattern — לאחד.

---

## 2. Reference — כפילויות ומבנה דומה

### 2.1 טיפוסי קבצי Reference (לפי פרויקט)

| פרויקט | Architecture | Security | API/Setup | אחר |
|--------|--------------|----------|-----------|-----|
| smart-volume | ✓ | (באדריכלות) | — | calculations, coding-patterns, message-guide, indicator-sources |
| source6681 | ✓ | (באדריכלות) | api, vercel-setup, ebay-setup | action-plan |
| hadaryaCRM | ✓ | security-audit ✓ | — | ui-ux-plan, cursor-mcp-setup |
| cms | ✓ | security-audit ✓ | — | add-website, environment, firestore, postback |
| proposal | ✓ | — | — | — |

### 2.2 כפילויות בין Reference לקבצים אחרים

| קובץ reference | כפילות עם |
|----------------|----------|
| smart-volume-radar-architecture | Key Decisions (Logging, Security) — גם ב־standards. אבל architecture מפרט יותר (validateTicker, p-limit). Standards מקצר. **המלצה:** architecture = פרטים; standards = כללים. דקה — OK. |
| smart-volume-radar-coding-patterns | Naming (fetch/load/get) — base כבר מגדיר. coding-patterns מתאר "observed patterns" בקוד — זה reference לא rule. **אין כפילות אמיתית** (מטרה שונה). |
| כל architecture | Tech Stack — גם ב־standards. **כפילות קלה.** אפשר ב־standards רק לינק "Tech stack: [[reference/xxx-architecture]]" ולהוציא Tech Stack מ־standards. |

### 2.3 קבצי Reference דומים — איחוד אפשרי?

| סוג | smart-volume | source6681 | hadaryaCRM | cms |
|-----|--------------|------------|------------|-----|
| architecture | 75 שורות | 97 | 67 | 59 |
| security-audit | — | — | 40 | 43 |
| setup/docs | — | 3 (api, vercel, ebay) | 2 (mcp) | 4 (env, firestore, postback, add-website) |

**מסקנה:** אין שני קבצי reference שמתארים אותו דבר. כל קובץ ייחודי לפרויקט. 

**אבל:** smart-volume יש **5** קבצי reference נפרדים (architecture, coding-patterns, calculations, message-guide, indicator-sources). 
- **calculations** — 244 שורות — חישובים (RVOL, SMA וכו׳) — ייחודי
- **message-guide** — 161 — פורמט הודעות Telegram — ייחודי  
- **indicator-sources** — 89 — מקורות לאינדיקטורים — ייחודי
- **coding-patterns** — 236 — patterns שנצפו — חופף חלקית ל־architecture ו־standards אבל מפורט יותר

**אופציה:** לאחד את coding-patterns לתוך architecture (סעיף "Observed Patterns") — מקטין קובץ אחד. מסוכן — architecture כבר 75 שורות, coding-patterns 236. ייצר קובץ ענק.

**אופציה אחרת:** להשאיר פיצול — כל קובץ מתמקד בנושא. אין כפילות תוכן אמיתית.

### 2.4 Reference — סיכום

- **אין כפילות בין פרויקטים** — כל reference ספציפי
- **כפילות קלה:** Tech Stack ב־architecture וגם ב־standards — אפשר לצמצם ב־standards ללינק
- **smart-volume 5 קבצים** — לגיטימיים; נושאים שונים. איחוד יוצר קובץ ענק — לא מומלץ

---

## 3. המלצות לפעולה

### 3.1 Standards — חובה

1. **להחליף Plan Lifecycle** בכל 5 קבצי standards ב־:
   ```
   ## Plan Lifecycle
   פירוט: [[04-knowledge/standards/maestro-project-doc-lifecycle]]
   ```
   ולמחוק את 4–6 השורות המקוריות.

2. **Plan file naming** — אם כל הפרויקטים משתמשים ב־YYYY-MM-DD-kebab, להוסיף ל־maestro-project-doc-lifecycle סעיף:
   ```
   ## תבנית שם תוכנית
   YYYY-MM-DD-kebab-description.md
   ```
   ולהוציא מכל project standards.

### 3.2 Standards — אופציונלי

3. **Tech Stack** — ב־standards: אם architecture כבר מכיל Tech Stack, אפשר ב־standards רק:
   ```
   ## Tech Stack
   [[04-knowledge/reference/<project>-architecture|Architecture]]
   ```
   חיסכון קטן.

### 3.3 Reference — לא נדרש

- אין איחוד מומלץ. הקבצים ייחודיים.
- smart-volume 5 קבצים — לשמור. כל אחד מתמקד בנושא.

---

## 4. סיכום ביצוע

| פעולה | קבצים נוגעים | חיסכון |
|-------|--------------|--------|
| Plan Lifecycle → maestro link | 5 standards | ~70 שורות |
| Plan file naming → maestro | maestro-project-doc-lifecycle + 5 standards | ~15 שורות |
| (אופציונלי) Tech Stack link | 5 standards | ~20 שורות |

**סה״כ:** הקטנת ~100 שורות כפילות. לא מקטין מספר קבצים — מקטין תוכן כפול.
