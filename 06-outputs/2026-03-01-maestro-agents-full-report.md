# Maestro Agents — דוח מלא על כל הסוכנים והאפשרויות

> **תאריך:** 1 במרץ 2026  
> **מטרה:** מיפוי מלא של כל הסוכנים בכספת + מה אפשר לעשות איתם

> **עדכון 2026-04-01:** מספרים וטבלאות למטה **עודכנו** למבנה הנוכחי — **3** core, **17** specialists, **17** workflows; אין `create-plan` נפרד (תכנון דרך `/plan` + `project-planner`); `preview` מוזג ל־`/status`; UI/UX ולימוד → specialists. מקור אמת: `03-agents/agent-routing.md`.

---

## TL;DR

בכספת Maestro יש **3 סוכני ליבה**, **17 מומחים**, **17 workflow**-ים, ו־**1 סוכן תוכן**. כולם נתמכים על ידי **50+ skills**. אין "הרצה אוטומטית" — סוכנים מופעלים לפי trigger keywords או slash commands.

**לגבי source6681:** התוכנית הקיימת `2026-02-27-source6681-remaining-tasks` מזהה משימות פתוחות — אפשר להתקדם דרך `/execute`, `/review`, `/finishing-branch`, ועוד.

---

## 1. סוכני ליבה (Core)

| סוכן | תיאור | מתי להפעיל |
|------|--------|------------|
| **orchestrator** | קואורדינציה של מספר סוכנים (מינימום 3) | משימות מורכבות, אבטחה + backend + frontend + tests |
| **project-planner** | פירוק משימות, תוכניות עם 🟩🟨🟥, dependency graph | `/plan`, לפני orchestration, תכנון פיצ'רים |
| **cto** | ארכיטקטורה, החלטות tech, code review | "architecture", "stack", "tech decisions" |

**מה אפשר לעשות:**
- **orchestrator:** להריץ ביחד security-auditor + backend-specialist + test-engineer + frontend-specialist
- **project-planner:** ליצור `docs/plans/{task-slug}.md` לפני כל orchestration; תוכניות עם **Overall Progress** ו־🟩🟨🟥 על משימות (ראו `workflows/plan.md`)
- **cto:** לקבל החלטות ארכיטקטוריות, שאלות הבהרה, review ברמת CTO

---

## 2. מומחים (Specialists) — 17 סוכנים

| סוכן | תחום | Triggers | מה אפשר לעשות |
|------|------|----------|----------------|
| **backend-specialist** | API, server | backend, api, endpoint, auth | Node.js, Python, Edge, API design |
| **compliance-auditor** | תאימות רגולטורית | healthcare, fda, legitscript | בדיקות תאימות |
| **debugger** | באגים, root cause | bug, error, crash, fix, debug | Reproduce → Isolate → Understand → Fix & Verify |
| **database-architect** | SQL, schema, migrations | database, sql, postgres, migration | סכמות, אינדקסים, migrations |
| **devops-engineer** | deploy, CI/CD | deploy, pm2, ssh, release, ci/cd | Deploy, rollback, תשתית |
| **documentation-writer** | Docs, README | readme, api docs, changelog | תיעוד, README, CHANGELOG |
| **explorer-agent** | גילוי קוד | codebase, discovery, audit | מיפוי codebase, תלותיות |
| **frontend-specialist** | React, UI, CSS | component, react, tailwind, frontend | Components, Tailwind, Next.js, React |
| **jules** | סוכן Google Jules | jules, background agent | משימות רקע / Jules |
| **mobile-developer** | React Native, Flutter | mobile, ios, android, expo | אפליקציות מובייל (לא web) |
| **penetration-tester** | pentest, red team | pentest, exploit, hack, pwn | בדיקות אבטחה התקפיות |
| **performance-optimizer** | Performance | performance, slow, lighthouse | Profiling, אופטימיזציה |
| **security-auditor** | אבטחה, OWASP | security, vulnerability, xss, auth | סקירות אבטחה, אימות OWASP Top 10 |
| **seo-specialist** | SEO, meta | seo, core web vitals, meta | Meta tags, SEO, analytics |
| **technical-educator** | הסבר, לימוד | explain, teach, למה | הסברים מובנים, למידה |
| **test-engineer** | Tests, coverage | test, jest, playwright, e2e | Unit, E2E, TDD, coverage |
| **ui-ux-specialist** | עיצוב UI/UX, design system | ui, ux, design system | עיצוב מוצר, נגישות, skill `ui-ux-pro-max` |

**מה אפשר לעשות:**
- **לכל פרויקט:** explorer → project-planner → specialists לפי תחום
- **source6681:** frontend-specialist, backend-specialist (Supabase), test-engineer, security-auditor, performance-optimizer

---

## 3. Workflows — 17 workflows

| Workflow | Slash | תיאור | מה אפשר לעשות |
|----------|-------|--------|----------------|
| **brainstorm** | `/brainstorm` | חקר רעיונות | 3+ אפשרויות, pros/cons, המלצה |
| **compliance** | — | compliance scan | Healthcare compliance |
| **create** | `/create` | אפליקציה חדשה | יצירת אפל חדש |
| **debug** | `/debug` | חקירת באגים | Gather → Hypotheses → Investigate → Fix |
| **deploy** | `/deploy` | פריסה ל-production | Release, rollback |
| **document** | `/document` | עדכון תיעוד | Post-execution docs |
| **enhance** | `/enhance` | הוספת פיצ'ר | Add feature |
| **execute** | `/execute` | מימוש לפי PLAN | ביצוע צעד־אחר־צעד, עדכון 🟩🟨🟥 |
| **finishing-branch** | `/finishing-branch` | סיום branch, merge/PR | Verify → Document → Merge/PR/Discard |
| **orchestrate** | — | תזמור | תזמור סוכנים (דרך orchestrator) |
| **peer-review** | — | ביקורת עמיתים | Peer review |
| **plan** | `/plan` | תכנון | תכנון + `project-planner` |
| **prd** | — | מסמך דרישות מוצר | PRD לפני פיתוח |
| **project-deep-audit** | — | סקירה מקיפה לפרויקט | audit מלא לפי workflow |
| **review** | `/review` | Code review מלא | 7 steps: Scope → SOLID → Removal → Security → Quality → Output |
| **status** | `/status` | סטטוס + dev server | התקדמות; `start` / `stop` / `check` / `preview` (alias) |
| **test** | `/test` | הרצת בדיקות | Run tests |

**מה אפשר לעשות:**
- **בכל סיום משימות:** `/finishing-branch` — Verify → Document → Merge/PR
- **לפני merge:** `/review` — code review מלא
- **לפני פיתוח:** `/brainstorm` או `/plan`
- **dev server:** `/status` (לא workflow נפרד `preview`)

---

## 4. תוכן ומשחקים

| סוכן | תחום | מה אפשר לעשות |
|------|------|----------------|
| **gold-ira-seo-content-writer** | Gold IRA, E-E-A-T, GEO | תוכן SEO לתחום Gold IRA |
| **game-developer** | Unity, Godot, Phaser | משחקים (ארכיון — אין צורך כרגע) |

---

## 5. Skills — 50+ skills

Skills הם "כישורים" שסוכנים יכולים לטעון. דוגמאות:

- **clean-code** — קונבנציות, איכות קוד
- **architecture** — ארכיטקטורה
- **vulnerability-scanner** — סקירת פגיעויות
- **plan-writing** — כתיבת plans
- **brainstorming** — סיעור מוחות
- **nextjs-react-expert** — Next.js/React
- **frontend-design** — עיצוב frontend
- **testing-patterns** — תבניות בדיקות
- **systematic-debugging** — דיבאג שיטתי
- **api-patterns** — תבניות API
- **database-design** — עיצוב DB

Skills כוללים גם scripts: `security_scan.py`, `lint_runner.py`, `lighthouse_audit.py`, `playwright_runner.py`, ועוד.

---

## 6. source6681 — מה לעשות עם הסוכנים

### מצב נוכחי (מתוך 2026-02-27-source6681-remaining-tasks)

| תחום | משימות פתוחות | סוכן מומלץ |
|------|--------------|------------|
| **Vercel Best Practices** | 6 משימות (BRAND_PATTERNS, Analytics, GA, content-visibility, wishlist) | frontend-specialist + execute |
| **Product & UX** | Checkout flow, eBay API | backend-specialist + frontend-specialist |
| **Performance** | Infinite scroll, server-side filters, skeletons, Error boundaries, URL filters | frontend-specialist + performance-optimizer |
| **Security** | Connection pooling, rate limiting | security-auditor + backend-specialist |
| **Testing** | Unit tests (formatPrice, getProductDisplayPrice), check-browser admin | test-engineer |

### זרימת עבודה מומלצת ל-source6681

1. **Vercel Best Practices (1–2 שעות)**  
   - `/execute` על `docs/plans/2026-02-28-vercel-react-best-practices.md`  
   - או: `/plan` (project-planner) → `/execute` → `/finishing-branch`

2. **ביקורת קוד**  
   - `/review` — לפני merge

3. **Performance**  
   - performance-optimizer + frontend-specialist

4. **Security**  
   - security-auditor — connection pooling, rate limiting

5. **Testing**  
   - test-engineer — unit tests, הרחבת check-browser

---

## 7. טריגרים — איך להפעיל סוכנים

### Trigger Matrix (מתוך agent-routing)

המערכת בודקת את ההודעה שלך לפי Priority; **ההתאמה הראשונה מנצחת**:

- **1** bug, error, crash → debugger
- **4** security, xss, auth → security-auditor
- **8** component, react, tailwind → frontend-specialist
- **9** test, jest, playwright → test-engineer
- **16** architecture, stack → cto
- **19** orchestrate, 3+ agents → orchestrator
- **22** /execute → execute workflow
- **25** /review → review workflow
- **36** /finishing-branch → finishing-branch

### Slash Commands

| פקודה | סוכן/Workflow |
|-------|----------------|
| `/execute` | execute |
| `/review` | review |
| `/brainstorm` | brainstorm |
| `/debug` | debug |
| `/deploy` | deploy |
| `/document` | document |
| `/plan` | plan |
| `/finishing-branch` | finishing-branch |

---

## 8. סיכום — מה אפשר לעשות עכשיו

### אפשרויות מיידיות ל-source6681

1. **להריץ Vercel Best Practices**  
   - `orchestrate Vercel React best practices for source6681`  
   - או: `/execute` עם plan קיים

2. **לעשות code review**  
   - `/review`

3. **לסיים branch**  
   - `/finishing-branch`

4. **לחקור באג**  
   - `/debug [תיאור הבאג]`

5. **לסדר תוכנית**  
   - `/plan` + `project-planner` → `docs/plans/` חדש

6. **לבנות פיצ'ר חדש**  
   - brainstorm → plan → execute → review → finishing-branch

### Common Flows (מתוך agent-routing)

| תרחיש | סדר מומלץ |
|-------|-----------|
| פיצ'ר חדש | `/plan` (project-planner) → `/execute` → `/finishing-branch` |
| באג | debugger → test-engineer |
| סקירת אבטחה | security-auditor → (אופציונלי) penetration-tester |
| ארכיטקטורה | cto / project-planner |
| Deploy | devops-engineer → deploy workflow |

---

## 9. הערות

1. **אין "הרצת כל הסוכנים"**  
   הסוכנים לא רצים כ־batch. הם מופעלים לפי המשימה — trigger או slash command.

2. **Orchestrator דורש PLAN**  
   לפני invoke של specialists, חייב קובץ plan ב-`docs/plans/`.

3. **Routing לפי סוג פרויקט**  
   - **WEB** → frontend-specialist (לא mobile-developer)  
   - **MOBILE** → mobile-developer (לא frontend-specialist)  
   source6681 = WEB.

4. **Maestro = מקור אמת**  
   כל עדכון ל-agents, workflows, skills — רק ב-vault.

---

*דוח זה נוצר מתוך סריקת Maestro vault ב־1 במרץ 2026.*
