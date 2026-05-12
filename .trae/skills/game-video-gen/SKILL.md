---
name: game-video-gen
description: >
  Game marketing video generation skill. Converts game character screenshots and text
  descriptions into 10s marketing videos via Jimeng AI (即梦) Visual API. Use when user asks to
  "generate game video", "create marketing video", "生成游戏视频", "生成营销视频",
  "游戏视频", or mentions "game-video-gen".
---

# Game Video Generator Skill

> AI-driven game marketing video generation system. Converts game character screenshots + text descriptions into high-quality short marketing videos through multi-role collaboration and Jimeng AI (即梦) Visual API.

**Core Pipeline**: `Screenshot Input → Character Analysis → Lore Research → Prompt Engineering → Video Generation → Quality Review`

> [!CAUTION]
> ## 🚨 Global Execution Discipline (MANDATORY)
>
> **This workflow is a strict serial pipeline. The following rules have the highest priority:**
>
> 1. **SERIAL EXECUTION** — Steps MUST be executed in order; the output of each step is the input for the next.
> 2. **BLOCKING = HARD STOP** — Steps marked ⛔ BLOCKING require a full stop; the AI MUST wait for an explicit user response before proceeding.
> 3. **NO CROSS-PHASE BUNDLING** — Cross-phase bundling is FORBIDDEN.
> 4. **GATE BEFORE ENTRY** — Each Step has prerequisites (🚧 GATE) listed at the top; these MUST be verified before starting that Step.
> 5. **NO SPECULATIVE EXECUTION** — "Pre-preparing" content for subsequent Steps is FORBIDDEN.
> 6. **NO SUB-AGENT VIDEO GENERATION** — Video generation MUST be completed by the current main agent end-to-end.

> [!IMPORTANT]
> ## 🌐 Language & Communication Rule
>
> - **Response language**: match the user's input language. Explicit user override takes precedence.
> - **JSON output fields**: use English field names regardless of conversation language. Content values may be in the user's language.

## Main Pipeline Scripts

| Script | Purpose |
|--------|---------|
| `${SKILL_DIR}/scripts/seedance_api.py` | Jimeng AI (即梦) Visual API client (HMAC auth, generate, poll) |
| `${SKILL_DIR}/scripts/image_analyzer.py` | Screenshot analysis (extract visual features) |
| `${SKILL_DIR}/scripts/character_db.py` | Game character knowledge base |
| `${SKILL_DIR}/scripts/video_manager.py` | Video project management (init, save, track) |
| `${SKILL_DIR}/scripts/video_download.py` | Video download and save |

## Standalone Workflows

| Workflow | Path | Purpose |
|----------|------|---------|
| `character-research` | `workflows/character-research.md` | Deep character research when not in built-in database |
| `video-iteration` | `workflows/video-iteration.md` | Video iteration and optimization after initial generation |

---

## Workflow

### Step 1: Input Processing

🚧 **GATE**: User has provided a game character screenshot (image file or URL) and a text description.

Receive and validate user input:

| User Provides | Action |
|---------------|--------|
| Local image file | Copy to project `input/` directory |
| Image URL | Download and save to project `input/` directory |
| Text description | Store as `input/description.txt` |
| Game name (optional) | Store as metadata for character lookup |

Initialize the project:

```bash
python3 ${SKILL_DIR}/scripts/video_manager.py init <project_name>
```

Save the screenshot to the project:

```bash
python3 ${SKILL_DIR}/scripts/video_manager.py save-input <project_path> --screenshot <image_path> --description "<text>"
```

**✅ Checkpoint — Input validated and project initialized. Proceed to Step 2.**

---

### Step 2: Character Analysis (Character_Analyst)

🚧 **GATE**: Step 1 complete; screenshot and description are saved in the project.

First, read the role definition:

```
Read references/character-analyst.md
```

Analyze the screenshot to extract visual features:

```bash
python3 ${SKILL_DIR}/scripts/image_analyzer.py <project_path>/input/screenshot.jpg
```

The analyzer outputs `character_visual_profile.json` containing:

```json
{
  "appearance": {
    "gender": "...",
    "hair": "...",
    "clothing": "...",
    "body_type": "...",
    "distinguishing_features": ["..."]
  },
  "equipment": {
    "weapon": "...",
    "accessories": ["..."],
    "armor": "..."
  },
  "pose": {
    "stance": "...",
    "action": "...",
    "expression": "..."
  },
  "scene_elements": {
    "background": "...",
    "lighting": "...",
    "effects": ["..."]
  },
  "visual_style": {
    "art_style": "...",
    "color_palette": ["..."],
    "rendering_quality": "..."
  }
}
```

**✅ Checkpoint — Visual profile extracted. Proceed to Step 3.**

---

### Step 3: Lore Research (Lore_Researcher)

🚧 **GATE**: Step 2 complete; `character_visual_profile.json` is available.

First, read the role definition:

```
Read references/lore-researcher.md
```

Query the character knowledge base:

```bash
python3 ${SKILL_DIR}/scripts/character_db.py search --visual-profile <project_path>/character_visual_profile.json
```

If the character is found in the database, the output is `character_lore_profile.json`. If not found, run the [`character-research`](workflows/character-research.md) workflow to build a temporary profile.

The lore profile contains:

```json
{
  "identity": {
    "name": "...",
    "game": "...",
    "element": "...",
    "role": "...",
    "rarity": "..."
  },
  "personality": "...",
  "voice_style": "...",
  "weapon": {
    "name": "...",
    "type": "...",
    "element": "...",
    "description": "..."
  },
  "signature_move": {
    "name": "...",
    "description": "...",
    "visual_effects": ["..."],
    "animation_sequence": ["..."]
  },
  "background": "...",
  "style_keywords": ["..."],
  "iconic_scenes": ["..."]
}
```

⛔ **BLOCKING**: Present the character lore profile to the user. Wait for explicit confirmation or modification before proceeding. The user may:
- Confirm the profile as-is
- Modify specific fields (e.g., correct the character name, adjust the signature move)
- Request deeper research via the `character-research` workflow

**✅ Checkpoint — Lore profile confirmed by user. Proceed to Step 4.**

---

### Step 4: Prompt Engineering (Prompt_Engineer)

🚧 **GATE**: Step 3 complete; `character_lore_profile.json` is confirmed by the user.

First, read the role definition:

```
Read references/prompt-engineer.md
```

Then read the prompt templates:

```
Read templates/prompt_templates.md
Read templates/style_references.md
```

Construct the Jimeng AI (即梦) video generation request by combining:

1. **Character visual profile** (from Step 2)
2. **Character lore profile** (from Step 3, user-confirmed)
3. **User's text description** (from Step 1)
4. **Selected prompt template** (based on game type)

Output `seedance_request.json`:

```json
{
  "prompt": "...",
  "images": ["..."],
  "image_roles": ["first_frame"],
  "duration": 10,
  "frames": 241,
  "seed": -1,
  "req_key": "jimeng_i2v_first_v30",
  "prompt_breakdown": {
    "character_description": "...",
    "action_description": "...",
    "camera_movement": "...",
    "style_modifiers": ["..."],
    "scene_description": "..."
  }
}
```

| Parameter | Default | When to Change |
|-----------|---------|----------------|
| `duration` | 10 | 5 for simple actions (sets frames=121) |
| `frames` | 241 (10s) | 121 for 5s; 241 for 10s; formula: 24×n+1 |
| `seed` | -1 | Set positive integer for reproducible results |
| `req_key` | "jimeng_i2v_first_v30" | Different model key for other capabilities |
| `images` | [screenshot path/URL] | Omit for text-to-video mode |

**Prompt construction rules**:
- Chinese prompt: 建议不超过400字，不超过800字
- Character description comes first (who)
- Action description comes second (what)
- Camera movement comes third (how we see it)
- Style modifiers come last (mood/aesthetic)
- When using image-to-video, the prompt should describe motion and action, not appearance (appearance comes from the reference image)
- Duration is controlled by `frames`: 5s=121, 10s=241

⛔ **BLOCKING**: Present the Seedance request to the user. Wait for explicit confirmation or modification. The user may:
- Confirm the request as-is
- Modify the prompt text
- Adjust video parameters (duration, aspect ratio, model)
- Request a different prompt template

**✅ Checkpoint — Seedance request confirmed by user. Proceed to Step 5.**

---

### Step 5: Video Generation (Video_Director)

🚧 **GATE**: Step 4 complete; `seedance_request.json` is confirmed by the user.

First, read the role definition:

```
Read references/video-director.md
```

Submit the video generation task:

```bash
python3 ${SKILL_DIR}/scripts/seedance_api.py generate \
  --request <project_path>/seedance_request.json \
  --output <project_path>/video_result.json
```

This submits the task to Seedance 2.0 API and returns a `task_id`.

Poll for completion:

```bash
python3 ${SKILL_DIR}/scripts/seedance_api.py poll \
  --task-id <task_id> \
  --output <project_path>/video_result.json \
  --interval 10 \
  --timeout 600
```

When status is `SUCCESS`, download the video:

```bash
python3 ${SKILL_DIR}/scripts/video_download.py \
  --url <video_url> \
  --output <project_path>/output/video.mp4
```

**Error handling**:
- If `50411/50412/50413` (content risk): inform user, modify prompt or image
- If `50429/50430` (rate limit): wait 60s and retry
- If `50500/50501` (internal error): retry once
- If `FAILED`: retry once; if still fails, inform user
- If timeout: inform user the task is still processing, provide task_id for manual checking

**✅ Checkpoint — Video generated and downloaded. Proceed to Step 6.**

---

### Step 6: Quality Review

🚧 **GATE**: Step 5 complete; video file is available in the project.

Present the generated video to the user with a summary:

```
## 🎬 Video Generated Successfully

- **Project**: <project_name>
- **Character**: <character_name>
- **Duration**: <duration>s
- **Resolution**: <resolution>
- **Model**: <model>
- **Video Path**: <project_path>/output/video.mp4

The video has been saved to your project directory.
```

The user may:
- ✅ Accept the result — workflow complete
- 🔄 Request iteration — run the [`video-iteration`](workflows/video-iteration.md) workflow
- 🔄 Request regeneration with modified prompt — return to Step 4

**✅ Checkpoint — Workflow complete or iteration requested.**

---

## Quick Reference

### Environment Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your Seedance API key
```

### Project Structure

```
projects/<project_name>/
├── input/
│   ├── screenshot.jpg              # Original screenshot
│   └── description.txt             # User's text description
├── character_visual_profile.json   # Step 2 output
├── character_lore_profile.json     # Step 3 output
├── seedance_request.json           # Step 4 output
├── video_result.json               # Step 5 output
└── output/
    └── video.mp4                   # Final video
```

### API Key Configuration

Set `VOLC_ACCESS_KEY_ID` and `VOLC_SECRET_ACCESS_KEY` in one of:
1. `.env` file in project root
2. Environment variables

Get your credentials from: https://console.volcengine.com/iam/keymanage/

### Supported Games (Built-in Database)

| Game | Characters | Status |
|------|-----------|--------|
| Genshin Impact | 20+ | Built-in |
| Honkai: Star Rail | 15+ | Built-in |
| Arknights | 15+ | Built-in |
| Wuthering Waves | 10+ | Built-in |
| Zenless Zone Zero | 10+ | Built-in |

> Characters not in the database will trigger the `character-research` workflow for AI-powered profile construction.
