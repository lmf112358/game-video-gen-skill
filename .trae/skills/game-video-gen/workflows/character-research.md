# Character Research Workflow

> Standalone workflow for deep character research when the character is not found in the built-in database.

## Trigger

This workflow is triggered when:
- `character_db.py search` returns no results
- The Lore_Researcher cannot confidently identify the character
- The user explicitly requests deeper research

## Workflow

### Step 1: Visual Feature Extraction

🚧 **GATE**: `character_visual_profile.json` is available.

Review the visual profile and identify the most distinctive features for search:

1. **Hair color and style** — Most distinctive visual identifier
2. **Weapon type** — Narrows down game and character class
3. **Clothing/armor style** — Indicates game universe and character role
4. **Visual effects** — Element/ability indicators
5. **Art style** — Helps identify the game engine and art direction

### Step 2: Game Identification

Based on visual features, attempt to identify the source game:

| Visual Clue | Likely Game |
|-------------|-------------|
| Anime cel-shaded, element symbols | Genshin Impact |
| Sci-fi anime, space themes | Honkai: Star Rail |
| Dark tactical, industrial | Arknights |
| Post-apocalyptic, resonance effects | Wuthering Waves |
| Urban neon, glitch effects | Zenless Zone Zero |
| Fantasy anime, turn-based | Honkai Impact 3rd |
| Chibi style, tower defense | Arknights (Endfield) |

If the game cannot be identified, proceed with a generic game character profile.

### Step 3: AI-Powered Character Profile Construction

Using the visual profile and any game identification, construct a character profile by inference:

**Inference Rules**:

1. **Personality from appearance**:
   - Stern expression + heavy armor → "disciplined, resolute"
   - Bright smile + casual outfit → "cheerful, friendly"
   - Mysterious aura + dark clothing → "enigmatic, calculating"

2. **Weapon from visual**:
   - Large two-handed sword → claymore/greatsword type
   - Thin blade → sword/dagger type
   - Long shaft → polearm/spear type
   - Ranged weapon → bow/gun type
   - Glowing orb → catalyst/magic type

3. **Element from effects**:
   - Red/orange effects → Fire/Pyro
   - Blue/cyan effects → Ice/Cryo or Water/Hydro
   - Purple effects → Lightning/Electro
   - Green effects → Wind/Anemo or Nature/Dendro
   - Gold/amber effects → Earth/Geo

4. **Signature move from weapon + element**:
   - Fire + claymore → "powerful flaming overhead slash"
   - Lightning + polearm → "rapid lightning thrusts ending in electric explosion"
   - Ice + sword → "freezing slash creating ice crystals"
   - Wind + bow → "piercing wind arrow creating tornado"

### Step 4: Profile Validation

⛔ **BLOCKING**: Present the inferred character profile to the user with clear disclaimers:

```
⚠️ This character was not found in the built-in database.
The following profile was constructed by AI inference from visual features.
Please review and correct any inaccuracies.

[Character Profile]

Confidence: LOW
Please verify:
1. Is the character name correct?
2. Is the game identification correct?
3. Are the personality traits accurate?
4. Is the signature move description appropriate?
```

Wait for user confirmation or corrections before proceeding.

### Step 5: Save and Return

Save the confirmed profile as `character_lore_profile.json` with:

```json
{
  "identity": { ... },
  "personality": "...",
  "voice_style": "...",
  "weapon": { ... },
  "signature_move": { ... },
  "background": "...",
  "style_keywords": ["..."],
  "iconic_scenes": ["..."],
  "confidence": {
    "character_match": "low",
    "notes": "Profile constructed by AI inference, not from database. User-verified."
  }
}
```

Return to SKILL.md Step 4 (Prompt Engineering) with the completed profile.
