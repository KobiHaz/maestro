# Documentation Audit Report

> **Date:** 2026-02-26  
> **Scope:** 6 projects under `~/.gemini/antigravity/projects/`  
> **Method:** Read documents, cross-reference with code, verify paths and architectural claims

---

## Per-project summary

| Project | Docs audited | OUTDATED | REDUNDANT | OBSOLETE | KEEP | Priority fixes |
|---------|--------------|----------|-----------|----------|------|----------------|
| **cms** | 70+ docs | 8 | 3 | 2 | ~55 | domains.json, products conflict, CODEBASE index |
| **hadaryaCRM** | 26 docs | 4 | 0 | 0 | 22 | README naming, Supabase in brief |
| **proposal-generator** | 8 docs | 1 | 0 | 0 | 7 | README project structure |
| **smart-volume-radar** | 6 docs | 1 | 0 | 0 | 5 | PLAN vs README config |
| **website** | 3 docs | 0 | 0 | 1 | 2 | Archive aka-agency |
| **source6681** | 8 docs | 0 | 0 | 1 | 7 | Replace boilerplate README |

---

## Detailed findings (project by project)

### 1. cms

**Root docs**

| Document | Status | Notes |
|----------|--------|-------|
| CODEBASE.md | OUTDATED | Security index points to `docs/archive/SECURITY_AUDIT_REPORT.md`; current audit is `docs/SECURITY_AUDIT_REPORT_2026-02.md`. Doc references `maestro/`, `.agent/` — verify these exist. |
| README.md | KEEP | Stack, scripts, structure accurate. Uses `pnpm` correctly. |

**docs/ — architecture & guides**

| Document | Status | Notes |
|----------|--------|-------|
| ARCHITECTURE.md | KEEP | Cache layers, manifest pattern, versioning match code. Paths `homepageService.ts`, `manifestService.ts` verified. |
| ADD_NEW_WEBSITE_GUIDE.md | OUTDATED | **Critical:** Steps 4, 7–9, checklist reference `configs/domains.json`. Code does not use it; MULTI_SITE_CMS_PERFECTION_PLAN notes "Not used by any code". Domain resolution uses Firestore `verticals` + `vertical-configs/*/config/vertical.json` via `verticalResolutionService.ts`. |
| COMPONENT_STORAGE_ARCHITECTURE.md | OUTDATED | Lists `products` under "Segment-Level Components (Can Have Overrides)". Code: `adminRegistry.ts` excludes `products` from `SEGMENT_OVERRIDABLE_COMPONENTS` — products are vertical-level only. |
| COMPONENT_STORAGE_ARCHITECTURE.md | REDUNDANT | Overlaps with ARCHITECTURE.md manifest section; minor redundancy. |
| ENVIRONMENT_SETUP.md | OUTDATED | Uses `npm run dev`; project uses `pnpm`. |
| SECURITY_AUDIT_REPORT_2026-02.md | KEEP | Accurate; findings reference correct paths. |
| CONTENT_SECTIONS_INFLATION_AND_MARKET_RISK.md | KEEP | Content-replacement guidance; no code claims. |
| TASKS.md | KEEP | Task tracking; no verification needed. |
| LOCALHOST_AND_PRODUCTION.md | KEEP | Env behavior. |

**docs/ — verification & audits** (sampled)

| Document | Status | Notes |
|----------|--------|-------|
| CACHE_SYSTEM_DOCUMENTATION.md | KEEP | Aligns with homepageService. |
| PATTERN_AND_ANTIPATTERN_ANALYSIS.md | KEEP | References verified. |
| MULTI_SITE_CMS_PERFECTION_PLAN.md | KEEP | Correctly states domains.json unused. |
| FIRESTORE_COLLECTIONS_ORGANIZATION.md | REDUNDANT | Overlaps with ARCHITECTURE + COMPONENT_STORAGE. |
| FUNCTIONS_AUDIT.md | KEEP | Functions audit. |

**docs/archive/**

| Document | Status | Notes |
|----------|--------|-------|
| SECURITY_AUDIT_REPORT.md | OBSOLETE | 2025 report on Secrets/CORS; superseded by SECURITY_AUDIT_REPORT_2026-02.md. |
| Multiple PLAN-*, FIX_* | ARCHIVE | Historical; correctly in archive. |

**Plans**

| Document | Status | Notes |
|----------|--------|-------|
| docs/plans/2026-02-23-audit-remediation-p0-p1.md | KEEP | Remediation plan. |

---

### 2. hadaryaCRM

| Document | Status | Notes |
|----------|--------|-------|
| README.md | OUTDATED | Title "Demo CRM"; project is hadaryaCRM (Xsheva CRM). Tech stack omits **Supabase**; code uses Supabase extensively. |
| docs/UI-UX-improvement-plan.md | OUTDATED | References "Demo CRM" and "furniture"; project pivoted to ad-agency/production workflows. Design direction may still apply but terminology is stale. |
| docs/entity-page-unification-plan.md | KEEP | EntityPageShell at `src/components/entity-page/EntityPageShell.tsx` exists; phases 1–5 marked complete. Correct. |
| docs/security-audit-2025-02-23*.md | KEEP | Audit findings. |
| docs/CURSOR-MCP-SETUP.md | KEEP | Setup guide. |
| docs/plans/* | KEEP | Implementation plans; paths verified. |
| docs/01-me/* | KEEP | Identity/tools/writing — generic agent context. |

---

### 3. proposal-generator

| Document | Status | Notes |
|----------|--------|-------|
| README.md | OUTDATED | Project Structure omits `LoginPage.tsx`, `MyProposalsPage.tsx` (Firebase auth + saved proposals). README lists `QuotePage`, `QuoteForm`, etc. — structure is otherwise correct. |
| docs/plans/* | KEEP | Firebase implementation, four-tabs design — accurate. |

---

### 4. smart-volume-radar

| Document | Status | Notes |
|----------|--------|-------|
| README.md | KEEP | Quick Start, Google Sheet watchlist, config table, project structure verified. |
| PLAN-hardening.md | OUTDATED | Step 3 says "Merge watchlist.json and sectors.json into tickers.json"; project uses Google Sheet + `src/config/` (israeliNames.json). No `tickers.json`. Either hardening reverted or config approach changed; README is source of truth. |
| docs/CALCULATIONS.md | KEEP | RVOL, SMA, price change formulas — accurate. |
| docs/INDICATOR_SOURCES.md | KEEP | Fetch vs calculate. |
| docs/MESSAGE_GUIDE.md | KEEP | Report format. |
| docs/plans/* | KEEP | Code quality hardening. |

---

### 5. website

| Document | Status | Notes |
|----------|--------|-------|
| README.md | KEEP | Xsheva stack, structure (xsheva/), scripts correct. |
| xsheva-rebranding-plan.md | KEEP | 100% complete; live at website-xsheva.web.app. |
| aka-agency-website.md | OBSOLETE | AKA Agency plan superseded by Xsheva rebrand. Folder `aka-agency/` not present; project uses `xsheva/`. |

---

### 6. source6681

| Document | Status | Notes |
|----------|--------|-------|
| README.md | OBSOLETE | Generic Lovable boilerplate with "REPLACE_WITH_PROJECT_ID". Project is React + Vite + Supabase e‑commerce. |
| docs/2026-02-23-project-review-consolidated.md | KEEP | Architecture, security, performance — accurate. |
| docs/vercel-react-best-practices-audit.md | KEEP | Audit findings. |
| docs/CLOUDFLARE_DNS_FIX.md | KEEP | Fix notes. |
| docs/plans/* | KEEP | Admin isolation, grid view, security plans. |

---

## ✅ Fixes Applied (2026-02-26)

- P0: ADD_NEW_WEBSITE_GUIDE (domains.json → Firestore/vertical.json)
- P0: COMPONENT_STORAGE_ARCHITECTURE (products removed from segment overrides)
- P0: CODEBASE (security audit link, maestro refs)
- P1: ENVIRONMENT_SETUP (npm → pnpm)
- P1: hadaryaCRM README (hadaryaCRM, Supabase)
- P1: hadaryaCRM UI-UX-improvement-plan (terminology update)
- P1: proposal-generator README (LoginPage, MyProposalsPage, Firebase auth)
- P1: smart-volume-radar PLAN-hardening (Step 3 clarified)
- P1: source6681 README (replaced Lovable boilerplate)
- Archived: website/aka-agency-website.md → docs/archive/

---

## Action items (prioritized)

### DELETE (low value, confusing)

1. None — prefer ARCHIVE for historical docs.

### ARCHIVE

1. **website/aka-agency-website.md** → `website/docs/archive/aka-agency-website.md` — superseded by Xsheva rebrand.
2. **cms/docs/archive/SECURITY_AUDIT_REPORT.md** — ensure CODEBASE stops linking here; 2026 report is canonical.

### FIX (update content)

| Priority | Project | Document | Fix |
|----------|---------|----------|-----|
| P0 | cms | ADD_NEW_WEBSITE_GUIDE.md | Remove Step 4 (domains.json), Steps 7–9 domain mapping references. Add note: domain resolution from Firestore `verticals` + vertical.json `domain`; `configs/domains.json` is optional/legacy. |
| P0 | cms | COMPONENT_STORAGE_ARCHITECTURE.md | Remove `products` from "Segment-Level Components (Can Have Overrides)" — products are vertical-level only per adminRegistry. |
| P0 | cms | CODEBASE.md | Change Security index to `docs/SECURITY_AUDIT_REPORT_2026-02.md`. |
| P1 | cms | ENVIRONMENT_SETUP.md | Replace `npm` with `pnpm` in commands. |
| P1 | hadaryaCRM | README.md | Rename to hadaryaCRM, add Supabase to stack. |
| P1 | hadaryaCRM | docs/UI-UX-improvement-plan.md | Update "Demo CRM" → hadaryaCRM; clarify if furniture context still applies or mark as legacy. |
| P1 | proposal-generator | README.md | Add LoginPage, MyProposalsPage to project structure; mention Firebase auth/saved proposals. |
| P1 | smart-volume-radar | PLAN-hardening.md | Clarify Step 3: if tickers.json was reverted, note "Google Sheet remains source; config consolidation deferred." |
| P1 | source6681 | README.md | Replace Lovable boilerplate with project-specific intro (React + Vite + Supabase e‑commerce, admin, wishlist, WhatsApp inquiry). |

### KEEP (no changes)

- cms: ARCHITECTURE.md, SECURITY_AUDIT_REPORT_2026-02.md, CACHE_SYSTEM_DOCUMENTATION.md, LOCALHOST_AND_PRODUCTION.md, most verification docs.
- hadaryaCRM: entity-page-unification-plan, security audits, CURSOR-MCP-SETUP, plans.
- proposal-generator: plans.
- smart-volume-radar: README, CALCULATIONS, INDICATOR_SOURCES, MESSAGE_GUIDE.
- website: README, xsheva-rebranding-plan.
- source6681: project-review, vercel audit, CLOUDFLARE_DNS_FIX, plans.

---

## Recommendations

1. **cms domains.json**: Decide formally — remove from ADD_NEW_WEBSITE_GUIDE or document as optional/legacy. Code does not use it; verticalResolutionService reads Firestore + vertical.json only.
2. **Single source of truth for segment overrides**: Use `adminRegistry.ts` `SEGMENT_OVERRIDABLE_COMPONENTS` as canonical; update COMPONENT_STORAGE_ARCHITECTURE and ARCHITECTURE to stay aligned.
3. **Project naming**: hadaryaCRM README and UI-UX plan still say "Demo CRM"; align with project brief in vault.
4. **source6681 README**: High impact — replace Lovable boilerplate with real project description; improves onboarding and AI context.
5. **docs index**: Consider a `docs/README.md` in cms with a table of canonical docs and their purposes to reduce redundancy and drift.
6. **Plans index**: For projects with many plans (hadaryaCRM ~25, cms ~60+), maintain a simple index (e.g. `docs/plans/README.md`) with date, title, status — avoid duplicating in vault.
