# 🚀 GitHub Commit Reminder

A simple personal accountability tool that checks your GitHub commit activity and sends a reminder or progress update to you through Telegram.

The project runs automatically using **GitHub Actions every 30 minutes**, so your computer does not need to be running.

---

## 📌 Overview

The idea behind this project is simple:

> **If I haven't committed anything today, remind me to code.**

Every 30 minutes, GitHub Actions runs the Python application. The application checks GitHub for the number of commits made during the current day and sends a message to Telegram.

### ✅ When commits have been made

```text
✅ GitHub Update

You have made 3 commits today. 🔥
```

### ⚠️ When no commits have been made

```text
⚠️ You haven't committed to GitHub today!

Go commit something. 💻🔥
```

---

## ✨ Features

- ⏰ Runs automatically every 30 minutes
- 🔍 Checks GitHub commit activity
- 📊 Counts commits made during the current day
- 📱 Sends notifications through Telegram
- 🔐 Uses GitHub Secrets to protect sensitive credentials
- ☁️ Runs entirely through GitHub Actions
- 💻 Does not require your computer to be running
- 🐍 Built with Python

---

## 🛠️ Technologies

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| GitHub REST API | Retrieves commit information |
| Telegram Bot API | Sends notifications |
| GitHub Actions | Automates execution |
| Requests | Makes HTTP requests |
| python-dotenv | Loads environment variables locally |

---

## 📂 Project Structure

```text
github_commit_reminder/
│
├── main.py
├── requirements.txt
├── .gitignore
├── README.md
│
└── .github/
    └── workflows/
        └── render.yml
```

### `main.py`

Contains the main application logic for:

- Connecting to the GitHub API
- Counting today's commits
- Sending Telegram messages

### `requirements.txt`

Contains the Python dependencies required by the project.

### `.github/workflows/render.yml`

Contains the GitHub Actions workflow responsible for running the application automatically every 30 minutes.

> The workflow is named `render.yml` because that was the filename used when setting up the project. It is a GitHub Actions workflow and is **not related to Render hosting**.

---

## ⚙️ How It Works

The application follows this process:

```text
                    GitHub Actions
                          │
                          │ Every 30 minutes
                          ▼
                     main.py runs
                          │
                          ▼
                   GitHub REST API
                          │
                          ▼
                Count today's commits
                       /       \
                      /         \
                     ▼           ▼
              0 commits       1+ commits
                  │                │
                  ▼                ▼
            ⚠️ Reminder       ✅ Progress
                  │                │
                  └───────┬────────┘
                          ▼
                      Telegram
                          │
                          ▼
                    📱 Notification
```

---

## 🔑 Environment Variables

The application requires four environment variables:

```env
GITHUB_USERNAME=your_github_username
GITHUB_TOKEN=your_github_token

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

### GitHub Variables

#### `GITHUB_USERNAME`

The GitHub username whose commits should be monitored.

#### `GITHUB_TOKEN`

A GitHub Personal Access Token used to authenticate requests to the GitHub API.

### Telegram Variables

#### `TELEGRAM_BOT_TOKEN`

The token provided by Telegram when creating the bot.

#### `TELEGRAM_CHAT_ID`

The Telegram chat ID where the bot should send notifications.

---

## 🔐 Security

**Never commit your tokens or credentials to GitHub.**

For local development, create a `.env` file:

```env
GITHUB_USERNAME=your_username
GITHUB_TOKEN=your_token
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

Make sure `.env` is included in `.gitignore`:

```gitignore
.env
__pycache__/
.venv/
```

When running through GitHub Actions, the credentials are stored as repository secrets.

The workflow passes them to the Python application as environment variables.

Example:

```yaml
env:
  GITHUB_USERNAME: ${{ secrets.MY_GITHUB_USERNAME }}
  GITHUB_TOKEN: ${{ secrets.MY_GITHUB_TOKEN }}
  TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
  TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
```

---

## 📦 Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/Rolie-CODE/github_commit_reminder.git
```

### 2. Navigate into the project

```bash
cd github_commit_reminder
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Create your `.env` file

```env
GITHUB_USERNAME=your_username
GITHUB_TOKEN=your_token
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 7. Run the application

```bash
python main.py
```

---

## 🤖 GitHub Actions

The project uses GitHub Actions to automatically execute the application.

The workflow is scheduled using:

```yaml
on:
  schedule:
    - cron: "*/30 * * * *"
```

This schedules the workflow to run approximately every 30 minutes.

A manual trigger is also configured:

```yaml
workflow_dispatch:
```

This allows the workflow to be tested manually.

### Manual Run

Go to:

```text
GitHub Repository
        ↓
     Actions
        ↓
GitHub Commit Reminder
        ↓
 Run workflow
```

---

## 📱 Telegram Notifications

The bot currently sends two types of notifications.

### When commits exist

```text
✅ GitHub Update

You have made X commits today. 🔥
```

### When no commits exist

```text
⚠️ You haven't committed to GitHub today!

Go commit something. 💻🔥
```

---

## 🧪 Testing

The application can be tested locally:

```bash
python main.py
```

It can also be tested through GitHub Actions.

Go to:

```text
Repository → Actions → GitHub Commit Reminder → Run workflow
```

### Successful workflow

A successful run should end with:

```text
Process completed with exit code 0
```

### Example: commits detected

```text
✅ You have made 3 commits today!
📱 Telegram reminder sent!
```

### Example: no commits detected

```text
❌ You haven't committed today.
📱 Telegram reminder sent!
```

---

## 🚧 Current Limitations

This is **Version 1**, so the project is intentionally simple.

Current limitations include:

- 👤 Designed primarily for personal use
- 🔑 Requires manually configured GitHub credentials
- 📱 Supports one Telegram destination
- 🗄️ No database
- 🔐 No GitHub OAuth
- ⚙️ No user configuration system
- 🔥 No commit streak tracking
- 📊 No dashboard
- 🤖 No Telegram commands
- 👥 No multi-user support
- ⏰ Reminder interval is currently fixed at 30 minutes

GitHub Actions scheduling can also occasionally experience delays, meaning a scheduled workflow may not execute exactly at the 30-minute mark.

---

## 🔮 Future Improvements

The project may eventually evolve from a personal script into a service that other developers can use.

### 👥 Multi-User Support

Allow multiple developers to connect their own GitHub and Telegram accounts.

### 🔐 GitHub OAuth

Replace manually configured Personal Access Tokens with GitHub OAuth.

### 🤖 Telegram Commands

Allow users to control the bot directly through Telegram.

Potential commands:

```text
/start
/stop
/status
/commits
/streak
/settings
```

### ⏰ Custom Reminder Intervals

Allow users to choose their preferred reminder frequency:

```text
15 minutes
30 minutes
1 hour
2 hours
```

### 🔥 Commit Streaks

Track consecutive days of GitHub activity.

Example:

```text
🔥 14 Day Commit Streak!

Keep going! 🚀
```

### 📊 Weekly Reports

Send users a weekly GitHub activity summary:

```text
📊 Weekly GitHub Summary

Commits: 27
Active Days: 6/7
Longest Streak: 6 days

Keep coding! 🚀
```

### 🗄️ Database

Introduce a database to store:

- Users
- GitHub accounts
- Telegram accounts
- Reminder preferences
- Commit history
- Streaks

### 🌐 Backend API

Build a dedicated backend using **FastAPI** to handle authentication, users, preferences, and integrations.

---

## 🎯 Project Goal

The long-term goal is to turn this simple personal automation into a **GitHub accountability bot for developers**.

The current V1 focuses on proving the core idea:

```text
Check GitHub
      ↓
Count commits
      ↓
Send notification
```

The project starts as a personal productivity tool and can eventually evolve into a multi-user developer accountability platform.

---

## 👨🏾‍💻 Author

**Roland Yeboah**

Built as a personal automation project to encourage consistent GitHub activity and maintain a regular coding habit.

---

## 📄 License

This project is currently intended for personal use.
