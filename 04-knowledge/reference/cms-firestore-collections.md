# CMS — Firestore Collections Reference

> Date: 2026-02-10. Code expectations vs DB structure.

## Canonical Structure

```
aggregation_queue/{verticalId}_{segmentId}     # Debounce queue
verticals/{verticalId}/aggregated_payloads/{targetId}   # Pre-built homepage (O(1))
verticals/{verticalId}/component_versions/{versionId}   # CMS content
verticals/{verticalId}/segments/{segmentId}/component_versions/{versionId}
verticals/{verticalId}/settings/{settingId}
```

## Collections Map

| Code Expects | Used By | Notes |
|--------------|---------|-------|
| aggregation_queue | debounceAggregation.ts | Queue aggregation tasks |
| aggregated_payloads | homepageService, aggregationQueueProcessor | Pre-built payload |
| component_versions | firestoreService, manifestResolver | CMS versions |
| admin_user | adminEmails.ts | Admin auth (not `admin`) |
| app_settings | App config | |
| verticals | Vertical config | |

## Naming Mismatches (Verify in Console)

- `aggregation` vs `aggregation_queue`
- `aggregated` vs `aggregated_payloads`
- `component` vs `component_versions` (migration script exists)

## published_components

Deprecated for homepage; `aggregated_payloads` is primary. `activePointerSync`, `migration.ts` still exist for live-build path — verify if still written.
