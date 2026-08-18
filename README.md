# snow-village-compass

Snow Villageコミュニティ向けの「8問・ルールベース診断」Webアプリです。  
SWT 2026来場者（特に初心者）に、参加しやすいコミュニティとネイバーを提案します。

## 特徴

- 8問の固定設問による短時間診断（約2分）
- ルールベース判定（LLM不使用）
- 診断結果:
  - ユーザータイプ（称号）
  - おすすめユーザーグループ（19以上）
  - おすすめネイバー（約30名データ）
  - おすすめSnowflake機能
- 外部アクション:
  - Tech Play / 登録ページリンク
  - X共有・メール送信
  - 直近イベント表示
- ライト/ダークテーマ切替
- 個人情報を収集しない設計

## 構成

- `index.html`: UI本体
- `styles.css`: スタイル
- `app.js`: 診断ロジック・表示制御
- `data/user-groups.json`: ユーザーグループ定義
- `data/neighbors.yml`: ネイバー定義
- `data/events.json`: イベント定義

> ネイバー情報は、実行時に以下の公式YAMLを優先して取得します。  
> https://github.com/snowvillage-cloud/snowvillage-cloud.github.io/blob/main/about/neighbors/userlist.yaml  
> 取得失敗時のみ `data/neighbors.yml` を利用します。

## ローカル確認

`fetch` でデータを読み込むため、ローカルでもHTTPサーバー経由で起動してください。

```powershell
cd c:\Users\desktop\VisualStodioCode\snow-village-compass
python -m http.server 8000
```

ブラウザで `http://localhost:8000` を開きます。

## GitHub Pages公開

このリポジトリをGitHubにpush後、Pagesを有効化すると静的サイトとして公開できます。
