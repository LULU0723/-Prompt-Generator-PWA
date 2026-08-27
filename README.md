# 成人小說 Prompt Generator PWA

手機優先、完全在瀏覽器本機運作的 Prompt Generator。

## GitHub Pages

預期網站網址：

https://lulu0723.github.io/-Prompt-Generator-PWA/

目前完整 PWA webroot 已發佈到 `gh-pages` 分支根目錄，包含：

- `index.html`
- `manifest.webmanifest`
- `service-worker.js`
- `icon-192.png`
- `icon-512.png`
- `apple-touch-icon.png`
- `.nojekyll`

若 GitHub Pages 尚未啟用，只需要在 GitHub 網頁做一次：

1. Repository → **Settings** → **Pages**
2. Build and deployment → Source 選 **Deploy from a branch**
3. Branch 選 **gh-pages**
4. Folder 選 **/ (root)**
5. Save

之後網址即為：

https://lulu0723.github.io/-Prompt-Generator-PWA/

## iPhone 使用

1. 用 Safari 開啟網站網址。
2. 點「分享」。
3. 選「加入主畫面」。
4. 之後可像 App 一樣從主畫面啟動。
5. 首次完整載入後，Service Worker 會快取 App Shell，之後可離線開啟。

## 隱私

- 不呼叫 LLM API。
- 不需要 backend 或 database。
- 角色庫使用瀏覽器 localStorage，只存在該網站來源的本機儲存空間。
- Prompt 產生與 Master Data 查詢全部在裝置端執行。

## Repository 結構

- `main`：部署來源與重建 workflow
- `gh-pages`：實際可由 GitHub Pages 提供的完整 PWA webroot

`.github/workflows/deploy-pages.yml` 會在 `main` 更新後重新建立 webroot 並更新 `gh-pages` 分支；GitHub Pages 的 Repository Settings 開關仍需由帳號端設定一次。

PWA V1.0.2。
