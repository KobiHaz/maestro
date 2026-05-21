---
project: consul-house
status: active
type: NO-CODE
platform: Make.com
---

# Consul House — Lead Automation ("The Brain")

Automated lead funnel for Consul House real estate. WordPress webhooks → normalize → deduplicate → iplan CRM.

## Client & Contract

| | |
|-|-|
| **Client** | Consul House (ConsulHouse.co.il) |
| **Supplier** | סו מדיה בע"מ (Xsheva / Kobi) |
| **Contract signed** | 11/03/2026 |
| **Model** | Managed — ₪3,500 setup + ₪550/month retainer |
| **Add-on available** | SMS/Email to client post-registration (+₪1,000) |

Payment milestones: 50% advance (on signature) → 0% beta test → 50% on delivery + go-live.

---

## System Logic — "The Brain"

```
WordPress (ConsulHouse.co.il)
  └─ Webhook → Make.com
        ├─ 1. Parse + Normalize
        │     └─ Text parsing, phone normalization (Israeli format)
        ├─ 2. Deduplicate
        │     └─ Google Sheets: phone appeared in last 30 days? → skip / flag
        ├─ 3. Push to iplan CRM
        │     └─ iplan API (API Key + Form ID)
        │     └─ Store result in Sheets (success / failure / duplicate)
        └─ 4. Retry
              └─ Auto-retry failed iplan sessions
```

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Automation | Make.com (primary), Zapier (fallback) |
| Lead source | ConsulHouse.co.il — WordPress webhook |
| Deduplication DB | Google Sheets |
| CRM target | iplan (API Key + Form ID) |
| Notifications (add-on) | SMS + Email via Make.com |

---

## Make.com Scenarios

| Scenario | Trigger | Purpose |
|----------|---------|---------|
| Lead Ingestion | WordPress webhook | Receive + normalize incoming lead |
| Deduplication Check | Called from Ingestion | Check Sheets for phone in last 30 days |
| iplan Push | After dedup pass | Send clean lead to iplan CRM |
| Retry Handler | Scheduled / error hook | Re-process failed iplan calls |
| Notification (add-on) | After successful push | SMS + email confirmation to client |

---

## Google Sheets Schema

| Column | Purpose |
|--------|---------|
| timestamp | Lead arrival time |
| phone | Normalized Israeli phone (05X-XXXXXXX) |
| name | Full name |
| source | WordPress form / campaign |
| iplan_status | success / failed / duplicate |
| iplan_lead_id | ID returned by iplan on success |
| retry_count | Number of retry attempts |

---

## iplan Integration

- **Auth:** API Key in Make.com connection
- **Required fields:** Form ID, phone (normalized), name, source
- **Response:** Lead ID on success, error message on failure
- **Rate limits:** TBD — monitor in first week

---

## Blockers (from client)

- [ ] iplan API Key
- [ ] iplan Form ID
- [ ] WordPress Admin access to ConsulHouse.co.il

---

## Retainer Scope (₪550/month)

- Make.com scenario management + updates
- Uptime monitoring
- Bug fixes (first 14 days free regardless of contract)

---

## Working with Claude on This Project

Claude can help with:
- **Make.com module configuration** — JSON structures, filters, iterators, error handlers
- **Google Sheets formulas** — deduplication logic, status tracking
- **iplan API calls** — HTTP module setup, headers, body mapping
- **Webhook normalization** — phone parsing, field mapping from WP forms
- **Client communications** — update emails, scope changes, invoices
- **System documentation** — scenario diagrams, SOPs

Always load this file before working on consul-house tasks.
