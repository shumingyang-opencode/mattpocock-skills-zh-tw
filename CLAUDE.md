技能以 bucket 資料夾形式組織在 `skills/` 下：

- `engineering/` — 每日程式碼工作
- `productivity/` — 每日非程式碼的工作流程工具
- `misc/` — 保留但少用，未推廣
- `in-progress/` — beta：刻意公開、歡迎回饋、未隨 plugin 發布
- `deprecated/` — 已不再使用

`engineering/` 或 `productivity/`（**已推廣（promoted）** 的 bucket）中的每個技能，都必須在頂層 `README.md` 有參照，並在 `.claude-plugin/plugin.json` 的 `skills` 陣列中有對應項目（Claude Code plugin 發布的正好就是已推廣的那一組）。`misc/`、`in-progress/`、`deprecated/` 中的技能不得出現在上述兩者之中。

安裝指令直接從 [.agents/install-block.md](./.agents/install-block.md) 複製。`.claude-plugin/marketplace.json` 讓 repo 成為自己的單一 plugin marketplace — 這是 install block 說明的備援方案，而非文件記載的路徑。觸碰任一 manifest 後，執行 `claude plugin validate . --strict`。為什麼做 Claude plugin 而（目前）不做 Codex plugin，記錄在 [.agents/adr/0002-ship-as-a-claude-code-plugin.md](./.agents/adr/0002-ship-as-a-claude-code-plugin.md)。

頂層 `README.md` 中每個技能的項目，必須把技能名稱連結到其 `SKILL.md`。

每個 bucket 資料夾都有 `README.md`，以一行描述列出 bucket 內每個技能，並把技能名稱連結到其 `SKILL.md`。已推廣 bucket 的 `README.md` 與頂層 `README.md` 把項目分成 **User-invoked（使用者觸發）** 與 **Model-invoked（模型觸發）**；未推廣 bucket（`misc/`、`in-progress/`）的 `README.md` 使用平鋪清單。

`engineering/` 與 `productivity/` 中的技能，也有位於 `docs/<bucket>/<skill-name>.md` 的給人看的文件頁（docs 樹鏡像 `skills/` 下的這兩個 bucket 資料夾）。發布的 URL 一律是 `https://aihero.dev/skills-<skill-name>`，與 bucket 無關 — docs 路徑只是 repo 的組織方式。當你在 `engineering/` 或 `productivity/` 新增、改名或改變某技能的**行為**時，依照 [.agents/writing-docs.md](./.agents/writing-docs.md) 建立或重新同步其 docs 頁。完成的頁面帶有四個章節 — **What it does（它做什麼）**、**When to reach for it（何時使用）**、**Common questions（常見問題）**、**It's working if（這樣就算成功）** — 而 `writing-docs.md` 保存模板、章節順序，以及哪裡可以找這些問題。未推廣 bucket（`misc/`、`in-progress/`、`deprecated/`）的技能**沒有** docs 頁。

每個 `SKILL.md` 不是 user-invoked（`disable-model-invocation: true` 加上 `agents/openai.yaml` 中的 `policy.allow_implicit_invocation: false`，僅由人觸發），就是 model-invoked（模型或使用者皆可觸發）。參見 [.agents/invocation.md](./.agents/invocation.md)。

[`ask-matt`](./skills/engineering/ask-matt/SKILL.md) 是路由每個可觸發技能及其關聯的路由器。觸發重新同步 docs 頁的同一條件也適用於它：每當你新增、改名、移除或改變某個可觸發技能在流程中的定位時，重新讀取 `ask-matt` 的 `SKILL.md` 並更新它，讓地圖保持準確 — 一個它從未提及的新技能，或一個它仍在路由的過時技能，就是一個會騙人的路由器。

要把每個技能（重新）連結到本機 harness 的 skill 目錄（`~/.claude/skills`、`~/.agents/skills`），執行 `scripts/link-skills.sh`。每個項目都是指回此 repo 的 symlink，因此 `git pull` 即可讓已安裝的技能保持最新；新增、移除或改名技能後重新執行該腳本。
