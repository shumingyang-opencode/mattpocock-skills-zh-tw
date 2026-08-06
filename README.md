> 這是 [mattpocock/skills](https://github.com/mattpocock/skills) 的**繁體中文翻譯版**（`mattpocock-skills-zh-tw`）。本 repo 只翻譯自然語言說明，保留目錄名稱、技能名稱、指令、程式碼區塊、路徑與工具識別符，以維持安裝與運行行為。英文原文請見上游 repo；安裝方式請依下方說明進行。
>
> **目前對齊上游 `mattpocock/skills` release `v1.2.2`（commit `8b36d4f`，2026-08-05）。** 上游有更新時，首頁「待辦事項 · 上游同步」面板會列出待翻譯項目。

<p>
  <a href="https://www.aihero.dev/s/skills-newsletter">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://res.cloudinary.com/total-typescript/image/upload/v1777382277/skills-repo-dark_2x.png">
      <source media="(prefers-color-scheme: light)" srcset="https://res.cloudinary.com/total-typescript/image/upload/v1777382277/skill-repo-light_2x.png">
      <img alt="Skills" src="https://res.cloudinary.com/total-typescript/image/upload/v1777382277/skill-repo-light_2x.png" width="369">
    </picture>
  </a>
</p>

# 給真正的工程師的技能（Skills For Real Engineers）

[![skills.sh](https://skills.sh/b/mattpocock/skills)](https://skills.sh/mattpocock/skills)

這是我每天用來做真正工程、而非 vibe coding 的代理技能。

開發真正的應用程式很難。GSD、BMAD、Spec-Kit 等做法試圖藉由接管流程來幫忙，但這麼一做的同時，它們拿走了你的掌控權，並讓流程中的 bug 難以解決。

這些技能被設計成小而容易改、且可組合。它們適用於任何模型，建立在數十年的工程經驗之上。隨意動手改改看，把它們變成你自己的。盡情享用。

如果你想跟上這些技能的變動，以及我之後創作的新技能，可以在我的電子報上加入約 60,000 位開發者的行列：

[訂閱電子報](https://www.aihero.dev/s/skills-newsletter)

## 安裝（30 秒設定）

兩條路，兩種哲學。**[Claude Code plugin](https://code.claude.com/docs/en/plugins)** 把整組技能安裝成受管、唯讀的 bundle，在我發布時更新 — 你是訂閱而非 fork。**[skills.sh](https://skills.sh/mattpocock/skills)** 則把可編輯的 skill 檔案複製到你的專案，讓你可以動手改、變成自己的。二選一 — 兩個都裝會讓你得到每種技能兩份。

### 1. 取得技能

<details>
<summary><strong>Claude Code</strong></summary>

```bash
claude plugins install mattpocock-skills
```

或從 session 內：

```
/plugin install mattpocock-skills
```

它位於 Claude Code 的官方 marketplace，所以無須先新增任何東西，更新自動送達。

</details>

<details>
<summary><strong>Codex 與其他代理</strong></summary>

```bash
npx skills@latest add mattpocock/skills
```

選擇你想要的技能，以及要安裝到哪些 coding agent。**安裝程式讓你挑選要帶走的技能 — 務必把 `setup-matt-pocock-skills` 列入其中。**

原生 Codex plugin 已在藍圖上 — 參見 [`.agents/adr/0002-ship-as-a-claude-code-plugin.md`](./.agents/adr/0002-ship-as-a-claude-code-plugin.md)。

</details>

<details>
<summary><strong>給愛動手的人</strong></summary>

在任何代理上使用同一個安裝程式 — 包括 Claude Code：

```bash
npx skills@latest add mattpocock/skills
```

它會把技能寫進你的 repo，作為你擁有且可編輯的普通檔案。沒有任何東西會在背後偷偷更新；想要時用 `npx skills update` 拉取我的最新變更。

</details>

### 2. 執行 `/setup-matt-pocock-skills`

在你的代理中，每個 repo 執行一次。它會：

- 問你想用哪個 issue tracker（GitHub、Linear 或本機檔案）
- 問你分診時套用哪些標籤（`/triage` 使用標籤）
- 問你想把我們建立的任何文件存到哪裡

### 3. 砰 — 你準備好了。

## 這些技能為什麼存在

我建立這些技能，是為了修復我在 Claude Code、Codex 與其他 coding agent 上看到的常見失敗模式。

### #1：代理沒做我想要的事

> 「沒有人真正知道自己想要什麼」
>
> David Thomas & Andrew Hunt，《The Pragmatic Programmer》(https://www.amazon.co.uk/Pragmatic-Programmer-Anniversary-Journey-Mastery/dp/B0833F1T3V)

**問題**。軟體開發中最常見的失敗模式是錯位（misalignment）。你以為開發者知道你要什麼，然後你看到他們做的東西 — 才發現它完全沒有理解你。

在 AI 時代這完全相同。你與代理之間存在溝通落差。解法是**詰問 session（grilling session）** — 讓代理問你關於你要建構之物的詳細問題。

**解法**是使用：

- [`/grill-me`](./skills/productivity/grill-me/SKILL.md) — 給非程式碼用途
- [`/grill-with-docs`](./skills/engineering/grill-with-docs/SKILL.md) — 與 [`/grill-me`](./skills/productivity/grill-me/SKILL.md) 相同，但加了更多好東西（見下方）

這是我最受歡迎的技能。它們幫你在開始前先與代理對齊，並深入思考你要做的變更。每次想做變更時，_都_用它們。

### #2：代理太囉嗦了

> 有了共通語言（ubiquitous language），開發者之間的對話與程式碼的表達，全都源自同一個領域模型。
>
> Eric Evans，《Domain-Driven-Design》(https://www.amazon.co.uk/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215)

**問題**：專案一開始，開發者與軟體使用對象（領域專家）通常說的是不同的語言。

我和我的代理之間也有同樣的張力。代理通常被丟進一個專案，要它們邊走邊搞懂行話。於是她們用 20 個字講 1 個字就夠的事。

**解法**是共享語言。那是一份幫代理解碼專案行話的文件。

<details>
<summary>
範例
</summary>

這是我的 `course-video-manager` repo 中的一個 [`CONTEXT.md`](https://github.com/mattpocock/course-video-manager/blob/076a5a7a182db0fe1e62971dd7a68bcadf010f1c/CONTEXT.md) 範例。哪一個比較好讀？

- **BEFORE（改寫前）**："There's a problem when a lesson inside a section of a course is made 'real' (i.e. given a spot in the file system)"
- **AFTER（改寫後）**："There's a problem with the materialization cascade"

這種精簡一次又一次地回報你。

</details>

這內建於 [`/grill-with-docs`](./skills/engineering/grill-with-docs/SKILL.md)。它是一場詰問 session，但幫你與 AI 建立共享語言，並把難以解釋的決策記錄在 ADR。

這有多強大真的很難解釋。它可能是這個 repo 裡最酷的單一技術。試試看就知道了。

> [!TIP]
> 共享語言除了減少囉嗦，還有許多其他好處：
>
> - **變數、函式與檔案都命名一致**，使用共享語言
> - 結果是**代理更容易在程式碼庫中導覽**
> - 代理**思考時花費更少的 token**，因為它能取得更精簡的語言

### #3：程式跑不起來

> 「永遠採取小而深思熟慮的步驟。回饋的速度就是你的速度上限。永遠不要接太大的任務。」
>
> David Thomas & Andrew Hunt，《The Pragmatic Programmer》(https://www.amazon.co.uk/Pragmatic-Programmer-Anniversary-Journey-Mastery/dp/B0833F1T3V)

**問題**：假設你與代理對要做什麼已經對齊。當代理_仍然_產出垃圾時會怎樣？

該檢視你的回饋迴圈了。沒有關於它產出的程式碼實際運作情形的回饋，代理就像在黑暗中飛行。

**解法**：你需要一整套慣常的回饋迴圈：靜態型別、瀏覽器存取與自動化測試。

就自動化測試而言，紅-綠-重構（red-green-refactor）迴圈至關重要。這是代理先寫一個失敗的測試，再修好測試。這幫代理獲得一致的回饋水準，從而產出好得多的程式碼。

我做了一個**[`/tdd`](./skills/engineering/tdd/SKILL.md) 技能**，可以放進任何專案。它鼓勵紅-綠-重構，並給代理大量關於好測試與壞測試的指引。

除錯方面，我也做了**[`/diagnosing-bugs`](./skills/engineering/diagnosing-bugs/SKILL.md)** 技能，把最佳除錯實務包裝成嚴謹的迴圈，逐階段把關。

### #4：我們蓋了一坨爛泥

> 「_每天_都投資在系統的設計上。」
>
> Kent Beck，《Extreme Programming Explained》(https://www.amazon.co.uk/Extreme-Programming-Explained-Embrace-Change/dp/0321278658)

> 「最好的模組是深度的。它們讓大量功能透過一個簡單的介面被存取。」
>
> John Ousterhout，《A Philosophy Of Software Design》(https://www.amazon.co.uk/Philosophy-Software-Design-2nd/dp/173210221X)

**問題**：多數用代理建構的應用程式既複雜又難改。因為代理能大幅加速寫程式，它們也加速了軟體熵。程式碼庫以空前的速度變得複雜。

**解法**是一個激進的 AI 驅動開發新方法：在乎程式碼的設計。

這內建在這些技能的每一層：

- [`/to-spec`](./skills/engineering/to-spec/SKILL.md) 在建立 spec 前盤問你碰了哪些模組

而關鍵的[`/improve-codebase-architecture`](./skills/engineering/improve-codebase-architecture/SKILL.md) 會調查程式碼庫的加深（deepening）機會，並把候選清單交到你手上。我建議每隔幾天就對程式碼庫跑一次。它是調查，不是救援：對真正老舊的程式碼庫，它會找到真正的候選項，但不會替你解開那坨泥。

### 摘要

軟體工程基本功比以往更重要。這些技能是我把這些基本功濃縮成可重複實務的最佳努力，幫你打造職涯中最好的應用程式。盡情享用。

## 參考

這些技能沿著一條軸線區分 — 誰能觸發它們。**User-invoked（使用者觸發）** 的技能只有當你輸入時才能觸發（例如 `/grill-me`）；它們的工作是指揮。**Model-invoked（模型觸發）** 的技能可以由你觸發，_或_當任務符合時由代理自動取得；它們保存可重用的紀律。user-invoked 技能可以觸發 model-invoked 技能，但永遠不能觸發另一個 user-invoked 技能。

### Engineering（工程）

我用於每日程式碼工作的技能。

**User-invoked**

- **[ask-matt](./skills/engineering/ask-matt/SKILL.md)** — 問哪個技能或流程適合你的處境。此 repo 中 user-invoked 技能的路由器。
- **[grill-with-docs](./skills/engineering/grill-with-docs/SKILL.md)** — 同時建立專案領域模型的詰問 session，磨利術語並內嵌更新 `CONTEXT.md` 與 ADR。
- **[triage](./skills/engineering/triage/SKILL.md)** — 讓 issue 通過分診角色的狀態機。
- **[improve-codebase-architecture](./skills/engineering/improve-codebase-architecture/SKILL.md)** — 掃描程式碼庫尋找加深機會，以視覺 HTML 報告呈現，再詰問你挑中的那一個。
- **[setup-matt-pocock-skills](./skills/engineering/setup-matt-pocock-skills/SKILL.md)** — 為工程技能設定此 repo（issue tracker、triage 標籤、領域文件排版）。使用其他工程技能前，每個 repo 執行一次。
- **[to-spec](./skills/engineering/to-spec/SKILL.md)** — 把目前的對話變成 spec 並發布到 issue tracker。不訪談 — 只是綜合你已經討論過的東西。
- **[to-tickets](./skills/engineering/to-tickets/SKILL.md)** — 把任何計畫、spec 或對話拆成一組曳光彈 ticket，每個都宣告其阻塞邊 — 寫成本機檔案的文字，或成為真實 tracker 上的原生阻塞連結。
- **[implement](./skills/engineering/implement/SKILL.md)** — 建構 spec 或一組 ticket 所描述的工作，在事前約定的接縫驅動 `/tdd`，並在 commit 前以 `/code-review` 收尾。
- **[wayfinder](./skills/engineering/wayfinder/SKILL.md)** — 把超出單一代理 session 容量的龐大工作，規劃成 issue tracker 上共享的決策 ticket 地圖 — 一次解決一個，直到通往目的地的路清晰為止。

**Model-invoked**

- **[prototype](./skills/engineering/prototype/SKILL.md)** — 建立一次性原型來回答設計問題 — 狀態/邏輯問題用單一可共享的 HTML 檔案，或從單一路由切換的多種截然不同的 UI 變體。
- **[diagnosing-bugs](./skills/engineering/diagnosing-bugs/SKILL.md)** — 針對困難 bug 與效能退化的嚴謹診斷迴圈：建立一個在此 bug 上轉紅的回饋迴圈 → 最小化 → 假設 → 插樁 → 修復 → 回歸測試。
- **[research](./skills/engineering/research/SKILL.md)** — 以高信任度主要來源調查問題，並把發現記錄成 repo 中帶引用的 Markdown 檔案，以後台代理執行。
- **[tdd](./skills/engineering/tdd/SKILL.md)** — 帶紅-綠-重構迴圈的測試驅動開發。一次一個垂直切片地建構功能或修復 bug。
- **[domain-modeling](./skills/engineering/domain-modeling/SKILL.md)** — 主動建立並磨利專案的領域模型 — 對照詞彙表質疑術語、以邊緣情境壓力測試，並內嵌更新 `CONTEXT.md` 與 ADR。
- **[codebase-design](./skills/engineering/codebase-design/SKILL.md)** — 設計深模組的共享紀律與詞彙：大量行為藏在小型介面之後、放在乾淨的接縫、可透過該介面測試。
- **[code-review](./skills/engineering/code-review/SKILL.md)** — 對固定點以來的 diff 做雙軸審查：**Standards（規範）**（是否遵循 repo 的編碼標準，加上 Fowler 壞味道基線？）與 **Spec（規格）**（是否忠實實作原始 issue/spec？），以平行子代理執行，使兩者互不污染。
- **[resolving-merge-conflicts](./skills/engineering/resolving-merge-conflicts/SKILL.md)** — 逐塊處理進行中的 git merge 或 rebase 衝突，依每側主要來源追溯意圖來解決，然後完成該操作 — 絕不 `--abort`。
- **[wizard](./skills/engineering/wizard/SKILL.md)** — 產生互動式 bash 精靈，引導人類完成只有他們能做的步驟：佈建基礎設施、設定憑證或 CI secrets、走過不熟悉的第三方儀表板，或執行一次性遷移/切換。

### Productivity（生產力）

通用工作流程工具，非程式碼專屬。

**User-invoked**

- **[grill-me](./skills/productivity/grill-me/SKILL.md)** — 針對計畫或設計被不斷訪談，直到設計樹的每個分支都解決。
- **[handoff](./skills/productivity/handoff/SKILL.md)** — 把目前對話壓縮成交接文件，讓另一個代理接手工作。
- **[teach](./skills/productivity/teach/SKILL.md)** — 以目前目錄作為有狀態的教學工作區，跨越多次 session 教使用者新技能或概念。
- **[to-questionnaire](./skills/productivity/to-questionnaire/SKILL.md)** — 把你無法獨自回答的決策，變成唯一能回答那人的 Markdown 問卷 — 非同步填寫，或會議中一起填。它詰問的是關於**寄送**（要寄給誰、你需要什麼回覆），而非主題。
- **[wait-what](./skills/productivity/wait-what/SKILL.md)** — 當訊息一落空就觸發。代理用你缺少的上下文、以淺白英文並使用你 `CONTEXT.md` 的詞彙，重新說明它。

**Model-invoked**

- **[grilling](./skills/productivity/grilling/SKILL.md)** — 針對計畫、決策或想法不斷訪談使用者，直到設計樹的每個分支都解決。`grill-me`、`grill-with-docs`、`triage`、`wayfinder` 與 `improve-codebase-architecture` 背後可重用的訪談原語。
- **[writing-for-agents](./skills/productivity/writing-for-agents/SKILL.md)** — 為代理撰寫文件：技能、AGENTS.md/CLAUDE.md，以及任何代理能透過指標取得的文件。
