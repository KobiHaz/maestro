# Gold IRA Quiz

> **Status:** Design complete (Option A), implementation planned  
> **Plan:** `docs/plans/GOLD-IRA-QUIZ-EXECUTION-PLAN.md` (in project repo)  
> **Audit:** `06-outputs/2026-03-07-gold-ira-quiz-audit-report.md`

## Stack (Current → Target)

| Layer | Current | Target |
|-------|---------|--------|
| Frontend | Vanilla HTML/CSS/JS | Next.js (static export) |
| Backend | Google Apps Script + Sheets | Firebase Firestore + Cloud Functions |
| Hosting | Static server | Cloudflare Pages |
| Auth | Admin token in body | Firebase Auth + origin whitelist |

## Path

`~/.gemini/antigravity/projects/gold-ira-quiz-next` (code); Maestro vault for plans/docs.

## Purpose

Multi-step Gold IRA quiz → lead capture → personalized brand landing page. Admin panel to control brand details and tier assignment.

## Option A (PII)

We do **not** store PII (name, email, phone). We generate a Lead ID, forward full lead to brand via webhook, and store only: leadId, timestamp, tier, brandId, score, quizAnswers, consentTimestamp.

## Funnel Analytics

- Events: `quiz_start`, `step_view`, `form_submit`
- Anonymous sessionId (UUID in sessionStorage)
- Metrics: starts, conversions, drop-off by step

## Branding (from CMS goldira)

- **Logo:** Three gold bars (metallic, transparent BG)
- **Colors:** Primary #dcbb57, Secondary #018060, BG #F9F6EE, Footer #003e21
- **Terms, Privacy, Footer, Disclaimer, Affiliate disclosure:** Content/structure from main CMS
- **Admin:** Separate from main CMS; basic auth at host

## Decisions

- **Brand matching:** Option D scoring (asset + goal + timeline + account + priority)
- **Tiers:** VIP, Tier 1 High, Tier 1 Mid (3 only)
- **Lead flow:** Option A — forward to brand webhook; no PII storage
- **Brands schema:** id, tier, name, description, ctaText, logoUrl, **ctaUrl**, **webhookUrl**
- **Admin:** admin.html + basic auth; Brands sheet is source of truth
- **Legal:** Static terms.html, policy.html; US-only, CCPA/TCPA compliant

## Related

- [[03-agents/content/gold-ira-seo-content-writer]]
