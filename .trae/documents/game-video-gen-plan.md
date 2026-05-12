# 游戏营销视频生成 Skill 实施计划

## 项目概述

构建一个面向游戏业务场景的营销视频生成 Skill（`game-video-gen`），参考 ppt-master 的多角色协作架构，实现从"游戏角色截图 + 文字描述"到"10s 营销短视频"的端到端自动化流程。

**核心管线**: `截图输入 → 角色分析 → 角色考据 → 提示词工程 → Seedance 2.0 视频生成 → 质量审核`

***

## 架构设计

### 参考项目 ppt-master 的关键模式

| 模式          | ppt-master 做法                            | 本项目适配                                                                      |
| ----------- | ---------------------------------------- | -------------------------------------------------------------------------- |
| 多角色协作       | Strategist → Image\_Generator → Executor | Character\_Analyst → Lore\_Researcher → Prompt\_Engineer → Video\_Director |
| SKILL.md 权威 | 单一入口，严格串行管线                              | 同样采用 SKILL.md 作为唯一权威                                                       |
| 阻塞确认        | 八项确认（⛔ BLOCKING）                         | 角色分析确认 + 提示词确认（⛔ BLOCKING）                                                 |
| 质量门控        | 每步有 🚧 GATE                              | 每步有前置条件检查                                                                  |
| 项目管理        | project\_manager.py                      | video\_manager.py                                                          |
| 后处理         | finalize\_svg.py → svg\_to\_pptx.py      | video\_download.py → video\_review\.py                                     |

### 角色定义

1. **Character\_Analyst（角色分析师）** — 分析截图，提取角色视觉特征（外观、装备、姿态、场景元素）
2. **Lore\_Researcher（角色考据师）** — 基于视觉特征+游戏知识，构建完整角色档案（性格、语音风格、武器、大招动作、背景故事）
3. **Prompt\_Engineer（提示词工程师）** — 将角色档案+用户文字描述转化为 Seedance 2.0 最优提示词，确保场景一致性、风格匹配
4. **Video\_Director（视频导演）** — 管理 Seedance 2.0 API 调用、参数配置、视频生成与下载

***

## 目录结构

```
f:\AIprogarm\task\
├── .trae/
│   └── skills/
│       └── game-video-gen/
│           ├── SKILL.md                          # 主工作流权威
│           ├── references/                       # 角色定义与技术规范
│           │   ├── character-analyst.md           # 角色分析师定义
│           │   ├── lore-researcher.md             # 角色考据师定义
│           │   ├── prompt-engineer.md             # 提示词工程师定义
│           │   ├── video-director.md              # 视频导演定义
│           │   └── shared-standards.md            # 共享技术标准
│           ├── scripts/                           # 工具脚本
│           │   ├── seedance_api.py                # Seedance 2.0 API 客户端
│           │   ├── image_analyzer.py              # 截图分析（调用视觉模型）
│           │   ├── character_db.py                # 游戏角色知识库
│           │   ├── video_manager.py               # 视频项目管理
│           │   └── video_download.py              # 视频下载与保存
│           ├── templates/                         # 提示词模板
│           │   ├── prompt_templates.md            # 视频提示词模板库
│           │   └── style_references.md            # 风格参考库
│           └── workflows/                         # 独立工作流
│               ├── character-research.md          # 角色深度考据工作流
│               └── video-iteration.md             # 视频迭代优化工作流
├── projects/                                      # 用户项目工作区
└── requirements.txt                               # Python 依赖
```

***

## 实施步骤

### 步骤 1: 创建项目基础结构

* 创建 `.trae/skills/game-video-gen/` 目录及所有子目录

* 创建 `projects/` 工作区目录

* 创建 `requirements.txt`（依赖：requests, Pillow, python-dotenv）

### 步骤 2: 编写 SKILL.md（核心工作流）

SKILL.md 是整个 Skill 的权威入口，定义完整的串行管线：

```
Step 1: 输入处理 — 接收截图+文字描述
  🚧 GATE: 用户提供了游戏截图和文字描述

Step 2: 角色分析 — Character_Analyst 分析截图
  - 调用 image_analyzer.py 提取视觉特征
  - 输出: character_visual_profile.json

Step 3: 角色考据 — Lore_Researcher 构建角色档案
  - 调用 character_db.py 查询角色知识
  - 基于视觉特征推断角色身份
  - 输出: character_lore_profile.json
  ⛔ BLOCKING: 展示角色档案，等待用户确认

Step 4: 提示词工程 — Prompt_Engineer 生成视频提示词
  - 读取角色档案 + 用户文字描述
  - 选择合适的提示词模板
  - 生成 Seedance 2.0 优化提示词
  - 确定视频参数（时长、比例、模型）
  ⛔ BLOCKING: 展示提示词，等待用户确认

Step 5: 视频生成 — Video_Director 调用 API
  - 调用 seedance_api.py 提交生成任务
  - 轮询任务状态
  - 下载生成的视频
  - 输出: 视频文件

Step 6: 质量审核 — 可选迭代
  - 展示生成结果
  - 用户可选择迭代优化
```

### 步骤 3: 编写角色定义文件（references/）

#### 3.1 character-analyst.md

* 角色职责：从截图中提取视觉特征

* 分析维度：角色外观（发型、服装、体型）、装备（武器、饰品）、姿态（战斗姿态、待机动作）、场景元素（背景环境、特效）

* 输出格式：character\_visual\_profile.json 的 schema 定义

* 分析原则：客观描述，不做主观推断

#### 3.2 lore-researcher.md

* 角色职责：基于视觉特征构建完整角色档案

* 考据维度：角色身份、性格特征、语音风格、武器详情、大招/技能动作、背景故事、人际关系

* 知识来源：内置角色数据库 + AI 推理

* 输出格式：character\_lore\_profile.json 的 schema 定义

* 一致性原则：所有推断必须与视觉特征一致

#### 3.3 prompt-engineer.md

* 角色职责：将角色档案转化为 Seedance 2.0 最优提示词

* 提示词结构：场景描述 + 角色动作 + 镜头运动 + 风格修饰 + 技术参数

* 优化策略：关键动作前置、风格一致性词汇、场景连贯性描述

* 模板选择：根据游戏类型（RPG/动作/策略/休闲）选择不同模板

* 输出格式：seedance\_request.json 的 schema 定义

#### 3.4 video-director.md

* 角色职责：管理 Seedance 2.0 API 调用全流程

* API 参数配置：model、duration、aspect\_ratio、images

* 异步处理：提交任务 → 轮询状态 → 下载结果

* 错误处理：API 限流、余额不足、生成失败

* 输出格式：video\_result.json 的 schema 定义

#### 3.5 shared-standards.md

* Seedance 2.0 API 技术规范

* 支持的参数范围

* 提示词长度限制（2000 字符）

* 视频规格（5/10/15s, 480p/720p/1080p）

* 角色档案 JSON schema

* 项目目录结构规范

### 步骤 4: 编写工具脚本（scripts/）

#### 4.1 seedance\_api.py — Seedance 2.0 API 客户端

```python
核心功能：
- generate_video(prompt, images, duration, aspect_ratio, model) → task_id
- poll_status(task_id) → status, video_url
- download_video(video_url, output_path) → local_path
- 支持环境变量 SEEDANCE_API_KEY
- 支持回调 URL（callback_url）
- 完善的错误处理和重试机制
```

API 端点：

* POST <https://seedanceapi.org/v2/generate>

* GET <https://seedanceapi.org/v2/status?task_id=xxx>

#### 4.2 image\_analyzer.py — 截图分析

```python
核心功能：
- analyze_screenshot(image_path) → CharacterVisualProfile
- 提取：角色外观、装备、姿态、场景元素
- 输出 JSON 格式的视觉特征档案
- 支持本地图片和 URL 图片
```

#### 4.3 character\_db.py — 游戏角色知识库

```python
核心功能：
- search_character(game_name, character_name) → CharacterLore
- 支持的游戏：原神、崩坏星穹铁道、明日方舟等
- 内置常见角色数据
- 支持扩展新角色
- 输出 JSON 格式的角色档案
```

#### 4.4 video\_manager.py — 视频项目管理

```python
核心功能：
- init_project(project_name) → project_path
- 保存截图到项目
- 保存角色档案到项目
- 保存提示词到项目
- 保存生成的视频到项目
- 项目状态追踪
```

#### 4.5 video\_download.py — 视频下载

```python
核心功能：
- download(video_url, output_path) → local_path
- 支持断点续传
- 自动命名（时间戳+项目名）
```

### 步骤 5: 编写提示词模板（templates/）

#### 5.1 prompt\_templates.md

按游戏类型分类的提示词模板：

**RPG 类（原神/崩铁）**:

```
[角色名]，[外观描述]，在[场景]中[动作描述]，[武器/元素特效]，
[镜头运动]，电影级光影，[风格修饰]，游戏营销风格
```

**动作类（永劫无间/战双）**:

```
[角色名]，[战斗姿态]，[武器特效]，[高速动作]，[打击感描述]，
动态镜头跟随，[风格修饰]，燃向营销风格
```

**策略类（明日方舟/碧蓝航线）**:

```
[角色名]，[指挥姿态]，[场景氛围]，[技能释放]，[战术动作]，
缓慢推镜头，[风格修饰]，史诗营销风格
```

#### 5.2 style\_references.md

* 各游戏画风特征描述

* 镜头语言参考

* 色调风格参考

* 动作风格参考

### 步骤 6: 编写独立工作流（workflows/）

#### 6.1 character-research.md

当角色不在内置数据库中时的深度考据流程：

* 基于视觉特征推断游戏来源

* 搜索角色背景信息

* 构建临时角色档案

#### 6.2 video-iteration.md

视频生成后的迭代优化流程：

* 分析当前视频不足

* 调整提示词策略

* 重新生成

* 对比评估

### 步骤 7: 编写 requirements.txt

```
requests>=2.31.0
Pillow>=10.0.0
python-dotenv>=1.0.0
```

### 步骤 8: 端到端测试

* 准备测试截图（原神角色截图）

* 运行完整管线

* 验证每个步骤的输出

* 确认视频生成成功

***

## Seedance 2.0 API 集成规范

### API 端点

| 端点                                              | 方法   | 用途       |
| ----------------------------------------------- | ---- | -------- |
| `https://seedanceapi.org/v2/generate`           | POST | 创建视频生成任务 |
| `https://seedanceapi.org/v2/status?task_id=xxx` | GET  | 查询任务状态   |

### 请求参数

| 参数            | 类型        | 必填 | 说明                               |
| ------------- | --------- | -- | -------------------------------- |
| prompt        | string    | 是  | 视频描述（最大 2000 字符）                 |
| duration      | number    | 否  | 5/10/15 秒，默认 5                   |
| aspect\_ratio | string    | 否  | 16:9/9:16/4:3/3:4，默认 16:9        |
| images        | string\[] | 否  | 图生视频：1-4 个图片 URL                 |
| model         | string    | 否  | seedance-2.0 或 seedance-2.0-fast |
| callback\_url | string    | 否  | 异步回调 URL                         |

### 认证

```
Authorization: Bearer YOUR_API_KEY
```

### 定价（credits）

| 模型                | 5s  | 10s | 15s |
| ----------------- | --- | --- | --- |
| seedance-2.0      | 240 | 480 | 720 |
| seedance-2.0-fast | 160 | 320 | 480 |

### 响应格式

生成任务创建：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "task_id": "xxx",
    "status": "IN_PROGRESS",
    "consumed_credits": 480
  }
}
```

任务状态查询：

```json
{
  "code": 200,
  "data": {
    "task_id": "xxx",
    "status": "SUCCESS",
    "response": ["https://cdn.example.com/videos/xxx.mp4"]
  }
}
```

***

## 数据流示意

```
用户输入
├── 游戏截图 (image)
└── 文字描述 (text): "勇士打地堡"
        │
        ▼
[Step 1] 输入处理
├── 保存截图到项目目录
├── 解析文字描述
└── 初始化项目
        │
        ▼
[Step 2] Character_Analyst
├── image_analyzer.py 分析截图
└── 输出: character_visual_profile.json
    {
      "appearance": "红发男性，穿着骑士铠甲",
      "weapon": "双手大剑",
      "pose": "战斗准备姿态",
      "scene_elements": "城堡走廊，火把照明",
      "visual_style": "日系二次元，高饱和度"
    }
        │
        ▼
[Step 3] Lore_Researcher
├── character_db.py 查询角色库
├── 匹配: 原神 - 卢迪克（迪卢克）
└── 输出: character_lore_profile.json
    {
      "identity": { "name": "迪卢克", "game": "原神", "element": "火" },
      "personality": "沉稳内敛，正义感强",
      "voice_style": "低沉磁性，简洁有力",
      "weapon": { "name": "双手剑", "type": "claymore" },
      "signature_move": "黎明·烈焰斩，火焰爆发的下劈攻击",
      "background": "蒙德城暗夜英雄",
      "style_keywords": ["火焰特效", "暗红光芒", "鹰翎纹饰"]
    }
        │
        ▼
⛔ BLOCKING: 用户确认角色档案
        │
        ▼
[Step 4] Prompt_Engineer
├── 读取角色档案 + "勇士打地堡"
├── 选择 RPG 模板
└── 输出: seedance_request.json
    {
      "prompt": "迪卢克，红发男性骑士，手持燃烧的双手大剑，在阴暗的地堡走廊中挥出火焰下劈斩击，火焰爆发照亮整个走廊，暗红光芒与火把交织，电影级低角度仰拍，缓慢推镜头至角色特写，日系二次元风格，高饱和度，游戏营销大片质感",
      "images": ["https://...screenshot.jpg"],
      "duration": 10,
      "aspect_ratio": "16:9",
      "model": "seedance-2.0"
    }
        │
        ▼
⛔ BLOCKING: 用户确认提示词
        │
        ▼
[Step 5] Video_Director
├── seedance_api.py 提交任务
├── 轮询状态（每 10s）
├── 下载视频
└── 输出: projects/xxx/output/video.mp4
        │
        ▼
[Step 6] 质量审核
├── 展示视频给用户
└── 可选: 进入 video-iteration 工作流
```

***

## 关键设计决策

1. **图生视频优先**: 用户提供了截图，优先使用 Seedance 2.0 的 image-to-video 模式，将截图作为首帧参考，确保角色外观一致性
2. **角色档案 JSON 化**: 所有中间产物以 JSON 格式存储，便于程序化处理和版本追踪
3. **提示词模板化**: 按游戏类型提供模板，确保提示词结构化和可复现性
4. **双阻塞确认**: 角色档案确认 + 提示词确认，确保用户对生成方向有完全控制
5. **异步轮询**: Seedance API 为异步模式，脚本自动轮询直到完成
6. **项目隔离**: 每次生成创建独立项目目录，所有中间产物和最终视频集中管理

***

## 实施优先级

| 优先级 | 步骤         | 说明                        |
| --- | ---------- | ------------------------- |
| P0  | 步骤 1-2     | 项目结构 + SKILL.md（核心）       |
| P0  | 步骤 4.1     | seedance\_api.py（API 客户端） |
| P0  | 步骤 3.1-3.4 | 角色定义文件                    |
| P1  | 步骤 4.2-4.5 | 工具脚本                      |
| P1  | 步骤 5       | 提示词模板                     |
| P2  | 步骤 6       | 独立工作流                     |
| P2  | 步骤 7-8     | 依赖与测试                     |

