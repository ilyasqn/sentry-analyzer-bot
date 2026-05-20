import os
from dotenv import load_dotenv

load_dotenv()

SENTRY_AUTH_TOKEN = os.environ["SENTRY_AUTH_TOKEN"]
SENTRY_ORG_SLUG = os.environ["SENTRY_ORG_SLUG"]

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")
