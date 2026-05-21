# 03-agents — Agent Network

> **Single source of truth.** All agents, workflows, and skills live here. Workspace = Maestro vault.

## Structure

| Folder | Content |
|--------|---------|
| `core/` | Reserved for future persistent personas. **Planning + PRD** — `workflows/plan.md` (`/plan`, `/prd`). **Orchestrator** + staffing catalog — `agent-routing.md`. **CTO** — `workflows/brainstorm.md`. |
| `specialists/` | 17 domain experts (including `ui-ux-specialist`, `technical-educator`, frontend, backend, …) |
| `games/` | game-developer + index (archive — optional for now) |
| `content/` | gold-ira-seo-content-writer |
| `workflows/` | Mode workflows (`/execute`, `/plan`, …); supply cycle summarized in [[agent-routing]] and detailed per file under *Place in the supply cycle* |
| `skills/` | Markdown skills + scripts — index: [[skills/README]] |

## Vault skills vs Cursor skills

| Layer | Where | When it applies |
|-------|--------|-----------------|
| **Vault skills** | `03-agents/skills/` (this repo) | Human + model read these in Obsidian/Cursor when working **in or from the Maestro vault**; agents reference them by path in prompts. |
| **Cursor / plugin skills** | e.g. `~/.cursor/skills`, bundled plugin `SKILL.md` files | Injected by Cursor rules/hooks when you edit matching paths or run matching commands — **not** the same files as the vault. |

Do not duplicate long checklists in both places. Prefer vault skills for Maestro-specific procedures; use Cursor skills for IDE/tooling automation.

## How to Use

**Workspace = Maestro vault.** Cursor opens on vault. Project code accessed from project paths.
- CLAUDE.md → rules from 01-me, 02-projects, **03-agents**, 04-knowledge
- Before a task: check `agent-routing.md` — which agent to invoke + [[04-knowledge/standards/maestro-project-doc-lifecycle|Project Rules]]
- Agents in `specialists/`, scripts in `skills/`, knowledge in `04-knowledge/`

## Key Links

- [[agent-routing]] — route tasks to the right agent
- [[workflows/invariant-sentinel]] — engineering invariant / drift monitoring (vault + Cursor Automations)
- [[games/README]] — games hub (archive)
- [[AGENT-TEMPLATE]] — template for new agents; **all** `specialists/*.md` and [[workflows/plan]] include the same **Maestro contract** sections (Role → Stop) for a uniform standard
- [[skills/README]] — skills index by domain
- [[skill-template]] — template for new skills (in skills/)
- `04-knowledge/` — research, guidelines, patterns

## Updates

Update **only in the vault**. All projects use the same agent infrastructure.
