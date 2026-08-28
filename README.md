# 成人小說 Prompt Generator PWA

手機優先、完全在瀏覽器本機運作的 Prompt Generator／成人玩法探索辭典。

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

`.github/workflows/deploy-pages.yml` 直接把 `main` 根目錄上傳為 GitHub Pages artifact 並部署；正式 source 與實際部署內容一致。

## V1.1 Dictionary

這一版把產品定位從「角色設定表」往「成人玩法辭典 + Prompt 編譯器」移動：

- 原有玩法全部保留，玩法辭典擴充至 140+ 條。
- 新增「親密接觸、高潮與節制、衣著／暴露、角色扮演／情境」等分類。
- 每張玩法卡保留一句話定義，並可展開「名詞解釋／相關資訊」。
- 辭典 metadata 可包含英文名、別名、搜尋關鍵詞、常見互動感受與容易混淆的概念。
- 搜尋會同時比對名稱、說明、英文、別名、關鍵詞、感受與分類。
- 辭典資訊只服務 UI；Compiler 仍只把玩法名稱與方向送入 Prompt，不把百科說明塞進正文要求。
- 角色的一般性格與親密互動特徵改為預設收合；只填基本人物資訊也可以正常使用，細節可交由 LLM 合理補完。
- 人格 chip／`polarityTags`／原有 deterministic Compiler 邏輯不變。
- Service Worker cache：`adult-prompt-generator-pwa-v1-1-0`。

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

- `main/index.html`：正式線上版本，也是審查來源。
- `main/service-worker.js`：正式 Service Worker。
- `.github/workflows/deploy-pages.yml`：只負責驗證並直接部署上述 webroot。

之後審查直接檢查 `main` 即可看到實際部署內容，不需要找 build artifact 或 `gh-pages`。

PWA V1.1.0 Dictionary。
