import argparse
import json
import os
import sys

from PIL import Image


def analyze_image_metadata(image_path):
    metadata = {}
    try:
        img = Image.open(image_path)
        metadata["width"] = img.width
        metadata["height"] = img.height
        metadata["format"] = img.format
        metadata["mode"] = img.mode
        metadata["aspect_ratio"] = f"{img.width}:{img.height}"

        if img.width >= 1920 or img.height >= 1080:
            metadata["quality_tier"] = "high"
        elif img.width >= 1280 or img.height >= 720:
            metadata["quality_tier"] = "medium"
        else:
            metadata["quality_tier"] = "low"

        thumbnail = img.copy()
        thumbnail.thumbnail((100, 100))
        pixels = list(thumbnail.getdata())

        r_avg = sum(p[0] for p in pixels) / len(pixels)
        g_avg = sum(p[1] for p in pixels) / len(pixels)
        b_avg = sum(p[2] for p in pixels) / len(pixels)

        metadata["dominant_color_channel"] = "red" if r_avg > g_avg and r_avg > b_avg else \
            "green" if g_avg > r_avg and g_avg > b_avg else "blue"
        metadata["brightness"] = (r_avg + g_avg + b_avg) / 3 / 255
        metadata["color_temperature"] = "warm" if r_avg > b_avg else "cool"

        img.close()
    except Exception as e:
        metadata["error"] = str(e)

    return metadata


def extract_visual_features(image_path):
    profile = {
        "appearance": {
            "gender": "not visible",
            "hair": "not visible",
            "clothing": "not visible",
            "body_type": "not visible",
            "distinguishing_features": []
        },
        "equipment": {
            "weapon": "not visible",
            "accessories": [],
            "armor": "not visible"
        },
        "pose": {
            "stance": "not visible",
            "action": "not visible",
            "expression": "not visible"
        },
        "scene_elements": {
            "background": "not visible",
            "lighting": "not visible",
            "effects": []
        },
        "visual_style": {
            "art_style": "not visible",
            "color_palette": [],
            "rendering_quality": "not visible"
        },
        "image_metadata": {}
    }

    metadata = analyze_image_metadata(image_path)
    profile["image_metadata"] = metadata

    if metadata.get("color_temperature") == "warm":
        profile["scene_elements"]["lighting"] = "warm lighting (detected from image)"
    else:
        profile["scene_elements"]["lighting"] = "cool lighting (detected from image)"

    if metadata.get("quality_tier"):
        profile["visual_style"]["rendering_quality"] = f"{metadata['quality_tier']}-quality image"

    return profile


ALLOWED_IMAGE_FORMATS = {".jpg", ".jpeg", ".png"}
MAX_IMAGE_SIZE_MB = 4.7
MAX_IMAGE_DIMENSION = 4096


def _validate_image(image_path):
    ext = os.path.splitext(image_path)[1].lower()
    if ext not in ALLOWED_IMAGE_FORMATS and ext != ".webp":
        print(f"WARNING: Image format '{ext}' may not be supported. Jimeng API recommends JPEG/PNG.", file=sys.stderr)

    try:
        size_mb = os.path.getsize(image_path) / (1024 * 1024)
        if size_mb > MAX_IMAGE_SIZE_MB:
            print(f"ERROR: Image too large ({size_mb:.1f} MB). Max {MAX_IMAGE_SIZE_MB} MB for Jimeng API.", file=sys.stderr)
            sys.exit(1)
    except OSError:
        pass

    try:
        img = Image.open(image_path)
        if img.width > MAX_IMAGE_DIMENSION or img.height > MAX_IMAGE_DIMENSION:
            print(f"WARNING: Image dimensions ({img.width}x{img.height}) exceed {MAX_IMAGE_DIMENSION}x{MAX_IMAGE_DIMENSION}. Jimeng API may reject.", file=sys.stderr)
        if img.width / max(img.height, 1) > 3 or img.height / max(img.width, 1) > 3:
            print(f"WARNING: Aspect ratio ({img.width}/{img.height}) exceeds 3:1 limit. Jimeng API may reject.", file=sys.stderr)
        img.close()
    except Exception:
        pass


def analyze_screenshot(image_path, output_path=None):
    if not os.path.exists(image_path):
        if image_path.startswith("http://") or image_path.startswith("https://"):
            pass
        else:
            print(f"ERROR: Image file not found: {image_path}", file=sys.stderr)
            sys.exit(1)

    local_file = None
    if image_path.startswith("http://") or image_path.startswith("https://"):
        import tempfile
        import requests as req_lib
        try:
            resp = req_lib.get(image_path, timeout=30)
            resp.raise_for_status()
            suffix = os.path.splitext(image_path.split("?")[0])[1] or ".jpg"
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp.write(resp.content)
            tmp.close()
            local_file = tmp.name
            image_path = local_file
        except Exception as e:
            print(f"ERROR: Failed to download image: {e}", file=sys.stderr)
            sys.exit(1)

    _validate_image(image_path)

    print(f"Analyzing screenshot: {image_path}")

    try:
        profile = extract_visual_features(image_path)
    finally:
        if local_file and os.path.exists(local_file):
            os.unlink(local_file)

    print("\n=== Visual Profile (Auto-detected) ===")
    print(f"Image: {profile['image_metadata'].get('width', '?')}x{profile['image_metadata'].get('height', '?')}")
    print(f"Quality: {profile['visual_style']['rendering_quality']}")
    print(f"Lighting: {profile['scene_elements']['lighting']}")
    print()
    print("NOTE: Auto-detection can only extract basic image metadata (resolution, color temperature, etc.).")
    print("Character features (appearance, equipment, pose, etc.) require AI vision analysis.")
    print("The AI agent will fill in these fields during the Character_Analyst step.")

    if output_path:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        print(f"\nProfile saved to: {output_path}")

    return profile


def main():
    parser = argparse.ArgumentParser(description="Game Screenshot Analyzer")
    parser.add_argument("image", help="Path or URL to game screenshot")
    parser.add_argument("--output", "-o", help="Output path for character_visual_profile.json")

    args = parser.parse_args()

    analyze_screenshot(args.image, args.output)


if __name__ == "__main__":
    main()
