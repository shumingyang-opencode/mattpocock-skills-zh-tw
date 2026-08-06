# 以原生 Claude Code plugin 發布技能集；暫緩原生 Codex plugin

這些技能一直可以透過 [skills.sh](https://skills.sh/mattpocock/skills)（`npx skills add mattpocock/skills`）安裝，它會把可編輯的 skill 檔案複製到使用者的專案，適用於 Claude Code、Codex 及其他 Agent-Skills 標準的 harness。一個反覆出現的需求是**即插即用**的分發方式：以唯讀、永遠最新的 bundle 訂閱整組技能，而不是訂閱一個你擁有的 fork。這正是原生 plugin 系統提供的東西。

我們發布原生 **Claude Code plugin**，並暫時**暫緩**原生 **Codex plugin**。此區分是兩個生態系的 plugin manifest 選擇技能的方式，對照此 repo 的 bucket 式排版所迫。

## 限制：bucket 式技能 vs 單一路徑選擇

技能位於 `skills/` 下的 bucket 資料夾 — `engineering/` 與 `productivity/` 是**已推廣**的（發布）；`misc/`、`personal/`、`in-progress/`、`deprecated/` 則**不是**。plugin 只能暴露已推廣的那一組，而這組橫跨兩個 bucket 資料夾。

- **Claude Code** — `.claude-plugin/plugin.json` 接受 `skills` 作為**顯式技能目錄路徑的陣列**。我們逐一列出已推廣技能，以零歧義排除其他一切，並加上 `.claude-plugin/marketplace.json` 讓 repo 成為自己的單一 plugin marketplace。端到端驗證過：`claude plugin validate . --strict` 通過，且 `marketplace add` → `install` 能解析所有已推廣技能。

- **Codex** — `.codex-plugin/plugin.json` 只接受 `skills` 作為**單一路徑字串**（陣列會被 `missing or invalid plugin.json` 拒絕），而 Codex 會遞迴探索其下的 `SKILL.md`。無法從單一路徑指定兩個 bucket 資料夾，或策展子集。測試過並否決了兩個逃生門：
  - 指向 `./skills/` 也會發布 `deprecated/`、`in-progress/`、`personal/` 與 `misc/` — 我們刻意不推廣的退休、草稿與個人技能。
  - 指向 bucket 的**symlink** 策展扁平目錄在安裝後無法存活：Codex 把 plugin 樹複製進快取並**丟棄 symlink**，所以技能到達時是空的。

給 Codex 單一且僅含已推廣路徑的穩健做法只有 (a) **重組**讓 `skills/` 只含已推廣技能（把未推廣 bucket 移出 — 橫跨 `CLAUDE.md`、`scripts/link-skills.sh`、bucket README、以及依賴 `in-progress/` 與 `personal/` 的本機開發流程，影響範圍很大），或 (b) **提交**已推廣技能的複製到扁平目錄（同步負擔，且成為第二個真相來源）。兩者都是結構性決策，不是該綁進發布 Claude plugin 的東西。這很可能就是 plugin 遲遲未發布的最初、被半遺忘的原因：manifest 格式無法乾淨地表達一個 bucket 式 repo 的策展子集。

## 決策

- 現在發布 **Claude Code plugin**（`.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json`），策展為已推廣那一組，作為 v1.2 的招牌交付物。
- 保留 **skills.sh** 作為通用安裝程式 — 它今天已服務 Codex 與其他 harness，所以沒有任何 Codex 使用者會失去安裝路徑。
- **暫緩**原生 Codex plugin，直到我們決定重組 `skills/` 為僅含已推廣技能，或提交產生的扁平複製。當 Codex 支援 `skills` 陣列/包含清單，或在安裝時保留 symlink 時，再重新審視。

## 這產生的不變量

- 每個已推廣技能都在 `.claude-plugin/plugin.json` 的 `skills` 陣列中有對應項目（這原本已是 `CLAUDE.md` 規則；現在它也把關 plugin 的內容）。
- `.claude-plugin/plugin.json` 的 `version` 追蹤 `package.json` 的版本 — 發布時一起升版。Claude 用 plugin 的 `version` 決定已安裝使用者何時看到更新。

## 更新，2026-08-05

`mattpocock-skills` 已獲准進入 **Claude Code 的官方 marketplace** — 設定名稱 `claude-plugins-official`、來源 repo `anthropics/claude-plugins-official` — 每個 Claude Code 安裝預設都有。`claude plugins install mattpocock-skills` 現在是記錄在案的路徑，上述 `marketplace add` → `install` 路徑已被取代。安裝措辭位於 [.agents/install-block.md](../install-block.md)。

官方列表指向此 repo 的 git URL，並直接讀取 `.claude-plugin/plugin.json`，因此它不依賴 `.claude-plugin/marketplace.json`。該檔案僅保留作為直接安裝 repo（未發布的 commit，或 fork）的備援。

2026-08-05 在 Claude Code 2.1.222 上對照線上列表驗證：

- `claude plugins install mattpocock-skills` 無須先新增 marketplace 即可解析，並回報 `mattpocock-skills@claude-plugins-official`。
- 接著 `claude plugin details mattpocock-skills` 回報版本 1.2.0 並載入已推廣技能。
- 列表的 `source` 是 `{"source": "url", "url": "https://github.com/mattpocock/skills.git", "sha": …}` — **sha 是固定的**，因此發布會在該固定點移動時送達已安裝使用者，而非我們打 tag 的當下。撰寫當下固定點落在 `main` 後兩個 commit，這正是它列出 22 個技能而非 `plugin.json` 中的 24 個的原因。
- session 內的 `/plugin install mattpocock-skills` **未**被實際演練 — `/plugin` 在無頭（`claude -p`）session 中不可用。它與 CLI 執行同一個解析器，而記錄在案的範例形式是 `/plugin install <name>@claude-plugins-official`。
