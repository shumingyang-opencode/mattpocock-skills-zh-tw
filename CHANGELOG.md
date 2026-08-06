# mattpocock-skills

## 1.2.2

### Patch Changes

- [#766](https://github.com/mattpocock/skills/pull/766) [`4aaccb5`](https://github.com/mattpocock/skills/commit/4aaccb58d40559d7e3c59a029b2290ae5ba538de) 感謝 [@mattpocock](https://github.com/mattpocock)! - 讓 `writing-for-agents` 在 Codex 中再次可被模型觸發。

  - 從 `agents/openai.yaml` 移除 `policy.allow_implicit_invocation: false`。Codex 原本把該技能過濾出模型可見的技能清單，因此它的 description 無法觸發它 — 只有明確的 `$writing-for-agents` 提及才有效。
  - 更新過時的 `interface.display_name` 與 `interface.short_description`，它們仍指著舊的 `writing-great-skills` 技能。
  - 把技能從 `README.md` 與 `skills/productivity/README.md` 的 **User-invoked** 清單移到 **Model-invoked** 清單。

## 1.2.0

### Minor Changes

- [#551](https://github.com/mattpocock/skills/pull/551) [`697d4ce`](https://github.com/mattpocock/skills/commit/697d4ce9742da558fd1ba6697c8e9775e2e302dd) 感謝 [@mattpocock](https://github.com/mattpocock)! - 在每個技能的 Claude Code frontmatter 旁加上 Codex 中繼資料，使整組技能在兩個 harness 中都能運作，無須產生副本。

  - 在每個 `SKILL.md` 旁加上帶 Codex UI 中繼資料（`interface.display_name`、`interface.short_description`）的 `agents/openai.yaml`。
  - 用 `policy.allow_implicit_invocation: false` 標記每個 user-invoked 技能，這是 `disable-model-invocation: true` 的 Codex 對應物，讓 Codex 把它排除在隱含觸發之外，同時顯式 `$skill` 觸發仍有效。
  - 在 `.agents/invocation.md`、`CLAUDE.md` 與已推廣 bucket 的 README 中記錄雙 harness 觸發模型。
  - 新增 `AGENTS.md` 作為指向 `CLAUDE.md` 的 symlink，讓 Codex 讀到相同的 repo 指令。

- [#593](https://github.com/mattpocock/skills/pull/593) [`0f2bdbd`](https://github.com/mattpocock/skills/commit/0f2bdbdb06220d2df3718b8f0483157c6c8a8600) 感謝 [@mattpocock](https://github.com/mattpocock)! - 將 **`to-questionnaire`** 從 `in-progress/` 升級到 **Productivity** bucket，使它隨 plugin 發布。它把你無法獨自回答的決策，變成唯一能回答那人的 Markdown 問卷 — 非同步填寫，或會議中一起完成。

  它的定義性動作是詰問你關於**寄送（send）**，而非主題：一般的詰問 session 盤問主題，而這正是你這裡無法回答的，所以訪談只問問卷要寄給誰、你需要什麼回覆，然後把每個問題瞄準兩者之間的落差。

  現在已接線為已推廣技能 — plugin 條目、頂層 + Productivity README 的 **User-invoked** 下、`docs/productivity/to-questionnaire.md` 的 docs 頁，以及 `ask-matt` 中把它定位為 `/grill-me` 之逆的 Standalone 路線（挖掘別人，不是自己）。

- [#680](https://github.com/mattpocock/skills/pull/680) [`b3376f8`](https://github.com/mattpocock/skills/commit/b3376f8d39848dd08572ec2667da4739a67c8c04) 感謝 [@mattpocock](https://github.com/mattpocock)! - 將 **`wizard`** 從 `in-progress/` 升級到 **Engineering** bucket，使它隨 plugin 發布 — 並把它改為 model-invoked。它產生互動式 bash 腳本，引導人類完成手動程序 — 第三方設定、一次性遷移、A→B 狀態轉換 — 開啟每個 URL、說要點什麼、擷取值，並寫入 `.env` 檔案與 GitHub Actions secrets。

  愉快的 UX 由內建的 `template.sh` 預先解決（帶剩餘時間的進度、確認關卡、含 WSL 的跨平台 URL 開啟、隱藏密碼輸入、冪等的 `.env` 更新、帶優雅退化的 `gh secret`/`gh variable` 寫入、結束時的跳過摘要）。`STAGES` 標記以上的所有東西都是固定的函式庫，絕不手工編輯 — 技能的工作只是界定程序範圍並撰寫其 **stages**。

  屬於 Engineering 而非 Productivity：它讀取 `.env*`、`docker-compose*`、框架設定與 `.github/workflows/` 中的每個 `secrets.*`/`vars.*` 參照來界定自己的範圍、寫 CI secrets，並以 `bash -n` 與 `shellcheck` 驗證輸出。

  因為它是 model-invoked，代理在遇到只有人才能執行的步驟的那一刻就能伸手，而不是把編號的指示倒進對話並祈禱你照做。輸入 `/wizard` 跟以前一樣有效 — 模型觸發永遠只會*增加*代理的觸及範圍。description 寫成決定它何時觸發的指標：它產生什麼、四個觸發分支（佈建基礎設施、設定憑證或 CI secrets、走過不熟悉的第三方儀表板、一次性遷移或切換），以及一個明確的非觸發條件 — 代理自己能做的步驟不要觸發它。代理能做的，就該代理做；wizard 是給你不會交給代理的點擊、核准與儀表板行程。寫入任何一行前的 stage-list 確認，現在同時充當代理在構建中途觸發它時的提案。

  現在已接線為已推廣技能 — plugin 條目、頂層 + Engineering README 的 **Model-invoked** 下、`docs/engineering/wizard.md` 的 docs 頁，以及 `ask-matt` 中給只有人能做的步驟的 Standalone 路線。模型觸發也讓它脫離 [#693](https://github.com/mattpocock/skills/issues/693) 的影響，該 issue 會把 user-invoked 技能從 Claude 桌面與網頁介面的列表移除。

- [#763](https://github.com/mattpocock/skills/pull/763) [`77d207e`](https://github.com/mattpocock/skills/commit/77d207ef03219cc603e2832e1159cbdd1c91818e) 感謝 [@mattpocock](https://github.com/mattpocock)! - 把 **`prototype`** 技能圍繞兩個想法重塑：demo 是**單一可共享的 HTML 檔案**，而原型是**主要來源**。

  邏輯分支現在產出單一自含檔案（純 HTML/CSS/JS，無建置、無伺服器），取代終端機應用程式 — 非開發者可以雙擊開啟，並用他們自己的領域語言操作：標籤化的狀態面板、永遠可用的自由操作按鈕，以及一組分頁的**引導式逐步操作（guided walkthroughs）**，每個都是一個情境，下面帶要依序按下的按鈕。可攜的純邏輯模組仍會搬進真正的程式碼；HTML 外殼才是被丟棄的部分。

  Throwaway（丟棄）不再意味著刪除。原型回答完問題後不會被移除，而是被捕捉為一次性分支（`prototype/<name>`，離開 main）上的可執行證據，並在實作 issue 上留下指向它的脈絡指標 — 如此 main 分支只保留經過驗證的決策，而探索過程保持可尋。答案（判定 + 問題）仍持久地捕捉在 issue/ADR/commit 中。

- [#536](https://github.com/mattpocock/skills/pull/536) [`42a5b70`](https://github.com/mattpocock/skills/commit/42a5b70fcacc7baff1977b13f3919fb2f63af14e) 感謝 [@mattpocock](https://github.com/mattpocock)! - 以原生 **Claude Code plugin** 發布技能集，並列入 Claude Code 的官方 marketplace。現在你可以把已推廣技能訂閱為受管、唯讀的 bundle，而非複製可編輯檔案：

  ```bash
  claude plugins install mattpocock-skills
  ```

  或從 session 內：

  ```
  /plugin install mattpocock-skills
  ```

  無須先新增 marketplace — 官方 marketplace 預設已設定。

  `.claude-plugin/plugin.json` 帶有完整的 plugin 中繼資料（version、description、author、license、keywords）以及已推廣技能的顯式清單。`skills.sh` 仍是通用安裝程式（也是 Codex 與其他 harness 目前的路徑）；原生 Codex plugin 已暫緩 — 原因見 `.agents/adr/0002-ship-as-a-claude-code-plugin.md`。

- [#751](https://github.com/mattpocock/skills/pull/751) [`355fa74`](https://github.com/mattpocock/skills/commit/355fa7420b418af838998f7ec4365ceda1c8dfcc) 感謝 [@mattpocock](https://github.com/mattpocock)! - 新增 **`wait-what`** — 一個針對模型囉嗦的一個字矯正。訊息一落空的瞬間輸入它，代理就會重新說明：一點上下文、ASD-STE100 簡化技術英文，以及你 `CONTEXT.md` 中的共通語言。User-invoked，只有三行。

  機制就是名稱本身。精簡技能會因為變長而失敗 — 400 行的技能仍讓模型囉嗦 — 所以這一個技能是單一精確的領頭詞，除此之外什麼都沒有。描述*輸出*的名稱（`/tldr`、`/no-fluff`）會讓模型剪裁字詞、讓你更迷失；命名*聽者*的狀態則一次要求兩半 — 更少的字**以及**你缺少的上下文。它也重用你全域 `CLAUDE.md` 中既有的領頭詞，因此技能、`CLAUDE.md` 與每個 `CONTEXT.md` 都伸手向同一組 token。

  它修復一則訊息；它不預防下一則。行話的解藥是先用 `/grill-with-docs` 建立共享語言；當你還沒有共享語言時，這就是你伸手的東西。

- [#763](https://github.com/mattpocock/skills/pull/763) [`77d207e`](https://github.com/mattpocock/skills/commit/77d207ef03219cc603e2832e1159cbdd1c91818e) 感謝 [@mattpocock](https://github.com/mattpocock)! - 把 `/wayfinder` 的單位命名為**決策 ticket（decision ticket）**，並用子代理燒掉研究 ticket。

  人們一直把 wayfinder ticket 讀成普通的_實作_ ticket — 一個要執行的建置切片 — 而 wayfinder 其實把它們用作**決策 ticket**：其解決方案是決策的問題。技能 description 與開頭一行現在引入此術語（並說明它為什麼是決策 ticket），`ask-matt`/engineering README 的簡介與 docs 頁同步 — 而術語確立後「ticket」仍是日常用字。`CONTEXT.md` 把 **Decision ticket** 記錄為領域術語，因此「avoid: ticket」的指引不再與 wayfinder 刻意使用這個字相矛盾。

  研究 ticket 不再停置給另行啟動的 session。研究仍是一個真實的 ticket 類型 — 它是下游決策所依賴的真正共享阻塞項，而那個依賴正是前沿的阻塞邊存在的目的。改變的是它如何解決：因為研究是 AFK 的，繪圖不會停下來讀它。建立 ticket 之後，繪圖 session 為每個研究 ticket 觸發一個 `/research` 子代理，平行把它們燒掉，把發現捕捉在一次性 `research/<name>` 分支並帶脈絡指標。研究 ticket 是「一個 session 一個 ticket」的唯一例外。

- [#763](https://github.com/mattpocock/skills/pull/763) [`77d207e`](https://github.com/mattpocock/skills/commit/77d207ef03219cc603e2832e1159cbdd1c91818e) 感謝 [@mattpocock](https://github.com/mattpocock)! - **破壞性變更：** 把 **`writing-great-skills`** 改名為 **`writing-for-agents`**、重組它，並新增領頭詞。

  此參考現在涵蓋代理消費的任何文件 — 技能、`AGENTS.md`/`CLAUDE.md`、透過指標取得的 docs — 而不只是技能。`GLOSSARY.md` 併入 `SKILL.md`（每個術語一個權威處理；`_Avoid_` 同義詞清單與獨立的 Predictability 定義已移除）；技能專屬的機制（frontmatter、model- vs user-invoked、路由器技能、拆分的觸發切分）揭露到新的 `SKILL-MECHANICS.md`。技能現在是 **model-invoked**：建立或編輯技能、或修改 `AGENTS.md`/`CLAUDE.md` 時觸發。`ask-matt` 的指標已更新。以新名稱重新安裝；舊名稱已消失（無別名）。

  精簡章節新增**快取**。單一事實來源現在延伸到文件之外進入環境 — `package.json` 的 scripts、設定檔、目錄排版、`--help` 輸出本身都是權威，所以重述它們的文件是查詢的快取，只有當查詢昂貴時才值得其負擔。正面目標：快取代理無法用「看」找到的東西（未寫下的慣例、選擇背後的理由、任何設定都不會坦白的陷阱），並把一個檔案、一個指令的查詢留給環境 — 它們在那裡不會過時。

- [#533](https://github.com/mattpocock/skills/pull/533) [`45afd80`](https://github.com/mattpocock/skills/commit/45afd8074a8b7de5fe073845d080fa9dd6c429fa) 感謝 [@mattpocock](https://github.com/mattpocock)! - 在 **`improve-codebase-architecture`** 技能的 Explore 步驟新增 YAGNI 範圍過濾器。它不再均勻掃描整個 repo，而是把範圍侷限在變更真正落地的地方：如果你指定方向就採用，否則它讀取最近約 20 則 commit 訊息，把探索偏向積極開發中的路徑。沒人碰的程式碼裡的加深機會，是永遠不會兌現的重構 — 槓桿只在你不斷編輯的地方才有回報 — 因此報告不再整理 repo 沉睡角落的雜物。

### Patch Changes

- [#763](https://github.com/mattpocock/skills/pull/763) [`77d207e`](https://github.com/mattpocock/skills/commit/77d207ef03219cc603e2832e1159cbdd1c91818e) 感謝 [@mattpocock](https://github.com/mattpocock)! - 磨利 `/ask-matt` — 路由器現在涵蓋階段邊界、兩個 wayfinder 錯誤，以及兩個它從未提及的技能。

  **階段邊界（Phase boundaries）。** **phase** 是 session 內的一塊工作 — 詰問、實作、QA — 而兩者之間的邊界正是你決定怎麼處理已建立的上下文的地方。兩個項目的 `Crossing sessions` 章節被帶全部五個選項的決策樹取代（**continue**、`/clear`、`/handoff`、**subagent**、`/compact`），推理揭露在新的 `PHASE-BOUNDARIES.md`。伴隨三個修正：

  - **`/handoff` 被過度銷售。** 它被讀成上下文視窗之間的通用橋樑。它其實很窄：只有當某些東西必須*移動*時你才需要它 — 新的 harness、新目錄、同事、或中途分叉的支線任務。它買到的是可攜性。
  - **`/compact` 是預設，不是第一選擇。** 它位於決策樹底部，在四個更便宜或更精確的問題之後。從那裡開始會產生一個對摘要壓平的任何東西都自信地搞錯的 session。
  - **兩個分支原本完全缺失。** **Continue** 是最先該排除的選項 — 它是唯一讓對話保持為主要來源而非其摘要的動作 — 而 **subagent** 處理任何範圍緊到足以 AFK 執行的任務。

  上下文衛生的逃生門現在說 `/compact` 而非 `/handoff`（同 harness、同目錄、在邊界上 — handoff 條款不適用），智慧區數字也從約 120k 更新為約 150k token。

  **Wayfinder 路由。** 人們對這個最重、認知上最費力的流程最常犯的兩個錯誤：

  - **過度伸手。** 它比單次 grill 更慢更密，所以被標記為最重的流程，並保留給真正裝不進一個 session 的想法 — 範圍良好的功能屬於 `/grill-with-docs`，不屬於這裡。
  - **交接時迷失方向。** 地圖清晰時，wayfinder 交接，不建構：從 `/to-spec` 併入主流程（它把地圖的連結決策收攏成可建構的計畫），而非把地圖直接迴圈進 `/implement`。直衝 `/implement` 只留給真的很小的成果。

  **缺失的路線。** `/grilling` 與 `/resolving-merge-conflicts` 原本完全不在路由器中，現在已加入，而 `grill-me` 以你是否在工作目錄中為準，從 `grill-with-docs` 分出。

- [#502](https://github.com/mattpocock/skills/pull/502) [`44eed54`](https://github.com/mattpocock/skills/commit/44eed545186ffd0263e8004867750b80cfddd215) 感謝 [@mattpocock](https://github.com/mattpocock)! - 讓 `/setup-matt-pocock-skills` 更友善，並讓 local-markdown tracker 對齊目前的 spec。

  - **Triage 標籤**現在只在 `triage` 技能已安裝時才被詢問，且是單一推薦-是問題（「保留預設的 triage 標籤？」），而非覆寫式的盤問。`triage` 未安裝時，該章節 — 以及 `docs/agents/triage-labels.md` — 被跳過。
  - **外部 PR 作為請求介面**不再是設定問題。GitHub/GitLab 模板仍帶旗標，預設關閉；使用者日後可在 `docs/agents/issue-tracker.md` 開啟它。
  - **領域文件**預設為單上下文而不詢問；只有當 repo 顯示 monorepo 訊號時才提供多上下文。
  - **Local-markdown tickets** 現在是 `.scratch/<feature>/issues/<NN>-<slug>.md` 下每個 ticket 一個檔案 — 絕不是單一合併的 `tickets.md`。`/to-tickets` 與 local issue-tracker 模板現在一致，spec 檔案是 `spec.md`（而非 `PRD.md`），以對齊 `/to-spec`。

  `setup-matt-pocock-skills` 與 `to-tickets` 的 docs 頁已重新同步。

- [#532](https://github.com/mattpocock/skills/pull/532) [`170ad48`](https://github.com/mattpocock/skills/commit/170ad48655825783d0193e850e31a9aac957bb95) 感謝 [@mattpocock](https://github.com/mattpocock)! - 將 **`grilling`** 的措辭改為通用用途。它的 description 與正文不再把訪談範圍限定於軟體計畫：「this plan」→「this」、「enact the plan」→「act on it」、「exploring the codebase」→「exploring the environment」。技術不變；它現在讀起來像對任何計畫、決策或想法的壓力測試。

- [#593](https://github.com/mattpocock/skills/pull/593) [`a4b2009`](https://github.com/mattpocock/skills/commit/a4b2009a1a3ac9575506c10b4c84f08f9bba7a38) 感謝 [@mattpocock](https://github.com/mattpocock)! - 把 **`grilling`** 從一次一題重作為一輪一輪。它現在繪製決策樹，並在單一編號的回合中問整個**前沿** — 每個前置條件已解決的問題 — 再從使用者的回答重新計算前沿，問下一輪。同樣 13 個問題落在約 3 回合，而非 13 回合。環境能回答的事實分派給背景子代理，因此研究絕不阻塞回合：只有一個進行中探索下游的問題才等它。session 在前沿空掉時結束。

  每回合的每個問題以一個固定形狀發射 — `❓ **Q1** - **<title>**`，接著是正文（散文或多選），然後是推薦放在自己的 `➡️` 行。一輪讀起來像可掃描的編號清單，每個推薦與問題視覺分離，因此你可以按編號回答，而不是把問題引述回去。

  `grill-me`、`grill-with-docs` 與 `triage` 也一次跑一輪前沿 — `triage` 的 grill 步驟與 `grilling` 的 Codex `short_description` 現在如此陳述，而非描述舊的節奏。一次一題的退出機制（你全域 `CLAUDE.md` 中的一行）不變。

- [#752](https://github.com/mattpocock/skills/pull/752) [`c66bdee`](https://github.com/mattpocock/skills/commit/c66bdeeee002d81e3f8b21403c07f9a0d7bea6da) 感謝 [@mattpocock](https://github.com/mattpocock)! - 從 repo 移除六個技能。它們都不在 Claude Code plugin 中，但六個都可透過 [skills.sh](https://skills.sh/mattpocock/skills) 安裝 — 它服務 repo 中的每個技能 — 所以這就是離開該列表的項目，以及每個的去向。

  四個退休技能，每個都已由做得更好的技能吸收：

  - **`ubiquitous-language`** → **`/domain-modeling`**，它建立並維護整個領域模型，而非從一次對話傾印詞彙表。
  - **`design-an-interface`** → **`/codebase-design`**。沒有遺失任何東西：「design it twice」技術 — 平行子代理產生截然不同的設計，源自 Ousterhout — 以 `DESIGN-IT-TWICE.md` 內建在該技能中。
  - **`qa`** → **`/triage`** 與 **`/to-tickets`**。
  - **`request-refactor-plan`** → **`/to-spec`** 與 **`/improve-codebase-architecture`**。

  還有兩個本來就只是我的 — 綁在我的機器上，從不打算給別人。`personal/` bucket 隨它們離開：

  - **`edit-article`**
  - **`obsidian-vault`**，它把路徑硬編碼到我自己 的 Obsidian vault。

  `skills/deprecated/` 保持為 bucket，現在是空的。`skills/in-progress/` 不變，現在照它實際的樣子描述：beta 頻道，刻意發布，可透過 skills.sh 一次安裝一個技能。

- [#734](https://github.com/mattpocock/skills/pull/734) [`a2f9333`](https://github.com/mattpocock/skills/commit/a2f9333669ff53db762c87ecda5a15442060a3be) 感謝 [@mattpocock](https://github.com/mattpocock)! - 完成 `to-prd` → `to-spec` 改名：「spec」現在是發布文字中唯一的術語。

  - **`to-spec`** 不再以「you may know this document as a PRD」開頭 — 括號從技能與其 docs 頁移除。Local-markdown tracker 模板移除同一個迴避語。
  - **`code-review`** 談的是原始 issue/spec，而非 issue/PRD — 在其 frontmatter description、雙軸摘要與 spec-source 搜尋順序中。兩個 README 已重新同步。
  - **GitHub 與 GitLab tracker 模板**現在說「Issues and specs for this repo live as GitHub/GitLab issues」— 它們在 local 模板更新時被留在「PRDs」，因此過時的術語傳播進每個被寫入的 repo。
  - **`docs/engineering/research.md`** 原本指向 `https://aihero.dev/skills-to-prd`，這是改名技能的死亡 slug；它現在像其他十九個 docs 頁一樣連結 `to-spec`。

  CHANGELOG 與既有 changesets 在記錄改名本身的地方仍指名 PRD，這是正確的。

## 1.1.0

### Minor Changes

- [#406](https://github.com/mattpocock/skills/pull/406) [`930a450`](https://github.com/mattpocock/skills/commit/930a450089f77a49af09001d955db8452a4b867d) 感謝 [@mattpocock](https://github.com/mattpocock)! - 讓 **`ask-matt`** 路由器跟上完整的技能集。它現在繪製了原本缺失的五個技能：**`tdd`**（織入主流程，作為 `implement` 驅動的紅-綠引擎）、**`diagnosing-bugs`**（新的「Something's broken」入口 — 原本沒有給 bug 的路線）、**`domain-modeling`** 與 **`codebase-design`**（新的「Vocabulary underneath」章節）、以及 **`grilling`**（共享訪談原語）。`prototype` 被充實為獨立技能，description 也從「user-invoked skills」拓寬為「the skills」。`CLAUDE.md` 新增一條維護規則，讓未來任何技能的新增/改名/移除或流程變更，除了既有的 docs 頁重新同步規則外，也觸發 `ask-matt` 重新檢查。

- [#464](https://github.com/mattpocock/skills/pull/464) [`639df6e`](https://github.com/mattpocock/skills/commit/639df6e7386dfddc739b2aecdeff37a876f2483b) 感謝 [@mattpocock](https://github.com/mattpocock)! - 推廣並強化 **`code-review`**。進行中的 **`review`** 技能改名為 **`code-review`**，並從 `in-progress/` 移到 `engineering/`：它現在隨 plugin 發布、列在頂層與 Engineering README（Model-invoked）、並在 `docs/engineering/code-review.md` 有 docs 頁。`/implement` 技能與 docs 指向 `/code-review`。

  它在 Standards 軸上也新增了常開的 **Fowler 壞味道基線** — 約 12 個精心挑選的高訊號「Bad Smells in Code」（Mysterious Name、Duplicated Code、Feature Envy、Data Clumps、Primitive Obsession、Repeated Switches、Shotgun Surgery、Divergent Change、Speculative Generality、Message Chains、Middle Man、Refused Bequest）內建進 `SKILL.md` 作為固定基線，與 repo 文件化的任何東西並存，而非新的第三軸。兩條綁定規則保護它：repo 文件化的標準覆寫基線，且每個壞味道都回報為判斷，絕不是硬性違規。

- [#464](https://github.com/mattpocock/skills/pull/464) [`639df6e`](https://github.com/mattpocock/skills/commit/639df6e7386dfddc739b2aecdeff37a876f2483b) 感謝 [@mattpocock](https://github.com/mattpocock)! - 在兩個前線磨利 **`grilling`**。

  **確認關卡。** 在你確認共享理解已達成之前，代理不會執行計畫 — 把技能既有的「shared understanding」完成標準變成明確的停止關卡。`description` 也招募已預訓練的 **`grill`** 領頭詞（「Grill the user relentlessly」）來磨利觸發，docs 頁已重新同步。

  **事實 vs 決策。** Grilling 現在把_事實_（查出來 — 探索程式碼庫）與_決策_（每個交給人並等回答）分開。舊的籠統行 —「如果問題可以藉由探索程式碼庫回答，就改為探索程式碼庫」— 是為即時人類案例寫的，但一旦另一個技能在「解決這個 ticket」的框架內跑 grilling，它讀起來就像也允許自主回答_決策_。分開兩者讓詰問代理不會衝上前自問自答。

- [#463](https://github.com/mattpocock/skills/pull/463) [`af6d692`](https://github.com/mattpocock/skills/commit/af6d6922c3e2b5288eef155346cbe319e4ed3bd0) 感謝 [@mattpocock](https://github.com/mattpocock)! - 為 **`writing-great-skills`** 新增兩個相鄰的 Steering 失敗模式，兩者都關於你認為「關掉」的語言如何仍然引導代理。**否定（Negation）** — 大象 — 是以禁止引導：指名_不要_做的事會把被禁的行為拖進上下文，讓它_更_可用而非更少（_不要想大象_），所以解藥是提示**正向**。**負空間（Negative Space）** — 虛無 — 是對你_省略_之物所造成的引導的盲目：技能拒絕的每個決策都被委派給代理的先驗，而非保持中性，所以解藥是讀草稿找出它的沉默，並刻意決定每個省略（填上它，或留成真正的**分支**）。保持為兩條而非一條 — 它們帶有不同的診斷與不同的解藥 — 每個都是完整的 `GLOSSARY.md` 條目加上 `SKILL.md` 失敗模式項目，與其他每個失敗模式的承載方式一致。

- [`850873c`](https://github.com/mattpocock/skills/commit/850873cd73d5f81826ebf512ad35d2b1e113001f) 感謝 [@mattpocock](https://github.com/mattpocock)! - 讓 **`prototype`** 技能變為 model-invoked，使代理能自主伸手（其他技能也能）。它的 description 圍繞領頭詞 _prototype_ 重寫 — 回答設計問題的一次性程式碼 — 每個分支一個觸發（狀態/邏輯健全性檢查，或 UI 探索）。

- [#409](https://github.com/mattpocock/skills/pull/409) [`0d74d01`](https://github.com/mattpocock/skills/commit/0d74d01cbc64ca27778a49b38599f70c534e76a0) 感謝 [@mattpocock](https://github.com/mattpocock)! - 新增 **`research`** 技能 — 一個小型、model-invoked 的技能，啟動**背景代理**以**主要來源**（官方文件、原始碼、spec、第一方 API）調查問題，然後在 repo 存放此類筆記的地方留下一份帶引用的 Markdown 檔案。它是可委派的閱讀雜務：它讀的時候你繼續工作，然後拿回一份可以拿來詰問、規劃或設計的文件。列在頂層與 Engineering README（Model-invoked）、加入 `.claude-plugin/plugin.json`、在 `docs/engineering/research.md` 有 docs 頁，並在 `ask-matt` 中路由為 Standalone。

- [#469](https://github.com/mattpocock/skills/pull/469) [`a0329ba`](https://github.com/mattpocock/skills/commit/a0329ba95751f58566ed7ab484475917a68f1629) 感謝 [@mattpocock](https://github.com/mattpocock)! - 把 **`to-issues`** 技能拆成精簡的 **Process** 與 **Reference** 章節，並教它處理**大範圍重構（wide refactor）** — 單一機械性變更（如改名欄位）的**影響半徑（blast radius）** 扇形展開橫跨整個程式碼庫，一次破壞數千個呼叫點，使任何垂直切片都無法轉綠。撰寫步驟現在指向兩個同處的參考區塊：普通曳光彈用的 **Vertical slice rules**，與 **Wide refactors** — 它用**擴展-收縮（expand–contract）**（在舊形式旁擴展新形式、按影響半徑分尺寸批量遷移呼叫點、再收縮掉舊形式）切分變更，使 CI 一批批保持綠 — 或做不到時，只在最終的「整合並驗證」issue 才停。issue 內文模板也移進 Reference。

- [#464](https://github.com/mattpocock/skills/pull/464) [`386d4ff`](https://github.com/mattpocock/skills/commit/386d4ff719a7c420ad1454232d0436b01f1b8c17) 感謝 [@mattpocock](https://github.com/mattpocock)! - 統一律畫技能。**`to-prd` 改名為 `to-spec`** —「spec」現在是單一的貫穿術語（為了可發現性，它仍以「you may know this document as a PRD」開頭）。**`to-plan` 與 `to-issues` 合併成單一 `to-tickets` 技能，`to-issues` 被刪除。**

  `to-tickets` 把計畫、spec 或對話拆成一組 **tickets** — 曳光彈垂直切片，每個宣告其**阻塞邊（blocking edges）**。這個產物依 `/setup-matt-pocock-skills` 設定的 tracker 有兩種讀法：**本機檔案**（`tickets.md`）把邊寫成文字，你手工自上而下處理；**真實 tracker** 把它們寫成原生阻塞連結，因此任何阻塞項已完成的 ticket 都在前沿，且可以同時跑多個代理。邊無論如何都活在 ticket 中 — 媒介只決定是否有任何東西平行作用於它們。

  發布偏好 tracker 的**原生子 issue** 給 parent → slice，**原生阻塞邊**給 `Blocked by`（tracker 支援時），保留 `## Parent`/`## Blocked by` 內文章節作為備援。「What to build」模板指向 `/prototype` 程式碼所在處，而非內嵌其中的片段。

  `ask-matt` 的主流程現在路由 `idea → /to-spec → /to-tickets → /implement`，並在 `docs/engineering/to-spec.md` 與 `docs/engineering/to-tickets.md` 有人看的 docs 頁。

- [#464](https://github.com/mattpocock/skills/pull/464) [`0557d57`](https://github.com/mattpocock/skills/commit/0557d57579d9b3d39839fdaf8d4a6542b17539ce) 感謝 [@mattpocock](https://github.com/mattpocock)! - 把 wayfinder 在 docs 中的地位定為**情境式入口（situational on-ramp）**，而非新的主要入口流程 — grill 主導的 _idea → ship_ 鏈保持正門（把 wayfinder 立為預設脊椎是 v2 規模的動作，不是 1.1）。**`ask-matt`** 路由器現在指名 wayfinder 的具體觸發 — 綠地專案或超大功能建置，超出一個 session 容量 — 而兩個 grill 正門（**`grill-me`**、**`grill-with-docs`**）為裝不進一個 session 的成果向上指向 wayfinder，因此入口從讀者真正開始的地方即可發現。

- [#464](https://github.com/mattpocock/skills/pull/464) [`639df6e`](https://github.com/mattpocock/skills/commit/639df6e7386dfddc739b2aecdeff37a876f2483b) 感謝 [@mattpocock](https://github.com/mattpocock)! - 升級並重新定位 **`wayfinder`** — 規劃超出單一代理 session 容量的龐大工作的技能。它從 `in-progress/` 移到 `engineering/`（plugin 條目、頂層 + Engineering README 的 **User-invoked** 下、`docs/engineering/wayfinder.md` 的 docs 頁、`ask-matt` 中的路線），以成熟技能落地。讓它達成的改名與重新定位：

  - **`decision-mapping` 改名為 `wayfinder`**，以 `/wayfinder` 觸發。「Decision map」既行話又不準確 — 只有一種 ticket 類型真的是決策。重新定位改為穿過迷霧般的問題繪製路線，給出單一連貫的領頭詞框架 — **fog of war（戰爭迷霧）**、**frontier（前沿）**、**the map（地圖）** — 而非層層疊加發明的術語。
  - **目的地作為領頭詞。** Wayfinding 找到通往目的地的*路*；它不衝去建構它。命名目的地是繪圖的第一個動作 — 它固定範圍、形塑每個 ticket — 因此地圖增加 `## Destination` 欄位，每個 session 都朝它定位，而 triage 在任何 ticket 存在之前就釘住它。
  - **規劃，不要動手。** 地圖產出**決策，而非交付物**；當有人在建構之前已沒有什麼可決策時，它就完成。成果可以在其 Notes 中覆寫這個設定。
  - **地圖是指標，不是倉庫。** 一個決策確切存在於一個地方 — 它的 ticket — 因此地圖只摘要與連結，絕不重述；把迷霧升級為 ticket 會清空升級過的那塊，使任何東西都不會殘留在兩個地方。
  - **預設協作。** 地圖從本機 Markdown 檔案移到 repo 的 issue tracker：單一 `wayfinder:map` issue，其 tickets 是它的子 issue — 團隊可觀看的單一共享 URL。Session 以低解析度載入地圖，並按需放大到 tickets。Wayfinder 保持 tracker 無關（GitHub、GitLab、local-markdown），透過 `docs/agents/issue-tracker.md` 的指標，而 `setup-matt-pocock-skills` 種下「Wayfinding operations」章節。
  - **以指派認領，而非標籤。** Session 透過把 ticket 指派給驅動開發者來認領它 — 受指派者*就是*認領 — 把標籤詞彙解放為只有 `wayfinder:<type>`。
  - **原生阻塞。** 阻塞偏好 tracker 的原生依賴關係，它會在 tracker 自己的 UI 中視覺渲染前沿，使人無須打開地圖就能看到什麼可拿。GitHub 與 GitLab 模板寫明原生配方，附內文慣例備援。
  - **迷霧 vs 超出範圍，分開。** 兩個命名清楚的圖章節 — `## Not yet specified`（範圍內的迷霧，前沿推進時升級）與 `## Out of scope`（被判定超出目的地的工作，已關閉，永不升級）— 如此超出目的地的讀起來就不會像是可拿的前沿。
  - **第四種 `task` ticket 類型。** 給阻塞決策的具體手動工作（佈建存取權、移動資料、註冊服務）— 唯一*動手*而非決策的類型，藉由解除決策阻塞而贏得地位。
  - **HITL / AFK ticket 分類。** 每個 ticket 類型是 **HITL**（人在迴圈中 — 詰問、原型）或 **AFK**（代理獨自 — 研究；task 兩者皆可）。HITL ticket 只能透過即時交流解決，因此「等人」從標籤中自然浮出 — 自問自答的詰問代理，依定義就是破壞了 HITL。（這修好了學生們回報的 `/wayfinder` 詰問_它自己_而非詰問人的現象。）
  - **恢復無迷霧早期退出。** 若開場的寬度優先詰問沒有浮現任何迷霧，旅程小到一個 session 就夠 — 於是它停下來問你想怎麼進行，而非建構一張沒人要的地圖。

### Patch Changes

- [#464](https://github.com/mattpocock/skills/pull/464) [`639df6e`](https://github.com/mattpocock/skills/commit/639df6e7386dfddc739b2aecdeff37a876f2483b) 感謝 [@mattpocock](https://github.com/mattpocock)! - 把 **`tdd`** 重塑為純參考技能，並新增缺失的反模式。

  **純參考。** 紅 → 綠 → 重構迴圈由模型已經握有的領頭詞錨定，因此逐步的 Workflow 大體上是在重述迴圈。移除 Workflow 與每週期檢查表；把它們唯一耐久的主意 — 垂直切片 / 曳光彈 — 折進 Anti-patterns 章節與簡短的 Rules-of-the-loop 清單。引入 **seam** 作為測試放哪裡的領頭詞：只在事前約定的接縫測試，並在任何測試寫出前與使用者確認。也移除重構階段 — TDD 現在是紅 → 綠；重構屬於審查階段，因此重構規則與 `refactoring.md` 移出（其家是 `code-review`）。

  **同義反覆測試。** 新增同義反覆測試反模式：斷言用程式碼計算的方式重新計算的測試，會因建構而通過、卻給零信心 — 與已涵蓋的實作耦合反模式不同。在相同位置新增為同級：一條 Philosophy 原則（期望值必須來自獨立的真相來源）、一條檢查表關卡，以及 `tests.md` 中的一對 BAD/GOOD 範例。

- [`e00eadb`](https://github.com/mattpocock/skills/commit/e00eadb4bb32c3d5a631ead1a5ed5d6a7c5f74e2) 感謝 [@mattpocock](https://github.com/mattpocock)! - 擴充 **`triage`** 技能以分診外部 pull request，把 PR 視為附帶程式碼、流經相同角色與狀態機的 issue。PR 與 issues 並排流動（由 per-repo 設定開關把關）、發現介面只浮現外部 PR、僅限 bug 的「reproduce」步驟概括為單一「verify the claim」步驟、冗餘檢查把已實作的請求解析為 `wontfix` 而不污染超出範圍的知識庫。`setup-matt-pocock-skills` 為 GitHub/GitLab 新增 PRs-as-a-request-surface 開關。

- [#472](https://github.com/mattpocock/skills/pull/472) [`d869d45`](https://github.com/mattpocock/skills/commit/d869d45afc32beab1c2d1350f8de5e81589512cd) 感謝 [@mattpocock](https://github.com/mattpocock)! - 修復 **`wayfinder`** 硬編碼 issue-tracker 文件路徑的問題，這破壞了整套技能依賴的間接層。

  `to-issues`、`to-prd` 與 `triage` 從不指名路徑 — 它們透過 `setup-matt-pocock-skills` 寫進 `CLAUDE.md`/`AGENTS.md` 的 `### Issue tracker` 區塊解析 tracker，該區塊指向 tracker 文件所在處。Wayfinder 反而釘住字面上的 `docs/agents/issue-tracker.md`，因此在把代理文件放在別處的 repo 中，它會默默回退到 local-markdown tracker — 即使是 `CLAUDE.md` 清楚宣告 GitHub issues 的那種。它現在透過同一個指標解析文件，並按名稱讀取其「Wayfinding operations」章節，讓間接層在整套技能中保持一致。

## 1.0.1

### Patch Changes

- [`d20ee26`](https://github.com/mattpocock/skills/commit/d20ee2684e2a9442698ac3c1e0f2c5b68c4cf296) 感謝 [@mattpocock](https://github.com/mattpocock)! - 讓 **`teach`** 技能重用優先。課程現在由 `./assets/` 中可重用的**元件**建立 — 樣式表、測驗 widget、模擬器、圖表輔助。重用是預設：代理在撰寫課程前先讀 `./assets/`、從既有的東西建立，並把任何新的、可重用的東西抽成元件，而非內嵌它。

## 1.0.0

### Major Changes

- [`47bde84`](https://github.com/mattpocock/skills/commit/47bde84da032afb2e5058f997f3bbca47d321dbd) 感謝 [@mattpocock](https://github.com/mattpocock)! - 新增 **`ask-matt`** 技能 — 一個 user-invoked 路由器，為你的處境指出正確的技能或流程。

  **破壞性變更：** `ask-matt` 在此 repo 的其他 user-invoked 技能上路由，因此它預期它們已安裝。

- [`47bde84`](https://github.com/mattpocock/skills/commit/47bde84da032afb2e5058f997f3bbca47d321dbd) 感謝 [@mattpocock](https://github.com/mattpocock)! - 新增共享設計技能，並把既有技能重新接線到它們。

  - 新的 **`codebase-design`** 技能 — 深模組詞彙（module、interface、depth、seam、adapter）與「把大量行為放在小型介面之後」的原則。先前住在 `improve-codebase-architecture/LANGUAGE.md` 的語言現在住在這裡，泛化為跨技能重用。
  - 新的 **`domain-modeling`** 技能 — 主動建立並磨利專案的領域模型，對照詞彙表壓力測試術語，並保持 `CONTEXT.md` 與 ADR 更新。
  - `improve-codebase-architecture` 現在從 `/codebase-design` 取得架構詞彙，從 `/domain-modeling` 取得領域模型。
  - `tdd` 現在依賴 `/codebase-design` 取得介面設計指引 — 其內嵌的 `deep-modules.md`/`interface-design.md` 筆記已移除，改用共享技能。
  - `grill-with-docs` 現在透過 `/domain-modeling` 內嵌建立領域模型。

  **破壞性變更：** 這些技能現在依賴新的 `codebase-design`/`domain-modeling` 技能，因此你也必須安裝它們。

- [`47bde84`](https://github.com/mattpocock/skills/commit/47bde84da032afb2e5058f997f3bbca47d321dbd) 感謝 [@mattpocock](https://github.com/mattpocock)! - 移除 **`caveman`** 與 **`zoom-out`** 技能。

  - `caveman` 是另一個我正在測試的技能的重複，從不打算公開。
  - `zoom-out` 在實務中未被使用，因此已從 repo 移除。

  **破壞性變更：** 兩個技能都已移除。

- [`47bde84`](https://github.com/mattpocock/skills/commit/47bde84da032afb2e5058f997f3bbca47d321dbd) 感謝 [@mattpocock](https://github.com/mattpocock)! - 把 **`diagnose`** 技能改名為 **`diagnosing-bugs`**。

  **破壞性變更：** 以 `/diagnosing-bugs` 觸發 — 舊的 `/diagnose` 名稱已不存在。

- [`47bde84`](https://github.com/mattpocock/skills/commit/47bde84da032afb2e5058f997f3bbca47d321dbd) 感謝 [@mattpocock](https://github.com/mattpocock)! - 用 **`writing-great-skills`** 取代 **`write-a-skill`**。

  - 移除 `write-a-skill`。
  - 新增 `writing-great-skills`（加上其 `GLOSSARY.md`）— 良好撰寫與編輯技能的參考：讓技能可預測的詞彙與原則，把 no-op 狩獵到句子層級。
  - 把 `grilling` 暴露為 model-invoked 技能 — `grill-me` 與 `grill-with-docs` 背後可重用的訪談迴圈。

  **破壞性變更：** `write-a-skill` 已移除；請改用 `writing-great-skills`。

### Minor Changes

- [`47bde84`](https://github.com/mattpocock/skills/commit/47bde84da032afb2e5058f997f3bbca47d321dbd) 感謝 [@mattpocock](https://github.com/mattpocock)! - 新增 **`resolving-merge-conflicts`** 技能 — 解決進行中的 git merge 或 rebase 衝突的迴圈。獨立技能，不依賴其他技能。

- [`47bde84`](https://github.com/mattpocock/skills/commit/47bde84da032afb2e5058f997f3bbca47d321dbd) 感謝 [@mattpocock](https://github.com/mattpocock)! - 把技能分類法從 **Commands / Skills** 改名為 **User-invoked / Model-invoked**（橫跨文件），並新增定義此區分的 `docs/invocation.md`：user-invoked 技能只在輸入時觸發、存在目的是指揮；model-invoked 技能在任務符合時也可被自動觸發。user-invoked 技能可以觸發 model-invoked 技能，但永遠不能觸發另一個 user-invoked 技能。

### Patch Changes

- [`47bde84`](https://github.com/mattpocock/skills/commit/47bde84da032afb2e5058f997f3bbca47d321dbd) 感謝 [@mattpocock](https://github.com/mattpocock)! - 收緊 **`review`** 技能：fail-fast ref 檢查、單一來源規則、與 no-op 削減。
