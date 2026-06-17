import os
from datetime import datetime, timezone


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
    print(payload)


if __name__ == "__main__":
    main()