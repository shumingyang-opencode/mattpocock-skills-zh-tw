## 用途

`to-tickets` 接受一個計畫、一份[規格說明](https://www.aihero.dev/ai-coding-dictionary/spec)，或你正在進行的對話，並把它拆成你 issue 追蹤器上的一組 **[ticket](https://www.aihero.dev/ai-coding-dictionary/ticket)**。每個 ticket 宣告它的**阻塞邊**——在它開始之前必須完成的其他 ticket。

每個 ticket 都是一顆**曳光彈**：穿越變更每一層——schema、API、UI、測試——的狹窄但完整的路徑，落地當下就能獨立 demo。這個約束讓它與顯而易見的拆分方式（一次切一個層，最後再整合）行為不同。它也會把每個 ticket 定尺寸到能裝進單一全新的[上下文視窗](https://www.aihero.dev/ai-coding-dictionary/context-window)，因為會接起 ticket 的東西是一個從未看過你規格說明的[會話](https://www.aihero.dev/ai-coding-dictionary/session)。

## 何時使用

你輸入 `/to-tickets` 來呼叫它——[代理](https://www.aihero.dev/ai-coding-dictionary/agent)不會自行使用它。

| 你在哪裡 | 跑什麼 |
| --- | --- |
| 你有一個規格 issue，且建置橫跨多個會話 | `/to-tickets`，或 `/to-tickets #<spec_issue>` |
| 計畫只存在於對話中，從未成文 | `/to-tickets` 直接讀對話——不需要規格說明 |
| 整個變更裝得進一個上下文視窗 | [implement](https://aihero.dev/skills-implement)——跳過 ticket |
| 還沒有任何東西被決定 | [grill-with-docs](https://aihero.dev/skills-grill-with-docs)，然後 [to-spec](https://aihero.dev/skills-to-spec) |
| [wayfinder](https://aihero.dev/skills-wayfinder) 地圖已清空 | 先 [to-spec](https://aihero.dev/skills-to-spec) 摺疊地圖，然後 `/to-tickets` |

`to-tickets` 產出的 ticket 靠建構就已是代理就緒。不要在它們上面跑 [triage](https://aihero.dev/skills-triage)——triage 是給來自其他人的工作。

## 前置條件

`to-tickets` 發布進追蹤器，所以 [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) 必須為此儲存庫設定一個，連同分診標籤詞彙。任一類型都行：像 GitHub 或 Linear 這樣真實的追蹤器，或 `.scratch/` 下的本機 markdown 檔案，後者開箱即受支援。

## 曳光彈，不是分層

**水平**切片交付變更的一層。要等到每一層都落地才有東西能運作，而每個 ticket 的驗收標準都得伸進另一個 ticket 擁有的工作。**垂直**切片——曳光彈——一次穿越所有層交付一條薄路徑，所以它能單獨驗證，並擁有它所評分的一切。

這是人們最常違反的規則，而後果廣為記載。有個團隊跑了一疊依層切分的 26 張 ticket——corpus、producer、aggregator、selector——每個已關閉 ticket 大約花了二十次代理執行，其中約四分之三是返工。他們自己的事後檢討把每個失敗類別都追溯到水平切片，而不是實作本身。

在發布任何東西之前有兩件事發生。`to-tickets` 尋找預先重構——「make the change easy, then make the easy change」——並把那項工作排到前面。然後它以編號清單呈現拆分，並就它盤問你：粒度對嗎、阻塞邊是真的嗎、有沒有東西該合併或拆分。在你批准之前沒有東西到達追蹤器，而那次盤問正是反擊的地方。

## 阻塞邊

邊是這項產物的重點。依追蹤器不同，它們有兩種讀法：

| 追蹤器 | 邊住在哪裡 | 你怎麼處理它們 |
| --- | --- | --- |
| 本機 markdown | `.scratch/<feature>/issues/<NN>-<slug>.md` 下每個 ticket 一個檔案的文字，阻塞者優先編號 | 從上到下，用手 |
| 真實追蹤器（GitHub、Linear） | 原生阻塞連結，或追蹤器有時的子 issue | 任何阻塞者完成的 ticket 都在**前沿**上，可以被抓走 |

無論哪種方式，邊都住在 ticket 中。媒介只決定是否有東西能平行作用於它們。`to-tickets` 產出產物；執行它——一次一個會話，或一整隊——是你的工作，不是技能的。

## 大範圍重構例外

一種形狀打破曳光彈規則。**大範圍重構**是單一機械性的變更——重新命名欄位、重新定義共用符號的型別——其**影響半徑**扇開到整個代碼庫，所以一次編輯弄壞數千個呼叫點，而沒有垂直切片能綠色落地。

`to-tickets` 改以**擴展-收縮**排序它：

- **擴展**——在舊形式旁邊加入新形式，所以沒有東西壞掉。
- **遷移**——依影響半徑定尺寸（每個套件、每個目錄）批次搬移呼叫點，每批一張 ticket，每個都被擴展阻塞。CI 保持綠色，因為舊形式仍然存在。
- **收縮**——一旦沒有呼叫者剩餘，在一個被每個遷移批次阻塞的 ticket 中刪除舊形式。

當連批次都無法單獨保持綠色時，它們共享一個集成分支，並全部阻塞最後一個整合並驗證的 ticket。綠色只在彼處被承諾。

## 常見問題

**它為一個三行的變更產出十二張 ticket。**

過度分解是此技能被回報最多的摩擦，而且在實務工作者之間一致：[模型](https://www.aihero.dev/ai-coding-dictionary/model)預設採原子單位，失去讓它們有意義的分組。盤問步驟正是為此存在——要求它合併，它就會。更深的答案是 ticket 有一個底線：如果整個變更裝得進一個上下文視窗，你根本不需要此技能。直接去 [implement](https://aihero.dev/skills-implement)。

**ticket 出來是一層一張——schema 全部在一張，API 全部在另一張。**

這是垂直切片規則為之而寫的失敗，而技能有時仍產出它。在盤問步驟抓住它，對每個 ticket 問一個問題：這個完成時我能 demo 什麼？沒有答案的 ticket 就是水平切片。有些人為此在每個 ticket 加入「demo path」一行，並回報它會把模型推向垂直分解。

**在 GitHub 上，ticket 沒有被建立為規格 issue 的子 issue。**

已知且未修復。它已被回報橫跨十幾次執行與好幾個模型，[issue #554](https://github.com/mattpocock/skills/issues/554) 記載最完整，而且在 Codex 上比在 Claude 上更糟。`gh` 自 v2.94 起原生支援這個：`gh issue create --parent <n>`，以及事後 `gh issue edit <parent> --add-sub-issue <n>`。在追蹤器模板偏好那些之前，執行後自己接上父連結是可靠的動作。

**「Blocked by」被寫進 issue 內文，而不是真實的阻塞連結。**

同類問題，[issue #513](https://github.com/mattpocock/skills/issues/513) 有記載，其中代理甚至斷言 GitHub 根本沒有原生阻塞關係。它有——`gh issue create --blocked-by 12,15`。因為阻塞者先發布，它們的號碼在建立時永遠可用。內文是給沒有原生邊的追蹤器的後備，不是預設。

**本機 ticket 去哪了？v1.1 的筆記說根層級有個 `tickets.md`。**

它們是那樣，而那曾是 bug——單一共用檔案在平行代理寫入時也會競爭。本機模式現在依相依順序，在 `.scratch/<feature-slug>/issues/<NN>-<slug>.md` 下每個 ticket 寫一個檔案，符合本機追蹤器模板已描述的配置。`NN` 前綴是真實的 ticket ID，所以 `/implement 03` 有效，而不是重新輸入長標題。

**它嘗試讀我的規格說明時一直截斷。**

非常大的規格說明可能超出追蹤器 issue 能乾淨回送的範圍，而且沒有本機副本可回退——代理接著燒掉 [tool calls](https://www.aihero.dev/ai-coding-dictionary/tool-call) 重新取得區塊，永遠到不了結尾。不要在 `/to-spec` 與 `/to-tickets` 之間 [clear](https://www.aihero.dev/ai-coding-dictionary/clearing) 或 [compact](https://www.aihero.dev/ai-coding-dictionary/compaction)。在同一個上下文視窗跑它們，規格說明就完全不需要被重新取得。

**驗收標準什麼都沒評分——有些在還沒做任何工作之前就通過了。**

模板要求標準，卻對它們能否失敗隻字未提，所以這會發生。三種形狀反覆出現：在基準 commit 已經為真的標準、只能由另一個 ticket 擁有的工作滿足的標準、以及重述請求而非從產物推導的標準。垂直切片防止其中大部分——一個交付過去不存在行為的切片，靠建構在基準 commit 就是紅的——但這項檢查仍值得手工做。對每個標準，點名能證明它為假的觀察，並確認它在實作者開始的 commit 上失敗。

**ticket 已發布。我要怎麼實際執行它們？**

技能止步於產物，沒有自動派發模式。派發是手工的：看板子、數沒有未結阻塞者的 ticket、開那麼多代理會話。每個全新上下文一個 ticket，之間清空。要注意 [implement](https://aihero.dev/skills-implement) 在完成時不會可靠地關閉或勾選 ticket——在 GitHub 或本機 markdown 都一樣——所以 ticket 的狀態由你更新。

## 這樣就算成功

- 每個 ticket 都有「this is done 時我能 demo 什麼？」的答案——而答案是行為，不是一層。
- 清單以編號回到你手上，每個都帶「Blocked by」一行，在任何東西發布之前。
- 頂端的 ticket 沒有阻塞者，可以立刻開始。
- ticket 內文中沒有檔案路徑或行號，除了原型產出的一段片段。
- 每個 ticket 讀起來都像全新會話能在你不在場的情況下完成的東西。
- 預先重構，在找到時，排在順序前面，而不是混進功能 ticket。

## 它在哪裡適用

`to-tickets` 是主建置鏈中的一個步驟：

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review
```

上游是 [to-spec](https://aihero.dev/skills-to-spec)，交給它一份定案的規格說明供切片——把兩者都放在一個不中斷的上下文視窗。下游是 [implement](https://aihero.dev/skills-implement)，每個全新會話建置一張 ticket，驅動 [tdd](https://aihero.dev/skills-tdd) 做測試，並以 [code-review](https://aihero.dev/skills-code-review) 收尾。當你不確定哪個技能或流程適用時，[ask-matt](https://aihero.dev/skills-ask-matt) 會幫你導航。
