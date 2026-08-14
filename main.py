import argparse
import os
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import requests
from dotenv import load_dotenv


load_dotenv()

USERNAME = os.getenv("GITHUB_USERNAME")
TOKEN = os.getenv("GITHUB_TOKEN")
SUMMARY_TIMEZONE = os.getenv("SUMMARY_TIMEZONE", "Africa/Accra")
GITHUB_COMMIT_SEARCH_URL = "https://api.github.com/search/commits"


def github_headers():
    return {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
    }


def search_commits(query, **params):
    """Run a GitHub commit search and return its JSON response."""
    response = requests.get(
        GITHUB_COMMIT_SEARCH_URL,
        headers=github_headers(),
        params={"q": query, "per_page": 100, **params},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


def get_today_commit_count():
    today = datetime.now(timezone.utc).date()
    data = search_commits(f"author:{USERNAME} committer-date:{today.isoformat()}")
    return data.get("total_count", 0)


def get_commit_count_for_day(day):
    data = search_commits(f"author:{USERNAME} committer-date:{day.isoformat()}")
    return data.get("total_count", 0)


def get_daily_summary(summary_date, local_timezone):
    """Return commit count, first/last commit times, and the active daily streak."""
    query = f"author:{USERNAME} committer-date:{summary_date.isoformat()}"
    oldest = search_commits(query, sort="committer-date", order="asc")
    newest = search_commits(query, sort="committer-date", order="desc")
    commit_count = oldest.get("total_count", 0)

    first_time = last_time = None
    if commit_count:
        first_time = parse_commit_time(oldest["items"][0], local_timezone)
        last_time = parse_commit_time(newest["items"][0], local_timezone)

    streak = get_current_streak(summary_date)
    return commit_count, first_time, last_time, streak


def parse_commit_time(item, local_timezone):
    timestamp = item["commit"]["committer"]["date"]
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).astimezone(local_timezone)


def get_current_streak(today):
    """Count consecutive UTC calendar days with at least one commit, ending today."""
    streak = 0
    day = today
    while get_commit_count_for_day(day) > 0:
        streak += 1
        day -= timedelta(days=1)
    return streak


def format_time(timestamp):
    return timestamp.strftime("%I:%M %p").lstrip("0")


def format_daily_summary(summary_date, local_timezone):
    commit_count, first_time, last_time, streak = get_daily_summary(
        summary_date, local_timezone
    )
    lines = ["📊 Daily GitHub Summary", "", f"Commits: {commit_count}"]
    if commit_count:
        lines.extend(
            [
                f"First commit: {format_time(first_time)}",
                f"Last commit: {format_time(last_time)}",
            ]
        )
    else:
        lines.append("No commits today.")
    lines.extend(["", f"🔥 Streak: {streak} day{'s' if streak != 1 else ''}"])
    return "\n".join(lines)


def send_telegram_message(message):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    response = requests.post(url, data={"chat_id": chat_id, "text": message}, timeout=20)
    response.raise_for_status()
    print("Telegram message sent!")


def send_commit_reminder():
    try:
        commit_count = get_today_commit_count()
        if commit_count > 0:
            print(f"You have made {commit_count} commits today!")
            send_telegram_message(
                f"✅ GitHub Update\n\nYou have made {commit_count} commits today. 🔥"
            )
        else:
            print("You have not committed today.")
            send_telegram_message(
                "⚠️ You haven't committed to GitHub today!\n\nGo commit something. 💻🔥"
            )
    except requests.RequestException as error:
        print(f"Failed to check commits or send reminder: {error}")
        raise


def send_daily_summary():
    try:
        local_timezone = ZoneInfo(SUMMARY_TIMEZONE)
        summary_date = datetime.now(local_timezone).date()
        message = format_daily_summary(summary_date, local_timezone)
        send_telegram_message(message)
    except (requests.RequestException, ValueError) as error:
        print(f"Failed to create or send daily summary: {error}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send GitHub commit notifications.")
    parser.add_argument("--summary", action="store_true", help="Send the daily summary.")
    args = parser.parse_args()

    if args.summary:
        send_daily_summary()
    else:
        send_commit_reminder()
