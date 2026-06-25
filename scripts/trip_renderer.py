#!/usr/bin/env python3
"""
tourAI 行程渲染器
读取 trip.json，支持：
  - 格式验证
  - Markdown 导出
  - HTML 骨架生成（供 Claude 进一步美化）
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime


def generate_trip_id() -> str:
    """生成行程 UUID"""
    return str(uuid.uuid4())[:8]


def validate_trip(trip_path: str) -> tuple[bool, list]:
    """基本结构验证（不依赖 jsonschema 库）"""
    errors = []

    try:
        with open(trip_path, "r", encoding="utf-8") as f:
            trip = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return False, [f"无法读取文件: {e}"]

    # 必需字段检查
    required = ["trip_id", "title", "destination", "duration_days", "itinerary", "metadata"]
    for field in required:
        if field not in trip:
            errors.append(f"缺少必需字段: {field}")

    # itinerary 检查
    if "itinerary" in trip:
        if not isinstance(trip["itinerary"], list) or len(trip["itinerary"]) == 0:
            errors.append("itinerary 必须是非空数组")
        else:
            for i, day in enumerate(trip["itinerary"]):
                if "day_number" not in day:
                    errors.append(f"Day {i+1}: 缺少 day_number")
                if "spots" not in day or not day["spots"]:
                    errors.append(f"Day {i+1}: 缺少 spots")
                if "meals" not in day:
                    errors.append(f"Day {i+1}: 缺少 meals")

    # spots 详细检查
    spot_count = 0
    for day in trip.get("itinerary", []):
        for spot in day.get("spots", []):
            spot_count += 1
            if "name" not in spot:
                errors.append(f"景点缺少 name")
            if "category" not in spot:
                errors.append(f"景点 '{spot.get('name', '?')}' 缺少 category")

    # metadata 检查
    if "metadata" in trip and "generated_at" not in trip["metadata"]:
        errors.append("metadata 缺少 generated_at")

    return len(errors) == 0, errors, trip


def render_markdown(trip: dict) -> str:
    """将 trip.json 渲染为 Markdown"""
    md = []

    # 标题
    md.append(f"# {trip.get('title', '旅行攻略')}")
    if trip.get("subtitle"):
        md.append(f"*{trip['subtitle']}*")
    md.append("")

    # 基本信息
    dest = trip.get("destination", {})
    md.append(f"**目的地**: {dest.get('city', '')}  |  ")
    md.append(f"**天数**: {trip.get('duration_days', '?')}天  |  ")
    md.append(f"**风格**: {', '.join(trip.get('style', []))}  |  ")
    md.append(f"**节奏**: {trip.get('pace', 'moderate')}")
    md.append("")

    # 交通
    if trip.get("transport_to_dest"):
        md.append("## 🚄 交通信息")
        md.append("")
        for t in trip["transport_to_dest"]:
            md.append(f"- **{t.get('mode', '')}** {t.get('from_city', '')} → {t.get('to_city', '')}")
            if t.get("duration_text"):
                md.append(f"  - 耗时: {t['duration_text']}")
            if t.get("price_min"):
                md.append(f"  - 票价: ¥{t['price_min']}-{t.get('price_max', '?')}")
        md.append("")

    # 每日行程
    md.append("## 📅 每日行程")
    md.append("")
    for day in trip.get("itinerary", []):
        day_num = day.get("day_number", "?")
        theme = day.get("theme", "")
        md.append(f"### Day {day_num} · {theme}")
        md.append("")

        # 路线
        if day.get("route_summary"):
            md.append(f"**路线**: {day['route_summary']}")
            md.append("")

        # 景点
        for i, spot in enumerate(day.get("spots", []), 1):
            emoji = spot.get("emoji", "📍")
            name = spot.get("name", "?")
            price = spot.get("ticket_price", 0)
            price_str = "免费" if price == 0 else f"¥{price}"
            md.append(f"#### {emoji} {name} *{price_str}*")
            md.append("")

            if spot.get("description"):
                md.append(spot["description"])
                md.append("")

            if spot.get("visit_duration_min"):
                md.append(f"- ⏱️ 建议游玩: {spot['visit_duration_min']}分钟")

            transit = spot.get("transit_from_previous")
            if transit:
                md.append(f"- {transit.get('emoji', '🚗')} 从 {transit['from_name']} 出发")
                md.append(f"  - {transit.get('distance_text', '?')} / {transit.get('duration_text', '?')}")

            if spot.get("romantic_moment"):
                md.append(f"- 💕 {spot['romantic_moment']}")

            if spot.get("pitfall_warning"):
                md.append(f"- ⚠️ {spot['pitfall_warning']}")

            md.append("")

        # 餐食
        meals = day.get("meals", {})
        if meals:
            md.append("**🍽️ 餐饮推荐**")
            md.append("")
            for meal_type, meal in meals.items():
                if meal:
                    type_label = {"breakfast": "早餐", "lunch": "午餐", "dinner": "晚餐"}.get(meal_type, meal_type)
                    md.append(f"- **{type_label}**: {meal.get('name', '')} ({meal.get('price_text', '')})")
                    if meal.get("recommended_dishes"):
                        md.append(f"  - 推荐: {', '.join(meal['recommended_dishes'][:3])}")
            md.append("")

        # 酒店
        hotel = day.get("hotel")
        if hotel:
            md.append(f"**🏨 住宿**: {hotel.get('name', hotel.get('area', ''))}")
            if hotel.get("price_range_text"):
                md.append(f"- 价格: {hotel['price_range_text']}")
            if hotel.get("recommendation_reason"):
                md.append(f"- 理由: {hotel['recommendation_reason']}")
            md.append("")

        md.append("---")
        md.append("")

    # 避坑
    if trip.get("avoid_list"):
        md.append("## ⚠️ 避坑清单")
        md.append("")
        for i, item in enumerate(trip["avoid_list"], 1):
            md.append(f"{i}. ❌ ~~{item['wrong']}~~")
            md.append(f"   ✅ {item['right']}")
            md.append("")

    # 预算
    budget = trip.get("budget")
    if budget:
        md.append("## 💰 预算估算")
        md.append("")
        md.append("| 类别 | 费用 |")
        md.append("|------|------|")
        md.append(f"| 🚗 交通 | ¥{budget.get('transport', 0)} |")
        md.append(f"| 🏨 住宿 | ¥{budget.get('hotel', 0)} |")
        md.append(f"| 🍜 餐饮 | ¥{budget.get('food', 0)} |")
        md.append(f"| 🎫 门票 | ¥{budget.get('tickets', 0)} |")
        if budget.get("shopping"):
            md.append(f"| 🛍️ 其他 | ¥{budget['shopping']} |")
        md.append(f"| **总计** | **¥{budget.get('total', 0)}** |")
        if budget.get("per_person"):
            md.append(f"| **人均** | **¥{budget['per_person']}** |")
        md.append("")

    # Tips
    if trip.get("tips"):
        md.append("## 💡 出行提示")
        md.append("")
        for tip in trip["tips"]:
            md.append(f"- {tip}")
        md.append("")

    # Footer
    meta = trip.get("metadata", {})
    md.append("---")
    md.append(f"*由 tourAI 生成 · {meta.get('generated_at', '')}*")
    md.append(f"*数据来源: {', '.join(meta.get('sources', []))}*")

    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(
        description="tourAI 行程渲染器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python trip_renderer.py --validate data/trips/abc123/trip.json
  python trip_renderer.py --trip data/trips/abc123/trip.json --format md --output guide.md
  python trip_renderer.py --trip trip.json --format skeleton --output skeleton.html
        """,
    )
    parser.add_argument("--trip", help="trip.json 文件路径")
    parser.add_argument("--validate", help="仅验证 trip.json 结构")
    parser.add_argument(
        "--format",
        choices=["md", "skeleton", "summary"],
        default="summary",
        help="输出格式 (默认: summary)",
    )
    parser.add_argument("--output", "-o", help="输出文件路径")

    args = parser.parse_args()

    trip_path = args.trip or args.validate
    if not trip_path:
        parser.print_help()
        print("\n错误: 需要 --trip 或 --validate 参数", file=sys.stderr)
        sys.exit(1)

    # 验证
    is_valid, errors, trip = validate_trip(trip_path)
    if not is_valid:
        print("❌ 验证失败:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ 验证通过: {trip.get('title', '')}, {trip.get('duration_days', '?')}天, {len(trip.get('itinerary', []))}天行程", file=sys.stderr)

    if args.validate:
        sys.exit(0)

    # 渲染
    if args.format == "md":
        output = render_markdown(trip)
    elif args.format == "summary":
        output = json.dumps({
            "trip_id": trip.get("trip_id"),
            "title": trip.get("title"),
            "destination": trip.get("destination"),
            "duration_days": trip.get("duration_days"),
            "days": len(trip.get("itinerary", [])),
            "total_spots": sum(len(d.get("spots", [])) for d in trip.get("itinerary", [])),
            "budget_total": trip.get("budget", {}).get("total"),
            "sources": trip.get("metadata", {}).get("sources", []),
            "amap_used": trip.get("metadata", {}).get("amap_used"),
        }, ensure_ascii=False, indent=2)
    else:
        output = json.dumps(trip, ensure_ascii=False, indent=2)

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"已保存到: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
