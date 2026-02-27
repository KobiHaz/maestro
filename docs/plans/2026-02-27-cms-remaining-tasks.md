# CMS — Remaining Tasks

> Consolidated: 2026-02-27. Pending tasks.

## Source

- Plan: `docs/plans/2026-02-23-audit-remediation-p0-p1.md` (partial)
- Tasks: `docs/TASKS.md`

---

## From Audit Plan (P0/P1)

### Task 5–6: Remove Debug console.log (Pending)

- **packages/shared/src/payload-logic/productsFromSlots.ts** — Remove all `console.log` blocks in mapped section
- **packages/shared/src/payload/homepagePayloadNormalizers.ts** — Remove all `console.log` in `normalizeContentSections`

### Task 8–9: Wire featured_articles and product_list_banner (Pending)

- **componentVersionTypes.ts**: Add `'featured_articles'`, `'product_list_banner'` to union, `ALL_COMPONENT_TYPES`, constants
- **strategies/index.ts**: Add strategy cases, add to `getAvailableComponentTypes`
- **adminRegistry.ts**: Register FeaturedArticlesPage, ProductListBannerPage in ADMIN_FEATURES
- **AdminRouter.tsx**: Add `'featured-articles'`, `'product-list-banner'` to AdminTab union

---

## From TASKS.md

### 1. Articles — Review (Pending)

- [ ] Review article content (titles, descriptions, links)
- [ ] Confirm thumbnails match article topics
- [ ] Check GoldIraRolloverGuidePage, GoldIraFeesPage, GoldIraCompaniesPage

### 2. Article Images → Firebase Storage (Pending)

- [ ] Upload article thumbnails to Firebase (e.g. `assets/articles/`)
- [ ] Update GoldIraArticlesPage, GoldIraRolloverGuidePage, GoldIraFeesPage, GoldIraCompaniesPage
- [ ] Remove local images from `public/`

### 3. Change Email — Footer, Terms, Contact (Pending)

- [ ] Change email in Admin → Footer → Contact Info
- [ ] Update fallback in ContactPage.tsx if needed

---

## Status

| Section | Done | Pending |
|---------|------|---------|
| Audit 5-6 | 0 | 2 |
| Audit 8-9 | 0 | 2 |
| TASKS | 0 | 3 |
