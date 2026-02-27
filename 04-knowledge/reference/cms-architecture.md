# CMS — Architecture Reference

> Source of truth: Obsidian. What the code does (always up to date).

## Tech Stack

- **Frontend:** React 19, Vite, React Query, React Router, Tailwind
- **Backend:** Firebase (Firestore, Hosting, Cloud Functions, Storage, Auth)
- **Monorepo:** pnpm, Turbo, @cms/shared, @vertical-configs/*

## Homepage Payload: Aggregated First + Live Fallback

1. Read from `verticals/{verticalId}/aggregated_payloads/{segmentId|'default'}`
2. If doc exists and valid → return (source = `'aggregated'`)
3. If missing/invalid → build live from component_versions (source = `'live'`)

**Code:** `homepageService.ts`, `getHomepagePayload` Cloud Function.

## Manifest Pattern

- **Manifest resolution:** `manifestService.ts` — segment override vs vertical
- **Overridable:** slots, hero, content_sections, carousel, top_pick
- **Vertical-only:** products, footer, header_navigation, sticky_bar, etc.
- **Path:** `verticals/{vid}/segments/{sid}/component_versions` or `verticals/{vid}/component_versions`

## Component Versioning

- Lifecycle: draft → published → archived
- `componentVersionService.ts`: getActiveComponentData, saveToDraft, publishDraft, duplicateVersion, archiveVersion
- Admin: `adminRegistry.ts`, ADMIN_FEATURES, ComponentType

## Component Storage (Vertical vs Segment)

| Level | Path | Examples |
|-------|------|----------|
| Vertical (shared) | `verticals/{vid}/component_versions` | footer, header, products, sticky_bar |
| Segment override | `verticals/{vid}/segments/{sid}/component_versions` | slots, hero, content_sections, carousel |

**Fetch:** segment first (if overridable), else vertical. `SEGMENT_OVERRIDABLE_COMPONENTS` in firestoreService.

## Data Transformation

- **Loader layer:** `smartNormalizeFromFirestore()` — snake_case → camelCase
- **Firestore:** snake_case only (migration complete)
- **Never normalize in components** — normalization at the edge only

## Core Principles

- **Single Source of Truth:** Payload has `products: Product[]` + `productsWithSlots: ProductSlotRef[]` (IDs only)
- **O(1) lookups:** Use `Map` — never `.find()` inside loops
- **Zero Tolerance:** No fake defaults, no cross-vertical fallbacks

## Reference Docs (vault)

- Security: `cms-security-audit.md`
- Firestore: `cms-firestore-collections.md`
- Postback HMAC: `cms-postback-hmac.md`
- Standards: `cms-standards.md`
- Remaining tasks: `docs/plans/2026-02-27-cms-remaining-tasks.md`
