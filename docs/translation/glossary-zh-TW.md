# 翻譯術語錨點表（繁體中文）

本表供翻譯 worker 翻譯時統一譯法使用。覆蓋跨技能重複出現、且譯法可能分歧的核心術語。

**使用規則**：
- 左欄英文術語出現時，右欄繁中譯法為強制標準，不得自行改寫。
- 標註「保留英文」的術語，翻譯時不譯，原樣保留。
- 本表未收錄的術語，按上下文自然翻譯，保持技能內部自洽。
- 技能名、slash 命令（`/xxx`）、指令、程式碼區塊、路徑、URL、識別符一律保留英文。

## 一、流程動詞 / 技能動作

| 英文 | 繁中譯法 | 備註 |
|---|---|---|
| grilling | 保留英文 | 技能名，不譯 |
| grill | 保留英文 | 技能觸發詞，不譯 |
| triage | 分診 | 地圖標籤錨點 |
| diagnose | 診斷 | |
| debug | 除錯 | 繁體慣用「除錯/偵錯」 |
| implement | 實作 | 地圖標籤錨點 |
| review | 審查 | code-review 情境下 |
| refactor | 重構 | |
| mock | 模擬 | 動詞/名詞皆譯「模擬」 |
| stub | 樁 | 測試替身語境 |
| spy | 間諜 | 測試替身語境 |
| bisect | 二分 | git bisect 情境 |
| stress-test | 壓力測試 | |
| synthesise / synthesize | 綜合 | to-spec 情境 |
| bootstrap | 引導 / 啟動 | 依上下文 |

## 二、artifact / 產物類型

| 英文 | 繁中譯法 | 備註 |
|---|---|---|
| PRD | 保留英文 | Product Requirements Document，不譯 |
| ADR | 保留英文 | Architecture Decision Record，不譯 |
| CONTEXT.md | 保留英文 | 檔名，不譯 |
| agent brief | 代理簡報 | triage 產物 |
| issue | issue | 首字母小寫時保留英文，不譯為「議題/工單」 |
| Issue | Issue | 首字母大寫時保留英文 |
| Issue tracker | Issue 追蹤器 | 不譯為 backlog manager |
| PR | 保留英文 | Pull Request，不譯 |
| spec | 規格說明 | to-spec 貫穿術語；PRD 仍保留英文 |
| regression test | 回歸測試 | |
| acceptance criteria | 驗收標準 | |
| user story | 使用者故事 | |
| snapshot | 快照 | 測試語境 |
| fixture | 固定裝置 | 測試輸入資料 |
| seam | 接縫 | codebase-design 核心術語，_Avoid_: boundary |
| tracer bullet | 曳光彈 | to-tickets / tdd 術語 |
| harness | 執行環境 | 指 agent 運行的 harness；或依上下文譯「測試架」 |

## 三、codebase-design 架構詞彙（強制統一，禁止替換）

| 英文 | 繁中譯法 | 備註 |
|---|---|---|
| module | 模組 | _Avoid_: unit, component, service |
| interface | 介面 | 含型別+不變量+約束 |
| implementation | 實作 | |
| depth | 深度 | |
| deep (module) | 深模組 | |
| shallow (module) | 淺模組 | |
| adapter | 轉接器 | 或「適配器」，全文統一 |
| leverage | 槓桿收益 | 呼叫方從深度獲得的收益 |
| locality | 局部性 | 維護方從深度獲得的收益 |
| port | 連接埠 | ports & adapters 模式 |
| dependency injection | 依賴注入 | |

## 四、triage 狀態角色

| 英文 | 繁中譯法 | 備註 |
|---|---|---|
| needs-triage | needs-triage | 狀態標籤，保留英文 |
| needs-info | needs-info | 狀態標籤，保留英文 |
| ready-for-agent | ready-for-agent | 狀態標籤，保留英文 |
| ready-for-human | ready-for-human | 狀態標籤，保留英文 |
| ready-for-afk | ready-for-afk | 狀態標籤，保留英文 |
| wontfix | wontfix | 狀態標籤，保留英文 |
| Triage role | 分診角色 | |

## 五、測試 / TDD 術語

| 英文 | 繁中譯法 | 備註 |
|---|---|---|
| red → green | 紅 → 綠 | TDD 循環 |
| red-green-refactor | 紅-綠-重構 | |
| vertical slice | 垂直切片 | _Avoid_: horizontal slice |
| prefactor | 預先重構 | 「先讓改動變容易，再做容易的改動」 |
| tautological (test) | 同義反覆（測試） | 斷言重算實作邏輯 |
| implementation-coupled | 耦合實作細節 | |
| test double | 測試替身 | |

## 六、code-review 雙軸術語

| 英文 | 繁中譯法 | 備註 |
|---|---|---|
| Standards (axis) | 規範（軸） | |
| Spec (axis) | 規格（軸） | |
| smell (code smell) | 壞味道 | Fowler 程式碼壞味道 |
| smell baseline | 壞味道基線 | |
| merge-base | 合併基點 | git 三點 diff |
| scope creep | 範圍蔓延 | |

## 七、Matt 生態專有詞 / 通用角色

| 英文 | 繁中譯法 | 備註 |
|---|---|---|
| agent | 代理 | AFK agent = 離線代理 |
| AFK | 保留英文 | Away From Keyboard，不譯 |
| maintainer | 維護者 | |
| reporter | 報告人 | issue 提交者 |
| collaborator | 協作者 | |
| sub-agent | 子代理 | |
| out-of-scope | 超出範圍 | 既指狀態也指目錄 |
| gold-plating | 鍍金 | 過度裝飾 |
| throwaway (prototype/harness) | 一次性（原型/測試架） | |
| primary source | 主要來源 / 第一手來源 | |
| feedback loop | 回饋迴圈 | diagnosing-bugs 核心 |
| hitl / HITL | 保留英文 | Human-In-The-Loop，不譯 |
| model | 模型 | |
| harness | 執行環境 | 指 agent 運行環境 |
| smart zone | 智慧區 | 模型推理的上下文上限 |
| mode (plan mode etc.) | 模式 | |

## 八、規劃 / wayfinder 術語

| 英文 | 繁中譯法 | 備註 |
|---|---|---|
| to-spec | 保留英文 | 技能名/指令，不譯 |
| to-tickets | 保留英文 | 技能名/指令，不譯 |
| wayfinder | 保留英文 | 技能名/指令，不譯 |
| wayfinding | 尋路 | wayfinder 的活動/過程 |
| ticket | 保留英文 | 不譯「工單/議題」 |
| map | 地圖 | wayfinder:map issue；_Avoid_: 技能圖譜 |
| destination | 目的地 | |
| frontier | 前沿 | 開放、未阻塞、未認領的 ticket |
| fog of war | 戰爭迷霧 | |
| fog | 迷霧 | |
| route | 路線 | |
| Not yet specified | 尚未明確 | 地圖章節名 |
| Decisions so far | 已作決策 | 地圖章節名 |
| Out of scope | 超出範圍 | 地圖章節名 |
| claim | 認領 | 認領 ticket（透過指派） |
| child issue | 子 issue | issue 保留英文 |
| parent issue | 父 issue | |
| blocking edge | 阻塞邊 | to-tickets/wayfinder 術語 |
| Blocked by | 阻塞於 | ticket 模板章節名 |
| unblocked | 未阻塞 | |
| resolution comment | 結論評論 | 關閉 ticket 時發布的答案 |
| graduate | 轉化 | 迷霧轉化為 ticket |
| task | 任務 | wayfinder 票型之一；標籤 `wayfinder:task` 保留英文 |
| wide refactor | 大範圍重構 | to-tickets 例外切片 |
| blast radius | 影響半徑 | |
| expand–contract | 擴展-收縮 | |
| call site | 呼叫點 | |
| integration branch | 集成分支 | |

## 九、繁中 vs 簡中常見差異（優先使用左欄繁中）

| 繁中（使用） | 簡中（避免） | 英文來源 |
|---|---|---|
| 檔案 | 文件（當指 file） | file |
| 文件 | 文档 | document |
| 資訊 | 信息 | information |
| 程式 | 程序 | program |
| 程式碼 | 代码 | code |
| 介面 | 接口 | interface |
| 資料 | 数据 | data |
| 使用者 | 用户 | user |
| 預設 | 默认 | default |
| 除錯 / 偵錯 | 调试 | debug |
| 網路 | 网络 | network |
| 協定 | 协议 | protocol |
| 執行緒 | 线程 | thread |
| 非同步 | 异步 | async |
| 陣列 | 数组 | array |
| 快取 | 缓存 | cache |
| 效能 | 性能 | performance |
| 伺服器 | 服务器 | server |
| 專案 | 项目 | project |
| 實作 | 实现 | implement |
| 相容 | 兼容 | compatible |
| 整合 | 集成 | integration |
| 相依 / 依賴 | 依赖 | dependency |
| 回饋 | 反馈 | feedback |
| 導覽 | 导航 | navigation |
| 型別 | 类型 | type |
| 重新整理 | 刷新 | refresh |
| 記憶體 | 内存 | memory |
| 硬碟 | 硬盘 | disk |
| 雲端 | 云 | cloud |
| 輕量 | 轻量 | lightweight |
| 多執行緒 | 多线程 | multithreaded |
