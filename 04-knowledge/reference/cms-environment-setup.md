# CMS — Environment Setup

> Full guide was in project `docs/ENVIRONMENT_SETUP.md`.

## Files

- **.env.local** — Local dev (gitignored)
- **.env** — Production build
- **.env.example** — Template

## Scripts

| Script | Uses | Purpose |
|--------|------|---------|
| `pnpm dev` | .env.local | Local |
| `pnpm build` | .env | Production |
| `pnpm deploy` | .env | Build + deploy |

## Required

```bash
VITE_GA4_MEASUREMENT_ID=G-xxx
```

## Vite Order

.env → .env.local (overrides) → .env.[mode]
