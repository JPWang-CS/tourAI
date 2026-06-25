#!/usr/bin/env python3
"""
马蜂窝旅游数据采集脚本
通过 Ajax API 获取目的地景点、美食、行程模板等信息

API 说明：
- 马蜂窝开放平台（open.mafengwo.cn）的 API 仅限商家使用
- 本脚本使用移动端 Ajax API（mapi.mafengwo.cn），签名算法简单
- 仅用于个人旅行规划，请勿用于商业用途

签名算法：
  _sn = MD5(json_params + SECRET)[2:12]  (取10位)
  _ts = 当前毫秒时间戳
"""

import argparse
import hashlib
import json
import sys
import time
import os
from typing import Optional

try:
    import requests
except ImportError:
    print("错误: 需要安装 requests 库", file=sys.stderr)
    print("pip install requests", file=sys.stderr)
    sys.exit(1)

# 马蜂窝移动端 API 常量
BASE_URL = "https://mapi.mafengwo.cn"
SECRET = "c9d6618dbc657b41a66eb0af952906f1"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) "
                  "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Accept": "application/json",
    "Referer": "https://m.mafengwo.cn/",
}


def generate_sign(params: dict) -> str:
    """生成马蜂窝 API 签名"""
    params_str = json.dumps(params, separators=(",", ":"), ensure_ascii=False)
    md5_full = hashlib.md5((params_str + SECRET).encode()).hexdigest()
    return md5_full[2:12]


def make_request(endpoint: str, params: dict, timeout: int = 15) -> Optional[dict]:
    """发送带签名的 Ajax 请求"""
    params["_ts"] = int(time.time() * 1000)
    params["_sn"] = generate_sign(params)

    url = f"{BASE_URL}/{endpoint}"
    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") == 0 or data.get("ret") is True or "data" in data:
            return data
        else:
            print(f"API 返回错误: {data.get('msg', '未知错误')}", file=sys.stderr)
            return None
    except requests.RequestException as e:
        print(f"请求失败: {e}", file=sys.stderr)
        return None


def search_destination(city: str) -> Optional[dict]:
    """搜索目的地，获取目的地 ID"""
    print(f"正在搜索目的地: {city}...", file=sys.stderr)

    params = {
        "q": city,
        "limit": 5,
        "type": "destination",
    }
    result = make_request("rest/search/q", params)
    if result and "data" in result:
        items = result["data"].get("list", [])
        for item in items:
            if item.get("type") == "destination" and city in item.get("name", ""):
                return {
                    "id": item["id"],
                    "name": item["name"],
                    "name_en": item.get("name_en", ""),
                    "province": item.get("province", ""),
                }
        # 返回第一个匹配
        if items:
            item = items[0]
            return {
                "id": item.get("id"),
                "name": item.get("name", city),
                "name_en": item.get("name_en", ""),
            }
    return None


def get_destination_overview(dest_id: int) -> Optional[dict]:
    """获取目的地概览（简介、最佳季节、交通等）"""
    print(f"获取目的地概览 (ID: {dest_id})...", file=sys.stderr)

    params = {"mddid": dest_id}
    result = make_request("rest/destination/detail", params)
    if result and "data" in result:
        data = result["data"]
        return {
            "name": data.get("name", ""),
            "name_en": data.get("name_en", ""),
            "intro": data.get("intro", ""),
            "best_season": data.get("best_season", ""),
            "transport": data.get("traffic", ""),
            "tips": data.get("tips", ""),
        }
    return None


def get_attractions(dest_id: int, page: int = 1, limit: int = 30) -> list:
    """获取景点列表"""
    print(f"获取景点列表 (第{page}页)...", file=sys.stderr)

    params = {
        "mddid": dest_id,
        "page": page,
        "limit": limit,
        "sort": "hot",  # 按热度排序
    }
    result = make_request("rest/poi/list", params)
    if result and "data" in result:
        spots = []
        for item in result["data"].get("list", []):
            spots.append({
                "name": item.get("name", ""),
                "name_en": item.get("name_en", ""),
                "category": "attraction",
                "rating": item.get("comment_score"),
                "rating_count": item.get("comment_count"),
                "description": item.get("intro", ""),
                "ticket_price": item.get("ticket_price", 0),
                "opening_hours": item.get("open_time", ""),
                "emoji": _pick_emoji(item.get("name", ""), item.get("tags", [])),
                "address": item.get("address", ""),
                "tags": item.get("tags", []),
            })
        return spots
    return []


def get_food(dest_id: int, page: int = 1, limit: int = 30) -> list:
    """获取美食推荐"""
    print(f"获取美食推荐 (第{page}页)...", file=sys.stderr)

    params = {
        "mddid": dest_id,
        "page": page,
        "limit": limit,
        "type": "food",
    }
    result = make_request("rest/poi/list", params)
    if result and "data" in result:
        foods = []
        for item in result["data"].get("list", []):
            foods.append({
                "name": item.get("name", ""),
                "cuisine": _guess_cuisine(item.get("tags", [])),
                "price_per_person": item.get("avg_price"),
                "recommended_dishes": item.get("recommend_dishes", []),
                "reason": item.get("intro", "")[:200],
                "address": item.get("address", ""),
                "rating": item.get("comment_score"),
                "tags": item.get("tags", []),
            })
        return foods
    return []


def get_classic_routes(dest_id: int) -> list:
    """获取经典行程模板"""
    print("获取经典行程模板...", file=sys.stderr)

    params = {"mddid": dest_id}
    result = make_request("rest/route/list", params)
    if result and "data" in result:
        routes = []
        for item in result["data"].get("list", []):
            days_info = item.get("days", [])
            routes.append({
                "title": item.get("title", ""),
                "duration_days": item.get("days_count", len(days_info)),
                "summary": item.get("summary", ""),
                "day_plans": [
                    {
                        "day": d.get("day", i + 1),
                        "theme": d.get("title", ""),
                        "spots": d.get("poi_names", []),
                    }
                    for i, d in enumerate(days_info)
                ],
            })
        return routes
    return []


def get_travel_guides(dest_id: int, page: int = 1, limit: int = 10) -> list:
    """获取游记攻略摘要"""
    print(f"获取游记攻略 (第{page}页)...", file=sys.stderr)

    params = {
        "mddid": dest_id,
        "page": page,
        "limit": limit,
        "sort": "hot",
    }
    result = make_request("rest/travel/notes/list", params)
    if result and "data" in result:
        guides = []
        for item in result["data"].get("list", []):
            guides.append({
                "title": item.get("title", ""),
                "author": item.get("user", {}).get("name", ""),
                "summary": item.get("summary", ""),
                "duration": item.get("duration", ""),
                "url": item.get("share_url", ""),
                "view_count": item.get("view_count", 0),
            })
        return guides
    return []


def _pick_emoji(name: str, tags: list) -> str:
    """根据名称和标签选择合适的 emoji"""
    name_lower = name.lower() if name else ""
    all_text = name_lower + " " + " ".join(tags)

    emoji_map = [
        (["海", "滨", "沙滩", "岛", "湾", "浪", "渔"], "🌊"),
        (["山", "峰", "岭", "岳", "崖", "谷"], "⛰️"),
        (["公园", "花园", "植物", "湿地"], "🌿"),
        (["寺", "庙", "佛", "塔", "祠", "宗教"], "🏛️"),
        (["博物馆", "纪念", "文化", "历史"], "🏛️"),
        (["街", "巷", "胡同", "步行", "夜市"], "🚶"),
        (["湖", "泉", "瀑", "溪"], "💧"),
        (["桥", "大桥"], "🌉"),
        (["广场", "中心"], "🏙️"),
    ]

    for keywords, emoji in emoji_map:
        if any(kw in all_text for kw in keywords):
            return emoji
    return "📍"


def _guess_cuisine(tags: list) -> str:
    """根据标签猜测菜系"""
    tag_str = " ".join(tags).lower()
    cuisine_map = [
        (["海鲜", "海产"], "海鲜"),
        (["火锅", "涮"], "火锅"),
        (["烧烤", "烤肉"], "烧烤"),
        (["面", "粉", "米线"], "面食"),
        (["小吃", "点心"], "小吃"),
        (["粤菜", "广东"], "粤菜"),
        (["川菜", "辣"], "川菜"),
        (["日料", "寿司", "刺身"], "日料"),
        (["韩式", "韩国", "烤肉"], "韩料"),
        (["甜品", "糖水", "冰"], "甜品"),
        (["茶馆", "茶"], "茶馆"),
    ]

    for keywords, cuisine in cuisine_map:
        if any(kw in tag_str for kw in keywords):
            return cuisine
    return "本地特色"


def main():
    parser = argparse.ArgumentParser(
        description="马蜂窝旅游数据采集 - 获取目的地攻略信息",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python mafengwo.py --destination 威海 --type overview
  python mafengwo.py --destination 厦门 --type spots
  python mafengwo.py --destination 大理 --type all --output result.json
        """,
    )
    parser.add_argument("--destination", required=True, help="目的地城市名称")
    parser.add_argument(
        "--type",
        default="all",
        choices=["overview", "spots", "food", "routes", "guides", "all"],
        help="数据类型 (默认: all)",
    )
    parser.add_argument("--output", "-o", help="输出 JSON 文件路径（默认输出到 stdout）")
    parser.add_argument("--page", type=int, default=1, help="页码 (默认: 1)")
    parser.add_argument("--limit", type=int, default=30, help="每页数量 (默认: 30)")

    args = parser.parse_args()

    # 1. 搜索目的地
    dest = search_destination(args.destination)
    if not dest:
        print(f"错误: 未找到目的地 '{args.destination}'", file=sys.stderr)
        sys.exit(1)

    print(f"找到目的地: {dest['name']} (ID: {dest['id']})", file=sys.stderr)

    result = {
        "destination": dest,
        "data": {},
        "meta": {
            "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "source": "mafengwo",
            "dest_id": dest["id"],
        },
    }

    # 2. 获取数据
    fetch_all = args.type == "all"

    if fetch_all or args.type == "overview":
        overview = get_destination_overview(dest["id"])
        if overview:
            result["data"]["overview"] = overview

    if fetch_all or args.type == "spots":
        spots = get_attractions(dest["id"], args.page, args.limit)
        result["data"]["spots"] = spots
        result["meta"]["spots_count"] = len(spots)

    if fetch_all or args.type == "food":
        foods = get_food(dest["id"], args.page, args.limit)
        result["data"]["food"] = foods
        result["meta"]["food_count"] = len(foods)

    if fetch_all or args.type == "routes":
        routes = get_classic_routes(dest["id"])
        result["data"]["routes"] = routes
        result["meta"]["routes_count"] = len(routes)

    if fetch_all or args.type == "guides":
        guides = get_travel_guides(dest["id"], args.page, min(args.limit, 10))
        result["data"]["guides"] = guides
        result["meta"]["guides_count"] = len(guides)

    # 3. 输出
    output_json = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_json)
        print(f"已保存到: {args.output}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
