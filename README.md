# Sentry Analyzer Bot

Receives Sentry webhooks → fetches issue details → analyzes with Gemini → posts explanation to Telegram.

## Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Fill in .env values
```

## Run

```bash
uvicorn main:app --host 0.0.0.0 --port 8001
```

For local testing use [ngrok](https://ngrok.com/):
```bash
ngrok http 8001
```

## Sentry Webhook Config

1. Go to **Settings → Integrations → Webhooks** in your Sentry org
   OR create an **Internal Integration** (recommended — gives you an auth token + webhook)
2. Set the webhook URL to: `https://your-domain.com/webhook/sentry`
3. Subscribe to **Issue** events (`issue.created`, `issue.assigned`, etc.)
4. Copy the signing secret → set `WEBHOOK_SECRET` in `.env`

## Example Telegram output

```
🤖 AI Analysis — DataError: value too long for type character varying(255)

🔍 What happened: A string value exceeded the 255-character limit of a database column.
💡 Why: The `create` method in `posts/serializers.py` is saving user input directly without validating its length before writing to the DB.
🛠 Fix: Add `max_length=255` validation on the serializer field, or increase the column size via a migration if longer values are valid.

Seen 3 times · superapp-backend
```

## Getting API Keys

- **Sentry token**: Sentry → Settings → Developer Settings → Internal Integrations → New Integration
- **Gemini**: https://aistudio.google.com/app/apikey (free tier: 15 req/min)
- **Telegram bot**: @BotFather → /newbot → add bot to your group → get chat ID via @userinfobot
