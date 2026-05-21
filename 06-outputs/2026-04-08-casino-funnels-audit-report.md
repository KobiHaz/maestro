# Project Audit Report — casino-funnels

**Date:** 2026-04-08  
**Project:** casino-funnels  
**Type:** WEB

## Sources Used

- `02-projects/casino-funnels/project.casino-funnels.md`
- `02-projects/casino-funnels/plans-and-tasks.md`
- `03-agents/agent-routing.md`
- `03-agents/workflows/project-deep-audit.md`
- `01-me/01-me-identity.md`
- `01-me/01-me-writing.md`
- `01-me/01-me-tools.md`
- `01-me/01-me-ai-preferences.md`
- `04-knowledge/reference/`* (checked; no `casino-funnels` reference docs found)
- `04-knowledge/standards/`* (checked; no `casino-funnels` standards file found)
- Repo analyzed: `~/.gemini/antigravity/projects/casino-funnels`
- Domain audit agents used: discovery, architecture/CTO, security, testing, performance, deployment/ops, SEO/docs
- Scripts executed:
  - `npm run lint`
  - `npm run build`
  - `npm run test:e2e`

## Findings by Domain

### Discovery (architecture map)

- Funnel is centered on `/wheel` with post-spin conversion in `CongratulationsOverlay` and timed fallback redirect.
- Attribution pipeline is client-side (`sessionStorage` + query propagation) via `src/lib/affiliateLink.ts`.
- Deployment path is Cloudflare Pages with edge middleware in `functions/_middleware.js`.
- Daily operational insight pipeline exists (`.github/workflows/daily-insights.yml` + `scripts/daily-insights.mjs`).

### Architecture (CTO review)

- Current stack is right-sized for a single-funnel web app (React + Vite + Pages).
- High drift risk between docs and implementation around A/B behavior (docs mention A/B cookie system; runtime currently emphasizes canonical-host middleware path).
- Analytics responsibilities are split across static HTML and runtime component logic, creating coupling and data-quality risk.
- Core conversion logic remains tightly coupled to UI components, limiting safe iteration and testability.

### Security

- **High:** Affiliate URL validation currently allows `http:` (not HTTPS-only), enabling downgrade and tampering risk if env is misconfigured.
- **Medium:** No hostname allowlist for affiliate destination; single env var can reroute all conversion traffic.
- **Medium:** Third-party trackers load before consent; privacy/compliance exposure and increased script supply-chain surface.
- **Medium:** CSP is not enforced, reducing defense-in-depth against future injection vectors.

### Backend / API

- No major server API surface in this project; risk is concentrated in edge redirect logic + client tracking pipeline.
- Server-side complexity is low, but this increases importance of strict frontend safety controls and config governance.

### Frontend

- `SpinWheel` and overlay path hold dense, mixed responsibilities (rendering, state machine, analytics, outbound action flow).
- Compliance and conversion elements are present, but some messaging consistency requires tightening (age/disclaimer consistency across pages).
- Social proof data in Trustpilot row is static/manual and can become stale.

### Database

- No internal database layer in this app.
- Data persistence is externalized (analytics vendors, Clarity exports, Telegram summaries), so data integrity depends on event contract consistency rather than DB schema controls.

### Tests

- Smoke routes are covered and currently pass (`4/4`), but behavior-critical conversion and compliance flows are under-tested.
- Missing high-value assertions include:
  - spin lifecycle (`idle -> spinning -> win`)
  - CTA click behavior (single-open + fallback path)
  - strict `/cookies -> /privacy#cookies` hash assertion
  - compliance/legal footer rendering guarantees
  - metadata canonical/OG behavior under env edge cases

### Ops / DevOps

- CI baseline exists (lint/build/e2e), and local runs passed in this audit.
- Release safety can improve with stricter deployment gating and an explicit rollback runbook.
- Node/runtime parity and secrets lifecycle practices should be hardened further for production reliability.

### Performance

- High-impact hotspot: animation loop churn in halo/wheel visuals during spin intensity ramp can recreate heavy effects repeatedly.
- Overlay celebration uses expensive visual layers (blur + many particles), likely to drop frames on weaker devices.
- Bundle currently ships as a relatively large main chunk; route/component splitting opportunities exist.
- Asset caching policy for immutable hashed files should be explicit.

### SEO

- **Critical risk:** `og-image` configuration appears inconsistent with actual asset availability/pathing and needs validation/fix.
- Missing `robots.txt` and `sitemap.xml` governance in current setup.
- Canonical strategy needs stronger explicitness beyond redirects (document-level canonical consistency).
- SPA metadata strategy can under-signal route-specific metadata for non-JS crawlers.

### Documentation

- Deployment docs are useful but need stronger SEO/compliance release checklist coverage.
- Documentation and runtime behavior should be synchronized for experimentation/tracking architecture.
- Project-specific `04-knowledge` docs for `casino-funnels` are currently absent (architecture + standards gap).

## Recommendations (Prioritized)

### P0 — Critical (execute first)

1. Enforce HTTPS-only affiliate destination and add hostname allowlist in `affiliateLink` flow.
2. Consolidate analytics loading strategy into one path (avoid static + runtime duplication).
3. Fix/verify OG image path and ensure valid social preview output.
4. Add minimum conversion-path tests: spin-to-win overlay + CTA open behavior + `/cookies` hash redirect.

### P1 — High

1. Add CSP and tighten security headers in deploy output.
2. Introduce consent-gated non-essential tracking for compliance-sensitive traffic.
3. Add release guardrails: required CI checks before production deploy + rollback runbook.
4. Refactor funnel logic into a domain layer (`experiment`, `conversion`, `event contract`) to reduce UI coupling.

### P2 — Medium

1. Reduce animation/compositing cost in win path for low/mid devices.
2. Add explicit long-lived cache headers for immutable hashed assets.
3. Add `robots.txt` + `sitemap.xml` and document SEO verification checklist.
4. Replace/manual-refresh static social-proof data with governed update process.

## Knowledge Gaps

- Create `04-knowledge/reference/casino-funnels-architecture.md`
- Create `04-knowledge/reference/casino-funnels-security-audit.md`
- Create `04-knowledge/standards/casino-funnels-standards.md`
- Add a `casino-funnels` release checklist (SEO + compliance + analytics integrity)

## Verification Notes

- Local scripts completed successfully:
  - `npm run lint` ✅
  - `npm run build` ✅
  - `npm run test:e2e` ✅
- Build output included a parse warning around `<noscript>` placement in `index.html`; build still completed. This should be cleaned to avoid parser ambiguity/toolchain fragility.

## Next Steps

- Implement P0 hardening items in one focused PR.
- Run `/plan` (`03-agents/workflows/plan.md`) to convert this audit into staffed execution tasks with priorities and owners.
- After implementation: run `/review` and `/finishing-branch` per Maestro lifecycle.