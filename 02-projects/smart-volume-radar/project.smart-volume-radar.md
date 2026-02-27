---
project: smart-volume-radar
status: active
path: ~/.gemini/antigravity/projects/smart-volume-radar
type: BACKEND
agents: [backend-specialist, devops-engineer]
---

# Smart Volume Radar

Automated stock volume monitoring with RVOL analysis, news enrichment, and Telegram delivery.

## Goal
Stock analysis bot — sends analysis results to Telegram for analyst collaboration (per [[01-me/01-me-identity]]).

## Tech Stack
- **Backend:** Node.js, tsx, TypeScript 5.9, ESM, Node >=20
- **APIs:** Yahoo Finance (yahoo-finance2), Finnhub, Telegram Bot
- **Testing:** Jest, ts-jest, node env
- **Code:** ESLint, Prettier, TypeScript ESLint
- **CI/CD:** GitHub Actions
- **Deployment:** GitHub Actions scheduled jobs

## How to run
```sh
cd ~/.gemini/antigravity/projects/smart-volume-radar && npm i && npm run start
```

## Workflow
1. Brainstorm feature or bug
2. Clarifying questions until understood
3. Discovery prompt for Cursor (file names, structure)
4. Break into phases, Cursor prompts per phase, status reports

## Status
Active. Hardening (p-limit, logger, config) complete. Maestro folder removed; docs in project + 04-knowledge.

## Decisions
- **Concurrency:** p-limit (3–5 tickers, 2 news) — from PLAN-hardening
- **Config:** Google Sheet watchlist + src/config; no tickers.json
- **Logging:** logger only; no console.log

## Docs
See [[02-projects/smart-volume-radar/README|smart-volume-radar docs index]]. Reference: [[04-knowledge/reference/smart-volume-radar-architecture|architecture]]. Standards: [[04-knowledge/standards/smart-volume-radar-standards|standards]].

## Links
- Path: `~/.gemini/antigravity/projects/smart-volume-radar`
