# דוח ניתוח כפילויות במטרות סוכנים וסקילס

**תאריך:** 2026-02-28  
**מטרה:** בדיקה אם יש סוכנים או סקילס עם מטרות חופפות שאפשר לאחד

> **עדכון 2026-04-01:** חלק מההמלצות למטה **יושמו** — אין `create-plan` נפרד; `ui-ux-pro-max` הועבר ל־`specialists/ui-ux-specialist.md`; `learning-opportunity` ל־`technical-educator`; `preview` מוזג ל־`workflows/status.md`. מקור אמת: `agent-routing.md`.

---

## סיכום מנהלים

נמצאו **כמה חפיפות משמעותיות** ו**כמה חפיפות קלות** שלא בהכרח מצריכות איחוד, אבל כדאי לשים לב אליהן.

### חפיפות משמעותיות (מומלץ לבחון איחוד)

| # | סוכנים/סקילס | סוג החפיפה | המלצה |
|---|--------------|------------|--------|
| 1 | **project-planner** vs ~~create-plan~~ | (היסטורי) שניהם יוצרים תוכניות עבודה | **בוצע:** תכנון אחיד דרך `/plan` + project-planner |
| 2 | **security-auditor** vs **penetration-tester** | שניהם בודקים אבטחה ופגיעויות | להשאיר נפרדים – מתודולוגיות שונות (defensive vs offensive) |
| 3 | **performance-optimizer** vs **seo-specialist** | שניהם נוגעים ב-Core Web Vitals | חפיפה מתונה – Triggers שונים; לשקול הפניה הדדית |
| 4 | **frontend-specialist** vs **ui-ux-specialist** | שניהם נוגעים ב־UI | חפיפה חלקית — frontend = יישום; ui-ux = עיצוב/מערכת עיצוב (skill `ui-ux-pro-max`) |

### חפיפות קלות (אין צורך באיחוד)

- **debugger** vs **performance-optimizer** – חפיפה מצומצמת (performance bugs)
- **plan (workflow)** vs **project-planner** – plan מפעיל את project-planner
- **compliance (workflow)** vs **compliance-auditor** – compliance מפעיל את compliance-auditor

---

## ניתוח מפורט לפי קטגוריה

### 1. Core Agents

| Agent | מטרה עיקרית | חפיפות |
|-------|-------------|--------|
| **orchestrator** | תיאום סוכנים מרובים, פירוק משימות | משתמש ב־project-planner – לא חפיפה |
| **cto** | ארכיטקטורה, החלטות טכנולוגיות | חפיפה קלה עם explorer – CTO מקבל החלטות, explorer ממפה |
| **project-planner** | פירוק למשימות, תוכניות עם 🟩🟨🟥, dependency graph | **אוחד (2026-04):** אין create-plan נפרד — `/plan` מפעיל project-planner |

**סטטוס (2026-04-01):** תוכניות כוללות **Overall Progress** ו־🟩🟨🟥 על משימות; ראו `workflows/plan.md`.

---

### 2. Specialists – אבטחה

| Agent | מטרה | Triggers |
|-------|------|----------|
| **security-auditor** | ביקורת אבטחה, OWASP, supply chain | security, vulnerability, owasp, xss... |
| **penetration-tester** | בדיקות חדירה, red team, exploitation | pentest, exploit, attack, hack... |

**ניתוח:**  
שניהם עוסקים באבטחה, אבל:
- **security-auditor**: defensive, code review, סקירת קוד
- **penetration-tester**: offensive, 시뮜ציה של תקיפה, exploitation

**המלצה:** להשאיר נפרדים – מתודולוגיות שונות. ב־agent-routing יש הבחנה ברורה לפי Triggers.

---

### 3. Specialists – ביצועים ו־SEO

| Agent | מטרה | חפיפה |
|-------|------|--------|
| **performance-optimizer** | Core Web Vitals, profiling, bundle optimization | — |
| **seo-specialist** | SEO, GEO, Core Web Vitals, E-E-A-T | Core Web Vitals חוזר |
| **frontend-specialist** | React, UI, ארכיטקטורה | "Optimizing performance (after profiling)" |

**ניתוח חפיפה:**
- **performance-optimizer** ו־**seo-specialist** שניהם מזכירים Core Web Vitals
- performance-optimizer: ממוקד בביצועים טכניים
- seo-specialist: ממוקד ב־ranking ו־AI search visibility

**המלצה:**
1. לשמור על שני סוכנים נפרדים (זוויות שונות)
2. להוסיף הפניות: SEO → performance עבור CWV, performance → SEO עבור השפעה על ranking

---

### 4. Specialists – UI / Frontend

| Agent / Workflow | מטרה |
|------------------|------|
| **frontend-specialist** | React/Next.js, components, ארכיטקטורה |
| **ui-ux-pro-max** | Design intelligence, search.py, סגנונות UI |

**ניתוח:**
- frontend-specialist: מתכנן וכותב קוד
- ui-ux-pro-max: workflow שמחפש סגנונות/צבעים/טקסטורות ואז מפעיל את ה־frontend-specialist

**המלצה:** להשאיר נפרדים – תפקידים שונים; ui-ux-pro-max הוא workflow מעל ה־specialist.

---

### 5. Specialists – Planning ו־Discovery

| Agent | מטרה |
|-------|------|
| **project-planner** | תוכנית פרויקט, task breakdown |
| **explorer-agent** | גילוי קוד, מיפוי ארכיטקטורה |
| **cto** | ארכיטקטורה, החלטות טכנולוגיות |

**ניתוח:**
- **explorer-agent**: גילוי ומיפוי
- **project-planner**: תכנון משימות
- **cto**: החלטות ותכנון ברמת ארכיטקטורה

explorer משמש כ־input ל־project-planner ול־orchestrator. אין חפיפה ישירה שדורשת איחוד.

---

### 6. Workflows vs Specialists

| Workflow | Specialist | יחס |
|----------|------------|-----|
| **plan** | project-planner | plan מפעיל את project-planner |
| **review** | — | מבצע review; יכול להפעיל specialists |
| **peer-review** | — | בודק feedback מודל אחר |
| **document** | documentation-writer | document מפעיל documentation-writer |
| **compliance** | compliance-auditor | compliance מפעיל compliance-auditor |

**המלצה:** אין כפילות – Workflows הם entry points שמפעילים Specialists.

---

### 7. review vs peer-review

| Workflow | תפקיד |
|----------|--------|
| **review** | ביצוע code review מלא |
| **peer-review** | הערכת findings של מודל אחר |

**ניתוח:** תפקידים שונים. peer-review משתמש ב־review כדי לוודא findings. אין צורך באיחוד.

---

### 8. Skills – חפיפות אפשריות

| Skill | מטרה | חפיפה |
|------|------|--------|
| **app-builder** | בניית אפליקציות, תכנון, תיאום סוכנים | משמש את project-planner |
| **plan-writing** | מסגרת לפירוק משימות | משמש project-planner (תכנון אחיד) |
| **brainstorming** | שאלות סוקרטיות, Socratic Gate | משמש planning agents |

**ניתוח:**
- app-builder: skill ל־project-planner
- plan-writing: skill לכל planning
- brainstorming: skill לתקשורת ותכנון

הם משלימים, לא כפולים. אין המלצה לאיחוד.

---

### 9. Content

| Agent | מטרה |
|-------|------|
| **seo-specialist** | SEO כללי |
| **gold-ira-seo-content-writer** | תוכן Gold IRA עם E-E-A-T/GEO |

**ניתוח:** gold-ira הוא specialization נישתי של SEO. אין חפיפה שדורשת איחוד.

---

## טבלת Triggers – בדיקת חפיפה

מ־agent-routing.md:

| Priority | Triggers | Agent |
|----------|----------|-------|
| 4 | security, vulnerability, owasp... | security-auditor |
| 5 | pentest, exploit... | penetration-tester |
| 10 | performance, optimize, speed... | performance-optimizer |
| 11 | seo, meta, core web vitals... | seo-specialist |
| 17 | plan, breakdown, tasks... | project-planner |
| 18 | execution plan, create plan, 🟩🟨🟥 | project-planner (אותו נתיב; ראו `workflows/plan.md`) |
| 20 | brainstorm, explore options | brainstorm |
| 25 | /review | review |
| 33 | peer review | peer-review |
| 32 | ui/ux pro, design system | ui-ux-specialist |

**מסקנה:** Triggers מאפשרים הפרדה ברורה ברוב המקרים.

---

## המלצות סופיות

### לא לאחד (להשאיר נפרדים)

1. **security-auditor** / **penetration-tester** – defensive vs offensive
2. **frontend-specialist** / **ui-ux-specialist** – יישום vs עיצוב/מערכת עיצוב
3. **review** / **peer-review** – review vs ולידציה של review
4. **seo-specialist** / **gold-ira-seo-content-writer** – כללי vs נישה
5. **performance-optimizer** / **seo-specialist** – ביצועים vs SEO (למרות CWV)

### בוצע (2026-04-01)

1. **project-planner** + ~~create-plan~~ — אוחד ל־`/plan` + project-planner עם 🟩🟨🟥 ו־Overall Progress

### שיפורים ללא איחוד

1. **performance-optimizer** ↔ **seo-specialist**: להוסיף הפניות הדדיות ל־Core Web Vitals
2. **documentation-writer**: להבהיר שלא מפעילים אותו אוטומטית, רק במפורש

---

## נספח: מפת סוכנים וסקילס

```
Core (2026-04-01):
├── orchestrator (תיאום)
├── cto (ארכיטקטורה)
└── project-planner (תכנון — כולל 🟩🟨🟥; דרך /plan)

Specialists:
├── debugger
├── devops-engineer
├── penetration-tester
├── security-auditor
├── mobile-developer
├── database-architect
├── backend-specialist
├── frontend-specialist
├── test-engineer
├── performance-optimizer
├── seo-specialist
├── documentation-writer
├── explorer-agent
├── compliance-auditor
├── jules
├── technical-educator
└── ui-ux-specialist

Content:
└── gold-ira-seo-content-writer

Games:
└── game-developer

Workflows (2026-04-01): brainstorm, compliance, create, debug, deploy,
document, enhance, execute, finishing-branch, orchestrate, peer-review,
plan, prd, project-deep-audit, review, status (כולל dev server / preview alias), test
```

---

**סוף הדוח**
