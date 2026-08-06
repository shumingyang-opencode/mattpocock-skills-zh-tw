# Issue 追蹤器：本機 Markdown

這個 repo 的 issue 與規格以 `.scratch/` 中的 markdown 檔案形式存在。

## 慣例

- 每個功能一個目錄：`.scratch/<feature-slug>/`
- 規格是 `.scratch/<feature-slug>/spec.md`
- 實作 issue 每個 ticket 一個檔案，位於 `.scratch/<feature-slug>/issues/<NN>-<slug>.md`，從 `01` 開始編號——絕不共用單一合併的 tickets 檔案
- 分診狀態以 `Status:` 一行記錄在每個 issue 檔案的頂端附近（角色字串見 `triage-labels.md`）
- 留言與對話歷史在 `## Comments` 標題下附加到檔案底部

## 當技能說「publish to the issue tracker」

在 `.scratch/<feature-slug>/` 下建立新檔案（需要的話建立目錄）。

## 當技能說「fetch the relevant ticket」

讀取所引用路徑的檔案。使用者通常會直接傳路徑或 issue 編號。

## 尋路操作

由 `/wayfinder` 使用。**地圖**是一個檔案，每個 ticket 一個**子**檔案。

- **地圖**：`.scratch/<effort>/map.md`——Notes / Decisions-so-far / Fog 的內容。
- **子 ticket**：`.scratch/<effort>/issues/NN-<slug>.md`，從 `01` 開始編號，問題在內容中。`Type:` 一行記錄 ticket 型別（`research`/`prototype`/`grilling`/`task`）；`Status:` 一行記錄 `claimed`/`resolved`。
- **阻塞**：頂端附近的 `Blocked by: NN, NN` 一行。當它列出的每個檔案都 `resolved` 時，ticket 就未阻塞。
- **前沿**：掃描 `.scratch/<effort>/issues/` 找開啟、未阻塞且未被認領的檔案；編號最小的第一個勝出。
- **認領**：任何工作前設定 `Status: claimed` 並儲存。
- **解決**：在 `## Answer` 標題下附加答案，設定 `Status: resolved`，然後在 `map.md` 的地圖 Decisions-so-far 附加一個上下文指標（gist + 連結）。
