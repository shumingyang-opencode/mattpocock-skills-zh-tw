# 明確的 `/setup-matt-pocock-skills` 指標只給硬依賴

工程技能依賴由 `/setup-matt-pocock-skills` 種下的各 repo 設定（issue tracker、triage 標籤詞彙、領域文件排版）。有些技能沒有該設定就無法有意義地運作 — 它們必須發布到特定 issue tracker，或套用特定標籤字串。其他技能只用它來磨利輸出（詞彙、ADR 意識），沒有也能優雅退化。

我們把它們分成**硬依賴**與**軟依賴**技能：

- **硬依賴**（`to-tickets`、`to-spec`、`triage`）— 帶有明確的一行：_"… 本應已提供給你 — 若未提供請執行 `/setup-matt-pocock-skills`。"_ 缺少對應時，輸出是錯的，而不只是模糊。
- **軟依賴**（`diagnose`、`tdd`、`improve-codebase-architecture`）— 僅以模糊的散文提及「專案的領域詞彙表」與「你觸碰範圍的 ADR」。文件不在時技能仍能運作；輸出只是沒那麼精準。

這個區分讓軟依賴技能保持 token 輕量，並避免把 setup 指標灌到其實不承重的每個角落。
