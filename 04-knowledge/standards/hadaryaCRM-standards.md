# hadaryaCRM — Cursor Rules & Standards

> **Extends:** [[04-knowledge/standards/base-coding-standards|base-coding-standards]]. Load both.
> Repo: hadaryaCRM. Project/product name: Demo CRM. Read this for rules when working on hadaryaCRM.

## Tech Stack

- Vite, React, TypeScript, Tailwind CSS, shadcn/ui
- Supabase (auth, DB, Edge Functions), TanStack Query

## Key Patterns

- **Entity pages:** Use `EntityPageShell` + `EntityToolbar` + `EntityKanban` for Leads, Deals, Quotes, Designs
- **Security:** `escapeIlike()` for all ILIKE search inputs; `escapeHtml()` for user data in HTML (e.g. send-quote)
- **Ad Agency:** Separate module at `src/pages/ad-agency/`, uses `useColumnVisibility`, `ColumnVisibilityDropdown`

## Naming (תוספות ל-base)

| Type | Pattern | Example |
|------|---------|---------|
| Folders | kebab-case | `entity-page`, `ad-agency`, `data-table` |

*Plan files — [[04-knowledge/standards/maestro-project-doc-lifecycle#4. תבנית שם תוכנית|maestro §4]].*

## Architecture

- **Entity pattern:** Use `EntityPageShell` + `EntityToolbar` + `EntityKanban` for Leads, Deals, Quotes, Designs.
- **Slots:** `renderKanban`, `renderTable`, `renderToolbar`, `renderColumnVisibility` — extend without changing core.
- **Ad-agency:** Separate module at `src/pages/ad-agency/` — Clients, Projects, Items, Tasks; uses `useColumnVisibility`, `ColumnVisibilityDropdown`.

## Security

- `escapeIlike()` for all ILIKE search inputs (Leads, Customers, LeadDialog, GlobalCommandPalette).
- `escapeHtml()` for user data in HTML (e.g. `send-quote` Edge Function).

## Plan Lifecycle

[[04-knowledge/standards/maestro-project-doc-lifecycle]]. **hadaryaCRM:** לא למחוק תוכניות בעצמך — להציע מחיקה ולאשר עם המשתמש.

## Reference

- Architecture: `04-knowledge/reference/hadaryaCRM-architecture.md`
- Remaining plan: `docs/plans/2026-02-27-hadaryaCRM-remaining-tasks.md` (in vault or project)
