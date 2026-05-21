# proposal-generator — Project Context

React-based proposal and quote generator. RTL Hebrew interface for affiliate agreements and CRM proposals.

**Stack:** React 19 + TypeScript + Vite + Tailwind v4 + Radix UI + Firebase

---

## Quick Start

```sh
npm install
npm run dev    # http://localhost:8085
```

---

## Folder Map

```
src/
  projects/       → Pages: ProposalPage, QuotePage, MyProposalsPage, LoginPage
  contexts/       → AuthContext (Firebase Auth), EditContext (editing state)
  lib/
    firestore.ts  → save / list / delete / get for proposals + agreements
  types/          → ProposalData, QuoteData (in src/projects/types.ts)
```

---

## Data Model

| Entity | Firestore Collection | Key Fields |
|--------|---------------------|------------|
| SavedProposal | `proposals` | `userId`, `variant` (crm\|automation), `data: ProposalData` |
| SavedAgreement | `agreements` | `userId`, `variant`, `data: QuoteData` |

**ProposalData:** recipient, specSections, basePackage, addOns, pricingRows, blockers
**QuoteData:** clientName, paymentModel (fixed\|hourly), pricing, terms

---

## Firestore Security Rules

```
// Create: userId must match auth
request.auth.uid == request.resource.data.userId

// Read / Delete: userId must match auth
request.auth.uid == resource.data.userId

// Update: userId must match auth AND userId must not change
request.auth.uid == resource.data.userId
  AND request.resource.data.userId == resource.data.userId
```

---

## Architecture Flow

```
UI (pages) → Contexts (Auth, Edit) → lib/firestore.ts → Firebase
```

- Firestore queries: `orderBy('updatedAt', 'desc')` — server-side sort
- Composite index required: `userId` + `orderBy('updatedAt')`
- Delete updates local state (filter) — no refetch

---

## UI Rules

- **RTL Hebrew** — `dir="rtl"` on all main containers
- **Number inputs** — always use `parseNumberInput(value)` for empty → 0 handling
- **Print** — styles in `index.css` @media print, never `dangerouslySetInnerHTML`
- **PDF export** — html2pdf.js

---

## Core Rules

1. **RTL everywhere** — `dir="rtl"` on all main containers
2. **No `console.log`** — use `console.error` for errors only
3. **Context memoization** — wrap context values in `useMemo` for referential stability
4. **Firestore userId immutability** — always enforce via security rule on update
5. **Composite index** — `userId` + `updatedAt` required for list queries
6. **parseNumberInput** — use for all number form fields
7. **Exhaustive switch** — in `getTabForDoc` and similar discriminated unions

---

## Reference

- [Architecture & Firestore rules](.claude/knowledge/architecture.md)
