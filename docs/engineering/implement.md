## 用途

`implement` 建置已經被決定的工作。你把它指向某個 [ticket](https://www.aihero.dev/ai-coding-dictionary/ticket)、[規格說明](https://www.aihero.dev/ai-coding-dictionary/spec)，或你剛在對話中同意的計畫，它就會撰寫程式碼、在接縫處驅動 [tdd](https://aihero.dev/skills-tdd)、邊做邊做型別檢查、在結尾執行 [code-review](https://aihero.dev/skills-code-review)，並提交到目前的分支。

它從不重新打開計畫。沒有訪談、沒有澄清輪、沒有提議不同做法。上游定案的一切就是輸入，而技能的整個工作就是把它變成一次 commit。這正是它與對全新[代理](https://www.aihero.dev/ai-coding-dictionary/agent)輸入「build this」的區別，後者會在建置時樂意地重新設計工作。

## 何時使用

你輸入 `/implement` 來呼叫它——代理不會自行使用它。它隨附 `disable-model-invocation: true`，所以其他技能也不能呼叫它。無論 [ask-matt](https://aihero.dev/skills-ask-matt) 或 [to-tickets](https://aihero.dev/skills-to-tickets) 在哪裡說「then `/implement` per ticket」，那是給你的指示，不是代理會未經提示就做的事。

工作目前所在的位置決定這是否為正確的技能：

| 工作目前… | 取用 |
| --- | --- |
| 追蹤器上的一個 ticket | `/implement #42`，每個[會話](https://www.aihero.dev/ai-coding-dictionary/session)處理一個 ticket，ticket 之間[清空](https://www.aihero.dev/ai-coding-dictionary/clearing)上下文 |
| 一份尚未拆分的規格說明，且建置橫跨多個會話 | 先 [to-tickets](https://aihero.dev/skills-to-tickets)，然後逐 ticket 執行 `/implement` |
| 一份規格說明，且建置很小 | 直接針對規格說明執行 `/implement` |
| 只存在於你剛才的對話中，而且仍然很小 | 直接在同一視窗執行 `/implement` |
| 還沒有寫在任何地方 | [grill-with-docs](https://aihero.dev/skills-grill-with-docs)，若沒有代碼庫則用 [grill-me](https://aihero.dev/skills-grill-me) |
| 一個你想要測試優先的具體行為，沒有規格說明 | 直接 [tdd](https://aihero.dev/skills-tdd) |
| 已經建置好，你想要它被檢查 | 直接 [code-review](https://aihero.dev/skills-code-review) |

同一會話的案例值得指名，因為技能自己的第一行沒涵蓋它。`SKILL.md` 說「the spec or tickets」，這會誘使[模型](https://www.aihero.dev/ai-coding-dictionary/model)去找一份不存在的檔案。如果計畫只存在於對話中，呼叫時說出來。

## 前置條件

`implement` 會提交到你目前所在的分支。它不建立分支，也不詢問。開始前先確認你在想要工作所在的分支上。

如果 ticket 來自 [to-tickets](https://aihero.dev/skills-to-tickets)，它們所在的追蹤器是由 [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) 設定的。`code-review` 在收尾時讀取相同的設定來找原始規格說明。

## 一次執行做什麼

一次執行是五拍，依序：

1. 讀取 ticket 或規格說明，並找出接縫。
2. 在預先約定的接縫處驅動 [tdd](https://aihero.dev/skills-tdd)，一次一個紅-綠切片。
3. 頻繁做型別檢查，邊做邊跑單一測試檔案。
4. 在結尾跑一次完整的測試套件。
5. 執行 [code-review](https://aihero.dev/skills-code-review)，然後提交到目前的分支。

一次執行涵蓋一個 ticket。[to-tickets](https://aihero.dev/skills-to-tickets) 產出的 ticket 是曳光彈式的垂直切片，大小適合放進單一全新的[上下文視窗](https://www.aihero.dev/ai-coding-dictionary/context-window)，所以預期的節奏是：清空上下文、實作一個 ticket、提交、再清空。每個 ticket 都自成一體，這正是讓前一個 ticket 的上下文變成可拋棄的原因。

## 預先約定的接縫

此技能賴以運作的概念是**接縫**：你觀察行為的公開邊界，而不深入內部。測試活在接縫處。在任何程式碼寫出之前就約定的接縫上工作，是讓測試持久的原因，因為底下的實作可以在不移動測試的情況下被重寫。

「預先約定」這個詞在做實際的工作，但它也是技能最弱的關節。`implement` 內部沒有東西會約定接縫。`tdd` 是那個會詢問的技能，而且它拒絕在未確認的接縫上寫測試。所以實際上，約定發生在上游的規格說明中，或發生在執行的第一次交流中。如果它沒在任何地方發生，前置條件永遠不會觸發，執行就悄悄變成「just write the code」。在規格說明中指名接縫正是阻止那件事的辦法。

## 常見問題

**它完成了，但我的 ticket 仍然開著，驗收標準仍未勾選。**

正確，而且是預期的。`implement` 沒有完成步驟。它止步於 commit，從不觸碰工作項目——這在 GitHub Issues 與本機 markdown 追蹤器上都已確認，所以不是追蹤器整合問題。它也不會處理 `code-review` 產出的發現，不會勾選原始 issue 上的 `- [ ]` 方框。你自己關閉 ticket 並核對標準。這在相依鏈上咬得最痛，因為 `to-tickets` 把前沿定義為所有阻塞者都已關閉的 ticket。如果沒有東西被關閉，就永遠不會有東西變成可見的未阻塞。

**我可以一次把它指向所有 ticket，或平行執行多個嗎？**

不行。一次呼叫，一個 ticket。跨 ticket 佇列的批次派發與[子代理](https://www.aihero.dev/ai-coding-dictionary/subagent)扇出都被反覆要求，但兩者都不存在。在同一個 checkout 中並排執行多個 `/implement` 會話，比不支援還糟：一則實地回報描述了某個會話中的 `git commit --amend` 落在另一個會話的 commit 上、一個 stash 從 `refs/stash` 消失、commit 落在錯誤的分支，全部發生在一個下午、橫跨三個 issue。這些會話共享一個工作目錄、一個 index、一個 HEAD。Git worktree 是社群的變通方案，而且要注意 `refs/stash` 在 worktree 之間也是共享的，所以光靠 worktree 不能修好 stash 的案例。如果你今天想要平行性，你得自己組裝它。

**它可以開 pull request 而不是提交嗎？**

沒有內建。它直接提交到目前的分支，這讓幾個人覺得太急：程式碼在他們有機會驗證它能運作之前就落地了。沒有設定旗標，也沒有 PR 模式。人們會在呼叫中覆寫它（「commit to a branch and open a PR」），或編輯技能的本機副本。

**`code-review` 說它看不到我的變更。**

`code-review` 審查 `git diff <fixed-point>...HEAD`，這會排除已暫存與工作樹的變更。`implement` 在提交前執行它，所以除非已有過渡性 commit，否則那個 diff 裡沒有東西可審查。多人已回報此事，而兩邊都未修復。先 commit，再以你分叉的點做審查。

另外，有些人刻意完全不想要執行中的審查，因為審查自己剛寫的程式碼的代理會偏袒自己的方案。在全新會話中針對固定點執行 [code-review](https://aihero.dev/skills-code-review) 是合理的替代方案，而那也正是該技能在兩個獨立子代理中執行兩個軸的原因。

**一個 ticket 燒掉 150k 個 token。我用錯了嗎？**

大概是 ticket 太大，而不是技能被誤用。一次執行會做代碼庫探索、每個接縫一個紅-綠迴圈、完整套件與一次審查，所以一個非瑣碎的 ticket 超過 100k [token](https://www.aihero.dev/ai-coding-dictionary/token) 是正常的，而不是某個東西壞了的跡象。施力點在上游：在 [to-tickets](https://aihero.dev/skills-to-tickets) 中把 ticket 尺寸調整正確，讓每個都能放進一個全新的視窗。如果單一 ticket 不斷爆掉，拆開它，而不是調高[投入](https://www.aihero.dev/ai-coding-dictionary/effort)等級。

**在全新會話中執行 `/implement #2` 卻處理了完全無關的東西。**

`#2` 是相對於代理能看到的任何編號清單解析的，在全新會話中可能是 todo 檔案、檢查清單或另一份工作清單，而不是已設定的追蹤器。解析是自信的，而不是失敗即封閉的，所以錯誤要等到開始後才明顯。傳入完整參照、issue URL 或 `owner/repo#2`，並要求它在開始前把標題回報確認。

## 這樣就算成功

- 會話以讀取 ticket 或規格說明並重述它要建置什麼開始，而不是問你要建置什麼。
- 你可以在追蹤紀錄中看到實際的 `/tdd` 呼叫，而不只是測試出現在 diff 中。
- 型別檢查與單一測試檔案在執行期間反覆執行，而完整套件在接近尾聲時執行一次。
- 執行在你目前的分支上到達一次 commit，不需要你催促它繼續。
- diff 是一個 ticket 份量的變更：穿透每個層的垂直切片，而不是幾張 ticket 混在一起。

## 它在哪裡適用

`implement` 是主鏈的建置步驟，倒數第二個：

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review
```

它的鄰居是 [to-tickets](https://aihero.dev/skills-to-tickets)——它產生此技能消費的 ticket，並宣告決定它們順序的阻塞邊；[tdd](https://aihero.dev/skills-tdd)——它在每個接縫內部驅動它；以及 [code-review](https://aihero.dev/skills-code-review)——它在提交前執行。它座落於規劃技能的下游並信任它們。它不會重新驗證交給它的東西的形狀，所以結構不良的地圖或水平分層的 ticket 會按原文被建置。

正是這種信任讓 [wayfinder](https://aihero.dev/skills-wayfinder) 在 [to-spec](https://aihero.dev/skills-to-spec) 處匯入鏈中，而不是把它的地圖直接迴圈進 `implement`。只有當工作結果真的很小時，才從地圖直接去 `implement`。

當你不確定自己身處哪條流程時，[ask-matt](https://aihero.dev/skills-ask-matt) 是整套技能的路由器。
