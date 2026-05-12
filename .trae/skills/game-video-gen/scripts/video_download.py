import argparse
import os
import sys
import time

import requests


MAX_RETRIES = 3
RETRY_DELAY_SECONDS = [2, 5, 15]


def download_video(url, output_path, chunk_size=8192):
    if not url:
        print("ERROR: No video URL provided", file=sys.stderr)
        sys.exit(1)

    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"Downloading video from: {url}")
        print(f"Saving to: {output_path}")
        if attempt > 1:
            print(f"Retry attempt {attempt}/{MAX_RETRIES}...")

        try:
            resp = requests.get(url, stream=True, timeout=120)
            resp.raise_for_status()

            total_size = int(resp.headers.get("content-length", 0))
            downloaded = 0

            with open(output_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = downloaded / total_size * 100
                            print(f"\r  Progress: {progress:.1f}% ({downloaded}/{total_size} bytes)", end="", flush=True)

            print(f"\n  Download complete: {downloaded} bytes")

            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"  File saved: {output_path} ({file_size} bytes)")
                return output_path
            else:
                print("ERROR: File was not saved", file=sys.stderr)
                sys.exit(1)

        except requests.exceptions.RequestException as e:
            last_error = e
            print(f"ERROR: Download failed (attempt {attempt}/{MAX_RETRIES}): {e}", file=sys.stderr)
            if os.path.exists(output_path):
                os.remove(output_path)

            if attempt < MAX_RETRIES:
                delay = RETRY_DELAY_SECONDS[min(attempt - 1, len(RETRY_DELAY_SECONDS) - 1)]
                print(f"Retrying in {delay} seconds...", file=sys.stderr)
                time.sleep(delay)

    print(f"ERROR: All {MAX_RETRIES} download attempts failed. Last error: {last_error}", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Video Downloader")
    parser.add_argument("--url", required=True, help="Video URL to download")
    parser.add_argument("--output", "-o", required=True, help="Output file path")

    args = parser.parse_args()

    download_video(args.url, args.output)


if __name__ == "__main__":
    main()
