import os
from dotenv import load_dotenv

load_dotenv()

SENTRY_AUTH_TOKEN = os.environ.get("SENTRY_AUTH_TOKEN")
SENTRY_ORG_SLUG = os.environ.get("SENTRY_ORG_SLUG")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")
