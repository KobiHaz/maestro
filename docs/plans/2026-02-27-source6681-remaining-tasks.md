# source6681 — Pending Tasks

> Consolidated plan: Vercel React Best Practices, OPEN-TASKS.

**Date:** 27 February 2026

---

## 1. Vercel React Best Practices (~1–2 hours)

| # | Task | File |
|---|------|------|
| 1 | Hoist BRAND_PATTERNS to module level | `ArchiveGridItem.tsx` |
| 2 | Defer Analytics + Speed Insights loading | `App.tsx` |
| 3 | Defer Google Analytics until after first paint | `index.html`, `main.tsx`, `ga-loader.ts` |
| 4 | content-visibility for Archive grid/list | `index.css`, `ArchiveFeed.tsx` |
| 5 | (Optional) localStorage with version for wishlist | `use-wishlist.ts` |
| 6 | (Phase 2) Lucide direct imports | Optional |

Source: vercel-react-best-practices-implementation. Recommended to use executing-plans.

---

## 2. Product & UX

### Purchase flow
- Cart → payment → confirmation. No Checkout currently (inquiry-only).

### Coupon
- When checkout is added: create_order RPC with server-side coupon validation.

### CTA
- Update "I Want This" / "Inquire" to "Buy Now" or alternative.

### eBay
- Check eBay availability API, document rate limits.

---

## 3. Performance & optimization

- Infinite scroll / progressive loading
- Server-side filtering and search (Supabase)
- Skeleton loaders, error boundaries
- URL filters (shareable)
- ProductModal: navigate similar products without reload

---

## 4. Security (not urgent)

- connection pooling, least-privilege
- API rate limiting
- is_admin check in Admin.tsx before dashboard

---

## 5. Testing

- Unit tests (formatPrice, useGlobalDiscount)
- check-browser — expand admin coverage
