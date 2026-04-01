---
project: casino-funnels
type: rollout-plan
partner: Crown Coins (affiliates_social / leadsl)
status: Draft
last_updated: 2026-03-31
language: en
related:
  - "[[PRD-clarity-insights-agent]]"
---

# Rollout plan — partner guidelines (tracking, compliance, geo)

This document operationalizes the partner email (Yuval): URL templates, disclaimer, restricted states, and product reference data. **It is not legal advice.**

---

## 1. Objectives

| Objective | Success criterion |
|-----------|-------------------|
| Clear source attribution | Each channel/campaign uses a unique `utm_medium` and a real `click_id` (no literal placeholders in live links) |
| Funnel consistency | `landing` matches the actual destination (`direct_su` / `direct_reg` / default homepage flow) |
| Lander compliance | Required disclaimer text is visible + pre-launch approval obtained |
| Geo safety | No paid/organic promotion targeted at restricted states; copy does not imply availability where prohibited |
| Unified analytics story | Event/tag names align with PRD Appendix A when measuring the same journey in Clarity |

---

## 2. Link matrix (source of truth)

### 2.1 Templates (replace placeholders before any live use)

| Use case | Template |
|----------|----------|
| Sign up | `https://crowncoinscasino.com/?landing=direct_su&utm_source=affiliates_social&utm_campaign=leadsl&utm_medium={site_name}&click_id={click_id}` |
| Homepage | `https://crowncoinscasino.com/?utm_source=affiliates_social&utm_campaign=leadsl&utm_medium={site_name}&click_id={click_id}` |
| Reg page | `https://crowncoinscasino.com/?landing=direct_reg&utm_source=affiliates_social&utm_campaign=leadsl&utm_medium={site_name}&click_id={click_id}` |

**Rules:**

- **`utm_medium`** — One stable value per source (e.g. `reddit`, `twitter_x`, `facebook_group_name`). Do not reuse the same placement with different values without documenting why.
- **`click_id`** — Use the ad/post platform’s click identifier when available. If none exists, define a policy (e.g. campaign+date surrogate) and **never** ship links that still contain `{click_id}`.
- **Internal mapping table** — Maintain: `utm_medium` → display name → owner.

### 2.2 Your funnel (if traffic is not direct to the partner domain)

If users hit your domain or app before the final redirect:

- Preserve the same UTM query parameters, or issue a 302 redirect that forwards the **full** query string.
- Ensure Clarity/GA4 still see the intended `landing` after the final navigation (or record a custom dimension that stores the original value).

---

## 3. Lander compliance

**Disclaimer text (per partner):**

> NO PURCHASE NECESSARY.  
> VOID WHERE PROHIBITED BY LAW.  
> SEE T&CS. 19+

**Process:**

1. **Placement** — Footer or other prominent location per partner requirements; readable size/contrast.
2. **Links** — Wire to your in-app Terms & Privacy pages (or partner pages if the lander is hosted only by them).
3. **Before the first campaign** — Send a sample lander (URL or screenshot) to Yuval for approval.

---

## 4. Geography and marketing

**Restricted states for marketing (partner list):**  
Idaho, Michigan, Nevada, Washington, Montana, Louisiana, Connecticut, New York, New Jersey, California, Indiana.

**Actions:**

- Configure ad platforms with geo exclusions or allow-lists consistent with your legal strategy.
- Audit that no targeting preset contradicts the list (e.g. “entire US” without exclusions).
- Brief content teams: do not promise availability in restricted states; avoid globally misleading copy.

**Product notes (support / internal copy only):**  
NY/FL redeem cap $5,000; Skrill up to $14,500 per transaction — do not publish in marketing without compliance sign-off.

---

## 5. Alignment with Clarity and the PRD

Goal: same language between GA4/Meta and Clarity ([[PRD-clarity-insights-agent]] Appendix A).

| Action | Owner |
|--------|--------|
| Mirror `wheel_ab_exposure`, `spin_start`, `spin_button_click`, … to Clarity | Stage 2 in `plans-and-tasks` |
| Filter recordings by `utm_medium` / `landing` (where Clarity or export supports it) | Define session tag or custom dimension per project capability |
| Bump dictionary version in PRD after any rename | Dev + PRD maintainer |

---

## 6. Brand and content

- [ ] Brandbook (Google Slides) — confirm access for design.
- [ ] Claims list (500+ games, daily rewards, min purchase, etc.) — **do not publish** without checking an up-to-date partner doc.
- [ ] Support channels: `support@crowncoinscasino.com`, `?ao=support`, [help center](https://help.crowncoinscasino.com/en/) — use in help/footer content if relevant.

---

## 7. Pre-flight checklist (every new campaign)

- [ ] New `utm_medium` registered in the mapping table
- [ ] No `{site_name}` / `{click_id}` in live ad links
- [ ] `landing` matches the destination experience
- [ ] Disclaimer displayed as required
- [ ] Geo targeting checked against the restricted list
- [ ] Sample sent for approval if first campaign or material lander change
- [ ] Critical funnel events firing in Clarity (once implemented)

---

## 8. Suggested execution order

1. **Internal policy** — `utm_medium` table, `click_id` rules, owner for partner approvals.
2. **Technical** — Query preservation on redirects; disclaimer in relevant components; preview all final URLs.
3. **Analytics** — Clarity event parity (overall project Stage 2).
4. **Launch** — Yuval approval → limited spend → monitor Clarity/GA4 by `utm_medium`.

---

## 9. Open items / external dependencies

- Internal legal sign-off on copy and geo (in addition to the partner list).
- Partner written approval on the lander sample.
- Process for updates if the partner changes URLs, campaign names, or state lists.
