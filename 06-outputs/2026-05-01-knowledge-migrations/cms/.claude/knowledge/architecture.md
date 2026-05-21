# cms — Architecture

## Monorepo (pnpm + Turbo)

```
apps/frontend/     → React SPA, domain-resolved multi-vertical
apps/functions/    → Firebase Cloud Functions
packages/shared/   → @cms/shared (components + utils)
packages/vertical-configs/{id}/config/vertical.json
```

## Domain Resolution

Request comes in → Firebase Hosting → Frontend → reads `window.location.hostname`
→ matches against `verticals` Firestore collection + `vertical.json` configs
→ resolves `verticalId` → fetches payload for that vertical

## Homepage Payload

**Code:** `homepageService.ts`, `getHomepagePayload` Cloud Function

```
1. Read verticals/{vid}/aggregated_payloads/{segmentId|'default'}
2. Valid doc → return { source: 'aggregated', ...payload }   ← O(1) fast path
3. Missing/invalid → live build from component_versions       ← fallback
```

## Manifest Resolution

**Code:** `manifestService.ts`

- Overridable at segment level: slots, hero, content_sections, carousel, top_pick
- Vertical-only: products, footer, header_navigation, sticky_bar
- Path: `verticals/{vid}/segments/{sid}/component_versions` → falls back to `verticals/{vid}/component_versions`
- `SEGMENT_OVERRIDABLE_COMPONENTS` is the gate

## Data Transformation

```
Firestore (snake_case) → smartNormalizeFromFirestore() → app (camelCase)
```

Never normalize inside components. Only at the loader/edge layer.

## Payload Structure (Key)

```ts
{
  products: Product[],              // full product objects
  productsWithSlots: ProductSlotRef[], // IDs only — resolve via Map
}
```

Use `Map` for O(1) product lookups from slot refs. Never `.find()` in loops.

## Component Versioning

**Code:** `componentVersionService.ts`, `adminRegistry.ts`

States: `draft → published → archived`

Admin panel uses `ADMIN_FEATURES` + `ComponentType` registry to render CMS editors.

## Cloud Functions (apps/functions)

| Function | Purpose |
|----------|---------|
| `getHomepagePayload` | Main SSR-like payload fetch |
| `aggregationQueueProcessor` | Debounce + rebuild aggregated_payloads |
| `registerClickEvent` | Affiliate click tracking |
| `postbackHandler` | Conversion postbacks (⚠️ no HMAC yet) |
| `reportFrontendError` | Client error reporting (⚠️ not wired in firebase.json) |

## Testing

| Tool | Scope |
|------|-------|
| Vitest + MSW | Unit + integration |
| Playwright | E2E |
| Storybook | Component development |

## Key Services

| Service | File | Purpose |
|---------|------|---------|
| Homepage | `homepageService.ts` | Aggregated payload fetch |
| Manifest | `manifestService.ts` | Segment/vertical manifest resolution |
| Component version | `componentVersionService.ts` | CRUD lifecycle |
| Firestore | `firestoreService.ts` | DB access + `SEGMENT_OVERRIDABLE_COMPONENTS` |
