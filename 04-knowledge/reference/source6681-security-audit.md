---
project: source6681
type: reference
---

# source6681 — Security Audit

> From project review 2026-02-23. Status as of optimization.

## Implemented

- CRON_SECRET for check-dropship-status cron path
- Admin Bearer for manual check-dropship
- RLS: products readable by all, writable by admins
- Storage: admin-only policies (verify)
- Coupon trigger: increment on order insert (protected)

## Gaps / Recommendations

| Item | Priority | Action |
|------|----------|--------|
| Admin route | P2 | Add `is_admin` check in Admin.tsx before dashboard |
| Storage policies | P1 | Restrict product bucket to `is_admin(auth.uid())` |
| create_order RPC | P1 | Not implemented; needed for checkout |
| Coupon usage | P1 | Ensure trigger, not client-callable RPC |
