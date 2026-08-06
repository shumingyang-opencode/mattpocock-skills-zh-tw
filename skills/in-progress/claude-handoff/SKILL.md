---
name: claude-handoff
description: 將目前的對話交給一個立即接手工作的全新背景代理。
argument-hint: "下一個 session 將用於什麼？"
disable-model-invocation: true
---

撰寫目前對話的交接摘要，讓一個全新的代理可以繼續進行工作。與其儲存它，不如啟動一個以摘要作為其提示種子的背景代理：`claude --bg --name "<描述性名稱>" "<交接摘要>"`。它在目前工作目錄中啟動並立即返回；使用者用 `claude agents` 管理它。

永遠傳入帶有描述性名稱的 `-n`/`--name`（例如 `--name "Fix login bug"`）— 它設定顯示在工作清單、session 選擇器與終端機標題中的顯示名稱。

在摘要中包含一個「建議技能（suggested skills）」段落，建議代理應該呼叫的技能。

不要重複其他產物（規格說明、計畫、ADR、issue、commit、diff）中已捕捉的內容。改以路徑或 URL 引用它們。

塗掉任何敏感資訊，例如 API key、密碼或可識別個人身分的資訊 — 摘要會成為代理的提示。

如果使用者傳入參數，將它們視為下一個 session 將專注於什麼的描述，並據此調整摘要。
