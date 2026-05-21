# Skill: Consul House Weekly Leads Report

## Context
- **Client:** Consul House — events/wedding venue in Jaffa
- **Spreadsheet ID:** `120O1vAeATTwjgut2DJ8tjxbGbemi7aZap5leO0K3db8`
- **Make.com scenarios:** 4904291 (Master), 4901312 (Facebook Leads Ads), 4904555 (Webhook)
- **Recipients (production):** kobi@xsheva.com, lee@consulhouse.co.il

## Sheet Structure

### "Leads" sheet — successfully sent to iplan (Status = "200 - OK")
| Column | Description |
|--------|-------------|
| Created At (Date) | DD/MM/YYYY HH:mm |
| Source | Website / Facebook campaign name / GMB |
| First Name, Last Name | Lead name |
| Event Type | חתונה / אחר / עסקי |
| Guests | 150-200 / 200-250 / 250-300 / 300-350 |
| Phone, Email | Contact details |
| Notes | Free text from lead |
| Estimated Date | Event date if provided |
| Status | "200 - OK" = successfully sent |
| Lead ID | UUID (website) or Facebook lead ID (numeric) |
| UtmCampaign, UtmMedium, UtmContent | Campaign tracking |
| Fbclid | Facebook click ID |

### "New" sheet — all incoming leads (includes duplicates)
Same columns + Status column can be "Duplicate"

### "Failed" sheet — leads that failed to reach iplan
Same columns + Error Code column

## Report Generation Steps

### 1. Read Google Sheets
Use Google Drive MCP (`read_file_content`) on spreadsheet ID `120O1vAeATTwjgut2DJ8tjxbGbemi7aZap5leO0K3db8`.
Filter rows where `Created At (Date)` is within the last 7 days.

Parse date format: DD/MM/YYYY HH:mm (Israeli format).

### 2. Read Make.com executions
Use Make MCP (`executions_list`) for scenario IDs 4904291, 4901312, 4904555.
Note: total runs, errors, incomplete executions in the last 7 days.

### 3. Calculate metrics
- **Total received** = count of all rows in "New" sheet this week
- **Sent to iplan** = count of rows in "Leads" sheet this week
- **Duplicates** = count of rows in "New" with Status = "Duplicate"
- **Failed** = count of rows in "Failed" sheet this week (if any)
- **By source** = group "Leads" rows by Source field, count per source
- **By event type** = group by Event Type (חתונה / עסקי / אחר)
- **By guest count** = group by Guests range

### 4. Build HTML email

```html
<!DOCTYPE html>
<html dir="ltr">
<head><meta charset="UTF-8"></head>
<body style="font-family:Arial,sans-serif;max-width:700px;margin:0 auto;padding:20px">

  <h2 style="color:#1a1a2e;border-bottom:2px solid #e0e0e0;padding-bottom:10px">
    Consul House — Weekly Leads Report
  </h2>
  <p style="color:#666">Period: [Monday DD/MM] — [Friday DD/MM/YYYY]</p>

  <!-- Summary -->
  <table style="border-collapse:collapse;width:100%;margin:20px 0">
    <tr style="background:#f5f5f5">
      <th style="padding:10px;text-align:left;border:1px solid #ddd">Metric</th>
      <th style="padding:10px;text-align:center;border:1px solid #ddd">Count</th>
    </tr>
    <tr><td style="padding:8px;border:1px solid #ddd">Total leads received</td><td style="text-align:center;border:1px solid #ddd">[N]</td></tr>
    <tr><td style="padding:8px;border:1px solid #ddd">✅ Sent to iplan</td><td style="text-align:center;border:1px solid #ddd">[N]</td></tr>
    <tr><td style="padding:8px;border:1px solid #ddd">🔁 Duplicates blocked</td><td style="text-align:center;border:1px solid #ddd">[N]</td></tr>
    <tr><td style="padding:8px;border:1px solid #ddd;color:[red if >0 else inherit]">❌ Failed sends</td><td style="text-align:center;border:1px solid #ddd">[N]</td></tr>
  </table>

  <!-- By Source -->
  <h3 style="color:#333">By Source</h3>
  <table style="border-collapse:collapse;width:100%;margin-bottom:20px">
    <tr style="background:#f5f5f5">
      <th style="padding:8px;text-align:left;border:1px solid #ddd">Source</th>
      <th style="padding:8px;text-align:center;border:1px solid #ddd">Leads</th>
    </tr>
    [row per source]
  </table>

  <!-- By Event Type -->
  <h3 style="color:#333">By Event Type</h3>
  [חתונה / עסקי / אחר counts]

  <!-- Lead Details -->
  <h3 style="color:#333">All Leads This Week</h3>
  <table style="border-collapse:collapse;width:100%;font-size:13px">
    <tr style="background:#f5f5f5">
      <th style="padding:6px;border:1px solid #ddd">Date</th>
      <th style="padding:6px;border:1px solid #ddd">Name</th>
      <th style="padding:6px;border:1px solid #ddd">Phone</th>
      <th style="padding:6px;border:1px solid #ddd">Event</th>
      <th style="padding:6px;border:1px solid #ddd">Guests</th>
      <th style="padding:6px;border:1px solid #ddd">Source</th>
      <th style="padding:6px;border:1px solid #ddd">Status</th>
    </tr>
    [one row per lead, sorted by date desc]
    [highlight duplicates in yellow, failures in red]
  </table>

  <!-- Failures (if any) -->
  [If failed > 0:]
  <h3 style="color:#c00">⚠️ Failed Sends — Require Attention</h3>
  [table of failed leads with error codes]

  <hr style="margin:30px 0;border:none;border-top:1px solid #eee">
  <p style="color:#999;font-size:11px">
    Report generated automatically by Xsheva | kobi@xsheva.com<br>
    Powered by Claude + Make.com automation
  </p>

</body>
</html>
```

### 5. Send via Gmail
- **To:** kobi@xsheva.com, lee@consulhouse.co.il
- **Subject:** `📊 Consul House — Weekly Report DD/MM – DD/MM/YYYY`
- **Body type:** HTML

### Error handling
If any step fails → send plain-text alert to kobi@xsheva.com:
- Subject: `⚠️ Consul House Weekly Report — Failed [date]`
- Body: step name + error details
