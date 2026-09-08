# 🧭 SnowVillage Compass (SVTI診断)

Snowflake World Tour Tokyo 2026（SWT 2026）の来場者向けに提供する、8問のルールベース診断アプリです。回答を4つの判定軸（`E`/`B`、`S`/`T`、`C`/`V`、`I`/`O`）で集計して SVTI 16タイプのいずれかを判定し、タイプカード・タイプが近い Neighbors / Mayors・おすすめのユーザーグループ・関連する Snowflake 機能・直近のイベントを提示します。

判定は固定の設問とルールによるもので、LLM は使用しません。回答の送信・保存も行いません。

> **本番の配信は SnowVillage 公式サイトへ移行しました。**
> 移行先: [snowvillage-cloud/snowvillage-cloud.github.io](https://github.com/snowvillage-cloud/snowvillage-cloud.github.io) の `swt2026/`（`https://snowvillage.cloud/swt2026`）
> 本リポジトリは移行元にあたります。GitHub Pages でも動作します: `https://mshdtksk.github.io/snow-village-compass.github.io/`

## 🔀 移行先との違い

同じ診断ですが、名簿の持ち方が異なります。移行先では名簿を公式サイトの一次情報から実行時に読み込むため、診断コードの割り当てだけを持ちます。本リポジトリは単独で動作させる必要があるため、名簿そのものを取り込んで保持します。

| | 本リポジトリ | 移行先（`swt2026/`） |
| :--- | :--- | :--- |
| 名簿の保持 | `data/neighbors.json`（氏名・所属・写真・SNS・診断コード） | `data/type-assignments.json`（氏名と診断コードのみ） |
| 名簿の取得元 | `tools/sync-people.py` で事前に取り込む | 実行時に `about/neighbors/userlist.yaml` などを読み込む |
| 人物写真 | 公式サイトの画像URLを参照 | 同一サイト内の `/images/` を参照 |
| 更新用スクリプト | `tools/` にあり | なし（JSON を直接編集） |
| CSS | `styles.css` | `../css/swt2026.css` |

## 📄 ファイルと構造

| ファイル / ディレクトリ | 役割 |
| :--- | :--- |
| **`index.html`** | ページ本体。Intro（導入）/ Quiz（設問）/ Result（結果）の3ビューを保持し、表示を切り替えて遷移します。 |
| **`app.js`** | 設問定義、タイプ判定、結果画面の描画、共有機能を担います。データの取得に失敗した場合に用いる代替値も保持します。 |
| **`styles.css`** | スタイル。ライト／ダークテーマを CSS 変数で切り替えます。 |
| **`data/`** | 診断に用いるデータ。詳細は次節を参照してください。 |
| **`logo/`** | ユーザーグループのロゴ（webp）と、`logo/types/` 配下の16タイプ用アイコン（png）。 |
| **`tools/`** | データを更新するための Python スクリプト。アプリの動作には不要です。 |

## 🔄 データ

`app.js` が実行時に読み込むのは次の5ファイルです。いずれもビルド処理を必要とせず、編集後にページを再読み込みすれば反映されます。

| ファイル | 構造 | 内容 |
| :--- | :--- | :--- |
| `data/types.json` | オブジェクト | 16タイプの定義。 |
| `data/user-groups.json` | 配列 | ユーザーグループの一覧（17件）。 |
| `data/neighbors.json` | 配列 | Neighbors / Mayors の名簿（37名）。 |
| `data/type-preferences.json` | オブジェクト | タイプ別の優先表示設定。 |
| `data/events.json` | 配列 | 結果画面に掲載するイベント。 |

次の3ファイルは `tools/` のスクリプトが読み書きするもので、アプリは参照しません。

| ファイル | 内容 |
| :--- | :--- |
| `data/survey-responses.json` | 診断アンケートの回答。診断コードの唯一の入力元です。 |
| `data/people-manual.json` | 公式サイトの名簿にまだ載っていない人を手動で足すためのファイル。現在は空です。 |
| `data/features.json` | 旧構成の機能一覧。`tools/apply-survey.py` が機能名の表記ゆれを吸収するために参照します。 |

### `types.json`

診断コードをキー、タイプ定義を値とするオブジェクトです。判定結果はいずれのコードにもなり得るため、16タイプすべてのキーを揃えてください。

```json
{
  "ESCI": {
    "code": "ESCI",
    "title": "データスーパーヒーロー",
    "subtitle": "Data Superhero (Advanced Technologist)",
    "emoji": "🦸",
    "catchphrase": "先端技術を自ら切り拓く、圧倒的データパイオニア",
    "description": "高い技術的好奇心と深い探求心を持ち、一人で最先端機能を検証・実装して成果を出すタイプです。",
    "axes": ["Explorer", "Solo", "Craft", "Innovator"],
    "colorGroup": "craft",
    "iconUrl": "logo/types/ESCI.png",
    "recommendedFeatures": [
      {
        "name": "Snowpark API",
        "description": "Python / Java / Scala で Snowflake 上にデータパイプラインや ML を実装",
        "url": "https://docs.snowflake.com/ja/developer-guide/snowpark/index"
      }
    ]
  }
}
```

| 項目 | 仕様 |
| :--- | :--- |
| `colorGroup` | 結果カードの配色を決定します。`craft` / `value` / `innovator` / `optimizer` のいずれかを指定してください。実際の配色は `styles.css` の `.result-digital-card[data-color=...]` で定義しています。 |
| `iconUrl` | `logo/types/<診断コード>.png` を指します。アイコンは16タイプ分を用意済みです。 |
| `recommendedFeatures` | 結果画面に表示する Snowflake 機能です。**このタイプに表示される機能は本項目がすべて**であり、`type-preferences.json` は表示順にのみ影響します。 |

### `neighbors.json`

人物を表すオブジェクトの配列です。`tools/sync-people.py` が公式サイトから取り込んで生成するため、**原則として手で編集しません**。

```json
[
  {
    "name": "安倍 航太",
    "affiliation": "株式会社BeeX",
    "title": "",
    "kind": "neighbor",
    "photo": "https://snowvillage-cloud.github.io/images/neighbors/abe_kota.png",
    "x_url": "https://x.com/_coco_se",
    "linkedin_url": "https://www.linkedin.com/in/kota-abe-220010398",
    "code": "ESVI"
  }
]
```

| 項目 | 仕様 |
| :--- | :--- |
| `kind` | `neighbor` または `mayor`。`mayor` は結果画面に Mayor バッジが付きます。 |
| `photo` | 公式サイトの画像URL。取り込み時に絶対URLへ変換されます。 |
| `code` | 診断コード。アンケートに回答した人だけが持ち、未回答は `null` です。**推測や仮の値を入れてはいけません**（別人が「同じタイプ」として表示されるため）。 |

### 結果画面に出る条件

Neighbors / Mayors のカードに出るのは、**次の両方を満たす人だけ**です。現在は37名中13名が該当します。

| 条件 | 理由 |
| :--- | :--- |
| `code` がある（アンケート回答済み） | 未確定の人に仮の値を入れると、まったく違うタイプの人が「あなたに近い人」として表示されるため。 |
| `photo` がある | 写真が無いとカードがほぼ空になり、会場で話しかけるきっかけとして機能しないため。 |

条件を満たさない人もデータは残るため、後から回答や写真が入れば自動的に表示されます。**画面に警告やエラーは表示しません。** 不足の把握は `data/neighbors.json` とスクリプトの実行ログで行います。

### `type-preferences.json`

診断コードをキーとし、そのタイプの回答者が実際に挙げたユーザーグループと Snowflake 機能を保持します。**表示対象を決めるものではなく、表示順を前に寄せるための設定**です。全16コードを網羅する必要はありません（現在9コード）。

```json
{
  "BSCI": {
    "groups": ["snowvillage-women", "snowvillage-main"],
    "features": ["Snowpark API", "動的テーブル"]
  }
}
```

| 項目 | 仕様 |
| :--- | :--- |
| `groups` | `user-groups.json` の `id` を指定します（表示名ではありません）。ここに挙げたグループが優先して表示され、残りの枠はタグの一致度による自動計算で補われます。定義のないコードでも、自動計算のみでグループは提示されます。 |
| `features` | `types.json` の `recommendedFeatures[].name` と完全に一致する文字列を指定します。一致した機能が先頭に並び替えられます。一致しない文字列を書いても機能は追加されず、並び替えにも使われません。 |

### `user-groups.json`

ユーザーグループを表すオブジェクトの配列です。

```json
[
  {
    "id": "snowvillage-main",
    "name": "SnowVillage - Japan Snowflake User Group",
    "abbr": "SV",
    "logoUrl": "logo/snowvillage.webp",
    "description": "日本最大級の Snowflake ユーザーコミュニティ。初心者から上級者まで、Snowflake に関わるすべての方の参加を歓迎。",
    "techplayUrl": "https://techplay.jp/community/snowvillage",
    "tags": ["latest", "lt", "meetup", "beginner", "ai"]
  }
]
```

| 項目 | 仕様 |
| :--- | :--- |
| `id` | `type-preferences.json` から参照される識別子です。 |
| `logoUrl` | `logo/` 配下の相対パス。省略した場合、ロゴの表示領域が空欄になります。画像を追加してから指定してください。 |
| `tags` | 結果画面に表示するラベルであると同時に、おすすめグループの自動計算にも用いられます。タグは TechPlay の公式タグと各コミュニティの実イベント履歴をもとに付与しています。 |

### `events.json`

イベントを表すオブジェクトの配列です。開催日の当日までを表示対象とし、それより前の日付のイベントは自動的に除外されます。対象が0件になった場合は、イベント欄自体が非表示になります。

```json
[
  {
    "date": "2026-09-11",
    "title": "Snowflake Community After Party 2026",
    "location": "SHINAGAWA PIVOT",
    "url": "https://techplay.jp/event/998891"
  }
]
```

`date` は `YYYY-MM-DD` 形式で記述してください。

## 🛠 更新用スクリプト

`tools/` の各スクリプトはデータを更新するためのもので、アプリの動作には不要です。手順の詳細は [`data/README.md`](data/README.md) を参照してください。

| スクリプト | 役割 |
| :--- | :--- |
| `tools/sync-people.py` | 公式サイトの名簿を取り込み、`data/neighbors.json` を更新します。既存の診断コードは氏名で引き継ぎます。 |
| `tools/apply-survey.py` | `data/survey-responses.json` を `data/neighbors.json` と `data/type-preferences.json` に反映します。 |
| `tools/sync-events.py` | TechPlay から開催予定のイベントを取得し、`data/events.json` を更新します。 |

いずれも Python 3 で動作します。実行にはローカル環境が必要です。

## 🖥 ローカル確認

`fetch` でデータを読み込むため、ローカルでも HTTP サーバー経由で確認してください。

```bash
python -m http.server 8000
```

`http://localhost:8000` を開き、診断を最後まで進めて、意図した人物・グループ・機能が提示されることを確認します。特定のタイプの結果だけを見たい場合は `http://localhost:8000/?code=ESCI` のようにコードを指定できます。

JSON の構文エラーや参照の不整合が生じた場合、画面上にエラーは表示されず、該当セクションが空欄になるか、既定の内容が表示されます。異常に気付きにくいため、編集後は構文の検証を実施してください。

```bash
for f in data/*.json; do python -c "import json,io,sys;json.load(io.open(sys.argv[1],encoding='utf-8'))" "$f" || echo "NG: $f"; done
```

## 💡 運用・更新のポイント

- **診断コードの出どころ**: `data/survey-responses.json` だけです。名簿の所属などから推測してはいけません。過去に推測した仮の値が原因で、別人が「同じタイプ」として表示される不具合が発生しています。
- **人物写真の参照**: `https://snowvillage-cloud.github.io/images/` を参照するため、公式サイト側で画像が移動・削除されると表示されなくなります。読み込めなかった場合はカードごと非表示にします。
- **ブランド表記**: 「SnowVillage」に統一します。語の間にスペースを入れた表記は使用しません。
- **個人情報**: 回答内容の送信および保存は行いません。ブラウザに保存するのはライト／ダークテーマの選択のみです（`localStorage` の `svc-theme`）。
- **未使用のファイル**: `js-yaml.min.js` と `data/types_matrix.tsv` は、現在どこからも参照されていません。名簿を YAML で読み込んでいた頃の名残です。
