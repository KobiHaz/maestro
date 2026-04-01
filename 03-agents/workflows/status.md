---
name: status
description: Project / agent status, file stats, and dev server (merged former /preview).
---

# /status — Project state and dev server

$ARGUMENTS

---

## Task

Report **project context**, **work board** (if inferable), **file activity**, and **local dev server** state.

Sub-commands (optional first token after `/status`):

```
/status              — Full status (project + agents + files + dev server)
/status preview      — Same as bare /status for dev URL/health (legacy alias)
/status start        — Start dev server (npm run dev / pnpm dev / project script)
/status stop         — Stop dev server (if you manage the process)
/status restart      — Restart dev server
/status check        — Health check only (URL responding)
```

If `$ARGUMENTS` is empty, run the **full** status. If it starts with `start|stop|restart|check|preview`, handle **dev server** as in the former `/preview` workflow.

---

### What full status includes

1. **Project**
   - Name, path, type/stack from `02-projects/[project]/` or repo README
2. **Agent / task board** (when plan or chat context exists)
   - Completed vs in-progress vs pending (from `docs/plans/*` or narrative)
3. **Files**
   - Rough created/modified counts if inferable from git
4. **Dev server**
   - Running or not, URL, simple health note

---

## Example output

```
=== Project Status ===

📁 Project: my-ecommerce
📂 Path: …/my-ecommerce
🏷️ Type: nextjs-ecommerce

🔧 Tech Stack: next.js, postgresql, clerk, …

✅ Features / milestones: …
⏳ Pending: …

📄 Files: N created, M modified (from git)

=== Agent / plan ===

(From active docs/plans/*.md or session context)

=== Dev server ===

🌐 URL: http://localhost:3000
💚 Health: OK
```

### Port conflict (on start)

If port in use, offer: alternate port, kill process, or user choice — same behavior as legacy `/preview start`.

---

## Technical

**Tools in vault:** `03-agents/scripts/` if present (`session_manager`, `auto_preview`). Otherwise: `02-projects/` brief, `npm run dev` / `pnpm dev` / `yarn dev` per project.

**Note:** `/preview` was **merged here** — use `/status` or `/status start` / `/status check`.
