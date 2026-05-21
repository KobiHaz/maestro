# MCP Setup — CRM (Supabase, GitHub, Vercel)

## Quick start

1. Restart Cursor / Cowork
2. Supabase — log in via browser
3. Vercel — authorize
4. Test: "List tables in the database using MCP"

## Overview

| Service | MCP | Usage |
|---------|-----|-------|
| Supabase | remote | SQL, migrations, Edge Functions, types |
| Vercel | remote | Deployments, logs |
| GitHub | PAT required | PRs, issues |

## Supabase project

- Project ID: `fbtnhhurjwizcrmcisci`
- URL: `https://fbtnhhurjwizcrmcisci.supabase.co`

## Vercel project

- Project: `democrm` (ID: `prj_lFTyxmM8gO9H0nF8DHm71fOlGSUV`)
- Org: `team_0TjG4YuI36Nck2PCBHYyUIvb`

## Security

- Manual approval ON for SQL, migrations
- `.cursor/mcp.json` in `.gitignore` if contains GitHub PAT
