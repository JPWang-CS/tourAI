#!/usr/bin/env python3
"""Update all hotels in trip.json with real verified data and recalculate budget."""

import json
import re

TRIP_PATH = r"D:\desktop\旅游\data\trips\jiuzhai-chuanxi-9d\trip.json"

with open(TRIP_PATH, "r", encoding="utf-8") as f:
    trip = json.load(f)

# ── Hotel definitions ──────────────────────────────────────────────

CHENGDU_HOTEL = {
    "name": "泰平·崇丽酒店(成都春熙路太古里店) ★首选 | 序里旅行酒店(成都太古里春熙路店) ★备选",
    "area": "春熙路/太古里商圈",
    "price_range": "¥200-400/晚",
    "highlights": "泰平·崇丽: 距太升南路地铁站490m, 步行至太古里1.3km, 免费停车场+自助早餐, 评分4.7, 2019年开业 | 序里: 距市二医院地铁站220m, 工业风设计+天台花园, 免费洗衣烘干+每日Citywalk活动, 欢迎水果, 评分4.7",
    "source": "websearch"
}

JIUZHAI_HOTEL = {
    "name": "智选假日酒店(九寨沟风景区店) ★首选 | 云孚里云宿·镜水云居(九寨沟千古情店) ★备选",
    "area": "九寨沟口漳扎镇",
    "price_range": "¥350-800/晚",
    "highlights": "智选假日: 彭丰村步行即达景区入口, 含免费早餐, 隔音好+淋浴水压足, 评分4.8 | 云孚里云宿: 步行15分钟到景区, 私汤温泉+藏服体验+摄影服务, 智能客控+地暖, 评分4.7",
    "source": "websearch"
}

SIGUNIANG_HOTEL = {
    "name": "归山牧雲民宿(双桥沟景区店) ★首选 | 观岳民宿(双桥沟景区店) ★备选",
    "area": "四姑娘山镇",
    "price_range": "¥400-700/晚",
    "highlights": "归山牧雲: 双碉村山坡上距景区6km, 躺在床上看雪山/日照金山, 地暖+智能马桶, 顶楼观景台烧烤观星, 免费骑马体验+牦牛火锅, 评分4.7 | 观岳: 景区内部步行到人参果坪10分钟, 窗外正对雪山, 含制氧机, 菌汤鸡锅+牦牛肉涮锅¥120/人, 评分4.7",
    "source": "websearch"
}

XINDUQIAO_HOTEL = {
    "name": "康定瑞楓民宿(新都桥店) ★首选 | 康定清康雅敘民宿(新都桥店) ★备选",
    "area": "新都桥镇",
    "price_range": "¥350-600/晚",
    "highlights": "瑞楓: 东俄洛二村(十里画廊入口), 传统藏式石木结构+现代简约, 落地窗直面雪山草甸, 藏式早餐¥15/人(酥油茶+青稞饼), 评分4.9, 2024年新开 | 清康雅敘: 东俄洛四村(十里画廊核心), 原木雕刻+彩绘藏式美学, 全屋地暖+供氧设备, 现煮酥油茶+牦牛肉包子早餐¥10/人, 2025年新开",
    "source": "websearch"
}

# ── Helper: replace text references ─────────────────────────────────

def replace_all_text(obj, old, new):
    """Recursively replace all string occurrences in a JSON-like structure."""
    if isinstance(obj, str):
        return obj.replace(old, new)
    if isinstance(obj, dict):
        return {k: replace_all_text(v, old, new) for k, v in obj.items()}
    if isinstance(obj, list):
        return [replace_all_text(v, old, new) for v in obj]
    return obj

# ── Day-specific hotel highlights customization ────────────────────

def chengdu_hotel_for_day(day_num, context_note):
    """Return Chengdu hotel with day-specific highlights suffix."""
    h = dict(CHENGDU_HOTEL)
    h["highlights"] = CHENGDU_HOTEL["highlights"] + " | " + context_note
    return h

# ── Apply hotel replacements per day ────────────────────────────────

for day in trip["itinerary"]:
    dn = day["day_number"]

    if dn in (1, 2, 4, 5, 8):
        # Chengdu nights
        notes = {
            1: "D1抵蓉首晚: 放下行李直奔苍蝇馆子, 春熙路太古里步行即达",
            2: "D2续住: 地铁至犀浦站换乘城际列车18分钟直达都江堰, 晚间返回便利",
            4: "D4九寨高铁返蓉: 成都东站打车约25分钟到店, 楼下美食街深夜营业",
            5: "D5成都慢生活: 睡到自然醒, 熊猫基地/鹤鸣茶社/太古里均在市区, 打车直达",
            8: "D8川西自驾归来: 还车后最后一晚, 楼下美食街深夜营业, 明早D9宽窄巷子告别成都",
        }
        day["hotel"] = chengdu_hotel_for_day(dn, notes[dn])

    elif dn == 3:
        day["hotel"] = dict(JIUZHAI_HOTEL)

    elif dn == 6:
        day["hotel"] = dict(SIGUNIANG_HOTEL)

    elif dn == 7:
        day["hotel"] = dict(XINDUQIAO_HOTEL)

    # D9 has hotel: null, skip

# ── Replace legacy hotel name references in all text ────────────────

trip = replace_all_text(trip, "嘉立精选酒店(成都春熙路太古里店)", "泰平·崇丽酒店(成都春熙路太古里店)")
trip = replace_all_text(trip, "嘉立精选酒店", "泰平·崇丽酒店")
trip = replace_all_text(trip, "嘉立精选", "泰平·崇丽")
trip = replace_all_text(trip, "全季酒店(成都春熙路太古里店)", "序里旅行酒店(成都太古里春熙路店)")
trip = replace_all_text(trip, "全季酒店", "序里旅行酒店")
trip = replace_all_text(trip, "见山民宿", "归山牧雲民宿")
trip = replace_all_text(trip, "归山牧雲民宿（四姑娘山镇）", "归山牧雲民宿(双桥沟景区店)")

# ── Update budget ───────────────────────────────────────────────────

# New hotel total calculation:
# Chengdu 5 nights: ¥200-400/night → ¥1000-2000
# Jiuzhaigou 1 night: ¥350-800/night
# Siguniang 1 night: ¥400-700/night
# Xinduqiao 1 night: ¥350-600/night
# Total: ¥2100-4100

hotel_low = 200*5 + 350 + 400 + 350  # 2100
hotel_high = 400*5 + 800 + 700 + 600  # 4100

trip["budget"]["hotel"]["total"] = f"{hotel_low}-{hotel_high}"
trip["budget"]["hotel"]["per_person"] = f"{hotel_low//2}-{hotel_high//2}"
trip["budget"]["hotel"]["detail"] = (
    "成都5晚——D1+D2+D4+D5+D8 泰平·崇丽(¥200-350)×5=¥1000-1750(或序里¥250-400×5=¥1250-2000); "
    "九寨沟口1晚¥350-800(D3智选假日¥350-500或云孚里云宿¥600-800); "
    "四姑娘山镇1晚¥400-700(D6归山牧雲¥500-700或观岳¥400-600); "
    "新都桥1晚¥350-600(D7瑞楓¥350-500或清康雅敘¥400-600)。"
    "均为2人一间共8晚。"
)

# Recalculate total budget
# Sum all low values, sum all high values
def parse_range(r):
    """Parse 'X-Y' or single number into (low, high)."""
    if isinstance(r, (int, float)):
        return (int(r), int(r))
    parts = str(r).split("-")
    low = int(parts[0])
    high = int(parts[1]) if len(parts) > 1 else low
    return (low, high)

total_low = 0
total_high = 0
for key in ["flight", "train", "bus", "car_rental", "hotel", "tickets", "food"]:
    val = trip["budget"][key]["total"]
    low, high = parse_range(val)
    total_low += low
    total_high += high

trip["budget"]["total"]["range"] = f"{total_low}-{total_high}"
trip["budget"]["total"]["per_person"] = f"{total_low//2}-{total_high//2}"
trip["budget"]["total"]["note"] = (
    "不含购物和个人消费。旺季(国庆)机票可能上浮30-50%, 酒店上浮20-30%。"
    "淡季(9月初/10月下旬)取预算低值。本方案以自然风光+免费观景台为主, 门票费用约¥1228。"
    "新方案优势: 成都取还车零异地费(省¥500+)+少开200km(省油费¥100)+多出D4高铁票(+¥280)和直通车(+¥102)。"
)

# ── Update metadata ─────────────────────────────────────────────────

trip["metadata"]["generated_at"] = "2026-06-29T18:00:00+08:00"
trip["metadata"]["version"] = "2.2.0"

# ── Write back ──────────────────────────────────────────────────────

with open(TRIP_PATH, "w", encoding="utf-8") as f:
    json.dump(trip, f, ensure_ascii=False, indent=2)

print("trip.json updated successfully!")
print(f"   Hotel total: {hotel_low}-{hotel_high}")
print(f"   Budget total: {total_low}-{total_high}")
