# Gold IRA Quiz — Implementation Plan

> **Source:** [design doc](./2026-03-06-gold-ira-quiz-design.md)

## Goal

Build the Gold IRA quiz (6 questions, scoring, brand landing), lead capture to Google Sheets, and admin panel for brand config. Plain HTML/CSS/JS.

---

## Tasks

### Phase 1: Project + Quiz UI

- [ ] **1. Scaffold** — Create `gold-ira-quiz/` with `index.html`, `styles.css`, `script.js`; minimal layout. → Verify: Open index.html in browser.
- [ ] **2. Intro + step shell** — Intro hero with "Start the Quiz", step containers (intro, q1–q6, analyze, email, contact, result). Show/hide via `.active` class. → Verify: Click "Start", see first question.
- [ ] **3. Quiz flow** — 6 questions with options; click option → auto-advance, update progress bar. Store answers in state object. → Verify: Answer all 6, reach analyze step.
- [ ] **4. Analyze step** — ~2.5s loading bar + status messages; then "We found your match!". → Verify: Full animation plays, advances to email step.

### Phase 2: Scoring + Results

- [ ] **5. Scoring logic** — Implement Option D scoring (config.js or inline). Compute tier from score. → Verify: Test combinations; $250k+ + IRA rollover + immediately → VIP.
- [ ] **6. Brand landing** — Result step shows brand (name, description, CTA) based on tier. Start with hardcoded config (3 placeholder brands). → Verify: Score VIP → see VIP brand; Tier1Mid → see Tier1Mid brand.

### Phase 3: Lead Capture + Google

- [ ] **7. Form validation** — Email format, required firstName/lastName/phone. → Verify: Empty submit blocked; valid submit enabled.
- [ ] **8. Google Apps Script** — Deploy script: GET returns brand JSON; POST accepts form data + appends to Leads sheet. Create Brands + Leads tabs. → Verify: curl GET returns JSON; POST adds row to Sheet.
- [ ] **9. Wire quiz to script** — Quiz POSTs lead data to Apps Script URL on "Get My Match". Fetches brand config from GET before showing result. → Verify: Submit → row in Sheet; result reflects fetched config.

### Phase 4: Branding, Legal & Footer

- [ ] **10. Logo + theme** — Add logo (assets/logo.png), CSS variables from goldira colors (#dcbb57, #018060, #F9F6EE, #003e21). → Verify: Logo in header, goldira palette applied.
- [ ] **11. Footer** — Footer with logo, brand block, Quick Links (Terms, Privacy), Legal links, disclaimer text, affiliate disclosure (text + "Learn more" modal). → Verify: Footer matches CMS style, all links work.
- [ ] **12. terms.html** — Static Terms of Use page (content from CMS Financial Advice version). → Verify: Full content, links to policy.
- [ ] **13. policy.html** — Static Privacy Policy page (content from CMS, adapted for lead capture). → Verify: Full content, contact link.

### Phase 5: Admin Panel

- [ ] **14. admin.html + admin.js** — Form for 3 brands (tier, name, description, ctaText, logoUrl). Same color system, distinct layout. Load from GET, save via POST (token). → Verify: Edit brand, save, reload quiz, see updated brand.

---

## Done When

- [ ] Quiz runs end-to-end: Intro → 6 questions → analyze → email → contact → brand result.
- [ ] Lead data lands in Google Sheet.
- [ ] Admin can edit brands and tier; quiz shows updated config.
- [ ] Logo, footer, Terms, Privacy, disclaimer, affiliate disclosure present.
- [ ] No framework; plain HTML/CSS/JS.

---

## Notes

- Apps Script URL stored in `script.js` (or config). Replace placeholder with deployed URL.
- Admin token: store in Script Properties or env; validate in doPost.
