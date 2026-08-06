## 用途

`wait-what` 是一則訊息沒落地時你輸入的東西。[代理](https://www.aihero.dev/ai-coding-dictionary/agent)接著重新說明它剛說的內容。它補上你缺失的上下文、以平白英文撰寫，並使用你專案 `CONTEXT.md` 的詞彙。

技能只有三行長。那是設計，不是未完成的草稿。對抗冗長的技能會因為成長而失敗：一個四百行的精簡技能仍讓[模型](https://www.aihero.dev/ai-coding-dictionary/model)保持冗長，因為模型讀的是份量，不是請求。這一個只攜帶單一精確的引導詞，除此之外什麼都沒有。

## 何時使用

你輸入 `/wait-what` 呼叫它。代理不會自行採用它，也不該。只有你知道自己何時停止跟上。

你注意到自己在瀏覽的那一秒就用它。代理已漂進它發明的行話、堆了五個縮寫，或解釋了一個前提你從沒看過的決策。它修好你已經在的對話。要阻止行話完全到達，用 [grill-with-docs](https://aihero.dev/skills-grill-with-docs)，它在事前建構共享語言。

## 名字就是機制

引導詞是 **wait**。「Be concise」是關於代理輸出的指示，而模型以裁掉字詞、讓你更迷路來服從它。**Wait** 是關於*你的*狀態。它說理解在這裡失敗了。聽到「be brief」的代理寫電報。聽到「wait, you lost me」的代理會後退並解釋。

那個差異就是整個技能。每個流行的冗長修復都點名*輸出*：`/tldr`、`/no-fluff`、`/talk-normal`。模型過度修正成原始人語域，更短卻沒有更清楚。點名*聽者*同時要求兩半：更少的字詞**與**你缺失的上下文。

技能說重新說明**那個**，而不是「that last message」。迷住你的通常是超過一個段落的東西，所以代理決定要退回多遠。

## 它插進你已有的語言

內容重用你全域 `CLAUDE.md` 與專案 `CONTEXT.md` 中已有的引導詞。ASD-STE100 Simplified Technical English 設定語域。共通語言供應名詞。技能、`CLAUDE.md` 與 `CONTEXT.md` 取用相同的 [token](https://www.aihero.dev/ai-coding-dictionary/token)，所以呼叫它不是新指示。它是代理已經同意的指示的提醒。

如果你沒有 `CONTEXT.md`，技能仍有效。你只失去領域詞彙那一半。

## 這樣就算成功

- 重新說明**更短且更清楚**，不是更短且更鈍。
- 它補上你缺失的前提，而不是只刪字。
- 專案名詞取代發明的。你 `CONTEXT.md` 中的術語回來。
- 你能連續用兩次，而它不會退化為簡短。

## 它在哪裡適用

你可以在任何時點、任何對話、任何其他技能內部使用 `wait-what`。它事後修復一則訊息。真正的解方是事前同意的共享語言，那就是 [grill-with-docs](https://aihero.dev/skills-grill-with-docs)：一場邊做邊跑 [domain-modeling](https://aihero.dev/skills-domain-modeling) 的 [grilling](https://www.aihero.dev/ai-coding-dictionary/grilling) 會話，讓你們雙方使用的用詞落進你的 `CONTEXT.md`。如果你不確定哪個技能適合當下，[ask-matt](https://aihero.dev/skills-ask-matt) 會幫你導航。
