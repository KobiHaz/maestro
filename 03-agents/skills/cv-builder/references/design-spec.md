# CV Design Specification

Reference design: `Kobi Hazout CV.pdf` (Desktop/CV/)
Generator: `scripts/generate_cv.py` (ReportLab, A4)

## Visual identity

| Element | Value |
|---|---|
| Header background | `#F07B3F` (orange) |
| Header text | White, name 32pt bold, title 9.5pt spaced |
| Body text dark | `#2C2C2C` |
| Body text mid | `#555555` |
| Timestamps / labels | `#888888` |
| Page size | A4 (595 × 842 pt) |

## Layout

```
┌─────────────────────────────────────────────────┐
│  ORANGE HEADER — Name + Title                   │ 100pt
├──────────────────┬──────────────────────────────┤
│  LEFT col 175pt  │  RIGHT col (fills remainder) │
│  Contact         │  Profile                     │
│  Education       │  Experience                  │
│  Military        │  Tools & Skills              │
│  Volunteer       │                              │
│  Interests       │                              │
└──────────────────┴──────────────────────────────┘
```

- Left column: `x = 30`, width `175pt`
- Right column: `x = 223`, width `~342pt`
- Vertical gap between columns: `18pt`
- Top of columns: `H - 100 - 28 = y_start`

## Section titles

- Font: `Helvetica-Bold` 8.5pt
- Text: letter-spaced with double-space between each char (`"  ".join(text)`)
- Underline: 0.6pt stroke, same width as text, 3pt below baseline
- Spacing after title: `−16pt` from title baseline

## Job entries (right column)

```
TITLE UPPERCASE  |  COMPANY UPPERCASE   ← Helvetica-Bold 8.5pt, DARK
PERIOD                                  ← Helvetica 7.5pt, LIGHT
• Bullet one                            ← 8pt, MID, wrapped to col width
• Bullet two
```

Gap between jobs: `−6pt` after last bullet.

## Bullets

- Dot: filled circle r=1.5pt at `(x+2.5, y+2.5)`
- Text starts at `x+9`
- Line height: `11.5pt`
- Gap after last bullet in block: `−2pt`

## One-page rule

Content must stay above `y = 28pt` (BOTTOM_PAD).
The script emits a WARNING if either column goes below this threshold.
Claude must shorten content before re-running if WARNING appears.

## Fonts

Standard PDF built-ins only (no TTF embedding required):
- `Helvetica-Bold`
- `Helvetica`
