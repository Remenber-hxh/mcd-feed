# 给家人单位或班级点团餐

适合请家人的同事、同学一起吃：给爸爸部门送下午茶、给妹妹全班加餐。参数：`beType=6`、`orderType=2`。

## 1. 听懂需求

| 要素 | 例子 | 缺了怎么办 |
|---|---|---|
| 送给谁 | 妹妹全班、爸爸部门 | 必须问 |
| 人数 | 30 人 | 必须问 |
| 预算 | 人均 25 元，或总共 800 元 | 必须问 |
| 送达地址 | 学校门卫室、公司前台 | 必须问 |
| 送达时间 | 周五下午 3 点 | 必须问，团餐一般要预约 |
| 口味要求 | 不要辣、要有饮料 | 可以没有 |

## 2. 地址和门店

1. 按 `references/delivery.md` 第 2 步找到或新建送达地址，联系人填负责接收的家人。
2. 调用 `delivery-query-stores`（`addressId`，`beType=6`），拿到 `storeCode` 和 `beCode`。
3. 没有支持团餐的门店时，告诉用户，并建议改成普通外送分几单送（`references/delivery.md`）。

## 3. 按人均预算搭配

调用 `query-meals`（`beType=6`、`orderType=2`、`reservationDate`），按人均预算搭配：

| 人均 | 搭配 |
|---|---|
| 20 元以下 | 小食 |
| 20–30 元 | 汉堡 + 小食，或汉堡 + 饮料 |
| 30–40 元 | 汉堡 + 薯条或小食 + 饮料 |
| 40–50 元 | 汉堡 + 薯条 + 小食 + 饮料 |
| 50 元以上 | 更丰富的组合，小食尽量不重复 |

口味和健康要求按 `references/meals.md` 第 2–4 步处理。

## 4. 满减和助餐服务

1. 调用 `query-promotions`（`beType=6`、`orderType=2`、`storeCode`、`beCode`、`reservationDate`），拿到满减、满折规则：`promotionType=31` 是满额减，`33` 是订单折扣；`products` 里 `type=1` 是只适用这些商品，`2` 是不适用，`3` 是全部适用。
2. 离下一档优惠只差一点时，算一下"加 X 元能省 Y 元"。只有加购成本低于优惠金额才建议加，并把净省多少说清楚。
3. 调用 `query-meal-assistance`（`storeCode`、`beCode`、`beType=6`、`orderType=2`、`reservationDate`），列出助餐服务，让用户选一个，记下 `gmServiceCode`。

## 5. 核价和确认

调用 `calculate-price`，带上 `gmServiceCode`。多种优惠不能叠加时，分别核价，取实付最低的方案，并说明为什么放弃其他方案。

```
团餐确认
送到：清竹园中学门卫室（妹妹接收）
送达：周五 15:00 左右
份数：30 份，板烧鸡腿堡 + 中薯条 + 中可乐
价格：原价 ¥1050.0，满减后 ¥780.0，人均 ¥26.0
助餐服务：XX
回复"好"就下单
```

## 6. 下单和通知

用户确认后调用 `create-order`：`addressId`、`storeCode`、`beCode`、`beType=6`、`orderType=2`、`items`、`gmServiceCode`、`reservationDate`、`remark`。把支付链接给用户。

写一条给家人的消息，说清几点送到、送到哪、一共几份，例如：

> 妹，周五下午 3 点给你们班送 30 份麦当劳到门卫室，到了你去拿一下。
