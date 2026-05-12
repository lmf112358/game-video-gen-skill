import argparse
import base64
import datetime
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.parse

import requests
from dotenv import load_dotenv

load_dotenv()

VOLC_HOST = "visual.volcengineapi.com"
VOLC_REGION = "cn-north-1"
VOLC_SERVICE = "cv"
VOLC_ENDPOINT = f"https://{VOLC_HOST}"
VOLC_VERSION = "2022-08-31"

DEFAULT_TIMEOUT = int(os.environ.get("JIMENG_TIMEOUT", "600"))


def get_credentials():
    ak = os.environ.get("VOLC_ACCESS_KEY_ID")
    sk = os.environ.get("VOLC_SECRET_ACCESS_KEY")
    if not ak or not sk:
        print("ERROR: VOLC_ACCESS_KEY_ID and VOLC_SECRET_ACCESS_KEY must be set.", file=sys.stderr)
        print("  Set them in .env file or as environment variables.", file=sys.stderr)
        print("  Get credentials from: https://console.volcengine.com/iam/keymanage/", file=sys.stderr)
        sys.exit(1)
    return ak, sk


def _hmac_sha256(key, msg):
    if isinstance(key, str):
        key = key.encode("utf-8")
    if isinstance(msg, str):
        msg = msg.encode("utf-8")
    return hmac.new(key, msg, hashlib.sha256).digest()


def _sha256_hex(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _get_signing_key(secret_key, date_stamp, region, service):
    k_date = _hmac_sha256(secret_key, date_stamp)
    k_region = _hmac_sha256(k_date, region)
    k_service = _hmac_sha256(k_region, service)
    k_signing = _hmac_sha256(k_service, "request")
    return k_signing


def _sign_request(ak, sk, method, path, query_params, body_bytes, headers):
    t = datetime.datetime.utcnow()
    x_date = t.strftime("%Y%m%dT%H%M%SZ")
    short_date = x_date[:8]

    content_type = "application/json"
    payload_hash = _sha256_hex(body_bytes)

    sorted_query = dict(sorted(query_params.items()))
    canonical_querystring = urllib.parse.urlencode(sorted_query, quote_via=urllib.parse.quote)

    signed_headers = ["content-type", "host", "x-content-sha256", "x-date"]
    canonical_headers = (
        f"content-type:{content_type}\n"
        f"host:{VOLC_HOST}\n"
        f"x-content-sha256:{payload_hash}\n"
        f"x-date:{x_date}\n"
    )
    signed_headers_str = ";".join(signed_headers)

    canonical_request = (
        f"{method}\n"
        f"{path}\n"
        f"{canonical_querystring}\n"
        f"{canonical_headers}\n"
        f"{signed_headers_str}\n"
        f"{payload_hash}"
    )

    credential_scope = f"{short_date}/{VOLC_REGION}/{VOLC_SERVICE}/request"
    string_to_sign = (
        f"HMAC-SHA256\n"
        f"{x_date}\n"
        f"{credential_scope}\n"
        f"{_sha256_hex(canonical_request)}"
    )

    signing_key = _get_signing_key(sk, short_date, VOLC_REGION, VOLC_SERVICE)
    signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    authorization = (
        f"HMAC-SHA256 "
        f"Credential={ak}/{credential_scope}, "
        f"SignedHeaders={signed_headers_str}, "
        f"Signature={signature}"
    )

    headers["X-Date"] = x_date
    headers["Authorization"] = authorization
    headers["X-Content-Sha256"] = payload_hash
    headers["Content-Type"] = content_type
    headers["Host"] = VOLC_HOST

    return headers


def _make_signed_request(ak, sk, action, body_dict):
    path = "/"
    query_params = {
        "Action": action,
        "Version": VOLC_VERSION,
    }

    body_bytes = json.dumps(body_dict, ensure_ascii=False).encode("utf-8")
    headers = {}
    headers = _sign_request(ak, sk, "POST", path, query_params, body_bytes, headers)

    url = f"{VOLC_ENDPOINT}?{urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)}"

    resp = requests.post(url, data=body_bytes, headers=headers, timeout=30)
    return resp


def generate_video(request_path, output_path):
    ak, sk = get_credentials()

    with open(request_path, "r", encoding="utf-8") as f:
        req_data = json.load(f)

    prompt = req_data.get("prompt", "")
    images = req_data.get("images", [])
    image_roles = req_data.get("image_roles", [])
    duration = req_data.get("duration", 10)
    seed = req_data.get("seed", -1)
    req_key = req_data.get("req_key", "jimeng_i2v_first_v30")

    if duration <= 5:
        frames = 121
    else:
        frames = 241

    if req_data.get("frames"):
        frames = req_data["frames"]

    body = {
        "req_key": req_key,
        "prompt": prompt,
        "seed": seed,
        "frames": frames,
    }

    if images:
        if images[0].startswith("http://") or images[0].startswith("https://"):
            body["image_urls"] = [images[0]]
        elif images[0].startswith("data:"):
            body["binary_data_base64"] = [images[0].split(",", 1)[1] if "," in images[0] else images[0]]
        else:
            with open(images[0], "rb") as img_file:
                b64 = base64.b64encode(img_file.read()).decode("utf-8")
                body["binary_data_base64"] = [b64]

    mode = "image-to-video" if images else "text-to-video"
    print(f"Submitting video generation task...")
    print(f"  API: Jimeng Visual API (即梦AI)")
    print(f"  req_key: {req_key}")
    print(f"  Duration: ~{frames // 24}s ({frames} frames)")
    print(f"  Mode: {mode}")
    print(f"  Prompt: {prompt[:80]}...")

    try:
        resp = _make_signed_request(ak, sk, "CVSync2AsyncSubmitTask", body)
        data = resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}", file=sys.stderr)
        result = {"status": "FAILED", "error_message": str(e)}
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        result = {"status": "FAILED", "error_message": str(e)}
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        sys.exit(1)

    code = data.get("code")
    if code != 10000:
        message = data.get("message", "Unknown error")
        request_id = data.get("request_id", "")
        print(f"API Error: code={code}, message={message}", file=sys.stderr)
        print(f"  Request ID: {request_id}", file=sys.stderr)

        result = {
            "status": "FAILED",
            "error_code": code,
            "error_message": message,
            "request_id": request_id,
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        sys.exit(1)

    task_id = data.get("data", {}).get("task_id")
    request_id = data.get("request_id", "")

    print(f"Task created successfully!")
    print(f"  Task ID: {task_id}")
    print(f"  Request ID: {request_id}")

    result = {
        "task_id": task_id,
        "status": "SUBMITTED",
        "req_key": req_key,
        "frames": frames,
        "duration_estimate": frames // 24,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "video_url": None,
        "local_path": None,
        "error_message": None,
        "request_id": request_id,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return result


def poll_status(task_id, output_path, interval=10, timeout=None):
    ak, sk = get_credentials()
    timeout = timeout or DEFAULT_TIMEOUT

    req_key = "jimeng_i2v_first_v30"

    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            result = json.load(f)
        req_key = result.get("req_key", req_key)
    else:
        result = {"task_id": task_id, "status": "POLLING"}

    start_time = time.time()
    poll_count = 0

    print(f"Polling task {task_id} (timeout: {timeout}s, interval: {interval}s)...")
    print(f"  NOTE: Video URLs expire after 1 hour. Download immediately after generation!")

    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout:
            print(f"Timeout after {elapsed:.0f}s.", file=sys.stderr)
            result["status"] = "TIMEOUT"
            result["error_message"] = f"Polling timed out after {timeout}s"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            sys.exit(2)

        body = {
            "req_key": req_key,
            "task_id": task_id,
        }

        try:
            resp = _make_signed_request(ak, sk, "CVSync2AsyncGetResult", body)
            data = resp.json()
        except Exception as e:
            print(f"Poll request failed: {e}. Retrying...", file=sys.stderr)
            time.sleep(interval)
            continue

        poll_count += 1
        code = data.get("code")

        if code == 10000:
            status_data = data.get("data", {})
            status = status_data.get("status", "unknown")

            print(f"  [{poll_count}] Status: {status} (elapsed: {elapsed:.0f}s)")

            if status == "done":
                video_url = status_data.get("video_url")
                aigc_tagged = status_data.get("aigc_meta_tagged")

                result.update({
                    "status": "SUCCESS",
                    "video_url": video_url,
                    "aigc_meta_tagged": aigc_tagged,
                    "completed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "error_message": None,
                })

                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)

                print(f"Video generated successfully!")
                print(f"  Video URL: {video_url}")
                print(f"  WARNING: Video URL expires in 1 hour. Download NOW!")
                return result

            elif status == "not_found":
                result.update({
                    "status": "NOT_FOUND",
                    "error_message": "Task not found or expired (12h)",
                })
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"Task not found or expired.", file=sys.stderr)
                return result

            elif status == "expired":
                result.update({
                    "status": "EXPIRED",
                    "error_message": "Task expired, please resubmit",
                })
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"Task expired.", file=sys.stderr)
                return result

        else:
            message = data.get("message", "Unknown error")
            print(f"  [{poll_count}] API error: code={code}, message={message}", file=sys.stderr)

            if code in (50429, 50430, 50500, 50501):
                print(f"  Retriable error, waiting {interval}s...", file=sys.stderr)
                time.sleep(interval)
                continue

            result.update({
                "status": "FAILED",
                "error_code": code,
                "error_message": message,
                "request_id": data.get("request_id", ""),
            })
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"Task failed: [{code}] {message}", file=sys.stderr)
            return result

        current_interval = interval
        if elapsed > 300:
            current_interval = 30
        elif elapsed > 120:
            current_interval = 15

        time.sleep(current_interval)


def main():
    parser = argparse.ArgumentParser(description="Jimeng AI (即梦) Video Generation API Client")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    gen_parser = subparsers.add_parser("generate", help="Submit video generation task")
    gen_parser.add_argument("--request", required=True, help="Path to seedance_request.json")
    gen_parser.add_argument("--output", required=True, help="Path to save video_result.json")

    poll_parser = subparsers.add_parser("poll", help="Poll task status")
    poll_parser.add_argument("--task-id", required=True, help="Task ID to poll")
    poll_parser.add_argument("--output", required=True, help="Path to save/update video_result.json")
    poll_parser.add_argument("--interval", type=int, default=10, help="Polling interval in seconds")
    poll_parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Timeout in seconds")

    args = parser.parse_args()

    if args.command == "generate":
        generate_video(args.request, args.output)
    elif args.command == "poll":
        poll_status(args.task_id, args.output, args.interval, args.timeout)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
