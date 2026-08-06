## 用途

`grill-me` 接受一個**鬆散的點子**，並訪談你，直到它裡面有真實的決策。你不需要一個推敲好的計畫才能開始——產生一個正是[會話](https://www.aihero.dev/ai-coding-dictionary/session)的用途。它以**輪**來問：每輪是整個**前沿**——每個前提條件你已定案的問題——所以你永遠不會被問到一個取決於它還沒聽過之答案的問題。

它是**[無狀態](https://www.aihero.dev/ai-coding-dictionary/stateless)**的。它不寫檔案，不留工作區。它只留下一樣東西：一個更銳利的想法版本，在你自己的腦中。

## 何時使用

你輸入 `/grill-me` 來呼叫它——[代理](https://www.aihero.dev/ai-coding-dictionary/agent)不會自行使用它。在**全新的對話**中開始它，不要疊在你已經讓代理寫好的計畫上。

當你有一個值得認真對待的點子時就取用它——一個功能、一個產品方向、一個商業決策、一篇寫作——而且遠在你推敲出它涉及什麼之前。模糊不是等待的理由；它是會話吞吃的東西。如果你已經能精確指定那個東西，你不需要 grill 它。

你要三個 grilling 技能中的哪一個，取決於眼前有什麼：

- **任何東西，任何地方**——`grill-me`。它不需要儲存庫、不寫檔案，而且主題不必是程式碼。
- **一個可供對齊的代碼庫**——[grill-with-docs](https://aihero.dev/skills-grill-with-docs)。相同的訪談，但是[有狀態](https://www.aihero.dev/ai-coding-dictionary/stateful)：它讀你的程式碼，並把它學到的保存進 `CONTEXT.md` 與 ADR。
- **大到塞不進單一會話**——[wayfinder](https://aihero.dev/skills-wayfinder)。它把工作繪成地圖，並在裡面跑 grilling 會話。

關掉[計畫模式](https://www.aihero.dev/ai-coding-dictionary/agent-mode)。計畫模式會讓代理傾向趕快產出計畫，這與保持在探究中相反。

## 它是對話，不是訪談

技能問問題，但**你**擁有範圍。那是人們漏掉的部分，它把「把點子變成決策的會話」與「產出自信廢話的會話」分開。

失敗模式是**被動**——對四十個問題回答「agreed, agreed, agreed」，然後出來一份代理寫的、你點頭的計畫。它因為很長而感覺有生產力。實際上沒有任何東西被決定，而結果帶著它沒賺來的確定性。

主動意味著引導。對低於你所需保真度的問題反擊。當範圍漂移時說出來。回答「I don't know」而且是認真的。這個技能的建構是協助工程師，而不是取代工程師：出來什麼跟隨你回答的品質，而不是被問的問題數。

相反的錯誤真實但較少見——留在訪談中太久，以致你永遠到不了程式碼。

## 可 grill 與不可 grill

有些問題可以靠對話回答。其他不行，而再多 grilling 也到不了。

「One long form or three pages?」與「how should this interaction feel?」是**不可 grill**的——它們需要東西來反應。當你撞到一個，停止 grilling。用 [prototype](https://aihero.dev/skills-prototype) 建置一次性版本，看它，然後回來用一行回答。

用對話撐過一個不可 grill 的問題，正是會話膨脹的地方。代理持續換句話說、你持續猜測，而範圍成長來填滿不確定性。

## 這樣就算成功

- 你對某件事不同意。一場沒有你反擊的會話，是一場你不需要的會話。
- 問題以少數幾輪到達，而不是一滴一滴地拖很長，而較晚的輪清楚建立在你較早說的話之上。
- 你最後去到一個你沒預期的地方，因為某個問題浮現了一個你一直在隱式做出的決策。
- 結尾時你能對不在場的人辯護每個選擇。

## 常見問題

**我該預期多少問題，而我要怎麼知道它結束了？**
數輪，不數問題。四輪共四十六個問題是一場普通的會話。它在前沿清空時結束——每個分支都拜訪過，沒有靜默假設剩下的東西。

**它問了我兩百個問題。哪裡出錯了？**
通常範圍太大了。先叫代理把工作拆成較小的片段，然後逐個 grill。非常長的會話也會漂進**[愚鈍區](https://www.aihero.dev/ai-coding-dictionary/smart-zone)**，在那裡[上下文視窗](https://www.aihero.dev/ai-coding-dictionary/context-window)滿到問題變得更糟。

**我可以回到一次只問一個問題嗎？**
可以。把它加入你的全域 `CLAUDE.md`：

```
When grilling, ask one question at a time.
```

**如果我真的是不知道答案呢？**
說出來。「I don't know」是真實的回答，而一個你無法回答的問題通常是該做原型的跡象，而不是該猜。

**寫規格說明之前我要開新會話嗎？**
不。會話的價值是你剛建立的[上下文](https://www.aihero.dev/ai-coding-dictionary/context)。把同一次對話直接交給 [to-spec](https://aihero.dev/skills-to-spec)。

**模型重要嗎？**
比對大多數技能更在乎。Grilling 倚賴[模型](https://www.aihero.dev/ai-coding-dictionary/model)自己對系統如何壞掉的感覺，所以給它你最好的。實作大多跟隨上下文，容忍較便宜的模型。

## 它在哪裡適用

`grill-me` 是**你可以在任何地方、對任何東西執行的獨立技能**。無狀態正是讓它可攜的原因：沒有儲存庫、沒有工作區、沒有設定，也不假設點子與軟體有關。人們把它指向商業決策、寫作、接下來要做什麼——任何在他們腦中坐不住的東西。

那種可攜性正是與 [grill-with-docs](https://aihero.dev/skills-grill-with-docs) 的全部差異，後者跑相同的訪談，但讀取代碼庫供對齊，並把它學到的記錄為 `CONTEXT.md` 與 ADR。兩者都座落在 [grilling](https://aihero.dev/skills-grilling) 原語上；`grill-me` 是由使用者呼叫的正門，不攜帶任何東西。

如果你 grill 的東西結果真是軟體，你可以把同一次對話交給 [to-spec](https://aihero.dev/skills-to-spec)，並繼續進入建置流程——那是個選項，不是技能的重點。當你不確定哪條流程適用時，[ask-matt](https://aihero.dev/skills-ask-matt) 會幫你導航。
