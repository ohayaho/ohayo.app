# できタップ

子ども向けの朝・夜したくトラッカー（iOSアプリ）。
（アプリ名は「できタップ」。v1.2.1で「できた！」から改名。ドメインは `ohayo-app.com`、Bundle ID は `app.ohayo.ohayo` のまま）

## 構成
- **アプリ本体**: `webapp/index.html`（単一ファイルに HTML/CSS/JS をすべて埋め込み、外部依存なし）。iOSの WKWebView にバンドルされる（`ios/` の Xcode プロジェクトが参照）
- **Web公開分**: ルートの `index.html`（ランディングページ）＋ `privacy.html` / `support.html` / `terms.html` のみ。`.vercelignore` はホワイトリスト方式で、アプリ本体（`webapp/`）は**Webには公開しない**
- ランディング・公開ページに **Vercel Analytics は入れない**（プライバシーポリシーの「解析なし」記述と整合させるため）

## モード
- ☀️ あさ (asa) — 朝の支度カード
- 🌙 よる (neru) — 夜の支度カード（プレミアム限定）

## マネタイズ（v1.2〜）
- 買い切り（非消費型）IAP `app.ohayo.ohayo.premium`。プレミアム判定は**ネイティブ（StoreKit）が正**で、JSは `window.OhayoStore` 経由で状態を受け取るだけ
- 無料版：あさモード＋カード裏画像の初回1回変更のみ

## データ永続化
- `localStorage` キー: `shitaku_custom_tasks` / `shitaku_reward_image` / `shitaku_clear_image`（画像は `{asa, neru}` のモード別）
- 端末内のみ保存・外部送信なし

## デプロイ
- Vercel (main ブランチ push で自動デプロイ)
