# できた！

子ども向けの朝・夜したくトラッカー。Vercelにデプロイ。
（アプリ名は「できた！」。ドメインは `ohayo-app.com`、Bundle ID は `app.ohayo.ohayo` のまま）

## 構成
- 単一ファイル (`index.html`) に HTML/CSS/JS をすべて埋め込み
- 外部依存なし（フレームワーク不使用）
- Vercel Analytics (`va()`) でイベント計測

## モード
- ☀️ あさ (asa) — 朝の支度カード
- 🌙 よる (neru) — 夜の支度カード

## データ永続化
- `localStorage` キー: `shitaku_custom_tasks`
- 設定画面からアイコン・ラベルをカスタマイズ可能

## デプロイ
- Vercel (main ブランチ push で自動デプロイ)
