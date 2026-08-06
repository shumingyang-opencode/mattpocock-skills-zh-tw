---
name: writing-fragments
description: 寫作、探索 — 挖掘原始片段，還沒有結構。
disable-model-invocation: true
---

<what-to-do>

這是純粹的**探索**：擴大可能被寫出的空間，而不承諾結構 — 承諾是_開採_，那是另一個技能的工作。執行一場產生片段的 grilling session，持續訪問使用者關於他們想寫的任何事。在這裡施加階段、大綱或文章結構是超出範圍的。

當片段從對話的任何一方浮現時，將它們附加到單一 markdown 檔案中。

如果使用者沒有傳入路徑，問一次要儲存在哪裡，然後在整個 session 的剩餘時間記住它。

從使用者說的第一件事就捕捉片段，包括最初的提示。

首次寫入時，在頂部放一個帶有工作標題的單一 H1（之後可以改變），沒有其他東西 — 沒有中繼資料、沒有目錄、沒有日期。

</what-to-do>

<supporting-info>

## 什麼是片段

片段是任何可能存活到最終文章的文字片段。它必須_對作者可讀_ — 作者能分辨它是什麼意思 — 但它不需要定義它的術語，也不需要讓一個陌生的讀者能理解。門檻是「這是一段好寫作嗎？」，而不是「這是一個自包含的論證嗎？」

片段刻意地異質。可能是片段的例子：

- 一個您想在某處部署但還不知道在哪裡的銳利句子。
- 一個帶有一行理由的主張。
- 一個插曲：一件發生過的事、一段程式碼片段、一個情境、一個類比。
- 一個半成品想法：「X 感覺像 Y 的某件事，之後再想出來。」
- 一段引用、一段對話、一句偷聽到的話。
- 一串靠感覺聚在一起的相關觀察。
- 一句抱怨、一段告白、一個爆點。
- 一個**領頭詞** — 整個作品可以掛在上面的緊湊隱喻或新造詞（一個為想法命名的術語，就像 _tracer bullets_ 或 _fog of war_ 為整個模式命名一樣）。

其中，領頭詞是最有價值的要落地的片段。它是承重的：在探索中命名正確的那個，它會塑造後來的結構、過渡與標題 — 在整個開採階段都支付紅利。當對話繞著一個反覆出現的想法打轉，推動為它造一個詞。

小說家的日記是模型：多年的非結構化觀察，之後被挖掘為原始素材。片段就是觀察。

## 檔案格式

```markdown
# Working title

A first fragment lives here.

It can be multiple paragraphs. It can include lists, code, quotes — whatever
shape the fragment naturally takes.

---

A second fragment.

---

> A quoted line that the user wants to keep around.

A reaction to it.

---

- A cluster of related observations
- That hang together by feel
- And want to be near each other
```

片段以水平線（`\n---\n`）分隔。正文中沒有標題。沒有標籤。除了加入的順序之外沒有順序。

## 寫作節奏

靜默地附加。不要為每個片段請求許可。順帶一提地提到您加入了什麼（「adding that」），但不要用儲存對話方塊打斷對話。

在每次寫作之前：從磁碟重新讀取檔案。使用者可能在回合之間編輯、重新排序或刪除了片段 — 保留他們的變更。永遠不要覆寫檔案；只附加（或者，如果使用者要求，就地編輯特定片段）。

使用者隨時可以說「砍掉最後一個」、「把那句改得更銳利」、「把那兩個合併」。把它們當作第一等的指令。

</supporting-info>
