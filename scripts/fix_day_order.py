#!/usr/bin/env python3
"""
Fix day order for jiuzhai-chuanxi-9d trip:
Swaps D2↔D5 pattern: 都江堰 moves to D2, 熊猫 moves to D5 (after 九寨沟),
Train to 九寨 moves to D3, 九寨沟+train back moves to D4.
"""

import json
import sys

TRIP_PATH = "D:/desktop/旅游/data/trips/jiuzhai-chuanxi-9d/trip.json"

def load():
    with open(TRIP_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save(trip):
    with open(TRIP_PATH, "w", encoding="utf-8") as f:
        json.dump(trip, f, ensure_ascii=False, indent=2)
    print("Saved trip.json")

def main():
    trip = load()
    old = trip["itinerary"]  # list of 9 days

    # Reorder: new[0]=old[0], new[1]=old[2], new[2]=old[3], new[3]=old[4], new[4]=old[1], new[5]=old[5], new[6]=old[6], new[7]=old[7], new[8]=old[8]
    new_order = [0, 2, 3, 4, 1, 5, 6, 7, 8]
    new_itinerary = [old[i] for i in new_order]

    # Update day_number on each
    for i, day in enumerate(new_itinerary):
        day["day_number"] = i + 1

    # ── NEW D2 (old D3): 都江堰 ──
    d2 = new_itinerary[1]
    d2["theme"] = "千年水利·都江堰奇迹全日游"
    d2["route_summary"] = "早晨地铁至犀浦站，乘城际列车18分钟到离堆公园站，按省体力下坡路线游览都江堰景区，中午灌县古城品尝非遗小吃和兔头，傍晚南桥看蓝眼泪夜景，乘城际列车返回成都"

    # Update D2 hotel highlights
    d2["hotel"]["highlights"] = "续住第二晚，交通便利，地铁直达犀浦站换乘城际列车。今晚从都江堰返回后好好休息——明天上午将搭乘高铁前往九寨沟，川西之旅正式启程。"

    # Update D2 spots - romantic moments
    for spot in d2["spots"]:
        if "都江堰" in spot["name"]:
            spot["romantic_moment"] = "牵手走过安澜索桥——这座被称为「天下第一爱情桥」的百年悬索桥横跨岷江，脚下江水奔涌，桥身悠悠摇晃。传说走过此桥的情侣会白头偕老，你们在桥中央停下，看远处玉垒山云雾缭绕。明天就要乘高铁去九寨沟了——今天都江堰的千年水利，是川西之旅最温柔的前奏。"
        if "灌县古城" in spot["name"]:
            spot["romantic_moment"] = "在南桥边找一家小店坐下，一碗热气腾腾的红糖醪糟粉子蛋端上来，醪糟的酒香混着红糖的甜蜜。夜幕降临，南桥蓝眼泪亮起，碧蓝的江水映着古城灯火。今晚早点回成都休息——明天高铁出发，九寨沟在等着你们。"

    # Update D2 meals notes
    for meal in d2["meals"]["dinner"]:
        if "黑竹香鸡" in meal.get("name", ""):
            meal["note"] = "成都本地人私藏的苍蝇馆子，乌骨鸡配魔芋+笋子的搭配一绝，鸡肉嫩滑魔芋Q弹入味。在抚琴小区深巷中，环境简陋但味道惊艳。今晚早点吃完回去休息，明天一早高铁去九寨沟。"
        if "三哥田螺" in meal.get("name", ""):
            meal["note"] = "1989年从街边大排档起家，30多年历史，成都最早一批冷淡杯（宵夜档）代表。重油重麻辣典型川式爆炒，承包两条街路边桌椅，烟火气十足。营业至凌晨4点。如回成都较晚可来这里宵夜，但建议别太晚——明天上午高铁去九寨沟。"

    # ── NEW D3 (old D4): Train to 九寨沟 ──
    d3 = new_itinerary[2]
    d3["theme"] = "高铁入九寨·漳扎镇高原缓冲"
    d3["route_summary"] = "上午成都东站乘高铁2小时抵达黄龙九寨站，换乘景区直通车1.5小时至九寨沟口，入住藏式酒店后在漳扎镇溜达适应高原，傍晚享用扎西藏餐牦牛肉火锅，为明天九寨沟全天暴走积蓄体力"

    # Update D3 hotel highlights
    d3["hotel"]["highlights"] = "藏式风格精品酒店或民宿，位置优越步行可达景区入口，地暖/电热毯供暖充足，部分房间可看到山景。仅住D3一晚，方便D4早上7:30步行进沟。D4下午出沟后直接乘直通车去高铁站不回酒店。提前网上预订，旺季价格上浮。漳扎镇超市晚上采购D4沟内干粮。"

    # Update D3 spots romantic moments
    for spot in d3["spots"]:
        if "漳扎镇" in spot["name"]:
            spot["romantic_moment"] = "高铁穿过隧道群，窗外的四川盆地渐渐变成川西高原。到站那一瞬间，空气里已经有了藏地的味道——稀薄、清冽、带着酥油茶的香。漳扎镇的傍晚，经幡在晚风里飘，你们慢慢走在藏式街道上，在超市采购明天沟内的午餐干粮。明天7:30，九寨沟Y字路线在等着你们——今晚早点休息，高原第一夜不洗澡。"

    # Update D3 meals notes
    for meal in d3["meals"]["breakfast"]:
        meal["note"] = "早点出发赶高铁——D3上午的高铁（建议9:00-10:00班次），酒店早餐或在成都东站买点包子带上。高铁上吃点零食，2小时到黄龙九寨站。"

    # ── NEW D4 (old D5): 九寨沟 + 高铁返蓉 ──
    d4 = new_itinerary[3]
    d4["theme"] = "人间仙境·九寨沟Y字精华+高铁返蓉"
    d4["route_summary"] = "7:30进沟按Y字精华路线快速打卡：五花海→珍珠滩瀑布→诺日朗→长海→五彩池→树正群海，15:30准时出沟（跳过盆景滩），沟口乘直通车1.5h至黄龙九寨站(¥51)，高铁C5798 18:19→20:39返回成都东(2h20min, ¥140)，晚上回嘉立精选酒店休整——这趟九寨沟一日暴走+高铁返蓉，紧凑但完全可行"

    # Change D4 hotel to 成都嘉立精选
    d4["hotel"] = {
        "name": "嘉立精选酒店(成都春熙路太古里店)",
        "area": "春熙路/太古里商圈",
        "price_range": "¥250-380/晚",
        "highlights": "高铁回成都后继D1-D3后续住嘉立精选。中式风格+智能化设备，离店送熊猫伴手礼，微信管家服务。D4晚从成都东站打车约25分钟到酒店。明天D5是成都慢生活一日——熊猫基地+鹤鸣茶社+太古里，不用赶路，睡到自然醒再起床。楼下美食街丰富，晚上还能出去吃宵夜。",
        "source": "websearch"
    }

    # Update D4 spots romantic moments
    for spot in d4["spots"]:
        if "九寨沟" in spot["name"]:
            spot["romantic_moment"] = "五花海——无法形容的蓝。湖水透明得像不存在，水底的沉木和钙华清晰可见。TA站在栈道上，水里倒映着两个人的身影。珍珠滩瀑布水声轰鸣水雾扑面，你们在瀑布前拍了一张合影——这会是这趟旅行里最蓝最清澈的一张。下午三点半出沟时回头望一眼，九寨沟在午后阳光里闪着光，但你们不觉得遗憾——晚上八点半就到成都了，嘉立精选的床在等着，明天还可以睡到自然醒。"

    # Update D4 meals
    for meal in d4["meals"]["dinner"]:
        if "巷子肥肠" in meal.get("name", ""):
            meal["note"] = "从黄龙九寨高铁2h20min回到成都东站，打车25分钟回嘉立精选酒店。巷子肥肠是成都本地人钟爱的苍蝇馆子——卤肥肠软糯入味，豆汤饭清鲜暖胃。九寨沟暴走一天后，一碗豆汤饭一碟卤肥肠把所有疲惫都治愈。如高铁晚点或太累，也可回嘉立精选酒店楼下美食街随便找家面馆吃碗担担面。"
        if "嘉立精选" in meal.get("name", ""):
            meal["note"] = "如果高铁到站太晚（21:00后）或太累不想跑远，嘉立精选酒店楼下美食街随便找一家就很好吃。春熙路周边遍地小吃，深夜也能找到热乎的。不用纠结，舒服最重要。明天D5是成都慢生活日——睡到自然醒再去熊猫基地也来得及。"

    # Update D4 breakfast note
    for meal in d4["meals"]["breakfast"]:
        meal["note"] = "早起在酒店吃饱——今天7:30进沟暴走到15:30，早餐一定要吃好。喝酥油茶暖身暖胃。高原徒步耗体力，多吃点碳水。D3晚上在漳扎镇超市已买好沟内干粮。"

    # ── NEW D5 (old D2): 熊猫 + 茶社 + 太古里 (REST DAY) ──
    d5 = new_itinerary[4]
    d5["theme"] = "熊猫萌宠·成都慢生活恢复日"
    d5["route_summary"] = "经历了D3高铁入九寨+D4九寨沟全天暴走两天的密集行程后，今天是成都慢生活恢复日——睡到自然醒再去熊猫基地看滚滚（不必赶7:30），中午品尝老牌川菜永乐饭店，下午人民公园鹤鸣茶社喝茶掏耳朵，傍晚逛太古里拍网红地标，晚餐地道川菜明园饭店"

    # Update D5 hotel highlights
    d5["hotel"]["highlights"] = "续住嘉立精选。中式风格+智能化设备，离店送熊猫伴手礼，微信管家服务。经历了九寨沟两天的高原奔波，今天在成都慢慢恢复——酒店楼下美食街丰富，春熙路步行即达。明天D6将开启川西自驾之旅——成都取车走G350熊猫大道去四姑娘山，好好享受今天在成都的慢时光。"

    # Update D5 spots - romantic moments
    for spot in d5["spots"]:
        if "熊猫" in spot["name"] or "大熊猫" in spot["name"]:
            spot["romantic_moment"] = "经历了九寨沟两天的高原奔波——高铁、直通车、Y字路线暴走、傍晚高铁回蓉——今天终于可以慢下来。睡到自然醒，来熊猫基地看滚滚抱着竹子憨态可掬地啃食。TA在你身边笑得像个孩子，两人相视一笑——成都的慢生活，原来这么美好。不用赶路，不用打卡，今天就是纯粹的成都时光。"
            spot["description"] = "全球最大的大熊猫繁育研究机构，可近距离观察大熊猫进食、玩耍、爬树。经历了九寨沟的暴走后，今天不用赶7:30——9:00-10:00到也能看到活跃的熊猫（虽然7:30-9:00最活跃，但今天的主题是「慢」）。建议从南大门进，坐观光车（¥30）到月亮产房和太阳产房。6号别墅每周一闭馆。"
        if "鹤鸣茶社" in spot["name"]:
            spot["romantic_moment"] = "百年茶馆里，两杯盖碗茶氤氲着茉莉花香。你们坐在湖边，看鹤发老人悠闲地掏耳朵，阳光透过梧桐叶洒在茶桌上。刚从九寨沟的高原回到成都平原，连呼吸都变得轻松——一壶开水无限续杯，时光慢得像回到了1930年代。这就是成都的疗愈力：两天高原奔波后，一杯茶就能让一切慢下来。"
        if "太古里" in spot["name"]:
            spot["romantic_moment"] = "夜幕降临，牵手漫步在太古里灯光璀璨的街区。在IFS爬墙大熊猫前拍下两人的合影——爬墙熊猫和今天上午看到的真熊猫，是这一天最好的呼应。千年古刹大慈寺的红墙前，两人并肩许下心愿。经历了九寨沟的壮阔和震撼，成都的温柔与慢生活在今天给了你们最好的疗愈。"

    # Update D5 meals notes
    for meal in d5["meals"]["lunch"]:
        if "永乐饭店" in meal.get("name", ""):
            meal["note"] = "1985年开业近40年，米其林必比登推荐，被誉为成都家常菜天花板。免费续加自制泡菜。11:00-14:00午市。宫保鸡丁+糯米排骨是招牌搭配。经历了九寨沟的藏餐和干粮，今天好好犒劳一下胃。"
    for meal in d5["meals"]["dinner"]:
        if "明园饭店" in meal.get("name", ""):
            meal["note"] = "开了几十年的老牌川菜馆，主厨年过七旬。没有固定菜单，直接到厨房选食材，老板娘负责凉拌菜（甜辣味拿手）。门口常坐满食客，市井烟火气浓。紧凑的九寨沟行程后，今晚在成都慢慢吃一顿老川菜——不赶高铁、不赶直通车、不赶景区末班车，就是纯吃。"

    # ── D6-D9 remain same but update day_number already done ──

    # Update D6 hotel highlights (references to old day numbering)
    d6 = new_itinerary[5]
    d6["hotel"]["highlights"] = "直面四姑娘山雪山景观，藏式风格客房，地暖充足，供氧设备。部分房间窗外即是幺妹峰，早起看日照金山。天台是看幺妹峰日落金山的最佳位置。今天只开了220km/4h，到民宿还有精力瘫在天台看幺妹峰被最后的日光照成金色。高原第一晚注意休息，不要洗澡洗头。"

    # Update D8 hotel
    d8 = new_itinerary[7]
    d8["hotel"] = {
        "name": "嘉立精选酒店(成都春熙路太古里店)",
        "area": "成都春熙路或双流机场周边",
        "price_range": "¥250-350/晚",
        "highlights": "川西自驾归来最后一晚。一嗨成都门店还车后打车回嘉立精选。D8晚回到成都，楼下美食街丰富——可以再去吃一顿巷子肥肠或来碗担担面。明天D9飞回，如果上午有时间还可以去宽窄巷子拍拍照。",
        "source": "websearch"
    }

    # Update D8 meals dinner
    for meal in d8["meals"]["dinner"]:
        if "巷子肥肠" in meal.get("name", ""):
            meal["note"] = "成都本地人钟爱的肥肠专门店，卤肥肠软糯入味，豆汤饭清鲜暖胃。三天川西自驾的最后一顿——一碗豆汤饭一碟卤肥肠，把高原的风雪和垭口的经幡都消化在成都的烟火气里。如还车较晚可在还车点附近就近解决。"

    # ── Update D9 ──
    d9 = new_itinerary[8]
    for spot in d9["spots"]:
        if "宽窄巷子" in spot["name"]:
            spot["romantic_moment"] = "最后一天在宽窄巷子，青砖黛瓦的四合院前，你们最后一次拍了张合影。九天的九寨川西之旅——D3高铁入九寨、D4 Y字路线的蓝、D2都江堰的安澜索桥、D5熊猫+茶社的慢成都、D6 G350熊猫大道的雪山长廊、D7疙瘩梁子的风、D8红海子的秋千——都在这张照片里。不是结束，是下一次出发的起点。"

    # Update spot route references for D9
    for spot in d9["spots"]:
        if spot.get("route"):
            spot["route"]["from_name"] = "嘉立精选酒店(成都春熙路太古里店)"

    # ── Update D1 route ──
    d1 = new_itinerary[0]
    d1["route_summary"] = "傍晚飞抵成都，入住春熙路附近嘉立精选酒店，直奔地道苍蝇馆子雨田饭店，饭后漫步春熙路感受成都夜生活——明天D2将前往都江堰看千年水利奇迹"
    for spot in d1["spots"]:
        if "春熙路" in spot["name"]:
            spot["romantic_moment"] = "夜幕下牵手漫步春熙路，路灯把两人的影子拉得长长的，街头传来吉他弹唱的民谣声，成都的慢生活从这一刻开始。明天D2就去都江堰——安澜索桥和蓝眼泪在等着你们，而三天后D3的高铁将带你们直奔九寨沟。九天的川西之旅，刚刚开始。"

    # Update D1 hotel
    d1["hotel"]["highlights"] = "中式风格+智能化设备，离店送熊猫伴手礼，微信管家服务，楼下美食街丰富，旺中带静。地理位置极佳，D2-D3地铁出行便利。D2都江堰一日游可地铁至犀浦站换乘城际列车。"

    # ── Set the new itinerary ──
    trip["itinerary"] = new_itinerary

    # ── Update budget hotel detail ──
    trip["budget"]["hotel"]["detail"] = "成都5晚——D1-D2嘉立精选¥250-380×2=¥500-760 + D4-D5嘉立精选¥250-380×2=¥500-760 + D8嘉立精选¥250-350 = ¥1250-1870；九寨沟口1晚¥400-800（D3藏式酒店）；四姑娘山镇1晚¥400-500（D6见山民宿）；新都桥1晚¥400-500（D7贡嘎宗）。均为2人一间共8晚。成都取还车省一晚九寨沟口高价房，多一晚成都性价比住宿。"

    # ── Update budget train detail ──
    trip["budget"]["train"]["detail"] = "D2犀浦↔离堆公园往返 ¥20×2人=¥40；D3成都东→黄龙九寨高铁 ¥140×2人=¥280；D4黄龙九寨→成都东高铁 ¥140×2人=¥280。合计¥600（2人）。提前在12306购票，旺季票源紧张。"

    # ── Update budget bus detail ──
    trip["budget"]["bus"]["detail"] = "D3黄龙九寨站→九寨沟口直通车 ¥51×2人=¥102；D4九寨沟口→黄龙九寨站直通车 ¥51×2人=¥102。合计¥204（2人）。车上购票或提前在旅游平台预订。约1.5小时车程。"

    # ── Update budget total note ──
    trip["budget"]["total"]["note"] = "不含购物和个人消费。旺季（国庆）机票可能上浮30-50%，酒店上浮20-30%。淡季（9月初/10月下旬）取预算低值。本方案以自然风光+免费观景台为主，门票费用仅约¥1228。新方案优势：成都取还车零异地费（省¥500+）+ 少开200km（省油费¥100）+ 九寨沟口少住一晚（省¥400-800）但多出D4高铁票（+¥280）和直通车（+¥102），净省约¥400-700。"

    # ── Update food_summary references ──
    for item in trip["food_summary"]:
        if item.get("reason"):
            if "D1和D9" in item["reason"]:
                item["reason"] = "成都资历最老的私营餐馆之一，1985年创立近40年。BBC纪录片取景地。红烧肉+藕汤经典搭配¥52/人，米饭¥1不限量。D1和D9首尾呼应。"
            if "D5高铁返蓉" in item["reason"]:
                item["reason"] = "D4高铁返蓉后的最佳慰藉——卤肥肠软糯+豆汤饭暖胃。九寨沟暴走一天后坐2h20min高铁回到成都，一碗豆汤饭一碟卤肥肠把所有疲惫都治愈。¥40/人。D8自驾归来也可再来一顿。"

    # ── Update avoid_list references ──
    for item in trip["avoid_list"]:
        if item.get("correct"):
            if "D5铁律" in item["correct"]:
                item["correct"] = "D4铁律：15:30必须出沟！盆景滩跳过不值得看。沟口直通车到黄龙九寨站需1.5h，C5798高铁18:19发车不等人。最晚16:00在沟口上直通车。错过这趟高铁下一班可能很晚甚至没票——那就只能在九寨沟口多住一晚，打乱全部后续行程。提前一天在漳扎镇超市买好干粮，沟内不浪费时间在诺日朗餐厅排队。"
            if "D4晚上在漳扎镇" in item["correct"]:
                item["correct"] = "诺日朗餐厅又贵又难吃（套餐¥60-100/人，味道敷衍）！D3晚上在漳扎镇超市采购面包、火腿肠、巧克力、自热米饭和水。诺日朗中心站有免费热水可以泡面。"
            if "D5高铁票" in item["correct"]:
                item["correct"] = "黄龙九寨→成都东高铁票务必提前在12306购买！C5798（18:19→20:39）是黄金时段，旺季（国庆）票源极紧张可能提前售罄。D3晚上在九寨沟口就可以在手机上买好D4的车票。¥140/人，2h20min到成都。如果这班售罄，备选C5796（17:15→19:46）但出沟时间更赶。"
            if "D2把熊猫基地安排" in item["correct"]:
                item["correct"] = "D5不用赶7:30——经历了九寨沟两天高原奔波后，今天是成都慢生活恢复日。9:00-10:00到也能看到活跃的熊猫，睡到自然醒再去完全OK。鹤鸣茶社和太古里就在市区，时间充裕。"

    # ── Update tips references ──
    for tip in trip["tips"]:
        if "D5高铁时间管理" in tip:
            # Update the tip index reference
            idx = trip["tips"].index(tip)
            trip["tips"][idx] = "D4高铁时间管理：黄龙九寨→成都东C5798（18:19→20:39）是黄金班次。15:30出沟→16:00沟口上直通车→17:30到黄龙九寨站→18:19发车。每段衔接紧凑但可行。务必提前在12306购票（D3晚上在九寨沟口就可以买好）！如果C5798售罄，备选C5796（17:15→19:46）但出沟时间需提前到14:30。"

    # ── Update title and metadata ──
    trip["metadata"]["version"] = "2.1.0"
    trip["metadata"]["generated_at"] = "2026-06-29T12:00:00+08:00"

    save(trip)
    print("Day order fixed successfully!")
    print("New order: D1 arrive → D2 都江堰 → D3 train to 九寨 → D4 九寨沟+返蓉 → D5 熊猫+慢成都 → D6 四姑娘山 → D7 新都桥 → D8 返成都 → D9 飞回")

if __name__ == "__main__":
    main()
