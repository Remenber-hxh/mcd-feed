# 活动日历、生日会和主题活动

## 1. 活动日历

用户问"最近麦当劳有什么活动"，或要给家人挑个日子时，调用 `campaign-calendar`：

- 不传参数：返回当月全部活动。
- 传 `specifiedDate`（`yyyy-MM-dd`）：返回那天，以及前后各一个有活动的日子。

展示进行中和即将开始的活动。和家人有关的就点一句，比如"周六有新品上市，可以那天给妹妹送一份"。

## 2. 预约生日会和主题活动

适用于：生日派对、主题派对、麦麦体验营、品鉴会、读书会、积分兑换活动。可以先运行 `python scripts/people.py birthdays` 看哪位家人快过生日。

**每一步都等用户选好，再进行下一步，不跳步。**

### 2.1 选活动

调用 `mall-points-products`，按类别筛选：

| catRuleIds | 类别 |
|---|---|
| `1>6>20` | 生日派对 |
| `1>6>21` | 主题派对 |
| `1>6>22` | 麦麦体验营 |
| `1>6>25` | 品鉴会 |
| `1>6>34` | 读书会 |
| `1>6>40` | 积分兑换活动 |

用户选中后，调用 `mall-product-detail`（`spuId`），拿到 `skuId` 和 `partyType`。商品的 `shopId` 必须是 5，否则改走 `references/points.md` 的兑换流程。

### 2.2 包场还是拼团

- 商品 `partyType=1`：只能包场。
- 商品 `partyType=2`：只能拼团。
- 商品 `partyType=-1`：问用户选包场（1）还是拼团（2）。

### 2.3 选城市、门店、日期、场次

1. 调用 `query-party-city`（`spuId`），选家人所在的城市，记下城市 `code`、`latitude`、`longitude`。
2. 调用 `query-party-store`（`code`、`latitude`、`longitude`、`spuId`），列出门店。优先推荐离家人近的，可参考档案里的 `place` 和 `store`。
3. 调用 `query-party-store-date`（`spuId`、`storeCode`），列出可预约日期。是生日会的话，优先推荐离生日最近的日子。
4. 调用 `query-party-store-session`（`spuId`、`storeCode`、`dateStr`），列出当天场次：开始和结束时间、剩余名额、成团人数上下限、价格。

### 2.4 确认和预约

```
活动预约确认
活动：生日派对（包场）
门店：清竹园店
时间：10 月 18 日 14:00–16:00
人数：8 人（本场成团 6–12 人，剩余名额 12）
费用：¥XXX
回复"好"就预约
```

用户确认后调用 `party-order-create`：`spuId`、`skuId`、`partyType`、`code`、`storeCode`、`dateStr`、`id`（场次 ID）、`timeStart`、`timeEnd`、`leftNum`、`count`，以及 `partyTimeInfo`（场次的 `id`、`leftNum`、`partyMin`、`partyMax`、`price`、`timeStart`、`timeEnd`）。有支付链接时交给用户自己支付。

### 2.5 通知家人

写一条消息说清时间、门店、要做什么准备，例如：

> 妹，10 月 18 号下午 2 点在清竹园店给你办了个生日会，叫上你的朋友，一共能来 8 个人。
