# Cursor MCP Setup: Supabase, GitHub, Vercel

## Quick start

1. Restart Cursor
2. Supabase — log in via browser
3. Vercel — authorize
4. Test: "List tables in the database using MCP"

## Overview

| Service | MCP | Usage |
|---------|-----|-------|
| Supabase | remote | SQL, migrations, Edge Functions, types |
| Vercel | remote | Deployments, logs |
| GitHub | PAT required | PRs, issues |

## Vercel project URL

```json
"vercel": { "url": "https://mcp.vercel.com/YOUR_TEAM_SLUG/hadaryaCRM" }
```

## Security

- Manual approval ON for SQL, migrations
- `.cursor/mcp.json` in `.gitignore` if contains GitHub PAT
