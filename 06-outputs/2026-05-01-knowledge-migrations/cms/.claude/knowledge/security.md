# cms — Security Reference

Last audit: 2026-02-24

## Open Issues

### Critical
**Postback No HMAC** (`postbackHandler.ts`)
- Accepts conversion postbacks without authentication
- Fix: Implement HMAC-SHA256 per `docs/POSTBACK_HMAC_DESIGN.md` + Secret Manager

### High
**Admin collection mismatch** (`adminEmails.ts:29`)
- Code queries `'admin'` but collection is `'admin_user'`
- Fix: `collection(db, 'admin_user')` — one-line change

**`report-error` not wired** (`firebase.json`)
- `/api/report-error` endpoint not connected to `reportFrontendError` function
- Fix: Add rewrite in `firebase.json`

**Postback no rate limit**
- Fix: 200 req/min per IP (Cloud Functions rate limiting)

### Medium
**CORS too permissive** (`registerClickEvent`)
- Uses `cors: true` → allow all origins
- Fix: Restrict to `ALLOWED_ORIGINS` in `apps/functions/src/config/cors.ts`

**Error leakage** — sanitize error messages before sending to clients
**Path traversal** — validate paths in storage handlers

## Positive

- Firestore rules: Least privilege ✓
- Admin custom claims ✓
- DOMPurify for user content ✓
- Payload sanitization ✓

## When Adding New Endpoints

- [ ] Add to ALLOWED_ORIGINS if needed
- [ ] Authenticate admin endpoints with custom claims
- [ ] Rate limit public endpoints
- [ ] Sanitize error responses
