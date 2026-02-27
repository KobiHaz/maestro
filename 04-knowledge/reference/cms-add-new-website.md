# CMS — Add New Website (Vertical)

> Full guide was in project `docs/ADD_NEW_WEBSITE_GUIDE.md`. Key steps:

## Checklist

1. **Config:** `packages/vertical-configs/{verticalId}/config/vertical.json` — id, name, domain, domainAliases
2. **Firestore:** `verticals/{verticalId}` doc with domain
3. **Segment:** `verticals/{verticalId}/segments/default` (optional)
4. **CORS:** `apps/functions/src/config/cors.ts` — add domains to ALLOWED_ORIGINS
5. **Firebase Hosting:** `.firebaserc` target; create site in Console; add custom domain
6. **Auth:** Firebase Auth + GCP OAuth — authorized domains
7. **Seed:** `pnpm run seed:manifests`
8. **Components:** Admin Panel — create hero, slots, footer, etc.
9. **Deploy:** `firebase deploy --only hosting:{target}`

## Paths

- Domain resolution: Firestore `verticals` + `vertical.json` (not configs/domains.json)
- CORS: `apps/functions/src/config/cors.ts`
- Component levels: see `cms-architecture.md`
