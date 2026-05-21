---
date: 2026-04-27
project: casino-funnels (LuckyMint)
type: WEB
workflow: workflows/project-deep-audit.md
---

# Project Deep Audit — casino-funnels / luckymint.co

**Repo:** `KobiHaz/casino` · **Live:** https://www.luckymint.co · **Worktree audited:** `adoring-poitras-902ec4` (branch `claude/adoring-poitras-902ec4`, clean)
**Stack:** React 19 + Vite 8 + TS, Tailwind v4, React Router 7, motion 12, Cloudflare Pages + Pages Functions, D1 (`leads-sunflower`).
**Surface:** Single funnel route `/wheel` (CTA → Crown Coins affiliate). Pages Functions: `/api/lead`, `/api/postback`, `/go`, `_middleware` (host redirect + A/B cookie).

## Sources Used
- Project files (read-only, no edits)
- 6 specialist agents run in parallel: `explorer-agent`, `security-auditor`, `backend-specialist`, `frontend-specialist`, `test-engineer`, `general-purpose` (perf+SEO+devops)
- Recent commits: `a9532e7` (block Crown branding from social previews), `a584790` (`/go` redirect), `9937f56` (stop forwarding inbound UTMs), `cbec50f` (postback log)
- Project memory: `project_ga4_open_tasks.md` (Cloudflare secrets + GA4 admin steps still pending)
- No vault project brief exists at `02-projects/casino-funnels/` — gap noted.

---

## Executive summary

The funnel is structurally clean and the recent commit cadence shows healthy hygiene (UTM hardening, postback diagnostics, brand suppression). **The single biggest exposure is unauthenticated write access to `/api/lead`** — the documented `LEAD_WEBHOOK_TOKEN` is set in `.env.example` but never read by the handler. Combined with attacker-controlled `created_at` and `leadId`, anyone can pollute D1 conversion data. **Second**, the postback token uses non-constant-time comparison and returns HTTP 200 on auth failure with the first 4 chars of the attempted token logged. **Third**, `.env.production` is committed with the live affiliate campaign URL. Beyond security: `HaloCanvas` runs a continuous full-viewport RAF with `willReadFrequently:true` (forces software rendering), the OG image is a JPEG mislabelled `.png` at the wrong dimensions, and Clarity loads inline in `<head>` outside the consent gate that protects every other tracker.

---

## Findings by domain

### Discovery (explorer-agent)
- Two simultaneous canvases on `/wheel`: 792×792 wheel ([SpinWheel.tsx:166](src/pages/SpinWheel.tsx:166)) + full-viewport `HaloCanvas` ([HaloCanvas.tsx:203-314](src/components/HaloCanvas.tsx:203)) running RAF for the whole page lifetime.
- **Spin outcome is hardcoded "win"** ([SpinWheel.tsx:250-263](src/pages/SpinWheel.tsx:250)) — `setPhase('win')` fires unconditionally after 4200 ms; the 10 prize segments are decorative. Sweepstakes/regulatory implication if the UI implies genuine random selection.
- **Clarity loads twice**: inline CDN snippet at [index.html:44](index.html:44) AND `@microsoft/clarity` npm import in [src/lib/analytics.ts](src/lib/analytics.ts).
- **Hardcoded fallback Meta Pixel ID** `1296696345654709` at [Analytics.tsx:24](src/components/Analytics.tsx:24) — fires on every preview/staging deploy.
- `inboundMarketing` detection re-creates a fresh lead row on any navigation that carries UTMs ([leadTracker.ts:341-353](src/lib/leadTracker.ts:341)), creating orphan rows.

### Architecture (no formal CTO pass — captured here)
- Edge-first design (Cloudflare Pages + Functions + D1) is correct for the funnel's traffic shape. Single binding `DB`, two migrations.
- Functions are plain JS, not TS — call-site mistakes (e.g. wrong bind count) only surface at runtime; one such bug already exists (see backend HIGH-2).
- No vault project brief at `02-projects/casino-funnels/` — recommend creating one with stack, agents, and link to this report.

### Security (security-auditor)

| ID | Sev | Title | File:line |
|----|-----|-------|-----------|
| F01 | P1 | `.env.production` committed (live affiliate URL + analytics IDs) | [.env.production:3-5](.env.production) |
| F02 | P1 | `/api/lead` has no auth — CORS is the only gate; `LEAD_WEBHOOK_TOKEN` is documented but never read | [functions/api/lead.js:51-174](functions/api/lead.js:51) |
| F03 | P1 | Client-supplied `body.timestamp` written to D1 `created_at` unvalidated | [functions/api/lead.js:106](functions/api/lead.js:106) |
| F04 | P1 | IDOR — any caller can stamp `is_spin`/`is_claim` on any `leadId` | [functions/api/lead.js:131-166](functions/api/lead.js:131) |
| F05 | P2 | `unsafe-inline` in `script-src` defeats CSP for XSS | [public/_headers:6](public/_headers) |
| F06 | P2 | No HSTS header | `public/_headers` (absent) |
| F07 | P2 | `localhost` allowed in production CORS | [functions/api/lead.js:37,53](functions/api/lead.js:37) |
| F08 | P2 | D1 `database_id` committed in `wrangler.toml` | [wrangler.toml:12](wrangler.toml:12) |
| F09 | P2 | No rate limiting on `/api/lead` or `/api/postback` | functions/api/* |
| F10 | P2 | Postback logs first 4 chars of submitted token | [functions/api/postback.js:96](functions/api/postback.js:96) |
| F11 | P3 | Missing `Cross-Origin-Opener-Policy`/`-Resource-Policy` | `public/_headers` |
| F12 | P3 | `VITE_REQUIRE_ANALYTICS_CONSENT=false` + no age gate / geo gate | [.env.production:6](.env.production) |
| F13 | P3 | `unsafe-inline` in `style-src` enables CSS attribute exfil | [public/_headers:6](public/_headers) |
| F14 | P3 | CI Lighthouse uses `continue-on-error:true` | [.github/workflows/ci.yml:67-68](.github/workflows/ci.yml) |
| F15 | P3 | `leadId` PK has no UUID format check (zero-byte / oversized values accepted) | [functions/api/lead.js:74-75](functions/api/lead.js:74) |

**Compliance flag (F12):** gambling advertiser + device-fingerprint-class data + no consent + no age/geo gate is material exposure under GDPR / UK Gambling Act / multiple US state regimes. Active risk if any EU/UK traffic reaches the funnel.

### Backend (backend-specialist)

| ID | Sev | Issue | File:line |
|----|-----|-------|-----------|
| B-CRIT-1 | P0 | `provided !== expectedToken` — non-constant-time comparison | [functions/api/postback.js:95](functions/api/postback.js:95) |
| B-CRIT-2 | P0 | Bad token returns HTTP 200 — no clean alerting signal | [functions/api/postback.js:98](functions/api/postback.js:98) |
| B-HIGH-1 | P1 | Postback retry overwrites `postback_su_at` (no idempotency) — first-write-wins lost | [functions/api/postback.js:121](functions/api/postback.js:121) |
| B-HIGH-2 | P1 | `go.js` `.bind(clickId, now, now, sanitizeClickId(clickId))` — 4 binds for 3 `?` params; sanitized value silently dropped, raw `clickId` becomes `lead_id`. Works by accident; column-order change will corrupt rows. | [functions/go.js:67](functions/go.js:67) |
| B-HIGH-3 | P1 | No index on `postback_log` (will full-scan as it grows) | [migrations/0002_postback_log.sql](migrations/0002_postback_log.sql) |
| B-MED-1 | P2 | `leadId` no length cap / format check (D1 key bloat possible) | [functions/api/lead.js:74](functions/api/lead.js:74) |
| B-MED-2 | P2 | Trusted client `body.timestamp` (overlaps F03) | [functions/api/lead.js:106](functions/api/lead.js:106) |
| B-MED-3 | P2 | Dead branch in `buildDestination` — both arms set `click_id` | [functions/go.js:32-37](functions/go.js:32) |
| B-MED-4 | P2 | `sendGA4Event`/`logToD1` awaited inline → adds latency to 302; should use `context.waitUntil` | [functions/api/postback.js:132](functions/api/postback.js:132), [functions/go.js:127](functions/go.js:127) |
| B-LOW-1 | P3 | `NOT NULL DEFAULT ''` everywhere makes "missing" indistinguishable from "empty" | [migrations/0001_init_leads.sql](migrations/0001_init_leads.sql) |
| B-LOW-2 | P3 | Functions in JS, not TS | functions/* |

### Frontend (frontend-specialist)

| ID | Sev | Issue | File:line |
|----|-----|-------|-----------|
| FE-P0-1 | P0 | `HaloCanvas` `willReadFrequently:true` on a write-only animation canvas → forces software rendering | [HaloCanvas.tsx:176](src/components/HaloCanvas.tsx:176) |
| FE-P0-2 | P0 | RAF loop closure recreated on every `spinIntensity` change → flicker during the spin ramp; brief concurrent loops in StrictMode | [HaloCanvas.tsx:203-314](src/components/HaloCanvas.tsx:203) |
| FE-P1-1 | P1 | `CongratulationsOverlay` has no `role="dialog"` / `aria-modal` / focus trap — conversion screen inaccessible to keyboard / SR | [CongratulationsOverlay.tsx:91](src/components/CongratulationsOverlay.tsx:91) |
| FE-P1-2 | P1 | Countdown redirect inside `setTimeLeft` updater can fire twice in concurrent mode | [AffiliateOfferCountdown.tsx:32](src/components/AffiliateOfferCountdown.tsx:32) |
| FE-P1-3 | P1 | Spin `setTimeout` not stored in ref / not cleaned up — fires into unmounted tree on back-nav | [SpinWheel.tsx:250](src/pages/SpinWheel.tsx:250) |
| FE-P1-4 | P1 | Static `<link rel=canonical href="%VITE_CANONICAL_ORIGIN%/wheel">` ships literally if env not provided at build (Vite does not substitute %VAR% in HTML by default) | [index.html:36](index.html:36) |
| FE-P1-5 | – | Crown branding block (`a9532e7`) **verified working** — no Crown leak in static `<head>` or runtime `setPageMeta` | – |
| FE-P2-1 | P2 | `reducedMotion()` called per RAF frame instead of cached once | [HaloCanvas.tsx:140-143](src/components/HaloCanvas.tsx:140) |
| FE-P2-3 | P2 | Wheel canvas duplicates `maxWidth: 86vw` already set on parent | [SpinWheel.tsx:348-360](src/pages/SpinWheel.tsx:348) |
| FE-P2-4 | P2 | Hardcoded fallback Meta Pixel ID in source | [Analytics.tsx:24-25](src/components/Analytics.tsx:24) |
| FE-P2-5 | P2 | `role="status"` on a static `<p>` causes spurious SR announcements | [TrustpilotInlineRow.tsx:88](src/components/TrustpilotInlineRow.tsx:88) |

### Tests (test-engineer)

**P0 coverage gaps (revenue / security):**
- `/go` endpoint has **zero** tests (no `buildDestination`, `isSocialBot`, missing-`AFFILIATE_LINK`, social-bot OG response, D1 log-path coverage).
- `_middleware` redirect (apex/`*.pages.dev` → `www.luckymint.co`) has **zero** tests.
- `getAffiliateHref` UTM-non-forwarding contract from `9937f56` is not pinned by any test → silent regression risk.
- Crown branding suppression in `/go` social-bot HTML has no string assertion against "Crown" / "crowncoins" → can be re-leaked silently.

**P1 gaps:**
- `sanitizeLeadText`, `sanitizeDeviceCategory`, `sanitizeHourInt`, `sanitizeTimingMsInt` — **none** unit-tested.
- `tests/api-security.test.mjs` re-implements `sanitizeClickId` inline ([api-security.test.mjs:94-98](tests/api-security.test.mjs:94)) instead of importing the real module — **the test does not actually cover the production sanitizer**.
- `/api/lead` `claim`/`timing` event types untested; malformed JSON / oversize body untested.
- `prod-luckymint-wheel.spec.ts` writes real rows to production D1 with no cleanup.

**P2:** Lighthouse CI thresholds are all `warn` ([`.lighthouserc.json`](.lighthouserc.json)) — score of 0 passes; `responsive.spec.ts` snapshot tolerances are widened in CI (0.03 → 0.12 / 0.12 → 0.20) which masks real diffs.

### Performance

1. **`og-image.png` & `favicon.png` are JPEGs renamed `.png`** at 1524×1600 / 87 KB each. [index.html:23](index.html:23) declares 1200×630 (correct intent), but [pageMeta.ts:64](src/lib/pageMeta.ts:64) overrides to 343×361 at runtime. Twitter cards may reject; favicon should be <2 KB.
2. **No `manualChunks` in `vite.config.ts`** — single bundle ships React 19 + react-router 7 + motion 12 (~50 KB gzip) + lucide-react + Clarity. `motion` is used for one button hover at [SpinWheel.tsx:393-409](src/pages/SpinWheel.tsx:393); replaceable with CSS.
3. **8 Google Fonts files in `<head>`** (Inter ×4 + Montserrat ×4) blocking LCP ([index.html:39-42](index.html:39)).
4. **Clarity inlined synchronously** at [index.html:44-50](index.html:44) — bypasses the `shouldSendWebAnalytics()` gate that protects GA4/GTM/Pixel.
5. **`HaloCanvas` full-viewport RAF + 75 particles + `willReadFrequently`** ([HaloCanvas.tsx:130-203](src/components/HaloCanvas.tsx:130)) — dominant INP/battery cost on mobile.

### SEO

1. **Zero structured data** anywhere (`grep` confirms no `application/ld+json`). Easy wins: `WebSite` + `Organization` + `Review` (mirror Trustpilot row).
2. **Unprocessed `%VITE_CANONICAL_ORIGIN%`** at [index.html:36](index.html:36) and **`%VITE_CLARITY_PROJECT_ID%`** at [index.html:49](index.html:49) — Vite does not substitute `%VAR%` in HTML without an explicit plugin. Verify against view-source on www.luckymint.co.
3. **Sitemap** at [public/sitemap.xml](public/sitemap.xml) lacks `<lastmod>` / `<changefreq>`.
4. **No `llms.txt`** for AI-search visibility (GEO).
5. **OG meta inconsistency** — static HTML says 1200×630, runtime overwrites to 343×361. Crawlers get different values depending on whether they execute JS.

**Confirmed clean:** Crown Coins branding does not appear in `index.html`, `pageMeta.ts`, or `public/`. Mentioned only in legal pages ([PrivacyPolicy.tsx:32](src/pages/PrivacyPolicy.tsx:32), [TermsOfService.tsx:30](src/pages/TermsOfService.tsx:30)) — appropriate disclosure that does not surface in social previews.

### DevOps

1. **No standalone type-check in CI** (build runs `tsc -b` so it does compile, but Lighthouse step has `continue-on-error:true` at [.github/workflows/ci.yml:70](.github/workflows/ci.yml:70) — perf regressions are silent).
2. **D1 migrations are fully manual on prod** ([package.json:20](package.json:20)). CI only applies `0001_init_leads.sql` locally ([ci.yml:46](.github/workflows/ci.yml:46)) — `0002_postback_log.sql` is not in the local-apply step, so pre-deploy tests run against a stale schema.
3. **Whitespace-tolerant secret lookup** at [functions/api/postback.js:86](functions/api/postback.js:86) — `(env[k] ?? env[k+' '] ?? env[' '+k]).trim()` — defensive workaround indicating someone hit a malformed Pages secret. Re-set the secret cleanly and remove the fallback.
4. **No PR preview deploy / smoke-test gate against the actual Pages preview URL.** Production rollouts unverified at the edge until manual `/wheel`, `/terms`, `/privacy` checks.
5. **Pending project secrets** (per memory): `GA4_MEASUREMENT_ID`, `GA4_API_SECRET`, plus `LEAD_WEBHOOK_TOKEN` (which once set will activate F02 mitigation) — still need configuration in Cloudflare Pages.

---

## Recommendations (prioritized)

### P0 — ship before next traffic spike
1. **`/api/postback`: timing-safe token check + return 401 on bad token.** Wrap with `crypto.subtle.timingSafeEqual` over `TextEncoder` buffers. Stop logging `provided.slice(0,4)`. ([functions/api/postback.js:95-99](functions/api/postback.js:95))
2. **`/api/lead`: enforce `LEAD_WEBHOOK_TOKEN`** on every POST. CORS is not server-side auth. ([functions/api/lead.js:51-174](functions/api/lead.js:51))
3. **Drop client-supplied `body.timestamp`.** Use server `now` only — one-line fix. ([functions/api/lead.js:106](functions/api/lead.js:106))
4. **Make postback updates idempotent** — `SET postback_su_at = COALESCE(postback_su_at, ?)`. ([functions/api/postback.js:121](functions/api/postback.js:121))
5. **Fix `go.js` D1 bind count** — 4 binds for 3 placeholders; sanitised `clickId` is silently dropped. ([functions/go.js:67](functions/go.js:67))
6. **Remove `willReadFrequently:true`** from `HaloCanvas` ([HaloCanvas.tsx:176](src/components/HaloCanvas.tsx:176)) and from the wheel canvas read-back path ([SpinWheel.tsx:166](src/pages/SpinWheel.tsx:166)) — restores GPU compositing.

### P1 — within 1–2 sprints
7. **Remove `.env.production` from git, rotate, and move to Pages env.** Add to `.gitignore`. (F01)
8. **CSP hardening:** drop `'unsafe-inline'` from `script-src`; adopt `strict-dynamic` + nonce via middleware; add `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`; add `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Resource-Policy: same-origin`. ([public/_headers](public/_headers))
9. **`CongratulationsOverlay` a11y:** add `role="dialog" aria-modal="true" aria-labelledby="win-overlay-title"` and move focus to the CTA on mount. ([CongratulationsOverlay.tsx:91](src/components/CongratulationsOverlay.tsx:91))
10. **Fix HTML env placeholders** at [index.html:36,49](index.html:36) — either configure `vite-plugin-html` / `envReplace` or hard-code the canonical URL and Clarity ID.
11. **Spin `setTimeout` cleanup** — store id in `useRef`, cancel in effect cleanup. ([SpinWheel.tsx:250](src/pages/SpinWheel.tsx:250))
12. **Move Clarity into `Analytics.tsx`** behind `shouldSendWebAnalytics()` and the consent gate; remove the inline block at [index.html:44-50](index.html:44). Eliminates double-load + consent bypass.
13. **Real OG image:** ship a 1200×630 PNG/WebP <60 KB; reconcile [pageMeta.ts:64-65](src/lib/pageMeta.ts:64) to 1200×630.
14. **CI: apply migration `0002_postback_log.sql`** in pre-deploy ([.github/workflows/ci.yml:46](.github/workflows/ci.yml:46)); add post-deploy `wrangler d1 migrations apply ... --remote` job on push to main.
15. **Test backlog top-5:**
    - `/go` unit tests (`buildDestination`, `isSocialBot`, missing-affiliate, social-bot OG response).
    - Crown-branding string assertion on `/go` social-bot HTML.
    - `getAffiliateHref` UTM-non-forwarding contract (lock in `9937f56`).
    - `_middleware` redirect (apex/pages.dev → www) + SPA fallback.
    - `leadSanitize.js` sanitiser unit tests; fix [tests/api-security.test.mjs:94](tests/api-security.test.mjs:94) to import the real `sanitizeClickId`.

### P2 — backlog
16. **Compliance gate (F12):** `VITE_REQUIRE_ANALYTICS_CONSENT=true` + geo-based consent via Cloudflare `cf.country` + age verification. Material legal exposure if any EU/UK traffic reaches the funnel.
17. **Indexes** — add `idx_postback_log_click_id` and `idx_postback_log_received_at` on [migrations/0002_postback_log.sql](migrations/0002_postback_log.sql).
18. **`context.waitUntil`** for GA4 + D1 logging in `/api/postback` and `/go` — removes external round-trips from the response path.
19. **Vite `manualChunks`** for `motion` + `react-router-dom`; consider replacing the single `motion` button-hover with CSS to drop ~50 KB gzip.
20. **Self-host the 8 Google Font files** and trim weights; defer.
21. **Rate limiting** on `/api/lead` and `/api/postback` via Cloudflare WAF / KV counter.
22. **Move `database_id` out of `wrangler.toml`** into a non-committed config.
23. **Remove hardcoded fallback Meta Pixel ID** ([Analytics.tsx:24](src/components/Analytics.tsx:24)) — default to `''`.
24. **Restrict `localhost` CORS to DEV builds only** ([functions/api/lead.js:37,53](functions/api/lead.js:37)).
25. **Lighthouse CI:** flip `accessibility` and `best-practices` from `warn` to `error`; drop `continue-on-error: true`.
26. **JSON-LD** (`WebSite` + `Organization` + `Review`/`AggregateRating` mirroring Trustpilot row) in `index.html`.
27. **Sitemap:** add `<lastmod>`. Create `public/llms.txt`.

### P3 — opportunistic
28. Convert `functions/*.js` to TypeScript with `tsconfig.functions.json`; would have caught B-HIGH-2 at build time.
29. Reconsider `NOT NULL DEFAULT ''` schema pattern (`migrations/0001`); make optional fields nullable so `WHERE col IS NULL` works as expected.
30. Stop `prod-luckymint-wheel.spec.ts` writing to live D1 without cleanup.
31. Address the design question on the wheel: outcome is hardcoded "win" with decorative segments ([SpinWheel.tsx:250-263](src/pages/SpinWheel.tsx:250)) — fine if Crown's terms cover this as a "guaranteed welcome offer", but a sweepstakes-style framing would be a regulatory issue. Confirm Crown's affiliate compliance language matches the UI.

---

## Knowledge gaps to fill in vault
- [ ] Create `02-projects/casino-funnels/project.casino-funnels.md` (stack, agents, path, status) — currently missing.
- [ ] Create `04-knowledge/reference/casino-funnels-architecture.md` capturing the data flow diagram from explorer-agent (lead lifecycle, postback updates).
- [ ] Append to `04-knowledge/standards/casino-funnels-standards.md`: edge-function language (TS), CSP nonce policy, D1 migration discipline.

## Next steps
- [ ] Open a `docs/plans/casino-funnels-security-hardening.md` plan covering P0+P1 items, staffed via `workflows/plan.md`.
- [ ] Confirm + clean Cloudflare Pages secrets — `LEAD_WEBHOOK_TOKEN`, `POSTBACK_TOKEN` (whitespace fix), `GA4_MEASUREMENT_ID`, `GA4_API_SECRET`.
- [ ] Decide on the consent / age-gate approach (P2) — this needs business input, not just engineering.
