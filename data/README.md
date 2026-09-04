# データの更新手順

すべて `data/` 配下のJSONで動く。編集後はブラウザを再読込すれば反映される。

## Neighbors / Mayors のタイプを追加・変更する

タイプ（診断コード）は **`survey-responses.json` が唯一の入力**。
`neighbors.json` の `code` は自動生成なので直接編集しない。

1. `data/survey-responses.json` の `responses` に追記する

   ```json
   { "name": "山田 太郎", "type": "テックエバンジェリスト",
     "groups": ["SnowVillage - Japan Snowflake User Group"],
     "features": ["Cortex Analyst"] }
   ```

   - `name` は `neighbors.json` の表記と完全に一致させる
   - `type` は `types.json` の `title`（例: パイプラインマスター）
   - `groups` は `user-groups.json` の `name`、`features` は機能名。
     どちらもそのタイプのおすすめとして集計される

2. 反映する

   ```
   python tools/apply-survey.py
   ```

   回答がある人だけ `code` が入り、それ以外は `null` になる。
   同時に `type-preferences.json` が作り直される。

### 結果画面に出る条件

次の**両方**を満たす人だけが表示される。

| 条件 | 理由 |
|---|---|
| `code` がある（回答済み） | 仮の値で別人が「同タイプ」として出る事故を防ぐ |
| `photo` がある | 写真が無いとカードがほぼ空になり情報にならない |

条件を満たさない人もデータは残るので、写真が入れば自動的に出るようになる。
写真URLはあるが読み込めなかった場合も、そのカードだけ消える。

不足している人は `neighbors.json` を `code` と `photo` で見れば分かる。
アプリ画面に警告やエラーが出ることはない。

名前が一致しないと `★ neighbors.json に居ない回答者` と表示されるので、
実行結果を確認すること。

## 大元サイトの Neighbors / Mayors を取り込む

snowvillage.cloud 側で人が増えたら実行する。

```
python tools/sync-people.py
```

- ネイバーは `about/neighbors/userlist.yaml`、
  メイヤーは `about/aboutData.js` の `mayorsData` から取得する
- 既存の `code` は名前をキーに引き継ぐ。新しく増えた人は `null` から始まる
- 大元サイトにまだ載っていない人は `people-manual.json` に書いておくと
  マージされる。大元側に載ったらそこから削除してよい

## イベントを更新する

```
python tools/sync-events.py
```

TechPlay の全コミュニティページから **開催予定のものだけ** を取得する。
過去のイベントは表示側でも除外され、0件になると欄ごと消える。

## アイコン

`logo/types/<コード>.png`。`types.json` の `iconUrl` が参照する。
`colorGroup` が結果カードの配色（craft / value / innovator / optimizer）を決め、
実際の色は `styles.css` の `.result-digital-card[data-color=...]` にある。
