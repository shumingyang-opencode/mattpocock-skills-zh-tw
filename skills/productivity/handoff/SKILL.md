---
name: handoff
description: 將目前的對話壓縮成一份交接文件，讓另一個代理接手。
argument-hint: "下一個 session 將用於什麼？"
disable-model-invocation: true
---

撰寫一份交接文件，總結目前對話，讓一個全新的代理可以繼續進行工作。儲存到使用者作業系統的暫存目錄 — 而非目前工作區。

在文件中包含一個「建議技能（suggested skills）」段落，建議代理應該呼叫的技能。

不要重複其他產物（規格說明、計畫、ADR、issue、commit、diff）中已捕捉的內容。改以路徑或 URL 引用它們。

塗掉任何敏感資訊，例如 API key、密碼或可識別個人身分的資訊。

如果使用者傳入參數，將它們視為下一個 session 將專注於什麼的描述，並據此調整文件內容。
