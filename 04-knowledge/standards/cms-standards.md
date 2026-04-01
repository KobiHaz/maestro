# CMS — Cursor Rules & Standards

> **Extends:** [[04-knowledge/standards/base-coding-standards|base-coding-standards]]. Load both.
> Repo: cms. Read this for rules when working on CMS.

## Tech Stack

- React 19, Vite, TypeScript, Tailwind, React Query
- Firebase (Firestore, Hosting, Functions, Storage, Auth)
- pnpm, @cms/shared, @vertical-configs/*

## Quick Reference — Entity & Security

| Domain | Pattern |
|--------|---------|
| **Payload** | `products: Product[]` + `productsWithSlots: ProductSlotRef[]` (IDs only) |
| **Vertical fallback** | NEVER fallback between verticals (goldira ↔ weightloss) |
| **Defaults** | Zero tolerance — no fake content; return empty |
| **Images** | Paths in Firestore; `getStorageUrl()` async in components |
| **Firestore** | snake_case only; `smartNormalizeFromFirestore()` in loaders |

*Data loading, lookups (Map O(1)) — see base sections 4, 5.*

## Naming (תוספות ל-base)

*Components, hooks, services, constants — see base. Plan files — [[04-knowledge/standards/maestro-project-doc-lifecycle#4. תבנית שם תוכנית|maestro §4]].*

## Plan Lifecycle

[[04-knowledge/standards/maestro-project-doc-lifecycle]]

## Architecture

- Feature-based: `features/content`, `features/layout`, `features/products`
- Admin registry: `adminRegistry.ts`, `ADMIN_FEATURES`, ComponentType
- Versioning: draft → published → archived

## Reference

- Architecture: `04-knowledge/reference/cms-architecture.md`
- Security: `04-knowledge/reference/cms-security-audit.md`
- Remaining tasks: `docs/plans/2026-02-27-cms-remaining-tasks.md`
