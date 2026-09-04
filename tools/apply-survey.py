#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""アンケート回答(data/survey-responses.json)を反映する。

    python tools/apply-survey.py

1. neighbors.json の code を、回答があった人だけ確定値にする。
   回答が無い人は code を null にする（結果画面に出さないため）。
   以前は全員に仮のコードを機械的に割り当てていたが、本物と区別が
   つかず「別人が同タイプとして表示される」問題を起こしたため。

2. 回答者が挙げたグループ・機能を、そのタイプのおすすめとして
   data/type-preferences.json に集計する。複数人が挙げたものを優先し、
   同数なら回答に出てきた順を保つ。
"""
import json, os, re, sys, io, tempfile, collections, unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SURVEY = 'data/survey-responses.json'
NEIGHBORS = 'data/neighbors.json'
GROUPS = 'data/user-groups.json'
TYPES = 'data/types.json'
OUT_PREF = 'data/type-preferences.json'

# シート表記のゆらぎをグループIDに寄せる
GROUP_ALIASES = {'frostyfriday': 'Frosty Friday'}

MANUAL = 'data/people-manual.json'


def norm(name):
    """表記ゆれを吸収して名前を突き合わせる。
    全角空白・連続空白・大文字小文字の違いで別人扱いにしないため。"""
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', name or '')).strip().lower()

# アンケートは改名前の機能名で回答されているため、現行の表記に寄せる
FEATURE_ALIASES = {
    'Notebooks': 'Snowflake Notebooks',
    'Container Services': 'Snowpark Container Services',
    'Horizon Catalog': 'Snowflake Horizon カタログ',
    'Semantic Views': 'セマンティックビュー',
    'Dynamic Tables': '動的テーブル',
    'Object Tagging': 'オブジェクトタグ',
    'Network Policies': 'ネットワークポリシー',
    'Alerts': 'アラート',
    'Quickstarts': 'Snowflake Developer Guides',
    'Snowpark': 'Snowpark API',
}


def save(path, obj):
    text = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    fd, tmp = tempfile.mkstemp(suffix='.json', dir=os.path.dirname(path))
    os.close(fd)
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(text); f.flush(); os.fsync(f.fileno())
    if open(tmp, encoding='utf-8').read() != text:
        os.unlink(tmp); raise SystemExit(f"書き出し検証に失敗: {path}")
    os.replace(tmp, path)


def main():
    survey = json.load(open(SURVEY, encoding='utf-8'))['responses']
    types = json.load(open(TYPES, encoding='utf-8'))
    groups = json.load(open(GROUPS, encoding='utf-8'))
    people = json.load(open(NEIGHBORS, encoding='utf-8'))

    title2code = {v['title']: c for c, v in types.items()}
    name2gid = {g['name']: g['id'] for g in groups}
    # 機能名は types.json だけでなく features.json 側にもあるため両方を見る
    featnames = {f['name'] for v in types.values() for f in v.get('recommendedFeatures', [])}
    feats = json.load(open('data/features.json', encoding='utf-8'))
    featnames |= {f['name'] for items in feats.values() for f in items}

    # 1. code の確定 / null 化
    ans = {}
    unknown_type = []
    for r in survey:
        code = title2code.get(r['type'])
        if not code:
            unknown_type.append((r['name'], r['type'])); continue
        ans[r['name']] = code

    # 名前は表記ゆれを吸収して突き合わせる
    by_norm = {norm(n): c for n, c in ans.items()}
    confirmed = cleared = 0
    matched = set()
    for p in people:
        key = norm(p['name'])
        if key in by_norm:
            p['code'] = by_norm[key]; confirmed += 1; matched.add(key)
        else:
            p['code'] = None; cleared += 1

    # 回答はあるが名簿に居ない人は、警告で終わらせず名簿に足す。
    # 大元サイトに載っていない人でも、回答したタイプが必ず反映されるようにする。
    added = [n for n in ans if norm(n) not in matched]
    if added:
        manual = json.load(open(MANUAL, encoding='utf-8')) if os.path.exists(MANUAL) else []
        known = {norm(m['name']) for m in manual}
        for n in added:
            people.append({'name': n, 'affiliation': '', 'title': '', 'kind': 'neighbor',
                           'photo': '', 'x_url': '', 'linkedin_url': '', 'code': ans[n]})
            confirmed += 1
            if norm(n) not in known:
                manual.append({'name': n, 'affiliation': '', 'kind': 'neighbor',
                               'photo': '', 'x_url': '', 'linkedin_url': ''})
        save(MANUAL, manual)
        print(f"名簿に無かった回答者{len(added)}名を追加しました: {', '.join(added)}")
        print(f"  （{MANUAL} にも登録したので sync-people.py を再実行しても残ります）")

    save(NEIGHBORS, people)

    print(f"回答あり（確定）: {confirmed}名 / 回答なし（code=null）: {cleared}名")
    if unknown_type:
        print("★ タイプ名が types.json に無い:", unknown_type)

    dist = collections.Counter(p['code'] for p in people if p['code'])
    covered = sorted(dist)
    allcodes = [a+b+c+d for a in 'EB' for b in 'ST' for c in 'CV' for d in 'IO']
    print(f"\n確定コードの分布（{len(covered)}/16タイプ）:")
    for c in allcodes:
        mark = f"{dist[c]}名" if dist[c] else "— 該当者なし"
        print(f"  {c} {types[c]['title']:<22} {mark}")

    # 2. タイプ別のおすすめを集計
    gcnt = collections.defaultdict(collections.Counter)
    fcnt = collections.defaultdict(collections.Counter)
    unknown_g, unknown_f = set(), set()
    for r in survey:
        code = title2code.get(r['type'])
        if not code:
            continue
        for gname in r.get('groups', []):
            key = GROUP_ALIASES.get(gname, gname)
            gid = name2gid.get(key)
            if gid:
                gcnt[code][gid] += 1
            else:
                unknown_g.add(gname)
        for f in r.get('features', []):
            key = FEATURE_ALIASES.get(f, f)
            if key in featnames:
                fcnt[code][key] += 1
            else:
                unknown_f.add(f)

    pref = {c: {'groups': [g for g, _ in gcnt[c].most_common()],
                'features': [f for f, _ in fcnt[c].most_common()]}
            for c in sorted(gcnt) }
    save(OUT_PREF, pref)

    print(f"\nタイプ別おすすめを {OUT_PREF} に出力（{len(pref)}タイプ）")
    for c, v in pref.items():
        print(f"  {c} {types[c]['title']}")
        print(f"      グループ: {', '.join(v['groups'])}")
        print(f"      機能    : {', '.join(v['features']) or '（なし）'}")
    if unknown_g:
        print("\n★ user-groups.json に無いグループ名:", sorted(unknown_g))
    if unknown_f:
        print("★ types.json に無い機能名:", sorted(unknown_f))


if __name__ == '__main__':
    main()
