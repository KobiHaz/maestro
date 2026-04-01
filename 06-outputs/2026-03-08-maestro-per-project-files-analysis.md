# Maestro — הקטנת קבצים פר־פרויקט

> **תאריך:** 2026-03-08 | **מצב:** ניתוח

---

## מצב נוכחי — קבצים פר־פרויקט

### 02-projects/<project>/

| פרויקט | project.md | README | plans-and-tasks | סה״כ |
|--------|------------|--------|-----------------|------|
| hadaryaCRM | ✓ | ✓ | — | 2 |
| cms | ✓ | ✓ | — | 2 |
| proposal-generator | ✓ | — | — | 1 |
| smart-volume-radar | ✓ | ✓ | — | 2 |
| website | ✓ | ✓ | docs/ | 2+ |
| source6681 | ✓ | ✓ | ✓ | 3 |
| gold-ira-quiz | ✓ | — | ✓ | 2 |

### 04-knowledge/reference/ — פר־פרויקט

| פרויקט | קבצים | שמות |
|--------|-------|------|
| smart-volume-radar | 5 | architecture, coding-patterns, calculations, message-guide, indicator-sources |
| source6681 | 5 | architecture, api, action-plan, vercel-setup, ebay-setup |
| hadaryaCRM | 4 | architecture, security-audit, ui-ux-plan, cursor-mcp-setup |
| cms | 6 | architecture, add-website, environment, firestore, postback, security |
| proposal-generator | 1 | architecture |

**סה״כ reference:** 21 קובץ

### 04-knowledge/standards/ — פר־פרויקט

| קובץ |
|------|
| smart-volume-radar-standards.md |
| source6681-standards.md |
| hadaryaCRM-standards.md |
| cms-standards.md |
| proposal-generator-standards.md |

**סה״כ standards:** 5 קבצים

### docs/plans/

תוכניות עם שם פרויקט — 6 קבצים. לפי maestro-project-doc-lifecycle המקור יחיד אמור להיות `02-projects/<project>/plans-and-tasks.md`.

---

## סיכום — קבצים פר־פרויקט כיום

| סוג | כמות | הערה |
|-----|------|------|
| 02-projects (brief + README + plans) | ~15 | משתנה לפי פרויקט |
| 04-knowledge/reference | 21 | פיצול ל־5–6 קבצים לפרויקט |
| 04-knowledge/standards | 5 | קובץ אחד לפרויקט |
| docs/plans | 6 | כפילות עם plans-and-tasks |

**סה״כ:** ~47 קבצים פר־פרויקט

---

## אפשרויות להקטנה

### 1. איחוד project + README

**רעיון:** `project.<name>.md` יכלול גם אינדקס התיעוד (מה שב־README).

**חיסכון:** 5–6 קבצי README.

**סיכון:** קובץ project נעשה ארוך. README כיום רק אינדקס קישורים.

**המלצה:** אפשרי — להוסיף סעיף "Reference" ב־project עם לינקים.

---

### 2. איחוד reference — קובץ אחד לפרויקט

**רעיון:** במקום `smart-volume-radar-architecture.md`, `-coding-patterns.md`, `-calculations.md` וכו׳ — קובץ אחד `smart-volume-radar-reference.md` עם סעיפים.

**חיסכון:** 21 קבצים → 5 קבצים (אחד לפרויקט).

**סיכון:** קבצים גדולים (למשל smart-volume-radar ~860 שורות). קושי למצוא נושא ספציפי.

**המלצה:** לפרויקטים עם 1–2 reference: לאחד. לפרויקטים עם 5+ (smart-volume, source6681, cms): לשקול תת־תיקייה `04-knowledge/reference/<project>/` עם קבצים, או להשאיר פיצול.

---

### 3. העברת reference לתוך 02-projects

**רעיון:** `04-knowledge/reference/smart-volume-radar-*.md` → `02-projects/smart-volume-radar/reference/` או `02-projects/smart-volume-radar/reference.md`.

**חיסכון:** לא מקטין כמות — רק מאחד מקום. כל פרויקט מרוכז תחת 02-projects.

**יתרון:** הכל תחת תיקיית הפרויקט. קל לנווט.

**המלצה:** טוב אם רוצים ריכוז — לא חיסכון בקבצים.

---

### 4. סטנדרטים — merge לתוך project brief

**רעיון:** סעיף "Standards" או "Conventions" בתוך `project.<name>.md` במקום קובץ נפרד.

**חיסכון:** 5 קבצי standards.

**סיכון:** סטנדרטים בדרך־כלל 50–100 שורות. project כבר 40–50. עלול להיות ארוך מדי.

**המלצה:** אפשרי לפרויקטים פשוטים. למורכבים — להשאיר נפרד.

---

### 5. docs/plans → 02-projects בלבד

**רעיון:** לפי maestro-project-doc-lifecycle — מקור יחיד הוא `plans-and-tasks.md`. למחוק/לאחד תוכניות מ־docs/plans.

**חיסכון:** 6 קבצים (או העברה — לא מחיקה).

**פעולה:** להעביר תוכן רלוונטי ל־plans-and-tasks, למחוק docs/plans ישנים. תוכניות חדשות רק ב־02-projects.

**המלצה:** **מומלץ** — תואם את maestro-project-doc-lifecycle.

---

### 6. proposal-generator — אין README

כבר מינימלי: project + reference אחד.

---

## תוכנית מימוש (לפי עדיפות)

| # | פעולה | חיסכון | קושי |
|---|--------|--------|------|
| 1 | docs/plans → plans-and-tasks; מחיקת כפילויות | 6 קבצים | נמוך |
| 2 | איחוד project + README (אינדקס בתוך project) | 5–6 קבצים | נמוך |
| 3 | standards קטנים → merge ל־project | 2–3 קבצים | בינוני |
| 4 | reference: איחוד לפרויקטים עם 1–2 קבצים | 2–3 קבצים | נמוך |
| 5 | reference: תיקייה לפרויקט במקום קבצים שטוחים | 0 (ארגון) | נמוך |

---

## סיכום

**הקטנה ריאלית:** 15–20 קבצים (מ־~47 ל־~30).

**שלב ראשון מומלץ:**
1. איחוד docs/plans ב־plans-and-tasks לפי maestro-project-doc-lifecycle
2. merge README ל־project (אינדקס כתת־סעיף)
3. לפרויקטים עם reference יחיד (proposal-generator) — לאחד לתוך project או להשאיר קובץ אחד
