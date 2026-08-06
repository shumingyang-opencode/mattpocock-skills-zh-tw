## 用途

`code-review` 沿著兩個軸審查 `HEAD` 與你所指定固定點之間的 diff——某個 commit、某個分支、某個標籤、`main`、`HEAD~5`。**規範**軸詢問程式碼是否遵循這個儲存庫撰寫程式碼的方式。**規格**軸詢問程式碼是否做了原始 issue 或[規格說明](https://www.aihero.dev/ai-coding-dictionary/spec)要求的事。每個軸在各自的[子代理](https://www.aihero.dev/ai-coding-dictionary/subagent)中執行，因此雙方都看不到另一方的推理過程。

這兩個軸永遠不會被合併，也永遠不會被重新排序。報告以*每個軸*最嚴重的問題作結，並拒絕跨軸選出單一贏家，因為一個變更可能通過一個軸卻在另一個軸失敗：遵循所有慣例但實作錯東西的程式碼會通過規範、輸在規格；完全按照 [ticket](https://www.aihero.dev/ai-coding-dictionary/ticket) 要求做、卻破壞儲存庫慣例的程式碼則恰好相反。綜合性的裁決會讓通過的軸掩蓋失敗的軸。

## 何時使用

輸入 `/code-review`，或者當你要求審查某個分支、某個 PR、進行中的工作，或任何「從 X 之後」的內容時，代理會自動採用它。

| 你的情境 | 取用 |
| --- | --- |
| 已有 diff，你想知道它是否建置正確*而且*是正確的東西 | `code-review` |
| 你想在 diff 中獵捕 bug——空值路徑、競態條件、差一錯誤 | Claude Code 內建的審查，而不是這個（見下方同名衝突） |
| 什麼都還沒寫，你想用測試優先的方式寫 | [tdd](https://aihero.dev/skills-tdd) |
| 整個規格說明都需要建置，包含審查 | [implement](https://aihero.dev/skills-implement)，它自己會呼叫此技能 |
| 整個代碼庫已經偏移，而不只是一個 diff | [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) |
| 某個東西壞了，你不知道為什麼 | [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) |

你必須提供固定點。如果沒提供，技能會問你，而不是亂猜；然後它會先檢查 ref 可解析、diff 非空，之後才會產生任何東西，因此打錯的分支名稱會在你面前就失敗，而不是在兩個子代理內部失敗。

## 前置條件

規範軸不需要任何東西。它會讀取儲存庫文件的一切（`CODING_STANDARDS.md`、`CONTRIBUTING.md` 等），並在儲存庫什麼都沒寫時回退到內建的基準。

規格軸需要規格說明存在且可被找到。它依下列順序尋找：

1. commit 訊息中的 issue 參照（`#123`、`Closes #45`、GitLab 的 `!67`），透過 `docs/agents/issue-tracker.md` 取得。
2. 你以參數傳入的路徑。
3. `docs/`、`specs/` 或 `.scratch/` 下符合分支或功能名稱的規格檔案。
4. 問你。

第 1 步依賴 [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) 寫出的 `docs/agents/issue-tracker.md`。沒有它，只要你提供路徑，該軸仍能運作。完全沒有規格說明時，規格子代理會被跳過，報告會寫「沒有可用的規格說明」，而不是自行發明需求。

## 兩個軸

| | 規範 | 規格 |
| --- | --- | --- |
| 問題 | 建置得正確嗎？ | 是做對的事情嗎？ |
| 讀取 | 儲存庫記錄的規範，加上壞味道基線 | 原始 issue 或規格說明 |
| 回報 | 有記錄的違規（可能很硬），以及壞味道（永遠是判斷） | 缺失或不完整的需求、範圍蔓延、實作錯誤的需求 |
| 每項發現都引用 | 規範檔案與規則，或具名的壞味道加上該區塊 | 規格說明的行 |

一個不知道你規範的通用審查技能，正是這個設計想避開的東西——它會標出你代碼庫中刻意的部分，卻漏掉你代碼庫真正依賴的不變量。因此，儲存庫自己的文件是規範軸的[主要來源](https://www.aihero.dev/ai-coding-dictionary/primary-source)，而且**儲存庫永遠優先**。

**壞味道基線**是它底下的地板：出自《Refactoring》第 3 章的十二種 Fowler 程式碼壞味道——Mysterious Name、Duplicated Code、Feature Envy、Data Clumps、Primitive Obsession、Repeated Switches、Shotgun Surgery、Divergent Change、Speculative Generality、Message Chains、Middle Man、Refused Bequest。每一種都是帶標籤的啟發式（「possible Feature Envy」），永遠不是硬性違規，每一種都以*它是什麼* → *如何修正* 的方式陳述，因此一項發現會附帶一個動作，而不是一句抱怨。你的 linter 已經強制執行的任何東西，兩個軸都會跳過。

## 常見問題

**它跟 Claude Code 自己的 `/code-review` 衝突。我該怎麼辦？**

這是這個技能被回報最多的問題，而且尚未修復。Claude Code 內建自己的 `/code-review`，做的卻是另一回事——它獵捕 diff 中的 bug，而這個技能檢查規格遵循與儲存庫規範。安裝這個程式庫意味著其中一個會勝出，而哪個勝出取決於你怎麼安裝。透過外掛市場安裝時，一切都以 `mattpocock-skills:` 前綴建立別名，內建的在你輸入未限定名稱時會難以觸及；透過一般的技能安裝，本機檔案會勝出，此技能會遮蔽內建的。一個乾淨的解法是完全移除 Claude Code 內建的技能：能省下大量[上下文](https://www.aihero.dev/ai-coding-dictionary/context)，而且衝突不再重要。遮蔽行為本身可說是 Claude Code [執行環境](https://www.aihero.dev/ai-coding-dictionary/harness)的 bug——技能作者本應可以自由為技能取名——因此另一個解法是改名本機副本。編輯 frontmatter 或重新命名目錄會被 `npx skills update` 還原；使用者回報的持久解法是把技能分叉成新名稱，並從受管集合中移除 `code-review`，同時記下你分叉時的 commit，以便日後手動重新同步。

**它的子代理一直再次呼叫 `/code-review`，產生更多代理。**

已知的未結 bug，多人重現過，而且發生在一個以上的執行環境。規範與規格的提示詞沒有禁止委派，因此子代理可能重新發現此技能並再次向外擴散——有則回報達到 50 多個代理。人們在 fork 上套用的修正是對兩個子代理簡報各追加一行：「不要呼叫 `/code-review` 或產生其他代理——直接執行這次審查。」有些人偏好在一開始就在執行環境層級處理，這樣每個技能都繼承這個防護。兩者都尚未進入發布的技能。如果你無人看管地執行它，請注意代理數量。

**我應該在寫出程式碼的那個[會話](https://www.aihero.dev/ai-coding-dictionary/session)中執行它嗎？**

偏好開新會話。正如一位讀者所說：「同一個上下文自己審查自己不是審查，而是加了 slash 指令的確認偏誤。」撰寫會話中的審查代理持有塑造該程式碼的所有假設，這正是獨立審查者不會有的上下文。這也就是為什麼人們要求 [implement](https://aihero.dev/skills-implement) 時會拿掉它內建的審查步驟——它會在剛寫出 diff 的同一會話內執行審查。從乾淨會話自行呼叫 `/code-review` 才是誠實的版本。

**每個 ticket 之後，還是最後一次？**

兩者都行，而技能不會替你決定。每個 ticket 審查讓每個 diff 夠小，規格軸有明確的規格可以比對，這是 `implement` 使用的模式。批次到分支結尾則能捕捉各 ticket 之間的互動，這是逐 ticket 審查都會漏掉的。如果你不確定，逐 ticket 審查，然後在分支點跑一次最終總檢查。

**我能相信這些發現嗎？**

不檢查就不能。子代理的輸出是假設，不是證據——有個團隊回報，散文式審查放過了十幾項破壞性變更。技能會逐字或略加整理地彙整兩份報告，而不是逐項核對檔案中的每項聲稱，因此一項發現可能引用錯誤位置或誇大影響。在對每項發現採取行動前，先閱讀它的引用來源。每項發現都必須附帶一個引用來源——一則規範規則、一個壞味道加上其區塊，或一行規格說明——正是這個設計讓檢查成為可能。

**為什麼我每次執行都會發現新的問題？**

因為修正會創造新的表面，也因為規範軸的判斷那一半在每次執行之間不是決定性的。一位讀者直白地描述了這個迴圈：「`/code-review` 和 `/improve-code-architecture` 每次都會找到新東西。我實作修正、重新執行這些技能，然後一次又一次。」沒有收斂保證。把一次通過當作一列線索，處理那些背後有引用規則的，然後停手——不要為了等到乾淨而無限循環執行，因為它不會。

**它會審查我未提交的工作嗎？**

不會。它比對 `<fixed-point>...HEAD`，用三個點，這是從合併基點量起的，排除已暫存與工作樹的變更。如果 `implement` 沒有先做過渡性 commit，即將提交的工作對審查是不可見的。先 commit，再審查，然後 amend 或補一個 fixup。

## 這樣就算成功

- 它拒絕在壞的 ref 或空 diff 上開始，而且是在任何子代理產生之前。
- 報告以 `## Standards` 與 `## Spec` 兩塊獨立區塊送達，而不是一份合併清單。
- 每項規範發現都指出你儲存庫某個檔案中的一條規則，或十二種壞味道之一，並引用該區塊；每項規格發現都引用規格說明的一行。
- 結尾摘要給出每個軸最嚴重的問題，並拒絕選出整體贏家。
- 沒有規格說明可用時，規格區塊會直接說明，而不是列出它從程式碼推斷出的需求。

## 它在哪裡適用

`code-review` 是建置鏈尾端的審查步驟——`grill-with-docs → to-spec → to-tickets → implement → code-review`——也能獨立應用於任何你指向的分支或 PR。

- [implement](https://aihero.dev/skills-implement) 是最接近的鄰居：它驅動建置，並在 commit 前呼叫此技能作為自己的收尾審查。
- [to-spec](https://aihero.dev/skills-to-spec) 與 [to-tickets](https://aihero.dev/skills-to-tickets) 產生規格軸比對的文件；模糊的規格說明會讓該軸跟著模糊。
- [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) 是整個代碼庫的對應物——此技能永遠只看一個 diff。

[ask-matt](https://aihero.dev/skills-ask-matt) 會在你拿不定該用哪個技能時，幫你導航整套技能。
