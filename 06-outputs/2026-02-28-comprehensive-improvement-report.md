# דוח שיפור מקיף — השוואה לרפזיטוריז חיצוניים

**תאריך:** 2026-02-28  
**מקורות:** code-review-expert, Superpowers, DeerFlow, awesome-llm-apps, Claude Code, Agent of Empires, TradingAgents

---

## חלק א׳: מיפוי — מה קיים אצלנו לעומת החוץ

### 1. השוואת Skills (Maestro vs חיצוני)

| Skill חיצוני | קובץ אצלנו | סטטוס |
|--------------|------------|--------|
| **code-review-expert** (solid, security, quality, removal) | `code-review-checklist/` + 4 references | ✅ יושם |
| **brainstorming** (Superpowers) | `brainstorming/brainstorming.md`, `dynamic-questioning.md` | ✅ יש |
| **writing-plans** (Superpowers) | `plan-writing/plan-writing.md` | ✅ יש |
| **systematic-debugging** (Superpowers) | `systematic-debugging/systematic-debugging.md` | ✅ יש |
| **test-driven-development** (Superpowers) | `tdd-workflow/tdd-workflow.md` | ✅ יש |
| **dispatching-parallel-agents** (Superpowers) | `parallel-agents/parallel-agents.md` | ✅ יש |
| **writing-skills** (Superpowers) | `skill-template.md` | ✅ יש |
| **frontend-design** (DeerFlow) | `frontend-design/` (9 קבצים) | ✅ יש — מפורט יותר |
| **web-design-guidelines** (DeerFlow) | `web-design-guidelines/web-design-guidelines.md` | ✅ יש |
| **receiving-code-review** (Superpowers) | — | ❌ חסר |
| **using-git-worktrees** (Superpowers) | — | ❌ חסר |
| **deep-research** (DeerFlow) | explorer-agent + brainstorming | ⚠️ חלקי — אין methodology מפורט |
| **find-skills** (DeerFlow) | `intelligent-routing/` | ⚠️ שונה — routing לסוכנים, לא חיפוש skills |
| **chart-visualization** (DeerFlow) | ui-ux-specialist / skill ui-ux-pro-max מזכיר charts | ❌ חסר skill ייעודי |
| **skill-creator** (DeerFlow) | `skill-template.md` | ⚠️ DeerFlow מפורט יותר — Progressive Disclosure |

### 2. השוואת Workflows

| Workflow חיצוני | אצלנו | סטטוס |
|-----------------|-------|--------|
| **finishing-a-development-branch** | `finishing-branch.md` | ✅ יושם |
| **executing-plans** | `execute.md` | ✅ יש + verification |
| **requesting-code-review** | `review.md` | ✅ יש (7 שלבים) |
| **receiving-code-review** | `peer-review.md` | ⚠️ peer-review בודק findings, לא מספק methodology להגיב |

---

## חלק ב׳: DeerFlow — ניתוח מעמיק

### מהו DeerFlow

DeerFlow (bytedance) הוא **Super Agent Harness** — runtime שמספק:
- **Skills** — מודולים נטענים באופן פרוגרסיבי
- **Sub-agents** — spawn עם context מבודד
- **Sandbox** — Docker עם filesystem מלא
- **Memory** — זכרון בין sessions
- **Context Engineering** — summarization, compression

**הבדל מהותי:** DeerFlow = פלטפורמה (LangGraph, backend, UI). Maestro = vault-based, Cursor-integrated.

### Skills ב-DeerFlow — מה אפשר לאמץ

#### 1. deep-research (גבוהה ערך)

**מה יש שם:**
- 4 שלבים: Broad Exploration → Deep Dive → Diversity & Validation → Synthesis Check
- חובה: web_fetch למקורות מלאים, לא רק snippets
- טבלת Information Types: Facts, Examples, Expert Opinions, Trends, Comparisons, Challenges
- Quality bar: 3–5 זוויות, נתונים קונקרטיים, דוגמאות, מומחים

**מה חסר אצלנו:**
- explorer-agent עוסק ב-codebase, לא ב-web research
- brainstorming עוסק ב-design exploration
- **אין** skill ל-web research מעמיק לפני יצירת תוכן

**המלצה:** ליצור `skills/deep-research/deep-research.md` — methodology לפני content generation, reports, documentation.

#### 2. find-skills (ערך בינוני)

**מה יש שם:**
- `npx skills find [query]` — חיפוש skills ב-ecosystem (skills.sh)
- התאמה: "how do I do X" → חיפוש skill

**מה אצלנו:**
- intelligent-routing — בוחר **agent** לפי intent
- אין logic ל"איזה skill לקרוא עבור משימה"

**המלצה:** intelligent-routing כבר מפנה לסוכנים. find-skills רלוונטי אם Maestro משתמש ב-external skills (npx skills). אם לא — נמוך עדיפות.

#### 3. chart-visualization (ערך בינוני–גבוה)

**מה יש שם:**
- 26 סוגי גרפים: line, area, bar, pie, scatter, sankey, treemap, radar, funnel...
- Decision tree: Time Series → line/area, Comparisons → bar/column, Part-to-Whole → pie/treemap
- Script `generate.js` עם JSON payload
- References לכל chart type

**מה אצלנו:**
- ui-ux-specialist (skill ui-ux-pro-max) מזכיר `chart` domain לחיפוש
- אין skill ייעודי לבחירת גרפים ו-best practices

**המלצה:** skill `chart-visualization` — decision tree לבחירת chart type, ספריות מומלצות (Recharts, Chart.js), anti-patterns. בלי script — Maestro רץ ב-Cursor, לא sandbox.

#### 4. skill-creator (ערך גבוה ל-design)

**מה יש שם (מעבר ל-skill-template שלנו):**
- **Progressive Disclosure** — 3 רמות: Metadata (~100 words) → SKILL.md (<5k) → References (as needed)
- **Bundled Resources** — scripts/, references/, assets/ — מתי כל אחד
- **Conditional details** — "Show basic, link to advanced"
- **Domain-specific organization** — reference/finance.md, reference/sales.md
- **init_skill.py**, **package_skill.py** — automation
- **What NOT to include** — README, INSTALLATION_GUIDE, CHANGELOG ב-skill

**מה אצלנו:**
- skill-template.md — בסיסי
- חלק מהעקרונות כבר מיושמים (references ב-code-review-checklist)

**המלצה:** להרחיב skill-template עם:
- Progressive Disclosure
- מתי scripts vs references vs assets
- מבנה references לפי domain
- "מה לא לכלול"

#### 5. Skills נוספים ב-DeerFlow (נמוך עדיפות)

| Skill | תיאור | רלוונטיות |
|-------|--------|-----------|
| report-generation | יצירת דוחות | niche |
| slide-creation, ppt-generation | מצגות | niche |
| image-generation, video-generation | מדיה | יש Gemini skill |
| podcast-generation | פודקסטים | niche |
| consulting-analysis, data-analysis | אנליזה | לא core |
| github-deep-research | מחקר GitHub | שימושי אם עובדים עם GitHub |
| vercel-deploy-claimable | deploy Vercel | devops מכסה |
| surprise-me | אקראי | לא |

---

## חלק ג׳: Superpowers — מה עוד חסר

### 1. receiving-code-review

**תוכן עיקרי:**
- Verify before implementing — לא לבצע באופן עיוור
- No performative agreement — "You're absolutely right!" = אסור
- Pushback עם technical reasoning
- Source-specific: human partner (trusted) vs external reviewer (skeptical)
- YAGNI check — "זה endpoint לא נקרא. להסיר?"
- Implementation order: Blocking → Simple → Complex

**איפה להוסיף:**
- הרחבת `peer-review.md` או skill נפרד `receiving-code-review`
- peer-review כרגע: ולידציה של feedback. חסר: **איך להגיב** — verify, pushback, order

**המלצה:** skill `receiving-code-review` בתוך `code-review-checklist/` או כ-skill עצמאי. peer-review יטען אותו.

### 2. using-git-worktrees

**תוכן עיקרי:**
- Directory selection: .worktrees > worktrees > CLAUDE.md > Ask
- Safety: `git check-ignore` לפני יצירת worktree — חייב להיות ב-.gitignore
- Creation: `git worktree add .worktrees/feature-x -b feature-x`
- Project setup: npm install, cargo build, pip install — auto-detect
- Baseline: run tests, report if fail
- Integration: brainstorming (phase 4), executing-plans — REQUIRED before execute

**רלוונטיות:**
- שימושי עבור feature work מבודד
- לפני execute — worktree = branch מבודד

**המלצה:** skill `using-git-worktrees` — ללא תלות ב-Superpowers. Maestro-style.

---

## חלק ד׳: השוואת skill-template ל-DeerFlow skill-creator

| נושא | skill-template (שלנו) | DeerFlow skill-creator |
|------|----------------------|-------------------------|
| Progressive Disclosure | לא מפורט | 3 רמות: metadata → body → resources |
| References | מזכיר | מתי references vs scripts vs assets |
| Conditional loading | לא | "Show basic, link to advanced" |
| Domain organization | לא | reference/finance.md, reference/sales.md |
| What NOT to include | לא | README, CHANGELOG, וכו' |
| Init/Package scripts | לא | init_skill.py, package_skill.py |
| Frontmatter guidance | בסיסי | description = primary trigger, include "when" |

**המלצה:** להעשיר skill-template עם העקרונות מ-DeerFlow (ללא scripts — Maestro לא משתמש ב-.skill packaging).

---

## חלק ה׳: תוכנית יישום מומלצת

### שלב 1 — עדיפות גבוהה

| # | משימה | מקור | פעולה |
|---|-------|------|--------|
| 1 | receiving-code-review | Superpowers | skill חדש או הרחבת peer-review |
| 2 | using-git-worktrees | Superpowers | skill חדש |
| 3 | העשרת skill-template | DeerFlow | Progressive Disclosure, what NOT to include |

### שלב 2 — עדיפות בינונית

| # | משימה | מקור | פעולה |
|---|-------|------|--------|
| 4 | deep-research | DeerFlow | skill — methodology ל-web research לפני content |
| 5 | chart-visualization | DeerFlow | skill — decision tree, chart types, ספריות |
| 6 | הרחבת intelligent-routing | — | הוספת "skill suggestion" כשחסר agent מתאים |

### שלב 3 — עדיפות נמוכה

| # | משימה | מקור | פעולה |
|---|-------|------|--------|
| 7 | bug-report workflow | Claude Code | workflow — מסמך מוכן ל-GitHub issue |
| 8 | 04-knowledge reference | awesome-llm-apps | קישור + תיאור קצר |
| 9 | github-deep-research | DeerFlow | אופציונלי — אם עובדים הרבה עם GitHub |

---

## חלק ו׳: מבנה מוצע לקבצים חדשים

```
03-agents/skills/
├── receiving-code-review/          ← חדש (או בתוך code-review-checklist)
│   └── receiving-code-review.md
├── using-git-worktrees/             ← חדש
│   └── using-git-worktrees.md
├── deep-research/                   ← חדש
│   └── deep-research.md
├── chart-visualization/             ← חדש
│   ├── chart-visualization.md
│   └── chart-types-reference.md    (אופציונלי)
├── skill-template.md               ← עדכון
└── ...
```

---

## חלק ז׳: TradingAgents — Multi-Agent Financial Trading Framework

### מהו TradingAgents

[TradingAgents](https://github.com/TauricResearch/TradingAgents) (TauricResearch) — פריימוורק multi-agent למסחר פיננסי מבוסס LLM. ~31k stars. מחקרי (arXiv), לא ייעוץ השקעות.

### ארכיטקטורה — מה יש שם

**צוותים מומחים (Role Decomposition):**

| צוות | תפקיד |
|------|--------|
| **Analyst Team** | Fundamentals, Sentiment, News, Technical — כל אחד תחום משלו |
| **Researcher Team** | Bullish + Bearish — דיון מובנה לפני החלטה |
| **Trader** | מבנה דוחות מ-analysts + researchers, מחליט על timing וגודל |
| **Risk Management** | הערכת סיכון (volatility, liquidity) |
| **Portfolio Manager** | אישור/דחייה סופית — רק אחרי אישור → ביצוע |

**טכנולוגיה:** LangGraph, תמיכה במספר LLM providers (OpenAI, Google, Anthropic, xAI, OpenRouter, Ollama).

### מה אפשר לאמץ ל-Maestro

| דפוס | תיאור | ישים? |
|------|--------|-------|
| **Role Decomposition** | פירוק משימה לצוותים מומחים (analysts → researchers → decision) | ✅ orchestrator כבר ממפה specialists |
| **Debate / Red Team** | Bullish vs Bearish — דיון לפני החלטה | ✅ red-team-tactics skill קיים |
| **Approval Workflow** | Portfolio Manager מאשר/דוחה — gate לפני ביצוע | ⚠️ אפשר להזכיר ב-orchestrate — "gate" לפני execute |
| **Risk Layer** | שכבת סיכון נפרדת לפני אישור | niche — רלוונטי ל-decision workflows |
| **Multi-Provider LLM** | תמיכה במספר providers | Maestro רץ ב-Cursor — provider בידי הפלטפורמה |

### המלצות

1. **04-knowledge** — להוסיף רשומה: TradingAgents כרפרנס ל-multi-agent role decomposition ו-debate patterns. [Paper (arXiv)](https://arxiv.org/abs/2412.20138).
2. **orchestrator** — להזכיר דפוס "analysts → researchers → approver" כשמתכננים workflows מורכבים (לא רק trading).
3. **parallel-agents** — דוגמה: analyst team = specialists מקבילים; researcher team = debate. כבר מכסים.
4. **לא skill חדש** — TradingAgents הוא domain-specific (finance). הדפוסים כלליים — Orchestrator + red-team מכסים.

### רלוונטיות

- **גבוהה** — דפוסי multi-agent (decomposition, debate, approval)
- **נמוכה** — הקוד עצמו (Python, LangGraph) — Maestro לא מיישם runtime
- **רפרנס** — 04-knowledge

---

## חלק ח׳: DeerFlow — רעיונות ארכיטקטוריים (ללא יישום ישיר)

| רעיון | תיאור | ישים ל-Maestro? |
|-------|--------|-----------------|
| **Progressive skill loading** | טעינת skill רק כש-trigger | ✅ agent-routing עושה דומה |
| **Sub-agent context isolation** | כל sub-agent עם context נפרד | ⚠️ Cursor Agent tool — תלוי בפלטפורמה |
| **Sandbox execution** | Docker עם filesystem | ❌ Maestro רץ בתוך Cursor, לא sandbox |
| **Long-term memory** | זכרון בין sessions | ❌ לא built-in ב-Cursor |
| **Context summarization** | דחיסת תוצאות ביניים | רעיון — אפשר להזכיר ב-orchestrator |
| **MCP integration** | DeerFlow תומך MCP | ✅ Maestro כבר משתמש ב-MCP |

---

## סיכום מנהלים

1. **מה יושם:** code-review (7 שלבים + checklists), finishing-branch, verification ב-execute.
2. **מה חסר ועדיף להוסיף:**
   - receiving-code-review (הגיב נכון ל-feedback)
   - using-git-worktrees (עבודה מבודדת)
   - deep-research (מחקר web לפני תוכן)
   - chart-visualization (dashboards)
   - העשרת skill-template (Progressive Disclosure)
3. **DeerFlow:** מקור עשיר ל-methodology (deep-research, skill-creator, chart). הארכיטקטורה (sandbox, memory) לא ישימה ישירות.
4. **מניעת כפילויות:** כל addition — skill או הרחבת קיים. אין סוכנים חדשים.
5. **TradingAgents:** מקור ל-multi-agent patterns (decomposition, debate, approval). רפרנס ב-04-knowledge, הזכרה ב-orchestrator.

---

## קישורים

- [DeerFlow](https://github.com/bytedance/deer-flow) — deerflow.tech
- [Superpowers](https://github.com/obra/superpowers)
- [code-review-expert](https://github.com/sanyuan0704/code-review-expert)
- [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps)
- [TradingAgents](https://github.com/TauricResearch/TradingAgents) — multi-agent financial trading (TauricResearch, ~31k ⭐), [arXiv](https://arxiv.org/abs/2412.20138)
