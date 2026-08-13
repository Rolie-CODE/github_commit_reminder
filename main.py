import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("GITHUB_USERNAME")
token = os.getenv("GITHUB_TOKEN")


def get_today_commit_count():

    url = "https://api.github.com/search/commits"

    today = datetime.now(timezone.utc).date()

    query = f"author:{username} committer-date:{today}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    params = {
        "q": query,
        "per_page": 100
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        print("Failed to get commits")
        print(response.text)
        return 0

    data = response.json()

    commit_count = data.get("total_count", 0)

    return commit_count


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


commit_count = get_today_commit_count()


if commit_count > 0:

    print(f"✅ You have made {commit_count} commits today!")

    send_telegram_message(
        f"✅ GitHub Update\n\n"
        f"You have made {commit_count} commits today. 🔥"
    )

else:

    print("❌ You haven't committed today.")

    send_telegram_message(
        "⚠️ You haven't committed to GitHub today!\n\n"
        "Go commit something. 💻🔥"
    )