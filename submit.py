import os
from datetime import datetime, timezone
import json
import hmac
import hashlib
import requests



def build_payload():
    repository = os.getenv("GITHUB_REPOSITORY")
    run_id = os.getenv("GITHUB_RUN_ID")

    timestamp = (
    datetime.now(timezone.utc)
    .isoformat(timespec="milliseconds")
    .replace("+00:00", "Z")
    )

    return {
        "action_run_link": f"https://github.com/{repository}/actions/runs/{run_id}",
        "email": os.getenv("EMAIL"),
        "name": os.getenv("NAME"),
        "repository_link": f"https://github.com/{repository}",
        "resume_link": os.getenv("RESUME_LINK"),
        "timestamp": timestamp,
    }


def main():
    payload = build_payload()
    canonical_json = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":")
    )
    signature = sign_payload(canonical_json)

    print("Payload:")
    print(canonical_json)

    print("\nSignature:")
    print(signature)
    result = submit_payload(canonical_json, signature)

    print("Receipt:")
    print(result["receipt"])

def sign_payload(payload_json):
    secret = os.getenv("B12_SECRET")
    
    if not secret:
        raise ValueError("B12_SECRET environment variable is missing")


    signature = hmac.new(
        secret.encode("utf-8"),
        payload_json.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    return signature

def submit_payload(payload_json, signature):
    response = requests.post(
        "https://b12.io/apply/submission",
        data=payload_json.encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Signature-256": f"sha256={signature}",
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()

if __name__ == "__main__":
    main()