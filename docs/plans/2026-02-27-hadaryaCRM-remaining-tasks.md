# hadaryaCRM — Pending Tasks

> Consolidated plan from all previous plans. Source: implementation-status, tech-stack-quick-wins, ui-ux-improvements.

**Date:** 27 February 2026

---

## Phase 2.5: Modular Permissions (deferred)

| ID | Task | Notes |
|----|------|------|
| A5 | Drop user_roles | Defer until all code uses user_module_roles. Settings still writes to both |
| A10 | scripts/add-user.js, send-quote: use user_module_roles | add-user uses user_roles; send-quote uses has_crm_access |
| A11 | Regenerate Supabase types | `npx supabase gen types typescript --project-id <REF> > src/integrations/supabase/types.ts` |
| A12 | RLS: leads user = only assigned_to | Optional improvement |

---

## Phase 3: Code Simplicity

| ID | Task |
|----|------|
| 8 | Centralize ad-agency status constants |
| 9 | Extract rowTotal helper |
| 10 | Remove unused renderExtra from EntityToolbar |

---

## Phase 4: Performance

| ID | Task |
|----|------|
| 11 | Lazy-load exportBudgetToExcel |

---

## Phase 5: Frontend

| ID | Task |
|----|------|
| 12 | Add background grain |
| 13 | Update accent color (per UI-UX-improvement-plan — teal/clay, not purple) |

---

## Phase 6: Types

| ID | Task |
|----|------|
| 14 | Regenerate types + remove unsafe casts |

---

## Tech Stack Quick Wins

| # | Task | File |
|---|------|------|
| 1 | Add 300ms debounce to Customers search | `src/pages/Customers.tsx` |
| 2 | Add 300ms debounce to GlobalCommandPalette | `src/components/GlobalCommandPalette.tsx` |
| 3 | Update maestro.config.json to Supabase | `maestro/maestro.config.json` |
| 4 | Split Leads.tsx into smaller components | Optional — LeadsToolbar, LeadsBulkActionsBar, LeadTableSection |

---

## UI/UX Improvements (from 2025-02-21-ui-ux-improvements)

### Phase 1: Typography & Colors
- Task 1: Add DM Serif Display font, typography variables
- Task 2: Add accent-action (teal) + semantic colors to CSS
- Task 3: Expose accent-action in Tailwind config
- Task 4: Add accent button variant
- Task 5–7: Replace hardcoded teal in Leads, LeadsEmptyState, LeadCard

### Phase 2: Backgrounds & Depth
- Task 8: Add subtle gradient to body background
- Task 9: Add card-enter, slide-in-right keyframes
- Task 10: Staggered reveal for StatsCards
- Task 11: Enhance Auth page background
- Task 12–13: Hover shadow LeadCard, DealCard

### Phase 3: UX Polish
- Task 14: Improve LeadsEmptyState hierarchy
- Task 15: Stagger Dashboard sections
- Task 16: Improve Sidebar active state and spacing
- Task 17: Build + lint verification

---

## Recommended priority order

1. **Critical:** A11 (types) if there are type issues
2. **Quick:** Tech Stack 1–3 (debounce, maestro config)
3. **Code improvement:** Phase 3 (8, 9, 10)
4. **Performance:** Phase 4 (11)
5. **Design:** Phase 5 + UI/UX as needed
