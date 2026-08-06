# HTML 報告格式

架構審查渲染成作業系統暫存目錄中單一自足的 HTML 檔案。Tailwind 與 Mermaid 都來自 CDN。Mermaid 可靠地處理圖形狀的圖表；手工打造的 div 與內嵌 SVG 處理更具編輯性的視覺（質量圖、剖面）。混用兩者——不要全部依賴 Mermaid，那會開始看起來千篇一律。

## 骨架

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review — {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      /* small custom layer for things Tailwind doesn't cover cleanly:
         dashed seam lines, hand-drawn-feeling arrow heads, etc. */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## 頁首

Repo 名稱、日期，與一個精簡圖例：實心方塊 = 模組、虛線 = 接縫、紅箭頭 = 洩漏、粗黑方塊 = 深模組。沒有引言段落——直接進候選。

## 候選卡片

圖表承重。散文稀疏、平實，並直接使用（`/codebase-design` 技能的）詞彙表術語，不加儀式。

每個候選是一個 `<article>`：

- **標題**——簡短，點出深化（例如「把 Order intake 管線收攏」）。
- **徽章列**——建議強度（`Strong` = emerald、`Worth exploring` = amber、`Speculative` = slate），加上相依分類的標籤（`in-process`、`local-substitutable`、`ports & adapters`、`mock`）。
- **檔案**——等寬字型清單，`font-mono text-sm`。
- **前 / 後圖**——主角。兩欄並排。見下面的模式。
- **問題**——一句話。什麼在痛。
- **解決方案**——一句話。什麼改變。
- **戰果**——條列，每條 ≤6 字。例如「Tests hit one interface」「Pricing logic stops leaking」「Delete 4 shallow wrappers」。
- **ADR callout**（如適用）——amber 色調方框中的一行。

沒有解釋段落。如果圖表需要段落才能被理解，重畫圖表。

## 圖表模式

挑符合候選的模式。混用。不要讓每張圖都長得一樣——變化本身就是重點的一部分。

### Mermaid 圖表（相依 / 呼叫流程的主力）

當重點是「X 呼叫 Y 呼叫 Z，看看這團亂」時，用 Mermaid `flowchart` 或 `graph`。用 Tailwind 樣式的卡片包住它，讓它不像是被硬塞進來的。用 classDef 把洩漏邊染色成紅色、深模組染成深色。序列圖很適合「之前：6 次來回；之後：1 次」。

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leak.-> D[PricingClient]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

### 手工打造的方塊與箭頭（當 Mermaid 的佈局跟你作對時）

模組用帶邊框與標籤的 `<div>`。箭頭用內嵌 SVG `<line>` 或 `<path>` 元素，絕對定位在 relative 容器上。當你想要「之後」圖感覺像一個粗邊框深模組、內部灰掉時用它——Mermaid 渲染不出那個重量。

### 剖面（適合分層淺度）

堆疊水平色帶（`h-12 border-l-4`）顯示一次呼叫穿過的層。之前：6 層薄層各自什麼都不做。之後：1 條粗色帶，標著合併後的責任。

### 質量圖（適合「介面跟實作一樣寬」）

每個模組兩個矩形——一個介面表面積、一個實作。之前：介面矩形幾乎跟實作矩形一樣高（淺）。之後：介面矩形矮、實作矩形高（深）。

### 呼叫圖收攏

之前：以巢狀方塊渲染的函式呼叫樹。之後：同一棵樹收攏進一個方塊，現在是內部的呼叫在裡面淡顯。

## 樣式指引

- 編輯風，不是公司儀表板風。充裕留白。標題可選襯線字體（`font-serif` 與 stone/slate 搭配很好）。
- 節制用色：一個主色（emerald 或 indigo）加紅色給洩漏、amber 給警告。
- 保持圖表約 320px 高，讓前/後舒服地並排而不捲動。
- 圖表內模組標籤用 `text-xs uppercase tracking-wider`——它們要讀起來像示意圖，不是 UI。
- 唯一的腳本是 Tailwind CDN 與 Mermaid ESM import。報告其餘部分靜態——沒有應用程式碼、沒有超越 Mermaid 自身渲染的互動。

## 頂級建議章節

一張較大的卡片。候選名稱、一句話說明為什麼、連到它卡片的錨點連結。就這樣。

## 語氣

平實英文、精簡——但架構名詞與動詞直接來自 `/codebase-design` 技能。精簡不是漂移的藉口。

**確切使用：** module、interface、implementation、depth、deep、shallow、seam、adapter、leverage、locality。

**絕不替換：** component、service、unit（指 module）· API、signature（指 interface）· boundary（指 seam）· layer、wrapper（指 module，當你意指 module 時）。

**符合這個風格的措辭：**

- "Order intake module is shallow — interface nearly matches the implementation."
- "Pricing leaks across the seam."
- "Deepen: one interface, one place to test."
- "Two adapters justify the seam: HTTP in prod, in-memory in tests."

**戰果條列**以詞彙表術語指名收益：*"locality: bugs concentrate in one module"*、*"leverage: one interface, N call sites"*、*"interface shrinks; implementation absorbs the wrappers"*。不要寫 *"easier to maintain"* 或 *"cleaner code"*——那些術語不在詞彙表裡，不配佔位置。

不模糊、不開場白、沒有「值得注意的是……」如果一句話能變成條列，就變成條列。如果一條能刪，就刪。如果某個術語不在 `/codebase-design` 詞彙表裡，在發明新詞之前先去找一個在的。
