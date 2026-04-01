# Consul House - Leads | Spec מלא

## גיליון Google Sheets

**URL:** https://docs.google.com/spreadsheets/d/1LfgZnvc_s6E-D7Io0a2Pc7J3mBid0DSiIfAyfHSnWcM/edit  
**Spreadsheet ID:** `1LfgZnvc_s6E-D7Io0a2Pc7J3mBid0DSiIfAyfHSnWcM`  
**Registry (gid):** 726075457

---

## מקורות לידים

| מקור | Make Trigger |
|------|--------------|
| אתר אינטרנט | Webhook |
| פייסבוק | Facebook Lead Ads |
| אינסטגרם | Instagram (או Webhook אם דרך כלי צד שלישי) |

### Webhook URL (אתר)

```
https://hook.eu1.make.com/8km72qkfd5ydtvjyyh1pmdhh9nlb7c26
```

**שליחה מטופס האתר / פייסבוק / אינסטגרם:** POST, `Content-Type: application/json`, Body:
```json
{
  "first_name": "...",
  "last_name": "...",
  "email": "...",
  "phone": "...",
  "event_type": "...",
  "guests": "...",
  "notes": "...",
  "source": "website"
}
```

**`source`** – ערכים: `website` | `facebook` | `instagram` (חובה – מציין את מקור הליד).

---

## מבנה Registry (גיליון Consul House - Leads)

| עמודה | תיאור |
|-------|--------|
| First Name | שם פרטי |
| Last Name | שם משפחה |
| Phone | טלפון |
| Email | אימייל |
| Event Type | סוג האירוע |
| Guests | מספר מוזמנים |
| Notes | הערות |
| Created At | תאריך יצירה |
| Status | `pending` \| `sent` \| `duplicate` \| `failed` |
| Retry | מספר ניסיונות שליחה (0, 1, 2...) |
| Updated At | תאריך עדכון אחרון |
| Source | `website` \| `instagram` \| `facebook` |
| iPlan Lead Id | מזהה הליד ב-iPlan (אחרי שליחה מוצלחת) |

---

## בדיקת כפילויות

- **לוגיקה:** חיפוש ב-Registry לפי **Email** או **Phone**
- **אם נמצא** → `Status=duplicate`, שליחת מייל התראה
- **אם לא נמצא** → המשך לשליחה ל-iPlan

---

## מיפוי ל-iPlan API

| Registry | iPlan API Field |
|----------|-----------------|
| First Name + Last Name | `contact_full_name` |
| Email | `contact_email` |
| Phone | `contact_phone` |
| Notes + Event Type + Guests | `request_content` או `request_matter` |
| - | `api_key` (מהגדרות) |
| - | `form_id` **(לבדיקה)** |

**Endpoint:** `https://iplan.co.il/he-IL/api/corp/leads.json`  
**Method:** POST  
**Headers:** `Content-Type: application/json`

---

## התראות

| אירוע | פעולה |
|-------|--------|
| ליד כפול | מייל ל־kobi@leadslords.com |
| כשל API (iPlan) | מייל ל־kobi@leadslords.com |
| validation_failed | (אופציונלי) מייל |

---

## Audit Log

`decision`: `sent` | `duplicate` | `validation_failed` | `api_error` | `fetch_failed`

---

## Webhook (אתר אינטרנט)

**URL:** `https://hook.eu1.make.com/8km72qkfd5ydtvjyyh1pmdhh9nlb7c26`

**Method:** POST  
**Content-Type:** `application/json`

**דוגמת Body:**
```json
{
  "first_name": "ישראל",
  "last_name": "ישראלי",
  "email": "test@example.com",
  "phone": "0501234567",
  "event_type": "Wedding",
  "guests": "50",
  "notes": "הערות",
  "source": "website"
}
```

**שדה `source` (חובה):** `website` | `facebook` | `instagram` – מקור הליד.

**הטמעה:** שליחת POST ל-URL עם JSON מלא. אתר/פייסבוק/אינסטגרם ישלחו `source` בהתאם. ב-Make: מיפוי `{{1.source}}` ל-Input של Main Logic.

---

## תלויות לביצוע

- [ ] אימות **form_id** ב-iPlan
- [ ] גיליון Consul House - Leads מוכן (Registry + Audit Log)
- [ ] חשבון Make + חיבורים (Google Sheets, HTTP, Gmail)
- [ ] API key חדש ל-iPlan (הישן נחשף)
