# Gemini UX Audit — Xsheva CRM

**תאריך:** 13.3.2026  
**מקור:** Gemini  
**הקשר:** המשך brainstorm scroll UX + בדיקת דפדפן

---

## Executive Summary

- **Total Issues:** 25
- **Critical Bugs:** 7 (immediate attention)
- **Estimated Effort:** ~16 hours

**Top Priority:** Mobile Kanban scroll + sticky table headers

---

## Critical Bugs (Sprint 1)

| ID | Issue | Impact | Fix |
|----|-------|--------|-----|
| BUG-01 | Kanban triggers body scroll | Mobile UI shifts sideways, header hides | `body { overflow-x: hidden; }` |
| BUG-02 | Wrong Nav Link | "הצעות מחיר" → /contracts instead of ad-agency quotes | Update href to `/ad-agency/price-quotes` |
| BUG-03 | Mid-scroll page load | Clients/Projects open halfway down | `window.scrollTo(0,0)` on route change |
| BUG-04 | Product Error Trap | No Retry when Shopify/Products fail | Add `<Button onClick={() => refetch()}>` |
| BUG-05 | Modal Double-Scroll | Background scrolls while Lead modal open | `overflow: hidden` on body when modal open |

---

## Major UX Issues (Sprint 2)

### 1. Table Data Accessibility
- **Sticky Headers:** `thead { position: sticky; top: 0; }`
- **Sticky First Column:** "Customer Name" visible when scrolling right
- **RTL:** `inset-inline-start: 0` for Hebrew/English

### 2. Mobile Layout & Filters
- **Filter Bar Clipping:** Horizontally scrollable container, `flex-wrap: nowrap`
- **Sidebar RTL:** Wrap Hebrew nav in `<nav dir="rtl">`

### 3. Mixed-Language Display
- **Bidi:** `unicode-bidi: plaintext` on card titles (Deals)

---

## Technical Recommendations

### Kanban Boards
```css
.kanban-board {
  display: flex;
  overflow-x: auto;
  overscroll-behavior: contain;
  scroll-snap-type: x mandatory;
}
```

### Tables — Corner Cell
```css
thead th:first-child {
  position: sticky;
  top: 0;
  inset-inline-start: 0;
  z-index: 3;
}
```

---

## Current Strengths
- Visual consistency (Dark Theme)
- Automation UI (Trigger-Action)
- Dashboard charts/KPI on mobile
- Global search accessible

---

## Priority Roadmap

| Sprint | Effort | Focus |
|--------|--------|-------|
| 1 | 5.5 hrs | 7 Critical Bugs + mobile containment |
| 2 | 8 hrs | Sticky headers/columns, RTL alignment |
| 3 | 2.5 hrs | Scroll shadows, Lead tab badges |

---

## Sprint 3 — בוצע (13.3.2026)

| Item | סטטוס | שינויים |
|------|-------|---------|
| Scroll shadows | ✅ | .scroll-shadow-x, .scroll-shadow-x-dark; Kanban + DataTable |
| Lead tab badges | ✅ | EntityPageShell: kanbanCount, tableCount; Leads, Deals, Quotes, Designs, AdAgencyProjects |

---

## Sprint 2 — בוצע (13.3.2026)

| Item | סטטוס | שינויים |
|------|-------|---------|
| Sticky headers | ✅ | table.tsx כבר היה sticky top-0 |
| Sticky first column | ✅ | DataTable: data-sticky-first-col, index.css |
| RTL sticky | ✅ | inset-inline-start, [dir="rtl"] box-shadow |
| Filter bar scroll | ✅ | EntityToolbar: overflow-x-auto על wrapper |
| Sidebar RTL | ✅ | SidebarGroup dir="rtl" למשרד פרסום |
| Bidi card titles | ✅ | .bidi-plaintext על DealCard |

---

## Sprint 1 — בוצע (13.3.2026)

| Bug | סטטוס | שינויים |
|-----|-------|---------|
| BUG-01 | ✅ | `index.css`: body overflow-x:hidden, .kanban-grid overscroll-behavior-x:contain |
| BUG-02 | ✅ | Sidebar, CommandPalette, Breadcrumb → /ad-agency/price-quotes; Route חדש |
| BUG-03 | ✅ | App.tsx: ScrollToTop component עם window.scrollTo(0,0) on pathname |
| BUG-04 | ✅ | Products.tsx: Retry button עם refetch() |
| BUG-05 | ✅ | index.css: body:has([role="dialog"][data-state="open"]) { overflow: hidden } |

---

## Cross-Reference: Brainstorm Scroll UX

| Gemini Audit | Brainstorm Option |
|--------------|-------------------|
| BUG-01 body scroll | Option D — layout fix |
| BUG-05 modal scroll | Option D — overscroll-behavior |
| Sticky headers/columns | Option C + D |
| Kanban overscroll-behavior | Option B — full-viewport |
| RTL sticky | Option C — inset-inline-start |
