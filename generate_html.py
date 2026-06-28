#!/usr/bin/env python3
"""Generate output.html from trip.json"""
import json
import os

TRIP_DIR = r'D:\desktop\旅游\data\trips\9781c492-874b-4e85-a9d7-2726c6a2bb6b'
trip_path = os.path.join(TRIP_DIR, 'trip.json')
output_path = os.path.join(TRIP_DIR, 'output.html')

with open(trip_path, 'r', encoding='utf-8') as f:
    trip = json.load(f)

# ===== Day card gradient classes =====
# D1橙粉/D2蓝青/D3紫粉/D4黄青/D5翠绿/D6金橙/D7深蓝/D8紫蓝/D9玫红
day_gradients = {
    1: ('d1', 'linear-gradient(135deg, #f6a085, #f2719c)', '#fff'),
    2: ('d2', 'linear-gradient(135deg, #4facfe, #00f2fe)', '#fff'),
    3: ('d3', 'linear-gradient(135deg, #a18cd1, #fbc2eb)', '#fff'),
    4: ('d4', 'linear-gradient(135deg, #fddb92, #d1fdff)', '#666'),
    5: ('d5', 'linear-gradient(135deg, #11998e, #38ef7d)', '#fff'),
    6: ('d6', 'linear-gradient(135deg, #f7971e, #ffd200)', '#333'),
    7: ('d7', 'linear-gradient(135deg, #0c3483, #a2b6df)', '#fff'),
    8: ('d8', 'linear-gradient(135deg, #667eea, #764ba2)', '#fff'),
    9: ('d9', 'linear-gradient(135deg, #c31432, #240b36)', '#fff'),
}

transport_icons = {
    'walking': '🚶',
    'taxi': '🚗',
    'transit': '🚇🚄',
    'driving': '🚗',
    'flight': '✈️',
}
transport_labels = {
    'walking': '步行',
    'taxi': '打车',
    'transit': '地铁+城际',
    'driving': '自驾',
    'flight': '飞行',
}

def fmt_price(v):
    """Format a ticket price: 0 -> 免费, >0 -> ¥N"""
    if v == 0:
        return '免费'
    return f'¥{v}'

def render_route_bar(route):
    """Render compact route info"""
    if not route:
        return ''
    emoji = route.get('emoji', '🚗')
    mode = route.get('transport_mode', 'driving')
    dist = route.get('distance_text', '')
    dur = route.get('duration_text', '')
    return f'{emoji} {dist} / {dur}'


# ===== Build HTML =====
html = []

# Helper to write lines
def w(s):
    html.append(s)

# ===== HEAD =====
w('<!DOCTYPE html>')
w('<html lang="zh-CN">')
w('<head>')
w('<meta charset="UTF-8">')
w('<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">')
w(f'<title>{trip["title"]}</title>')
w('<link rel="preconnect" href="https://fonts.googleapis.com">')
w('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
w('<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">')
w('<style>')

# ===== CSS =====
w('''
/* === Reset === */
* { margin:0; padding:0; box-sizing:border-box; }

body {
  font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
  background: #f5f5f5;
  color: #333;
  line-height: 1.7;
}

/* === Quick Navigation === */
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

/* === Collapsible === */
.collapsible { cursor: pointer; user-select: none; }
.collapsible .collapse-icon { display: inline-block; margin-left: 8px; font-size: .7em; transition: transform 0.3s ease; opacity: 0.5; }
.collapsible.collapsed .collapse-icon { transform: rotate(-90deg); }
.collapse-content { max-height: 50000px; overflow: hidden; transition: max-height 0.5s ease-out; }
.collapse-content.collapsed { max-height: 0; }

/* Day card collapse */
.day-card .day-header { cursor: pointer; position: relative; }
.day-card .day-header::after { content: '▼'; position: absolute; right: 20px; top: 50%; transform: translateY(-50%); font-size: .7em; opacity: 0.5; transition: transform 0.3s ease; }
.day-card.collapsed .day-header::after { transform: translateY(-50%) rotate(-90deg); }
.day-card .spots-wrapper { transition: max-height 0.5s ease-out; max-height: 20000px; overflow: hidden; }
.day-card.collapsed .spots-wrapper { max-height: 0; }

/* === Hero === */
.hero {
  position: relative; min-height: 420px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  overflow: hidden; display: flex; align-items: center; justify-content: center; text-align: center;
  padding: 50px 24px 80px;
}
.hero::before { content: ''; position: absolute; bottom: -1px; left: 0; width: 100%; height: 60px; background: #f5f5f5; clip-path: ellipse(55% 100% at 50% 100%); }
.hero::after { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: url(\"data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E\"); opacity: 0.5; }
.hero-inner { position: relative; z-index: 1; max-width: 700px; }
.hero h1 { font-size: 2.4em; font-weight: 700; color: #fff; text-shadow: 0 2px 20px rgba(0,0,0,.2); margin-bottom: 6px; letter-spacing: 2px; }
.hero .subtitle { font-size: 1.15em; color: rgba(255,255,255,.9); font-weight: 300; margin-bottom: 4px; }
.hero .tag-row { margin-top: 16px; display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
.hero .tag { background: rgba(255,255,255,.2); backdrop-filter: blur(6px); color: #fff; padding: 6px 16px; border-radius: 20px; font-size: .84em; font-weight: 400; }
.hero .emojis { font-size: 3.2em; margin-bottom: 10px; }

/* === Container === */
.container { max-width: 780px; margin: 0 auto; padding: 20px 16px 60px; }

/* === Transport Card === */
.transport-card { background: #fff; border-radius: 16px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 12px rgba(0,0,0,.06); }
.transport-card h2 { font-size: 1.2em; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.transport-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.t-item { background: #f8f9ff; border-radius: 12px; padding: 16px; position: relative; }
.t-item .t-title { font-weight: 700; font-size: .95em; margin-bottom: 6px; }
.t-item .t-detail { font-size: .82em; color: #888; line-height: 1.5; }
.t-item .t-price { font-size: 1.15em; font-weight: 700; color: #e05a3a; margin-top: 8px; }
.t-item .t-note { font-size: .78em; color: #999; margin-top: 6px; line-height: 1.5; }

/* === Day Cards === */
.day-card { background: #fff; border-radius: 16px; overflow: hidden; margin-bottom: 24px; box-shadow: 0 2px 12px rgba(0,0,0,.06); }
.day-header { padding: 22px 28px 18px; color: #fff; position: relative; }
.day-header.d4, .day-header.d6 { color: #444; }
.day-header .day-num { font-size: 1.7em; font-weight: 700; }
.day-header .day-title { font-size: 1.15em; font-weight: 500; margin-top: 4px; }
.day-header .day-route { font-size: .84em; opacity: .85; margin-top: 8px; line-height: 1.6; }

/* === Route Bars === */
.route-bar { display: flex; align-items: center; gap: 4px; padding: 10px 28px; background: linear-gradient(90deg, #e8f0ff, #f0e6ff); font-size: .82em; color: #5b7fdb; overflow-x: auto; flex-wrap: wrap; border-left: 4px solid #7c6ef0; font-weight: 500; }
.route-bar .dot { width: 8px; height: 8px; border-radius: 50%; background: #7c6ef0; flex-shrink: 0; }
.route-bar .r-item { white-space: nowrap; font-weight: 600; }

/* Hotel→Spot Route Bar */
.hotel-route-bar { display: flex; align-items: center; gap: 4px; padding: 8px 28px; background: linear-gradient(90deg, #fff0f5, #fff5f0); font-size: .8em; color: #d06; overflow-x: auto; flex-wrap: wrap; border-left: 4px solid #f2719c; font-weight: 500; }
.hotel-route-bar .hdot { width: 8px; height: 8px; border-radius: 50%; background: #f2719c; flex-shrink: 0; }
.hotel-route-bar .hroute-item { white-space: nowrap; }

/* === Spots === */
.spot { padding: 20px 28px; border-bottom: 1px solid #f0f0f0; position: relative; }
.spot:last-child { border-bottom: none; }
.spot-head { display: flex; align-items: flex-start; gap: 14px; }
.spot-icon { width: 48px; height: 48px; min-width: 48px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 1.5em; flex-shrink: 0; }
.spot-icon.c1 { background: #fff0f0; }
.spot-icon.c2 { background: #f0f4ff; }
.spot-icon.c3 { background: #f0fff4; }
.spot-icon.c4 { background: #fff8f0; }
.spot-name { font-weight: 700; font-size: 1.08em; margin-bottom: 4px; }
.spot-price { display: inline-block; background: #fff3e0; color: #e65100; font-size: .75em; padding: 2px 10px; border-radius: 8px; margin-left: 6px; font-weight: 500; }
.spot-transit { display: inline-flex; align-items: center; gap: 4px; background: linear-gradient(135deg, #e8f0ff, #f0e6ff); color: #5b7fdb; font-size: .72em; padding: 3px 10px; border-radius: 8px; margin-left: 6px; font-weight: 500; white-space: nowrap; }
.spot-desc { font-size: .88em; color: #666; margin-top: 8px; line-height: 1.7; }
.spot-romance { margin-top: 10px; padding: 10px 14px; background: linear-gradient(90deg, #fff5f5, #fff0fb); border-radius: 10px; font-size: .84em; color: #c06; border-left: 3px solid #f2719c; line-height: 1.6; }
.spot-photo { margin-top: 6px; padding: 6px 10px; background: #f0f9ff; border-radius: 8px; font-size: .78em; color: #0369a1; }
.spot-avoid { margin-top: 8px; padding: 8px 12px; background: #fffbe6; border-radius: 10px; font-size: .82em; color: #ad6800; border-left: 3px solid #faad14; line-height: 1.5; }

/* === Parking === */
.parking-info {
  margin-top: 8px; padding: 8px 12px;
  background: #f0fdf4; border-radius: 8px;
  font-size: .78em; color: #166534;
  display: inline-flex; align-items: center; gap: 6px; flex-wrap: wrap;
  border-left: 3px solid #22c55e;
}
.parking-info .pk-price { font-weight: 700; color: #15803d; }

/* === Waypoint === */
.waypoint-bar {
  margin: 4px 28px; padding: 10px 16px;
  background: #fffbeb; border-radius: 10px;
  font-size: .8em; color: #92400e;
  display: flex; align-items: flex-start; gap: 8px; flex-wrap: wrap;
  border: 1px dashed #fcd34d; line-height: 1.6;
}
.waypoint-bar .wp-icon { font-size: 1.1em; flex-shrink: 0; }
.waypoint-bar .wp-name { font-weight: 700; white-space: nowrap; }
.waypoint-bar .wp-detail { color: #78716c; font-size: .92em; }
.waypoint-bar .wp-tip { color: #0f766e; font-size: .92em; }

/* === Food in Day === */
.food-section-inline { margin: 16px 28px; padding: 18px 20px; background: linear-gradient(135deg, #fef9f0, #fff8f5); border-radius: 12px; }
.food-section-inline h3 { font-size: 1em; font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; gap: 6px; }
.food-grid-inline { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.food-item-mini { background: #fff; border-radius: 10px; padding: 12px; }
.food-item-mini .fm-name { font-weight: 700; font-size: .88em; color: #333; }
.food-item-mini .fm-addr { font-size: .72em; color: #aaa; margin-top: 2px; }
.food-item-mini .fm-sig { font-size: .76em; color: #888; margin-top: 4px; line-height: 1.5; }
.food-item-mini .fm-price { color: #e05a3a; font-weight: 700; font-size: .88em; margin-top: 6px; }
.food-item-mini .fm-note { font-size: .72em; color: #999; margin-top: 4px; line-height: 1.4; }
.fm-label { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: .7em; font-weight: 600; margin-bottom: 4px; }
.fm-label.bf { background: #fff7e6; color: #d46b08; }
.fm-label.lu { background: #e6fffb; color: #08979c; }
.fm-label.dn { background: #f9f0ff; color: #7c3aed; }

/* === Hotel in Day === */
.hotel-rec-section { margin: 16px 28px 20px; padding: 18px 20px; background: linear-gradient(135deg, #f8f9ff, #f0f4ff); border-radius: 12px; }
.hotel-rec-section .hr-title { font-weight: 700; font-size: 1em; margin-bottom: 10px; }
.hotel-rec-section .hr-name { font-weight: 700; font-size: .92em; color: #333; }
.hotel-rec-section .hr-area { font-size: .78em; color: #999; margin-top: 2px; }
.hotel-rec-section .hr-price { font-size: .82em; color: #e05a3a; font-weight: 600; margin-top: 4px; }
.hotel-rec-section .hr-desc { font-size: .8em; color: #666; margin-top: 6px; line-height: 1.6; }

/* === Food Summary === */
.food-section { background: #fff; border-radius: 16px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 12px rgba(0,0,0,.06); }
.food-section h2 { font-size: 1.2em; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.food-city-group { margin-bottom: 18px; }
.food-city-group:last-child { margin-bottom: 0; }
.food-city-title { font-size: .95em; font-weight: 700; color: #555; margin-bottom: 10px; padding-bottom: 6px; border-bottom: 2px solid #f0f0f0; display: flex; align-items: center; gap: 6px; }
.food-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.food-item { background: #fef9f0; border-radius: 12px; padding: 14px; }
.food-item .f-name { font-weight: 700; font-size: .92em; }
.food-item .f-cuisine { font-size: .72em; color: #aaa; margin-top: 2px; }
.food-item .f-dishes { font-size: .78em; color: #888; margin-top: 4px; line-height: 1.5; }
.food-item .f-price { color: #e05a3a; font-weight: 700; font-size: .92em; margin-top: 6px; }
.food-item .f-reason { font-size: .76em; color: #999; margin-top: 4px; line-height: 1.4; }

/* === Avoid List === */
.avoid-section { background: #fff; border-radius: 16px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 12px rgba(0,0,0,.06); }
.avoid-section h2 { font-size: 1.2em; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.avoid-list { display: grid; grid-template-columns: 1fr; gap: 8px; }
.avoid-item { display: flex; gap: 10px; padding: 12px 16px; border-radius: 10px; background: #fff5f5; font-size: .86em; line-height: 1.6; }
.avoid-item .a-num { background: #ff4d4f; color: #fff; min-width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: .75em; font-weight: 700; flex-shrink: 0; }
.avoid-item .a-wrong { color: #ff4d4f; font-weight: 700; text-decoration: line-through; }
.avoid-item .a-right { color: #52c41a; font-weight: 500; }
.avoid-item .a-cat { display: inline-block; font-size: .7em; padding: 1px 8px; border-radius: 4px; margin-left: 6px; font-weight: 500; }
.avoid-item .a-cat.critical { background: #fff1f0; color: #cf1322; }
.avoid-item .a-cat.warning { background: #fffbe6; color: #d48806; }

/* === Budget === */
.budget-card { background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 16px; padding: 24px; margin-bottom: 20px; color: #fff; }
.budget-card h2 { font-size: 1.2em; margin-bottom: 16px; }
.budget-row { display: flex; justify-content: space-between; padding: 8px 0; font-size: .92em; border-bottom: 1px solid rgba(255,255,255,.15); align-items: center; }
.budget-row .br-item { font-weight: 500; }
.budget-row .br-amount { font-weight: 700; font-size: 1.05em; }
.budget-row .br-detail { font-size: .72em; opacity: .75; }
.budget-row-sub { display: flex; justify-content: space-between; padding: 4px 0 4px 16px; font-size: .78em; opacity: .75; }
.budget-total { text-align: center; margin-top: 16px; padding-top: 16px; border-top: 2px solid rgba(255,255,255,.3); font-size: 1.4em; font-weight: 700; }
.budget-total .bt-sub { font-size: .65em; opacity: .75; margin-top: 4px; font-weight: 400; }

/* === Tips === */
.tips-card { background: linear-gradient(135deg, #fff0f5, #fff5f0); border-radius: 16px; padding: 24px; margin-bottom: 20px; }
.tips-card h2 { font-size: 1.2em; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.tips-weather { margin-bottom: 14px; padding: 12px 16px; background: #fff; border-radius: 10px; font-size: .86em; color: #666; line-height: 1.6; }
.tips-weather strong { color: #333; }
.tips-grid { display: grid; grid-template-columns: 1fr; gap: 10px; }
.tip-item { padding: 10px 14px; font-size: .88em; display: flex; gap: 10px; background: #fff; border-radius: 10px; line-height: 1.6; }
.tip-item .tip-num { background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; min-width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: .8em; font-weight: 700; flex-shrink: 0; }
.tip-item .tip-text { color: #555; }

/* === Footer === */
.footer { text-align: center; padding: 30px 0 20px; color: #bbb; font-size: .84em; line-height: 1.8; }
.footer .footer-title { font-size: 1em; font-weight: 500; color: #999; }
.footer .footer-desc { font-size: .8em; color: #ccc; }

/* ============================================================
   Responsive
   ============================================================ */

@media (max-width: 1024px) { .quick-nav { display: none; } }

@media (max-width: 768px) {
  .hero { min-height: 320px; padding: 40px 16px 70px; }
  .hero h1 { font-size: 1.6em; word-break: break-word; }
  .hero .subtitle { font-size: .9em; }
  .hero .emojis { font-size: 2.2em; }
  .hero .tag { font-size: .72em; padding: 4px 10px; }
  .container { padding: 16px 12px 40px; }
  .transport-grid, .food-grid-inline, .food-grid, .hotel-grid { grid-template-columns: 1fr; }
  .day-header { padding: 16px 18px 14px; }
  .day-header .day-num { font-size: 1.3em; }
  .spot { padding: 14px 18px; }
  .spot-icon { width: 40px; height: 40px; min-width: 40px; font-size: 1.2em; border-radius: 10px; }
  .spot-name { font-size: .95em; }
  .spot-transit { font-size: .68em; }
  .route-bar { padding: 8px 18px; font-size: .76em; }
  .hotel-route-bar { padding: 6px 18px; font-size: .74em; }
  .parking-info { font-size: .72em; display: block; }
  .waypoint-bar { margin: 4px 18px; font-size: .74em; }
  .food-section-inline { margin: 12px 18px; padding: 14px 16px; }
  .hotel-rec-section { margin: 12px 18px 16px; padding: 14px 16px; }
}

@media (max-width: 375px) {
  .container { padding: 12px; }
  .hero h1 { font-size: 1.35em; }
  .hero .tag { font-size: .68em; padding: 3px 8px; }
  .hero .tag-row { gap: 6px; }
  .spot-icon { width: 36px; height: 36px; min-width: 36px; font-size: 1.1em; border-radius: 8px; }
}

@media (hover: none) {
  .quick-nav .nav-item { padding: 6px 0; }
  * { -webkit-tap-highlight-color: transparent; }
}

@media print {
  .quick-nav { display: none; }
  .day-card { break-inside: avoid; }
}
</style>
</head>
<body>
''')

# ===== QUICK NAV =====
w('<nav class="quick-nav" id="quickNav">')
nav_items = [f'Day {d["day_number"]}' for d in trip['itinerary']]
nav_items.append('🍜 美食推荐')
nav_items.append('⚠️ 避坑清单 (25条)')
nav_items.append('💰 预算估算')
nav_items.append('💕 出行Tips')
for ni in nav_items:
    w(f'<div class="nav-item" data-target="{ni}"><span class="nav-dot"></span><span class="nav-label">{ni}</span></div>')
w('</nav>')

# ===== HERO =====
w('<section class="hero">')
w('<div class="hero-inner">')
w('<div class="emojis">🏔️🚗🍜🐼🌊</div>')
w(f'<h1>{trip["title"]}</h1>')
w(f'<div class="subtitle">9天自驾之旅 · 成都→九寨沟→川西大环线→成都</div>')
w('<div class="tag-row">')
tags = ['🏔️ 自然风光', '🚗 自驾', '🍜 美食', '🐼 熊猫', '🌊 九寨沟', '🏘️ 藏寨碉楼', '📸 摄影天堂']
for t in tags:
    w(f'<span class="tag">{t}</span>')
w('</div>')
w('</div>')
w('</section>')

w('<div class="container">')

# ===== TRANSPORT CARD =====
w('<div class="transport-card collapsible" data-nav="🚄 交通信息">')
w('<h2>✈️ 往返交通 <span class="collapse-icon">▼</span></h2>')
w('<div class="collapse-content">')
w('<div class="transport-grid">')
for t_item in trip['transport_to_dest']:
    w(f'<div class="t-item">')
    w(f'<div class="t-title">✈️ {t_item["mode"]} · {t_item["from"]} → {t_item["to"]}</div>')
    w(f'<div class="t-detail">⏱️ {t_item["duration"]} · 优选双流机场离市区更近</div>')
    w(f'<div class="t-price">¥{t_item["estimated_price"]} /人</div>')
    w(f'<div class="t-note">{t_item["note"]}</div>')
    w('</div>')
for t_item in trip['transport_return']:
    w(f'<div class="t-item">')
    w(f'<div class="t-title">✈️ {t_item["mode"]} · {t_item["from"]} → {t_item["to"]}</div>')
    w(f'<div class="t-detail">⏱️ {t_item["duration"]} · 优选18:00后起飞</div>')
    w(f'<div class="t-price">¥{t_item["estimated_price"]} /人</div>')
    w(f'<div class="t-note">{t_item["note"]}</div>')
    w('</div>')
w('</div>')
w('</div>')
w('</div>')

# ===== DAY CARDS =====
icon_colors = ['c1', 'c2', 'c3', 'c4']

for day in trip['itinerary']:
    dn = day['day_number']
    dclass, dgradient, dcolor = day_gradients[dn]

    w(f'<div class="day-card" data-nav="Day {dn}">')

    # Day Header
    w(f'<div class="day-header {dclass}" style="background:{dgradient};color:{dcolor};">')
    w(f'<div class="day-num">Day {dn} · {day["theme"]}</div>')
    w(f'<div class="day-route">{day["route_summary"]}</div>')
    w('</div>')

    w('<div class="spots-wrapper">')

    # Hotel→First Spot Route Bar (Day 2+)
    if dn >= 2 and day.get('spots') and day['spots'][0].get('route'):
        prev_day = trip['itinerary'][dn - 2]  # 0-indexed
        prev_hotel = prev_day.get('hotel', {}).get('name', '酒店')
        first_spot = day['spots'][0]
        r = first_spot['route']
        mode_icon = transport_icons.get(r.get('transport_mode', 'driving'), '🚗')
        w(f'<div class="hotel-route-bar">')
        w(f'<span class="hdot"></span>')
        w(f'<span class="hroute-item">🏨 {prev_hotel}</span>')
        w(f'<span>→ {mode_icon} {r.get("distance_text","")} / {r.get("duration_text","")} →</span>')
        w(f'<span class="hroute-item">📍 {first_spot["name"]}</span>')
        w('</div>')

    # Route summary bar (spots chain)
    if day.get('spots'):
        w('<div class="route-bar">')
        w('<span class="dot"></span>')
        for i, spot in enumerate(day['spots']):
            w(f'<span class="r-item">{spot.get("emoji","📍")} {spot["name"]}</span>')
            if i < len(day['spots']) - 1:
                next_spot = day['spots'][i + 1]
                nr = next_spot.get('route', {})
                mode_icon = transport_icons.get(nr.get('transport_mode', 'driving'), '🚗')
                w(f'<span>→ {mode_icon} {nr.get("distance_text","")} / {nr.get("duration_text","")} →</span>')
        w('</div>')

    # Spot Details
    for i, spot in enumerate(day['spots']):
        iclass = icon_colors[i % 4]
        r = spot.get('route', {})

        w(f'<div class="spot">')
        w(f'<div class="spot-head">')
        w(f'<div class="spot-icon {iclass}">{spot.get("emoji","📍")}</div>')
        w('<div style="flex:1;">')

        # Name + price + transit info
        ticket_label = fmt_price(spot.get('ticket_price', 0))
        w(f'<div class="spot-name">{spot["name"]}')
        w(f'<span class="spot-price">{ticket_label}</span>')

        # Transit from previous spot (or origin)
        if r:
            mode_label = transport_labels.get(r.get('transport_mode', 'driving'), '自驾')
            mode_icon = transport_icons.get(r.get('transport_mode', 'driving'), '🚗')
            from_name = r.get('from_name', '出发点')
            w(f'<span class="spot-transit">')
            w(f'{mode_icon} 从 {from_name} · {mode_label} · {r.get("distance_text","")} / {r.get("duration_text","")}')
            w(f'</span>')
        w('</div>')

        w(f'<div class="spot-desc">{spot.get("description","")}</div>')
        w('</div>')
        w('</div>')

        # Parking info
        parking = spot.get('parking')
        if parking:
            w(f'<div class="parking-info">')
            w(f'🅿️ {parking.get("name","")} · {parking.get("distance_text","")} · ')
            w(f'<span class="pk-price">{parking.get("price_text","")}</span>')
            if parking.get('tips'):
                w(f' · 💡 {parking["tips"]}')
            w('</div>')

        # Waypoints
        waypoints = r.get('waypoints', [])
        if waypoints:
            for wp in waypoints:
                w(f'<div class="waypoint-bar">')
                w(f'<span class="wp-icon">🛣️</span>')
                w(f'<span class="wp-name">{wp.get("name","")}</span>')
                w(f'<span class="wp-detail">（约{wp.get("at_distance_km","")}km处）· {wp.get("facilities","")}</span>')
                if wp.get('tips'):
                    w(f'<br><span class="wp-tip">💡 {wp["tips"]}</span>')
                w('</div>')

        # Romantic moment
        if spot.get('romantic_moment'):
            w(f'<div class="spot-romance">💕 浪漫时刻：{spot["romantic_moment"]}</div>')

        # Photo tip
        if spot.get('photo_tip'):
            w(f'<div class="spot-photo">📸 拍照建议：{spot["photo_tip"]}</div>')

        # Pitfall warning
        if spot.get('pitfall_warning'):
            w(f'<div class="spot-avoid">⚠️ 避坑：{spot["pitfall_warning"]}</div>')

        w('</div>')  # close .spot

    # Meals
    meals = day.get('meals', {})
    if meals.get('breakfast') or meals.get('lunch') or meals.get('dinner'):
        w('<div class="food-section-inline">')
        w('<h3>🍽️ 当日餐饮推荐</h3>')
        w('<div class="food-grid-inline">')

        for meal_type, meal_list, meal_icon, meal_label in [
            ('breakfast', meals.get('breakfast', []), '🌅', '早餐'),
            ('lunch', meals.get('lunch', []), '☀️', '午餐'),
            ('dinner', meals.get('dinner', []), '🌙', '晚餐'),
        ]:
            for m in meal_list:
                ml_class = {'breakfast': 'bf', 'lunch': 'lu', 'dinner': 'dn'}.get(meal_type, '')
                w(f'<div class="food-item-mini">')
                w(f'<span class="fm-label {ml_class}">{meal_icon} {meal_label}</span>')
                w(f'<div class="fm-name">{m["name"]}</div>')
                if m.get('address'):
                    w(f'<div class="fm-addr">📍 {m["address"]}</div>')
                if m.get('signature'):
                    sigs = '、'.join(m['signature'][:5])
                    w(f'<div class="fm-sig">🔥 招牌：{sigs}</div>')
                w(f'<div class="fm-price">人均 ¥{m["price_per_person"]}</div>')
                if m.get('note'):
                    w(f'<div class="fm-note">💡 {m["note"]}</div>')
                w('</div>')
        w('</div>')
        w('</div>')

    # Hotel
    hotel = day.get('hotel')
    if hotel:
        w('<div class="hotel-rec-section">')
        w('<div class="hr-title">🏨 推荐酒店住宿地</div>')
        w(f'<div class="hr-name">{hotel["name"]}</div>')
        w(f'<div class="hr-area">📍 {hotel.get("area","")}</div>')
        w(f'<div class="hr-price">💰 {hotel.get("price_range","")}</div>')
        w(f'<div class="hr-desc">{hotel.get("highlights","")}</div>')
        w('</div>')

    w('</div>')  # close .spots-wrapper
    w('</div>')  # close .day-card

# ===== FOOD SUMMARY =====
w('<div class="food-section collapsible" data-nav="🍜 美食推荐">')
w('<h2>🍜 美食推荐汇总（11家） <span class="collapse-icon">▼</span></h2>')
w('<div class="collapse-content">')

# Group by city
food_by_city = {}
for f in trip['food_summary']:
    addr = f.get('address', '')
    if '都江堰' in addr:
        city = '都江堰'
    elif '九寨沟' in addr:
        city = '九寨沟口'
    else:
        city = '成都'
    food_by_city.setdefault(city, []).append(f)

# Add 茂县简餐 as the 11th restaurant
food_by_city.setdefault('茂县（川西路途）', []).append({
    'name': '茂县简餐（川菜/羌族简餐）',
    'cuisine': '川菜·羌族简餐',
    'price_per_person': 35,
    'recommended_dishes': ['川味盖饭', '牦牛肉面', '羌族土豆糍粑'],
    'reason': 'D6全程唯一理想的午餐补给站。茂县是羌族聚居县城，有川菜馆和简餐店。吃完可补充零食和水，下午翻巴朗山。',
    'address': '茂县县城',
})

city_icons = {'成都': '🐼', '都江堰': '🏯', '九寨沟口': '🏔️', '茂县（川西路途）': '🚗'}
for city in ['成都', '都江堰', '九寨沟口', '茂县（川西路途）']:
    items = food_by_city.get(city, [])
    if not items:
        continue
    ci = city_icons.get(city, '🍜')
    w(f'<div class="food-city-group">')
    w(f'<div class="food-city-title">{ci} {city}（{len(items)}家）</div>')
    w('<div class="food-grid">')
    for f in items:
        dishes = '、'.join(f.get('recommended_dishes', [])[:4])
        w(f'<div class="food-item">')
        w(f'<div class="f-name">🍽️ {f["name"]}</div>')
        w(f'<div class="f-cuisine">{f.get("cuisine","")}</div>')
        if dishes:
            w(f'<div class="f-dishes">🔥 推荐：{dishes}</div>')
        w(f'<div class="f-price">人均 ¥{f["price_per_person"]}</div>')
        if f.get('reason'):
            w(f'<div class="f-reason">💡 {f["reason"]}</div>')
        w('</div>')
    w('</div>')
    w('</div>')

w('</div>')
w('</div>')

# ===== AVOID LIST =====
avoid_list = list(trip['avoid_list'])

w('<div class="avoid-section collapsible" data-nav="⚠️ 避坑清单 (25条)">')
w('<h2>⚠️ 避坑清单 <span style="font-size:.7em;color:#999;">25条 · 避一个坑省1000元</span> <span class="collapse-icon">▼</span></h2>')
w('<div class="collapse-content">')
w('<div class="avoid-list">')
for idx, a in enumerate(avoid_list, 1):
    cat_class = 'critical' if a.get('severity') == 'critical' else 'warning'
    cat_label = '🔴 严重' if a.get('severity') == 'critical' else '🟡 注意'
    w(f'<div class="avoid-item">')
    w(f'<div class="a-num">{idx}</div>')
    w('<div style="flex:1;">')
    w(f'<span class="a-wrong">❌ {a["wrong"]}</span> <span class="a-cat {cat_class}">{cat_label}</span>')
    w(f'<br><span class="a-right">✅ {a["correct"]}</span>')
    w('</div>')
    w('</div>')
w('</div>')
w('</div>')
w('</div>')

# ===== BUDGET =====
w('<div class="budget-card" data-nav="💰 预算估算">')
w(f'<h2>💰 预算估算（{trip["persons"]}人）</h2>')

b = trip['budget']
budget_rows = [
    ('✈️ 往返机票', b['flight']['total'], f'去程+回程 · ¥{b["flight"]["per_person"]}/人', b['flight'].get('detail', '')),
    ('🚄 高铁/城际列车', b['train']['total'], f'犀浦↔离堆公园 + 成都东→黄龙九寨 · ¥{b["train"]["per_person"]}/人', b['train'].get('detail', '')),
    ('🚌 景区直通车', b['bus']['total'], f'黄龙九寨站→九寨沟口 · ¥{b["bus"]["per_person"]}/人', b['bus'].get('detail', '')),
    ('🚗 租车+油费+过路费', b['car_rental']['total'], f'3天（D6-D8）SUV · ¥{b["car_rental"]["per_person"]}/人', b['car_rental'].get('note', '')),
    ('🏨 酒店住宿（8晚）', b['hotel']['total'], f'成都3晚+九寨沟2晚+四姑娘山1晚+新都桥1晚+成都1晚 · ¥{b["hotel"]["per_person"]}/人', b['hotel'].get('detail', '')),
    ('🎫 景区门票', b['tickets']['total'], f'¥{b["tickets"]["per_person"]}/人', b['tickets'].get('detail', '')),
    ('🍜 餐饮美食', b['food']['total'], f'9天×2人 · ¥{b["food"]["per_person"]}/人', b['food'].get('detail', '')),
]

for label, amount, per_info, detail in budget_rows:
    w(f'<div class="budget-row">')
    w(f'<span class="br-item">{label}</span>')
    w(f'<span class="br-amount">¥{amount}</span>')
    w('</div>')
    w(f'<div class="budget-row-sub"><span>{per_info}</span><span></span></div>')

tot = b['total']
per = tot.get('per_person', '') if isinstance(tot, dict) else b['total'].get('per_person', '')
tot_range = tot.get('range', tot) if isinstance(tot, dict) else tot

w(f'<div class="budget-total">')
w(f'总计 ¥{b["total"]["range"]}')
w(f'<div class="bt-sub">人均 ¥{b["total"]["per_person"]}（不含购物和个人消费）</div>')
w(f'</div>')
if b['total'].get('note'):
    w(f'<div style="margin-top:10px; font-size:.76em; opacity:.7; text-align:center; line-height:1.5;">💡 {b["total"]["note"]}</div>')
w('</div>')

# ===== TIPS =====
w('<div class="tips-card" data-nav="💕 出行Tips">')
w('<h2>💕 出行Tips（15条）</h2>')

weather = trip.get('weather', {})
if weather:
    w('<div class="tips-weather">')
    w(f'🌤️ <strong>天气参考：</strong>{weather.get("season","")} · {weather.get("temp_range","")}<br>')
    w(f'👔 <strong>穿衣建议：</strong>{weather.get("clothing","")}<br>')
    w(f'⚠️ <strong>注意事项：</strong>{weather.get("precautions","")}')
    w('</div>')

w('<div class="tips-grid">')
for idx, tip in enumerate(trip['tips'], 1):
    w(f'<div class="tip-item">')
    w(f'<div class="tip-num">{idx}</div>')
    w(f'<div class="tip-text">{tip}</div>')
    w('</div>')
w('</div>')
w('</div>')

# ===== FOOTER =====
w('<div class="footer">')
w(f'<div class="footer-title">{trip["title"]}</div>')
w(f'<div class="footer-desc">9天 · 成都→九寨沟→四姑娘山→新都桥→康定→成都 · 自驾约800公里</div>')
w(f'<div class="footer-desc">数据来源：WebSearch + 本地知识库 · 生成时间：{trip.get("metadata",{}).get("generated_at","2026-06-29")}</div>')
w(f'<div class="footer-desc" style="margin-top:8px;">🏔️ 愿你走遍川西山河，归来仍是少年 🏔️</div>')
w('</div>')

w('</div>')  # close .container

# ===== SCRIPTS =====
w('''
<script>
// === Quick Nav: Generate and scroll-spy ===
(function() {
  var nav = document.getElementById('quickNav');
  if (!nav) return;

  // Map of nav items -> DOM sections
  var navItems = nav.querySelectorAll('.nav-item');
  var sections = [];

  navItems.forEach(function(item) {
    var target = item.getAttribute('data-target');
    // Find corresponding section
    var section = document.querySelector('[data-nav="' + target + '"]');
    if (section) {
      sections.push({ el: section, navItem: item, label: target });
    }
  });

  // Scroll spy
  var ticking = false;
  window.addEventListener('scroll', function() {
    if (!ticking) {
      window.requestAnimationFrame(function() {
        var current = '';
        sections.forEach(function(s) {
          if (window.scrollY >= s.el.offsetTop - 120) {
            current = s.label;
          }
        });
        navItems.forEach(function(item) {
          var label = item.getAttribute('data-target');
          if (label === current) {
            item.classList.add('active');
          } else {
            item.classList.remove('active');
          }
        });
        ticking = false;
      });
      ticking = true;
    }
  });

  // Click to scroll
  navItems.forEach(function(item) {
    item.addEventListener('click', function() {
      var target = item.getAttribute('data-target');
      var section = document.querySelector('[data-nav="' + target + '"]');
      if (section) {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
})();

// === Day Card Collapse ===
document.querySelectorAll('.day-card .day-header').forEach(function(header) {
  header.addEventListener('click', function() {
    header.parentElement.classList.toggle('collapsed');
  });
});

// === Section Collapse ===
document.querySelectorAll('.collapsible').forEach(function(el) {
  el.addEventListener('click', function() {
    el.classList.toggle('collapsed');
    var content = el.querySelector('.collapse-content');
    if (content) {
      content.classList.toggle('collapsed');
    }
  });
});

// === Initial state: first day open, others collapsed ===
// (keep all open by default for better first impression)
</script>
</body>
</html>
''')

# ===== WRITE FILE =====
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(html))

print(f'Generated: {output_path}')
print(f'Size: {os.path.getsize(output_path)} bytes')
print(f'Days: {len(trip["itinerary"])}')
print(f'Food items: {len(trip["food_summary"])}')
print(f'Avoid items: {len(avoid_list)}')
print(f'Tips: {len(trip["tips"])}')
print('Done!')
