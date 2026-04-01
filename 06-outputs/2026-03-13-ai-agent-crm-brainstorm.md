# 🧠 Brainstorm: סוכן AI אוטומטי ללקוחות CRM

## Context

hadaryaCRM הוא CRM מותאם ללקוחות (Xsheva). כיום יש דף Automations עם אוטומציות קבועות (שליחת הצעות, לכידת לידים, ארכוב, וואטסאפ) — אבל אין מנוע AI שעושה דברים בצורה חכמה ואוטומטית.

**צורך:** משהו ש**לקוחות המשתמשים ב-CRM** ייהנו ממנו — סוכן שרץ ברקע ומבצע תהליכים אוטומטיים, לא רק אוטומציות if-then קבועות.

---

## Option A: AI Assistant בצ'אט (Agent as Interface)

**תיאור:** צ'אטאבוט בתוך ה-CRM — הלקוח כותב "תזכור לי לשלוח follow-up ללידים שלא ענו שבוע" או "סכם לי את הדילס החשובים היום", והסוכן מבצע.

✅ **Pros:**
- חוויית שימוש טבעית — שיחה במקום ללחוץ כפתורים
- יכול להשיג תוצאות שלא תכננת מראש (emergent capability)
- הלקוח מגדיר בעצמו מה חשוב — "תעדכן לידים שלא דיברנו איתם 5 ימים"

❌ **Cons:**
- דורש UI חדש (צ'אט), אינטגרציה עם LLM, טיפול ב-context
- עלויות API לפי שיחה
- צריך להחליט: real-time או async?

📊 **Effort:** High

---

## Option B: AI-Powered Scheduled Jobs (Agent as Background Worker)

**תיאור:** משימות מתוזמנות שהסוכן מפעיל — למשל כל בוקר: "נתח לידים, עדכן סטטוס, צור משימות follow-up ללידים שלא טופלו". הלקוח מגדיר מתי וה-prompt, הסוכן רץ ברקע.

✅ **Pros:**
- ערך מיידי: "כל יום 08:00 — תמצא לידים ללא פעילות 7 ימים ותצור משימות"
- לא דורש UI שיחה — אפשר להוסיף לדף Automations הקיים
- Edge Function / cron פשוט יחסית עם Supabase

❌ **Cons:**
- פחות גמיש — הלקוח לא שואל שאלות ad-hoc
- צריך prompts מוגדרים מראש או template לבחירה

📊 **Effort:** Medium

---

## Option C: Smart Enrichment & Suggestions (Agent as Enhancer)

**תיאור:** הסוכן מעשיר נתונים אוטומטית — כשנכנס ליד חדש, הסוכן ממלא פרטי חברה, LinkedIn, וכו'. כשסוכן נכנס לדיל — מקבל הצעות "מה הלאה" (email template, reminder).

✅ **Pros:**
- ערך ברור: פחות הקלדה, פחות שכחה
- יכול להימסר דרך הרחבת ה-UI הקיים (tooltips, badges, suggested actions)
- לא דורש "שיחה" — הכל אוטומטי ברקע

❌ **Cons:**
- דורש APIs חיצוניים (enrichment) או היסטוריה מקומית (suggestions)
- עלול להרגיש "פחות סוכן" ויותר "feature חכמה"

📊 **Effort:** Medium

---

## Option D: Hybrid — Command Palette + Scheduled Agent

**תיאור:** שילוב: 
1. **Command Palette** (כבר קיים ב-GlobalCommandPalette) — הרחבה עם פקודות AI: "מצא לידים ללא פעילות", "סכם את הלידים החדשים השבוע"
2. **Scheduled Agent** — משימות מתוזמנות שמוגדרות ב-Automations

✅ **Pros:**
- משתמש ב-UI קיים (Command Palette)
- גם on-demand (הלקוח מבקש) וגם scheduled (אוטומטי)
- התחלה קטנה — פקודה אחת, אחר כך מתרחב

❌ **Cons:**
- דורש אינטגרציה ל-LLM + tools (CRUD לידים, deals, משימות)
- צריך לתכנן action parity (כל מה שהמשתמש עושה ב-UI — הסוכן יכול)

📊 **Effort:** Medium–High

---

## 💡 Recommendation

**Option D (Hybrid)** או **Option B** — תלוי בעדיפויות:

- אם הלקוח רוצה **להרגיש** שיש "סוכן שעובד בשבילו" → **Option D** — Command Palette עם פקודות AI מרגיש כמו עוזר זמין.
- אם הערך העיקרי הוא **חסכון זמן בלי אינטראקציה** → **Option B** — משימות מתוזמנות פשוטות ליישם, ו-Automations כבר קיים.

**צעד ראשון מומלץ:** הוספת **AI Scheduled Job** אחד לדף Automations — למשל "לידים ללא פעילות 7 ימים → צור משימות follow-up". זה מאפשר:
1. הוכחת ערך מהירה
2. למידה מה הלקוחות רוצים
3. תשתית שממנה אפשר להרחיב ל-Command Palette / צ'אט

---

## Next Step

מה הכיוון שמעניין אותך?
- **A** — צ'אט מלא
- **B** — משימות מתוזמנות בלבד
- **C** — העשרה והצעות
- **D** — היבריד (Command Palette + scheduled)

אחרי שתבחר → invoke `project-planner` לתוכנית יישום מפורטת.
