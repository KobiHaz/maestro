# hadaryaCRM — Comprehensive Project Audit

**Date:** 1 March 2026  
**Project:** Demo CRM — Vite + React + TypeScript + Supabase + TanStack Query  
**Type:** WEB  
**Source:** Maestro project-deep-audit — explorer, security-sentinel, performance-oracle, architecture-strategist, code-simplicity-reviewer, **data-flow (explorer Mapping Mode + React performance checker)**

---

## Sources Used

- `02-projects/hadaryaCRM/project.hadaryaCRM.md`
- `04-knowledge/reference/hadaryaCRM-*.md` (architecture, security, entity unification, UI/UX, MCP)
- `04-knowledge/standards/hadaryaCRM-standards.md`
- Security scan: `03-agents/skills/vulnerability-scanner/scripts/security_scan.py`
- React performance checker: `03-agents/skills/nextjs-react-expert/scripts/react_performance_checker.py`
- Explorer agent (Mapping Mode): data-flow tracing per `03-agents/specialists/explorer-agent.md`
- Project docs: `hadaryaCRM/docs/PERFORMANCE_REPORT.md`, `hadaryaCRM/docs/hadaryaCRM-security-audit.md`

---

## Executive Summary

| Aspect | Score | Key Findings |
|--------|-------|--------------|
| **Architecture** | Good | Unified Entity pattern; no central API layer |
| **Security** | Good (recent fixes) | escapeIlike/escapeHtml ✓; P1 send-quote & payment-proofs **FIXED**; 1 critical (scripts) |
| **Performance** | Needs work | 3 chunks >500KB; ExcelJS 938KB; no React.memo |
| **Code quality** | Medium | No tests; TypeScript non-strict; large pages (Leads ~866 lines) |
| **Documentation** | Basic | README short; JSDoc partial; Maestro up to date |
| **Data flow** | Good (Dashboard) | Dashboard parallel; AdAgencyProjectDetail has minor waterfall |

---

## 1. Discovery — Project Structure

### 1.1 Tech Stack

| Category | Packages |
|----------|----------|
| **Core** | React 18, react-router-dom |
| **Backend** | @supabase/supabase-js |
| **State** | TanStack Query, react-hook-form, zod |
| **UI** | shadcn/ui (Radix), Tailwind |
| **Extras** | @dnd-kit, recharts, exceljs, cmdk, Sentry |

### 1.2 Entity Pattern

| Page | Shell | Toolbar | Kanban | Table | Saved views |
|------|-------|---------|--------|-------|-------------|
| Leads | ✓ | ✓ | ✓ | ✓ | ✓ |
| Deals | ✓ | ✓ | ✓ | ✓ | ✓ |
| Quotes | ✓ | ✓ | ✓ | ✓ | — |
| DesignRequests | ✓ | ✓ | ✓ | ✓ | — |
| AdAgencyProjects | ✓ | ✓ | ✓ | ✓ | — |

### 1.3 Gaps

- **Ad Agency (Tasks, Items, Clients)** — EntityToolbar only; no Shell/Kanban
- **Saved views** — Leads and Deals only; Quotes and DesignRequests lack
- **No route guard** — Users can navigate to `/ad-agency` without module access (sidebar hides links; RLS enforces data)

---

## 2. Security

### 2.1 Verified ✓

| Item | Status |
|------|--------|
| escapeIlike for all ILIKE | ✓ (Leads, Customers, GlobalCommandPalette, LeadDialog) |
| escapeHtml in send-quote | ✓ |
| No hardcoded secrets in app code | ✓ |
| Route protection (ProtectedLayout) | ✓ |
| RLS on tables | ✓ |
| **send-quote** uses `user_module_roles` | ✓ (fixed 2026-03-01) |
| **payment-proofs** bucket + RLS | ✓ (migration `20260301120000_payment_proofs_bucket.sql`) |

### 2.2 Critical (P1)

| # | Finding | Action |
|---|---------|--------|
| 1 | **scripts/add-ad-agency-users.js** — hardcoded email/password pairs (ori@harsinai.co.il, kobi@leadslords.com) | Move to env; use `add-user.js` with env vars |
| 2 | **scripts/seed-admin-and-leads.sql** — contains password reference | Remove or move to .gitignore; use fix-password.sql with env |

### 2.3 High (P2)

| # | Finding | Action |
|---|---------|--------|
| 3 | send-quote no input validation | Add Zod schema for request body |
| 4 | CORS `Access-Control-Allow-Origin: *` in Edge Functions | Restrict to known origins in production |
| 5 | Storage DELETE uses legacy `has_role` | Update to `has_module_admin` |
| 6 | **11 npm vulnerabilities** (6 high: react-router-dom, glob, minimatch, etc.) | Run `npm audit fix`; upgrade react-router-dom |
| 7 | **chart.tsx** — `dangerouslySetInnerHTML` (theme/config; low risk) | Document as intentional; config not user-supplied |

### 2.4 Medium (P3)

| # | Finding | Action |
|---|---------|--------|
| 8 | No module-level route guard for ad-agency | Add redirect in DashboardLayout if path.startsWith("/ad-agency") && !canAccessModule("ad_agency") |
| 9 | Limited Zod usage (only DealDialog) | Extend to Lead, Customer, Quote forms |
| 10 | No security headers config (CSP, HSTS) | Add in vite build or hosting config |

### 2.5 Security Scan Output

```
Status: [!!] CRITICAL ISSUES FOUND
DEPENDENCIES: 6 high (npm audit); yarn/pnpm lock missing (project uses npm — low impact)
SECRETS: scripts/add-ad-agency-users.js, run-seed-migration.js (docs/placeholder)
CODE_PATTERNS: dangerouslySetInnerHTML in chart.tsx (app-defined config — low risk)
CONFIG: No security headers (medium)
```

---

## 3. Performance

### 3.1 Bundle Size (Current Build)

| Chunk | Size | Cause |
|-------|------|-------|
| exceljs.min | 938 KB | ExcelJS in exportBudgetToExcel |
| index | 625 KB | React, Supabase, Radix, Sentry |
| Dashboard | 404 KB | recharts |
| Deals | 82 KB | — |
| Leads | 44 KB | — |

### 3.2 Quick Wins

| Action | Impact |
|--------|--------|
| Dynamic import for ExcelJS in exportBudgetToExcel | −200KB+ on ProjectDetail |
| `loading="lazy"` + width/height on images | CLS, LCP |
| React.memo on LeadCard, DealCard, ProductCard | Fewer re-renders |
| useCallback for setTimeRange in DashboardContext | Fewer re-renders |
| DB indexes for op_*, deals | Faster queries |

### 3.3 Strengths

- TanStack Query with queryKey, enabled, staleTime
- Route-level lazy loading with Suspense
- useMemo/useCallback in tables
- Existing indexes on leads, customers, quotes

---

## 4. Architecture

### 4.1 Inconsistencies

- **Ad Agency** — Tasks, Items, Clients use EntityToolbar only
- **Saved views** — Only Leads and Deals
- **Query keys** — No central `query-keys.ts`; mixed styles
- **useTablePreferences vs useColumnVisibility** — Clarify roles or unify

### 4.2 Technical Debt

1. **Large pages** — Leads.tsx ~866 lines; Quotes.tsx ~500+
2. **No services layer** — Supabase calls from components
3. **ROUTE_MAP** — Missing Ad Agency paths
4. **EntityKanbanColumn** — Exported but unused externally

### 4.3 Recommendations

1. `src/lib/query-keys.ts` with factories
2. `useEntityTablePreferences` shared for Leads, Deals
3. `services/` or `api/` layer for Supabase
4. Split Leads.tsx into hooks and subcomponents

---

## 5. Code Quality & Tests

### 5.1 Tests

| Type | Status |
|------|--------|
| Unit/Integration | ❌ No Vitest/Jest |
| E2E | ❌ No Playwright |
| Test files | ❌ None |

**Recommendation:** Add Vitest; Playwright for critical flows.

### 5.2 TypeScript

| Option | Current | Recommended |
|--------|---------|-------------|
| strict | false | true |
| noImplicitAny | false | true |
| strictNullChecks | false | true |

### 5.3 Error Handling

- Sentry + ErrorBoundary ✓
- try/catch + toast ✓
- **Missing:** handleExportExcel in AdAgencyProjectDetail — no catch; errors don’t reach user

---

## 6. Recommendations (Prioritized)

### P0 — Critical

| # | Area | Action |
|---|------|--------|
| 1 | Security | Remove hardcoded credentials from add-ad-agency-users.js; use env |
| 2 | Performance | Dynamic import ExcelJS in exportBudgetToExcel |
| 3 | Quality | Add Vitest and first tests |
| 4 | Quality | Enable TypeScript strict (or gradual) |

### P1 — High

| # | Area | Action |
|---|------|--------|
| 5 | Security | Zod for send-quote; restrict CORS |
| 6 | Security | npm audit fix |
| 7 | Performance | `loading="lazy"` + dimensions on images |
| 8 | Performance | React.memo on Card components |
| 9 | Quality | catch for handleExportExcel; QueryClient default onError |
| 10 | Architecture | query-keys.ts; useEntityTablePreferences |

### P2 — Medium

| # | Area | Action |
|---|------|--------|
| 11 | Security | Route guard for ad-agency module |
| 12 | Performance | DB indexes for op_*, deals |
| 13 | Performance | Lazy-load recharts; manualChunks |
| 14 | **Data flow** | AdAgencyProjectDetail: enable sections with `!!id` only (sections are global) |
| 15 | Architecture | services layer; split Leads.tsx |
| 16 | Quality | README; JSDoc for hooks |

### P3 — Low

| # | Area | Action |
|---|------|--------|
| 17 | General | ROUTE_MAP for Ad Agency |
| 18 | General | Remove unused EntityKanbanColumn export |
| 19 | Security | Extend Zod to more forms |
| 20 | A11y | ARIA and labels audit |

---

## 7. Data Flow (explorer-agent Mapping Mode + React performance checker)

**Agent:** explorer-agent (Mapping Mode — traces data flow from entry points to data stores) + `react_performance_checker.py` (waterfalls, barrel imports, memoization)

### 7.1 React Performance Checker Output

```
SUMMARY: Critical Issues: 0 | Warnings: 0
[SUCCESS] No major performance issues detected!
```

No sequential `await` patterns, barrel imports, or missing dynamic imports flagged by the script.

### 7.2 Dashboard Data Flow

```
Dashboard (DashboardProvider)
├── timeRange state → StatsCards (used for date range)
├── StatsCards     → useQuery(["dashboard-stats", timeRange, role, userId])
│                    └── Promise.all([leads, deals, quotes, currDeals, prevDeals]) ✓ parallel
├── OrdersChart    → useQuery(["deals-by-month", assignedTo]) ✓ independent
├── LeadsBySourceChart → useQuery(["leads-by-source", assignedTo]) ✓ independent
├── ActivityFeed   → useQuery(["recent-activity", assignedTo])
│                    └── Promise.all([leads, quotes, deals]) ✓ parallel
└── QuickActions   → static links
```

**Finding:** All Dashboard components use TanStack Query with parallel fetches. StatsCards, OrdersChart, LeadsBySourceChart, ActivityFeed run **in parallel** when mounted. No waterfall.

**Note:** OrdersChart and LeadsBySourceChart do **not** use `timeRange`; only StatsCards does. Charts show all-time or unfiltered data — intentional or oversight.

### 7.3 AdAgencyProjectDetail Data Flow (Waterfall)

```
project (useQuery, enabled: !!id)
   ↓ waits
projectItemsForExport (enabled: !!id && !!project) ──┬── parallel once project exists
sections (enabled: !!id && !!project) ──────────────┘
```

**Waterfall:** `project` must resolve before `projectItemsForExport` and `sections` run. **Optimization:** `op_budget_sections` is global — could run with `enabled: !!id` (no project dependency). Would save ~1 round-trip.

### 7.4 Leads Page (leadQuotes dependency)

```
leadsData (useQuery)
   ↓ leadIds from visible leads
leadQuotes (useQuery, enabled: leadIds.length > 0)
```

**Intentional waterfall:** leadQuotes depends on leadIds from leadsData. Batched by leadIds to avoid N+1. OK per design.

### 7.5 Recommendations (Data Flow)

| Priority | Finding | Action |
|----------|---------|--------|
| P2 | AdAgencyProjectDetail: sections waits for project | Change sections `enabled` to `!!id`; sections are global |
| P3 | Dashboard charts don’t filter by timeRange | Consider adding timeRange to OrdersChart/LeadsBySourceChart if UX requires |

---

## 8. Knowledge Gaps

- [x] Create/update `04-knowledge/reference/hadaryaCRM-architecture.md` with current entity layout (2026-03-02: Performance section added; LeadDialogsOrchestrator, normalize, useLeads)
- [x] Update `04-knowledge/reference/hadaryaCRM-security-audit.md` with P1 fixes and new script findings (2026-03-01, 2026-03-02)

---

## 9. Next Steps

1. **Immediate:** Move add-ad-agency-users.js credentials to env; run npm audit fix
2. **Short term:** Dynamic import ExcelJS; Zod for send-quote; route guard for ad-agency
3. **Medium term:** Vitest setup; TypeScript strict; split Leads.tsx; services layer

---

## 10. Summary

hadaryaCRM is a solid CRM with a consistent Entity pattern and an Ad Agency module. Strengths: input security (escapeIlike, escapeHtml), TanStack Query, and recent fixes for send-quote (user_module_roles) and payment-proofs bucket. Main gaps: hardcoded credentials in scripts, bundle size (ExcelJS), no tests, and TypeScript non-strict. **Data flow:** Dashboard fetches are parallel; AdAgencyProjectDetail has a minor waterfall (sections could run with project). Priority fixes: remove credentials from scripts, dynamic-import ExcelJS, add Vitest, and tighten npm dependencies.

---

*Generated by Maestro project-deep-audit — 1 March 2026*  
*Agents: explorer, security-sentinel, performance-oracle, architecture-strategist, code-simplicity-reviewer, data-flow (explorer Mapping Mode + react_performance_checker)*
