import argparse
import json
import os
import shutil
import sys
from datetime import datetime


def init_project(project_name, base_dir=None):
    if base_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        skill_dir = os.path.dirname(script_dir)
        game_video_gen_dir = os.path.dirname(skill_dir)
        skills_dir = os.path.dirname(game_video_gen_dir)
        trae_dir = os.path.dirname(skills_dir)
        base_dir = os.path.join(trae_dir, "projects")

    project_path = os.path.join(base_dir, project_name)

    if os.path.exists(project_path):
        print(f"Project already exists: {project_path}")
        return project_path

    os.makedirs(os.path.join(project_path, "input"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "output"), exist_ok=True)

    meta = {
        "project_name": project_name,
        "created_at": datetime.now().isoformat(),
        "status": "initialized",
        "steps_completed": [],
        "steps_remaining": [
            "character_analysis",
            "lore_research",
            "prompt_engineering",
            "video_generation",
            "quality_review"
        ]
    }

    with open(os.path.join(project_path, "project_meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"Project initialized: {project_path}")
    return project_path


def save_input(project_path, screenshot=None, description=None):
    input_dir = os.path.join(project_path, "input")
    os.makedirs(input_dir, exist_ok=True)

    if screenshot:
        if screenshot.startswith("http://") or screenshot.startswith("https://"):
            import requests
            try:
                resp = requests.get(screenshot, timeout=30)
                resp.raise_for_status()
                suffix = os.path.splitext(screenshot.split("?")[0])[1] or ".jpg"
                dest = os.path.join(input_dir, f"screenshot{suffix}")
                with open(dest, "wb") as f:
                    f.write(resp.content)
                print(f"Screenshot downloaded to: {dest}")
            except Exception as e:
                print(f"Failed to download screenshot: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            if not os.path.exists(screenshot):
                print(f"Screenshot file not found: {screenshot}", file=sys.stderr)
                sys.exit(1)
            suffix = os.path.splitext(screenshot)[1] or ".jpg"
            dest = os.path.join(input_dir, f"screenshot{suffix}")
            shutil.copy2(screenshot, dest)
            print(f"Screenshot copied to: {dest}")

    if description:
        desc_path = os.path.join(input_dir, "description.txt")
        with open(desc_path, "w", encoding="utf-8") as f:
            f.write(description)
        print(f"Description saved to: {desc_path}")

    meta_path = os.path.join(project_path, "project_meta.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        meta["status"] = "input_saved"
        if "input_saved" not in meta["steps_completed"]:
            meta["steps_completed"].append("input_saved")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)


def update_status(project_path, step_name, status="completed"):
    meta_path = os.path.join(project_path, "project_meta.json")
    if not os.path.exists(meta_path):
        print(f"Project meta not found: {meta_path}", file=sys.stderr)
        return

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    if status == "completed" and step_name not in meta["steps_completed"]:
        meta["steps_completed"].append(step_name)
    if step_name in meta["steps_remaining"]:
        meta["steps_remaining"].remove(step_name)

    meta["status"] = f"step_{step_name}_{status}"
    meta["updated_at"] = datetime.now().isoformat()

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"Project status updated: {step_name} -> {status}")


def validate_project(project_path):
    if not os.path.exists(project_path):
        print(f"Project not found: {project_path}", file=sys.stderr)
        return False

    meta_path = os.path.join(project_path, "project_meta.json")
    if not os.path.exists(meta_path):
        print(f"Project meta not found", file=sys.stderr)
        return False

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    print(f"Project: {meta['project_name']}")
    print(f"Status: {meta['status']}")
    print(f"Created: {meta['created_at']}")
    print(f"Steps completed: {', '.join(meta['steps_completed']) or 'None'}")
    print(f"Steps remaining: {', '.join(meta['steps_remaining']) or 'None'}")

    input_dir = os.path.join(project_path, "input")
    if os.path.exists(input_dir):
        files = os.listdir(input_dir)
        print(f"Input files: {', '.join(files) or 'None'}")

    output_dir = os.path.join(project_path, "output")
    if os.path.exists(output_dir):
        files = os.listdir(output_dir)
        print(f"Output files: {', '.join(files) or 'None'}")

    return True


def main():
    parser = argparse.ArgumentParser(description="Video Project Manager")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    init_parser = subparsers.add_parser("init", help="Initialize a new project")
    init_parser.add_argument("name", help="Project name")
    init_parser.add_argument("--base-dir", help="Base directory for projects")

    save_parser = subparsers.add_parser("save-input", help="Save input files to project")
    save_parser.add_argument("project_path", help="Path to project directory")
    save_parser.add_argument("--screenshot", help="Path or URL to screenshot")
    save_parser.add_argument("--description", help="Text description")

    status_parser = subparsers.add_parser("update-status", help="Update project step status")
    status_parser.add_argument("project_path", help="Path to project directory")
    status_parser.add_argument("--step", required=True, help="Step name")
    status_parser.add_argument("--status", default="completed", help="Status (default: completed)")

    validate_parser = subparsers.add_parser("validate", help="Validate project structure")
    validate_parser.add_argument("project_path", help="Path to project directory")

    args = parser.parse_args()

    if args.command == "init":
        init_project(args.name, args.base_dir)
    elif args.command == "save-input":
        save_input(args.project_path, args.screenshot, args.description)
    elif args.command == "update-status":
        update_status(args.project_path, args.step, args.status)
    elif args.command == "validate":
        validate_project(args.project_path)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
