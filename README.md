# 见麦如面

[![在线演示](https://img.shields.io/badge/%E5%9C%A8%E7%BA%BF%E6%BC%94%E7%A4%BA-%E7%AB%8B%E5%8D%B3%E4%BD%93%E9%AA%8C-ff6f00?style=flat-square&labelColor=b74f00)](https://remenber-hxh.github.io/mcd-feed/) [![技能包](https://img.shields.io/badge/%E6%8A%80%E8%83%BD%E5%8C%85-%E4%B8%8B%E8%BD%BD_zip-2ea44f?style=flat-square&labelColor=217638&logo=github&logoColor=white)](https://github.com/Remenber-hxh/mcd-feed/releases/latest/download/mcd-feed.zip) [![WorkBuddy](https://img.shields.io/badge/WorkBuddy-%E5%AE%89%E8%A3%85%E6%95%99%E7%A8%8B-1677ff?style=flat-square&labelColor=0f55b7)](INSTALL.md) [![麦当劳 MCP](https://img.shields.io/badge/%E9%BA%A6%E5%BD%93%E5%8A%B3_MCP-35_%E4%B8%AA%E5%B7%A5%E5%85%B7-e53935?style=flat-square&labelColor=a42926)](MCP_INTEGRATION.md) [![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?style=flat-square&labelColor=27547b&logo=python&logoColor=white)](#安装) [![版本](https://img.shields.io/github/v/release/Remenber-hxh/mcd-feed?style=flat-square&color=00b4d8&labelColor=00819b&label=%E7%89%88%E6%9C%AC)](https://github.com/Remenber-hxh/mcd-feed/releases) [![许可证](https://img.shields.io/github/license/Remenber-hxh/mcd-feed?style=flat-square&color=8957e5&labelColor=623ea4&label=%E8%AE%B8%E5%8F%AF%E8%AF%81)](LICENSE)

人在远方，一餐替我回家。

见麦如面是一个 AI 技能，帮在外地的人给家里点麦当劳。你只管说"明早 8 点给我妈送份早餐"，剩下的交给它。

基于[麦当劳中国 MCP](https://github.com/M-China/mcd-mcp-server) 开发的 Agent Skill，可在 WorkBuddy、Claude Code 等支持 `SKILL.md` 的客户端中使用。

在线演示（示例数据，不需要安装）：[remenber-hxh.github.io/mcd-feed](https://remenber-hxh.github.io/mcd-feed/)

## 功能

| 功能 | 说明 |
|---|---|
| 送餐上门 | 早餐、夜宵、考前那顿饭都能预约送达，菜单按送达时段切换 |
| 到店或得来速取餐 | 家人顺路自己去拿，取餐码直接发给他 |
| 给单位、班级点团餐 | 按人数和人均预算搭配，自动算满减值不值得凑单 |
| 照顾健康 | 家人控糖、少盐、在减脂，用麦当劳的营养数据挑餐 |
| 用券算价 | 经你同意领券，逐个方案核价，选实付最低的 |
| 积分换礼物 | 查快过期的积分，换周边、礼品卡寄到家人那儿 |
| 生日会和活动 | 查活动日历，给家人预约麦当劳生日会、主题派对 |
| 记住家里每个人 | 地址、口味、忌口、健康注意、生日记一次，下次只说"给爸爸送夜宵" |
| 写好消息 | 下单后写一条消息，告诉家人几点送到、在哪取 |
| 跟进订单 | 问"送到了吗"、取消订单、看之前点过什么 |

下单、兑换、预约、抽奖前都会先给你确认，付款由你自己完成。麦当劳 MCP 的 35 个工具全部接入，明细见 [MCP_INTEGRATION.md](MCP_INTEGRATION.md)。

## 使用示例

```
你：明早 8 点给我妈送份早餐，跟她说天冷了多穿点

技能：下单确认
      收餐人：妈妈（清竹园，138****5678）
      送达：明天 08:00 左右
      餐品：猪柳蛋麦满分套餐（不要洋葱）
      价格：原价 ¥24.0，用券后 ¥15.0
      回复"好"就下单

你：好

技能：已下单，付款链接：……
      可以转给妈妈：
      妈，我给你点了麦当劳早餐，明早 8 点左右送到，记得开门。天冷了多穿点。
```

其他说法：

- 今晚 11 点给我爸送份夜宵，他今天加班
- 让我爸下班去得来速取一份，他 6 点半到
- 周五下午给我妹全班送下午茶，30 人，人均 25
- 我妈在控糖，以后给她点餐注意一下
- 用快过期的积分给我妈换个周边寄到家
- 下个月我妹生日，在她家附近的麦当劳办个生日会
- 最近麦当劳有什么活动
- 送到了吗

示例中的人名、地址、价格均为虚构。

## 适合谁

离家在外工作、上学或常出差，想照顾家里人的人。

## 安装

WorkBuddy 用户看 **[安装教程](INSTALL.md)**，大约 5 分钟：申请 Token → 添加麦当劳连接器 → 上传技能包 [mcd-feed.zip](https://github.com/Remenber-hxh/mcd-feed/releases/latest/download/mcd-feed.zip)。

其他支持 `SKILL.md` 的客户端：配好 [`mcp-config.example.json`](mcp-config.example.json) 里的连接器，把 `skill/mcd-feed/` 复制到客户端的技能目录（Claude Code 为 `~/.claude/skills/`）。

运行环境：Python 3.10 及以上，仅使用标准库。

## 隐私与安全

- 家人的手机号和详细地址只保存在你自己的麦当劳账户里。
- 本机档案 `~/.mcd-feed/people.json` 只记称呼、联系人姓名、小区名、口味、忌口、健康注意、生日和常去门店，不进仓库。
- 展示手机号时打码。
- 不代付，不主动取消订单，不主动抽奖；下单、兑换、预约前都要你确认。
- 仓库内不含真实 Token，配置文件只使用环境变量占位符。

## 目录结构

```
mcd-feed/
├── README.md
├── CONTEST_DECLARATION.md        参赛声明
├── INSTALL.md                    WorkBuddy 安装教程
├── MCP_INTEGRATION.md            MCP 集成说明
├── mcp-config.example.json       脱敏配置示例
├── skill/mcd-feed/
│   ├── SKILL.md                  技能入口：触发词、规则、按需求选流程
│   ├── references/               各流程的步骤
│   │   ├── delivery.md           送餐上门
│   │   ├── pickup.md             到店、得来速取餐
│   │   ├── group.md              团餐
│   │   ├── meals.md              挑餐、健康把关、用券核价
│   │   ├── points.md             积分、积分商城、抽奖
│   │   ├── events.md             活动日历、生日会
│   │   └── after-order.md        订单跟进
│   └── scripts/people.py         家人档案管理
└── docs/index.html               在线演示页
```

## 声明

麦当劳程序员创意开发大赛参赛作品，个人独立开发，非麦当劳官方产品。餐品、价格及供应状态以麦当劳官方渠道的实时结果为准。详见 [CONTEST_DECLARATION.md](CONTEST_DECLARATION.md)。

## 许可证

[MIT](LICENSE)
