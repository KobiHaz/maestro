# cms — Add New Vertical Checklist

When adding a new comparison/affiliate website vertical:

1. **Config:** `packages/vertical-configs/{verticalId}/config/vertical.json`
   ```json
   { "id": "verticalId", "name": "Display Name", "domain": "domain.com", "domainAliases": [] }
   ```

2. **Firestore:** Create `verticals/{verticalId}` document with `domain` field

3. **Segment:** Create `verticals/{verticalId}/segments/default` (optional baseline)

4. **CORS:** `apps/functions/src/config/cors.ts` — add domain to `ALLOWED_ORIGINS`

5. **Firebase Hosting:** `.firebaserc` hosting target + create site in Firebase Console + add custom domain

6. **Auth:** Firebase Auth + GCP OAuth — add domain to Authorized Domains

7. **Seed:** `pnpm run seed:manifests`

8. **Components:** Admin Panel — create hero, slots, footer, header components

9. **Deploy:** `firebase deploy --only hosting:{target}`

## Key Paths

- Domain → vertical resolution: Firestore `verticals` collection + `vertical.json` (not `configs/domains.json`)
- CORS config: `apps/functions/src/config/cors.ts`
- Component levels: see `architecture.md`
