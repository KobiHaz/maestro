---
project: source6681
type: reference
---

# source6681 — Architecture & API

React SPA on Vercel, Supabase (Auth, Postgres, Storage, Edge Functions). Admin lazy-loaded.

## Structure

```
src/pages/            → Routes (Index, Admin, About, FAQ...)
src/components/       → Shared UI (ArchiveFeed, ProductModal, ErrorBoundary...)
src/components/admin/ → Admin-only (lazy, never import in public pages)
src/hooks/            → use-wishlist, use-toast, use-mobile
src/lib/              → format-price, proxy-image, product-utils, ga-loader, analytics, logger
src/integrations/     → supabase client, types
supabase/functions/   → Edge Functions
supabase/migrations/  → SQL
```

## Data Flow

### Public (Archive)

```
ArchiveFeed (Index)
├── fetchProductsPage() — Supabase: .eq(brand_id), .eq(condition_rank), .eq(is_sold), .or(ilike) + .range() pagination
├── URL sync — useSearchParams(?brandId, ?conditionRank, ?status, ?q) → shareable links
├── Infinite scroll — IntersectionObserver, loadMore, PAGE_SIZE=24
├── Wishlist — localStorage (use-wishlist)
├── ErrorBoundary — wraps routes, catches component errors
├── ArchiveSkeleton — loading state (no "LOADING ARCHIVE...")
└── ProductModal — similar products via Supabase query
```

### Admin

```
Admin → AdminDashboard (is_admin RPC check first)
├── products CRUD — supabase.from("products")
├── ProductForm — eBay import (fetch-ebay-item), Storage upload
├── BrandsManager — brands table + Storage
└── check-dropship-status — Edge Function
```

## Routes

| Path | Access |
|------|--------|
| `/` | Public — archive grid |
| `/about`, `/terms`, `/faq`, `/shipping-returns` | Public |
| `/admin` | Admin — login + dashboard |

## Entity: Product

- `products` table. `brand_id` → brands. `brand` denormalized for fallback.
- `Product.brands?.name ?? product.brand ?? extractBrand(title)` for display.
- `Product.brands?.logo_url` — brand logo in ProductModal (main + similar products).
- Brand normalization: DB trigger `products_normalize_brand`.

## Edge Functions

| Function | Auth | Purpose |
|---------|------|---------|
| `fetch-ebay-item` | Admin Bearer | Import from eBay URL |
| `check-dropship-status` | Admin or `x-cron-secret` | Sync sold status |
| `proxy-image` | None | Proxy eBay images (rate-limit stub in _shared) |
| `get-exchange-rate` | None | USD→ILS rate |

**CORS:** `source6681.com`, `localhost:5173`, Vercel preview URLs.

## RLS / Security

- **products:** SELECT all, INSERT/UPDATE/DELETE via `is_admin(auth.uid())`
- **brands:** SELECT all, INSERT/UPDATE/DELETE via `is_admin(auth.uid())`
- **storage:** Admin-only policies
- **Admin route:** `is_admin` RPC check before dashboard

## CI/CD

- GitHub Actions: lint, build, test on push/PR to main and feat/**
- Vercel deploy: production on push to main
- vercel.json images domain: build-time injection from VITE_SUPABASE_URL ([[04-knowledge/reference/source6681-vercel-setup|Vercel]])

## API Quick Reference

Full spec: [[04-knowledge/reference/source6681-api|source6681-api]].

- **fetch-ebay-item:** POST, `{ "ebay_id": "v1|..." }`. 401/400/404/500.
- **check-dropship-status:** POST, `{ "ebay_ids": [...] }` or empty for cron. 401/403/503/500.
- **proxy-image:** GET `?u=<base64_url>`.
- **get-exchange-rate:** GET. Returns `{ rate, base, target }`.

Secrets: `EBAY_APP_ID`, `EBAY_CERT_ID`, `CRON_SECRET`.
