# תהליך הקמה ב-Make – Consul House Leads

## סקירה כללית

| שלב | תיאור | זמן משוער |
|-----|--------|------------|
| 0 | הכנה לפני Make | 10 דק׳ |
| 1 | Scenario ראשי – לוגיקה משותפת | 45 דק׳ |
| 2 | Scenario Website – Webhook | 15 דק׳ |
| 3 | Scenarios פייסבוק ואינסטגרם | 20 דק׳ |
| 4 | בדיקות ותחזוקה | 15 דק׳ |

---

## שלב 0: הכנה לפני Make

### 0.1 גיליון Google Sheets "Consul House - Leads"

**URL:** https://docs.google.com/spreadsheets/d/1LfgZnvc_s6E-D7Io0a2Pc7J3mBid0DSiIfAyfHSnWcM/edit  
**Spreadsheet ID:** `1LfgZnvc_s6E-D7Io0a2Pc7J3mBid0DSiIfAyfHSnWcM`

**טאב Registry:**
| First Name | Last Name | Phone | Email | Event Type | Guests | Notes | Created At | Status | Retry | Updated At | Source | iPlan Lead Id |

**טאב Audit Log:**
| timestamp | run_id | email | phone | source | decision | reason | metadata |

### 0.2 חיבורים ב-Make

1. **Settings** → **Connections**
2. הוסף:
   - **Google Sheets** – התחברות לחשבון הגוגל
   - **Gmail** – התחברות (להתראות ל-kobi@leadslords.com)
3. **HTTP** – לא דורש connection (משתמש ב-module ישירות)

### 0.3 פרטים ל-iPlan

- **api_key** – מפתח API חדש (לא הישן שנחשף)
- **form_id** – מזהה הטופס מ-iPlan

---

## שלב 1: Scenario "Leads to iPlan - Main Logic"

### 1.1 יצירת Scenario

1. **Create a new scenario**
2. שם: `Leads to iPlan - Main Logic`
3. **Schedule** → בחר **On-demand** (אייקון שעון עם יד)

### 1.2 הגדרת Inputs

1. לחץ על שם ה-Scenario למעלה
2. **Scenario settings** → **Inputs** → **Add input**
3. הוסף:

| Name | Type | Default | Required |
|------|------|---------|----------|
| first_name | Text | - | no |
| last_name | Text | - | no |
| email | Text | - | no |
| phone | Text | - | no |
| event_type | Text | - | no |
| guests | Text | - | no |
| notes | Text | - | no |
| source | Text | website | no |

### 1.3 מודול 1: Set Variable (Tools)

1. **+** → **Tools** → **Set variable**
2. הוסף משתנים:

| Variable | Formula |
|----------|---------|
| email_norm | `lower(trim(1.email))` |
| phone_norm | `replace(trim(1.phone); " "; "")` |
| full_name | `trim(1.first_name & " " & 1.last_name)` |
| request_content | `trim(1.notes & " \| Event: " & 1.event_type & " \| Guests: " & 1.guests)` |

*שים לב: ב-Make המספר 1 מתייחס ל-Trigger/Input. התאם לפי המספור בפועל.*

### 1.4 מודול 2: Router (Flow control)

1. **+** → **Flow control** → **Router**
2. **Route 1 – validation_failed:**
   - Filter: `2.email_norm` is empty **AND** `2.phone_norm` is empty
3. **Route 2 – להמשיך:**
   - Filter: Else (או: Not Route 1)

---

### 1.5 Route 1 (validation_failed)

**מודול 1a: Google Sheets → Add a row**
- Spreadsheet: Consul House - Leads
- Sheet: Audit Log
- Map: timestamp, run_id, email, phone, source, decision=`validation_failed`, reason=`missing_email_and_phone`

---

### 1.6 Route 2 (new/duplicate)

**מודול 2a: Google Sheets → Search rows**
- Spreadsheet: Consul House - Leads
- Sheet: Registry
- Search: Email = `{{2.email_norm}}` (או Phone אם email ריק)
- Max rows: 1

**מודול 2b: Router – Duplicate vs New**
- **Route A (duplicate):** `2a` מחזיר ≥1 שורה
- **Route B (new):** `2a` מחזיר 0 שורות

*הערה: אם Search מחזיר 0, Make עשוי לא להעביר bundle. השתמש ב-"Resume" או "Allow empty" אם זמין.*

---

### 1.7 Route A (duplicate)

**מודול A1: Gmail → Send an email**
- To: kobi@leadslords.com
- Subject: `ליד כפול – Consul House | {{2.email_norm}}`
- Content: `ליד כפול. אימייל: {{2.email_norm}}, טלפון: {{2.phone_norm}}, מקור: {{1.source}}`

**מודול A2: Google Sheets → Add a row (Audit Log)**
- decision=`duplicate`, reason=`found_in_registry`

---

### 1.8 Route B (new – שליחה ל-iPlan)

**מודול B1: HTTP → Make a request**
- URL: `https://iplan.co.il/he-IL/api/corp/leads.json`
- Method: POST
- Headers: `Content-Type: application/json`
- Body type: JSON
- Body:
```json
{
  "api_key": "YOUR_API_KEY",
  "form_id": "YOUR_FORM_ID",
  "contact_full_name": "{{2.full_name}}",
  "contact_email": "{{2.email_norm}}",
  "contact_phone": "{{2.phone_norm}}",
  "request_content": "{{2.request_content}}",
  "request_matter": "{{1.event_type}}"
}
```

**Error Handler** על HTTP:
- Add row ל-Audit Log: decision=`api_error`, reason=טקסט השגיאה
- Send email: kobi@leadslords.com, נושא "כשל iPlan"

**מודול B2: Google Sheets → Add a row (Registry)**
- כל השדות לפי מבנה Registry
- Status=`sent`, Retry=`0`
- iPlan Lead Id = השדה מתגובת iPlan

**מודול B3: Google Sheets → Add a row (Audit Log)**
- decision=`sent`, reason=`success`

**HTTP → Reconnect:** 3 ניסיונות, 5 שניות

### 1.9 שמירה ובדיקה

1. **Save**
2. **Run once** – הזן נתוני בדיקה
3. בדוק Registry, Audit Log, iPlan

---

## שלב 2: Scenario "Website Leads"

### 2.1 יצירת Scenario

1. **Create a new scenario**
2. שם: `Website Leads`
3. **Schedule** → **Instant** (Webhooks)

### 2.2 מודול 1: Webhooks → Custom webhook

1. **+** → **Webhooks** → **Custom webhook**
2. **Add** – Make יוצר URL
3. **API key** (אופציונלי): הוסף key לאבטחה – ישלח עם header `x-make-apikey`
4. העתק את ה-URL

### 2.3 מודול 2: Make → Run a scenario

1. **+** → **Make** → **Run a scenario**
2. **Scenario:** Leads to iPlan - Main Logic
3. **Mapping:**

| Input | Map from |
|-------|----------|
| first_name | `1.first_name` |
| last_name | `1.last_name` |
| email | `1.email` |
| phone | `1.phone` |
| event_type | `1.event_type` |
| guests | `1.guests` |
| notes | `1.notes` |
| source | `1.source` |

**חשוב:** ה־Webhook מקבל `source` מהבקשה – `website` / `facebook` / `instagram`. כל מקור (אתר, פייסבוק, אינסטגרם) שולח את הערך המתאים.

*התאם שמות לשדות שהטופס שולח.*

### 2.4 הפעלה

1. **Save**
2. **ON** – הפעל את ה-Scenario

### 2.5 הטמעה באתר

שלח POST ל-Webhook URL:
- **Headers:** `Content-Type: application/json`, `x-make-apikey: YOUR_KEY`
- **Body:** JSON עם first_name, last_name, email, phone, event_type, guests, notes, **source** (`website` / `facebook` / `instagram`)

---

## שלב 3: Scenarios פייסבוק ואינסטגרם

### 3.1 Facebook Lead Ads

1. **Create scenario** → **Instant**
2. מודול 1: **Facebook Lead Ads** → **Watch Lead Ad Forms**
3. מודול 2: **Make** → **Run a scenario** → Leads to iPlan - Main Logic
4. Mapping: שדות Facebook → inputs, source=`facebook`

### 3.2 Instagram

- אם יש מודול Instagram ללידים: כמו Facebook
- אם דרך ManyChat/כלי אחר: Webhook נוסף עם source=`instagram`

---

## שלב 4: בדיקות

### 4.1 בדיקה ידנית

```
Run once על Scenario הראשי:
first_name=Test, last_name=User, email=test@example.com, phone=0501234567, source=website
```

### 4.2 בדיקת Webhook

```bash
curl -X POST "https://hook.eu1.make.com/YOUR_WEBHOOK_ID" \
  -H "Content-Type: application/json" \
  -H "x-make-apikey: YOUR_KEY" \
  -d '{"first_name":"Test","last_name":"User","email":"test@example.com","phone":"0501234567","event_type":"Wedding","guests":"20","notes":"בדיקה","source":"website"}'
```

### 4.3 בדיקת duplicate

הרץ פעמיים עם אותו email – בפעם השנייה: מייל "ליד כפול" + Audit Log.

---

## סיכום מודולים

```
[Trigger/Input]
       ↓
[Set Variable] → email_norm, phone_norm, full_name, request_content
       ↓
[Router] → validation_failed? | continue?
       ↓
[Search Rows] Registry (Email או Phone)
       ↓
[Router] → duplicate? | new?
       ↓                    ↓
[Email + Audit]        [HTTP → iPlan]
                              ↓
                        [Registry + Audit]
```

---

## רפרנס

| פריט | ערך |
|------|-----|
| Webhook URL | https://hook.eu1.make.com/8km72qkfd5ydtvjyyh1pmdhh9nlb7c26 |
| iPlan endpoint | https://iplan.co.il/he-IL/api/corp/leads.json |
| מייל התראות | kobi@leadslords.com |
| Spreadsheet | Consul House - Leads (Registry + Audit Log) |
