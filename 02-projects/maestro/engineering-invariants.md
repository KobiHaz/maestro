# Engineering invariants — Maestro vault

> **CI entrypoint:** `./scripts/invariants-check.sh` (same command locally and in GitHub Actions).

## Metadata

| Field | Value |
|-------|--------|
| Project | Maestro (Obsidian second-brain vault) |
| Owner | Vault maintainer |
| Last reviewed | 2026-04-04 |

## How we verify

- **CI:** `.github/workflows/invariants.yml` runs `scripts/invariants-check.sh` on every PR and push to `main`, plus weekly schedule.
- **Cursor Automations:** optional; see `03-agents/workflows/invariant-sentinel.md`.

## Invariants

| ID | Property (must always hold) | How to verify | Notes |
|----|-----------------------------|---------------|--------|
| INV-MAESTRO-001 | Invariant Sentinel workflow file exists | `test -f 03-agents/workflows/invariant-sentinel.md` | Supply-cycle doc |
| INV-MAESTRO-002 | Agent routing registers the workflow | `git grep -q 'workflows/invariant-sentinel.md' -- 03-agents/agent-routing.md` | Trigger + table |
| INV-MAESTRO-003 | Invariant template exists | `test -f 05-templates/engineering-invariants.md` | Per-app projects copy from here |
| INV-MAESTRO-004 | Invariant Sentinel workflow has valid `name` in frontmatter | `head -n 15 03-agents/workflows/invariant-sentinel.md \| grep -q '^name: invariant-sentinel'` | After `---` block |
| INV-MAESTRO-005 | No PEM private key blocks in tracked files | `git grep` for `BEGIN … PRIVATE KEY-----` / PKCS#8 `BEGIN PRIVATE KEY-----` in `invariants-check.sh` | Accidental key commits |

## Exclusions

- None.

## Change log

| Date | Change |
|------|--------|
| 2026-04-04 | Initial invariants + CI |
