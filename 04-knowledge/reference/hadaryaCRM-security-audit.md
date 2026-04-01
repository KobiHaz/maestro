# Security Audit — hadaryaCRM

**Date:** 23 February 2025  
**Reference:** Initial + Follow-up

---

## Verified Fixed ✓

- **Shopify token** — `VITE_SHOPIFY_STOREFRONT_TOKEN` from env
- **Passwords in scripts** — env vars only
- **ILIKE injection** — `escapeIlike` in Customers, GlobalCommandPalette, Leads, LeadDialog
- **XSS send-quote** — `escapeHtml` on all fields in send-quote
- **.env tracked** — removed from git
- **send-quote user_roles** — 2026-03-01: switched to `user_module_roles` (invite-user users can now send quotes)
- **payment-proofs bucket** — 2026-03-01: migration `20260301120000_payment_proofs_bucket.sql` + RLS

---

## Open / Deferred

- **scripts/add-ad-agency-users.js** — 2026-03-01: Fixed; now reads from ADD_AGENCY_USERS env
- **RLS sales policy** — Sales sees all leads; optional: `assigned_to = auth.uid()` for sales
- **NotFound auth** — 404 without auth (P1)
- **send-quote validation** — 2026-03-01: Zod schema added ✓
- **website-lead rate limiting** (P2)
- **LeadDialog** — `escapeIlike(digits)` for consistency (P2)

---

## Security Checklist

| Requirement | Status |
|-------------|--------|
| escapeIlike for all ILIKE | ✓ |
| escapeHtml in send-quote | ✓ |
| No secrets in code | ✓ |
| Auth on routes | ✓ |
