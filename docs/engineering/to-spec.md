## 用途

`to-spec` 把你剛才的對話變成一份**[規格說明](https://www.aihero.dev/ai-coding-dictionary/spec)**，並以單一 issue 發布到你的 issue 追蹤器。

它不會訪談你。當你取用它時，決策早已完成，所以它綜合已知的內容——來自對話、來自代碼庫、來自你的 `CONTEXT.md` 與 ADR——而不是開啟新一輪問題。規格說明是已作決策的紀錄，不是做出新決策的地方。

## 何時使用

你輸入 `/to-spec` 來呼叫它——[代理](https://www.aihero.dev/ai-coding-dictionary/agent)不會自行使用它。

當建置大到單一代理[會話](https://www.aihero.dev/ai-coding-dictionary/session)裝不下、且必須在拆分到多個會話中存活時取用它。這就是全部的觸發條件：

| 你在哪裡 | 跑什麼 |
| --- | --- |
| 你還沒有決定任何事情 | 先 [grill-with-docs](https://aihero.dev/skills-grill-with-docs) |
| 已決定，且工作裝得進一個[上下文視窗](https://www.aihero.dev/ai-coding-dictionary/context-window) | [implement](https://aihero.dev/skills-implement)——跳過規格說明 |
| 已決定，且工作橫跨多個會話 | `/to-spec`，然後 [to-tickets](https://aihero.dev/skills-to-tickets) |
| [wayfinder](https://aihero.dev/skills-wayfinder) 地圖已清空 | `/to-spec #<map_issue>` |

## 前置條件

`to-spec` 以 issue 發布規格說明，所以 [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) 必須先為此儲存庫設定追蹤器與分診標籤詞彙。任一類型都行：像 GitHub 這樣真實的追蹤器，或 `.scratch/` 下的本機 markdown 檔案，後者開箱即受支援。

## 規格說明是決策紀錄

規格說明存在，是因為上下文視窗會結束。你在 [grilling](https://www.aihero.dev/ai-coding-dictionary/grilling) 期間定案的一切——解決方案的形狀、你辯論過的選擇、你刻意拒絕的——都在一場即將被清空的對話中。規格說明就是在清空中存活的東西。

所以它不驗證任何東西，也不決定任何東西。它以你專案自己的詞彙捕捉已被決定的內容，讓全新會話可以在你不重新解釋的情況下接手工作。規格說明斷言了你從未真正說過的任何東西，都是缺陷。

## 先接縫，後散文

在寫出任何一個字之前，`to-spec` 會勾勒功能將被測試的**接縫**，並與你確認。它偏好已存在的接縫勝過新接縫，並取它所能取的最高接縫——一個變更的理想數目是一。

那些約定的接縫接著會旅行。[tdd](https://aihero.dev/skills-tdd) 只在預先約定的接縫工作，而 [code-review](https://aihero.dev/skills-code-review) 對照規格說明審查 diff，所以沒人約定的接縫會以審查發現的形式出現。約束是間接的——它透過這份文件運作——這正是為什麼接縫對話值得在這裡被認真對待，而不是把它延後到實作。

## 常見問題

**`/to-prd` 去哪裡了？**
它就是這個技能，在 v1.1 改名。「Spec」現在是唯一的貫穿術語，而舊的 `to-prd` slug 已死——以新名稱重新安裝。取代舊詞彙的配對是 *spec* 與 *tickets*：規格說明是目的地與固定它的決策，[ticket](https://www.aihero.dev/ai-coding-dictionary/ticket) 是抵達那裡的執行步驟。如果你轉向，刪除未完成的 ticket，保留規格說明。

**為什麼規格說明會拿到 `ready-for-agent` 標籤？我不想要代理據它實作。**
這個標籤的意思是「no further triage needed」——文件完整到代理足以據以工作。它是輸入的指定，不是工作指令。但如果你執行輪詢 `ready-for-agent` 的 [AFK](https://www.aihero.dev/ai-coding-dictionary/afk) 代理，那個區別對它們不可見，它們會樂意在一次執行中嘗試建置整個規格說明，而不是接起 ticket 切片。這是此技能被回報最多的粗糙邊緣。在它改變之前，在你的 AFK 代理提示詞中明確排除父規格說明，或在 `/to-tickets` 跑完後拔掉標籤。

**為什麼不從 grilling 直接去 `/to-tickets`，跳過規格說明？**
常常你應該——規格說明只在多會話工作上才值得它那一步。它划得來的地方在於 ticket 是可拋棄的，而規格說明不是：每個 ticket 為一個全新上下文視窗定尺寸並被刪除或關閉，而規格說明作為它們背後推理所在的唯一地方留存。在單一會話的變更上，這不為你買到任何東西，而且你付了一個額外的綜合步驟，[模型](https://www.aihero.dev/ai-coding-dictionary/model)可能在那裡漂移。走 grilling → `/implement`。

**我剛完成 wayfinder 地圖。我該餵給它什麼？**
主地圖 issue——`/to-spec #<map_issue>`，而不是個別的決策 ticket。[wayfinder](https://aihero.dev/skills-wayfinder) 產出的是決策而不是交付物，散落在整張地圖上；`to-spec` 是把它們摺疊成一份可建置文件的步驟。把地圖直接迴圈進 `/implement` 會丟掉那次摺疊。

**規格說明是給我看的，還是只給代理？**
大部分是給代理的，而它讀起來也是那樣——完整、密集、引用繁重。值得你眼睛的部分是接縫與超出範圍區段，因為那是兩個「錯誤決策最容易捕捉、也最昂貴發現」的地方。從頭到尾讀整份是大家真實的抱怨，而且沒有摘要模式：誠實的答案是，如果規格說明讓你意外，那是 grilling 太淺，而不是規格說明太長。

**ticket 開始之後，我要讓規格說明保持凍結，還是讓代理重寫它？**
沒有東西讓它保持同步，所以實際上它是一個「你當下所知」的快照，而實作第一次教會你某件事時它就過時了。工作交付後把它當成一次性。注定要活得比它久的是你的 `CONTEXT.md` 與 ADR——如果實作期間學到的東西值得留存，它屬於那裡，而不是一份被編輯的規格說明。

**我的工作是重構或模組邊界，不是功能。模板合適嗎？**
比較不好，而這是已知的限制。模板強烈倚賴使用者故事，這對架構工作來說是錯誤的形狀——你最後會圍繞著其實關於介面與不變量的決策，寫出沒人要求的故事。改為倚賴實作決策與測試決策區段，並讓持久的架構裁決以 ADR 形式透過 [grill-with-docs](https://aihero.dev/skills-grill-with-docs) 落地，而不是試著讓規格說明承載它們。

**它會檢查追蹤器中相關的工作，或引用它尊重的 ADR 嗎？**
兩者都說不。它讀取並尊重涵蓋它觸及區域的 ADR，但它不連結它們，也不在草擬前搜尋追蹤器中重疊的 issue——所以規格說明可能默默重複某人已提出的工作。如果那個區域很熱鬧，先自己搜尋追蹤器。

**`/to-tickets` 讀不了我的規格說明——它一直截斷。**
非常大的規格說明可能超出追蹤器 issue 能乾淨回送的範圍，而且沒有本機副本可回退。修正是上下文衛生：不要在 `/to-spec` 與 `/to-tickets` 之間 [clear](https://www.aihero.dev/ai-coding-dictionary/clearing) 或 [compact](https://www.aihero.dev/ai-coding-dictionary/compaction)。在同一個視窗跑它們，規格說明就完全不需要被重新取得。

## 這樣就算成功

- 它開始寫，而不是問你一輪新問題。
- 它在寫之前把接縫交給你看，並提議盡可能少的接縫。
- 它以你專案的名詞回來，而不是泛泛的產品管理套版文字。
- 其中每個決策都是你記得自己做過的。沒有為了填滿區段而發明的東西。
- 超出範圍區段有真實的東西——你拒絕的東西通常是頁面上最有用的幾行。

## 它在哪裡適用

`to-spec` 是主建置鏈中的一個步驟，而且只在它的多會話分支上：

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review
```

它上游的鄰居是 [grill-with-docs](https://aihero.dev/skills-grill-with-docs)——做此技能只記錄的決策——以及 [wayfinder](https://aihero.dev/skills-wayfinder)，其完成的地圖正是在這裡匯入鏈中。下游，[to-tickets](https://aihero.dev/skills-to-tickets) 把規格說明切成曳光彈 ticket 供 [implement](https://aihero.dev/skills-implement) 建置。當你不確定哪個技能或流程適用時，[ask-matt](https://aihero.dev/skills-ask-matt) 會幫你導航。
