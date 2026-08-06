# 超出範圍知識庫

repo 中的 `.out-of-scope/` 目錄儲存被拒絕功能請求的持久記錄。它有兩個用途：

1. **組織記憶** — 功能為何被拒絕，這樣 issue 關閉時推理不會遺失
2. **去重複** — 當新進的 issue 與先前的拒絕相符時，技能可以浮現先前的決策，而不是重新爭論一遍

## 目錄結構

```
.out-of-scope/
├── dark-mode.md
├── plugin-system.md
└── graphql-api.md
```

每個**概念**一個檔案，而不是每個 issue 一個。請求相同內容的多個 issues 會歸入同一個檔案。

## 檔案格式

檔案應以輕鬆、可讀的風格撰寫——比較像一份簡短的設計文件，而不是資料庫條目。用段落、程式碼範例與實例讓推理清楚明瞭，對第一次接觸它的人有用。

```markdown
# Dark Mode

This project does not support dark mode or user-facing theming.

## Why this is out of scope

The rendering pipeline assumes a single color palette defined in
`ThemeConfig`. Supporting multiple themes would require:

- A theme context provider wrapping the entire component tree
- Per-component theme-aware style resolution
- A persistence layer for user theme preferences

This is a significant architectural change that doesn't align with the
project's focus on content authoring. Theming is a concern for downstream
consumers who embed or redistribute the output.

```ts
// The current ThemeConfig interface is not designed for runtime switching:
interface ThemeConfig {
  colors: ColorPalette; // single palette, resolved at build time
  fonts: FontStack;
}
```

## Prior requests

- #42 — "Add dark mode support"
- #87 — "Night theme for accessibility"
- #134 — "Dark theme option"
```

### 為檔案命名

為概念使用簡短、具描述性的 kebab-case 名稱：`dark-mode.md`、`plugin-system.md`、`graphql-api.md`。名稱要夠容易辨識，讓瀏覽目錄的人不需要開啟檔案就能理解什麼被拒絕了。

### 撰寫理由

理由應該有實質內容——不是「我們不想要這個」，而是為什麼。好的理由會引用：

- 專案範圍或理念（「本專案聚焦於 X；theming 是下游的考量」）
- 技術限制（「支援這個需要 Y，而這與我們的 Z 架構衝突」）
- 策略決策（「我們選擇使用 A 而非 B，因為……」）

理由應該耐用。避免引用暫時的情況（「我們現在太忙了」）——那些不是真正的拒絕，而是延後。

## 何時檢查 `.out-of-scope/`

在分診期間（第 1 步：收集上下文），讀取 `.out-of-scope/` 中的所有檔案。評估新 issue 時：

- 檢查請求是否與現有的超出範圍概念相符
- 比對依概念相似度，而非關鍵字——「night theme」會對應到 `dark-mode.md`
- 如果有相符，把它浮現給維護者：「這類似 `.out-of-scope/dark-mode.md`——我們先前因為 [reason] 拒絕過這個。你現在還是一樣的看法嗎？」

維護者可以：

- **確認** — 新 issue 被加到既有檔案的「Prior requests（先前請求）」清單，然後關閉
- **重新考慮** — 超出範圍的檔案被刪除或更新，issue 繼續走正常分診
- **不同意** — 這些 issues 相關但不同，繼續正常分診

## 何時寫入 `.out-of-scope/`

只有當**enhancement**（而非 bug）以 `wontfix` 被*拒絕*時。這對 enhancement PR 的適用，與對 issues 完全相同——被拒絕的 PR 會記錄在這裡，這樣相同的請求不會以新程式碼的形式再次出現。

當某個東西因為**已實作**而以 `wontfix` 關閉時，**不要**寫在這裡。那是已建置的功能，而不是被拒絕的；記錄它會以虛假的拒絕污染去重複檢查。相反地，關閉評論會指向該功能已經存在的地方。

流程：

1. 維護者決定某個功能請求超出範圍
2. 檢查是否已有相符的 `.out-of-scope/` 檔案
3. 如果有：把新 issue 附加到「Prior requests（先前請求）」清單
4. 如果沒有：建立新檔案，包含概念名稱、決策、理由與第一筆先前請求
5. 在 issue 上貼評論，說明決策並提及 `.out-of-scope/` 檔案
6. 以 `wontfix` 標籤關閉 issue

## 更新或移除超出範圍的檔案

如果維護者對先前拒絕的概念改變了想法：

- 刪除 `.out-of-scope/` 檔案
- 技能不需要重新開啟舊 issues——它們是歷史記錄
- 觸發重新考慮的新 issue 繼續走正常分診
