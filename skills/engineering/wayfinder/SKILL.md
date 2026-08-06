---
name: wayfinder
description: 把一大塊工作——大得單一代理 session 裝不下——規劃成 Issue 追蹤器上決策 tickets 的共享地圖，逐一解決，直到通往目的地的路徑清晰為止。
disable-model-invocation: true
---

一個鬆散的點子來了——大得單一代理 session 裝不下，而且籠罩在迷霧中：從這裡到**目的地**的路徑還看不見。尋路是關於找出那條路徑，而不是朝目的地衝刺。這個技能把路徑繪製成 repo Issue 追蹤器上的**共享地圖**，然後逐一處理它的**決策 tickets**——其解決是決策、而非待執行的建置切片的問題——直到路線清晰為止。

目的地因努力而異，而為它命名是繪圖的第一個動作——它會塑造每一張 ticket。它可能是要交接並反覆迭代的規格說明、要在規劃開始前鎖定的決策，或是一項就地完成的變更，例如資料結構遷移。地圖與領域無關——工程工作、課程內容，任何符合這個形狀的東西都行。

## 規劃，而非動手

Wayfinder 預設是**規劃**：每張 ticket 解決一個決策，而當地圖清晰時就完成了——在有人去做這件事之前，沒有什麼需要再決定。那股只想動手做的衝動，通常就是你已經到達地圖邊緣、該交接的訊號。一次努力可以在它的 **Notes（備註）** 中推翻這個預設——把執行帶進地圖本身——但若沒有這樣做，產出的是決策，而非交付物。

## 用名稱引用

每張地圖與每張 ticket 都是一個 issue，所以它有個**名稱**——它的標題。在人類閱讀的一切中——敘述、地圖的 Decisions so far——都用那個名稱引用它，絕不用孤伶伶的 id、編號或 slug。一整面 `#42, #43, #44` 難以閱讀；名稱則一眼就能看懂。id 與 URL 不會消失——名稱包裹著它的連結——但它們待在名稱*裡面*，絕不代替名稱。

## 地圖

地圖是這個 repo Issue 追蹤器上單一的 issue，標籤為 `wayfinder:map`——正式產物。它的 tickets 是地圖的子 issues。

地圖是**索引**，不是儲存庫。它列出已作的決策，並指向持有其細節的 tickets；一個決策只住在一個地方——它的 ticket——所以地圖絕不重述它，只摘要並連結它。

**地圖、它的子 tickets、阻塞與前沿查詢實際存在哪裡，是追蹤器特定的。** Issue 追蹤器應該已經提供給你——如果沒有，執行 `/setup-matt-pocock-skills`。查閱追蹤器文件的「Wayfinding operations」區段，了解*這個* repo 如何表達它們。如果沒有提供追蹤器，預設使用本機 markdown 追蹤器。

### 地圖內文

整張地圖以低解析度呈現，每個 session 載入一次。開放的 tickets **不**被列出——它們是開放的子 issues，靠查詢找到。

```markdown
## Destination

<what reaching the end of this map looks like — the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

<!-- the index — one line per closed ticket: enough to judge relevance, then zoom the link for the detail the ticket holds -->

- [<closed ticket title>](link) — <one-line gist of the answer>

## Not yet specified

<!-- see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- see "Out of scope": work ruled beyond the destination; closed, never graduates -->
```

### Tickets

每張 ticket 是地圖的**子 issue**；追蹤器的 issue id 是它的身分。它的內文就是問題，大小以一次 100K token 的代理 session 為準：

```markdown
## Question

<the decision or investigation this ticket resolves>
```

每張 ticket 帶一個 `wayfinder:<type>` 標籤——`research`、`prototype`、`grilling`、`task` 其中之一（見 [Ticket Types（ticket 類型）](#ticket-types)）。

session 透過把 ticket 指派給驅動地圖的開發者來**認領**它，且要在任何工作**之前**先做，這樣並行的 sessions 就會跳過它。被指派者*就是*認領：一張開放、未指派的 ticket 就是未被認領的。

阻塞使用追蹤器的**原生**相依關係——這很重要，因為它會在追蹤器自己的 UI 中*視覺化*呈現前沿，讓人在不開啟地圖的情況下就能看到什麼可以拿。只有缺少原生阻塞的追蹤器才會退回內文慣例。當阻塞它的每張 ticket 都關閉時，ticket 就**未阻塞**；**前沿**是開放、未阻塞、未被認領的子項——已知領域的邊緣。

答案不是內文的一部分——它在解決時被記錄（見 [Work through the map（走完地圖）](#work-through-the-map)）。解決 ticket 時建立的資產從 issue 連結，而不是貼進去。

## Ticket 類型

每張 ticket 要不是 **HITL**——人在迴圈中，與一位為自己發聲的人類一起處理——就是 **AFK**，由代理獨自驅動。HITL ticket 只能透過那種即時交流解決；代理絕不代替人類的那一方（一個自己回答自己問題的 grilling 代理就是破壞了這個原則）。

- **Research**（AFK）：閱讀文件、第三方 API，或知識庫等本機資源，以浮現決策所等待的事實。由 `/research` **子代理**解決。當需要目前工作目錄之外的知識時使用。
- **Prototype**（HITL）：藉由做出便宜、粗略、具體的產物來提高討論的逼真度——大綱、粗略草稿、樁，或透過 /prototype 技能的 UI／邏輯程式碼。把原型連結為資產。當「它應該長什麼樣」或「它應該怎麼運作」是關鍵問題時使用。
- **Grilling**（HITL）：對話。預設情況。永遠叫用 /grilling 與 /domain-modeling 技能。
- **Task**（HITL 或 AFK）：在能做出*決策*之前必須發生的手動工作——沒有什麼要決定、原型或研究，但討論會被阻塞直到它完成。註冊一個服務以便評估它的 API、佈建存取權、移動資料以便看到它的形狀。這是唯一一個*動手做*而非做決策的類型——它靠解除決策的阻塞來贏得一席之地，而不是靠交付目的地。代理在能獨自驅動的地方獨自驅動（AFK）；否則它給人類一份精確的檢查清單（HITL）。工作完成時解決；答案記錄做了什麼，以及後續 tickets 依賴的任何衍生事實（憑證位置、新的 URL、行數）。

## 戰爭迷霧

地圖是*刻意*不完整的：別繪製你尚看不見的東西。在活躍的 tickets 之外是**戰爭迷霧**——那些你曉得即將到來、卻還無法確定的決策與調查的模糊視野，因為它們懸在仍然開放的問題上。解決一張 ticket 會清除它前方的迷霧，把現在可以明確化的東西轉化為新的 tickets——一次一個，直到通往目的地的路徑清晰、沒有剩餘的 tickets 為止。

地圖的 **Not yet specified（尚未明確）** 區段就是寫下那種模糊視野的地方：被懷疑的問題、之後要再回來看的區域。它是*朝向*目的地的未發現前沿——這裡的一切都在範圍內，只是還不夠銳利到可以做成 ticket。視視野允許的程度，盡量鬆散或盡量完整地寫；它同時也是給協作者閱讀、標示這次努力將走向何處的路標。

**迷霧還是 ticket？** 判準是你能不能*現在*就精確陳述這個問題——*不是*你現在能不能回答它。

- **做成 ticket** 當問題已經銳利時——即使它被阻塞、你還沒辦法採取行動。
- **尚未明確** 當你還沒辦法把它陳述得那麼銳利時。別把迷霧預先切成 ticket 大小的碎片：它比 ticket 更粗略，而且一旦前沿到達它，一片迷霧可能轉化為好幾張 tickets，或一張都沒有。

**尚未明確** 排除已經決定的內容（Decisions so far）、已經在線的 ticket，以及超出範圍的內容（下一節）。

## 超出範圍

迷霧只會*朝向*目的地聚集。目的地固定了範圍，所以超出它的工作是**超出範圍**——它不是迷霧，也不屬於 **Not yet specified**。它在地圖上有自己的一節 **Out of scope（超出範圍）**：你刻意排除出*這次*努力的工作。讓它落在這裡的是範圍，不是銳利度。

超出範圍的工作永遠不會轉化——前沿在目的地停止——所以它只有在目的地被重新繪製時才會回來，而且是以一次新努力的形式，而不是恢復。

把某個東西裁定為超出範圍是一個界定範圍的行為，而不是路線上的步驟。當一張既有的 ticket 原來位於目的地之外——繪圖時被錯納入範圍，或被某次解決所暴露——就**關閉它**（已關閉的 ticket 明確地脫離前沿），並在 **Out of scope** 區段留下一行：要點加為什麼它超出範圍，並連結那張已關閉的 ticket。它不會進入 **Decisions so far**，那個區段記錄的是實際走過的路線——範圍邊界不是路線上的步驟。

## 叫用

兩種模式。無論哪種，**每個 session 絕不解決超過一張 ticket**——research tickets 除外。

### 繪製地圖

使用者以一個鬆散的點子叫用。

1. **為目的地命名。** 執行 `/grilling` 與 `/domain-modeling` session，確定這張地圖在尋找到達的目標——規格說明、決策或變更。目的地固定了範圍，所以要最先定案。
2. **繪製前沿。** 再次 grill，這次**廣度優先**：在整個空間展開，而不是在任一條線索上深入，浮現開放的決策與現在可以採取的初步步驟。**如果這沒有浮現任何迷霧**——通往目的地的路徑已經清晰，整個旅程小到單一 session 就裝得下——你不需要地圖。停下來詢問使用者想要怎麼進行。
3. **建立地圖**（標籤 `wayfinder:map`）：填好 Destination 與 Notes，Decisions so far 留空，把迷霧草擬進 **Not yet specified**。
4. **建立你現在可以明確化的 tickets**，作為地圖的子 issues——然後在**第二輪**中接上阻塞邊（issues 需要先有 ids 才能互相引用）。接線把它們分成前沿與被阻塞；任何你尚無法明確化的東西留在迷霧中——**Not yet specified** 區段。
5. **啟動 research 子代理。** 對你剛建立的每張 `research` ticket，啟動一個 `/research` 子代理平行解決它，在一條一次性 `research/<name>` 分支上捕捉它的發現，並從 ticket 帶一個上下文指標。
6. 停下——繪圖是一次 session 的工作；它不手工解決任何東西。

### 走完地圖

使用者以一張地圖（URL 或編號）叫用。ticket 是**選用**的——沒有指定時，由你挑選下一個決策，而不是使用者。

1. 載入**地圖**——低解析度的檢視，而不是每張 ticket 的內文。
2. 選擇 ticket。如果使用者點名了某張，就使用它。否則依序取下第一張前沿 ticket。**認領它**：在任何工作之前把它指派給自己。
3. 解決它——**視需要放大**：按需取用任何相關或已關閉 ticket 的完整內文；叫用 `## Notes` 區塊點名的技能。有疑問時，使用 `/grilling` 與 `/domain-modeling`。
4. 記錄解決：把答案貼成**結論評論**，**關閉** issue，並把**上下文指標**附加到地圖的 Decisions so far。
5. 加入新浮現的 tickets（先建立再接線）；把答案使之明確化的任何迷霧轉化，並把每片已轉化的迷霧從 **Not yet specified** 清除，讓它只以新 ticket 的形式存在。如果答案揭露某張 ticket——這張或其他張——位於目的地之外，**裁定它超出範圍**，而不是在路線上解決它。如果這個決策使地圖的其他部分失效，更新或刪除那些 tickets。

使用者可能平行處理未阻塞的 tickets，所以要預期其他 sessions 會同時編輯追蹤器。
