# source6681 — Cursor Rules & Standards

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

## Naming

| Type | Pattern | Example |
|------|---------|---------|
| Components | PascalCase | `ArchiveGridItem.tsx`, `ProductModal.tsx` |
| Hooks | kebab-case, `use-` | `use-wishlist.ts`, `use-global-discount.ts` |
| Lib | kebab-case | `format-price.ts`, `proxy-image.ts` |
| Migrations | `YYYYMMDDHHMMSS_snake.sql` | `20260226120000_add_brand.sql` |
| Plans | `YYYY-MM-DD-topic.md` | `2026-02-27-source6681-remaining-tasks.md` |

## Plan Lifecycle

**Whenever you complete a task or plan:**

1. Update the relevant docs — Obsidian `02-projects/source6681`, `04-knowledge/reference/source6681-*`
2. Suggest deleting the old work plan if it has been fully implemented
3. Don't delete plans yourself — suggest deletion and let the user approve

## Reference

- Architecture & API: `04-knowledge/reference/source6681-architecture.md`
- Security: `04-knowledge/reference/source6681-security-audit.md`
- Remaining tasks: `docs/plans/2026-02-27-source6681-remaining-tasks.md` (in vault)
