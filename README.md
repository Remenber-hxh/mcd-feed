# 见麦如面

人在远方，一餐替我回家。

见麦如面是一个 AI 技能，帮在外地的人给家里点麦当劳。你只管说"明早 8 点给我妈送份早餐"，剩下的交给它。

基于[麦当劳中国 MCP](https://github.com/M-China/mcd-mcp-server) 开发的 Agent Skill，可在 WorkBuddy、Claude Code 等支持 `SKILL.md` 的客户端中使用。

在线演示（示例数据，不需要安装）：[remenber-hxh.github.io/mcd-feed](https://remenber-hxh.github.io/mcd-feed/)

## 功能

| 功能 | 说明 |
|---|---|
| 记住家里每个人 | 地址、口味、忌口记一次，下次只说"给爸爸送夜宵" |
| 预约送达 | 早餐、夜宵、考前那顿饭都可以提前约好，菜单按送达时段切换 |
| 用券算价 | 经你同意领券，查门店可用券，逐个方案核价，选实付最低的 |
| 下单前确认 | 收餐人、送达时间、餐品、价格先给你看，你说"好"才下单，付款由你完成 |
| 写好消息 | 下单后写一条消息，告诉家人几点送到，带上你想说的话 |
| 查配送 | 问"送到了吗"，返回制作、配送或已送达 |

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
- 周六中午给我妹送顿饭，她下午月考
- 送到了吗

示例中的人名、地址、价格均为虚构。

## 适合谁

离家在外工作、上学或常出差，想照顾家里人的人。

## 安装

1. 申请 MCP Token：在 [open.mcd.cn/mcp](https://open.mcd.cn/mcp) 用手机号登录，进入控制台，点击"激活"。
2. 配置连接器（以 WorkBuddy 为例）：左侧边栏【专家·技能·连接器】→【连接器】→【自定义连接器】→【配置 MCP】，粘贴 [`mcp-config.example.json`](mcp-config.example.json) 的内容，把 `${MCD_MCP_TOKEN}` 换成你的 Token，保存后启用 `mcd-mcp`。
3. 安装技能：把 `skill/mcd-feed/` 整个目录复制到客户端的技能目录。
   - WorkBuddy：`~/.workbuddy/skills/`（Windows 为 `%USERPROFILE%\.workbuddy\skills\`）
   - Claude Code：`~/.claude/skills/`
4. 在对话框里说"给我妈送份早餐"。

运行环境：Python 3.10 及以上，仅使用标准库。

## 隐私与安全

- 家人的手机号和详细地址只保存在你自己的麦当劳账户里。
- 本机档案 `~/.mcd-feed/people.json` 只记称呼、联系人姓名、小区名、口味和忌口，不进仓库。
- 展示手机号时打码。
- 不代付，不主动取消订单，每次下单前都要你确认。
- 仓库内不含真实 Token，配置文件只使用环境变量占位符。

## 目录结构

```
mcd-feed/
├── README.md
├── CONTEST_DECLARATION.md        参赛声明
├── MCP_INTEGRATION.md            MCP 集成说明
├── mcp-config.example.json       脱敏配置示例
├── skill/mcd-feed/
│   ├── SKILL.md                  技能定义：触发词、流程、规则
│   └── scripts/people.py         家人档案管理
└── docs/index.html               在线演示页
```

## 声明

麦当劳程序员创意开发大赛参赛作品，个人独立开发，非麦当劳官方产品。餐品、价格及供应状态以麦当劳官方渠道的实时结果为准。详见 [CONTEST_DECLARATION.md](CONTEST_DECLARATION.md)。

## 许可证

[MIT](LICENSE)
