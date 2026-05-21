# Consul House — Automation Workflow Detail

## Lead Ingestion Flow (Make.com)

### Module 1 — Webhook (Trigger)
- Type: Custom Webhook
- Source: ConsulHouse.co.il WordPress (Contact Form 7 or similar)
- Expected fields: `name`, `phone`, `email` (optional), `source`, `timestamp`

### Module 2 — Text Parsing / Normalization
- Strip non-digits from phone
- Normalize to Israeli format: `05X-XXXXXXX`
  - Input: `0501234567` / `+9720501234567` → Output: `050-1234567`
- Trim whitespace from name
- Tag source (campaign / form name)

### Module 3 — Google Sheets: Check Duplicate
- Lookup: search `phone` column for match in last 30 days
- Filter: `timestamp >= NOW() - 30 days AND phone = normalized_phone`
- If found: log as `duplicate`, stop scenario

### Module 4 — Google Sheets: Log Lead
- Append row: timestamp, phone, name, source, status=`pending`

### Module 5 — iplan HTTP Call
- Method: POST
- URL: `https://app.iplan.co.il/api/...` (confirm with client)
- Headers: `Authorization: Bearer {API_KEY}`
- Body: `{ "form_id": FORM_ID, "phone": phone, "name": name, "source": source }`

### Module 6 — Update Sheets Status
- On success: update row → `iplan_status=success`, `iplan_lead_id=response.id`
- On failure: update row → `iplan_status=failed`, log error message

### Module 7 — Error Handler / Retry
- On iplan failure: route to retry queue
- Retry up to 3 times (Make.com error handler or separate scheduled scenario)

---

## Deduplication Logic

```
phone_normalized = normalize(incoming_phone)
last_30_days = rows WHERE timestamp >= TODAY-30
match = last_30_days WHERE phone == phone_normalized

IF match EXISTS:
  log as duplicate (don't push to iplan)
  STOP
ELSE:
  proceed to iplan push
```

---

## Error Scenarios

| Error | Action |
|-------|--------|
| Webhook malformed | Log to Sheets, send alert |
| iplan 401 | Check API Key, alert Kobi immediately |
| iplan 429 rate limit | Back off 60s, retry |
| iplan 5xx | Retry up to 3x, then mark failed |
| Sheets API error | Log locally, alert |

---

## Monitoring Checklist (Monthly Retainer)

- [ ] Make.com scenario runs — no unexpected errors
- [ ] iplan push success rate > 95%
- [ ] Retry queue empty or managed
- [ ] Sheets data clean (no corrupt rows)
- [ ] Webhook still receiving from WordPress
