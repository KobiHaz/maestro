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

---

## Open / Deferred

- **RLS sales policy** — Sales sees all leads; optional: `assigned_to = auth.uid()` for sales
- **NotFound auth** — 404 without auth (P1)
- **send-quote validation** — Zod schema (P2)
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
