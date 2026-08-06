---
name: setup-ts-deep-modules
description: 將 dependency-cruiser 接入 TypeScript repo，讓每個套件都是深模組 — 實作藏在子資料夾中，只能透過其進入點檔案觸達。使用者觸發。
disable-model-invocation: true
---

# 設定 TS 深模組（Setup TS Deep Modules）

讓此 repo 中的每個套件都是**深模組**：小介面後面的大量行為。套件的公開表面是它的**進入點** — 套件根目錄中的檔案 — 而其子資料夾中的一切都被隱藏。此技能安裝 [dependency-cruiser](https://github.com/sverweij/dependency-cruiser) 以及讓進入點成為唯一入口的規則，然後證明規則確實咬人。

對於詞彙（深模組、介面、接縫、深度），執行 `/codebase-design` 技能 — 全程使用它的語言。

## 這強制出來的形狀

```
src/packages/
  <name>/
    index.ts        ← 一個進入點（公開）。從外部匯入這個。
    client.ts       ← 另一個進入點。套件可以暴露多個（SEVERAL）。
    lib/            ← 實作：對外隱藏，彼此之間可以自由匯入。
    tests/          ← 共置的測試 + 固定裝置（一個子資料夾，所以是私有的）。
```

公開表面是套件的**根目錄檔案** — 不是一個指定的 `index.ts`。依照慣例，實作住在 `lib/`、測試住在 `tests/`，給每個套件相同的兩資料夾形狀。但規則本身是通用的：*任何*子資料夾中的*任何東西*都是私有的，所以您永遠不需要擴充設定來新增資料夾。

四個規則，全部是 `error`：

1. **進入點邊界** — 套件外的程式碼（app 程式碼或另一個套件）只能匯入該套件的進入點（其根目錄檔案），絕不能匯入其子資料夾中的任何東西。
2. **套件內自由** — 套件自己的檔案彼此自由匯入。
3. **測試透過進入點** — `<pkg>/tests/` 下的檔案可以匯入任何套件的進入點與它們自己的 `tests/` 固定裝置，但絕不能匯入任何套件的子資料夾內部（即使自己的也不行）。跨套件的整合測試可以；深層匯入不行。
4. **無循環** — 沒有依賴循環。

**進入點，不是 barrel。** 因為公開表面是*每個*根目錄檔案，一個套件可以暴露幾個小的進入點（`index.ts`、`client.ts`、`server.ts`），而不是把一切漏斗進一個巨大的 `index.ts`。重新匯出整個子樹的 barrel 檔案是不被鼓勵的 — 保持進入點小而把實作藏在子資料夾中。

分層（哪個套件可以依賴哪個）是*另一個*關注點，在設定中留為一個註解掉的樁，供此 repo 填寫。

## 步驟

### 1. 偵測環境

- **套件管理員** — `pnpm-lock.yaml` → pnpm、`yarn.lock` → yarn、`bun.lockb` → bun，否則 npm。用它執行下面每個命令（`pnpm`/`yarn`/`npm run`/`bunx`）。
- **套件根目錄** — 如果 `src/` 存在就用 `src/packages`，否則用 `packages`。如果 repo 已經有一個不同的明顯慣例，與使用者確認選擇。
- **既有設定** — 檢查是否有 `.dependency-cruiser.*` 檔案。如果存在，**不要**覆寫它：把四個規則與選項合併進去，並告訴使用者您新增了什麼。

**完成於：** 套件管理員、套件根目錄與既有設定狀態都已得知。

### 2. 安裝 dependency-cruiser

用偵測到的套件管理員安裝 `dependency-cruiser` 作為 devDependency。

**完成於：** `dependency-cruiser` 在 `devDependencies` 中。

### 3. 撰寫設定

將 [`dependency-cruiser.config.cjs`](./dependency-cruiser.config.cjs) 複製到 repo 根目錄作為 `.dependency-cruiser.cjs`。將 `PACKAGES_ROOT` 設定為第 1 步偵測到的根目錄。規則基於路徑深度且與副檔名無關，所以沒有其他需要調整的。

**完成於：** `.dependency-cruiser.cjs` 存在且 `PACKAGES_ROOT` 正確，四個禁止規則都在。

### 4. 將它接入檢查

- 新增一個 `lint:boundaries` 腳本：`depcruise <packages-root>`（或 `depcruise src`）。
- 將它摺進 repo 的總括檢查命令 — 那個已經執行型別檢查的命令（例如 `check` / `ci` / `validate` 腳本）。**不要**碰 `tsconfig` 或新增路徑別名。
- 如果沒有總括腳本，新增 `lint:boundaries` 並告訴使用者把它納入 CI。

**完成於：** `lint:boundaries` 存在，並作為與型別檢查同一個命令的一部分執行。

### 5. 建立範例套件

建立一個已提交的 `<packages-root>/example/` 作為 copy-me 範本：

- `index.ts` — 一個進入點。匯出一個委派給內部檔案的函式（這樣套件可以看得見地*深*，而不是一個直通）。
- `lib/impl.ts` — 一個在**子資料夾**中的內部檔案，由 `index.ts` 匯入，從外部無法觸達。
- `tests/example.test.ts` — 只匯入 `../index`（一個進入點），並對公開函式做斷言。

告訴使用者這是一個可以複製或刪除的起始範本。

**完成於：** 範例套件存在，透過根目錄進入點暴露它的行為，並把 `impl` 藏在子資料夾中。

### 6. 證明規則確實咬人

這是整個技能的完成標準 — 一個在違反時不會失敗的設定是沒有價值的。

1. 執行 `lint:boundaries`。它必須在乾淨的範例上**通過**。
2. 暫時在 `tests/example.test.ts` 中新增一個深層匯入（例如 `import { thing } from "../lib/impl"`）。再次執行 `lint:boundaries` — 它必須以 `tests-through-entrypoints` **失敗**。
3. 回復深層匯入。再執行一次 — 它必須**通過**。

**完成於：** 您觀察到一個通過、然後深層匯入失敗、然後再通過。如果第 2 步沒有失敗，表示規則沒有正確接上 — 在結束前修正。

### 7. 記錄慣例

在**套件資料夾中**（`<packages-root>/README.md`）撰寫一個 `README.md` — 就在它所治理的套件旁邊 — 涵蓋：`src/packages/<name>/` 佈局（進入點在根目錄、`lib/` 給實作、`tests/` 給測試）、「只透過套件的進入點（其根目錄檔案）匯入」，以及如何執行 `lint:boundaries`。**明確勸阻 barrel 檔案** — 暴露幾個小的進入點，而不是透過一個 index 重新匯出整個子樹。讓它保持為 copy-me 片段加上每個規則一段。

然後從 repo 的代理指令檔案 — 存在的話用 `CLAUDE.md`，否則用 `AGENTS.md`（如果兩者都不存在就建立 `AGENTS.md`）— 新增一個**脈絡指標**指向它。一行就夠了，例如 `Packages are deep modules — see [src/packages/README.md](./src/packages/README.md) before adding or importing one.` 這正是讓代理發現邊界規則而不是絆倒它的方式。

**完成於：** `<packages-root>/README.md` 存在且勸阻 barrels，repo 的 `CLAUDE.md`/`AGENTS.md` 連結到它。

## 備註

- 設定的 `$1` 反向引用（dependency-cruiser 的群組比對）正是讓套件可以觸達自己的內部而外部不能的方式 — 不要把它們拍平成每個套件的獨立規則。
- 公開與私有由**深度**決定：套件的根目錄檔案是進入點；子資料夾中的任何東西都是私有的。慣用的子資料夾是 `lib/`（實作）與 `tests/`，但規則不會硬編碼它們 — 任何子資料夾都是私有的，所以一個新資料夾永遠不需要變更設定。新增進入點只是新增一個根目錄檔案 — 不需要 barrel。
- 套件是**平坦的**：根目錄下只有一層直接子項。套件的內部可以嵌套到您喜歡的深度；一個套件不能包含另一個套件。
- 使用 `.cjs`（不是 `.js`），這樣設定的 `module.exports` 即使在 `"type": "module"` repo 中也能運作。
