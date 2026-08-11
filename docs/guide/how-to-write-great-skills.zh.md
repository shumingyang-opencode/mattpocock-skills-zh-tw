## 失落的手冊：如何寫出好技能

這份指南把 Matt Pocock 在 AI Engineer World's Fair 的演講 **「Building Great Agent Skills: The Missing Manual」** 濃縮成一份四關卡檢查清單，你可以拿它來檢視自己寫的任何技能——或任何下載回來的技能。同一套檢查清單，也被編碼成機器可讀的 [`writing-for-agents`](writing-for-agents/SKILL.html) 技能。

## Skill hell——收集不等於會用

我們開發者似乎很擅長替自己找各種地獄。幾年前有 **tutorial hell（教學地獄）**——進了一堆教學，卻永遠拼不起來。然後是 **framework hell（框架地獄）**——每十分鐘就有個新的 JavaScript 框架問世。現在又多了一個：**skill hell（技能地獄）**。

Skill hell 是當你有滿坑滿谷可以免費下載、可以貢獻、可以自己摸索的技能，但你分不出好技能跟壞技能，看不出這些零件怎麼拼在一起，最後拿不到技能「號稱」能給你的成果。壞技能比沒技能更糟：它們燒你的 token、偷走 agent 的注意力，也偷走你對它的信任。

## 檢查清單——四道關卡

缺的是一份共享的評分表：一個能讓你看著技能說「這些是好的、這些是壞的」的框架。就是它。四道關卡，依序是：**Trigger（觸發）**——技能怎麼被叫起來；**Structure（結構）**——技能內部怎麼組成；**Steering（引導）**——你怎麼讓 agent 做你要它做的事；**Pruning（精簡）**——你怎麼把技能做到盡可能小。

## ① 觸發——決定：user-invoked 還是 model-invoked

技能有兩種叫法。**Model-invoked（模型觸發）** 的技能帶有一段 description，常駐在 agent 的 context window 裡；agent 讀到後決定要不要把 `SKILL.md` 拉進來。那段 description 就是一個 **context pointer（脈絡指標）**。**User-invoked（使用者觸發）** 的技能把指標藏起來——description 只給使用者看（`disable-model-invocation: true`），所以 agent 自己觸發不了。

Model-invoked 聽起來全面比較好——更靈活，model 可以在適合的時候自己伸手。但每多一個 model-invoked 技能，就多一份 **context load（脈絡負擔）**：每一次 request 都要多燒一份 description 的 token，也多一件讓 agent 分心的事。一百個 model-invoked 技能就是一百段 description 塞在 context 裡。

User-invoked 技能把成本推到另一邊——壓在**你**身上的 **cognitive load（認知負擔）**。User-invoked 技能越多，你得記在腦子裡「什麼時候該叫哪個」的就越多。

兩種哲學各自對應到真實的技能集：**Superpowers** 以 model-invoked 為主（把超能力交給 agent）；Matt 偏好自己掌握方向盤——user-invoked 讓 agent 的 context load 保持最小，也直接消掉一整類問題：「我的技能有沒有在對的時機被觸發？」沒有免費的午餐——看你要掌控還是要彈性，二選一。

## ② 結構——steps + reference，還有小小的 SKILL.md

一個技能由兩大單元組成。**Steps（步驟）** 是技能會一步步走完的程序。**Reference（參考資料）** 是幫助它走完那些步驟的輔助資訊。技能可以全是步驟、全是參考、或兩者皆有——用這個角度想，技能就好拆解、也容易從零寫起。

然後是硬性限制：**讓主要的 `SKILL.md` 檔案盡可能小。** 技能越小越好維護、越好稽核，而且你每砍掉一個字，就是在每次 request 的技能成本上省下一個 token。

讓它保持小的技術叫 **progressive disclosure（漸進式揭露）**：想想技能的 branches（分支）——技能各種不同的用法。只有某個分支用得到的參考資料，就是移出主檔的候選。用 **context pointer（脈絡指標）** 指向它——一個跟技能捆在一起的外部參考檔，agent 只在需要那個分支時才拉進來。

## ③ 引導——leading words 與 legwork

這是槓桿最高的一道關卡。Agent 常不照做，是因為你沒用 **leading words（引導詞）**——那些早就活在模型預訓練裡的緊湊概念，把小空間塞進大量意義。把引導詞放進技能文字，agent 在推理時會一直把它複述給自己聽，而正因為它不斷強調那個詞，它的行為就跟著走了。

經典案例：agent 習慣 **一層一層** 寫程式——先整個資料庫、再全部 schema、再全部 API、最後才前端。你可以寫一大段懇求它先做出小東西、先能跑再說。或者你丟進引導詞 **「vertical slice（垂直切片）」**——一個開發圈耳熟能詳的詞，會觸發 agent 的先驗。你甚至能驗證它有沒有生效：看 reasoning traces，就會看到 agent 自言自語「我們先做一個薄的垂直切片」。

第二根槓桿是 **legwork（實地功夫）**——當 agent 看得到終點線時，就會在某個步驟上偷懶。經典案例是 plan mode：「問澄清問題」永遠得不到足夠的功夫，因為 agent 看得到最終目標（產出計畫），就急著衝過去。Matt 的解法：把規劃拆成**獨立的一個技能**，讓 agent 一次只看得到一步。把未來的目標藏起來，反而逼出對當下這一步的專注。有時候「資訊給更少」才是把工作做深的方法。

## ④ 精簡——不要重複、不要沉積、不要空指令

一個巨大的技能通常是別的失敗模式的症狀。跑三項檢查：

**不要重複自己。** 每一塊都該有 single source of truth（單一真實來源）——一個權威位置，讓「改變行為」就是「在一個地方改一次」。連參考資料之間的跨檔重複也要注意。

**留意沉積（sediment）。** 當一群人一起編輯同一份共享文件、又沒人敢刪或改別人的東西時，最後就會沉積出一大坨常常跟主題無關的內容。如果加進去的東西不是所有分支都用得到，就把它移進對的分支——或直接砍掉。

**獵殺空指令（no-ops）。** 這是 AI 寫的技能最經典的病：看起來在做事、實際上完全沒影響 agent 的行為。測試方法是 **deletion test（刪除測試）**：把那一段刪掉，然後問 agent 的行為有沒有變。沒變，那段就是 no-op。要刪就刪整句，不是修修剪剪——而有爭議時，用「實際跑一次」來裁決，不要用辯論。

## 這套框架現在住哪裡

以上全部被編碼進 Matt repo 裡的一個技能——原名 `writing-great-skills`，v1.1 改名為 [`writing-for-agents`](writing-for-agents/SKILL.html)。它是撰寫任何「給 agent 看」的文件的參考：技能、`AGENTS.md`/`CLAUDE.md`、規格、ticket。技能專屬的機制（frontmatter、model- vs user-invoked、路由器技能）放在 [`SKILL-MECHANICS.md`](writing-for-agents/SKILL-MECHANICS.html)。把你正要安裝的任何技能——或那份沒人照做的 SOP——拿來跑一遍這四關吧。
