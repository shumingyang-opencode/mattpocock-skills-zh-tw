# 何時模擬

只在**系統邊界**模擬：

- 外部 API（付款、電子郵件等）
- 資料庫（有時——偏好測試資料庫）
- 時間 / 隨機性
- 檔案系統（有時）

不要模擬：

- 你自己的類別 / 模組
- 內部協作者
- 任何你能控制的東西

## 為可模擬性而設計

在系統邊界，設計容易模擬的介面：

**1. 使用依賴注入**

把外部相依傳入，而不是在內部建立：

```typescript
// Easy to mock
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Hard to mock
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

**2. 偏好 SDK 風格的介面，而不是通用 fetcher**

為每個外部操作建立特定函式，而不是一個帶條件邏輯的通用函式：

```typescript
// GOOD: Each function is independently mockable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// BAD: Mocking requires conditional logic inside the mock
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

SDK 方式的好處：
- 每個 mock 回傳一個特定形狀
- 測試設定中沒有條件邏輯
- 更容易看出一個測試觸及哪些端點
- 每個端點都有型別安全
