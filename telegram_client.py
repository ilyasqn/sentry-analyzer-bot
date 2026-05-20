import httpx
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

BASE = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def send_analysis(context: dict, analysis: str) -> None:
    text = (
        f"🤖 <b>AI Analysis</b> — <a href='{context['url']}'>{context['title']}</a>\n\n"
        f"{analysis}\n\n"
        f"<i>Seen {context['times_seen']} times · {context['project']}</i>"
    )
    httpx.post(
        f"{BASE}/sendMessage",
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        },
        timeout=10,
    ).raise_for_status()
