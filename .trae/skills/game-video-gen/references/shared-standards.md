# Shared Technical Standards

## 即梦AI Visual API Specification (当前使用)

### Base URL

```
https://visual.volcengineapi.com
```

### Authentication

HMAC-SHA256 签名认证，使用火山引擎 IAM 的 AccessKeyID + SecretAccessKey。

```
Authorization: HMAC-SHA256 Credential={AK}/{Date}/{Region}/{Service}/request, SignedHeaders=content-type;host;x-content-sha256;x-date, Signature={Signature}
```

固定值：Region=`cn-north-1`, Service=`cv`

获取凭证：https://console.volcengine.com/iam/keymanage/

### API Endpoints

| Action | Method | Purpose |
|--------|--------|---------|
| `CVSync2AsyncSubmitTask` | POST | 创建视频生成任务 |
| `CVSync2AsyncGetResult` | POST | 查询任务状态 |

Query 参数固定：`Version=2022-08-31`

### 当前使用模型

| req_key | 模型 | 能力 |
|---------|------|------|
| `jimeng_i2v_first_v30` | 即梦视频3.0 720P | 图生视频-首帧 |

### Request Format (提交任务)

```json
{
  "req_key": "jimeng_i2v_first_v30",
  "binary_data_base64": ["base64_image_data"],
  "image_urls": ["https://example.com/image.jpg"],
  "prompt": "提示词文本",
  "seed": -1,
  "frames": 121
}
```

**图片输入**（binary_data_base64 与 image_urls 二选一）：
- `binary_data_base64`: 图片 base64 编码，仅支持 1 张，JPEG/PNG
- `image_urls`: 图片 URL，仅支持 1 张

**图片要求**：
- 格式：JPEG、PNG
- 大小：最大 4.7MB
- 分辨率：最大 4096×4096，最短边不低于 320
- 长短边比例：3 以内

**帧数与时长**：
- `frames`: 总帧数 = 24×n+1
- 5s → `frames: 121`
- 10s → `frames: 241`

**提示词**：
- 中英文均可
- 建议不超过 400 字，不超过 800 字
- 过长可能效果异常

### Response Format (提交任务)

```json
{
  "code": 10000,
  "data": {
    "task_id": "7392616336519610409"
  },
  "message": "Success",
  "request_id": "20240720103939AF0029465CF6A74E51EC"
}
```

`code=10000` 表示成功，否则为错误。

### Request Format (查询任务)

```json
{
  "req_key": "jimeng_i2v_first_v30",
  "task_id": "7392616336519610409"
}
```

### Response Format (查询任务)

```json
{
  "code": 10000,
  "data": {
    "status": "done",
    "video_url": "https://xxxx",
    "aigc_meta_tagged": true
  }
}
```

### Task Status Values

| Status | Description |
|--------|-------------|
| `in_queue` | 任务已提交，排队中 |
| `generating` | 任务处理中 |
| `done` | 处理完成（成功或失败，看外层 code） |
| `not_found` | 任务未找到或已过期(12h) |
| `expired` | 任务已过期 |

### Video URL Expiry

**⚠️ 重要**: 生成的视频 URL 仅保留 **1 小时**，超时后自动清理，务必立即下载！

### Error Codes

| Code | Message | 描述 | 可重试 |
|------|---------|------|--------|
| 10000 | — | 成功 | — |
| 50411 | Pre Img Risk Not Pass | 输入图片审核未通过 | 否 |
| 50511 | Post Img Risk Not Pass | 输出图片审核未通过 | 是 |
| 50412 | Text Risk Not Pass | 输入文本审核未通过 | 否 |
| 50413 | Post Text Risk Not Pass | 输入文本含敏感词/版权词 | 否 |
| 50516 | Post Video Risk Not Pass | 输出视频审核未通过 | 是 |
| 50429 | Request Has Reached API Limit | QPS超限 | 是 |
| 50430 | Request Has Reached API Concurrent Limit | 并发超限 | 是 |
| 50500 | Internal Error | 内部错误 | 是 |
| 50501 | Internal RPC Error | 内部算法错误 | 是 |

---

## 火山方舟 Ark Seedance API (备选)

如需使用 Ark Seedance API（1.5 Pro 有声视频等高级功能），需单独配置 `ARK_API_KEY`。

详见：https://www.volcengine.com/docs/82379/1520757

---

## JSON Schemas

### seedance_request.json

```json
{
  "prompt": "string (建议不超过400字)",
  "images": ["string (本地路径/URL/base64)"],
  "image_roles": ["first_frame"],
  "duration": 10,
  "frames": 241,
  "seed": -1,
  "req_key": "jimeng_i2v_first_v30",
  "prompt_breakdown": {
    "character_description": "string",
    "action_description": "string",
    "camera_movement": "string",
    "style_modifiers": ["string"],
    "scene_description": "string"
  },
  "template_used": "rpg|action|strategy|casual",
  "mode": "image-to-video|text-to-video"
}
```

### video_result.json

```json
{
  "task_id": "string",
  "status": "SUCCESS|FAILED|SUBMITTED|TIMEOUT|NOT_FOUND|EXPIRED",
  "req_key": "jimeng_i2v_first_v30",
  "frames": 241,
  "duration_estimate": 10,
  "video_url": "string (1小时过期!)",
  "aigc_meta_tagged": true,
  "created_at": "ISO8601",
  "completed_at": "ISO8601",
  "local_path": "string",
  "error_message": "string|null",
  "error_code": "int|null",
  "request_id": "string"
}
```

### character_visual_profile.json

```json
{
  "appearance": {
    "gender": "string",
    "hair": "string",
    "clothing": "string",
    "body_type": "string",
    "distinguishing_features": ["string"]
  },
  "equipment": {
    "weapon": "string",
    "accessories": ["string"],
    "armor": "string"
  },
  "pose": {
    "stance": "string",
    "action": "string",
    "expression": "string"
  },
  "scene_elements": {
    "background": "string",
    "lighting": "string",
    "effects": ["string"]
  },
  "visual_style": {
    "art_style": "string",
    "color_palette": ["string"],
    "rendering_quality": "string"
  }
}
```

### character_lore_profile.json

```json
{
  "identity": {
    "name": "string",
    "game": "string",
    "element": "string",
    "role": "string",
    "rarity": "string"
  },
  "personality": "string",
  "voice_style": "string",
  "weapon": {
    "name": "string",
    "type": "string",
    "element": "string",
    "description": "string"
  },
  "signature_move": {
    "name": "string",
    "description": "string",
    "visual_effects": ["string"],
    "animation_sequence": ["string"]
  },
  "background": "string",
  "style_keywords": ["string"],
  "iconic_scenes": ["string"],
  "confidence": {
    "character_match": "high|medium|low",
    "notes": "string"
  }
}
```

---

## Project Directory Structure

```
projects/<project_name>/
├── input/
│   ├── screenshot.jpg
│   └── description.txt
├── character_visual_profile.json
├── character_lore_profile.json
├── seedance_request.json
├── video_result.json
└── output/
    └── video.mp4
```

---

## Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Project name | `{game}_{character}_{date}` | `genshin_diluc_20260512` |
| Screenshot | `screenshot.{ext}` | `screenshot.png` |
| Video output | `video_{timestamp}.mp4` | `video_20260512_010800.mp4` |

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `VOLC_ACCESS_KEY_ID` | Yes (即梦API) | 火山引擎 IAM AccessKeyID |
| `VOLC_SECRET_ACCESS_KEY` | Yes (即梦API) | 火山引擎 IAM SecretAccessKey |
| `ARK_API_KEY` | No (备选) | 火山方舟 ARK API Key |
| `JIMENG_TIMEOUT` | No | 轮询超时（秒），默认 600 |
