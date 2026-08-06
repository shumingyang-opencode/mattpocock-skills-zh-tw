# 好測試與壞測試

## 好測試

**整合風格**：透過真實介面測試，而不是模擬內部部件。

```typescript
// GOOD: Tests observable behavior
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

特徵：

- 測試使用者 / 呼叫者在乎的行為
- 只使用公開 API
- 能安然度過內部重構
- 描述 WHAT，不是 HOW
- 每個測試一個邏輯斷言

## 壞測試

**實作細節測試**：耦合到內部結構。

```typescript
// BAD: Tests implementation details
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

紅旗：

- 模擬內部協作者
- 測試私有方法
- 對呼叫次數 / 順序做斷言
- 重構但行為不變時測試壞掉
- 測試名稱描述 HOW 而不是 WHAT
- 透過外部手段而不是介面驗證

```typescript
// BAD: Bypasses interface to verify
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// GOOD: Verifies through interface
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```

**同義反覆測試**：期望值重述實作，所以測試依構造而通過。

```typescript
// BAD: Expected value is recomputed the way the code computes it
test("calculateTotal sums line items", () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, i) => sum + i.price, 0);
  expect(calculateTotal(items)).toBe(expected);
});

// GOOD: Expected value is an independent, known literal
test("calculateTotal sums line items", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```
