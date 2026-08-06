## 用途

`resolving-merge-conflicts` 逐區塊處理進行中的 git merge 或 rebase，然後執行專案自己的檢查，並以一次 commit 完成操作。

它拒絕把衝突當成文字問題。在觸碰區塊之前，它把每一方追溯回其**[主要來源](https://www.aihero.dev/ai-coding-dictionary/primary-source)**——commit 訊息、PR、原始 issue——所以它是在兩個意圖之間做選擇，而不是在兩塊文字之間，而且只要兩者相容，它會兩者都保留。當它們真的不相容時，它挑選符合 merge 既定目標的那一方，並點名取捨。它不會發明新行為來掩蓋衝突，而且 `--abort` 不是它擁有的選項：merge 永遠會被帶到完成的 commit。

## 何時使用

輸入 `/resolving-merge-conflicts`，或當任務適用時，[代理](https://www.aihero.dev/ai-coding-dictionary/agent)會自動採用它。

當 git 已經停在它自己無法解決的衝突上時取用它。它的範圍限定在你面前的衝突，而不是它任何一側的東西：

| 你的情境 | 技能 |
| --- | --- |
| merge 或 rebase 進行中，樹中有衝突標記 | 這個 |
| merge 完成，現在有東西以你看不到的原因行為異常 | [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) |
| 規劃如何切分工作，讓分支比較不會碰撞 | 都不是——見下方平行工作的問題 |

## 主要來源優先於 ours 與 theirs

這個技能存在是為了消滅的失敗模式是按旗標解析：`--ours`、`--theirs`，或手工刪除看起來較不重要的區塊，讓標記消失、建置能編譯。那種解析在語法上可能完美，卻仍然默默丟掉某人刻意做的變更。

你無法保留你沒讀過的意圖。所以工作從歷史開始——commit、PR、[ticket](https://www.aihero.dev/ai-coding-dictionary/ticket)——然後才移到 diff。迴圈中還有一個步驟出於相同理由存在：技能找出儲存庫自己的[自動化檢查](https://www.aihero.dev/ai-coding-dictionary/automated-check)並在提交前執行它們，因為 merge 是 git 中最容易產生「同時滿足兩個分支、卻通不過任何一方測試」的程式碼的地方。

## 常見問題

**Claude Code 自己已經很會解決衝突了。為什麼這需要技能？**

附加價值是「找到主要來源」與「跑回饋迴圈」這兩個步驟，否則它們每次都得用手工提示。未提示的代理通常只憑 diff 就能產出看似合理的解析，然後就此打住。技能的價值是它不讓代理跳過的兩個步驟——閱讀每一方為何存在，以及之後執行檢查。這對一個好的[模型](https://www.aihero.dev/ai-coding-dictionary/model)來說是薄薄的一層優勢，而且本來就是：至少有一位讀者預測過，這是一個會隨著模型進步而變成 no-op 的完整技能。

**我應該把平行代理隔離在相同檔案之外，從根本上避免衝突嗎？**

大多不必。在平行任務之間劃分檔案區，花費比省下更多，因為代理對 merge 衝突已經夠好，取捨沒有看起來那麼嚴苛。值得保留的一項紀律是先做大型重構。在十個分支從它分叉之後才落地的大型改名，就是保持昂貴的案例。

一則關於平行 worktree 的使用者回報中的一個注意事項：當兄弟[會話](https://www.aihero.dev/ai-coding-dictionary/session)各自在自己的樹中建置一個 ticket 時，合併回去最好由寫下那個變更的會話執行，因為它就是已經知道意圖的那一個。最後把所有人的衝突批次丟給一個代理，正好丟掉此技能第 2 步必須回去重建的[上下文](https://www.aihero.dev/ai-coding-dictionary/context)。

**為什麼永遠不用 `--abort`？**

Abort 會丟掉解析工作，並在你下次嘗試時把你送回同一個、不變的衝突。技能是為 merge 必然會發生的案例寫的。如果你已經決定它不該發生，那是呼叫前該做的決定，不是迴圈內部的分支。

## 這樣就算成功

- 代理在解析時會引用 commit 訊息、PR 或 issue 給你看，而不只是 diff 區塊。
- 每個區塊最後都保有雙方的行為，或附帶一個點名丟掉什麼與原因的明確註記。
- 結果中沒有出現任何原本不屬於兩個分支之一的東西。
- 型別檢查、測試與格式化在 commit *之前*就被找到並以綠色跑完，而不是在你注意到某個東西壞了之後。
- 你在乾淨的樹上結束，操作完成——包括多 commit rebase 中每一個剩餘的 commit。

## 它在哪裡適用

一個隨時可取用的獨立技能，不依賴任何其他技能：它在 git 停住時開始，在樹乾淨且已提交時結束。它唯一的真實鄰居是 [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs)，後者在 merge 乾淨解決但合併後的程式碼行為異常——這是診斷問題，不是衝突問題——的地方接手。它完全脫離從點子到交付的主流程，所以 [ask-matt](https://aihero.dev/skills-ask-matt) 是它在之前與之後該跑什麼的地圖。
