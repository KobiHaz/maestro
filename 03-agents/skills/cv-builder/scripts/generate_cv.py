#!/usr/bin/env python3
"""
CV Builder — JSON → styled PDF
Usage: python3 generate_cv.py <input.json> <output.pdf>

JSON schema: see cv-builder.md Step 3
Design: orange header, two-column (left 175pt / right fills page), one page A4
"""

import json
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# ── Colours ──────────────────────────────────────────────────────────────
ORANGE = colors.HexColor("#F07B3F")
DARK   = colors.HexColor("#2C2C2C")
MID    = colors.HexColor("#555555")
LIGHT  = colors.HexColor("#888888")
WHITE  = colors.white

# ── Layout constants ─────────────────────────────────────────────────────
W, H       = A4
MARGIN_L   = 30
MARGIN_R   = 30
LEFT_W     = 175
RIGHT_X    = MARGIN_L + LEFT_W + 18
RIGHT_W    = W - RIGHT_X - MARGIN_R
HEADER_H   = 100
BOTTOM_PAD = 28   # minimum y before overflow is declared

# ─────────────────────────────────────────────────────────────────────────
# Drawing helpers
# ─────────────────────────────────────────────────────────────────────────

def section_title(c, x, y, text):
    spaced = "  ".join(text.upper())
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(DARK)
    c.drawString(x, y, spaced)
    tw = c.stringWidth(spaced, "Helvetica-Bold", 8.5)
    c.setStrokeColor(DARK)
    c.setLineWidth(0.6)
    c.line(x, y - 3, x + tw, y - 3)
    return y - 16


def wrap_text(c, x, y, text, width, font="Helvetica", size=8,
              color=MID, line_height=11):
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    line = ""
    for word in words:
        test = (line + " " + word).strip()
        if c.stringWidth(test, font, size) <= width:
            line = test
        else:
            c.drawString(x, y, line)
            y -= line_height
            line = word
    if line:
        c.drawString(x, y, line)
        y -= line_height
    return y


def bullet_lines(c, x, y, items, width, size=8, line_height=11.5):
    bx = x + 9
    for item in items:
        c.setFillColor(DARK)
        c.circle(x + 2.5, y + 2.5, 1.5, fill=1, stroke=0)
        y = wrap_text(c, bx, y, item, width - 9, size=size,
                      line_height=line_height, color=MID)
        y -= 2
    return y


def job_entry(c, x, y, title, company, period, bullets, width):
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(DARK)
    c.drawString(x, y, title.upper() + "  |  " + company.upper())
    y -= 12
    c.setFont("Helvetica", 7.5)
    c.setFillColor(LIGHT)
    c.drawString(x, y, period)
    y -= 13
    y = bullet_lines(c, x, y, bullets, width)
    return y - 6


# ─────────────────────────────────────────────────────────────────────────
# Column renderers
# ─────────────────────────────────────────────────────────────────────────

def draw_header(c, data):
    c.setFillColor(ORANGE)
    c.rect(0, H - HEADER_H, W, HEADER_H, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 32)
    c.drawString(MARGIN_L, H - 50, data["name"])
    title_spaced = "  ".join(data["title"].upper())
    c.setFont("Helvetica", 9.5)
    c.drawString(MARGIN_L + 2, H - 70, title_spaced)


def draw_left(c, data):
    x = MARGIN_L
    y = H - HEADER_H - 28

    # Contact
    y = section_title(c, x, y, "Contact")
    icons = {"phone": "☎", "email": "✉", "linkedin": "⊕", "github": "⊕"}
    for key, icon in icons.items():
        val = data["contact"].get(key, "")
        if val:
            c.setFont("Helvetica", 7.5)
            c.setFillColor(DARK)
            c.drawString(x, y, f"{icon}  {val}")
            y -= 12
    y -= 8

    # Education
    edu = data["education"]
    y = section_title(c, x, y, "Education")
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(DARK)
    c.drawString(x, y, edu["degree"])
    y -= 11
    c.setFont("Helvetica", 7.5)
    c.setFillColor(MID)
    y = wrap_text(c, x, y, edu["school"], LEFT_W - 5)
    c.drawString(x, y, edu["years"])
    y -= 18

    # Military
    mil = data.get("military")
    if mil:
        y = section_title(c, x, y, "Military Service")
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(DARK)
        y = wrap_text(c, x, y, mil["unit"].upper(), LEFT_W - 5,
                      font="Helvetica-Bold", size=8, color=DARK)
        y = wrap_text(c, x, y, mil["description"], LEFT_W - 5)
        c.setFont("Helvetica", 7.5)
        c.setFillColor(MID)
        c.drawString(x, y, mil["years"])
        y -= 18

    # Volunteer
    vol = data.get("volunteer")
    if vol:
        y = section_title(c, x, y, "Volunteer")
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(DARK)
        c.drawString(x, y, f"{vol['title'].upper()}  |  {vol['org'].upper()}")
        y -= 11
        c.setFont("Helvetica", 7.5)
        c.setFillColor(LIGHT)
        c.drawString(x, y, vol["period"])
        y -= 12
        y = bullet_lines(c, x, y, vol["bullets"], LEFT_W - 5)
        y -= 8

    # Interests
    interests = data.get("interests", [])
    if interests:
        y = section_title(c, x, y, "Interests")
        for item in interests:
            c.setFont("Helvetica", 7.5)
            c.setFillColor(MID)
            c.drawString(x, y, f"•  {item}")
            y -= 11

    return y


def draw_right(c, data):
    x = RIGHT_X
    y = H - HEADER_H - 28
    w = RIGHT_W

    # Profile
    y = section_title(c, x, y, "Profile")
    y = wrap_text(c, x, y, data["profile"], w, size=8.5,
                  color=MID, line_height=12.5)
    y -= 14

    # Experience
    y = section_title(c, x, y, "Experience")
    for job in data["experience"]:
        y = job_entry(c, x, y,
                      job["title"], job["company"],
                      job["period"], job["bullets"], w)

    # Skills
    skills = data.get("skills", [])
    if skills:
        y -= 4
        y = section_title(c, x, y, "Tools & Skills")
        for row in skills:
            label = row["label"] + ":"
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(DARK)
            lw = c.stringWidth(label + "  ", "Helvetica-Bold", 8)
            c.drawString(x, y, label)
            c.setFont("Helvetica", 8)
            c.setFillColor(MID)
            c.drawString(x + lw, y, row["value"])
            y -= 12

    return y


# ─────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────

def build(input_path: str, output_path: str):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    c = canvas.Canvas(output_path, pagesize=A4)
    c.setTitle(f"{data['name']} – {data['title']}")

    draw_header(c, data)
    left_bottom  = draw_left(c, data)
    right_bottom = draw_right(c, data)

    lowest = min(left_bottom, right_bottom)
    if lowest < BOTTOM_PAD:
        print(f"WARNING: content may overflow page (lowest y={lowest:.1f}). "
              "Shorten profile or reduce bullets.", file=sys.stderr)

    c.save()
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: generate_cv.py <input.json> <output.pdf>")
        sys.exit(1)
    build(sys.argv[1], sys.argv[2])
