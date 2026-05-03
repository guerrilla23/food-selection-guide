# デプロイ & ローカル動作確認

## 1. ローカル動作確認

Service Worker は `file://` では動かないので、必ず HTTP サーバー経由で開く。

### 推奨: Python (macOS にプリインストール)

```bash
cd food_pwa_sample
python3 -m http.server 8000
```

→ ブラウザで `http://localhost:8000/` を開く。

### 代替: Node.js

```bash
cd food_pwa_sample
npx serve -l 8000
# または
npx http-server -p 8000 -c-1   # -c-1 はキャッシュ無効(開発用)
```

### iPhone 実機での確認(同一 Wi-Fi)

```bash
# Mac の IP を確認
ipconfig getifaddr en0
# 例: 192.168.1.10

# サーバー起動(0.0.0.0 で全インターフェース listen)
python3 -m http.server 8000 --bind 0.0.0.0
```

iPhone Safari で `http://192.168.1.10:8000/` にアクセス。

> ⚠️ Service Worker は HTTPS か `localhost` でしか動かない仕様。
> iPhone から HTTP の IP 直アクセスでは SW が登録されない(画面表示は OK)。
> オフライン動作の実機検証は GitHub Pages (HTTPS) にデプロイしてから。

---

## 2. GitHub Pages へのデプロイ

### 初回セットアップ

```bash
# food_pwa_sample/ をリポジトリのルートに置く前提
cd food_pwa_sample

# Git 初期化
git init
git add .
git commit -m "Initial PWA"

# GitHub にリポジトリ作成後
git branch -M main
git remote add origin https://github.com/<username>/<repo-name>.git
git push -u origin main
```

### Pages を有効化

1. GitHub リポジトリ → **Settings** → **Pages**
2. **Source**: `Deploy from a branch`
3. **Branch**: `main` / **Folder**: `/ (root)`
4. **Save**
5. 1〜2分待つ → `https://<username>.github.io/<repo-name>/` で公開

### iPhone でホーム画面に追加

1. iPhone Safari で公開 URL を開く
2. 共有ボタン(下部の □↑) → **「ホーム画面に追加」**
3. 名前を確認して **追加**
4. ホーム画面のアイコンから起動 → スタンドアロンアプリとして動く

---

## 3. データ更新後のキャッシュ反映

ファイルを更新したら `sw.js` の `CACHE_VERSION` を上げる:

```js
const CACHE_VERSION = 'v1';   // → 'v2' に変更してコミット
```

ユーザーがアプリを開くと、新しい SW がインストールされ古いキャッシュが破棄される。
HTML は network-first 戦略なのでオンライン時は常に最新版が取れる。

---

## 4. オフライン動作の確認手順

1. ブラウザで一度開く → SW がアセットをプリキャッシュ
2. DevTools → Application → Service Workers で登録を確認
3. DevTools → Network タブで「Offline」にチェック
4. リロード → カード一覧と詳細画面が表示されればOK

iPhone 実機なら機内モード ON で同様に確認できる。

---

## 5. ディレクトリ構造(納品物)

```
food_pwa_sample/
├── index.html               # 単一ファイルPWA本体
├── manifest.json            # iOSホーム画面追加用
├── sw.js                    # オフライン用Service Worker
├── DEPLOY.md                # このファイル
├── README.md                # プロジェクト仕様(既存)
├── data/
│   ├── foods.json           # サンプル3品データ
│   └── foods_template.json  # 残り45品の雛形
├── scripts/
│   └── extract_parts.py     # 詳細SVGからパーツSVGを切り出す
├── icons/                   # PWA + iOS用アイコン
├── images/                  # 旧PNG (参考用、現在は使用しない)
├── svg/
│   ├── daikon.svg           # 詳細SVG (パーツ抽出のソース)
│   ├── carrot.svg
│   ├── negi.svg
│   └── parts/               # ← アプリが実際に使用するパーツ
│       ├── daikon_ok.svg    # 食材本体イラストのみ
│       ├── daikon_ng.svg
│       ├── carrot_ok.svg
│       ├── carrot_ng.svg
│       ├── negi_ok.svg
│       └── negi_ng.svg
```

---

## 6. アイコンの再生成

`rsvg-convert` を使って `icons/icon-source.svg` から再生成できる:

```bash
brew install librsvg  # 未インストールなら

cd food_pwa_sample
rsvg-convert -w 192 -h 192 icons/icon-source.svg -o icons/icon-192.png
rsvg-convert -w 512 -h 512 icons/icon-source.svg -o icons/icon-512.png
rsvg-convert -w 180 -h 180 icons/icon-source.svg -o icons/apple-touch-icon.png
rsvg-convert -w 32  -h 32  icons/icon-source.svg -o icons/favicon-32.png
```

---

## 7. 新しい食材を追加する手順

詳細画面の図解は JS の `buildDiagram(food)` が自動生成するので、
新食材を追加するときは以下3つだけでOK:

### 手順
1. **`data/foods.json` の `items[]` に追記**
   `data/foods_template.json` から該当エントリをコピーして空欄を埋める。
   とくに `summary_ok` / `summary_ng` (5〜15文字の短キーワード) は図解に表示されるので必ず記入。

2. **パーツSVG 2ファイルを作成** (`svg/parts/<id>_ok.svg` と `<id>_ng.svg`)
   - viewBox は食材イラストが収まるサイズ (例: `-110 -250 220 440`)
   - 食材本体だけを描く。タイトル・キャプション・○/×バッジは入れない
   - 既存のパーツSVG (例: `svg/parts/daikon_ok.svg`) をテンプレートにすると速い
   - 既存形式の詳細SVGがあるなら `python3 scripts/extract_parts.py` で抽出可能
     (スクリプト先頭の `VIEWBOXES` に `<id>` エントリを追加してから実行)

3. **`sw.js` の `PRECACHE_URLS` にパーツSVGを追加** + `CACHE_VERSION` をbump
   ```js
   './svg/parts/<id>_ok.svg',
   './svg/parts/<id>_ng.svg',
   ```

これだけで一覧カード・詳細図解・OK/NG セクション・検索・カテゴリフィルター
すべて自動的に動作する。

### 図解レイアウトの仕組み
```
┌─────────────┐  ┌─────────────┐
│ ○ 良い大根   │  │ × 避けたい大根│   ← buildDiagramBlock(food, 'ok'/'ng')
├─────────────┤  ├─────────────┤
│  [parts/    │  │  [parts/    │
│   daikon_   │  │   daikon_   │
│   ok.svg]   │  │   ng.svg]   │
├─────────────┤  ├─────────────┤
│ summary_ok   │  │ summary_ng   │   ← 短キーワード
└─────────────┘  └─────────────┘
   (スマホ縦画面では縦積み)
```

## 8. 拡張ポイント(コード上の TODO)

- `index.html` の `Storage` モジュール: 現在 localStorage。Phase 2 で IndexedDB に差し替え可能
- `index.html` の `#fav-btn`: `hidden` 属性を外せばお気に入りボタン UI が出る
- `index.html` の `.feedback-fab`: `hidden` 属性を外せばフィードバック FAB が出る
- ダークモード: `prefers-color-scheme: dark` で自動切替済み。手動トグルは `:root.dark { ... }` を追加して `<html>` に class をつける形で実装可能
