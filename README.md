# 成人小說 Prompt Generator PWA

手機優先、完全在瀏覽器本機運作的 Prompt Generator／成人元素探索工具。

## GitHub Pages

網站網址：

https://lulu0723.github.io/-Prompt-Generator-PWA/

目前 `main` 分支根目錄就是正式 PWA webroot；`.github/workflows/deploy-pages.yml` 只負責驗證並直接部署 `main`，正式 source 與實際部署內容一致。

## V1.2 Composer

這一版把「大量平鋪玩法 tag」往「核心元素 + 功能 modifier」重構。

### 核心元素組合器

先選具體核心元素，再選真正會改變互動機制的功能。例如：

- 觸手：插入、注入、吸附／吸吮、胸部吸附、乳首吸附、束縛功能、脈動、膨脹／變粗、分泌液、自主活動、依反應調整、多條／多點。
- 束縛：輕度限制、中度限制、高度限制、完全無法動彈、姿勢固定、動態限制、逐步收緊、逐步解除。
- 炮機：自動往復、固定節奏、漸進增強、隨機節奏、反覆停止／開始、由另一角色控制、自動程序、無法自行停止、長時間運作。
- 八爪椅：多點同步、束縛功能、姿勢固定、震動、插入、吸附、操控其他玩具、遠端控制、自動程序、依反應調整。
- 其他核心：機械臂、跳蛋／小型震動器、吸吮器／氣壓刺激器、Strap-on、插入式玩具、遙控玩具、史萊姆／液態體、魔法拘束。

這種結構刻意避免把「綁手腕／綁腳踝」之類肢體位置拆成大量近義 tag；若差異不會實質改變模型的互動機制，就不額外建立獨立元素。

Compiler 會輸出：

- `核心成人元素與功能：`
- `觸手：注入、脈動、自主活動`
- `束縛：高度限制`

沒有選 modifier 時，只輸出核心元素名稱，細節交由模型自然處理。

### 既有辭典

V1.1 的既有成人玩法辭典暫時完整保留在「其他元素辭典」中，作為補充搜尋來源；後續再依實際使用情況逐步合併、刪除重複或低價值標籤。

### 其他

- 人格建議詞仍使用手機可點 chip，不使用 `<datalist>`。
- 人格 `polarityTags` 與既有 deterministic Compiler 邏輯保留。
- Service Worker cache：`adult-prompt-generator-pwa-v1-2-0`。

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
- Prompt 產生與資料查詢全部在裝置端執行。

## Repository 結構

- `main/index.html`：正式線上版本，也是審查來源。
- `main/service-worker.js`：正式 Service Worker。
- `.github/workflows/deploy-pages.yml`：驗證並直接部署上述 webroot。

PWA V1.2.0 Composer。
