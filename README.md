# 成人小說 Prompt Generator PWA

手機優先、完全在瀏覽器本機運作的 Prompt Generator。

## GitHub Pages

網站網址：

https://lulu0723.github.io/-Prompt-Generator-PWA/

目前 `main` 分支根目錄就是正式 PWA webroot，包含：

- `index.html`
- `manifest.webmanifest`
- `service-worker.js`
- `icon-192.png`
- `icon-512.png`
- `apple-touch-icon.png`
- `.nojekyll`

`.github/workflows/deploy-pages.yml` 直接把 `main` 根目錄上傳為 GitHub Pages artifact 並部署，不再經過 `gh-pages` 重建、bundle 解包或執行期 patch。

## iPhone 使用

1. 用 Safari 開啟網站網址。
2. 點「分享」。
3. 選「加入主畫面」。
4. 之後可像 App 一樣從主畫面啟動。
5. 首次完整載入後，Service Worker 會快取 App Shell，之後可離線開啟。

## V1.0.3 手機詞庫 UI

- 人格建議詞改為常駐可點 chip，不再依賴 `<datalist>`。
- 關係類型也提供常駐 chip。
- 自由文字輸入仍保留。
- 人格 chip 仍透過既有 `vocabTrait()` 建立 trait，因此 `polarityTags` 與人格融合邏輯保持不變。
- Service Worker cache：`adult-prompt-generator-pwa-v1-0-3`。

## 隱私

- 不呼叫 LLM API。
- 不需要 backend 或 database。
- 角色庫使用瀏覽器 localStorage，只存在該網站來源的本機儲存空間。
- Prompt 產生與 Master Data 查詢全部在裝置端執行。

## Repository 結構

- `main/index.html`：正式線上版本，也是審查來源。
- `main/service-worker.js`：正式 Service Worker。
- `.github/workflows/deploy-pages.yml`：只負責驗證並直接部署上述 webroot。

因此之後審查不需要查看 build artifact 或 `gh-pages`；直接檢查 `main` 即可看到實際部署內容。

PWA V1.0.3。
