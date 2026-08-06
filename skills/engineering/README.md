# 工程技能

我每天做程式工作時使用的技能。

## 使用者叫用

只有當你輸入它們時才可觸達（Claude Code：`disable-model-invocation: true`；Codex：在 `agents/openai.yaml` 中 `policy.allow_implicit_invocation: false`）。

- **[ask-matt](./ask-matt/SKILL.md)** — 詢問哪個技能或流程最符合你的情況。這個 repo 中使用者叫用技能的路由器。
- **[grill-with-docs](./grill-with-docs/SKILL.md)** — 同時建立專案領域模型的 grilling session，磨利術語並就地更新 `CONTEXT.md` 與 ADRs。
- **[triage](./triage/SKILL.md)** — 讓 issues 穿過分診角色的狀態機。
- **[improve-codebase-architecture](./improve-codebase-architecture/SKILL.md)** — 掃描程式碼庫找出深化機會，以視覺化 HTML 報告呈現，然後對你挑選的任何一個進行 grill。
- **[setup-matt-pocock-skills](./setup-matt-pocock-skills/SKILL.md)** — 為工程技能設定這個 repo（issue tracker、分診標籤、領域文件布局）。每個 repo 執行一次。
- **[to-spec](./to-spec/SKILL.md)** — 把目前的對話轉成規格說明並發佈到 Issue 追蹤器。
- **[to-tickets](./to-tickets/SKILL.md)** — 把任何計畫、規格說明或對話拆成一組曳光彈 tickets，每個都宣告自己的阻塞邊——在本機檔案中寫成文字，或在真正的追蹤器上用原生阻塞連結。
- **[implement](./implement/SKILL.md)** — 建置規格說明或一組 tickets 所描述的工作，在事先約定的接縫上驅動 `/tdd`，並在 commit 前以 `/code-review` 收尾。
- **[wayfinder](./wayfinder/SKILL.md)** — 規劃一大塊工作——大得單一代理 session 裝不下——作為 Issue 追蹤器上決策 tickets 的共享地圖，逐一解決，直到通往目的地的路徑清晰為止。

## 模型叫用

可由模型或使用者觸達（使用豐富的觸發措辭，讓模型可以伸手取用它們）。

- **[prototype](./prototype/SKILL.md)** — 建立一次性原型回答設計問題：一個可分享的單一 HTML 檔案處理狀態／邏輯，或幾種可切換的 UI 變體。

- **[diagnosing-bugs](./diagnosing-bugs/SKILL.md)** — 針對棘手 bug 與效能回歸的有紀律診斷迴圈：建立對這個 bug 顯示紅色的回饋迴圈 → 最小化 → 假設 → 插樁 → 修復 → 回歸測試。
- **[research](./research/SKILL.md)** — 針對高可信度的主要來源調查一個問題，並把發現作為一份有引用的 Markdown 檔案留在 repo 中，以背景代理執行。
- **[tdd](./tdd/SKILL.md)** — 帶有紅-綠-重構迴圈的測試驅動開發。一次一個垂直切片建置功能或修復 bug。
- **[domain-modeling](./domain-modeling/SKILL.md)** — 主動建立並磨利專案的領域模型——質疑術語、以情境壓力測試、就地更新 `CONTEXT.md` 與 ADRs。
- **[codebase-design](./codebase-design/SKILL.md)** — 設計深模組的共享紀律與詞彙：小介面、乾淨接縫、可透過介面測試。
- **[code-review](./code-review/SKILL.md)** — 針對自固定基點以來的 diff 做雙軸審查：**規範**（是否符合 repo 的程式碼規範，加上 Fowler 壞味道基線？）與**規格**（是否忠實實作源頭的 issue／spec？），以平行子代理執行。
- **[resolving-merge-conflicts](./resolving-merge-conflicts/SKILL.md)** — 逐塊處理進行中的 git merge 或 rebase 衝突，依追溯到每一方主要來源的意圖解決，然後完成操作——絕不 `--abort`。
- **[wizard](./wizard/SKILL.md)** — 產生一個互動式 bash wizard，引導人類走過只有他們能做的步驟：佈建基礎設施、設定憑證或 CI secrets、走訪陌生的第三方儀表板，或執行一次性遷移或切換。
