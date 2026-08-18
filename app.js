const questions = [
  {
    id: 1,
    text: "SWT会場で一番やってみたいことは？",
    options: [
      { text: "セッションを回って知識を集める", score: { analysis: 2, governance: 1 } },
      { text: "ブースで実際に手を動かして試す", score: { build: 2, creativity: 1 } },
      { text: "人に話しかけて仲間を増やす", score: { community: 2, leadership: 1 } }
    ]
  },
  {
    id: 2,
    text: "新しい技術に触れるときのスタイルは？",
    options: [
      { text: "まず資料を読んで全体像をつかむ", score: { analysis: 2 } },
      { text: "まず触って動かしてみる", score: { build: 2 } },
      { text: "誰かと一緒に試して学ぶ", score: { community: 2 } }
    ]
  },
  {
    id: 3,
    text: "チームでの役割として近いのは？",
    options: [
      { text: "進行を整えるファシリテーター", score: { leadership: 2, governance: 1 } },
      { text: "実装を前進させるビルダー", score: { build: 2, leadership: 1 } },
      { text: "洞察を出すアナリスト", score: { analysis: 2, creativity: 1 } }
    ]
  },
  {
    id: 4,
    text: "惹かれるSnowflakeトピックは？",
    options: [
      { text: "データ基盤・パイプライン", score: { build: 2, analysis: 1 } },
      { text: "ガバナンス・セキュリティ", score: { governance: 2, analysis: 1 } },
      { text: "アプリ開発・体験設計", score: { creativity: 2, community: 1 } }
    ]
  },
  {
    id: 5,
    text: "コミュニティに参加する目的は？",
    options: [
      { text: "同じ関心の仲間とつながりたい", score: { community: 2 } },
      { text: "スキルを磨いて成果を出したい", score: { build: 2, analysis: 1 } },
      { text: "挑戦を後押ししてもらいたい", score: { leadership: 1, community: 1, creativity: 1 } }
    ]
  },
  {
    id: 6,
    text: "課題にぶつかったとき、まずどうする？",
    options: [
      { text: "原因を切り分けて整理する", score: { analysis: 2, governance: 1 } },
      { text: "最小のプロトタイプを作る", score: { build: 2, creativity: 1 } },
      { text: "詳しい人に相談しながら進める", score: { community: 2, leadership: 1 } }
    ]
  },
  {
    id: 7,
    text: "2日目ナイトパーティーで楽しみなのは？",
    options: [
      { text: "タイプ別チームで会話すること", score: { community: 2, leadership: 1 } },
      { text: "プロダクトや作品の話をすること", score: { creativity: 2, build: 1 } },
      { text: "知見交換して次の学びを決めること", score: { analysis: 2, governance: 1 } }
    ]
  },
  {
    id: 8,
    text: "この診断の後に一番やりたいアクションは？",
    options: [
      { text: "気になるグループへすぐ登録する", score: { community: 2, leadership: 1 } },
      { text: "機能を試せるハンズオンに出る", score: { build: 2, creativity: 1 } },
      { text: "おすすめネイバーに声をかける", score: { community: 1, analysis: 1, leadership: 1 } }
    ]
  }
];

const NEIGHBORS_REMOTE_URL = "https://raw.githubusercontent.com/snowvillage-cloud/snowvillage-cloud.github.io/main/about/neighbors/userlist.yaml";
const GROUPS_REMOTE_URL = "https://raw.githubusercontent.com/mshdtksk/snow-village-compass/main/sub-community-list.yaml";
const NEIGHBOR_PHOTO_BASE = "https://snowvillage-cloud.github.io/images/neighbors/";

const typeDefinitions = {
  dataSuperhero: {
    title: "データスーパーヒーロー",
    description: "分析力と実装力で、課題をデータで解決する実践派。まずはハンズオン系コミュニティから始めると仲間が見つかります。",
    tags: ["analysis", "build", "data", "hands-on"],
    featureRecommendations: ["Snowpark", "Dynamic Tables", "Tasks", "Notebooks"],
    actionHints: ["ブースでタイプ別カードを受け取る", "ナイトパーティーで同タイプとチーム交流する", "会場でおすすめネイバーを探して声をかける"]
  },
  dreamTeamCreator: {
    title: "ドリームチームクリエイター",
    description: "人をつなげる力が強み。コミュニティの中心で、学びと交流の場を生み出すタイプです。",
    tags: ["community", "leadership", "network", "event"],
    featureRecommendations: ["Native Apps", "Streamlit in Snowflake", "Snowsight Dashboards", "Marketplace"],
    actionHints: ["タイプ別カードで交流のきっかけを作る", "気になったグループにその場で登録する", "イベント告知から次回参加予定を決める"]
  },
  insightNavigator: {
    title: "インサイトナビゲーター",
    description: "ガバナンスと分析のバランス感覚が高く、チームの意思決定を支えるタイプです。",
    tags: ["analysis", "governance", "quality", "architecture"],
    featureRecommendations: ["Horizon Catalog", "Row Access Policy", "Masking Policy", "Data Quality Monitoring"],
    actionHints: ["ガバナンス系セッションに参加する", "設計が得意なネイバーと会場で対話する", "関連グループへ登録して継続学習する"]
  },
  automationAlchemist: {
    title: "オートメーションアルケミスト",
    description: "試作と改善のループが速い、ものづくりタイプ。自動化の仕組み化が得意です。",
    tags: ["build", "creativity", "automation", "engineering"],
    featureRecommendations: ["Snowpipe", "Streams & Tasks", "Cortex Functions", "Git Integration"],
    actionHints: ["ハンズオン中心のグループを優先登録する", "自動化事例をネイバーに相談する", "ナイトパーティーで制作系の仲間を見つける"]
  },
  trustGuardian: {
    title: "トラストガーディアン",
    description: "安全性と運用性を守りながら前進させる頼れるタイプ。組織に安心をもたらします。",
    tags: ["governance", "leadership", "security", "ops"],
    featureRecommendations: ["Object Tagging", "Access History", "Network Policies", "Tri-Secret Secure"],
    actionHints: ["運用・セキュリティ系コミュニティに参加する", "会場で同領域のネイバーを探す", "チーム分け交流で運用課題を共有する"]
  },
  storySparkAmbassador: {
    title: "ストーリースパークアンバサダー",
    description: "伝える力で価値を広げるタイプ。発信やコミュニティ活性の場で力を発揮します。",
    tags: ["creativity", "community", "story", "sharing"],
    featureRecommendations: ["Snowsight", "Streamlit", "Semantic Views", "Cortex Analyst"],
    actionHints: ["X共有で診断結果を発信する", "発信系・コミュニティ運営系グループに参加する", "ネイバーとコラボのきっかけを作る"]
  },
  frontierExplorer: {
    title: "フロンティアエクスプローラー",
    description: "新領域に飛び込み、学びを実践に変える挑戦型。最初の一歩が速いタイプです。",
    tags: ["build", "community", "challenge", "beginner-friendly"],
    featureRecommendations: ["Quickstarts", "Snowflake Marketplace", "Snowflake ML", "Container Services"],
    actionHints: ["初心者歓迎グループに登録する", "おすすめネイバーに自己紹介してみる", "次回イベント参加をその場で決める"]
  },
  calmMentor: {
    title: "カームメンター",
    description: "落ち着いた視点で周囲を支えるタイプ。知見共有や相談相手として信頼されます。",
    tags: ["leadership", "analysis", "mentoring", "support"],
    featureRecommendations: ["Data Sharing", "Secure Views", "Notebooks", "Alerts"],
    actionHints: ["相談しやすいネイバーとして交流する", "初心者支援系コミュニティに参加する", "タイプ別カードを使って会話を始める"]
  }
};

// ── インライン埋め込みデータ（リモート取得失敗時のフォールバック） ──────────────
const INLINE_GROUPS = [
  { id: "snowvillage-main",          abbr: "SV",     logoUrl: "logo/snowvillage.webp",                          name: "SnowVillage - Japan Snowflake User Group",           description: "日本最大級のSnowflakeユーザーコミュニティ。初心者から上級者まで参加歓迎。",                                          techplayUrl: "https://techplay.jp/community/snowvillage",                              tags: ["community", "beginner-friendly", "event", "data"] },
  { id: "snowvillage-financial",     abbr: "金融",   logoUrl: "logo/snowvillage-financial.webp",                name: "Snowflake金融ユーザー会",                              description: "金融業界でのSnowflake活用をテーマに、ガバナンス・セキュリティ・分析の知見を業界横断で共有。",              techplayUrl: "https://techplay.jp/community/snowvillage-financial",                    tags: ["governance", "security", "analysis", "data"] },
  { id: "snowvillage-data-management", abbr: "DM",   logoUrl: "logo/snowvillage-data-management.webp",          name: "SnowVillage - データマネジメント分科会 -",             description: "データ品質・カタログ・メタデータ管理を深掘りする分科会。",                                                    techplayUrl: "https://techplay.jp/community/snowvillage-data-management",              tags: ["governance", "data", "quality", "architecture"] },
  { id: "snowflake-rookies-camp",    abbr: "RC",     logoUrl: "logo/snowvillage-snowflake-rookies-camp.webp",   name: "Snowflake Rookies Camp",                               description: "Snowflakeをこれから学びたい方向けの初心者コミュニティ。ハンズオンでベストプラクティスを学べる。",              techplayUrl: "https://techplay.jp/community/snowvillage-snowflake-rookies-camp",       tags: ["beginner-friendly", "hands-on", "community", "support"] },
  { id: "snowvillage-west",          abbr: "WEST",   logoUrl: "logo/snowvillage-west.webp",                     name: "Snowflake WEST User Group",                           description: "関西地域を中心としたSnowflakeユーザーコミュニティ。ハンズオン・ミートアップを通じて西日本を活性化。",            techplayUrl: "https://techplay.jp/community/snowvillage-west",                         tags: ["community", "event", "hands-on", "data"] },
  { id: "snowvillage-datascience",   abbr: "DS/DE",  logoUrl: "logo/snowvillage-datascience.webp",              name: "SnowVillage DataScience&DataEngineering支部",          description: "DataScience・DataEngineeringチャネルのイベントを運営するコミュニティ。",                                       techplayUrl: "https://techplay.jp/community/snowvillage-datascience",                  tags: ["analysis", "engineering", "data", "challenge"] },
  { id: "snowvillage-women",         abbr: "女子会", logoUrl: "logo/snowvillage-women.webp",                    name: "Snowflake女子会",                                      description: "女性エンジニア同士のつながりと活躍の場を作るコミュニティ。初心者から経験者まで参加可能。",                      techplayUrl: "https://techplay.jp/community/snowvillage-women",                        tags: ["community", "support", "hands-on", "beginner-friendly"] },
  { id: "snowvillage-unconference",  abbr: "UNC",    logoUrl: "logo/snowvillage-unconference.webp",             name: "SnowVillage Unconference支部",                         description: "参加者主体で知識共有と交流を深めるUnconferenceイベントを運営するコミュニティ。",                               techplayUrl: "https://techplay.jp/community/snowvillage-unconference",                 tags: ["event", "community", "leadership", "network"] },
  { id: "snowvillage-kyushu",        abbr: "九州",   logoUrl: "logo/snowvillage-kyushu.webp",                   name: "Snowflake Kyushu User Group",                         description: "Snowflakeの良さを九州企業に届け、データで九州を盛り上げることを目指すグループ。",                            techplayUrl: "https://techplay.jp/community/snowvillage-kyushu",                       tags: ["community", "event", "data", "beginner-friendly"] },
  { id: "snowvillage-ai-data-cloud", abbr: "AI",     logoUrl: "logo/snowvillage-ai-data-cloud.webp",            name: "SnowVillage AI DATA User Group",                       description: "SnowflakeのAI関連機能をテーマに定期的な勉強会・情報交換を行うコミュニティ。",                                  techplayUrl: "https://techplay.jp/community/snowvillage-ai-data-cloud",                tags: ["challenge", "data", "app", "creativity"] },
  { id: "snowvillage-healthcare",    abbr: "HC",     logoUrl: "logo/snowvillage-healthcare.webp",               name: "Snowflakeヘルスケア・ライフサイエンスユーザー会",      description: "ヘルスケア・ライフサイエンス業界でのSnowflake活用をテーマに、事例共有を通じて業界全体の発展を目指す。",          techplayUrl: "https://techplay.jp/community/snowvillage-healthcare",                   tags: ["governance", "analysis", "data", "community"] },
  { id: "sf2ug",                     abbr: "SF×SF",  logoUrl: "logo/sf2ug.webp",                                name: "Snowflake x Salesforce User Group",                   description: "Snowflake と Salesforce を掛け合わせたデータ活用について議論するUser Group。",                                techplayUrl: "https://techplay.jp/community/sf2ug",                                    tags: ["engineering", "app", "build", "data"] },
  { id: "snowvillage-central",       abbr: "中部",   logoUrl: "logo/snowvillage-central.webp",                  name: "Snowflake CENTRAL User Group",                        description: "中部エリアを中心としたSnowflakeユーザーコミュニティ。活用事例・最新機能・データ分析の知見を共有。",              techplayUrl: "https://techplay.jp/community/snowvillage-central",                      tags: ["community", "event", "data", "analysis"] },
  { id: "snowvillage-sustainability", abbr: "🌱SV", logoUrl: "logo/snowvillage-sustainability.webp",           name: "SnowVillage サステナvillage",                          description: "サステナビリティをテーマとするコミュニティ。Snowflakeを活用しながらサステナブルな取り組みを後押し。",          techplayUrl: "https://techplay.jp/community/snowvillage-sustainability",               tags: ["story", "community", "governance", "creativity"] },
  { id: "snowvillage-okinawa",       abbr: "沖縄",   logoUrl: "logo/snowvillage-okinawa.webp",                  name: "Snowflake OKINAWA User Group",                        description: "Snowflakeの技術情報を沖縄から発信し、ユーザーコミュニティの活性化を目指すグループ。",                          techplayUrl: "https://techplay.jp/community/snowvillage-okinawa",                      tags: ["community", "event", "beginner-friendly", "data"] }
];

const INLINE_NEIGHBORS = [
  { name: "Sate Katsuaki",      affiliation: "",                           photo_url: NEIGHBOR_PHOTO_BASE+"sate_katsuaki.png",     x_url: "https://x.com/katsu_dailylake",  linkedin_url: "",                                                tags: ["community", "data"] },
  { name: "安倍 航太",           affiliation: "株式会社BeeX",               photo_url: NEIGHBOR_PHOTO_BASE+"abe_kota.png",           x_url: "https://x.com/_coco_se",         linkedin_url: "https://www.linkedin.com/in/kota-abe-220010398",  tags: ["engineering", "build", "data"] },
  { name: "Daisuke Onoe",       affiliation: "",                           photo_url: NEIGHBOR_PHOTO_BASE+"daisuke_onoe.png",       x_url: "https://x.com/wonohe",           linkedin_url: "",                                                tags: ["community", "data"] },
  { name: "山本 且秋",           affiliation: "株式会社アシスト",           photo_url: NEIGHBOR_PHOTO_BASE+"kayamamoto.png",         x_url: "https://x.com/kayamamoto_",      linkedin_url: "https://www.linkedin.com/in/katsuaki-yamamoto-2b3692329", tags: ["data", "analysis"] },
  { name: "Tatchan",            affiliation: "AI Data Cloud",              photo_url: NEIGHBOR_PHOTO_BASE+"tatchan.png",            x_url: "https://x.com/tad_ao",           linkedin_url: "https://www.linkedin.com/in/tadashi-aobayashi-a93790126/", tags: ["data", "community", "challenge"] },
  { name: "Kaori Nishimura",    affiliation: "株式会社メソドロジック",     photo_url: NEIGHBOR_PHOTO_BASE+"nishimurakaori.jpg",     x_url: "https://x.com/usakoyama",        linkedin_url: "https://www.linkedin.com/in/kaori-nishimura-180368168/", tags: ["community", "event"] },
  { name: "ぬん",               affiliation: "",                           photo_url: NEIGHBOR_PHOTO_BASE+"guen.png",               x_url: "https://x.com/guen",             linkedin_url: "",                                                tags: ["community"] },
  { name: "萩野谷 旭洋",         affiliation: "インフォテック株式会社",     photo_url: NEIGHBOR_PHOTO_BASE+"haginoya_teruhiro.png",  x_url: "https://x.com/_hgny_s67",        linkedin_url: "",                                                tags: ["engineering", "data"] },
  { name: "山口 歩夢",           affiliation: "DATUM STUDIO株式会社",       photo_url: NEIGHBOR_PHOTO_BASE+"yamaguchi_ayumu.png",    x_url: "https://x.com/Yamaguchi_aaaaa",  linkedin_url: "",                                                tags: ["engineering", "build", "data"] },
  { name: "守川 耀",             affiliation: "DATUM STUDIO株式会社",       photo_url: NEIGHBOR_PHOTO_BASE+"morikawa_yo.png",        x_url: "https://x.com/elc_small",        linkedin_url: "https://www.linkedin.com/in/yo-morikawa-68787234a", tags: ["engineering", "build", "data"] },
  { name: "tomo Wakamatsu",     affiliation: "Snowflake合同会社",           photo_url: NEIGHBOR_PHOTO_BASE+"tomo.png",               x_url: "https://x.com/tomowk1",          linkedin_url: "https://www.linkedin.com/in/tomo-wakamatsu/",     tags: ["community", "event", "data"] },
  { name: "森田 将之",           affiliation: "株式会社ＪＥＲＡ",           photo_url: NEIGHBOR_PHOTO_BASE+"morita_masayuki.png",    x_url: "https://x.com/mark_xxxx13",      linkedin_url: "https://www.linkedin.com/in/masayuki-morita-710807215", tags: ["data", "analysis"] },
  { name: "神谷 篤司",           affiliation: "セキュリティ系の会社",       photo_url: NEIGHBOR_PHOTO_BASE+"atsushi_kamiya.jpg",     x_url: "https://x.com/baihebu",          linkedin_url: "https://www.linkedin.com/in/atsushi-kamiya-93584571", tags: ["security", "governance"] },
  { name: "中山 晋一",           affiliation: "株式会社電通総研",           photo_url: NEIGHBOR_PHOTO_BASE+"nakayama_shinichi.jpg",  x_url: "https://x.com/datashin360",      linkedin_url: "https://www.linkedin.com/in/shinichi-nakayama-280902191/", tags: ["data", "analysis", "engineering"] },
  { name: "アスタ",              affiliation: "",                           photo_url: NEIGHBOR_PHOTO_BASE+"tsunoda_katsuma.png",    x_url: "https://x.com/ASTOUND_",         linkedin_url: "https://www.linkedin.com/in/katsunoda-0339313a8",  tags: ["community", "challenge"] },
  { name: "ロー / LowSE01",     affiliation: "ちゅらデータ株式会社",       photo_url: NEIGHBOR_PHOTO_BASE+"lowse01.jpg",            x_url: "https://x.com/VizFantasista",    linkedin_url: "https://www.linkedin.com/in/lowse01/",            tags: ["story", "creativity", "app"] },
  { name: "伊佐 薫明",           affiliation: "",                           photo_url: NEIGHBOR_PHOTO_BASE+"nobu_13.jpg",            x_url: "https://x.com/Nobu13tech",       linkedin_url: "https://www.linkedin.com/in/no-isa/",             tags: ["community", "data"] },
  { name: "原田 雄斗",           affiliation: "クオリサイトテクノロジーズ", photo_url: NEIGHBOR_PHOTO_BASE+"harada_yuto.png",        x_url: "https://x.com/HYuto30325",       linkedin_url: "",                                                tags: ["data", "analysis"] },
  { name: "横澤 直樹",           affiliation: "株式会社メディアフォース",   photo_url: NEIGHBOR_PHOTO_BASE+"naoki_yokozawa.jpeg",    x_url: "https://x.com/naoki_yokozawa",   linkedin_url: "",                                                tags: ["data", "community"] },
  { name: "Masaki Moriyama",    affiliation: "",                           photo_url: NEIGHBOR_PHOTO_BASE+"masaki_moriyama.png",    x_url: "https://x.com/masa_tectec",      linkedin_url: "",                                                tags: ["community"] },
  { name: "柴田 祐大",           affiliation: "株式会社ロイヤリティマーケティング", photo_url: NEIGHBOR_PHOTO_BASE+"yoshihiro_shibata.png", x_url: "",                        linkedin_url: "",                                                tags: ["data", "analysis"] },
  { name: "加藤 智也",           affiliation: "",                           photo_url: NEIGHBOR_PHOTO_BASE+"tomoya_kato.png",        x_url: "",                               linkedin_url: "https://www.linkedin.com/in/tomoya-kato-466875394", tags: ["community"] },
  { name: "滝川 皇",             affiliation: "",                           photo_url: NEIGHBOR_PHOTO_BASE+"takigawa_mikoto.jpg",    x_url: "https://x.com/takimiko_gohan",   linkedin_url: "https://www.linkedin.com/in/mikoto-takigawa-baa587373", tags: ["community", "data"] },
  { name: "Ryo Toshiki",        affiliation: "",                           photo_url: NEIGHBOR_PHOTO_BASE+"t_ryo.jpg",              x_url: "https://x.com/tryo_sing",        linkedin_url: "",                                                tags: ["community"] },
  { name: "Kazuya Iwata",       affiliation: "DATUM STUDIO株式会社",       photo_url: NEIGHBOR_PHOTO_BASE+"iwata.png",              x_url: "",                               linkedin_url: "",                                                tags: ["engineering", "build", "data"] },
  { name: "田代 学",             affiliation: "ちゅらデータ株式会社",       photo_url: NEIGHBOR_PHOTO_BASE+"gaku_tashiro.jpg",       x_url: "https://x.com/gak_t12",          linkedin_url: "https://www.linkedin.com/in/gakut12/",            tags: ["data", "engineering"] },
  { name: "Yuta Hishinuma",     affiliation: "ちゅらデータ株式会社",       photo_url: NEIGHBOR_PHOTO_BASE+"yuta_hishinuma.jpg",     x_url: "https://x.com/foursue",          linkedin_url: "",                                                tags: ["data", "engineering"] }
];

const INLINE_EVENTS = [
  { date: "2026-09-11", title: "Snowflake World Tokyo 2026 Day 1", location: "東京国際フォーラム", url: "https://www.snowflake.com/events/snowflake-world-tour/" },
  { date: "2026-09-12", title: "Snowflake World Tokyo 2026 Day 2 + ナイトパーティー", location: "東京国際フォーラム", url: "https://www.snowflake.com/events/snowflake-world-tour/" },
  { date: "2026-09-19", title: "Snow Village SWT振り返り回", location: "Online", url: "https://techplay.jp/community/snowvillage" },
  { date: "2026-10-02", title: "Snowflake Rookies Camp — SWT後ハンズオン", location: "Tokyo", url: "https://techplay.jp/community/snowvillage-snowflake-rookies-camp" },
  { date: "2026-10-15", title: "SnowVillage DataScience&DE 支部 勉強会", location: "Online", url: "https://techplay.jp/community/snowvillage-datascience" }
];

const INLINE_FEATURES = {
  dataSuperhero:        [{ name: "Snowpark",        description: "Python/Java/ScalaでSnowflake上に直接データパイプラインやMLを実装",  url: "https://docs.snowflake.com/ja/developer-guide/snowpark/index" }, { name: "Dynamic Tables", description: "宣言的にデータ変換パイプラインを定義し自動的に最新化", url: "https://docs.snowflake.com/ja/user-guide/dynamic-tables-intro" }, { name: "Notebooks", description: "Snowflake上でインタラクティブにデータ探索・分析・可視化", url: "https://docs.snowflake.com/ja/user-guide/ui-snowsight-notebooks-gs" }],
  dreamTeamCreator:     [{ name: "Native Apps",             description: "Snowflakeマーケットプレイスで配布できるアプリを構築・公開", url: "https://docs.snowflake.com/ja/developer-guide/native-apps/native-apps-about" }, { name: "Streamlit in Snowflake", description: "データアプリをコード1枚でSnowflake上に即デプロイ", url: "https://docs.snowflake.com/ja/developer-guide/streamlit/about-streamlit" }, { name: "Snowflake Marketplace", description: "データ・アプリ・モデルを社外と安全に共有・公開", url: "https://docs.snowflake.com/ja/user-guide/data-sharing-marketplace" }],
  insightNavigator:     [{ name: "Horizon Catalog",     description: "メタデータ・系譜・品質を一元管理するデータカタログ機能",     url: "https://docs.snowflake.com/ja/guides-overview-govern" }, { name: "Row Access Policy", description: "行レベルでのアクセス制御をポリシーで一元管理", url: "https://docs.snowflake.com/ja/user-guide/security-row-intro" }, { name: "Data Quality Monitor", description: "データの品質指標を継続的に計測・アラートで監視", url: "https://docs.snowflake.com/ja/user-guide/data-quality-intro" }],
  automationAlchemist:  [{ name: "Snowpipe",        description: "ファイル到着をトリガーにリアルタイムでデータをロード",           url: "https://docs.snowflake.com/ja/user-guide/data-load-snowpipe-intro" }, { name: "Streams & Tasks", description: "変更データキャプチャ(CDC)とスケジュール実行で自動化パイプライン", url: "https://docs.snowflake.com/ja/user-guide/streams-intro" }, { name: "Git Integration", description: "GitHubリポジトリを直接Snowflakeに接続してコードを管理", url: "https://docs.snowflake.com/ja/developer-guide/git/git-setting-up" }],
  trustGuardian:        [{ name: "Object Tagging",   description: "テーブル・列にタグを付与してガバナンス・分類を自動化",         url: "https://docs.snowflake.com/ja/user-guide/object-tagging" }, { name: "Access History", description: "誰がいつどのデータにアクセスしたかを完全な監査ログで追跡", url: "https://docs.snowflake.com/ja/sql-reference/account-usage/access_history" }, { name: "Network Policies", description: "IPアドレス・プライベートリンクによる接続制限でセキュリティ強化", url: "https://docs.snowflake.com/ja/user-guide/network-policies" }],
  storySparkAmbassador: [{ name: "Snowsight",        description: "インタラクティブなダッシュボードと可視化でデータをストーリーに", url: "https://docs.snowflake.com/ja/user-guide/ui-snowsight" }, { name: "Cortex Analyst", description: "自然言語でデータを問い合わせ・分析できるAIアシスタント", url: "https://docs.snowflake.com/ja/user-guide/snowflake-cortex/cortex-analyst" }, { name: "Semantic Views", description: "ビジネス用語でデータモデルを定義しAIと人間が理解しやすく", url: "https://docs.snowflake.com/ja/user-guide/views-introduction" }],
  frontierExplorer:     [{ name: "Quickstarts",      description: "Snowflakeを素早く試せるステップバイステップのガイド集",    url: "https://quickstarts.snowflake.com/" }, { name: "Snowflake ML", description: "Snowflake上でモデル学習から推論まで完結するML基盤", url: "https://docs.snowflake.com/ja/guides-overview-ml-functions" }, { name: "Container Services", description: "Snowflakeのエコシステム内でコンテナアプリを実行", url: "https://docs.snowflake.com/ja/developer-guide/snowpark-container-services/overview" }],
  calmMentor:           [{ name: "Secure Data Sharing", description: "コピーなしでデータをリアルタイムに安全共有",             url: "https://docs.snowflake.com/ja/user-guide/data-sharing-intro" }, { name: "Notebooks", description: "Snowflake上でインタラクティブにデータ探索・分析・可視化", url: "https://docs.snowflake.com/ja/user-guide/ui-snowsight-notebooks-gs" }, { name: "Alerts", description: "データ変化やしきい値超過を検知して通知・アクション自動化", url: "https://docs.snowflake.com/ja/user-guide/alerts" }]
};
// ──────────────────────────────────────────────────────────────────────────────

const state = {
  index: 0,
  answers: [],
  groups: [],
  neighbors: [],
  events: [],
  features: {}
};

const viewRefs = {
  intro: document.getElementById("intro-view"),
  quiz: document.getElementById("quiz-view"),
  result: document.getElementById("result-view")
};

const questionText = document.getElementById("question-text");
const optionRoot = document.getElementById("options");
const progressLabel = document.getElementById("progress-label");
const progressFill = document.getElementById("progress-fill");
const resultTitle = document.getElementById("result-title");
const resultDescription = document.getElementById("result-description");
const groupList = document.getElementById("group-list");
const neighborList = document.getElementById("neighbor-list");
const featureList = document.getElementById("feature-list");
const eventList = document.getElementById("event-list");
const actionList = document.getElementById("action-list");

document.getElementById("start-button").addEventListener("click", startQuiz);
document.getElementById("restart").addEventListener("click", resetApp);
document.getElementById("theme-toggle").addEventListener("click", toggleTheme);
document.getElementById("share-x").addEventListener("click", shareToX);
document.getElementById("share-mail").addEventListener("click", shareByMail);

initializeTheme();
const dataReady = initializeData();

async function initializeData() {
  const [groups, neighbors, events, features] = await Promise.all([
    loadGroupsData(),
    loadNeighborsData(),
    loadEventsData(),
    loadFeaturesData()
  ]);
  state.groups = groups;
  state.neighbors = neighbors;
  state.events = events;
  state.features = features;
}

async function loadGroupsData() {
  // data/user-groups.json を優先（logoUrl/abbr情報を保持）
  try {
    const res = await fetch("data/user-groups.json");
    if (!res.ok) throw new Error(`status ${res.status}`);
    return normalizeGroups(await res.json());
  } catch { /* fallthrough */ }
  // リモートYAMLへフォールバック
  try {
    const res = await fetch(GROUPS_REMOTE_URL);
    if (!res.ok) throw new Error(`status ${res.status}`);
    return normalizeGroups(jsyaml.load(await res.text()));
  } catch { /* fallthrough */ }
  // 最終フォールバック: インラインデータ
  return INLINE_GROUPS;
}

async function loadNeighborsData() {
  try {
    const res = await fetch(NEIGHBORS_REMOTE_URL);
    if (!res.ok) throw new Error(`status ${res.status}`);
    return normalizeNeighbors(jsyaml.load(await res.text()));
  } catch {
    // リモート取得失敗 → インラインデータを使用
    return INLINE_NEIGHBORS;
  }
}

async function loadEventsData() {
  try {
    const res = await fetch("data/events.json");
    if (!res.ok) throw new Error(`status ${res.status}`);
    return res.json();
  } catch {
    return INLINE_EVENTS;
  }
}

async function loadFeaturesData() {
  try {
    const res = await fetch("data/features.json");
    if (!res.ok) throw new Error(`status ${res.status}`);
    return res.json();
  } catch {
    return INLINE_FEATURES;
  }
}

function initializeTheme() {
  const saved = localStorage.getItem("svc-theme");
  const theme = saved || "light";
  document.documentElement.setAttribute("data-theme", theme);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme") || "light";
  const next = current === "light" ? "dark" : "light";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem("svc-theme", next);
}

async function startQuiz() {
  await dataReady;
  state.index = 0;
  state.answers = [];
  switchView("quiz");
  renderQuestion();
}

function resetApp() {
  state.index = 0;
  state.answers = [];
  switchView("intro");
}

function switchView(key) {
  for (const name of Object.keys(viewRefs)) {
    viewRefs[name].classList.toggle("hidden", name !== key);
  }
}

const TYPE_ICONS = {
  dataSuperhero:        "🦸",
  dreamTeamCreator:     "🌐",
  insightNavigator:     "🔭",
  automationAlchemist:  "⚗️",
  trustGuardian:        "🛡️",
  storySparkAmbassador: "✨",
  frontierExplorer:     "🚀",
  calmMentor:           "🌿"
};

function renderQuestion() {
  const question = questions[state.index];
  const pct = Math.round(((state.index + 1) / questions.length) * 100);
  progressLabel.textContent = `Q${state.index + 1} / ${questions.length}`;
  document.getElementById("progress-pct").textContent = `${pct}%`;
  progressFill.style.width = `${pct}%`;
  questionText.textContent = question.text;
  optionRoot.innerHTML = "";

  question.options.forEach((option) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "secondary-button option-button";
    button.textContent = option.text;
    button.addEventListener("click", () => selectAnswer(option.score));
    optionRoot.appendChild(button);
  });
}

function selectAnswer(score) {
  state.answers.push(score);
  if (state.index < questions.length - 1) {
    state.index += 1;
    renderQuestion();
    return;
  }
  showResult();
}

function showResult() {
  const scores = aggregateScores(state.answers);
  const topDimensions = getTopDimensions(scores);
  const typeKey = resolveType(topDimensions);
  const type = typeDefinitions[typeKey];
  const recommendedGroups = getRecommendedGroups(type, topDimensions);
  const recommendedNeighbors = getRecommendedNeighbors(type, topDimensions);
  const features = (state.features[typeKey] || type.featureRecommendations || []).slice(0, 3);

  document.getElementById("result-icon").textContent = TYPE_ICONS[typeKey] || "🌟";
  resultTitle.textContent = type.title;
  resultDescription.textContent = type.description;
  renderNeighbors(recommendedNeighbors.slice(0, 3));
  renderGroups(recommendedGroups.slice(0, 3));
  renderFeatures(features);
  renderEvents(state.events.slice(0, 3));
  renderActions(type.actionHints.slice(0, 3));

  switchView("result");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function aggregateScores(answers) {
  const base = { community: 0, build: 0, analysis: 0, creativity: 0, governance: 0, leadership: 0 };
  answers.forEach((score) => {
    Object.entries(score).forEach(([key, value]) => {
      base[key] += value;
    });
  });
  return base;
}

function getTopDimensions(scores) {
  return Object.entries(scores)
    .sort((a, b) => b[1] - a[1])
    .map(([name]) => name)
    .slice(0, 3);
}

function resolveType([first, second, third]) {
  const map = {
    "analysis:build": "dataSuperhero",
    "build:analysis": "dataSuperhero",
    "community:leadership": "dreamTeamCreator",
    "leadership:community": "dreamTeamCreator",
    "analysis:governance": "insightNavigator",
    "governance:analysis": "insightNavigator",
    "build:creativity": "automationAlchemist",
    "creativity:build": "automationAlchemist",
    "governance:leadership": "trustGuardian",
    "leadership:governance": "trustGuardian",
    "creativity:community": "storySparkAmbassador",
    "community:creativity": "storySparkAmbassador",
    "build:community": "frontierExplorer",
    "community:build": "frontierExplorer",
    "leadership:analysis": "calmMentor",
    "analysis:leadership": "calmMentor"
  };
  const pairKey = `${first}:${second}`;
  if (map[pairKey]) {
    return map[pairKey];
  }
  const fallbackByTop = {
    analysis: "insightNavigator",
    build: "automationAlchemist",
    community: "dreamTeamCreator",
    creativity: "storySparkAmbassador",
    governance: "trustGuardian",
    leadership: third === "analysis" ? "calmMentor" : "dreamTeamCreator"
  };
  return fallbackByTop[first] || "frontierExplorer";
}

function getRecommendedGroups(type, topDimensions) {
  const tags = [...type.tags, ...topDimensions.map(mapDimensionToTag)];
  return state.groups
    .map((group) => {
      const match = group.tags.filter((tag) => tags.includes(tag)).length;
      return { ...group, match };
    })
    .sort((a, b) => b.match - a.match)
    .slice(0, 4);
}

function getRecommendedNeighbors(type, topDimensions) {
  const tags = [...type.tags, ...topDimensions];
  return state.neighbors
    .map((neighbor) => {
      const score = (neighbor.tags || []).filter((tag) => tags.includes(tag)).length;
      return { ...neighbor, score };
    })
    .sort((a, b) => b.score - a.score)
    .slice(0, 5);
}

function mapDimensionToTag(dimension) {
  const map = {
    community: "community",
    build: "engineering",
    analysis: "data",
    creativity: "app",
    governance: "governance",
    leadership: "event"
  };
  return map[dimension];
}

function renderGroups(groups) {
  groupList.innerHTML = "";
  groups.forEach((group) => {
    const card = document.createElement("article");
    card.className = "group-card";
    const link = group.techplayUrl || group.url || "";

    // ロゴ: 画像URLがあれば<img>、なければ略称バッジ（onerrorで切り替え）
    const abbr = getGroupAbbr(group);
    const bgStyle = getGroupColorStyle(group.id);
    let logoHtml;
    if (group.logoUrl) {
      logoHtml = `<img class="group-logo-img" src="${group.logoUrl}" alt="${group.name}" loading="lazy"
        onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
        <div class="group-logo-abbr" style="${bgStyle}display:none">${abbr}</div>`;
    } else {
      logoHtml = `<div class="group-logo-abbr" style="${bgStyle}">${abbr}</div>`;
    }

    card.innerHTML = `
      <div class="group-logo-wrap">${logoHtml}</div>
      <div class="group-info">
        <strong class="group-name">${group.name}</strong>
        <p class="group-desc">${group.description || ""}</p>
        ${link ? `<a class="group-link" href="${link}" target="_blank" rel="noopener noreferrer">Tech Play で見る →</a>` : ""}
      </div>
    `;
    groupList.appendChild(card);
  });
}

function getGroupAbbr(group) {
  if (group.abbr) return group.abbr;
  const name = group.name || "";
  const uppers = name.match(/[A-Z]/g);
  if (uppers && uppers.length >= 2) return uppers.slice(0, 2).join("");
  const words = name.split(/[\s・\-\/]/);
  if (words.length >= 2) return (words[0][0] + words[1][0]).toUpperCase();
  return name.slice(0, 2).toUpperCase();
}

// グループIDをハッシュして一意のブランドカラーを返す
const GROUP_COLOR_PALETTE = [
  "#29B5E8", "#1a7fc1", "#0052cc", "#6B4FBB", "#00875A",
  "#C05621", "#0077B6", "#36B37E", "#403294", "#B91C1C"
];
function getGroupColorStyle(id) {
  let h = 0;
  for (const c of (id || "")) h = (h * 31 + c.charCodeAt(0)) >>> 0;
  const color = GROUP_COLOR_PALETTE[h % GROUP_COLOR_PALETTE.length];
  return `background:${color};`;
}

function renderNeighbors(neighbors) {
  neighborList.innerHTML = "";
  neighbors.forEach((neighbor) => {
    const card = document.createElement("article");
    card.className = "neighbor-card";
    const xLink = sanitizeUrl(neighbor.x_url);
    const liLink = sanitizeUrl(neighbor.linkedin_url);

    let avatarHtml;
    if (neighbor.photo_url) {
      avatarHtml = `<img class="neighbor-avatar" src="${neighbor.photo_url}" alt="${neighbor.name}" loading="lazy" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
        <div class="neighbor-avatar-placeholder" style="display:none">🧑</div>`;
    } else {
      avatarHtml = `<div class="neighbor-avatar-placeholder">🧑</div>`;
    }

    const links = [];
    if (xLink) links.push(`<a class="neighbor-link" href="${xLink}" target="_blank" rel="noopener noreferrer">𝕏</a>`);
    if (liLink) links.push(`<a class="neighbor-link" href="${liLink}" target="_blank" rel="noopener noreferrer">in</a>`);

    card.innerHTML = `
      ${avatarHtml}
      <div class="neighbor-name">${neighbor.name}</div>
      <div class="neighbor-affiliation">${neighbor.affiliation || "Snow Village"}</div>
      <div class="neighbor-links">${links.join("")}</div>
    `;
    neighborList.appendChild(card);
  });
}

function renderFeatures(features) {
  featureList.innerHTML = "";
  features.forEach((item) => {
    const li = document.createElement("li");
    // features.json形式（{name, description, url}）と旧来の文字列どちらにも対応
    if (typeof item === "object" && item.name) {
      li.innerHTML = item.url
        ? `<a href="${item.url}" target="_blank" rel="noopener noreferrer">${item.name}</a>`
        : item.name;
      if (item.description) {
        const desc = document.createElement("span");
        desc.className = "feature-desc";
        desc.textContent = ` — ${item.description}`;
        li.appendChild(desc);
      }
    } else {
      li.textContent = String(item);
    }
    featureList.appendChild(li);
  });
}

function renderEvents(events) {
  eventList.innerHTML = "";
  events.forEach((event) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <span class="event-date">${event.date}</span>
      <span>
        <a href="${event.url}" target="_blank" rel="noopener noreferrer">${event.title}</a>
        <span class="event-location"> — ${event.location}</span>
      </span>
    `;
    eventList.appendChild(li);
  });
}

function renderActions(actions) {
  actionList.innerHTML = "";
  actions.forEach((value) => {
    const li = document.createElement("li");
    li.textContent = value;
    actionList.appendChild(li);
  });
}

function getShareMessage() {
  const type = resultTitle.textContent || "Snow Villageタイプ";
  const firstGroup = groupList.querySelector("strong")?.textContent || "おすすめコミュニティ";
  return `私は「${type}」でした！ #snow_village_compass で診断して、${firstGroup} が気になっています。`;
}

function shareToX() {
  const text = encodeURIComponent(getShareMessage());
  const url = encodeURIComponent(window.location.href);
  window.open(`https://twitter.com/intent/tweet?text=${text}&url=${url}`, "_blank", "noopener");
}

function shareByMail() {
  const subject = encodeURIComponent("Snow Village Compass 診断結果");
  const body = encodeURIComponent(`${getShareMessage()}\n${window.location.href}`);
  window.location.href = `mailto:?subject=${subject}&body=${body}`;
}

function normalizeNeighbors(rawNeighbors) {
  if (!Array.isArray(rawNeighbors)) {
    return [];
  }
  return rawNeighbors
    .filter((entry) => entry && entry.name && entry.name !== "Neighbor")
    .map((entry) => {
      const affiliation = typeof entry.affiliation === "string" ? entry.affiliation.trim() : "";
      // photo パス (例: ../../images/neighbors/abe_kota.png) からファイル名を取り出してURL構築
      let photo_url = "";
      if (entry.photo && typeof entry.photo === "string") {
        const filename = entry.photo.split("/").pop();
        if (filename) photo_url = NEIGHBOR_PHOTO_BASE + filename;
      }
      return {
        name: entry.name,
        affiliation: affiliation && affiliation !== "--" && affiliation !== "ー" ? affiliation : "",
        photo_url,
        x_url: sanitizeUrl(entry.x_url || entry.xUrl),
        linkedin_url: sanitizeUrl(entry.linkedInUrl || entry.linkedinUrl),
        tags: inferNeighborTags(entry)
      };
    });
}

function inferNeighborTags(entry) {
  const source = `${entry.name || ""} ${entry.affiliation || ""}`.toLowerCase();
  const tags = [];
  if (source.includes("security")) tags.push("security", "governance");
  if (source.includes("data")) tags.push("data", "analysis");
  if (source.includes("studio")) tags.push("engineering", "build");
  if (source.includes("snowflake")) tags.push("community", "event");
  if (tags.length === 0) tags.push("community");
  return tags;
}

function sanitizeUrl(url) {
  if (!url || typeof url !== "string") {
    return "";
  }
  const trimmed = url.trim();
  if (!trimmed || trimmed === "--") {
    return "";
  }
  return trimmed;
}

function normalizeGroups(rawGroups) {
  if (!Array.isArray(rawGroups)) {
    return [];
  }
  return rawGroups
    .filter((entry) => entry && entry.name && (entry.url || entry.techplayUrl))
    .map((entry) => {
      const url = entry.techplayUrl || entry.url || "";
      const urlSegment = url.split("/").pop() || entry.name;
      return {
        id: entry.id || urlSegment,
        name: entry.name,
        abbr: entry.abbr || "",
        logoUrl: entry.logoUrl || "",
        description: (entry.description || "").trim(),
        techplayUrl: url,
        tags: entry.tags || inferGroupTags(entry)
      };
    });
}

function inferGroupTags(entry) {
  const name = (entry.name || "").toLowerCase();
  const desc = (entry.description || "").toLowerCase();
  const url = (entry.url || "").toLowerCase();
  const source = `${name} ${desc} ${url}`;
  const tags = new Set(["community"]);

  if (/金融|financial/.test(source)) tags.add("governance"), tags.add("security"), tags.add("analysis");
  if (/データマネジメント|data.management/.test(source)) tags.add("governance"), tags.add("data"), tags.add("quality");
  if (/rookies|初心者|beginner/.test(source)) tags.add("beginner-friendly"), tags.add("hands-on");
  if (/west|関西/.test(source)) tags.add("event"), tags.add("hands-on");
  if (/datascience|dataengineering|data.science|data.engineering/.test(source)) tags.add("analysis"), tags.add("engineering"), tags.add("data");
  if (/女子|women/.test(source)) tags.add("support"), tags.add("hands-on");
  if (/unconference/.test(source)) tags.add("event"), tags.add("leadership");
  if (/kyushu|九州/.test(source)) tags.add("event");
  if (/ai data|ai-data|ai_data/.test(source)) tags.add("challenge"), tags.add("data"), tags.add("app");
  if (/ヘルスケア|healthcare|ライフサイエンス/.test(source)) tags.add("governance"), tags.add("analysis"), tags.add("data");
  if (/salesforce|sf2ug/.test(source)) tags.add("engineering"), tags.add("app"), tags.add("build");
  if (/central|中部/.test(source)) tags.add("event"), tags.add("data");
  if (/サステナ|sustain/.test(source)) tags.add("story"), tags.add("governance"), tags.add("creativity");
  if (/okinawa|沖縄/.test(source)) tags.add("event"), tags.add("beginner-friendly");
  if (/data/.test(source)) tags.add("data");

  return [...tags];
}
