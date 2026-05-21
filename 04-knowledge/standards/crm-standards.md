# CRM — Cursor Rules & Standards

> **Extends:** `04-knowledge/standards/base-coding-standards.md`. Load both.
> Project path: `~/.gemini/antigravity/projects/hadaryaCRM`
> Knowledge layer: `.claude/CLAUDE.md` in the project repo (source of truth for Claude).

## Tech Stack

- Vite, React, TypeScript, Tailwind CSS, shadcn/ui
- Supabase (auth, DB, Edge Functions), TanStack Query v5

## Key Patterns

- **Entity pages:** Use `EntityPageShell` + `EntityToolbar` + `EntityKanban` for Leads, Deals, Contracts, Designs
- **Security:** `escapeIlike()` for all ILIKE search inputs; `escapeHtml()` for user data in HTML (e.g. send-quote)
- **Ad Agency:** Separate module at `src/pages/ad-agency/`, uses `useColumnVisibility`, `ColumnVisibilityDropdown`
- **Auth:** Use `canAccessModule()` / `isModuleAdmin()` — never the deprecated `role` field

## Naming

| Type | Pattern | Example |
|------|---------|---------|
| Folders | kebab-case | `entity-page`, `ad-agency`, `data-table` |
| Components | PascalCase | `LeadDialog`, `EntityKanban` |
| Hooks | camelCase (use prefix) | `useLeads`, `useCrmTeam` |

## Architecture

- **Entity pattern:** Use `EntityPageShell` + `EntityToolbar` + `EntityKanban` for Leads, Deals, Contracts, Designs.
- **Slots:** `renderKanban`, `renderTable`, `renderToolbar`, `renderColumnVisibility` — extend without changing core.
- **Ad-agency:** Separate module at `src/pages/ad-agency/` — Clients, Projects, Items, Tasks.

## Security

- `escapeIlike()` for all ILIKE search inputs (Leads, Customers, LeadDialog, GlobalCommandPalette).
- `escapeHtml()` for user data in HTML (e.g. `send-quote` Edge Function).
- Every new table needs `ENABLE ROW LEVEL SECURITY` + policies using `has_module_access()` / `has_module_admin()`.

## Plan Lifecycle

Do not delete plans unilaterally — propose deletion and confirm with the user.

## Reference

- Architecture: `04-knowledge/reference/crm-architecture.md`
- Security audit: `04-knowledge/reference/crm-security-audit.md`
- UI/UX plan: `04-knowledge/reference/crm-ui-ux-improvement-plan.md`
- MCP setup: `04-knowledge/reference/crm-cursor-mcp-setup.md`
