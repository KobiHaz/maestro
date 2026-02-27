# Proposal Generator — Architecture & Reference

> Project: proposal-generator. Source of truth for "what the code does" — always up to date.

## Tech Stack

| Layer | Tech |
|-------|------|
| Framework | React 19, TypeScript, Vite |
| Styling | Tailwind v4, Radix UI, Lucide, CVA, clsx, tailwind-merge |
| Backend | Firebase Auth + Firestore (proposals, agreements) |
| PDF | html2pdf.js |

## Architecture

```
UI (pages) → Contexts (Auth, Edit) → lib/firestore.ts → Firebase
```

- **Pages:** ProposalPage, QuotePage, MyProposalsPage, LoginPage
- **Contexts:** AuthContext (Firebase Auth), EditContext (editing state)
- **Data:** Firestore collections `proposals`, `agreements`; userId-scoped

## Entities & Types

| Entity | Collection | Key Fields |
|--------|------------|------------|
| SavedProposal | proposals | userId, variant (crm|automation), data: ProposalData |
| SavedAgreement | agreements | userId, variant, data: QuoteData |

- `ProposalData` — recipient, specSections, basePackage, addOns, pricingRows, blockers
- `QuoteData` — clientName, paymentModel (fixed|hourly), pricing, terms

## Security (Firestore Rules)

- **Create:** `request.auth.uid == request.resource.data.userId`
- **Read/Delete:** `request.auth.uid == resource.data.userId`
- **Update:** `request.auth.uid == resource.data.userId` **and** `request.resource.data.userId == resource.data.userId` (userId immutability)

## Conventions (Implemented)

- No `console.log` in production paths
- Error handling with retry UI in MyProposalsPage
- `parseNumberInput()` for QuoteForm number fields (empty → 0)
- `orderBy('updatedAt', 'desc')` in Firestore queries (server-side sort)
- Exhaustive switch in `getTabForDoc` (App.tsx)
- Context values memoized (AuthContext, EditContext)
- Delete updates local state (filter) instead of refetch

## Lessons (from 2025-02-23 plans)

- Firestore userId must be immutable on update — rule enforces equality
- Composite index required: `userId` + `orderBy('updatedAt')`
- Print styles in `index.css` @media print — not dangerouslySetInnerHTML
