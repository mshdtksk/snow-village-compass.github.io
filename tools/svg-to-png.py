#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""logo/types の SVG を PNG に変換する。

    python tools/svg-to-png.py [--size 512]

build-type-icons.py が出力する SVG だけを対象にした簡易ラスタライザ。
polygon / circle / rect / line / path(円弧) / clipPath のみ扱う。
Pillow だけで動くので、ImageMagick や cairo の導入が要らない。

生成AIツールなど SVG を読めない相手に渡すとき用。アプリ自体は SVG を使う。
"""
import math, os, re, sys, io, argparse
from PIL import Image, ImageDraw

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SRC_DIR = 'logo/types'
OUT_DIR = 'logo/types/png'
SS = 4  # 縁を滑らかにするための拡大率


def hex2rgb(c):
    c = c.lstrip('#')
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def attr(tag, name, default=None):
    m = re.search(rf'\b{name}="([^"]*)"', tag)
    return m.group(1) if m else default


def fnum(tag, name, default=0.0):
    v = attr(tag, name)
    return float(v) if v is not None else default


def points_of(tag, s):
    raw = attr(tag, 'points', '')
    out = []
    for pair in raw.replace(',', ' ').split():
        out.append(float(pair))
    return [(out[i] * s, out[i + 1] * s) for i in range(0, len(out) - 1, 2)]


def arc_points(x1, y1, rx, ry, laf, sf, x2, y2, steps=48):
    """SVG の楕円弧を折れ線に落とす。今回は rx==ry の円弧しか使っていない。"""
    if rx == 0 or ry == 0:
        return [(x1, y1), (x2, y2)]
    dx2, dy2 = (x1 - x2) / 2.0, (y1 - y2) / 2.0
    denom = (rx * rx * dy2 * dy2 + ry * ry * dx2 * dx2)
    if denom == 0:
        return [(x1, y1), (x2, y2)]
    num = rx * rx * ry * ry - denom
    factor = math.sqrt(max(num / denom, 0))
    if laf == sf:
        factor = -factor
    cxp, cyp = factor * rx * dy2 / ry, -factor * ry * dx2 / rx
    cx, cy = cxp + (x1 + x2) / 2.0, cyp + (y1 + y2) / 2.0

    def ang(ux, uy):
        return math.atan2(uy, ux)

    t1 = ang((dx2 - cxp) / rx, (dy2 - cyp) / ry)
    t2 = ang((-dx2 - cxp) / rx, (-dy2 - cyp) / ry)
    dt = t2 - t1
    if sf == 0 and dt > 0:
        dt -= 2 * math.pi
    elif sf == 1 and dt < 0:
        dt += 2 * math.pi
    return [(cx + rx * math.cos(t1 + dt * i / steps),
             cy + ry * math.sin(t1 + dt * i / steps)) for i in range(steps + 1)]


def parse_path(d, s):
    m = re.match(r'\s*M\s*(-?[\d.]+)[ ,]+(-?[\d.]+)\s*A\s*(-?[\d.]+)[ ,]+(-?[\d.]+)[ ,]+'
                 r'(-?[\d.]+)[ ,]+([01])[ ,]+([01])[ ,]+(-?[\d.]+)[ ,]+(-?[\d.]+)', d)
    if not m:
        return []
    x1, y1, rx, ry, _rot, laf, sf, x2, y2 = (float(v) for v in m.groups())
    pts = arc_points(x1, y1, rx, ry, int(laf), int(sf), x2, y2)
    return [(x * s, y * s) for x, y in pts]


def draw_tag(dr, tag, s):
    name = re.match(r'<(\w+)', tag).group(1)
    fill = attr(tag, 'fill')
    stroke = attr(tag, 'stroke')
    sw = fnum(tag, 'stroke-width', 1.0) * s
    op = float(attr(tag, 'opacity', '1'))

    def col(c):
        if not c or c == 'none':
            return None
        return hex2rgb(c) + (int(255 * op),)

    f, st = col(fill), col(stroke)

    if name == 'polygon':
        pts = points_of(tag, s)
        if len(pts) >= 3:
            if f:
                dr.polygon(pts, fill=f)
            if st:
                dr.line(pts + [pts[0]], fill=st, width=max(1, round(sw)), joint='curve')
    elif name == 'circle':
        cx, cy, r = fnum(tag, 'cx') * s, fnum(tag, 'cy') * s, fnum(tag, 'r') * s
        box = [cx - r, cy - r, cx + r, cy + r]
        if f:
            dr.ellipse(box, fill=f)
        if st:
            dr.ellipse(box, outline=st, width=max(1, round(sw)))
    elif name == 'rect':
        x, y = fnum(tag, 'x') * s, fnum(tag, 'y') * s
        w, h = fnum(tag, 'width') * s, fnum(tag, 'height') * s
        rx = fnum(tag, 'rx', 0) * s
        box = [x, y, x + w, y + h]
        if rx > 0:
            dr.rounded_rectangle(box, radius=rx, fill=f, outline=st,
                                 width=max(1, round(sw)) if st else 0)
        else:
            dr.rectangle(box, fill=f, outline=st, width=max(1, round(sw)) if st else 0)
    elif name == 'line':
        p = [(fnum(tag, 'x1') * s, fnum(tag, 'y1') * s),
             (fnum(tag, 'x2') * s, fnum(tag, 'y2') * s)]
        if st:
            dr.line(p, fill=st, width=max(1, round(sw)))
    elif name == 'path':
        pts = parse_path(attr(tag, 'd', ''), s)
        if len(pts) >= 2:
            if f:
                dr.polygon(pts, fill=f)
            if st:
                dr.line(pts, fill=st, width=max(1, round(sw)), joint='curve')


def render(svg_text, out_w, out_h):
    vb = attr(svg_text[:400], 'viewBox', '0 0 128 128').split()
    vw, vh = float(vb[2]), float(vb[3])
    s = out_w * SS / vw
    W, H = out_w * SS, int(round(out_h * SS))

    clips = {}
    for cid, body in re.findall(r'<clipPath id="([^"]+)">(.*?)</clipPath>', svg_text, re.S):
        pt = re.search(r'<polygon[^>]*>', body)
        if pt:
            clips[cid] = points_of(pt.group(0), s)

    body = re.sub(r'<defs>.*?</defs>', '', svg_text, flags=re.S)
    base = Image.new('RGBA', (W, H), (0, 0, 0, 0))

    # クリップされたグループは別レイヤーに描いてからマスク合成する
    pos = 0
    for m in re.finditer(r'<g clip-path="url\(#([^)]+)\)">(.*?)</g>', body, re.S):
        head = body[pos:m.start()]
        dr = ImageDraw.Draw(base)
        for t in re.findall(r'<(?:polygon|circle|rect|line|path)\b[^>]*>', head):
            draw_tag(dr, t, s)
        layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        dl = ImageDraw.Draw(layer)
        for t in re.findall(r'<(?:polygon|circle|rect|line|path)\b[^>]*>', m.group(2)):
            draw_tag(dl, t, s)
        mask = Image.new('L', (W, H), 0)
        cp = clips.get(m.group(1))
        if cp:
            ImageDraw.Draw(mask).polygon(cp, fill=255)
        else:
            mask.paste(255, (0, 0, W, H))
        base = Image.alpha_composite(base, Image.composite(
            layer, Image.new('RGBA', (W, H), (0, 0, 0, 0)), mask))
        pos = m.end()
    dr = ImageDraw.Draw(base)
    for t in re.findall(r'<(?:polygon|circle|rect|line|path)\b[^>]*>', body[pos:]):
        draw_tag(dr, t, s)

    return base.resize((out_w, int(round(out_h))), Image.LANCZOS)


def build_sheet(icons, cell=260, cols=4, bg=(18, 80, 125)):
    """個別PNGを並べて一覧シートを作る。
    SVG版シートは入れ子svgで組んでいてこのラスタライザでは解釈できないため、
    ここでは出力済みのPNGを貼り合わせる。"""
    from PIL import ImageFont
    rows = (len(icons) + cols - 1) // cols
    pad, label_h = 24, 46
    W = cols * cell + pad * 2
    H = rows * (cell + label_h) + pad * 2
    sheet = Image.new('RGB', (W, H), bg)
    dr = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype('meiryo.ttc', 22)
    except Exception:
        font = ImageFont.load_default()
    for i, (code, img) in enumerate(icons):
        x = pad + (i % cols) * cell
        y = pad + (i // cols) * (cell + label_h)
        thumb = img.resize((cell - 30, cell - 30), Image.LANCZOS)
        sheet.paste(thumb, (x + 15, y), thumb)
        tw = dr.textlength(code, font=font)
        dr.text((x + cell / 2 - tw / 2, y + cell - 6), code, font=font, fill=(255, 255, 255))
    return sheet


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--size', type=int, default=512, help='アイコン1辺のpx（既定512）')
    args = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    order = [a + b + c + d for a in 'EB' for b in 'ST' for c in 'CZ' for d in 'IO']
    total = 0
    icons = []
    for code in order:
        text = open(os.path.join(SRC_DIR, f'{code}.svg'), encoding='utf-8').read()
        img = render(text, args.size, args.size)
        icons.append((code, img))
        out = os.path.join(OUT_DIR, f'{code}.png')
        img.save(out, 'PNG', optimize=True)
        n = os.path.getsize(out)
        total += n
        print(f"  {out}  {img.size[0]}x{img.size[1]}  ({n:,} bytes)")

    sheet = build_sheet(icons)
    out = os.path.join(OUT_DIR, 'contact-sheet.png')
    sheet.save(out, 'PNG', optimize=True)
    n = os.path.getsize(out)
    total += n
    print(f"  {out}  {sheet.size[0]}x{sheet.size[1]}  ({n:,} bytes)  ← 一覧シート")
    print(f"\n{len(order) + 1}枚を出力 / 合計 {total/1024:.0f} KB")


if __name__ == '__main__':
    main()
