#!/usr/bin/env python3
"""
旅游攻略搜索关键词生成器
根据目的地和查询类型生成精准搜索词，用于 WebSearch / XHS / 马蜂窝等平台

v2.0 - 增强结构化输出，支持直接对接 gather-agent
"""

import argparse
import json
import sys
import time

# 搜索类别定义
SEARCH_CATEGORIES = {
    "general": {
        "label": "综合攻略",
        "icon": "📋",
        "queries": [
            "{city}旅游攻略",
            "{city}自由行攻略",
            "{city}必去景点推荐",
            "{city}行程安排规划",
        ],
    },
    "food": {
        "label": "美食推荐",
        "icon": "🍜",
        "queries": [
            "{city}美食推荐",
            "{city}必吃美食排行",
            "{city}本地人推荐餐厅",
            "{city}网红餐厅打卡",
            "{city}地道小吃攻略",
        ],
    },
    "avoid": {
        "label": "避坑指南",
        "icon": "⚠️",
        "queries": [
            "{city}避坑指南",
            "{city}旅游注意事项",
            "{city}旅游陷阱踩雷",
            "{city}不建议去的地方",
        ],
    },
    "hotel": {
        "label": "住宿推荐",
        "icon": "🏨",
        "queries": [
            "{city}住宿推荐",
            "{city}酒店攻略",
            "{city}住哪里方便",
            "{city}民宿推荐排行榜",
        ],
    },
    "transport": {
        "label": "交通攻略",
        "icon": "🚗",
        "queries": [
            "{city}怎么去最方便",
            "{city}交通攻略",
            "{city}市内交通指南",
            "{city}机场到市区交通",
        ],
    },
    "romantic": {
        "label": "情侣浪漫",
        "icon": "💕",
        "queries": [
            "{city}情侣打卡地",
            "{city}浪漫景点推荐",
            "{city}约会好去处",
            "{city}拍照最好看的地方",
            "{city}蜜月旅行攻略",
        ],
    },
    "photo": {
        "label": "拍照出片",
        "icon": "📸",
        "queries": [
            "{city}拍照圣地",
            "{city}网红打卡点",
            "{city}出片攻略",
            "{city}最佳机位",
        ],
    },
    "season": {
        "label": "季节信息",
        "icon": "🌤️",
        "queries": [
            "{city}最佳旅游季节",
            "{city}几月份去最好",
            "{city}旅游天气穿衣",
        ],
    },
}

# 平台搜索偏好
PLATFORM_PREFERENCES = {
    "xiaohongshu": {
        "prefix": "小红书",
        "best_for": ["food", "photo", "romantic", "avoid"],
        "query_style": "自然语言风格",
    },
    "mafengwo": {
        "prefix": "马蜂窝",
        "best_for": ["general", "transport", "hotel", "season"],
        "query_style": "攻略导向风格",
    },
    "websearch": {
        "best_for": ["general", "transport", "avoid"],
        "query_style": "通用搜索引擎风格",
    },
}


def generate_queries(city: str, category: str = None) -> dict:
    """生成搜索关键词"""
    if category and category in SEARCH_CATEGORIES:
        cats = {category: SEARCH_CATEGORIES[category]}
    else:
        cats = SEARCH_CATEGORIES

    result = {}
    for cat_key, cat_info in cats.items():
        queries = [q.format(city=city) for q in cat_info["queries"]]
        result[cat_key] = {
            "label": cat_info["label"],
            "icon": cat_info["icon"],
            "queries": queries,
            "best_platforms": [
                p
                for p, pinfo in PLATFORM_PREFERENCES.items()
                if cat_key in pinfo["best_for"]
            ],
        }
    return result


def main():
    parser = argparse.ArgumentParser(
        description="旅游攻略搜索关键词生成器 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python search_guide.py --destination 威海 --all
  python search_guide.py --destination 大理 --type food
  python search_guide.py --destination 厦门 --all --output search.json
        """,
    )
    parser.add_argument("--destination", required=True, help="目的地名称")
    parser.add_argument(
        "--type",
        default="all",
        choices=list(SEARCH_CATEGORIES.keys()) + ["all"],
        help="查询类型 (默认: all)",
    )
    parser.add_argument("--output", "-o", help="输出 JSON 文件路径")
    parser.add_argument(
        "--platform",
        choices=["xiaohongshu", "mafengwo", "websearch"],
        help="按平台优化搜索词",
    )

    args = parser.parse_args()

    # 生成搜索词
    category = None if args.type == "all" else args.type
    queries = generate_queries(args.destination, category)

    result = {
        "destination": args.destination,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "search_categories": queries,
        "platform": args.platform,
        "total_queries": sum(len(v["queries"]) for v in queries.values()),
        "usage": {
            "websearch": "使用 WebSearch 工具搜索这些关键词",
            "xiaohongshu": "使用 XHS MCP search_notes(keyword=...) 搜索",
            "mafengwo": "使用 scripts/mafengwo.py --destination ... 获取结构化数据",
            "priority": [
                "1. 先使用 Amap MCP 获取 POI + 坐标数据",
                "2. 再使用 scripts/mafengwo.py 获取结构化攻略",
                "3. 使用 XHS MCP 获取真实用户评价",
                "4. 使用 WebSearch 填补空缺",
            ],
        },
    }

    output_json = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_json)
        print(f"已保存到: {args.output}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
