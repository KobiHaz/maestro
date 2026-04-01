# Consul House - Leads | התקנה והגדרה

## 1. יצירת הגיליון ב-Google Sheets

### צעד 1.1: גיליון Consul House - Leads

**גיליון קיים:** [Consul House - Leads](https://docs.google.com/spreadsheets/d/1LfgZnvc_s6E-D7Io0a2Pc7J3mBid0DSiIfAyfHSnWcM/edit)  
**Spreadsheet ID:** `1LfgZnvc_s6E-D7Io0a2Pc7J3mBid0DSiIfAyfHSnWcM`

אם צריך ליצור גיליון חדש:
1. היכנס ל-[Google Sheets](https://sheets.google.com)
2. לחץ **Blank** (או **+** ליצירת גיליון ריק)
3. שנה את שם הגיליון ל-**Consul House - Leads**

### צעד 1.2: מבנה Tab "Registry"

1. הטאב הראשון כבר קיים – שנה את שמו ל-**Registry**
2. בשורה 1 הזן את כותרות העמודות:

| A | B | C | D | E | F | G | H | I | J | K | L | M |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| First Name | Last Name | Phone | Email | Event Type | Guests | Notes | Created At | Status | Retry | Updated At | Source | iPlan Lead Id |

**מקורות לידים:** אתר, אינסטגרם, פייסבוק

**ערכי Status:** `pending` | `sent` | `duplicate` | `failed`

**Retry:** מספר ניסיונות (0, 1, 2...)

**התראות מייל:** kobi@leadslords.com

### צעד 1.3: יצירת Tab "Audit Log"

1. בתחתית – **+** (או לחיצה ימנית על הטאב → **Insert sheet**)
2. שנה את שם הטאב ל-**Audit Log**
3. בשורה 1 הזן:

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| timestamp | run_id | email | phone | source | decision | reason | metadata |

### ערכי decision (לשימוש ב-Make)

- `sent` – ליד חדש נשלח בהצלחה
- `duplicate` – ליד כפול (נמצא ב-Registry)
- `fetch_failed` – כשל בקבלת הנתונים
- `validation_failed` – אימייל/טלפון חסר או לא תקין
- `api_error` – כשל בקריאה ל-iPlan API

---

## 2. הגדרת MCP ל-Google Sheets (mcp-gsheets)

### דרישות מוקדמות

- חשבון Google Cloud
- [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com) מופעל
- Service Account עם מפתח JSON

### צעד 2.1: יצירת Service Account

1. היכנס ל-[Google Cloud Console](https://console.cloud.google.com)
2. בחר פרויקט (למשל `democrm-489100`) או צור פרויקט חדש
3. **APIs & Services** → **Library** → חפש **Google Sheets API** → **Enable**
4. **APIs & Services** → **Credentials** → **Create Credentials** → **Service Account**
5. תן שם (למשל `consul-house-sheets`)
6. **Keys** → **Add Key** → **Create new key** → **JSON** → הורד את הקובץ

### צעד 2.2: שיתוף הגיליון עם ה-Service Account

1. פתח את קובץ ה-JSON – העתק את הערך של `client_email`
2. פתח את הגיליון **Consul House - Leads**
3. **Share** → הוסף את ה-`client_email` עם הרשאות **Editor**

### צעד 2.3: הגדרת Cursor

קובץ ה-MCP כבר מוגדר ב-`~/.cursor/mcp.json`. עדכן את הנתיב לקובץ ה-Service Account:

```json
"mcp-gsheets": {
  "command": "npx",
  "args": ["-y", "mcp-gsheets@latest"],
  "env": {
    "GOOGLE_PROJECT_ID": "democrm-489100",
    "GOOGLE_APPLICATION_CREDENTIALS": "/absolute/path/to/your-service-account-key.json"
  }
}
```

החלף את `/absolute/path/to/your-service-account-key.json` בנתיב המלא לקובץ ה-JSON שהורדת.

### צעד 2.4: הפעלה מחדש

- הפעל מחדש את Cursor או **Reload MCP** דרך ההגדרות

---

## 3. בדיקה

אחרי חיבור ה-MCP:

1. פתח צ'אט ב-Cursor
2. בקש מה-AI: "קרא את הגיליון Consul House - Leads"
3. אם אין שגיאות – החיבור תקין

---

## קישורים שימושיים

| פריט | קישור |
|------|--------|
| יצירת גיליון חדש | https://docs.google.com/spreadsheets/create |
| Google Cloud Console | https://console.cloud.google.com |
| Google Sheets API | https://console.cloud.google.com/apis/library/sheets.googleapis.com |

---

## צעד הבא

לאחר יצירת הגיליון והגדרת MCP:
- הגדרת Scenarios ב-Make
- חיבור ל-iPlan API
