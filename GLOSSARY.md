# Matt Pocock 技能集

由 Claude Code 載入的一組代理技能（slash 指令與行為）。技能依 bucket 組織，並由 `/setup-matt-pocock-skills` 輸出的各 repo 設定來使用。

## 語言

**Issue tracker**：
承載 repo 的 issue 的工具 — GitHub Issues、Linear、本機 `.scratch/` markdown 慣例或其他類似工具。`to-tickets`、`to-spec`、`triage` 等技能會從中讀取並寫入。
_Avoid_: backlog manager、backlog backend、issue host

**Issue**：
**Issue tracker** 內一個受追蹤的工作單元 — 由 `to-tickets` 產生的 bug、任務、spec 或切片。
_Avoid_: ticket（僅在引用外部系統稱呼它們為 ticket 時，或用於 **Decision ticket** — 見下方）

**Decision ticket**：
`wayfinder` 的單位 — `wayfinder:map` 的子 **Issue**，持有「其解決方案是決策」而非「要執行的建置切片」的*問題*。**decision** 修飾詞正是它與實作 ticket 的區別所在；`wayfinder` 引入此術語後便使用「ticket」。

**Triage role**：
triage 期間套用於 **Issue** 的典型狀態機標籤（例如 `needs-triage`、`ready-for-afk`）。每個角色透過 `docs/agents/triage-labels.md` 對應到 **Issue tracker** 中的實際標籤字串。

## 關係

- 一個 **Issue tracker** 承載多個 **Issues**
- 一個 **Issue** 同一時間帶有一個 **Triage role**
- 一個 **Decision ticket** 是一個 **Issue**（`wayfinder:map` 的子項目）

## 標記的歧義

- 「backlog」先前同時被用來指稱承載 issue 的*工具*與其中的*工作總量* — 已決議：工具就是 **Issue tracker**；「backlog」不再作為領域術語使用。
- 「backlog backend」/「backlog manager」— 已決議：併入 **Issue tracker**。
