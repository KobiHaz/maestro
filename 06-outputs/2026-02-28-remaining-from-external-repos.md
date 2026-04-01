# מה עוד יש ברפוזיטוריז — סקירה מלאה

**תאריך:** 2026-02-28  
**מה כבר יישמנו:** code-review-expert (checklists + workflow), finishing-branch, verification ב־execute

---

## 1. Superpowers (obra/superpowers)

**מה יש שם — 14 Skills:**

| Skill | תיאור | יש אצלנו? |
|-------|--------|-----------|
| **brainstorming** | שאלות סוקרטיות, design בחתיכות | ✅ brainstorming skill |
| **writing-plans** | פירוק משימות, 2–5 דקות | ✅ plan-writing |
| **executing-plans** | ביצוע עם checkpoints | ✅ execute workflow |
| **finishing-a-development-branch** | Merge/PR/cleanup | ✅ finishing-branch |
| **systematic-debugging** | 4 שלבים, root cause | ✅ systematic-debugging |
| **test-driven-development** | RED-GREEN-REFACTOR | ✅ tdd-workflow |
| **verification-before-completion** | לוודא לפני "done" | ✅ נוסף ל־execute |
| **dispatching-parallel-agents** | subagents במקביל | ✅ parallel-agents |
| **requesting-code-review** | checklist לפני review | חלקי — יש ב־review |
| **receiving-code-review** | איך להגיב ל־feedback | ❌ חסר |
| **using-git-worktrees** | worktrees מבודדים | ❌ חסר |
| **subagent-driven-development** | subagent לכל task | חלקי — orchestrator |
| **using-superpowers** | intro ל־skills | לא רלוונטי |
| **writing-skills** | יצירת skills חדשים | ✅ skill-template |

### מה כדאי להוסיף

- **receiving-code-review** — איך להגיב ל־code review: Verify לפני implementation, no performative agreement, pushback עם reasoning. להרחיב את peer-review או skill נפרד.
- **using-git-worktrees** — יצירת worktrees מבודדים (`.worktrees/`), verify ignored, baseline tests. שימושי לפני execute כשעובדים על feature מבודד.

---

## 2. DeerFlow (bytedance/deer-flow)

**מה יש שם — 15 Skills:**

| Skill | תיאור | רלוונטי ל-Maestro? |
|-------|--------|---------------------|
| **deep-research** | מחקר מעמיק | explorer + brainstorm מכסים |
| **report-generation** | יצירת דוחות | אולי — לא בדקנו |
| **slide-creation** | מצגות | לא core |
| **web-page** | יצירת דפי web | app-builder מכסה |
| **image-generation** | יצירת תמונות | לא core (יש Gemini skill) |
| **chart-visualization** | גרפים וויזואליזציה | שימושי — dashboards |
| **data-analysis** | ניתוח נתונים | לא core |
| **consulting-analysis** | ייעוץ/אנליזה | לא core |
| **find-skills** | חיפוש skills לפי משימה | שימושי — intelligent-routing |
| **frontend-design** | עיצוב frontend | ✅ frontend-design |
| **web-design-guidelines** | הנחיות UI | ✅ web-design-guidelines |
| **github-deep-research** | מחקר GitHub | שימושי — research |
| **podcast-generation** | יצירת פודקסטים | niche |
| **ppt-generation** | מצגות PowerPoint | niche |
| **video-generation** | יצירת וידאו | niche |
| **skill-creator** | יצירת skills | ✅ skill-template |
| **surprise-me** | פיצ'ר אקראי | לא |
| **vercel-deploy-claimable** | deploy ל־Vercel | devops מכסה |

### מה כדאי להוסיף

- **chart-visualization** — בחירת סוגי גרפים, ספריות (Chart.js, Recharts), best practices ל־dashboards.
- **find-skills** — logic: "איזה skill לקרוא עבור X?" — אפשר להרחיב את intelligent-routing.
- **deep-research** — אולי workflow ל־research מעמיק (explorer + synthesis).

---

## 3. code-review-expert (sanyuan0704)

**מה יישמנו:** solid, security, code-quality, removal-plan + workflow 7 שלבים.

**מה נשאר (אם בכלל):**

- `agents/agent.yaml` — הגדרת agent ל־Claude Code. לא רלוונטי ל-Maestro (מבנה שונה).
- Inline comments format `::code-comment{...}` — תלוי בפלטפורמה. Cursor עשוי לא לתמוך.

---

## 4. awesome-llm-apps (Shubhamsaboo)

**סוג:** אינדקס/רשימה — לא skill אחד.

**קטגוריות:**

- Starter agents: Blog→Podcast, Data Analysis, Travel, Research
- Advanced: Deep Research, VC Due Diligence, Consultant, System Architect, Financial Coach
- Multi-agent teams: Finance, Legal, Recruitment, Real Estate, Game Design
- Voice agents, MCP agents (Browser, GitHub, Notion)
- RAG: Agentic RAG, Hybrid Search, Vision RAG, Knowledge Graph
- Memory: ArXiv, Travel, Personalized Memory
- Chat with X: GitHub, Gmail, PDF, YouTube
- Optimization: Token optimization, Context compression
- Fine-tuning: Gemma, Llama

**שימוש:** רפרנס ב־04-knowledge — קישור לפרויקטים לדוגמה. לא skills ישירים.

---

## 5. Claude Code (anthropics/claude-code)

**מה יש:** CLI tool, plugins, commands.

- `.claude/commands` — slash commands
- `plugins/` — הרחבות
- `/bug` — דיווח באגים

**רלוונטיות:** Maestro רץ ב־Cursor, לא Claude Code. מבנה שונה.  
**רעיון:** workflow "bug report" — ליצור מסמך מוכן ל־GitHub issue. אופציונלי.

---

## 6. Agent of Empires (njbrake)

**מה יש:** Session manager — tmux, worktrees, TUI.

**רלוונטיות:** כלי חיצוני שרץ agents. Maestro יכול לרוץ מתוכו. תיעוד אינטגרציה אפשרי, לא שינוי ב-Maestro.

---

## סיכום — מה כדאי להוסיף

| עדיפות | פריט | מקור | פעולה |
|--------|------|------|--------|
| גבוהה | receiving-code-review | Superpowers | skill או הרחבת peer-review |
| גבוהה | using-git-worktrees | Superpowers | skill — worktrees מבודדים |
| בינונית | chart-visualization | DeerFlow | skill — dashboards, גרפים |
| בינונית | find-skills logic | DeerFlow | הרחבת intelligent-routing |
| נמוכה | deep-research workflow | DeerFlow | אופציונלי |
| נמוכה | bug-report | Claude Code | workflow אופציונלי |
| רפרנס | awesome-llm-apps | — | קישור ב־04-knowledge |
