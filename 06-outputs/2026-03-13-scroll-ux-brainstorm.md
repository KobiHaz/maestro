# 🧠 Brainstorm: שיפור חוויית Scroll בטבלאות וב-Kanban

## Context

המשתמש צריך לבצע **המון scroll** במערכת — ימינה, שמאלה, למעלה ולמטה — במיוחד בטבלאות וב-Kanban. זו בעיית UX משמעותית שמשפיעה על יעילות העבודה.

### מצב נוכחי (ממצאי בדיקה)

**היררכיית Scroll:**
1. **DashboardLayout** — `main` עם `overflow-y-auto`, ו-div פנימי נוסף עם `overflow-y-auto` (כפילות)
2. **Kanban** — `overflow-x-auto` על הרשת (scroll אופקי); כל עמודה עם `overflow-y-auto` (scroll אנכי **per column**)
3. **טבלאות** — `overflow-x-auto` על ה-wrapper
4. **EntityPageShell** — `overflow-x-hidden` (חוסם scroll אופקי ברמת העמוד)

**בעיות מזוהות:**
- **Nested scroll** — scroll בתוך scroll (main → inner content → kanban column)
- **כפילות אנכית** — main ו-inner div שניהם scroll אנכי
- **Kanban** — scroll אופקי + scroll אנכי בכל עמודה
- **טבלאות** — scroll אופקי כשהטבלה רחבה
- **RTL** — ad-agency כבר מטפל ב-scrollLeft ל־0 אבל עדיין יש overflow-x-auto

**אימות בדפדפן (13.3.2026):**
- **Leads Pipeline** — כפתור Table דרש "Scrolled 1 nested container(s)" כדי לגשת
- **Leads Table** — scroll horizontal (256px) ו-vertical (179px) עבדו; scrollbar אופקי + אנכי נראים
- **Ad-agency Projects** — scrollbar אופקי + אנכי; עמודות Kanban (טיוטה, ממתין לאישור, תכנון...) — חלק חתוך

---

### Option A: Single Scroll — Single Source of Truth

**רעיון:** כל האזור הראשי הוא **scroll container אחד** — רק main או רק ה-content. אין scroll בתוך עמודות Kanban; הן מתרחבות לגובה התוכן.

**שינויים:**
- `main` — `overflow-y-auto` (אחד)
- הסרת `overflow-y-auto` מה-inner content div
- **EntityKanbanColumn** — הסרת `overflow-y-auto` מה-drop zone; `min-h` בלבד, ללא `max-h`
- Kanban grid — נשאר `overflow-x-auto` (אופקי)

✅ **Pros:**
- חוויית scroll אחת וברורה
- אין בלבול "איפה אני גולל"
- פשוט ליישם

❌ **Cons:**
- עמודות Kanban ארוכות מאוד = עמוד ארוך מאוד
- על mobile — scroll אנכי ארוך

📊 **Effort:** Low–Medium

---

### Option B: Full-Viewport Kanban + Sticky Columns

**רעיון:** Kanban תופס את כל ה-viewport (minus header) — `height: calc(100vh - header)`. scroll אופקי ברמת העמוד; scroll אנכי **רק** בתוך העמודות; header sticky.

**שינויים:**
- `main` — `overflow-y-auto` רק כשהתוכן לא Kanban
- EntityPageShell — כש־viewMode=kanban: `min-h-[calc(100vh-280px)]` או `h-[calc(100vh-280px)]` + `overflow-hidden` על העמוד
- Kanban grid — `overflow-x-auto` + `overflow-y-hidden` (כל העמודה גוללת)
- עמודות — `overflow-y-auto` + `flex-1` כדי למלא את הגובה

✅ **Pros:**
- Kanban מרגיש כמו "מסך מלא" — אין scroll כפול
- עמודות ברורות עם scroll עצמאי

❌ **Cons:**
- צריך לוגיקה שונה ל-kanban vs table
- על mobile — viewport קטן

📊 **Effort:** Medium

---

### Option C: Reduce Horizontal Scroll — Column Picker + Compact Tables

**רעיון:** פחות צורך ב-scroll אופקי — **הפחתת רוחב** במקום scroll.

**שינויים:**
- **טבלאות:** Column visibility (כבר קיים ב-Customers/Suppliers) — להרחיב לכל הטבלאות; עמודות ברירת מחדל מצומצמות
- **Kanban:** Column picker — להסתיר עמודות; להציג רק 3–5 עמודות ברירת מחדל
- **טבלאות:** Sticky first column — עמודה ראשונה צמודה
- **טבלאות:** `table-layout: fixed` + `text-overflow: ellipsis` — עמודות לא מתרחבות

✅ **Pros:**
- פחות scroll = פחות עומס
- משתמש בוחר מה לראות

❌ **Cons:**
- לא פותר scroll אנכי
- Column picker דורש UX

📊 **Effort:** Medium

---

### Option D: Hybrid — Scroll + Layout Fixes

**רעיון:** שילוב של A + B + C — תיקון layout + הפחתת scroll.

**שינויים:**
1. **Layout:** הסרת כפילות scroll (main vs inner content)
2. **Kanban:** Full-viewport כש־kanban (Option B)
3. **טבלאות:** Column visibility + sticky first column
4. **כללי:** `overscroll-behavior: contain` — scroll לא "דולף" בין containers

✅ **Pros:**
- פתרון מקיף
- מטפל בכל סוגי הבעיות

❌ **Cons:**
- יותר עבודה
- צריך לבדוק כל view

📊 **Effort:** High

---

## 💡 Recommendation

**Option D (Hybrid)** — כי הבעיה היא multi-faceted:
- scroll כפול (layout)
- scroll בתוך Kanban (UX)
- scroll אופקי בטבלאות (column visibility)

**פריוריטיזציה:**  
1. **Quick wins:** הסרת כפילות scroll ב-DashboardLayout + `overscroll-behavior: contain`  
2. **Kanban:** Full-viewport Kanban (Option B)  
3. **Tables:** Column visibility + sticky first column (Option C)

---

## Next Step (Handoff)

- **Ready to plan** → Invoke `/plan` + `project-planner` (אין `create-plan` נפרד)
- **Need deeper research** → explorer-agent for codebase discovery
