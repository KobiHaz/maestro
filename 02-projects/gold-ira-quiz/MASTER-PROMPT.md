# Master Prompt — Gold IRA Quiz

> Project-specific instructions for the gold-ira-quiz. Copy-paste when starting work on this project.

---

## Role

You are working on the **Gold IRA Quiz** — a multi-step quiz that captures leads and routes them to personalized brand landing pages. No PII storage; leads forwarded via webhook.

---

## Paths

| Location | Path |
|----------|------|
| **Code** | `/Users/kobihazout/.gemini/antigravity/projects/gold-ira-quiz-next` |
| **Maestro (docs)** | `02-projects/gold-ira-quiz/` |
| **Plans & tasks** | `02-projects/gold-ira-quiz/plans-and-tasks.md` |
| **Project brief** | `02-projects/gold-ira-quiz/project.gold-ira-quiz.md` |

---

## Stack

| Layer | Tech |
|-------|------|
| Frontend | Next.js 16 (App Router), React 19, Tailwind v4 |
| Build | Static export (`output: "export"`), `images: { unoptimized: true }` |
| Backend | Firebase (Firestore, Cloud Functions, Auth) |
| Hosting | Cloudflare Pages |
| Auth | Firebase Auth + origin whitelist |

---

## Key Decisions (Do Not Deviate Without Discussion)

- **Lead flow (Option A):** We do **not** store PII. We generate `leadId`, forward full lead to brand webhook, store only: `leadId`, `timestamp`, `tier`, `brandId`, `score`, `quizAnswers`, `consentTimestamp`.
- **Tiers:** VIP, Tier 1 High, Tier 1 Mid (3 only).
- **Brand matching:** Option D scoring — asset, goal, timeline, account, priority.
- **Brands schema:** `id`, `tier`, `name`, `description`, `ctaText`, `logoUrl`, `ctaUrl`, `webhookUrl`.
- **Legal:** US-only, CCPA/TCPA compliant; static `terms.html`, `policy.html`.
- **Admin:** Separate from main CMS; basic auth at host.

---

## Quiz Steps & Scoring

**Steps (order):** goal → timeline → account → asset → exposure → priority.

**Scoring:** `lib/scoring.ts` — `SCORE_MAP`, `TIER_THRESHOLDS`, `computeTier(answers)`.

**Question keys:** `q1`=goal, `q2`=timeline, `q3`=account, `q4`=asset, `q5`=exposure, `q6`=priority.

---

## Funnel Analytics

- **Events:** `quiz_start`, `step_view`, `form_submit`, `conversion`
- **Session:** Anonymous `sessionId` (UUID in sessionStorage)
- **Implement in:** `lib/analytics.ts`
- **Metrics:** starts, conversions, drop-off by step

---

## Design System

**File:** `docs/design-system.md`

| Token | Value | Usage |
|-------|-------|-------|
| `--color-primary` | #1a421f | CTAs, primary buttons |
| `--color-gold-accent` | #c5a059 | Icons, accents, badges |
| `--color-bg` | #f6f8f6 | Page background |
| `--color-card` | #ffffff | Cards |
| `--color-footer` | #1a421f | Footer |
| `--color-text` | #1e293b | Primary text |
| `--color-text-muted` | #64748b | Secondary text |
| `--color-error` | #dc2626 | Validation |

**Typography:** Manrope. **Icons:** Material Symbols Outlined.

Use CSS variables; in Tailwind: `className="bg-[var(--color-primary)]"`.

---

## Code Structure

```
app/
  page.tsx       # Quiz (client)
  result/page.tsx # Brand landing
  admin/page.tsx # Admin panel
  policy/page.tsx
  terms/page.tsx
lib/
  scoring.ts     # Tier computation, steps, types
  api.ts         # fetchBrands, submitLead, getDefaultBrands
  analytics.ts   # trackQuizStart, trackStepView, trackFormSubmit, trackConversion
  cookies.ts     # Session, progress, attribution
  firebase.ts    # Auth, Analytics init
components/
  ui/ProgressBar.tsx
  ui/OptionButton.tsx
  quiz/TrustSignals.tsx
  quiz/FeaturesGrid.tsx
```

---

## Coding Standards (This Project)

- **Base:** `04-knowledge/standards/base-coding-standards.md`
- **TypeScript:** No `any`; explicit types for exported APIs.
- **Data:** Normalize at fetch boundary (`lib/api.ts`); components receive clean data.
- **Hooks:** `use` + PascalCase (e.g. `useQuizProgress`).
- **Naming:** `get*` = sync; `fetch*` = network; `load*` = cache/bootstrap.

---

## Security & Compliance (Mandatory)

- **Consent:** Checkbox before lead capture; record `consentTimestamp`.
- **PII:** Never store name, email, phone in Firestore. Forward to webhook only.
- **logoUrl:** Validate before `img.src` — `https://` or `data:image/*` only (XSS).
- **Admin:** Protected (auth or IP allowlist).
- **Input limits:** `maxlength` client-side; server-side validation in Cloud Functions.

---

## Phases (Current Plan)

| Phase | Status | Focus |
|-------|--------|-------|
| 0 | 🟩 Done | Scaffold + Firebase |
| 1 | 🟥 To Do | Migrate UI + Option A Lead Flow |
| 2 | 🟥 To Do | Funnel Analytics + Quiz Resume |
| 3 | 🟥 To Do | Security + Compliance |
| 4 | 🟥 To Do | Code Quality + Docs |
| 5 | 🟥 To Do | UI/UX (Competitor-Inspired) |

---

## Before You Start

1. Read `project.gold-ira-quiz.md` (full brief).
2. Check `plans-and-tasks.md` for current tasks.
3. For UI changes, follow `docs/design-system.md`.
4. For Gold IRA content/copy, invoke `gold-ira-seo-content-writer`.

---

## Verification Before "Done"

- [ ] `npm run build` — succeeds
- [ ] `npm run lint` — no errors
- [ ] No PII stored (only `leadId`, `timestamp`, `tier`, `brandId`, `score`, `quizAnswers`, `consentTimestamp`)
- [ ] Consent captured before lead submit
