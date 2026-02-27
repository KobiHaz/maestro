# Maestro Vault — PKM Analysis & Improvement Recommendations

> **Date:** 2026-02-26  
> **Type:** Analysis, Best Practices, Migration Plan  
> **Scope:** Obsidian vault for AI agents, prompts, and Cursor integration

---

## 1. Understanding the Current Structure and Implied Workflow

### Architecture

The vault uses a **numeric structure** (00–07) that defines a clear hierarchy:

| Folder | Role | Actual Content |
|--------|------|----------------|
| **00-inbox** | Entry — ideas, links | README |
| **01-me** | Identity — who you are, style, tools | identity, tools, writing, ai-preferences |
| **02-projects** | Projects — connection to agents | **Empty** |
| **03-agents** | Agents, workflows | core (4), specialists (14), content (1), workflows (17) |
| **04-knowledge** | Knowledge | research, competitors, insights |
| **05-templates** | Templates | project-brief, output-post, meeting-notes |
| **06-outputs** | Final outputs | reports, posts |
| **07-logs** | Logs | weekly journal |
| **docs/plans** | Implementation plans | plans, design docs |

### Implied Workflow

```
User → CLAUDE.md (instructions) → agent-routing.md → Agent/Workflow → Output
                ↓
         01-me (personal context)
         02-projects (project context — inactive)
```

**Key Points:**
1. **CLAUDE.md** = entry point for AI — defines protocol before every task.
2. **agent-routing** = routing table — task → appropriate agent.
3. **Workflows** = centralized prompts (orchestrate, brainstorm, plan...) — commands with `$ARGUMENTS`.
4. **Agents** = personas + behavior — frontmatter + detailed content.
5. **Symlinks** = connection to code projects (hadaryaCRM, CMS) — agents available from the project.

### Important Distinction: Agent vs Prompt

| Type | Example | Role |
|------|---------|------|
| **Agent** | frontend-specialist, orchestrator | Persona + long-term behavior |
| **Workflow** | orchestrate, brainstorm, plan | Point-in-time prompt / command — `$ARGUMENTS` |
| **Template** | project-brief, output-post | Data structure / output |

The distinction exists but is not explicit. There is no separate `Prompts` folder — workflows serve as prompts.

---

## 2. Strengths of the Current Structure

### Structure and Documentation
- ✅ **Numeric hierarchy** — clear order, easy to navigate.
- ✅ **CLAUDE.md** — central instructions, consistent protocol.
- ✅ **agent-routing.md** — organized routing table by Core / Specialists / Content / Workflows.
- ✅ **Common Flows** — defined scenarios (bug, feature, security).
- ✅ **README in every folder** — 00-inbox, 04-knowledge, 05-templates, 06-outputs, 07-logs.

### Agents
- ✅ **Consistent frontmatter** — name, description (in many); tools, model, domain (in some).
- ✅ **AGENT-TEMPLATE** — clear template for new agent.
- ✅ **Domain separation** — core / specialists / content / workflows.
- ✅ **High quality** — frontend-specialist, orchestrator well detailed.

### Connection to Cursor
- ✅ **Symlinks** — maestro/01-me, maestro/03-agents → vault.
- ✅ **VAULT_PATH.md** — absolute path for IDE access.
- ✅ **Connection documentation** — docs/plans with hadaryaCRM, CMS details.

### Workflows
- ✅ **Structured prompts** — `$ARGUMENTS`, clear behavior.
- ✅ **Variety** — orchestrate, brainstorm, plan, debug, deploy...

---

## 3. Weaknesses and Chaos

### Structure and Folders
| Issue | Details |
|-------|---------|
| **02-projects empty** | No agents ↔ projects connection — CLAUDE section on "read project brief" not implemented |
| **No separate Prompts** | Workflows = prompts, but no explicit distinction and no folder for general prompts |
| **No System/Meta** | 01-me = identity, no place for working principles, routines, method settings |
| **docs outside hierarchy** | docs/plans not part of 00–07 structure — hard to find |

### Agents
| Issue | Details |
|-------|---------|
| **Inconsistent frontmatter** | workflows: only `description`, missing `name`, `domain` |
| **api-designer missing** | Referenced in orchestrator, not in agent-routing or as a file |
| **Non-English text** | orchestrate.md contains "Renk tercihiniz var mı?" (Turkish) |
| **Lack of links** | agent ↔ prompts ↔ project — no links in the system |

### Prompts (Workflows)
| Issue | Details |
|-------|---------|
| **No versions** | No v1, v2, v3 — hard to track changes |
| **No "what worked" documentation** | Missing feedback loop for prompts |
| **Inconsistent template** | Some with `$ARGUMENTS`, some without — lack of standard |
| **No link to agent** | workflow doesn't define which agent runs it |

### Naming
| Issue | Details |
|-------|---------|
| **Lack of consistency** | frontend-specialist vs gold-ira-seo-content-writer — different formats |
| **No prefix** | agent., prompt., project. — doesn't allow efficient search/filtering |

---

## 4. Comparison to Best Practices

### Sources
- [Organize AI Prompts with Obsidian + Templater](https://cosmo-edge.com/organize-ai-prompts-obsidian-templater/)
- [AI-Native Obsidian Vault Setup](https://curiouslychase.com/)
- [PKM with Obsidian and Claude](https://krucho.ski/)
- [ballred/obsidian-claude-pkm](https://github.com/ballred/obsidian-claude-pkm)

### Relevant Best Practices

| Best Practice | Status in Vault | Gap |
|---------------|-----------------|-----|
| **Consistent folder structure** (Agents, Prompts, Projects, Archives) | 03-agents exists, 02-projects empty, no Prompts | Missing Prompts; 02-projects inactive |
| **Standard frontmatter for agent** (role, goals, constraints, tools, contexts) | name, description, tools, domain — partial | Missing: goals, constraints, contexts |
| **Templates for prompts** (header, inputs, I/O examples) | workflows with $ARGUMENTS | Missing: I/O examples, fixed template structure |
| **Versions for prompts** (v1, v2, v3) | Not present | Completely missing |
| **Links** agent ↔ prompt ↔ project | Not present | Completely missing |
| **Naming convention** (agent.*, prompt.*) | None | Missing |
| **CLAUDE.md at center** | ✅ exists | — |
| **Markdown-native, local-first** | ✅ | — |

---

## 5. Target Structure (Ideal Structure)

### Proposed Folder Hierarchy

```
Maestro/
├── 00-inbox/
├── 01-me/                    # Identity + System/Meta (unified)
│   ├── identity/
│   ├── tools/
│   └── system/               # Principles, routines, meta
├── 02-projects/              # Projects — connection to agents
│   └── project.[name].md
├── 03-agents/
│   ├── core/
│   ├── specialists/
│   ├── content/
│   └── workflows/            # Or: separate 04-prompts
├── 04-prompts/               # [Optional] General prompts outside workflows
│   └── prompt.[agent].[use-case].v01.md
├── 05-knowledge/             # (Replace 04)
├── 06-templates/
├── 07-outputs/
├── 08-logs/
├── 09-archive/               # Old prompts/sessions
├── docs/
│   └── plans/
├── CLAUDE.md
└── VAULT_PATH.md
```

**Note:** Changing 04→05, 05→06... requires migration. **Simpler option:** keep existing numbers and only add:
- `04-prompts/` (or leave workflows in 03-agents)
- `09-archive/`
- `01-me/system/` for method principles

---

### Recommended Templates

#### a. AI Agent Template

```markdown
---
name: [agent-id]
description: [1-2 sentences — when to use]
domain: [frontend | backend | security | planning | content | ...]
tools: inherit
model: inherit
goals: []
constraints: []
contexts: []        # Files/folders for context
prompts: []         # Linked prompts/workflows
projects: []        # Relevant projects
---

# [Agent Name]

## Role
## When to Use
## Constraints
## Tools & Skills
```

#### b. Prompt Template

```markdown
---
name: [prompt-id]
agent: [agent-id]           # Which agent runs it
use_case: [short description]
version: v01
created: YYYY-MM-DD
works_well: []              # What worked well
needs_improvement: []       # What to improve
---

# [Prompt Title]

## Context
## Input
$ARGUMENTS

## Expected Output Format
## Example I/O
### Input:
### Output:
```

#### c. Session / Chat Log Template (Agent ↔ Project)

```markdown
---
project: [project-id]
agent: [agent-id]
date: YYYY-MM-DD
session_type: [planning | implementation | review]
---

# Session: [Project] — [Agent]

## Task
## Decisions
## Outputs
## Next Steps
```

---

### Recommended Naming Convention

| Type | Format | Example |
|------|--------|---------|
| **Agent** | `agent.[domain].[name].md` or `[name].md` in folder | `frontend-specialist.md`, `orchestrator.md` |
| **Prompt** | `prompt.[agent].[use-case].vNN.md` | `prompt.orchestrator.multi-agent.v01.md` |
| **Project** | `project.[name].md` | `project.hadaryaCRM.md` |
| **Output** | `YYYY-MM-DD-[description].md` | `2026-02-26-vault-analysis.md` |
| **Session** | `session.[project].[date].md` | `session.hadaryaCRM.2026-02-26.md` |

**With Cursor:** prefixes like `agent.`, `prompt.` help with quick search by type.

---

## 6. Practical Migration Steps

### Phase 1: Non-Disruptive Infrastructure (Week 1)

1. **Create 02-projects**
   - [ ] File `02-projects/README.md` — explanation + link to agent-routing.
   - [ ] Template `05-templates/project-brief.md` — already exists.
   - [ ] Create `project.hadaryaCRM.md`, `project.cms.md` — link to relevant agents.

2. **Fix orchestrate.md**
   - [ ] Replace "Renk tercihiniz var mı?" with "What color palette do you prefer?"
   - [ ] Check for other non-English text.

3. **api-designer**
   - [ ] Decision: create agent or remove from orchestrator.
   - [ ] If creating — `03-agents/specialists/api-designer.md` + update agent-routing.

### Phase 2: Frontmatter Consistency (Week 2)

4. **Workflows**
   - [ ] Add `name`, `agent` (or `domain`) to every workflow.
   - [ ] Save template in `05-templates/workflow-template.md`.

5. **Agents**
   - [ ] Verify every specialist/core/content has: name, description.
   - [ ] Add domain if missing.
   - [ ] Sync agent-routing — agent list = file list.

### Phase 3: Links and Structure (Week 3)

6. **Links**
   - [ ] In each agent: `prompts: [[workflow-x]]` — workflows that use it.
   - [ ] In each project: `agents: [[agent-x]], [[agent-y]]`.
   - [ ] In agent-routing: links to files instead of text.

7. **System/Meta**
   - [ ] Folder `01-me/system/` or `01-me/meta/`.
   - [ ] File `principles.md` — working principles.
   - [ ] File `routines.md` — daily/weekly routines.
   - [ ] Update CLAUDE.md: "Before task — read 01-me/system/principles if relevant."

### Phase 4: Versions and Prompts (Week 4)

8. **Prompt versions**
   - [ ] For main workflows: duplicate to `workflow-name.v01.md`.
   - [ ] Add frontmatter: version, created, works_well, needs_improvement.
   - [ ] Archiving: old workflows → `09-archive/workflows/`.

9. **Prompt template**
   - [ ] Create `05-templates/prompt-template.md`.
   - [ ] New prompts — use the template.

### Phase 5: Naming (Optional)

10. **Rename files**
    - [ ] Decision: prefix (agent., prompt.) or keep current.
    - [ ] If changing — update links in CLAUDE, agent-routing, README.

---

## 7. Automation Ideas

| Idea | How | Benefit |
|------|-----|---------|
| **Templater** | Templates with `tp.date`, `tp.file` | Quick note creation with date and metadata |
| **Dataview** | Queries: agents by domain, workflows by agent | Dynamic views |
| **Buttons** | "New project" button → project-brief template | Less friction |
| **QuickAdd** | Capture → inbox, Capture → session log | Fast input |
| **Cursor rule** | "Before task — read project brief if exists" | Keeps context |
| **Git hooks** | pre-commit: check agent-routing is up to date | Prevents drift |
| **Validation script** | List agents in agent-routing vs files | Auto sync |
| **Obsidian Daily Note** | Daily template with [[07-logs/YYYY-Www]] | Auto link to log |

---

## 8. Guiding Principles (3–5)

### 1. New agent
> **Check agent-routing** — Is there a similar agent? If yes — extend. If no — create from AGENT-TEMPLATE. Add to agent-routing and link to prompts/relevant projects.

### 2. New prompt
> **Define use-case** — What does the prompt do? Which agent runs it? Create from prompt-template. If changing existing workflow — save version (v01 → v02) and document "what worked".

### 3. New project
> **Create project.[name].md** in 02-projects. Link to relevant agents. Keep brief (goal, status, decisions). Read it before tasks in the project.

### 4. Connectivity
> **Agent ↔ Prompt ↔ Project** — maintain links in frontmatter. Enables quick navigation and Dataview queries.

### 5. Language and localization
> **English in agent and prompt files** — work with Cursor/Claude. Hebrew allowed in 01-me (identity), 02-projects (business description), 07-logs.

---

## 9. Clarification Questions to Improve Recommendations

1. **02-projects:** Is there intent to use project briefs? If yes — what information is important (tech stack, decisions, links)?

2. **Separate Prompts:** Are there general prompts not in workflows? If yes — consider folder `04-prompts/` or `03-agents/prompts/`.

3. **System/Meta:** Where are working principles and daily routines stored? In 01-me or elsewhere?

4. **api-designer:** Is the agent needed? If yes — what is the scope (REST, GraphQL, OpenAPI)?

5. **Naming:** How important are prefixes (agent., prompt.) — for Cursor search or Obsidian filtering?

---

## 10. Summary

The vault is well established: clear structure, strong agent-routing, Cursor connection via symlinks. Main gaps:

- **02-projects empty** — agents ↔ projects connection missing.
- **No explicit distinction** between agent, prompt, workflow.
- **Missing:** prompt versions, mutual links, System/Meta.
- **Inconsistent frontmatter** — especially in workflows.

Recommended steps are ordered by implementation, focused, and can be applied step by step. Answers to the clarification questions can refine the prompts and projects structure.
