# 🧠 Brainstorm: אוטומציית לידים → iPlan CRM (Zapier/Make)

## Context

- **מטרה:** לחבר את כל מקורות הלידים (אתר, אינסטגרם, פייסבוק) למערכת iPlan CRM, עם בדיקת כפילויות, התראות על כפילויות, סיכום שבועי, ומנגנון retry.
- **משתמש:** עסק שמשתמש ב־iPlan CRM ומאסי לידים מטופסי אתר ורשתות חברתיות.
- **אילוצים:** iPlan יש API (REST) ליצירת לידים – אין אפליקציה native ב־Zapier. בדיקת כפילויות דורשת מקור אמת (registry) כי iPlan API מספק רק `POST /leads`, לא חיפוש לידים.

---

## MCP: Zapier vs Make

| | Zapier MCP | Make MCP |
|---|---|---|
| **קיים?** | ✅ כן – רשמי מ־Zapier | ✅ כן – `@makehq/mcp-server` |
| **סוג חיבור** | URL (SSE): `https://actions.zapier.com/mcp/YOUR_MCP_KEY/sse` | stdio: `npx -y @makehq/mcp-server` |
| **מה ה־MCP עושה** | מאפשר ל־AI להפעיל **Actions** שבחרת (כל פעולה = 2 tasks ב־Zapier) | מפעיל **Scenarios** מסוג On-Demand (לא Triggers) |
| **התאמה לאוטומציה** | MCP = הפעלת פעולות ביד; **אוטומציה רציפה** נעשית ב־**Zaps** (לא דרך MCP) | MCP = הפעלת סקריפוים; **אוטומציה רציפה** ב־**Scenarios** |

**מסקנה חשובה:** Zapier MCP ו־Make MCP מתאימים ל־**הפעלת פעולות מהצ'אט**, לא לניהול אוטומציות רציפה.  
האוטומציה עצמה (Trigger → בדיקת כפילויות → שליחה ל־iPlan) נבנית ב־**Zapier Zaps** או ב־**Make Scenarios**, והחיבור ל־Cursor MCP שימושי כשאתה רוצה להפעיל פעולות נקודתיות או לבדוק סטטוס.

---

## Option A: Zapier (Zaps) + Google Sheets כ־Registry

**תיאור:** יוצרים Zaps נפרדים לאתר, אינסטגרם ופייסבוק. כל Zap: (1) מקבל ליד, (2) בודק ב־Google Sheet אם האימייל/טלפון כבר קיים, (3) אם לא – שולח ל־iPlan (דרך Webhooks), רושם ב־Sheet; אם כן – שולח מייל התראה.

✅ **Pros:**
- ממשק נוח, הרבה אפליקציות out-of-the-box (כולל Facebook Lead Ads, Instagram)
- Zapier Retries מובנה (כל Zap מנסה שוב אוטומטית במקרה כישלון)
- קל לתחזוקה ללא קוד

❌ **Cons:**
- iPlan אין אפליקציה native – צריך Webhooks/HTTP Request
- בדיקת כפילות דרך Google Sheets דורשת Zap מורכב (Lookup + Filter + Paths)
- עלות Tasks – כל ליד = כמה tasks (Trigger + Lookup + HTTP + Update Sheet)

📊 **Effort:** Medium

---

## Option B: Make (Scenarios) + Google Sheets / Airtable

**תיאור:** אותו רעיון עם Make. Scenario לכל מקור, בדיקת כפילויות ב־Google Sheets או Airtable, שליחה ל־iPlan דרך HTTP module.

✅ **Pros:**
- Make חזק יותר ב־Logic (Router, Filter, Aggregator) – מתאים לזרימות מורכבות
- Retry ו־Error handling מדויקים יותר
- מחיר לפי Operations – לעיתים זול יותר מנפח גבוה

❌ **Cons:**
- עקומת למידה קצת גבוהה מ־Zapier
- גם כאן iPlan דרך HTTP – אין connector native

📊 **Effort:** Medium–High

---

## Option C: Zapier + Make היברידי + Zapier MCP

**תיאור:** Zapier ל־Triggers (אתר, אינסטגרם, פייסבוק) – כיוון שיש להם connectors מובנים; Make או Zapier ל־Logic (כפילויות, retry, סיכומים). Zapier MCP מחובר ל־Cursor כדי שתוכל להפעיל פעולות (למשל "שלח ליד ידני ל־iPlan") מהצ'אט.

✅ **Pros:**
- שימוש ביתרונות של כל פלטפורמה
- MCP מאפשר שליטה ו־debug מהצ'אט

❌ **Cons:**
- תחזוקה בשתי פלטפורמות
- עלול להיות מבלבל לאיזה שירות הולך כל ליד

📊 **Effort:** High

---

## רכיבים נדרשים (חלים על כל האופציות)

### 1. בדיקת כפילויות
- **מקור אמת:** Google Sheet / Airtable עם עמודות: email, phone, source, created_at
- **לוגיקה:** לפני שליחה ל־iPlan – חיפוש לפי email או phone; אם קיים → Path "duplicate" → מייל; אם לא → Path "new" → שליחה + רישום

### 2. התראה על כפול
- Gmail / Outlook דרך Zapier/Make – "ליד כפול: [email], מקור: [source]"

### 3. סיכום שבועי (כל חמישי בלילה)
- Schedule Trigger (חמישי 00:00 או 23:00)
- אגרגציה: ספירת לידים חדשים, כפילויות, לפי מקור
- שליחת מייל סיכום (או Slack)

### 4. מנגנון Retry
- **Zapier:** Retries אוטומטיים; אפשר להוסיף Zap נפרד שבודק "לידים שנשלחו אבל לא אומתו" (דורש לוג)
- **Make:** Error Handler + Reconnect; אפשר Scenario שרץ על תאריך מסוים ובודק לידים "ממתינים לאימות"

---

## 💡 Recommendation

**Option A (Zapier + Google Sheets)** אם אתה מעדיף פשטות וזרימה מהירה.

**Option B (Make)** אם אתה מצפה להרבה לידים, לוגיקה מורכבת, או שרוצה שליטה חזקה ב־retry ו־error handling.

בשני המקרים:
1. **חבר Zapier MCP** ל־Cursor – שימושי להפעלות ידניות ו־debug.
2. **חבר Make MCP** רק אם אתה בוחר ב־Make כפלטפורמת אוטומציה ראשית.

---

## צעדים מעשיים מיידיים

### חיבור Zapier MCP ל־Cursor
1. היכנס ל־[Zapier MCP Settings](https://actions.zapier.com/settings/mcp/)
2. העתק את ה־MCP URL
3. ב־Cursor: Settings (⇧⌘J) → MCP → Add MCP Server
4. הוסף לקובץ ההגדרות:
```json
"Zapier MCP": {
  "url": "https://actions.zapier.com/mcp/YOUR_MCP_KEY/sse"
}
```
5. בחר ב־[Zapier MCP](https://actions.zapier.com/mcp/start/) אילו Actions ה־AI יכול להפעיל

### חיבור Make MCP (אופציונלי)
```json
"make": {
  "command": "npx",
  "args": ["-y", "@makehq/mcp-server"],
  "env": {
    "MAKE_API_KEY": "<from make.com profile>",
    "MAKE_ZONE": "eu2.make.com",
    "MAKE_TEAM": "<team-id from URL>"
  }
}
```

### iPlan API
- Endpoint: `https://iplan.co.il/he-IL/api/corp/leads.json`
- Headers: `Content-Type: application/json`
- Body: `api_key`, `form_id`, `contact_full_name`, `contact_email`/`contact_phone`, `request_content`, `request_matter`
- [מסמכי API](http://apidocs.iplan.co.il/)

---

## Next Step

כשתבחר כיוון:
- **Zapier** → Invoke `project-planner` לתכנון Zaps מפורט (טריגרים, Paths, Webhooks)
- **Make** → אותו דבר עם Scenarios
- **חיבור MCP** → אפשר להוסיף את ההגדרות ל־`.cursor/mcp.json` של הפרויקט
