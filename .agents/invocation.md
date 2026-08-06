# Model-invoked vs user-invoked

此 repo 中的每個 `SKILL.md` 都是一個技能。區分它們的唯一軸線是**觸發方式（invocation）** — 誰能呼叫它：

- **User-invoked** — 只有**人輸入其名稱**時才能觸發。在 frontmatter（Claude Code）設定 `disable-model-invocation: true`，並在 `agents/openai.yaml`（Codex）設定 `policy.allow_implicit_invocation: false`。`description` 是**給人看的**：一句話摘要，供瀏覽 slash 指令的人閱讀。刪除觸發清單（「當使用者說……時」）。
- **Model-invoked** — **模型或使用者**皆可觸發。這是預設：省略 `disable-model-invocation` 以及 `agents/openai.yaml` 中的 `policy` 區塊。`description` 是**給模型看的**，並保有豐富的觸發措辭（「當使用者想要……、提到……、要求……」），讓自動觸發得以生效。判斷技能是否應維持 model-invoked 的測試：_模型能否自主且有用地觸發它？_（重用是把技能抽離出來的理由，不是測試。）

每個 harness 以各自的方式把 user-invoked 技能排除在模型的觸發範圍之外，因此除了人以外沒有東西能觸發它 — 其他技能也不行。user-invoked 技能可以觸發 model-invoked 技能，但永遠不能觸發另一個 user-invoked 技能。

每個技能在 `SKILL.md` 旁也帶有 `agents/openai.yaml`。它保存 Codex UI 中繼資料 — 技能選擇器的 `interface.display_name` 與 `interface.short_description` — 以及（對 user-invoked 技能）與 `disable-model-invocation` 成對的 `policy.allow_implicit_invocation: false`。兩者要保持同步：一個技能在兩個 harness 中皆為 user-invoked，或皆非。

Bucket 的 `README.md` 與頂層 `README.md` 把項目分成 **User-invoked** 與 **Model-invoked**。

## 兩者之間的依賴

依賴以 **`/skill` 風格的散文式觸發**表達（「執行 `/grilling` 技能」），而非深層的 `../other-skill/FILE.md` 交叉參照。共用的參考文件放在擁有它的技能內部；其他技能透過觸發該技能取得素材，而非跨資料夾連結。

## 被動 vs 主動的領域工作

只是*閱讀* `CONTEXT.md` 取得詞彙，是一行的散文指標，不是 `domain-modeling` 技能。唯有主動的建立/磨練紀律（質疑術語、邊緣情境、寫 ADR、內嵌更新 `CONTEXT.md`）才是 `domain-modeling`。
