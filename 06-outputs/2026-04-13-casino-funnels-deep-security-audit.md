# Project Deep Audit — casino-funnels

**Date:** 2026-04-13  
**Project:** casino-funnels (luckymint.co)  
**Type:** WEB  
**Triggered by:** deep analysis + deep security analysis request  
**Workflow:** `project-deep-audit` + `security-auditor` + `penetration-tester`

---

## Sources Used

- `02-projects/casino-funnels/plans-and-tasks.md`
- `functions/api/lead.js`, `functions/api/postback.js`, `functions/_middleware.js`, `functions/api/ping.js`
- `src/lib/affiliateLink.ts`, `src/lib/analytics.ts`, `src/lib/leadTracker.ts`
- `src/components/Analytics.tsx`, `src/components/CongratulationsOverlay.tsx`
- `src/pages/SpinWheel.tsx`, `src/App.tsx`
- `public/_headers`, `.env.example`, `.env.local`, `.env.production`
- `wrangler.toml`, `package.json`, `.github/workflows/ci.yml`
- `npm audit` output (live)

**Agents invoked:**  
explorer-agent, security-auditor, penetration-tester, backend-specialist, frontend-specialist, devops-engineer, seo-specialist, test-engineer, compliance-auditor (inline)

---

## Executive Summary

The casino-funnels project is a Cloudflare Pages–hosted affiliate funnel (React + TypeScript + Vite) for Crown Coins Casino. The post-audit hardening from 2026-04-08 addressed the most obvious issues (CSP headers, consent gate, CI permissions, HTTPS affiliate link enforcement). However this deeper analysis uncovers **three critical security issues, four high-severity findings, and multiple medium/low issues** that require immediate action.

**Risk level: HIGH** — A long-lived Clarity API JWT is present in plaintext on disk, the frontend embeds a webhook secret token visible to any end-user, and unauthenticated endpoints are silently accepted when env vars are missing.

---

## Findings by Domain

---

### 🔍 Discovery (explorer-agent)

**Stack:** React 19 + TypeScript, Vite 8, Tailwind CSS 4, React Router DOM 7, Framer Motion (motion 12), Cloudflare Pages + Functions (Workers), Google Sheets API as data store.

**Architecture summary:**

```
Browser → CDN (Cloudflare Pages)
             ├── Static SPA (React)
             │     ├── leadTracker.ts → POST /api/lead
             │     ├── affiliateLink.ts → window.open(crowncoinscasino.com)
             │     └── analytics.ts → GA4, Meta Pixel, Clarity
             └── Cloudflare Functions
                   ├── _middleware.js  (canonical redirect + SPA fallback)
                   ├── /api/lead       (lead webhook → Google Sheets)
                   ├── /api/postback   (affiliate postback → Google Sheets)
                   └── /api/ping       (health check)
```

**Dependency count:** ~10 runtime deps, ~12 dev deps  
**Key external services:** Google Sheets API (service account), Microsoft Clarity, GA4/GTM, Meta Pixel, Telegram (daily insights)

---

### 🏛️ Architecture (CTO review)

**Strengths:**

- Cloudflare Pages is an excellent fit: global CDN, zero cold starts, free DDoS protection
- Cloudflare Workers/Functions for serverless API is the right choice at this scale
- TypeScript throughout the frontend with clean separation of concerns
- Consent gate approach for analytics is architecturally sound

**Concerns:**

- **Google Sheets as a database is a risk at scale.** Row scanning (`findLeadRow`, `findRowByClickId`) reads the entire column on every request — O(n) read. At ~1000+ leads this becomes slow and approaches Sheets API rate limits (100 reads/100 seconds). A KV or D1 database should be planned for.
- **No request queuing or retry logic** in the Workers Functions. A transient Google OAuth error permanently loses a lead event.
- **Single service account** with full Sheets write access. Should use least-privilege (only the specific spreadsheet).

---

### 🔐 Security (security-auditor + penetration-tester)

#### CRITICAL

---

**[SEC-C1] Long-lived Clarity JWT in plaintext `.env.local`**

- **Severity:** CRITICAL  
- **File:** `.env.local`  
- **Finding:** `CLARITY_DATA_EXPORT_TOKEN` is a JWT with `exp: 4928383844` (year ~2126 — effectively non-expiring). The token is stored in plaintext on disk in `.env.local`. While gitignored, any local machine compromise, accidental `git add -f`, or file sync to cloud exposes this token. If leaked, an attacker can exfiltrate all Clarity session recordings, heatmaps, and behavioral data for the project indefinitely.
- **OWASP:** A04 (Cryptographic Failures), A07 (Authentication Failures)
- **Remediation:**
  1. Rotate this token immediately in Clarity → Settings → Data Export.
  2. Store the new token in macOS Keychain or a secrets manager (e.g. 1Password CLI, Doppler).
  3. Load it at runtime via `op read` or similar — never write it to a file on disk.
  4. Add a pre-commit hook that scans for JWT patterns in staged files.

---

**[SEC-C2] Webhook bearer token embedded in client-side JavaScript bundle**

- **Severity:** CRITICAL  
- **File:** `src/lib/leadTracker.ts` (lines 148–151), Vite env vars
- **Finding:** `VITE_LEAD_LOG_WEBHOOK_TOKEN` is a `VITE_` prefixed env var, meaning Vite bakes it into the compiled JavaScript bundle served to every browser. Any visitor can open DevTools → Sources → search for the token and find it. They can then call `POST /api/lead` with arbitrary lead data (spam, fake conversions, data poisoning).
- **Impact:** Adversary injects fake leads → pollutes Google Sheets → ad attribution is corrupted → media budget is wasted.
- **OWASP:** A07 (Authentication Failures), A04 (Cryptographic Failures)
- **Remediation:**
  1. Remove `VITE_LEAD_LOG_WEBHOOK_TOKEN` from the frontend entirely.
  2. Instead, add an `Origin` allowlist check in `/api/lead`: reject requests not from `https://www.luckymint.co`.
  3. Use Cloudflare's built-in WAF rule to block requests to `/api/lead` that don't carry the `Origin: https://www.luckymint.co` header.
  4. Supplement with a HMAC signature computed from a server-side secret (not exposed to client).

---

**[SEC-C3] Silent auth bypass when env vars are not configured**

- **Severity:** CRITICAL  
- **Files:** `functions/api/lead.js` (line 173), `functions/api/postback.js` (line 163)
- **Finding:**
  ```js
  // lead.js
  const token = ((env.LEAD_WEBHOOK_TOKEN ?? ...)).trim()
  if (token) { /* check auth */ }   // ← if env var missing, entire auth block is skipped

  // postback.js
  const expectedToken = g('POSTBACK_TOKEN')
  if (expectedToken) { /* check auth */ }  // ← same pattern
  ```
  If these env vars are not set in Cloudflare Pages (e.g., in a new environment, staging, or after an accidental deletion), the endpoints become fully public with zero authentication.
- **OWASP:** A01 (Broken Access Control), A07 (Authentication Failures)
- **Remediation:**
  ```js
  const token = g('LEAD_WEBHOOK_TOKEN')
  if (!token) {
    console.error('[lead] LEAD_WEBHOOK_TOKEN not configured — rejecting all requests')
    return json({ ok: false, error: 'service_unavailable' }, 503)
  }
  ```
  Always **fail closed**: missing secret = reject, not accept.

---

#### HIGH

---

**[SEC-H1] Internal error details leaked to client in `/api/lead`**

- **Severity:** HIGH  
- **File:** `functions/api/lead.js` (line 241)
- **Finding:**
  ```js
  return json({ ok: false, error: 'sheets_error', detail: msg }, 500)
  ```
  The Google Sheets API error message (`msg`) is returned to the browser. This can expose service account email, sheet ID, internal API URLs, or Google OAuth error strings — valuable reconnaissance for an attacker.
- **Remediation:** Remove `detail` from the 500 response. Log the full error server-side only:
  ```js
  console.error('[lead] error:', msg)
  return json({ ok: false, error: 'internal_error' }, 500)
  ```

---

**[SEC-H2] CORS wildcard on an authenticated API endpoint**

- **Severity:** HIGH  
- **File:** `functions/api/lead.js` (lines 154–158, 163–169)
- **Finding:**
  ```js
  headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
  // And OPTIONS:
  'Access-Control-Allow-Origin': '*'
  ```
  `/api/lead` accepts `Authorization: Bearer <token>` but allows cross-origin requests from any domain. Combined with SEC-C2 (token visible in bundle), any third-party site can embed a script that reads the token from the bundle and fires fake lead events.
- **Remediation:** Pin CORS to the canonical origin:
  ```js
  'Access-Control-Allow-Origin': 'https://www.luckymint.co'
  ```
  And in the middleware, validate `Origin` header on write requests.

---

**[SEC-H3] Vite HIGH-severity CVEs — unpatched**

- **Severity:** HIGH (CVSS 7.5+)  
- **Source:** `npm audit`
- **CVEs:**
  - **Vite: Path Traversal in `.map` file handling** — may allow reading arbitrary files through the dev server
  - **Vite: `server.fs.deny` bypass via query strings** — allows reading files outside the allowed root
  - **Vite: Arbitrary file read via dev server WebSocket** — unauthenticated WebSocket can read project files
- **Context:** These are dev-server vulnerabilities (not production). However the dev server runs on development machines that also hold `.env.local` secrets. If a developer visits a malicious page while running `vite dev`, files can be exfiltrated.
- **Remediation:** `npm update vite` — fix is available. Bump to latest `^8.x` patch.

---

**[SEC-H4] Webhook token sent as URL query parameter (logged by proxies)**

- **Severity:** HIGH  
- **File:** `src/lib/leadTracker.ts` (lines 159–165)
- **Finding:**
  ```ts
  if (!url.searchParams.get('authToken')) {
    url.searchParams.set('authToken', webhook.token)
  }
  requestUrl = url.toString()
  ```
  The bearer token is appended as `?authToken=<secret>` to the URL. URL query params appear in server access logs, CDN logs, browser history, Referer headers, and referrer analytics. The token is also sent as `Authorization: Bearer` header (good) but the URL param creates unnecessary exposure paths.
- **Remediation:** Remove the `authToken` URL param fallback. Use header-only auth. If the API must support URL param auth (for compatibility), use a separate read-only, short-lived token for that purpose.

---

#### MEDIUM

---

**[SEC-M1] CSP allows `unsafe-inline` for scripts**

- **Severity:** MEDIUM  
- **File:** `public/_headers`
- **Finding:**
  ```
  script-src 'self' 'unsafe-inline' https://www.googletagmanager.com ...
  ```
  `'unsafe-inline'` allows any inline `<script>` tag to execute. This is required for some GTM functionality but significantly weakens XSS protection. A stored XSS in a dynamically rendered element would be executable.
- **Remediation:** Migrate to CSP nonce-based approach (requires server-side rendering or Cloudflare Transform Rules to inject nonce) or use `'strict-dynamic'` + hashes for known inline scripts. GTM supports nonce-based loading.

---

**[SEC-M2] No rate limiting on `/api/postback` and `/api/lead`**

- **Severity:** MEDIUM  
- **Finding:** Both endpoints have no rate limiting. An adversary can:
  - Flood `/api/postback` with random `click_id` values → full column scan on every request → Google Sheets rate limit exhaustion → denial of service on lead tracking
  - Flood `/api/lead` with `init` events → append unlimited rows to the spreadsheet
- **Remediation:** Add Cloudflare WAF rate limiting rules on `/api/postback` (50 req/min/IP) and `/api/lead` (30 req/min/IP). Or implement Cloudflare Turnstile on the frontend before lead init fires.

---

**[SEC-M3] Picomatch ReDoS vulnerability (devDependency)**

- **Severity:** MEDIUM (CVSS 7.5 — but devDependency only)  
- **Source:** `npm audit` — `picomatch >=4.0.0 <4.0.4`
- **Finding:** ReDoS via extglob quantifiers. This is a build-tool dependency, not production code. Risk is limited to build pipeline (CI could be slowed/hung on malicious input).
- **Remediation:** `npm update` — fix is available.

---

**[SEC-M4] Google service account scoped to full Sheets API**

- **Severity:** MEDIUM  
- **Finding:** The JWT scope is `https://www.googleapis.com/auth/spreadsheets` — full read/write access to ALL spreadsheets owned by the service account. If the private key is compromised, the attacker has write access to any sheet.
- **Remediation:** Restrict scope to `https://www.googleapis.com/auth/spreadsheets` on only the specific `GOOGLE_SPREADSHEET_ID`. Share the spreadsheet with the service account at the spreadsheet level only, not at the Drive level. Consider using a Google Cloud service account with Workload Identity Federation if moving off Cloudflare in the future.

---

**[SEC-M5] Real identifiers in `.env.example`**

- **Severity:** MEDIUM (informational)  
- **File:** `.env.example`
- **Finding:**
  ```
  VITE_GA_MEASUREMENT_ID=G-0JWLQ0LHLW
  VITE_CLARITY_PROJECT_ID=w3bhoc125h
  ```
  Real production measurement IDs are committed in the example file. While these are "public" (baked into the frontend bundle), having them in a committed example file also exposes the affiliate link target `https://crowncoinscasino.com/` without any macros — a complete production URL that could be reverse-engineered by competitors.
- **Remediation:** Replace with placeholder values: `VITE_GA_MEASUREMENT_ID=G-XXXXXXXXXX`. Keep real values only in `.env.local` (gitignored) and Cloudflare Pages env vars.

---

#### LOW

---

**[SEC-L1] `brace-expansion` DoS vulnerability (devDependency)**

- **Severity:** LOW (CVSS 6.5 — build tool only)  
- **Remediation:** `npm update` — fix is available.

---

**[SEC-L2] `click_id` accepts both `?click_id=` and `?gclid=` without validation**

- **Severity:** LOW  
- **File:** `src/lib/leadTracker.ts` (line 102)  
- **Finding:** `click_id` can be up to 512 characters (enforced). However it's stored verbatim in Google Sheets and used to look up rows in `postback.js`. No character validation exists. A malformed click_id like `=IMPORTRANGE(...)` would create a formula injection in Google Sheets (CSV injection / Sheets formula injection).
- **Remediation:** Sanitize click_id to alphanumeric + hyphens/underscores only before storage. Or prefix with a literal `'` to force Sheets to treat it as text when writing.

---

**[SEC-L3] `/api/ping` unauthenticated endpoint reveals service is alive**

- **Severity:** LOW (informational)  
- **Finding:** `GET /api/ping` returns `{"ok":true,"ts":1234567890}` to any caller. Minor information disclosure (confirms the Functions runtime is active). Not exploitable alone but useful in reconnaissance.
- **Remediation:** Add a static Cloudflare Worker response at edge or remove if not needed for monitoring.

---

### 🖥️ Backend (backend-specialist)

`**/api/lead` handler:**

- O(n) row scan on every spin/claim event — should cache leadId→row mapping or use a proper DB
- Error handling is correct (try/catch) but the `detail` leak (SEC-H1) must be fixed
- The `ensureHeader` call on every request adds an extra Sheets API round-trip — cache this or make it idempotent once only
- `onRequestPost` for the lead endpoint correctly parses JSON, validates required fields, and handles eventType routing

`**/api/postback` handler:**

- `onRequestGet as onRequestPost` alias is correct — handles both GET and POST
- Token auth logic is sound except for the missing-env bypass (SEC-C3)
- The "return 200 to partner on auth failure" pattern (line 169) is a good operational decision but must NOT be applied to missing-env case

`**_middleware.js`:**

- Canonical redirect logic is correct (apex → www, pages.dev → www)
- SPA fallback using `context.env.ASSETS.fetch` is the correct Cloudflare Pages pattern
- Missing: HTTP → HTTPS redirect (relying on Cloudflare's "Always Use HTTPS" setting — should be explicitly documented)

---

### 🎨 Frontend (frontend-specialist)

**SpinWheel.tsx:**

- Canvas-based wheel is performant (WebGL-level control without the complexity)
- `SPIN_DURATION_MS` and `targetDegrees` are both random/fixed in the frontend — the win is purely cosmetic; the overlay always shows the same offer (good design, no rigged outcome)
- `wheelCanvasDebug` is production-safe (only logs when `VITE_DEBUG_WHEEL_CANVAS=true`)
- `Math.random()` for spin target is fine here (no security implications since outcome is fixed)

**Analytics.tsx:**

- GTM/GA/Meta script injection is done correctly (dynamic createElement, no innerHTML)
- `encodeURIComponent(gtmId)` before injecting into src — good XSS prevention
- The `metaPixelId` validation `/^\d{5,20}$/` before injection is good
- **Issue:** Clarity is loaded via `index.html` (not in the component) — means Clarity always loads regardless of consent gate. Check that `VITE_REQUIRE_ANALYTICS_CONSENT` also blocks Clarity in `index.html`.

**CongratulationsOverlay.tsx:**

- `window.open(targetUrl, '_blank', 'noopener,noreferrer')` — correct anti-clickjacking usage
- `eventCallback` timeout fallback (500ms) ensures navigation even if Meta Pixel is blocked — good
- `affiliateHref` validated to HTTPS + allowlist in `affiliateLink.ts` — correct

**affiliateLink.ts:**

- Strong: `ALLOWED_AFFILIATE_HOSTS` allowlist prevents open redirect
- Strong: `MAX_PARAM_VALUE_LEN = 512` prevents oversized payloads
- Strong: HTTPS protocol enforcement

**leadTracker.ts:**

- Concern: `sendLeadUpdate` silently swallows all fetch errors (`.catch(() => {})`) — no observability when lead events fail in production
- Lead ID uses `crypto.randomUUID()` with fallback — correct

---

### 🗄️ Database / Data Layer (database-architect)

**Google Sheets as data store — critical limitations:**

1. **No ACID guarantees** — concurrent spin events can cause row duplication or missed updates
2. **API rate limits:** 100 read requests / 100 seconds / project. At moderate traffic this will throttle
3. **Linear scan per request** — `findLeadRow` scans the entire C column on every `spin`/`claim` event
4. **No indexing** — Google Sheets has no concept of indexed lookups
5. **Data retention** — No TTL, no archiving strategy, sheet will grow unbounded

**Recommendation:** For >500 leads/day, migrate to Cloudflare D1 (SQLite at the edge) for lead storage. Keep the Google Sheets sync as a "mirror" via a scheduled Worker, not the primary write path.

---

### 🧪 Tests (test-engineer)

**Current coverage:**

- `tests/smoke.spec.ts` — Playwright E2E smoke test (4/4 passing per plans-and-tasks.md)
- No unit tests
- No API endpoint tests (no auth rejection test, no missing-env test)

**Gaps:**

- `[TEST-G1]` No test for what happens when `LEAD_WEBHOOK_TOKEN` is missing → should return 503 (SEC-C3 fix must be test-driven)
- `[TEST-G2]` No test for CORS rejection from disallowed origins
- `[TEST-G3]` No test for formula injection in `click_id` (SEC-L2)
- `[TEST-G4]` No test for postback token bypass (missing `POSTBACK_TOKEN`)
- `[TEST-G5]` No test for rate limiting behavior

---

### ⚙️ DevOps / CI (devops-engineer)

**CI pipeline (`.github/workflows/ci.yml`):**

- Good: `permissions: contents: read`, `concurrency` cancel-in-progress, Node 22 pinned
- **Missing:** `npm audit --audit-level=high` step — HIGH vulnerabilities currently pass CI silently
- **Missing:** `npm ci --frozen-lockfile` strict mode (using `npm ci` which is already correct)
- **Missing:** Secret scanning step (e.g. `truffleHog` or `gitleaks`)
- **Missing:** Dependency review action for PRs

**Cloudflare Pages setup:**

- `wrangler.toml` is minimal and correct for Pages
- `compatibility_date = "2025-03-23"` — should update to a 2026 date to get latest runtime fixes

**Recommended CI additions:**

```yaml
- name: Security audit
  run: npm audit --audit-level=high

- name: Check for secrets
  uses: trufflesecurity/trufflehog@main
  with:
    path: ./
    base: main
```

---

### 🚀 Performance (performance-optimizer)

**Frontend:**

- No explicit code splitting — entire app is one chunk (small enough now, ~50-100KB gzipped estimated)
- Canvas wheel drawing is efficient (no React re-renders during animation)
- Framer Motion (motion 12) is well-used — only used for overlay animation, not the wheel itself
- `@tailwindcss/vite` plugin (Tailwind 4) → CSS-in-JS-free, excellent build performance

**API performance:**

- Google Sheets O(n) scan is the biggest bottleneck — already documented above
- No caching layer between Functions and Sheets API
- `ensureHeader` call on every request adds ~100-200ms latency (round-trip to Sheets API to check header row)

**Recommendation:** Cache the "header row exists" check in a Cloudflare KV with a 24h TTL. This eliminates one API round-trip per request.

---

### 🔍 SEO (seo-specialist)

**Strengths:**

- `robots.txt` present and correct
- `sitemap.xml` present
- Dynamic canonical via `usePageSEO` hook
- OG image (`og-image.png`) present
- `<meta name="viewport">` (assumed via standard Vite template)
- Schema-free (no structured data, appropriate for a funnel page)
- `Referrer-Policy: strict-origin-when-cross-origin` — good (prevents UTM leakage via referrer)

**Gaps:**

- `sitemap.xml` should be submitted to Google Search Console and validated
- No `hreflang` (single locale — OK for now)
- `ComplianceFooter` content should include `noindex` on `/terms` and `/privacy` if they are thin pages (prevents diluting authority)
- Core Web Vitals not measured (no Lighthouse CI in pipeline)

---

### 📋 Compliance (compliance-auditor)

**Social casino affiliate compliance:**

- ✅ Age gate language: "adults 19+" in SpinWheel SEO description and Terms
- ✅ Disclaimer: "Independent affiliate page. Play responsibly." in SEO meta
- ✅ `ComplianceFooter` component present
- ⚠️ `VITE_REQUIRE_ANALYTICS_CONSENT` is available but `.env.production` does NOT enable it — analytics fires without explicit consent in production
- ⚠️ The Clarity script in `index.html` may load before consent is checked (see frontend finding)
- ⚠️ GDPR/CCPA: No cookie banner or consent management platform (CMP) integrated. If EU traffic is expected, this is required
- ⚠️ No geo-blocking for US states where Crown Coins is not available (this is the partner's responsibility but a risk to document)

---

## Recommendations (Prioritized)

### P0 — Critical (Fix This Week)


| ID     | Issue                                  | Action                                                      |
| ------ | -------------------------------------- | ----------------------------------------------------------- |
| SEC-C1 | Clarity JWT in `.env.local`            | Rotate token, store in Keychain/1Password                   |
| SEC-C2 | Webhook token in client bundle         | Remove `VITE_LEAD_LOG_WEBHOOK_TOKEN`, use Origin-based auth |
| SEC-C3 | Silent auth bypass on missing env vars | Fail closed (503) when secret is missing                    |


### P1 — High (Fix This Sprint)


| ID     | Issue                          | Action                                   |
| ------ | ------------------------------ | ---------------------------------------- |
| SEC-H1 | Error detail leakage           | Strip `detail` from 500 responses        |
| SEC-H2 | CORS wildcard on auth endpoint | Pin to `https://www.luckymint.co`        |
| SEC-H3 | Vite HIGH CVEs                 | `npm update vite`                        |
| SEC-H4 | Token in URL query param       | Remove `authToken` from URL, header-only |


### P2 — Medium (Next 2 Weeks)


| ID         | Issue                           | Action                                                               |
| ---------- | ------------------------------- | -------------------------------------------------------------------- |
| SEC-M1     | `unsafe-inline` CSP             | Migrate to nonce-based CSP                                           |
| SEC-M2     | No rate limiting                | Add Cloudflare WAF rules on `/api/`*                                 |
| SEC-M3     | Picomatch ReDoS                 | `npm update`                                                         |
| SEC-M4     | Service account over-scoped     | Restrict at spreadsheet level                                        |
| SEC-M5     | Real IDs in `.env.example`      | Replace with placeholders                                            |
| TEST-G1-G4 | Missing security tests          | Add Playwright/Vitest API tests                                      |
| CI         | No `npm audit` in CI            | Add `--audit-level=high` step                                        |
| COMPLIANCE | Analytics fires without consent | Enable `VITE_REQUIRE_ANALYTICS_CONSENT=true` in production + add CMP |


### P3 — Low / Strategic (Backlog)


| ID       | Issue                            | Action                                            |
| -------- | -------------------------------- | ------------------------------------------------- |
| SEC-L2   | Formula injection via click_id   | Sanitize to `[a-zA-Z0-9_-]` + 64 char max         |
| SEC-L3   | /api/ping information disclosure | Gate or remove                                    |
| DB       | Google Sheets as primary store   | Plan migration to Cloudflare D1 at >500 leads/day |
| PERF     | `ensureHeader` on every request  | Cache in KV                                       |
| PERF     | Code splitting for pages         | Add Vite `manualChunks` if bundle grows           |
| SEO      | Lighthouse CI                    | Add `@lhci/cli` to CI pipeline                    |
| WRANGLER | `compatibility_date` stale       | Update to `2026-04-01`                            |


---

## Knowledge Gaps

- Create `04-knowledge/reference/casino-funnels-architecture.md` (none exists)
- Create `04-knowledge/standards/casino-funnels-standards.md` (none exists)
- Document Cloudflare Pages env var configuration (which vars are set in which environments)
- Document Google service account permissions and rotation schedule

---

## Next Steps

- **SEC-C1:** Rotate `CLARITY_DATA_EXPORT_TOKEN` in Clarity dashboard → store in 1Password
- **SEC-C2:** Refactor lead webhook auth → remove `VITE_LEAD_LOG_WEBHOOK_TOKEN` from Vite, add `Origin` check in `/api/lead`
- **SEC-C3:** Add fail-closed guard to both `/api/lead` and `/api/postback` for missing tokens
- **SEC-H1/H2:** Patch CORS + error detail in `functions/api/lead.js`
- **SEC-H3/M3:** `npm update` to clear all auto-fixable CVEs
- Open plan file `docs/plans/casino-funnels-security-hardening-2.md` via `/plan` for task tracking

---

*Generated by: project-deep-audit workflow | security-auditor | penetration-tester | explorer-agent | backend-specialist | frontend-specialist | devops-engineer | seo-specialist | test-engineer | compliance-auditor*