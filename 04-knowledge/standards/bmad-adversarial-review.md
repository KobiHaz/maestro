# BMAD Adversarial Review — Reference

מקור: [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD), [docs.bmad-method.org](https://docs.bmad-method.org/explanation/adversarial-review/)

## עיקרון מרכזי

**חובה למצוא ממצאים.** אין "נראה טוב". המבקר מאמץ עמדה סקפטית — מניח שיש בעיות ומחפש אותן.

## למה זה עובד

- **הטיית אישור** — בלי המנדט "מצא בעיות" קל לאשר מהר מדי
- **א-asymmetry מידע** — הרצה עם הקשר רענן (ללא גישה להנמקה המקורית)
- **ממצאים ספציפיים** — לא דאגות מעורפלות
- **מחפש חסר** — "מה לא כאן?" הופך לשאלה טבעית

## כלל אפס ממצאים

**אפס ממצאים → לעצור.** לבדוק שוב או להסביר למה אין בעיות.

## סינון אנושי

המערכת מניחה שיש בעיות ולכן תמצא — כולל false positives. המשתמש מחליט מה אמיתי.

## דוגמה

במקום: "האימות נראה סביר. מאושר."

ב-adversarial review:
1. LOW — Magic number `3600` → `SESSION_TIMEOUT_SECONDS`
2. MEDIUM — אין audit log לכישלונות login
3. MEDIUM — ולידציית סיסמה רק client-side
4. HIGH — Session token ב-localStorage (XSS)
5. HIGH — אין rate limiting על login כושל

## שימוש ב-Maestro

Workflow: `03-agents/workflows/review.md` מיישם adversarial review.
