---
name: enhance
description: Add or update features in existing application. Used for iterative development.
---

# /enhance - Update Application

$ARGUMENTS

---

## Task

**Tools in vault:** `03-agents/`, `04-knowledge/`. Session/preview scripts from `03-agents/scripts/` if present. Otherwise: `npm run dev`, project brief from `02-projects/[project]/`.

This command adds features or makes updates to existing application.

### Not duplicate of `/execute`

| | **`/enhance` (this workflow)** | **`/execute`** (`workflows/execute.md`) |
|--|-------------------------------|----------------------------------------|
| **Trigger** | Natural-language feature request | Next 🟥 step in **`docs/plans/*.md`** |
| **Tracking** | Light (optional user confirmation before big diffs) | Mandatory emoji progress + lifecycle checklist |

If you already have a staffed plan in `docs/plans/`, **prefer `/execute`**. Use **`/enhance`** for small or exploratory changes without a plan file.

### Steps:

1. **Understand Current State**
   - Load project state with `session_manager.py`
   - Understand existing features, tech stack

2. **Plan Changes**
   - Determine what will be added/changed
   - Detect affected files
   - Check dependencies

3. **Present Plan to User** (for major changes)
   ```
   "To add admin panel:
   - I'll create 15 new files
   - Update 8 files
   - Takes ~10 minutes
   
   Should I start?"
   ```

4. **Apply**
   - Call relevant agents
   - Make changes
   - Test

5. **Update Preview**
   - Hot reload or restart

---

## Usage Examples

```
/enhance add dark mode
/enhance build admin panel
/enhance integrate payment system
/enhance add search feature
/enhance edit profile page
/enhance make responsive
```

---

## Caution

- Get approval for major changes
- Warn on conflicting requests (e.g., "use Firebase" when project uses PostgreSQL)
- Commit each change with git
