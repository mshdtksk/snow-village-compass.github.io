#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""snowvillage.cloud からネイバーとメイヤーを取得して data/neighbors.json を作り直す。

大元サイト(snowvillage-cloud/snowvillage-cloud.github.io)が更新されたら
リポジトリのルートで実行する:

    python tools/sync-people.py

- ネイバー: about/neighbors/userlist.yaml
- メイヤー: about/aboutData.js の mayorsData
  （メイヤーは専用データファイルが無く、画像も images/organizers/ 側にある）

診断コード(code)は既存の data/neighbors.json から名前をキーに引き継ぐので、
手で調整した割り当ては再実行しても失われない。新規の人には人数が少ない
コードから順に仮の値を割り当てる。

data/people-manual.json に書いた人は、大元サイトにまだ載っていなくても
マージされる。大元サイトに載った時点でそちらが優先されるので、
people-manual.json から消してよい。
"""
import json, re, os, sys, io, tempfile, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SITE = "https://snowvillage-cloud.github.io/"
RAW = "https://raw.githubusercontent.com/snowvillage-cloud/snowvillage-cloud.github.io/main/"
UA = {'User-Agent': 'Mozilla/5.0 (snow-village-compass sync)'}
OUT = 'data/neighbors.json'
MANUAL = 'data/people-manual.json'
CODES = [a + b + c + d for a in 'EB' for b in 'ST' for c in 'CV' for d in 'IO']


def get(path):
    req = urllib.request.Request(RAW + path, headers=UA)
    return urllib.request.urlopen(req, timeout=30).read().decode('utf-8')


def to_url(p):
    """../../images/neighbors/x.png -> https://snowvillage-cloud.github.io/images/neighbors/x.png"""
    if not p:
        return ""
    if p.startswith('http'):
        return p
    return SITE + re.sub(r'^(\.\./)+', '', p.strip())


def clean(v):
    v = (v or "").strip().strip('"').strip("'")
    return "" if v in ('--', 'ー') else v


def fetch_neighbors():
    people, cur = [], None
    for line in get("about/neighbors/userlist.yaml").splitlines():
        m = re.match(r'^-\s+name\s*:\s*(.+)$', line)
        if m:
            if cur:
                people.append(cur)
            cur = {'name': clean(m.group(1))}
            continue
        # 大元のYAMLには「photo : x」のようにキー名の後ろへ空白を入れた行があり、
        # コロン直結だけを見ていると写真・所属・SNSをまるごと取りこぼす。
        m = re.match(r'^\s+([a-zA-Z_]+)\s*:\s*(.*)$', line)
        if m and cur is not None:
            cur[m.group(1)] = clean(m.group(2))
    if cur:
        people.append(cur)
    # 記入例の行は除く
    return [n for n in people if n.get('name') and n['name'] != 'Neighbor']


def fetch_mayors():
    js = get("about/aboutData.js")
    block = re.search(r'const mayorsData\s*=\s*\[(.*?)\n\];', js, re.S).group(1)
    out = []
    for chunk in re.findall(r'\{(.*?)\}\s*,?\s*(?=\{|$)', block, re.S):
        def field(key):
            m = re.search(key + r':\s*"((?:[^"\\]|\\.)*)"', chunk)
            return clean(m.group(1)) if m else ""
        if not field('name'):
            continue
        out.append({
            'name': field('name'),
            # desc は自己紹介文なので <br> の前だけを所属として拾う
            'affiliation': re.split(r'<br\s*/?>', field('desc'))[0].strip(),
            'title': field('role'),
            'photo': field('photo'),
            'xUrl': field('xUrl'),
            'linkedInUrl': field('linkedInUrl'),
        })
    return out


def row(name, affiliation, title, kind, photo, x_url, linkedin_url):
    return {
        'name': name, 'affiliation': affiliation, 'title': title, 'kind': kind,
        'photo': to_url(photo), 'x_url': clean(x_url), 'linkedin_url': clean(linkedin_url),
    }


def main():
    neighbors = fetch_neighbors()
    mayors = fetch_mayors()
    print(f"大元サイト: ネイバー{len(neighbors)}名 / メイヤー{len(mayors)}名")

    people = [row(n['name'], clean(n.get('affiliation')), '', 'neighbor',
                  n.get('photo'), n.get('xUrl'), n.get('linkedInUrl')) for n in neighbors]
    people += [row(m['name'], m['affiliation'], m['title'], 'mayor',
                   m['photo'], m['xUrl'], m['linkedInUrl']) for m in mayors]

    # 大元サイトにまだ載っていない人を足す（既に載っていれば大元を優先）
    if os.path.exists(MANUAL):
        known = {p['name'] for p in people}
        added = 0
        for m in json.load(open(MANUAL, encoding='utf-8')):
            if m['name'] in known:
                print(f"  {MANUAL} の「{m['name']}」は大元サイトにも存在するため、大元側を採用")
                continue
            people.append(row(m['name'], m.get('affiliation', ''), m.get('title', ''),
                              m.get('kind', 'neighbor'), m.get('photo'),
                              m.get('x_url') or m.get('xUrl'),
                              m.get('linkedin_url') or m.get('linkedInUrl')))
            added += 1
        if added:
            print(f"{MANUAL} から{added}名を追加")

    # 既存の code を名前で引き継ぐ
    existing = {}
    if os.path.exists(OUT):
        for e in json.load(open(OUT, encoding='utf-8')):
            existing[e['name']] = e.get('code')
    used = {c: 0 for c in CODES}
    for p in people:
        # 診断コードはアンケート回答があった人だけが持つ。
        # ここで機械的に仮の値を振ると、別人が「同タイプ」として
        # 表示される事故につながるため、無い人は null のままにする。
        # コードの付与は tools/apply-survey.py が行う。
        c = existing.get(p['name'])
        p['code'] = c if c in used else None
        if p['code']:
            used[c] += 1

    uncovered = [c for c, n in used.items() if n == 0]
    confirmed = sum(1 for p in people if p['code'])
    print(f"合計{len(people)}名（コード確定 {confirmed}名 / 未回答 {len(people) - confirmed}名）"
          f" / コード網羅 {16 - len(uncovered)}/16"
          + (f" (該当者なし: {', '.join(uncovered)})" if uncovered else ""))

    # 同じフォルダに一時ファイルを作ってから置き換える（書き込み失敗で壊さないため）
    text = json.dumps(people, ensure_ascii=False, indent=2) + "\n"
    fd, tmp = tempfile.mkstemp(suffix='.json', dir='data')
    os.close(fd)
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    if open(tmp, encoding='utf-8').read() != text:
        os.unlink(tmp)
        raise SystemExit(f"書き出し検証に失敗。{OUT} は変更していません")
    os.replace(tmp, OUT)
    print(f"{OUT} を更新")


if __name__ == '__main__':
    main()
