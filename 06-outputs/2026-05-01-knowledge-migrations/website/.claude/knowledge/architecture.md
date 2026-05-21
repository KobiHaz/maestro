# website (Xsheva) — Architecture

## Stack

React 19, TypeScript, Vite, Tailwind v4, Framer Motion, React Hook Form, TanStack Query
Firebase (Firestore, Functions, Auth, Hosting), ImageKit, Sentry

## Key Packages

| Package | Purpose |
|---------|---------|
| `@cms/shared` | Shared components + utils with cms monorepo |
| `framer-motion` | Page/section animations |
| `react-hook-form` | Lead capture forms |
| `@tanstack/react-query` | Server state, caching |
| `imagekit-javascript` | Image transformations |

## Firebase Usage

- **Firestore:** Lead data, form submissions
- **Functions:** Backend processing, email triggers
- **Auth:** Admin access
- **Hosting:** Production deployment

## @cms/shared Integration

website imports from `@cms/shared` — this is a shared workspace package with the cms project.
Changes to shared package propagate to both website and cms verticals.
Always test both when modifying `@cms/shared`.

## TanStack Query Pattern

```ts
// Server state: TanStack Query (not useEffect + setState)
const { data, isLoading } = useQuery({
  queryKey: ['leads'],
  queryFn: fetchLeads,
});
```

## ImageKit Pattern

```ts
// Use ImageKit transformations for all images
const imageUrl = imagekit.url({
  path: '/hero.jpg',
  transformation: [{ width: 1200, quality: 80 }]
});
```

## Error Monitoring

Sentry captures unhandled errors + React ErrorBoundary crashes.
Firebase Analytics tracks page views + conversion events.
