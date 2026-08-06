## 用途

`triage` 依序處理專案追蹤器上的 issue，讓每個 issue 通過由**分診角色**組成的迷你狀態機——一個分類角色與一個狀態角色——並留下代理簡報、給報告人的具體問題，或帶有記錄原因的已關閉 issue。

它只適用於**你沒有建立**的 issue。原始 bug 報告、湧入的功能請求、未預告就抵達的外部 pull request——從外部落入追蹤器的工作，以報告人留下的任何形狀。[to-tickets](https://aihero.dev/skills-to-tickets) 產出的 [ticket](https://www.aihero.dev/ai-coding-dictionary/ticket) 靠建構就已是代理就緒，在它們上面跑 `triage` 頂多是浪費工作。規則是平直的：`/triage` 只用於湧入的 issue，不用於你自己建立的 issue。

第二件讓它與手工貼標籤不同的事：它建議並等待。它告訴你它的分類與狀態判定，附帶推理，加上它在代碼庫中找到的內容，而且在你指示之前不套用任何東西。

## 何時使用

你輸入 `/triage` 並以平白語言描述你要什麼——[代理](https://www.aihero.dev/ai-coding-dictionary/agent)不會自行使用它。「Show me anything that needs my attention」、「let's look at #42」、「move #42 to ready-for-agent」。

| 你有什麼 | 該去哪裡 |
| --- | --- |
| 一個充滿其他人原始報告的追蹤器 | `/triage` |
| 你自己粗略的想法，什麼都沒寫下來 | [grill-with-docs](https://aihero.dev/skills-grill-with-docs) |
| 一場要變成[規格說明](https://www.aihero.dev/ai-coding-dictionary/spec)的定案對話 | [to-spec](https://aihero.dev/skills-to-spec) |
| 一份要拆成代理就緒 ticket 的規格說明 | [to-tickets](https://aihero.dev/skills-to-tickets) |
| 一個需要根本原因、不是標籤的已確認 bug | [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) |

## 前置條件

`triage` 讀寫你的 issue 追蹤器，所以 [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) 必須先設定那個追蹤器與它的標籤詞彙。下方的角色名稱是**標準**；你追蹤器中的標籤字串可能不同，而對應就是設定提供的東西。如果你的追蹤器已經精確使用標準名稱，就沒有什麼要對應、沒有什麼要設定。

追蹤器設定也決定外部 pull request 是否算請求表面，以及誰算外部。那個旗標預設為關，不再是設定的問題——如果你想讓 PR 納入範圍，在 `docs/agents/issue-tracker.md` 中把它打開。

## 狀態機

每個被分診的項目最後都恰好攜帶一個分類角色與一個狀態角色。兩個分類：`bug`（有東西壞了）與 `enhancement`（新功能或改進）。五個狀態：

| 狀態 | 意思 |
| --- | --- |
| `needs-triage` | 你需要評估它。未標籤 issue 通常最先落腳的地方。 |
| `needs-info` | 等待報告人。他們回覆時回到 `needs-triage`。 |
| `ready-for-agent` | 完全指定，附代理簡報。[AFK](https://www.aihero.dev/ai-coding-dictionary/afk) 代理可以接下它。 |
| `ready-for-human` | 相同簡報，加上為什麼這不能被委派——判斷、外部存取、手工測試。 |
| `wontfix` | 已關閉，原因已記錄。 |

這就是全部的詞彙，而「恰好一個狀態角色」的不變量正是讓查詢保持簡單的東西。它也是此[技能](https://www.aihero.dev/ai-coding-dictionary/skill)被要求最多的區域：使用者要求過一個給「已指定但阻塞於另一個 issue」工作的第六狀態、一個以未來觸發條件為門檻的 `deferred` 工作狀態，以及一個終端 `implemented` 狀態。這些都沒發布。見下方問題。

`wontfix` 有三種拆分，而差異重要，因為只有其中一種寫入知識庫：

| 你為什麼關閉它 | 會發生什麼 |
| --- | --- |
| 已經實作 | 一個指向它已存在處的評論。`.out-of-scope/` 不寫入任何東西——它是已建置的功能，不是被否決的，歸檔到那裡會毒化去重檢查。 |
| 被否決的 bug | 禮貌的解釋，然後關閉。 |
| 被否決的增強 | `.out-of-scope/` 中的一個檔案，從關閉評論連結，然後關閉。 |

`.out-of-scope/` 是每個被否決**概念**一個 markdown 檔案，而不是每個 issue 一個，以簡短設計文件而非資料庫列的方式撰寫：什麼被否決、為什麼，以及每個要求過它的 issue。`triage` 在評估任何東西之前讀取整個目錄，並以概念而非關鍵字比對——「night theme」比對到 `dark-mode.md`。當它命中時，它浮現舊決策並問你是否仍有同樣感覺，而不是從頭重新爭辯請求。

## 在撰寫簡報之前先驗證

在任何 [grilling](https://www.aihero.dev/ai-coding-dictionary/grilling) 之前，`triage` 檢查聲稱是否真的成立。對 bug，它依報告人的步驟重現。對 PR，它檢出分支並跑相關測試。然後它回報三種事情的哪一種發生：已確認，附程式碼路徑；無法重現；或細節不足無法嘗試——這本身就是最強烈的 `needs-info` 訊號。

它在同一次處理中對代碼庫再跑兩項檢查——**冗餘**（這是否已實作，以領域概念而非報告人的措辭搜尋？）與**先前否決**（`.out-of-scope/` 是否已說不？）。兩者都便宜，而兩者在命中時都產生 `wontfix`。

這一切都是為了讓一件產物變好：**代理簡報**，即 issue 移到 `ready-for-agent` 時發布的結構化評論。一旦發布，簡報就是契約，而原始報告只是上下文。簡報以**持久**而非精確為目標撰寫，因為 issue 可能在 `ready-for-agent` 待上數週，而程式碼在它底下移動。所以它們點名型別、簽章與行為契約，永遠不點名檔案路徑或行號。已確認的重現比猜測做出強得多的簡報。

## PR 是附帶程式碼的 issue

當追蹤器把外部 pull request 當作請求表面時，它們通過同一台機器——相同分類、相同狀態、相同轉換。狀態只是對照 diff 讀：`ready-for-agent` 表示附了簡報，代理應該對程式碼採取下一步；`ready-for-human` 表示它已準備好讓人合併。PR 上的簡報描述的是對既有 diff 還剩什麼要做，而不是如何從無到有建置那個東西。

探索只浮現*外部* PR，因為協作者進行中的分支不是分診工作。那個篩選器只影響探索——明確點名一個 PR，無論誰寫的它都會被分診。一個粗糙邊緣：GitHub 模板的外部 PR 列出指令要求 `gh pr list` 提供一個 `gh` 不暴露的 `authorAssociation` 欄位，所以照寫的指令直接失敗（[#468](https://github.com/mattpocock/skills/issues/468)）。

## 常見問題

**我跑了 `/to-spec` 與 `/to-tickets`，現在那些 ticket 坐在那沒被分診。我要在它們上面跑 `/triage` 嗎？**
不。它們已經代理就緒——`to-tickets` 在發布時套用 `ready-for-agent` 標籤，正是為了讓 AFK 執行者不用再跑一次就能接起它們。遇到這個問題的使用者跑了規格流程、在輸出上看到 `needs-triage`，然後發現他們的 AFK 執行者忽略了一切。`triage` 是外來工作的入口；規格流程是你主動發起的工作的車道。它們在 `ready-for-agent` 會合，而不是更早。

**既然有了 `to-spec` → `to-tickets` → `implement` 流程，`triage` 還有用嗎？**
只有當你有湧入的工作時。`triage` 早於那條脊柱，做的是不同的工作：它是別人歸檔的報告的車道。如果你追蹤器中的一切都出自你自己的規劃，你很少會打開它。如果你維護任何公開的東西，或你的團隊朝你回報 bug，它是正門。主要用途是接收外部貢獻者 issue 的開源儲存庫。

**代理嘗試套用 `ready-for-agent`，`gh` 說那個標籤不存在。**
已知的未結 bug（[#616](https://github.com/mattpocock/skills/issues/616)）。`setup-matt-pocock-skills` 把標籤詞彙寫進 `docs/agents/triage-labels.md`，但不會在你的追蹤器中建立標籤。用 `gh label create` 或追蹤器的 UI 自己建立五個狀態標籤與兩個分類標籤，一次，它就停了。issue 有連結一個尚未合併的社群修復分支。

**五個狀態不夠——那 blocked、deferred 或 implemented 呢？**
這是此技能被登記最多的缺口，有三種形狀。一個完全指定、但等待另一個 issue 關閉的 issue（[#139](https://github.com/mattpocock/skills/issues/139)）——報告人的抱怨是 `ready-for-agent` 在那裡「technically true」卻有誤導性，所以代理接起它然後撞牆。以未來觸發條件為門檻、已打算做但還不可執行的未來工作（[#297](https://github.com/mattpocock/skills/issues/297)）。以及一個給「implemented, awaiting verification」的終端狀態，沒有它 AFK 執行者可能把完成的 ticket 重新排隊。Matt 已同意阻塞的案例是真的，並對名稱（`blocked` 對 `paused`）未定。它們都沒發布。人們用的變通法是分類旁加一個儲存庫本機的額外標籤，讓標準狀態槽被誠實的東西佔據，代價是技能不知道它。一個社群衍生技能走得更遠，加入 `needs-slicing`、`tracking` 與 effort 標籤——那有效，但那是他們的，不是技能的。

**這跟 `/diagnosing-bugs` 有什麼不同？**
這裡的驗證步驟刻意很淺——足以回答「這是不是真的、大概住在哪裡」，而不是找根本原因。當 bug 無法在幾分鐘內依報告人的步驟重現時，誠實的動作是 `needs-info`，或如果你想現在追它，用 [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs)。兩個技能的文字目前都不提對方；有位使用者發現了那個接縫，它仍開著。

**我可以把它指向整個 backlog 讓它跑嗎？**
你可以要求，但留意它讀什麼。「show what needs attention」的處理是便宜的清單，目的是*挑選*——你挑一個，然後它對你挑的那個收集完整[上下文](https://www.aihero.dev/ai-coding-dictionary/context)。一次對二十個 issue 跑，代理可能悄悄退到那份便宜清單作為證據基礎，那會回傳 issue 內文，但不回傳評論。有位使用者正好遇到這個：三個 issue 已帶有「already fixed, recommend closing」的評論，而三個都改得到全新的代理簡報。如果你想要批量處理，明確說出每個 issue 都必須讀評論。

**它能用 Linear 或其他非 GitHub Issues 的追蹤器嗎？**
可以——追蹤器是設定，不是寫死的假設，而人們會對 Linear（透過 `linear` CLI）、GitLab 與 `.scratch/` 下的純 markdown 檔案跑它。常見的分法是 issue 與規劃用 Linear、程式碼與 PR 用 GitHub：說「issue tracker」的技能對應到 Linear，說「PR」的技能對應到 GitHub。在本機 markdown 追蹤器上有一個未結的模板 bug，產生的檔案可能把驗收標準攜帶兩次，一次在頂層，一次在代理簡報內（[#200](https://github.com/mattpocock/skills/issues/200)）。

## 這樣就算成功

- 它觸及的每個項目最後都恰好有一個分類角色與一個狀態角色——永遠不是零，永遠不是兩個衝突的狀態。
- 它給你附帶推理的建議並停下來，而不是重新貼標籤然後繼續。
- 在任何東西到達 `ready-for-agent` 之前，bug 被重現了，或 PR 被檢出並執行了。
- 它寫的簡報點名型別與行為，且不含檔案路徑與行號。
- 一個六個月前被否決的請求回來，它會說明並引用舊原因，而不是把它當成新的重新分診。
- 它發布的每個評論都以 `> *This was generated by AI during triage.*` 開頭。

## 它在哪裡適用

`triage` 是**入口**，不是主鏈中的一個步驟。主流程從你有的點子開始——grill、規格說明、ticket、實作、審查——而 `triage` 是外來工作的平行車道。它在同一個地方匯合：一個帶簡報、標示 `ready-for-agent` 的 issue，[implement](https://aihero.dev/skills-implement) 會以處理 [to-tickets](https://aihero.dev/skills-to-tickets) ticket 的方式接起它。當請求在能寫簡報之前需要磨利時，`triage` 一起跑 [grilling](https://aihero.dev/skills-grilling) 與 [domain-modeling](https://aihero.dev/skills-domain-modeling)，一次一輪問題，所以決策在做出當下就落進 `CONTEXT.md` 與 ADR。當你不確定自己在哪條車道時，[ask-matt](https://aihero.dev/skills-ask-matt) 會幫你導航。
