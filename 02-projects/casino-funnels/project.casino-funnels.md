---
project: casino-funnels
status: active
path: ~/.gemini/antigravity/projects/casino-funnels
type: WEB
agents: [frontend-specialist]
niche: Social Casino / Sweepstakes Affiliate
---

# casino-funnels

Single-focus conversion funnel: **spin wheel only** (`/wheel`) for Social Casino / Sweepstakes affiliate traffic, with A/B-tested CTA and post-spin **`CongratulationsOverlay`**. **`/`** and unknown paths redirect to **`/wheel`** (including legacy `/win-overlay`).

## How to Run

```sh
cd ~/.gemini/antigravity/projects/casino-funnels
npm install
npm run dev
```

http://localhost:5173 → `/wheel`

## Stack

- React 19 + TypeScript
- Vite 8
- Tailwind CSS v4 (via @tailwindcss/vite)
- React Router 7

## Routes

| Route | Purpose |
|-------|---------|
| `/` | Redirect → `/wheel` |
| `/wheel` | Prize wheel + `CongratulationsOverlay` after spin |
| `*` | Redirect → `/wheel` |

## Key Files

| Path | Purpose |
|------|---------|
| `src/App.tsx` | React Router config |
| `src/lib/affiliateLink.ts` | `getAffiliateHref()` from `VITE_AFFILIATE_LINK` |
| `src/hooks/usePageSEO.ts` | Per-route `document.title` + meta / OG (client) |
| `src/components/ComplianceFooter.tsx` | Shared legal footer |
| `src/components/CongratulationsOverlay.tsx` | Post-spin conversion modal |
| `src/pages/SpinWheel.tsx` | /wheel — canvas wheel + overlay |
| `functions/_middleware.js` | Cloudflare Pages A/B cookie on `/wheel` |

## Affiliate Links

Set **`VITE_AFFILIATE_LINK`** at build time (see `.env.example`, Cloudflare Pages env). CTAs and timer redirect use `getAffiliateHref()`; invalid or missing env shows a disabled state instead of a broken relative URL.

## Compliance

Funnel pages include `<ComplianceFooter />` with 18+ / responsible gaming / 1-800-GAMBLER messaging aligned with ad policy.

## Product docs

| Document | Purpose |
|----------|---------|
| [[PRD-clarity-insights-agent]] | PRD: autonomous insights agent on Clarity (REST, optional MCP, instrumentation, LLM) — **source of truth before planning this initiative** |
| [[plans-and-tasks]] | תכנון ומשימות (ממופה מה-PRD אחרי **`/plan`** / `workflows/plan.md`) |

## CI & tests

GitHub Actions: lint, build, Playwright smoke on main/PRs. Locally: `npm run build && npm run test:e2e` (preview needs `dist/`).

## Build

```sh
npm run build   # outputs to dist/
```
