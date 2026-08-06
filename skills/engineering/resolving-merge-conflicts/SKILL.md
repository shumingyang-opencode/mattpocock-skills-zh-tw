---
name: resolving-merge-conflicts
description: "當你需要解決進行中的 git merge/rebase 衝突時使用。"
---

1. **檢視目前狀態**，也就是 merge/rebase 的目前狀態。檢查 git 歷史與衝突檔案。

2. **為每個衝突找出主要來源**。深入理解每個變更為什麼被做，以及原始意圖是什麼。讀 commit 訊息、查 PR、查原始 issue/ticket。

3. **解決每個 hunk。** 盡可能保留兩邊的意圖。在不相容之處，選擇符合 merge 陳述目標的一方，並記下取捨。**不要**發明新行為。永遠解決；絕不 `--abort`。

4. 找出專案的**自動化檢查**並執行它們——通常是 typecheck，然後測試，然後格式。修好任何被 merge 弄壞的東西。

5. **完成 merge/rebase。** 把所有東西加入並 commit。如果是在 rebase，繼續 rebase 流程直到所有 commit 都 rebase 完。
