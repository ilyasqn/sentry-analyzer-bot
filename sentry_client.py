import httpx
from config import SENTRY_AUTH_TOKEN, SENTRY_ORG_SLUG

BASE = "https://sentry.io/api/0"
HEADERS = {"Authorization": f"Bearer {SENTRY_AUTH_TOKEN}"}


def get_issue(issue_id: str) -> dict:
    r = httpx.get(f"{BASE}/issues/{issue_id}/", headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()


def get_latest_event(issue_id: str) -> dict:
    r = httpx.get(f"{BASE}/issues/{issue_id}/events/latest/", headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()


def build_context(issue_id: str) -> dict:
    issue = get_issue(issue_id)
    event = get_latest_event(issue_id)

    stacktrace = ""
    for entry in event.get("entries", []):
        if entry["type"] == "exception":
            for exc in entry["data"].get("values", []):
                stacktrace += f"Exception: {exc.get('type')}: {exc.get('value')}\n"
                frames = exc.get("stacktrace", {}).get("frames", [])
                for frame in frames[-5:]:  # last 5 frames
                    stacktrace += (
                        f"  File: {frame.get('filename')} line {frame.get('lineno')} "
                        f"in {frame.get('function')}\n"
                    )
                    if frame.get("context_line"):
                        stacktrace += f"    {frame['context_line'].strip()}\n"

    return {
        "title": issue.get("title", ""),
        "culprit": issue.get("culprit", ""),
        "level": issue.get("level", ""),
        "times_seen": issue.get("times_seen", 0),
        "first_seen": issue.get("firstSeen", ""),
        "last_seen": issue.get("lastSeen", ""),
        "project": issue.get("project", {}).get("name", ""),
        "stacktrace": stacktrace,
        "url": f"https://bepro-2v.sentry.io/issues/{issue_id}/",
    }
