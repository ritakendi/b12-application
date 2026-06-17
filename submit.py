import os
from datetime import datetime, timezone
import json
import hmac
import hashlib


def build_payload():
    repository = os.getenv("GITHUB_REPOSITORY")
    run_id = os.getenv("GITHUB_RUN_ID")

    return {
        "action_run_link": f"https://github.com/{repository}/actions/runs/{run_id}",
        "email": os.getenv("EMAIL"),
        "name": os.getenv("NAME"),
        "repository_link": f"https://github.com/{repository}",
        "resume_link": os.getenv("RESUME_LINK"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
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

if __name__ == "__main__":
    main()