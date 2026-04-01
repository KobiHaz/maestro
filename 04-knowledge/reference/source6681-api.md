---
project: source6681
type: reference
---

# source6681 — Edge Functions API Reference

Base URL: `https://<project-ref>.supabase.co/functions/v1/<function-name>`

CORS: `source6681.com`, `localhost:5173`, Vercel preview URLs.

---

## Quick Start

| Function | Auth | Method |
|----------|------|--------|
| fetch-ebay-item | Admin Bearer | POST |
| check-dropship-status | Admin Bearer or `x-cron-secret` | POST |
| proxy-image | None | GET |
| get-exchange-rate | None | GET |

---

## Authentication

### Admin Bearer

```http
Authorization: Bearer <supabase_jwt>
```

JWT must belong to a user with `is_admin(auth.uid()) = true`.

### Cron Secret

```http
x-cron-secret: <CRON_SECRET>
```

Used for scheduled `check-dropship-status` (no body; syncs all products with `ebay_item_id`).

---

## Endpoints

### fetch-ebay-item

**Import product from eBay URL.** Admin only.

**Request:**
```http
POST /functions/v1/fetch-ebay-item
Authorization: Bearer <jwt>
Content-Type: application/json

{ "ebay_id": "v1|123456789|0" }
```

`ebay_id` — eBay item ID. If without `v1|` prefix, formatted as `v1|{id}|0`.

**Response (200):**
```json
{
  "success": true,
  "title": "...",
  "price": 199.99,
  "original_price_usd": 249.99,
  "buy_price_usd": 199.99,
  "currency": "USD",
  "material": "Leather",
  "height_cm": 25,
  "width_cm": 35,
  "depth_cm": 12,
  "images": ["https://..."],
  "description": "תיאור בעברית...",
  "original_description": "...",
  "condition": "Pre-Owned",
  "condition_rank": "A",
  "year_era": "2000s Tom Ford Era",
  "brand": "Gucci",
  "model": "...",
  "color": "...",
  "all_aspects": { ... }
}
```

**Error codes:**

| Code | Body | Cause |
|------|------|-------|
| 401 | `{ "error": "Unauthorized" }` | Missing or invalid Authorization |
| 401 | `{ "error": "Invalid token" }` | JWT validation failed |
| 403 | `{ "error": "Admin access required" }` | User is not admin |
| 400 | `{ "error": "Please provide ebay_id" }` | Missing ebay_id in body |
| 404 | `{ "error": "Item not found or eBay API error: 404" }` | eBay item not found |
| 500 | `{ "error": "eBay credentials not configured" }` | EBAY_APP_ID / EBAY_CERT_ID missing |
| 500 | `{ "error": "..." }` | Server error |

---

### check-dropship-status

**Sync sold status from eBay.** Admin or cron.

**Manual (Admin):**
```http
POST /functions/v1/check-dropship-status
Authorization: Bearer <jwt>
Content-Type: application/json

{ "ebay_ids": ["v1|123|0", "v1|456|0"] }
```

`ebay_ids` optional. Max 100 items. Empty array → `{ success: true, processed: 0, results: [] }`.

**Cron (Scheduled):**
```http
POST /functions/v1/check-dropship-status
x-cron-secret: <CRON_SECRET>
```

No body. Fetches all products with `ebay_item_id`, `is_sold = false`.

**Response (200):**
```json
{
  "success": true,
  "processed": 5,
  "new_sold_count": 2,
  "results": [
    { "ebay_id": "v1|123|0", "success": true, "status": "Sold", "newly_sold": true, "title": "..." },
    { "ebay_id": "v1|456|0", "success": true, "status": "Active", "newly_sold": false, "title": "..." }
  ]
}
```

**Error codes:**

| Code | Body | Cause |
|------|------|-------|
| 401 | `{ "error": "Unauthorized" }` | Missing auth, invalid Bearer, or wrong x-cron-secret |
| 403 | `{ "error": "Admin access required" }` | Bearer used but user not admin |
| 400 | `{ "error": "Invalid request body: ..." }` | Invalid JSON body |
| 503 | `{ "error": "eBay API auth failed. Check: ..." }` | eBay credentials issue |
| 500 | `{ "error": "..." }` | Server error |

---

### proxy-image

**Proxy eBay images.** No auth.

**Request:**
```http
GET /functions/v1/proxy-image?u=<base64_encoded_url>
# or
GET /functions/v1/proxy-image?url=<url_encoded>
```

`u` or `url` — Image URL. base64 or plain. Allowed hosts: `i.ebayimg.com`, `i.ebayimg.sandbox.ebay.com`, `thumbs2.ebayimg.com`, `thumbs4.ebayimg.com`.

**Response (200):** Image body with appropriate `Content-Type`, `Cache-Control: public, max-age=604800`.

**Error codes:**

| Code | Body | Cause |
|------|------|-------|
| 400 | `{ "error": "Missing image URL (use ?u= or ?url=)" }` | No u/url param |
| 400 | `{ "error": "Invalid URL encoding" }` | Bad base64 |
| 403 | `{ "error": "URL not in allowed hosts" }` | Domain not whitelisted |
| 429 | `{ "error": "Too many requests" }` | Rate limit (stub: 120/min; see rate-limit.ts) |
| 500 | `{ "error": "Proxy failed" }` | Upstream error or server error |

---

### get-exchange-rate

**USD→ILS rate.** No auth.

**Request:**
```http
GET /functions/v1/get-exchange-rate
```

**Response (200):**
```json
{
  "rate": 3.65,
  "base": "USD",
  "target": "ILS",
  "timestamp": "2026-03-01T12:00:00.000Z"
}
```

On upstream API failure, returns 200 with fallback:
```json
{
  "error": "...",
  "rate": 3.65,
  "isFallback": true
}
```

---

## Error Format

All JSON errors: `{ "error": "string" }`.

---

## Rate Limiting

- **proxy-image:** `_shared/rate-limit.ts` — stub (always allows). TODO: Deno KV or Upstash.
- **Other functions:** No rate limit yet.

Secrets: `EBAY_APP_ID`, `EBAY_CERT_ID`, `CRON_SECRET`. AI (fetch-ebay-item Auto-Fill): `GEMINI_API_KEY` primary; `GROQ_API_KEY` fallback when Gemini fails/quota; `LOVABLE_API_KEY` optional if no Gemini. `EBAY_SANDBOX` (check-dropship sandbox).
