# CMS — Security Audit Reference

> Date: 2026-02-24. OWASP Top 10 + project-specific.

## Risk Summary

| Severity | Count |
|----------|-------|
| Critical | 1 |
| High | 3 |
| Medium | 6 |
| Low | 4 |

## Critical

**1.1 Postback No HMAC** — `postbackHandler.ts` accepts unauthenticated postbacks. Remediation: Implement HMAC per `POSTBACK_HMAC_DESIGN.md`, Secret Manager.

## High

**2.1 Admin Collection Mismatch** — `adminEmails.ts:29` queries `'admin'` but collection is `admin_user`. Change to `collection(db, 'admin_user')`.

**2.2 report-error Not Wired** — Add rewrite in `firebase.json` for `/api/report-error` → `reportFrontendError` (per audit plan).

**2.3 Postback No Rate Limit** — Add rate limiting (e.g. 200 req/min per IP).

## Medium (Key)

- CORS: `registerClickEvent` uses `cors: true` → restrict to `ALLOWED_ORIGINS`
- Error leakage: Sanitize error messages to clients
- Path traversal: Validate paths in storage handlers

## Positive

- Firestore rules: Least privilege ✓
- Admin claims ✓
- DOMPurify ✓
- Payload sanitization ✓

## Reference

- Full report in project: `docs/SECURITY_AUDIT_REPORT_2026-02.md` (pre-deletion)
- Postback design: `docs/POSTBACK_HMAC_DESIGN.md`
