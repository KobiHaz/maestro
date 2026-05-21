# Maestro Improvement Plan
**Date:** 2026-04-16  
**Agent:** project-planner (`03-agents/workflows/plan.md`)  
**Scope:** שיפור מבני של Maestro vault — HR routing, model staffing, status protocol, ניקיון תפעולי

---

## Overall Progress: 0%

---

## Context & Vision

**מה אנחנו בונים:** Maestro כ-second brain + HR system לagents.  
**השראה:** Superpowers (model staffing, status protocol, context isolation) + BMAD (scale-adaptive planning).  
**מה לא משנים:** המבנה הבסיסי (00-07 folders), 04-knowledge, plans-and-tasks pattern — אלה עובדים.

---

## Phases

---

### Phase 1 — Operational Cleanup 🟥
**מטרה:** לנקות את מה שמצטבר ולא בשימוש. אין סיכון, רק order.

#### Tasks

**1.1** — נקות `docs/plans/` 🟥  
**Agent:** `03-agents/specialists/explorer-agent.md`  
**עבודה:**
- לכל קובץ ישן שם — לבדוק האם הידע שלו כבר ב-`04-knowledge/` או `plans-and-tasks.md`
- אם כן → מחק
- אם לא → העבר תחילה, אז מחק
- קבצים לבדוק: `2026-02-27-cms-*`, `2026-02-27-crm-*`, `2026-03-01-smart-volume-*`, `2026-03-06-gold-ira-*`, `casino-funnels-post-audit.md`

**1.2** — נקות `06-outputs/` 🟥  
**Agent:** `03-agents/specialists/explorer-agent.md`  
**עבודה:**
- להסיר קבצים שאינם outputs: `package.json`, `package-lock.json`, `.mjs` scripts, `.csv` files, `.code-workspace`
- לבדוק לאן כל אחד שייך (אם בכלל) לפני מחיקה
- outputs עם תאריך — נשארים (זה הarchivals הנכונים)

**1.3** — כתוב brief רציני ל-Maestro עצמו 🟥  
**Agent:** project-planner (manually)  
**עבודה:** להרחיב את `02-projects/maestro/project.maestro.md` — חזון, goals, open decisions, roadmap בסיסי. כרגע זה 10 שורות בלבד.

---

### Phase 2 — HR Routing Redesign 🟥
**מטרה:** להפוך את agent-routing מlookup table ל-HR system עם intake triage.

#### Core concept

```
Task → [Intake Triage] → [Staffing Decision] → [Dispatch]
              ↓                   ↓
         complexity           who + how many
         risk level           model level
         domain count         sequential / parallel
```

#### Tasks

**2.1** — הוסף Intake Triage כ-mandatory first step 🟥  
**Agent:** `03-agents/workflows/plan.md` + `03-agents/specialists/documentation-writer.md`  
**עבודה:** להוסיף ל-`agent-routing.md` סעיף חדש **"Intake Assessment"** לפני כל routing:

```markdown
## Intake Assessment (FIRST STEP — mandatory)

Before routing any task, answer:

| Question | Simple | Medium | Complex | Critical |
|---|---|---|---|---|
| Domains touched | 1 | 1-2 | 3+ | any |
| Risk if wrong | low | medium | high | irreversible |
| Requirements clear? | yes | mostly | no | — |
| Files affected | 1-3 | 3-10 | 10+ | — |

→ Simple: skip to direct agent dispatch (no plan file needed)  
→ Medium: plan in plans-and-tasks.md, 1-2 agents  
→ Complex: docs/plans/{slug}.md, orchestrator, full cycle  
→ Critical: full cycle + explicit human sign-off before execute
```

**2.2** — פצל את `agent-routing.md` 🟥  
**Agent:** `03-agents/specialists/documentation-writer.md`  
**עבודה:** agent-routing.md הוא 420 שורות עם 4 דברים שונים. לפצל:

| קובץ חדש | תוכן |
|---|---|
| `agent-routing.md` | Intake Assessment + routing catalog + trigger matrix בלבד (~150 שורות) |
| `03-agents/workflows/orchestrate.md` | Orchestrator persona מועבר לכאן (כבר קיים הקובץ, רק למלא) |

**2.3** — הוסף Scale-Adaptive Paths 🟥  
**Agent:** `03-agents/workflows/plan.md`  
**עבודה:** ב-`agent-routing.md` להחליף את ה"default order" הנוכחי (שתמיד מציג full cycle) ב:

```markdown
## Default Paths (pick by intake level)

Simple:   agent → execute → done
Medium:   plan (plans-and-tasks.md) → execute → review → done  
Complex:  brainstorm? → PRD? → docs/plans/ → execute → test → review → finishing-branch
Critical: above + explicit approval checkpoint before execute
```

---

### Phase 3 — Agent Execution Protocol (from Superpowers) 🟥
**מטרה:** להוסיף model-appropriate staffing ו-status protocol לכל agent dispatch.

#### Tasks

**3.1** — הוסף Model-Appropriate Staffing 🟥  
**Agent:** `03-agents/specialists/documentation-writer.md`  
**עבודה:** להוסיף לכל agent definition (specialists + workflows) שורת frontmatter `model`:

```yaml
---
model: haiku    # mechanical tasks: 1-2 files, clear spec
model: sonnet   # integration tasks: multi-file coordination  
model: opus     # architecture, review, ambiguous/high-risk
---
```

**Priority agents לעדכן תחילה:** `executor`, `frontend-specialist`, `backend-specialist`, `security-auditor`, `debugger`, `explorer-agent`, `plan`

**3.2** — הוסף Status Protocol 🟥  
**Agent:** `03-agents/workflows/execute.md` + `03-agents/workflows/orchestrate.md`  
**עבודה:** להוסיף לsection של execution בשני הקבצים:

```markdown
## Agent Status Protocol

Every dispatched agent returns one of:

| Status | Meaning | What to do |
|---|---|---|
| DONE | Completed as requested | Proceed to review/next task |
| DONE_WITH_CONCERNS | Done but flagged something | Read concern → proceed if observational, fix if correctness |
| NEEDS_CONTEXT | Missing information | Provide missing context, re-dispatch |
| BLOCKED | Cannot proceed | Diagnose: context gap? scope issue? plan flaw? Fix then re-dispatch |

Rule: Never ignore an escalation. Never force retry without change.
```

**3.3** — הוסף Context Isolation Guideline 🟥  
**Agent:** `03-agents/workflows/orchestrate.md`  
**עבודה:** להוסיף עיקרון ל-orchestrator:

```markdown
## Context Isolation (CRITICAL)

Each dispatched subagent receives ONLY:
1. The specific task text
2. Relevant files (not the full session history)
3. Project brief (from 02-projects/)
4. Relevant standards (from 04-knowledge/standards/)

Do NOT pass: full conversation history, outputs of unrelated agents, entire codebase context.
Why: reduces cost, prevents confusion, improves focus.
```

---

### Phase 4 — Skills Library Pruning 🟥
**מטרה:** לצמצם מ-35+ skills ל~15 שבאמת בשימוש פעיל.

#### Tasks

**4.1** — מיפוי שימוש בפועל 🟥  
**Agent:** `03-agents/specialists/explorer-agent.md`  
**עבודה:** לבדוק אילו skills מוזכרים ב:
- frontmatter של כל workflow/specialist
- CLAUDE.md
- agent-routing.md

Skills שלא מוזכרים בשום agent definition → קנדידט לארכיב.

**4.2** — ארכיב skills לא בשימוש 🟥  
**Agent:** manual  
**עבודה:** להעביר לתיקיית `03-agents/skills/_archive/` כל skill שלא עבר מיפוי שימוש.  
**לשמור בוודאות:** `brainstorming`, `plan-writing`, `parallel-agents`, `clean-code`, `architecture`, `api-patterns`, `systematic-debugging`, `tdd-workflow`, `behavioral-modes`, `app-builder`, `vulnerability-scanner`, `code-review-checklist`, `nextjs-react-expert`, `frontend-design`, `database-design`

---

## Staffing Summary

| Phase | Task | Agent | Estimated effort |
|---|---|---|---|
| 1 | Cleanup docs/plans + outputs | explorer-agent | 30 min |
| 1 | Maestro brief | manual | 20 min |
| 2 | Intake Triage section | documentation-writer | 45 min |
| 2 | Split agent-routing.md | documentation-writer | 1 hr |
| 2 | Scale-adaptive paths | plan | 30 min |
| 3 | Model staffing frontmatter | documentation-writer | 45 min |
| 3 | Status protocol | documentation-writer | 30 min |
| 3 | Context isolation | documentation-writer | 20 min |
| 4 | Skills usage map | explorer-agent | 30 min |
| 4 | Archive unused skills | manual | 20 min |

---

## Order of Execution

```
Phase 1 (cleanup)     → no dependencies, do first
Phase 2 (routing)     → after Phase 1 (cleaner slate)
Phase 3 (protocols)   → parallel to Phase 2
Phase 4 (skills)      → after Phase 2 (routing references skills)
```

---

## Definition of Done

- [ ] `docs/plans/` מכיל רק תוכניות פעילות
- [ ] `06-outputs/` מכיל רק outputs עם תאריך + files רלוונטיים
- [ ] `agent-routing.md` ≤ 200 שורות + Intake Assessment section
- [ ] `03-agents/workflows/orchestrate.md` מכיל Orchestrator persona
- [ ] כל agent ראשי מכיל `model:` בfrontmatter
- [ ] Status Protocol מתועד ב-execute.md + orchestrate.md
- [ ] Skills: רק active set נגיש, שאר ב-`_archive/`
- [ ] `02-projects/maestro/project.maestro.md` מלא

---

## Sync to plans-and-tasks

לאחר execution — לסנכרן ל-`02-projects/maestro/plans-and-tasks.md` ולמחוק קובץ זה.
