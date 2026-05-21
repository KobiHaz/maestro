# proposal-generator — Architecture

## Stack Details

| Layer | Tech |
|-------|------|
| Framework | React 19, TypeScript, Vite |
| Styling | Tailwind v4, Radix UI, Lucide, CVA, clsx, tailwind-merge |
| Backend | Firebase Auth + Firestore |
| PDF | html2pdf.js |
| State | React Context (AuthContext + EditContext) |

## Component Flow

```
App.tsx
├── AuthContext (Firebase Auth, user session)
├── EditContext (editing mode, draft state)
├── LoginPage (public)
└── Protected:
    ├── ProposalPage     → create/edit CRM or automation proposals
    ├── QuotePage        → create/edit affiliate agreements (quote)
    └── MyProposalsPage  → list all saved proposals + agreements
```

## Firestore Operations (lib/firestore.ts)

```ts
saveProposal(userId, variant, data)   → upsert to proposals
saveAgreement(userId, variant, data)  → upsert to agreements
listDocuments(userId)                 → proposals + agreements, orderBy updatedAt desc
deleteDocument(collection, id)        → delete + filter local state
getDocument(collection, id)           → single doc fetch
```

## Firestore Rules Pattern

```javascript
// proposals and agreements collections
match /proposals/{docId} {
  allow create: if request.auth.uid == request.resource.data.userId;
  allow read, delete: if request.auth.uid == resource.data.userId;
  allow update: if request.auth.uid == resource.data.userId
    && request.resource.data.userId == resource.data.userId; // userId immutable
}
// Same pattern for /agreements/{docId}
```

## Key Implementation Details

- **Composite index:** `userId ASC` + `updatedAt DESC` in Firestore — required for list queries
- **Delete pattern:** Filter local state array after delete — don't refetch
- **Number inputs:** `parseNumberInput(value)` normalizes empty string → 0
- **RTL:** `dir="rtl"` on all main containers (not just body)
- **Print styles:** `@media print` in `index.css` — never inline `dangerouslySetInnerHTML`

## Conventions

| Rule | Detail |
|------|--------|
| No `console.log` | Use `console.error` for error paths only |
| Context values | Always wrapped in `useMemo` |
| Switch statements | Must be exhaustive (TypeScript `never` default) |
| Error handling | Retry UI in MyProposalsPage for list failures |
