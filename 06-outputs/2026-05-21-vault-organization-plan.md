---
title: Maestro Vault — Organization & AI Integration Plan
date: 2026-05-21
status: draft — awaiting approval
owner: Kobi
scope: vault cleanup, capture flow, AI tool integration
---

# Maestro Vault — תכנית סדר וחיבור ל-AI

## למה זה כאן

`/Users/kobihazout/Library/Mobile Documents/iCloud~md~obsidian/Documents/Maestro` הוא ה-vault המרכזי שלך. הוא:
- מסונכרן ל-iCloud (זמין במובייל/דסקטופ)
- git repo עם remote ב-[github.com/KobiHaz/maestro](https://github.com/KobiHaz/maestro)
- נטען אוטומטית ל-Claude דרך `~/.claude/CLAUDE.md`
- מכיל היום ~350 קבצים מעל 10 ספריות עליונות

הבעיות שזיהינו (2026-05-21):
1. כפילות skills בין ה-vault ל-Claude plugins הגלובליים
2. אין capture flow שעובד — `00-inbox` ריק
3. `06-outputs` מערבב markdown deliverables עם קבצי קוד
4. קבצים יתומים ב-root
5. כלי AI חיצוניים (NotebookLM, OpenHuman) לא מחוברים שיטתית

המטרה: הופך את ה-vault ל**מקור אמת יחיד** של ידע אישי + עסקי, שמוזן אוטומטית, נקי מ-noise, ונגיש לכל כלי AI שאני משתמש בו.

---

## מצב נוכחי (snapshot)

```
Maestro/
├── 00-inbox/         1 file   ← לא בשימוש
├── 01-me/            6 files  ✓ זהות, business, preferences
├── 02-projects/      30 files, 14 פרויקטים (CRM, CMS, smart-volume-radar...)
├── 03-agents/        184 files
│   ├── specialists/  17  ✓ custom specialists
│   ├── workflows/    17  ✓ workflows
│   ├── skills/       42  ⚠️ 25 מתוכם כפולים של anthropic-skills גלובליים
│   ├── content/      1
│   └── games/        2
├── 04-knowledge/     32 files (reference + standards)  ✓ נקי יחסית
├── 05-templates/     5 files  ⚠️ דליל
├── 06-outputs/       65 files  ⚠️ מערבב md + csv + js + package.json
├── 07-logs/          9 files  ⚠️ דליל, אין daily/weekly
├── docs/, scripts/   ⚠️ לא חלק מהמספור
├── CLAUDE.md         ✓ vault-level
├── Home.md           ✓
├── Untitled.canvas   ⚠️ ריק
├── Untitled.base     ⚠️ ריק
└── 2026-04-13.md     ⚠️ ריק
```

**Obsidian plugins פעילים:** `obsidian-local-rest-api`, `obsidian-tasks-plugin` בלבד.

**Skills כפולים שזוהו** (קיימים גם ב-vault וגם כ-anthropic-skill גלובלי ב-Claude):
api-patterns · architecture · clean-code · code-review-checklist · database-design · deployment-procedures · documentation-templates · game-development · geo-fundamentals · i18n-localization · intelligent-routing · lint-and-validate · mcp-builder · mobile-design · nextjs-react-expert · nodejs-best-practices · performance-profiling · plan-writing · python-patterns · tailwind-patterns · tdd-workflow · testing-patterns · vulnerability-scanner · web-artifacts-builder · web-design-guidelines · webapp-testing

**Skills custom (vault-only, לשמור):**
app-builder · bash-linux · behavioral-modes · brainstorming · consul-house-weekly-report · cv-builder · d1-leads-analysis · frontend-design · parallel-agents · powershell-windows · red-team-tactics · rust-pro · seo-fundamentals · server-management · systematic-debugging · skill-template

(הערה: חלק מהשמות בעצם קיימים כ-anthropic-skill — צריך בדיקה לפני מחיקה. ב-Phase 1.)

---

## Phase 1 — Cleanup (1.5h)

**מטרה:** vault רזה, בלי כפילויות, בלי קבצים יתומים.

### 1.1 מחיקת קבצים יתומים ב-root
- `Untitled.canvas` (2 bytes)
- `Untitled.base` (39 bytes)
- `2026-04-13.md` (0 bytes)
- `.DS_Store` (להוסיף ל-.gitignore אם לא שם)

### 1.2 ארגון מחדש של `06-outputs/`
**חוק חדש:** רק markdown deliverables. אין `.mjs`, `.csv` חיים, `.json`, `package.json`.

קבצים להעביר:
- `Consul-House-Registry-headers.csv` → `02-projects/consul-house/data/`
- `create-consul-house-sheet.mjs` → `02-projects/consul-house/scripts/`
- `package.json` + `package-lock.json` → `02-projects/consul-house/`
- `Documents.code-workspace` → למחוק (workspace file ל-VSCode, לא שייך)

### 1.3 ניקוי skills כפולים
**גישה:** עבור כל skill ב-`03-agents/skills/` שיש לו תאום ב-anthropic-skills:
1. השוואה — לבדוק שה-anthropic version מכסה את התוכן של ה-vault
2. אם כן — מחיקה מה-vault, השארת comment ב-`03-agents/skills/README.md` שמפנה ל-anthropic
3. אם ה-vault version יותר עשיר → השארה + שינוי שם ל-`<name>-extended` כדי שלא יתחרה

**שמות לבדיקה ידנית:** `bash-linux`, `behavioral-modes`, `brainstorming`, `frontend-design`, `parallel-agents`, `seo-fundamentals`, `systematic-debugging` — חלקם כן קיימים ב-anthropic-skills/superpowers, חלקם הם custom שלך.

### 1.4 ספריות לא ממוספרות
החלטה לגבי `docs/` ו-`scripts/`:
- **`docs/plans/`** → אם זה plans פעילים, להעביר ל-`02-projects/maestro/plans/`. אם זה ארכיון, ל-`07-logs/`.
- **`scripts/`** → אם זה vault-maintenance scripts, להשאיר אבל לשנות שם ל-`.vault-scripts/` (מוסתר מ-Obsidian).

### 1.5 Verification
- [ ] `06-outputs/` מכיל רק `.md` ותתי-ספריות עם date prefix
- [ ] `03-agents/skills/` ירד מ-42 ל-≤25 (custom only)
- [ ] root נקי מקבצים ריקים
- [ ] `git status` מראה רק את השינויים שתכננו

---

## Phase 2 — Capture flow (2h)

**מטרה:** כל מחשבה/לינק/מסמך נכנס למקום מוגדר תוך פחות מ-10 שניות. עיבוד שבועי 30 דקות.

### 2.1 מבנה `00-inbox/`
```
00-inbox/
├── README.md              ← הסבר על ה-flow
├── quick-notes/           ← capture מהיר מהמובייל
├── web-clips/             ← Obsidian Web Clipper
├── voice-memos/           ← קבצי שמע + transcript
├── screenshots/           ← תיוג + תאריך
└── _processed/            ← ארכיון אחרי triage
```

### 2.2 Plugins לחובה להתקין
| Plugin | למה |
|---|---|
| **Templater** | החלפת ה-template variables ב-frontmatter, daily note auto |
| **Periodic Notes** | daily/weekly/monthly notes אוטומטיים |
| **QuickAdd** | macro לקליטה מהירה: "new project", "new reference", "log entry" |
| **Obsidian Web Clipper** (browser ext) | קליטת web pages ישר ל-`00-inbox/web-clips/` |

### 2.3 Templates ב-`05-templates/`
- `daily-note.md` — מבנה לכל יום: priorities, log, captures, links
- `weekly-review.md` — checklist לעיבוד inbox, סקירת projects
- `project-readme.md` — template ל-project חדש ב-`02-projects/`
- `reference-doc.md` — template ל-reference document
- `meeting-notes.md` — לפגישות (עם backlinks לאנשים/פרויקטים)

### 2.4 Daily notes flow
- מיקום: `07-logs/daily/2026/05/2026-05-21.md` (תקייה אוטומטית לפי תאריך)
- נפתח אוטומטית כש-Obsidian נטען
- כל היום מקלידים שם הערות / לוגים
- בסוף יום: רץ macro QuickAdd "EOD" שעובר על הקבצים החדשים ב-`00-inbox/` ומציע סיווג

### 2.5 Weekly review (שישי 30 דק׳)
template `05-templates/weekly-review.md` שכולל:
1. עבור על `00-inbox/` — לכל פריט: keep / file / archive / delete
2. עבור על `02-projects/*` שלא נגעת בהם השבוע — האם להעביר ל-`07-logs/archive/projects/`?
3. סנכרון `01-me/01-me.md` — שינויים בהעדפות/business
4. push ל-git

### 2.6 Verification
- [ ] 4 plugins מותקנים ופעילים
- [ ] daily note נפתח אוטומטית
- [ ] 5 templates ב-`05-templates/`
- [ ] שבוע ראשון של שימוש עבר (test בשבת)

---

## Phase 3 — AI integration (2-3h)

**מטרה:** כל כלי AI שאני משתמש בו רואה את אותו ה-vault, ללא export ידני, עם הרשאות נכונות.

### 3.1 Claude Code (כבר עובד)
- `~/.claude/CLAUDE.md` הגלובלי טוען את `01-me/01-me.md` ו-`agent-routing.md` בכל סשן
- ה-vault הוא git repo, כך ש-Claude יכול לעשות לו commits
- **שיפור:** לוודא ש-`~/.claude/skills/` מצביע ל-`03-agents/skills/` (symlink) כדי שה-custom skills יהיו זמינים גלובלית גם שאנחנו לא ב-vault

```bash
# הצעה לסימלינק (אחרי ניקוי Phase 1)
ln -sfn "/Users/kobihazout/Library/Mobile Documents/iCloud~md~obsidian/Documents/Maestro/03-agents/skills" \
        ~/.claude/skills/maestro-custom
```

### 3.2 NotebookLM
- היום מחובר: MediaNet → notebook `66e5cb4e` (LegitScript)
- **תכנית:** notebook אחד לכל **תחום** עיקרי (לא לכל project):
  - `Maestro-Business` ← `01-me/01-me-business.md` + `02-projects/*/README.md`
  - `Maestro-Engineering` ← `04-knowledge/reference/` + `04-knowledge/standards/`
  - `Maestro-Compliance-Health` ← (קיים: 66e5cb4e)
- **Sync strategy:** export שבועי של תקיות רלוונטיות כ-PDF/markdown לתוך Drive folder ש-NotebookLM קורא
- אופציה: script שרץ pre-commit hook ב-git ומעדכן NotebookLM sources דרך API (אם NotebookLM יחשוף API ציבורי — בינתיים ידני)

### 3.3 OpenHuman (אופציונלי, בנפרד)
- early beta, GPL — בודקים לפני שמכניסים לתהליך
- **אם משתמשים:** מגדירים את ה-vault path כ-Obsidian wiki source שלו (כי הוא תוכנן בדיוק לזה)
- ה-Memory Tree שלו יבנה אוטומטית מהקבצים שלך
- **חיבור משותף:** `memory.backend = "agentmemory"` ב-OpenHuman config — אותו memory store ישמש גם Claude Code (דרך agentmemory MCP server אם יותקן)
- **לא לפני** שעובר Phase 1+2 — אחרת OpenHuman יבלע גם את ה-noise

### 3.4 Public / Private split
ה-vault הוא git repo עם remote ב-GitHub. צריך לוודא:
- `01-me/` — האם מכיל מידע אישי? לבדוק מה לא לדחוף
- `02-projects/*/secrets.md`, `*.env` — `.gitignore` כבר קיים אבל לבדוק
- אופציה: לפצל ל-2 repos: `maestro-public` (knowledge, skills, agents) + `maestro-private` (01-me, business secrets, project credentials)

### 3.5 Verification
- [ ] Claude Code רואה את ה-custom skills גלובלית
- [ ] לפחות notebook NotebookLM אחד נוסף חדש, עם sources מ-vault
- [ ] (אופציונלי) OpenHuman מותקן ועובד עם ה-vault
- [ ] git audit — אין סודות ב-public remote

---

## Open decisions (לפני שמתחילים)

1. **Skills custom שכמעט-כפולים** (bash-linux, frontend-design, וכו') — האם להשוות אחד-אחד ידנית או לסמוך על ה-anthropic version ולמחוק עיוורת?
   → המלצה: ידני. 10 דק׳ לכל אחד.

2. **`docs/` ו-`scripts/` ב-root** — האם זה תוכן שאמור להישאר ב-vault או שזה צריך לעבור ל-`02-projects/maestro/`?

3. **2 repos public+private או 1 repo עם .gitignore חזק?**
   → המלצה: 1 repo עם .gitignore. פחות תחזוקה.

4. **OpenHuman עכשיו או אחרי 2-3 חודשים שהוא בוגר יותר?**
   → המלצה: לדחות. הוא ב-early beta. agentmemory + NotebookLM מספיקים.

5. **Sync שיטה ל-NotebookLM** — manual שבועי או pre-commit hook?
   → המלצה: manual עד שיש workflow קבוע, אז להחליט.

---

## הצעת execution order

יום של ~6 שעות, מחולק:

| בלוק | משך | תוכן |
|---|---|---|
| בוקר | 1.5h | Phase 1 — cleanup |
| בוקר | 1h | Phase 2.1-2.2 — מבנה inbox + plugins |
| צהריים | 1h | Phase 2.3-2.4 — templates + daily notes |
| צהריים | 0.5h | Phase 2.5 — weekly review template |
| אחה"צ | 1.5h | Phase 3.1-3.2 — Claude symlink + NotebookLM |
| אחה"צ | 0.5h | Phase 3.4 — git audit |
| סיום | 30min | בדיקת golden path: capture → process → find |

---

## מה אני צריך ממך לפני שאני מתחיל

1. אישור על ה-execution order (או דחיית/הוספת שלבים)
2. תשובות ל-5 ה-open decisions
3. אישור שאני יכול לעשות `git commit` לאורך הדרך (כדי שיהיה rollback path)

אחרי האישור — אני מתחיל ב-Phase 1 וכותב log שוטף ב-`07-logs/2026-05-21-vault-cleanup.md`.
