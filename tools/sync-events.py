#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""TechPlay から実在する開催予定イベントを取得して data/events.json を作り直す。

    python tools/sync-events.py

data/user-groups.json に載っている全コミュニティのページを見て、
開催予定（開始時刻が未来）のイベントだけを集める。
URL は個別イベントページ（https://techplay.jp/event/<id>）を指すので、
コミュニティのトップページに飛ばされることがない。

以前の events.json は実在しないイベントが手書きされていたため、
このスクリプトで生成したものに置き換えた。定期的に再実行して更新する。
"""
import json, re, html, os, sys, io, time, tempfile, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

OUT = 'data/events.json'
GROUPS = 'data/user-groups.json'
UA = {'User-Agent': 'Mozilla/5.0 (snow-village-compass sync)'}
MAX_EVENTS = 12


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')


def parse_events(page, now):
    """埋め込みJSONからイベントを拾う。開始時刻が未来のものだけ返す。"""
    s = html.unescape(page)
    out = []
    # 1件分のオブジェクトは id → title → started_at → place の順に並ぶ
    pat = re.compile(
        r'"id":(\d+),"title":"((?:[^"\\]|\\.)*)".*?"started_at":(\d+|null).*?"place":"((?:[^"\\]|\\.)*)"',
        re.S)
    for m in pat.finditer(s):
        eid, title, started, place = m.groups()
        if started == 'null':
            continue
        started = int(started)
        if started <= now:
            continue
        # マッチが長すぎる場合は別イベントをまたいでいる可能性があるので捨てる
        if len(m.group(0)) > 3000:
            continue
        out.append({
            'id': int(eid),
            'title': title.replace('\\/', '/').strip(),
            'started_at': started,
            'place': place.replace('\\/', '/').strip(),
        })
    return out


def main():
    groups = json.load(open(GROUPS, encoding='utf-8'))
    now = int(time.time())
    found = {}
    for g in groups:
        url = g.get('techplayUrl')
        if not url:
            continue
        try:
            evs = parse_events(fetch(url), now)
        except Exception as e:
            print(f"  [NG] {g['id']}: {e}")
            continue
        for e in evs:
            found.setdefault(e['id'], e)
        print(f"  {g['id']:<32} 開催予定 {len(evs)}件")
        time.sleep(0.8)

    events = sorted(found.values(), key=lambda x: x['started_at'])[:MAX_EVENTS]
    rows = []
    for e in events:
        t = time.localtime(e['started_at'])
        rows.append({
            'date': time.strftime('%Y-%m-%d', t),
            'title': e['title'],
            'location': e['place'] or 'Online',
            'url': f"https://techplay.jp/event/{e['id']}",
        })

    text = json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
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

    print(f"\n開催予定イベント {len(rows)}件を {OUT} に書き出し")
    for r in rows:
        print(f"  {r['date']}  {r['title'][:52]}")
        print(f"              {r['url']}  ({r['location'][:28]})")
    if not rows:
        print("  ※ 開催予定のイベントが1件も見つかりませんでした。"
              "結果画面の「直近イベント」欄は非表示になります。")


if __name__ == '__main__':
    main()
