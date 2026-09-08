# -*- coding: utf-8 -*-
"""Xやチャットにリンクを貼ったとき、タイプごとの結果カードが画像で出るようにする。

Xのクローラは JavaScript を実行しないため、?code=XXXX のクエリでは中身を
読み取れない。そこでタイプごとに静的ページ(t/XXXX.html)とOGP画像(og/XXXX.png)
を書き出し、共有にはそのURLを使う。人が開いた場合はアプリへ転送する。

  python tools/build-share-assets.py
"""
import json, os, sys, io, html, tempfile

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://mshdtksk.github.io/snow-village-compass.github.io/"
OG_DIR = os.path.join(ROOT, 'og')
PAGE_DIR = os.path.join(ROOT, 't')
W, H = 1200, 630

# 結果カードの配色(styles.css)と同じ3点。135度=左上から右下へ。
GRADIENTS = {
    'craft':     ('#4A0206', '#8E1E1F', '#CD554B'),
    'value':     ('#002852', '#12599E', '#2E95E3'),
    'innovator': ('#4A4404', '#A67806', '#E8B62A'),
    'optimizer': ('#0B3D12', '#2A7A1C', '#78B84A'),
}

FONT_CANDIDATES = [
    (r'C:\Windows\Fonts\YuGothB.ttc', r'C:\Windows\Fonts\YuGothM.ttc'),
    (r'C:\Windows\Fonts\meiryob.ttc', r'C:\Windows\Fonts\meiryo.ttc'),
    ('/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc', '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc'),
    ('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'),
]


def find_fonts():
    for bold, regular in FONT_CANDIDATES:
        if os.path.exists(bold) and os.path.exists(regular):
            return bold, regular
    sys.exit("日本語フォントが見つかりません。FONT_CANDIDATES に環境のフォントを追加してください。")


def rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lerp(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def gradient(stops):
    """135度(左上→右下)の3点グラデーション。"""
    c0, c1, c2 = (rgb(s) for s in stops)
    img = Image.new('RGB', (W, H))
    px = img.load()
    # 対角線への射影で位置を出す
    for y in range(H):
        for x in range(W):
            t = (x + y) / (W + H - 2)
            px[x, y] = lerp(c0, c1, t / 0.55) if t <= 0.55 else lerp(c1, c2, (t - 0.55) / 0.45)
    return img


def fit(draw, text, font_path, max_width, start, minimum=28):
    """max_width に収まる最大のフォントサイズを返す。"""
    size = start
    while size > minimum:
        f = ImageFont.truetype(font_path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 2
    return ImageFont.truetype(font_path, minimum)


def wrap(draw, text, font, max_width):
    """1行に収まらないときは、2行の長さが近くなる位置で折る。

    素直に詰めて折ると最後の行に1文字だけ残ることがあり、収まりが悪いため。
    """
    if draw.textlength(text, font=font) <= max_width:
        return [text]
    best, best_gap = None, None
    for k in range(1, len(text)):
        a = draw.textlength(text[:k], font=font)
        b = draw.textlength(text[k:], font=font)
        if a > max_width or b > max_width:
            continue
        if best_gap is None or abs(a - b) < best_gap:
            best, best_gap = k, abs(a - b)
    if best is None:  # 2行にも収まらない長さは素直に詰める
        lines, cur = [], ''
        for ch in text:
            if draw.textlength(cur + ch, font=font) <= max_width:
                cur += ch
            else:
                lines.append(cur)
                cur = ch
        if cur:
            lines.append(cur)
        return lines
    return [text[:best], text[best:]]


def save_atomic(img_or_text, path, is_image):
    """同じディレクトリに書いてから置き換える(途中で壊れた版を残さない)。"""
    d = os.path.dirname(path)
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, suffix='.tmp')
    os.close(fd)
    try:
        if is_image:
            img_or_text.save(tmp, 'PNG', optimize=True)
        else:
            with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
                f.write(img_or_text)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):  # 途中で失敗しても .tmp を残さない
            os.remove(tmp)


def build_image(t, bold, regular):
    img = gradient(GRADIENTS.get(t.get('colorGroup'), GRADIENTS['craft']))
    d = ImageDraw.Draw(img, 'RGBA')

    # 軸のバッジ
    x, chip_font = 64, ImageFont.truetype(bold, 26)
    for axis in t.get('axes', []):
        label = f"# {axis}"
        w = d.textlength(label, font=chip_font)
        d.rounded_rectangle([x, 56, x + w + 36, 104], radius=24, fill=(255, 255, 255, 46))
        d.text((x + 18, 66), label, font=chip_font, fill=(255, 255, 255, 235))
        x += w + 52

    # アイコン
    icon_path = os.path.join(ROOT, t['iconUrl'].replace('/', os.sep))
    text_left = 64
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert('RGBA').resize((208, 208), Image.LANCZOS)
        img.paste(icon, (64, 168), icon)
        text_left = 312

    text_width = W - text_left - 64
    d.text((text_left, 176), "YOUR STYLE TYPE", font=ImageFont.truetype(bold, 24), fill=(255, 255, 255, 200))
    title_font = fit(d, t['title'], bold, text_width, 76)
    d.text((text_left, 212), t['title'], font=title_font, fill=(255, 255, 255))
    sub_font = fit(d, t['subtitle'], regular, text_width, 30)
    d.text((text_left, 300), t['subtitle'], font=sub_font, fill=(255, 255, 255, 205))

    # キャッチコピー
    # まず1行に収まるサイズを探し、それでも無理なら2行に折る
    body_font = fit(d, t['catchphrase'], regular, W - 128 - 48, 34, minimum=28)
    lines = wrap(d, t['catchphrase'], body_font, W - 128 - 48)
    box_h = 36 + 46 * len(lines)
    d.rounded_rectangle([64, 400, W - 64, 400 + box_h], radius=18, fill=(0, 0, 0, 64))
    for i, line in enumerate(lines):
        d.text((96, 418 + 46 * i), line, font=body_font, fill=(255, 255, 255, 240))

    d.text((64, H - 66), "SnowVillage SVTI診断", font=ImageFont.truetype(bold, 26), fill=(255, 255, 255, 190))
    return img


PAGE = '''<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title_esc} | SnowVillage SVTI診断</title>
    <meta name="description" content="{desc_esc}" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="SnowVillage SVTI診断" />
    <meta property="og:title" content="{og_title_esc}" />
    <meta property="og:description" content="{desc_esc}" />
    <meta property="og:url" content="{page_url}" />
    <meta property="og:image" content="{image_url}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="{title_esc}のタイプカード" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{og_title_esc}" />
    <meta name="twitter:description" content="{desc_esc}" />
    <meta name="twitter:image" content="{image_url}" />
    <link rel="canonical" href="{app_url}" />
    <!-- 人が開いたときはアプリの結果画面へ送る。クローラはここまで読めば足りる。 -->
    <meta http-equiv="refresh" content="0; url={app_rel}" />
    <script>
      location.replace("{app_rel}");
    </script>
  </head>
  <body>
    <p><a href="{app_rel}">診断結果を開く</a></p>
  </body>
</html>
'''


def build_default(bold, regular):
    """トップページ用。まだタイプが決まっていないので診断そのものを見せる。

    画像は作り直さない限り残り続けるので、開催年など時期に縛られる文言は入れない。
    """
    img = gradient(GRADIENTS['value'])
    d = ImageDraw.Draw(img, 'RGBA')
    d.text((64, 200), "SnowVillage", font=ImageFont.truetype(bold, 40), fill=(255, 255, 255, 205))
    d.text((64, 252), "SVTI診断", font=ImageFont.truetype(bold, 92), fill=(255, 255, 255))
    d.text((64, 372), "8問・約2分で、あなたのデータ活用スタイルと", font=ImageFont.truetype(regular, 36), fill=(255, 255, 255, 230))
    d.text((64, 424), "合うコミュニティ・Neighborsが分かります。", font=ImageFont.truetype(regular, 36), fill=(255, 255, 255, 230))
    d.text((64, H - 66), "snowvillage.cloud", font=ImageFont.truetype(bold, 26), fill=(255, 255, 255, 190))
    return img


def main():
    bold, regular = find_fonts()
    types = json.load(open(os.path.join(ROOT, 'data', 'types.json'), encoding='utf-8'))
    save_atomic(build_default(bold, regular), os.path.join(OG_DIR, 'default.png'), True)
    print("  default  トップページ用")
    for code, t in sorted(types.items()):
        save_atomic(build_image(t, bold, regular), os.path.join(OG_DIR, f'{code}.png'), True)
        e = html.escape
        page = PAGE.format(
            title_esc=e(t['title']),
            og_title_esc=e(f"私のSVTIタイプは「{t['title']}」でした！"),
            desc_esc=e(t['catchphrase']),
            page_url=f"{SITE}t/{code}.html",
            image_url=f"{SITE}og/{code}.png",
            app_url=f"{SITE}?code={code}",
            app_rel=f"../?code={code}",
        )
        save_atomic(page, os.path.join(PAGE_DIR, f'{code}.html'), False)
        print(f"  {code}  {t['title']}")
    print(f"\n{len(types)}タイプ分の og/*.png と t/*.html を書き出し")


if __name__ == '__main__':
    main()
