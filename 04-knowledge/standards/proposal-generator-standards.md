# Proposal Generator — Cursor Standards

> Coding standards. Read when working on proposal-generator.

## Naming

| Type | Pattern | Example |
|------|---------|---------|
| Components | PascalCase | `ProposalPage.tsx`, `QuoteForm.tsx` |
| Hooks | `use` + PascalCase | `useAuth`, `useEdit` |
| Lib | camelCase | `firestore.ts`, `utils.ts` |
| Types | PascalCase | `ProposalData`, `SavedProposal` |
| Plan files | `YYYY-MM-DD-kebab.md` | `2025-02-27-proposal-remaining-tasks.md` |

## Architecture

- **Pages** in `src/projects/` — ProposalPage, QuotePage, MyProposalsPage, LoginPage
- **Contexts** in `src/contexts/` — AuthContext, EditContext
- **Types** in `src/projects/types.ts` — ProposalData, QuoteData
- **Firestore** in `src/lib/firestore.ts` — save/list/delete/get
- **RTL Hebrew** — `dir="rtl"` on main containers

## Conventions

- Functional components, TypeScript strict
- No `console.log`; use `console.error` for errors only
- No `any`; prefer typed interfaces
- Exhaustive switch for union types (`default: const _: never`)
- Context values wrapped in `useMemo`
- Number inputs: `parseNumberInput(value)` for empty handling

## Plan Lifecycle

1. **On task completion** — Update `04-knowledge/reference/proposal-generator-architecture.md`
2. **Completed plans** — Delete (from project or vault)
3. **Pending tasks** — Single file in `02-projects/proposal-generator/` or `06-outputs/` in vault
4. **Before deletion** — Ensure all relevant decisions have been moved to Reference
