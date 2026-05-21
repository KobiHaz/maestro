# CRM — Architecture Reference

> What the code does (always up to date). For reading from project docs.

## Tech Stack

- Vite, React, TypeScript, Tailwind CSS, shadcn/ui
- Supabase (auth, DB, Edge Functions), TanStack Query v5

## Entity Pages (Unified Pattern)

All entity pages share: EntityPageShell, EntityToolbar, EntityKanban/Table. Only title, subtitle, add-button, and card/form content vary.

```
┌─────────────────────────────────────────────────────────┐
│ [Title]                                    [Add Button] │
│ [Subtitle]                                               │
├─────────────────────────────────────────────────────────┤
│ [Pipeline] [Table]  [Filters / Tabs (optional)]         │
│  Pipeline: Kanban | Table: sorting + filters             │
└─────────────────────────────────────────────────────────┘
```

| Page | Shell | Toolbar | Kanban | Table |
|------|-------|---------|--------|-------|
| Leads | ✓ | ✓ | LeadKanban | LeadTable |
| Deals | ✓ | ✓ | DealKanban | DealTable |
| Contracts | ✓ | ✓ | QuoteKanban | QuoteTable |
| Designs | ✓ | ✓ | DesignRequestKanban | DesignRequestTable |
| Ad Agency (4) | Projects only | All 4 | ProjectKanban | All 4 tables |

**Location:** `src/components/entity-page/` — EntityPageShell.tsx, EntityToolbar.tsx, EntityKanban.tsx

## Key Components

- `EntityPageShell` — wrapper for entity pages
- `EntityToolbar` — filters, saved views, sort, column visibility slot
- `EntityKanban` — Kanban board with configurable columns
- `ColumnVisibilityDropdown` — ad-agency tables only
- `LeadDialogsOrchestrator` — groups LeadDialog, QuoteBuilder, QuotePreview, SaveView dialog

## Data Patterns

- `src/lib/normalize.ts` — `quotesByLeadId()`, `arrayToRecord()` for O(1) lookups
- `useCrmTeam` returns `membersByUserId: Map<string, CrmTeamMember>` for assignee display
- `useLeads` — leads page state, queries, mutations (Leads.tsx delegates to it)
- `src/data/demoLeads.ts` — DEMO_LEADS constant

## Security

- `src/lib/escapeIlike.ts` — ILIKE escaping
- `escapeHtml` in `supabase/functions/send-quote/index.ts` — XSS prevention

## Performance (2026-03-02)

- ExcelJS dynamic import — AdAgencyProjectDetail chunk ~26KB (was 964KB)
- `manualChunks` in Vite — vendor-react, vendor-query, vendor-supabase
- React.memo on LeadCard, DealCard, ProductCard
- Sentry deferred via requestIdleCallback

## Reference Docs (vault)

- Security: `crm-security-audit.md`
- UI/UX plan: `crm-ui-ux-improvement-plan.md`
- MCP setup: `crm-cursor-mcp-setup.md`
