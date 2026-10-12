# 挑餐、健康把关、用券算价

外送、到店、团餐三个流程都用这一套。调用时带上所在流程的场景参数：

| 流程 | 参数 |
|---|---|
| 外送 | `beType=2`、`orderType=2`、`storeCode`、`beCode` |
| 到店自取 | `beType=1`、`orderType=1`、`storeCode`，不传 `beCode` |
| 得来速 | `beType=5`、`orderType=1`、`storeCode`、`beCode` |
| 团餐 | `beType=6`、`orderType=2`、`storeCode`、`beCode` |

预约时，下面每个调用都带同一个 `reservationDate`。

## 1. 拉菜单

调用 `query-meals`，得到在售餐品的分类、编码、价格、标签，以及可随单购买的商品（`withOrder`，如早餐卡、麦金卡和随单优惠商品）。

## 2. 挑 1–3 个候选

按这个顺序：

1. 用户点名要的；
2. 档案里的 `usual`（常点）和 `likes`；
3. 按时段推荐：早上选早餐套餐，中午和晚上选汉堡套餐，夜里选份量小的。

去掉含 `avoid` 的餐品。

## 3. 特制和换配菜

忌口能靠特制解决（"不要洋葱""可乐去冰"），或用户想换套餐里的配菜时，调用 `query-meal-detail`（`code` 为餐品编码）：

- `supportModify=true` 表示可以特制。不主动展开全部特制选项，只处理用户提到的。
- 传 `modification.values[]` 时：用户选中的项，`key` 用 `selectedKey`；同组里有 `unselectedKey` 的未选中项，也要传入，`key` 用 `unselectedKey`。
- 换配菜通过 `roundList[].comboItemList[]` 传入新选的商品编码和数量。

## 4. 健康把关

档案里有 `health`，或用户提到"控糖、少盐、在减脂、血压高"时：

1. 调用 `list-nutrition-foods`，拿到常见餐品的能量、蛋白质、脂肪、碳水化合物、钠等数据。
2. 用这些数据给候选排序或剔除，例如：控糖时饮料换无糖或不加糖，避开甜品；少盐时优先钠低的；低热量时控制总能量。
3. 在确认卡里用一行说明依据，例如"按控糖挑的：饮料换成了无糖豆浆"。只写数据能支持的话，不给医疗建议。

营养数据里查不到的餐品，如实说明"没有这款的营养数据"。

## 5. 用券

1. 调用 `available-coupons` 看有没有可领的券。有的话问一句："有 N 张券可以领，要我顺手领了吗？"用户同意后调用 `auto-bind-coupons`。
2. 调用 `query-store-coupons`，拿到这家店、这个时段、这种取餐方式能用的券。
3. 用户问"我有哪些券"时，调用 `query-my-coupons` 展示卡包。卡包里的券不一定能用在当前订单，能不能用以 `query-store-coupons` 为准。

## 6. 核价，选最省的方案

对每个候选，分别用"不用券"和"用能用的券"调用 `calculate-price`，必要时加上随单购商品，比较实付金额。

- 返回金额单位是"分"，展示时除以 100。
- 到店场景，`calculate-price` 返回的 `data.takeWayList[]` 是取餐方式（堂食、外带等），记下用户选的 `code`，下单时作为 `takeWayCode` 传入。
- 团餐场景另需 `gmServiceCode`，见 `references/group.md`。
- 菜单价和核价结果不一致时，以核价结果为准。

确认卡里展示：原价、用券后实付、用了哪几张券、配送费（外送时）。
