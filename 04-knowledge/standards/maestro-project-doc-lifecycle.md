---
type: standard
applies: all-projects
---

# Maestro — חוקי פרויקט (חובה)

> **מפנים:** [[03-agents/agent-routing]]

## 1. מקור יחיד

תוכניות פעולה (תוכניות) ומשימות — **רק בקובץ אחד** לכל פרויקט:
- `02-projects/<project>/plans-and-tasks.md`

אין תוכניות מפוצלות. אין קבצי משימות נפרדים.

## 2. מחיקה לאחר ביצוע

אחרי שמשימה בוצעה:
- למחוק את המשימה מהקטע "פתוח" (או להעביר ל"הושלם" בקצרה)
- למחוק תוכניות מפורטות ישנות שכבר הושלמו
- לשמור רק את המקור היחיד — `plans-and-tasks.md` מעודכן

## 3. עדכון דוקומנטציה

אחרי שינויים בקוד:
- לעדכן `04-knowledge/reference/<project>-*` — אם ארכיטקטורה/API השתנו
- לעדכן `04-knowledge/standards/<project>-standards.md` — אם נוספו conventions
- הבסיס המשותף: `04-knowledge/standards/base-coding-standards.md` — עובדים על כל הפרויקטים
- במידת הצורך — לא כל שינוי מחייב; רק כשיש השפעה על התיעוד

### דוחות — רק בכספת

אין לשמור דוחות (אבטחה, ביצועים, ביקורת) בתיקיית `docs/` של הפרויקט. מקור האמת הוא הכספת: `04-knowledge/reference/`, `06-outputs/`, `07-logs/`.

## 4. תבנית שם תוכנית

`YYYY-MM-DD-kebab.md` או `YYYY-MM-DD-kebab-description.md`  
דוגמאות: `2026-03-01-smart-volume-radar-remaining-tasks.md`, `2025-02-23-modular-permissions-implementation.md`

## מבנה

```
02-projects/<project>/
  project.<project>.md     ← כרטיס פרויקט
  plans-and-tasks.md       ← מקור יחיד לתוכניות ומשימות

04-knowledge/
  reference/<project>-*.md
  standards/<project>-standards.md
```
