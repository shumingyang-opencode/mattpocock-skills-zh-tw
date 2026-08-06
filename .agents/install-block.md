# 標準安裝區塊

一套安裝說明，一種措辭。`README.md`、`.changeset/*` 與 `docs/` 下的每個頁面都只能說**這一套**。先在這裡改，再往外散播。

`mattpocock-skills` 已列在 **Claude Code 的官方 marketplace** — 設定名稱 `claude-plugins-official`、來源 repo `anthropics/claude-plugins-official` — 每個 Claude Code 安裝預設都有。無須先新增任何 marketplace。官方 Anthropic marketplace 預設啟用自動更新（[discover-plugins](https://code.claude.com/docs/en/discover-plugins)），所以「更新自動送達」是事實，不是期望。

## Claude Code — plugin

<canonical-block name="claude-code">

```bash
claude plugins install mattpocock-skills
```

或從 session 內：

```
/plugin install mattpocock-skills
```

它位於 Claude Code 的官方 marketplace，所以無須先新增任何東西，更新自動送達。

</canonical-block>

## Codex 與其他代理 — skills.sh

這個 plugin 僅限 Claude Code。其他所有地方，[skills.sh](https://skills.sh/mattpocock/skills) 會把可編輯的 skill 檔案複製到專案中。`README.md` 使用整組形式：

<canonical-block name="skills-sh-whole-set">

```bash
npx skills@latest add mattpocock/skills
```

選擇你想要的技能，以及要安裝到哪些 coding agent。**安裝程式讓你挑選要帶走的技能 — 務必把 `setup-matt-pocock-skills` 列入其中。**

</canonical-block>

…而單一技能形式用在單獨指名某個技能的地方。注意 **`docs/` 頁面不是這個區塊的消費者**：ai-hero 會在正文上方渲染安裝 widget，所以頁面把指令寫出來反而重複了它。參見 [writing-docs.md](./writing-docs.md)。

<canonical-block name="skills-sh-one-skill">

```bash
npx skills@latest add mattpocock/skills --skill=<name>
```

```bash
npx skills@latest update <name>
```

</canonical-block>

`skills@latest` 是三者皆用的固定拼法。`docs/` 下的頁面過去各自攜帶一份這些指令；這些區塊現在是刪除而非更正，因為網站自己會渲染安裝指令。

## 兩條路線互斥

plugin 是你訂閱的受管、唯讀 bundle。skills.sh 則寫入你擁有並可編輯的檔案。兩者都裝會讓使用者得到每種技能兩份 — 永遠要說「二選一」。

## 不是安裝故事

`.claude-plugin/marketplace.json` 讓 repo 成為自己的單一 plugin marketplace（`/plugin marketplace add mattpocock/skills`，再 `/plugin install mattpocock-skills@mattpocock`）。官方列表已取代它。它保留作為直接安裝 repo（未發布的 commit，或 fork）的備援，且**不**對使用者記錄在案。
