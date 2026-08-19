#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the standalone webpage for the optimized Jiuzhai/Siguniang trip."""

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRIP_PATH = ROOT / "data" / "trips" / "jiuzhai-chuanxi-9d-optimized" / "trip.json"
OUT_PATH = ROOT / "data" / "trips" / "jiuzhai-chuanxi-9d-optimized" / "output.html"


def esc(value):
    return html.escape(str(value or ""))


HOTELS = [
    {
        "area": "成都",
        "badge": "新·位置优先",
        "name": "锦著酒店（成都春熙路太古里店）",
        "score": "4.7/5",
        "view": "2024年开业，现代智能房型，适合多晚不换酒店",
        "location": "春熙路/太古里附近，距地铁步行约10分钟；适合D1、D2、D4、D5",
        "booking": "约¥350–650/晚；国庆需以实时订单为准",
        "freshness": "2024年开业（到本次出行约2年）",
        "url": "https://m.ctrip.com/html5/hotel/hoteldetail/119737846.html",
        "source": "携程酒店页；开业年份和近期住客评价可核查",
    },
    {
        "area": "成都",
        "badge": "新·高空景观",
        "name": "成都LOUIS高空酒店（春熙路太古里店）",
        "score": "近期评价较好",
        "view": "2023年开业，全落地窗和高层城市景观，拍照优势明显",
        "location": "春熙路/太古里核心商圈，适合D1、D2、D4、D5",
        "booking": "约¥400–800/晚；按房型和日期浮动",
        "freshness": "2023年开业（到本次出行约3年半）",
        "url": "https://hotels.ctrip.com/hotels/112234105.html",
        "source": "携程酒店页；预订时确认具体房型视野和隔音",
    },
    {
        "area": "成都",
        "badge": "旧店·只作备选",
        "name": "成都尼依格罗酒店",
        "score": "4.8/5",
        "view": "高层城市景观突出，适合把成都住宿做成旅途缓冲",
        "location": "太古里核心商圈，出行和餐饮最方便",
        "booking": "通常约¥900–1600/晚；预算压力较大",
        "freshness": "开业/最近装修年份未在公开资料中充分确认，不纳入新酒店首选",
        "url": "https://hotels.ctrip.com/hotels/1666127.html",
        "source": "携程酒店页；景观优势来自高层定位，预订前确认近期房态",
    },
    {
        "area": "九寨沟沟口",
        "badge": "新·沟口首选",
        "name": "九寨沟景区游客中心漫心酒店",
        "score": "4.7/5",
        "view": "2025年开业，房间和公共区域较新，适合只住一晚的效率型安排",
        "location": "漳扎镇隆康村，步行约4分钟到九通客运服务站，重点确认到游客中心的实际步行/接驳",
        "booking": "约¥450–800/晚；国庆价格波动最大",
        "freshness": "2025年开业（到本次出行约1年）",
        "url": "https://hotels.ctrip.com/hotels/131950085.html",
        "source": "携程酒店页；开业年份、近期评价和沟口位置可核查",
    },
    {
        "area": "九寨沟沟口",
        "badge": "景观·停车",
        "name": "九寨沟千鹤国际大酒店",
        "score": "4.6/5",
        "view": "山谷景观和公共空间更宽，适合自驾或行李较多",
        "location": "漳扎镇主路片区；离沟口通常需要接驳/打车",
        "booking": "约¥400–750/晚；优先确认停车和接驳",
        "freshness": "2021年升级装修，已超出4年窗口，仅作停车/空间备选",
        "url": "https://hk.trip.com/hotels/jiuzhaigou-hotel-detail-436646/qianhe-rezen-hotel/review.html",
        "source": "Trip.com住客评价 + 携程酒店页",
    },
    {
        "area": "九寨沟沟口",
        "badge": "连锁·旧店备选",
        "name": "九寨沟智选假日酒店",
        "score": "4.6/5",
        "view": "景观不如山景型酒店，但服务标准和早餐预期更稳定",
        "location": "沟口片区；适合重视连锁体系和早出发",
        "booking": "约¥500–900/晚；以官方和订单页面为准",
        "freshness": "2020年建设，最近装修年份未确认，不满足新酒店优先条件",
        "url": "https://www.ihg.com/holidayinnexpress/hotels/cn/zh/jiuzhaigou/jihha/hoteldetail",
        "source": "洲际官方酒店页；携程酒店页可辅助比价",
    },
    {
        "area": "四姑娘山",
        "badge": "新·综合首选",
        "name": "悠然牧居智能酒店（四姑娘山店）",
        "score": "4.7/5",
        "view": "2024年开业，供氧、智能客控、山景和停车配置较均衡",
        "location": "四姑娘山镇金锋村风情街，方便D7双桥沟早出发",
        "booking": "约¥500–900/晚；确认供氧、地暖和停车",
        "freshness": "2024年开业（到本次出行约2年）",
        "url": "https://hotels.ctrip.com/hotels/123285455.html",
        "source": "携程酒店页；开业年份、供氧、停车和近期评价可核查",
    },
    {
        "area": "四姑娘山",
        "badge": "新·风景优先",
        "name": "四姑娘山仰望星空·Vacilando度假庄园",
        "score": "4.8/5",
        "view": "2024年开业，长坪沟方向山景和日照金山条件更好，适合拍照",
        "location": "四姑娘山长坪沟/斯古拉神山方向；确认到双桥沟游客中心距离",
        "booking": "约¥600–1000/晚；国庆库存少，价格易上浮",
        "freshness": "2024年开业（到本次出行约2年）",
        "url": "https://hotels.ctrip.com/hotels/116857753.html",
        "source": "携程酒店页；重点核对停车、供氧、暖气和到双桥沟车程",
    },
    {
        "area": "四姑娘山",
        "badge": "稳妥备选",
        "name": "阅山四季酒店",
        "score": "4.7/5",
        "view": "主打山景和安静环境，适合作为满房时替代",
        "location": "四姑娘山镇片区；下单前确认具体朝向",
        "booking": "约¥500–900/晚；以实时房价为准",
        "freshness": "2023年开业（到本次出行约3年），满足新旧筛选窗口",
        "url": "https://hotels.ctrip.com/hotels/106356885.html",
        "source": "携程酒店页；景观取决于房型和朝向",
    },
    {
        "area": "新都桥",
        "badge": "新·景观首选",
        "name": "Ozz·nice5·时光赦免度假庄园（康定新都桥店）",
        "score": "4.7/5",
        "view": "2024年开业，贡嘎雪山视野、270°落地窗、弥散供氧和地暖突出",
        "location": "新都桥新二村；景观优先但离主街有距离，适合自驾",
        "booking": "约¥700–1300/晚；国庆先确认供氧、地暖和早餐",
        "freshness": "2024年开业（到本次出行约2年）",
        "url": "https://hotels.ctrip.com/hotels/123791988.html",
        "source": "携程酒店页及近期住客评价；风景取决于房型和天气",
    },
    {
        "area": "新都桥",
        "badge": "新·稳定性价比",
        "name": "全季酒店（康定新都桥318国道店）",
        "score": "4.8/5",
        "view": "2024年开业，供氧、停车、洗衣和早餐稳定，部分房型可看山景",
        "location": "新都桥岗邱上街579号，靠近318国道；停车方便但可能有道路噪声",
        "booking": "约¥450–850/晚；确认供氧、房间朝向和早餐",
        "freshness": "2024年开业（到本次出行约2年）",
        "url": "https://hotels.ctrip.com/hotels/116452805.html",
        "source": "携程酒店页及2026年住客评价；优先看房间朝向",
    },
    {
        "area": "新都桥",
        "badge": "新·贡嘎视野",
        "name": "康定赞蕃大酒店（新都桥店）",
        "score": "4.5/5",
        "view": "2023年开业，直面贡嘎雪山观景台，弥散供氧和水暖配置更适合高原恢复",
        "location": "瓦泽乡营关村贡嘎雪山观景台南50米；景观好但离镇主街较远",
        "booking": "约¥500–1000/晚；确认供氧设备、热水、停车和餐厅营业",
        "freshness": "2023年开业（到本次出行约3年）",
        "url": "https://hotels.ctrip.com/hotels/108747741.html",
        "source": "携程酒店页及近期住客评价；优先看具体房型",
    },
]


# 餐饮不按“必吃榜”排序，而按证据强弱和路线可执行性筛选。
# 高：官方老字号/地方政府或官方旅游门户；中：地图可定位且有独立资料交叉；
# 现场：川西乡镇公开资料不足，只给菜系和现场判断规则，不把软文包装成确定推荐。
FOOD_GUIDE = [
    {
        "day": "D1 / D5 / D8",
        "area": "成都",
        "name": "钟水饺（就近老字号门店）",
        "type": "传统小吃",
        "dishes": "红油水饺、清汤水饺、甜水面",
        "price": "约¥25–60/人",
        "confidence": "高",
        "address": "春熙路/市区就近门店；以地图当日营业门店为准",
        "reason": "1893年创立的中华老字号，适合抵达日、取车日或返程前吃一顿轻食；不需要为一碗小吃跨区排队。",
        "source": "商务部老字号数字博物馆",
        "url": "https://lzhbwg.mofcom.gov.cn/edi_ecms_web_front/thb/detail/8cf137a439d24c3a8ed22112e6243665",
        "caution": "老字号只能证明传承和品牌，不等于每家分店当天口味相同；看实时评价和排队长度。",
    },
    {
        "day": "D1 / D5 / D8",
        "area": "成都",
        "name": "盘飧市（老字号熟食/川菜）",
        "type": "传统川味正餐",
        "dishes": "卤味、烧白、粉蒸肉、凉菜；按当日菜单点2–3样",
        "price": "约¥60–100/人",
        "confidence": "高",
        "address": "成都城区门店；优先选择离酒店/还车点近的门店",
        "reason": "官方老字号名录中的成都传统餐饮品牌，比“装修出片”的网红川菜馆更符合这次想吃本地味的目标。",
        "source": "中华老字号名录（四川省成都市饮食公司）",
        "url": "https://www.contmusic.com/kyguanwangmanbetx/uploadfile/file/20230204/769f39c66.pdf",
        "caution": "不建议点满桌招牌或套餐；两人按一荤一素一凉菜/汤控制分量。",
    },
    {
        "day": "D2 午餐",
        "area": "都江堰",
        "name": "老号尤兔头（都江堰大道店）",
        "type": "都江堰地方味",
        "dishes": "兔头、冷吃兔、家常川菜；怕辣先说明",
        "price": "约¥50–90/人",
        "confidence": "高",
        "address": "都江堰大道店；以官方旅游门户和地图实时位置为准",
        "reason": "都江堰官方旅游门户列出的本地餐饮，四川省乡村名菜/体验店资料也收录了老号尤兔头；比灌县古城门口随机套餐更可控。",
        "source": "都江堰官方旅游美食专题 + 四川省乡村名菜及体验店名单",
        "url": "https://www.djy517.com/channel-djymeishi.html",
        "caution": "先看单点菜单和斤两，拒绝不明海鲜/河鲜套餐；景区附近价格浮动时直接换店。",
    },
    {
        "day": "D2 下午茶",
        "area": "都江堰灌县古城",
        "name": "古城小吃短停，不安排网红打卡店",
        "type": "本地小吃",
        "dishes": "醪糟粉子蛋、红糖糍粑、锅贴/小面，三选一即可",
        "price": "约¥15–35/人",
        "confidence": "现场",
        "address": "离堆公园—灌县古城一带；看本地客流和现做情况",
        "reason": "D2晚还要回成都，不把下午茶做成排队项目；少量尝味比在古城吃高价旅游套餐更合适。",
        "source": "都江堰官方旅游美食专题",
        "url": "https://www.djy517.com/channel-djymeishi.html",
        "caution": "不采信“古城第一名店/必吃榜”标题；有菜单、有明码标价、现做且本地客流稳定再买。",
    },
    {
        "day": "D3 晚餐",
        "area": "九寨沟沟口",
        "name": "源湘味·鲜牦牛肉汤锅",
        "type": "牦牛汤锅",
        "dishes": "清汤牦牛肉、土豆/萝卜/菌类；少量主食",
        "price": "约¥70–110/人",
        "confidence": "中",
        "address": "漳扎镇漳扎村二组18号附1号",
        "reason": "有高德地图可定位的实体店和明确地址，适合作为D3沟口一晚的首个核验对象；公开资料不足，不把口味写成确定事实。",
        "source": "高德地图实体店信息",
        "url": "https://www.amap.com/place/B0LD740VY9",
        "caution": "到店先看牦牛肉来源、斤两和锅底价格；不买“歌舞晚宴/豪华套餐”，不喝酒，吃七分饱。",
    },
    {
        "day": "D3 备选",
        "area": "九寨沟沟口",
        "name": "漳扎镇普通藏餐/面食店（现场筛选）",
        "type": "藏羌风味",
        "dishes": "藏式面食、牦牛肉、酥油茶、青稞饼；一人一份即可",
        "price": "约¥35–80/人",
        "confidence": "现场",
        "address": "游客中心周边步行可达范围；不为餐厅绕路",
        "reason": "九寨沟沟口餐饮宣传内容广告化明显，公开资料很难证明哪家长期稳定；用“看菜单、看本地客流、看明码标价”替代盲信榜单。",
        "source": "九寨沟官方公告 + 地方餐饮交叉检索后的保守建议",
        "url": "https://www.jiuzhai.com/news/notice/11001-2026-03-23-01-36-44",
        "caution": "避开野生鱼、虫草、松茸、天价牦牛和歌舞宴等强推项目；出现强制消费或模糊菜单直接离店。",
    },
    {
        "day": "D4 午餐",
        "area": "九寨沟景区",
        "name": "自带干粮，不把景区餐厅作为主餐",
        "type": "景区执行餐",
        "dishes": "面包、坚果、能量棒、饼干、温水；出沟后回成都吃热食",
        "price": "约¥30–50/两人",
        "confidence": "高",
        "address": "D3晚在沟口采购，D4随身携带",
        "reason": "D4要在15:00左右出沟赶车，景区内排队吃饭会直接侵蚀返程缓冲；这是一项交通安全安排，不是为了省餐费。",
        "source": "九寨沟官方开放与景区管理信息",
        "url": "https://www.jiuzhai.com/news/notice/11001-2026-03-23-01-36-44",
        "caution": "只带密封、无异味、可带入的食品；以景区当日禁限带规则为准，不在栈道边边走边吃。",
    },
    {
        "day": "D5 午晚餐",
        "area": "成都",
        "name": "熊猫基地/取车点附近清淡川菜",
        "type": "恢复日正餐",
        "dishes": "小份回锅肉、豆花、青菜、面/饭；少油少辣",
        "price": "约¥50–90/人",
        "confidence": "现场",
        "address": "熊猫基地返酒店或取车门店附近；不跨城找店",
        "reason": "D5的核心是熊猫基地、取车、采购和检查车辆。餐饮要服务于下午流程，避免为“热门店”排队导致物资没买齐。",
        "source": "熊猫基地官方开放与入园规则 + 路线执行判断",
        "url": "https://www.panda.org.cn/cn/service/opentime/",
        "caution": "熊猫基地附近先看明码标价和翻台客流；不把园区周边“熊猫主题套餐”当作特色美食。",
    },
    {
        "day": "D6 午餐",
        "area": "卧龙/小金沿线",
        "name": "沿途乡镇面馆或小炒店",
        "type": "自驾补给餐",
        "dishes": "面、蛋炒饭、番茄蛋汤、时蔬；车上另备干粮",
        "price": "约¥25–50/人",
        "confidence": "现场",
        "address": "G350映秀—卧龙—小金沿线，看到正规停车和本地客流再停",
        "reason": "这段路的价值是赶到四姑娘山和双桥沟，不适合为餐厅折返；热食、卫生、出餐速度优先于“特色装修”。",
        "source": "四姑娘山官方交通指引 + 路线现场策略",
        "url": "https://www.sgnsgeopark.cn/guideline/traffic",
        "caution": "不在路肩临停，不吃生冷；14:00前到不了双桥沟时，优先取消进沟而不是压缩吃饭和休息。",
    },
    {
        "day": "D6 晚餐",
        "area": "四姑娘山镇",
        "name": "镇上客流稳定的牦牛肉汤锅/菌汤",
        "type": "川西高原热食",
        "dishes": "清汤牦牛肉、菌汤、土豆/萝卜/时蔬；不点超大拼盘",
        "price": "约¥70–110/人",
        "confidence": "现场",
        "address": "四姑娘山镇主街，优先酒店步行可达店",
        "reason": "四姑娘山镇具体餐厅的独立、非推广资料很少，网页不伪造“本地人第一名”；现场看锅底、菜单和客流更可靠。",
        "source": "四姑娘山路线餐饮交叉检索后的保守建议",
        "url": "https://www.sgnsgeopark.cn/guideline/traffic",
        "caution": "高原第一晚少酒少辣，点小锅或半份；饭后不洗长时间热水澡，不剧烈活动。",
    },
    {
        "day": "D7 午餐",
        "area": "丹巴县城",
        "name": "罕额林卡藏餐厅",
        "type": "丹巴藏餐/地方菜",
        "dishes": "火烧子馍馍、牦牛肉汤锅、贡椒鱼/野生菌牦牛杂汤锅（按当日供应）",
        "price": "约¥60–100/人",
        "confidence": "高",
        "address": "丹巴县城；到店前用地图核对营业状态和停车",
        "reason": "四川省官方乡村名菜及体验店名单明确收录丹巴罕额林卡藏餐厅及当地菜品，是本次川西段少数有政府名单支撑的具体餐饮对象。",
        "source": "四川省商务厅乡村名菜及体验店名单",
        "url": "https://swt.sc.gov.cn/sccom/tzgg/2022/9/23/e5fd9c9526a44c969ac7fb104ecd4520/files/b78c3ef887e2427589296dff939fb684.pdf",
        "caution": "名单不能保证2026年营业和当天出品；先电话/地图确认，点菜时问清鱼、菌和汤锅价格。",
    },
    {
        "day": "D7 晚餐",
        "area": "新都桥",
        "name": "本地藏餐或牦牛汤锅，现场择店",
        "type": "新都桥地方风味",
        "dishes": "牦牛肉汤锅、青稞饼、酥油茶、牦牛酸奶；不强求全套藏餐",
        "price": "约¥70–120/人",
        "confidence": "现场",
        "address": "新都桥镇主街/住宿附近；优先步行可达、明码标价店",
        "reason": "新都桥公开内容高度集中在牦牛汤锅和藏餐，但具体店铺的独立资料不足；这次不把单篇探店文章中的店名升级为“必吃”，按现场规则选。",
        "source": "康定市政府节假日服务信息 + 菜系交叉判断；不采信单篇探店",
        "url": "https://www.kangding.gov.cn/xzdt/article/711506",
        "caution": "公开资料不足，不给出“必吃店”结论；不预付套餐、不买模糊“野生菌/虫草”加价菜，先确认分量。",
    },
    {
        "day": "D8 午餐",
        "area": "康定/泸定",
        "name": "王凉粉或丁三哥老字号（择一）",
        "type": "康定本地小吃",
        "dishes": "康定凉粉、锅盔、牦牛杂汤/牦牛肉汤",
        "price": "约¥20–60/人",
        "confidence": "中",
        "address": "康定市区；若不进康定则在泸定县城吃简餐",
        "reason": "康定本地资料长期提到凉粉、锅盔和牦牛杂汤，比在S434沿线临时找餐馆更符合路线；D8仍需为返成都留足时间。",
        "source": "康定地方旅游攻略资料；到店前地图复核",
        "url": "https://m.tuniucdn.com/filebroker/cdn/olb/96/79/96796e72b9480e7bb649b6337cbbe959.pdf?alias=%E5%BA%B7%E5%AE%9A%E6%97%85%E6%B8%B8%E6%94%BB%E7%95%A5.pdf",
        "caution": "非官方实时营业信息，不能据此保证店还在营业；若时间紧，泸定县城正规快餐/面馆优先。",
    },
    {
        "day": "D8 晚餐",
        "area": "成都",
        "name": "成都老字号川味收官餐",
        "type": "返程恢复餐",
        "dishes": "盘飧市卤味/烧白，或就近钟水饺、龙抄手；不安排跨区火锅",
        "price": "约¥60–100/人",
        "confidence": "高",
        "address": "还车后酒店附近；按到店时间就近选择",
        "reason": "D8已完成高原长途驾驶，收官餐应稳定、好消化、离酒店近；老字号品牌资料可核查，但不需要为“网红火锅”排队。",
        "source": "商务部老字号数字博物馆/中华老字号名录",
        "url": "https://lzhbwg.mofcom.gov.cn/edi_ecms_web_front/thb/detail/8236b3b91b554e27b8120caa19bd4f47",
        "caution": "如果还车晚于21:00，直接选酒店周边营业中的面食/粥/简餐，不跨区。",
    },
    {
        "day": "D9 早餐",
        "area": "成都/天府机场",
        "name": "酒店早餐或机场早餐",
        "type": "返程保障",
        "dishes": "粥、面、鸡蛋、面包和水；不安排专程美食",
        "price": "约¥20–40/人",
        "confidence": "高",
        "address": "按航班和还车/进机场时间决定",
        "reason": "返程日餐饮服从航班，不能用一顿早餐交换误机风险。",
        "source": "返程交通安排",
        "url": "https://jtt.sc.gov.cn/jtt/c101586/2023/3/24/7d66eabfde78487881306b6bbbf9bf89.shtml",
        "caution": "不跨区、不排队、不安排熊猫基地附近早餐；提前确认酒店早餐开始时间。",
    },
]


BOOKING_RULES = {
    "都江堰景区": {
        "status": "国庆按必须预约",
        "class_name": "must",
        "action": "通过“青城山都江堰”或“悦游都江堰”官方渠道实名购票/预约；选择入园时段，出发前再看客流预警。",
        "source": "都江堰官方门票预订页",
        "url": "https://www.djy517.com/online.html?channelCode=mpyd",
    },
    "九寨沟风景区": {
        "status": "必须实名预约",
        "class_name": "must",
        "action": "通过“九寨沟旅游官方平台”实名预约购票；未预约不要前往，携带预约人身份证原件。",
        "source": "九寨沟官方票务信息",
        "url": "https://www.jiuzhai.com/intelligent-service/tickets",
    },
    "成都大熊猫繁育研究基地": {
        "status": "必须实名预约",
        "class_name": "must",
        "action": "成人等普通游客须线上实名预约，提前14日放票；上午票为7:30–12:00。熊猫塔免费但不免票，需另行线上预约。",
        "source": "熊猫基地官方票务服务",
        "url": "https://www.panda.org.cn/cn/service/ticket/",
    },
    "成都大熊猫繁育研究基地（可选）": {
        "status": "必须实名预约",
        "class_name": "must",
        "action": "与D5熊猫基地使用同一官方预约规则；D9只有航班宽裕且预约成功才保留。",
        "source": "熊猫基地官方票务服务",
        "url": "https://www.panda.org.cn/cn/service/ticket/",
    },
    "双桥沟精华段": {
        "status": "必须提前购票/预约",
        "class_name": "must",
        "action": "提前核对四姑娘山官方在线预订和观光车安排；按8:00–15:00入园窗口倒推，不接受到场后再赌票。",
        "source": "四姑娘山官方在线预订/入园通告",
        "url": "https://www.sgns.cn/?presets=preset5",
    },
    "丹巴甲居藏寨": {
        "status": "建议提前购票/预约",
        "class_name": "recommended",
        "action": "国庆按至少提前1天核对官方平台、公众号或景区电话；确认门票、观光车和入园方式，不能只看“全天开放”。",
        "source": "丹巴县政府·甲居藏寨票务管理信息",
        "url": "https://www.danba.gov.cn/tzhj/article/700326",
    },
    "康定/泸定桥收束段": {
        "status": "需购票，建议提前买",
        "class_name": "recommended",
        "action": "泸定桥景区官网提供电子门票；是否需要指定时段预约以当日票务页为准，国庆排队不可控时直接跳过。",
        "source": "泸定桥景区官网电子门票",
        "url": "https://www.scldq.cn/book.html",
    },
}


def booking_rule(spot_name):
    return BOOKING_RULES.get(
        spot_name,
        {
            "status": "无需预约",
            "class_name": "none",
            "action": "不需要景区预约；但公路、垭口、观景台受天气、施工、交通管制和现场停车管理影响。",
            "source": "路线执行判断",
            "url": "https://www.sgnsgeopark.cn/guideline/traffic",
        },
    )


DAY_DETAILS = {
    1: {
        "transport": "去程落地成都双流国际机场，不安排跨城移动；双流机场到市区可核对地铁10号线或网约车，晚间只做补给和晚餐。",
        "timeline": ["抵达后：办理入住、确认D2都江堰交通", "傍晚：春熙路/太古里轻量散步", "晚上：买水、能量棒、晕车药，检查后续动车和租车订单"],
        "meal": "晚餐选酒店周边川菜或小吃，推荐担担面、红油抄手、回锅肉；航班晚点时不跨区找网红店。",
        "risk": "D1的任务是把航班延误风险吸收掉。不要把熊猫基地、宽窄巷子和都江堰硬塞在抵达日。",
        "photo": "太古里适合夜景和建筑线条，手机夜景模式即可，不建议为拍照走太远。",
        "budget": "住宿约¥250–650；晚餐两人约¥120–180；市内交通按¥50–100预留。",
    },
    2: {
        "transport": "成都→都江堰可选地铁/城际；景区内按秦堰楼进、离堆公园出走下坡线，晚上返回成都同一酒店。",
        "timeline": ["08:00左右：成都出发，预留进站和安检", "上午至下午：秦堰楼—二王庙—安澜索桥—鱼嘴—飞沙堰—宝瓶口", "17:00后：灌县古城、南桥，晚餐后返回成都"],
        "meal": "午餐在灌县古城解决，兔头、醪糟粉子蛋、红糖糍粑即可；晚餐回成都吃川菜，不追求景区门口高价套餐。",
        "risk": "都江堰景区面积大且台阶多，先确认入口和返程站点；不要从离堆公园一路上坡走到秦堰楼。",
        "photo": "安澜索桥拍鱼嘴和水利分流，南桥蓝调时段更适合拍倒影；下雨时石阶湿滑。",
        "budget": "门票约¥80/人；往返交通约¥50–150/人；餐饮两人约¥220。",
    },
    3: {
        "transport": "成都东→黄龙九寨站动车，再换景区直通车/预约接驳到漳扎镇；动车和接驳必须分别确认，不要默认下车就有车。",
        "timeline": ["早上：酒店打包早餐，提前到成都东站", "中午：黄龙九寨站下车，核对接驳点和行李", "下午：入住、采购沟内干粮，散步适应海拔，22:00前休息"],
        "meal": "动车上准备面包、坚果、能量棒和水；晚餐选漳扎镇热食，牦牛肉汤锅或藏式面食优先，少酒少油。",
        "risk": "D3只住一晚，必须把D4出沟后的返程票/包车在今天确认；任何交通环节不确定，就减少D4景点。",
        "photo": "抵达日只拍漳扎镇山谷和藏式建筑，避免为了日落跑远，给第二天早入沟留体力。",
        "budget": "动车约¥140/人；接驳约¥50–100/人；沟口住宿约¥450–800；晚餐两人约¥160。",
    },
    4: {
        "transport": "酒店→九寨沟游客中心步行/接驳；入沟后依景区观光车调度游览；15:00左右出沟，接驳或包车前往黄龙九寨站，再乘晚间动车回成都。",
        "timeline": ["07:00：早餐和进沟准备，按预约时段入园", "上午：五花海、珍珠滩瀑布、诺日朗", "下午：长海、五彩池；根据排队在15:00左右出沟", "出沟后：直接去车站，不在沟口临时吃正餐或购物"],
        "meal": "早餐吃饱；午餐用前一晚采购的干粮，补水优先；回成都后再吃热汤和面食，不把景区餐厅作为主要用餐。",
        "risk": "这是全程最紧的一天。不要赌最后一班车衔接；若景区排队、天气或交通异常，立刻删减树正群海等非核心点。",
        "photo": "上午优先五花海和珍珠滩，下午长海、五彩池看天气；雨后路滑，拍照时不要离开栈道。",
        "budget": "九寨沟门票+观光车约¥280/人；出沟接驳约¥50–100/人；返程动车约¥140/人。",
    },
    5: {
        "transport": "成都酒店→熊猫基地→返回酒店取行李→成都取车门店→商超/药店采购→回酒店；D5不再去黄龙。",
        "timeline": ["07:00前：酒店早餐，前往熊猫基地南门或西门", "07:30–11:30：上午票游览产房、活动区、熊猫塔/博物馆按时间取舍", "12:00：熊猫基地或沿线简餐，返回酒店取行李", "14:00左右：成都取车，核对保险、车况、救援电话和还车规则", "15:30–17:30：采购干粮、水、药品、防晒、纸巾，下载阿坝/甘孜离线地图", "晚上：整理车辆和行李，早点休息，为D6争取14:00前到双桥沟游客中心"],
        "meal": "早餐酒店解决；午餐在熊猫基地或返程沿线吃热食；晚餐选择取车点附近川菜，采购完成后不再安排远距离夜游。",
        "risk": "熊猫基地上午票必须预约，12:00后不能继续使用上午入园时段；D5下午取车、采购和车辆检查优先级高于人民公园/宽窄巷子等可选项目。",
        "photo": "熊猫上午活动度通常更高，先看产房和活动区；城市项目只做机动项，不为拍照拖延D6物资准备。",
        "budget": "熊猫基地成人票约¥55/人；成都餐饮两人约¥220；租车押金/保险和D6-D8三天用车以订单为准；补给约¥200–400。",
    },
    6: {
        "transport": "成都取车，经蓉昌高速至映秀，再走G350中国熊猫大道，经卧龙、巴朗山隧道抵达四姑娘山镇；下午完成双桥沟精华段，晚上住镇上。",
        "timeline": ["07:00：取车、加水、检查轮胎和证件", "上午：成都—映秀—卧龙，贝母坪/大雪塘观景点视路况停留", "中午后：巴朗山隧道—猫鼻梁，确认双桥沟预约后入沟", "下午：红杉林—盆景滩—人参果坪，17:00前坐末班观光车出沟", "晚上：四姑娘山镇入住，清淡晚餐，不饮酒、不剧烈运动"],
        "meal": "车上备水、面包、坚果和晕车药；午餐在卧龙或小金沿途解决；双桥沟内自带干粮，晚餐回镇上吃牦牛肉汤锅/菌汤。",
        "risk": "D6虽然是完整小环线的第一天，但进双桥沟有时间门槛：若14:00后仍未到游客中心，取消进沟，改为猫鼻梁和镇上休息，D7不再补双桥沟。",
        "photo": "G350沿线贝母坪、大雪塘、巴朗山隧道口和猫鼻梁是公路雪山机位；双桥沟下午优先红杉林、盆景滩、人参果坪。只在正规停车区停留。",
        "budget": "租车、油费、过路费按三天合计约¥1800–2600预留；双桥沟约¥150/人；镇上住宿约¥500–900；晚餐两人约¥170。",
    },
    7: {
        "transport": "四姑娘山镇→猫鼻梁晨拍→小金/牦牛河谷→丹巴甲居藏寨→八美→雅拉雪山观景台→塔公草原路边→新都桥，约250–280公里，含停靠为全天高强度驾驶。",
        "timeline": ["06:30：猫鼻梁拍四姑娘山晨光，回镇吃早餐", "08:00：经小金前往丹巴，沿牦牛河谷停靠拍红石滩/秋色", "上午至中午：甲居藏寨观景台，游览约1–1.5小时", "午后：丹巴吃饭并买干粮，前往八美、雅拉雪山观景台、疙瘩梁子", "傍晚：塔公草原路边短停，日落前抵达新都桥办理入住"],
        "meal": "必须在丹巴县城吃饱并补水买干粮；丹巴→八美→塔公段不要期待沿途餐馆；晚餐在新都桥镇选择汤锅或川菜。",
        "risk": "D7是小环线最漂亮也最累的一天。甲居、雅拉、疙瘩梁子、塔公不能全部深度停留；若国庆拥堵，优先甲居＋雅拉观景台，取消疙瘩梁子或塔公收费景区。",
        "photo": "猫鼻梁上午顺光；甲居1号观景台拍藏寨全景；雅拉雪山观景台拍雪山和经幡；塔公路边拍木雅金塔与雅拉雪山同框。",
        "budget": "甲居藏寨门票按官方实时价格；新都桥住宿约¥500–1000；餐饮两人约¥250；沿途停车和干粮约¥100。",
    },
    8: {
        "transport": "新都桥→杨树林晨拍→S434/塔北路景观段→红海子（天气好再去）→雅拉山口/康定机场路→斯丁措（晴天可选）→折多塘→康定/泸定→雅康高速→成都还车。",
        "timeline": ["07:00前：新都桥十里杨树长廊晨拍", "上午：沿S434选择红海子、雅拉山口、康定机场路停靠，阴天跳过湖泊倒影点", "中午后：康定/泸定简餐；泸定桥只在排队可控时进入", "下午至傍晚：雅康高速返成都，完成还车并入住机场/成都东站酒店"],
        "meal": "早餐在新都桥酒店或镇上解决；S434沿途备足干粮；康定/泸定吃简餐，晚餐回成都后再安排。",
        "risk": "D8仍是返程日，但不是一早直奔成都：S434沿线只取舍停靠。遇到施工、降雪、管制或预计天黑前无法到成都，立刻放弃后续观景，改走安全可通行路线。",
        "photo": "新都桥杨树长廊必须早拍；红海子看天气，阴天直接跳过；康定机场路拍公路线条要靠边停车并开双闪；机场附近严禁随意放飞无人机。",
        "budget": "新都桥住宿约¥500–1000；S434沿线多数观景点免费，红海子可能有停车/清洁费用；康定/泸定餐饮两人约¥220；成都住宿约¥250–500。",
    },
    9: {
        "transport": "回程从成都天府国际机场起飞，酒店→天府机场按航班提前至少3小时到达；只有15:00后航班且预约成功，才考虑上午熊猫基地。",
        "timeline": ["早航班：早餐后直接机场", "晚航班：上午熊猫基地，12:00前离园", "机场：还留出还车、托运行李、安检和国庆排队时间"],
        "meal": "早餐在酒店或机场解决，不安排跨区餐厅；返程日的优先级是准时和不遗失行李。",
        "risk": "熊猫基地是可选项，不是必须项。航班时间、机场交通和预约任一不确定，就直接去机场。",
        "photo": "熊猫基地上午更适合看活动状态；不要为了拍摄停留到午后，至少给机场交通留足缓冲。",
        "budget": "熊猫基地可选门票约¥55/人；机场交通按¥50–150/人预留。",
    },
}


def hotel_section():
    groups = []
    for area in ("成都", "九寨沟沟口", "四姑娘山", "新都桥"):
        cards = []
        for hotel in [item for item in HOTELS if item["area"] == area]:
            cards.append(
                """<article class="hotel-card">
<div class="hotel-top"><span class="hotel-badge">{badge}</span><span class="score">{score}</span></div>
<h3>{name}</h3>
<p class="hotel-view">{view}</p>
<p><b>位置：</b>{location}</p>
<p><b>新旧：</b>{freshness}</p>
<p><b>价格参考：</b>{booking}</p>
<p class="evidence">证据：{source}</p>
<a class="source-link" href="{url}" target="_blank" rel="noreferrer">打开比价/评价来源 ↗</a>
</article>""".format(**{key: esc(value) for key, value in hotel.items()})
            )
        groups.append('<div class="hotel-group"><h3>{}</h3><div class="hotel-grid">{}</div></div>'.format(esc(area), "".join(cards)))
    return """<section id="hotels" class="section hotel-section">
<div class="section-kicker">独立住宿决策</div>
<h2>酒店全盘对比｜优先风景、位置与高原配套</h2>
<p class="lead">以下是按本次路线筛选的实际住宿候选。价格是国庆前后预算区间，不是承诺价；网页链接用于核对房型、评价和实时库存。新旧筛选以“2022年9月以后开业/装修”为优先，2021年及更早的酒店只保留为停车、连锁或满房备选；“开业新”不等于每个房型都没有磨损，仍要看近期住客图。</p>
<div class="notice"><b>先说结论：</b>成都优先锦著（2024）或LOUIS（2023）；九寨沟只住D3一晚，优先游客中心漫心（2025）；四姑娘山优先悠然牧居（2024），风景优先仰望星空（2024）；D7新都桥优先Ozz·nice5（2024），预算和稳定性选全季（2024）。</div>
{}
<div class="matrix-wrap"><table class="compare-table"><thead><tr><th>区域</th><th>首选</th><th>为什么选它</th><th>什么时候换备选</th><th>预订重点</th></tr></thead><tbody>
<tr><td>成都</td><td class="best">锦著 / LOUIS</td><td>分别是2024开业和2023开业；锦著更稳妥，LOUIS高层景观更强。</td><td>美居只有在确认2024装修属实后再考虑；尼依格罗不按新酒店首选。</td><td>确认房型朝向、隔音、早餐、停车和到成都东站/取车点时间。</td></tr>
<tr><td>九寨沟沟口</td><td class="best">游客中心漫心</td><td>2025开业、距沟口交通节点近，最适合只住D3一晚。</td><td>千古情漫心同为2025新店但需确认接驳；千鹤是2021升级装修的旧备选。</td><td>确认到游客中心接驳、早餐开始时间、寄存和国庆接送安排。</td></tr>
<tr><td>四姑娘山</td><td class="best">悠然牧居</td><td>2024开业，供氧、智能客控、停车和双桥沟出发较均衡。</td><td>仰望星空偏风景；阅山四季为2023开业的稳妥备选。</td><td>确认供氧是否全夜、地暖、热水、停车、早餐和具体房间朝向。</td></tr>
<tr><td>新都桥</td><td class="best">Ozz·nice5</td><td>2024开业，贡嘎视野、地暖、弥散供氧和景观房匹配拍照需求。</td><td>全季2024更稳定但临318可能有噪声；赞蕃2023景观强但离主街远。</td><td>确认D7晚到店、晚餐供应、供氧、地暖、停车和实际观景朝向。</td></tr>
</tbody></table></div>
<div class="long-list"><div class="long-item"><h4>为什么不建议住进九寨沟景区</h4><p>九寨沟执行“沟内游、沟外住”，游客住宿应安排在漳扎镇等沟口区域。把“住沟里”当成预订目标，容易被不规范宣传误导；本路线按沟口酒店执行。</p></div><div class="long-item"><h4>为什么D4不继续住九寨沟</h4><p>你已经明确不想承担两晚沟口高价。D4游完约15:00出沟，直接返成都，D5回到低海拔恢复；代价是D4交通必须提前锁定，不能临时拼车。</p></div><div class="long-item"><h4>景观房不是默认山景</h4><p>酒店页面写“山景/观景”不代表每个房型都有视野。下单前要看房型名称、朝向、楼层和评价图片，必要时给酒店留言确认。</p></div><div class="long-item"><h4>高原配套优先级</h4><p>四姑娘山住宿排序应是安全和恢复能力优先：供氧/地暖、热水、停车、早餐时间，再比较装修和网红拍照点。</p></div></div>
<div class="hotel-rules"><b>预订时逐项确认：</b>具体房型是否正对山景、供氧/地暖是否在房价内、停车是否免费、到景区是否有接驳、早餐开始时间是否赶得上早入沟。</div>
</section>""".format("".join(groups))


def transport_section(trip):
    budget = trip.get("budget", {})
    outbound = trip.get("transport_to_dest", [{}])[0]
    inbound = trip.get("transport_return", [{}])[0]
    return """<section id="transport" class="section">
<div class="section-kicker">路线骨架</div>
<h2>交通与预算</h2>
<div class="notice"><b>抵达：</b>{from_city} → {to_city}，{duration}；{note}</div>
<div class="notice"><b>返程：</b>{from_city2} → {to_city2}，{duration2}；{note2}</div>
<div class="notice"><b>两人预算：</b>约¥{total}，人均约¥{per_person}；住宿预算约¥{hotel}（成都5晚、九寨沟1晚、四姑娘山2晚）。动车、租车和国庆酒店价格以实时订单为准。</div>
<p class="lead">路线核心是：D3进九寨沟，D4游完返成都；D6走G350进入四姑娘山并视时间进双桥沟精华；D7经过丹巴、八美、塔公到新都桥；D8走S434经康定/泸定回成都，完成川西小环线后还车，再前往D9天府机场。</p>
</section>""".format(
        from_city=esc(outbound.get("from")),
        to_city=esc(outbound.get("to")),
        duration=esc(outbound.get("duration")),
        note=esc(outbound.get("note")),
        from_city2=esc(inbound.get("from")),
        to_city2=esc(inbound.get("to")),
        duration2=esc(inbound.get("duration")),
        note2=esc(inbound.get("note")),
        total=esc(budget.get("total")),
        per_person=esc(budget.get("per_person")),
        hotel=esc(budget.get("hotel")),
    )


def itinerary_section(trip):
    cards = []
    for day in trip.get("itinerary", []):
        number = day.get("day_number")
        detail = DAY_DETAILS.get(number, {})
        spot_blocks = []
        for spot in day.get("spots", []):
            booking = booking_rule(spot.get("name", ""))
            spot_blocks.append(
                """<div class="spot-detail"><div class="spot-title"><span class="spot-emoji">{emoji}</span><div><h4>{name}</h4><span class="spot-category">{category}</span></div></div>
<p>{description}</p><div class="spot-facts"><span>⏱ 游览 {duration}分钟</span><span>🎫 门票 ¥{ticket}/人</span><span>🕘 开放：{hours}</span><span class="booking-tag booking-{booking_class}">📌 {booking_status}</span></div>
<div class="booking-inline"><b>预约/购票：</b>{booking_action} <a href="{booking_url}" target="_blank" rel="noreferrer">核对来源 ↗</a></div>
{photo}{pitfall}</div>""".format(
                    emoji=esc(spot.get("emoji", "📍")),
                    name=esc(spot.get("name")),
                    category=esc(spot.get("category")),
                    description=esc(spot.get("description")),
                    duration=esc(spot.get("visit_duration_min")),
                    ticket=esc(spot.get("ticket_price")),
                    hours=esc(spot.get("opening_hours") or "以景区/道路当日公告为准"),
                    booking_class=esc(booking["class_name"]),
                    booking_status=esc(booking["status"]),
                    booking_action=esc(booking["action"]),
                    booking_url=booking["url"],
                    photo=("<div class=\"callout photo\"><b>拍摄：</b>{}</div>".format(esc(spot.get("photo_tip"))) if spot.get("photo_tip") else ""),
                    pitfall=("<div class=\"callout warning\"><b>风险：</b>{}</div>".format(esc(spot.get("pitfall_warning"))) if spot.get("pitfall_warning") else ""),
                )
            )
        hotel = day.get("hotel") or {}
        stay = "{}（{}）".format(hotel.get("name", "不住宿"), hotel.get("area", "")) if hotel else "当天返程，不住宿"
        area = hotel.get("area", "")
        hotel_area = "九寨沟沟口" if "九寨" in area or "漳扎" in area else ("四姑娘山" if "四姑娘" in area else ("新都桥" if "新都桥" in area else "成都"))
        candidates = [item for item in HOTELS if item["area"] == hotel_area][:3]
        hotel_refs = "".join("<li><b>{}</b>：{}；{}</li>".format(esc(item["name"]), esc(item["view"]), esc(item["booking"])) for item in candidates)
        timeline = "".join("<li>{}</li>".format(esc(item)) for item in detail.get("timeline", []))
        meal_rows = []
        for meal_type, meal_items in day.get("meals", {}).items():
            label = {"breakfast": "早餐", "lunch": "午餐", "dinner": "晚餐"}.get(meal_type, meal_type)
            for meal_item in meal_items:
                signature = "、".join(str(x) for x in meal_item.get("signature", []))
                tail = "；推荐：{}".format(signature) if signature else ""
                price = "；约¥{}/人".format(meal_item.get("price_per_person")) if meal_item.get("price_per_person") else ""
                meal_rows.append("<li><b>{}</b> {}{}{} </li>".format(esc(label), esc(meal_item.get("name")), esc(price), esc(tail)))
        meal_raw = "<ul class=\"meal-raw\">{}</ul>".format("".join(meal_rows)) if meal_rows else ""
        cards.append(
            """<article class="day-card" id="day-{number}">
<div class="day-header"><div class="day-number">D{number}</div><div><h3>{theme}</h3><p>{date} · {route}</p></div></div>
<div class="day-content"><div class="day-summary"><b>这一日怎么走：</b>{route_summary}</div>
<div class="detail-columns"><div class="detail-box"><h4>时间线</h4><ul>{timeline}</ul></div><div class="detail-box"><h4>交通安排</h4><p>{transport}</p></div></div>
<div class="spot-grid">{spots}</div>
<div class="detail-columns"><div class="detail-box"><h4>餐饮安排</h4><p>{meal}</p>{meal_raw}</div><div class="detail-box"><h4>预算参考</h4><p>{budget}</p></div></div>
<div class="day-advice"><div><b>安全与取舍：</b>{risk}</div><div><b>拍摄提示：</b>{photo}</div></div>
<div class="stay"><b>住宿：</b>{stay}<br><span>{highlights}</span></div>
<div class="hotel-mini"><h4>本日住宿候选</h4><ul>{hotel_refs}</ul><a href="#hotels">回到酒店全盘对比 ↑</a></div>
<p class="day-note"><b>原始数据备注：</b>{notes}</p></div>
</article>""".format(
                number=esc(number),
                theme=esc(day.get("theme")),
                date=esc(day.get("date")),
                route=esc(day.get("route_summary")),
                route_summary=esc(day.get("route_summary")),
                timeline=timeline,
                transport=esc(detail.get("transport")),
                spots="".join(spot_blocks),
                meal=esc(detail.get("meal")),
                meal_raw=meal_raw,
                budget=esc(detail.get("budget")),
                risk=esc(detail.get("risk")),
                photo=esc(detail.get("photo")),
                stay=esc(stay),
                highlights=esc(hotel.get("highlights", "按当天实际订单确认供氧、地暖、停车和早餐")),
                hotel_refs=hotel_refs or "<li>当天不住宿；请把行李和返程交通作为首要任务。</li>",
                notes=esc(day.get("notes")),
            )
        )
    return """<section id="itinerary" class="section">
<div class="section-kicker">9天8晚·逐日执行版</div>
<h2>每日行程｜按时间、交通、吃住和取舍展开</h2>
<p class="lead">这一版不是景点清单，而是可以照着执行的日程：每一天都拆出时间线、交通衔接、景点票务、餐饮、住宿、预算和“时间不够时删什么”。九寨沟只住D3一晚，D4游完返回成都；D6-D8补回完整川西小环线，但把高海拔景点做成可删减短停。</p>
<div class="day-list">{}</div>
</section>""".format("".join(cards))


def overview_section(trip):
    return """<section id="overview" class="section">
<div class="section-kicker">先看决策逻辑</div>
<h2>这条路线到底优化了什么</h2>
<p class="lead">原行程的问题不是景点少，而是把九寨沟、四姑娘山和川西小环线的每个点都按深度游安排，导致国庆期间驾驶、预约、住宿换房和返程风险同时上升。本版保留完整小环线的关键节点，但把每站改成短停和可删减的景观带，避免“路线完整、执行崩盘”。</p>
<div class="long-list"><div class="long-item"><h4>保留：九寨沟一晚</h4><p>D3进沟口，D4早入沟看Y字精华，15:00左右出沟后直接返成都。只住一晚，把高价住宿和高原连续暴走压缩到可控范围。</p></div><div class="long-item"><h4>保留：四姑娘山＋双桥沟</h4><p>D6走G350熊猫大道，若14:00前到游客中心进双桥沟精华；若时间不足就取消进沟，D7不补，把小环线主线交给丹巴和新都桥。</p></div><div class="long-item"><h4>补回：完整川西小环线</h4><p>D7经过猫鼻梁、丹巴甲居、牦牛河谷、雅拉雪山、八美、塔公、新都桥；D8再走新都桥—S434—康定/泸定—成都，形成不回头的景观环线。</p></div><div class="long-item"><h4>控制方式：景点可删、主线不乱</h4><p>D7优先甲居＋雅拉，D8优先新都桥晨拍＋安全返程；疙瘩梁子、塔公收费区、红海子、斯丁措和泸定桥都按天气、排队和到达时间取舍。</p></div></div>
<div class="timeline-strip"><div class="timeline-step"><b>D1–D2</b>双流落地＋成都/都江堰，住宿不换</div><div class="timeline-step"><b>D3–D5</b>九寨沟一晚＋D5熊猫基地、取车、采购</div><div class="timeline-step"><b>D6–D7</b>G350进四姑娘山＋丹巴/八美/塔公/新都桥</div><div class="timeline-step"><b>D8–D9</b>S434收束小环线＋天府机场返程</div></div>
</section>"""


def transport_detail_section():
    rows = [
        ("D1", "双流机场→成都酒店", "地铁10号线/网约车", "以航班为准", "双流离市区更近；只做抵达缓冲"),
        ("D2", "成都↔都江堰", "地铁/城际＋景区步行", "单程约1–1.5小时", "秦堰楼进、离堆公园出"),
        ("D3", "成都东→黄龙九寨站", "动车，提前12306购票", "约2小时", "到站再换接驳，不默认有车"),
        ("D3", "黄龙九寨站→沟口", "景区直通车/预约接驳", "约1.5小时", "确认下车点和行李安排"),
        ("D4", "沟口→九寨沟景区", "步行/酒店接驳＋观光车", "早入沟", "按Y字精华走，不回头"),
        ("D4", "沟口→黄龙九寨站→成都", "接驳/包车＋动车", "下午出沟后衔接", "必须提前锁定，时间不足删景点"),
        ("D5", "成都熊猫基地→取车→采购", "市内打车/网约车＋租车", "上午景点，下午准备", "熊猫上午票，取车和物资优先"),
        ("D6", "成都→四姑娘山镇", "租车自驾，经映秀/卧龙", "按国庆路况预留全天", "不走夜路，猫鼻梁可取消"),
        ("D8", "新都桥→S434→康定/泸定→成都", "租车自驾，成都还车", "按国庆路况预留全天", "观景点短停，天气/施工异常即改线"),
        ("D9", "成都酒店→天府机场", "地铁18号线快线/网约车", "至少提前3小时到机场", "天府距离市区更远；熊猫基地只在航班宽裕时安排"),
    ]
    body = "".join("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(*(esc(x) for x in row)) for row in rows)
    return """<section id="transport-detail" class="section">
<div class="section-kicker">逐段交通</div>
<h2>交通执行表｜每一段都知道怎么接</h2>
<div class="matrix-wrap"><table class="compare-table"><thead><tr><th>日期</th><th>路段</th><th>方式</th><th>时间</th><th>执行重点</th></tr></thead><tbody>{}</tbody></table></div>
<div class="notice"><b>交通底线：</b>高原和国庆期间不把导航最短时间当成承诺；山路不走夜路，返程不压到航班当天，任何衔接不确定都通过删减景点解决。</div>
</section>""".format(body)


def avoid_section(trip):
    items = [
        ("D4进九寨沟前没锁返程", "D3晚确认动车/包车，D4约15:00出沟；不确定就删树正群海等非核心点。"),
        ("把九寨沟住宿订在景区里面", "按官方“沟内游、沟外住”规则，住漳扎镇沟口，不相信模糊的“景区内住宿”宣传。"),
        ("D6下午抵达四姑娘山还进双桥沟", "D6只转场和入住，D7完整游双桥沟。"),
        ("国庆把丹巴、新都桥、S434全部深度游", "完整经过小环线关键节点，但每站短停；优先甲居、雅拉、新都桥晨拍，其他点按路况删减。"),
        ("高原第一晚喝酒、剧烈运动、长时间洗澡", "保暖、清淡、早点休息，出现明显不适及时就医。"),
        ("把黄龙临时塞进D5", "只有专车、预约和后续车票全部确认才考虑；默认不去。"),
        ("熊猫基地放在早航班前", "只有15:00后航班且预约成功才去，否则直接机场。"),
        ("只看酒店总评分不看房型", "逐项确认朝向、楼层、山景是否真实、供氧/地暖和停车。"),
        ("九寨沟只住一晚却选离游客中心很远的酒店", "优先沟口效率；若住远处，必须把接驳和早餐时间算进去。"),
        ("以景区门票价格推算全部成本", "把动车、接驳、租车、油费、过路费、停车和国庆涨价单独列出。"),
        ("动车到站后再找接驳", "提前问清黄龙九寨站接驳点、末班时间和行李规则。"),
        ("景区午餐完全依赖现场", "九寨沟和双桥沟都自带能量棒、面包和水，先解决体力再拍照。"),
        ("国庆早上还睡到自然醒", "D6进山、D7进双桥沟、D4九寨沟都要早起，早出发是避堵和避排队的核心。"),
        ("只准备一件薄外套", "成都、沟口、垭口温差大，带抓绒、冲锋衣或轻薄羽绒和防滑鞋。"),
        ("为了观景台在弯道停车", "只用正规停车区，猫鼻梁天气和路况不合适就取消。"),
        ("把D8返程当成最后一个景点日", "D8的任务是白天安全返成都并完成还车，不追加路线。"),
        ("租车只看日租价", "确认取还车门店、营业时间、保险、押金、车型、雪山路况适配和夜间还车规则。"),
        ("把天气预报当成确定条件", "出发前7天、3天、当天分别复核景区公告和道路管制。"),
    ]
    body = "".join("<div class=\"long-item\"><h4>{}</h4><p>✅ {}</p></div>".format(esc(wrong), esc(right)) for wrong, right in items)
    return """<section id="avoid" class="section"><div class="section-kicker">风险管理</div><h2>避坑清单｜不是提醒，是执行规则</h2><p class="lead">这次行程的风险主要来自国庆拥堵、高原体力、交通衔接和酒店宣传信息不对称。下列规则建议直接复制到出发群里。</p><div class="long-list">{}</div></section>""".format(body)


def budget_section(trip):
    budget = trip.get("budget", {})
    rows = "".join("<tr><td>{}</td><td>{}</td><td>¥{}</td><td>{}</td></tr>".format(esc(item.get("category")), esc(item.get("item")), esc(item.get("amount")), esc(item.get("note"))) for item in budget.get("details", []))
    return """<section id="budget" class="section"><div class="section-kicker">钱花在哪里</div><h2>预算估算｜两人9天8晚</h2><div class="notice"><b>当前估算：</b>两人约¥{total}，人均约¥{per_person}；不含已购机票和大额购物。酒店只住九寨沟一晚后，沟口住宿减少，但成都增加恢复住宿，整体不是简单地把一晚房费全部省掉。</div><div class="matrix-wrap"><table class="compare-table"><thead><tr><th>类别</th><th>包含内容</th><th>估算</th><th>备注</th></tr></thead><tbody>{rows}</tbody></table></div><div class="long-list"><div class="long-item"><h4>最容易超支</h4><p>国庆酒店、租车车型和D4九寨沟返成都接驳。优先提前锁定不可替代的交通和沟口酒店，餐饮反而容易控制。</p></div><div class="long-item"><h4>可以压缩</h4><p>成都酒店可选美居，九寨沟满房时比较千鹤和智选假日；不要为了省几百元把沟口住址换到远处再增加接驳时间。</p></div><div class="long-item"><h4>不要漏算</h4><p>停车费、景区干粮、行李寄存、司机等待费、租车保险和国庆临时改签成本。</p></div><div class="long-item"><h4>付款顺序</h4><p>先交通票和景区预约，再酒店，再租车；每天把取消规则截图留存，避免只记在聊天记录里。</p></div></div></section>""".format(total=esc(budget.get("total")), per_person=esc(budget.get("per_person")), rows=rows)


def preparation_section(trip):
    weather = trip.get("weather", {})
    return """<section id="preparation" class="section"><div class="section-kicker">出发前与随身物品</div><h2>准备清单｜按时间和场景准备</h2><div class="detail-columns"><div class="detail-box"><h4>出发前7天</h4><ul><li>复核九寨沟、双桥沟开放与预约规则。</li><li>确认D3动车、黄龙九寨站接驳、D4返程动车/包车。</li><li>锁定沟口酒店具体房型和四姑娘山供氧/地暖。</li><li>确认租车门店、车型、保险、取还车时间。</li></ul></div><div class="detail-box"><h4>出发前3天</h4><ul><li>看道路管制、国庆车流和山路天气。</li><li>把身份证、驾驶证、订单和联系人离线保存。</li><li>购买干粮、晕车药、充电宝、保温杯。</li><li>把D4和D8设为不可随意加点的交通日。</li></ul></div></div><div class="detail-columns"><div class="detail-box"><h4>衣物与安全</h4><p>{clothing}</p><p><b>天气判断：</b>{temp}</p><p><b>注意：</b>{precautions}</p></div><div class="detail-box"><h4>每天车上固定放置</h4><ul><li>水、面包、坚果、能量棒、纸巾和垃圾袋</li><li>墨镜、防晒霜、帽子、抓绒、冲锋衣/轻薄羽绒</li><li>晕车药、常用药、充电线、移动电源</li><li>纸质/离线版订单、身份证和驾驶证复印件</li></ul></div></div><div class="notice"><b>高原不适处理：</b>不要用“再坚持一下”替代判断。出现持续头痛、明显恶心、胸闷、呼吸困难或意识异常，停止游玩并及时就医；路线安排服从现场安全。</div></section>""".format(clothing=esc(weather.get("clothing")), temp=esc(weather.get("temp_range")), precautions=esc(weather.get("precautions")))


def food_section():
    cards = []
    for item in FOOD_GUIDE:
        cards.append(
            """<article class="food-card">
<div class="food-top"><span class="food-day">{day}</span><span class="food-confidence confidence-{confidence_class}">证据：{confidence}</span></div>
<div class="food-area">{area} · {type}</div><h3>{name}</h3>
<p class="food-dishes"><b>建议点：</b>{dishes}</p>
<p><b>位置：</b>{address}</p><p><b>预算：</b>{price}</p>
<p class="food-reason"><b>为什么放进路线：</b>{reason}</p>
<p class="evidence">核查来源：{source}</p>
<p class="food-caution"><b>到店规则：</b>{caution}</p>
<a class="source-link" href="{url}" target="_blank" rel="noreferrer">打开核查来源 ↗</a>
</article>""".format(
                day=esc(item["day"]), area=esc(item["area"]), type=esc(item["type"]), name=esc(item["name"]),
                dishes=esc(item["dishes"]), address=esc(item["address"]), price=esc(item["price"]),
                reason=esc(item["reason"]), source=esc(item["source"]), caution=esc(item["caution"]),
                url=item["url"], confidence=esc(item["confidence"]),
                confidence_class={"高": "high", "中": "medium", "现场": "onsite"}.get(item["confidence"], "onsite"),
            )
        )
    return """<section id="food" class="section food-section">
<div class="section-kicker">全网餐饮核查</div><h2>吃饭安排｜本地味优先，广告内容不采信</h2>
<p class="lead">这部分把每个用餐节点单独拆出来：能找到官方老字号、地方政府名单或地图实体信息的，才给出具体店名；川西乡镇公开资料不足的地方，只给可靠菜系和现场筛选规则，不把一篇达人笔记或企业软文包装成“必吃”。</p>
<div class="notice food-notice"><b>筛选结论：</b>成都、都江堰可以锁定老字号/地方店；九寨沟、四姑娘山、新都桥的重点是牦牛汤锅、藏餐和热食，但店铺营业、价格和出品波动大，建议到店看菜单和客流。<br><b>明确排除：</b>企业博客式推广稿、招商/采购软文、单篇达人探店、“必吃榜”标题、强推歌舞宴和模糊套餐；这些只作为反向线索，不作为推荐证据。</div>
<div class="food-legend"><span><b>高</b> 官方老字号/政府或官方旅游门户</span><span><b>中</b> 地图实体＋独立资料</span><span><b>现场</b> 公开资料不足，按规则选店</span></div>
<div class="food-grid">{}</div>
<div class="matrix-wrap"><table class="compare-table"><thead><tr><th>日期</th><th>用餐策略</th><th>优先吃什么</th><th>不要做什么</th></tr></thead><tbody>
<tr><td>D1</td><td>抵达后就近</td><td>钟水饺/老字号小吃或酒店附近家常川菜</td><td>不为网红店跨区、不在晚到时排队</td></tr>
<tr><td>D2</td><td>都江堰午餐，晚餐回成都</td><td>尤兔头；古城少量醪糟粉子蛋、红糖糍粑</td><td>不吃景区门口不明套餐</td></tr>
<tr><td>D3</td><td>沟口只吃一顿热食</td><td>清汤牦牛肉/藏式面食</td><td>不买歌舞宴、野生鱼、虫草松茸加价菜</td></tr>
<tr><td>D4</td><td>景区带干粮，返成都后再吃</td><td>面包、坚果、温水；晚间热汤/面</td><td>不让景区排队影响返程车</td></tr>
<tr><td>D5</td><td>熊猫基地和取车之间就近</td><td>少油少辣的川菜、豆花、面饭</td><td>不为拍照餐厅拖延采购和车况检查</td></tr>
<tr><td>D6</td><td>沿线快吃，四姑娘山晚餐</td><td>面/小炒；晚餐清汤牦牛肉或菌汤</td><td>不为吃饭绕路，不饮酒</td></tr>
<tr><td>D7</td><td>丹巴吃饱再进八美/新都桥</td><td>丹巴藏餐、火烧子馍馍、牦牛汤锅</td><td>不期待雅拉—塔公沿线稳定餐馆</td></tr>
<tr><td>D8–D9</td><td>返程优先准时</td><td>康定凉粉/牦牛杂汤；成都老字号或酒店/机场早餐</td><td>不跨区找火锅，不拿早餐换误机风险</td></tr>
</tbody></table></div>
</section>""".format("".join(cards))


def booking_section(trip):
    rows = []
    seen = set()
    for day in trip.get("itinerary", []):
        day_number = day.get("day_number")
        for spot in day.get("spots", []):
            name = spot.get("name", "")
            if name in seen:
                continue
            seen.add(name)
            rule = booking_rule(name)
            rows.append(
                "<tr><td>D{}</td><td><b>{}</b></td><td><span class=\"booking-table-tag booking-{}\">{}</span></td><td>{}</td><td>{}<br><a class=\"source-link\" href=\"{}\" target=\"_blank\" rel=\"noreferrer\">{} ↗</a></td></tr>".format(
                    esc(day_number), esc(name), esc(rule["class_name"]), esc(rule["status"]),
                    esc(rule["action"]), esc(rule["source"]), rule["url"], esc(rule["source"]),
                )
            )
    return """<section id="booking" class="section booking-section">
<div class="section-kicker">预约与购票管理</div><h2>所有景点预约/购票状态｜按这张表执行</h2>
<p class="lead">这里把行程中的所有景点和景观节点逐一列出。不要把“预约”与“开放时间”“买票”“道路管制”混为一谈：收费景区要看预约/购票，免费观景台不需要预约，但可能因天气、施工、停车或客流管控无法进入。</p>
<div class="notice"><b>本次真正必须优先锁定的项目：</b>九寨沟、成都大熊猫繁育研究基地、双桥沟；都江堰国庆按必须预约处理。甲居藏寨和泸定桥属于提前购票/预约更稳妥，其他公路、垭口和开放式观景点不需要预约。</div>
<div class="booking-legend"><span class="booking-table-tag booking-must">必须预约/购票</span><span class="booking-table-tag booking-recommended">建议提前预约/购票</span><span class="booking-table-tag booking-none">无需预约</span></div>
<div class="matrix-wrap"><table class="compare-table booking-table"><thead><tr><th>日期</th><th>景点/节点</th><th>状态</th><th>执行动作</th><th>官方/核查来源</th></tr></thead><tbody>{}</tbody></table></div>
<div class="long-list"><div class="long-item"><h4>建议建立预约日历</h4><p>D1到成都后就把D2都江堰、D4九寨沟、D5熊猫基地、D6双桥沟和D7甲居的订单/预约截图保存到手机离线相册。预约成功不等于可以晚到，入园时间、身份证和接驳同样要核对。</p></div><div class="long-item"><h4>预约失败怎么办</h4><p>九寨沟和熊猫基地没有预约不进；双桥沟没有票就取消景区内游览；都江堰满额则改为灌县古城/南桥和成都城市活动；甲居、泸定桥可以按时间直接删掉。</p></div></div>
</section>""".format("".join(rows))


def hours_section(trip):
    rows = []
    for day in trip.get("itinerary", []):
        for spot in day.get("spots", []):
            booking = booking_rule(spot.get("name", ""))
            hours = spot.get("opening_hours") or "以景区/道路当日公告为准"
            ticket = "¥{}".format(spot.get("ticket_price")) if spot.get("ticket_price") is not None else "以现场为准"
            rows.append("<tr><td>D{}</td><td>{}</td><td>{}</td><td><b>{}</b></td><td><span class=\"booking-table-tag booking-{}\">{}</span></td><td>{}</td></tr>".format(esc(day.get("day_number")), esc(spot.get("name")), esc(spot.get("category")), esc(hours), esc(booking["class_name"]), esc(booking["status"]), esc(ticket)))
    return """<section id="hours" class="section"><div class="section-kicker">景点时间管理</div><h2>景点营业/入园时间速查</h2><p class="lead">把景点时间单独列出来，避免把“全天可到达的观景台”和“有入园时段的收费景区”混为一谈。收费景区按预约时段执行，公路和观景台按道路、天气、现场管理执行。</p><div class="matrix-wrap"><table class="compare-table"><thead><tr><th>日期</th><th>景点/节点</th><th>类型</th><th>营业/入园时间</th><th>预约状态</th><th>票价参考</th></tr></thead><tbody>{}</tbody></table></div><div class="notice"><b>临行规则：</b>九寨沟、双桥沟、熊猫基地和都江堰要重新核对官方预约页面；甲居和泸定桥要看实时票务；“全天”只表示理论可到达，不代表夜间适合停车、拍摄或翻越垭口。</div></section>""".format("".join(rows))


def research_section():
    sources = [
        ("双流机场官方交通", "去程机场交通重点核对地铁10号线、航站楼和末班时间。", "https://www.cdairport.com/traffic3.aspx?t=36"),
        ("四川省交通运输厅·天府机场", "回程天府机场可核对地铁18号线和机场接驳。", "https://jtt.sc.gov.cn/jtt/c101586/2023/3/24/7d66eabfde78487881306b6bbbf9bf89.shtml"),
        ("九寨沟官方开放公告", "核对全域开放、景区管理和临时调整。", "https://www.jiuzhai.com/news/notice/11290-2026-07-29-02-04-43"),
        ("九寨沟官方开放时间", "核对旺季入园和18:00前离沟规则；景区内禁止住宿。", "https://www.jiuzhai.com/news/notice/11001-2026-03-23-01-36-44"),
        ("九寨沟县政府·国庆出游提示", "核对阿坝旅游网预约、黄龙九寨站接驳和官方咨询入口。", "https://www.jzg.gov.cn/jzgrmzf/c100051/202509/9441662374df478f93fbb7192c0f4b0f.shtml"),
        ("成都熊猫基地官方开放时间", "核对3—10月上午票7:30—12:00、预约、门票和清园时间。", "https://www.panda.org.cn/cn/service/opentime/"),
        ("成都熊猫基地官方票务", "核对线上实名预约、提前14日预订、成人票55元和证件要求。", "https://www.panda.org.cn/cn/service/ticket/"),
        ("四姑娘山官方入园时间", "双桥沟目前按8:00–15:00入园窗口规划，国庆仍需临行复核。", "https://www.sgnsgeopark.cn/trends/notice/896-2026-04-07-06-36-51"),
        ("四姑娘山官方交通指引", "核对成都—卧龙—四姑娘山自驾主线和公共交通入口。", "https://www.sgnsgeopark.cn/guideline/traffic"),
        ("阿坝州道路信息", "核对G350巴朗山隧道、冬季/施工期临时管制信息；出发前要查最新公告。", "https://abazhou.gov.cn/abazhou/c109697/202601/f502e238b878418699c51d31e530fe50.shtml"),
        ("都江堰官方门票预订", "核对实名购票、入园时段、开放时间和国庆客流预警。", "https://www.djy517.com/online.html?channelCode=mpyd"),
        ("丹巴县政府·甲居藏寨", "核对智慧票务、身份证/二维码核验和临时入园管理。", "https://www.danba.gov.cn/tzhj/article/700326"),
        ("泸定桥景区官网", "核对夏秋开放时间、停止售票时间和天气影响。", "https://www.scldq.cn/book.html"),
        ("道孚县政府·墨石公园", "核对八美墨石公园位置、海拔和景观节点；本版将其设为可选而非硬塞。", "https://www.gzdf.gov.cn/bmjq/article/693724"),
        ("康定市政府·新都桥节假日保障", "核对新都桥重点拥堵点、停车和假期服务信息。", "https://www.kangding.gov.cn/xzdt/article/711506"),
        ("2026川西小环线路况交叉参考", "用于补充路线距离、路段体验和自驾取舍，但不替代官方道路公告。", "https://travel.sina.cn/2026-06-29/detail-inieznpi0328649.d.html?vt=4"),
    ]
    cards = "".join("<div class=\"long-item\"><h4>{}</h4><p>{}</p><a class=\"source-link\" href=\"{}\" target=\"_blank\" rel=\"noreferrer\">打开来源 ↗</a></div>".format(esc(title), esc(note), url) for title, note, url in sources)
    return """<section id="research" class="section"><div class="section-kicker">全网核查记录</div><h2>旅行攻略依据｜官方公告＋路线交叉搜索</h2><p class="lead">攻略不是只按单一平台的推荐生成。本版把机场、景区、交通、地方政府和路线体验分开核查：官方来源负责开放时间、预约、机场和道路规则；路线类资料只用于补充距离、停车和景观取舍，并在页面中标注“出发前复核”。</p><div class="long-list">{}</div><div class="notice"><b>时间敏感项：</b>2026年9月26日至10月4日正值国庆前后，动车余票、酒店房价、景区预约、S434施工组织和天气都可能变化；出发前7天、3天、当天各复核一次。</div></section>""".format(cards)


def render(trip):
    css = """
:root{--ink:#24312d;--muted:#6c7a75;--green:#2f6f5e;--light:#eef5f0;--gold:#c38b3d;--line:#dce8df;--paper:#fbfdfb}
*{box-sizing:border-box}body{margin:0;background:linear-gradient(135deg,#f3f8f4,#fffdf8);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;line-height:1.7}a{color:inherit}.wrap{max-width:1160px;margin:0 auto;padding:0 22px}.hero{padding:68px 0 48px;background:linear-gradient(120deg,#dcefe2,#f8efe0);border-bottom:1px solid var(--line)}.eyebrow,.section-kicker{letter-spacing:.14em;text-transform:uppercase;font-size:12px;color:var(--green);font-weight:700}.hero h1{font-size:clamp(32px,5vw,58px);line-height:1.15;margin:12px 0}.hero p{max-width:800px;color:#50605a;font-size:18px}.meta{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}.pill{background:#ffffffb8;border:1px solid #fff;padding:7px 13px;border-radius:20px;font-size:13px}.nav{position:sticky;top:0;z-index:3;background:#ffffffeb;backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}.nav .wrap{display:flex;gap:20px;overflow:auto}.nav a{padding:13px 0;text-decoration:none;white-space:nowrap;font-size:14px;color:var(--muted)}.section{padding:54px 0;border-bottom:1px solid var(--line)}h2{font-size:30px;line-height:1.3;margin:7px 0 12px}h3{line-height:1.35}.lead{color:var(--muted);max-width:900px}.notice,.hotel-rules{padding:16px 18px;background:var(--light);border-left:4px solid var(--green);margin:22px 0}.hotel-group{margin-top:30px}.hotel-group>h3{margin-bottom:12px;color:var(--green)}.hotel-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.hotel-card{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:19px;box-shadow:0 8px 24px #2f6f5e0d}.hotel-card h3{margin:12px 0 8px;font-size:20px}.hotel-card p{margin:7px 0;font-size:14px}.hotel-top{display:flex;justify-content:space-between;align-items:center}.hotel-badge{color:#fff;background:var(--green);border-radius:14px;padding:3px 9px;font-size:12px}.score{font-weight:700;color:var(--gold)}.hotel-view{font-weight:600;color:#405d52}.evidence{font-size:12px!important;color:var(--muted)}.source-link{display:inline-block;margin-top:8px;color:var(--green);font-size:13px;font-weight:700}.day-list{display:grid;gap:14px}.day-card{display:grid;grid-template-columns:110px 1fr;background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden}.day-label{background:var(--green);color:#fff;font-size:28px;font-weight:800;padding:20px 14px;text-align:center}.day-label span{display:block;font-size:12px;font-weight:400;margin-top:8px}.day-body{padding:18px 22px}.day-body h3{margin:0 0 4px}.route{color:var(--green);font-weight:600;margin:4px 0 10px}.day-body ul{margin:8px 0;padding-left:20px}.stay{background:#f7f3e9;padding:8px 12px;border-radius:8px;font-size:14px}.day-note{color:var(--muted);font-size:13px;margin-bottom:0}.footer{padding:38px 0 70px;color:var(--muted);font-size:13px}.footer a{color:var(--green)}@media(max-width:820px){.hotel-grid{grid-template-columns:1fr 1fr}}@media(max-width:560px){.wrap{padding:0 15px}.hero{padding:45px 0 34px}.hero p{font-size:16px}.hotel-grid{grid-template-columns:1fr}.day-card{grid-template-columns:72px 1fr}.day-label{font-size:23px;padding:16px 6px}.day-body{padding:15px}.day-body ul{font-size:14px}}
.day-header{display:flex;gap:18px;align-items:center;padding:22px 24px;background:linear-gradient(120deg,#356f5d,#9bc5a6);color:#fff}.day-number{font-size:34px;font-weight:800;min-width:76px}.day-header h3{margin:0;font-size:21px}.day-header p{margin:5px 0 0;font-size:13px;opacity:.9}.day-content{padding:22px 24px}.day-summary{padding:12px 15px;background:#eef7f0;border-left:4px solid var(--green);margin-bottom:18px}.detail-columns{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:14px 0}.detail-box{background:#fbfdfb;border:1px solid var(--line);border-radius:12px;padding:15px}.detail-box h4,.hotel-mini h4{margin:0 0 8px;color:var(--green)}.detail-box p{margin:0;font-size:14px}.detail-box ul{margin:0;padding-left:20px;font-size:14px}.meal-raw{margin-top:10px!important;padding-top:8px;border-top:1px dashed var(--line);font-size:12px!important;color:var(--muted)}.meal-raw li{margin:3px 0}.spot-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin:16px 0}.spot-detail{border:1px solid var(--line);border-radius:13px;padding:15px;background:#fff}.spot-title{display:flex;gap:10px;align-items:center}.spot-emoji{font-size:27px}.spot-detail h4{margin:0;font-size:17px}.spot-category{font-size:12px;color:var(--muted)}.spot-detail p{font-size:14px;margin:10px 0}.spot-facts{display:flex;flex-wrap:wrap;gap:7px}.spot-facts span{font-size:12px;padding:3px 8px;border-radius:10px;background:#f3f6f3;color:#52645b}.callout{font-size:12px;margin-top:10px;padding:8px 10px;border-radius:8px}.callout.photo{background:#fff8e7;color:#805b1c}.callout.warning{background:#fff1ef;color:#9a4237}.day-advice{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:15px 0;font-size:13px}.day-advice div{padding:11px 13px;background:#f8f3e9;border-radius:10px}.hotel-mini{margin-top:16px;padding:15px;background:#f5f8ff;border-radius:12px}.hotel-mini ul{margin:0 0 5px;padding-left:20px;font-size:13px}.hotel-mini a{font-size:12px;color:var(--green);font-weight:700}.day-note{margin-top:14px;padding-top:12px;border-top:1px dashed var(--line)}.matrix-wrap{overflow:auto;margin-top:20px}.compare-table{width:100%;border-collapse:collapse;min-width:760px;background:#fff}.compare-table th,.compare-table td{padding:12px 13px;border:1px solid var(--line);vertical-align:top;text-align:left;font-size:13px}.compare-table th{background:#edf5ef;color:var(--green)}.compare-table .best{background:#fff7e5;font-weight:700}.long-list{display:grid;grid-template-columns:1fr 1fr;gap:12px}.long-item{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px;font-size:14px}.long-item h4{margin:0 0 6px;color:var(--green)}.long-item p{margin:0;color:#52645b}.timeline-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:20px 0}.timeline-step{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px;font-size:13px}.timeline-step b{display:block;color:var(--green);margin-bottom:5px}.small-note{font-size:12px;color:var(--muted)}@media(max-width:820px){.spot-grid,.detail-columns,.day-advice,.long-list{grid-template-columns:1fr}}@media(max-width:560px){.day-header{padding:18px 15px;gap:10px}.day-number{font-size:26px;min-width:55px}.day-content{padding:16px 15px}.timeline-strip{grid-template-columns:1fr 1fr}}
.section{max-width:1160px;width:100%;margin:0 auto;padding:52px 22px}.day-card{display:block;box-shadow:0 10px 26px rgba(36,49,45,.08);transition:transform .2s ease,box-shadow .2s ease}.day-card:hover{transform:translateY(-2px);box-shadow:0 14px 32px rgba(36,49,45,.13)}.hotel-card{transition:transform .2s ease,box-shadow .2s ease}.hotel-card:hover{transform:translateY(-3px);box-shadow:0 14px 30px rgba(47,111,94,.14)}.hotel-section,.day-list,.matrix-wrap{scroll-margin-top:70px}.nav .wrap{max-width:1160px;margin:0 auto}.notice{border-radius:10px}.compare-table tr:nth-child(even) td{background:#fbfdfb}.hotel-rules{border-radius:10px}.footer{max-width:1160px;margin:0 auto}.section-kicker{margin-bottom:3px}
.section h2{letter-spacing:-.02em}.day-list{gap:22px}.hotel-group{padding-top:8px}.hotel-card h3{letter-spacing:-.01em}.spot-detail{box-shadow:0 5px 18px rgba(36,49,45,.04)}@media(max-width:560px){.section{padding:38px 15px}.section h2{font-size:25px}.day-list{gap:16px}.hotel-card{padding:16px}.compare-table th,.compare-table td{padding:9px 10px;font-size:12px}}
.food-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin:22px 0}.food-card{background:#fff;border:1px solid var(--line);border-radius:15px;padding:18px;box-shadow:0 7px 22px rgba(36,49,45,.05)}.food-card h3{margin:7px 0 8px;font-size:20px}.food-card p{font-size:14px;margin:7px 0}.food-top{display:flex;justify-content:space-between;gap:10px;align-items:center}.food-day{font-size:12px;color:var(--green);font-weight:800}.food-confidence{font-size:12px;border-radius:12px;padding:3px 9px}.confidence-high{background:#e4f2e8;color:#246249}.confidence-medium{background:#fff3d9;color:#805b1c}.confidence-onsite{background:#f0f1f0;color:#5b6862}.food-area{font-size:12px;color:var(--muted);margin-top:8px}.food-dishes{color:#405d52}.food-reason{padding-top:8px;border-top:1px dashed var(--line)}.food-caution{background:#fff8e7;padding:9px 11px;border-radius:9px;color:#705526}.food-legend{display:flex;flex-wrap:wrap;gap:10px;margin:15px 0}.food-legend span{font-size:12px;background:#fff;border:1px solid var(--line);border-radius:12px;padding:5px 10px;color:var(--muted)}.food-legend b{color:var(--green)}.food-notice{line-height:1.8}@media(max-width:820px){.food-grid{grid-template-columns:1fr}}@media(max-width:560px){.food-card{padding:15px}.food-card h3{font-size:18px}}
.booking-tag,.booking-table-tag{font-weight:700}.booking-must{background:#ffe9e5!important;color:#9a3d32!important}.booking-recommended{background:#fff3d9!important;color:#805b1c!important}.booking-none{background:#e9f4ec!important;color:#246249!important}.booking-inline{margin-top:10px;padding:9px 11px;border-radius:9px;background:#f6f8f6;color:#4f6159;font-size:12px}.booking-inline a{color:var(--green);font-weight:700;text-decoration:none;margin-left:4px}.booking-legend{display:flex;flex-wrap:wrap;gap:10px;margin:15px 0}.booking-legend span{display:inline-block;border-radius:12px;padding:5px 10px;font-size:12px}.booking-table{min-width:980px}.booking-table-tag{display:inline-block;border-radius:11px;padding:3px 8px;font-size:12px;white-space:nowrap}
"""
    budget = trip.get("budget", {})
    meta = "".join(
        "<span class=\"pill\">{}：{}</span>".format(esc(label), esc(value))
        for label, value in (
            ("日期", "{} 至 {}".format(trip.get("dates", {}).get("start"), trip.get("dates", {}).get("end"))),
            ("人数", "{}人".format(trip.get("persons"))),
            ("预算", "约¥{} / 两人".format(budget.get("total"))),
            ("九寨沟", "只住1晚"),
        )
    )
    html_doc = [
        "<!doctype html><html lang=\"zh-CN\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>{}</title><style>{}</style></head><body>".format(esc(trip.get("title")), css),
        "<header class=\"hero\"><div class=\"wrap\"><div class=\"eyebrow\">Sichuan · trip decision page</div><h1>{}</h1><p>{}</p><div class=\"meta\">{}</div></div></header>".format(esc(trip.get("title")), esc(trip.get("subtitle")), meta),
        "<nav class=\"nav\"><div class=\"wrap\"><a href=\"#overview\">优化逻辑</a><a href=\"#transport-detail\">交通执行表</a><a href=\"#booking\">预约购票</a><a href=\"#hours\">营业时间</a><a href=\"#food\">餐饮全盘对比</a><a href=\"#hotels\">酒店全盘对比</a><a href=\"#itinerary\">每日行程</a><a href=\"#avoid\">避坑清单</a><a href=\"#budget\">预算</a><a href=\"#preparation\">准备清单</a><a href=\"#research\">搜索依据</a></div></nav>",
        overview_section(trip),
        transport_section(trip),
        transport_detail_section(),
        booking_section(trip),
        hours_section(trip),
        food_section(),
        hotel_section(),
        itinerary_section(trip),
        avoid_section(trip),
        budget_section(trip),
        preparation_section(trip),
        research_section(),
        "<section id=\"tips\" class=\"section\"><div class=\"section-kicker\">最后确认</div><h2>出发前一周再次核对</h2><div class=\"long-list\">{}</div></section>".format("".join("<div class=\"long-item\"><h4>检查{}</h4><p>{}</p></div>".format(index + 1, esc(tip)) for index, tip in enumerate(trip.get("tips", [])))),
        "<footer id=\"sources\" class=\"footer\"><div class=\"wrap\"><p>本页为优化版详细行程，原始网页未覆盖。酒店价格仅作预算，不替代实时订单；链接用于核对评价、房型和库存。</p><p>规则来源：<a href=\"https://www.jiuzhai.com/news/notice/9817-2024-07-25-07-49-17\" target=\"_blank\" rel=\"noreferrer\">九寨沟官方公告</a> · <a href=\"https://www.jiuzhai.com/news/notice/11001-2026-03-23-01-36-44\" target=\"_blank\" rel=\"noreferrer\">九寨沟开放时间公告</a></p><p>行程数据：<a href=\"trip.json\">trip.json</a> · 生成时间：{}</p></div></footer></body></html>".format(esc(trip.get("metadata", {}).get("generated_at"))),
    ]
    return "".join(html_doc)


def main():
    trip = json.loads(TRIP_PATH.read_text(encoding="utf-8"))
    OUT_PATH.write_text(render(trip), encoding="utf-8")
    print("generated", OUT_PATH)


if __name__ == "__main__":
    main()
