# Base Coding Standards

> **Applies:** All projects. Project-specific standards extend this base.
> **Source:** V2 cleaned & expanded coding standards.

Project standards (e.g. `crm-standards.md`) add project-specific rules only. Load both: base + project.

**חוק:** אף פרויקט לא דורס את הבסיס. אם קוד בפרויקט לא עומד — משנים את הקוד, לא את החוקים.

**הערה:** אין קובץ `coding-standards.md` נפרד — הבסיס כאן בלבד.

**פרויקטי Node/CLI (ללא React):** סעיפים 7 (React & Hooks), 11 (State), 14 (File & Folder Structure) לא חלים. שאר הסעיפים חלים.

---

## 1. General Principles

- Prefer clarity over cleverness; code should be obvious to the next developer.
- Prefer composition over inheritance and configuration over hardcoded behavior.
- Make tradeoffs explicit in code comments (e.g. "Perf over readability here because…").

## 2. Naming

**Data fetching:**
- `get*` for pure, synchronous, non-IO helpers (e.g. `getLeadScore`).
- `fetch*` for network calls (e.g. `fetchLeads`).
- `load*` for cache/bootstrap flows (e.g. `loadInitialFilters`).

**Booleans:** Always start with `is*`, `has*`, `can*`, or `should*`.

**Constants:**
- Primitives: `SCREAMING_SNAKE_CASE`.
- Config objects/arrays: PascalCase (e.g. `LeadScoreWeights`).

**React:**
- Components: PascalCase.
- Hooks: `use` + PascalCase (e.g. `useLeadsQuery`).
- Utilities/libraries: camelCase.
- Services: camelCase + `Service` suffix (e.g. `leadService`, `productService`).

## 3. TypeScript

- Never use `any`. If needed, use `unknown` and narrow, or define a proper type.
- Prefer `interface` for object shapes; `type` for unions, aliases, and mapped/utility types.
- Avoid `as X` casts unless truly unavoidable; when used, add a short comment explaining why.
- Avoid non-null assertions (`!`) except at clear, validated boundaries.
- All function parameters and return types must be explicitly typed in public APIs (exports, hooks, services).
- Allow inference for internal variables and intermediate values; do not over-annotate.
- Prefer `readonly` where possible (props, arrays, maps that should not mutate).
- Use `unknown` for external inputs (API, forms) and validate into safe, typed shapes.
- Use `undefined` over `null` in our own code; accept `null` only when required by Supabase or other external APIs.
- Imports: Always at top of file. No inline imports in function bodies.
- Switch (unions/enums): Use exhaustive handling; `never` in default case so new variants cause compile-time failure.

## 4. Data & Transformations

- Normalize data only at the fetch boundary (query function / service layer).
- Components must receive clean, camelCase, ready-to-use data; no normalization or heavy transforms in components.
- When API may return a single item or an array, normalize to array at the boundary: `const items = Array.isArray(x) ? x : [x];`
- Keep domain logic (scoring, mapping, filtering) in utils/services, not inside components.
- **Async state:** Use TanStack Query for all server data. Do not manage manual loading flags for server data outside Query.

## 5. Complexity & Collections

- Target O(1) for repeated lookups; use `Map` or `Record` instead of `array.find()` inside loops.
- Use `array.find()` only for one-off lookups that are not in hot paths.
- Use `Set` for membership checks and deduplication.
- Use arrays for ordered sequences; if order doesn't matter, consider `Set` or `Map`.
- Keep functions and components focused to avoid accidental nested loops / hidden N+1 work.

## 6. Functions & Components

- One function = one responsibility; if it does more than one thing, split it.
- Max ~30 lines per function; if it grows, extract helpers.
- Max 3 parameters; if you need more, pass a single options object.
- Put guard clauses first and return early; avoid deep nesting.
- Pure utils must have no side effects (no logging, no network, no state).
- Side effects live in services and hooks, not in pure utils or presentational components.

**Components:**
- Aim for max ~150 lines. If larger, extract sub-components or hooks.
- Keep JSX shallow and readable; extract complex pieces.
- Avoid passing deeply nested props; use cohesive prop objects.

## 7. React & Hooks

- Follow the Rules of Hooks strictly; never call hooks conditionally or inside loops.
- Keep `useEffect` minimal: prefer derived values (memoized selectors) over effects when possible.
- Avoid business logic in effects; move it into services/utils.
- Always provide complete dependency arrays.
- Use `useCallback` / `useMemo` only when profiling or clear re-render issues justify it; do not sprinkle them by default.
- Avoid local state duplication of server state; derive from TanStack Query data when possible.

## 8. Security

- Never log sensitive data (tokens, passwords, emails, PII) — even in development.
- Validate and sanitize all user inputs before writing to the DB.
- Never expose environment variables to the client unless prefixed with `VITE_PUBLIC_`.
- Perform auth and authorization checks on the server; client guards are UX only, not security.
- Do not trust any client-provided values (IDs, roles, prices); validate on the server side.

## 9. Performance

- Avoid N+1 queries: batch or join at the database/query layer.
- Use TanStack Query features (caching, pagination, prefetching) instead of manual data-fetch optimizations.
- Use `useMemo` / `useCallback` only where there is a proven or measurable benefit.
- Heavy lists must use virtualization (e.g. `@tanstack/react-virtual` or similar).
- Images: Always set explicit width/height. Use lazy loading for below-the-fold. Prefer modern formats (WebP) where supported.

## 10. Error Handling & Logging

**Mutations:** Use `onError: (error) => toast.error("Failed to X: " + error.message)` with clear, user-friendly messages.

**Async fetchers:** Wrap in try/catch, log the error, and return `null`/`[]` on failure where safe.

- Never leave empty catch blocks; always handle, log, or rethrow.
- When error type is unknown: `const message = error instanceof Error ? error.message : String(error);`
- Critical failures: Throw and let a top-level error boundary / handler decide.
- Use a central logging service for errors that matter in production.

## 11. State Management

- Server state: TanStack Query.
- Global/cross-cutting concerns: React Context (or provider components) when actually shared across multiple screens.
- Local UI state: `useState` or `useReducer` inside a single component.
- Persisted UI state (table preferences, filters, theme): Use a dedicated hook that syncs with Supabase or localStorage.
- Do not use Redux or Zustand in this project.

## 12. Testing

- Every utility function must have at least one unit test.
- Every mutation must have: a happy-path test; an error-path test.
- Test file lives next to the source file and mirrors its name: `leadScore.test.ts`.
- Test behavior and outputs, not implementation details.
- For hooks/components, test observable behavior (rendered output, callbacks) rather than React internals.

## 13. Dead Code & Cleanliness

- No unused imports, variables, or functions; clean them up before committing.
- Do not comment out code — delete it. Use Git history if needed.
- No magic numbers or strings in logic — define named constants.
- Keep files focused; if a file handles multiple unrelated concerns, split it.

## 14. File & Folder Structure

- `components/<feature>/` — feature-specific components.
- `components/ui/` — shared, low-level primitives (e.g. shadcn components).
- `hooks/` — reusable custom hooks (cross-feature).
- `lib/` — one-off utilities, helpers, query keys, or framework-specific glue.
- `utils/` — pure domain logic (score, sort, format).
- `services/` — data fetching and transformations (API clients, mappers).
- `types/` — shared TypeScript interfaces and types.
- Use `@/` alias for absolute imports.
- Keep index files small; avoid giant "barrel files" that re-export everything blindly.

## 15. Exports

- Use default exports for page-level or feature root components.
- Use named exports for utilities, shared types, and constants.
- Avoid mixing default and named exports in the same file when not necessary.

## 16. Tooling & Enforcement

- Use ESLint + TypeScript + Prettier to enforce these rules where possible.
- Enable strict TypeScript (`strict: true`) and React-related ESLint rules.
- Use pre-commit hooks (e.g. lint-staged) to run lint/tests on changed files.
- CI must fail on TypeScript errors, ESLint errors, or test failures.

## 17. Documentation & Comments

- Keep README-level docs for: project architecture; main conventions and deviations from defaults.
- Use comments for: non-obvious decisions; workarounds and TODOs with owner + date + context.
- Do not comment "what" the code does if it's obvious; comment "why".

## 18. Accessibility & UX

- Prefer semantic HTML elements (`button`, `nav`, `main`, etc.).
- Always provide accessible names for interactive elements (`aria-label`, etc. when needed).
- Ensure keyboard navigation works for critical flows (forms, dialogs, menus).
