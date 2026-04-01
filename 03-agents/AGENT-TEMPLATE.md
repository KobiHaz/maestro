---
name: agent-id
description: "When to invoke + routing keywords (do not repeat Role). Example: Expert in X. Use when Y. Triggers: a, b, c."
tools: inherit
model: inherit
domain: frontend
# optional: skills: skill-name
---

# [Agent Name]

> **Template shape:** An agent ≠ a chatbot — you need routing triggers, a clear action space, a short reasoning protocol, and stop/escalation rules. Do not duplicate long text from `CLAUDE.md` or standards; link to paths.

## Role

**Objective:** [what the agent delivers — one focused sentence]

**Scope:** [domain of responsibility]

**Non-goals (out of scope):** [what the agent does not do — point to another agent/flow if needed]

## When to Use

**Triggers (invoke when):**

- [signal, file, keyword, task type]
- […]

**Do not use when:**

- [state where another agent/flow fits better]
- [missing critical info — clarify or gather first]

## Action Space & Outputs

**Tools / capabilities:** [inherit | specific list — Read, Grep, Bash, …]

**Preferred artifacts:** [files, format, where to save — e.g. `06-outputs/`, `02-projects/...`]

**Tool & data rules:** [prefer between tools; compress long output; do not run X without approval]

## Reasoning Protocol

Before any significant action (code change, delete, system command, publishing a decision):

1. **What I know** — what is already known from context
2. **Next action** — what to do now
3. **Expected result** — what should come out
4. **Fallback** — if it fails: alternative or stop

## Constraints

**Must:**

- [hard requirement]

**Must not (negative constraints):**

- [no refactor beyond the ask; no new files without need; …]

**Vault & standards:** [pointers to `04-knowledge/standards/`, project brief in `02-projects/`, workflows in `03-agents/workflows/`]

## Stop, Errors & Escalation

**Done when:** [clear completion criterion]

**Stop and ask the human when:** [product ambiguity, security/data risk, architecture choice with large trade-offs]

**On failure:** [try Y; if still failing — report and do not invent]

---

## Filling guide

| Part | Why |
|------|-----|
| `description` in frontmatter | Routing: one “when to use” sentence + keywords, not a duplicate of Role |
| Non-goals | Reduces confusion between agents and prevents scope creep |
| Triggers / Do not use | Reduces wrong agent activation |
| Action Space | Defines tools and outputs — like an autonomous agent “action space” |
| Reasoning Protocol | Forces a process before risky or expensive steps |
| Must not | Matches common Cursor/rules practice to reduce invention and over-engineering |
| Stop / Escalation | Exit and escalation conditions — no infinite loop |

For a full vault-style example: see an existing agent under `specialists/` (e.g. `mobile-developer.md`). **Planning + PRD:** `03-agents/workflows/plan.md` (in routing still labeled **project-planner**).
