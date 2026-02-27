---
project: source6681
type: reference
---

# source6681 — Architecture & API

React SPA on Vercel, Supabase (Auth, Postgres, Storage, Edge Functions). Admin lazy-loaded.

## Structure

```
src/pages/          → Routes (Index, Admin, About, FAQ...)
src/components/     → Shared UI
src/components/admin/ → Admin-only (lazy, never import in public pages)
src/hooks/          → use-wishlist, use-global-discount
src/lib/            → format-price, proxy-image, analytics
supabase/functions/ → Edge Functions
supabase/migrations/ → SQL
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
- Brand normalization: `src/lib/brand-canonical.json`, DB trigger `products_normalize_brand`.

## Edge Functions

| Function | Auth | Purpose |
|---------|------|---------|
| `fetch-ebay-item` | Admin Bearer | Import from eBay URL |
| `check-dropship-status` | Admin or `x-cron-secret` | Sync sold status |
| `proxy-image` | None | Proxy eBay images |
| `get-exchange-rate` | None | USD→ILS rate |

**CORS:** `source6681.com`, `localhost:5173`, Vercel preview URLs.

## API Quick Reference

- **fetch-ebay-item:** POST, `{ "ebay_id": "v1|..." }`. 401/400/404/500.
- **check-dropship-status:** POST, `{ "ebay_ids": [...] }` or empty for cron. 401/403/503/500.
- **proxy-image:** GET `?u=<base64_url>`.
- **get-exchange-rate:** GET. Returns `{ rate, base, target }`.

Secrets: `EBAY_APP_ID`, `EBAY_CERT_ID`, `CRON_SECRET`.
