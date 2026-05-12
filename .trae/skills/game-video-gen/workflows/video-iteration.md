# Video Iteration Workflow

> Standalone workflow for iterating and optimizing generated videos.

## Trigger

This workflow is triggered when:
- The user is unsatisfied with the generated video
- The user requests modifications to the video
- The quality review in Step 6 identifies issues

## Common Issues and Fixes

### Issue 1: Character Inconsistency

**Symptom**: Generated character doesn't match the reference screenshot.

**Fix**:
1. Strengthen the image reference by ensuring the screenshot is high-quality and clearly shows the character
2. Add more specific character description to the prompt (even in I2V mode)
3. Use `seedance-2.0` (standard) instead of `seedance-2.0-fast` for better consistency

**Prompt adjustment**:
```
Before: "Character swings a flaming sword..."
After:  "The red-haired knight in dark armor swings a flaming claymore..."
```

### Issue 2: Insufficient Action/Motion

**Symptom**: Video is too static, character barely moves.

**Fix**:
1. Add more dynamic verbs and motion descriptions
2. Specify camera movement to create perceived motion
3. Describe sequential actions instead of a single action

**Prompt adjustment**:
```
Before: "Character stands with a flaming sword"
After:  "Character charges forward, leaps into the air, and delivers a devastating downward slash with the flaming sword, creating a shockwave of fire"
```

### Issue 3: Wrong Scene/Environment

**Symptom**: Generated scene doesn't match the user's description.

**Fix**:
1. Move scene description earlier in the prompt
2. Add more specific environmental details
3. Include lighting and atmosphere descriptions

**Prompt adjustment**:
```
Before: "Character fights in a dungeon"
After:  "In a dimly lit stone dungeon corridor with flickering torches and moss-covered walls, character fights..."
```

### Issue 4: Poor Style Match

**Symptom**: Video style doesn't match the game's art direction.

**Fix**:
1. Add game-specific style keywords from `style_references.md`
2. Include art style modifiers explicitly
3. Add quality and rendering descriptors

**Prompt adjustment**:
```
Before: "Character attacks with fire"
After:  "Character attacks with fire, anime cel-shaded style, vibrant colors, elemental particle effects, cinematic anime camera, game marketing trailer quality"
```

### Issue 5: Too Short/Too Long Actions

**Symptom**: Actions feel rushed (5s) or drawn out (15s).

**Fix**:
- For 5s: Focus on one impactful action
- For 10s: Describe 2-3 sequential actions
- For 15s: Include build-up, climax, and resolution

## Iteration Process

### Step 1: Identify the Issue

Ask the user what specifically they want to improve:

| Question | Options |
|----------|---------|
| What needs improvement? | Character look / Action / Scene / Style / Duration |
| How would you describe the issue? | [Free text] |
| What should change? | More dynamic / More accurate / Different scene / Different style |

### Step 2: Adjust the Prompt

Based on the identified issue, modify `seedance_request.json`:

1. Read the current request
2. Apply the appropriate fix from the common issues above
3. Update `prompt_breakdown` to reflect changes
4. Save the updated request

### Step 3: Regenerate

Submit the modified request:

```bash
python3 ${SKILL_DIR}/scripts/seedance_api.py generate \
  --request <project_path>/seedance_request.json \
  --output <project_path>/video_result_v2.json
```

Poll and download as in the main workflow.

### Step 4: Compare and Evaluate

Present both versions to the user:

```
## Video Comparison

| | V1 (Original) | V2 (Iteration) |
|---|---|---|
| Prompt | [summary] | [summary] |
| Changes | — | [what changed] |
| Video | [path] | [path] |

Which version do you prefer?
- Keep V2
- Keep V1
- Iterate again
```

### Step 5: Finalize or Continue

- If user accepts V2 → Replace original video, workflow complete
- If user wants another iteration → Return to Step 2
- If user wants to revert → Keep V1, workflow complete

## Iteration Limits

- Maximum 3 iterations per video to avoid excessive API usage
- After 3 iterations, suggest the user adjust their input (screenshot or description) instead
- Track iteration count in `project_meta.json`
