#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate output.html from trip.json for trip 57cec94c."""

import json
import os

TRIP_DIR = os.path.dirname(os.path.abspath(__file__))
TRIP_FILE = os.path.join(TRIP_DIR, 'trip.json')
OUTPUT_FILE = os.path.join(TRIP_DIR, 'output.html')

# Day header gradients (9 kinds)
GRADIENTS = {
    1: ('d1', '#f6a085', '#f2719c', '#fff'),
    2: ('d2', '#4facfe', '#00f2fe', '#fff'),
    3: ('d3', '#a18cd1', '#fbc2eb', '#fff'),
    4: ('d4', '#fddb92', '#d1fdff', '#666'),
    5: ('d5', '#43e97b', '#38f9d7', '#fff'),
    6: ('d6', '#f7971e', '#ffd200', '#666'),
    7: ('d7', '#0c3483', '#6b8cce', '#fff'),
    8: ('d8', '#8e2de2', '#4a00e0', '#fff'),
    9: ('d9', '#00b4db', '#0083b0', '#fff'),
}

SPOT_EMOJIS = {
    '春熙路步行街': '🌃',
    '成都大熊猫繁育研究基地': '🐼',
    '人民公园鹤鸣茶社': '🍵',
    '太古里': '🏬',
    '都江堰景区': '🏛️',
    '灌县古城': '🏘️',
    '漳扎镇高原漫步': '🏔️',
    '五花海': '🎨',
    '珍珠滩瀑布': '💦',
    '诺日朗瀑布': '🌊',
    '长海': '🏔️',
    '五彩池': '🌈',
    '树正群海': '🌳',
    '九若路(S445)': '🛣️',
    '若尔盖野湖': '💧',
    '黄河九曲第一湾': '🌅',
    '甘加草原': '🌿',
    '癿石秘境(白石崖)': '⛰️',
    '隆务峡谷（途经）': '🏔️',
    '沙索麻村观景台（坎布拉免费版）': '🏞️',
    '青海湖（环湖西路牧民小道）': '💎',
}

TRANSPORT_LABELS = {
    'walking': '步行',
    'taxi': '打车',
    'transit': '公共交通',
    'driving': '自驾',
}

TRANSPORT_EMOJIS = {
    'walking': '🚶',
    'taxi': '🚗',
    'transit': '🚇🚄🚌',
    'driving': '🚗',
}

MEAL_EMOJIS = {
    'breakfast': '🌅',
    'lunch': '☀️',
    'dinner': '🌙',
}

MEAL_LABELS = {
    'breakfast': '早餐',
    'lunch': '午餐',
    'dinner': '晚餐',
}

def get_spot_emoji(name):
    for k, v in SPOT_EMOJIS.items():
        if k in name:
            return v
    return '📍'

def ticket_label(price):
    if price == 0:
        return '免费'
    return f'¥{price}'

def nav_data(itinerary):
    """Generate data-nav entries for right quick nav."""
    items = []
    for day in itinerary:
        items.append(f'Day {day["day_number"]}')
    items.append('🍜 美食推荐')
    items.append('⚠️ 避坑清单(18条)')
    items.append('💰 预算估算')
    items.append('💡 出行Tips')
    return items

def gen_hero(trip):
    """Generate hero section."""
    title = trip['title']
    subtitle = '9天自然风光之旅'
    tags = [
        '🏔️ 自然风光',
        '🚗 秘境公路',
        '🍜 美食老店',
        '🌊 青海湖',
        '👫 2人出行',
    ]
    tag_html = '\\n'.join(f'          <span class=\"tag\">{t}</span>' for t in tags)

    return f'''  <!-- ===== HERO ===== -->
  <section class=\"hero\">
    <div class=\"hero-inner\">
      <div class=\"emojis\">🏔️🚗🍜🌊</div>
      <h1>{title}</h1>
      <div class=\"subtitle\">{subtitle}</div>
      <div class=\"tag-row\">
{tag_html}
      </div>
    </div>
  </section>'''


def gen_transport(trip):
    """Generate transport cards (arrival + departure)."""
    to_items = []
    for t in trip.get('transport_to_dest', []):
        to_items.append(f'''        <div class=\"t-item\">
          <div class=\"t-title\">✈️ 航班 · {t['from']} → {t['to']}</div>
          <div class=\"t-detail\">飞行约{t['duration']} · {t.get('note', '')}</div>
          <div class=\"t-price\">¥{t['estimated_price']}/人</div>
        </div>''')

    for t in trip.get('transport_from_dest', []):
        to_items.append(f'''        <div class=\"t-item\">
          <div class=\"t-title\">✈️ 返程 · {t['from']} → {t['to']}</div>
          <div class=\"t-detail\">飞行约{t['duration']} · {t.get('note', '')}</div>
          <div class=\"t-price\">¥{t['estimated_price']}/人</div>
        </div>''')

    items_html = '\\n'.join(to_items)

    return f'''  <!-- ===== TRANSPORT CARD ===== -->
  <div class=\"transport-card collapsible\" data-nav=\"✈️ 交通信息\">
    <h2>✈️ 交通信息 <span class=\"collapse-icon\">▼</span></h2>
    <div class=\"collapse-content\">
      <div class=\"transport-grid\">
{items_html}
      </div>
    </div>
  </div>'''


def gen_day_card(day, is_first=False):
    """Generate a single day card."""
    dn = day['day_number']
    grad_class, grad_start, grad_end, text_color = GRADIENTS[dn]

    theme = day['theme']
    route_summary = day['route_summary']

    # Build hotel-route-bar (for Day 2+)
    hotel_bar_html = ''
    if not is_first and day.get('spots') and day['spots'][0].get('route'):
        r = day['spots'][0]['route']
        hotel_name = r.get('from_name', '酒店')
        first_spot_name = day['spots'][0]['name']
        emoji = r.get('emoji', '🚗')
        dist = r.get('distance_text', '')
        dur = r.get('duration_text', '')
        hotel_bar_html = f'''    <div class=\"hotel-route-bar\">
      <span class=\"hdot\"></span>
      <span class=\"hroute-item\">🏨 {hotel_name}</span>
      <span>→ {emoji} {dist}/{dur} →</span>
      <span class=\"hroute-item\">📍 {first_spot_name}</span>
    </div>
'''

    # Build spot-to-spot route bar
    spots = day['spots']
    route_parts = []
    for i, spot in enumerate(spots):
        sname = spot['name']
        semoji = get_spot_emoji(sname)
        route_parts.append(f'<span class=\"r-item\">{semoji} {sname}</span>')
        if i < len(spots) - 1:
            next_route = spots[i + 1].get('route', {})
            emoji = next_route.get('emoji', '→')
            dist = next_route.get('distance_text', '')
            dur = next_route.get('duration_text', '')
            route_parts.append(f'<span>→ {emoji} {dist}/{dur} →</span>')

    route_bar_html = f'''    <div class=\"route-bar\">
      <span class=\"dot\"></span>
      {' '.join(route_parts)}
    </div>
'''

    # Build spot details
    spot_html_parts = []
    for i, spot in enumerate(spots):
        emoji = get_spot_emoji(spot['name'])
        price = spot.get('ticket_price', 0)
        price_text = ticket_label(price)
        price_class = 'spot-price free' if price == 0 else 'spot-price'
        desc = spot.get('description', '')
        romantic = spot.get('romantic_moment', '')

        # Transit from previous
        transit_html = ''
        if i > 0:
            prev_route = spot.get('route', {})
            from_name = prev_route.get('from_name', '')
            mode = prev_route.get('transport_mode', '')
            mode_label = TRANSPORT_LABELS.get(mode, mode)
            dist = prev_route.get('distance_text', '')
            dur = prev_route.get('duration_text', '')
            t_emoji = prev_route.get('emoji', '🚗')
            transit_html = f'''
            <span class=\"spot-transit\">
              <span class=\"transit-icon\">{t_emoji}</span>
              从 {from_name} · {mode_label}
              <span class=\"transit-time\">{dist}/{dur}</span>
            </span>'''

        # Waypoints for this spot's route
        waypoints_html = ''
        route = spot.get('route', {})
        if route.get('waypoints'):
            for wp in route['waypoints']:
                wp_type_label = {'rest_stop': '休息站', 'viewpoint': '观景点', 'scenic': '景观段'}.get(wp.get('type', ''), '途经点')
                wp_tips = wp.get('tips', '')
                wp_fac = wp.get('facilities', '')
                waypoints_html += f'''
    <div class=\"waypoint-bar\">
      🛣️ {wp['name']}（约{wp['at_distance_km']}km处）· <span class=\"wp-facilities\">{wp_type_label}：{wp_fac}</span>
      {'· 💡 ' + wp_tips if wp_tips else ''}
    </div>'''

        romantic_html = ''
        if romantic:
            romantic_html = f'''
      <div class=\"spot-romance\">💕 浪漫时刻：{romantic}</div>'''

        spot_html_parts.append(f'''    <div class=\"spot\">
      <div class=\"spot-head\">
        <div class=\"spot-icon\">{emoji}</div>
        <div>
          <div class=\"spot-name\">
            {spot['name']}
            <span class=\"{price_class}\">{price_text}</span>{transit_html}
          </div>
          <div class=\"spot-desc\">{desc}</div>
        </div>
      </div>{romantic_html}
    </div>''')
        if waypoints_html:
            spot_html_parts.append(waypoints_html.rstrip())

    spots_all_html = '\\n'.join(spot_html_parts)

    # Meals section
    meals_html = ''
    meals = day.get('meals', {})
    meal_items = []
    for meal_type in ['breakfast', 'lunch', 'dinner']:
        for m in meals.get(meal_type, []):
            sig = '、'.join(m.get('signature', [])[:4])
            note = m.get('note', '')
            meal_items.append(f'''        <div class=\"food-item\">
          <div class=\"f-name\">{MEAL_EMOJIS[meal_type]} {MEAL_LABELS[meal_type]}</div>
          <div class=\"f-shop\">{m['name']}{' · ' + m.get('address', '') if m.get('address') else ''}</div>
          <div class=\"f-price\">人均 ¥{m['price_per_person']}</div>
          <div class=\"f-note\">推荐：{sig}{' · ' + note if note else ''}</div>
        </div>''')

    if meal_items:
        meals_html = f'''    <div class=\"food-section-inline\">
      <h2>🍽️ 餐饮推荐</h2>
      <div class=\"food-grid\">
{chr(10).join(meal_items)}
      </div>
    </div>'''

    # Hotel section
    hotel_html = ''
    hotel = day.get('hotel')
    if hotel:
        area = hotel.get('area', '')
        price = hotel.get('price_range', '')
        highlights = hotel.get('highlights', '')
        hotel_html = f'''    <div class=\"hotel-rec-section\">
      <div class=\"hr-title\">🏨 推荐住宿</div>
      <div class=\"hr-grid\">
        <div class=\"hr-item\">
          <div class=\"hr-name\">{hotel['name']}</div>
          <div class=\"hr-area\">{area}</div>
          <div class=\"hr-price\">💰 {price}</div>
          <div class=\"hr-desc\">{highlights}</div>
        </div>
      </div>
    </div>'''

    return f'''  <!-- ===== DAY {dn} ===== -->
  <div class=\"day-card\" data-nav=\"Day {dn}\">
    <div class=\"day-header d{dn}\">
      <div class=\"day-num\">Day {dn} · {theme}</div>
      <div class=\"day-route\">{route_summary}</div>
    </div>
    <div class=\"spots-wrapper\">
{hotel_bar_html}{route_bar_html}{spots_all_html}{meals_html}{hotel_html}
    </div>
  </div>'''


def gen_food_summary(trip):
    """Generate food summary grouped by city."""
    # Collect all restaurants by city
    city_foods = {}
    for day in trip['itinerary']:
        city = _infer_city(day)
        meals = day.get('meals', {})
        for meal_type in ['breakfast', 'lunch', 'dinner']:
            for m in meals.get(meal_type, []):
                if m['name'] not in city_foods:
                    city_foods[m['name']] = (city, m)

    # Group by city
    city_order = ['成都', '都江堰', '九寨沟', '若尔盖/唐克', '甘南/夏河', '尖扎', '西宁']
    grouped = {}
    for name, (city, m) in city_foods.items():
        if city not in grouped:
            grouped[city] = []
        grouped[city].append((name, m))

    # Filter out convenience store meals
    skip_keywords = ['酒店早餐', '客栈', '自带干粮', '高铁上', '简餐', '沿途', '便利店', '超市', '藏式早餐', '民宿藏式早餐', '客栈藏式早餐', '合作/碌曲', '湖边藏家乐']
    filtered = {}
    for city, items in grouped.items():
        kept = [(n, m) for n, m in items if not any(kw in n for kw in skip_keywords)]
        if kept:
            filtered[city] = kept

    sections = []
    for city in city_order:
        if city in filtered:
            items_html = []
            for name, m in filtered[city]:
                sig = '、'.join(m.get('signature', [])[:4])
                note = m.get('note', '')
                items_html.append(f'''        <div class=\"food-item\">
          <div class=\"f-name\">🍜 {name}</div>
          <div class=\"f-shop\">{m.get('address', '')}</div>
          <div class=\"f-price\">人均 ¥{m['price_per_person']}</div>
          <div class=\"f-note\">招牌：{sig}{' · ' + note if note else ''}</div>
        </div>''')
            sections.append(f'''    <div class=\"food-city\">
      <h3>📍 {city}</h3>
      <div class=\"food-grid\">
{chr(10).join(items_html)}
      </div>
    </div>''')

    return f'''  <!-- ===== FOOD SUMMARY ===== -->
  <div class=\"food-section collapsible\" data-nav=\"🍜 美食推荐\">
    <h2>🍜 美食推荐汇总 <span class=\"collapse-icon\">▼</span></h2>
    <div class=\"collapse-content\">
{chr(10).join(sections)}
    </div>
  </div>'''


def _infer_city(day):
    """Infer city from day context."""
    dn = day['day_number']
    if dn <= 3:
        return '成都'
    if dn == 4 or dn == 5:
        return '九寨沟'
    if dn == 6:
        return '若尔盖/唐克'
    if dn == 7:
        return '甘南/夏河'
    if dn == 8:
        return '尖扎'
    if dn == 9:
        return '西宁'
    return '其他'

# Also add D3 meals in 都江堰 and D8/D9
def _infer_city_detailed(day):
    dn = day['day_number']
    theme = day.get('theme', '')
    if '都江堰' in theme:
        return '都江堰'
    if dn <= 2:
        return '成都'
    if dn in (4, 5):
        return '九寨沟'
    if dn == 6:
        return '若尔盖/唐克'
    if dn == 7:
        return '甘南/夏河'
    if '尖扎' in theme or dn == 8:
        # D8 has lunch at 尖扎
        pass
    if dn == 8:
        return '尖扎→西宁'
    if dn == 9:
        return '西宁'
    return '其他'


def gen_food_summary_v2(trip):
    """Better food summary with correct city grouping."""
    # Manually curated list
    all_restaurants = []

    for day in trip['itinerary']:
        dn = day['day_number']
        meals = day.get('meals', {})
        for meal_type in ['breakfast', 'lunch', 'dinner']:
            for m in meals.get(meal_type, []):
                # Skip convenience meals
                name = m['name']
                skip_kw = ['酒店早餐', '客栈', '自带干粮', '高铁上', '简餐', '沿途', '便利店', '超市', '藏式早餐', '民宿藏式早餐', '客栈藏式早餐', '合作/碌曲', '湖边藏家乐', '夏河街边', '面馆']
                if any(kw in name for kw in skip_kw):
                    continue
                # Skip duplicates
                if any(r['name'] == name for r in all_restaurants):
                    continue

                city = '成都'
                if dn == 3 and ('都江堰' in m.get('address', '') or '都江堰' in m.get('note', '')):
                    city = '都江堰'
                elif dn in (4, 5):
                    city = '九寨沟'
                elif dn == 6:
                    city = '若尔盖/唐克'
                elif dn == 7:
                    city = '甘南/夏河'
                elif dn == 8:
                    if '尖扎' in m.get('address', '') or '尖扎' in m.get('note', ''):
                        city = '尖扎'
                    elif '西宁' in m.get('address', '') or '西宁' in m.get('note', ''):
                        city = '西宁'
                    elif '同仁' in m.get('address', '') or '夏河' in m.get('address', ''):
                        city = '甘南/夏河'
                    else:
                        city = '西宁'
                elif dn == 9:
                    city = '西宁'

                all_restaurants.append({
                    'name': name,
                    'city': city,
                    'address': m.get('address', ''),
                    'price': m['price_per_person'],
                    'signature': m.get('signature', []),
                    'note': m.get('note', ''),
                    'source': m.get('source', ''),
                })

    # Also add 三哥田螺 (D3 dinner), 明园饭店 (D2 dinner)
    # Group by city
    city_order = ['成都', '都江堰', '九寨沟', '若尔盖/唐克', '甘南/夏河', '尖扎', '西宁']
    grouped = {}
    for r in all_restaurants:
        c = r['city']
        if c not in grouped:
            grouped[c] = []
        grouped[c].append(r)

    # Output in city order
    sections = []
    for city in city_order:
        if city in grouped and grouped[city]:
            items_html = []
            for r in grouped[city]:
                sig = '、'.join(r['signature'][:4])
                note = r['note']
                items_html.append(f'''        <div class=\"food-item\">
          <div class=\"f-name\">🍜 {r['name']}</div>
          <div class=\"f-shop\">{r['address']}</div>
          <div class=\"f-price\">人均 ¥{r['price']}</div>
          <div class=\"f-note\">招牌：{sig}{' · ' + note if note else ''}</div>
        </div>''')
            sections.append(f'''    <div class=\"food-city\">
      <h3>📍 {city}</h3>
      <div class=\"food-grid\">
{chr(10).join(items_html)}
      </div>
    </div>''')

    return f'''  <!-- ===== FOOD SUMMARY ===== -->
  <div class=\"food-section collapsible\" data-nav=\"🍜 美食推荐\">
    <h2>🍜 美食推荐汇总 <span class=\"collapse-icon\">▼</span></h2>
    <div class=\"collapse-content\">
{chr(10).join(sections)}
    </div>
  </div>'''


def gen_avoid_list(trip):
    """Generate 18-item avoid list."""
    items = []
    for i, a in enumerate(trip['avoid_list'], 1):
        items.append(f'''      <div class=\"avoid-item\">
        <div class=\"a-num\">{i}</div>
        <div style=\"flex:1;\">
          <span class=\"a-wrong\">❌ {a['error']}</span><br>
          <span class=\"a-right\">✅ {a['correct']}</span>
        </div>
      </div>''')

    return f'''  <!-- ===== AVOID LIST ===== -->
  <div class=\"avoid-section collapsible\" data-nav=\"⚠️ 避坑清单(18条)\">
    <h2>⚠️ 避坑清单 <span class=\"avoid-count\">共18条</span> <span class=\"collapse-icon\">▼</span></h2>
    <div class=\"collapse-content\">
      <div class=\"avoid-list\">
{chr(10).join(items)}
      </div>
    </div>
  </div>'''


def gen_budget(trip):
    """Generate budget card."""
    b = trip['budget']
    persons = trip.get('persons', 2)

    rows = []
    # Flight
    rows.append(f'''    <div class=\"budget-row\"><span>✈️ 往返机票</span><span>¥{b['flight']['total']}</span></div>''')
    # Train
    rows.append(f'''    <div class=\"budget-row\"><span>🚄 高铁/城际</span><span>¥{b['train']['total']}</span></div>''')
    # Bus
    rows.append(f'''    <div class=\"budget-row\"><span>🚌 景区直通车</span><span>¥{b['bus']['total']}</span></div>''')
    # Car rental
    rows.append(f'''    <div class=\"budget-row\"><span>🚗 租车自驾(D6-D9)</span><span>¥{b['car_rental']['total']}</span></div>''')
    # Hotel
    rows.append(f'''    <div class=\"budget-row\"><span>🏨 住宿(8晚)</span><span>¥{b['hotel']['total']}</span></div>''')
    # Tickets
    rows.append(f'''    <div class=\"budget-row\"><span>🎫 门票(已节省¥1170)</span><span>¥{b['tickets']['total']}</span></div>''')
    # Food
    rows.append(f'''    <div class=\"budget-row\"><span>🍜 餐饮</span><span>¥{b['food']['total']}</span></div>''')

    total_range = b['total']['range']
    per_person = b['total']['per_person']
    total_note = b['total'].get('note', '')

    # Details
    detail_items = []
    for key in ['flight', 'train', 'bus', 'car_rental', 'hotel', 'tickets', 'food']:
        if key in b:
            detail_text = b[key].get('detail') or b[key].get('note') or key
            detail_items.append(f'''      <div style=\"display:flex;justify-content:space-between;padding:2px 0;\"><span>{detail_text}</span><span>¥{b[key]['total']}</span></div>''')

    # Savings highlight
    savings = '''    <div class=\"budget-saving\">🎉 门票节省 ¥1,170：取消花湖(¥110)、尕海湖(¥50)、甘加秘境(¥80)、坎布拉(¥50)、二郎剑(¥90)，替换为免费或低价替代景点。</div>
'''

    return f'''  <!-- ===== BUDGET ===== -->
  <div class=\"budget-card\" data-nav=\"💰 预算估算\">
    <h2>💰 预算估算（{persons}人）</h2>
{chr(10).join(rows)}
    <div class=\"budget-total\">总计 ¥{total_range} · 人均 ¥{per_person}</div>
    <div style=\"margin-top:12px; font-size:.8em; opacity:.85;\">
{chr(10).join(detail_items)}
    </div>
{savings}
    <div style=\"margin-top:8px; font-size:.75em; opacity:.7;\">{total_note}</div>
  </div>'''


def gen_tips(trip):
    """Generate tips section."""
    items = []
    for t in trip['tips']:
        items.append(f'    <div class=\"tip-item\">💡 {t}</div>')

    return f'''  <!-- ===== TIPS ===== -->
  <div class=\"tips-card\" data-nav=\"💡 出行Tips\">
    <h2>💡 出行Tips（{len(trip['tips'])}条实用建议）</h2>
{chr(10).join(items)}
  </div>'''


def gen_footer(trip):
    """Generate footer."""
    meta = trip.get('metadata', {})
    gen_at = meta.get('generated_at', '')
    version = meta.get('version', '')
    sources = '、'.join(meta.get('sources', ['websearch']))
    amap = meta.get('amap_used', False)

    return f'''  <!-- ===== FOOTER ===== -->
  <footer class=\"footer\">
    <p>由 <strong>tourAI v{version}</strong> 生成 · {gen_at}</p>
    <p>数据来源：{sources}</p>
    <p style=\"margin-top:8px; font-size:.75em; color:#ccc;\">
      信息仅供参考，出行前请核实最新价格和开放时间
    </p>
  </footer>'''


def gen_css():
    """Generate the complete CSS with all 9 day gradients."""
    return '''/* ============================================================
   tourAI Design System — Self-contained Stylesheet
   ============================================================ */

/* === Import === */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

/* === Reset === */
* { margin:0; padding:0; box-sizing:border-box; }

:root {
  --primary: #667eea;
  --primary-dark: #764ba2;
  --accent: #f2719c;
  --warn: #faad14;
  --success: #52c41a;
  --danger: #ff4d4f;
  --bg: #f5f5f5;
  --card-bg: #ffffff;
  --text: #333333;
  --text-secondary: #666666;
  --text-muted: #888888;
}

body {
  font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.7;
  overflow-x: hidden;
  position: relative;
}

/* === Quick Navigation (right side, PC only) === */
.quick-nav {
  position: fixed; right: 16px; top: 50%;
  transform: translateY(-50%); z-index: 100;
  display: flex; flex-direction: column; gap: 6px;
  opacity: 0.65; transition: opacity 0.3s ease;
  background: rgba(255,255,255,.85);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 12px 10px;
  box-shadow: 0 2px 16px rgba(0,0,0,.08);
  max-height: 80vh; overflow-y: auto;
}
.quick-nav:hover { opacity: 1; }
.quick-nav .nav-item {
  display: flex; align-items: center; gap: 6px;
  cursor: pointer; transition: all 0.2s ease; padding: 3px 8px;
  border-radius: 6px;
}
.quick-nav .nav-item:hover { background: rgba(102,126,234,.08); }
.quick-nav .nav-item.section-divider {
  border-top: 1px solid #e8e8e8; margin-top: 4px; padding-top: 8px;
}
.quick-nav .nav-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: #bbb; transition: all 0.2s ease; flex-shrink: 0;
}
.quick-nav .nav-item:hover .nav-dot { background: var(--primary); }
.quick-nav .nav-item.active .nav-dot {
  background: var(--primary); width: 8px; height: 8px;
  box-shadow: 0 0 6px rgba(102,126,234,.5);
}
.quick-nav .nav-label {
  font-size: 11px; color: #666; white-space: nowrap;
  transition: color 0.2s ease;
}
.quick-nav .nav-item:hover .nav-label { color: #333; }
.quick-nav .nav-item.active .nav-label { color: var(--primary); font-weight: 600; }
.quick-nav .nav-item.section-nav .nav-label { font-weight: 500; }

/* === Collapsible Sections === */
.collapsible { cursor: pointer; user-select: none; }
.collapsible .collapse-icon {
  display: inline-block; margin-left: 8px; font-size: .7em;
  transition: transform 0.3s ease; opacity: 0.5;
}
.collapsible.collapsed .collapse-icon { transform: rotate(-90deg); }
.collapse-content {
  max-height: 5000px; overflow: hidden;
  transition: max-height 0.4s ease-out;
}
.collapse-content.collapsed { max-height: 0; }

/* Day card collapse */
.day-card .day-header { cursor: pointer; }
.day-card .day-header::after {
  content: '▼'; position: absolute; right: 20px; top: 50%;
  transform: translateY(-50%); font-size: .7em; opacity: 0.5;
  transition: transform 0.3s ease;
}
.day-card.collapsed .day-header::after { transform: translateY(-50%) rotate(-90deg); }
.day-card .spots-wrapper {
  transition: max-height 0.4s ease-out; max-height: 10000px; overflow: hidden;
}
.day-card.collapsed .spots-wrapper { max-height: 0; }

/* === Hero === */
.hero {
  position: relative; height: 420px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  overflow: hidden; display: flex; align-items: center; justify-content: center;
  text-align: center;
}
.hero::before {
  content: ''; position: absolute; bottom: -1px; left: 0;
  width: 100%; height: 60px; background: #f5f5f5;
  clip-path: ellipse(55% 100% at 50% 100%);
}
.hero-inner { position: relative; z-index: 1; }
.hero h1 {
  font-size: 2.4em; font-weight: 700; color: #fff;
  text-shadow: 0 2px 20px rgba(0,0,0,.2); margin-bottom: 8px;
  letter-spacing: 1px;
}
.hero .subtitle { font-size: 1.1em; color: rgba(255,255,255,.9); font-weight: 300; }
.hero .tag-row {
  margin-top: 16px; display: flex; gap: 8px;
  justify-content: center; flex-wrap: wrap;
}
.hero .tag {
  background: rgba(255,255,255,.2); backdrop-filter: blur(6px);
  color: #fff; padding: 5px 16px; border-radius: 20px;
  font-size: .84em; font-weight: 400;
}
.hero .emojis { font-size: 3em; margin-bottom: 12px; }

/* === Container === */
.container { max-width: 780px; margin: 0 auto; padding: 24px 16px 60px; }

/* === Transport Card === */
.transport-card {
  background: #fff; border-radius: 16px; padding: 24px;
  margin-bottom: 20px; box-shadow: 0 2px 12px rgba(0,0,0,.06);
}
.transport-card h2 { font-size: 1.2em; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.transport-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.t-item {
  background: #f8f9ff; border-radius: 12px; padding: 14px;
  position: relative;
}
.t-item .t-title { font-weight: 700; font-size: .95em; margin-bottom: 4px; }
.t-item .t-detail { font-size: .82em; color: #888; }
.t-item .t-price {
  font-size: 1.1em; font-weight: 700; color: #e05a3a; margin-top: 6px;
}

/* === Day Cards === */
.day-card {
  background: #fff; border-radius: 16px; overflow: hidden;
  margin-bottom: 24px; box-shadow: 0 2px 12px rgba(0,0,0,.06);
  transition: box-shadow 0.2s ease;
}
.day-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,.1); }
.day-header { padding: 24px 28px 20px; color: #fff; position: relative; }
.day-header .day-num { font-size: 1.7em; font-weight: 700; margin-bottom: 4px; }
.day-header .day-route { font-size: .85em; opacity: .85; margin-top: 6px; line-height: 1.5; }

/* Day gradients */
.day-header.d1 { background: linear-gradient(135deg, #f6a085 0%, #f2719c 100%); }
.day-header.d2 { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
.day-header.d3 { background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%); }
.day-header.d4 { background: linear-gradient(135deg, #fddb92 0%, #d1fdff 100%); color: #666; }
.day-header.d5 { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
.day-header.d6 { background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%); color: #666; }
.day-header.d7 { background: linear-gradient(135deg, #0c3483 0%, #6b8cce 100%); }
.day-header.d8 { background: linear-gradient(135deg, #8e2de2 0%, #4a00e0 100%); }
.day-header.d9 { background: linear-gradient(135deg, #00b4db 0%, #0083b0 100%); }

/* === Spots === */
.spot {
  padding: 20px 28px; border-bottom: 1px solid #f0f0f0;
  position: relative; transition: background 0.2s ease;
}
.spot:hover { background: #fafbff; }
.spot:last-child { border-bottom: none; }
.spot-head { display: flex; align-items: flex-start; gap: 14px; }
.spot-icon {
  width: 48px; height: 48px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.5em; flex-shrink: 0;
}
.spot:nth-child(odd) .spot-icon { background: #fff0f0; }
.spot:nth-child(even) .spot-icon { background: #f0f4ff; }
.spot-name { font-weight: 700; font-size: 1.08em; }
.spot-price {
  display: inline-block; background: #fff3e0; color: #e65100;
  font-size: .75em; padding: 2px 10px; border-radius: 8px;
  margin-left: 8px; font-weight: 500;
}
.spot-price.free { background: #f0fdf4; color: #15803d; }
.spot-transit {
  display: inline-flex; align-items: center; gap: 4px;
  background: linear-gradient(135deg, #e8f0ff, #f0e6ff); color: #5b7fdb;
  font-size: .72em; padding: 3px 10px; border-radius: 8px;
  margin-left: 6px; font-weight: 500; white-space: nowrap;
}
.spot-transit .transit-icon { font-size: .9em; }
.spot-transit .transit-time { color: #7c6ef0; font-weight: 700; }
.spot-desc {
  font-size: .88em; color: #666; margin-top: 8px;
  line-height: 1.65;
}
.spot-romance {
  margin-top: 10px; padding: 10px 14px;
  background: linear-gradient(90deg, #fff5f5, #fff0fb);
  border-radius: 10px; font-size: .85em; color: #c06;
  border-left: 3px solid #f2719c; line-height: 1.6;
}

/* === Route Bars === */
.route-bar {
  display: flex; align-items: center; gap: 5px;
  padding: 12px 28px; background: linear-gradient(90deg, #e8f0ff, #f0e6ff);
  font-size: .83em; color: #5b7fdb; overflow-x: auto; flex-wrap: wrap;
  border-left: 4px solid #7c6ef0; font-weight: 500; white-space: nowrap;
}
.route-bar .dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: #7c6ef0; flex-shrink: 0;
}
.route-bar .r-item { white-space: nowrap; }

/* Hotel→Spot Route Bar */
.hotel-route-bar {
  display: flex; align-items: center; gap: 5px;
  padding: 10px 28px; background: linear-gradient(90deg, #fff0f5, #fff5f0);
  font-size: .81em; color: #d06; overflow-x: auto; flex-wrap: wrap;
  border-left: 4px solid #f2719c; font-weight: 500; white-space: nowrap;
}
.hotel-route-bar .hdot {
  width: 8px; height: 8px; border-radius: 50%;
  background: #f2719c; flex-shrink: 0;
}
.hotel-route-bar .hroute-item { white-space: nowrap; }

/* === Highway Waypoint === */
.waypoint-bar {
  margin: 8px 28px; padding: 10px 16px;
  background: #fffbeb; border-radius: 8px;
  font-size: .79em; color: #92400e;
  display: flex; align-items: center; gap: 6px; flex-wrap: wrap;
  border: 1px dashed #fcd34d; line-height: 1.5;
}
.waypoint-bar .wp-facilities { color: #666; font-size: .92em; }

/* === Food Section (inline in day cards) === */
.food-section-inline { margin: 20px 28px; padding: 20px; background: #fffdf7; border-radius: 12px; border: 1px solid #fef0d0; }
.food-section-inline h2 { font-size: 1.05em; margin-bottom: 14px; color: #333; }

/* === Hotel Rec Section (inline) === */
.hotel-rec-section {
  margin: 20px 28px; padding: 20px;
  background: linear-gradient(135deg, #f8f9ff, #f0f4ff);
  border-radius: 12px;
}
.hr-title { font-weight: 700; font-size: 1.05em; margin-bottom: 12px; }
.hr-grid { display: grid; grid-template-columns: 1fr; gap: 10px; }
.hr-item { background: #fff; border-radius: 10px; padding: 14px; }
.hr-name { font-weight: 700; font-size: .92em; color: #333; }
.hr-area { font-size: .78em; color: #888; margin-top: 2px; }
.hr-price { font-size: .82em; color: #e05a3a; font-weight: 600; margin-top: 6px; }
.hr-desc { font-size: .78em; color: #666; margin-top: 6px; line-height: 1.55; }

/* === Food Summary Section === */
.food-section {
  background: #fff; border-radius: 16px; padding: 24px;
  margin-bottom: 20px; box-shadow: 0 2px 12px rgba(0,0,0,.06);
}
.food-section h2 { font-size: 1.2em; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.food-city { margin-bottom: 20px; }
.food-city:last-child { margin-bottom: 0; }
.food-city h3 { font-size: .95em; color: var(--primary); margin-bottom: 10px; padding-bottom: 6px; border-bottom: 1px solid #eee; }
.food-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.food-item {
  background: #fef9f0; border-radius: 12px; padding: 14px;
  transition: box-shadow 0.2s ease;
}
.food-item:hover { box-shadow: 0 2px 8px rgba(0,0,0,.06); }
.food-item .f-name { font-weight: 700; font-size: .92em; }
.food-item .f-shop { font-size: .78em; color: #999; margin-top: 3px; }
.food-item .f-price { color: #e05a3a; font-weight: 700; font-size: .9em; margin-top: 6px; }
.food-item .f-note { font-size: .78em; color: #666; margin-top: 3px; line-height: 1.5; }

/* === Avoid List === */
.avoid-section {
  background: #fff; border-radius: 16px; padding: 24px;
  margin-bottom: 20px; box-shadow: 0 2px 12px rgba(0,0,0,.06);
}
.avoid-section h2 { font-size: 1.2em; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.avoid-section .avoid-count {
  display: inline-block; background: #ff4d4f; color: #fff;
  font-size: .7em; padding: 2px 10px; border-radius: 10px; font-weight: 600;
}
.avoid-list { display: grid; grid-template-columns: 1fr; gap: 8px; }
.avoid-item {
  display: flex; gap: 12px; padding: 12px 16px;
  border-radius: 10px; background: #fff5f5; font-size: .86em;
  line-height: 1.6;
}
.avoid-item .a-num {
  background: #ff4d4f; color: #fff;
  width: 24px; height: 24px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: .75em; font-weight: 700; flex-shrink: 0;
}
.avoid-item .a-wrong { color: #ff4d4f; font-weight: 700; text-decoration: line-through; }
.avoid-item .a-right { color: #52c41a; font-weight: 600; }

/* === Budget === */
.budget-card {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 16px; padding: 24px; margin-bottom: 20px; color: #fff;
}
.budget-card h2 { font-size: 1.2em; margin-bottom: 16px; }
.budget-row {
  display: flex; justify-content: space-between; padding: 8px 0;
  font-size: .9em; border-bottom: 1px solid rgba(255,255,255,.15);
}
.budget-row:last-child { border: none; }
.budget-total {
  text-align: center; margin-top: 16px; padding-top: 16px;
  border-top: 2px solid rgba(255,255,255,.3);
  font-size: 1.4em; font-weight: 700;
}
.budget-saving {
  margin-top: 12px; padding: 10px 14px; background: rgba(255,255,255,.15);
  border-radius: 10px; font-size: .82em; line-height: 1.5;
}

/* === Tips === */
.tips-card {
  background: linear-gradient(135deg, #fff0f5, #fff5f0);
  border-radius: 16px; padding: 24px; margin-bottom: 20px;
}
.tips-card h2 { font-size: 1.2em; margin-bottom: 14px; }
.tips-card .tip-item {
  padding: 9px 0; font-size: .88em; display: flex; gap: 8px;
  line-height: 1.6; border-bottom: 1px solid rgba(0,0,0,.04);
}
.tips-card .tip-item:last-child { border-bottom: none; }

/* === Footer === */
.footer {
  text-align: center; padding: 30px 0 20px; color: #bbb; font-size: .82em;
}

/* ============================================================
   Responsive Breakpoints
   ============================================================ */

/* Hide quick nav on tablet and below */
@media (max-width: 1024px) { .quick-nav { display: none; } }

/* Tablet (768px) */
@media (max-width: 768px) {
  .hero { height: auto; min-height: 300px; padding: 48px 16px 70px; }
  .hero h1 { font-size: 1.6em; padding: 0 8px; word-break: break-word; }
  .hero .subtitle { font-size: .9em; padding: 0 8px; }
  .hero .emojis { font-size: 2.2em; margin-bottom: 8px; }
  .hero .tag { font-size: .72em; padding: 3px 10px; }
  .hero .tag-row { gap: 6px; }
  .container { padding: 16px 12px 40px; }
  .transport-grid, .food-grid { grid-template-columns: 1fr; }
  .day-header { padding: 18px 16px 16px; }
  .day-header .day-num { font-size: 1.3em; }
  .day-header::after { right: 14px; }
  .spot { padding: 16px 16px; }
  .spot-name { font-size: .95em; }
  .spot-transit { font-size: .68em; }
  .route-bar { padding: 10px 16px; font-size: .78em; }
  .spot-icon { width: 40px; height: 40px; font-size: 1.3em; }
  .waypoint-bar { margin: 8px 16px; font-size: .74em; }
  .food-section-inline { margin: 16px 16px; padding: 16px; }
  .hotel-rec-section { margin: 16px 16px; padding: 16px; }
  .hotel-route-bar { padding: 8px 16px; font-size: .76em; }
}

/* Phone (375px) */
@media (max-width: 375px) {
  .container { padding: 12px 8px; }
  .hero { min-height: 260px; padding: 36px 12px 60px; }
  .hero h1 { font-size: 1.3em; }
  .hero .tag { font-size: .68em; padding: 2px 8px; }
  .spot-icon { width: 36px; height: 36px; font-size: 1.1em; }
  .transport-card, .food-section, .avoid-section, .budget-card, .tips-card { padding: 16px; }
  .avoid-item { padding: 10px 12px; font-size: .8em; }
}

/* Touch Optimization */
@media (hover: none) {
  .quick-nav .nav-item { padding: 6px 0; }
  * { -webkit-tap-highlight-color: transparent; }
}

/* Print */
@media print {
  .quick-nav { display: none; }
  .day-card { break-inside: avoid; }
  .hero { height: auto; padding: 30px; }
}
'''


def gen_js(nav_items):
    """Generate JavaScript for nav and collapse."""
    nav_html_items = []
    for i, item in enumerate(nav_items):
        cls = ''
        if 'Day' not in item:
            cls = ' section-divider section-nav'
        nav_html_items.append(f'    <div class=\"nav-item{cls}\"><span class=\"nav-dot\"></span><span class=\"nav-label\">{item}</span></div>')

    return f'''<!-- ===== Right Quick Nav ===== -->
<nav class=\"quick-nav\" id=\"quickNav\">
{chr(10).join(nav_html_items)}
</nav>

<script>
// === Quick Nav: Auto-generate from sections ===
(function() {{
  var sections = document.querySelectorAll('[data-nav]');
  var nav = document.getElementById('quickNav');
  if (!nav || !sections.length) return;

  // Clear auto-generated and rebuild
  nav.innerHTML = '';
  sections.forEach(function(s) {{
    var dataNav = s.getAttribute('data-nav');
    var item = document.createElement('div');
    item.className = 'nav-item';
    if (dataNav.indexOf('Day') !== 0) item.classList.add('section-nav');
    // Check if previous was day and this is not => divider
    item.innerHTML = '<span class=\"nav-dot\"></span><span class=\"nav-label\">' + dataNav + '</span>';
    item.addEventListener('click', function() {{
      s.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }});
    nav.appendChild(item);
  }});

  // Scroll spy
  var items = nav.querySelectorAll('.nav-item');
  window.addEventListener('scroll', function() {{
    var current = '';
    sections.forEach(function(s) {{
      if (window.scrollY >= s.offsetTop - 120) current = s.getAttribute('data-nav');
    }});
    items.forEach(function(item) {{
      var label = item.querySelector('.nav-label').textContent;
      item.classList.toggle('active', label === current);
    }});
  }});
}})();

// === Collapse: Day cards ===
document.querySelectorAll('.day-card .day-header').forEach(function(header) {{
  header.addEventListener('click', function() {{
    header.parentElement.classList.toggle('collapsed');
  }});
}});

// === Collapse: Other sections with .collapsible class ===
document.querySelectorAll('.collapsible').forEach(function(el) {{
  el.addEventListener('click', function() {{
    el.classList.toggle('collapsed');
    var content = el.nextElementSibling;
    if (content && content.classList.contains('collapse-content')) {{
      content.classList.toggle('collapsed');
    }}
  }});
}});
</script>'''


def main():
    with open(TRIP_FILE, 'r', encoding='utf-8') as f:
        trip = json.load(f)

    nav_items = nav_data(trip['itinerary'])

    # Build HTML parts
    hero = gen_hero(trip)
    transport = gen_transport(trip)

    # Day cards
    day_cards = []
    for i, day in enumerate(trip['itinerary']):
        is_first = (day['day_number'] == 1)
        day_cards.append(gen_day_card(day, is_first=is_first))

    day_cards_html = '\\n'.join(day_cards)

    food = gen_food_summary_v2(trip)
    avoid = gen_avoid_list(trip)
    budget = gen_budget(trip)
    tips = gen_tips(trip)
    footer = gen_footer(trip)
    css = gen_css()
    js = gen_js(nav_items)

    # Assemble complete HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
<title>{trip['title']} — tourAI</title>
<style>
{css}
</style>
</head>
<body>

{js}

{hero}

<div class="container">

{transport}

{day_cards_html}

{food}

{avoid}

{budget}

{tips}

{footer}

</div>

</body>
</html>'''

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'Generated: {OUTPUT_FILE}')
    print(f'Size: {len(html)} bytes')
    print(f'Lines: {html.count(chr(10))}')


if __name__ == '__main__':
    main()
