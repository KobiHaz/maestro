# Proposal Generator — Cursor Standards

> **Extends:** [[04-knowledge/standards/base-coding-standards|base-coding-standards]]. Load both.
> Coding standards. Read when working on proposal-generator.

## Naming (תוספות ל-base)

*Components, hooks, lib, types — see base. Plan files — [[04-knowledge/standards/maestro-project-doc-lifecycle#4. תבנית שם תוכנית|maestro §4]].*

## Architecture

- **Pages** in `src/projects/` — ProposalPage, QuotePage, MyProposalsPage, LoginPage
- **Contexts** in `src/contexts/` — AuthContext, EditContext
- **Types** in `src/projects/types.ts` — ProposalData, QuoteData
- **Firestore** in `src/lib/firestore.ts` — save/list/delete/get
- **RTL Hebrew** — `dir="rtl"` on main containers

## Conventions (תוספות ל-base)

- No `console.log`; use `console.error` for errors only
- Context: wrap value in `useMemo` (per base §7 — justified for referential stability)
- Number inputs: `parseNumberInput(value)` for empty handling

*TypeScript, exhaustive switch — base §3.*

## Plan Lifecycle

[[04-knowledge/standards/maestro-project-doc-lifecycle]]
