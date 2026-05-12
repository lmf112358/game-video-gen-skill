import argparse
import json
import os
import sys

CHARACTER_DATABASE = {
    "genshin_impact": {
        "diluc": {
            "identity": {
                "name": "Diluc",
                "name_cn": "迪卢克",
                "game": "Genshin Impact",
                "game_cn": "原神",
                "element": "Pyro",
                "element_cn": "火",
                "role": "Main DPS",
                "rarity": "5-star"
            },
            "personality": "Stoic and reserved, driven by a strong sense of justice. Speaks little but acts decisively. Carries the weight of his past silently.",
            "voice_style": "Deep, measured, and authoritative. Each word carries weight. Low and magnetic, concise and forceful.",
            "weapon": {
                "name": "Claymore",
                "type": "claymore",
                "element": "Pyro",
                "description": "A massive two-handed sword engulfed in crimson flames when channeling Pyro energy"
            },
            "signature_move": {
                "name": "Dawn",
                "name_cn": "黎明",
                "description": "Releases a giant flaming bird that sweeps forward, then explodes in a massive firestorm",
                "visual_effects": ["phoenix-shaped flame projectile", "explosive fire burst", "lingering burn marks", "screen-wide crimson flash"],
                "animation_sequence": ["raise claymore overhead", "channel pyro energy into blade", "swing downward releasing phoenix", "phoenix sweeps forward", "massive fiery explosion"]
            },
            "background": "The uncrowned king of Mondstadt's wine industry and its secret dark knight hero. Lost his father to a Fatui plot and now fights alone against injustice.",
            "style_keywords": ["flame aura", "crimson glow", "eagle feathers", "powerful overhead swing", "dark knight aesthetic", "wine red palette"],
            "iconic_scenes": ["Standing atop Dawn Winery at sunset", "Unleashing Dawn burst in a dark alley", "Walking through Mondstadt streets at night"],
            "visual_cues": {
                "hair": "red",
                "clothing": "dark knight armor",
                "weapon_type": "claymore",
                "element_color": "crimson"
            }
        },
        "raiden_shogun": {
            "identity": {
                "name": "Raiden Shogun",
                "name_cn": "雷电将军",
                "game": "Genshin Impact",
                "game_cn": "原神",
                "element": "Electro",
                "element_cn": "雷",
                "role": "Main DPS / Battery",
                "rarity": "5-star"
            },
            "personality": "Majestic and imperious, with an otherworldly detachment from mortal concerns. Speaks with absolute authority.",
            "voice_style": "Regal and commanding, with an ethereal quality. Each statement is delivered as an absolute decree.",
            "weapon": {
                "name": "Polearm (Engulfing Lightning)",
                "type": "polearm",
                "element": "Electro",
                "description": "A naginata-style polearm crackling with purple lightning, capable of cutting through eternity itself"
            },
            "signature_move": {
                "name": "Secret Art: Musou Shinsetsu",
                "name_cn": "奥义·梦想真说",
                "description": "Draws a sword of pure lightning from her chest, slashes through reality, then plunges the blade creating a massive electro explosion",
                "visual_effects": ["purple lightning blade", "reality-warping slash", "electro explosion", "floating musou no hitotachi stance"],
                "animation_sequence": ["pull lightning sword from chest", "assume floating stance", "single devastating slash", "plunge blade into ground", "massive electro shockwave"]
            },
            "background": "The Electro Archon and ruler of Inazuma, who pursues eternity by freezing all change under the Vision Hunt Decree.",
            "style_keywords": ["purple lightning", "imperial authority", "eternal stillness", "floating stance", "sakura petals", "electro crackle"],
            "iconic_scenes": ["Floating above Inazuma city", "Drawing the Musou Isshin from her chest", "Standing before the Statue of the Omnipresent God"],
            "visual_cues": {
                "hair": "purple long braid",
                "clothing": "japanese imperial armor",
                "weapon_type": "polearm",
                "element_color": "purple"
            }
        },
        "zhongli": {
            "identity": {
                "name": "Zhongli",
                "name_cn": "钟离",
                "game": "Genshin Impact",
                "game_cn": "原神",
                "element": "Geo",
                "element_cn": "岩",
                "role": "Shield Support",
                "rarity": "5-star"
            },
            "personality": "Elegant and knowledgeable, speaks with the wisdom of six thousand years. Calm and composed in any situation.",
            "voice_style": "Deep and resonant, measured and scholarly. Speaks with ancient authority and refined eloquence.",
            "weapon": {
                "name": "Polearm (Staff of Homa)",
                "type": "polearm",
                "element": "Geo",
                "description": "An elegant polearm that summons geo constructs and meteor strikes"
            },
            "signature_move": {
                "name": "Planet Befall",
                "name_cn": "天星",
                "description": "Summons a massive meteor from the sky that crashes down, petrifying all enemies in its impact zone",
                "visual_effects": ["giant falling meteor", "golden geo energy", "petrification effect", "ground-shaking impact"],
                "animation_sequence": ["raise hand to sky", "summon massive meteor", "meteor descends with golden trail", "catastrophic impact", "enemies turn to stone"]
            },
            "background": "The retired Geo Archon Rex Lapis, who walked among mortals as a funeral consultant in Liyue after stepping down from godhood.",
            "style_keywords": ["golden geo energy", "ancient wisdom", "meteor strike", "dragon motifs", "amber glow", "imperial elegance"],
            "iconic_scenes": ["Summoning a meteor over Liyue Harbor", "Sipping tea at a Liyue teahouse", "Standing before the Golden House"],
            "visual_cues": {
                "hair": "dark brown with amber tips",
                "clothing": "formal geo-themed suit",
                "weapon_type": "polearm",
                "element_color": "amber gold"
            }
        }
    },
    "honkai_star_rail": {
        "jing_yuan": {
            "identity": {
                "name": "Jing Yuan",
                "name_cn": "景元",
                "game": "Honkai: Star Rail",
                "game_cn": "崩坏：星穹铁道",
                "element": "Lightning",
                "element_cn": "雷",
                "role": "Follow-up DPS",
                "rarity": "5-star"
            },
            "personality": "Laid-back and seemingly lazy, but possesses sharp tactical intellect. Known as the Dozing General.",
            "voice_style": "Relaxed and unhurried, with underlying authority. Speaks casually but with strategic depth.",
            "weapon": {
                "name": "Cloud-Piercer",
                "type": "polearm",
                "element": "Lightning",
                "description": "An ornate polearm that summons the Lightning-Lord, a divine lion construct of pure electro energy"
            },
            "signature_move": {
                "name": "Lightning-Lord, Merciful Bloom",
                "name_cn": "神君·花开无处",
                "description": "Summons the Lightning-Lord who delivers devastating lightning slashes, increasing in power with each strike",
                "visual_effects": ["giant lightning lion construct", "progressive lightning slashes", "golden-red energy", "divine authority aura"],
                "animation_sequence": ["lazy stance shift", "summon Lightning-Lord behind", "lion delivers rapid slashes", "final devastating strike", "lightning explosion"]
            },
            "background": "The Divine Foresight of the Xianzhou Luofu and one of the six Arbiter-Generals. Known for his strategic brilliance masked by apparent laziness.",
            "style_keywords": ["lightning lion", "golden-red energy", "divine authority", "lazy power", "xianzhou aesthetic", "strategic mastery"],
            "iconic_scenes": ["Dozing at the Seat of Divine Foresight", "Summoning the Lightning-Lord in battle", "Standing amid Xianzhou architecture"],
            "visual_cues": {
                "hair": "long white hair",
                "clothing": "xianzhou general armor",
                "weapon_type": "polearm",
                "element_color": "golden-red"
            }
        },
        "kafka": {
            "identity": {
                "name": "Kafka",
                "name_cn": "卡芙卡",
                "game": "Honkai: Star Rail",
                "game_cn": "崩坏：星穹铁道",
                "element": "Lightning",
                "element_cn": "雷",
                "role": "DoT DPS",
                "rarity": "5-star"
            },
            "personality": "Enigmatic and alluring, with a motherly yet dangerous charm. Speaks in a mesmerizing, hypnotic tone.",
            "voice_style": "Husky and seductive, with a hypnotic cadence. Every word feels like a gentle command.",
            "weapon": {
                "name": "Submachine Guns",
                "type": "ranged",
                "element": "Lightning",
                "description": "Dual submachine guns that fire lightning-infused bullets, creating webs of electric shock"
            },
            "signature_move": {
                "name": "Twilight Trill",
                "name_cn": "暮色交响",
                "description": "Unleashes a barrage of lightning bullets that create cascading shock webs, then detonates all accumulated shocks in a purple explosion",
                "visual_effects": ["lightning bullet barrage", "cascading shock webs", "purple electro explosion", "spider-web patterns"],
                "animation_sequence": ["draw dual guns", "fire lightning bullet barrage", "shock webs spread across field", "snap fingers to detonate", "massive purple explosion"]
            },
            "background": "A member of the Stellaron Hunters and the one who created the Trailblazer. Obsessed with the feeling of fear, which she can no longer experience.",
            "style_keywords": ["purple lightning", "spider motifs", "hypnotic charm", "dual guns", "shock webs", "mysterious allure"],
            "iconic_scenes": ["Emerging from shadows with a smile", "Firing lightning bullets in slow motion", "Standing amid purple lightning arcs"],
            "visual_cues": {
                "hair": "purple short hair",
                "clothing": "black tactical outfit with spider motifs",
                "weapon_type": "dual guns",
                "element_color": "purple"
            }
        }
    },
    "arknights": {
        "silverash": {
            "identity": {
                "name": "SilverAsh",
                "name_cn": "银灰",
                "game": "Arknights",
                "game_cn": "明日方舟",
                "element": "Arts (Ice)",
                "element_cn": "源石技艺（冰）",
                "role": "Guard (Ranged)",
                "rarity": "6-star"
            },
            "personality": "Ambitious and calculating, with absolute confidence in his vision. A natural leader who sees everything as pieces on his board.",
            "voice_style": "Calm and authoritative, with a slight edge of superiority. Speaks with the certainty of a ruler.",
            "weapon": {
                "name": "Longsword (Arts-infused)",
                "type": "sword",
                "element": "Arts (Ice)",
                "description": "An elegant longsword that channels freezing Arts energy, creating ice crystals and blizzard effects"
            },
            "signature_move": {
                "name": "Truesilver Slash",
                "name_cn": "真银斩",
                "description": "Unleashes a devastating wide-area slash that sends waves of freezing energy across the entire battlefield",
                "visual_effects": ["wide-area ice slash", "freezing shockwave", "blizzard effect", "silver energy trails"],
                "animation_sequence": ["assume commanding stance", "raise longsword", "channel freezing arts", "massive horizontal slash", "freezing shockwave expands"]
            },
            "background": "The leader of Karlan and head of the Karlan Commercial. A brilliant strategist who will sacrifice anything for his vision of a better future.",
            "style_keywords": ["silver ice energy", "commanding presence", "blizzard effects", "noble authority", "freezing slash", "strategic mastermind"],
            "iconic_scenes": ["Standing atop Karlan mountains", "Unleashing Truesilver Slash across the battlefield", "Overlooking his domain with calculating eyes"],
            "visual_cues": {
                "hair": "silver-white",
                "clothing": "military commander uniform",
                "weapon_type": "longsword",
                "element_color": "silver ice"
            }
        }
    },
    "wuthering_waves": {
        "jiyan": {
            "identity": {
                "name": "Jiyan",
                "name_cn": "鉴心",
                "game": "Wuthering Waves",
                "game_cn": "鸣潮",
                "element": "Broadblade",
                "element_cn": "长刃",
                "role": "Resonator",
                "rarity": "5-star"
            },
            "personality": "Disciplined and resolute, with unwavering dedication to protecting others. A natural warrior.",
            "voice_style": "Firm and commanding, with undertones of compassion. Speaks with military precision.",
            "weapon": {
                "name": "Broadblade",
                "type": "broadblade",
                "element": "Aero",
                "description": "A massive broadblade that channels wind energy, creating devastating aerial slashes"
            },
            "signature_move": {
                "name": "Verdant Wind",
                "name_cn": "翠风",
                "description": "Leaps into the air and delivers a devastating downward slash creating a massive wind explosion",
                "visual_effects": ["wind energy blade", "aerial leap", "downward slash shockwave", "green wind explosion"],
                "animation_sequence": ["charge wind energy", "leap into air", "raise broadblade overhead", "devastating downward slash", "massive wind explosion"]
            },
            "background": "A disciplined warrior who channels the power of wind through his broadblade to protect those who cannot protect themselves.",
            "style_keywords": ["wind energy", "green aura", "aerial combat", "broadblade mastery", "disciplined warrior", "protective resolve"],
            "iconic_scenes": ["Leaping into battle with wind trailing", "Delivering the decisive downward slash", "Standing guard over allies"],
            "visual_cues": {
                "hair": "dark with green highlights",
                "clothing": "military-style combat gear",
                "weapon_type": "broadblade",
                "element_color": "green wind"
            }
        }
    }
}


def search_by_name(name, game=None):
    results = []
    name_lower = name.lower().strip()

    games_to_search = [game.lower()] if game else CHARACTER_DATABASE.keys()

    for game_key in games_to_search:
        if game_key not in CHARACTER_DATABASE:
            continue
        for char_key, char_data in CHARACTER_DATABASE[game_key].items():
            identity = char_data.get("identity", {})
            if (name_lower == char_key.lower() or
                name_lower == identity.get("name", "").lower() or
                name_lower == identity.get("name_cn", "")):
                results.append({
                    "game_key": game_key,
                    "char_key": char_key,
                    "data": char_data,
                    "match_type": "exact"
                })

    if not results:
        for game_key in CHARACTER_DATABASE:
            for char_key, char_data in CHARACTER_DATABASE[game_key].items():
                identity = char_data.get("identity", {})
                if (name_lower in char_key.lower() or
                    name_lower in identity.get("name", "").lower() or
                    name_lower in identity.get("name_cn", "")):
                    results.append({
                        "game_key": game_key,
                        "char_key": char_key,
                        "data": char_data,
                        "match_type": "partial"
                    })

    return results


def search_by_visual_cues(visual_profile, game=None):
    results = []
    appearance = visual_profile.get("appearance", {})
    equipment = visual_profile.get("equipment", {})

    search_hair = appearance.get("hair", "").lower()
    search_weapon = equipment.get("weapon", "").lower()

    if search_hair == "not visible" and search_weapon == "not visible":
        return results

    games_to_search = [game.lower()] if game else CHARACTER_DATABASE.keys()

    for game_key in games_to_search:
        if game_key not in CHARACTER_DATABASE:
            continue
        for char_key, char_data in CHARACTER_DATABASE[game_key].items():
            cues = char_data.get("visual_cues", {})
            score = 0

            if search_hair != "not visible":
                cue_hair = cues.get("hair", "").lower()
                if any(word in cue_hair for word in search_hair.split() if len(word) > 2):
                    score += 2

            if search_weapon != "not visible":
                cue_weapon = cues.get("weapon_type", "").lower()
                if any(word in cue_weapon for word in search_weapon.split() if len(word) > 2):
                    score += 2

            if score > 0:
                results.append({
                    "game_key": game_key,
                    "char_key": char_key,
                    "data": char_data,
                    "match_type": "visual",
                    "match_score": score
                })

    results.sort(key=lambda x: x.get("match_score", 0), reverse=True)
    return results


def list_characters(game=None):
    output = []
    games_to_list = [game.lower()] if game else CHARACTER_DATABASE.keys()

    for game_key in games_to_list:
        if game_key not in CHARACTER_DATABASE:
            continue
        for char_key, char_data in CHARACTER_DATABASE[game_key].items():
            identity = char_data.get("identity", {})
            output.append({
                "game": identity.get("game", game_key),
                "game_cn": identity.get("game_cn", ""),
                "name": identity.get("name", char_key),
                "name_cn": identity.get("name_cn", ""),
                "element": identity.get("element", ""),
                "rarity": identity.get("rarity", "")
            })

    return output


def main():
    parser = argparse.ArgumentParser(description="Game Character Knowledge Base")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    search_parser = subparsers.add_parser("search", help="Search for a character")
    search_parser.add_argument("--name", help="Character name to search")
    search_parser.add_argument("--game", help="Game name to filter")
    search_parser.add_argument("--visual-profile", help="Path to character_visual_profile.json for visual matching")

    list_parser = subparsers.add_parser("list", help="List all characters")
    list_parser.add_argument("--game", help="Game name to filter")

    args = parser.parse_args()

    if args.command == "search":
        seen_keys = set()
        results = []

        if args.name:
            name_results = search_by_name(args.name, args.game)
            for r in name_results:
                key = (r["game_key"], r["char_key"])
                if key not in seen_keys:
                    seen_keys.add(key)
                    results.append(r)
            if name_results:
                print(f"Found {len(results)} match(es) by name:")
                for r in results:
                    identity = r["data"]["identity"]
                    print(f"  [{r['match_type']}] {identity.get('name_cn', '')} ({identity.get('name', '')}) - {identity.get('game_cn', '')}")

        if args.visual_profile:
            if os.path.exists(args.visual_profile):
                with open(args.visual_profile, "r", encoding="utf-8") as f:
                    visual_profile = json.load(f)
                visual_results = search_by_visual_cues(visual_profile, args.game)
                if visual_results:
                    print(f"Found {len(visual_results)} match(es) by visual cues:")
                    for r in visual_results:
                        identity = r["data"]["identity"]
                        print(f"  [score: {r.get('match_score', 0)}] {identity.get('name_cn', '')} ({identity.get('name', '')}) - {identity.get('game_cn', '')}")
                    for r in visual_results:
                        key = (r["game_key"], r["char_key"])
                        if key not in seen_keys:
                            seen_keys.add(key)
                            results.append(r)
            else:
                print(f"Visual profile not found: {args.visual_profile}", file=sys.stderr)

        if not args.name and not args.visual_profile:
            print("Please provide --name or --visual-profile", file=sys.stderr)
            sys.exit(1)

        if not results:
            print("No matching characters found in database.")
            print("The character-research workflow will be triggered for AI-powered profile construction.")

    elif args.command == "list":
        characters = list_characters(args.game)
        if characters:
            print(f"Available characters ({len(characters)}):")
            for c in characters:
                print(f"  {c['name_cn']} ({c['name']}) - {c['game_cn']} [{c['element']}] {c['rarity']}")
        else:
            print("No characters found.")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
