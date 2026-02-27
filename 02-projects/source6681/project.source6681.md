---
project: source6681
status: active
path: ~/.gemini/antigravity/projects/source6681
type: WEB
agents: [frontend-specialist, backend-specialist, test-engineer]
---

# source6681

Vintage luxury handbag archive and dropship e-commerce. React + Vite + Supabase.

## How to Run

```sh
cd ~/.gemini/antigravity/projects/source6681
npm install
cp .env.example .env
# Set VITE_SUPABASE_URL, VITE_SUPABASE_PUBLISHABLE_KEY
npm run dev
```

http://localhost:5173 | Admin: http://localhost:5173/admin

## Key Directories

| Path | Purpose |
|------|---------|
| `src/` | React app |
| `src/components/admin/` | Admin panel (lazy-loaded) |
| `supabase/functions/` | Edge Functions |
| `supabase/migrations/` | SQL migrations |

## Edge Functions

- `fetch-ebay-item` — Import from eBay URL (admin only)
- `check-dropship-status` — Sync sold status (admin or cron)
- `proxy-image` — Proxy eBay images (no auth)
- `get-exchange-rate` — USD→ILS (no auth)

## Scripts

| Command | Purpose |
|---------|---------|
| `npm run dev` | Dev server (5173) |
| `npm run build` | Production build |
| `npm run create-admin` | Create admin user |
| `npm run check-browser` | Playwright smoke test |

## eBay Setup

1. [eBay Developer](https://developer.ebay.com/) → App ID, Cert ID
2. Supabase Edge Functions Secrets: `EBAY_APP_ID`, `EBAY_CERT_ID`

## Reference

- [[04-knowledge/reference/source6681-architecture|Architecture & API]]
- [[04-knowledge/reference/source6681-security-audit|Security audit]]
- [[04-knowledge/standards/source6681-standards|Standards]]
- Remaining tasks: `docs/plans/2026-02-27-source6681-remaining-tasks.md`
