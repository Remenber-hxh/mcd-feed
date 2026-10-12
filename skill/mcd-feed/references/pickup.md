# 家人到店或开车取餐

适合家人顺路去取：下班路上、开车经过。订单下在用户自己的账户里，家人凭取餐码取餐。

| 方式 | 参数 |
|---|---|
| 到店自取 | `beType=1`、`orderType=1`，不传 `beCode` |
| 得来速（开车取餐） | `beType=5`、`orderType=1`，必须传 `beCode` |

用户没说清时问一句："他是走进店里拿，还是开车从得来速拿？"

## 1. 找门店

调用 `query-nearby-stores`：

- 档案里有 `store`，或用户说了地点：`searchType=2`，`city` 填城市，`keyword` 填地点关键词（如"清竹园""建设路地铁站"）。
- 用户说"就去我收藏的那家"：`searchType=1`。没有收藏记录时，改用 `searchType=2`。

展示 2–3 家门店让用户选。门店 `reservation=true` 时，完整展示 `reservationTimeOptions`，`today=true` 的标"（今天）"。得来速记下所选门店的 `beCode`。

## 2. 取餐时间

家人想几点到店就按几点预约，换算成 `reservationDate`；马上去拿就不传。

## 3. 挑餐和算价

按 `references/meals.md` 完成，用本流程的场景参数。核价返回的 `takeWayList[]` 列出取餐方式（如堂食、外带），按用户的选择记下 `takeWayCode`。

## 4. 确认卡

```
下单确认
取餐人：爸爸
门店：建设路店（得来速）
取餐时间：今天 18:30
餐品：麦辣鸡腿堡套餐（可乐去冰）
取餐方式：外带
价格：原价 ¥39.0，用券后 ¥27.0
回复"好"就下单
```

## 5. 下单

用户确认后调用 `create-order`：`storeCode`、`beCode`（仅得来速）、`beType`、`orderType=1`、`items`、`takeWayCode`、预约时的 `reservationDate`。把支付链接给用户。

## 6. 把取餐码给家人

用户付完款后调用 `query-order`，拿到取餐码；外带订单如果返回了取餐柜二维码，一并告诉用户。然后写一条带门店、时间、取餐码的消息，例如：

> 爸，我在建设路店给你点了份晚饭，6 点半以后开车过去，得来速报取餐码 A123 就行。

运行 `python scripts/people.py log <称呼> "<餐品名>"`；用户说了常去的门店，用 `set --store` 记下。
