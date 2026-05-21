# Engineering invariants — template

> Copy to `02-projects/<project>/engineering-invariants.md` and replace placeholders. Each invariant must be **checkable** (grep, file rule, or one script).

## Metadata

| Field | Value |
|-------|--------|
| Project | |
| Owner | |
| Last reviewed | YYYY-MM-DD |

## How we verify

- **CI (primary):** one command in the **app repo** (e.g. `npm run check:invariants` or `scripts/invariants-check.sh`) runs **all** rows below; GitHub Actions (or equivalent) runs it on **every PR** and optionally **nightly** on the default branch. Merge should fail when the command exits non-zero.
- **Cursor Automations:** optional scheduled pass (see `03-agents/workflows/invariant-sentinel.md`) — does not replace CI if you need a merge gate.
- **Evidence:** every invariant links to **how** we check it (pattern, path, or command) and that logic must live behind the shared CI entrypoint.

## Invariants

| ID | Property (must always hold) | How to verify | Notes / owner |
|----|-----------------------------|---------------|----------------|
| INV-001 | e.g. No hardcoded API keys in `src/` | `rg -n "(api[_-]?key|secret)\s*[:=]\s*['\"]" src/` returns no hits in app code | Allowlist test fixtures in `__fixtures__/` if needed |
| INV-002 | e.g. All `/api/admin/*` routes require session + role | Grep route files for middleware import + role guard | |
| INV-003 | e.g. SQL uses parameterized queries only | Ban `raw(` / string concat patterns per ORM — document allowed exceptions | |
| INV-004 | | | |

## Exclusions

Document **intentional** exceptions (with expiry date if temporary):

- 

## Change log

| Date | Change |
|------|--------|
| | |
