# Log — 2026-04-13 — Security Hardening Round 2 — Execution

**Plan:** `docs/plans/security-hardening-2.md` (deleted after completion)  
**Status:** All tasks 🟩

## Changes Made

### `functions/api/lead.js`
- `g()` helper hoisted above auth check (DRY)
- Auth now fails closed (503) when `LEAD_WEBHOOK_TOKEN` is missing
- Removed `authToken` URL param from auth check — header-only
- `Access-Control-Allow-Origin` changed from `*` to `https://www.luckymint.co` + `Vary: Origin`
- Error response changed from `{ error: 'sheets_error', detail: <msg> }` to `{ error: 'internal_error' }`

### `functions/api/postback.js`
- Auth now fails closed (logs error, returns `{ ignored: true, reason: 'service_unavailable' }`) when `POSTBACK_TOKEN` is missing

### `src/lib/leadTracker.ts`
- Removed `VITE_LEAD_LOG_WEBHOOK_TOKEN` usage entirely
- Removed `authToken` URL param logic
- Removed `Authorization: Bearer` header from client requests
- `getWebhookConfig()` simplified to `getWebhookUrl()` — returns only URL

### `.env.example`
- Removed `VITE_LEAD_LOG_WEBHOOK_TOKEN` documentation
- Replaced real `VITE_GA_MEASUREMENT_ID` with placeholder `G-XXXXXXXXXX`
- Replaced real `VITE_CLARITY_PROJECT_ID` with placeholder `XXXXXXXXXX`

### `.github/workflows/ci.yml`
- Added `npm audit --audit-level=high` step

### `package.json` / `package-lock.json`
- `npm update vite picomatch brace-expansion` → 0 vulnerabilities

## Verification Results

| Check | Result |
|-------|--------|
| `npm audit --audit-level=high` | ✅ 0 findings |
| `npm run lint` | ✅ 0 errors |
| `npm run build` | ✅ success (409KB bundle) |
| Bundle grep for LEAD_LOG_WEBHOOK_TOKEN | ✅ CLEAN |
| `npm run test:e2e` | ✅ 4/4 passed |

## Remaining Manual Action

**SEC-C1:** `CLARITY_DATA_EXPORT_TOKEN` in `.env.local` is a ~100-year JWT.
- Go to Clarity → Settings → Data Export → revoke the current token → generate new one
- Store in 1Password only (not in any file)
- Update `scripts/daily-insights.mjs` reference if needed
