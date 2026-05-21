import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-pro")

PROMPT_TEMPLATE = """You are a senior backend developer. Analyze this Sentry error and explain it clearly.

Project: {project}
Error: {title}
Location: {culprit}
Seen: {times_seen} times (first: {first_seen}, last: {last_seen})

Stacktrace:
{stacktrace}

Reply in this exact format (short and clear, no markdown headers):

🔍 What happened: <one sentence explaining the error>
💡 Why: <root cause in 1-2 sentences>
🛠 Fix: <concrete fix suggestion in 1-2 sentences>"""


def analyze(context: dict) -> str:
    prompt = PROMPT_TEMPLATE.format(**context)
    response = model.generate_content(prompt)
    return response.text.strip()
