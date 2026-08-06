## 用途

`grill-with-docs` 對你進行關於某個計畫或設計的訪談，直到你與[代理](https://www.aihero.dev/ai-coding-dictionary/agent)對它形成共同理解，並在過程中把詞彙與艱難決策寫進你的儲存庫。它與 [grill-me](https://aihero.dev/skills-grill-me) 執行的是相同的訪談——一輪問題，然後等待，然後下一輪——只是指向某個代碼庫。

它是**[有狀態](https://www.aihero.dev/ai-coding-dictionary/stateful)**的。其他每個 grilling 技能都把[會話](https://www.aihero.dev/ai-coding-dictionary/session)留在你腦中；這個會把檔案留在磁碟上。術語定案後就會寫進 `CONTEXT.md`，在定案的當下，而不是結尾批次處理。決策通過三道閘門後會以 ADR 落地。這就是全部的差異，也是人們對這個技能大多數麻煩的來源：產物是真實儲存庫中的真實檔案，所以當你預期它們出現時它們可能缺席，而當不只一個人在寫它們時它們會漂移。

## 何時使用

你輸入 `/grill-with-docs` 來呼叫它——代理不會自行使用它。

在變更開始時、在某個儲存庫中、當計畫仍模糊、事情的用詞尚未定案時取用它。它是單一會話的工具。你要哪個 grilling 技能取決於眼前有什麼：

| 你有什麼 | 取用 |
| --- | --- |
| 你完全不在工作目錄中 | [grill-me](https://aihero.dev/skills-grill-me) |
| 一個儲存庫，以及一個你能在單一會話定案的變更 | `grill-with-docs` |
| 一個大到無法塞進單一會話的工作——全新專案的建置、一個大型功能 | [wayfinder](https://aihero.dev/skills-wayfinder) |
| 一個完全沒有領域文件的儲存庫，也沒有特定功能在腦中 | `grill-with-docs`，指向儲存庫而非某個變更 |
| 一個卡在別人腦中知識上的決策 | [to-questionnaire](https://aihero.dev/skills-to-questionnaire) |

與 wayfinder 的分野歸結為會話數：單一會話規劃用 `/grill-with-docs`，多會話規劃用 `/wayfinder`。

## 前置條件

技能會寫入你的儲存庫，所以你需要身處一個寫入安全的地方。定案的術語去根目錄的 `CONTEXT.md` 詞彙表——或者，如果根目錄的 `CONTEXT-MAP.md` 把儲存庫標記為多上下文，就去相關上下文的 `CONTEXT.md`。決策去 `docs/adr/`。兩者都是惰性建立；在第一個術語或決策結晶之前什麼都不存在，所以事前沒有什麼要搭的。

它還需要另外兩個技能存在，因為它自己的 `SKILL.md` 只有一行，把工作委派給它們：[grilling](https://aihero.dev/skills-grilling) 提供訪談，[domain-modeling](https://aihero.dev/skills-domain-modeling) 提供撰寫。只安裝 `grill-with-docs` 會得到一個無法運作的技能。

## 文件軌跡

一場會話會產生三樣東西，而且它們並不相等。

| 定案的東西 | 落在哪裡 |
| --- | --- |
| 一個術語——專案自己對某件事的用詞 | `CONTEXT.md`，行內，定案的當下 |
| 一個難以逆轉、沒有情境會令人意外、且是真實取捨的決策 | `docs/adr/` 下的 ADR |
| 你決定的其他一切 | 會話，而且只在那裡 |

第三行就是讓大家措手不及的那一行。`CONTEXT.md` 是詞彙表，而且刻意保持為詞彙表——沒有實作細節、沒有[規格說明](https://www.aihero.dev/ai-coding-dictionary/spec)、沒有隨手筆記。ADR 由三項條件同時把關，所以大多數決策不符合資格，而大多數會話不會產出任何 ADR。一場會話產出更銳利的詞彙表和零個 ADR，這是按設計運作，但它意味著你同意的內容大部分只存在於你同意它的那個[上下文視窗](https://www.aihero.dev/ai-coding-dictionary/context-window)中。把同一次對話交給 [to-spec](https://aihero.dev/skills-to-spec)，而不是[清空](https://www.aihero.dev/ai-coding-dictionary/clearing)它。

詞彙表才是重點。領域語言是這個技能真正在建構的東西——專案自己的用詞，一次議定，這樣你、代理與你的同事就不必再付費重新推導它們。值得說的是，並非所有人都同意這能為你買到代理效能：最銳利的公開反駁是，一個術語與它的平白英文展開，從[模型](https://www.aihero.dev/ai-coding-dictionary/model)得到的結果相同，而詞彙真正壓縮的是共享它的人類之間的溝通。那個觀點仍讓詞彙表有價值；只是把價值移了位。

## 它假定只有一位作者

有狀態的輸出假定由單一人策管。一個在單一儲存庫跑了四個月的兩人開發團隊回報，抽樣合併 PR 中約 20% 出現狀態漂移，ADR 引用與 README 聲稱是漂移最嚴重的表面——刻意、由人工策管的文件比代理記憶漂移得更嚴重。清理過時文件沒有守住；同樣的掃描幾天內又過時了。有效的做法是徹底刪除影子狀態，並在 CI 加入確定性的引用與連結 linter。

相關地：在同一個儲存庫中對不相關的變更重複執行技能，往往會累積混雜主題的文件，因為沒有任何東西把一次會話的輸出與另一次的分開。這兩者目前都尚未在技能中修復。

## 常見問題

**我該用這個還是 `/wayfinder`？**
範圍決定它。任何你能在單一會話定案的事用它；當工作大到塞不進一個會話時用 [wayfinder](https://aihero.dev/skills-wayfinder)，它先把工作繪成決策 [ticket](https://www.aihero.dev/ai-coding-dictionary/ticket) 的地圖。Wayfinder 較慢也較密，而在範圍良好的功能上取用它是最常見的錯誤。它不取代此技能——它可以為地圖中適合的部分落入某個 grilling 會話。

**它跑了，但沒有出現 `CONTEXT.md`，也沒有出現 ADR。**
兩個已知原因。平淡的那個：沒有東西符合資格。ADR 需要三道閘門全過，而一場關於沒有新詞彙的變更的會話，真的沒什麼好寫。真正的 bug：當技能在另一個編排層內部執行——規格驅動開發的包裝、多代理框架、把它當成別人管線中一個步驟呼叫的規則——檔案寫入那一半被回報為默默地不發生，而訪談仍繼續。這已登記且未修復。如果你身處這種設定，先檢查工作目錄，再相信會話的輸出。

**它一次問完所有事情，沒有任何建議，也從未提到 `CONTEXT.md`。**
那是技能未能載入它的兩個相依技能。因為 `SKILL.md` 是一行委派，一個沒有載入 [grilling](https://aihero.dev/skills-grilling) 與 [domain-modeling](https://aihero.dev/skills-domain-modeling) 的代理會去猜 grilling 的意思，你就得到一場無差別的問題傾倒。部分載入是更令人困惑的案例——`grilling` 載入了，`domain-modeling` 沒有——你得到一場好的訪談，卻沒有文件軌跡。它與模型及[投入](https://www.aihero.dev/ai-coding-dictionary/effort)等級相關，而且是此技能被回報最多的問題。如果你懷疑，直接問代理它載入了哪些技能。

**我其他的決策都到哪裡去了？**
只進入會話。這是關於此技能最實質的未結抱怨：詞彙表不是規格說明，大多數回答不值得一份 ADR，也沒有分類帳把每個定案的回答串到規格說明、ticket 與測試。精確的回答——排序保證、負向需求、數值預設——在下游被軟化為較弱的散文，結果可能看起來完整，卻漏掉了你實際決定的東西。目前可用的緩解是保留會話並直接餵給 [to-spec](https://aihero.dev/skills-to-spec)，並以你自己的回答重新對照規格說明，而不是假定它捕捉到了它們。

**我可以把它指向一個完全沒有文件的既有儲存庫嗎？**
可以。對於沒有 ADR、沒有領域語言、沒有設計原則的代碼庫，這正是正確的技能——呼叫它並說「help me document my repo」。社群模式把它與 [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) 配對，用於建立或修復 `CONTEXT.md`。要預期你得引導它：它會讀程式碼並問你它找到的東西，而由你來決定代碼庫中已有的哪些用詞才是正確的。

**會話結束時我該做什麼？**
技能收尾的訊息往往是開放式的，這是已知的粗糙邊緣。在主流程中，答案是在同一次對話裡用 [to-spec](https://aihero.dev/skills-to-spec)。如果變更小到可以立刻建置，改為直接去 [implement](https://aihero.dev/skills-implement)。

**為什麼它叫這個名字？**
沒有人對這個名字滿意。有一個未結建議把它改名為 `grill-domain-model`，這更誠實地描述其行為。這件事沒有進展。如果改名真的落地，文件頁面會跟著動，URL 也會改變。

## 這樣就算成功

- `CONTEXT.md` 在會話*期間*逐詞改變，而不是結尾一次出現一大塊。
- 詞彙表讀起來是純粹的詞彙——專案的用詞加上緊湊的定義——且不含實作細節或類規格的散文。
- 代碼庫能回答的問題會透過讀取代碼庫來回答，而不是問你。
- 你得到很少或零個 ADR，而你得到的那些，都是你重新爭辯時會很煩的決策。
- 它會質疑你使用的某個詞，因為你既有的詞彙表對它有不同定義。

## 它在哪裡適用

`grill-with-docs` 是主建置鏈的起點：

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review
```

它在任何東西被寫成規格說明之前登場——它產出共同理解與定案的詞彙，[to-spec](https://aihero.dev/skills-to-spec) 之後在不重新訪談你的情況下綜合這些。它近旁的鄰居是 [grill-me](https://aihero.dev/skills-grill-me)——沒有儲存庫、沒有檔案的相同訪談——以及它驅動的詞彙表與 ADR 紀律 [domain-modeling](https://aihero.dev/skills-domain-modeling)；兩者都座落在 [grilling](https://aihero.dev/skills-grilling) 原語上。在它上游，[wayfinder](https://aihero.dev/skills-wayfinder) 繪製大到無法塞進單一會話的工作，並可以把地圖的部分交回給它。當你不確定哪個技能或流程適用時，[ask-matt](https://aihero.dev/skills-ask-matt) 會幫你導航。
