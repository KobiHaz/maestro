---
project: proposal-generator
status: active
path: ~/.gemini/antigravity/projects/proposal-generator
type: WEB
agents: [frontend-specialist, backend-specialist]
---

# Proposal Generator

React-based proposal and quote generator. RTL Hebrew interface for affiliate agreements and proposals.

## Goal
Quote & agreement systems — proposal submission, affiliate agreement building (per [[01-me/01-me-identity]]).

## Tech Stack
- **Frontend:** React 19, TypeScript, Vite, Tailwind v4, Radix UI, Lucide, date-fns, clsx, tailwind-merge, CVA
- **State:** React State + Firebase Auth + EditContext
- **Backend:** Firebase (Auth, Firestore — proposals, agreements)

## Workflow
1. Brainstorm feature or bug
2. Clarifying questions until understood
3. Discovery prompt for Cursor (file names, structure)
4. Break into phases, Cursor prompts per phase, status reports

## Status
Active.

## Decisions
## Docs (vault = single source)
- **Reference:** [[04-knowledge/reference/proposal-generator-architecture|proposal-generator-architecture]] — architecture, security
- **Standards:** [[04-knowledge/standards/proposal-generator-standards|proposal-generator-standards]] — naming, rules, plan lifecycle

**Run:** `npm run dev` → http://localhost:8085

## Links
- Path: `~/.gemini/antigravity/projects/proposal-generator`
