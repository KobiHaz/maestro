# Project Audit Report — gold-ira-quiz

**Date:** 2026-03-07  
**Project:** gold-ira-quiz  
**Type:** WEB

## Sources Used

- `02-projects/gold-ira-quiz/project.gold-ira-quiz.md`
- Agents: explorer-agent, security-sentinel, frontend-specialist
- Project path: `/Users/kobihazout/.gemini/antigravity/projects/gold-ira-quiz`
- Prior docs: `docs/NEXT-LEVEL-PLAN.md`, `docs/plans/EXECUTION-PLAN.md`, `docs/AUDIT-ANALYSIS.md`

---

## Findings by Domain

### Discovery (explorer-agent)

- **Structure:** Vanilla HTML/CSS/JS; no build; static files + separate Google Apps Script backend
- **Entry points:** index.html (quiz), result.html (landing), admin.html (config)
- **Data flow:** Quiz → script.js → POST lead → GAS doPost → Sheets; brands from GAS doGet
- **Risk areas:** Admin unprotected; affiliate modal triggers (#affiliate-trigger, #footer-affiliate-trigger) missing; logo 404; lead submit ignores response; duplicated brand defaults
- **P0:** Consent before lead, result disclosure, affiliate triggers, logo asset, admin protection

### Security (security-sentinel)

| Severity | Count | Top issues |
|----------|-------|------------|
| Critical | 3 | Admin unprotected; token in POST body; logoUrl XSS |
| High | 3 | No CORS/origin validation; formula injection (Sheets); no CSRF |
| Medium | 3 | No input limits; timing-safe token; innerHTML (mitigated) |

**Remediation roadmap:** Protect admin; validate logo URL; move token to Authorization header; sanitize Sheets formula triggers; add maxlength + server limits.

### Frontend (frontend-specialist)

- **a11y P0:** Form inputs missing labels; option buttons lack radiogroup/radio semantics
- **a11y P1:** No focus styles; modal lacks dialog semantics; affiliate modal triggers missing
- **a11y P2:** Progress bar label; aria-live for step changes; loader status; logo alt
- **UX:** Competitor notes from ConsumerAffairs: icons per option, stronger selected state, horizontal layout for 2–4 options, URL hash for steps

---

## Recommendations (Prioritized)

### P0 — Critical

1. Add consent checkbox before lead capture (GDPR)
2. Add affiliate disclosure on result page (FTC)
3. Add #affiliate-trigger and #footer-affiliate-trigger in footer or remove dead code
4. Add assets/logo.png or make logo conditional (no 404)
5. Protect admin (auth or IP allowlist)
6. Validate logoUrl before img.src (https or data:image/* only)

### P1 — High

7. Lead submit: disable during fetch; show error on !res.ok
8. Form labels: associate <label for="..."> with all inputs
9. Result CTA: use brand.ctaUrl instead of #
10. Centralize brand defaults (single source)
11. Input length limits (client + server)
12. Formula injection sanitization in GoogleAppsScript.gs
13. Move token to Authorization header; origin whitelist in GAS

### P2 — Medium

14. Option buttons: role="radiogroup"/"radio", aria-checked
15. Modal: role="dialog", focus trap, ESC to close
16. :focus-visible for buttons
17. CORS/origin checks in GAS
18. Progress bar aria-label; aria-live for step changes
19. Privacy contact in footer; CCPA Do Not Sell

---

## Knowledge Gaps

- [ ] Create `04-knowledge/reference/gold-ira-quiz-architecture.md` (current + target)
- [ ] Create `04-knowledge/standards/gold-ira-quiz-standards.md` (React/Next.js conventions)

---

## Next Steps (Planned Migration)

Per `docs/NEXT-LEVEL-PLAN.md` and `docs/plans/EXECUTION-PLAN.md`:

- **Phase 0:** Next.js scaffold + Firebase init + Functions stubs
- **Phase 1:** Migrate quiz UI + Option A lead flow + consent + affiliate disclosure
- **Phase 2:** Funnel analytics (events), quiz resume (cookie), attribution
- **Phase 3:** Security (admin auth, origin whitelist, logo validation, input limits)
- **Phase 4:** Code quality (affiliate triggers, lead UX, form labels, README)
- **Phase 5:** UI/UX (icons, selected state, URL hash, horizontal layout)
