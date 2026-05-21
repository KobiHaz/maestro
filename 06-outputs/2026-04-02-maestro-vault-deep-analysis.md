# Maestro vault — deep analysis (2026-04-02)

## Perplexity MCP status

**Not used in this run:** calls to `perplexity_research` and `perplexity_search` returned **401** with `insufficient_quota` from the Perplexity API. Fix at [Perplexity API / billing settings](https://www.perplexity.ai/settings/api), then retry research from Cursor (MCP restart after adding quota or a new key).

This document is therefore a **local vault analysis** plus **industry-pattern commentary** (not web-cited via Perplexity).

---

## 1. What this project is

**Maestro** is an **Obsidian-native second brain** that doubles as **agent and workflow infrastructure** for software work:

| Layer | Role |
|--------|------|
| **Vault as workspace** | Cursor opens the vault; `CLAUDE.md` is the global instruction contract. |
| **02-projects** | Per-project briefs + `plans-and-tasks.md` as single source of truth for ongoing work. |
| **03-agents** | Specialists (~17), workflows (16 markdown modes), `skills/` library, `games/`, routing in `agent-routing.md`. |
| **04-knowledge** | Shared standards (`base-coding-standards`, per-repo standards), reference architecture notes. |
| **05–07** | Templates, dated outputs, logs. |

**Code lives elsewhere** (paths referenced from project briefs, e.g. Antigravity project roots). The vault is **governance + knowledge**, not the application monorepo.

---

## 2. Architectural strengths

1. **Clear separation of concerns** — Project truth in `02-projects`, process in `03-agents/workflows`, long-lived norms in `04-knowledge/standards`. Matches how strong eng teams split “what we build” vs “how we work.”

2. **Explicit supply cycle** — `agent-routing.md` ties **brainstorm → PRD/plan → execute → test → document → review → finishing-branch**, with staffing rules and “catalog first, not keywords.” Reduces ad-hoc agent shopping.

3. **Documented lifecycle for plans** — `maestro-project-doc-lifecycle.md` (Hebrew + structure) enforces **one** `plans-and-tasks.md` per project, ephemeral `docs/plans/`, and **no audit reports stranded in app repos** — vault-only outputs. That directly fights doc sprawl.

4. **Scale of skills** — Large `03-agents/skills/` tree (API patterns, frontend-design, TDD, debugging, etc.) gives repeatable procedures without stuffing everything into one mega-prompt.

5. **Multi-project portfolio** — One agent network serves many products (CRM, radar, source6681, casino-funnels, gold-ira-quiz, website, etc.) with per-project standards files.

---

## 3. Risks and failure modes

| Risk | Why it hurts | Mitigation (already or suggested) |
|------|----------------|----------------------------------|
| **Vault ↔ code drift** | Brief says stack X; repo moved to Y. | Periodic `project-deep-audit`; brief “last verified” dates. |
| **Agent / skill duplication** | Same guidance in vault skills vs Cursor plugin skills. | `03-agents/README.md` already warns; prefer one owner per procedure. |
| **Oversized routing table** | `agent-routing.md` is long; models may skim wrong row. | Keep “staffing in plan overrides matrix”; consider a one-page “default path” summary. |
| **Secrets in vault / MCP** | Obsidian REST `data.json`, API keys in `~/.cursor/mcp.json`. | `.gitignore` for plugin secrets; never paste keys in chat; rotate after exposure. |
| **Git + iCloud + Obsidian** | Sync conflicts, accidental commits of plugins. | Narrow `.gitignore`; avoid committing full `main.js` plugin trees if not needed. |
| **Hebrew + English split** | Some standards Hebrew-only; models may underweight them. | Critical global rules also in English in `CLAUDE.md` or `04-knowledge` where possible. |

---

## 4. Comparison to common PKM + AI patterns (conceptual)

- **PARA / Johnny.Decimal** — Maestro is **project-centric + agent-centric**, not classic PARA; that’s appropriate for **delivery**, not generic life admin.
- **“One app for notes, IDE for code”** — You unify **instructions and routing in the vault** while code stays in repos: aligns with **docs-as-code** and **agent context packs**, but requires discipline to **link** brief ↔ repo path.
- **MCP-heavy Cursor setups** — Your stack is a good fit: vault for stable prompts; MCP (GitHub, Obsidian, Perplexity when quota works) for **live** data. Perplexity specifically helps **web-time** questions; it does **not** replace reading `02-projects` / `04-knowledge`.

---

## 5. Recommendations (prioritized)

1. **Restore Perplexity API quota** — Use MCP for **fresh** benchmarks, dependency advisories, and competitor docs; keep vault analysis **file-grounded** as in this note.

2. **Add “last reviewed” to project briefs** — One line per brief: date + “stack verified against repo.”

3. **Optional index note** — A single `Maestro-INDEX.md` linking **active** projects + **canonical** standards path reduces navigation load.

4. **Quarterly prune** — Archive or merge overlapping `06-outputs` reports; align with lifecycle doc so `docs/plans/` stays ephemeral.

5. **Obsidian MCP key** — Ensure `OBSIDIAN_API_KEY` in Cursor matches the **current** Local REST API key after any rotation.

---

## 6. Inventory snapshot (2026-04-02)

- **Specialists:** 17 files under `03-agents/specialists/`.
- **Workflows:** 16 files under `03-agents/workflows/` (includes `plan`, `execute`, `project-deep-audit`, `finishing-branch`, etc.).
- **Standards:** 8 markdown files under `04-knowledge/standards/` (shared + per-project).
- **Projects in README table:** casino-funnels, cms, gold-ira-quiz, hadaryaCRM, proposal-generator, smart-volume-radar, source6681, website.

---

## 7. When Perplexity works again — suggested MCP prompts

- “Compare Maestro-style vault governance (single plans-and-tasks, ephemeral docs/plans) with Shape Up or GitHub’s recommended product docs — tradeoffs for solo maintainer.”
- “2025–2026 best practices for MCP security: secrets, least privilege, auditing tool use in IDEs.”
- “Risks of large markdown agent libraries in repos: token limits, maintenance, versioning.”

Run these via **`perplexity_research`** with `reasoning_effort: high` for synthesis comparable to this doc, **with citations**.

---

*Generated as a deep analysis of the Maestro vault; Perplexity MCP unavailable due to API quota at generation time.*
