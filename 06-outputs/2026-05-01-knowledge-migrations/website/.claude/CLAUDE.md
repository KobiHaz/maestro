# website (Xsheva) — Project Context

Xsheva brand marketing website. Lead generation architecture for US market.
CRM, automations, affiliate services. Mysterious, high-tech, results-driven brand.

**Stack:** React 19 + TypeScript + Vite + Tailwind v4 + Firebase + ImageKit

---

## Quick Start

```sh
npm install
npm run dev    # Vite dev server
npm run test   # Vitest
```

---

## Brand Identity

- **Vision:** Growth architecture — "secret formula" for business opportunities with mathematical precision
- **Tone:** Direct, Minimalist, Confident, Intriguing
- **Colors:** Deep Space Black, Stark White, Neon Orange (#FF6B35)
- **Typography:** Sans-Serif Geometric, clean, wide, premium
- **Taglines:** "The Growth Variable" | "Decoded Demand" | "Autonomous Opportunity" | "Multiply Everything"

---

## Tech Stack Detail

| Layer | Tech |
|-------|------|
| Framework | React 19, TypeScript, Vite |
| Styling | Tailwind v4, Framer Motion |
| Forms | React Hook Form |
| Server state | TanStack Query |
| Backend | Firebase (Firestore, Functions, Auth, Hosting) |
| Shared | @cms/shared |
| Images | ImageKit |
| Testing | Vitest, Playwright |
| Monitoring | Sentry, Firebase Analytics |

---

## Shared Package

Uses `@cms/shared` — components and utilities shared with the cms monorepo.
**Rule:** Changes to `@cms/shared` affect both website and cms verticals.

---

## Core Rules

1. **Brand consistency** — always match Xsheva tone (direct, minimal, confident); no fluff
2. **TanStack Query for server state** — not manual useEffect + useState
3. **ImageKit for all images** — use ImageKit transformations, not raw URLs
4. **Framer Motion for animations** — keep animations minimal and purposeful
5. **US market** — English only, LTR
6. **Sentry** — wrap critical paths in error boundaries; don't swallow errors

---

## Reference

- [Architecture](.claude/knowledge/architecture.md)
