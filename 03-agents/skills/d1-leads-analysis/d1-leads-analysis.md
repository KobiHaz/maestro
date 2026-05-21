---
name: d1-leads-analysis
description: Query the Cloudflare D1 `leads-sunflower` database (LuckyMint / casino-funnels project) for canonical signup, FTD, QFTD, and traffic-quality metrics. Use whenever the user asks how many leads/signups/deposits we got today/yesterday/this-week, asks to verify Meta CAPI numbers against the database, asks about postback success vs failure rates, or asks "did the campaign convert" / "is the data clean". The skill enforces the canonical rule: NEVER trust the `leads` table for headline counts — always count from `postback_log` filtered to `outcome='success' AND token_ok=1` to exclude test postbacks, scanner traffic, and unauthorized noise.
allowed-tools: Bash
---

# D1 Leads Analysis — LuckyMint / casino-funnels

Canonical playbook for analyzing the `leads-sunflower` D1 database (id `4e8f1253-baea-4fab-9203-17ae398597ab`).

## ⚠️ The single most important rule

**Do not count signups/FTDs/QFTDs from the `leads` table.** That table is the application's working state — it gets polluted by:
- QA / smoke-test traffic that we run against prod
- Stale rows from old click_id flows
- Rows with NULL postback timestamps (lead created, no postback ever)

The **affiliate's postback to our endpoint is the source of truth**. Every postback attempt (real, fake, scanner, malformed) is logged to `postback_log`. The canonical filter is:

```sql
WHERE outcome = 'success' AND token_ok = 1
```

Everything else is noise — `unauthorized` (16+ per day, mostly scanners and our own tests), `service_unavailable` (transient backend issues), `click_id_not_found` (postback for an unknown click_id).

## Authenticating to D1

The user runs `wrangler` via OAuth, but in non-interactive shells the OAuth refresh tends to fail. Two paths:

1. **Preferred:** ask the user for a `CLOUDFLARE_API_TOKEN` (Custom Token → Account → D1 → Read on the `leads-sunflower` DB) and run:

   ```bash
   cd /Users/kobihazout/.gemini/antigravity/projects/wheel
   CLOUDFLARE_API_TOKEN='<token>' npx wrangler d1 execute leads-sunflower --remote --json --command "<SQL>"
   ```

2. **Fallback:** ask the user to run `npx wrangler login` in their own terminal, then re-try without the env var.

Always use `--remote` and `--json` (the latter makes parsing trivial). Do not rely on the table-formatted output — it truncates.

## Schema (as of 2026-04-29)

### `postback_log` — the truth source

```sql
CREATE TABLE postback_log (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  received_at TEXT    NOT NULL,        -- ISO 8601, e.g. '2026-04-29T07:14:33Z'
  event       TEXT    NOT NULL,        -- 'su' | 'ftd' | 'qftd' | 'ping' | other
  click_id    TEXT    NOT NULL,        -- the affiliate's click_id (matches leads.click_id)
  token_ok    INTEGER NOT NULL,        -- 1 = bearer token valid, 0 = invalid
  outcome     TEXT    NOT NULL,        -- 'success' | 'unauthorized' | 'service_unavailable' | 'click_id_not_found' | …
  ip          TEXT    NOT NULL,
  user_agent  TEXT    NOT NULL
);
-- Indexes: idx_postback_log_click_id, idx_postback_log_received_at
```

`event` enum (Crown spec): `su` (signup), `ftd` (first deposit), `qftd` (qualified first deposit, $250+), `ping` (health check).

### `leads` — application state (only use for joins, never for headline counts)

Has columns `click_id`, `fbclid`, `email`, `phone`, `request_ip`, `request_ua`, plus timestamps `created_at`, `updated_at`, `postback_su_at`, `postback_ftd_at`, `postback_qftd_at`, plus their VIRTUAL `*_date` and `*_time` splits. Use only when correlating attribution data with a postback (`JOIN postback_log USING(click_id)`).

There is also a view `leads_enriched` that re-derives `acquisition_channel` from raw attribution columns.

## Canonical queries

### Q1 — How many real signups/FTDs/QFTDs today (or any date range)?

⚠️ **CRITICAL — count by `leads.created_at`, not by `postback_log.received_at`.**

Crown batches postbacks every 1–2 hours. A user who signed up at 23:14 UTC may not generate a postback until 01:19 UTC the next day. If you count by `received_at`, you'll overcount today and undercount yesterday — and **disagree with Crown's affiliate dashboard**, which counts by signup time.

The canonical query joins postback_log to leads and groups by the **lead's** creation date:

```sql
SELECT
  substr(l.created_at, 1, 10) AS signup_date,
  p.event,
  COUNT(*) AS n
FROM postback_log p
JOIN leads l ON l.click_id = p.click_id
WHERE p.outcome = 'success'
  AND p.token_ok = 1
  AND p.user_agent LIKE 'python-requests/%'  -- Crown legitimate UA
  AND p.ip LIKE '2600:1900:0:2d0%::%'        -- Crown GCP IPv6 range
GROUP BY signup_date, p.event
ORDER BY signup_date, p.event;
```

For a quick non-joined check of postback volume (less accurate, but useful for diagnosing pipeline issues):

```sql
SELECT substr(received_at, 1, 10) AS date, event, COUNT(*) AS n
FROM postback_log
WHERE outcome = 'success' AND token_ok = 1
  AND received_at >= '2026-04-27'
GROUP BY date, event
ORDER BY date, event;
```

If the two queries disagree by N, that N is your "in-flight batch" — postbacks for signups on day D-1 that Crown sent on day D.

### Q2 — Postback health (what's failing and why)

```sql
SELECT
  substr(received_at, 1, 10) AS date,
  event,
  outcome,
  token_ok,
  COUNT(*) AS n
FROM postback_log
WHERE received_at >= '2026-04-27'
GROUP BY date, event, outcome, token_ok
ORDER BY date, event, outcome;
```

Use this to spot:
- spikes in `unauthorized` (scanner attacks or wrong token from Crown)
- `service_unavailable` (Worker/Meta CAPI fail loop — needs investigation)
- `click_id_not_found` (Crown postbacks for click_ids we never issued — cookie/sticky bug or Crown timing)

### Q3 — Reconcile against Meta dashboard

When the user shares a Meta Ads Manager screenshot:

```sql
-- Real SU postbacks for the day Meta reports
SELECT COUNT(*) AS real_su
FROM postback_log
WHERE event = 'su'
  AND outcome = 'success' AND token_ok = 1
  AND substr(received_at, 1, 10) = '<DATE>';

-- Of those, how many had fbclid (i.e. would have been sent to Meta CAPI)
SELECT COUNT(*) AS sent_to_meta
FROM postback_log p
JOIN leads l ON l.click_id = p.click_id
WHERE p.event = 'su'
  AND p.outcome = 'success' AND p.token_ok = 1
  AND substr(p.received_at, 1, 10) = '<DATE>'
  AND l.fbclid <> '' AND l.fbclid IS NOT NULL;
```

CAPI dispatches Lead only when `fbclid` is present (gated post-2026-04-28). The "sent_to_meta" number should match Meta's reported leads to within a few minutes' lag.

### Q4 — Identify test postbacks polluting the log

```sql
SELECT ip, user_agent, COUNT(*) AS n
FROM postback_log
WHERE outcome = 'unauthorized'
  AND received_at >= '2026-04-27'
GROUP BY ip, user_agent
ORDER BY n DESC
LIMIT 20;
```

Recurring IPs / UAs here are usually our own QA traffic, scanner bots, or Crown sending the wrong token. If user wants those filtered from analytics, propose adding an `is_test` flag or filtering by IP at query time.

### Q5 — Funnel: SU → FTD → QFTD per day

```sql
SELECT
  substr(received_at, 1, 10) AS date,
  SUM(CASE WHEN event='su'   AND outcome='success' AND token_ok=1 THEN 1 ELSE 0 END) AS su,
  SUM(CASE WHEN event='ftd'  AND outcome='success' AND token_ok=1 THEN 1 ELSE 0 END) AS ftd,
  SUM(CASE WHEN event='qftd' AND outcome='success' AND token_ok=1 THEN 1 ELSE 0 END) AS qftd
FROM postback_log
WHERE received_at >= '<START>'
GROUP BY date
ORDER BY date;
```

Note: FTD/QFTD usually arrive hours-to-days after SU, so the same-day funnel will undercount. Compare against a leads-table query joined by `click_id` if you need cohort analysis.

## How to deliver results to the user

1. **Lead with the canonical count** (filtered to `success + token_ok=1`), one number per day, in a table.
2. **Show the noise too** if it's relevant — `unauthorized` count and `service_unavailable` count flag whether the system is healthy.
3. **Reconcile against external sources** the user mentions (Meta Ads, Crown affiliate dashboard, GA4) — call out matches and explain mismatches.
4. **Never** quote "leads = X today" from the `leads` table without explicitly saying "application state, includes test rows."

## UA / IP fingerprints — known sources

When you see a successful postback, check the UA + IP before reporting it as "real customer signup":

| Pattern | Identity | Action |
|---|---|---|
| `python-requests/2.32.3` from IPv6 `2600:1900:0:2d0X::*` | **Crown legitimate** (their affiliate platform on GCP). Click_ids are real UUIDs, lead row exists with real `fbclid`. | Count as real. |
| `curl/8.x` from any IP | Manual CLI test (us). Often paired with another event 1–4s later from same click_id. | Filter out. |
| `Mozilla/... Chrome/14X` from desktop IP | Browser visit — someone clicked the URL directly. Almost always a test or accidental share. | Filter out unless click_id matches a real lead with fbclid. |
| `WhatsApp/2.X.X.X` | WA link preview crawler — fires when a postback URL is shared in a WA chat (e.g. integration testing with Crown over WhatsApp). Click_id often literal `"click_id"` or `"click_Id"` placeholder. | Filter out — these are template URLs, not real events. |
| `python-requests/X` from non-GCP IP, sporadic times | Likely external monitor / scanner / our own tooling. | Investigate before counting. |

To filter test/synthetic traffic in queries:

```sql
-- Real Crown postbacks only
WHERE outcome = 'success' AND token_ok = 1
  AND user_agent LIKE 'python-requests/%'
  AND ip LIKE '2600:1900:0:2d0%::%'
```

If Crown migrates infrastructure (different GCP project, AWS, on-prem) the IP range will shift — re-derive from a fresh sample of postbacks that join to leads with real `fbclid`.

## Manual backfills — when to fire CAPI, when not

When the user asks to mark click_ids as SU/FTD/QFTD from a Crown affiliate dashboard list (manual reconciliation), **do NOT trigger Meta CAPI for those rows**, with rare exceptions.

### The two failure modes

`functions/lib/metaCapi.js` derives `event_time` from `eventTimeIso` (set by the postback handler to "now"), or falls back to `Date.now()`. There is no path that uses the lead's original `created_at`. So:

1. **Replay through `/api/postback` today** → Meta gets `event_time = now`. The original signup may have been days/weeks ago, but Meta will think it just happened and attribute it to today's running ads. **Pollutes attribution and corrupts ad-set learning.** ❌
2. **Direct Graph API call with `event_time = lead.created_at`** → if older than 7 days, Meta rejects (`Event time too old`). Within 7 days, Meta accepts but the event was "missed" by the live pipeline for a reason — usually data quality (missing fbclid, broken click_id, etc.) — so you'd be sending degraded events. ⚠️
3. **Direct Graph API call with falsified `event_time`** → outright lie, distorts both attribution and reporting. ❌

### The rule

**For manual backfills from a Crown reconciliation list:**
- Update `leads.postback_su_at` and insert an audit row in `postback_log` with `ip='manual-backfill'` and `user_agent='manual-backfill-YYYY-MM-DD-<reason>'`. (Already documented above.)
- Leave `leads.capi_su_sent_at` as **NULL**. This is the signal that the row is intentionally not sent to Meta.
- Document the decision in the conversation: these are bookkeeping events for internal reporting and Crown reconciliation, not Meta optimization signals.

**Exceptions** where firing CAPI is OK:
- Lead is < 6 days old AND was missed by the live pipeline due to a reproducible bug (e.g. transient Worker outage, Crown retry timing) — in that case fire via `/api/postback` so the same dedup/event_id logic runs naturally. Need `POSTBACK_TOKEN` from Pages env.
- User explicitly opts in despite the warning, in which case quote them their own decision and use direct Graph API with `event_time = lead.created_at` so at least the event time is honest. Need `META_CAPI_TOKEN` from Pages env.

### Why Cloudflare Pages secrets aren't fetchable

`POSTBACK_TOKEN`, `META_CAPI_TOKEN`, `LEAD_WEBHOOK_TOKEN` are all stored as **encrypted env vars** in Cloudflare Pages. They are decrypted only at runtime inside the Pages Function — the API and dashboard expose names but not values (the dashboard "Reveal" button is the only path, and only for authorised users). Don't promise to fetch them via any token; ask the user to paste from the dashboard if they're truly needed.

## Common gotchas

- **`leads.postback_su_at` ≠ count of real SUs.** A row in `leads` with `postback_su_at` filled means the postback was processed and applied to that row — but rows from QA test postbacks pollute this. Trust `postback_log`.
- **Date columns are VIRTUAL** (`postback_su_date = substr(postback_su_at, 1, 10)`). Free to use — no storage cost — but they don't exist on `postback_log`; there you must `substr(received_at, 1, 10)` yourself.
- **Timezone:** all timestamps are UTC. The user lives in `Asia/Jerusalem` (UTC+2/+3). When the user says "today" they usually mean Jerusalem-day. For accurate day-boundaries: `WHERE received_at >= datetime('YYYY-MM-DDT00:00:00', '-3 hours')` etc., or just be explicit about which boundary you used.
- **Don't write to D1.** This skill is read-only; if migration or backfill is requested, hand off to the migration playbook in `project_d1_state.md`.

## Path to the repo

The wrangler.toml binding is at `/Users/kobihazout/.gemini/antigravity/projects/wheel/wrangler.toml`. All commands run from that directory.

## Related memory

- `project_d1_state.md` — DB lifecycle, migration history, auth tokens
- `reference_secrets_split.md` — where `LEAD_WEBHOOK_TOKEN` / `POSTBACK_TOKEN` live
- `project_ga4_open_tasks.md` — GA4 admin steps pending (separate from this skill but adjacent)
