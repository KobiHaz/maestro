---
project: source6681
type: reference
---

# source6681 — Vercel Setup & Best Practices

## CI/CD (Deploy on Push, Preview Deployments)

1. Connect repo to Vercel: [vercel.com/new](https://vercel.com/new)
2. Select GitHub/GitLab/Bitbucket and choose this project.
3. Vercel will:
   - **Deploy production** on push to main (or your production branch)
   - **Create a unique Preview URL** for each Pull Request
4. Add environment variables in Vercel Project Settings → Environment Variables:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_PUBLISHABLE_KEY`
   - `VITE_GA_MEASUREMENT_ID` (optional, for Google Analytics)

## Image Optimization

For Vercel Image Optimization to work, image domains must be whitelisted in `vercel.json`.

**Automatic:** The build script injects the Supabase host from `VITE_SUPABASE_URL` into `vercel.json` before each build. Ensure `VITE_SUPABASE_URL` is set in Vercel Project Settings → Environment Variables.

**Manual fallback:** If `VITE_SUPABASE_URL` is not set, replace `YOUR_PROJECT.supabase.co` in `vercel.json` → `images.domains` with your actual Supabase project host (e.g. `abcdefgh.supabase.co`).

---

## React Best Practices

> [Vercel React Best Practices](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices). **סטטוס מרץ 2026:** מיושם.

| Rule | Fix | סטטוס |
|------|-----|-------|
| 2.3 | Defer Analytics + Speed Insights (requestIdleCallback) | ✅ |
| 6.2 | content-visibility for archive items | ✅ |
| 7.9 | Hoist BRAND_PATTERNS in ArchiveGridItem | ✅ |
| GA | Defer GA until after initial paint | ✅ |

**אופציונלי (P3):** Lucide direct imports — מדוד השפעה על bundle לפני.
