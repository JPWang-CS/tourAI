#!/usr/bin/env python3
"""
Fill all route fields in trip.json with estimated real-world data.
No Amap MCP available — all routes use computed_by="estimated".
"""

import json
import sys

TRIP_PATH = "D:/desktop/旅游/data/trips/57cec94c-04a6-4408-9e82-78905dfc4be5/trip.json"

def make_route(from_name, to_name, transport_mode, distance_meters, duration_seconds,
               distance_text, duration_text, emoji, waypoints=None):
    route = {
        "from_name": from_name,
        "to_name": to_name,
        "transport_mode": transport_mode,
        "distance_meters": distance_meters,
        "duration_seconds": duration_seconds,
        "distance_text": distance_text,
        "duration_text": duration_text,
        "computed_by": "estimated",
        "emoji": emoji
    }
    if waypoints:
        route["waypoints"] = waypoints
    return route


def fill_routes(trip):
    """Fill routes for all spots in all days."""

    # =========================================================================
    # Day 1 — 抵达蓉城·苍蝇馆子初体验
    # =========================================================================
    day1_routes = [
        make_route(
            from_name="嘉立精选酒店(成都春熙路太古里店)",
            to_name="春熙路步行街",
            transport_mode="walking",
            distance_meters=500,
            duration_seconds=420,
            distance_text="500米",
            duration_text="7分钟",
            emoji="🚶"
        ),
    ]

    # =========================================================================
    # Day 2 — 熊猫萌宠·老成都慢生活
    # =========================================================================
    day2_routes = [
        make_route(
            from_name="嘉立精选酒店(成都春熙路太古里店)",
            to_name="成都大熊猫繁育研究基地",
            transport_mode="taxi",
            distance_meters=18000,
            duration_seconds=2400,
            distance_text="18公里",
            duration_text="40分钟",
            emoji="🚗"
        ),
        make_route(
            from_name="成都大熊猫繁育研究基地",
            to_name="人民公园鹤鸣茶社",
            transport_mode="taxi",
            distance_meters=16000,
            duration_seconds=2100,
            distance_text="16公里",
            duration_text="35分钟",
            emoji="🚗"
        ),
        make_route(
            from_name="人民公园鹤鸣茶社",
            to_name="太古里",
            transport_mode="walking",
            distance_meters=1200,
            duration_seconds=900,
            distance_text="1.2公里",
            duration_text="15分钟",
            emoji="🚶"
        ),
    ]

    # =========================================================================
    # Day 3 — 千年水利·都江堰奇迹一日游
    # =========================================================================
    day3_routes = [
        make_route(
            from_name="嘉立精选酒店(成都春熙路太古里店)",
            to_name="都江堰景区(秦堰楼入口)",
            transport_mode="transit",
            distance_meters=65000,
            duration_seconds=5400,
            distance_text="65公里",
            duration_text="1小时30分钟",
            emoji="🚇🚄",
            waypoints=[
                {
                    "name": "犀浦站",
                    "type": "rest_stop",
                    "at_distance_km": 15,
                    "facilities": "地铁2号线换乘城际列车",
                    "tips": "春熙路站乘地铁2号线至犀浦站约30分钟，同站换乘城际列车"
                },
                {
                    "name": "离堆公园站",
                    "type": "rest_stop",
                    "at_distance_km": 64,
                    "facilities": "出站后步行约800米至都江堰景区",
                    "tips": "犀浦→离堆公园城际列车约18分钟，票价¥10，建议提前在12306购票"
                }
            ]
        ),
        make_route(
            from_name="都江堰景区(离堆公园出口)",
            to_name="灌县古城",
            transport_mode="walking",
            distance_meters=500,
            duration_seconds=420,
            distance_text="500米",
            duration_text="7分钟",
            emoji="🚶"
        ),
    ]

    # =========================================================================
    # Day 4 — 穿越川西·高铁奔赴九寨沟
    # =========================================================================
    day4_routes = [
        make_route(
            from_name="嘉立精选酒店(成都春熙路太古里店)",
            to_name="漳扎镇(九寨沟沟口)",
            transport_mode="transit",
            distance_meters=450000,
            duration_seconds=16200,
            distance_text="450公里",
            duration_text="4小时30分钟",
            emoji="🚇🚄🚌",
            waypoints=[
                {
                    "name": "成都东站",
                    "type": "rest_stop",
                    "at_distance_km": 10,
                    "facilities": "地铁2号线可达，高铁站",
                    "tips": "春熙路站乘地铁至成都东站约25分钟"
                },
                {
                    "name": "黄龙九寨站",
                    "type": "rest_stop",
                    "at_distance_km": 360,
                    "facilities": "川青铁路高铁站，出站有景区直通大巴",
                    "tips": "成都东→黄龙九寨高铁约2小时，票价¥135-149。旺季建议提前15天在12306购票"
                }
            ]
        ),
    ]

    # =========================================================================
    # Day 5 — 人间仙境·九寨沟全天深度游
    # =========================================================================
    day5_routes = [
        make_route(
            from_name="阿布藏家客栈(九寨沟漳扎镇)",
            to_name="五花海",
            transport_mode="transit",
            distance_meters=15000,
            duration_seconds=1800,
            distance_text="15公里",
            duration_text="30分钟",
            emoji="🚌",
            waypoints=[
                {
                    "name": "九寨沟景区入口",
                    "type": "rest_stop",
                    "at_distance_km": 0.5,
                    "facilities": "检票入园，乘坐景区观光车",
                    "tips": "7:30第一班入园，旺季需提前预约门票¥280/人。观光车包含在门票内，上车后告诉调度员去日则沟方向"
                }
            ]
        ),
        make_route(
            from_name="五花海",
            to_name="珍珠滩瀑布",
            transport_mode="walking",
            distance_meters=1500,
            duration_seconds=1500,
            distance_text="1.5公里",
            duration_text="25分钟",
            emoji="🚶"
        ),
        make_route(
            from_name="珍珠滩瀑布",
            to_name="诺日朗瀑布",
            transport_mode="transit",
            distance_meters=5000,
            duration_seconds=900,
            distance_text="5公里",
            duration_text="15分钟",
            emoji="🚌"
        ),
        make_route(
            from_name="诺日朗瀑布",
            to_name="长海",
            transport_mode="transit",
            distance_meters=18000,
            duration_seconds=1800,
            distance_text="18公里",
            duration_text="30分钟",
            emoji="🚌",
            waypoints=[
                {
                    "name": "诺日朗中心站",
                    "type": "rest_stop",
                    "at_distance_km": 0.5,
                    "facilities": "餐厅、卫生间、休息区",
                    "tips": "在此换乘则查洼沟方向观光车前往长海"
                }
            ]
        ),
        make_route(
            from_name="长海",
            to_name="五彩池",
            transport_mode="walking",
            distance_meters=1000,
            duration_seconds=900,
            distance_text="1公里",
            duration_text="15分钟",
            emoji="🚶"
        ),
        make_route(
            from_name="五彩池",
            to_name="树正群海",
            transport_mode="transit",
            distance_meters=25000,
            duration_seconds=2400,
            distance_text="25公里",
            duration_text="40分钟",
            emoji="🚌",
            waypoints=[
                {
                    "name": "诺日朗中心站",
                    "type": "rest_stop",
                    "at_distance_km": 18,
                    "facilities": "换乘树正沟方向观光车",
                    "tips": "从五彩池乘车返回诺日朗中心，换乘树正沟方向出沟。建议在树正寨下车后步行游览至盆景滩，再乘车出沟"
                }
            ]
        ),
    ]

    # =========================================================================
    # Day 6 — 草原天路·花湖湿地与黄河落日
    # =========================================================================
    day6_routes = [
        make_route(
            from_name="川主寺镇",
            to_name="花湖",
            transport_mode="driving",
            distance_meters=242000,
            duration_seconds=16200,
            distance_text="242公里",
            duration_text="4小时30分钟",
            emoji="🚗",
            waypoints=[
                {
                    "name": "尕力台垭口",
                    "type": "viewpoint",
                    "at_distance_km": 45,
                    "facilities": "观景台",
                    "tips": "九若路(九寨沟—若尔盖公路)最高点，海拔约3800米，可远眺岷山雪峰。弯道密集，谨慎驾驶"
                },
                {
                    "name": "若尔盖县城",
                    "type": "rest_stop",
                    "at_distance_km": 192,
                    "facilities": "加油站、餐馆、卫生间",
                    "tips": "在此加油并用午餐。之后加油站间距大，务必加满油再出发"
                }
            ],
        ),
        make_route(
            from_name="花湖",
            to_name="黄河九曲第一湾",
            transport_mode="driving",
            distance_meters=90000,
            duration_seconds=5400,
            distance_text="90公里",
            duration_text="1小时30分钟",
            emoji="🚗"
        ),
    ]

    # =========================================================================
    # Day 7 — 信仰之路·从郎木寺到拉卜楞寺
    # =========================================================================
    day7_routes = [
        make_route(
            from_name="吉祥自在·落霞庭民宿(唐克镇)",
            to_name="赛赤寺(达仓郎木赛赤寺/甘肃寺)",
            transport_mode="driving",
            distance_meters=87000,
            duration_seconds=5400,
            distance_text="87公里",
            duration_text="1小时30分钟",
            emoji="🚗",
            waypoints=[
                {
                    "name": "U13县道-兰磨线岔口",
                    "type": "rest_stop",
                    "at_distance_km": 40,
                    "facilities": "部分路段无信号",
                    "tips": "唐克至郎木寺段弯道较多，部分路段无手机信号，出发前下载离线地图"
                }
            ]
        ),
        make_route(
            from_name="赛赤寺(达仓郎木赛赤寺/甘肃寺)",
            to_name="格尔底寺(达仓郎木格尔底寺/四川寺)+纳摩大峡谷",
            transport_mode="walking",
            distance_meters=1000,
            duration_seconds=900,
            distance_text="1公里",
            duration_text="15分钟",
            emoji="🚶"
        ),
        make_route(
            from_name="格尔底寺(达仓郎木格尔底寺/四川寺)",
            to_name="拉卜楞寺",
            transport_mode="driving",
            distance_meters=184000,
            duration_seconds=10800,
            distance_text="184公里",
            duration_text="3小时",
            emoji="🚗",
            waypoints=[
                {
                    "name": "尕海湖",
                    "type": "viewpoint",
                    "at_distance_km": 50,
                    "facilities": "路边观景",
                    "tips": "途径尕海湿地保护区，路边可远眺尕海湖。阿木去乎—尕海之间约22公里信号盲区，务必提前下载离线地图"
                },
                {
                    "name": "桑科草原",
                    "type": "viewpoint",
                    "at_distance_km": 140,
                    "facilities": "路边观景",
                    "tips": "沿途穿越桑科草原，9月草原金黄，可停车拍照（注意安全）"
                },
                {
                    "name": "合作市",
                    "type": "rest_stop",
                    "at_distance_km": 100,
                    "facilities": "加油站、餐馆、卫生间",
                    "tips": "甘南州首府，可在此加油休整"
                }
            ]
        ),
        make_route(
            from_name="拉卜楞寺",
            to_name="转经廊(转经筒长廊)",
            transport_mode="walking",
            distance_meters=300,
            duration_seconds=300,
            distance_text="300米",
            duration_text="5分钟",
            emoji="🚶"
        ),
    ]

    # =========================================================================
    # Day 8 — 归途美食·西宁味蕾告别之旅
    # =========================================================================
    day8_routes = [
        make_route(
            from_name="山禾悦Meeting·度假民宿(夏河)",
            to_name="益鑫手抓羊肉(花园北街店)",
            transport_mode="driving",
            distance_meters=260000,
            duration_seconds=16200,
            distance_text="260公里",
            duration_text="4小时30分钟",
            emoji="🚗",
            waypoints=[
                {
                    "name": "同仁市(隆务峡)",
                    "type": "viewpoint",
                    "at_distance_km": 70,
                    "facilities": "路边观景",
                    "tips": "途径隆务峡，黄河在此呈现碧绿色，峡谷景观壮丽。同仁是热贡艺术之乡"
                },
                {
                    "name": "坎布拉国家地质公园(远眺)",
                    "type": "viewpoint",
                    "at_distance_km": 120,
                    "facilities": "路边观景",
                    "tips": "沿途可远眺坎布拉丹霞地貌，红色山体与碧绿黄河交相辉映"
                },
                {
                    "name": "尖扎县",
                    "type": "rest_stop",
                    "at_distance_km": 100,
                    "facilities": "加油站、餐馆",
                    "tips": "夏河→西宁段有高速公路（G0611张汶高速），全程约¥60-100过路费"
                },
                {
                    "name": "西宁曹家堡机场(一嗨还车点)",
                    "type": "rest_stop",
                    "at_distance_km": 255,
                    "facilities": "一嗨租车还车点、加油站",
                    "tips": "抵达西宁后先到机场附近还车，再打车进城用餐。一嗨全国免异地还车费"
                }
            ]
        ),
        make_route(
            from_name="益鑫手抓羊肉(花园北街店)",
            to_name="德禄酸奶(莫家街店)",
            transport_mode="walking",
            distance_meters=1000,
            duration_seconds=900,
            distance_text="1公里",
            duration_text="15分钟",
            emoji="🚶"
        ),
        make_route(
            from_name="德禄酸奶(莫家街店)",
            to_name="莫家街",
            transport_mode="walking",
            distance_meters=200,
            duration_seconds=180,
            distance_text="200米",
            duration_text="3分钟",
            emoji="🚶"
        ),
    ]

    # =========================================================================
    # Apply routes to each day
    # =========================================================================
    all_routes = {
        1: day1_routes,
        2: day2_routes,
        3: day3_routes,
        4: day4_routes,
        5: day5_routes,
        6: day6_routes,
        7: day7_routes,
        8: day8_routes,
    }

    for day in trip["itinerary"]:
        day_num = day["day_number"]
        routes = all_routes.get(day_num, [])
        spots = day.get("spots", [])

        if len(routes) != len(spots):
            print(f"WARNING: Day {day_num} has {len(spots)} spots but {len(routes)} routes defined!")

        for i, spot in enumerate(spots):
            if i < len(routes):
                spot["route"] = routes[i]
            else:
                print(f"WARNING: Day {day_num} spot {i} ({spot.get('name')}) has no route!")

    # Update metadata
    trip["metadata"]["amap_used"] = False
    trip["metadata"]["enriched_at"] = "2026-06-28T13:00:00+08:00"

    # Update notes
    existing_notes = trip["metadata"].get("notes", [])
    # Remove old notes about routes being null
    existing_notes = [n for n in existing_notes if "route字段全部设为null" not in n]
    existing_notes.append("所有route字段已通过estimated模式填充（无高德MCP可用时使用已知距离估算）。自驾段使用项目提供的真实里程数据，市内段使用合理估算值。")
    trip["metadata"]["notes"] = existing_notes

    return trip


def main():
    print(f"Reading trip.json from: {TRIP_PATH}")
    with open(TRIP_PATH, "r", encoding="utf-8") as f:
        trip = json.load(f)

    trip = fill_routes(trip)

    print(f"Writing updated trip.json to: {TRIP_PATH}")
    with open(TRIP_PATH, "w", encoding="utf-8") as f:
        json.dump(trip, f, ensure_ascii=False, indent=2)

    # Print summary
    total_routes = sum(len(day["spots"]) for day in trip["itinerary"])
    print(f"\nDone! Filled {total_routes} routes across {len(trip['itinerary'])} days.")
    print(f"metadata.amap_used = {trip['metadata']['amap_used']}")

    # Verify no null routes remain
    null_routes = []
    for day in trip["itinerary"]:
        for i, spot in enumerate(day["spots"]):
            if spot.get("route") is None:
                null_routes.append(f"  Day {day['day_number']} Spot {i+1}: {spot.get('name')}")
    if null_routes:
        print(f"\nWARNING: {len(null_routes)} routes still null:")
        for nr in null_routes:
            print(nr)
    else:
        print("\nAll routes filled successfully!")


if __name__ == "__main__":
    main()
