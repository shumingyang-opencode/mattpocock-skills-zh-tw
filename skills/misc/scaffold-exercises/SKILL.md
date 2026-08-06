---
name: scaffold-exercises
description: 建立帶有 section、題目、解答與講解、且能通過 lint 檢查的練習目錄結構。當使用者想要建立練習骨架、建立練習樁，或設定新的課程 section 時使用。
---

# 建立練習骨架（Scaffold Exercises）

建立能通過 `pnpm ai-hero-cli internal lint` 的練習目錄結構，然後用 `git commit` 提交。

## 目錄命名

- **Sections**：`exercises/` 內部的 `XX-section-name/`（例如 `01-retrieval-skill-building`）
- **練習**：section 內部的 `XX.YY-exercise-name/`（例如 `01.03-retrieval-with-bm25`）
- Section 號碼 = `XX`，練習號碼 = `XX.YY`
- 名稱使用 dash-case（小寫、連字號）

## 練習變體

每個練習至少需要以下子資料夾之一：

- `problem/` - 帶有 TODO 的學生工作區
- `solution/` - 參考實作
- `explainer/` - 概念性材料，沒有 TODO

建立樁時，除非計畫另有指定，否則預設使用 `explainer/`。

## 必備檔案

每個子資料夾（`problem/`、`solution/`、`explainer/`）需要一個 `readme.md`，它必須：

- **不是空的**（必須有真實內容，即使是單一標題行也可以）
- 沒有壞掉的連結

建立樁時，建立一個帶有標題與描述的最小 readme：

```md
# Exercise Title

Description here
```

如果子資料夾有程式碼，它也需要一個 `main.ts`（>1 行）。但對於樁，一個只有 readme 的練習也可以。

## 工作流程

1. **解析計畫** - 擷取 section 名稱、練習名稱與變體類型
2. **建立目錄** - 為每個路徑 `mkdir -p`
3. **建立樁 readmes** - 每個變體資料夾一個帶有標題的 `readme.md`
4. **執行 lint** - `pnpm ai-hero-cli internal lint` 來驗證
5. **修正任何錯誤** - 反覆直到 lint 通過

## Lint 規則摘要

linter（`pnpm ai-hero-cli internal lint`）檢查：

- 每個練習都有子資料夾（`problem/`、`solution/`、`explainer/`）
- `problem/`、`explainer/` 或 `explainer.1/` 至少有一個存在
- 主要子資料夾中 `readme.md` 存在且非空
- 沒有 `.gitkeep` 檔案
- 沒有 `speaker-notes.md` 檔案
- readme 中沒有壞掉的連結
- readme 中沒有 `pnpm run exercise` 命令
- 每個子資料夾需要 `main.ts`，除非它只有 readme

## 移動/重新命名練習

重新編號或移動練習時：

1. 使用 `git mv`（不是 `mv`）來重新命名目錄 - 保留 git 歷史
2. 更新數字前綴以維持順序
3. 移動後重新執行 lint

範例：

```bash
git mv exercises/01-retrieval/01.03-embeddings exercises/01-retrieval/01.04-embeddings
```

## 範例：從計畫建立樁

給定一個像這樣的計畫：

```
Section 05: Memory Skill Building
- 05.01 Introduction to Memory
- 05.02 Short-term Memory (explainer + problem + solution)
- 05.03 Long-term Memory
```

建立：

```bash
mkdir -p exercises/05-memory-skill-building/05.01-introduction-to-memory/explainer
mkdir -p exercises/05-memory-skill-building/05.02-short-term-memory/{explainer,problem,solution}
mkdir -p exercises/05-memory-skill-building/05.03-long-term-memory/explainer
```

然後建立 readme 樁：

```
exercises/05-memory-skill-building/05.01-introduction-to-memory/explainer/readme.md -> "# Introduction to Memory"
exercises/05-memory-skill-building/05.02-short-term-memory/explainer/readme.md -> "# Short-term Memory"
exercises/05-memory-skill-building/05.02-short-term-memory/problem/readme.md -> "# Short-term Memory"
exercises/05-memory-skill-building/05.02-short-term-memory/solution/readme.md -> "# Short-term Memory"
exercises/05-memory-skill-building/05.03-long-term-memory/explainer/readme.md -> "# Long-term Memory"
```
