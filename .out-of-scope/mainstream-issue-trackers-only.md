# Issue tracker 整合僅限於主流工具

`setup-matt-pocock-skills` 只對**主流** issue tracker 提供第一等支援。為小眾、新興或單一廠商的實驗性 tracker 新增支援的要求，均屬超出範圍。

## 為什麼這超出範圍

每個 issue-tracker 後端都把 CLI 形態硬編碼進技能（指令、旗標、輸出解析）。每個新後端都是永久性的維護面 — 它必須隨著工具的 CLI 演進而持續可用，也必須持續被 `/to-spec`、`/to-tickets`、`/triage` 及其同儕測試。這成本只值得為實際上有相當比例使用者持有的 tracker 付出。

「主流」是判斷，不是數字門檻：

- GitHub、GitLab 與 Backlog.md 是我們視為主流的工具 — 廣為人知、被廣泛使用、早已脫離實驗階段。
- 一個只有幾百顆 GitHub star 的全新、以代理為焦點的工具不算主流，無論設計多有趣。

star 數、年齡與下載量是有用的訊號，但沒有哪一個是規則。規則是一般的工程師是否認得這個工具、並合理地為團隊選用它。

非主流 tracker 的逃生門已經存在：

- 輕量的 repo 內追蹤用 `local markdown`。
- 想自己接線的人用 `other/custom`。

兩者都不需要核心技能知道特定工具。

## 先前的請求

- #99 —「把 dex 加入為 issue tracker 後端」（dex 在請求當下約 3 個月大、約 300 顆 star）
