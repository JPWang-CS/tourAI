#!/usr/bin/env python3
"""Update output.html with new hotel names, hotel sections, and budget from trip.json."""

import json
import re

TRIP_PATH = r"D:\desktop\旅游\data\trips\jiuzhai-chuanxi-9d\trip.json"
HTML_PATH = r"D:\desktop\旅游\data\trips\jiuzhai-chuanxi-9d\output.html"

with open(TRIP_PATH, "r", encoding="utf-8") as f:
    trip = json.load(f)

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# ══════════════════════════════════════════════════════════════════════
# A) Global text replacements
# ══════════════════════════════════════════════════════════════════════

replacements = [
    ("嘉立精选酒店(成都春熙路太古里店)", "泰平·崇丽酒店(成都春熙路太古里店)"),
    ("嘉立精选酒店", "泰平·崇丽酒店"),
    ("嘉立精选", "泰平·崇丽"),
    ("全季酒店(成都春熙路太古里店)", "序里旅行酒店(成都太古里春熙路店)"),
    ("全季酒店", "序里旅行酒店"),
    ("见山民宿", "归山牧雲民宿"),
]

for old, new in replacements:
    html = html.replace(old, new)

print(f"Global replacements done.")

# ══════════════════════════════════════════════════════════════════════
# B) Build hotel HTML blocks for each day
# ══════════════════════════════════════════════════════════════════════

def make_hotel_block(day, night_label):
    """Build hotel recommendation HTML from trip.json day data."""
    h = day.get("hotel")
    if not h:
        return ""

    name = h["name"]
    price = h["price_range"]
    highlights = h.get("highlights", "")

    # Split into primary and alternative
    if "|" in name:
        parts = [p.strip() for p in name.split("|")]
    else:
        parts = [name]

    primary_name = parts[0] if len(parts) > 0 else name
    alt_name = parts[1] if len(parts) > 1 else ""

    # Split highlights similarly - first part for primary, second for alt, rest is context
    hl_parts = [p.strip() for p in highlights.split("|")]
    primary_hl = hl_parts[0] if len(hl_parts) > 0 else ""
    alt_hl = hl_parts[1] if len(hl_parts) > 1 else ""
    context_hl = " | ".join(hl_parts[2:]) if len(hl_parts) > 2 else ""

    if context_hl:
        primary_hl = primary_hl + " | " + context_hl

    lines = []
    lines.append(f'    <div class="hotel-rec-section">')
    lines.append(f'      <div class="hr-title">🏨 推荐住宿（{night_label}）</div>')
    lines.append(f'      <div class="hr-grid">')
    lines.append(f'        <div class="hr-item">')
    lines.append(f'          <div class="hr-name">{primary_name}</div>')
    lines.append(f'          <div class="hr-price">💰 {price}</div>')
    lines.append(f'          <div class="hr-desc">{primary_hl}</div>')
    lines.append(f'        </div>')
    if alt_name:
        lines.append(f'        <div class="hr-item">')
        lines.append(f'          <div class="hr-name">{alt_name}</div>')
        lines.append(f'          <div class="hr-price">💰 {price}</div>')
        lines.append(f'          <div class="hr-desc">{alt_hl}</div>')
        lines.append(f'        </div>')
    lines.append(f'      </div>')
    lines.append(f'    </div>')
    return "\n".join(lines)


day_labels = {
    1: "成都第1晚",
    2: "成都第2晚 · 续住",
    3: "九寨沟口第1晚",
    4: "成都第3晚 · 高铁返蓉",
    5: "成都第4晚 · 慢生活",
    6: "四姑娘山镇第1晚",
    7: "新都桥第1晚",
    8: "成都第5晚 · 自驾归来",
}

# Pre-build hotel blocks
hotel_blocks = {}
for dn in range(1, 9):
    day = trip["itinerary"][dn - 1]
    hotel_blocks[dn] = make_hotel_block(day, day_labels[dn])

# Find and replace each hotel section
# The hotel-rec-section div is always followed by \n  </div> (closing spots-wrapper)
MARKER = '<div class="hotel-rec-section">'

# Collect all positions before any modifications
positions = []
pos = 0
count = 0
while True:
    idx = html.find(MARKER, pos)
    if idx == -1:
        break
    # Find the closing: </div>\n  </div> pattern after hotel-rec-section
    # Actually the hotel section ends at its own </div>, then spots-wrapper closes with </div>
    # Pattern: hotel-rec-section content </div>\n  </div>\n</div>
    # Let's find the end of hotel-rec-section by counting div depth from marker

    # Simpler: find </div>\n  </div>\n</div> which is the standard closing pattern
    # after hotel section inside day card
    search_start = idx + len(MARKER)
    close_pattern = '</div>\n  </div>\n</div>'
    close_idx = html.find(close_pattern, search_start)
    if close_idx == -1:
        # Try alternative: </div>\n    </div>\n  </div>
        close_pattern = '</div>\n    </div>\n  </div>'
        close_idx = html.find(close_pattern, search_start)
    if close_idx == -1:
        print(f"  WARNING: Cannot find close for hotel section at position {idx}")
        pos = search_start
        continue

    section_end = close_idx + len('</div>')
    # The hotel-rec-section is from idx to close_idx
    # After close_idx + len('</div>'), we have \n  </div>\n</div> or similar
    positions.append((idx, section_end, count))
    count += 1
    pos = section_end

print(f"Found {len(positions)} hotel sections")

if len(positions) != 8:
    print(f"WARNING: Expected 8 hotel sections, found {len(positions)}")
    # Fallback: just do the global text replacements and skip section replacement
else:
    # Replace from last to first to preserve positions
    for idx, end_idx, section_num in reversed(positions):
        dn = section_num + 1  # sections are in order D1-D8
        if dn in hotel_blocks:
            new_block = hotel_blocks[dn]
            html = html[:idx] + new_block + "\n  " + html[end_idx:]
            print(f"  D{dn}: Hotel section replaced")

# ══════════════════════════════════════════════════════════════════════
# C) Replace budget section
# ══════════════════════════════════════════════════════════════════════

budget = trip["budget"]

def ps(r):
    if isinstance(r, (int, float)):
        return str(int(r))
    return str(r)

train_val = ps(budget["train"]["total"])
bus_val = ps(budget["bus"]["total"])
train_plus_bus = str(int(train_val) + int(bus_val))

budget_html = f'''<!-- ===== BUDGET ===== -->
<div class="budget-card" data-nav="预算估算">
  <h2>💰 预算估算（2人 · 9天8晚）</h2>
  <div class="budget-row"><span>✈️ 往返机票</span><span>¥{ps(budget["flight"]["total"])}</span></div>
  <div class="budget-row"><span>🚄🚌 高铁+直通车</span><span>¥{train_val} + {bus_val} = ¥{train_plus_bus}</span></div>
  <div class="budget-row"><span>🚗 租车3天（含油费+过路费）</span><span>¥{ps(budget["car_rental"]["total"])}</span></div>
  <div class="budget-row"><span>🏨 住宿8晚（成都5+九寨1+四姑娘山1+新都桥1）</span><span>¥{ps(budget["hotel"]["total"])}</span></div>
  <div class="budget-row"><span>🎫 门票</span><span>¥{ps(budget["tickets"]["total"])}</span></div>
  <div class="budget-row" style="border:none;"><span>🍜 餐饮</span><span>¥{ps(budget["food"]["total"])}</span></div>
  <div class="budget-total">总计 ¥{ps(budget["total"]["range"])} · 人均 ¥{ps(budget["total"]["per_person"])}</div>
  <div style="margin-top:12px; font-size:.78em; opacity:.8;">
    <div style="display:flex; justify-content:space-between; padding:2px 0;"><span>高铁明细：D2犀浦↔离堆公园¥20×2 + D3成都东→黄龙九寨¥140×2 + D4黄龙九寨→成都东¥140×2 = ¥{train_val}</span></div>
    <div style="display:flex; justify-content:space-between; padding:2px 0;"><span>直通车明细：D3黄龙九寨站→沟口¥51×2 + D4沟口→黄龙九寨站¥51×2 = ¥{bus_val}</span></div>
    <div style="display:flex; justify-content:space-between; padding:2px 0;"><span>门票明细：熊猫基地¥110 + 都江堰¥160 + 九寨沟¥518 + 双桥沟¥300 + 甲居藏寨¥100 + 泸定桥¥20 + 红海子¥20 = ¥1,228</span></div>
    <div style="display:flex; justify-content:space-between; padding:2px 0;"><span>住宿明细：成都5晚(泰平·崇丽¥200-350×5=¥1000-1750 或 序里¥250-400×5=¥1250-2000) + 九寨1晚¥350-800 + 四姑娘山1晚¥400-700 + 新都桥1晚¥350-600 = ¥2100-4100</span></div>
    <div style="display:flex; justify-content:space-between; padding:2px 0;"><span>{budget["total"]["note"]}</span></div>
  </div>
</div>'''

budget_start = html.find('<!-- ===== BUDGET ===== -->')
if budget_start == -1:
    print("WARNING: Cannot find budget section")
else:
    budget_end = html.find('<!-- ===== TIPS ===== -->', budget_start)
    if budget_end == -1:
        budget_end = html.find('<footer class="footer"', budget_start)
    if budget_end == -1:
        print("WARNING: Cannot find end of budget section")
    else:
        html = html[:budget_start] + budget_html + "\n\n" + html[budget_end:]
        print("Budget section replaced")

# ══════════════════════════════════════════════════════════════════════
# D) Verify and write
# ══════════════════════════════════════════════════════════════════════

# Quick check for legacy names
for legacy in ["嘉立精选", "全季酒店", "见山民宿"]:
    count = html.count(legacy)
    if count > 0:
        print(f"WARNING: {count} remaining '{legacy}' references")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("\noutput.html updated successfully!")
