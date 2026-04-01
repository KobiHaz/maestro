# iPlan API – Create new message [POST]

**Endpoint:** `https://iplan.co.il/he-IL/api/corp/leads.json`  
**Docs:** https://apidocs.iplan.co.il/#create-new-message-post

## Request (JSON)

```json
{
  "api_key": "YOUR_API_KEY",
  "form_id": 123456789,
  "contact_full_name": "Test User",
  "contact_email": "test@example.com",
  "contact_phone": "0501234567",
  "request_content": "Event: Wedding | Guests: 20 | Notes: בדיקה",
  "request_matter": "Wedding"
}
```

## Parameters

| Parameter | Type | Required | Max | Description |
|-----------|------|----------|-----|-------------|
| api_key | string | ✅ | - | API key from iPlan |
| form_id | **integer** | ✅ | - | Form ID from `מאגרים > טפסי פנייה` → קוד |
| contact_full_name | string | ✅ | 100 | Full name |
| contact_email | string | ⚠️ one of email/phone | 100 | Email address |
| contact_phone | string | ⚠️ one of email/phone | 20 | Phone number |
| request_content | string | ✅ | 1024 | Message/content |
| request_matter | string | no | 20 | Subject (default: "Request received via API") |

## Response (success)

```json
{
  "status": "ok",
  "message_id": 12345
}
```

## Response (validation error – 422)

```json
{
  "status": "validation_failed",
  "message": "validation failed",
  "errors": {
    "contact_full_name": "must be present",
    "contact_email": "invalid format"
  }
}
```

## Headers

```
Content-Type: application/json
```

## מיפוי מ-Make (לפי Webhook)

| iPlan field | Map from Make |
|-------------|---------------|
| api_key | קבוע / משתנה |
| form_id | קבוע (מספר) |
| contact_full_name | `{{FirstName}} {{LastName}}` |
| contact_email | `{{Email}}` |
| contact_phone | `{{Phone}}` |
| request_content | `{{Notes}} \| Event: {{EventType}} \| Guests: {{Guests}}` |
| request_matter | `{{EventType}}` |
