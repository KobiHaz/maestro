---
project: source6681
type: reference
---

# source6681 — eBay Setup

Used by: `fetch-ebay-item`, `check-dropship-status`.

---

## 1. eBay Developer Account

1. Go to [eBay Developer Portal](https://developer.ebay.com/)
2. Sign in or create an account
3. Create an application → get **App ID** and **Cert ID**
4. For production: use Production credentials
5. For sandbox testing: use Sandbox credentials and set `EBAY_SANDBOX=true` (check-dropship only)

---

## 2. Supabase Edge Functions Secrets

Add in **Supabase Dashboard → Project Settings → Edge Functions → Secrets**:

| Secret | Required | Description |
|--------|----------|-------------|
| `EBAY_APP_ID` | Yes | eBay App ID from Developer Portal |
| `EBAY_CERT_ID` | Yes | eBay Cert ID from Developer Portal |
| `EBAY_SANDBOX` | No | `true` = use sandbox API (check-dropship-status) |
| `GEMINI_API_KEY` | For AI | למלוי Era, תיאור בעברית (Editor's Note) ו-Dimensions (fallback). בלי המפתח — השדות האלה יישארו ריקים ב-Auto-Fill. |

---

## 3. API Usage

- **fetch-ebay-item** — Imports item from eBay Browse API. Uses OAuth Client Credentials. Admin Bearer only.
- **check-dropship-status** — Syncs sold/ended status from eBay. Supports cron via `x-cron-secret` or manual Admin Bearer.

See [[04-knowledge/reference/source6681-api|API Reference]].
