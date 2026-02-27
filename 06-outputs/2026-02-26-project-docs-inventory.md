# Project Docs Inventory — Relevant for Vault Management

> **Date:** 2026-02-26  
> **Purpose:** Documents describing projects and/or decisions that can be managed in the vault (02-projects)

---

## hadaryaCRM

**Path:** `~/.gemini/antigravity/projects/hadaryaCRM`

| Document | Location | Type | Relevant for vault |
|----------|----------|------|---------------------|
| README | root | Description | ✅ — basic technologies |
| UI-UX-improvement-plan | docs/ | Plan | ✅ — design direction, decisions |
| entity-page-unification-plan | docs/ | Plan | ✅ |
| CURSOR-MCP-SETUP | docs/ | setup | ✅ — Cursor settings |
| security-audit-2025-02-23 | docs/ | Decisions | ✅ |
| security-audit-2025-02-23-follow-up | docs/ | Decisions | ✅ |
| plans/* | docs/plans/ | ~35 plans | ✅ — index or move key ones |

---

## cms

**Path:** `~/.gemini/antigravity/projects/cms`

| Document | Location | Type | Relevant for vault |
|----------|----------|------|---------------------|
| CODEBASE | root | Architecture | ✅ — monorepo structure |
| README | root | Description | ✅ |
| ARCHITECTURE | docs/ | Architecture | ✅ — Cache, Manifest, Versioning |
| ADD_NEW_WEBSITE_GUIDE | docs/ | Guide | ✅ |
| CONTENT_CLUSTER_MASTER_PLAN_2026 | docs/ | Plan | ✅ |
| CONTENT_SECTIONS_INFLATION_AND_MARKET_RISK | docs/ | Decisions | ✅ |
| SECURITY_AUDIT_REPORT_2026-02 | docs/ | Decisions | ✅ |
| TASKS | docs/ | Tasks | ✅ |
| ~60 more documents | docs/ | guides, audits | Index only |

---

## proposal-generator

**Path:** `~/.gemini/antigravity/projects/proposal-generator`

| Document | Location | Type | Relevant for vault |
|----------|----------|------|---------------------|
| README | root | Description | ✅ |
| plans/* | docs/plans/ | Plans | ✅ — index |

---

## smart-volume-radar

**Path:** `~/.gemini/antigravity/projects/smart-volume-radar`

| Document | Location | Type | Relevant for vault |
|----------|----------|------|---------------------|
| README | root | Description | ✅ — Features, Quick Start |
| PLAN-hardening | root | Plan | ✅ |
| CALCULATIONS | docs/ | Specific | ✅ — RVOL formulas, stocks |
| INDICATOR_SOURCES | docs/ | Specific | ✅ |
| MESSAGE_GUIDE | docs/ | Specific | ✅ |
| plans/* | docs/plans/ | Plans | ✅ — index |

---

## website

**Path:** `~/.gemini/antigravity/projects/website`

| Document | Location | Type | Relevant for vault |
|----------|----------|------|---------------------|
| README | root | Description | ✅ |
| xsheva-rebranding-plan | root | Decisions/Plan | ✅ — Brand, Critical Decisions |
| aka-agency-website | root | Plan | ✅ |

---

## source6681

**Path:** `~/.gemini/antigravity/projects/source6681`

| Document | Location | Type | Relevant for vault |
|----------|----------|------|---------------------|
| README | root | Description | ✅ — Lovable project |
| 2026-02-23-project-review-consolidated | docs/ | Review | ✅ — Architecture, Security, Gaps |
| vercel-react-best-practices-audit | docs/ | Audit | ✅ |
| CLOUDFLARE_DNS_FIX | docs/ | fix | ✅ |
| plans/* | docs/plans/ | Plans | ✅ — index |

---

## Proposed vault structure: 02-projects/[project]/

```
02-projects/
├── project.[name].md          # Brief (exists)
├── README.md                  # Index of all projects (exists)
└── [project-name]/            # Project folder — key documents
    ├── README.md              # Index of documents in project
    ├── architecture.md        # Architecture (if relevant)
    ├── decisions.md           # Key decisions
    ├── plans/                 # Plans (or link to docs/plans in project)
    └── [specific-docs]        # As needed
```

**Options:**
1. **Index only** — README in vault that points to file paths in the project
2. **Copy** — Key documents copied to vault (single source of truth)
3. **Symlinks** — Link from vault to project files (read-only)

---

## Recommendation

- **Brief + Links** — project.[name].md contains description, Tech Stack, Workflow. "Docs" section with table of documents and paths.
- **Critical documents** — architecture, key decisions, strategic plans — copy to 02-projects/[project]/ if you want to manage in the vault.
- **Many plans** — Index in README, no copy (stay in project).
