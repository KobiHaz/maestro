# CMS — Cursor Rules & Standards

> Repo: cms. Read this for rules when working on CMS.

## Tech Stack

- React 19, Vite, TypeScript, Tailwind, React Query
- Firebase (Firestore, Hosting, Functions, Storage, Auth)
- pnpm, @cms/shared, @vertical-configs/*

## Quick Reference — Entity & Security

| Domain | Pattern |
|--------|---------|
| **Data loading** | Normalize in loaders only; components receive camelCase |
| **Payload** | `products: Product[]` + `productsWithSlots: ProductSlotRef[]` (IDs only) |
| **Lookups** | `Map` for O(1); never `.find()` in loops |
| **Vertical fallback** | NEVER fallback between verticals (goldira ↔ weightloss) |
| **Defaults** | Zero tolerance — no fake content; return empty |
| **Images** | Paths in Firestore; `getStorageUrl()` async in components |
| **Firestore** | snake_case only; `smartNormalizeFromFirestore()` in loaders |

## Naming

| Type | Pattern | Example |
|------|---------|---------|
| Components | PascalCase | `ProductCard.tsx` |
| Hooks | `use` + PascalCase | `useComponentData.ts` |
| Services | camelCase | `firestoreService.ts` |
| Constants | SCREAMING_SNAKE | `CACHE_DURATION` |
| Plan files | `YYYY-MM-DD-kebab.md` | `2026-02-27-cms-remaining-tasks.md` |

## Plan Lifecycle

1. **On task completion** — Update docs in Obsidian (`04-knowledge/reference/cms-*.md`)
2. **Completed plans** — Delete from `docs/plans/` (or move to archive)
3. **Pending tasks** — Single file in `docs/plans/YYYY-MM-DD-cms-remaining-tasks.md` in vault
4. **Before deleting Plan** — Ensure all relevant decisions have been moved to Reference

## Architecture

- Feature-based: `features/content`, `features/layout`, `features/products`
- Admin registry: `adminRegistry.ts`, `ADMIN_FEATURES`, ComponentType
- Versioning: draft → published → archived

## Reference

- Architecture: `04-knowledge/reference/cms-architecture.md`
- Security: `04-knowledge/reference/cms-security-audit.md`
- Remaining tasks: `docs/plans/2026-02-27-cms-remaining-tasks.md`
