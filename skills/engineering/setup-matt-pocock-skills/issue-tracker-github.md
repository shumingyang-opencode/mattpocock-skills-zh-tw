# Issue 追蹤器：GitHub

這個 repo 的 issue 與規格以 GitHub issue 的形式存在。所有操作使用 `gh` CLI。

## 慣例

- **建立 issue**：`gh issue create --title "..." --body "..."`。多行 body 使用 heredoc。
- **讀取 issue**：`gh issue view <number> --comments`，用 `jq` 過濾留言並同時擷取標籤。
- **列出 issue**：`gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`，搭配適當的 `--label` 與 `--state` 過濾。
- **在 issue 上留言**：`gh issue comment <number> --body "..."`
- **套用 / 移除標籤**：`gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **關閉**：`gh issue close <number> --comment "..."`

從 `git remote -v` 推斷 repo——`gh` 在 clone 內執行時會自動做到。

## Pull request 作為分診表面

**PR 作為請求表面：否。** _（如果這個 repo 把外部 PR 當成功能請求，設為 `yes`；`/triage` 會讀這個旗標。）_

設為 `yes` 時，PR 與 issue 跑同一套標籤與狀態，使用 `gh pr` 的對應指令：

- **讀取 PR**：`gh pr view <number> --comments`，diff 用 `gh pr diff <number>`。
- **列出待分診的外部 PR**：`gh pr list --state open --json number,title,body,labels,author,authorAssociation,comments`，然後只保留 `authorAssociation` 為 `CONTRIBUTOR`、`FIRST_TIME_CONTRIBUTOR` 或 `NONE` 的（丟掉 `OWNER`/`MEMBER`/`COLLABORATOR`）。
- **留言 / 標籤 / 關閉**：`gh pr comment`、`gh pr edit --add-label`/`--remove-label`、`gh pr close`。

GitHub 在 issue 與 PR 之間共享單一編號空間，所以裸的 `#42` 可能是任一者——用 `gh pr view 42` 解析，回退到 `gh issue view 42`。

## 當技能說「publish to the issue tracker」

建立一個 GitHub issue。

## 當技能說「fetch the relevant ticket」

執行 `gh issue view <number> --comments`。

## 尋路操作

由 `/wayfinder` 使用。**地圖**是單一 issue，**子** issue 是 ticket。

- **地圖**：單一帶 `wayfinder:map` 標籤的 issue，容納 Notes / Decisions-so-far / Fog 的內容。`gh issue create --label wayfinder:map`。
- **子 ticket**：以 GitHub 子 issue（sub-issues 端點上的 `gh api`）連到地圖的 issue。在未啟用子 issue 時，把子項加進地圖內容的任務清單，並在子項內容頂端放 `Part of #<map>`。標籤：`wayfinder:<type>`（`research`/`prototype`/`grilling`/`task`）。一旦被認領，ticket 指派給執行的開發者。
- **阻塞**：GitHub 的**原生 issue 相依**——標準、UI 可見的表示。用 `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>` 加入邊，其中 `<blocker-db-id>` 是阻塞者的數字**資料庫 id**（`gh api repos/<owner>/<repo>/issues/<n> --jq .id`，_不是_ `#number` 或 `node_id`）。GitHub 回報 `issue_dependencies_summary.blocked_by`（只有開啟的阻塞者——即時的門）。在相依不可用時，回退到子項內容頂端的 `Blocked by: #<n>, #<n>` 一行。當每個阻塞者都關閉時，ticket 就未阻塞。
- **前沿查詢**：列出地圖的開啟子項（`gh issue list --state open`，限定在地圖的子 issue / 任務清單），丟掉任何有開啟阻塞者（`issue_dependencies_summary.blocked_by > 0`，或 `Blocked by` 行中有開啟的 issue）或已有指派者的；地圖順序第一個勝出。
- **認領**：`gh issue edit <n> --add-assignee @me`——這個 session 的第一次寫入。
- **解決**：`gh issue comment <n> --body "<answer>"`，然後 `gh issue close <n>`，然後在地圖的 Decisions-so-far 附加一個上下文指標（gist + 連結）。
