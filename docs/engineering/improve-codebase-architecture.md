## 用途

`improve-codebase-architecture` 調查代碼庫找出**加深機會**——淺模組（介面幾乎與它隱藏的東西一樣複雜）能變成深模組的地方——把它們寫成一份自成一體的 HTML 報告，然後針對你挑選的那一個對你進行 [grilling](https://www.aihero.dev/ai-coding-dictionary/grilling)。

它從不改變程式碼。整個執行只在你的作業系統暫存目錄中產出一份 HTML 檔案與一場對話；重構本身發生在稍後、在分開的[會話](https://www.aihero.dev/ai-coding-dictionary/session)中，透過正常的建置流程。這正是它作為調查而非重構工具的原因，也是這個技能值得在一個你還沒準備好動手的代碼庫上執行的原因。

兩個篩選器讓報告不會變成泛泛的清理建議。每個候選者都必須通過**刪除測試**——移除這個模組會把複雜度集中在較小的介面背後，還是只是把它分散到呼叫方身上？只有「集中」的案例才能獲得一張卡片。而且除非你把它指向特定區域，否則它會先讀取近期的 commit 歷史，把掃描偏向正在積極變更的路徑，理由是：在沒人碰的程式碼上做加深，是一次你永遠不會兌現的重構。

## 何時使用

你輸入 `/improve-codebase-architecture` 來呼叫它——[代理](https://www.aihero.dev/ai-coding-dictionary/agent)不會自行使用它。

它位在建置迴圈之外——它不是主迴圈中的一個步驟，而是你定期執行、為改善代碼庫排隊更多工作的東西。它會被用在四種情境：

| 情境 | 使用方式 |
| --- | --- |
| 例行維護 | 每隔幾天跑一次，或只要有空檔就跑，阻止結構在功能之間腐爛。 |
| 大型建置前 | 把它指向[規格說明](https://www.aihero.dev/ai-coding-dictionary/spec)：「how can we make this change easy?」這對它是最有效的提示詞。 |
| 既有代碼庫稽核 | 在大型、無結構或 [vibe-coded](https://www.aihero.dev/ai-coding-dictionary/vibe-coding) 的儲存庫上執行，找出它實際上處於什麼形狀。 |
| 遺留測試工作 | 在對不可測試的程式碼寫測試之前，先用它找出缺失的接縫。 |

它與兄弟技能容易混淆的地方：

- 要設計一個你已經選好的模組，用 [codebase-design](https://aihero.dev/skills-codebase-design)——那是長凳，這是找出該放什麼上去的調查。
- 對一個大到塞不進單一會話的整個工作，用 [wayfinder](https://aihero.dev/skills-wayfinder)。
- 對「這個特定東西壞了」，用 [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs)。當真正的發現是沒有好的接縫能鎖住 bug 時，它會交回這裡。

## 前置條件

執行它不需要任何前置。它會讀取 `CONTEXT.md` 與 `docs/adr/` 中任何存在的 ADR，並在存在時用你領域自己的名詞說話——候選者讀起來是「加深 Order intake 模組」，而不是「重構 FooBarHandler」。

它寫入兩個地方。報告去 `<tmpdir>/architecture-review-<timestamp>.html`，在儲存庫之外。在 grilling 迴圈中，它會在 `CONTEXT.md` 加入或磨利術語，若檔案不存在則建立它，並提議把被否決的候選者記錄為 ADR，這樣未來的執行不會再建議它。

## 深度，以及獵捕它的報告

這個技能靠一個概念運轉：**深度**。深模組把小而穩定的介面背後放進大量行為。淺模組讓實作透過幾乎與底下程式碼一樣寬的介面洩漏。報告是對淺薄的獵捕——純粹為了可測試性而抽取、真實 bug 卻活在呼叫方式中的純函式（沒有**局部性**）、跨越**接縫**洩漏的模組、一個不打開五個檔案就無法理解的概念——以及修復它的加深提案。

每個候選者都是一張卡片：涉及的檔案、摩擦點、平白英文的解決方案、以**局部性**與**槓桿收益**陳述的效益、前後對照圖，以及一個強度徽章。

| 徽章 | 對你的意義 |
| --- | --- |
| `Strong` | 刪除測試清楚通過，且摩擦點真實存在。認真對待這些。 |
| `Worth exploring` | 合理的加深，但報酬取決於程式碼接下來要去哪裡。 |
| `Speculative` | 為了完整性而浮現。這些大多可以安全忽略。 |

報告以**首要建議**作結——它會先處理的那一個——然後技能停下來，問你想探索哪個候選者。那時還沒有任何東西被決定，也沒有任何程式碼被移動。

## 你挑一個之後會發生什麼

挑選一個候選者會對它啟動 [grilling](https://aihero.dev/skills-grilling) 會話：約束、接縫背後是什麼、哪些測試存活、加深後的介面應該長什麼樣。那場會話的輸出是決策，不是 diff。從那裡適用正常流程——把決策帶進 [to-spec](https://aihero.dev/skills-to-spec)，然後 [to-tickets](https://aihero.dev/skills-to-tickets)，然後 [implement](https://aihero.dev/skills-implement)。

## 常見問題

**它對一個想法 grill 了我一個小時，而不是給我看選項。我能關掉它嗎？**

可以——呼叫時說出來（「don't grill me, just show the report」）。這是這個技能最大的抱怨。有位使用者說得很直接：他喜歡它作為「一種取得全面改進分析的便利方式」，而在 grilling 迴圈被加入後，覺得它「borderline unusable」，回報了它提出單一方案然後問「10's or 100's of questions」的會話。設計意圖是報告先來，grill 只在你挑選的候選者上開始，但較弱的[模型](https://www.aihero.dev/ai-coding-dictionary/model)直接跳去訪談它們想到的第一個想法。那串討論中的回報因模型而差異巨大，而這是未結 issue——技能還沒有有文件記載的 no-grill 模式。

**報告以沒有樣式的原始 HTML 開啟，沒有圖。發生什麼事了？**

報告從 CDN 載入 Tailwind 與 Mermaid，所以你在打開它時需要網路存取，而當有東西阻擋那些腳本時，它會無聲地壞掉。已登記的案例是某個資安掛鉤要求 SRI hash：代理加入了它們，CDN 送給瀏覽器的位元組與送給用來計算 hash 的 `curl` 不同，瀏覽器就阻擋了腳本。離線與封閉環境也會撞到同一堵牆。代理看不到這件事，因為它從不渲染頁面。變通法是要求行內 CSS 與手工打造的 SVG 圖，而不是 CDN 支架。這是未結 issue，也是真實的粗糙邊緣。

**它給了我十二個候選者。我要在同一個會話處理它們，還是開新的？**

一個會話一個候選者。在一次對話中處理好幾個，會把報告、grilling、領域模型編輯與程式碼變更同時塞滿[上下文視窗](https://www.aihero.dev/ai-coding-dictionary/context-window)。報告只活在暫存檔案中，所以攜帶候選者本身，而不是檔案：挑一個、grill 它、把決策帶進 `/to-spec`，並把其餘的變成你之後可以獨立接手的 [ticket](https://www.aihero.dev/ai-coding-dictionary/ticket)。把挑中的改進放進規格說明，而不是直接去實作。這是個一再出現的問題，技能本身卻沒有有文件記載的工作流程。

**我該怎麼提示它？**

把你要建置的下一個東西放在心上。當大型建置即將到來時，把它指向規格說明並問「how can we make this change easy?」。未提示的執行會自行掃描熱點，這對例行維護沒問題，但點名一個方向才是讓報告可執行的關鍵。

**它能在大型遺留代碼庫上運作嗎？**

部分可以。它對缺乏一致結構的大型既有代碼庫很強，而且是任何一次性結構設定後建議的維護機制。誠實的反向平衡：專案真正失控的使用者回報它「helped a little but still doesn't seem to cut it」，而一位有八年遺留代碼庫的開發者回報，在同一個技能對整齊儲存庫產出乾淨圖表的同時，模型卻原地打轉。那個案例還沒有專用的 `/refactor` 技能。如果代碼庫完全沒有共享詞彙，先 [grill-with-docs](https://aihero.dev/skills-grill-with-docs) 建立一套，往往會讓此技能的輸出好很多。

**這跟 `/codebase-design` 有什麼不同？**

`/codebase-design` 是參考，不是會話驅動器。它提供詞彙——module、interface、depth、seam、adapter、leverage、locality——而此技能借用它。把全新代理指向 `/codebase-design` 當成要「做」的事是已知的失敗：沒有自己的流程可循時，代理會發明一個、重新探索程式碼，跑非常久才問你任何東西。用這個技能驅動；消費那一個。

**它會告訴我代碼庫很好嗎？**

很少，而你在進去之前就該知道。技能的建構目的是輸出發現，所以框架會把它推向產出候選者，而不是得出沒有錯的結論。強度徽章是防禦——一份所有東西都是 `Speculative` 的報告，就是技能用它所知的唯一方式告訴你：它什麼都沒找到。

**它在 Codex 或其他執行環境中能運作嗎？**

部分可以。探索步驟直接指名 Claude Code 的 `Agent` 工具並帶 `subagent_type=Explore`，所以沒有那個工具的[執行環境](https://www.aihero.dev/ai-coding-dictionary/harness)可能會跳過平行探索，而不是用自己取代。技能仍會執行；掃描只是較不徹底。有人提議過與執行環境無關的重寫，但尚未合併。

**我要如何在 TypeScript 中實際實作深模組？**

技能沒有隨附好的答案。反覆出現的需求是一份給出原則具體檔案與模組配置的 `TYPESCRIPT.md`，而它並不存在。技能會告訴你加深該落在哪裡、接縫背後該放什麼；把它轉成套件或目錄結構目前是你的工作。

## 這樣就算成功

- 候選者點名你領域的概念，而不是發明的類別名稱——「the Order intake module」，而不是「the FooBarHandler」。
- 候選者聚集在你近期編輯過的檔案中，而不是儲存庫沉睡的角落。
- 執行期間沒有任何程式碼改變。唯一的新檔案是你暫存目錄中的 HTML 報告。
- 它在報告之後停下來，問你要哪個候選者，而不是自己繼續。
- 每張卡片都把報酬解釋為局部性或槓桿收益，並說出哪些測試會變簡單——而不只是「this is cleaner」。
- 為持久理由否決候選者時，你會獲得記錄 ADR 的提議，讓下一次執行不再建議它。

## 它在哪裡適用

`improve-codebase-architecture` 是**定期維護**——每隔幾天執行，在任何鏈之外，目的是為工作排隊而不是執行它。它的鄰居是 [codebase-design](https://aihero.dev/skills-codebase-design)——擁有每個候選者都用其寫成的深度與接縫詞彙；[grilling](https://aihero.dev/skills-grilling)——在你挑選候選者後走過決策樹；以及 [domain-modeling](https://aihero.dev/skills-domain-modeling)——在決策落定時讓 `CONTEXT.md` 與 ADR 保持最新。它產出的是想法，在 [grill-with-docs](https://aihero.dev/skills-grill-with-docs) 或 [to-spec](https://aihero.dev/skills-to-spec) 處重新進入主建置流程。至於哪個技能適合某種情境，[ask-matt](https://aihero.dev/skills-ask-matt) 是整套的路由器。
