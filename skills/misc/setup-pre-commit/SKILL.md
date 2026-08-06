---
name: setup-pre-commit
description: 在目前的 repo 中以 lint-staged（Prettier）、型別檢查與測試設定 Husky pre-commit hooks。當使用者想要新增 pre-commit hooks、設定 Husky、設定 lint-staged，或新增提交時的格式化/型別檢查/測試時使用。
---

# 設定 Pre-Commit Hooks

## 這會設定什麼

- **Husky** pre-commit hook
- **lint-staged** 在所有已暫存的檔案上執行 Prettier
- **Prettier** 設定（如果缺少）
- pre-commit hook 中的 **typecheck** 與 **test** 腳本

## 步驟

### 1. 偵測套件管理員

檢查 `package-lock.json`（npm）、`pnpm-lock.yaml`（pnpm）、`yarn.lock`（yarn）、`bun.lockb`（bun）。使用存在的那個。如果不清楚，預設為 npm。

### 2. 安裝相依套件

安裝為 devDependencies：

```
husky lint-staged prettier
```

### 3. 初始化 Husky

```bash
npx husky init
```

這會建立 `.husky/` 目錄，並將 `prepare: "husky"` 加到 package.json。

### 4. 建立 `.husky/pre-commit`

寫入這個檔案（Husky v9+ 不需要 shebang）：

```
npx lint-staged
npm run typecheck
npm run test
```

**調整**：將 `npm` 取代為偵測到的套件管理員。如果 repo 在 package.json 中沒有 `typecheck` 或 `test` 腳本，省略那些行並告知使用者。

### 5. 建立 `.lintstagedrc`

```json
{
  "*": "prettier --ignore-unknown --write"
}
```

### 6. 建立 `.prettierrc`（如果缺少）

只有當沒有 Prettier 設定存在時才建立。使用這些預設值：

```json
{
  "useTabs": false,
  "tabWidth": 2,
  "printWidth": 80,
  "singleQuote": false,
  "trailingComma": "es5",
  "semi": true,
  "arrowParens": "always"
}
```

### 7. 驗證

- [ ] `.husky/pre-commit` 存在且可執行
- [ ] `.lintstagedrc` 存在
- [ ] package.json 中的 `prepare` 腳本是 `"husky"`
- [ ] `prettier` 設定存在
- [ ] 執行 `npx lint-staged` 來驗證它可以運作

### 8. 提交

暫存所有變更/建立的檔案，並以訊息提交：`Add pre-commit hooks (husky + lint-staged + prettier)`

這會跑過新的 pre-commit hooks — 一個很好的煙霧測試，確認一切都能運作。

## 備註

- Husky v9+ 不需要 hook 檔案中的 shebangs
- `prettier --ignore-unknown` 會跳過 Prettier 無法解析的檔案（圖片等）
- pre-commit 先執行 lint-staged（快速、只針對已暫存），然後是完整的型別檢查與測試
