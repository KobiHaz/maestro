# Coding Standards

> Source: Reverse-engineered from source6681 and Maestro agents. Use when writing or reviewing code.

## Naming

| Type | Pattern | Example |
|------|---------|---------|
| Component files | PascalCase | `ArchiveGridItem.tsx`, `ProductModal.tsx` |
| Hooks | kebab-case, `use-` prefix | `use-wishlist.ts`, `use-global-discount.ts` |
| Lib / utils | kebab-case | `format-price.ts`, `proxy-image.ts` |
| Migrations | `YYYYMMDDHHMMSS_snake_case.sql` | `20260226120000_add_brand_to_products.sql` |
| Plan files | `YYYY-MM-DD-topic-design.md` | `2026-02-26-brands-management-design.md` |

## Architecture (web projects)

- **Admin isolation:** Admin code in `src/components/admin/` only. Never import admin components in public pages. Lazy-load admin routes.
- **Types:** Define in `src/types/`. Align with Supabase schema where applicable.
- **Schema:** Use Supabase migrations; no direct ALTER in app code.

## Conventions

- Functional components, TypeScript, `@/` path alias.
- No `any`. Prefer strict typing.
- No `console.log` in production.
- No hardcoded secrets; use env vars.

## Documentation

- After completing a plan: update relevant docs, then delete the plan file.
- Capture lessons and decisions in permanent docs before plan deletion.
