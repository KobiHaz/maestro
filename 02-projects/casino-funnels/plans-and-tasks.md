# casino-funnels — plans & tasks

מקור אמת לתכנון: [[PRD-clarity-insights-agent]] · מילון מדדים: נספח א׳ ב-PRD (גרסה `dictionary_version` בפרונט־מאטר).

**שותף (Crown Coins — affiliate):** [[plan-affiliate-crown-coins-rollout]] — קישורי UTM, דיסקליימר, גיאוגרפיה, יישור Clarity.

## פעולה הבאה

להפעיל **`/plan`** (`03-agents/workflows/plan.md`) עם הקישור ל-PRD כשמאשרים או מקפיאים החלטות מוצעות (סעיף 8).

---

## שלב 0 — לפני קוד (מוצר)

- [ ] לאשר **בעלים** בשדה Overview ב-PRD
- [ ] לאשר או לשנות **החלטות מוצעות** (פלט, MVP, שמירה)
- [ ] לסגור **שאלות וידוא** (LLM/DPA, consent)

---

## שלב 1 — MVP סוכן (ללא חובת LLM)

- [ ] סקריפט/Job: משיכת Data Export + כתיבת JSON עם חותמת זמן (לפי FR-1, FR-2)
- [ ] חילוץ מדדי חיכוך בסיסיים (סשנים, dead/rage/script errors לפי צורך) + טקסט סיכום קבוע (כללים)
- [ ] פלט לפי נספח ב׳ ב-PRD (`schema_version` 1)
- [ ] אחסון/ארטיפקט לפי ההחלטה בסעיף 8

---

## שלב 2 — התאמה למשפך האתר

- [ ] ליישר אירועי GA4 קיימים שמסומנים «מומלץ ל-Clarity» בנספח א׳ (`trackClarityEvent` / `setTag` לפי הצורך)
- [ ] להוסיף אירועים חסרים (`overlay_view`, `overlay_dismiss` אם רלוונטי)
- [ ] לעדכן גרסת מילון ב-PRD ובפלט הסוכן
- [ ] (אם טראפיק עובר דרך הלנדר שלך) לשמר/להעביר `utm_*`, `landing`, `click_id` עד ליעד — ראו [[plan-affiliate-crown-coins-rollout]] סעיף 2.2

---

## שלב 3 — עומק

- [ ] שכבת LLM על אותו קלט + פרומפט «השערות בלבד»
- [ ] (אופציונלי) Clarity MCP לצוות — תיעוד הרצה מקומית
- [ ] השוואות היסטוריות (שבוע־לשבוע) כשיש מאגר צילומים

---

## משימות מפורטות אחרי תכנון

_(יפורקו על ידי **`/plan`** / `03-agents/workflows/plan.md` (`project-planner`) לקובץ תכנון ב-`docs/plans/` או כאן.)_
