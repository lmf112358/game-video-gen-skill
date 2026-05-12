# 🎬 Game Video Gen — 游戏营销视频生成 Skill

基于即梦AI (Jimeng) Visual API 的 AI 驱动游戏营销视频生成系统。通过多角色协作，将游戏角色截图 + 文字描述自动转化为高质量短视频。

## ✨ 特性

- 🎮 **游戏角色智能识别** — 内置原神/崩铁/明日方舟/鸣潮角色知识库，自动匹配角色档案
- 🔍 **视觉特征提取** — AI 分析截图提取外观、装备、姿态、场景等视觉特征
- 📝 **提示词工程** — 按游戏类型（RPG/动作/策略/休闲）自动生成优化提示词
- 🎬 **即梦AI Visual API** — 火山引擎官方 API，HMAC-SHA256 签名认证，即梦视频3.0 720P
- 🔄 **迭代优化** — 视频生成后可迭代调整提示词，逐步优化效果
- 🛡️ **双阻塞确认** — 角色档案确认 + 提示词确认，用户完全控制生成方向

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置凭证

```bash
# 复制配置模板
copy .env.example .env

# 编辑 .env，填入火山引擎 IAM 凭证
# VOLC_ACCESS_KEY_ID=你的AccessKeyID
# VOLC_SECRET_ACCESS_KEY=你的SecretAccessKey
```

获取凭证：访问 [火山引擎访问控制](https://console.volcengine.com/iam/keymanage/)

### 3. 使用 Skill

在 Trae 中提供游戏角色截图 + 文字描述：

> 这是一张原神迪卢克的截图，帮我生成一段"勇士打地堡"的营销视频

Skill 自动执行完整管线，两个确认点等待你审核。

## 📐 系统架构

```
用户输入 (截图 + 文字描述)
        │
        ▼
[Step 1] 输入处理 — 保存截图和描述，初始化项目
        │
        ▼
[Step 2] Character_Analyst — 分析截图，提取视觉特征
        │
        ▼
[Step 3] Lore_Researcher — 构建角色档案（性格/武器/大招/语音风格）
        │
        ⛔ 阻塞确认：用户审核角色档案
        │
        ▼
[Step 4] Prompt_Engineer — 生成即梦AI优化提示词
        │
        ⛔ 阻塞确认：用户审核提示词
        │
        ▼
[Step 5] Video_Director — 调用即梦AI API 生成视频，下载保存
        │
        ▼
[Step 6] 质量审核 — 展示结果，可选迭代优化
```

## 🎭 四角色协作

| 角色 | 职责 | 输出 |
|------|------|------|
| **Character_Analyst** | 分析截图提取视觉特征 | `character_visual_profile.json` |
| **Lore_Researcher** | 构建完整角色档案 | `character_lore_profile.json` |
| **Prompt_Engineer** | 生成即梦AI优化提示词 | `seedance_request.json` |
| **Video_Director** | 管理 API 调用与视频生成 | `video.mp4` |

## 📁 项目结构

```
.trae/skills/game-video-gen/
├── SKILL.md                          # 核心工作流权威
├── references/                       # 角色定义与技术规范
│   ├── character-analyst.md           # 角色分析师
│   ├── lore-researcher.md             # 角色考据师
│   ├── prompt-engineer.md             # 提示词工程师
│   ├── video-director.md              # 视频导演
│   └── shared-standards.md            # 共享技术标准
├── scripts/                           # 工具脚本
│   ├── seedance_api.py                # 即梦AI Visual API 客户端（HMAC签名）
│   ├── image_analyzer.py              # 截图分析
│   ├── character_db.py                # 游戏角色知识库
│   ├── video_manager.py               # 视频项目管理
│   └── video_download.py              # 视频下载
├── templates/                         # 提示词模板
│   ├── prompt_templates.md            # 4种游戏类型模板
│   └── style_references.md            # 5款游戏风格参考
└── workflows/                         # 独立工作流
    ├── character-research.md           # 角色深度考据
    └── video-iteration.md             # 视频迭代优化
```

## 🛠️ 手动使用脚本

### 项目管理

```bash
# 初始化项目
python .trae/skills/game-video-gen/scripts/video_manager.py init "genshin_diluc_20260512"

# 保存输入
python .trae/skills/game-video-gen/scripts/video_manager.py save-input projects/genshin_diluc_20260512 --screenshot "C:\path\to\diluc.jpg" --description "勇士打地堡"
```

### 角色查询

```bash
# 按名称搜索
python .trae/skills/game-video-gen/scripts/character_db.py search --name "迪卢克"

# 列出所有角色
python .trae/skills/game-video-gen/scripts/character_db.py list
```

### 视频生成

```bash
# 提交生成任务
python .trae/skills/game-video-gen/scripts/seedance_api.py generate --request projects/xxx/seedance_request.json --output projects/xxx/video_result.json

# 轮询状态
python .trae/skills/game-video-gen/scripts/seedance_api.py poll --task-id "7392616336519610409" --output projects/xxx/video_result.json

# 下载视频（生成成功后1小时内有效！）
python .trae/skills/game-video-gen/scripts/video_download.py --url "https://..." -o projects/xxx/output/video.mp4
```

## 🎮 内置角色数据库

| 游戏 | 角色 | 元素 |
|------|------|------|
| 原神 | 迪卢克 (Diluc) | 火 Pyro |
| 原神 | 雷电将军 (Raiden Shogun) | 雷 Electro |
| 原神 | 钟离 (Zhongli) | 岩 Geo |
| 崩坏：星穹铁道 | 景元 (Jing Yuan) | 雷 Lightning |
| 崩坏：星穹铁道 | 卡芙卡 (Kafka) | 雷 Lightning |
| 明日方舟 | 银灰 (SilverAsh) | 冰 Arts |
| 鸣潮 | 鉴心 (Jiyan) | 风 Aero |

> 不在库中的角色会自动触发 AI 推理构建角色档案。

## 🎬 当前使用模型

| req_key | 模型 | 能力 | 分辨率 |
|---------|------|------|--------|
| `jimeng_i2v_first_v30` | 即梦视频3.0 720P | 图生视频-首帧 | 720P |

**视频时长**：5s (frames=121) 或 10s (frames=241)

## 📋 提示词模板

按游戏类型提供 4 种提示词模板：

| 模板 | 适用游戏 | 风格特点 |
|------|---------|---------|
| **RPG** | 原神、崩铁、鸣潮 | 元素特效、大招动画、电影级光影 |
| **动作** | 永劫无间、战双、绝区零 | 高速连击、打击感、动态镜头 |
| **策略** | 明日方舟、碧蓝航线 | 战术技能、指挥气场、史诗氛围 |
| **休闲** | 社交/偶像/休闲游戏 | 可爱动作、闪光特效、温馨氛围 |

## ⚠️ 重要注意事项

- **视频 URL 1 小时过期** — 生成后必须立即下载转存！
- **提示词长度** — 建议不超过 400 字，不超过 800 字
- **截图要求** — 仅支持 JPEG/PNG，最大 4.7MB，分辨率最大 4096×4096
- **认证方式** — HMAC-SHA256 签名，使用火山引擎 IAM 的 AccessKeyID/SecretAccessKey
- **内容审核** — API 会审核输入输出内容，敏感词/版权词会被拦截

## 🔧 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `VOLC_ACCESS_KEY_ID` | ✅ | 火山引擎 IAM AccessKeyID |
| `VOLC_SECRET_ACCESS_KEY` | ✅ | 火山引擎 IAM SecretAccessKey |
| `ARK_API_KEY` | ❌ | 火山方舟 ARK API Key（备选） |
| `JIMENG_TIMEOUT` | ❌ | 轮询超时（秒），默认 600 |

## 📄 License

MIT
