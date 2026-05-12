# Video Prompt Templates

Templates for constructing Seedance 2.0 prompts, organized by game genre.

---

## Template Structure

Every prompt follows this order:

```
[Character] + [Action] + [Camera] + [Scene] + [Style]
```

Priority when trimming to fit 2000 char limit: Action > Camera > Style > Scene > Character

---

## RPG Template

**Games**: Genshin Impact, Honkai: Star Rail, Wuthering Waves, Zenless Zone Zero

### Image-to-Video (with screenshot)

```
{character_name} {signature_move_animation}, {element_visual_effects}, {scene_from_description}, {camera_movement}, {art_style}, cinematic lighting, game marketing trailer quality
```

**Example (Diluc - Genshin Impact)**:
> Diluc unleashes his Dawn attack — raises his flaming claymore overhead, channels crimson energy, then swings downward releasing a massive phoenix-shaped fire projectile that illuminates the dark dungeon corridor, lingering embers and sparks, slow push-in to close-up, anime cel-shaded style, volumetric fire lighting, epic game marketing trailer quality

### Text-to-Video (no screenshot)

```
{character_name}, {appearance_description}, {signature_move_animation}, {element_visual_effects}, {scene_from_description}, {camera_movement}, {art_style}, cinematic lighting, game marketing trailer quality
```

**Example (Raiden Shogun - Genshin Impact)**:
> Raiden Shogun, purple-haired woman in imperial Japanese armor, draws a sword of pure lightning from her chest, assumes a floating stance, delivers a single devastating slash that warps reality, then plunges the blade creating a massive electro shockwave, purple lightning crackling across the battlefield, slow orbit camera, anime cel-shaded style, dramatic purple lighting, epic game marketing trailer quality

---

## Action Template

**Games**: Naraka: Bladepoint, Punishing: Gray Raven, Zenless Zone Zero (combat)

### Image-to-Video

```
{character_name} {rapid_combat_sequence}, {impact_effects}, {dynamic_camera}, {art_style}, high-octane game marketing style
```

**Example (Action character)**:
> Character dashes forward in a blur, executes a rapid three-hit combo with blazing weapon, each strike sending shockwaves of fire, final hit creates a massive explosion, dynamic camera follows each strike with slight slow-motion on impact, anime action style, intense fire particle effects, high-octane game marketing style

### Text-to-Video

```
{character_name}, {appearance}, {rapid_combat_sequence}, {impact_effects}, {dynamic_camera}, {art_style}, high-octane game marketing style
```

---

## Strategy Template

**Games**: Arknights, Azur Lane, Girls' Frontline

### Image-to-Video

```
{character_name} {tactical_skill_activation}, {area_effect}, {scene_description}, {dramatic_camera}, {art_style}, epic strategic marketing style
```

**Example (SilverAsh - Arknights)**:
> SilverAsh unleashes Truesilver Slash — assumes commanding stance, raises his longsword, channels freezing Arts energy, then delivers a massive horizontal slash sending waves of freezing energy across the entire battlefield, blizzard effects and ice crystals forming, slow dramatic pull-back reveal, tactical anime style, atmospheric cold lighting, epic strategic marketing style

### Text-to-Video

```
{character_name}, {appearance}, {commanding_presence}, {tactical_skill_activation}, {area_effect}, {dramatic_camera}, {art_style}, epic strategic marketing style
```

---

## Casual Template

**Games**: Social/casual games, idol games, cozy games

### Image-to-Video

```
{character_name} {charming_action}, {sparkle_effects}, {bright_scene}, {gentle_camera}, {art_style}, warm inviting marketing style
```

### Text-to-Video

```
{character_name}, {appearance}, {charming_action}, {sparkle_effects}, {bright_scene}, {gentle_camera}, {art_style}, warm inviting marketing style
```

---

## Camera Movement Reference

| Movement | Description | Use Case |
|----------|-------------|----------|
| `slow push-in to close-up` | Camera slowly moves toward subject | Character intro, dramatic reveal |
| `slow pull-back reveal` | Camera moves back revealing scene | Scene establishment, scale |
| `low angle tracking shot` | Camera follows from below | Power shots, boss moments |
| `orbit around subject` | Camera circles around | 360° showcase, character display |
| `dynamic follow cam` | Camera follows fast movement | Chase scenes, combat |
| `dramatic dutch angle` | Tilted camera | Tension, action sequences |
| `overhead bird's eye` | Top-down view | Scale, tactical overview |
| `crane shot rising` | Camera rises vertically | Grand reveal, epic scale |

---

## Style Modifier Reference

| Category | Modifiers |
|----------|-----------|
| Art Style | `anime cel-shaded`, `cinematic 3D render`, `painterly`, `pixel art`, `chibi` |
| Lighting | `volumetric lighting`, `dramatic backlight`, `golden hour`, `neon glow`, `moonlight` |
| Mood | `epic`, `mysterious`, `intense`, `melancholic`, `heroic`, `dark and brooding` |
| Quality | `high detail`, `4K quality`, `particle effects`, `motion blur`, `depth of field` |
| Marketing | `game marketing trailer quality`, `cinematic marketing shot`, `promotional video aesthetic` |

---

## Prompt Construction Checklist

Before finalizing a prompt, verify:

- [ ] Total length under 2000 characters
- [ ] Character description is first (or omitted for I2V)
- [ ] Action/motion is vividly described with specific verbs
- [ ] Camera movement is specified
- [ ] At least one style modifier is included
- [ ] Scene matches user's text description
- [ ] Element effects match character's element
- [ ] No negative words ("no", "without", "not")
- [ ] For I2V: prompt focuses on motion, not appearance
