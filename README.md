# Render Text into Visualizable Model — 文本知识星球

将中文叙事文本转化为可交互的 3D 知识图谱。基于 Google LangExtract 进行实体与因果关系提取，使用 3d-force-graph + Three.js 将知识结构呈现在可旋转的球体上。

## 项目概览

```
输入文本 → [LangExtract 提取] → JSONL → [转换脚本] → graph_data.json → [3D 可视化] → cosmos.html
                ↑                                              ↑                    ↑
          milestone2_extract.py                         milestone3_convert.py   cosmos_template.html
                                                              ↓
                                                     milestone5_quality.py (质量检查)
```

### 示例文本：蝴蝶回声

一个蝴蝶效应式的中国村庄故事，约 3000 字，包含丰富的实体类型和清晰的因果链。从女孩林溪吹一口气到矿难救援，所有事件环环相扣。

### 提取的实体类别

| 类别 | 颜色 | 对应英文 key |
|------|------|-------------|
| 人物 | <span style="color:#FF6B6B;">●</span> | `person` |
| 动物 | <span style="color:#4ECDC4;">●</span> | `animal` |
| 物体 | <span style="color:#FFD93D;">●</span> | `object` |
| 地点 | <span style="color:#6BCB77;">●</span> | `place` |
| 事件 | <span style="color:#FF8C42;">●</span> | `event` |
| 情绪 | <span style="color:#C77DFF;">●</span> | `emotion` |
| 概念 | <span style="color:#48B5E4;">●</span> | `concept` |

## 文件结构

```
├── Earth.md                     # 项目蓝图（5 个里程碑）
├── sample_text.txt              # 示例输入文本
├── requirements.txt             # Python 依赖
│
├── milestone1_design.py         # 里程碑 1：提取模板设计（Prompt + Examples）
├── milestone2_extract.py        # 里程碑 2：LangExtract 提取脚本（需要 API Key）
├── generate_sample_data.py      # 替代方案：手工构造 72 条提取数据
├── milestone3_convert.py        # 里程碑 3：JSONL → graph_data.json 转换
├── milestone5_quality.py        # 里程碑 5：数据质量检查与自动清洗
│
├── extraction_results.jsonl     # 提取原始数据（72 条记录）
├── graph_data.json              # 图数据（61 节点，64 边）
├── graph_data.js                # 图数据 JS 变量（供 cosmos.html 加载）
│
├── cosmos_template.html         # 可视化 HTML 模板
├── build_cosmos.py              # 构建脚本：graph_data.json → graph_data.js + cosmos.html
├── cosmos.html                  # 最终可视化页面（可直接浏览器打开）
├── highlight.html               # 原文高亮对照页面（LangExtract 生成）
│
├── test_graph.html              # 最小 5 节点渲染测试
├── test_step.html               # 分步诊断测试
│
├── run_all.bat                  # 一键运行：提取 → 转换 → 可视化
└── README.md
```

## 快速开始

### 环境要求

- Python 3.10+
- 现代浏览器（Chrome / Edge / Firefox）
- （可选）Google Gemini API Key（用于 LangExtract 提取）

### 安装

```bash
pip install -r requirements.txt
```

### 方式一：直接查看可视化（推荐）

如果只是想看效果，直接用浏览器打开 `cosmos.html` 即可。

操作方式：
- **拖拽** 旋转球体
- **滚轮** 缩放
- **点击节点** 查看详情、原文证据和关联实体
- **点击关联标签** 跳转到对应节点
- **右键 / Esc** 关闭详情、复位视角

### 方式二：使用现有数据完整构建

```bash
# 从 graph_data.json 生成 graph_data.js 和 cosmos.html
python build_cosmos.py

# 质量检查
python milestone5_quality.py --input graph_data.json

# 自动修复问题
python milestone5_quality.py --input graph_data.json --fix
```

### 方式三：从零运行完整管线

1. 准备文本文件（或用 `sample_text.txt`）
2. 配置 API Key：
   ```bash
   set GOOGLE_API_KEY=your_key_here
   ```
3. 运行：
   ```bash
   run_all.bat
   ```
   或手动逐步执行：
   ```bash
   python milestone2_extract.py          # 步骤1：提取实体与关系
   python milestone3_convert.py          # 步骤2：转换为图数据
   python milestone5_quality.py --fix    # 步骤3：质量检查与清洗
   python build_cosmos.py                # 步骤4：构建可视化页面
   ```

### 在没有 API Key 的情况下

`generate_sample_data.py` 手工构造了示例文本的提取结果，输出 `extraction_results.jsonl` 和 `highlight.html`，可直接运行：

```bash
python generate_sample_data.py
```

## 技术栈

| 层 | 技术 | 用途 |
|----|------|------|
| 提取 | [LangExtract](https://github.com/google/langextract) | LLM 驱动的结构化信息提取，带精确文本溯源 |
| 转换 | Python 脚本 | JSONL → 节点/边图数据结构 |
| 可视化 | [3d-force-graph](https://github.com/vasturiano/3d-force-graph) v1.73.0 | 3D 力导向图 |
| 渲染 | [Three.js](https://threejs.org/) r158 | WebGL 3D 渲染 |
| 测试 | [Playwright](https://playwright.dev/) | 无头浏览器自动化测试与截图 |

## 开发过程遇到的问题及解决方案

### Bug 1: `Invalid or unexpected token` — JS 语法错误导致页面白屏

**现象：** `cosmos.html` 始终显示"星球加载中..."，3D 球体无法渲染。`test_graph.html`（5 个硬编码节点）能正常运行。

**调试过程：**
1. 怀疑是 `nodeThreeObject` 覆盖了默认球体渲染 — 移除后无效
2. 怀疑是 IIFE / `'use strict'` 导致的问题 — 移除后无效
3. 怀疑是内嵌 JSON 数据的转义问题 — 改为外部 `<script src="graph_data.js">` 加载后无效
4. 使用 Playwright 无头浏览器捕获页面错误 — 发现 `Invalid or unexpected token`
5. 用 Node.js `--check` 对提取出的内联 JS 做语法检查 — **精准定位到第 126 行**

**根因：** `openSidebar` 函数中，动态构建关联节点芯片的 `onclick` 属性时，嵌套引号转义彻底错乱：

```javascript
// 错误写法（\" 出现在 JS 表达式级别，非法语法）
ch+='...onclick="focusNodeById(\''+esc(nb.nodeId).replace(/'/g,\"\\\\'\")+'\')">...';
```

**修复：** 放弃内联 `onclick`，改用 `data-nid` 属性 + 事件委托（在 `#connected-list` 上统一监听点击）。彻底消除了嵌套转义问题。

---

### Bug 2: `cvs.getContext is not a function` — 星空背景崩溃

**现象：** 修复 Bug 1 后脚本能执行了，但星空初始化失败。

**根因：** 星空背景的 `<canvas>` 被错误地写成了 `<div>`：
```html
<!-- 错误 -->
<div id="starfield"></div>

<!-- 正确 -->
<canvas id="starfield"></canvas>
```
`getContext('2d')` 是 canvas 元素的方法，div 上没有。这个 Bug 之前被 Bug 1 的语法错误掩盖了。

---

### Bug 3: `enableNavigationGlobe is not a function` — API 不存在

**根因：** `enableNavigationGlobe()` 方法在 3d-force-graph@1.73.0 中不存在，可能是后续版本才引入或已移除。

**修复：** 删除该调用。

---

### 警告（非致命）：Multiple instances of Three.js

**现象：** 控制台提示 `WARNING: Multiple instances of Three.js being imported.`

**原因：** 3d-force-graph@1.73.0 内部打包了一份 Three.js，与 CDN 引入的 `three@0.158.0` 产生版本冲突。

**解决：** 测试确认不能移除独立的 Three.js CDN（3d-force-graph 不暴露 `THREE` 全局变量），此警告不影响渲染和交互，保留现状。

---

### 经验教训

1. **JavaScript 语法错误要在构建阶段检测** — 可以用 `node -c` 或 `new Function(code)` 做编译期检查
2. **无头浏览器（Playwright）是调试前端问题的利器** — 能精确捕获 JS 运行时错误
3. **复杂的嵌套引号转义是 Bug 温床** — 优先使用 data 属性 + 事件委托模式
4. **版本兼容性要在早期验证** — CDN 库的方法名和可用性可能与文档不一致

## 数据类型

### 图数据节点结构
```json
{
  "id": "林溪",
  "group": "person",
  "color": "#FF6B6B",
  "size": 7,
  "connections": 5,
  "char_interval": {"start_pos": 18, "end_pos": 20},
  "attributes": {"性别": "女", "特征": "蓝色眼睛"}
}
```

### 图数据边结构
```json
{
  "source": "林溪对蝴蝶吹了一口气",
  "target": "蝴蝶扇动翅膀飞向天空",
  "relation": "导致",
  "description": "因果关系"
}
```

## License

MIT
