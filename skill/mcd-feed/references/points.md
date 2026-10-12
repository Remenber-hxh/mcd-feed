# 积分、积分商城、抽奖

## 1. 查积分

调用 `query-my-account`，展示可用积分、累计积分、冻结积分、即将过期的积分和过期时间。

有积分快过期时，提一句可以怎么用：换成券，下次给家人点餐时用；或者换个周边、礼品卡寄给家人。

## 2. 积分商城

调用 `mall-points-products`，可按 `catRuleIds` 筛选（逗号分隔多选）：

| catRuleIds | 类别 | 怎么用在家人身上 |
|---|---|---|
| `1>4` | 商品券 | 券进用户账户，下次给家人点餐时用 |
| `2` | 实物商品 | 寄到家人地址 |
| `2>8` | 周边产品 | 寄给家人当小礼物 |
| `2>9` | 实物礼品卡 | 寄给家人，让他们自己去吃 |
| `1>6>20` 等 | 派对和活动 | 走 `references/events.md` |

用户选中商品后，调用 `mall-product-detail`（`spuId`），列出各规格（SKU）让用户选。

- `shopId=2` 的商品用本文件的兑换流程。
- `shopId=5` 的是派对和活动，改走 `references/events.md`。

## 3. 兑换

兑换实物（`spuCategory="2"`）要收货地址：按 `references/delivery.md` 第 2 步找到家人的地址，拿到 `addressId`。

确认卡：

```
兑换确认
商品：麦麦周边 XX（规格：XX）× 1
消耗：XXX 积分（当前 XXXX，兑换后剩 XXX）
寄到：妈妈（清竹园，138****5678）
回复"好"就兑换
```

用户确认后调用 `mall-create-order`：`skuId`、`spuCategory`、`count`、实物时的 `addressId`。

- 一次只兑换一种商品。要换多种时，等上一单成功返回后再下下一单。
- 返回 `status=1` 是全部成功，`2` 是部分成功，`0` 是失败。部分成功或失败时，如实说明哪件没成。
- 换到的是券时，展示券名和券码数量。券码只展示给用户，不写进给家人的消息。
- 实物兑换成功后，写一条给家人的消息，例如："妈，用积分给你换了个麦当劳的杯子，过几天寄到家。"

## 4. 商城订单

- 用户问"我换过什么"：调用 `mall-order-list`（`size` 最多 10，翻页用上一页最后一条的 `lastId`）。
- 用户问某一单：调用 `mall-order-detail`（`orderId`），展示积分、金额、状态。凭证等信息引导用户在麦当劳 App 里查看。

## 5. 抽奖（仅在用户主动要求时）

1. 调用 `query-lottery-info`，展示活动名称、起止时间、单次消耗、奖品列表，以及 `drawDecision.nextConsumption`（这次实际会扣什么）。`fallbackConsumption` 不为空时，说明"本次先用抽奖次数，次数用完后改扣积分"。
2. `drawDecision.resourceEligible` 为 false 时，告诉用户这次抽不了，不调用抽奖。能不能抽只看这个字段，不根据 `availableTimes` 自己推断。
3. 用户明确确认后，调用 `draw-lottery` 一次。展示是否中奖和奖品；`status.code` 不是 SUCCESS 时，原样展示 `status.message`。
4. 不连抽，不试抽。用户想再抽一次，从第 1 步重新确认。
5. 用户问"我抽中过什么"：调用 `query-my-prizes`，按时间倒序展示奖品和状态（可用、已使用、已过期等）。
