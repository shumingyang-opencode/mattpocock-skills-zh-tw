# 領域文件

工程技能在探索程式碼時應如何消費這個 repo 的領域文件。

## 探索前，先讀這些

- repo 根目錄的 **`CONTEXT.md`**，或
- repo 根目錄的 **`CONTEXT-MAP.md`**（如果存在）——它指向每個上下文一份 `CONTEXT.md`。讀與主題相關的每一份。
- **`docs/adr/`**——讀會觸及你即將工作的區域的 ADR。在多上下文 repo 中，也檢查 `src/<context>/docs/adr/` 是否有上下文範圍的決策。

如果這些檔案有任何一個不存在，**靜默繼續**。不要標記它們的缺失；不要建議先建立它們。`/domain-modeling` 技能（經由 `/grill-with-docs` 與 `/improve-codebase-architecture` 到達）在術語或決策真正定案時惰性地建立它們。

## 檔案結構

單一上下文 repo（多數 repo）：

```
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

多上下文 repo（根目錄有 `CONTEXT-MAP.md`）：

```
/
├── CONTEXT-MAP.md
├── docs/adr/                          ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  ← context-specific decisions
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

## 使用詞彙表的詞彙

當你的輸出為某個領域概念命名時（在 issue 標題、重構提案、假設、測試名稱中），使用 `CONTEXT.md` 中定義的術語。不要漂移到詞彙表明確避免的同義詞。

如果你需要的概念還不在詞彙表裡，那是個訊號——不是你在發明專案沒用的語言（再想想），就是存在真實的缺口（為 `/domain-modeling` 記下它）。

## 標記 ADR 衝突

如果你的輸出與既有 ADR 矛盾，明確把它浮上檯面，而不是默默覆寫：

> _與 ADR-0007（事件溯源訂單）矛盾——但值得重新討論，因為……_
