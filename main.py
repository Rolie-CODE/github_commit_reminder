import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("GITHUB_USERNAME")
token = os.getenv("GITHUB_TOKEN")


def has_committed_today():
    url = f"https://api.github.com/users/{username}/events"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to get GitHub activity")
        return False

    events = response.json()

    today = datetime.now(timezone.utc).date()

    for event in events:
        if event["type"] == "PushEvent":
            event_date = datetime.fromisoformat(
                event["created_at"].replace("Z", "+00:00")
            ).date()

            if event_date == today:
                return True

    return False


def send_telegram_message(message):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": message
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("📱 Telegram reminder sent!")
    else:
        print("❌ Failed to send Telegram message")
        print(response.text)


if has_committed_today():
    print("✅ You have committed today!")
else:
    print("❌ You have NOT committed today!")

    send_telegram_message(
        "⚠️ You haven't committed to GitHub today!\n\n"
        "Go commit something. 💻🔥"
    )