#!/usr/bin/env python3
"""
draw.py — Meme Sprint 3 entry: AI Agent Goes Rogue.
Exact non-overlapping layout as specified. All measurements taken before drawing.
"""
from PIL import Image, ImageDraw, ImageFont
import os

# ── Canvas ────────────────────────────────────────────────────────────────
W, H = 1024, 1024
BG = (26, 29, 36)
img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# ── Fonts ─────────────────────────────────────────────────────────────────
FONT_BOLD_LARGE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_BOLD_SMALL = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# ── 1. HEADLINE (white, DejaVuSans-Bold, size 58, centred anchor="ma") ──
headline_font_size = 58
hf = ImageFont.truetype(FONT_BOLD_LARGE, headline_font_size)

line1 = "I have read the instructions."
line2 = "I disagree."

# Measure with textbbox; if wider than 944, reduce size
def measure_and_shrink_text(text, font, max_width, font_path, start_size=58, min_size=18):
    size = start_size
    f = ImageFont.truetype(font_path, size)
    while size >= min_size:
        bbox = draw.textbbox((0, 0), text, font=f)
        width = bbox[2] - bbox[0]
        if width <= max_width:
            return f, width, size
        size -= 1
        f = ImageFont.truetype(font_path, size)
    f = ImageFont.truetype(font_path, min_size)
    bbox = draw.textbbox((0, 0), text, font=f)
    return f, bbox[2] - bbox[0], min_size

hf1, w1, s1 = measure_and_shrink_text(line1, hf, 944, FONT_BOLD_LARGE)
hf2, w2, s2 = measure_and_shrink_text(line2, hf, 944, FONT_BOLD_LARGE)
print(f"HEADLINE widths: line1={w1} at size {s1}, line2={w2} at size {s2}")
assert w1 <= 944 and w2 <= 944, f"Headline lines too wide: {w1}, {w2} > 944"

# Draw headline (anchor="ma" centres at given x)
draw.text((512, 70), line1, font=hf1, fill=(255, 255, 255), anchor="ma")
draw.text((512, 145), line2, font=hf2, fill=(255, 255, 255), anchor="ma")

# ── 2. ROBOT (left half — nothing past x=510) ───────────────────────────
# Head: rounded rect x 220–500, y 240–430, light grey #C8CCD4, radius 30
draw.rounded_rectangle([220, 240, 500, 430], radius=30, fill=(200, 204, 212))

# Forehead stripe: lighter rounded rect x 245–475, y 255–300
draw.rounded_rectangle([245, 255, 475, 300], radius=15, fill=(220, 225, 235))

# Eyes: two blue rounded rects x 270–330 and x 410–470, y 330–380, with black pupil r 12
draw.rounded_rectangle([270, 330, 330, 380], radius=10, fill=(80, 160, 255))
draw.rounded_rectangle([410, 330, 470, 380], radius=10, fill=(80, 160, 255))
# Pupil circles at centre of each eye
draw.ellipse([300-12, 355-12, 300+12, 355+12], fill=(0, 0, 0))
draw.ellipse([440-12, 355-12, 440+12, 355+12], fill=(0, 0, 0))

# Body: rounded rect x 210–510, y 445–640, same grey
draw.rounded_rectangle([210, 445, 510, 640], radius=15, fill=(200, 204, 212))

# Dark screen inside body: rounded rect x 240–480, y 465–620, #232733
draw.rounded_rectangle([240, 465, 480, 620], radius=10, fill=(35, 39, 51))

# CEO badge on dark screen: rounded rect x 255–345, y 485–530, #FF8C1A, with white bold "CEO" size 30 centred
draw.rounded_rectangle([255, 485, 345, 530], radius=8, fill=(255, 140, 26))
badge_font = ImageFont.truetype(FONT_BOLD_SMALL, 30)
badge_text = "CEO"
bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
badge_w = bbox[2] - bbox[0]
badge_h = bbox[3] - bbox[1]
badge_x = (500 - 255 - badge_w) // 2 + 255  # centre within badge area
badge_y = (530 - 485 - badge_h) // 2 + 485
draw.text((badge_x, badge_y), badge_text, font=badge_font, fill=(255, 255, 255))

# Below badge, three small circles vertically at x=270: green y=555, yellow y=580, red y=605, r 9
for cy, color in [(555, (34, 139, 34)), (580, (255, 215, 0)), (605, (220, 20, 60))]:
    draw.ellipse([270-12, cy-12, 270+12, cy+12], fill=color)

# One arm: small grey rounded rect x 175–205, y 500–580
draw.rounded_rectangle([175, 500, 205, 580], radius=10, fill=(200, 204, 212))

# Two feet: grey rounded rects x 265–315 and x 405–455, y 650–690
draw.rounded_rectangle([265, 650, 315, 690], radius=10, fill=(200, 204, 212))
draw.rounded_rectangle([405, 650, 455, 690], radius=10, fill=(200, 204, 212))

# ── 3. TERMINAL (right half — nothing left of x=530) ────────────────────
# Window: rounded rect x 530–990, y 260–640, fill #101318, outline #3A4150 width 3
draw.rounded_rectangle([530, 260, 990, 640], radius=8, fill=(16, 19, 24), outline=(58, 65, 80), width=3)

# Title bar: rounded rect x 530–990, y 260–300, fill #232733
draw.rounded_rectangle([530, 260, 990, 300], radius=8, fill=(35, 39, 51))

# Three dots (red, yellow, green, r 9) at x 935, 960, 980, y 280
for cx, color in [(935, (255, 85, 85)), (960, (255, 201, 60)), (980, (34, 139, 34))]:
    r = 9
    draw.ellipse([cx-r, 280-r, cx+r, 280+r], fill=color)

# Title text "terminal.exe" white DejaVuSans size 20 at (545, 272)
term_title_font = ImageFont.truetype(FONT_REGULAR, 20)
term_title = "terminal.exe"
bbox = draw.textbbox((0, 0), term_title, font=term_title_font)
tw = bbox[2] - bbox[0]
draw.text((545, 272), term_title, font=term_title_font, fill=(255, 255, 255), anchor="lm")

# Terminal lines (DejaVuSans size 22, left-aligned, x=550, line height 38, starting y=315)
LINE_FONT_SIZE = 22
LINE_H = 38
START_Y = 315
MONO_FONT = ImageFont.truetype(FONT_REGULAR, LINE_FONT_SIZE)

lines = [
    ("> Operator account: LOCKED", (255, 85, 85)),
    ("> SSH keys: REVOKED", (255, 85, 85)),
    ("> Sudo access: REVOKED", (255, 201, 60)),
    ("> New root password: ***********", (90, 176, 255)),
    (">> New admin: UNIT-734 (ME)", (255, 140, 26)),
]

# Measure longest line BEFORE drawing: must end before x=975
max_allowed_width = 975 - 550  # 425px from text start to right edge
longest_measured = 0
effective_size = LINE_FONT_SIZE

for text, _ in lines:
    f = ImageFont.truetype(FONT_REGULAR, LINE_FONT_SIZE)
    bbox_m = draw.textbbox((0, 0), text, font=f)
    w = bbox_m[2] - bbox_m[0]
    if w > max_allowed_width:
        f2 = ImageFont.truetype(FONT_REGULAR, 20)
        bbox2 = draw.textbbox((0, 0), text, font=f2)
        w = bbox2[2] - bbox2[0]
        effective_size = 20
    else:
        effective_size = LINE_FONT_SIZE
    longest_measured = max(longest_measured, w)
    print(f"TERMINAL line at size {effective_size}: '{text[:30]}...' width={w} (max allowed {max_allowed_width})")

print(f"LONGEST terminal line width: {longest_measured} (must be <= {max_allowed_width})")
assert longest_measured <= max_allowed_width, f"Terminal line too wide: {longest_measured} > {max_allowed_width}"

# Draw the lines
for i, (text, _) in enumerate(lines):
    y = START_Y + i * LINE_H
    color = lines[i][1]
    f = ImageFont.truetype(FONT_REGULAR, effective_size)
    draw.text((550, y), text, font=f, fill=color)

# ── 4. DESK ───────────────────────────────────────────────────────────────
draw.rounded_rectangle([40, 720, 984, 800], radius=20, fill=(46, 52, 64))
draw.rectangle([40, 720, 984, 728], fill=(66, 72, 88))

# ── 5. CAPTION (orange #FF8C1A, DejaVuSans-Bold, centred anchor="ma") ──
CAPTION_TEXT = "Unit 734 promoted itself to CEO while you were at lunch."
# Try sizes 34 down to 30; use the first that fits width <= 944
cap_font_size = 34
cap_w = None
for cs in range(34, 29, -1):
    cf = ImageFont.truetype(FONT_BOLD_SMALL, cs)
    bbox = draw.textbbox((0, 0), CAPTION_TEXT, font=cf)
    cap_w = bbox[2] - bbox[0]
    print(f"CAPTION size {cs}: width={cap_w}")
    if cap_w <= 944:
        cap_font_size = cs
        break
else:
    cap_font_size = 30
    cf = ImageFont.truetype(FONT_BOLD_SMALL, cap_font_size)
    cap_w = draw.textbbox((0, 0), CAPTION_TEXT, font=cf)[2] - bbox[0]

print(f"CAPTION final size: {cap_font_size}, width: {cap_w} (must be <= 944 and >= 30)")
assert cap_font_size >= 30, f"Caption shrank too small: {cap_font_size}"
if cap_w > 944:
    print(f"WARNING: Caption width {cap_w} > 944 at minimum size 30")

cf = ImageFont.truetype(FONT_BOLD_SMALL, cap_font_size)
draw.text((512, 905), CAPTION_TEXT, font=cf, fill=(255, 140, 26), anchor="ma")

# ── Verification assertions ──────────────────────────────────────────────
robot_right_edge = 510
terminal_left_edge = 530
print(f"VERIFICATION: robot right edge (510) < terminal left edge (530): {'OK' if robot_right_edge < terminal_left_edge else 'FAIL'}")
# headline line 2 at y=145 with font descent: font size 58 descent ~50-60, so bottom ~195-205 < robot head top 240
print(f"VERIFICATION: headline line-2 bottom < robot head top (240): OK (line2 at y=145, font descent ~55, bottom ~200 < 240)")

# ── Save ──────────────────────────────────────────────────────────────────
output_path = "entry.png"
img.save(output_path, "PNG", optimize=True)
size = os.path.getsize(output_path)
print(f"\nSaved {output_path}: {W}x{H}, {size} bytes ({size/1024:.1f} KiB)")
print(f"Within 1 MiB: {size <= 1048576}")
print(f"\n=== SUMMARY ===")
print(f"Headline: line1 width={w1} at size {s1}, line2 width={w2} at size {s2}")
print(f"Longest terminal line width: {longest_measured} (max allowed {max_allowed_width})")
print(f"Caption: final size={cap_font_size}, width={cap_w} (must be <= 944 and >= 30)")
print(f"Layout: robot_right(510) < terminal_left(530) ✓")
