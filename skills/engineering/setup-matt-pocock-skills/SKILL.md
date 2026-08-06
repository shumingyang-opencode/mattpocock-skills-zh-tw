---
name: setup-matt-pocock-skills
description: 為工程技能設定這個 repo——設定它的 issue 追蹤器、分診標籤詞彙與領域文件佈局。首次使用其他工程技能前執行一次。
disable-model-invocation: true
---

# 設定 Matt Pocock 的技能

為工程技能假設的每個 repo 設定建立骨架：

- **Issue 追蹤器**——issue 放在哪裡（預設 GitHub；本機 markdown 也開箱即支援）
- **分診標籤**——五個標準分診角色使用的字串
- **領域文件**——`CONTEXT.md` 與 ADR 放在哪裡，以及讀取它們的消費規則

這是一個提示驅動的技能，不是確定性腳本。探索、呈現你所發現的、與使用者確認，然後寫入。

## 流程

### 1. 探索

檢視目前 repo，理解它的起點狀態。讀任何存在的東西；不要臆測：

- `git remote -v` 與 `.git/config`——這是 GitHub repo 嗎？哪一個？
- repo 根目錄的 `AGENTS.md` 與 `CLAUDE.md`——兩者存在嗎？其中一個是否已經有 `## Agent skills` 章節？
- repo 根目錄的 `CONTEXT.md` 與 `CONTEXT-MAP.md`
- `docs/adr/` 與任何 `src/*/docs/adr/` 目錄
- `docs/agents/`——這個技能先前的輸出是否已經存在？
- `.scratch/`——顯示本機 markdown issue 追蹤器慣例已在使用的跡象
- `triage` 技能有安裝嗎？（旁邊的 `triage` 技能資料夾，或在你可用的技能中。）這決定 B 章節要不要跑。
- Monorepo 訊號——`pnpm-workspace.yaml`、`package.json` 中的 `workspaces` 欄位，或有自己 `src/` 的 `packages/*`。只有在真正的大型多套件 repo 中才呈現；它們不存在代表單一上下文，而幾乎每個 repo 都是。

### 2. 呈現發現並詢問

總結有哪些、缺哪些。然後依序處理各章節——一個章節、一個答案，然後下一章節。

每個章節都以建議答案領頭，讓使用者一個字就能接受。只有當選擇真的分歧時才給一行說明；探索已經定案時直接跳過該章節（`triage` 未安裝時跳過 B 章節、沒有 monorepo 時跳過 C 章節）。

**A 章節——Issue 追蹤器。**

> 說明：「issue 追蹤器」是這個 repo 的 issue 所在之處。`to-tickets`、`triage` 與 `to-spec` 等技能會讀寫它——它們需要知道該呼叫 `gh issue create`、在 `.scratch/` 下寫 markdown 檔案，還是遵循你描述的其他工作流程。選一個你實際用來追蹤這個 repo 工作的場所。

預設姿態：這些技能是為 GitHub 設計的。如果 `git remote` 指向 GitHub，提出 GitHub。如果 `git remote` 指向 GitLab（`gitlab.com` 或自架的 host），提出 GitLab。否則（或使用者偏好時），提供：

- **GitHub**——issue 存在 repo 的 GitHub Issues（使用 `gh` CLI）
- **GitLab**——issue 存在 repo 的 GitLab Issues（使用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI）
- **本機 markdown**——issue 以 `.scratch/<feature>/` 下的檔案形式存在於此 repo（適合個人專案或沒有 remote 的 repo）
- **其他**（Jira、Linear 等）——請使用者用一段話描述工作流程；技能會把它記錄為自由格式散文

把選擇記錄在 `docs/agents/issue-tracker.md`。GitHub 與 GitLab 模板帶有「PRs as a request surface」旗標，預設**關閉**——保持關閉且不要提起它；想要外部 PR 進分診佇列的使用者可以之後在檔案中開啟該旗標。

**B 章節——分診標籤詞彙。** 如果 `triage` 技能未安裝（探索已告訴你），整節跳過——未安裝的技能不需要標籤。

如果有安裝，只問一個問題：

> 你想保留預設的分診標籤嗎？（建議：**是**）

預設就是五個標準角色，每個標籤字串等於它的名稱：`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human`、`wontfix`。答**是**就原樣寫入。只有當使用者說不——通常是因為他們的追蹤器已使用其他名稱（例如用 `bug:triage` 代替 `needs-triage`）——才收集覆寫，讓 `triage` 套用既有標籤而不是建立重複的。

**C 章節——領域文件。** 預設**單一上下文**——repo 根目錄一份 `CONTEXT.md` + `docs/adr/`。這適合幾乎每個 repo；不用問就寫。

只有當探索發現 monorepo 訊號時，才提供**多上下文**——根目錄的 `CONTEXT-MAP.md` 指向每個上下文的 `CONTEXT.md` 檔案。然後確認他們想要哪種佈局。

### 3. 確認與編輯

給使用者看草稿：

- 要加入 `CLAUDE.md` / `AGENTS.md` 其中一個（見第 4 步的選擇規則）的 `## Agent skills` 區塊
- `docs/agents/issue-tracker.md`、`docs/agents/domain.md` 與 `docs/agents/triage-labels.md` 的內容（最後一個只在 `triage` 已安裝時）

寫入前讓他們編輯。

### 4. 寫入

**選擇要編輯的檔案：**

- 如果 `CLAUDE.md` 存在，編輯它。
- 否則如果 `AGENTS.md` 存在，編輯它。
- 如果兩者都不存在，問使用者要建立哪個——不要替他們選。

當 `CLAUDE.md` 已經存在時，絕不建立 `AGENTS.md`（反之亦然）——永遠編輯已經在那裡的。

如果所選檔案中已有 `## Agent skills` 區塊，就地更新它的內容，而不是附加重複的。不要覆寫使用者對周邊章節的編輯。

區塊：

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout — "single-context" or "multi-context"]. See `docs/agents/domain.md`.
```

只在 `triage` 已安裝且 B 章節有跑時，包含 `### Triage labels` 子區塊並寫 `docs/agents/triage-labels.md`。沒安裝時，兩者都省略。

然後用本技能資料夾中的種子模板作為起點寫文件檔案：

- [issue-tracker-github.md](./issue-tracker-github.md) — GitHub issue 追蹤器
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md) — GitLab issue 追蹤器
- [issue-tracker-local.md](./issue-tracker-local.md) — 本機 markdown issue 追蹤器
- [triage-labels.md](./triage-labels.md) — 標籤對應（只有 `triage` 已安裝時）
- [domain.md](./domain.md) — 領域文件消費規則 + 佈局

對「其他」issue 追蹤器，從零用使用者的描述寫 `docs/agents/issue-tracker.md`。

### 5. 完成

告訴使用者設定完成，以及哪些工程技能現在會讀取這些檔案。提到他們之後可以直接編輯 `docs/agents/*.md`——只有在他們想切換 issue 追蹤器或從頭重來時，才需要重跑這個技能。
