# מיפוי נכון ל-Scenario Inputs – Leads to iPlan

## עדכון ב-Make.com

השתמש ב-**snake_case** לכל השדות. עבור **Scenario Inputs** (כאשר מודול 1 = Webhook):

| שדה ב-Scenario | ערך נכון |
|----------------|----------|
| **first_name** | `1.first_name` |
| **last_name** | `1.last_name` |
| **phone** | `1.phone` |
| **event_type** | `1.event_type` |
| **guests** | `1.guests` |
| **source** | `1.source` |
| **lead_id** | `{{runId}}` או `{{iterationId}}` |
| **email** | `1.email` |
| **created** | `now` |

## JSON שצריך להגיע ל-Webhook

```json
{
  "first_name": "Test",
  "last_name": "User",
  "email": "test@example.com",
  "phone": "0501234567",
  "event_type": "Wedding",
  "guests": "20",
  "notes": "בדיקה מעודכנת",
  "source": "website"
}
```

## Webhook URL

```
https://hook.eu1.make.com/bpibpo5klk0te7l89l2cb8ydl1saov3o
```
