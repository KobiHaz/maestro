---
project: source6681
type: plans-and-tasks
updated: 2026-03-11
---

# source6681 — תוכניות ומשימות

> **מקור יחיד:** [[../04-knowledge/reference/source6681-action-plan|source6681-action-plan]] — כל המשימות, העדיפויות והתוכנית במקום אחד.

## AI enrichment: Groq fallback + single call (2026-03-11)

Done: `enrichWithAI` returns era, dimensions, Hebrew in one call. Primary: Gemini/Lovable; fallback: Groq when Gemini fails or quota exceeded. Add `GROQ_API_KEY` in Supabase Edge Functions for fallback.

## Stitch design fetch (2026-03-08)

Plan: fetch 4 Stitch screens (images + code) for 66.81 Archive — Landing (desktop/mobile), Product View (desktop/mobile). Plan in `docs/plans/2026-03-08-stitch-screens-fetch.md`. Done.

## Stitch design implementation (2026-03-08)

Plan: implement Stitch design on branch `feat/stitch-design-v2` — typography (Bodoni Moda, accent-gold), hero ("Authentic Luxury Curated Vintage"), editor's picks section header, footer (משלוחים לכל הארץ, 4-col links). Build passes. Ready for PR.
