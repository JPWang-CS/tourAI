# 🌍 tourAI · 智能旅行规划助手

<p align="center">
  <img src="https://img.shields.io/badge/tourAI-v2.0.0-blueviolet?style=for-the-badge">
  <img src="https://img.shields.io/badge/Agent_Pipeline-✅-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Multi_Source-小红书%20%7C%20马蜂窝%20%7C%20高德-orange?style=for-the-badge">
</p>

<p align="center">
  <b>🤖 多源数据驱动 · Agent 流水线 · 一键生成精美旅游攻略</b><br>
  <b>从小红书、马蜂窝、高德地图获取真实数据，自动规划、渲染、输出</b>
</p>

---

## ✨ 核心亮点

tourAI 是 tour-guide-generator 的 v2.0 重构版本，升级为**多 Agent 流水线**架构：

| 能力 | 说明 |
|------|------|
| 🔄 **Agent 流水线** | Gather → Plan → Enrich → Render 四阶段自动化 |
| 📡 **多源融合** | 小红书（体验）+ 马蜂窝（排名）+ 高德（路线）+ WebSearch |
| 📊 **结构化数据** | trip.json 作为中枢，支持增量编辑和重新渲染 |
| 🗺️ **真实路线** | 高德 API 计算景点间距离和时间 |
| 🎨 **精美 HTML** | 响应式设计、可折叠模块、右侧导航、浪漫配色 |
| 💾 **智能缓存** | 目的地数据缓存 7 天，避免重复搜索 |

## 🚀 快速开始

### 用法

直接告诉 tourAI 你的需求：

```
帮我规划威海4天浪漫游
```

```
生成大理3天自由行攻略，从深圳出发
```

```
帮我做厦门周末2天攻略，要美食+拍照
```

tourAI 会自动：
1. 📡 从多个平台收集威海数据
2. 📋 规划每日行程（景点 + 餐饮 + 酒店）
3. 🗺️ 计算真实路线距离和时间
4. 🎨 生成精美 HTML 攻略文件

### 推荐配置

1. **高德 API Key**（用于真实路线计算）：
   ```
   设置环境变量: AMAP_KEY=你的Key
   ```
   申请地址：https://lbs.amap.com/

2. **小红书 Cookie**（用于获取真实用户评价，可选）：
   ```
   设置环境变量: XHS_COOKIE=你的Cookie
   ```
   详见 `references/data-sources.md`

## 📁 项目结构

```
tourAI/
├── SKILL.md                    ← 主编排器（入口）
├── .claude/agents/             ← 4 个 Agent 定义
│   ├── gather-agent.md         多源数据收集
│   ├── plan-agent.md           行程结构规划
│   ├── enrich-agent.md         高德路线计算
│   └── render-agent.md         HTML 渲染输出
├── schemas/                    ← JSON Schema 定义
├── data/                       ← 缓存 + 行程持久化
├── scripts/                    ← Python 工具
├── templates/                  ← HTML 模板参考
├── references/                 ← 设计 + 数据源文档
└── examples/                   ← 生成示例
```

## 🎯 生成的 HTML 包含

- 🌊 Hero 区域（渐变背景 + 标签）
- 🚄 交通信息卡片
- 📅 每日行程卡片（精确到分钟的路线）
- 🍜 美食推荐网格
- 🏨 酒店推荐 + 次日衔接
- ⚠️ 避坑清单（❌错误 vs ✅正确）
- 💰 预算估算
- 💕 浪漫出行 Tips
- 📱 PC/移动端自适应

## 📝 更新日志

### v2.0.0（2026-06-25）
- 🔄 重构为多 Agent 流水线架构
- 📡 新增小红书 + 马蜂窝数据源
- 📊 新增 JSON Schema 结构化数据层
- 💾 新增目的地数据缓存
- 📁 模块化模板系统
- 🏗️ 支持增量编辑和局部重跑
- 📖 完善多源数据集成文档

### v1.0.1（2026-05-19）
- 🧭 右侧快速导航
- 📂 可折叠模块

### v1.0.0（2026-05-19）
- 🎉 首次发布

## 📄 许可证

MIT License

## 👨‍💻 作者

JPWang-CS
GitHub: https://github.com/JPWang-CS/tourAI
