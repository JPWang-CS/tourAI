# 多源数据集成指南

tourAI 从多个平台收集旅游数据，按优先级融合。本文档说明各个数据源的接入方式、适用场景和容错策略。

## 数据源总览

| 源 | 接入方式 | 数据特点 | 优先级 | 配置难度 |
|---|---------|---------|--------|---------|
| 🗺️ 高德地图 | MCP Server | POI坐标、路线、天气 | ⭐⭐⭐ | 低 |
| 📕 小红书 | MCP Server | 用户评价、美食、避坑 | ⭐⭐ | 中 |
| 🐝 马蜂窝 | Python脚本 | 攻略模板、景点排名 | ⭐⭐ | 低 |
| 🔍 WebSearch | 内置工具 | 最新信息、兜底 | ⭐ | 无 |

---

## 1. 高德地图（Amap MCP）

### 接入方式

**方式一（推荐）：MCP Server**

在 `.claude/settings.local.json` 中添加：

```json
{
  "mcpServers": {
    "amap": {
      "command": "npx",
      "args": ["-y", "@sugarforever/amap-mcp-server"],
      "env": {
        "AMAP_KEY": "你的高德API Key"
      }
    }
  }
}
```

获取 Key：访问 https://lbs.amap.com/ 注册并创建「Web服务」应用。

**方式二：Python 脚本**

```bash
python scripts/amap_route.py --origin "威海公园" --destination "火炬八街" --city 威海
```

### 可用工具（MCP）

| 工具 | 用途 | 示例 |
|------|------|------|
| `poi_search` | 搜索景点/餐厅/酒店 | `poi_search(keyword="威海 景点", region="威海")` |
| `geocode` | 地址→坐标 | `geocode(address="威海公园", city="威海")` |
| `driving_route` | 驾车路线 | `driving_route(origin="116.3,39.9", destination="116.4,40.0")` |
| `walking_route` | 步行路线 | `walking_route(origin="...", destination="...")` |
| `transit_route` | 公交路线 | `transit_route(origin="...", destination="...", city="威海")` |
| `weather` | 天气查询 | `weather(city="威海")` |
| `distance` | 批量距离 | `distance(origins="...", destination="...", type=1)` |

### 数据示例

```json
{
  "name": "威海公园",
  "coordinates": {"lng": 122.121, "lat": 37.513},
  "category": "park",
  "rating": 4.5,
  "amap_poi_id": "B0211012HG",
  "address": "山东省威海市环翠区海滨北路"
}
```

---

## 2. 小红书（XHS MCP）

### 接入方式

安装 MCP Server：

```bash
npx -y @anthropic-fans/xhs-mcp
```

**需要配置环境变量** `XHS_COOKIE`：

1. 在浏览器中打开 https://www.xiaohongshu.com 并登录
2. 按 F12 打开开发者工具 → Application → Cookies → 复制 `web_session` 的值
3. 设置环境变量：
   ```bash
   export XHS_COOKIE="web_session=YOUR_COOKIE_VALUE"
   ```

### 可用工具

| 工具 | 用途 |
|------|------|
| `search_notes` | 搜索笔记标题和内容 |
| `get_note_detail` | 获取单条笔记详情 |
| `search_feeds` | 搜索信息流内容 |
| `get_user_profile` | 获取用户主页 |

### 最佳搜索模式

```
search_notes(keyword="威海 旅游攻略")
search_notes(keyword="威海 必吃美食")
search_notes(keyword="威海 避坑 踩雷")
search_notes(keyword="威海 情侣 拍照")
search_notes(keyword="威海 民宿 推荐")
```

### Cookie 管理

- Cookie 有效期通常 1-2 周
- 过期后会返回认证错误
- 定期在浏览器中重新获取

---

## 3. 马蜂窝（Python 脚本）

### 接入方式

```bash
python scripts/mafengwo.py --destination <城市> --type <类型>
```

无需额外配置，脚本自动处理签名。

### 支持的数据类型

| --type | 返回数据 |
|--------|---------|
| `overview` | 城市简介、最佳季节、交通概况 |
| `spots` | 景点列表（排名、评分、门票、开放时间） |
| `food` | 美食推荐（菜系、人均、推荐菜） |
| `routes` | 经典行程模板 |
| `guides` | 游记攻略摘要 |
| `all` | 以上全部 |

### 数据示例

```json
{
  "destination": {"id": 12176, "name": "威海", "province": "山东"},
  "data": {
    "spots": [
      {
        "name": "刘公岛",
        "rating": 4.6,
        "rating_count": 15200,
        "ticket_price": 122,
        "description": "甲午战争纪念地...",
        "opening_hours": "07:30-17:00"
      }
    ]
  }
}
```

---

## 4. WebSearch（兜底）

### 使用方式

```
WebSearch(query="威海 最新门票价格 2026")
WebSearch(query="威海 新开网红餐厅")
```

### 适用场景

- 其他源都无法覆盖的最新信息
- 航班时刻表和实时票价
- 活动/节庆信息
- 新开业店铺

---

## 数据合并规则

当多个源返回同一景点的数据时，按以下规则合并：

1. **坐标** → 高德（最精准）
2. **评分** → 马蜂窝 POI 排名 > 高德
3. **体验评价** → 小红书（真实用户）
4. **门票/时间** → 高德（官方数据） > 马蜂窝
5. **美食推荐** → 小红书（真实体验） > 马蜂窝
6. **酒店价格** → WebSearch 最新结果

去重规则：同名景点坐标距离 < 500m 视为同一地点。

---

## 容错策略

| 故障 | 处理 |
|------|------|
| Amap MCP 不可用 | 坐标用 WebSearch + 估算；路线用直线距离 × 1.4，驾车速度 30km/h |
| XHS MCP 不可用 | WebSearch 搜索小红书公开片段 |
| 马蜂窝脚本报错 | 跳过，用 WebSearch 替代 |
| WebSearch 无结果 | 使用 LLM 自有知识，source="llm" |
| 全部不可用 | 告知用户，请提供参考链接 |

---

## 缓存策略

- 目的地概览：7天 TTL
- 景点数据：14天 TTL
- 餐厅/酒店：3天 TTL（变化快）
- 天气：不缓存（实时）
- 用户可通过 `force_refresh=true` 强制刷新
