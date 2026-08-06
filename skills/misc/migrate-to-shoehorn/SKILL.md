---
name: migrate-to-shoehorn
description: 將測試檔案從 `as` 型別斷言遷移到 @total-typescript/shoehorn。當使用者提到 shoehorn、想在測試中取代 `as`，或需要部分測試資料時使用。
---

# 遷移到 Shoehorn

## 為什麼用 shoehorn？

`shoehorn` 讓您可以在測試中傳入部分資料，同時讓 TypeScript 保持滿意。它以型別安全的替代方案取代 `as` 斷言。

**僅限測試程式碼。** 絕不要在正式程式碼中使用 shoehorn。

測試中 `as` 的問題：

- 被訓練成不要使用它
- 必須手動指定目標型別
- 對刻意錯誤的資料使用雙重 `as`（`as unknown as Type`）

## 安裝

```bash
npm i @total-typescript/shoehorn
```

## 遷移模式

### 大型物件但只需要少數屬性

之前：

```ts
type Request = {
  body: { id: string };
  headers: Record<string, string>;
  cookies: Record<string, string>;
  // ...20 more properties
};

it("gets user by id", () => {
  // Only care about body.id but must fake entire Request
  getUser({
    body: { id: "123" },
    headers: {},
    cookies: {},
    // ...fake all 20 properties
  });
});
```

之後：

```ts
import { fromPartial } from "@total-typescript/shoehorn";

it("gets user by id", () => {
  getUser(
    fromPartial({
      body: { id: "123" },
    }),
  );
});
```

### `as Type` → `fromPartial()`

之前：

```ts
getUser({ body: { id: "123" } } as Request);
```

之後：

```ts
import { fromPartial } from "@total-typescript/shoehorn";

getUser(fromPartial({ body: { id: "123" } }));
```

### `as unknown as Type` → `fromAny()`

之前：

```ts
getUser({ body: { id: 123 } } as unknown as Request); // wrong type on purpose
```

之後：

```ts
import { fromAny } from "@total-typescript/shoehorn";

getUser(fromAny({ body: { id: 123 } }));
```

## 何時使用每個

| Function        | Use case                                           |
| --------------- | -------------------------------------------------- |
| `fromPartial()` | Pass partial data that still type-checks           |
| `fromAny()`     | Pass intentionally wrong data (keeps autocomplete) |
| `fromExact()`   | Force full object (swap with fromPartial later)    |

## 工作流程

1. **收集需求** - 詢問使用者：
   - 哪些測試檔案有造成問題的 `as` 斷言？
   - 他們是否在處理只有某些屬性重要的大型物件？
   - 他們是否需要傳入刻意錯誤的資料來進行錯誤測試？

2. **安裝並遷移**：
   - [ ] 安裝：`npm i @total-typescript/shoehorn`
   - [ ] 找到帶有 `as` 斷言的測試檔案：`grep -r " as [A-Z]" --include="*.test.ts" --include="*.spec.ts"`
   - [ ] 用 `fromPartial()` 取代 `as Type`
   - [ ] 用 `fromAny()` 取代 `as unknown as Type`
   - [ ] 從 `@total-typescript/shoehorn` 新增 imports
   - [ ] 執行型別檢查來驗證
