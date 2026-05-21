---
title: Cabinet — Cleanup & AI Integration Plan (revised)
date: 2026-05-21
status: draft — awaiting approval
owner: Kobi
scope: cabinet cleanup, capture flow, retire vault, Claude Code wiring
supersedes: ~/Library/Mobile Documents/.../Maestro/06-outputs/2026-05-21-vault-organization-plan.md
---

# Cabinet — תכנית מתוקנת

## הקשר חדש

ה-Obsidian vault ב-iCloud (`Maestro/`) הוא **clone של רגע המיגרציה ל-Cowork**.
- התוכן זהה כרגע ל-`~/cabinet/`
- כל עריכה ב-Cowork יוצרת drift עד שה-vault יישאר תקוע בעבר
- אתה לא משתמש ב-Obsidian/iCloud mobile/GitHub web → ה-vault הוא baggage נטו

**החלטה (2026-05-21):**
- Cabinet = source of truth יחיד
- Vault → archive ואז למחוק
- Interfaces: Cowork desktop + Claude Code CLI בלבד

---

## Phase 0 — להריץ עכשיו (~30 min)

**מטרה:** לעצור את ה-bleeding. Claude Code לא יקרא יותר מ-vault.

### 0.1 לעדכן ~/.claude/CLAUDE.md

ה-file הזה כרגע מצביע על vault paths:
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Maestro/01-me/01-me.md
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Maestro/03-agents/agent-routing.md
```

צריך להחליף ל:
```
~/cabinet/me/01-me-identity.md      (השם שונה ב-cabinet)
~/cabinet/agent-library/agent-routing.md
```

### 0.2 לעדכן הפניות coding standards
ב-CLAUDE.md הגלובלי יש הפניות ל:
```
…/Maestro/04-knowledge/standards/base-coding-standards.md
…/Maestro/01-me/01-me-writing.md
```
→ להחליף ל:
```
~/cabinet/knowledge/standards/base-coding-standards.md
~/cabinet/me/01-me-writing.md
```

### 0.3 Verification
- [ ] לפתוח session חדש של Claude Code, לשאול "what's in my identity file" → לוודא שזה קורא מ-cabinet
- [ ] לבדוק שאין breaks

---

## Phase 1 — Archive & Delete vault (~20 min)

**מטרה:** להוציא את ה-vault מהמשחק לחלוטין, אבל לא לאבד שום דבר.

### 1.1 Pre-flight: לוודא ש-cabinet מכיל הכל
```bash
diff -rq /Users/kobihazout/cabinet "$VAULT" \
  | grep "Only in.*Maestro" \
  | grep -v "\.obsidian\|\.git\|\.DS_Store\|\.github\|\.gitignore\|\.repo.yaml\|\.claude"
```
צריך להחזיר ריק. אם יש קבצים שהם רק ב-vault (ולא metadata) — צריך להעתיק אותם ל-cabinet קודם.

### 1.2 Backup לארכיון
```bash
# יצירת tarball של ה-vault (כדי שיהיה ניתן לשחזר אם משהו ידרש)
tar -czf ~/Documents/maestro-vault-archive-2026-05-21.tar.gz \
  -C "/Users/kobihazout/Library/Mobile Documents/iCloud~md~obsidian/Documents" \
  Maestro
```

### 1.3 Push אחרון של ה-vault ל-GitHub (snapshot של "last day of vault era")
```bash
cd "$VAULT"
git add -A && git commit -m "Final snapshot before retirement — superseded by cabinet"
git push
```
(זה משאיר עקבות ב-github.com/KobiHaz/maestro כתיעוד היסטורי)

### 1.4 מחיקת ה-vault מ-iCloud
```bash
rm -rf "/Users/kobihazout/Library/Mobile Documents/iCloud~md~obsidian/Documents/Maestro"
```

### 1.5 Verification
- [ ] iCloud free space שוחרר
- [ ] `~/.claude/CLAUDE.md` לא מצביע על שום vault path
- [ ] tarball קיים ב-`~/Documents/maestro-vault-archive-2026-05-21.tar.gz`
- [ ] github.com/KobiHaz/maestro מציג את הקומיט "Final snapshot"

---

## Phase 2 — Cleanup of cabinet (~1.5h)

אותם בעיות שזיהיתי קודם — אבל עכשיו ב-cabinet (שזה ה-source of truth):

### 2.1 Skills duplication
ב-`~/cabinet/agent-library/skills/` יש 42 ספריות. ~25 מתוכן הן עותקים של skills שמגיעים כ-anthropic-skills גלובליים ב-Claude Code (api-patterns, architecture, clean-code, וכו').

**מומלץ:**
- למחוק את ה-25 הכפולים
- להשאיר את ה-17 הייחודיים שלך (cv-builder, d1-leads-analysis, consul-house-weekly-report, וכו')
- ב-`README.md` להבהיר: "כל skill כאן הוא custom, לא קיים ב-anthropic-skills"

רשימת skills שכן ייחודיים (שווה לבדוק כל אחד לפני מחיקה):
app-builder · bash-linux · behavioral-modes · brainstorming · consul-house-weekly-report · cv-builder · d1-leads-analysis · frontend-design · parallel-agents · powershell-windows · red-team-tactics · rust-pro · seo-fundamentals · server-management · systematic-debugging

הערה: חלק מאלה גם קיימים כ-anthropic או כ-superpowers (brainstorming, systematic-debugging, parallel-agents). השוואה ידנית קצרה (10 דק׳ לכל אחד) לפני מחיקה.

### 2.2 Outputs cleanup
ב-`~/cabinet/outputs/` יש 66 קבצים, חלקם קוד (`.mjs`, `.csv`, `package.json`).

קבצים להעביר (אותם בעיות כמו בתכנית הקודמת, רק עם paths חדשים):
- `Consul-House-Registry-headers.csv` → `~/cabinet/projects/consul-house/data/`
- `create-consul-house-sheet.mjs` → `~/cabinet/projects/consul-house/scripts/`
- `package.json`, `package-lock.json` → `~/cabinet/projects/consul-house/`
- `Documents.code-workspace` → מחיקה (workspace file ל-VSCode, לא שייך)

**חוק חדש ב-cabinet:** `outputs/` רק markdown deliverables.

### 2.3 הסרת empty/orphan files
- `Untitled.canvas`, `Untitled.base` — אם קיימים ב-cabinet (קיימים בvault, יתכן שגם כאן), למחוק
- `2026-04-13.md` ריק — למחוק

### 2.4 Verification
- [ ] `agent-library/skills/` ≤ 25 ספריות
- [ ] `outputs/` רק `.md`
- [ ] git diff נקי, רק השינויים שתכננו

---

## Phase 3 — Capture flow (~2h)

ה-cabinet אין לו `00-inbox`. צריך לבנות capture flow שעובד **דרך Cowork**, לא דרך Obsidian.

### 3.1 מבנה חדש ב-cabinet
```
~/cabinet/
├── inbox/                      ← חדש
│   ├── README.md
│   ├── quick-notes/
│   ├── web-clips/
│   ├── voice-memos/
│   └── _processed/
├── logs/
│   ├── daily/                  ← חדש
│   │   └── 2026/05/2026-05-21.md
│   └── weekly/                 ← חדש
└── templates/                  ← קיים, להעשיר
    ├── daily-note.md           ← חדש
    ├── weekly-review.md        ← חדש
    ├── project-readme.md       ← חדש
    └── reference-doc.md        ← חדש
```

### 3.2 ה-Cowork-native capture
במקום Obsidian plugins, לנצל את הכלים של Cowork:

- **Quick capture:** chat thread ב-Cowork → סוכן יקטלג ויעביר ל-`inbox/quick-notes/`
- **Daily note auto:** סוכן ב-`.agents/` שרץ בבוקר, יוצר `logs/daily/YYYY/MM/YYYY-MM-DD.md` מ-template
- **Web clipper:** Chrome extension (יש Claude in Chrome MCP זמין כאן) → שמירה ל-`inbox/web-clips/`
- **Weekly review:** סוכן בשישי שמייצר checklist על בסיס `inbox/` + שינויים בפרויקטים

### 3.3 Templates
4 templates ב-`~/cabinet/templates/`:

**daily-note.md:**
```markdown
---
date: {{date}}
type: daily
---
# {{date}}

## Priorities today
- [ ]

## Log

## Captures from inbox

## Tomorrow
```

**weekly-review.md:**
```markdown
---
week: {{week}}
date: {{date}}
type: weekly-review
---
# Week {{week}} review

## Inbox triage
[ ] עבור על inbox/, סווג כל פריט

## Project activity
- פרויקטים שזזו השבוע:
- פרויקטים שלא נגעתי:

## Decisions made

## Carry forward
```

### 3.4 Verification
- [ ] `inbox/` קיים עם 4 תתי-תקיות
- [ ] 4 templates ב-`templates/`
- [ ] daily note אוטומטי קיים ב-`logs/daily/2026/05/`
- [ ] שבוע נוסה בפועל

---

## Phase 4 — AI tools integration (~1h)

קצר עכשיו כי `Obsidian-native` הוסר.

### 4.1 Claude Code
- כבר עובד דרך CLAUDE.md הגלובלי המעודכן (Phase 0)
- ה-custom skills של ה-cabinet כבר זמינים מקומית (במיקום `agent-library/skills/`). שווה לעשות symlink:
  ```bash
  ln -sfn ~/cabinet/agent-library/skills ~/.claude/skills/cabinet-custom
  ```

### 4.2 NotebookLM
- היום מחובר: MediaNet → `66e5cb4e`
- **תוכנית:** notebook נוסף לכל תחום (לא לפרויקט):
  - `Cabinet-Business` ← `me/01-me-business.md` + `projects/*/README.md`
  - `Cabinet-Engineering` ← `knowledge/reference/` + `knowledge/standards/`
- Sync: ידני שבועי (export markdown ל-Drive folder ש-NotebookLM קורא)

### 4.3 OpenHuman — לדחות
Early beta + GPL. לחזור עוד 2-3 חודשים.

### 4.4 Git audit
ה-cabinet אין לו remote כרגע. החלטה:
- האם להוסיף remote private ל-GitHub (`KobiHaz/cabinet-private`)?
- או לסמוך על iCloud/Time Machine backup?

→ המלצה: private remote. ל-backup + history + רב-מכשירי.

---

## Execution order מתוקן (~5h)

| בלוק | משך | תוכן |
|---|---|---|
| 1 | 30min | Phase 0 — עדכון CLAUDE.md הגלובלי |
| 2 | 20min | Phase 1 — archive + delete vault |
| 3 | 1.5h | Phase 2 — cleanup cabinet (skills, outputs, orphans) |
| 4 | 1.5h | Phase 3 — capture flow + templates |
| 5 | 1h | Phase 4 — AI integration + git remote |
| 6 | 20min | Verification full pass — capture → process → find |

---

## פתוח להכרעה

1. **מתי לבצע Phase 1 (vault retirement)?**
   - מיד אחרי Phase 0
   - אחרי Phase 2 (לוודא ש-cabinet יציב)
   - לדחות בשבוע — לוודא שלא חסר כלום

2. **`docs/` ו-`scripts/` ב-cabinet?**
   - יש לבדוק אם הם בכלל קיימים ב-cabinet (קיימים ב-vault)

3. **Git remote ל-cabinet?**
   - private GitHub repo
   - או לוותר ולסמוך על iCloud/TM backup

4. **Skills כפולים — manual review או bulk delete?**
   - manual: 10 דק׳ לכל אחד = ~3 שעות לכל ה-25
   - bulk: 5 דקות אבל סיכון לאבד custom variant

---

## מה אני צריך ממך

1. אישור על ה-order החדש (5h במקום 6h)
2. החלטה על 4 ה-open questions
3. **חשוב:** לוודא שלא יש שום עריכה פעילה ב-vault ברגע ההמרה — אם יש משהו ב-iCloud שעוד לא הסתנכרן, נאבד אותו
