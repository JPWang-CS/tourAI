#!/usr/bin/env python3
"""
Generate full styled HTML from trip.json for jiuzhai-chuanxi-9d.
"""

import json
import sys
import os

TRIP_PATH = "D:/desktop/旅游/data/trips/jiuzhai-chuanxi-9d/trip.json"
OUT_PATH = "D:/desktop/旅游/data/trips/jiuzhai-chuanxi-9d/output.html"

DAY_GRADIENTS = [
    "d1",  # D1 - warm pink
    "d3",  # D2 - purple/pink
    "d4",  # D3 - yellow/cyan
    "d5",  # D4 - purple/blue
    "d2",  # D5 - blue/cyan
    "d1",  # D6 - warm pink
    "d2",  # D7 - blue/cyan
    "d3",  # D8 - purple/pink
    "d4",  # D9 - yellow/cyan
]

def load_trip():
    with open(TRIP_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def css():
    return '''@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

* { margin:0; padding:0; box-sizing:border-box; }

body {
  font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
  background: #f5f5f5;
  color: #333;
  line-height: 1.7;
}

/* Quick Navigation */
.quick-nav {
  position: fixed; right: 16px; top: 50%;
  transform: translateY(-50%); z-index: 100;
  display: flex; flex-direction: column; gap: 8px;
  opacity: 0.65; transition: opacity 0.3s ease;
}
.quick-nav:hover { opacity: 1; }
.quick-nav .nav-item { display: flex; align-items: center; gap: 6px; cursor: pointer; transition: all 0.2s ease; padding: 2px 0; }
.quick-nav .nav-dot { width: 6px; height: 6px; border-radius: 50%; background: #888; transition: all 0.2s ease; flex-shrink: 0; }
.quick-nav .nav-item:hover .nav-dot { background: #555; }
.quick-nav .nav-item.active .nav-dot { background: #7c6ef0; }
.quick-nav .nav-label { font-size: 11px; color: #666; white-space: nowrap; transition: color 0.2s ease; }
.quick-nav .nav-item:hover .nav-label { color: #333; }
.quick-nav .nav-item.active .nav-label { color: #7c6ef0; font-weight: 500; }

/* Collapsible */
.collapsible { cursor: pointer; user-select: none; }
.collapsible .collapse-icon { display: inline-block; margin-left: 8px; font-size: .7em; transition: transform 0.3s ease; opacity: 0.5; }
.collapsible.collapsed .collapse-icon { transform: rotate(-90deg); }
.collapse-content { max-height: 5000px; overflow: hidden; transition: max-height 0.4s ease-out; }
.collapse-content.collapsed { max-height: 0; }

/* Day card collapse */
.day-card .day-header { cursor: pointer; position: relative; }
.day-card .day-header::after { content: '\\25BC'; position: absolute; right: 20px; top: 50%; transform: translateY(-50%); font-size: .7em; opacity: 0.5; transition: transform 0.3s ease; color: inherit; }
.day-card.collapsed .day-header::after { transform: translateY(-50%) rotate(-90deg); }
.day-card .spots-wrapper { transition: max-height 0.4s ease-out; max-height: 10000px; overflow: hidden; }
.day-card.collapsed .spots-wrapper { max-height: 0; }

/* Hero */
.hero {
  position: relative; height: 380px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  overflow: hidden; display: flex; align-items: center; justify-content: center; text-align: center;
}
.hero::before { content: ''; position: absolute; bottom: -1px; left: 0; width: 100%; height: 60px; background: #f5f5f5; clip-path: ellipse(55% 100% at 50% 100%); }
.hero-inner { position: relative; z-index:1; padding: 0 16px; }
.hero h1 { font-size: 2.2em; font-weight: 700; color: #fff; text-shadow: 0 2px 20px rgba(0,0,0,.2); margin-bottom: 6px; }
.hero .subtitle { font-size: 1.05em; color: rgba(255,255,255,.9); font-weight: 300; }
.hero .tag-row { margin-top: 14px; display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; }
.hero .tag { background: rgba(255,255,255,.2); backdrop-filter: blur(6px); color: #fff; padding: 4px 14px; border-radius: 20px; font-size: .82em; }
.hero .emojis { font-size: 2.8em; margin-bottom: 10px; }

/* Container */
.container { max-width: 780px; margin: 0 auto; padding: 20px 16px 60px; }

/* Transport Card */
.transport-card { background: #fff; border-radius: 16px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 12px rgba(0,0,0,.06); }
.transport-card h2 { font-size: 1.2em; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.transport-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.t-item { background: #f8f9ff; border-radius: 12px; padding: 14px; position: relative; }
.t-item.recommend { background: linear-gradient(135deg, #e8f0ff, #f0e6ff); border: 2px solid #7c6ef0; }
.t-item .badge { position: absolute; top: -8px; right: 10px; background: #7c6ef0; color: #fff; font-size: .7em; padding: 2px 10px; border-radius: 10px; }
.t-item .t-title { font-weight: 700; font-size: .95em; margin-bottom: 4px; }
.t-item .t-detail { font-size: .82em; color: #888; }
.t-item .t-price { font-size: 1.1em; font-weight: 700; color: #e05a3a; margin-top: 6px; }

/* Day Cards */
.day-card { background: #fff; border-radius: 16px; overflow: hidden; margin-bottom: 24px; box-shadow: 0 2px 12px rgba(0,0,0,.06); }
.day-header { padding: 20px 24px 16px; color: #fff; }
.day-header.d1 { background: linear-gradient(135deg, #f6a085, #f2719c); }
.day-header.d2 { background: linear-gradient(135deg, #4facfe, #00f2fe); }
.day-header.d3 { background: linear-gradient(135deg, #a18cd1, #fbc2eb); }
.day-header.d4 { background: linear-gradient(135deg, #fddb92, #d1fdff); color: #666; }
.day-header.d5 { background: linear-gradient(135deg, #667eea, #764ba2); }
.day-header .day-num { font-size: 1.6em; font-weight: 700; }
.day-header .day-title { font-size: .9em; opacity: .85; margin-top: 2px; }
.day-header .day-route { font-size: .82em; opacity: .85; margin-top: 6px; }

/* Spots */
.spot { padding: 18px 24px; border-bottom: 1px solid #f0f0f0; position: relative; }
.spot:last-child { border-bottom: none; }
.spot-head { display: flex; align-items: flex-start; gap: 12px; }
.spot-icon { width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.4em; flex-shrink: 0; }
.spot:nth-of-type(odd) .spot-icon { background: #fff0f0; }
.spot:nth-of-type(even) .spot-icon { background: #f0f4ff; }
.spot-name { font-weight: 700; font-size: 1.05em; }
.spot-price { display: inline-block; background: #fff3e0; color: #e65100; font-size: .75em; padding: 1px 8px; border-radius: 8px; margin-left: 6px; font-weight: 500; }
.spot-transit { display: inline-flex; align-items: center; gap: 4px; background: linear-gradient(135deg, #e8f0ff, #f0e6ff); color: #5b7fdb; font-size: .72em; padding: 2px 10px; border-radius: 8px; margin-left: 6px; font-weight: 500; flex-wrap: wrap; }
.spot-transit .transit-time { color: #7c6ef0; font-weight: 700; }
.spot-desc { font-size: .88em; color: #666; margin-top: 6px; line-height: 1.6; }
.spot-romance { margin-top: 8px; padding: 8px 12px; background: linear-gradient(90deg, #fff5f5, #fff0fb); border-radius: 10px; font-size: .84em; color: #c06; border-left: 3px solid #f2719c; }

/* Route Bars */
.route-bar { display: flex; align-items: center; gap: 4px; padding: 10px 24px; background: linear-gradient(90deg, #e8f0ff, #f0e6ff); font-size: .82em; color: #5b7fdb; overflow-x: auto; flex-wrap: wrap; border-left: 4px solid #7c6ef0; font-weight: 500; }
.route-bar .dot { width: 6px; height: 6px; border-radius: 50%; background: #7c6ef0; flex-shrink: 0; }
.route-bar .r-item { white-space: nowrap; }

/* Parking */
.parking-info { margin-top: 6px; padding: 6px 10px; background: #f0fdf4; border-radius: 8px; font-size: .78em; color: #166534; display: inline-flex; align-items: center; gap: 6px; flex-wrap: wrap; border-left: 3px solid #22c55e; }
.parking-info .pk-price { font-weight: 700; color: #15803d; }
.parking-info .pk-tip { color: #854d0e; font-size: .92em; }

/* Waypoint */
.waypoint-bar { margin: 0 24px; padding: 8px 14px; background: #fffbeb; border-radius: 8px; font-size: .78em; color: #92400e; display: flex; align-items: center; gap: 6px; flex-wrap: wrap; border: 1px dashed #fcd34d; }
.waypoint-bar .wp-facilities { color: #666; font-size: .92em; }

/* Pitfall */
.pitfall { margin-top: 8px; padding: 8px 12px; background: #fffbe6; border-radius: 10px; font-size: .82em; color: #ad6800; border-left: 3px solid #faad14; }

/* Hotel Rec Section */
.hotel-rec-section { margin: 16px 24px; padding: 16px 20px; background: linear-gradient(135deg, #f8f9ff, #f0f4ff); border-radius: 12px; }
.hr-title { font-weight: 700; font-size: 1em; margin-bottom: 10px; }
.hr-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.hr-item { background: #fff; border-radius: 10px; padding: 12px; }
.hr-name { font-weight: 700; font-size: .88em; }
.hr-price { font-size: .8em; color: #e05a3a; font-weight: 600; margin-top: 4px; }
.hr-desc { font-size: .76em; color: #666; margin-top: 4px; line-height: 1.5; }

/* Food Section */
.food-section { background: #fff; border-radius: 16px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 12px rgba(0,0,0,.06); }
.food-section h2 { font-size: 1.2em; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.food-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.food-item { background: #fef9f0; border-radius: 12px; padding: 14px; }
.food-item .f-name { font-weight: 700; font-size: .92em; }
.food-item .f-shop { font-size: .78em; color: #999; margin-top: 2px; }
.food-item .f-price { color: #e05a3a; font-weight: 700; font-size: .9em; margin-top: 4px; }
.food-item .f-note { font-size: .78em; color: #666; margin-top: 2px; }

/* Avoid List */
.avoid-section { background: #fff; border-radius: 16px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 12px rgba(0,0,0,.06); }
.avoid-section h2 { font-size: 1.2em; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.avoid-list { display: grid; grid-template-columns: 1fr; gap: 8px; }
.avoid-item { display: flex; gap: 10px; padding: 10px 14px; border-radius: 10px; background: #fff5f5; font-size: .86em; }
.avoid-item .a-num { background: #ff4d4f; color: #fff; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: .75em; font-weight: 700; flex-shrink: 0; }
.avoid-item .a-wrong { color: #ff4d4f; font-weight: 700; text-decoration: line-through; }
.avoid-item .a-right { color: #52c41a; font-weight: 500; }

/* Budget */
.budget-card { background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 16px; padding: 24px; margin-bottom: 20px; color: #fff; }
.budget-card h2 { font-size: 1.2em; margin-bottom: 16px; }
.budget-row { display: flex; justify-content: space-between; padding: 6px 0; font-size: .9em; border-bottom: 1px solid rgba(255,255,255,.15); }
.budget-row.nb { border: none; }
.budget-total { text-align: center; margin-top: 14px; padding-top: 14px; border-top: 2px solid rgba(255,255,255,.3); font-size: 1.3em; font-weight: 700; }

/* Tips */
.tips-card { background: linear-gradient(135deg, #fff0f5, #fff5f0); border-radius: 16px; padding: 24px; margin-bottom: 20px; }
.tips-card h2 { font-size: 1.2em; margin-bottom: 14px; }
.tips-card .tip-item { padding: 8px 0; font-size: .9em; display: flex; gap: 8px; }

/* Footer */
.footer { text-align: center; padding: 30px 0 20px; color: #bbb; font-size: .82em; }

/* Responsive */
@media (max-width: 1024px) { .quick-nav { display: none; } }
@media (max-width: 768px) {
  .hero { height: auto; min-height: 280px; padding: 40px 16px 70px; }
  .hero h1 { font-size: 1.5em; padding: 0 8px; word-break: break-word; }
  .hero .subtitle { font-size: .85em; padding: 0 8px; }
  .hero .emojis { font-size: 2em; margin-bottom: 8px; }
  .hero .tag { font-size: .72em; padding: 3px 8px; }
  .container { padding: 16px 12px 40px; }
  .transport-grid, .hr-grid { grid-template-columns: 1fr; }
  .food-grid { grid-template-columns: 1fr; }
  .day-header { padding: 16px 16px 14px; }
  .spot { padding: 14px 16px; }
  .spot-name { font-size: .95em; }
  .spot-transit { font-size: .68em; }
  .route-bar { padding: 8px 16px; font-size: .76em; }
  .parking-info { font-size: .72em; display: block; }
  .waypoint-bar { margin: 0 16px; font-size: .72em; }
}
@media (max-width: 375px) {
  .container { padding: 12px; }
  .hero h1 { font-size: 1.3em; }
  .hero .tag { font-size: .68em; padding: 2px 6px; }
  .spot-icon { width: 34px; height: 34px; font-size: 1.1em; }
}
@media (hover: none) {
  .quick-nav .nav-item { padding: 6px 0; }
  * { -webkit-tap-highlight-color: transparent; }
}
@media print {
  .quick-nav { display: none; }
  .day-card { break-inside: avoid; }
}'''


def make_hero(trip):
    title = trip.get("title", "")
    emojis = "🐼🏔️🍜🏯🚗"
    subtitle = "高铁入九寨 + 熊猫大道自驾 + 秘境S434 · 2人深度慢游"
    tags = [
        "🏔️ 自然风光", "🍜 美食之旅", "🚗 川西自驾",
        "📸 9天8晚", "💑 双人浪漫"
    ]
    tag_html = "".join(f'<span class="tag">{t}</span>' for t in tags)
    return f'''<section class="hero">
  <div class="hero-inner">
    <div class="emojis">{emojis}</div>
    <h1>{title}</h1>
    <div class="subtitle">{subtitle}</div>
    <div class="tag-row">{tag_html}</div>
  </div>
</section>'''


def make_transport(trip):
    items = []
    for t in trip.get("transport_to_dest", []):
        items.append(f'''      <div class="t-item recommend">
        <div class="badge">去程</div>
        <div class="t-title">✈️ 航班 · {t.get('from','')} → {t.get('to','')}</div>
        <div class="t-detail">双流/天府机场 · {t.get('duration','')} · D1傍晚前抵达</div>
        <div class="t-price">¥{t.get('estimated_price','')}/人</div>
      </div>''')
    for t in trip.get("transport_return", []):
        items.append(f'''      <div class="t-item recommend">
        <div class="badge">回程</div>
        <div class="t-title">✈️ 航班 · {t.get('from','')} → {t.get('to','')}</div>
        <div class="t-detail">双流/天府机场 · {t.get('duration','')} · D9下午/晚班</div>
        <div class="t-price">¥{t.get('estimated_price','')}/人</div>
      </div>''')

    # Fixed transport items
    extra = [
        ('🚄 城际 · 犀浦 ↔ 离堆公园', '18分钟 · ¥10 · D2往返都江堰', '¥10/人'),
        ('🚄 高铁 · 成都东 → 黄龙九寨', '约2小时 · ¥140 · D3去程', '¥140/人'),
        ('🚄 高铁 · 黄龙九寨 → 成都东', '约2h20min · ¥140 · D4回程', '¥140/人'),
        ('🚌 直通车 · 黄龙九寨 ↔ 沟口', '约1.5小时 · ¥51 · D3去/D4回', '¥51/人'),
        ('🚗 自驾 · 一嗨成都取还', '3天(D6-D8) · G350+S434 · 零异地费', '¥1200-1800'),
    ]
    for title, detail, price in extra:
        cls = "t-item"
        items.append(f'''      <div class="{cls}">
        <div class="t-title">{title}</div>
        <div class="t-detail">{detail}</div>
        <div class="t-price">{price}</div>
      </div>''')

    return f'''<div class="transport-card collapsible" data-nav="交通信息">
  <h2>🚄 交通信息 <span class="collapse-icon">▼</span></h2>
  <div class="collapse-content">
    <div class="transport-grid">
{chr(10).join(items)}
    </div>
  </div>
</div>'''


def price_label(price):
    if price == 0 or price is None:
        return "免费"
    return f"¥{price}"


def make_route_bar(day):
    """Build route bar from spots with routes"""
    if not day.get("spots"):
        return ""
    parts = ['<span class="dot"></span>']
    for i, spot in enumerate(day["spots"]):
        emoji = spot.get("emoji", "📍")
        name = spot.get("name", "?")
        # Truncate name for route bar
        short_name = name[:10] + "…" if len(name) > 10 else name
        parts.append(f'<span class="r-item">{emoji} {short_name}</span>')
        if i < len(day["spots"]) - 1:
            route = spot.get("route")
            if route:
                dist = route.get("distance_text", "")
                dur = route.get("duration_text", "")
                emoji_r = route.get("emoji", "🚗")
                parts.append(f'<span>→ {emoji_r} {dur}/{dist} →</span>')
            else:
                parts.append('<span>→</span>')
    return f'''    <div class="route-bar">
      {chr(10) + "      ".join(parts)}
    </div>'''


def make_spot_html(spot):
    name = spot.get("name", "?")
    price = spot.get("ticket_price", 0)
    emoji = spot.get("emoji", "📍")
    desc = spot.get("description", "")
    romance = spot.get("romantic_moment", "")
    pitfall = spot.get("pitfall_warning", "")
    photo_tip = spot.get("photo_tip", "")

    route = spot.get("route")
    transit_html = ""
    if route:
        from_n = route.get("from_name", "")
        mode = route.get("transport_mode", "")
        dist = route.get("distance_text", "")
        dur = route.get("duration_text", "")
        emoji_r = route.get("emoji", "🚗")
        transit_html = f'''
            <span class="spot-transit">{emoji_r} {from_n} <span class="transit-time">{dist}/{dur}</span></span>'''

    price_str = price_label(price)
    if price != 0:
        price_sp = f' <span class="spot-price">{price_str}</span>'
    else:
        price_sp = f' <span class="spot-price">{price_str}</span>'

    html = f'''    <div class="spot">
      <div class="spot-head">
        <div class="spot-icon">{emoji}</div>
        <div>
          <div class="spot-name">{name}{price_sp}{transit_html}</div>
          <div class="spot-desc">{desc}</div>'''

    if photo_tip:
        html += f'''
          <div class="parking-info" style="background:#fff7ed;border-left-color:#f97316;color:#9a3412;">📷 {photo_tip}</div>'''

    if romance:
        html += f'''
          <div class="spot-romance">💕 {romance}</div>'''

    if pitfall:
        html += f'''
          <div class="pitfall">⚠️ {pitfall}</div>'''

    html += '''
        </div>
      </div>
    </div>'''
    return html


def make_waypoints(spot):
    wps = spot.get("route", {}).get("waypoints", [])
    if not wps:
        return ""
    html_parts = []
    for wp in wps:
        wname = wp.get("name", "")
        wtype = wp.get("type", "viewpoint")
        wdist = wp.get("at_distance_km", 0)
        wfac = wp.get("facilities", "")
        wtips = wp.get("tips", "")
        if wtype == "rest_stop":
            icon = "🚄"
        else:
            icon = "🏔️"
        html_parts.append(f'    <div class="waypoint-bar">{icon} {wname}（约{wdist}km处）· {wfac} · 💡 {wtips}</div>')
    return "\n".join(html_parts)


def make_parking(parking):
    if not parking:
        return ""
    name = parking.get("name", "")
    dist = parking.get("distance_text", "")
    price = parking.get("price_text", "")
    tips = parking.get("tips", "")
    return f'''    <div class="parking-info">
      🅿️ {name} · {dist} · <span class="pk-price">{price}</span>
      <span class="pk-tip">💡 {tips}</span>
    </div>'''


def make_day_food(day):
    meals = day.get("meals", {})
    if not meals:
        return ""

    all_items = []
    for mtype, label in [("breakfast", "🌅 早餐"), ("lunch", "☀️ 午餐"), ("dinner", "🌙 晚餐")]:
        mlist = meals.get(mtype, [])
        for m in mlist:
            name = m.get("name", "")
            price = m.get("price_per_person", 0)
            note = m.get("note", "")
            addr = m.get("address", "")
            all_items.append(f'''        <div class="food-item">
          <div class="f-name">{label}{'（备选）' if '备选' in name else ''}</div>
          <div class="f-shop">{name}</div>
          <div class="f-price">人均 ¥{price}</div>
          <div class="f-note">{note}{' 地址：' + addr if addr and len(addr) < 30 else ''}</div>
        </div>''')

    if not all_items:
        return ""

    return f'''    <div class="food-section" style="margin: 16px 24px; padding: 16px 20px; box-shadow: none;">
      <h2>🍽️ 餐饮推荐</h2>
      <div class="food-grid">
{chr(10).join(all_items)}
      </div>
    </div>'''


def make_day_hotel(day, night_num, city_label):
    hotel = day.get("hotel")
    if not hotel:
        return ""
    name = hotel.get("name", "")
    price = hotel.get("price_range", "")
    desc = hotel.get("highlights", "")
    return f'''    <div class="hotel-rec-section">
      <div class="hr-title">🏨 推荐住宿（{city_label}第{night_num}晚{f' · 续住' if night_num > 1 else ''}）</div>
      <div class="hr-grid">
        <div class="hr-item">
          <div class="hr-name">{name}</div>
          <div class="hr-price">💰 {price}</div>
          <div class="hr-desc">{desc}</div>
        </div>
      </div>
    </div>'''


def make_day_card(day, idx, night_tracker):
    dn = day.get("day_number", idx + 1)
    theme_parts = day.get("theme", "").split("·", 1)
    if len(theme_parts) == 2:
        day_num_title = theme_parts[0].strip()
        day_subtitle = theme_parts[1].strip()
    else:
        day_num_title = f"Day {dn}"
        day_subtitle = theme_parts[0] if theme_parts else ""

    route_summary = day.get("route_summary", "")
    gradient = DAY_GRADIENTS[idx] if idx < len(DAY_GRADIENTS) else "d1"

    # Determine hotel night label
    hotel = day.get("hotel")
    hotel_area = ""
    if hotel:
        hname = hotel.get("name", "")
        if "嘉立精选" in hname or "成都" in hotel.get("area", ""):
            hotel_area = "成都"
            key = "chengdu"
        elif "九寨" in hname or "漳扎" in hotel.get("area", ""):
            hotel_area = "九寨沟口"
            key = "jiuzhai"
        elif "四姑娘" in hname or "四姑娘" in hotel.get("area", ""):
            hotel_area = "四姑娘山"
            key = "siguniang"
        elif "新都桥" in hname or "贡嘎" in hname or "新都" in hotel.get("area", ""):
            hotel_area = "新都桥"
            key = "xinduqiao"
        else:
            hotel_area = "成都"
            key = "chengdu"

        night_tracker[key] = night_tracker.get(key, 0) + 1
        night_num = night_tracker[key]
    else:
        night_num = 0

    html = f'''<div class="day-card" data-nav="Day {dn}">
  <div class="day-header {gradient}">
    <div class="day-num">Day {dn} · {day_num_title}</div>
    <div class="day-title">{day_subtitle}</div>
    <div class="day-route">{route_summary}</div>
  </div>
  <div class="spots-wrapper">'''

    # Route bar for multi-spot days
    if len(day.get("spots", [])) > 1:
        html += "\n" + make_route_bar(day) + "\n"

    for spot in day.get("spots", []):
        html += "\n" + make_spot_html(spot)
        html += "\n" + make_waypoints(spot)
        html += "\n" + make_parking(spot.get("parking"))

    html += "\n" + make_day_food(day)
    html += "\n" + make_day_hotel(day, night_num, hotel_area if hotel_area else "成都")

    html += '''
  </div>
</div>'''
    return html


def make_food_summary(trip):
    items = trip.get("food_summary", [])
    if not items:
        return ""

    item_html = []
    for f in items:
        name = f.get("name", "")
        cuisine = f.get("cuisine", "")
        source = f.get("source", "")
        price = f.get("price_per_person", 0)
        reason = f.get("reason", "")
        dishes = ", ".join(f.get("recommended_dishes", [])[:4])
        item_html.append(f'''      <div class="food-item">
        <div class="f-name">🥢 {name}</div>
        <div class="f-shop">{cuisine} · {source}</div>
        <div class="f-price">人均 ¥{price}</div>
        <div class="f-note">推荐：{dishes}。{reason}</div>
      </div>''')

    return f'''<div class="food-section collapsible" data-nav="美食推荐">
  <h2>🍜 美食推荐汇总（{len(items)}家必吃） <span class="collapse-icon">▼</span></h2>
  <div class="collapse-content">
    <div class="food-grid">
{chr(10).join(item_html)}
    </div>
  </div>
</div>'''


def make_avoid_list(trip):
    items = trip.get("avoid_list", [])
    if not items:
        return ""

    item_html = []
    for i, a in enumerate(items, 1):
        wrong = a.get("wrong", "")
        correct = a.get("correct", "")
        item_html.append(f'''      <div class="avoid-item"><div class="a-num">{i}</div><div style="flex:1;"><span class="a-wrong">❌ {wrong}</span><br><span class="a-right">✅ {correct}</span></div></div>''')

    return f'''<div class="avoid-section collapsible" data-nav="避坑清单">
  <h2>⚠️ 避坑清单（{len(items)}条 · 必看） <span class="collapse-icon">▼</span></h2>
  <div class="collapse-content">
    <div class="avoid-list">
{chr(10).join(item_html)}
    </div>
  </div>
</div>'''


def make_budget(trip):
    b = trip.get("budget", {})
    flight = b.get("flight", {})
    train = b.get("train", {})
    bus = b.get("bus", {})
    car = b.get("car_rental", {})
    hotel = b.get("hotel", {})
    tickets = b.get("tickets", {})
    food = b.get("food", {})
    total = b.get("total", {})

    flight_range = flight.get("total", "2000-2800")
    train_total = train.get("total", 600)
    bus_total = bus.get("total", 204)
    car_range = car.get("total", "1500-2100")
    hotel_range = hotel.get("total", "2550-3870")
    tickets_total = tickets.get("total", 1416)
    food_range = food.get("total", "2500-3000")
    total_range = total.get("range", "10814-14434")
    per_person = total.get("per_person", "5407-7217")

    return f'''<div class="budget-card" data-nav="预算估算">
  <h2>💰 预算估算（2人 · 9天8晚）</h2>
  <div class="budget-row"><span>✈️ 往返机票</span><span>¥{flight_range}</span></div>
  <div class="budget-row"><span>🚄🚌 高铁+直通车</span><span>¥{train_total} + {bus_total} = ¥{train_total + bus_total}</span></div>
  <div class="budget-row"><span>🚗 租车3天（含油费+过路费）</span><span>¥{car_range}</span></div>
  <div class="budget-row"><span>🏨 住宿8晚（成都5+九寨1+四姑娘山1+新都桥1）</span><span>¥{hotel_range}</span></div>
  <div class="budget-row"><span>🎫 门票</span><span>¥{tickets_total}</span></div>
  <div class="budget-row" style="border:none;"><span>🍜 餐饮</span><span>¥{food_range}</span></div>
  <div class="budget-total">总计 ¥{total_range} · 人均 ¥{per_person}</div>
  <div style="margin-top:12px; font-size:.78em; opacity:.8;">
    <div style="display:flex; justify-content:space-between; padding:2px 0;"><span>高铁明细：D2犀浦↔离堆公园¥20×2 + D3成都东→黄龙九寨¥140×2 + D4黄龙九寨→成都东¥140×2 = ¥{train_total}</span></div>
    <div style="display:flex; justify-content:space-between; padding:2px 0;"><span>直通车明细：D3黄龙九寨站→沟口¥51×2 + D4沟口→黄龙九寨站¥51×2 = ¥{bus_total}</span></div>
    <div style="display:flex; justify-content:space-between; padding:2px 0;"><span>门票明细：熊猫基地¥110 + 都江堰¥160 + 九寨沟¥518 + 双桥沟¥300 + 甲居藏寨¥100 + 泸定桥¥20 + 红海子¥20 = ¥1,228</span></div>
    <div style="display:flex; justify-content:space-between; padding:2px 0;"><span>住宿明细：成都5晚(¥1,250-1,870) + 九寨1晚(¥400-800) + 四姑娘山1晚(¥400-500) + 新都桥1晚(¥400-500) = ¥2,450-3,670</span></div>
    <div style="display:flex; justify-content:space-between; padding:2px 0;"><span>新方案优势：成都取还零异地费(省¥500+) + 少开200km(省¥100) + 九寨沟口少住一晚(省¥400-800)但多出D4高铁票(+¥280)和直通车(+¥102)，净省约¥400-700</span></div>
  </div>
</div>'''


def make_tips(trip):
    tips = trip.get("tips", [])
    weather = trip.get("weather", {})
    weather_line = f"🌤️ {weather.get('season','')} · {weather.get('temp_range','')} · {weather.get('clothing','')}"

    tip_html = '\n'.join(f'  <div class="tip-item">✨ {t}</div>' for t in tips)

    return f'''<div class="tips-card" data-nav="出行Tips">
  <h2>💕 浪漫自驾出行Tips</h2>
  <div style="margin-bottom:12px; font-size:.88em; color:#666;">
    {weather_line}
  </div>
{tip_html}
</div>'''


def make_footer(trip):
    meta = trip.get("metadata", {})
    gen_date = meta.get("generated_at", "")[:10]
    sources = ", ".join(meta.get("sources", []))
    return f'''<footer class="footer">
  <p>由 <strong>tourAI</strong> 生成 · {gen_date}</p>
  <p>数据来源：{sources}（高德地图路线 + 小红书/马蜂窝体验 + WebSearch兜底）</p>
  <p>路线数据由 <strong>高德地图</strong> 提供</p>
  <p style="margin-top:8px; font-size:.75em; color:#ccc;">信息仅供参考，出行前请核实最新价格和开放时间</p>
</footer>'''


def js_code():
    return '''
<script>
// === Quick Nav: Auto-generate from sections ===
(function() {
  var sections = document.querySelectorAll('[data-nav]');
  var nav = document.getElementById('quickNav');
  if (!nav || !sections.length) return;

  sections.forEach(function(s) {
    var item = document.createElement('div');
    item.className = 'nav-item';
    item.innerHTML = '<span class="nav-dot"></span><span class="nav-label">' + s.dataset.nav + '</span>';
    item.addEventListener('click', function() {
      s.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    nav.appendChild(item);
  });

  // Scroll spy
  var items = nav.querySelectorAll('.nav-item');
  window.addEventListener('scroll', function() {
    var current = '';
    sections.forEach(function(s) {
      if (window.scrollY >= s.offsetTop - 100) current = s.dataset.nav;
    });
    items.forEach(function(item) {
      var label = item.querySelector('.nav-label').textContent;
      if (label === current) { item.classList.add('active'); }
      else { item.classList.remove('active'); }
    });
  });
})();

// === Collapse: Day cards ===
document.querySelectorAll('.day-card .day-header').forEach(function(header) {
  header.addEventListener('click', function() {
    header.parentElement.classList.toggle('collapsed');
  });
});

// === Collapse: Other sections with .collapsible class ===
document.querySelectorAll('.collapsible').forEach(function(el) {
  el.addEventListener('click', function() {
    el.classList.toggle('collapsed');
    var content = el.querySelector('.collapse-content');
    if (content) {
      content.classList.toggle('collapsed');
    }
  });
});
</script>'''


def main():
    trip = load_trip()

    parts = []
    parts.append('<!DOCTYPE html>')
    parts.append('<html lang="zh-CN">')
    parts.append('<head>')
    parts.append('<meta charset="UTF-8">')
    parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">')
    parts.append(f'<title>{trip.get("title", "旅行攻略")}</title>')
    parts.append('<style>')
    parts.append(css())
    parts.append('</style>')
    parts.append('</head>')
    parts.append('<body>')
    parts.append('')
    parts.append('<!-- ===== Right Quick Nav (generated by JS) ===== -->')
    parts.append('<nav class="quick-nav" id="quickNav"></nav>')
    parts.append('')
    parts.append('<!-- ===== HERO ===== -->')
    parts.append(make_hero(trip))
    parts.append('')
    parts.append('<div class="container">')
    parts.append('')
    parts.append('<!-- ===== TRANSPORT CARD ===== -->')
    parts.append(make_transport(trip))
    parts.append('')

    # Day cards with night tracking
    night_tracker = {}
    for i, day in enumerate(trip.get("itinerary", [])):
        parts.append(f'<!-- ===== DAY {i+1} ===== -->')
        parts.append(make_day_card(day, i, night_tracker))
        parts.append('')

    parts.append('<!-- ===== FOOD SUMMARY ===== -->')
    parts.append(make_food_summary(trip))
    parts.append('')

    parts.append('<!-- ===== AVOID LIST ===== -->')
    parts.append(make_avoid_list(trip))
    parts.append('')

    parts.append('<!-- ===== BUDGET ===== -->')
    parts.append(make_budget(trip))
    parts.append('')

    parts.append('<!-- ===== TIPS ===== -->')
    parts.append(make_tips(trip))
    parts.append('')

    parts.append('<!-- ===== FOOTER ===== -->')
    parts.append(make_footer(trip))
    parts.append('')
    parts.append('</div><!-- /container -->')
    parts.append('')
    parts.append(js_code())
    parts.append('')
    parts.append('</body>')
    parts.append('</html>')

    html = '\n'.join(parts)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML written to {OUT_PATH}")
    print(f"Size: {len(html)} chars, {html.count(chr(10))+1} lines")


if __name__ == "__main__":
    main()
