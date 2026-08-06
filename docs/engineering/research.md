## 用途

`research` 透過閱讀持有答案的來源來回答問題，然後在儲存庫中留下一份帶引用的 Markdown 檔案。它只從**[主要來源](https://www.aihero.dev/ai-coding-dictionary/primary-source)**工作——官方文件、原始碼、規格說明、第一方 API——並把每項聲稱追溯回持有它的來源，所以當 API 自己的文件可及時，它不會重複某篇部落格文章對該 API 的敘述。

它不會在對話中回答你。輸出是一份檔案，寫在儲存庫已經存放此類筆記的地方，每項聲稱都附帶連結。這就是重點：一份你可以回應、交給另一個代理或丟掉的文件，而不是一個在[會話](https://www.aihero.dev/ai-coding-dictionary/session)結束時消失的答案。

## 何時使用

輸入 `/research`，或當任務變成閱讀跑腿工作時，[代理](https://www.aihero.dev/ai-coding-dictionary/agent)會自動採用它。

當下一步是從工作目錄之外*查明某件事*——第三方 API 如何運作、規格說明實際說了什麼、某個版本聲稱是否成立——而且你寧可不要自己停下來做閱讀時取用它。你需要什麼決定哪個技能：

| 你需要 | 取用 |
| --- | --- |
| 一個決策在等待的外部事實 | `research` |
| 一個*與你一起*、透過訪談做出的決策 | [grilling](https://aihero.dev/skills-grilling) |
| 一個持久、寫入 `CONTEXT.md` 與 ADR 的架構決策 | [grill-with-docs](https://aihero.dev/skills-grill-with-docs) |
| 查明某個做法是否在你的代碼庫中有效 | [prototype](https://aihero.dev/skills-prototype) |
| 一個大到塞不進單一會話的計畫 | [wayfinder](https://aihero.dev/skills-wayfinder) |

`research` 與 `grill-with-docs` 之間的界線是**回傳內容的保存期限**。研究產出短命的資產——這個函式庫的認證機制截至本週做什麼。ADR 記錄一個你保留的決策。如果你產出的是決策而非事實，你是在 [grilling](https://www.aihero.dev/ai-coding-dictionary/grilling)，不是在研究。

## 委派的跑腿工作

定義性的動作是閱讀以**背景代理**的方式執行。你繼續工作；它走開、把每項聲稱追溯到其主要來源、寫一份 Markdown 檔案，然後回報。研究是你委派的跑腿工作，不是外包的思考——你得到一份可供 grill、規劃或設計的文件，而裁量權仍然在你手上。

委派是沒有防護的，而背景代理可以再產生自己的背景代理。這是此技能最廣為記載的粗糙邊緣。

檔案落在哪裡由儲存庫決定，不是由技能決定：它會配合已存在的筆記慣例，而如果沒有慣例，它會挑一個合理的地方並告訴你。每次執行寫一份檔案。

## 常見問題

**它產生第二個研究代理——這是預期的嗎？**

不是。這是未結 bug，[issue #530](https://github.com/mattpocock/skills/issues/530)。技能告訴它的呼叫者啟動背景代理，但沒有限制代理型別，所以它產生的代理是持有 `Agent` 工具與相同指示的 `general-purpose` 代理——然後又觸發它們一次。一位回報者測量到單一研究任務在三場重疊執行中花費約 450k [token](https://www.aihero.dev/ai-coding-dictionary/token)，重複的執行在完全看不到的地方半小時後完成。它在 Claude Code 之外也能重現；同樣的巢狀在 Codex 配 GPT-5.6-sol 上也獲得確認。沒有發布的修復。使用者以一行指示修補自己安裝的副本，告訴已經是[子代理](https://www.aihero.dev/ai-coding-dictionary/subagent)的代理自己完成工作，這有幫助，但屬於指示層級，不是結構層級。呼叫後留意你的背景任務清單，並停掉重複的。

相反的失敗也存在：如果你自己的全域指示禁止代理重新委派工作，背景代理會禮貌地拒絕任務，而技能默默地什麼都不做。

**檔案該放在哪裡——我該提交它嗎？**

技能把檔案放在儲存庫已經存放筆記的地方，除此之外沒有意見。社群共識相當確定：ADR 保留，研究檔案不保留。最尖銳的版本，來自正好討論這個問題的 Discord 串：「ADRs yes. Everything else archive or delete after done. It otherwise becomes cruft of work and can poison future repo reads if you've drifted away from the spec/research.」研究檔案記錄的是寫下當天為真的事，所以過時的比沒有更糟。總體而言，這些產物並不真正屬於 git，也沒有標準的家——人們改用 Obsidian、分開的知識儲存庫，或 issue 追蹤器。

**什麼才算「高可信度」的主要來源，由誰決定？**

[模型](https://www.aihero.dev/ai-coding-dictionary/model)決定。技能點名符合資格的來源*類型*——官方文件、原始碼、規格說明、第一方 API——沒有允許清單、沒有領域限制、沒有驗證輪。這是技能最初被提議時最大的反對意見，而且從未被公開回答：「Five research subagents pointed at junk just gives you five confident wrong answers faster. How are you gating what counts as high-trust sources?」你實際擁有的緩解是每項聲稱上的引用。追蹤其中兩三個。如果它們落在某件事的摘要上，而不是那件事本身，執行就在它唯一的職責上失敗了。

**之後的會話會重用先前執行找到的東西嗎？**

不會。沒有東西自動載入過去的研究檔案；它是一份坐在儲存庫裡的文件，直到人類或技能指向它。這在早期被提出，作為對設計最強的挑戰——「the value's the markdown becoming context the agent re-reads later, not the fetch itself. A write-once dead file is just a fancy search」——而發布的技能沒有解決它。實際上，檔案靠被刻意餵進下一步來證明價值：把它附加到規格說明、在 grilling 會話中引用它、用 [ticket](https://www.aihero.dev/ai-coding-dictionary/ticket) 指向它。

**為什麼不直接叫代理去看文件？**

你可以，而一段正好這樣說的兩行提示詞，就是此技能取代的做法。技能比提示詞多買到兩樣東西：它在背景執行，所以你的會話保持[上下文](https://www.aihero.dev/ai-coding-dictionary/context)乾淨；而且主要來源約束與引用檔案輸出每次都以相同方式產出，而不是取決於你碰巧怎麼措辭。相對於[執行環境](https://www.aihero.dev/ai-coding-dictionary/harness)自己的深度研究模式，差異在於產物與來源紀律，不在於搜尋。如果兩行提示詞能在小問題上給你需要的東西，就用兩行提示詞。

**它什麼時候停止閱讀？**

技能中沒有停止標準，而這以兩種看起來相反、其實是同一個缺口的方式出現：跑得太深的代理，以及廣泛涵蓋主題卻漏掉唯一重要細節的代理。一位實務工作者說：「deep-research skills are a bit too deep sometimes. And telling an agent to research usually results in missing crucial details.」範圍界定是你的事。狹窄、可回答的問題——一個 API、一個行為、一個版本聲稱——回來的結果遠比「research X」好。

**`/wayfinder` 建立了研究 ticket——那些我自己解決嗎？**

不是，它現在會替你觸發它們。在 v1.1 之後尚未發布的變更中，繪製地圖的會話會為每個研究 ticket 產生一個 `/research` 子代理，並平行把它們燒掉，在一次性 `research/<name>` 分支上捕捉發現，並從 ticket 帶[上下文指標](https://www.aihero.dev/ai-coding-dictionary/context-pointer)。研究 ticket 是 wayfinder 每會話一個 ticket 規則的唯一例外，因為它們是 [AFK](https://www.aihero.dev/ai-coding-dictionary/afk)——沒有什麼在等你。那些分支有兩個已知的卡點：子代理曾被看到從一個從不打算合併的分支開草稿 PR（[issue #576](https://github.com/mattpocock/skills/issues/576)），而稍後刪除分支會弄壞 ticket 持有的上下文指標。

## 這樣就算成功

- 你自己的會話持續進行。如果你坐在那看它閱讀，委派就沒發生。
- 正好出現一個新背景任務。第二個名稱幾乎相同的，就是巢狀 bug。
- 出現一份新的 Markdown 檔案，在儲存庫已用於筆記的資料夾中，而代理告訴你路徑。
- 其中每項聲稱都附帶連結，而隨機追蹤兩個會把你帶到官方文件、規格說明或實際的原始檔——而不是某人對它的轉述。
- 你能僅憑那份檔案做出你卡住的決策，不必自己再回去查來源。

## 它在哪裡適用

一個隨時可取用的獨立技能，餵養思考型技能，而不是待在建置鏈中。它的檔案是該*帶進*流程的東西：當事實已經攤在桌上時，[grilling](https://aihero.dev/skills-grilling) 與 [grill-with-docs](https://aihero.dev/skills-grill-with-docs) 會問出更銳利的問題，而 [to-spec](https://aihero.dev/skills-to-spec) 可以對照它綜合。wayfinder 是唯一直接呼叫它的技能，以 `/research` 子代理解決它地圖上每個研究 ticket。至於整張地圖，見 [ask-matt](https://aihero.dev/skills-ask-matt)。
