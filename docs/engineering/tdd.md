## 用途

`tdd` 以測試優先的方式建置功能或修復 bug：一個失敗的測試，然後剛好足夠通過它的程式碼，然後下一個行為。它承載讓那個迴圈產出值得保留之測試的標準——什麼是好測試、測試放哪裡、模擬是做什麼用的，以及三個悄悄毀掉套件的反模式。

它不會在未先約定的接縫上寫測試。在任何測試存在之前，它點名它打算測試的公開邊界，並停下來等你確認，因為測試精力是有限的，而這正是你把精力花在關鍵路徑而非每個邊緣案例的地方。另一件該知道的事是 `tdd` 是**參考**，不是驅動器。它持有迴圈的規則，而別的東西（你，或 [implement](https://aihero.dev/skills-implement)）執行應用它們的[會話](https://www.aihero.dev/ai-coding-dictionary/session)。

## 何時使用

輸入 `/tdd`，或當任務適用時，[代理](https://www.aihero.dev/ai-coding-dictionary/agent)會自動採用它——以測試優先方式建置功能或修復 bug，或當你說「red-green-refactor」時。

當有具體行為要建置、有輸入與可觀察的輸出、而且你想要能在重構中存活的測試時取用它。

| 你的情境 | 該去哪裡 |
| --- | --- |
| 有定義輸入與輸出的行為——商業邏輯、請求/回應契約、轉換、驗證 | `tdd` |
| 行為還沒有定案 | [to-spec](https://aihero.dev/skills-to-spec)，它也會在任何程式碼寫出之前約定測試接縫 |
| 問題其實是介面的形狀，不是測試 | [codebase-design](https://aihero.dev/skills-codebase-design) |
| 你有[規格說明](https://www.aihero.dev/ai-coding-dictionary/spec)或 [ticket](https://www.aihero.dev/ai-coding-dictionary/ticket)，想要整個建置為你執行 | [implement](https://aihero.dev/skills-implement)，它逐 ticket 驅動 `tdd` |
| 設定、接線、膠水程式碼、型別註記、直接的 CRUD 委派 | 這裡沒有什麼合適的——見下方未結的缺口 |

最後一行是真實的洞，不是風格偏好。技能決定接縫該放在*哪裡*；它裡面沒有任何東西決定某個變更是否*值得*走這個迴圈。拿它執行一個沒有獨立真相來源可斷言的變更，你會得到一個重述實作的測試——技能自己警告過的同義反覆反模式，只是從另一個方向到達。它是 [issue #746](https://github.com/mattpocock/skills/issues/746)，仍開著。在它關閉之前，那個判斷是你或你的 `CLAUDE.md` 的。

## 前置條件

需要安裝 [codebase-design](https://aihero.dev/skills-codebase-design)。`tdd` 過去隨附自己的深模組與介面設計筆記；在 v1.0 那些被刪除，改由共用技能負責，`tdd` 現在倚賴它取得介面設計詞彙。沒有其他——技能是[無狀態](https://www.aihero.dev/ai-coding-dictionary/stateless)的，不寫自己的檔案。

## 迴圈，以及它執行的接縫

三個詞承載這個技能。

**紅-綠。**寫下失敗的測試，然後只寫剛好足夠通過它的程式碼。不要預先猜測接下來的下一個測試。沒有重構階段：它在 2026 年 6 月被移除，因為代理基本上從不執行它，也因為審查與實作作為分開的會話效果更好。重構屬於 [code-review](https://aihero.dev/skills-code-review)。

**垂直切片。**一個接縫、一個測試、一個最小實作，然後重複——第一個循環是證明單一路徑端到端的**曳光彈**。相反的是水平切片：先寫所有測試，然後所有程式碼。整批測試驗證的是*想像的*行為，它們檢查事物的形狀，而不是使用者做的事，而且它們在你理解實作之前就把你綁定在測試結構上。

**預先約定的接縫。**接縫是你觀察行為、不深入內部的公開邊界。規則是絕對的：未確認的接縫上沒有測試。在完整鏈中，接縫在較早的 [to-spec](https://aihero.dev/skills-to-spec) 期間被約定——「`/tdd` is told to only work at pre-agreed test seams, `/code-review` checks that only agreed-upon test seams were used.」單獨呼叫時，`tdd` 直接問你。

它撰寫來防止的三個反模式：

| 反模式 | 跡象 |
| --- | --- |
| 耦合實作細節 | 當你重新命名內部函式時測試會壞，即使行為沒變。被模擬的內部協作者、斷言的呼叫次數、用來驗證而非介面的資料庫查詢。 |
| 同義反覆 | 期望值以程式碼計算它的方式計算，所以測試靠建構就通過。期望值必須來自別處——已知良好的字面值、推導過的範例、規格說明。 |
| 水平切片 | 一整批測試在任何實作之前落地。 |

模擬只用於系統邊界——外部 API、時間、隨機性，有時是檔案系統或資料庫。而不是你自己的模組。

## 常見問題

**為什麼它不重構？描述說「red-green-refactor」。**

因為重構步驟被移除，而描述沒有。移除是刻意的：代理基本上從不執行它，而且把實作與審查放在分開的會話效果更好。結果是否仍按書算 TDD，不如迴圈是否產出更好的程式碼重要。觸發詞與內容之間的不一致已登記為 [issue #589](https://github.com/mattpocock/skills/issues/589) 且仍開著，所以「red-green-refactor」繼續作為觸發此技能的片語。你得到的是紅 → 綠，以及在 [code-review](https://aihero.dev/skills-code-review) 中的重構。

**它叫我選一個測試接縫，而我毫無頭緒。**

這是此技能被回報最多的摩擦（[issue #607](https://github.com/mattpocock/skills/issues/607)）。提示詞只列出候選接縫的名稱，沒有說明每個接縫捕捉什麼或漏掉什麼，所以你在標籤之間做選擇。還沒有發布的修復。實際變通法是在回答之前向代理要取捨——元件層級接縫漏掉、而整合接縫捕捉到的是什麼，以及它慢多少。這也正是鏈在 `to-spec` 中預先約定接縫的原因，在那裡你看到整個功能，而不是一個提示詞。

**即使技能說紅優先，它還是先寫了實作。**

會發生。有位使用者對[模型](https://www.aihero.dev/ai-coding-dictionary/model)施加壓力，得到一個異常誠實的回答：「I knew the skill said 'one test at a time, watch it fail for the right reason' — I read it. I just defaulted to my normal habit.」技能是以接受這件事的方式撰寫的。沒有指示能讓代理 100% 順從，而把這一點逼得更用力只會為了小收益限制代理的創造力——即使沒有嚴格遵循，這個迴圈仍值得跑，因為結果整體仍然更好。如果特定切片需要嚴格遵循，盯緊執行，而不是相信技能會強制它。

**它應該先寫瀏覽器或端到端測試嗎？**

通常不要，而技能也不會阻止它。有位使用者回報代理先寫 Playwright 測試，然後燒掉一個長迴圈重新執行它，並針對一個還不存在的功能結論*測試*壞了。在 `CLAUDE.md` 中設定這個。瀏覽器測試慢到紅-綠回饋迴圈不再划得來；在你的儲存庫 `CLAUDE.md` 中宣告它們要在行為能運作之後才寫。

**`/tdd` 取代 `/implement`，或課程的 `/do-work` 嗎？**

不。`/tdd` 記錄方法論；`/implement` 是非常簡單的工作→回饋→commit 迴圈，是 `/do-work` 的直接替代。課程的單一 `/do-work` 步驟現在拆分到 `/implement`、`/tdd` 與 `/code-review`。如果你在問對一個 ticket 該跑哪一個，答案幾乎總是 `/implement`。

**深模組與介面設計指引去哪裡了？**

在 v1.0 併入 [codebase-design](https://aihero.dev/skills-codebase-design)，一般化到幾個技能共享一套詞彙。`refactoring.md` 同時離開；重構現在是 [code-review](https://aihero.dev/skills-code-review) 的工作，而該技能承載 Fowler 的壞味道基線。

**它知道我其他的 ticket 嗎？**

不知道。拿它執行一個 ticket，它會樂意提議屬於兄弟 ticket 的工作，因為它看不到 issue 圖的其餘部分（[issue #129](https://github.com/mattpocock/skills/issues/129)）。Matt 的立場是這不是 `tdd` 的職責。把規格說明與 ticket 一起傳進去有幫助；一開始就把 ticket 尺寸調整正確更有幫助。

## 這樣就算成功

- 在任何測試檔案存在之前，它停下來點名它打算測試的接縫，並等待。
- 一個測試出現、轉紅、獲得剛好足夠通過的程式碼，然後下一個測試才出現——不是一批測試後跟著一批程式碼。
- 測試名稱讀起來是能力（「user can checkout with valid cart」），不是內部（「checkout calls paymentService.process」）。
- 斷言中的期望值是你可追溯到規格說明的字面值，而不是以程式碼計算它們的方式重新計算的值。
- 重新命名內部函式不會弄壞套件中的任何東西。
- 模擬只出現在外部邊界——付款 API、時鐘——永遠不會繞著你自己的模組。

## 它在哪裡適用

`tdd` 是主鏈建置步驟內部的引擎，而不是它自己的一個步驟：

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review
```

[to-spec](https://aihero.dev/skills-to-spec) 預先約定測試接縫，[implement](https://aihero.dev/skills-implement) 逐 ticket 驅動 `tdd`，而 [code-review](https://aihero.dev/skills-code-review) 事後檢查只有約定的接縫被使用——並擁有 `tdd` 不再做的重構。它的另一個鄰居是 [codebase-design](https://aihero.dev/skills-codebase-design)，也就是 `tdd` 所說接縫與深模組詞彙的共同來源。你也可以單獨取用它，只要有具體行為要建置、且沒有完整規格說明在進行。當你不確定哪個技能適合你的情境時，[ask-matt](https://aihero.dev/skills-ask-matt) 會幫你導航。
