# 成人小說 Prompt Generator PWA

手機優先、完全在瀏覽器本機運作的 Prompt Generator。

## GitHub Pages

部署完成後網址：

https://lulu0723.github.io/-Prompt-Generator-PWA/

### iPhone 使用

1. 用 Safari 開啟上方網址。
2. 點「分享」。
3. 選「加入主畫面」。
4. 之後可像 App 一樣從主畫面啟動。
5. 首次完整載入後，Service Worker 會快取 App Shell，之後可離線開啟。

## 隱私

- 不呼叫 LLM API。
- 不需要 backend 或 database。
- 角色庫使用瀏覽器 localStorage，只存在該網站來源的本機儲存空間。
- Prompt 產生與 Master Data 查詢全部在裝置端執行。

## 部署

`.github/workflows/deploy-pages.yml` 會在 `main` 更新後自動部署 GitHub Pages，並嘗試在尚未啟用時自動啟用 Pages。

## 主要檔案

- `index.html`
- `manifest.webmanifest`
- `service-worker.js`
- `icon-192.png`
- `icon-512.png`
- `apple-touch-icon.png`
- `.nojekyll`

PWA V1.0.2。
