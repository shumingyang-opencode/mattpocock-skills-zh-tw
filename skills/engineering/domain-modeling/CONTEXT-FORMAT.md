# CONTEXT.md 格式

## 結構

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

## 規則

- **要有主張。** 當同一個概念存在多個詞，挑最好的，其餘列在 `_Avoid_` 底下。
- **定義要精簡。** 最多一兩句。定義它是**什麼**，而不是它做什麼。
- **只納入這個專案上下文特有的術語。** 一般程式設計概念（timeout、錯誤型別、工具模式）即使專案大量使用也不屬於。加入術語前先問：這是這個上下文獨有的概念，還是一般程式設計概念？只有前者屬於。
- **當自然聚類浮現時，把術語歸在子標題下。** 如果所有術語都屬於單一內聚領域，扁平清單就夠了。

## 單一 vs 多上下文 repo

**單一上下文（多數 repo）：** 根目錄一份 `CONTEXT.md`。

**多個上下文：** 根目錄的 `CONTEXT-MAP.md` 列出上下文、它們在哪裡、以及它們彼此如何關聯：

```md
# Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md) — receives and tracks customer orders
- [Billing](./src/billing/CONTEXT.md) — generates invoices and processes payments
- [Fulfillment](./src/fulfillment/CONTEXT.md) — manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

技能會推斷適用哪種結構：

- 如果 `CONTEXT-MAP.md` 存在，讀它來找上下文
- 如果只有根目錄的 `CONTEXT.md`，是單一上下文
- 如果兩者都不存在，第一個術語定案時惰性地建立根目錄的 `CONTEXT.md`

當有多個上下文時，推斷目前主題與哪一個相關。如果不清楚，就問。
