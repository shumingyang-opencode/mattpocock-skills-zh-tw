# In Progress

測試版。這些技能是有意公開的 — 試試它們並告訴我有什麼壞掉的地方。它們被排除在 plugin 與頂層 README 之外，直到它們轉化到一個穩定類別；它們沒有文件頁，而且可能無預警地改變或消失。

plugin 不會給您這些。直接安裝一個：

```bash
npx skills@latest add mattpocock/skills --skill=<name>
```

- **[loop-me](./loop-me/SKILL.md)** — 以目前目錄作為有狀態工作區，在多次 session 中把您自己 grill 成可實作的 workflow 規格說明。使用者觸發。
- **[writing-beats](./writing-beats/SKILL.md)** — 將文章塑造成一連串節拍的旅程，選擇你自己的冒險風格。挑選一個起始節拍，只寫那個節拍，然後轉向下一個，直到文章達到自然的結尾。
- **[writing-fragments](./writing-fragments/SKILL.md)** — 一場從您身上挖掘片段的 grilling session — 異質的寫作碎片 — 並將它們附加到單一文件中，作為未來文章的原始素材。
- **[writing-shape](./writing-shape/SKILL.md)** — 將一份原始素材的 markdown 檔案，一段一段地塑造成文章，每一步都論證格式選擇。
- **[claude-handoff](./claude-handoff/SKILL.md)** — 將目前的對話交給一個全新的背景代理，它立即接手工作，並透過 `claude --bg` 以交接摘要作為種子。使用者觸發。
- **[setup-ts-deep-modules](./setup-ts-deep-modules/SKILL.md)** — 將 dependency-cruiser 接入 TypeScript repo，讓每個套件都是深模組 — 實作藏在子資料夾中，只能透過其進入點檔案觸達，測試也透過那些進入點來演練它。使用者觸發。
