# Gold IRA Quiz & Brand Landing Page — Design Document

> **Date:** 2026-03-06  
> **Status:** Approved for implementation  
> **Project:** New standalone (gold-ira-quiz/)

---

## 1. Overview

Static multi-step Gold IRA quiz with lead capture and personalized brand landing page. Plain HTML, CSS, JavaScript. Lead capture → Google Sheets. Brand matching via scoring. Admin panel to control brand details and tier assignment.

**Design source:** UI/UX, colors, Terms, Privacy, footer, and affiliate disclosure adapted from the main CMS project (goldira vertical). Admin panel is separate and distinct from main CMS.

---

## 2. User Flow

| Step | Description |
|------|--------------|
| Intro | Hero with "Start the Quiz" button |
| Quiz (6 questions) | Auto-advance on answer, step progress bar |
| Analyze | Loading (~2.5s), status messages, then "We found your match!" |
| Email | Single email field, "Continue" |
| Contact | First name, last name, phone, "Get My Match" |
| Brand landing | Personalized result based on score → tier → assigned brand |

---

## 3. Quiz Questions (6 total)

Contact preference removed. All leads receive a call.

1. **Primary goal** — IRA rollover | physical delivery | diversification
2. **Timeline** — immediately | 30 days | 6 months | researching
3. **Account type** — 401(k) | IRA | Roth | TSP | not sure
4. **Asset value** — Under $25k | $25k–50k | $50k–100k | $100k–250k | $250k+
5. **Portfolio exposure** — 0–25% | 25–50% | 50–75% | 75–100%
6. **Priority** — lowest fees | best bonus | highest ratings | fastest processing

---

## 4. Brand Matching — Option D (Scoring)

### Point values

| Question | Option | Points |
|----------|--------|--------|
| **Asset value** | $250k+ | 3.0 |
| | $100k–250k | 2.0 |
| | $50k–100k | 1.0 |
| | $25k–50k | 0.5 |
| | Under $25k | 0 |
| **Primary goal** | IRA rollover | 0.5 |
| | physical delivery | 0.25 |
| | diversification | 0 |
| **Timeline** | immediately | 0.5 |
| | 30 days | 0.25 |
| | 6 months | 0 |
| | researching | 0 |
| **Account type** | 401(k), IRA, Roth, TSP | 0.25 |
| | not sure | 0 |
| **Priority** | fastest processing | 0.25 |
| | highest ratings | 0.125 |
| | best bonus, lowest fees | 0 |
| **Portfolio exposure** | (reserved / future use) | 0 |

### Tier mapping

| Score range | Tier |
|-------------|------|
| ≥ 3.0 | VIP |
| 1.5 – 2.99 | Tier 1 High |
| < 1.5 | Tier 1 Mid |

---

## 5. Admin Panel

### Purpose

- Edit brand details (name, description, CTA, logo URL)
- Assign each brand to a tier (VIP, Tier 1 High, Tier 1 Mid)
- Quiz result shows the brand assigned to the user's tier

### Data model (brand config)

```json
{
  "brands": [
    {
      "id": "brand-1",
      "tier": "VIP",
      "name": "Premium Gold Partners",
      "description": "Exclusive service for high-net-worth investors.",
      "ctaText": "Schedule Your Consultation",
      "logoUrl": "https://..."
    },
    { "id": "brand-2", "tier": "Tier1High", ... },
    { "id": "brand-3", "tier": "Tier1Mid", ... }
  ]
}
```

Only one brand per tier. Admin swaps which brand is VIP, Tier 1 High, or Tier 1 Mid.

### Admin approach: Google Sheet + Apps Script

| Component | Role |
|-----------|------|
| **Google Sheet tab "Brands"** | Columns: id, tier, name, description, ctaText, logoUrl |
| **Apps Script** | GET /brands → JSON for quiz; POST /brands (admin only); stores in Sheet |
| **admin.html** | Simple form to edit 3 brands + tier dropdown; uses Apps Script API |

**Auth:** Simple token in URL (`?token=xxx`) or Apps Script Session.getActiveUser() for deploy-as-user. Apps Script validates before write.

**Flow:** Admin opens admin.html → loads current brands → edits → saves → quiz fetches updated config on next load.

---

## 6. Architecture

```
gold-ira-quiz/
├── index.html          # Quiz + brand landing (public)
├── admin.html          # Admin panel (same origin, token-protected)
├── styles.css
├── script.js           # Quiz logic, scoring, form submit
├── admin.js            # Admin form logic
└── assets/             # Logos, images

Google Apps Script (deployed as web app):
├── doGet(e)            # Serve brand config as JSON
├── doPost(e)           # Form submissions + admin brand updates
└── Brands sheet        # Source of truth for brand config
```

---

## 7. Google Sheets Integration

### Sheet 1: Leads

Columns: timestamp, email, firstName, lastName, phone, tier, score, quizAnswers (JSON string)

### Sheet 2: Brands

Columns: id, tier, name, description, ctaText, logoUrl

Apps Script reads Brands → serves to quiz; admin writes back to Brands.

---

## 8. Technical Notes

- **No framework** — Plain HTML, CSS, JS
- **Single-page quiz** — Steps shown/hidden via JS (e.g. `.active` class)
- **Progress bar** — Updates on each quiz step (6 segments + intro + analyze + email + contact)
- **Validation** — Email format, required fields, before submit
- **Responsive** — Mobile-first CSS
- **Config fetch** — Quiz fetches brand config from Apps Script URL before showing result step

---

## 9. Branding, Legal & Footer (from CMS)

### 9.1 Logo

Use the **three gold bars logo** (metallic gold, increasing height, transparent background). Source: `assets/image__3_-80100974-53b9-4e20-9e79-a0c25c014424.png` (or copy to `gold-ira-quiz/assets/logo.png`). Display in header/nav and footer.

### 9.2 UI/UX Colors (goldira vertical)

| Token | Value | Usage |
|-------|-------|--------|
| Primary | `#dcbb57` | Accents, CTAs, rating |
| Secondary | `#018060` | Links, secondary actions |
| Background | `#F9F6EE` | Page background |
| Card | `#FFFFFF` | Cards, surfaces |
| Footer BG | `#003e21` | Footer background |
| Text primary | `#000000` | Headings, body |
| Footer link | `#9CA3AF` | Footer links |
| Footer link hover | `#60A5FA` | Footer link hover |

### 9.3 Footer

- **Layout:** Dark background (`#003e21`), max-w-7xl, grid columns (brand col + Quick Links + Legal)
- **Brand block:** Logo + brand name + tagline + description
- **Quick Links:** Terms of Use, Privacy Policy (links to static pages)
- **Legal:** Terms of Use, Privacy Policy
- **Disclaimer:** Footer disclaimer text (below main content, above copyright)
- **Affiliate disclosure:** Inline in footer + link to popup/modal with full text
- **Copyright:** e.g. "© 2026 [Brand]. All rights reserved."

### 9.4 Terms of Use

Static HTML page at `/terms.html`. Content from CMS `TermsOfUsePage` (Financial Advice version):
- Financial Advice Disclaimer
- Introduction, Changes to Terms, Eligibility, Access and Use Rights
- Scope of Services (Referral-Only, Gold IRA context)
- Prohibited Uses, Intellectual Property
- Third-Party Services, Content Accuracy
- Advertising Relationships and Rating Methodology (affiliate disclosure)
- Information Disclosure, Links, Privacy, Warranty Disclaimers
- Limitation of Liability, Indemnification, Term/Termination
- Governing Law (Hong Kong)
- Internal links: Privacy Policy (`policy.html`), Contact

### 9.5 Privacy Policy

Static HTML page at `policy.html`. Content from CMS `PrivacyPolicyPage`:
- Full sections 1–14 (Policy Amendments, Data Controller, Information We Collect, etc.)
- Contact link, California/other jurisdiction notices
- Adapted for lead-capture context (quiz submissions → Google Sheets)

### 9.6 Disclaimer & Affiliate Disclosure

- **Disclaimer:** In footer, below copyright area. Standard financial disclaimer (not financial advice, perform own research, consult professional).
- **Affiliate disclosure:** Bar below header OR in footer. Text: "Rankings and 'Top' picks are influenced by referral fees. This compensation may impact the location and order in which brands appear. Our ratings are not an endorsement of performance or reliability." Link text: "Learn more" → opens modal/popup with full disclosure.

### 9.7 Typography

- ** headings:** Lora, Georgia, serif
- **Body:** Inter, system-ui, sans-serif

---

## 10. Admin Panel (Separate from Main CMS)

### 10.1 Purpose

Dedicated admin for the Gold IRA quiz website only. Not part of the main CMS. Token-protected.

### 10.2 Styling

- **Same color system** as quiz (goldira palette) for brand consistency
- **Distinct layout:** Lighter background (`#F9F6EE` or `#FFFFFF`) for forms; dark accents
- **Header:** Logo + "Quiz Admin" label; minimal nav
- **Forms:** Card-based, clear labels, primary CTA color (`#dcbb57` / `#018060`)
- **No CMS chrome:** No main CMS sidebar, header, or navigation

### 10.3 Pages

- Brand config: Edit 3 brands (tier, name, description, ctaText, logoUrl)
- (Future: view leads, if needed)

---

## 11. Out of Scope (v1)

- Hash routing / shareable URLs
- A/B testing
- Analytics events (can add later)
- Multiple brands per tier

---

## Next Step

Invoke **writing-plans** skill to create implementation plan.
