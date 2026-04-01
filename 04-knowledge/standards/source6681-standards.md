# source6681 — Cursor Rules & Standards

> **Extends:** [[04-knowledge/standards/base-coding-standards|base-coding-standards]]. Load both.
> Repo: source6681. Vintage handbag archive/dropship. Read when working on source6681.

## Tech Stack

Vite, React 18, TypeScript, shadcn/ui, Tailwind, Supabase, Vercel

## Entity

- **Product:** `products` table, `brand_id` → brands. Display: `product.brands?.name ?? product.brand ?? extractBrand(title)`.
- **Brand:** First-class. Add in Brands tab before eBay import.

## Security

- Admin only in `src/components/admin/` — never import in public pages.
- Edge Functions: Bearer + admin for fetch-ebay-item, check-dropship-status; `x-cron-secret` for cron.
- RLS: products readable by all, writable by admins. Storage admin-only.

## UI / Styling

- **Text direction & font:** Fixed per component type (Tailwind classes). No dynamic `getTextDirection` — use `dir`, `text-left`/`text-right`, `font-mono` per component.
- ProductModal: title LTR, description RTL. ArchiveItem/TheEditSection: fixed per layout.

## Naming (תוספות ל-base)

| Type | Pattern | Example |
|------|---------|---------|
| Migrations | `YYYYMMDDHHMMSS_snake.sql` | `20260226120000_add_brand.sql` |
| Plans | מקור יחיד בכספת | `04-knowledge/reference/source6681-action-plan.md` |

*Components, Hooks, Lib, Constants — base.*

## Plan Lifecycle

[[04-knowledge/standards/maestro-project-doc-lifecycle]]. תוספת source6681: עדכן גם `source6681-action-plan.md`, `source6681-*`, `source6681-standards` במידת צורך.

## Reference

- Architecture: [[04-knowledge/reference/source6681-architecture]]
- API: [[04-knowledge/reference/source6681-api]]
- Vercel: [[04-knowledge/reference/source6681-vercel-setup]]
- Security & tasks: [[04-knowledge/reference/source6681-action-plan]]
- Plans & tasks: [[02-projects/source6681/plans-and-tasks]]
