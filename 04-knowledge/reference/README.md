# 04-knowledge/reference

Project-specific reference docs. One folder, no subfolders.

## Convention

- **Naming:** `<project>-<topic>.md` (e.g. `smart-volume-radar-architecture.md`)
- **Scope:** Only files tied to projects in `02-projects/`
- **No duplicates:** One doc per topic; use `06-outputs/` for dated reports/audits
- **Hub:** Each project has a primary doc (e.g. architecture); others link from it

## Current projects & ref count

| Project | Ref files |
|---------|-----------|
| smart-volume-radar | 5 |
| crm | 4 |
| source6681 | 5 |
| cms | 6 |
| proposal-generator | 1 |
| website | 0 |

## Rules (from maestro-project-doc-lifecycle)

- Update `04-knowledge/reference/<project>-*` when architecture/API changes
- Audits/reports → `06-outputs/` or `04-knowledge/reference/<project>-security-audit` (canonical)
- Do not keep audit/performance reports in project `docs/`
