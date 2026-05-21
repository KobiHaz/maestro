# casino-funnels — Master Plans & Tasks

**Project:** LuckyMint (`https://www.luckymint.co`)
**Last updated:** 2026-04-30
**Overall progress:** ~15% (Wave 1 P0 security not yet started)

---

## ✅ Done

Items confirmed shipped based on audit progression and memory.md.

| Date | Item | Notes |
|------|------|-------|
| 2026-04-08 | Analytics consolidated to `Analytics.tsx` — removed duplicate `index.html` init | Post-audit hardening |
| 2026-04-08 | `VITE_REQUIRE_ANALYTICS_CONSENT=true` in production | Consent gate for GA4 / Meta / Clarity |
| 2026-04-08 | Affiliate link validation — HTTPS + `ALLOWED_AFFILIATE_HOSTS` allowlist | Prevents open redirect |
| 2026-04-08 | Age compliance aligned to 19+ across Terms | Crown Coins requirement |
| 2026-04-13 | `VITE_LEAD_LOG_WEBHOOK_TOKEN` removed from client bundle | Was baked into public JS (SEC-C2) |
| 2026-04-13 | `authToken` URL param removed from `leadTracker.ts` | Token no longer in URLs/logs |
| 2026-04-13 | `detail` field stripped from all 500 responses | Error details no longer leak to client |
| 2026-04-13 | Clarity JWT rotated, stored in 1Password only | Was exp 2126 in `.env.local` |
| 2026-04-13 | `npm update vite picomatch brace-expansion` — 0 audit findings | Cleared HIGH/MEDIUM CVEs |
| 2026-04-13 | CORS partially tightened | `localhost` still leaks (see T5) |
| 2026-04-18 | GA4 key events fixed (`qualify_lead`, `close_convert_lead`, `spin_complete`, `cta_click`) | Was 0 conversions on 372 users |
| 2026-04-18 | Postback → GA4 event mapping: `su→sign_up`, `ftd/qftd→purchase` | Alignment with GA4 standard events |
| —  | D1 database `leads-sunflower` set up + `wrangler.toml` configured | — |
| —  | Migration 0001: `init_leads.sql` applied | — |
| —  | Migration 0002: `postback_log.sql` table added | — |
| —  | Crown branding blocked from social previews | Commit `a9532e7` |
| —  | `/go` redirect endpoint added | Commit `a584790` |
| —  | UTM non-forwarding to Crown | Commit `9937f56` |
| —  | Postback logging added | Commit `cbec50f` |
| —  | `npm audit --audit-level=high` added to CI | — |

---

## 🔴 Open — Wave 1: P0 Security Critical (start here, can run in parallel)

> These are live production issues. Ship before next traffic spike.

### T1 — Enforce `LEAD_WEBHOOK_TOKEN` server-side
- **File:** `functions/api/lead.js` — token documented but never read; endpoint is effectively open
- **Fix:** Read `LEAD_WEBHOOK_TOKEN` from `env`; if missing → 503 (fail-closed); if wrong → 401
- **Verify:** `curl -X POST /api/lead` without token → 401; missing env → 503

### T2 — Fix silent data loss on unknown `eventType` + drop client timestamp
- **File:** `functions/api/lead.js:83` (fallthrough on unknown eventType returns 200); `:116` (trusts `body.timestamp`)
- **Fix:** Replace if/else chain with handler map → 400 on unknown eventType. Always use server `now` for `created_at`
- **Verify:** Unknown eventType → 400; `created_at` always matches server time

### T3 — Fix postback idempotency + correct HTTP status codes
- **File:** `functions/api/postback.js:59` (overwrites timestamps on re-fire); `:95` (non-constant-time comparison); `:98` (auth failure returns 200)
- **Fix:** Add `AND col IS NULL` guard (first-write-wins). Use `crypto.subtle.timingSafeEqual`. Auth failure → 401; missing config → 503; DB error → 500
- **Verify:** Duplicate postback for same `click_id` → timestamps unchanged; auth failure → 401

### T4 — Harden input validation (`leadId` + `sanitizeLeadText`)
- **File:** `functions/api/lead.js:84` (leadId unsanitized); `functions/lib/leadSanitize.js:10` (single injection char, no Unicode bidi)
- **Fix:** Add `sanitizeLeadId()` UUID-format allowlist regex. Fix `sanitizeLeadText`: `[=+\-@]+` and strip Unicode bidi chars
- **Verify:** Non-UUID `leadId` → 400; double injection chars stripped; bidi stripped

---

## 🟠 Open — Wave 2: P1 Hardening (parallel, after Wave 1)

### T5 — Tighten CORS + remove token prefix from postback logs
- **Depends on:** T1
- **File:** `functions/api/lead.js:40` (`localhost` still in allowlist); `functions/api/postback.js:39` (logs token prefix)
- **Fix:** Replace broad allowlist with project-specific preview regex. Remove partial token from `console.warn`
- **Verify:** Request from `localhost` → CORS rejection; log line has no token prefix

### T6 — Fix `markLeadAction` race condition (orphaned lead)
- **File:** `src/lib/leadTracker.ts:365` — UPDATE fires on non-existent row when session has no init
- **Fix:** When `readState()` returns null, fire `sendLeadUpdate(state, 'init')` before the action event
- **Verify:** `spin` on a fresh session creates D1 row before UPDATE fires

### T7 — D1 schema migration 0002 (indexes + constraints)
- **File:** New `migrations/0002_add_indexes_and_constraints.sql`
- **Fix:** UNIQUE INDEX on `click_id`, INDEX on `created_at DESC`, INDEX on `(acquisition_channel, utm_campaign)`, partial indexes on postback timestamps, new columns `meta_event_id` / `postback_*_attempts`
- **Verify:** `npm run db:migrate:local` passes; `EXPLAIN QUERY PLAN` shows index use

### T8 — API performance — merge timing into init, slim payloads
- **Depends on:** T2
- **File:** `src/lib/leadTracker.ts` — 4 round trips per session
- **Fix:** Bundle `timing` fields into `init` payload. Add `toMinimalPayload(leadId, action)` for `spin`/`claim`
- **Verify:** ≤3 API calls per session in network tab; spin/claim payloads ~50–100 bytes

### T10 — Meta Pixel — pass `external_id` for match quality
- **File:** `src/components/Analytics.tsx:117` — `fbq('init', pixelId)` with no user data
- **Fix:** Read `leadId` from sessionStorage; pass `external_id: SHA256(leadId)` in `fbq('init')`
- **Verify:** Meta Pixel Helper shows 64-char SHA-256 `external_id` on init; no raw PII sent

---

## 🟡 Open — Wave 3: P1 Tests (after Wave 2)

### T9 — Test coverage for hardened endpoints
- **Depends on:** T1, T2, T3, T4
- **Fix:** Tests for: unknown `eventType` → 400, invalid `leadId` → 400, duplicate postback idempotency, auth failure → 401, CORS rejection from `localhost`
- **Verify:** `npm run test:api` all green

---

## 🟢 Open — Wave 4: P2 Observability & Reporting

### T11 — Structured perf logs per session
- **Fix:** On `timing` event emit `{ event: 'perf', lead_id, nav_ttfb_ms, nav_dcl_ms, nav_load_ms, … }`. On `spin` emit `{ event: 'spin_timing', spin_latency_ms }`
- **Verify:** `wrangler pages dev` shows structured JSON logs; `spin_latency_ms` is positive int

### T12 — Analytics dashboard (`/api/dashboard` + `/dashboard`)
- **Depends on:** T7
- **Fix:** `functions/api/dashboard.js` protected by `DASHBOARD_PASSWORD`; `src/pages/Dashboard.tsx` at `/dashboard` (only when `VITE_DASHBOARD_ENABLED=true`)
- **Verify:** `GET /api/dashboard` without auth → 401; with password → valid JSON metrics

### T13 — Spin/claim rate analytics in Telegram digest
- **Depends on:** T7, T11
- **Fix:** Extend `daily-insights.mjs` with D1 query block for spin/claim/su rates by channel
- **Verify:** `node scripts/daily-insights.mjs` outputs `spin_rate_pct` + `claim_rate_pct` per channel

---

## 🔴 Open — Security / Infrastructure (from CLAUDE.md)

| ID | Item | Action |
|----|------|--------|
| SEC-M1 | CSP — migrate `unsafe-inline` → nonce-based | Cloudflare Transform Rules to inject nonce |
| SEC-M2 | Rate limiting — WAF rules on `/api/*` | 30 req/min `/api/lead`, 50 req/min `/api/postback` |
| SEC-M4 | Google service account — scope down | Restrict to spreadsheet-level; remove Drive API access |

---

## 🔴 Open — Meta CAPI Plan (0% complete)

> Goal: forward Sunflower postbacks to Meta CAPI for campaign optimization.
> T1 + T4 can start in parallel.

| Task | Description | Depends on |
|------|-------------|------------|
| **T1** | D1 migration — add `capi_su_sent_at`, `capi_ftd_sent_at`, `capi_qftd_sent_at` columns | — |
| **T2** | `sendMetaCAPI` helper in `postback.js` (Workers Web Crypto, fail-closed) | T1 |
| **T3** | Wire CAPI into postback flow with dedup guard | T2 |
| **T4** | Set CF Pages secrets: `META_PIXEL_ID`, `META_CAPI_TOKEN`, `META_TEST_CODE` *(manual)* | — |
| **T5** | E2E test via Meta Test Events + remove `META_TEST_CODE` before going live | T3, T4 |

**Secrets needed:**
- `META_PIXEL_ID` = `1296696345654709`
- `META_CAPI_TOKEN` = system user token (long-lived, from Meta)
- `META_TEST_CODE` = `TEST6753` (temp only — remove after T5)

---

## Execution Order

```
Wave 1 (P0, parallel)  →  T1, T2, T3, T4           security critical
Wave 2 (P1, parallel)  →  T5, T6, T7, T8, T10      hardening + schema + perf
Wave 3 (P1, seq)       →  T9                         tests validate prior changes
Wave 4 (P2, parallel)  →  T11, T12, T13             observability + dashboard

Parallel track         →  SEC-M2 (WAF rate limiting) can be done anytime in CF dashboard
Parallel track         →  Meta CAPI (T1+T4 parallel, then T2→T3→T5)
```

---

## Final Verification Checklist

- [ ] `npm run lint` passes
- [ ] `npm run build` passes — no token in `dist/`
- [ ] `npm run test:api` — all new cases green
- [ ] `npm run test:e2e` — no regressions
- [ ] `npm run db:migrate:local` succeeds
- [ ] Duplicate postback → `click_id` timestamp unchanged on second fire
- [ ] Unknown `eventType` → 400
- [ ] CORS from `localhost` → rejected
- [ ] `GET /api/dashboard` without auth → 401; with password → valid JSON
- [ ] `spin_rate_pct` + `claim_rate_pct` in Telegram digest
- [ ] `spin_latency_ms` in structured logs
- [ ] Meta Pixel Helper shows `external_id` (64-char SHA-256) on init
- [ ] Meta Test Events shows `Lead` event; duplicate postback → no second event
- [ ] `META_TEST_CODE` removed from CF secrets before going live

---

## 🟠 Open — UX Copy Fixes (copy-only, no logic changes)

> Source: `outputs/ux-copy-audit-2026-04-30.md`. All changes are string-only.
> Phase 1 is a prerequisite for any new paid campaign.

### Phase 1 — Critical (≤ 15 min)

- [ ] **`src/content/winOverlayCopy.ts`** — replace 5 strings: `badge → "YOUR PRIZE IS READY"`, `title → 'You Just Won a +150% Welcome Boost'`, `offerTitle → '800,000 Gold Coins + 40 Sweep Coins'`, remove "through the button below", `"T&Cs" → "terms"`, `ctaDisabledLabel → 'Offer currently unavailable'`
- [ ] **`src/components/ComplianceFooter.tsx`** — `Terms of Use` → `Terms of Service`

### Phase 2 — Major (≤ 30 min)

- [ ] **`src/pages/SpinWheel.tsx`** — spin button: `"Spin the wheel"` → `"SPIN NOW"`
- [ ] **`src/pages/SpinWheel.tsx`** — add GC/SC legend below spin button: `GC = Gold Coins · SC = Sweep Coins`
- [ ] **`src/pages/SpinWheel.tsx`** — JACKPOT segment: decide replace with real prize value (e.g. `150% BOOST`) or match overlay copy. Add code comment documenting decision. *(Kobi input needed)*
- [ ] **`src/components/AffiliateOfferCountdown.tsx`** — `'Expires in'` → `'Offer held for'`; `'Opening offer…'` → `'Opening your offer…'`

### Phase 3 — Minor polish (≤ 20 min)

- [ ] **`src/components/TrustpilotInlineRow.tsx`** — `'Last update:'` → `'Last updated:'`
- [ ] **`src/lib/pageMeta.ts`** — OG image alt → title case: `'LuckyMint — Spin the Wheel and See What You Win'`
- [ ] **`src/pages/SpinWheel.tsx`** — SEO description: `'Tap to spin'` → `'Spin now'`
- [ ] **`src/pages/TermsOfService.tsx`** — SEO description → `'Read the Terms of Service for LuckyMint — the independent affiliate prize wheel operated by JoyaAI. Adults 19+ only.'`
- [ ] **`src/pages/PrivacyPolicy.tsx`** — SEO description → `'Learn how JoyaAI handles your data on LuckyMint. Covers analytics, cookies, affiliate links, and your privacy rights.'`

### Phase 4 — Verify

- [ ] `npm run lint` — 0 errors; `npm run build` — clean; manual smoke test on `npm run dev`

---

## Reference

| File | Contents |
|------|---------|
| `knowledge/architecture.md` | Data flow, env vars, GA4 events, Sheets column map |
| `knowledge/standards.md` | Rule examples, test patterns, CF env config |
| `memory.md` | Past decisions and resolved issues |
| `outputs/ux-copy-audit-2026-04-30.md` | Full UX copy audit with rewrites and priority table |
| `06-outputs/2026-04-27-casino-funnels-audit-report.md` (Maestro) | Most recent full audit |
