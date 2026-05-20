import hmac
import hashlib
import logging
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks

from config import WEBHOOK_SECRET
from sentry_client import build_context
from gemini_client import analyze
from telegram_client import send_analysis

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = FastAPI()


def verify_sentry_signature(body: bytes, signature: str) -> bool:
    if not WEBHOOK_SECRET:
        return True
    expected = hmac.new(WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def process_issue(issue_id: str) -> None:
    try:
        log.info(f"Processing Sentry issue {issue_id}")
        context = build_context(issue_id)
        analysis = analyze(context)
        send_analysis(context, analysis)
        log.info(f"Analysis sent for issue {issue_id}")
    except Exception as e:
        log.error(f"Failed to process issue {issue_id}: {e}")


@app.post("/webhook/sentry")
async def sentry_webhook(request: Request, background_tasks: BackgroundTasks):
    body = await request.body()

    sig = request.headers.get("sentry-hook-signature", "")
    if WEBHOOK_SECRET and not verify_sentry_signature(body, sig):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json() if not body else __import__("json").loads(body)

    action = payload.get("action")
    if action not in ("created", "triggered"):
        return {"status": "ignored", "action": action}

    issue = payload.get("data", {}).get("issue", {})
    issue_id = issue.get("id")
    if not issue_id:
        raise HTTPException(status_code=400, detail="No issue ID in payload")

    background_tasks.add_task(process_issue, issue_id)
    return {"status": "ok", "issue_id": issue_id}


@app.get("/health")
def health():
    return {"status": "ok"}
