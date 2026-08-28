# 成人小說 Prompt Generator PWA

手機優先、完全在瀏覽器本機運作的 Prompt Generator／成人元素探索工具。

## GitHub Pages

網站網址：

https://lulu0723.github.io/-Prompt-Generator-PWA/

目前 `main` 分支根目錄就是正式 PWA webroot；`.github/workflows/deploy-pages.yml` 會驗證並直接部署 `main`，正式 source 與實際部署內容一致。

## V1.2.1 Quick Prompt

V1.2.1 在 V1.2 Composer 上新增兩條輸出路徑：

- **完整模式**：使用角色、關係、場景、成人元素、節奏與自由補充，產生完整小說 Prompt。
- **玩法速貼模式**：不要求角色資料，只要選核心成人元素、其他元素或填自由補充，就能產生一段可直接貼給 LLM 的玩法 Prompt。

切換模式只改 UI 與 validation，不會清除已填資料。從玩法速貼切回完整模式時，原本的角色、關係與場景仍保留。

完整模式另外提供「只複製玩法 Prompt」，可在不改動完整 Prompt 預覽的情況下，直接把目前選到的成人元素與節奏複製出去。

### Quick Prompt 輸出

玩法速貼會依已填內容省略空區塊，可包含：

- 內容方向
- 核心成人元素與功能 modifier
- 其他想加入的元素
- 節奏
- 自由補充

舊辭典玩法在 Quick Prompt 中只輸出玩法名稱，不輸出 A/B assignment；人物、關係與場景交由 LLM 依故事需要合理補完。

### 核心元素組合器

V1.2 起採「核心元素 + 功能 modifier」而非大量平鋪複合 tag。例如：

- 觸手：插入、注入、吸附／吸吮、胸部吸附、乳首吸附、束縛功能、脈動、膨脹／變粗、分泌液、自主活動、依反應調整、多條／多點。
- 束縛：輕度限制、中度限制、高度限制、完全無法動彈、姿勢固定、動態限制、逐步收緊、逐步解除。
- 炮機：自動往復、固定節奏、漸進增強、隨機節奏、反覆停止／開始、由另一角色控制、自動程序、無法自行停止、長時間運作。
- 其他核心包含八爪椅、機械臂、跳蛋／小型震動器、吸吮器／氣壓刺激器、Strap-on、插入式玩具、遙控玩具、史萊姆／液態體與魔法拘束。

V1.1 的既有玩法辭典仍保留在「其他元素辭典」中，作為補充搜尋來源。

## 技術與隱私

- 不呼叫 LLM API。
- 不需要 backend 或 database。
- 角色庫使用瀏覽器 localStorage。
- Prompt 產生與資料查詢全部在裝置端執行。
- 人格建議詞使用手機可點 chip，不使用 `<datalist>`。
- GitHub Actions 會對正式 `index.html` 的 inline JavaScript 與 `service-worker.js` 執行 `node --check`。
- Service Worker cache：`adult-prompt-generator-pwa-v1-2-1`。

## iPhone 使用

1. 用 Safari 開啟網站網址。
2. 點「分享」。
3. 選「加入主畫面」。
4. 之後可像 App 一樣從主畫面啟動。
5. 首次完整載入後，Service Worker 會快取 App Shell，之後可離線開啟。

## Repository 結構

- `main/index.html`：正式線上版本，也是審查來源。
- `main/service-worker.js`：正式 Service Worker。
- `.github/workflows/deploy-pages.yml`：驗證並直接部署上述 webroot。

PWA V1.2.1 Quick Prompt。
