# Productivity

一般工作流程工具，非程式碼特定。

## 使用者觸發（User-invoked）

僅在您輸入時才可觸達（Claude Code：`disable-model-invocation: true`；Codex：`agents/openai.yaml` 中的 `policy.allow_implicit_invocation: false`）。

- **[grill-me](./grill-me/SKILL.md)** — 針對計畫或設計接受持續的質詢，直到設計樹的每個分支都被解決。
- **[handoff](./handoff/SKILL.md)** — 將目前的對話壓縮成一份交接文件，讓另一個代理可以繼續進行工作。
- **[teach](./teach/SKILL.md)** — 以目前目錄作為有狀態的教學工作區，跨越多次 session 教導使用者一項新技能或概念。
- **[to-questionnaire](./to-questionnaire/SKILL.md)** — 將一個您無法獨自回答的決策，轉化為一份 Markdown 問卷，交給唯一能回答的人 — 可以非同步填寫，或在會議中一起填寫。
- **[wait-what](./wait-what/SKILL.md)** — 當訊息無法被理解的那一刻就觸發它。代理會以您所缺少的脈絡，用您的 `CONTEXT.md` 詞彙，以淺白英文重新闡述。

## 模型觸發（Model-invoked）

模型或使用者皆可觸達（使用豐富的觸發措辭，讓模型能取用它）。

- **[grilling](./grilling/SKILL.md)** — 針對計畫、決策或想法持續質詢使用者，直到設計樹的每個分支都被解決。
- **[writing-for-agents](./writing-for-agents/SKILL.md)** — 為代理撰寫文件：技能、AGENTS.md/CLAUDE.md，以及任何代理透過指標觸達的文件。
