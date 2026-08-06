# 撰寫代理簡報

代理簡報是當 issue 或 PR 移入 `ready-for-agent` 時，貼在 GitHub issue 或 PR 上的結構化評論。它是 AFK 代理據以工作的權威規格說明。原始內文與討論是脈絡——代理簡報才是合約。

簡報陳述**代理應該做什麼**，這延伸到兩個介面：對 issue 而言，是從零開始建置這項變更；對 PR 而言，是*對既有 diff* 還剩什麼要做——完成它、補上缺口、處理審查意見。兩種情況的原則相同；下方的 PR 範例會顯示差異。

## 原則

### 耐用勝於精確

issue 可能會在 `ready-for-agent` 停留數天或數週。程式碼庫在此期間會改變。撰寫簡報時，要讓它在檔案被重新命名、移動或重構後依然有用。

- **要** 描述介面、型別與行為合約
- **要** 指名代理應尋找或修改的具體型別、函式簽名或設定形狀
- **不要** 引用檔案路徑——它們會過時
- **不要** 引用行號
- **不要** 假設目前的實作結構會保持不變

### 行為式，而非程序式

描述系統應該做**什麼**，而不是**如何**實作。代理會重新探索程式碼庫，做出自己的實作決策。

- **好：**「`SkillConfig` 型別應該接受型別為 `CronExpression` 的選用 `schedule` 欄位」
- **壞：**「開啟 src/types/skill.ts，並在第 42 行加上 schedule 欄位」
- **好：**「當使用者以無參數執行 `/triage` 時，他們應該看到需要關注的 issues 摘要」
- **壞：**「在 main handler 函式中加上一個 switch 陳述式」

### 完整的驗收標準

代理需要知道何時算完成。每個代理簡報都必須有具體、可測試的驗收標準。每個標準都應該可以獨立驗證。

- **好：**「執行 `gh issue list --label needs-triage` 會回傳已通過初步分類的 issues」
- **壞：**「Triage 應該正常運作」

### 明確的範圍邊界

明確說明什麼是超出範圍的。這能防止代理鍍金，或對相鄰功能做出臆測。

## 範本

```markdown
## Agent Brief

**Category:** bug / enhancement
**Summary:** one-line description of what needs to happen

**Current behavior:**
Describe what happens now. For bugs, this is the broken behavior.
For enhancements, this is the status quo the feature builds on.

**Desired behavior:**
Describe what should happen after the agent's work is complete.
Be specific about edge cases and error conditions.

**Key interfaces:**
- `TypeName` — what needs to change and why
- `functionName()` return type — what it currently returns vs what it should return
- Config shape — any new configuration options needed

**Acceptance criteria:**
- [ ] Specific, testable criterion 1
- [ ] Specific, testable criterion 2
- [ ] Specific, testable criterion 3

**Out of scope:**
- Thing that should NOT be changed or addressed in this issue
- Adjacent feature that might seem related but is separate
```

## 範例

### 好的代理簡報（bug）

```markdown
## Agent Brief

**Category:** bug
**Summary:** Skill description truncation drops mid-word, producing broken output

**Current behavior:**
When a skill description exceeds 1024 characters, it is truncated at exactly
1024 characters regardless of word boundaries. This produces descriptions
that end mid-word (e.g. "Use when the user wants to confi").

**Desired behavior:**
Truncation should break at the last word boundary before 1024 characters
and append "..." to indicate truncation.

**Key interfaces:**
- The `SkillMetadata` type's `description` field — no type change needed,
  but the validation/processing logic that populates it needs to respect
  word boundaries
- Any function that reads SKILL.md frontmatter and extracts the description

**Acceptance criteria:**
- [ ] Descriptions under 1024 chars are unchanged
- [ ] Descriptions over 1024 chars are truncated at the last word boundary
      before 1024 chars
- [ ] Truncated descriptions end with "..."
- [ ] The total length including "..." does not exceed 1024 chars

**Out of scope:**
- Changing the 1024 char limit itself
- Multi-line description support
```

### 好的代理簡報（enhancement）

```markdown
## Agent Brief

**Category:** enhancement
**Summary:** Add `.out-of-scope/` directory support for tracking rejected feature requests

**Current behavior:**
When a feature request is rejected, the issue is closed with a `wontfix` label
and a comment. There is no persistent record of the decision or reasoning.
Future similar requests require the maintainer to recall or search for the
prior discussion.

**Desired behavior:**
Rejected feature requests should be documented in `.out-of-scope/<concept>.md`
files that capture the decision, reasoning, and links to all issues that
requested the feature. When triaging new issues, these files should be
checked for matches.

**Key interfaces:**
- Markdown file format in `.out-of-scope/` — each file should have a
  `# Concept Name` heading, a `**Decision:**` line, a `**Reason:**` line,
  and a `**Prior requests:**` list with issue links
- The triage workflow should read all `.out-of-scope/*.md` files early
  and match incoming issues against them by concept similarity

**Acceptance criteria:**
- [ ] Closing a feature as wontfix creates/updates a file in `.out-of-scope/`
- [ ] The file includes the decision, reasoning, and link to the closed issue
- [ ] If a matching `.out-of-scope/` file already exists, the new issue is
      appended to its "Prior requests" list rather than creating a duplicate
- [ ] During triage, existing `.out-of-scope/` files are checked and surfaced
      when a new issue matches a prior rejection

**Out of scope:**
- Automated matching (human confirms the match)
- Reopening previously rejected features
- Bug reports (only enhancement rejections go to `.out-of-scope/`)
```

### 好的代理簡報（PR）

對 PR 而言，「Current behavior（目前行為）」描述 diff 的狀態，簡報要求代理完成或修復它，而不是從零開始建置。

```markdown
## Agent Brief

**Category:** enhancement
**Summary:** Finish the contributor's `--json` output flag for `triage list`

**Current behavior:**
The PR adds a `--json` flag that serializes the issue list to JSON. The happy
path works and the diff matches the project's command structure. Two gaps
remain: errors are still printed as human text (not JSON), and the new flag has
no test coverage.

**Desired behavior:**
With `--json`, all output — including errors — is well-formed JSON on stdout,
and the command's exit codes are unchanged. The existing human-readable output
is untouched when the flag is absent.

**Key interfaces:**
- The command's error path should emit `{ "error": string }` under `--json`
  instead of the plain-text error
- Reuse the existing serializer the PR already added; don't introduce a second

**Acceptance criteria:**
- [ ] `triage list --json` emits valid JSON for both success and error cases
- [ ] Exit codes match the non-JSON command
- [ ] A test covers the `--json` success output and one error case
- [ ] Default (non-JSON) output is byte-for-byte unchanged

**Out of scope:**
- Adding `--json` to any other command
- Changing the JSON shape of the success payload the PR already defined
```

### 壞的代理簡報

```markdown
## Agent Brief

**Summary:** Fix the triage bug

**What to do:**
The triage thing is broken. Look at the main file and fix it.
The function around line 150 has the issue.

**Files to change:**
- src/triage/handler.ts (line 150)
- src/types.ts (line 42)
```

這個很糟糕，因為：

- 沒有類別
- 描述含糊（「the triage thing is broken」）
- 引用了會過時的檔案路徑與行號
- 沒有驗收標準
- 沒有範圍邊界
- 沒有描述目前行為與期望行為的差異
