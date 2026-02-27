# Entity Page Unification Plan — Leads, Quotes, Deals, Designs

**Goal:** Maximum shared code between the 4 pages. Only title, subtitle, add-button text, and card/form content vary.

---

## 1. Shared structure (current)

All pages use the same pattern:

```
┌─────────────────────────────────────────────────────────┐
│ [Title]                                    [Add Button] │
│ [Subtitle]                                               │
├─────────────────────────────────────────────────────────┤
│ [Pipeline] [Table]  [Filters / Tabs (optional)]         │
├─────────────────────────────────────────────────────────┤
│  Pipeline: Kanban with columns by status                │
│  or Table: table with sorting and filters               │
└─────────────────────────────────────────────────────────┘
```

## 2. Implementation status ✓

- [x] **Phase 1–5** — EntityPageShell, EntityToolbar, EntityKanban — all pages migrated
- Leads, Deals, Quotes, Designs use EntityPageShell + EntityToolbar
- LeadKanban, DealKanban, QuoteKanban, DesignRequestKanban use EntityKanban

## 3. Reference

Location: `src/components/entity-page/` — EntityPageShell.tsx, EntityToolbar.tsx, EntityKanban.tsx
