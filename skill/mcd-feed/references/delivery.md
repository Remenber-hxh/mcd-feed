# 给家人送餐上门（麦乐送）

参数：`beType=2`、`orderType=2`。

## 1. 听懂需求

从用户的话里提取以下几项，缺的再问，一次只问一个：

| 要素 | 例子 | 缺了怎么办 |
|---|---|---|
| 收餐人 | 妈妈、对象、妹妹 | 必须问 |
| 送达时间 | 现在、明早 8 点、今晚 10 点 | 默认现在尽快送 |
| 想吃什么 | 早餐、汉堡、老样子 | 按档案推荐 |
| 想说的话 | 天冷了多穿点 | 可以没有 |
| 给骑手的备注 | 放门口、到了打电话 | 可以没有 |

读收餐人档案，按 SKILL.md"时间"一节换算送达时间。

## 2. 找到收货地址

调用 `delivery-query-addresses`。返回列表在 `data.addresses[]`，每项有 `addressId`、`contactName`、`fullAddress`、`phone`。

- 用档案里的 `contact` 匹配 `contactName`；同一联系人有多个地址时，再用 `place` 匹配 `fullAddress`。
- 找不到时，向用户收集：城市（如"南京市"）、地址（小区或楼宇）、门牌号、联系人姓名、称谓（先生 / 女士）、11 位手机号。复述一遍，用户确认后调用 `delivery-create-address`，再重新查询拿到 `addressId`。
- 这些信息只用于在用户自己的麦当劳账户里建地址。本地档案只记联系人姓名和小区名。

## 3. 找能送的门店

调用 `delivery-query-stores`（`addressId`，`beType=2`），取第一家可配送门店的 `storeCode` 和 `beCode`，后续都用这一家。

- 没有可配送门店：告诉用户"这个地址附近暂时没有能送的麦当劳"，建议换个时间再试，或改成到店取餐（`references/pickup.md`）。

## 4. 挑餐和算价

按 `references/meals.md` 完成挑餐、健康把关、用券和核价。场景参数：`storeCode`、`beCode`、`beType=2`、`orderType=2`，预约时带 `reservationDate`。

## 5. 确认卡

```
下单确认
收餐人：妈妈（清竹园，138****5678）
送达：明天 08:00 左右
门店：XX 店
餐品：猪柳蛋麦满分套餐（不要洋葱）
价格：原价 ¥24.0，用券后 ¥15.0（含配送费 ¥X）
给骑手的备注：放门口，不用敲门
回复"好"就下单
```

- 备注 `remark` 最多 50 字，是给门店和骑手看的。用户想对家人说的话放进第 7 步的消息，不写进备注。
- 用户要改（换餐、改时间、去掉某样东西），回到对应步骤重新算价，再出确认卡。

## 6. 下单

用户确认后调用 `create-order`：`addressId`、`storeCode`、`beCode`、`beType=2`、`orderType=2`、`items`（含 `couponId` / `couponCode`、特制 `modification`）、`withOrder`（随单购，有才传）、预约时的 `reservationDate`、`remark`、`needTableware`。

把支付链接给用户，并说："付完回我'付好了'，我帮你看订单状态。"

## 7. 写消息和记账

- 按 SKILL.md"写给家人的消息"写一条可转发的消息。
- 运行 `python scripts/people.py log <称呼> "<餐品名>"`。第一次给这位家人下单时，先用 `set` 建档。
- 后续跟进见 `references/after-order.md`。
