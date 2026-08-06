## 用途

`codebase-design` 固定你用於設計模組的用詞：**模組**、**介面**、**深度**、**接縫**、**轉接器**、**槓桿收益**、**局部性**。它精確定義每一個，禁止鬆散的替代詞（「component」、「service」、「API」、「boundary」），並陳述由它們推導出的少數原則。

它是一份參考，不是一個流程。沒有要跑的迴圈、沒有它產生的產物、沒有它問你問題的檢查點。其他所有觸及設計的技能都會借用它的詞彙；它單獨存在時，只給你語言，然後就此打住。這是在你呼叫它之前該知道的事，因為一個沒有流程、沒有停止規則的技能，如果你把[會話](https://www.aihero.dev/ai-coding-dictionary/session)指向它並說「開始」，它就會臨場發揮一個流程——見下方問題。

## 何時使用

輸入 `/codebase-design`，或者當設計任務適用時，代理會自動採用它。

當你已經知道要重新設計哪段程式碼、需要思考它的形狀時取用它：接縫放在哪裡、介面能縮到多小、一次抽取是否值得。它也是你用來裁決某個詞彙含義爭論時會取用的技能。

有幾個技能跟它很接近。你要哪一個取決於實際問題是什麼：

| 問題 | 技能 |
|---|---|
| 單一模組的形狀——它的介面、接縫、深度 | `codebase-design` |
| *領域的用詞*——「account」有三種意思、兩個人對「cancellation」各有不同理解 | [domain-modeling](https://aihero.dev/skills-domain-modeling) |
| 你還不知道要重新設計*哪個*模組 | [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture)——找出候選者的調查 |
| 你想讓設計被辯論，而不只是被命名 | [grilling](https://aihero.dev/skills-grilling) |
| 有具體的行為要建置，你想要能在重構中存活的測試 | [tdd](https://aihero.dev/skills-tdd) |

## 詞彙

詞彙表就是這個技能。每個詞都是相對於其他詞定義的，而且每個詞都附帶它取代的詞。

| 術語 | 含義 | 別說 |
|---|---|---|
| **模組** | 任何具有介面與實作的東西。刻意與規模無關——一個函式、一個類別、一個套件、跨越各層的切片。 | unit, component, service |
| **介面** | 呼叫方為了正確使用而必須知道的一切：型別簽章，加上不變量、順序約束、錯誤模式、所需設定、效能特性。 | API, signature |
| **深度** | 介面上的槓桿收益——呼叫方或測試每學習一單位介面所能運用的行為量。**深**：小介面背後有大量行為。**淺**：介面幾乎與實作一樣複雜。 | — |
| **接縫** | Michael Feathers 的術語：可以在不於該處編輯的前提下變更行為的地方。它是介面的*位置*，而把它放在哪裡是它自己的決定，與它背後放什麼是分開的。 | boundary |
| **轉接器** | 在接縫處滿足介面的具體東西。指涉的是角色，而非本質——記憶體中的 fake 和 Postgres repo 都是轉接器。 | — |
| **槓桿收益** | 呼叫方從深度得到的東西：每單位已學習的介面獲得更多能力。 | — |
| **局部性** | 維護者從深度得到的東西：變更、bug 與驗證集中在同一處。修一次，處處修好。 | — |

深度刻意*不*定義為實作行數對介面行數的比率——那是 Ousterhout 自己的定義。那個指標會獎勵灌水實作。這裡改用「深度即槓桿收益」。

## 四項原則

- **深度是介面的屬性，不是實作的屬性。** 深模組可以由內部小而可替換的零件建構。它們只是不會浮現給呼叫方。一個模組可以有自己測試使用的內部接縫，以及介面處的一個外部接縫。
- **刪除測試。** 想像刪除這個模組。如果複雜度消失了，它是個純傳遞。如果複雜度在 N 個呼叫方身上重新出現，它就值得保留。
- **介面就是測試表面。** 呼叫方與測試跨越同一個接縫。如果你想在*介面之外*測試，模組的形狀就錯了。
- **一個轉接器代表假設性的接縫。兩個轉接器才是真的。** 在真的有東西跨越它而變化之前，別切接縫。單一轉接器的接縫只是間接層。

兩份輔助檔案可以更進一步，而技能會按需讀取，而非預先讀取。[DEEPENING.md](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/DEEPENING.md) 為候選者的相依性分類——進程內、可本機取代、遠端但自有、真正外部——因為類別決定加深後的模組要如何在接縫處接受測試。[DESIGN-IT-TWICE.md](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/DESIGN-IT-TWICE.md) 啟動平行的[子代理](https://www.aihero.dev/ai-coding-dictionary/subagent)為同一個模組產出三種以上截然不同的介面，然後以深度、局部性與接縫位置比較它們。

## 常見問題

**我要如何在 TypeScript 中實際建構深模組？**

這是關於此技能最常被問的問題，而技能不回答它。它定義深模組*是*什麼；它對如何阻止一個亂入的 import 越過介面隻字未提。[Issue #458](https://github.com/mattpocock/skills/issues/458) 說得很直接：「let's say we're happy with the interface, it hides the details, etc. But how do we enforce it? I think without linting or clear guardrails, humans and LLMs alike will start making it messy over time.」Matt 在那串討論中的回答是三種選項：把它包進 class 或 IIFE，並接受這個 class 會長得很大；在 monorepo 中把它做成套件，並接受 monorepo 的工具；或者用 [dependency-cruiser](https://github.com/sverweij/dependency-cruiser) 之類的 linter 禁止繞過介面的 import。他另外單獨稱 Effect 是最佳機制，dependency-cruiser 是第二佳。儲存庫的 `in-progress/` 桶裡有一個 `setup-ts-deep-modules` 技能，會建立 `src/packages/<name>/index.ts` 慣例，但它是沒有文件頁面的 beta 頻道技能，而且沒有隨附 lint 規則。

**我把會話指向它，它燒掉 100k 個 [token](https://www.aihero.dev/ai-coding-dictionary/token) 重新設計了我從未要求的東西。**

已知，且已登記為 [issue #449](https://github.com/mattpocock/skills/issues/449)。這個技能由模型呼叫，描述自己是詞彙，但它裡面沒有任何東西硬性阻止代理把它當成可執行的流程。被告知「在 /codebase-design 中繼續並推動未決決策」後，一個代理伸手抓它能找到的最「行動形狀」內容——`DESIGN-IT-TWICE.md` 中的平行子代理——重新探索了先前會話已對映過的程式碼，跑了很遠才問任何事情。驅動型技能會有的防護（檢查點、一次只問一題、不自動前進）在這裡一個都沒有，因為參考本來就沒有。解法是指名一個驅動型技能，讓這個技能待在它底下：`/grill-with-docs`、`/improve-codebase-architecture` 或 `/tdd`，以 `codebase-design` 作為詞彙。該 issue 仍開著。

**`design-an-interface` 去哪裡了？有 `/interface-design` 技能嗎？**

`design-an-interface` 被移除並併入此技能。沒有損失任何東西：它的「設計兩次」技巧——平行子代理產生截然不同的設計，源自 Ousterhout——以 `DESIGN-IT-TWICE.md` 的形式隨附於此。此外，有幾個人要求一個專門的 `/interface-design` 技能來承載深模組／薄介面哲學；那個哲學已經住在這裡，沒有規劃獨立技能。如果你本來找的是這兩個名字任一個，這一頁就是了。

**這不是檔案結構慣例嗎——資料夾、barrel 檔案、功能切片？**

不是，而技能在反覆施壓下仍堅持這條線。[Issue #95](https://github.com/mattpocock/skills/issues/95) 提議把正式的碎形樹檔案結構作為深模組的具體實作；回覆是兩者正交——「deep modules are about the design of the interface and accessing through a strict interface, no matter what the file system looks like. It seems perfectly possible that you could have shallow modules with this approach.」同樣的事在 #458 出現：「I think you might be tying the concept of modules too closely to the file system. The file system can certainly be a useful hint to the shape of modules, but there's no need to use the file system in the construction of deep modules.」詞彙表刻意把**模組**定義為與規模無關。

**`tdd` 真的會用這套詞彙嗎？**

現在會了。以前很長一段時間不會。過去住在 `tdd` 內部的行內深模組筆記，在 v1.0 被移除，改由這個共用技能負責，但取代它們的指標從未被加入——所以 `tdd` 自己定義了「seam」，卻不引用任何東西。這個缺口已封閉：指標現在在技能中，在介面形狀（而非測試）成為未決問題時觸及。`tdd` 仍擁有「seam」作為你在*測試*時的邊界；此技能擁有它背後的模組形狀。

**design-it-twice 模式在 Claude Code 之外能用嗎？**

無法乾淨地使用。`DESIGN-IT-TWICE.md` 說「spawn 3+ sub-agents in parallel using the Agent tool」，這是 Claude Code 以 Claude Code 名義命名的[工具](https://www.aihero.dev/ai-coding-dictionary/tool)。儲存庫為其他[執行環境](https://www.aihero.dev/ai-coding-dictionary/harness)（包括 Codex）附上中繼資料，而那些執行環境可能不會在該名稱下暴露任何東西——所以平行設計階段不如技能的中繼資料暗示的那樣可攜。追蹤於 [issue #564](https://github.com/mattpocock/skills/issues/564)，開著。

**我可以把自己的概念加進詞彙表嗎——connascence、模組祕密、[漸進式揭露](https://www.aihero.dev/ai-coding-dictionary/progressive-disclosure)？**

有人正好提出過這些。[Issue #180](https://github.com/mattpocock/skills/issues/180) 把 Parnas 的模組祕密與 Page-Jones 的 connascence 加進去，作為跨越接縫*什麼*在洩漏的命名層，並附上可用的 diff；[issue #303](https://github.com/mattpocock/skills/issues/303) 提議在實作內部做漸進式揭露，讓在公開介面很深的模組不會在底下是一整塊無區別的厚板。兩者都未結、未合併。發布的詞彙表刻意很小，而它保持小顆粒的理由寫在技能本身：一致的語言才是重點，而一個沒人一致使用的術語比沒有術語更糟。

## 這樣就算成功

- 設計對話停止產生「component」、「service」與「boundary」，開始產生「module」、「interface」與「seam」。
- 有人能指著一項提案的抽取，毫不含糊地說出它是否通過刪除測試。
- 提議的接縫附帶第二個被點名的轉接器，而不只是第一個。
- 關於介面的討論涵蓋不變量、順序與錯誤模式——而不只是型別簽章。
- 呼叫它不會開始一個會話。如果代理只憑 `/codebase-design` 就開始讀檔並提議重構，它就把參考誤當成驅動器了。

## 它在哪裡適用

`codebase-design` 是**隨時可取用的獨立技能**，是工程技能底下的詞彙層，而不是任何鏈中的一個步驟。它最接近的鄰居是 [domain-modeling](https://aihero.dev/skills-domain-modeling)，也就是*問題領域*用詞（而非模組形狀）的平行參考——兩者通常需要一起用，因為要為深模組取好名字兩者都需要。[improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) 是另一個：它調查代碼庫找出加深候選者，並用這套詞彙寫下每一個，所以它找到模組，而此技能是你在上面設計它的長凳。當你不確定哪個技能或流程適用時，[ask-matt](https://aihero.dev/skills-ask-matt) 會幫你導航。
