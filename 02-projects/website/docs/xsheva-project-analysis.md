# Xsheva (xsheva.com) — Project Analysis

> **Source:** https://xsheva.com/ | **Analysis date:** 2025-03-03

---

## 1. Stitch Project Creation

**Status:** ⚠️ The Stitch MCP server (`user-stitch`) is **not** enabled in this workspace. I cannot create a Stitch project programmatically until you enable it.

**Stitch** = Google's AI design tool (labs.google/stitch) that turns text prompts into UI designs and frontend code. The MCP tools (`create_project`, `generate_screen_from_text`, etc.) would let me create a project titled "Xsheva — xsheva.com" and generate screens from prompts.

**To enable:** Add the Stitch MCP server to your Cursor MCP config so that `user-stitch` appears in the list of available servers.

---

## 2. Live Site Analysis (xsheva.com)

### Purpose
- **Lead generation** for Xsheva — CRM, automations, affiliate services
- US market, high-tech, results-driven brand
- Tagline: "Multiply Everything"

### Structure
| Section | Content |
|---------|---------|
| **Hero** | X logo, "sheva: Multiply Everything.", subtitle, CTA |
| **Services** | Precision Targeting, Autonomous Systems, Infinite Scale, Decoded Demand |
| **Approach** | The Growth Variable — Precision, Scale, Modernity, Exclusivity |
| **Contact** | Form (FormSubmit.co) — Name, Email, Message |

### Brand
- **Colors:** Deep Space Black (#000), Stark White (#FFF), Neon Orange (#FF6B35)
- **Fonts:** Space Grotesk (headings), Inter (body)
- **Tone:** Direct, minimalist, confident, intriguing

### Tech (live site)
- Static HTML + CSS (no React on live — Maestro brief mentions React 19/Vite stack as target)
- FormSubmit for contact form
- Firebase initialized (via scripts/main.js)
- Smooth scroll, simple IntersectionObserver for scroll reveal

---

## 3. Local Codebase Analysis

### Structure
```
website/
├── xsheva/           ← main app
│   ├── index.html
│   ├── scripts/main.js
│   ├── scripts/firebase.js
│   ├── styles/main.css
│   ├── public/
│   ├── package.json
│   └── firebase.json
├── README.md
└── .cursorrules
```

### Current Stack
- **Build:** Vite 6
- **Runtime:** Vanilla JS (no React in package.json)
- **Hosting:** Firebase Hosting
- **Form:** FormSubmit.co (external)
- **Dependencies:** `firebase` ^11.0.0

### Gap vs Maestro Brief
The project brief states: React 19, TypeScript, Tailwind v4, Framer Motion, etc. The current codebase is **vanilla HTML/CSS/JS** with Vite. So either:
- The live site is legacy/static, and the full stack is planned or elsewhere, or
- The brief is aspirational and the current implementation is intentionally minimal.

### Design System (main.css)
- CSS custom properties for colors, typography, spacing
- Responsive breakpoints: 768px, 480px
- Scroll-reveal on `.service-card` and `.value-item`
- Fixed header with backdrop blur

---

## 4. Recommendations for Stitch

When Stitch MCP is enabled, use prompts like:

1. **Desktop hero:** "Landing hero for Xsheva: Multiply Everything. Black background, orange accent #FF6B35, Space Grotesk typography, minimalist, premium. CTA: Get Started."
2. **Services grid:** "4-card grid: Precision Targeting, Autonomous Systems, Infinite Scale, Decoded Demand. Dark theme, orange accents, modern B2B SaaS style."
3. **Contact form:** "Minimal contact form: Name, Email, Message, Submit. Dark theme, orange focus states."

Theme settings for Stitch: `colorMode: DARK`, `customColor: #FF6B35`, `headlineFont: SPACE_GROTESK`, `bodyFont: INTER`.

---

## 5. Summary

| Aspect | Finding |
|--------|---------|
| **Stitch project** | Blocked: MCP not enabled |
| **Live site** | Static, branded, functional — matches Maestro brand |
| **Codebase** | Vanilla stack; differs from Maestro React/Tailwind brief |
| **Design system** | Well-defined in main.css; ready for Stitch prompts |
