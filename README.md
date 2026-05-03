# 食材選び方PWA - プロジェクト仕様

## プロジェクト概要

買い物中にスマホからサッと食材の選び方を確認できるPWA(Progressive Web App)。
最終的に約45品の食材データベースを目指すが、まずはサンプル3品(大根・人参・ねぎ)で骨格を構築する。

## ディレクトリ構造

```
food_pwa_sample/
├── data/
│   └── foods.json        # 食材マスターデータ
├── svg/
│   ├── daikon.svg        # 食材ごとのOK/NG比較図解
│   ├── carrot.svg
│   └── negi.svg
├── images/
│   ├── daikon.png        # SVGをPNG化したもの(参考用)
│   ├── carrot.png
│   └── negi.png
└── README.md             # このファイル
```

## データスキーマ(foods.json)

各食材は以下のフィールドを持つ:

| フィールド | 型 | 説明 |
|---|---|---|
| `id` | string | URL/key用の英語ID(例: "daikon") |
| `name` | string | 表示名(例: "大根") |
| `name_en` | string | 英語名(検索補助) |
| `category` | string | "vegetable" / "fruit" / "mushroom" / "fish" / "meat" / "egg_dairy_bean" / "game_meat" |
| `category_label` | string | 日本語カテゴリ名 |
| `subcategory` | string | 細分類(例: "根菜", "葉物・香味") |
| `color_theme` | string | 食材を表すメインカラー(HEX) |
| `accent_color` | string | アクセントカラー(HEX) |
| `season` | string[] | 旬の月(配列) |
| `season_peak` | string | 旬のピーク表現(例: "冬") |
| `ok_points` | string[] | OK判定のチェックポイント(4項目程度) |
| `ng_points` | string[] | NG判定のチェックポイント(4項目程度) |
| `storage` | object | `method`, `duration`, `tips`を含む保存方法 |
| `usage_tips` | string | 部位別の使い分け、調理のコツ |
| `nutrition_highlight` | string | 栄養面のハイライト |
| `svg_file` | string | 対応するSVGファイル名 |

## 図解SVGの仕様

- viewBox: `0 0 1080 600`
- 左側にOK例、右側にNG例(左右対比レイアウト)
- 中央に破線のディバイダー
- OK側は鮮やかな色・健康的な状態、NG側はくすんだ色・劣化した状態
- 下部にOK/NGそれぞれのチェックポイント表記(緑背景・赤背景)
- 円形バッジ(○/×)で視覚的に明示
- フォント: Noto Sans CJK JP

## PWAに実装してほしい機能

### MVP(最小限)

1. **ホーム画面**: 食材カードのグリッド表示(画像 + 名前 + カテゴリタグ)
2. **検索バー**: 食材名(日本語/英語/ひらがな)でフィルタリング
3. **カテゴリフィルター**: タブ切り替えで野菜/果物/魚/肉などを絞り込み
4. **詳細画面**: カードタップで図解SVG + 全データ表示
5. **オフライン動作**: Service Workerで全データをキャッシュ
6. **ホーム画面追加**: manifest.jsonでiOSにインストール可能に

### あると嬉しい機能(Phase 2)

7. **お気に入り機能**: よく見る食材をピン留め(IndexedDB)
8. **季節フィルター**: 「今が旬」を一発表示
9. **メモ機能**: 各食材に個人メモを追加(IndexedDB)
10. **食材追加機能**: ユーザーが独自の食材を追加できる
11. **ダークモード対応**

## 技術スタック推奨

- **フロントエンド**: 単一HTMLファイル + Vanilla JS(狩猟記録アプリと同じ構成)
  - もしくはVue 3 (CDN版) で軽量実装
- **データ管理**: foods.jsonをfetchで読み込み、IndexedDBでユーザーデータ保存
- **PWA**: manifest.json + Service Worker(Cache API)
- **デプロイ**: GitHub Pages(無料・HTTPS自動)

## 残り42品の追加方針

サンプル3品の構造に従って、以下の食材を順次追加:

### 野菜(残り14品)
トマト、きゅうり、じゃがいも、玉ねぎ、かぼちゃ、ニンニク、小松菜、キャベツ、レタス、白菜、なす、ピーマン、ブロッコリー、生姜

### 果物(11品)
バナナ、りんご、みかん、レモン、アボカド、いちご、キウイ、ぶどう、桃、柿、梨

### きのこ(5品)
椎茸、しめじ、エノキ、エリンギ、舞茸

### 魚介(5品)
鮭(切り身)、鯖、アジ、エビ、一尾魚の見方(汎用ガイド)

### 肉類(4品)
鶏肉、豚肉、牛肉、ひき肉

### 卵・乳・豆(4品)
卵、豆腐、納豆、ヨーグルト

### ジビエ(2品)
鹿肉、猪肉
※ヒロキさんの専門領域。狩猟記録アプリと連携した独自コンテンツ可能性あり

## Claude Codeへの依頼テンプレ

```
このプロジェクトのREADMEを読んで、サンプル3品(大根・人参・ねぎ)で
動作するPWAのMVPを作ってください。

要件:
- 単一HTMLファイル + Vanilla JS で実装
- foods.jsonを読み込んでカード表示
- 検索バーとカテゴリフィルター
- カードタップで詳細画面(SVG表示)
- Service Workerでオフライン対応
- iOS Safariで「ホーム画面に追加」可能

完成後、残り42品分のJSON雛形を生成して、私が埋められる形にしてください。
```

## デプロイ手順(参考)

1. GitHubリポジトリ作成
2. このフォルダ一式をプッシュ
3. Settings > Pages で main ブランチを公開
4. iPhoneのSafariで `https://username.github.io/repo-name/` にアクセス
5. 共有ボタン → 「ホーム画面に追加」

## 拡張アイデア(将来)

- 食材ごとのレシピリンク
- 旬カレンダー(月別ビュー)
- 買い物リスト機能
- 写真撮影 → AI判定(Claude API使用)
- 狩猟記録アプリとのデータ連携(ジビエ部位の鮮度判定)
