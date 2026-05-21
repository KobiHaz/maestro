---
name: cv-builder
description: Builds a tailored, one-page PDF CV for a specific job posting. Use when user asks to create, tailor, or adapt a CV/resume for a role. Reads CV source from 02-projects/cv/project.cv.md, adapts content to the job description, and generates a styled PDF.
allowed-tools: Read, Write, Edit, Bash
---

# CV Builder Skill

Produces a one-page, professionally styled PDF CV tailored to a specific job description.
Inspired by: rendercv (data → PDF), Awesome-CV (ATS-friendly structure), best-resume-ever (visual polish).

## Constraints (always enforced)

- **One page only** — never overflow. Trim bullets, shorten profile, reduce spacing before adding a page.
- **No tables** — use bullet lists and inline key-value pairs only.
- **Language** — CV content always in English; conversation in Hebrew.
- **Design** — preserve the orange header two-column layout defined in `references/design-spec.md`.
- **Output** — PDF saved to `/Users/kobihazout/Desktop/CV/<YYYY-MM-DD>-cv-<company-slug>.pdf` and markdown copy to `06-outputs/`.

---

## Workflow

### Step 1 — Load context
Read both files before doing anything else:
- `02-projects/cv/project.cv.md` — full professional history (source of truth)
- `03-agents/skills/cv-builder/references/design-spec.md` — visual design rules

### Step 2 — Analyse the job description
Identify:
1. **Role type** → determines the CV title (e.g. "Business Operations & Growth", "Game Producer", "Head of TechOps")
2. **Top 5 required skills / keywords** → must appear naturally in profile or bullets
3. **Explicit advantages** (e.g. "B.Sc. Information Systems", "Make.com", "HubSpot") → surface prominently
4. **Tone** → startup = lean, direct; corporate = structured, metrics-heavy

### Step 3 — Build the JSON payload
Populate the schema below. Every field is mandatory.
Keep bullets ≤ 18 words each. Profile ≤ 55 words.

```json
{
  "name": "KOBI HAZOUT",
  "title": "<ROLE TYPE — e.g. BUSINESS OPERATIONS & GROWTH>",
  "contact": {
    "phone": "(+972) 054-978-9001",
    "email": "Kobihazout2@gmail.com",
    "linkedin": "LinkedIn",
    "github": "GitHub"
  },
  "profile": "<55-word summary. Lead with years + domain. End with strongest JD match.>",
  "experience": [
    {
      "title": "<JOB TITLE>",
      "company": "<COMPANY>",
      "period": "<MON YYYY – MON YYYY>",
      "bullets": [
        "<Achievement 1 — metric or outcome>",
        "<Achievement 2>",
        "<Achievement 3>"
      ]
    }
  ],
  "skills": [
    { "label": "<Category>", "value": "<tool1, tool2, tool3>" }
  ],
  "education": {
    "degree": "B.Sc. Information Systems",
    "school": "The Academic College of Tel Aviv-Yaffa",
    "years": "2019 – 2022"
  },
  "military": {
    "unit": "Elite Unit of the Golani Brigade",
    "years": "2013 – 2016",
    "description": "Combat commander in Palhan Golani, led teams in a specialized battalion."
  },
  "volunteer": {
    "title": "Project Manager",
    "org": "FrontLife",
    "period": "Sep 2022 – Mar 2024",
    "bullets": [
      "Supporting veterans as they transition to civilian life.",
      "Coordinating initiatives that maximize personal and professional development."
    ]
  },
  "interests": ["Snowboarding", "Yoga", "Stock Market & Crypto", "Vinyl Collector", "Catan", "Dota 2"]
}
```

### Step 4 — Generate the JSON input file
Write the payload to a temp file:
```
/tmp/cv_input.json
```

### Step 5 — Run the PDF generator
```bash
python3 "/Users/kobihazout/Library/Mobile Documents/iCloud~md~obsidian/Documents/Maestro/03-agents/skills/cv-builder/scripts/generate_cv.py" \
  /tmp/cv_input.json \
  "/Users/kobihazout/Desktop/CV/$(date +%Y-%m-%d)-cv-<company-slug>.pdf"
```

### Step 6 — Verify output
- Read the generated PDF and confirm it rendered correctly (no overflow, no missing sections).
- If content overflows one page: shorten profile to 45 words, reduce each role to max 3 bullets.

### Step 7 — Save markdown copy
Write the JSON-derived content as a clean `.md` file to:
`06-outputs/YYYY-MM-DD-cv-<company-slug>.md`

### Step 8 — Report to user
State: filename, what was tailored, and ask if any changes are needed.

---

## Content guidelines (from Awesome-CV & rendercv)

- **Bullets start with a strong past-tense verb**: Built, Led, Reduced, Automated, Standardized, Deployed, Managed, Scaled.
- **Every bullet answers**: what did you do, and what was the outcome (metric when possible).
- **Profile**: 3 sentences max — who you are, what you bring, why you fit this role.
- **Skills section**: only list tools explicitly mentioned in the JD or obviously relevant — never pad.
- **ATS keywords**: mirror the JD's exact phrasing (e.g. if JD says "HubSpot", write "HubSpot" not "CRM tool").

---

## One-page enforcement rules

If the PDF overflows, apply in order until it fits:
1. Remove the least-relevant job's 3rd bullet
2. Trim profile to 40 words
3. Reduce oldest Spinomenal role to 2 bullets
4. Reduce skills to 4 rows
5. Shorten volunteer bullets to 1 line each

Never remove: name, title, contact, education, military, profile, most recent 2 roles.
