# cms — Firestore Collections

## Canonical Structure

```
aggregation_queue/{verticalId}_{segmentId}

verticals/{verticalId}/
  aggregated_payloads/{targetId}
  component_versions/{versionId}
  segments/{segmentId}/
    component_versions/{versionId}
  settings/{settingId}

admin_user/{docId}          ← NOT 'admin' (historical mismatch)
app_settings/{docId}
```

## Collections

| Collection Path | Used By | Purpose |
|----------------|---------|---------|
| `aggregation_queue` | `debounceAggregation.ts` | Queue aggregation tasks |
| `verticals/{vid}/aggregated_payloads` | `homepageService`, `aggregationQueueProcessor` | Pre-built O(1) payload |
| `verticals/{vid}/component_versions` | `firestoreService`, `manifestResolver` | Vertical-level CMS content |
| `verticals/{vid}/segments/{sid}/component_versions` | `firestoreService` | Segment overrides |
| `admin_user` | `adminEmails.ts` | Admin whitelist |
| `app_settings` | App config | Global settings |
| `verticals` | Domain resolution | Vertical config |

## Critical Naming Note

Code queries `'admin_user'` — **not** `'admin'`.
`adminEmails.ts:29` has a bug querying `'admin'` (High severity security issue — fix to `'admin_user'`).

## Aggregated Payloads

Pre-built homepage snapshots. Written by `aggregationQueueProcessor` when component versions change.
Key field: `targetId` = `segmentId` or `'default'`.
Validity check: doc exists + passes schema validation.

## Deprecated

`published_components` — deprecated for homepage. `aggregated_payloads` is primary.
`activePointerSync` and `migration.ts` may still write it — verify before removing.

## Firestore Rules Summary

- Firestore least-privilege rules in place ✓
- Admin claims used for admin writes ✓
- userId scoping on user-owned collections ✓
