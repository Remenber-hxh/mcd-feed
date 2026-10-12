"""收餐人档案：称呼 -> 麦当劳收货地址联系人、口味、忌口、常点。

数据保存在本机 ~/.mcd-feed/people.json（可用环境变量 MCD_FEED_HOME 改目录），
不进仓库，不保存手机号。只用 Python 标准库。
"""

import argparse
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

USUAL_LIMIT = 5


def data_file() -> Path:
    home = os.environ.get("MCD_FEED_HOME") or Path.home() / ".mcd-feed"
    return Path(home) / "people.json"


def load() -> dict:
    path = data_file()
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save(people: dict) -> None:
    path = data_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(people, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def split_list(text: str | None) -> list[str]:
    if not text:
        return []
    return [s.strip() for s in text.replace("，", ",").split(",") if s.strip()]


def cmd_list(people: dict, _args) -> dict:
    return {
        "people": [
            {"name": name, "place": p.get("place", ""), "usual": p.get("usual", [])[:1]}
            for name, p in people.items()
        ]
    }


def cmd_show(people: dict, args) -> dict:
    if args.name not in people:
        return {"found": False, "name": args.name}
    return {"found": True, "name": args.name, **people[args.name]}


def cmd_set(people: dict, args) -> dict:
    p = people.setdefault(args.name, {"likes": [], "avoid": [], "usual": [], "history": []})
    if args.contact is not None:
        p["contact"] = args.contact
    if args.place is not None:
        p["place"] = args.place
    if args.likes is not None:
        p["likes"] = split_list(args.likes)
    if args.avoid is not None:
        p["avoid"] = split_list(args.avoid)
    if args.health is not None:
        p["health"] = split_list(args.health)
    if args.birthday is not None:
        p["birthday"] = args.birthday
    if args.store is not None:
        p["store"] = args.store
    if args.note is not None:
        p["note"] = args.note
    save(people)
    return {"saved": True, "name": args.name, **p}


def cmd_log(people: dict, args) -> dict:
    if args.name not in people:
        return {"saved": False, "error": f"没有 {args.name} 的档案，先用 set 建档"}
    p = people[args.name]
    history = p.setdefault("history", [])
    history.append({"meal": args.meal, "at": datetime.now().strftime("%Y-%m-%d %H:%M")})
    del history[:-50]
    counts: dict[str, int] = {}
    for h in history:
        counts[h["meal"]] = counts.get(h["meal"], 0) + 1
    p["usual"] = sorted(counts, key=lambda m: -counts[m])[:USUAL_LIMIT]
    save(people)
    return {"saved": True, "name": args.name, "usual": p["usual"], "times": len(history)}


def cmd_birthdays(people: dict, args) -> dict:
    today = date.today()
    upcoming = []
    for name, p in people.items():
        try:
            month, day = (int(x) for x in p.get("birthday", "").split("-"))
            nxt = date(today.year, month, day)
            if nxt < today:
                nxt = nxt.replace(year=today.year + 1)
        except ValueError:
            continue
        days = (nxt - today).days
        if days <= args.days:
            upcoming.append({"name": name, "birthday": nxt.isoformat(), "in_days": days})
    return {"upcoming": sorted(upcoming, key=lambda x: x["in_days"])}


def cmd_remove(people: dict, args) -> dict:
    existed = people.pop(args.name, None) is not None
    if existed:
        save(people)
    return {"removed": existed, "name": args.name}


def main(argv: list[str] | None = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(prog="people.py", description="见麦如面 · 家人档案")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="列出所有收餐人")

    p_show = sub.add_parser("show", help="查看某人档案")
    p_show.add_argument("name")

    p_set = sub.add_parser("set", help="新建或修改档案")
    p_set.add_argument("name")
    p_set.add_argument("--contact", help="麦当劳收货地址里的联系人姓名")
    p_set.add_argument("--place", help="小区或楼宇名，用来区分同名联系人的多个地址")
    p_set.add_argument("--likes", help="爱吃的，逗号分隔")
    p_set.add_argument("--avoid", help="不吃的，逗号分隔")
    p_set.add_argument("--health", help="健康注意事项，逗号分隔，如 控糖,少盐,低热量")
    p_set.add_argument("--birthday", help="生日，MM-DD")
    p_set.add_argument("--store", help="到店取餐常去的门店或地点关键词")
    p_set.add_argument("--note", help="其他备注，比如作息")

    p_log = sub.add_parser("log", help="记录一次下单")
    p_log.add_argument("name")
    p_log.add_argument("meal")

    p_bd = sub.add_parser("birthdays", help="列出最近要过生日的家人")
    p_bd.add_argument("--days", type=int, default=30, help="往后看多少天，默认 30")

    p_rm = sub.add_parser("remove", help="删除某人档案")
    p_rm.add_argument("name")

    args = parser.parse_args(argv)
    handlers = {"list": cmd_list, "show": cmd_show, "set": cmd_set, "log": cmd_log,
                "birthdays": cmd_birthdays, "remove": cmd_remove}
    result = handlers[args.cmd](load(), args)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
