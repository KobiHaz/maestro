# מדריך בניית Scenarios ב-Make – Consul House Leads

## מבנה כללי

```
3 Scenarios טריגר (אתר | פייסבוק | אינסטגרם)
        ↓
   Run Scenario
        ↓
1 Scenario ראשי "Leads to iPlan - Main Logic" (On-Demand)
```

---

## תכונות לפני שמתחילים

- [ ] גיליון **Consul House - Leads** (Registry + Audit Log)  
  URL: https://docs.google.com/spreadsheets/d/1LfgZnvc_s6E-D7Io0a2Pc7J3mBid0DSiIfAyfHSnWcM/edit
- [ ] חיבור **Google Sheets** ב-Make
- [ ] חיבור **Gmail** (או Email) ל-kobi@leadslords.com
- [ ] **form_id** מ-iPlan (אם עדיין לא – השאר placeholder)
- [ ] **API key** חדש ל-iPlan (הישן נחשף)

---

# Scenario 1: Leads to iPlan - Main Logic (ראשי)

**Schedule:** On-Demand

## 1.1 Inputs של ה-Scenario

**Scenario settings** → **Inputs** → הוסף:

| Name       | Type  | Default    | Description                |
|-----------|-------|------------|----------------------------|
| first_name| Text  | -          | שם פרטי                    |
| last_name | Text  | -          | שם משפחה                   |
| email     | Text  | -          | אימייל                     |
| phone     | Text  | -          | טלפון                      |
| event_type| Text  | -          | סוג אירוע                  |
| guests    | Text  | -          | מספר מוזמנים               |
| notes     | Text  | -          | הערות                      |
| source    | Text  | website    | website / instagram / facebook |

## 1.2 מודולים – סדר הביצוע

### מודול 1: Tools → Set Variable

**נרמול שדות:**
- `email_norm` = `lower(trim({{1.email}}))`
- `phone_norm` = `replace(trim({{1.phone}}); " "; "")`
- `full_name` = `trim({{1.first_name}} & " " & {{1.last_name}})`
- `request_content` = `trim({{1.notes}} & " | Event: " & {{1.event_type}} & " | Guests: " & {{1.guests}})`

### מודול 2: Router (Flow control)

**מטרה:** לשלוח ל-duplicate / new / validation_failed

**תנאי Route 1 – validation_failed:**
- `{{email_norm}}` equals `` (ריק) **AND**
- `{{phone_norm}}` equals `` (ריק)

**תנאי Route 2 – להמשיך (new או duplicate):**
- אחרת (או: NOT Route 1)

---

### Route 1 (validation_failed)

#### מודול 1a: Google Sheets → Add a row

**Spreadsheet:** Consul House - Leads  
**Sheet:** Audit Log  

| Column   | Value                                   |
|----------|-----------------------------------------|
| timestamp| `{{formatDate(now; "YYYY-MM-DDTHH:mm:ss")}}` |
| run_id   | `{{runId}}`                             |
| email    | `{{1.email}}`                           |
| phone    | `{{1.phone}}`                           |
| source   | `{{1.source}}`                          |
| decision | `validation_failed`                     |
| reason   | `missing_email_and_phone`               |
| metadata | -                                       |

*(בהתאם לשמות העמודות בפועל בגיליון)*

---

### Route 2 (new או duplicate)

#### מודול 2a: Google Sheets → Search Rows

**Spreadsheet:** Consul House - Leads  
**Sheet:** Registry  
**Filter:** `Email` equals `{{email_norm}}`  

*(הפעל רק כאשר `email_norm` לא ריק. אם Make לא מאפשר – השאר ריק ובדוק במקום אחר)*

#### מודול 2b: Google Sheets → Search Rows

**Spreadsheet:** Consul House - Leads  
**Sheet:** Registry  
**Filter:** `Phone` equals `{{phone_norm}}`

**גישה פשוטה לכפילויות:** הרץ **חיפוש אחד** – לפי Email אם קיים, אחרת לפי Phone. ב-Router: אם Search מחזיר **0 פריטים** → new. אם **≥1** → duplicate.  
אם צריך OR (גם Email וגם Phone): הרץ שני חיפושים; ב-Router – duplicate אם **אחד מהם** החזיר תוצאות.

#### מודול 2c: Router – Duplicate vs New

**תנאי Route A (duplicate):**  
מספר התוצאות מ-Search Rows > 0 (או: `{{2a.array}}` לא ריק – לפי שמות השדות ב-Make).

**תנאי Route B (new):**  
מספר התוצאות = 0.

**טיפ Make:** אם Search Rows מחזיר 0 שורות, ה-scenario עשוי לא להעביר bundle הלאה. השתמש ב־**Settings** של Search Rows: "Allow empty output" / "Continue even if no results" – אם זמין. אחרת: הוסף **Flow control → Resume** שרץ גם כשאין תוצאות.

---

### Route A (duplicate)

#### מודול A1: Gmail → Send an email

- **To:** kobi@leadslords.com
- **Subject:** `ליד כפול – Consul House | {{email_norm}}`
- **Content:**  
  `ליד כפול זוהה. אימייל: {{email_norm}}, טלפון: {{phone_norm}}, מקור: {{1.source}}`

#### מודול A2: Google Sheets → Add a row

**Sheet:** Audit Log  

| Column   | Value               |
|----------|---------------------|
| timestamp| `{{formatDate(now; ...)}}` |
| run_id   | `{{runId}}`         |
| email    | `{{email_norm}}`    |
| phone    | `{{phone_norm}}`    |
| source   | `{{1.source}}`      |
| decision | `duplicate`         |
| reason   | `found_in_registry` |
| metadata | -                   |

---

### Route B (new – שליחה ל-iPlan)

#### מודול B1: HTTP → Make a request

- **URL:** `https://iplan.co.il/he-IL/api/corp/leads.json`
- **Method:** POST
- **Headers:**  
  `Content-Type`: `application/json`
- **Body type:** Raw / JSON

**Body:**
```json
{
  "api_key": "YOUR_NEW_API_KEY",
  "form_id": "YOUR_FORM_ID",
  "contact_full_name": "{{full_name}}",
  "contact_email": "{{email_norm}}",
  "contact_phone": "{{phone_norm}}",
  "request_content": "{{request_content}}",
  "request_matter": "{{1.event_type}}"
}
```

החלף `YOUR_NEW_API_KEY` ו-`YOUR_FORM_ID` בערכים האמיתיים.

#### Error Handler על HTTP

במקרה שגיאה:

1. **Google Sheets → Add a row** (Audit Log):
   - decision: `api_error`
   - reason: `{{3.error}}` או טקסט השגיאה

2. **Gmail → Send an email**:
   - To: kobi@leadslords.com
   - Subject: `כשל iPlan – Consul House | {{email_norm}}`
   - Content: `שגיאת API: {{3.error}}`

#### מודול B2 (אחרי HTTP מוצלח): Google Sheets → Add a row

**Sheet:** Registry  

| Column      | Value |
|-------------|-------|
| First Name  | `{{1.first_name}}` |
| Last Name   | `{{1.last_name}}` |
| Phone       | `{{1.phone}}` |
| Email       | `{{email_norm}}` |
| Event Type  | `{{1.event_type}}` |
| Guests      | `{{1.guests}}` |
| Notes       | `{{1.notes}}` |
| Created At  | `{{formatDate(now; ...)}}` |
| Status      | `sent` |
| Retry       | `0` |
| Updated At  | `{{formatDate(now; ...)}}` |
| Source      | `{{1.source}}` |
| iPlan Lead Id | `{{3.id}}` או השדה שמחזיר iPlan |

*(התאם את `{{3.xxx}}` לפי מבנה תגובת iPlan)*

#### מודול B3: Google Sheets → Add a row (Audit Log)

- decision: `sent`
- reason: `success`
- metadata: `iplan_id={{3.id}}` (או דומה)

#### הגדרת Reconnect ב-HTTP

ב־HTTP module: **Reconnect** – 3 ניסיונות, מרווח 5 שניות.

---

# Scenario 2: Website Leads (טריגר)

**Schedule:** Instant (Webhooks)

## 2.1 Webhook URL

```
https://hook.eu1.make.com/8km72qkfd5ydtvjyyh1pmdhh9nlb7c26
```

**הטמעה באתר/מקור:** השליחה צריכה להיות:
- **Method:** POST
- **Content-Type:** application/json
- **Headers:** `x-make-apikey: gzQiCaQ4f6r-nEg` (אם הוגדר)
- **Body:** שדות `first_name`, `last_name`, `email`, `phone`, `event_type`, `guests`, `notes`, **`source`** (`website` | `facebook` | `instagram`)

## 2.2 מודולים

### מודול 1: Webhooks → Custom webhook

- Make יוצר את ה-URL – השתמש בו בטופס האתר

### מודול 2: Make → Run a scenario

- **Scenario:** Leads to iPlan - Main Logic
- **Mapping:**

| Input     | Source                      |
|-----------|-----------------------------|
| first_name| `{{1.first_name}}` או לפי שדה מהטופס |
| last_name | `{{1.last_name}}`           |
| email     | `{{1.email}}`               |
| phone     | `{{1.phone}}`               |
| event_type| `{{1.event_type}}`          |
| guests    | `{{1.guests}}`              |
| notes     | `{{1.notes}}`               |
| source    | `{{1.source}}`              |

**`source`** מתקבל מהבקשה – יש לשלוח `website`, `facebook` או `instagram` לפי מקור הליד. התאם את השמות לשדות שהטופס/מקור שולח ל־Webhook.

---

# Scenario 3: Facebook Lead Ads (טריגר)

**Schedule:** Instant

### מודול 1: Facebook Lead Ads → Watch Lead Ad Forms

- התחברות ל-Facebook
- בחירת טופס / דף

### מודול 2: Make → Run a scenario

- **Scenario:** Leads to iPlan - Main Logic
- **Mapping:** map שדות מ-Facebook ל-inputs, כולל `source` = `facebook`

---

# Scenario 4: Instagram (טריגר)

**Schedule:** Instant (או Webhook אם דרך כלי חיצוני)

אם יש מודול Instagram ללידים – אותו מבנה כמו Facebook.  
אם הלידים מגיעים דרך ManyChat/דומיו – Webhook שמקבל JSON ומעביר ל־Run scenario עם `source` = `instagram`.

---

# בדיקה ראשונית

1. הפעל **Run once** על Scenario הראשי עם:
   - first_name: Test  
   - last_name: User  
   - email: test@example.com  
   - phone: 0501234567  
   - source: website  

2. וודא:
   - רשומה ב-Registry
   - רשומה ב-Audit Log עם decision=sent
   - ליד ב-iPlan (אם ה-API מוגדר נכון)

3. הריץ שוב עם אותו אימייל – אמור לקבל duplicate ומייל.

---

# צעדים עוקבים (לאחר שהזרימה עובדת)

- הוספת Scenario לסיכום שבועי (Schedule – כל חמישי)
- Scenario לבדיקת לידים תקועים (יומי)
- חיבור Make MCP ל-Cursor (להרצה ידנית ודיבוג)

---

## רפרנס מהיר

| פריט          | ערך                   |
|---------------|------------------------|
| iPlan endpoint| `https://iplan.co.il/he-IL/api/corp/leads.json` |
| מייל התראות   | kobi@leadslords.com   |
| Status values | pending, sent, duplicate, failed |
| Source values | website, instagram, facebook |
