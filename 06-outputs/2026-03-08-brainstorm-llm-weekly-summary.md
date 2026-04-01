# 🧠 Brainstorm: הוספת ניתוח LLM לסיכום השבועי

### Context

**בעיה:** סיכום Setup מלא השבועי (`weekly-setup-evaluation`) שולח כיום טבלת נתונים בלבד (TICKER | תאריך | מחיר אז | מחיר עכשיו | Δ% | ימים) בלי פרשנות אנליטית.

**משתמש:** משקיע שמקבל את הסיכום ב‑Telegram בימי ראשון.

**אילוצים:**
- Workflow רץ ב‑GitHub Actions (אין secrets של LLM ב־weekly-setup-evaluation כרגע)
- יש כבר `llmSummary.ts` עם OpenAI/Gemini/Perplexity/Groq
- טבלה בעברית; LLM צריך לקבל הקשר ברור

---

### Option A: הרחבה של llmSummary + שילוב ב־evaluate-setups.ts

הוספת פונקציה `getWeeklyLlmCommentary(rows, avgChange, total)` ב־`llmSummary.ts`. ה־script קורא לה אחרי בניית הטבלה, מקבל 2–3 משפטי פרשנות, ומדביק לפני/אחרי ההודעה. ה‑workflow מקבל את כל הפלט (טבלה + LLM) כרגיל.

✅ **Pros:**
- שימוש חוזר בתשתית LLM הקיימת (providers, config, API keys)
- לוגיקה אחת, בדיקות יחידה במקום אחד
- פלט אחיד לקובץ אחד

❌ **Cons:**
- `evaluate-setups` יהפוך תלוי ב־llmSummary (כבר תלוי ב־marketData)
- צריך להעביר API keys ל‑workflow (GEMINI_API_KEY וכו') – כרגע אין

📊 **Effort:** Medium

---

### Option B: Script נפרד לניתוח LLM + שליחה בשתי הודעות

Script חדש `scripts/weekly-llm-commentary.ts` שמקבל את `eval_output.txt`, שולח לטבלה ל‑LLM, מחזיר פרשנות. ה‑workflow:
1. מריץ `evaluate-setups` → eval_output.txt
2. מריץ `weekly-llm-commentary` → commentary.txt
3. שולח שתי הודעות ל‑Telegram: טבלה, ואז פרשנות

✅ **Pros:**
- הפרדה ברורה: evaluation = נתונים, commentary = פרשנות
- טבלה נשארת גם אם LLM נכשל
- אפשר לכבות LLM בקלות (דילוג על צעד 2–3)

❌ **Cons:**
- שתי הודעות Telegram – פחות זרימה
- קוד כפול (קריאות API) אלא אם משתפים מודול

📊 **Effort:** Medium–High

---

### Option C: LLM בתוך Workflow (curl / script מינימלי)

בלי שינוי ב־`evaluate-setups.ts`. הוספת step ב‑workflow:
- קורא את eval_output.txt
- שולח ל‑API (curl ל‑OpenAI/Gemini) עם prompt קבוע
- מדביק את התשובה להודעה ושולח

✅ **Pros:**
- אין שינוי ב־TypeScript
- מהיר ליישם

❌ **Cons:**
- לוגיקה ב‑YAML/Shell – קשה לתחזוקה
- צריך לטפל ב‑ escaping, limit 4096 של Telegram
- לא משתמש ב־`llmSummary` הקיים

📊 **Effort:** Low–Medium

---

### Option D: LLM אופציונלי – flag + config

הוספת `ENABLE_LLM_WEEKLY_SUMMARY` (default: false). כש‑true – `evaluate-setups` קורא ל־`getWeeklyLlmCommentary` ומדביק. ה‑workflow מעביר `GEMINI_API_KEY` ו־`ENABLE_LLM_WEEKLY_SUMMARY=true` רק כש־secret קיים.

✅ **Pros:**
- לא שובר משתמשים בלי API key
- אפשר להפעיל/ לכבות בלי deployment

❌ **Cons:**
- עוד משתנה config
- צריך לעדכן README ו־.env.example

📊 **Effort:** Medium

---

## 💡 Recommendation

**Option A + D** (שילוב):  
הוספת `getWeeklyLlmCommentary` ב־`llmSummary.ts`, וקריאה אופציונלית מתוך `evaluate-setups.ts` לפי `ENABLE_LLM_WEEKLY_SUMMARY`.  
ה‑workflow יעביר `GEMINI_API_KEY` (או provider אחר) ו־`ENABLE_LLM_WEEKLY_SUMMARY=true` כשארוצים פרשנות.

**נימוק:**
1. שימוש חוזר בתשתית הקיימת
2. אופציונליות – לא חובה לריצות בלי API key
3. הודעה אחת – חוויית קריאה רציפה
4. fallback: אם LLM נכשל, נשלחת רק הטבלה (כמו היום)

---

## צעדי יישום מוצעים

1. להוסיף `getWeeklyLlmCommentary(rows, avgChange, total)` ב־`llmSummary.ts` עם prompt מותאם
2. לעדכן `evaluate-setups.ts`: לקרוא לפונקציה (אם `ENABLE_LLM_WEEKLY_SUMMARY=true` ו־API key קיים), להדביק פרשנות בתחילת ההודעה
3. לעדכן `weekly-setup-evaluation.yml`: להעביר `GEMINI_API_KEY`, `ENABLE_LLM_WEEKLY_SUMMARY`, `LLM_PROVIDER`
4. לעדכן `.env.example` ו־README

מה הכיוון המועדף עליך?

---

## ✅ יושם (2026-03-08)

אופציה A+D: הוספת `getWeeklyLlmCommentary` ב־`llmSummary.ts`, קריאה מ־`evaluate-setups.ts`, flag `ENABLE_LLM_WEEKLY_SUMMARY`. ה־workflow מעביר GEMINI_API_KEY ו־LLM_PROVIDER.
