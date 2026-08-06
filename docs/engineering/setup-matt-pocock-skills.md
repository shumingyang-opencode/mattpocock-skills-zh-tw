## 用途

`setup-matt-pocock-skills` 回答關於一個儲存庫的三個問題——issue 住在哪裡、分診標籤叫什麼、領域文件放在哪裡——並把答案以 markdown 檔案記錄在 `docs/agents/` 下。

那些檔案是儲存庫之間唯一不同的東西。技能們在任何地方都相同；它們在執行時讀取 `docs/agents/issue-tracker.md` 並照著做。這就是為什麼這套技能不受限於 GitHub，也為什麼沒有任何技能檔案需要編輯才能指向別處。以「link the skills to a custom issue tracker」呼叫它，對任何你能以程式方式連接的東西都有效，技能本身零變更。

它是提示詞驅動的技能，不是確定性腳本。它讀取你的 `git remote`、既有的 `CLAUDE.md`、既有的 `CONTEXT.md`，提議它找到的內容，並在寫入任何東西之前等你確認。

## 何時使用

你輸入 `/setup-matt-pocock-skills` 來呼叫它——[代理](https://www.aihero.dev/ai-coding-dictionary/agent)不會自行使用它。它刻意被標記為不可呼叫，所以其他技能也不能替你觸發它。

每個儲存庫一次，在任何其他工程技能首次使用之前。如果 [triage](https://aihero.dev/skills-triage)、[to-spec](https://aihero.dev/skills-to-spec)、[to-tickets](https://aihero.dev/skills-to-tickets) 或 [wayfinder](https://aihero.dev/skills-wayfinder) 開始猜你的 issue 該去哪裡，或套用你的追蹤器沒有的標籤，那就是它們在這裡還沒被設定。一個專案已進行一半的儲存庫也是執行它的好地方；技能會讀取已存在的內容，先前的工作不會浪費。

## 前置條件

它寫入你執行它的儲存庫：

| 它寫入 | 哪裡 |
| --- | --- |
| `issue-tracker.md` | `docs/agents/` |
| `domain.md` | `docs/agents/` |
| `triage-labels.md` | `docs/agents/`，只在安裝 `triage` 技能時 |
| 一個 `## Agent skills` 區塊 | `CLAUDE.md` / `AGENTS.md` 中已存在的那一個 |

全部都是會提交的 markdown。沒有使用者層級或全域模式：設定住在儲存庫中，所以每個儲存庫都有自己的副本。

## 三個決定

它用建議的答案引領每個區段，並跳過已經定案的探索。大多數執行是兩次確認就完成。

| 決定 | 它提議什麼 | 它實際上什麼時候問 |
| --- | --- | --- |
| **Issue 追蹤器** | 符合你 `git remote` 的那一個 | 永遠——這是唯一真正的選擇 |
| **分診標籤** | 保留五個標準名稱（`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human`、`wontfix`） | 只在安裝 `triage` 技能時 |
| **領域文件** | 單一上下文：根目錄一個 `CONTEXT.md` 加上 `docs/adr/` | 只在它偵測到 monorepo 訊號時，然後它會提供多上下文的 `CONTEXT-MAP.md` |

追蹤器選項：

| 選項 | issue 住在哪裡 | 需要 |
| --- | --- | --- |
| **GitHub** | 儲存庫的 GitHub Issues | `gh` CLI |
| **GitLab** | 儲存庫的 GitLab Issues | `glab` CLI |
| **本機 markdown** | 此儲存庫中 `.scratch/<feature>/` 下的檔案 | 不需要——完全沒有 remote |
| **其他** | 你說的地方 | 你的一段描述工作流程的文字 |

前三種以模板形式隨附在技能中，開箱即用。本機 markdown 是一等選項，不是後備：沒有 remote 的個人專案獲得完整支援。一個值得重複的注意事項：如果你在用 GitHub，就別用本機 markdown。它們是替代方案，不是分層。

「其他」也不是樁。它就是 Jira、Linear、Azure DevOps 與 Beads 都能運作的原因：你描述工作流程，技能把你的文字記錄在 `docs/agents/issue-tracker.md`，而下游技能遵循文字。社群已經做過——Jira 透過 [MCP](https://www.aihero.dev/ai-coding-dictionary/mcp) 的變體、外觀像 `gh` 的 Gitea CLI、手工打造的本機儀表板。

## 常見問題

**我必須用 GitHub 嗎？**

不必。GitHub、GitLab 與 `.scratch/` 下的本機 markdown 都以現成模板隨附，而其他任何東西都能透過「other」路徑運作。這是紀錄中被重複最多次的問題，大致是這些話：*「hard locked to github」*、*「can I use GitLab / Jira」*、*「what about Azure DevOps」*。每次的答案都是：追蹤器是設定的答案，不是技能的屬性。

**更新技能之後我需要重新執行它嗎？**

在 v1.1 之後直接被問時，Matt 說要。技能自己的收尾訊息比較軟——它告訴你重新執行只在切換追蹤器或重來時需要。兩者都站得住腳，而差距的原因是真實的：種子模板在不同版本之間會變，所以較舊版本寫出的 `docs/agents/issue-tracker.md` 可能對現在讀它的技能過時。如果下游技能開始做文件描述得不同的東西，重新執行就是便宜的修復。

**它寫到 `CLAUDE.md`，但我用的是 Codex。**

已知缺口，仍開著。檔案選擇規則是「edit `CLAUDE.md` if it exists, else `AGENTS.md`」——它檢查哪個檔案存在，而不是哪個[執行環境](https://www.aihero.dev/ai-coding-dictionary/harness)在跑。一個留有 Claude Code 的 `CLAUDE.md` 的儲存庫，它的 `## Agent skills` 區塊會落在 Codex 從不讀取的地方。有兩個變通方案在流通：手工把區塊移到 `AGENTS.md`，或讓 `AGENTS.md` 保持標準並把 `CLAUDE.md` 變成指向它的一行指標。如果兩個檔案都不存在，技能會問你建立哪一個，而不是自己選——這讓預期它直接決定的人感到困惑。

**它沒有建立我的分診標籤。**

它不會。`docs/agents/triage-labels.md` 是*對應*——它告訴 `/triage` 你追蹤器中的哪些字串對應五個標準角色。它不會執行 `gh label create`。在全新的 GitHub 儲存庫上，標籤真的還不存在，而這已被當成 bug 登記不止一次。兩個後續：

- 如果你的追蹤器已使用標準名稱，對應就是恆等表，沒有什麼要設定的。那是預期的常見案例，不是缺失的步驟。
- [wayfinder](https://aihero.dev/skills-wayfinder) 的 `wayfinder:map` 與 `wayfinder:<type>` 標籤也不會在這裡被建立，而 `gh issue create --label <missing>` 會直接失敗，而不是建立標籤。在 GitHub 儲存庫第一次跑 wayfinder 之前，手工建立它們。

**我可以在這裡設定其他技能的行為嗎——[grilling](https://www.aihero.dev/ai-coding-dictionary/grilling) 的節奏、問題格式、語氣？**

不行。它設定三件事：追蹤器、標籤、文件配置。一直有直接請求要把它變成每位使用者偏好的家，而常駐的答案是技能保持有主見：*「Config is death.」*偏好屬於你的 `CLAUDE.md`，以一般指示的形式，而每個技能本來就會讀它。

**我可以把設定放在 `~/.claude`，而不是提交到每個儲存庫嗎？**

今天不行。有一個未結請求正是要這個，來自一個在許多儲存庫間執行這些技能的人，而沒有使用者層級模式存在。每個儲存庫都攜帶自己的 `docs/agents/`。

**有技能來設定其他技能，不奇怪嗎？**

一個長期存在的抱怨說是，用這些話：*「having a skill to set up the other skill does not feel right to me — that means the LLM is configuring its own skills.」*取捨是真實且被承認的：設定步驟的替代方案，是把追蹤器指示複製進每個觸及 issue 的技能。輸出是可檢查、可編輯的 markdown，這就是緩解——你可以讀它寫的每個檔案並手工修改，而日常微調正是那樣，不是再跑一次。

## 這樣就算成功

- `docs/agents/issue-tracker.md` 與 `docs/agents/domain.md` 存在，加上安裝 `triage` 時的 `triage-labels.md`。
- `## Agent skills` 區段出現在你的執行環境實際讀取的指示檔案中，並有指向那些檔案各自的一行摘要。
- 它提議的追蹤器符合你真正使用的 remote，而標籤字串符合你追蹤器中真實存在的標籤。
- 之後，`/to-tickets` 不再問你 issue 住在哪裡就直接發布，而 `/triage` 套用標籤而不是發明它們。
- 技能檔案本身沒有任何東西改變。如果設定編輯了 `SKILL.md`，就是出事了。

## 它在哪裡適用

`setup-matt-pocock-skills` 是工程流程的**一次性設定**，是其他一切都假設的前置條件，而不是鏈中的一個步驟。它的鄰居是它的讀者：[triage](https://aihero.dev/skills-triage)——套用在這裡寫下的標籤詞彙；[to-spec](https://aihero.dev/skills-to-spec) 與 [to-tickets](https://aihero.dev/skills-to-tickets)——發布進這裡點名的追蹤器；以及 [wayfinder](https://aihero.dev/skills-wayfinder)——讀取同一份追蹤器檔案的「Wayfinding operations」區段，來知道地圖與子 [ticket](https://www.aihero.dev/ai-coding-dictionary/ticket) 如何儲存。它記錄的領域文件配置，是 [domain-modeling](https://aihero.dev/skills-domain-modeling) 之後會填滿的那個——它在術語或決策真正定案時惰性建立 `CONTEXT.md` 與 ADR，所以設定後是空的儲存庫是預期狀態。至於接下來該取用哪個技能，[ask-matt](https://aihero.dev/skills-ask-matt) 導航整套。
