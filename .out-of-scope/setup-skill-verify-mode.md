# 為 `setup-matt-pocock-skills` 提供驗證/檢查模式

本專案不會為 `setup-matt-pocock-skills` 新增專屬的驗證/檢查模式（或獨立的 verify 技能）。

## 為什麼這超出範圍

新增第二個技能 — 或 `--verify` 旗標 — 來檢查 `docs/agents/*.md` 產物是否仍符合 seed-template schema，會重複現有 setup 技能已在對話中處理的工作。

預期的流程是：**執行 `/setup-matt-pocock-skills` 並叫它驗證你目前的設定。** 該技能由提示驅動，所以維護者可以把它的範圍限定為一輪驗證（「不要重寫任何東西，只要把我既有的檔案對照目前的 seed templates 檢查，並回報漂移」），無須獨立程式路徑。新增旗標或兄弟技能會把一個已可透過自然語言入口表達的功能，拆散它的表面範圍。

把設定管理保持在單一技能，也避免了 seed templates 演進時兩個技能互相漂移的維護成本。

## 先前的請求

- #106 — 功能請求：為 setup-matt-pocock-skills 提供 verify/check 模式
