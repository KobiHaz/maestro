# Log — Invariant Sentinel in Maestro

**Date:** 2026-04-04

## What changed

- Added workflow `03-agents/workflows/invariant-sentinel.md` (portable invariant/drift checks; links to Cursor marketplace automation and reference MCP).
- Added template `05-templates/engineering-invariants.md` for per-project invariant lists under `02-projects/<project>/`.
- Registered in `03-agents/agent-routing.md` (Trigger Matrix + Phase 4 workflows + Common flows).
- Indexed from `03-agents/skills/README.md` and `03-agents/README.md`.

## Why

Align the vault with Cursor’s Invariant Sentinel pattern so projects can run scheduled or on-demand assurance with logged evidence.

## Follow-up (same day)

- Clarified in `workflows/invariant-sentinel.md`: **merge-blocking checks belong in CI** (script + workflow in the app repo); Cursor Automations are an optional second layer. Repaired YAML frontmatter on that file.
- Template `05-templates/engineering-invariants.md` updated to state CI as primary.

## CI implementation (Maestro repo)

- `scripts/invariants-check.sh` — single entrypoint for invariant checks.
- `.github/workflows/invariants.yml` — `pull_request`, `push` to `main`, weekly `cron`.
- `02-projects/maestro/engineering-invariants.md` + `02-projects/maestro/project.maestro.md`.
- `02-projects/README.md` links the Maestro brief and invariants.
