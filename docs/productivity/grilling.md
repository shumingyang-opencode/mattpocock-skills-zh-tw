## 用途

`grilling` 是在任何人採取行動之前壓力測試計畫、決策或點子的訪談迴圈。它把主題對映成**設計樹**——每個決策分支成掛在它下面的決策——並逐分支訪談你，直到沒有靜默假設剩下的東西。

它不一次問一個問題，也不一次問完所有東西。每**輪**問整個**前沿**：每個前提條件已定案的決策，僅此而已。如果兩個問題彼此相依，它們永遠不會共享同一輪——取決於仍開放之答案的問題屬於較晚的輪。你的回答定案決策、前沿向外移動，而下一輪問那些被解除阻塞的。十三個問題通常落在約三輪，而不是十三輪。

## 何時使用

輸入 `/grilling`，或當任務適用時，[代理](https://www.aihero.dev/ai-coding-dictionary/agent)會自行採用它。它是 grilling 家族中唯一由模型呼叫的[技能](https://www.aihero.dev/ai-coding-dictionary/skill)，這就是為什麼你很少輸入它：通常是某個你*確實*輸入的技能在為你執行它。

直接輸入 `/grilling` 得到純粹的訪談，沒有其他。當你想要比那更多的東西時：

| 你有什麼 | 取用 |
| --- | --- |
| 你不在工作目錄中 | [grill-me](https://aihero.dev/skills-grill-me)——相同的[會話](https://www.aihero.dev/ai-coding-dictionary/session)，以代理永遠不會自己觸發的名稱 |
| 你在工作目錄中 | [grill-with-docs](https://aihero.dev/skills-grill-with-docs)——相同的會話，而且邊做邊寫 `CONTEXT.md` 與 ADR |
| 一個大到塞不進單一會話的工作 | [wayfinder](https://aihero.dev/skills-wayfinder)——它繪製地圖，並在決策 ticket 內部跑 grilling |
| 一個對話無法定案的問題——某件事應該看起來或感覺起來如何 | [prototype](https://aihero.dev/skills-prototype)——建置一次性版本，然後回來 |
| 一個需要訪談的你自己的技能 | 從它內部呼叫 `/grilling`，而不是撰寫另一個訪談 |

## 輪、前沿與誰決定

三個概念承載整個技能。

**設計樹**是主題的模型：帶著掛在下面的決策的決策。**前沿**是前提條件都定案的決策集合——到目前為止唯一能被誠實問出的問題。**輪**是一個前沿，被完整問出、被完整回答。

在一輪內部，每個問題都以固定形狀到達：在 `❓` 後面編號並標題，然後內容，然後代理的建議答案單獨在 `➡️` 行。這正是讓一輪能以號碼回答的原因——「1 yes, 2 the second option, 3 no, here's why」——而不是把問題引用回去。這個格式有一個已知的粗糙邊緣：建議有時*反對*照措辭的問題，所以同意建議意味著對問題回答「no」。發生時，回答建議並說明。

設計的另一半是事實與決策的區分。事實是技能自己的工作：當前沿問題需要[環境](https://www.aihero.dev/ai-coding-dictionary/environment)能定案的東西時，它派出[子代理](https://www.aihero.dev/ai-coding-dictionary/subagent)去查明，而不是問你。它不會為此阻塞——只有執行中的探索下游的問題等待。決策是你的，而它必須等它們。一個執行 `grilling` 卻回答自己決策的代理已經弄壞技能，而不是寬鬆地詮釋它。會話在前沿清空時結束，而在你確認已達成共同理解之前，它不會對你同意的內容採取行動。

誠實的界線：前沿是代理的判斷，不是計算出的圖。它可能把兩個問題放進同一輪，事後才發現一個答案本應改變另一個。除了告訴它之外沒有防護，那會在下一輪重新打開受影響的分支。

## 什麼住在這裡，什麼住在包裝裡

這一頁涵蓋機制。人們最常要的東西記錄在往上一層。

| 問題 | 在哪裡被回答 |
| --- | --- |
| 樹、前沿、輪、問題格式、事實對決策 | 這裡 |
| 會話該跑多久、怎麼處理你無法靠對話回答的問題、如何避免一直點頭 | [grill-me](https://aihero.dev/skills-grill-me) |
| 什麼被寫進 `CONTEXT.md`、什麼變成 ADR | [grill-with-docs](https://aihero.dev/skills-grill-with-docs) |

## 常見問題

**我可以回到一次只問一個問題嗎？**
可以，而且很大一部分受眾這麼做。把它加入你的全域 `CLAUDE.md`：

```
When grilling, ask one question at a time.
```

以輪為基礎的預設真的備受爭議。閱讀慢、用第二語言工作、或把依序格式當作專注支架的實務工作者，都回報一次一個的節奏對他們更好，而且這個退出選項是被支持的，而不是被容忍的。

**`/batch-grill-me` 去哪裡了？**
併入這個技能。以輪為基礎的提問曾以獨立技能短暫發布，然後移入 `grilling` 本身，所以建在原語上的一切——`grill-me`、`grill-with-docs`、`triage`、`wayfinder`——同時獲得它。沒有 `batch-grill-me` 可安裝，也沒有分開的依序技能；上方的 `CLAUDE.md` 那一行就是回到一次一個的方式。

**一次問完一整輪，必定會失去我較早回答本來會引出的問題。不是嗎？**
這是對輪設計最常見的反對，而前沿就是答案：一輪永遠只包含不彼此相依的問題，所以一輪中的回答無法使那輪中的另一個問題無效。回答仍重塑下游的一切——下一輪是重新計算的，不是預先寫好的。你失去的比「all questions at once」暗示的小，比「沒有」大：見上方前沿的界線。

**它用完問題，然後開始建置。**
確認閘門正是為此存在：技能在前沿清空時沒有完成，它在你說理解是共享時才完成。較弱、較快的[模型](https://www.aihero.dev/ai-coding-dictionary/model)仍會弄壞它——這最常被回報於較低投入或非前沿的模型，它們把「interview until shared understanding」塌縮成幾個問題與一份大綱。如果你的會弄壞，可靠的修復是在你自己的 `AGENTS.md` 或 `CLAUDE.md` 中放一行，告訴代理未經許可不要實作。

**它回答自己的問題，而不是問我。**
那是執行中的 bug，不是預期的行為，而它就是技能文字中事實與決策被分開的原因。它最常出現在另一個技能在「解決這張 ticket」框架內執行 `grilling` 時，在那裡周圍的任務讀起來像是繼續前進的許可證。同一個約束也是沒有非同步模式的原因：人們要求過一個讀取 GitHub issue 並發布一份合併決策備忘錄的變體，而那是不同的技能，因為一場沒人回答的 grilling 會話產出的是代理的意見，而不是你的。

**我可以限制問題數嗎？**
不行，而上限刻意超出範圍。有些計畫需要三個問題，有些需要五十個；固定上限要嘛截斷困難的案例，要嘛在簡單的案例上感覺武斷。以平白語言引導是預期的控制——叫它收尾，或停下來接受現狀的計畫。如果會話跑得非常久，原因通常是範圍太大；把工作拆開並逐塊 grill。

**我只安裝了 `grill-me`，卻什麼都沒發生。**
`grill-me` 是一行技能，其全部內容是「run a `/grilling` session」，所以它也需求此技能已安裝。`grill-with-docs` 也是，它還需要 [domain-modeling](https://aihero.dev/skills-domain-modeling)。安裝整套能避免問題；選擇性安裝意味著也要安裝原語。

**`grill-with-docs` 跑了，但它從未載入 `grilling`。**
真實且未修復的粗糙邊緣，橫跨[執行環境](https://www.aihero.dev/ai-coding-dictionary/harness)與模型被回報：一個點名另一個技能的技能，無法可靠地讓那個技能載入，而 `grill-with-docs` 點名了兩個。跡象是一場一次問完所有東西、沒有任何建議附著的會話——那是模型臨場發揮訪談，而不是執行這一個。直接問代理它是否載入了 `grilling` 與 `domain-modeling` 通常能恢復。

## 這樣就算成功

- 一輪以編號清單到達，每個問題的建議在分開的 `➡️` 行，而你能以號碼回答整輪。
- 一輪中沒有東西需要同一輪中另一個問題先被回答。
- 較晚的輪問第一輪不可能問的事。
- 它會去查事實——讀檔案、派出子代理——而不是問你它本來就能查明的事。
- 背景中執行的研究不會讓輪停滯；只有依賴它的問題等待。
- 它在結尾停下來，請你確認理解是共享的，而不是開始工作。
- 問題數保持高，而輪數保持低。

## 它在哪裡適用

`grilling` 是**原語**，不是你要排程的步驟：訪談技巧的單一真相來源，放在一個地方，讓每個需要訪談的技能取用它，而不是發明一個。[grill-me](https://aihero.dev/skills-grill-me) 與 [grill-with-docs](https://aihero.dev/skills-grill-with-docs) 是它的兩個由使用者呼叫的正門，而 `grill-with-docs` 是主建置鏈開始的地方，在 [to-spec](https://aihero.dev/skills-to-spec) 之前。[wayfinder](https://aihero.dev/skills-wayfinder) 跑它來解決決策 ticket，[triage](https://aihero.dev/skills-triage) 用它把模糊的報告 grill 成可用的報告，而 [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) 在挑選要加深的候選者後用它走過樹。當你不確定哪個入口適用時，[ask-matt](https://aihero.dev/skills-ask-matt) 會幫你導航。
