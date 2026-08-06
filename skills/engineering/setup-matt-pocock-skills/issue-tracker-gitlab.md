# Issue 追蹤器：GitLab

這個 repo 的 issue 與規格以 GitLab issue 的形式存在。所有操作使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI。

## 慣例

- **建立 issue**：`glab issue create --title "..." --description "..."`。多行 description 使用 heredoc。傳 `--description -` 開啟編輯器。
- **讀取 issue**：`glab issue view <number> --comments`。用 `-F json` 取得機器可讀的輸出。
- **列出 issue**：`glab issue list -F json`，搭配適當的 `--label` 過濾。
- **在 issue 上留言**：`glab issue note <number> --message "..."`。GitLab 稱留言為 "notes"。
- **套用 / 移除標籤**：`glab issue update <number> --label "..."` / `--unlabel "..."`。多個標籤可用逗號分隔或重複旗標。
- **關閉**：`glab issue close <number>`。`glab issue close` 不接受關閉留言，所以先用 `glab issue note <number> --message "..."` 發表說明，再關閉。
- **Merge request**：GitLab 稱 PR 為 "merge request"。用 `glab mr create`、`glab mr view`、`glab mr note` 等——形狀與 `gh pr ...` 相同，只是用 `mr` 代替 `pr`、用 `note`/`--message` 代替 `comment`/`--body`。

從 `git remote -v` 推斷 repo——`glab` 在 clone 內執行時會自動做到。

## Merge request 作為分診表面

**MR 作為請求表面：否。** _（如果這個 repo 把外部 merge request 當成功能請求，設為 `yes`；`/triage` 會讀這個旗標。）_

設為 `yes` 時，MR 與 issue 跑同一套標籤與狀態，使用 `glab mr` 的對應指令：

- **讀取 MR**：`glab mr view <number> --comments`，diff 用 `glab mr diff <number>`。
- **列出待分診的外部 MR**：`glab mr list -F json`，然後只保留作者不是專案成員/擁有者的 MR（貢獻者的 MR，不是維護者進行中的工作）。
- **留言 / 標籤 / 關閉**：`glab mr note`、`glab mr update --label`/`--unlabel`、`glab mr close`。

不像 GitHub，GitLab 分開編號 issue 與 MR，所以一旦你知道維護者指的是哪個表面，`#42` 就沒有歧義。

## 當技能說「publish to the issue tracker」

建立一個 GitLab issue。

## 當技能說「fetch the relevant ticket」

執行 `glab issue view <number> --comments`。

## 尋路操作

由 `/wayfinder` 使用。**地圖**是單一 issue，**子** issue 是 ticket。

- **地圖**：單一帶 `wayfinder:map` 標籤的 issue，容納 Notes / Decisions-so-far / Fog 的內容。`glab issue create --label wayfinder:map`。（在原生支援 epic 的 GitLab 層級，epic 可以容納地圖；有標籤的 issue 在任何地方都能用。）
- **子 ticket**：description 頂端帶 `Part of #<map>`、標籤為 `wayfinder:<type>`（`research`/`prototype`/`grilling`/`task`）的 issue。一旦被認領，ticket 指派給執行的開發者。
- **阻塞**：GitLab 的**原生阻塞連結**——標準、UI 可見的表示。用 `/blocked_by #<n>` 快速動作加入，以 note 發佈（`glab issue note <child> --message "/blocked_by #<blocker>"`）。原生阻塞連結是 Premium/Ultimate 功能；在免費層（或不可用時）回退到 description 頂端的 `Blocked by: #<n>, #<n>` 一行。當每個阻塞者都關閉時，ticket 就未阻塞。
- **前沿查詢**：`glab issue list -F json` 限定在地圖的子項，丟掉任何有開啟阻塞者的——指向開啟 issue 的原生 `blocked_by` 連結（`glab api projects/:id/issues/:iid/links`），或 `Blocked by` 行中的開啟 issue——或已有指派者的；地圖順序第一個勝出。
- **認領**：`glab issue update <n> --assignee @me`——這個 session 的第一次寫入。
- **解決**：`glab issue note <n> --message "<answer>"`，然後 `glab issue close <n>`，然後在地圖的 Decisions-so-far 附加一個上下文指標（gist + 連結）。
