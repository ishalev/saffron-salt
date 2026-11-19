# Rules figures 1-3 as an editable deck: screenshot + native callouts, numbers and arrows.
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree

RED = RGBColor(0xC8, 0x20, 0x2F); INK = RGBColor(0x3B, 0x2A, 0x1E); WHITE = RGBColor(0xFF, 0xFF, 0xFF)
prs = Presentation(); prs.slide_width = Inches(10); prs.slide_height = Inches(7.5)
BL = prs.slide_layouts[6]

def arrow(s, x1, y1, x2, y2, w=2.25):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = RED; c.line.width = Pt(w)
    ln = c.line._get_or_add_ln()
    te = etree.SubElement(ln, qn('a:tailEnd')); te.set('type', 'triangle'); te.set('w', 'med'); te.set('len', 'med')
    return c

def badge(s, n, cx, cy, d=0.42):
    o = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx - d / 2), Inches(cy - d / 2), Inches(d), Inches(d))
    o.fill.solid(); o.fill.fore_color.rgb = RED; o.line.color.rgb = WHITE; o.line.width = Pt(1.5)
    tf = o.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = str(n); r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = 'Arial'
    return o

def label(s, text, x, y, w, h, size=12, align=PP_ALIGN.LEFT, color=INK, bold_first=True):
    t = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = t.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.04); tf.margin_top = tf.margin_bottom = Inches(0.02)
    for i, line in enumerate(text.split('\n')):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.alignment = align
        r = p.add_run(); r.text = line; r.font.size = Pt(size); r.font.name = 'Arial'; r.font.color.rgb = color
        r.font.bold = bold_first and i == 0
    return t

def ring(s, x, y, w, h):
    r = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    r.fill.background(); r.line.color.rgb = RED; r.line.width = Pt(2.5)
    return r

def title(s, text):
    label(s, text, 0.25, 0.05, 9.5, 0.4, size=16)

# ---------- Figure 1: setup ----------
s = prs.slides.add_slide(BL)
title(s, 'Figure 1 - Game setup')
X0, Y0, K = 0.25, 0.5, 8.0 / 800          # image origin and inches per pixel of the 800-px reference
s.shapes.add_picture('fig1_setup.png', Inches(X0), Inches(Y0), width=Inches(8.0))
P = lambda px, py: (X0 + px * K, Y0 + py * K)
# 1 player board (stored cards)
tx, ty = P(650, 215); badge(s, 1, 8.75, ty); arrow(s, 8.53, ty, tx + 0.85, ty)
# 5 hand of cards
tx, ty = P(368, 225); badge(s, 5, 5.0, ty); arrow(s, 4.78, ty, tx + 0.02, ty)
# 6 cards placed in the market, 7 cards added by the seasoning number
tx, ty = P(393, 108); badge(s, 6, 3.55, 2.05); arrow(s, 3.68, 1.88, tx - 0.02, ty + 0.03)
tx, ty = P(470, 108); badge(s, 7, 5.45, 2.05); arrow(s, 5.32, 1.88, tx + 0.05, ty + 0.03)
# 2 start spaces, 3 MOQ / checkpoint, 4 neutral cubes (badges under the image)
yb = Y0 + 581 * K + 0.42
tx, ty = P(137, 532); badge(s, 2, tx, yb); arrow(s, tx, yb - 0.21, tx, ty - 0.02)
tx, ty = P(307, 411); badge(s, 3, tx, yb); arrow(s, tx, yb - 0.21, tx, ty + 0.12)
tx, ty = P(392, 451); badge(s, 4, tx, yb); arrow(s, tx, yb - 0.21, tx, ty + 0.03)
label(s, 'Numbers match the Setup steps. Shown in the digital edition: the Stored cards panel stands in for the player board, and the MOQ spaces stand in for the checkpoint tiles.',
      5.3, yb - 0.25, 4.5, 0.6, size=10, bold_first=False)

# ---------- Figure 2: seasoning (before / after) ----------
s = prs.slides.add_slide(BL)
title(s, 'Figure 2 - Seasoning numbers')
K = 9.5 / 2400; X0 = 0.25
label(s, 'Before: each player places one card in the market', 0.25, 0.65, 9.5, 0.3)
s.shapes.add_picture('fig2_before.png', Inches(X0), Inches(1.0), width=Inches(9.5))
YA = 2.95
label(s, 'After: deal cards onto each one, as many as its seasoning number shows', 0.25, YA - 0.35, 9.5, 0.3)
s.shapes.add_picture('fig2_market.png', Inches(X0), Inches(YA), width=Inches(9.5))
P = lambda px, py, y0: (X0 + px * K, y0 + py * K)
for y0 in (1.0, YA):   # ring the +2 and +3 badges in both images
    for bx in (594, 1178):
        cx, cy = P(bx, 297, y0); ring(s, cx - 0.16, cy - 0.11, 0.32, 0.22)
for x1, x2, n, txt in ((688, 1016, 2, 'Cinnamon 29 shows +2:\n2 cards dealt onto it'), (1271, 1771, 3, 'Chili 6 shows +3:\n3 cards dealt onto it')):
    ax, ay = P(x1, 115, YA); bx, by = P(x2, 328, YA)
    ring(s, ax - 0.04, ay - 0.04, bx - ax + 0.08, by - ay + 0.08)
    lx = (ax + bx) / 2
    label(s, txt, lx - 1.2, YA + 1.85, 2.4, 0.6, size=12, align=PP_ALIGN.CENTER)
    arrow(s, lx, YA + 1.82, lx, by + 0.08)
label(s, 'In the printed game, a white seasoning icon means the added cards are dealt faceup, and a black icon means facedown. The digital edition deals every lot faceup, so these screenshots show faceup cards only.',
      0.4, 6.35, 9.2, 0.8, size=11, bold_first=False)

# ---------- Figure 3: card anatomy ----------
s = prs.slides.add_slide(BL)
title(s, 'Figure 3 - Spice card and coin card')
X0, Y0, K = 1.7, 1.0, 6.6 / 600
s.shapes.add_picture('fig3_cards.png', Inches(X0), Inches(Y0), width=Inches(6.6))
P = lambda px, py: (X0 + px * K, Y0 + py * K)
items = [('Bid value', 'Higher numbers beat lower ones.', (100, 75), 1.2),
         ('Spice icons', 'Move 1 space per icon: this card moves 2.', (213, 85), 2.1),
         ('Salt', "Salted moves can't skip over markers.", (88, 200), 3.05),
         ('Spice name', '', (150, 236), 3.85),
         ('Seasoning number', 'Cards added when it goes to the market.', (148, 258), 4.4)]
for h, d, (px, py), ly in items:
    label(s, h + ('\n' + d if d else ''), 0.1, ly, 1.6, 0.8, size=11)
    tx, ty = P(px, py); arrow(s, 1.65, ly + 0.15, tx - 0.12, ty)
items = [('Card number', 'Its bid value (79-83).', (400, 70), 1.2),
         ('Coins', 'Cash in right away: this card pays 2.', (450, 150), 2.5),
         ('Seasoning number', '', (448, 258), 4.25)]
for h, d, (px, py), ly in items:
    label(s, h + ('\n' + d if d else ''), 8.35, ly, 1.6, 0.8, size=11)
    tx, ty = P(px, py); arrow(s, 8.32, ly + 0.15, tx + 0.15, ty)
label(s, 'Coin cards show no spice. They are numbered 79-83 and still count as spice cards for bidding.', 1.7, 5.4, 6.6, 0.6, size=11, bold_first=False)
prs.save('rules-figures-1-3.pptx')
print('saved')
