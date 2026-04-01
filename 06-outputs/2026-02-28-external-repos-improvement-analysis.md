# דוח שיפור סוכנים — למידה מרפוזיטוריז חיצוניים

**תאריך:** 2026-02-28  
**מקורות:** code-review-expert, Claude Code, awesome-llm-apps, DeerFlow, Superpowers, Agent of Empires

---

## הערה: Antigravity

**"Antigravity"** במערכת שלך מתייחס לנתיב הפרויקטים `~/.gemini/antigravity/projects/` — זה המיקום הפיזי של הפרויקטים (hadaryaCRM, cms, proposal-generator וכו'), לא רפוזיטור חיצוני.

אם התכוונת לרפוזיטור אחר — ציין ואעדכן.

---

## סיכום מנהלים

| מקור | מה אפשר לקחת | עדיפות |
|------|---------------|--------|
| **code-review-expert** | Workflow מקצועי ל-code review, checklists מפורטים, P0-P3, SOLID, removal plan | גבוהה מאוד |
| **Superpowers (obra)** | finishing-a-development-branch, receiving-code-review, שיפור execute workflow | גבוהה |
| **DeerFlow** | Progressive skill loading, skill-creator, find-skills | בינונית |
| **Claude Code** | MCP integration, plugin structure | נמוכה (תלויה בפלטפורמה) |
| **Agent of Empires** | ניהול session, multi-agent parallel — לא ישים ישירות | נמוכה |
| **awesome-llm-apps** | אינדקס רחב של patterns — יותר רפרנס מאשר שינוי | נמוכה |

---

## 1. code-review-expert — העשרת Code Review

**מקור:** [sanyuan0704/code-review-expert](https://github.com/sanyuan0704/code-review-expert)

### מה חסר לנו לעומת code-review-expert

| נושא | שלנו (Maestro) | code-review-expert |
|------|----------------|---------------------|
| **workflow** | review.md כללי | 7 שלבים מוגדרים: Preflight → SOLID → Removal → Security → Code Quality → Output → Confirmation |
| **git integration** | לא מוזכר | `git diff`, `git status -sb` — סקירת שינויים בלבד |
| **SOLID checklist** | code-review-checklist מזכיר "SOLID" | solid-checklist מפורט עם שאלות לכל עיקרון |
| **Removal plan** | אין | removal-plan.md — dead code, safe vs defer |
| **Severity levels** | CRITICAL/HIGH/MEDIUM/LOW | P0/P1/P2/P3 עם פעולות ספציפיות |
| **Next steps** | אין | "Fix all / Fix P0+P1 / Fix specific / No changes" |
| **Race conditions** | לא מפורט | security-checklist מכסה TOCTOU, concurrent access |
| **Boundary conditions** | לא מפורט | code-quality: null, empty, off-by-one, numeric limits |

### המלצות יישום

1. **העשרת review workflow** עם:
   - Preflight: `git diff` scope
   - שלב SOLID נפרד
   - שלב Removal candidates
   - Next steps confirmation

2. **יצירת skills/code-review/** עם:
   - `solid-checklist.md` (מ־code-review-expert)
   - `security-checklist.md` (להרחיב עם race conditions)
   - `code-quality-checklist.md` (boundary conditions, error handling)
   - `removal-plan.md` (תבנית למחיקת קוד)

3. **עדכון review workflow**:
   - שימוש ב־specialists לפי סוג קוד
   - פורמט output: P0/P1/P2/P3
   - Inline comments format (אם הפלטפורמה תומכת)

4. **חיבור ל־test-engineer**:
   - code-review-expert שואל לפני implementation
   - Maestro כבר מפריד review מ־execute — לשמור על זה

---

## 2. Superpowers (obra) — שיפורי Workflow

**מקור:** [obra/superpowers](https://github.com/obra/superpowers)

### מה יש ב־Superpowers שאין אצלנו

| Skill | תיאור | רלוונטי ל-Maestro? |
|-------|--------|---------------------|
| **using-git-worktrees** | יצירת workspace מבודד על branch חדש | כן — יש parallel-agents |
| **finishing-a-development-branch** | Merge/PR decision, verify tests, cleanup worktree | כן — חסר workflow סיום |
| **receiving-code-review** | מענה ל־feedback מקוד review | כן — peer-review דומה אבל לא זהה |
| **subagent-driven-development** | subagent לכל task + two-stage review | כן — orchestrator עושה דומה |
| **executing-plans** | Batch execution עם checkpoints | כן — execute.md דומה |
| **verification-before-completion** | לוודא שהתיקון באמת עובד | חלקי — יש ב-debugger |
| **dispatching-parallel-agents** | subagents במקביל | יש parallel-agents skill |

### המלצות

1. **workflow חדש: finishing-branch** (מבוסס finishing-a-development-branch):
   ```
   כשכל המשימות הושלמו:
   - Verify tests pass
   - Present options: Merge / PR / Keep branch / Discard
   - Cleanup worktree if needed
   ```

2. **הרחבת peer-review** עם receiving-code-review:
   - פורמט למענה לכל finding
   - Priorities לטיפול
   - אימות שה־fix אכן פותר את הבעיה

3. **שילוב verification-before-completion** ב־execute:
   - לפני "done" — הרצת `npm run test`, `npm run build`
   - וידוא שכל הבדיקות עוברות

---

## 3. DeerFlow — Progressive Skills & Find-Skills

**מקור:** [bytedance/deer-flow](https://github.com/bytedance/deer-flow)

### רעיונות רלוונטיים

| רעיון | תיאור | יישום ב-Maestro |
|-------|--------|-----------------|
| **Progressive loading** | Skills נטענים רק כשצריך | Maestro טוען לפי agent-routing — כבר דומה |
| **find-skills** | חיפוש skills לפי משימה | אפשר skill: "איזה skill לקרוא עבור X?" |
| **skill-creator** | יצירת skills חדשים | יש skill-template — אפשר להרחיב |
| **Deep research** | מחקר מעמיק | explorer-agent + brainstorming מכסים חלקית |

### המלצות

1. **intelligent-routing** קיים — לוודא שהוא מפנה ל־skills הנכונים
2. **skill-template** — להוסיף סעיף "כיצד לבדוק skill חדש" (מ־Superpowers writing-skills)
3. **Deep research workflow** — לשקול אם יש צורך (explorer + brainstorm אולי מספיקים)

---

## 4. Claude Code — אינטגרציה

**מקור:** [anthropics/claude-code](https://github.com/anthropics/claude-code)

### מה רלוונטי

- MCP servers — Maestro כבר משתמש ב־MCP (Notion, Firebase, Cloudflare וכו')
- Plugin structure — Cursor פלטפורמה שונה
- `/bug` command — אפשר להוסיף workflow דומה: "דווח על באג" → יוצר issue מסודר

### המלצה

- **workflow: bug-report** — כשמשתמש מדווח על באג, ליצור מסמך מוכן ל־GitHub issue עם: תיאור, צעדים לשחזור, expected vs actual, סביבה.

---

## 5. Agent of Empires — Multi-Session

**מקור:** [njbrake/agent-of-empires](https://github.com/njbrake/agent-of-empires)

### מה עושה AoE

- ניהול sessions של agents (Claude Code, Cursor CLI וכו')
- Git worktrees — הרצת agents על branches שונים במקביל
- TUI dashboard

### רלוונטיות ל-Maestro

- Maestro הוא vault-based, לא session manager
- AoE משלים — אפשר להריץ Maestro מתוך AoE
- לא לשנות את Maestro בהתאם — יותר תיעוד "עבודה עם AoE"

---

## 6. awesome-llm-apps — רפרנס

**מקור:** [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps)

- אוסף רחב של LLM apps, agents, RAG
- שימושי כרפרנס ורעיונות
- אין skill/workflow ספציפי להעתקה
- המלצה: לשמור קישור ב־04-knowledge כרפרנס

---

## מניעת כפילויות — וידוא לפני יישום

### מה קיים היום

| סוג | שם | מיקום | תפקיד |
|-----|-----|-------|-------|
| **Skill** | code-review-checklist | skills/code-review-checklist/ | checklist כללי ל־code review |
| **Workflow** | review | workflows/review.md | /review — code review |
| **Workflow** | peer-review | workflows/peer-review.md | ולידציה של feedback ממודל אחר |
| **Workflow** | execute | workflows/execute.md | ביצוע תוכנית |

### כללי יישום (אין סוכנים/סקילס כפולים)

1. **אין סוכנים חדשים** — רק skills ו־workflows.
2. **code-review** — לא ליצור `skills/code-review/` נפרד. להרחיב את `code-review-checklist`:
   - להוסיף `solid-checklist.md`, `security-checklist.md`, `code-quality-checklist.md`, `removal-plan.md` **בתוך** `skills/code-review-checklist/`
   - כך נשאר skill אחד: `code-review-checklist`
3. **finishing-branch** — workflow חדש, לא חופף:
   - execute = מימוש תוכנית; finishing-branch = merge/PR/cleanup אחרי סיום
4. **review.md** — עדכון workflow קיים, לא יצירת workflow חדש.

---

## תוכנית יישום מומלצת

### שלב 1 — Code Review (גבוהה עדיפות)

| משימה | קובץ | פעולה |
|-------|------|--------|
| 1 | `03-agents/skills/code-review-checklist/` | **הרחבה** — הוספת קבצי reference (לא תיקייה חדשה) |
| 2 | `solid-checklist.md` | יצירה **בתוך** code-review-checklist |
| 3 | `security-checklist.md` | יצירה **בתוך** code-review-checklist (+ race conditions) |
| 4 | `code-quality-checklist.md` | יצירה **בתוך** code-review-checklist |
| 5 | `removal-plan.md` | יצירה **בתוך** code-review-checklist |
| 6 | `03-agents/workflows/review.md` | עדכון workflow קיים (7 שלבים) |
| 7 | `agent-routing.md` | ללא שינוי — review כבר ב־trigger 25 |

### שלב 2 — Workflows חסרים (בינונית עדיפות)

| משימה | קובץ | פעולה | כפילות? |
|-------|------|--------|---------|
| 1 | `03-agents/workflows/finishing-branch.md` | יצירה — merge/PR/cleanup | אין — execute בונה, finishing מסכם |
| 2 | `03-agents/workflows/execute.md` | הוספת verification-before-completion | עדכון קיים |
| 3 | `03-agents/workflows/peer-review.md` | הרחבת receiving-code-review | עדכון קיים |
| 4 | `03-agents/workflows/bug-report.md` | אופציונלי — bug report מוכן | אין — workflow חדש ייחודי |

### שלב 3 — שיפורים קלים (נמוכה עדיפות)

| משימה | פעולה |
|-------|--------|
| 1 | עדכון skill-template עם testing methodology |
| 2 | הוספת 04-knowledge reference ל־awesome-llm-apps |
| 3 | תיעוד אינטגרציה עם Agent of Empires (אם רלוונטי) |

---

## השוואת Code Review — לפני ואחרי

### לפני (נוכחי)

```
review.md:
- Check For: Logging, Error Handling, TypeScript...
- Output: ✅ Looks Good / ⚠️ Issues Found
- Severity: CRITICAL, HIGH, MEDIUM, LOW
```

### אחרי (מומלץ)

```
review.md:
1. Preflight: git diff scope
2. SOLID + Architecture (solid-checklist)
3. Removal candidates (removal-plan)
4. Security (security-checklist, כולל race conditions)
5. Code Quality (boundary conditions, error handling)
6. Output: P0/P1/P2/P3 format
7. Next Steps: Fix all / Fix P0+P1 / Fix specific / No changes

+ Load references from 03-agents/skills/code-review-checklist/
```

---

## קישורים

- [code-review-expert](https://github.com/sanyuan0704/code-review-expert)
- [Superpowers](https://github.com/obra/superpowers)
- [DeerFlow](https://github.com/bytedance/deer-flow)
- [Claude Code](https://github.com/anthropics/claude-code)
- [Agent of Empires](https://github.com/njbrake/agent-of-empires)
- [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps)

---

**סוף הדוח**
