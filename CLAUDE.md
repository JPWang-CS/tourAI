# CLAUDE.md —— tourAI 项目约定

## 项目概述

tourAI 是一个 Claude Code Skill，通过**多 Agent 流水线**帮助用户完成旅行规划，生成精美的 HTML 攻略。

## 核心架构原则

1. **数据优先** —— 所有行程数据以 `trip.json`（schemas/trip.schema.json）为中心。Agent 通过 `data/` 目录交换结构化 JSON，不通过内存传递。

2. **Agent 独立性** —— 四个 Agent（gather/plan/enrich/render）各自独立，通过磁盘通信：
   - `.claude/agents/gather-agent.md` — 多源数据收集（高德MCP + 小红书MCP + 马蜂窝 + WebSearch）
   - `.claude/agents/plan-agent.md` — 行程结构规划（地理聚类 + 时间分配 + 预算）
   - `.claude/agents/enrich-agent.md` — 高德路线计算（距离+时间+坐标）
   - `.claude/agents/render-agent.md` — HTML 渲染输出

3. **多源融合** —— 数据源优先级：高德（地理） > 小红书（体验） > 马蜂窝（排名） > WebSearch（兜底）

4. **幂等可重跑** —— 每个 Agent 检查输入/输出是否存在，支持增量编辑后局部重跑。

5. **产生可操作的攻略** —— 精确到分钟的时间表、真实路线距离、具体餐厅名称和价格、12条避坑清单。

## 目录结构约定

- `data/cache/<city_pinyin>/` — 目的地缓存（TTL 7天）
- `data/trips/<uuid>/` — 行程输出（trip.json + output.html）
- `scripts/` — Python 工具，通过 Bash 工具调用
- `templates/html/` — HTML 设计参考（Agent 读取后直接生成，非模板引擎）
- `schemas/` — JSON Schema 定义，用于数据验证

## 开发约定

- Agent 之间不要直接通信，通过 `data/` 目录交换数据
- 不要编造数据 —— 所有景点/餐厅/酒店信息必须来自真实搜索
- source 字段标注数据来源（amap/xhs/mafengwo/websearch/llm）
- route 对象统一使用 `schemas/route.schema.json` 格式
- 每次生成前检查缓存，避免重复抓取

## 输出标准

生成的 HTML 必须包含：
- Hero 区域（渐变背景 + 标签）
- 交通信息卡片
- 每日行程卡片（含路线条、景点详情、浪漫时刻、避坑提示、餐饮推荐、酒店推荐）
- 美食推荐汇总
- 避坑清单（❌错误做法 ~~删除线~~ + ✅正确做法 绿色）
- 预算估算
- 出行 Tips
- 右侧快速导航（PC端）+ 滚动高亮
- 可折叠模块
- 响应式（768px + 375px 断点）

## 设计规范

参考 `references/design-spec.md`：
- 配色：主色 #667eea → #764ba2，强调色 #f2719c
- 字体：Noto Sans SC
- 卡片：圆角 16px，阴影 0 2px 12px rgba(0,0,0,.06)
- Day 卡片渐变色轮换（5种）
