---
name: git-guardrails-claude-code
description: 設定 Claude Code hooks 來在執行前阻擋危險的 git 命令（push、reset --hard、clean、branch -D 等）。當使用者想要防止破壞性的 git 操作、新增 git 安全 hooks，或在 Claude Code 中阻擋 git push/reset 時使用。
---

# 設定 Git 護欄（Setup Git Guardrails）

設定一個 PreToolUse hook，在 Claude 執行危險 git 命令之前攔截並阻擋它們。

## 會被阻擋的內容

- `git push`（所有變體，包含 `--force`）
- `git reset --hard`
- `git clean -f` / `git clean -fd`
- `git branch -D`
- `git checkout .` / `git restore .`

當被阻擋時，Claude 會看到一則訊息，告訴它沒有權限存取這些命令。

## 步驟

### 1. 詢問範圍

詢問使用者：只為**此專案**安裝（`.claude/settings.json`）還是**所有專案**（`~/.claude/settings.json`）？

### 2. 複製 hook 腳本

隨附的腳本位於：[scripts/block-dangerous-git.sh](scripts/block-dangerous-git.sh)

根據範圍將它複製到目標位置：

- **專案**：`.claude/hooks/block-dangerous-git.sh`
- **全域**：`~/.claude/hooks/block-dangerous-git.sh`

用 `chmod +x` 使它可執行。

### 3. 將 hook 加入設定

加到適當的設定檔：

**專案**（`.claude/settings.json`）：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

**全域**（`~/.claude/settings.json`）：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

如果設定檔已經存在，將 hook 合併到既有的 `hooks.PreToolUse` 陣列中 — 不要覆寫其他設定。

### 4. 詢問客製化

詢問使用者是否要從阻擋清單中新增或移除任何模式。據此編輯已複製的腳本。

### 5. 驗證

執行一個快速測試：

```bash
echo '{"tool_input":{"command":"git push origin main"}}' | <path-to-script>
```

應該以代碼 2 結束，並在 stderr 列印一則 BLOCKED 訊息。
