# hadaryaCRM — Architecture Reference

> What the code does (always up to date). For reading from project docs.

## Tech Stack

- Vite, React, TypeScript, Tailwind CSS, shadcn/ui
- Supabase (auth, DB, Edge Functions), TanStack Query

## Entity Pages

| Page | Shell | Toolbar | Kanban | Table |
|------|-------|---------|--------|-------|
| Leads | ✓ | ✓ | LeadKanban | LeadTable |
| Deals | ✓ | ✓ | DealKanban | DealTable |
| Quotes | ✓ | ✓ | QuoteKanban | QuoteTable |
| Designs | ✓ | ✓ | DesignRequestKanban | DesignRequestTable |
| Ad Agency (4) | Projects only | All 4 | ProjectKanban | All 4 tables |

## Key Components

- `EntityPageShell` — wrapper for entity pages
- `EntityToolbar` — filters, saved views, sort, column visibility slot
- `EntityKanban` — Kanban board with configurable columns
- `ColumnVisibilityDropdown` — ad-agency tables only

## Security

- `src/lib/escapeIlike.ts` — ILIKE escaping
- `escapeHtml` in `supabase/functions/send-quote/index.ts` — XSS prevention

## Reference Docs (vault)

- Entity unification: `hadaryaCRM-entity-page-unification.md`
- Security: `hadaryaCRM-security-audit.md`
- UI/UX plan: `hadaryaCRM-ui-ux-improvement-plan.md`
- MCP setup: `hadaryaCRM-cursor-mcp-setup.md`
- Remaining tasks: `docs/plans/2026-02-27-hadaryaCRM-remaining-tasks.md`
