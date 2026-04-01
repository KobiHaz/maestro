# Project Audit Report — casino-funnels

**Date:** 2026-03-25  
**Project:** casino-funnels  
**Type:** WEB (Social Casino / Sweepstakes affiliate funnel)  
**Code path:** `~/.gemini/antigravity/projects/casino-funnels`  
**Live (per README):** [casino-agf.pages.dev](https://casino-agf.pages.dev)

## Sources Used

- `02-projects/casino-funnels/project.casino-funnels.md`
- `04-knowledge/reference/casino-funnels-*` — **none found** (gap)
- `04-knowledge/standards/casino-funnels-standards.md` — **none found** (gap)
- `02-projects/casino-funnels/plans-and-tasks.md` — **not present**
- **Scripts run:** `frontend-design/scripts/ux_audit.py`, `vulnerability-scanner/scripts/security_scan.py`
- **Scripts not run:** `lighthouse_audit.py` (Lighthouse CLI not installed in environment)
- **Verification:** `npm run build` (pass), `npm run lint` (1 warning)

---

## Findings by Domain

### Discovery (architecture)

- **Stack:** React 19, TypeScript, Vite 8, Tailwind v4, React Router 7, Motion, Lucide. Matches README; **Maestro project brief still says “React Router v6”** — outdated.
- **Routes:** `/` → `/slots`; `/slots`, `/wheel`, `/plinko`, `/crash`, `/win-overlay`; catch-all → `/slots` (`App.tsx`).
- **Conversion path:** Mini-games use `CongratulationsOverlay` (e.g. slots, wheel); affiliate exit via `getAffiliateHref()` from `VITE_AFFILIATE_LINK`.
- **Edge:** Cloudflare Pages `functions/_middleware.js` sets `ab-test-wheel` cookie on `/wheel` only (50/50, SameSite=Lax, Secure on HTTPS).
- **Static hosting:** `public/_redirects` SPA fallback to `/index.html`.
- **Legacy folder:** `vanilla-slot/` (standalone HTML/JS) — not part of Vite bundle but flagged by security scanner for `innerHTML` usage.

### Architecture / CTO view

- **Affiliate handling is centralized and validated:** `getAffiliateHref()` parses URL and restricts to `http:`/`https:`, returns `null` when missing — avoids the old “relative YOUR_AFFILIATE_LINK” bug documented in repo brainstorms.
- **Brief drift:** Project note still says “Replace `AFFILIATE_LINK` at top of each page”; implementation uses **env + shared helper** and overlays — update the brief to avoid onboarding confusion.
- **Single bundle:** Production build ~400 kB JS (~127 kB gzip) — route-based code splitting is a future optimization if the funnel grows.

### Security

- **Affiliate CTAs:** `CongratulationsOverlay` / `WinOverlayPage` use `rel="noopener noreferrer"` on `target="_blank"` links. `TrustpilotWinWidget` same.
- **Analytics:** GA inline script uses `gaId.replace` for quotes; ID from env — low XSS risk if env is trusted. Clarity snippet escapes double quotes in ID.
- **Env in git:** `.env.development` and `.env.production` are **tracked** (affiliate URL only today). Risk if secrets are added later; prefer `.env.example` + CI/host env only.
- **security_scan.py highlights:**
  - False-positive “missing yarn/pnpm lock” while **npm** uses `package-lock.json` — ignore for npm-only repos or tune script.
  - **XSS pattern** in `vanilla-slot/slot-logic.js` (`innerHTML`) — not shipped in main app; remove, quarantine, or document as non-production artifact.
  - **No security headers** in repo (CSP, HSTS, X-Frame-Options) — typical for static Pages; configure via Cloudflare **Transform Rules** or `_headers` if supported by your setup.

### Backend / API

- **None** — fully static SPA + optional Pages middleware. No server-side auth or PII collection in code reviewed.

### Frontend / UX / accessibility

- **Reduced motion:** `index.css` media query; `WinOverlayPage` uses `useReducedMotion`; `HaloCanvas` checks `matchMedia` — good baseline.
- **ESLint:** `HaloCanvas.tsx` — `react-hooks/exhaustive-deps` warning (`wheelSize` missing from dependency array).
- **ux_audit.py:** **FAIL** with 6 “issues” — several are **false positives** (static HTML fixtures in repo scanned as pages; `index.css` / motion “inputs”). Actionable items:
  - **Plinko.tsx:** Tailwind `purple-*` classes — conflicts with Maestro “purple ban” rule; consider teal/cyan/emerald tokens for brand consistency.
- **Touch targets / typography:** Review game UIs against 44px minimum where tappable (script flagged fixtures; still worth manual pass on `/wheel` and overlays).

### Database

- **N/A**

### Tests

- **No `test` script** in `package.json`; no unit or E2E suite detected. High regression risk for A/B, analytics events, and overlay flows.

### Ops / DevOps

- **No `.github/workflows`** — no automated build/lint on PRs.
- **Deploy:** Documented for Cloudflare Pages (build `npm run build`, output `dist`); `wrangler` present for `pages:dev`.
- **Lighthouse:** Not executed here; install `lighthouse` CLI or use Pages/Web Vitals for production CWV.

### Performance

- **Build:** Fast (~200 ms transform on machine used for audit). **Single JS chunk** — consider lazy routes for `/plinko`, `/crash`, etc., if LCP/TTI matters on slow devices.
- **Fonts:** Google Fonts with `preconnect` — good; consider `font-display: swap` in CSS if not already inherited.

### SEO / discoverability

- **index.html:** `<title>casino-funnels</title>` only — no meta description, Open Graph, or Twitter cards.
- **Per-route titles:** Not observed — all routes share one title (bad for sharing and SERP snippets).
- **Structured data:** None — optional for landing pages but worth OG tags for link previews.

### Documentation

- **README** is strong: repo link, live URL, env table, deployment, A/B overrides.
- **docs/deployment.md** referenced — aligns with Cloudflare Pages.
- **Maestro vault** project card needs sync with Router version and affiliate/env model.

---

## Recommendations (Prioritized)

### P0 — Critical

- None identified in code review for a static affiliate funnel, assuming production `VITE_AFFILIATE_LINK` is set on Pages.

### P1 — High

1. **Add automated checks:** GitHub Action (or Cloudflare) running `npm ci && npm run build && npm run lint` on every PR.
2. **SEO / sharing:** Per-route `<title>` + meta description + minimal OG (`og:title`, `og:description`, `og:image`) for `/wheel` and other entry URLs used in ads.
3. **Tests (smoke):** At least Playwright flows: open `/wheel`, spin, overlay visible, CTA href resolves when env set.

### P2 — Medium

1. **Update Maestro `project.casino-funnels.md`:** React Router **7**, env-based affiliate (remove per-file `AFFILIATE_LINK` instruction).
2. **`.env` policy:** Stop tracking `.env.production` / `.env.development` if they ever hold non-public values; rely on Pages env + `.env.example` only.
3. **Plinko palette:** Replace `purple-*` with on-brand non-purple tokens per Maestro UX rules.
4. **Fix ESLint warning** in `HaloCanvas.tsx` (deps or intentional disable with comment).
5. **Route code splitting** if bundle size or mobile performance becomes an issue.
6. **Security headers** at Cloudflare for the live hostname (CSP baseline, HSTS).
7. **Legacy `vanilla-slot/`:** Delete from repo or move to a separate archive branch to avoid scanner noise and confusion.

### P3 — Low

1. Install Lighthouse (or use CI) and record scores for [casino-agf.pages.dev](https://casino-agf.pages.dev) on `/wheel` and `/slots`.
2. Tune `ux_audit.py` excludes for `*.html` design exports if they remain in-repo.

---

## Knowledge Gaps

- [ ] Create `04-knowledge/reference/casino-funnels-architecture.md` (routes, A/B cookie, env contract, deploy).
- [ ] Create `04-knowledge/standards/casino-funnels-standards.md` (analytics event names, compliance copy rules, color tokens).
- [ ] Optional: `02-projects/casino-funnels/plans-and-tasks.md` for active roadmap.

---

## Next Steps

- [x] Sync Maestro project brief with repository reality (Router 7, env affiliate). *(2026-03-25)*
- [x] Add CI workflow + smallest valuable E2E test. *(GitHub Actions + Playwright smoke)*
- [x] Ship meta/OG for primary ad landing routes. *(per-route `usePageSEO`, `index.html` defaults, `public/og-image.png`)*
- [ ] Re-run Lighthouse after CLI available; attach scores to this report or a new dated output.

---

## Agent / Script Equivalence

This report consolidates the roles of: discovery, architecture, security, frontend, performance, SEO, tests, ops, and documentation — as specified in `project-deep-audit.md`, without separate subagent invocations (single-session synthesis).
