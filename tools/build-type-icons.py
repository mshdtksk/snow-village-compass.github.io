#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""16タイプのアイコンSVGを生成する。

    python tools/build-type-icons.py

共通のローポリ六角バッジ(FRAME)＋タイプごとのシンボル(SYMBOLS)という構成。
フレームが共通なので16個が必ず「組」に見える。色を変えたいときは
PALETTE を直して再実行すれば16個すべてに反映される。

出力: logo/types/<CODE>.svg
"""
import math, os, re, sys, io, tempfile

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

OUT_DIR = 'logo/types'
SIZE = 128
CX = CY = 64

# styles.css のトークンと同じ値にそろえる
PALETTE = {
    'navy':   '#0F5485',
    'mid':    '#1370A8',
    'blue':   '#29B5E8',
    'light':  '#46CCF7',
    'ice':    '#E6F7FD',
    'white':  '#FFFFFF',
}


def hexagon(cx, cy, r, rotate=0.0):
    """平頂六角形の頂点"""
    pts = []
    for i in range(6):
        a = math.radians(60 * i + rotate)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def pts_str(pts):
    return ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)


def star(cx, cy, R, r, n=5, rotate=-90.0):
    pts = []
    for i in range(n * 2):
        rad = R if i % 2 == 0 else r
        a = math.radians(180 * i / n + rotate)
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return pts


def build_frame():
    """ローポリ六角バッジ。中心から6分割した面を少しずつ違う青にする。"""
    outer = hexagon(CX, CY, 58)
    # 面ごとに明度を変えてローポリらしい陰影をつくる（左上が明るい）
    facet_colors = [
        PALETTE['mid'], PALETTE['navy'], PALETTE['navy'],
        PALETTE['mid'], PALETTE['blue'], PALETTE['light'],
    ]
    parts = []
    for i in range(6):
        a, b = outer[i], outer[(i + 1) % 6]
        parts.append(
            f'<polygon points="{CX},{CY} {a[0]:.1f},{a[1]:.1f} {b[0]:.1f},{b[1]:.1f}" '
            f'fill="{facet_colors[i]}"/>'
        )
    # 内側の暗い台座。シンボルを淡色にしてもここで必ず読める
    inner = hexagon(CX, CY, 45)
    parts.append(f'<polygon points="{pts_str(inner)}" fill="{PALETTE["navy"]}" opacity="0.92"/>')
    # 外周の縁取り。カード背景（青のグラデーション）から浮かせるため
    parts.append(
        f'<polygon points="{pts_str(outer)}" fill="none" '
        f'stroke="{PALETTE["ice"]}" stroke-width="3" stroke-linejoin="round"/>'
    )
    return '\n  '.join(parts)


I, W, A = PALETTE['ice'], PALETTE['white'], PALETTE['light']
N = PALETTE['navy']

# 16タイプ共通の人物シルエット（頭＋肩）。顔は描かない。
# 小さく表示しても崩れず、特定の見た目を想起させないため。
HEAD = pts_str(hexagon(64, 52, 14, 90))
BODY = '43,102 49,81 58,73 70,73 79,81 85,102'
PERSON = f'''<polygon points="{BODY}" fill="{W}"/>
  <polygon points="64,73 79,81 85,102 64,102" fill="{I}"/>
  <polygon points="{HEAD}" fill="{I}"/>
  <polygon points="{pts_str(hexagon(64, 52, 14, 90)[:3])}" fill="{W}"/>'''

# {PERSON} の前が背面（マント・羽・背景）、後ろが前面（被り物・持ち物）。
SYMBOLS = {
    # 🦸 データスーパーヒーロー: たなびくマントと胸のエンブレム
    'ESCI': f'''<polygon points="34,104 46,72 58,74 44,104" fill="{A}"/>
  <polygon points="94,104 82,72 70,74 84,104" fill="{A}"/>
  {{PERSON}}
  <polygon points="64,82 70,90 64,98 58,90" fill="{N}"/>''',

    # 🧭 インサイトナビゲーター: 探検帽と方位磁針
    'ESCO': f'''{{PERSON}}
  <polygon points="43,40 85,40 78,30 50,30" fill="{A}"/>
  <rect x="41" y="38" width="46" height="5" fill="{W}"/>
  <circle cx="64" cy="90" r="10" fill="{N}" stroke="{W}" stroke-width="2"/>
  <polygon points="64,83 67,90 64,97 61,90" fill="{W}"/>''',

    # 🔮 ビジョナリーアナリスト: 頭上に浮かぶ予知の光
    'ESZI': f'''{{PERSON}}
  <polygon points="{pts_str(hexagon(64, 34, 10, 30))}" fill="{A}"/>
  <polygon points="{pts_str(hexagon(64, 34, 10, 30)[:3])}" fill="{W}"/>
  <line x1="50" y1="40" x2="44" y2="46" stroke="{A}" stroke-width="3"/>
  <line x1="78" y1="40" x2="84" y2="46" stroke="{A}" stroke-width="3"/>''',

    # 🎯 ストラテジックオプティマイザー: 襟元と的のバッジ
    'ESZO': f'''{{PERSON}}
  <polygon points="64,74 73,81 64,91 55,81" fill="{N}"/>
  <circle cx="80" cy="88" r="10" fill="{N}" stroke="{W}" stroke-width="2"/>
  <circle cx="80" cy="88" r="4.5" fill="{A}"/>''',

    # 📡 テックエバンジェリスト: ヘッドセットと発信の弧
    'ETCI': f'''{{PERSON}}
  <path d="M48 52 A 17 17 0 0 1 80 52" fill="none" stroke="{A}" stroke-width="4"/>
  <rect x="43" y="49" width="8" height="12" rx="3" fill="{W}"/>
  <rect x="77" y="49" width="8" height="12" rx="3" fill="{W}"/>
  <path d="M32 46 A 20 20 0 0 1 32 66" fill="none" stroke="{A}" stroke-width="3"/>
  <path d="M96 46 A 20 20 0 0 0 96 66" fill="none" stroke="{A}" stroke-width="3"/>''',

    # 🏗️ チームアーキテクト: ヘルメットと設計図
    'ETCO': f'''{{PERSON}}
  <path d="M49 44 A 15 15 0 0 1 79 44" fill="{A}"/>
  <rect x="43" y="42" width="42" height="5" fill="{W}"/>
  <rect x="47" y="84" width="34" height="17" fill="{N}"/>
  <line x1="53" y1="90" x2="75" y2="90" stroke="{A}" stroke-width="2"/>
  <line x1="53" y1="96" x2="69" y2="96" stroke="{A}" stroke-width="2"/>''',

    # 🌟 ドリームチームクリエイター: 頭上の星
    'ETZI': f'''{{PERSON}}
  <polygon points="{pts_str(star(64, 38, 11, 4.5))}" fill="{W}"/>
  <polygon points="{pts_str(star(38, 52, 6, 2.5))}" fill="{A}"/>
  <polygon points="{pts_str(star(90, 52, 6, 2.5))}" fill="{A}"/>''',

    # 🤝 コミュニティハーモナイザー: 肩を並べる2人
    'ETZO': f'''<polygon points="28,102 33,82 40,75 51,75 58,82 62,102" fill="{I}"/>
  <polygon points="{pts_str(hexagon(45, 55, 11, 90))}" fill="{I}"/>
  <polygon points="66,102 70,82 77,75 88,75 95,82 100,102" fill="{W}"/>
  <polygon points="{pts_str(hexagon(83, 55, 11, 90))}" fill="{W}"/>
  <rect x="57" y="79" width="14" height="7" fill="{A}"/>''',

    # ⚙️ パイプラインマスター: 作業帽と歯車
    'BSCI': f'''{{PERSON}}
  <polygon points="45,42 83,42 77,32 51,32" fill="{A}"/>
  <rect x="43" y="40" width="42" height="5" fill="{W}"/>
  <polygon points="{pts_str(hexagon(84, 86, 11))}" fill="{A}"/>
  <circle cx="84" cy="86" r="5" fill="{N}"/>''',

    # 🛡️ サイレントガーディアン: フードと盾
    'BSCO': f'''<polygon points="42,76 47,44 64,34 81,44 86,76" fill="{A}"/>
  {{PERSON}}
  <polygon points="47,76 81,76 81,92 64,102 47,92" fill="{N}" stroke="{W}" stroke-width="2"/>
  <polygon points="64,81 71,88 64,96 57,88" fill="{A}"/>''',

    # 🚀 プロダクトイノベーター: 頭上に打ち上がるロケット
    'BSZI': f'''{{PERSON}}
  <polygon points="64,26 71,40 71,48 57,48 57,40" fill="{W}"/>
  <polygon points="57,43 50,51 57,49" fill="{A}"/>
  <polygon points="71,43 78,51 71,49" fill="{A}"/>
  <circle cx="64" cy="38" r="3.5" fill="{N}"/>
  <polygon points="59,49 69,49 64,57" fill="{A}"/>''',

    # 📊 ビジネスエンジニア: ネクタイとグラフ
    'BSZO': f'''{{PERSON}}
  <polygon points="64,73 70,80 66,96 62,96 58,80" fill="{N}"/>
  <rect x="76" y="88" width="6" height="13" fill="{A}"/>
  <rect x="85" y="80" width="6" height="21" fill="{W}"/>''',

    # 🏔️ プラットフォームリーダー: 背後にそびえる山
    'BTCI': f'''<polygon points="26,102 46,56 62,84 76,62 96,102" fill="{A}" opacity="0.85"/>
  <polygon points="46,56 55,72 37,72" fill="{W}"/>
  {{PERSON}}''',

    # ⚔️ データギルドマスター: 兜と剣
    'BTCO': f'''{{PERSON}}
  <polygon points="48,48 48,38 64,30 80,38 80,48" fill="{A}"/>
  <rect x="60" y="38" width="8" height="20" fill="{W}"/>
  <polygon points="86,48 94,48 92,86 88,86" fill="{W}"/>
  <rect x="82" y="62" width="16" height="5" fill="{A}"/>''',

    # 🦋 トランスフォーメーションリーダー: 背中の羽
    'BTZI': f'''<polygon points="56,82 28,58 31,86" fill="{A}"/>
  <polygon points="72,82 100,58 97,86" fill="{A}"/>
  <polygon points="56,82 34,98 53,96" fill="{I}" opacity="0.8"/>
  <polygon points="72,82 94,98 75,96" fill="{I}" opacity="0.8"/>
  {{PERSON}}''',

    # 🎖️ オペレーションキャプテン: 船長帽と勲章
    'BTZO': f'''{{PERSON}}
  <polygon points="45,40 83,40 79,29 49,29" fill="{N}"/>
  <rect x="43" y="38" width="42" height="6" fill="{W}"/>
  <rect x="57" y="31" width="14" height="7" fill="{A}"/>
  <polygon points="{pts_str(star(82, 88, 10, 4))}" fill="{A}"/>
  <rect x="76" y="74" width="12" height="8" fill="{W}"/>''',
}

# 人物はバッジ内側でクリップする。肩が下端で切れて肖像画のように収まり、
# 被り物や持ち物がフレームの縁を越えることもなくなる。
TEMPLATE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}" role="img" aria-label="{code}">
  <title>{code}</title>
  <defs><clipPath id="badge-{code}"><polygon points="{clip}"/></clipPath></defs>
  {frame}
  <g clip-path="url(#badge-{code})">
  {symbol}
  </g>
</svg>
'''


def write_atomic(path, text):
    d = os.path.dirname(path) or '.'
    fd, tmp = tempfile.mkstemp(suffix='.svg', dir=d)
    os.close(fd)
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    if open(tmp, encoding='utf-8').read() != text:
        os.unlink(tmp)
        raise SystemExit(f"書き出し検証に失敗: {path}")
    os.replace(tmp, path)


def build_contact_sheet():
    """16個を一覧できるシートを作る。デザイン確認と共有用で、アプリからは参照しない。
    結果カードと同じ濃い青を背景に敷いて、実際の見え方に近づけている。"""
    import json
    types = json.load(open('data/types.json', encoding='utf-8'))
    order = [a + b + c + d for a in 'EB' for b in 'ST' for c in 'CZ' for d in 'IO']
    cw, ch, cols = 170, 180, 4
    w = 680
    h = (len(order) // cols) * ch + 30
    clip = pts_str(hexagon(CX, CY, 45))
    parts = [
        f'<svg width="100%" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img">',
        '<title>16タイプアイコン一覧</title>',
        f'<rect x="0" y="0" width="{w}" height="{h}" fill="#12507d" rx="12"/>',
        f'<defs><clipPath id="sheet-badge"><polygon points="{clip}"/></clipPath></defs>',
    ]
    for i, code in enumerate(order):
        src = open(os.path.join(OUT_DIR, f'{code}.svg'), encoding='utf-8').read()
        inner = re.search(r'</defs>(.*)</svg>', src, re.S).group(1).strip()
        inner = inner.replace(f'url(#badge-{code})', 'url(#sheet-badge)')
        x = (i % cols) * cw + 15
        y = (i // cols) * ch + 18
        parts.append(f'<svg x="{x + 25}" y="{y}" width="90" height="90" viewBox="0 0 128 128">{inner}</svg>')
        parts.append(f'<text x="{x + 70}" y="{y + 108}" text-anchor="middle" '
                     f'font-family="sans-serif" font-size="13" font-weight="500" fill="#FFFFFF">{code}</text>')
        parts.append(f'<text x="{x + 70}" y="{y + 126}" text-anchor="middle" '
                     f'font-family="sans-serif" font-size="11" fill="#C7E7F7">{types[code]["title"]}</text>')
    parts.append('</svg>')
    text = '\n'.join(parts) + '\n'
    path = os.path.join(OUT_DIR, 'contact-sheet.svg')
    write_atomic(path, text)
    print(f"  {path}  ({len(text.encode('utf-8')):,} bytes)  ← 一覧シート")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    frame = build_frame()
    total = 0
    for code, symbol in SYMBOLS.items():
        # ETZO は2人構成なので共通シルエットを使わない
        body = symbol.replace('{PERSON}', PERSON) if '{PERSON}' in symbol else symbol
        svg = TEMPLATE.format(size=SIZE, code=code, frame=frame, symbol=body,
                              clip=pts_str(hexagon(CX, CY, 45)))
        path = os.path.join(OUT_DIR, f'{code}.svg')
        write_atomic(path, svg)
        total += len(svg.encode('utf-8'))
        print(f"  {path}  ({len(svg.encode('utf-8')):,} bytes)")
    print(f"\n{len(SYMBOLS)}個を生成 / 合計 {total/1024:.1f} KB")
    build_contact_sheet()
    missing = [c for c in
               [a+b+x+y for a in 'EB' for b in 'ST' for x in 'CZ' for y in 'IO']
               if c not in SYMBOLS]
    if missing:
        raise SystemExit(f"シンボル未定義: {missing}")


if __name__ == '__main__':
    main()
