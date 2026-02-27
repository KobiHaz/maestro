# hadaryaCRM — Cursor Rules & Standards

> Repo: hadaryaCRM. Project/product name: Demo CRM. Read this for rules when working on hadaryaCRM.

## Tech Stack

- Vite, React, TypeScript, Tailwind CSS, shadcn/ui
- Supabase (auth, DB, Edge Functions), TanStack Query

## Key Patterns

- **Entity pages:** Use `EntityPageShell` + `EntityToolbar` + `EntityKanban` for Leads, Deals, Quotes, Designs
- **Security:** `escapeIlike()` for all ILIKE search inputs; `escapeHtml()` for user data in HTML (e.g. send-quote)
- **Ad Agency:** Separate module at `src/pages/ad-agency/`, uses `useColumnVisibility`, `ColumnVisibilityDropdown`

## Naming

| Type | Pattern | Example |
|------|---------|---------|
| Component files | PascalCase | `EntityPageShell.tsx`, `LeadKanban.tsx` |
| Hooks | `use` + PascalCase | `useColumnVisibility.ts`, `useTablePreferences.ts` |
| Lib / utils | camelCase | `escapeIlike.ts` |
| Folders | kebab-case | `entity-page`, `ad-agency`, `data-table` |
| Plan files | `YYYY-MM-DD-kebab-description.md` | `2025-02-23-modular-permissions-implementation.md` |

## Architecture

- **Entity pattern:** Use `EntityPageShell` + `EntityToolbar` + `EntityKanban` for Leads, Deals, Quotes, Designs.
- **Slots:** `renderKanban`, `renderTable`, `renderToolbar`, `renderColumnVisibility` — extend without changing core.
- **Ad-agency:** Separate module at `src/pages/ad-agency/` — Clients, Projects, Items, Tasks; uses `useColumnVisibility`, `ColumnVisibilityDropdown`.

## Security

- `escapeIlike()` for all ILIKE search inputs (Leads, Customers, LeadDialog, GlobalCommandPalette).
- `escapeHtml()` for user data in HTML (e.g. `send-quote` Edge Function).

## Plan Lifecycle

**Whenever you complete a task or plan:**

1. Update the relevant docs — Obsidian `02-projects/hadaryaCRM`, `04-knowledge/reference/hadaryaCRM-architecture.md`
2. Suggest deleting the old work plan from `docs/plans/` if it has been fully implemented
3. Don't delete plans yourself — suggest deletion and let the user approve

## Reference

- Architecture: `04-knowledge/reference/hadaryaCRM-architecture.md`
- Remaining plan: `docs/plans/2026-02-27-hadaryaCRM-remaining-tasks.md` (in vault or project)
