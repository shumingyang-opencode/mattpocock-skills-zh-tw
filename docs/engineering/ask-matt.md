## 用途

`ask-matt` 是本儲存庫中所有技能的「路由器」。你描述目前所處的情境——一個無法著手的點子、一堆湧入的 bug 報告、一個已經跑很久的[會話](https://www.aihero.dev/ai-coding-dictionary/session)——它會指出適合的技能或技能順序，以及該順序中人類決策所在的位置。

它只提供建議，然後就此打住。它不會 grill、不會寫[規格說明](https://www.aihero.dev/ai-coding-dictionary/spec)、不會開啟檔案，也不會執行它剛提到的技能；你得到的只是下一步該輸入的內容，而你負責輸入。此外，它是本儲存庫中技能的手寫地圖，而不是掃描你已安裝的內容，因此它不會將你導向你自己或別的作者寫的技能。

## 何時使用

你輸入 `/ask-matt` 來呼叫它——代理不會自行使用它。

| 你的情境 | 路由器給你的回覆 |
| --- | --- |
| 有點子，卻不知從何開始 | 主流程的起點，以及這次建置是否小到可以跳過規格說明 |
| 來自其他人的 bug 與請求 | [triage](https://aihero.dev/skills-triage) 的入口，以及為什麼你自己產生的 [ticket](https://www.aihero.dev/ai-coding-dictionary/ticket) 不屬於它 |
| 兩個看起來可互換的技能 | 兩者之間的界線，而且通常是一個具體的測試，而不是品味問題。[grill-me](https://aihero.dev/skills-grill-me) 或 [grill-with-docs](https://aihero.dev/skills-grill-with-docs) 取決於你是否在某個工作目錄中；[grill-with-docs](https://aihero.dev/skills-grill-with-docs) 或 [wayfinder](https://aihero.dev/skills-wayfinder) 則取決於這項工作是否能在單一會話內完成 |
| 一個長時間的會話，以及關於[上下文](https://www.aihero.dev/ai-coding-dictionary/context)的決定 | 階段邊界上五個選項的排序樹 |
| 一個你已經選好的技能 | 沒有有用的東西。直接呼叫那個技能。 |

## 前置條件

路由器會指出技能名稱；但它不會安裝技能。它指向的所有東西都必須已安裝，建議才有意義，而且它只認識本儲存庫中已推廣的技能。

依賴追蹤器的路線——triage、`to-spec`、`to-tickets`、`implement`——假設 [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) 已經在儲存庫中設定好 issue 追蹤器。路由器在完成之前也會毫不猶豫地推薦它們。

## 是流程，不是技能

這個技能給你思考的關鍵字是**流程**：一條*穿過*技能的路徑，而不是單一技能。描述你的情境會把你在某一步放入某條流程，這跟「這就是符合你關鍵字的技能」是不一樣的答案。一共有四種路線，而技能本身完整地承載它們：

- **主流程**，從點子到交付。Grill、規格說明、ticket、實作、審查，內部還有兩個分支：當某個問題需要可執行的程式碼才能定案時，走原型繞道；以及規格說明與 ticket 的分流，只有在建置橫跨多個會話時，這個分流才值得它的成本。
- **入口**，適用於會產生工作、然後匯入主流程的情境：湧入的 bug 報告、某個壞掉的東西，或是一項太模糊、太大而無法塞進單一會話的工作。
- **獨立技能**，脫離所有流程，依自身條件被取用——原型、問卷，或你正身陷其中的合併衝突。
- **底層的詞彙層**，當問題在於用詞而非流程時，其他技能會引入的兩份參考。

## 階段邊界

它交給你的另一個概念是**階段邊界**。階段是會話內的一段工作——[grilling](https://www.aihero.dev/ai-coding-dictionary/grilling)、實作、QA——而兩個階段之間的邊界，是「我該拿這段上下文怎麼辦？」這個問題唯一該出現的地方。在階段中沒有什麼好決定的：繼續，或把剩下的工作拆分給[子代理](https://www.aihero.dev/ai-coding-dictionary/subagent)。

| 選項 | 什麼時候用 |
| --- | --- |
| **繼續** | 下一個階段需要原樣保留此階段，或者你還有[智慧區](https://www.aihero.dev/ai-coding-dictionary/smart-zone)可用。它是唯一能讓會話保持為[主要來源](https://www.aihero.dev/ai-coding-dictionary/primary-source)的動作，所以先把它排除 |
| **`/clear`** | 你身後的一切都是可拋棄的。這是棋盤上最便宜的動作，但如果你錯了就無法回頭 |
| **[handoff](https://aihero.dev/skills-handoff)** | 有些東西必須被攜帶：新的[執行環境](https://www.aihero.dev/ai-coding-dictionary/harness)、新目錄、同事、階段中途分岔出去的旁支任務 |
| **子代理** | 任務的範圍夠小，可以在你[離開鍵盤](https://www.aihero.dev/ai-coding-dictionary/afk)時執行 |
| **`/compact`** | 以上皆非。它是預設選項，而且常常落在此處 |

其中兩個常被誤用，這就是為什麼路由器承載的是順序而非清單。`/handoff` 讀起來像是窗口之間通用的橋樑，但其實不是：它買到的一切就是可攜性。`/compact` 是樹的底部，而不是第一個伸手可及的選項，因為它上面的四個問題各自更便宜或更精確。

## 常見問題

**難道不就是一份按正確順序排列的技能清單嗎？**

人們一直要求在 README 中放這樣一份清單。這個技能就是那份清單——這就是它存在的目的。一張靜態表格會寫出 `wayfinder → to-spec → to-tickets → implement → code-review`，而且在大多數情況下都會是錯的，因為有趣的地方在於分支——有沒有代碼庫？建置是否橫跨多個會話？這個問題能不能靠對話解決？誠實的成本在於路由器是手工維護的，會落後於儲存庫。`/grilling` 和 `/resolving-merge-conflicts` 早在路由器提到它們之前很久就已發布。

**它跟我說有一半的技能沒安裝。**

這是已知的 bug，尚未修復。路由器引導你經過的大多數技能都設定了 `disable-model-invocation: true`，這意味著執行環境會把它們從注入代理上下文的技能清單中移除。代理把那份清單視為完整清單，於是回報它們缺失。有一則回報的會話中，它宣稱整個規格說明與 ticket 流程不存在，並重新導向到光禿禿的 `/grilling` 和 `/tdd`。這個外掛的二十二個技能中有十三個帶有此旗標，所以這是常見情況，而非邊緣案例。它們其實有安裝。還是輸入 slash 指令吧，或者檢查 `.claude-plugin/plugin.json`，那才是判斷內容存在的權威來源。

**它描述了一個技能的行為，但那個技能並不會那樣做。**

同樣屬實，也同樣未修復。路由器是根據自己對每個技能的一行摘要來回答，而不是根據技能本身。一則詳盡的回報追蹤了單一會話中的三個案例，包括一個僅憑「把對話變成規格說明」這句註解就建議跳過 [to-spec](https://aihero.dev/skills-to-spec) 的例子——`to-spec/SKILL.md` 從未被打開。在每個案例中，它都只在使用者質疑後才去驗證，而且從未主動驗證。在那裡跳過 `to-spec` 損失了一次真實的接縫檢查，而產出的 ticket 也低估了工作量。當路由器對另一個技能做出承載性的斷言時，先要求它打開那份 `SKILL.md`。這同樣適用於地圖完全沒涵蓋的問題，例如是否要使用[計畫模式](https://www.aihero.dev/ai-coding-dictionary/agent-mode)：那個答案來自[模型](https://www.aihero.dev/ai-coding-dictionary/model)的推論，而不是寫在這裡的內容。

**為什麼它是散文而不是編號清單？**

這是合理的抱怨，已被登記為未結 issue，主張大部分的路由都是確定性的，而敘事體讓人難以快速瀏覽。沒人阻止你要求壓縮形式——「直接給我順序」就能得到順序。散文承載的是條件那一半：分支、預期人類決策的地方，以及步驟之間該在哪裡 clear 或 compact。一份扁平的清單恰恰會丟掉這些。

**它能不能導航到我自己或別的作者寫的技能？**

不能。有三份不同的提案要求路由器讀取你的本機 `skills/` 目錄，並從已安裝的內容推薦。`ask-matt` 不是那樣的東西。它是一組技能的對映，靠手工維護，而且對你撰寫或從他處安裝的技能一無所知。

**它叫我編輯 SKILL.md。**

這個建議常常是對的，但很少能持久。有人問它如何讓 [implement](https://aihero.dev/skills-implement) 關閉 ticket，得到的建議是在技能中加一行，但他立刻發現問題：`npx skills update` 會覆寫檔案，而且外掛安裝是唯讀的。把常駐行為寫進你自己的 `CLAUDE.md` 或 `AGENTS.md`，或者在呼叫時說明。提示詞層級的調整可以撐過更新——把流程指向 Linear 而不是 GitHub，或問它哪些未結 ticket 可以平行執行，都是人們這樣做的事。

**它提到一個我沒有的技能，或漏掉一個我有的技能。**

在假定它消失之前，先到變更日誌看看是否有改名。`writing-great-skills` 改名為 [writing-for-agents](https://aihero.dev/skills-writing-for-agents) 且沒有別名，`to-prd` 改名為 [to-spec](https://aihero.dev/skills-to-spec)，`pathfinder` 改名為 [wayfinder](https://aihero.dev/skills-wayfinder)。有四個技能被直接退役，併入吸收它們的技能：`ubiquitous-language`、`design-an-interface`、`qa` 和 `request-refactor-plan`。反向的案例就是上面提到的路由器自身落後問題。

## 這樣就算成功

- 它最後指出要輸入的內容並就此打住，而不是自己開始工作。
- 它給回的路線會提到在哪裡 clear 或 compact 上下文、哪裡需要你審查，而不只是一份技能名稱清單。
- 當兩個技能相近時，它會指出該用哪一個，以及為什麼另一個不適合你。
- 它對另一個技能行為所做的任何斷言，都會在追蹤紀錄中顯示為它讀取了該技能的 `SKILL.md`。
- 它在回覆中呈現的是你自己的情境，而不是最接近的通用情境。

## 它在哪裡適用

`ask-matt` 是一個**獨立路由器**，位於整套技能之上。它永遠不是某條鏈中的一個步驟；它指向每一條鏈，而且是其他文件頁面連結回來的節點，這樣它們就不用重畫這張圖。從這裡，你最常會落到 [grill-with-docs](https://aihero.dev/skills-grill-with-docs)——主流程的起點，或 [triage](https://aihero.dev/skills-triage)——外來工作（而非你主動開始的工作）的入口。

相對於它所描述的技能，它是[次要來源](https://www.aihero.dev/ai-coding-dictionary/secondary-source)。當路由器與 `SKILL.md` 意見不一致時，以 `SKILL.md` 為準。
