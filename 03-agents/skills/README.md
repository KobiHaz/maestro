# Vault skills — index

Markdown playbooks and optional scripts under `03-agents/skills/`. Load by path when prompting agents in Cursor or reading in Obsidian. For Cursor-only auto-injected skills, see the table in [[../README]] (*Vault skills vs Cursor skills*).

**Top-level folders** (35 + `skill-template.md` at this level):

## Planning, process, agents

| Folder | Notes |
|--------|--------|
| `brainstorming/` | Ideation |
| `plan-writing/` | Plan structure |
| `parallel-agents/` | Multi-agent patterns |
| `intelligent-routing/` | Routing hints |
| `behavioral-modes/` | Modes / tone |

## Frontend & web

| Folder | Notes |
|--------|--------|
| `frontend-design/` | UI, a11y scripts |
| `nextjs-react-expert/` | Next/React performance slices + scripts |
| `tailwind-patterns/` | Tailwind |
| `web-design-guidelines/` | General web UI |
| `webapp-testing/` | Playwright runner |

## Backend, data, platform

| Folder | Notes |
|--------|--------|
| `api-patterns/` | API design |
| `architecture/` | System design |
| `database-design/` | Schema, migrations, scripts |
| `nodejs-best-practices/` | Node |
| `python-patterns/` | Python |
| `rust-pro/` | Rust |
| `server-management/` | Ops-style server work |
| `mcp-builder/` | MCP servers |

## Security & quality

| Folder | Notes |
|--------|--------|
| `vulnerability-scanner/` | `security_scan.py`, checklists |
| `red-team-tactics/` | Offensive mindset |
| `code-review-checklist/` | Solid, security, quality |
| `clean-code/` | Style |
| `systematic-debugging/` | Debug flow |
| `lint-and-validate/` | Lint / type coverage scripts |

## Testing & performance

| Folder | Notes |
|--------|--------|
| `tdd-workflow/` | TDD |
| `testing-patterns/` | Tests + `test_runner.py` |
| `performance-profiling/` | Lighthouse script |

## SEO, GEO, content

| Folder | Notes |
|--------|--------|
| `seo-fundamentals/` | SEO + `seo_checker.py` |
| `geo-fundamentals/` | GEO + script |
| `documentation-templates/` | Docs |

## Mobile, i18n, deploy

| Folder | Notes |
|--------|--------|
| `mobile-design/` | Mobile UX + `mobile_audit.py` |
| `i18n-localization/` | i18n script |
| `deployment-procedures/` | Release |

## App scaffolding

| Folder | Notes |
|--------|--------|
| `app-builder/` | Templates (Next, Nuxt, FastAPI, monorepo, etc.) |

## Shell / OS

| Folder | Notes |
|--------|--------|
| `bash-linux/` | Unix shell |
| `powershell-windows/` | Windows |

## Game development (archive-aligned)

| Folder | Notes |
|--------|--------|
| `game-development/` | Tree of topics (2D/3D, multiplayer, audio, …). Aligns with archived [[../games/README|games/]] hub — use only when game work is in scope. |

## Templates

- `skill-template.md` — new skill scaffold

Nested-only trees: everything under `game-development/` and `app-builder/templates/`; no extra top-level folders required beyond the parent above.
