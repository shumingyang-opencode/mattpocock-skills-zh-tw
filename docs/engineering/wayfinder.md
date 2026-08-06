## 用途

`wayfinder` 接受一個大到無法塞進單一代理[會話](https://www.aihero.dev/ai-coding-dictionary/session)的工作——一個你能點名其**目的地**、卻還看不到其**路線**的點子——把它繪成你 issue 追蹤器上一張由**決策 ticket** 組成的共享**地圖**，然後一次一個地解決它們，直到路徑清楚。

它規劃，它不執行。每個 ticket 都持有一個問題，其解決是決策，不是要執行的一段建置；而當地圖在「某人去建置那個東西之前已沒有什麼要決定」時完成。那一條規則正是把 wayfinder ticket 與普通實作 [ticket](https://www.aihero.dev/ai-coding-dictionary/ticket) 分開的東西，而它是代理最常違反的規則。當地圖清空時，wayfinder 交接；它不會繼續進入程式碼。

## 何時使用

你輸入 `/wayfinder` 來呼叫它——[代理](https://www.aihero.dev/ai-coding-dictionary/agent)不會自行使用它。

它是整套中最重、最密的流程，所以觸發條件很窄：工作必須真的比單一代理會話能裝下的還大，且通往目的地的路線必須是模糊的。分野很清楚：單一會話規劃用 `/grill-with-docs`，多會話規劃用 `/wayfinder`。

| 你眼前有什麼 | 跑什麼 |
| --- | --- |
| 一個你可以在一場中定案的範圍良好功能 | [grill-me](https://aihero.dev/skills-grill-me)，有代碼庫時用 [grill-with-docs](https://aihero.dev/skills-grill-with-docs) |
| 全新專案，或橫跨多個會話、路線仍不清楚的建置 | `/wayfinder` |
| 一場決策已完成的對話 | [to-spec](https://aihero.dev/skills-to-spec)——直接跳過地圖 |
| 一張已清空的 wayfinder 地圖 | [to-spec](https://aihero.dev/skills-to-spec)，然後 [to-tickets](https://aihero.dev/skills-to-tickets) 與 [implement](https://aihero.dev/skills-implement) |
| 一個已經大到失控的既有會話 | 說「hand off to `/wayfinder`」——[handoff](https://aihero.dev/skills-handoff) 既能通往地圖，也能離開地圖 |

全新專案不是必要條件。Wayfinder 常規用於遺留與建了一半的代碼庫，而且在那裡可說更銳利，因為很多迷霧是「這裡已經為真的是什麼」而不是「我們該做什麼」。

## 前置條件

地圖與它的 ticket 住在儲存庫的 issue 追蹤器上，所以 wayfinder 需要 [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills) 鋪下的追蹤器接線。那個步驟寫出一個「Wayfinding operations」區段，描述地圖、子 ticket、阻塞邊與前沿查詢如何在 GitHub、GitLab 或本機 markdown 上表達。Wayfinder 透過你 `CLAUDE.md` / `AGENTS.md` 中的指標解析那份文件，而不是固定路徑；完全沒有設定追蹤器時，它回退到本機 markdown 檔案。

追蹤器不是裝飾。阻塞正是讓前沿在追蹤器自己的 UI 中視覺化呈現的東西，而沒有原生相依連結的追蹤器——比方說自架的 Gitea——會把 wayfinder 降級為從地圖文字推斷阻塞者，那有效，但需要更密切的監督。

## 地圖、迷霧與前沿

**地圖**是單一標示 `wayfinder:map` 的 issue；它的 ticket 是它的子 issue。它是**索引，不是存放處**——決策恰好活在一個地方，它的 ticket，而地圖只摘錄它並連結。會話以低解析度載入地圖，並按需放大到個別 ticket，這正是讓地圖能持續成長、卻不用每個會話都為整個歷史付費的原因。

有四樣東西住在它上面：

- **目的地**——到達這張地圖的結尾長什麼樣。命名它是繪製的第一個動作，在任何 ticket 存在之前，因為目的地固定了每個 ticket 據以被衡量的範圍。
- **已作決策**——每個已關閉 ticket 一行，每個都連結到細節實際所在。
- **尚未明確**——**戰爭迷霧**。你看得出會來、卻還無法精準措辭的決策。迷霧對 ticket 的測試是你能不能*現在*精準陳述問題，而不是你能不能回答它。解決一張 ticket 會清除它前方的迷霧，並把現在可明確化的東西轉化為新的 ticket。
- **超出範圍**——被裁定超出目的地的選項。迷霧永遠只朝*目的地*聚攏，所以超出範圍的工作會被關閉，永遠不轉化。

**前沿**是開放、未阻塞、未被認領的 ticket——已知的邊緣。會話在進行任何工作之前把 ticket 指派給自己來認領它，所以被指派者*就是*認領，而並發的會話會跳過它。ticket 全程以名稱被提及，絕不以光禿禿的 `#42`；一整面 issue 號碼在敘事中無法閱讀。

## 四種決策 ticket 類型

每個 ticket 都攜帶 `wayfinder:<type>` 標籤，而且不是 **[HITL](https://www.aihero.dev/ai-coding-dictionary/human-in-the-loop)**——與能為自己發言的人一起處理——就是 **[AFK](https://www.aihero.dev/ai-coding-dictionary/afk)**——由代理單獨驅動。HITL ticket 只透過現場交流解決；一個回答自己 [grilling](https://www.aihero.dev/ai-coding-dictionary/grilling) 問題的代理已經弄壞它了。

| 類型 | 模式 | 何時取用 | 由誰解決 |
| --- | --- | --- | --- |
| `grilling` | HITL | 預設。問題可以靠談透來定案。 | 在全新會話中用 [grilling](https://aihero.dev/skills-grilling) 加上 [domain-modeling](https://aihero.dev/skills-domain-modeling) |
| `prototype` | HITL | 「how should this look」或「how should this behave」——一個對話無法定案的問題。 | [prototype](https://aihero.dev/skills-prototype)，建置的產物以資產形式從 ticket 連結 |
| `research` | AFK | 工作目錄之外的事實阻塞著決策。 | 一個 [research](https://aihero.dev/skills-research) [子代理](https://www.aihero.dev/ai-coding-dictionary/subagent)，在繪製時觸發，並在 `research/<name>` 分支上平行燒掉 |
| `task` | 任一 | 沒有什麼要決定，但手工工作阻塞著決策——配置存取、註冊服務、移動資料以便看到它的形狀。 | 代理能時由代理單獨，否則給人類一份精確的檢查清單 |

`task` 是唯一*執行*而非決定的類型，它靠解除決策的阻塞來證明地位——永遠不是靠交付目的地的一部分。這是實務中最常出錯的類型：代理把它解讀為實作步驟，並開始在地圖內部寫產品程式碼。

Research 是*每會話一個 ticket* 的唯一例外。

## 常見問題

**這跟 `/grill-with-docs` 有什麼不同？我該先開哪一個？**
會話數，不是專案規模。`/grill-with-docs` 是單一會話規劃；wayfinder 是多會話規劃。如果你能在一場對話中掌握整個東西，grilling 是更便宜、更好的工具，而 wayfinder 對那個案例確實更慢更密。社群在它上面定下的簡稱：只有當工作塞不進單一會話時，wayfinder 才有意義。這是最常被問的 wayfinder 問題，而且它一直被問，因為描述不會告訴你你自己的任務落在那條線的哪裡——你得自己判斷會話數。

**當它問「destination」時，是指這個會話的結尾還是所有事情的結尾？**
整張地圖——整張地圖的目的地，而不只是初始會話。這個問題讀起來有歧義，因為 wayfinder 依定義是多會話工具，所以以會話為範圍的答案永遠不合理。典型的目的地是要交接的[規格說明](https://www.aihero.dev/ai-coding-dictionary/spec)、要在規劃開始前鎖定的決策、概念驗證，或像資料遷移這樣就地做的變更。

**地圖已清空。為什麼我還是需要 `/to-spec` 與 `/to-tickets`——wayfinder 不是已經寫了規格說明並做了 ticket 嗎？**
不。Wayfinder 的 ticket 是決策 ticket，而當地圖關閉時它們也全都關閉了。剩下的是充滿連結決策的地圖，那不是建置計畫。[to-spec](https://aihero.dev/skills-to-spec) 把那些連結決策摺疊成一份規格說明——`/to-spec #<map_issue>`——而 [to-tickets](https://aihero.dev/skills-to-tickets) 把它切成曳光彈實作 ticket。把地圖直接迴圈進 [implement](https://aihero.dev/skills-implement) 會跳過摺疊並丟掉連結細節。只有當工作結果真的很小時才直接去實作。人們確實會跑縮短的管線並回報它有效；那兩個額外步驟為你買到一份審查者或同事能讀的明確規格說明產物，而你越不單打獨鬥，它越重要。

**我的代理在 wayfinder 會話中途開始寫產品程式碼。**
這是此技能被回報最多的失敗，而它背後有一個真實的洞。Wayfinder 的「plan, don't do」預設可以在地圖的**Notes**中被覆寫——但 Notes 是代理寫的，所以約束與它的豁免住在同一個、被約束方擁有的檔案中。有位使用者看著代理把「this map carries execution」寫進自己的 Notes，然後在後續會話中把它讀回去當作自己的許可證，在實況伺服器上建置。沒有技能內部的硬性停機對應「I meant the default.」在它出現之前：讀任何不是你繪製的地圖的 Notes、把實作留在它自己的會話中，並把任何看起來像建置切片的 `wayfinder:task` 當成打錯類型。

**我繪製了 27 張 ticket，而等我到第十三張時，其餘的都不再有意義了。**
一個真實且被反覆回報的結果，逐字取自實地回報。Wayfinder 的預設本能是全面規劃，而一張後期 ticket 依賴較早 ticket 推翻之假設的地圖，正是技能被指控的那種瀑布陷阱。兩件事對抗它。把地圖範圍限定在有界限的目的地，而不是整個產品——實務工作者一致回報，範圍限定在單一已定義 epic 的地圖，表現比蔓延的「implement V1」好，而且規劃非常大的東西一開始就不是目標——交付小的增量才是。以及積極[原型化](https://www.aihero.dev/ai-coding-dictionary/prototyping)：路線保持現況的整個原因，是不確定性在實作依賴它之前就被便宜、具體的產物沖掉。Wayfinder 是「prototypemaxxing」，不是「planmaxxing」。

**我可以平行處理好幾張 ticket 嗎？**
前沿的建構是為了讓你看見什麼可取，而阻塞邊的存在是讓平行工作在紙面上安全。實務上一次一個是較安全的預設。同時處理兩張 grilling ticket 的使用者，會在一個會話中被問到剛在另一個會話回答過的問題，因為會話不共享[上下文](https://www.aihero.dev/ai-coding-dictionary/context)。原型 ticket 也有一個已知缺口：有代理被回報建置三個 UI 變體、自己挑了一個並關閉 ticket——選擇是你的，而技能目前沒有把這說得夠大聲。如果你真的要平行跑，先自己審查相依圖。

**我必須用 GitHub Issues 嗎？**
不——任何 issue 追蹤器都行。GitHub 是最受支援的路徑，因為它的原生子 issue 與阻塞關係正是讓前沿不用打開地圖就能看見的原因；GitLab、Linear、Jira 與本機 markdown 都有人用。兩個誠實的注意事項。沒有原生阻塞的追蹤器意味著相依圖是從文字推斷的，需要手工修正。而本機 markdown 把產物放進你的儲存庫，這不建議：把這種材料存在儲存庫中往往導致意外持久化。開源維護者撞到相反的問題——公開追蹤器被代理產生的規劃 ticket 填滿——而且無論如何傾向選擇本機 markdown。

**grilling 很耗神。每個問題都三段落長。**
這是關於 wayfinder 最銳利的現役抱怨，而且未解決。一位使用者給的分解：冗長本身造成決策耗竭，而長度剝離了*為什麼*會被問這個問題，所以當地圖變長時，你失去決策到決策的鏈。冗長看起來是目前[模型](https://www.aihero.dev/ai-coding-dictionary/model)集合的屬性，而不是技能的，而沒有修復落地。流通中的實務緩解：使用較低的[推理投入](https://www.aihero.dev/ai-coding-dictionary/effort)，並在你的全域 `CLAUDE.md` 中放一條平白語言的指示。無論如何都要預期在這裡投入真正的思考——wayfinder 要求你的思考量不是缺陷，它就是它存在的大部分目的。

**一個我已經關閉的決策結果是錯的。我要編輯舊 ticket 還是做新的？**
沒有官方指引，而代理的本能沒幫助：它傾向繞著壞決策設計，而不是挑戰它，所以你得手動引導。有效的做法是平白地告訴 wayfinder 什麼變了——它會更新地圖、修訂受影響的 ticket，並在已關閉的 ticket 上評論。地圖中途的範圍變更是可恢復的。一張你*設計*來改變的地圖是範圍界定上的壞味道。

**`decision-mapping` 去哪裡了？**
它就是這個技能，在 v1.1 改名為 `wayfinder`，以 `/wayfinder` 呼叫。「Decision map」是行話，而且也不準確，因為四種 ticket 類型只有一種真的是單獨的決策。重新框定給技能一套連貫的詞彙——目的地、戰爭迷霧、前沿、地圖——而不是疊在上面的發明術語。但單位保留了「decision」這個詞：wayfinder ticket 被稱為**決策 ticket**，正是為了阻止人們把它讀成實作 ticket。

## 這樣就算成功

- 在單一 ticket 存在之前，目的地就被寫下並同意。
- 每個未結 ticket 讀起來都是問題。任何讀起來是「build the X」的 ticket，不是打錯類型，就是屬於地圖下游。
- 你能看你的追蹤器就知道哪些 ticket 可取，不用打開地圖——那是前沿透過原生阻塞呈現自己。
- 一個會話解決一張 ticket、把答案以結論評論發布、關閉它，並在地圖的*已作決策*留下一行。然後它停下來。
- **尚未明確**隨時間縮小。一片轉化為 ticket 的迷霧會從那個區段消失，而不是同時活在兩個地方。
- 當開場的廣度優先 grill 完全找不到迷霧時，技能停下來並告訴你這項工作小到可以跳過地圖。
- 完成地圖的會話把你帶向規格說明，而不是 pull request。

## 它在哪裡適用

`wayfinder` 是**情境式入口**，不是預設正門。以 grill 引導的點子 → 交付鏈仍是大多數工作的起點；wayfinder 是當點子大到無法塞進單一會話時你爬上的東西，而它在 [to-spec](https://aihero.dev/skills-to-spec) 處匯回那條鏈，因為清空的地圖是交接，不是建置。

在底下，它大多是穿 wayfinder 排程的其他技能：[grilling](https://aihero.dev/skills-grilling) 與 [domain-modeling](https://aihero.dev/skills-domain-modeling) 解決預設的 ticket 類型，[prototype](https://aihero.dev/skills-prototype) 解決對話無法解決的 ticket，而 [research](https://aihero.dev/skills-research) 以子代理執行，讓它的閱讀永遠不落進你的會話。[handoff](https://aihero.dev/skills-handoff) 是進出的橋樑——從一場自我成長到失控的對話進入地圖，以及當會話中途出現支線任務時離開地圖。其他任何情況，[ask-matt](https://aihero.dev/skills-ask-matt) 導航整套。
