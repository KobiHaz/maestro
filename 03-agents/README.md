# 03-agents — Agent Network

> **Single source of truth.** All agents, workflows, and skills live here. Workspace = Maestro vault.

## Structure

| Folder | Content |
|--------|---------|
| `core/` | orchestrator, cto, project-planner, create-plan |
| `specialists/` | 14 specialists (frontend, backend, security, test, debug, seo, ...) |
| `content/` | gold-ira-seo-content-writer |
| `workflows/` | orchestrate, brainstorm, plan, create, debug, deploy, document, execute, review, ... |
| `skills/` | scripts (security_scan, lint_runner, compliance_checker, etc.) when present |

## How to Use

**Workspace = Maestro vault.** Cursor opens on vault. Project code accessed from project paths.
- CLAUDE.md → rules from 01-me, 02-projects, **03-agents**, 04-knowledge
- Before a task: check `agent-routing.md` — which agent to invoke
- Agents in `specialists/`, scripts in `skills/`, knowledge in `04-knowledge/`

## Key Links

- [[agent-routing]] — route tasks to the right agent
- [[AGENT-TEMPLATE]] — template for new agents
- `04-knowledge/` — research, guidelines, patterns

## Updates

Update **only in the vault**. All projects use the same agent infrastructure.
