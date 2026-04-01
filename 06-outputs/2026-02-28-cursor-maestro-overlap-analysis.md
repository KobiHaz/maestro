# Cursor Setup — source6681 — Maestro כמקור יחיד

> **תאריך:** 28 February 2026 | **מצב:** מוגדר — Maestro מקור אמת יחיד

---

## מה מוגדר

| מקום | תוכן |
|------|------|
| **Maestro** | כל החוקים, סטנדרטים, workflows, agent-routing, specialists, skills |
| **source6681/.cursorrules** | שורה אחת — מפנה ל-maestro-source |
| **source6681/.cursor/rules/maestro-source.mdc** | Rule יחיד: Maestro only, disregard Cloudflare |

## מבנה Cursor ל-source6681

```
source6681/
├── .cursorrules              ← "מקור אמת: Maestro. See .cursor/rules/"
└── .cursor/
    └── rules/
        └── maestro-source.mdc   ← alwaysApply, מפנה לכספת, מתעלם מ-Cloudflare
```

## מה הועבר ל-Maestro (בוטלו כפילות)

- **TypeScript:** imports at top, exhaustive switch → `04-knowledge/standards/source6681-standards.md`
- **Workflows:** execute, review, finishing-branch, brainstorm → `03-agents/workflows/`, `03-agents/skills/`
- **Standards:** stack, entity, security, naming → `04-knowledge/standards/source6681-standards.md`

## Cursor Settings — פעולה ידנית (אופציונלי)

אם Cloudflare workers rule עדיין מוזרק:

- **Cursor Settings → Rules, Skills, Subagents**
- Scope: **source6681**
- השבת את **workers** rule (Cloudflare) — source6681 משתמש ב-Vercel, לא Cloudflare.

## Skills — Maestro קודם

כשמתאים: execute, review, finishing-branch, brainstorm — קרא מ-`03-agents/` בכספת.
Cursor skills (verification, TDD, vercel-react-best-practices) — משלימים, לא חופפים.
