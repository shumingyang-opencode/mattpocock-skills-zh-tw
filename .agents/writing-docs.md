# 撰寫 docs 頁面

`engineering/` 與 `productivity/` 中的每個技能，都有位於 `docs/<bucket>/<skill-name>.md` 的**給人看的 docs 頁** — docs 樹鏡像 `skills/` 下的這兩個 bucket 資料夾。它發布在 `https://aihero.dev/skills-<skill-name>`；URL 一律是 `skills-<skill-name>`，與 bucket 無關，所以 docs 路徑只是 repo 的組織方式。頁面不是技能本身，也不是 `SKILL.md` 的副本。只有這兩個 bucket 是已推廣的；其餘（`misc/`、`in-progress/`、`deprecated/`）不發布 docs 頁。

這些技能多數是 **user-invoked**：代理永遠不會替你觸發它們，所以*你*是那個必須記得它們存在、以及何時使用的索引。這份記憶就是**認知負擔**。docs 頁的工作就是減輕它 — 讓一位讀者圍繞一個技能找到方向，使他們能把技能放在腦中、知道何時使用、並看出它在系統中的位置。這些頁面集體是一個分散式路由器；每個頁面都是一個節點。

每當已推廣技能被新增、改名或行為被改變時就動手：建立或重新同步它的 docs 頁。改名也會移動檔案（`docs/<bucket>/<old>.md` → `docs/<bucket>/<new>.md`），因為發布的 URL 追蹤名稱；在 `engineering/` 與 `productivity/` 之間移動的技能，其 docs 檔案也移到對應資料夾。`misc/`、`in-progress/`、`deprecated/` 中的技能沒有頁面 — 這些 bucket 沒有一個是已推廣的。從其中之一移*出*進入 `engineering/` 或 `productivity/` 的技能獲得頁面；反向移動則失去頁面。

因為這些頁面發布在 `aihero.dev` 上，**每個連結都是絕對路徑** — 絕不用 repo 相對路徑。連到其他技能的連結指向 `https://aihero.dev/skills-<name>`；連進 repo 的連結指向完整的 `https://github.com/mattpocock/skills/...` URL。在 repo 中可用的相對連結，發布後就會壞掉。

沒有 H1 — 發布的頁面從 slug 取標題。

## 頁面結構

填入下列模板，保持其順序。**固定框架**（`## What it does`、`## When to reach for it`、`## Where it fits`）出現在每個頁面。`## Prerequisites` 與自由形式的實質章節只承載這個特定技能需要的東西；其餘刪除。

四個章節讓頁面值得一讀：`What it does`、`When to reach for it`、`Common questions`、`It's working if`。前兩個幫讀者定位；後兩個是頁面停止摘要技能、開始回答讀者自身處境的地方。後兩者各有要跨越的門檻，如下 — 但把兩者皆未跨越的頁面視為未完成，而非「短而完整」。

**頁面不帶安裝指令。** ai-hero 的頁面模板自己會渲染安裝 widget — 一個複製按鈕、單一技能指令、整組指令與更新行 — 在正文上方。頁面若再寫一遍，讀者會看到同一指令兩次，且兩份複製會漂移：每個頁面上手寫的那對，對照身旁的 widget 逐漸過時。安裝措辭是網站的屬性，不是頁面的。需要改時，在 ai-hero 改；標準措辭位於[安裝區塊](./install-block.md)。

<page-template>

## What it does

一兩段淺白語言。以技能的一句工作開頭，然後說明**定義性約束（defining constraint）** — 讓此技能與顯而易見的預設行為不同的單一事實（對 `to-spec` 而言：它不再訪談使用者，而是綜合已知的東西）。把它寫成樸素的直述句 — 絕不要用「The defining constraint:」或「The key thing:」這類帶標籤的旁白；那種公式讀起來像填充。這行是頁面上最有價值的；絕不省略。

## When to reach for it

何時以及如何觸發技能 — 兩個節拍，兩者實際上永遠存在：

- **觸發模式（Invocation mode）**。說明是你輸入它還是代理觸發它。user-invoked 技能：「你輸入 `/<name>` 觸發 — 代理不會自己伸手。」model-invoked 技能：「輸入 `/<name>`，或當任務符合時由代理自動觸發。」
- **觸發邊界（Trigger boundary）**。索引項目：「當……時使用」。技能與兄弟技能易混淆的地方，加上另一半 —「要 <X> 請改用 [<sibling>](https://aihero.dev/skills-<sibling>)。」

## Prerequisites

可選 — 僅當技能需要某些東西就位才能運作時才包含；否則整個省略此標題。涵蓋：它**寫入的工作區**（`grill-with-docs` 這類有狀態技能寫 `CONTEXT.md` 與 ADR；`teach` 會建立整個目錄 — 說清楚它寫什麼、寫在哪）、**先前的設定**（`triage`/`to-spec`/`to-tickets` 需要 `setup-matt-pocock-skills` 已設定 issue tracker）、或 **repo 特定工具**。在何處都能跑的無狀態技能沒有前置需求 — 省略該章節。

## <free-form middle>

一到三個短章節，用技能*自己的詞彙*，讓它豁然開朗 — 選擇適合該技能的標題：它執行的迴圈、它產生的產物、它做出的分叉、它消滅的那個反模式。沒有規定的標題；技能太異質，無法用一個標題涵蓋。

唯一不可妥協的是：**浮現技能的領頭詞 / 定義性想法** — `tight`（緊密的）回饋迴圈、`deep module`（深模組）、一次性程式碼回答一個問題、red-green（紅-綠）。它有雙重回報：讀者學會技能*是什麼*，也學會他們日後用來*觸發*它的那個字。

## Common questions

讀者真的會問這個技能的問題，每個問題粗體、答案在下方幾行 — 不用子標題。

觀察到的問題永遠勝過發明的問題，所以撰寫前先去把它們找出來：

- **Wiki**。若這台機器上存在 `~/repos/matt/personal-wiki`，它就是最豐富的來源。它的 `wiki/audience/` 區域圍繞讀者想要什麼、討論什麼、**被什麼搞糊塗**而組織 — 先讀 `wiki/index.md` 取得頁面註冊表，再讀與此技能相關的頁面。每個頁面都帶有指向原始 X、Discord、GitHub 與 email 討論串的 `sources:` 回鏈；wiki 是次要來源，所以要引用提問者自己的問題，而不是 wiki 對它的摘要。目錄不存在時略過此項。
- **此 repo 的 issues**。`gh issue list --repo mattpocock/skills --search "<skill-name>" --state all`。被提出兩次以上的問題，就是頁面欠它一個答案的問題。
- **`CHANGELOG.md`**。任何被改名、移動或行為改變的東西，都會產生「它跑去哪了？」的問題，頁面必須回答。

搜尋結果稀疏時，章節也可以放讀者明顯會問的問題 — 但**數量要對證據誠實**。被充分討論的技能賺到六題；冷門的賺一到兩題，或完全沒有。把單薄技能灌到和豐富技能一樣多，就是章節被沒人問過的問題塞滿的方式，而發明的問題教不了讀者任何東西。

按出現頻率排序，最尖銳的在前，而且該說不討喜的事實就說 — 一場非常冗長的詰問 session 通常代表範圍太大；被叫去寫自己的技能的模型會產出囉嗦的東西。沒有值得回答的內容時省略此標題。

## It's working if

幾條項目符號，說明技能發揮作用時讀者會看到什麼。每一條的門檻是讀者不需要打開 `SKILL.md` 就能檢查 — 是讀者自己工作中的訊號，或眼前 trace 中的訊號。「文件越好就越短」通過；「library 區段與 `template.sh` 位元組一致」是用本節名稱偽裝的、對技能內部的合規檢查。微兆明確的地方就包含它；保持含糊時省略此標題。

## Where it fits

永遠存在。用一兩句話把技能放進系統：

- **角色（Role）**。為它命名：**鏈上步驟（chain step）**（`grill-with-docs → to-spec → to-tickets → implement → code-review`）、**一次性的設定（run-once setup）**（`setup-matt-pocock-skills`）、**定期維護（periodic maintenance）**（`improve-codebase-architecture`，「每隔幾天」）、或**隨時取用的獨立技能（reach-for-it-anytime standalone）**（`diagnosing-bugs`、`prototype`、`handoff`）。獨立技能的地圖就是一句誠實的話 — 遠勝過省略此章節。
- **鄰居（Neighbours）**。相關的一兩個兄弟技能，各附一個 because 子句，用絕對路徑連結。
- **地圖（The map）**。指向 [ask-matt](https://aihero.dev/skills-ask-matt)、整個集合的路由器，讓這個頁面保持為節點，永遠不必重畫圖。

</page-template>

## 慣例

- 解釋**為什麼**，而不是流程。頁面定位並安置技能；它絕不重現 `SKILL.md` 的步驟或模板傾印 — 選擇工具的人不需要 runbook。
- **絕不提作者姓名。** 頁面是技術文件，不是誰說了什麼的紀錄。「Matt says」、「Matt's own answer」、「his position is」、引用的回覆 — 全部去掉。從問題搜尋中發現的發現值得保留；它的出處不值得。把實質內容陳述成關於技能的樸素主張（「修法是直接指示：……」，「區分歸結為 session 數量」），並丟掉框架。讀者是在決定要不要用一個工具；意見無論如何都有一樣的分量，而帶出處的意見一旦立場移動就過時。引用*使用者*則沒問題 —「有位使用者回報……」是關於技能在真實世界的證據，而且保持匿名。
- 使用技能的**領頭詞**（`seam`（接縫）、`deep module`（深模組）、`tracer bullet`（曳光彈）），讓頁面與技能說同一種語言。
- **AI Coding Dictionary 有術語時使用該術語，並在頁面上連結它的首次出現。** 字典是 AI 程式設計的家用詞彙 — `context window`、`subagent`、`harness`、`primary source`、`agent mode`。用它定義的字，勝過你發明的同義詞。每個術語的首次出現連結到 `https://www.aihero.dev/ai-coding-dictionary/<slug>`（slug 是術語轉小寫、非字母數字以連字號取代：`context window` → `context-window`），之後的出現全部不連結。只有當該字承載字典的意義時才連結 — 領域*模型*、背景*上下文*或驗證*token* 是不同的字，只是碰巧相同。絕不在標題、code span 或既有連結內連結，也絕不連結本 repo 中指名某技能而非概念的字。完整的術語清單，若此機器存在 `~/repos/ai/ai-coding-dictionary/dictionary/` 就讀它 — 每個術語一個檔案，檔名*就是*術語 — 否則讀 [mattpocock/dictionary-of-ai-coding](https://github.com/mattpocock/dictionary-of-ai-coding)，無論如何它都是真相來源。
- **分支放表格或清單，絕不放段落。** 頁面呈現選擇時 — 技能能產生的兩種產物、觸發它的四種處境、邊界上的五個選項 — 讀者是在掃描符合自己處境的那一行。段落迫使他們全部讀完才找到。簡短的 markdown 表格（條件在左欄，怎麼做在右欄）或項目符號清單一眼就還給它。這適用於分支出現的每個地方，最常在 `## When to reach for it` 與自由形式中間。
- 讓頁面本身保持低負擔。它是關於低認知負擔技能的文件；傢俱（多餘的標題、重述的連結）正是它在對抗的東西。

## 完成條件

- 頁面存在於 `docs/<bucket>/<name>.md`，且改名或 bucket 移動後沒有過時頁面存活。
- 頁面不帶來源連結，也不寫自己的安裝指令。
- `## What it does` 以樸素散文陳述定義性約束，而非帶標籤的旁白。
- 頁面不提作者、不引用作者 — 每個主張都自行成立。
- `## When to reach for it` 陳述觸發模式與觸發邊界。
- `## Where it fits` 指名角色並連結到 `ask-matt`。
- 有前置需求（工作區、先前設定、工具）就陳述，沒有就省略該章節。
- 中間浮現領頭詞。
- 頁面使用的每個 AI Coding Dictionary 術語都按字典拼法，且其首次出現 — 且僅首次出現 — 連結到字典條目。
- 每個多路分支都是表格或清單，不是要讀者全文讀完的段落。
- 真實問題的搜尋確實執行了 — wiki、issues、changelog — 而 `## Common questions` 依搜尋結果定尺寸，而非灌水去匹配較豐富技能的頁面。
- 每個 `## It's working if` 項目符號都不需要打開 `SKILL.md` 就能檢查。
- 章節依模板順序出現。
- 每個連結都是絕對路徑，且每個都能解析。
