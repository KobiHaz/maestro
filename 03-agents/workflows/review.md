---
name: review
description: Comprehensive code review task.
---

# /review - Code Review Mode

Perform comprehensive code review. Be thorough but concise.

**Tools in vault:** Use relevant specialists from `03-agents/specialists/` (frontend-specialist, backend-specialist, security-auditor) per code type. Review checklists in `04-knowledge/` if relevant.

## Check For:

- **Logging** - No `console.log` statements, uses proper logger with context.
- **Error Handling** - Try-catch for async, centralized handlers, helpful messages.
- **TypeScript** - No `any` types, proper interfaces, no `@ts-ignore`.
- **Production Readiness** - No debug statements, no TODOs, no hardcoded secrets.
- **React/Hooks** - Effects have cleanup, dependencies complete, no infinite loops.
- **Performance** - No unnecessary re-renders, expensive calcs memoized.
- **Security** - Auth checked, inputs validated, RLS policies in place.
- **Accessibility** - Elements meet ARIA standards and WCAG 2.1 compliance.
- **Architecture** - Follows existing patterns, code in correct directory.

## Output Format

### ✅ Looks Good
- [Item 1]
- [Item 2]

### ⚠️ Issues Found
- **[Severity]** [[File:line](File:line)] - [Issue description]
  - Fix: [Suggested fix]

### 📊 Summary
- Files reviewed: X
- Critical issues: X
- Warnings: X

## Severity Levels
- **CRITICAL** - Security, data loss, crashes.
- **HIGH** - Bugs, performance issues, bad UX.
- **MEDIUM** - Code quality, maintainability.
- **LOW** - Style, minor improvements.
