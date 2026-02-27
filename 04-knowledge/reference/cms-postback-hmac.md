# CMS — Postback HMAC Design

> Design only. Implementation deferred until affiliates support.

## Overview

HMAC verification for trusted affiliate postbacks. When enabled, invalid/missing signature → reject.

## Design

- **Header:** `X-Webhook-Signature` or `X-Postback-Signature`
- **Algorithm:** HMAC-SHA256 of raw query string or body
- **Secret:** Secret Manager `POSTBACK_HMAC_SECRET`
- **Enable:** `POSTBACK_HMAC_ENFORCE=true`

## Flow

1. Affiliate computes `HMAC-SHA256(secret, queryString)`, sends in header
2. Handler recomputes, timing-safe comparison
3. If `POSTBACK_HMAC_ENFORCE=false`: no verification (current)
4. If true and invalid: 401

## Rollout

1. Add secret (optional)
2. Deploy with `POSTBACK_HMAC_ENFORCE=false`
3. Coordinate with affiliate
4. Enable when ready
