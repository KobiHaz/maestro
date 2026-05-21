# cms — Project Context

React + TypeScript CMS monorepo. Comparison/affiliate content sites with component versioning, Firebase backend, multi-vertical (goldira, weightloss).

**Stack:** React 19 + TypeScript + Vite + Tailwind v3.4 + TanStack Query + Firebase + pnpm + Turbo

---

## Quick Start

```sh
pnpm install
cp apps/frontend/.env.example apps/frontend/.env.local
pnpm dev             # goldira — port 5174
pnpm dev:weightloss  # weightloss vertical
pnpm test            # Vitest
```

Admin Panel: Firebase hosting URL `/admin`

---

## Monorepo Structure

```
apps/
  frontend/     → React SPA (all verticals, domain-resolved)
  functions/    → Firebase Cloud Functions
packages/
  shared/       → @cms/shared — shared components + utils
  vertical-configs/{verticalId}/
    config/vertical.json  → id, name, domain, domainAliases
```

---

## Data Architecture

### Homepage Payload Flow

```
Request → getHomepagePayload (Cloud Fn)
  1. Read aggregated_payloads/{segmentId|'default'}
  2. If valid → return (source: 'aggregated')   ← fast path
  3. If missing/invalid → build live from component_versions (source: 'live')
```

### Firestore Structure

```
verticals/{verticalId}/
  aggregated_payloads/{targetId}            ← pre-built homepage (O(1))
  component_versions/{versionId}            ← shared (footer, header, products)
  segments/{segmentId}/
    component_versions/{versionId}          ← segment overrides (hero, slots)
  settings/{settingId}
aggregation_queue/{verticalId}_{segmentId}  ← debounce queue
admin_user/{docId}                          ← admin auth (NOT 'admin')
```

### Component Storage Rules

| Level | Path | Components |
|-------|------|------------|
| Vertical (shared) | `verticals/{vid}/component_versions` | footer, header, products, sticky_bar |
| Segment override | `verticals/{vid}/segments/{sid}/component_versions` | slots, hero, content_sections, carousel |

Fetch: segment first (if in `SEGMENT_OVERRIDABLE_COMPONENTS`), else vertical.

### Component Versioning Lifecycle

`draft → published → archived`

Service: `componentVersionService.ts` — `getActiveComponentData`, `saveToDraft`, `publishDraft`, `duplicateVersion`, `archiveVersion`

---

## Security Issues (Open)

| Severity | Issue | File | Fix |
|----------|-------|------|-----|
| Critical | Postback No HMAC | `postbackHandler.ts` | Implement HMAC per POSTBACK_HMAC_DESIGN.md |
| High | Admin collection mismatch | `adminEmails.ts:29` | Change `'admin'` → `'admin_user'` |
| High | `report-error` not wired | `firebase.json` | Add rewrite for `/api/report-error` |
| High | No rate limit on postback | — | Add 200 req/min per IP |
| Medium | CORS too permissive | `registerClickEvent` | Restrict to ALLOWED_ORIGINS |

---

## Core Rules

1. **Never normalize in components** — normalization via `smartNormalizeFromFirestore()` at the edge only
2. **O(1) lookups only** — use `Map`; never `.find()` inside loops
3. **No fake defaults, no cross-vertical fallbacks** — zero tolerance
4. **Admin collection is `admin_user`** — not `admin` (historical mismatch)
5. **Firestore snake_case** — all DB fields; `smartNormalizeFromFirestore` converts to camelCase
6. **Segment before vertical** — always check `SEGMENT_OVERRIDABLE_COMPONENTS` before vertical path
7. **TanStack Query for server state** — not manual useEffect + setState
8. **Add new vertical via checklist** — see `.claude/knowledge/add-new-vertical.md`

---

## Reference

- [Architecture & data flow](.claude/knowledge/architecture.md)
- [Firestore collections](.claude/knowledge/database.md)
- [Security audit](.claude/knowledge/security.md)
- [Add new vertical](.claude/knowledge/add-new-vertical.md)
